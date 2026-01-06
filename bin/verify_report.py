import sys
import json
import argparse

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

    table_width = 63

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
    print("Expert Rank vs Approach Rank")
    print(f"{'-' * table_width}")
    print(f"| {'Poster ID':^10} | {'Grade':^10} | {'Approach Rank':^15} | {'Expert Rank':^15} |")
    print(f"{'-' * table_width}")

    # Print Rows
    for i, res in enumerate(results, 1):
        fname = res.get("poster_file", "")
        # Extract ID from filename (assuming id.jpeg)
        pid = fname.split(".")[0] if fname else "N/A"
        grade = res.get("final_grade", "N/A")
        expert = EXPERT_RANKS.get(pid, "N/A")
        
        print(f"| {pid:^10} | {grade:^10} | {i:^15} | {expert:^15} |")
    
    # Print Footer
    print(f"{'-' * table_width}")

if __name__ == "__main__":
    main()
