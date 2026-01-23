"""
Generate mock results to populate the downloads folder

Can be used standalone or imported by test_gui_mock.py to generate 
mock results for uploaded posters with specific job IDs.
"""

import csv
import json
import random
from pathlib import Path

# Define the downloads directory
downloads_dir = Path(__file__).parent / "downloads"


def generate_grades_for_approach(approach: str):
    """Generate grades based on evaluation approach"""
    score_multipliers = {
        'direct': 0.85,
        'reasoning': 0.82,
        'deep_analysis': 0.90,
        'strict': 0.75
    }
    
    multiplier = score_multipliers.get(approach, 0.80)
    
    return {
        "Q1": int(8 * multiplier),
        "Q2": int(8 * multiplier),
        "Q3": int(6 * multiplier),
        "Q4": int(6 * multiplier),
        "Q5": int(8 * multiplier),
        "Q6": int(7 * multiplier),
        "Q7": int(7 * multiplier),
        "Q8": int(6 * multiplier),
        "Q9": int(5 * multiplier),
        "Q10": int(4 * multiplier),
        "Q11": int(5 * multiplier),
        "Q12": int(9 * multiplier),
        "Q13": int(5 * multiplier),
        "Q14": int(5 * multiplier),
        "Q15": int(7 * multiplier),
        "Q16": int(8 * multiplier),
    }


def calculate_final_grade(grades):
    """Calculate final grade from individual question scores"""
    total = sum(grades.values())
    return round((total / 160) * 100, 1)


def generate_poster_data(poster_file: str):
    """Generate poster metadata"""
    return {
        "poster_file": poster_file,
        "project_number": f"23-1-1-{hash(poster_file) % 9000 + 1000}",
        "advisor_name": "Dr. Mock Advisor",
        "presenter_names": "Mock Student A, Mock Student B",
    }


def populate_folder(folder_path, approach, poster_files=None):
    """Populate a single download folder with mock results
    
    Args:
        folder_path: Path to folder for this job
        approach: Evaluation approach (direct, reasoning, deep_analysis, strict)
        poster_files: List of poster filenames (if None, uses sample data)
    """
    folder_path.mkdir(parents=True, exist_ok=True)
    
    results_csv = folder_path / "results_master.csv"
    run_log_jsonl = folder_path / "run_log.jsonl"
    
    # Use provided poster files or sample data
    if poster_files:
        sample_data = [{"poster_file": f} for f in poster_files]
    else:
        sample_data = [
            {"poster_file": "2729.jpeg"},
            {"poster_file": "2732.jpeg"},
            {"poster_file": "2745.jpeg"},
        ]
    
    # Create CSV with results
    with open(results_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'poster_file', 'project_number', 'advisor_name', 'presenter_names',
            'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10',
            'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'final_grade',
            'poster_summary', 'evaluation_summary', 'overall_opinion'
        ])
        writer.writeheader()
        
        for poster_entry in sample_data:
            poster_file = poster_entry['poster_file']
            poster_data = generate_poster_data(poster_file)
            grades = generate_grades_for_approach(approach)
            final_grade = calculate_final_grade(grades)
            
            row = {
                'poster_file': poster_data['poster_file'],
                'project_number': poster_data['project_number'],
                'advisor_name': poster_data['advisor_name'],
                'presenter_names': poster_data['presenter_names'],
                **grades,
                'final_grade': final_grade,
                'poster_summary': f"Mock summary for {poster_file} using {approach}",
                'evaluation_summary': f"Mock evaluation of poster using {approach} approach",
                'overall_opinion': f"Well-structured poster with good content (evaluated via {approach})",
            }
            writer.writerow(row)
    
    # Create JSONL with processing logs
    with open(run_log_jsonl, 'w') as f:
        for i, poster_entry in enumerate(sample_data):
            poster_file = poster_entry['poster_file']
            grades = generate_grades_for_approach(approach)
            final_grade = calculate_final_grade(grades)
            
            log_entry = {
                "file": poster_file,
                "status": "ok",
                "grade": final_grade,
                "duration_ms": random.randint(1000, 5000),
                "error": None,
                "approach": approach,
                "timestamp": f"2024-01-{i+1:02d}T{random.randint(10, 23):02d}:{random.randint(0, 59):02d}:00Z"
            }
            f.write(json.dumps(log_entry) + '\n')
    
    print(f"  ✓ Generated {approach} results in {folder_path.name}")
