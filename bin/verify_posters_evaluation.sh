#!/bin/bash

# Configuration
PORT=8090
ID=$(date +%s)
SERVER_SCRIPT="run.py"
UPLOAD_ENDPOINT="http://localhost:$PORT/upload/batch"
HEALTH_ENDPOINT="http://localhost:$PORT/health"
JOBS_ENDPOINT_TEMPLATE="http://localhost:$PORT/jobs"
OUTPUT_FILE="bin/${ID}_posters_evaluation_results.txt"

# Approaches
STRATEGIES=("direct" "reasoning" "deep_analysis" "strict")
declare -A LABELS
LABELS=( ["strict"]="Strict" ["direct"]="Direct" ["reasoning"]="Reasoning" ["deep_analysis"]="Deep Analysis" )

# Cleanup helper function
cleanup() {
    # Kill server process by port (Windows specific adaptation)
    netstat -ano | grep ":$PORT" | awk '{print $5}' | sort -u | xargs -I {} taskkill //F //PID {} > /dev/null 2>&1
    
    if [ -n "$SERVER_PID" ]; then
        kill "$SERVER_PID" 2>/dev/null
        wait "$SERVER_PID" 2>/dev/null
    fi

    # Remove temporary server log
    rm -f bin/server_log.txt
}

# Trap exit/interrupt signals to ensure cleanup runs
trap cleanup EXIT INT TERM

# Construct CURL file args dynamically from docs/posters
CURL_ARGS=""
for FILEPATH in docs/posters/*.jpeg; do
    if [ -f "$FILEPATH" ]; then
        CURL_ARGS="$CURL_ARGS -F files=@$FILEPATH;type=image/jpeg"
    fi
done

if [ -z "$CURL_ARGS" ]; then
    echo "Error: No poster images found in docs/posters/"
    exit 1
fi

# Helper to parse JSON
get_json_value() {
    echo "$1" | python -c "import sys, json; print(json.load(sys.stdin).get('$2', ''))" 2>/dev/null
}

for strategy in "${STRATEGIES[@]}"; do
    label="${LABELS[$strategy]}"
    echo "=== Used Approach: $label ==="

    export EVALUATION_APPROACH="$strategy"
    export APP_PORT="$PORT"
    export APP_RELOAD="false"
    
    echo "Starting server..."
    python "$SERVER_SCRIPT" > bin/server_log.txt 2>&1 &
    SERVER_PID=$!
    
    # Wait for server
    SERVER_UP=0
    for i in {1..30}; do
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_ENDPOINT")
        if [ "$HTTP_CODE" == "200" ]; then
            SERVER_UP=1
            break
        fi
        sleep 1
    done
    
    if [ "$SERVER_UP" -eq 0 ]; then
        echo "Server failed to start."
        cat bin/server_log.txt
        kill "$SERVER_PID" 2>/dev/null
        continue
    fi
    
    echo "Server UP. Uploading batch..."
    
    # Execute batch upload
    RESPONSE=$(curl -s -X POST "$UPLOAD_ENDPOINT" \
      -H "accept: application/json" \
      -H "Content-Type: multipart/form-data" \
      $CURL_ARGS)
      
    JOB_ID=$(get_json_value "$RESPONSE" "job_id")
    
    if [ -z "$JOB_ID" ]; then
        echo "Upload failed: $RESPONSE"
    else
        echo "Job started: $JOB_ID"
        
        while true; do
            sleep 2
            # Use curl directly
            JOB_STATUS_JSON=$(curl -s "$JOBS_ENDPOINT_TEMPLATE/$JOB_ID")
            STATUS=$(get_json_value "$JOB_STATUS_JSON" "status")
            
            if [ "$STATUS" == "completed" ]; then
                echo "Job completed!"
                echo "Posters Evaluation Results (Rankings) - $label" >> "$OUTPUT_FILE"
                
                # Save raw JSON for debugging
                echo "$JOB_STATUS_JSON" > "bin/${ID}_json_output.json"
                
                # Generate Report
                echo "$JOB_STATUS_JSON" | python bin/verify_report.py --strategy "$strategy" | tee -a "$OUTPUT_FILE"

                # Print final message
                echo "Posters evaluation complete. Results saved to $OUTPUT_FILE"
                break
            elif [ "$STATUS" == "failed" ]; then
                echo "Job failed!"
                # Extract the most descriptive error available (prioritize detailed logs over generic lists)
                ERROR=$(echo "$JOB_STATUS_JSON" | python bin/verify_error.py 2>/dev/null)
                echo "Error: $ERROR"
                break
            fi
        done
        echo ""
    fi
done
