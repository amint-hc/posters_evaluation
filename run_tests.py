#!/usr/bin/env python3
"""
Test runner script for the Poster Evaluation API.
"""

import subprocess
import sys
import os

def run_tests():
    """Run the test suite."""
    print("Starting Poster Evaluation API Test Suite...")
    print("=" * 50)
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Run tests without coverage (pytest-cov not installed)
    cmd = [
        "python", "-m", "pytest",
        "-v"
    ]
    
    try:
        result = subprocess.run(cmd, check=False)
        
        if result.returncode == 0:
            print("\n" + "=" * 50)
            print("ALL TESTS PASSED!")
        else:
            print("\n" + "=" * 50)
            print("SOME TESTS FAILED!")
            return False
            
    except Exception as e:
        print(f"Error running tests: {e}")
        return False
    
    return True

def run_specific_test(test_pattern):
    """Run specific tests matching pattern."""
    cmd = [
        "python", "-m", "pytest",
        "-v",
        "-k", test_pattern
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test pattern
        test_pattern = sys.argv[1]
        print(f"Running tests matching: {test_pattern}")
        run_specific_test(test_pattern)
    else:
        # Run all tests
        success = run_tests()
        sys.exit(0 if success else 1)
