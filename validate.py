#!/usr/bin/env python3
"""
Quick validation script to test the poster evaluation implementation.
This script validates the code structure and imports without requiring all dependencies.
"""

import sys
import os
import importlib.util
from pathlib import Path

def validate_file_structure():
    """Validate that all required files exist."""
    print("🔍 Validating file structure...")
    
    required_files = [
        "src/__init__.py",
        "src/main.py",
        "src/evaluator.py",
        "src/models/__init__.py",
        "src/models/poster_data.py",
        "src/models/openai_client.py",
        "src/models/prompts.py",
        "src/processors/__init__.py",
        "src/processors/output_generator.py",
        "src/utils/__init__.py",
        "src/utils/validators.py",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "tests/conftest.py",
        "tests/test_api.py",
        "tests/test_evaluator.py",
        "tests/test_integration.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files exist")
        return True

def validate_python_syntax():
    """Validate Python syntax for all source files."""
    print("\n🔍 Validating Python syntax...")
    
    python_files = [
        "src/main.py",
        "src/evaluator.py",
        "src/models/poster_data.py",
        "src/models/openai_client.py",
        "src/models/prompts.py",
        "src/processors/output_generator.py",
        "src/utils/validators.py"
    ]
    
    syntax_errors = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Compile to check syntax
            compile(content, file_path, 'exec')
            print(f"  ✅ {file_path}")
            
        except SyntaxError as e:
            syntax_errors.append(f"{file_path}: {e}")
            print(f"  ❌ {file_path}: {e}")
        except Exception as e:
            syntax_errors.append(f"{file_path}: {e}")
            print(f"  ❌ {file_path}: {e}")
    
    if syntax_errors:
        print(f"\n❌ Syntax errors found:")
        for error in syntax_errors:
            print(f"  - {error}")
        return False
    else:
        print("\n✅ All Python files have valid syntax")
        return True

def validate_api_structure():
    """Validate FastAPI application structure."""
    print("\n🔍 Validating API structure...")
    
    try:
        # Read main.py and check for key components
        with open('src/main.py', 'r') as f:
            content = f.read()
        
        required_components = [
            'FastAPI',
            'app = FastAPI',
            '/upload/single',
            '/upload/batch',
            '/jobs/{job_id}',
            'download',
            '/health'
        ]
        
        missing_components = []
        for component in required_components:
            if component not in content:
                missing_components.append(component)
        
        if missing_components:
            print(f"  ❌ Missing API components: {missing_components}")
            return False
        else:
            print("  ✅ All required API endpoints present")
            return True
            
    except Exception as e:
        print(f"  ❌ API structure validation error: {e}")
        return False

def main():
    """Main validation function."""
    print("🚀 Poster Evaluation API - Code Validation")
    print("=" * 50)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    all_valid = True
    
    # Run all validations
    all_valid &= validate_file_structure()
    all_valid &= validate_python_syntax()
    all_valid &= validate_api_structure()
    
    print("\n" + "=" * 50)
    if all_valid:
        print("🎉 All validations passed! The implementation looks good.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up environment: cp .env.example .env")
        print("3. Add your OpenAI API key to .env")
        print("4. Run tests: python run_tests.py")
        print("5. Start the API: uvicorn src.main:app --reload")
    else:
        print("❌ Some validations failed. Please fix the issues above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
