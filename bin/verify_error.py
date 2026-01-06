import sys
import json
import io

# Set stdout to UTF-8 for Windows consistency
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_error_message(data):
    """Extract the most relevant error message from the JSON response data."""
    # Priority 1: Check processing_logs for detailed errors from specific poster failures
    if data.get('processing_logs'):
        failed_logs = [
            log.get('error') 
            for log in data.get('processing_logs', []) 
            if log.get('status') == 'failed' and log.get('error')
        ]
        if failed_logs:
            # Join multiple errors if present, but usually one is enough for summary
            return failed_logs[0]

    # Priority 2: Check the general errors list
    errors = data.get('errors')
    if errors and isinstance(errors, list):
        return '; '.join(filter(None, errors))

    # Priority 3: Check the top-level error field
    return data.get('error')

def main():
    try:
        # Read JSON from stdin
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Invalid JSON input")
        return
    except Exception as e:
        print(f"Error reading input: {e}")
        return

    error_msg = extract_error_message(data)
    
    if error_msg:
        # Clean up whitespace and print
        print(str(error_msg).strip())
    else:
        print("Unknown error")

if __name__ == "__main__":
    main()
