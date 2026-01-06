import io
import sys
import json
import argparse

# Set stdout to UTF-8 for Windows consistency
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Poster ID -> Expert Rank Mapping
EXPERT_RANKS = {
    "2850": 1,
    "2849": 2,
    "2826": 3,
    "2745": 3,
    "2902": 4,
    "2862": 5,
    "2916": 6,
    "2729": 7,
    "2732": 8,
    "2908": 9,
    "2883": 10
}

def main():
    parser = argparse.ArgumentParser(description="Generate verification report.")
    parser.add_argument("--strategy", required=True, help="Evaluation strategy name")
    args = parser.parse_args()

    cell_width = 76

    try:
        # Read JSON from stdin
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    results = data.get("results", [])
    
    # Sort by grade descending
    results.sort(key=lambda x: x.get("final_grade", 0), reverse=True)

    # Print Report Header
    print("")
    print("Approach Rank vs Expert Rank")
    print(f"{'-' * cell_width}")
    print(f"| {'Poster ID':^10} | {'Grade':^10} | {'Approach Rank':^15} | {'Expert Rank':^15} | {'Match':^10} |")
    print(f"{'-' * cell_width}")

    # Print Rows
    for i, res in enumerate(results, 1):
        fname = res.get("poster_file", "")
        pid = fname.split(".")[0] if fname else "N/A"
        grade = res.get("final_grade", "N/A")
        expert = EXPERT_RANKS.get(pid, "N/A")
        
        match_status = "YES" if i == expert else "NO"
        print(f"| {pid:^10} | {grade:^10} | {i:^15} | {expert:^15} | {match_status:^10} |")
    
    # Print Footer
    print(f"{'-' * cell_width}")

if __name__ == "__main__":
    main()
