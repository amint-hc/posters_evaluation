"""
GUI Backend Module for Poster Evaluation System

This module provides the backend logic for the GUI application, including:
- FastAPI server lifecycle management
- API key management with .secret file
- HTTP client for FastAPI communication
- Results processing and formatting
"""

import os
import time
import json
import subprocess
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple


class SecretManager:
    """Manages API key storage with 7-day expiration"""
    
    SECRET_FILE = Path(".secret")
    EXPIRATION_DAYS = 7
    
    @classmethod
    def save_api_key(cls, api_key: str):
        """Save API key to .secret file with timestamp"""
        data = {
            "api_key": api_key,
            "created_at": datetime.now().isoformat()
        }
        with open(cls.SECRET_FILE, 'w') as f:
            json.dump(data, f)
    
    @classmethod
    def load_api_key(cls) -> Optional[str]:
        """Load API key from .secret file if not expired"""
        if not cls.SECRET_FILE.exists():
            return None
        
        try:
            with open(cls.SECRET_FILE, 'r') as f:
                data = json.load(f)
            
            created_at = datetime.fromisoformat(data['created_at'])
            age = datetime.now() - created_at
            
            # Check if expired (7 days)
            if age > timedelta(days=cls.EXPIRATION_DAYS):
                cls.SECRET_FILE.unlink()  # Delete expired file
                return None
            
            return data['api_key']
        except (json.JSONDecodeError, KeyError, ValueError):
            # Invalid file format, delete it
            cls.SECRET_FILE.unlink()
            return None
    
    @classmethod
    def clear_api_key(cls):
        """Delete .secret file"""
        if cls.SECRET_FILE.exists():
            cls.SECRET_FILE.unlink()


class ServerManager:
    """Manages FastAPI server lifecycle"""
    
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.base_url = "http://localhost:8080"
    
    def start_server(self, api_key: str) -> bool:
        """
        Start FastAPI server with given API key
        
        Args:
            api_key: OpenAI API key
        
        Returns:
            True if server started successfully, False otherwise
        """
        # Check if already running
        if self.is_running():
            print("Server is already running")
            return True
        
        # Set environment variables
        env = os.environ.copy()
        env['OPENAI_API_KEY'] = api_key
        env['APP_PORT'] = '8080'
        env['APP_RELOAD'] = 'false'
        
        # Start server process
        try:
            print("Starting FastAPI server process...")
            self.process = subprocess.Popen(
                ['python', 'run.py'],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            # Wait for server to be ready (max 20 seconds)
            print("Waiting for server to be ready...")
            max_attempts = 40
            for attempt in range(max_attempts):
                time.sleep(0.5)
                if self.is_running():
                    print(f"Server started successfully after {attempt * 0.5:.1f} seconds")
                    return True
                if attempt % 4 == 0:  # Print every 2 seconds
                    print(f"  Attempt {attempt + 1}/{max_attempts}...")
            
            print(f"Server failed to start within {max_attempts * 0.5} seconds")
            return False
        except Exception as e:
            print(f"Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop FastAPI server gracefully"""
        if self.process:
            try:
                if os.name == 'nt':
                    # Windows: send CTRL_BREAK_EVENT
                    self.process.send_signal(subprocess.signal.CTRL_BREAK_EVENT)
                else:
                    # Unix: send SIGTERM
                    self.process.terminate()
                
                # Wait for process to exit (max 5 seconds)
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if not responding
                self.process.kill()
            except Exception as e:
                print(f"Error stopping server: {e}")
            finally:
                self.process = None
    
    def is_running(self) -> bool:
        """Check if server is running and responding"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except (requests.RequestException, requests.ConnectionError, requests.Timeout):
            return False
        except Exception:
            return False


class EvaluationClient:
    """HTTP client for FastAPI communication"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
    
    def upload_batch(self, folder_path: str, approach: str = "direct") -> Optional[str]:
        """
        Upload batch of posters for evaluation
        
        Args:
            folder_path: Path to folder containing poster images
            approach: Evaluation approach to use (direct, reasoning, deep_analysis, strict)
        
        Returns:
            Job ID if successful, None otherwise
        """
        folder = Path(folder_path)
        if not folder.exists() or not folder.is_dir():
            raise ValueError(f"Invalid folder path: {folder_path}")
        
        # Find all image files
        image_extensions = {'.jpg', '.jpeg', '.png'}
        image_files = [
            f for f in folder.iterdir()
            if f.suffix.lower() in image_extensions
        ]
        
        if not image_files:
            raise ValueError("No image files found in folder")
        
        # Prepare multipart upload with files and approach as form data
        files = [
            ('files', (f.name, open(f, 'rb'), 'image/jpeg'))
            for f in image_files
        ]
        
        # Add approach as form data
        data = {'approach': approach}
        
        try:
            response = requests.post(
                f"{self.base_url}/upload/batch",
                files=files,
                data=data,  # Send approach in request body as form data
                timeout=30
            )
            
            # Close file handles
            for _, (_, file_obj, _) in files:
                file_obj.close()
            
            if response.status_code == 200:
                return response.json()['job_id']
            else:
                print(f"Upload failed: {response.status_code} - {response.text}")
                return None
        except requests.RequestException as e:
            print(f"Upload error: {e}")
            return None
    
    def poll_job_status(self, job_id: str) -> Dict:
        """
        Poll job status
        
        Args:
            job_id: Job ID to check
        
        Returns:
            Job status dict
        """
        try:
            response = requests.get(
                f"{self.base_url}/jobs/{job_id}",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "error", "message": f"HTTP {response.status_code}"}
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    def get_results(self, job_id: str) -> Optional[Dict]:
        """
        Get evaluation results for completed job
        
        Args:
            job_id: Job ID
        
        Returns:
            Results dict or None
        """
        try:
            response = requests.get(
                f"{self.base_url}/jobs/{job_id}/results",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.RequestException as e:
            print(f"Error getting results: {e}")
            return None
    
    def download_excel(self, job_id: str, save_path: str) -> bool:
        """
        Download Excel file for job
        
        Args:
            job_id: Job ID
            save_path: Path to save Excel file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/jobs/{job_id}/download/excel",
                timeout=30
            )
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                return False
        except requests.RequestException as e:
            print(f"Error downloading Excel: {e}")
            return False

    def download_comparison_excel(self, job_ids: Dict[str, str], save_path: str) -> bool:
        """
        Generate and download comparison Excel file
        
        Args:
            job_ids: Dict mapping approach name to job ID
            save_path: Path to save Excel file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # 1. Request comparison report generation
            response = requests.post(
                f"{self.base_url}/jobs/compare",
                json=job_ids,
                timeout=60
            )
            
            if response.status_code != 200:
                print(f"Comparison generation failed: {response.status_code} - {response.text}")
                return False
                
            data = response.json()
            download_url = data.get('download_url')
            if not download_url:
                return False
                
            # 2. Download the generated file
            download_response = requests.get(
                f"{self.base_url}{download_url}",
                timeout=30
            )
            
            if download_response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(download_response.content)
                return True
            else:
                print(f"Comparison download failed: {download_response.status_code}")
                return False
                
        except requests.RequestException as e:
            print(f"Error in comparison workflow: {e}")
            return False


class ResultsProcessor:
    """Process and format evaluation results"""
    
    @staticmethod
    def format_for_display(results: List[Dict]) -> List[Tuple]:
        """
        Format results for TreeView display
        
        Args:
            results: List of evaluation results
        
        Returns:
            List of tuples (project_number, publishers, direct_grade, reasoning_grade, deep_grade, strict_grade)
        """
        formatted = []
        for result in results:
            project_number = result.get('project_number', 'N/A')
            
            # Support multiple publishers (comma-separated)
            presenter_names = result.get('presenter_names', 'N/A')
            
            # Get final grade (this is from a single approach run)
            grade = result.get('final_grade', 0)
            
            formatted.append((project_number, presenter_names, grade))
        
        return formatted
    
    @staticmethod
    def combine_multi_approach_results(job_ids: Dict[str, str], client: EvaluationClient) -> List[Dict]:
        """
        Combine results from all 4 evaluation approaches
        
        Args:
            job_ids: Dict mapping approach name to job ID
            client: EvaluationClient instance
        
        Returns:
            List of combined results with all approach grades
        """
        # Get results for each approach
        all_results = {}
        for approach, job_id in job_ids.items():
            results = client.get_results(job_id)
            if results and 'results' in results:
                all_results[approach] = {
                    r['poster_file']: r for r in results['results']
                }
        
        # Combine by poster file
        combined = []
        if all_results:
            # Get all poster files from first approach
            first_approach = list(all_results.values())[0]
            for poster_file in first_approach.keys():
                entry = {
                    'poster_file': poster_file,
                    'project_number': first_approach[poster_file].get('project_number', 'N/A'),
                    'presenter_names': first_approach[poster_file].get('presenter_names', 'N/A'),
                }
                
                # Add grades from each approach
                for approach in ['direct', 'reasoning', 'deep_analysis', 'strict']:
                    if approach in all_results and poster_file in all_results[approach]:
                        entry[f'{approach}_grade'] = all_results[approach][poster_file].get('final_grade', 0)
                    else:
                        entry[f'{approach}_grade'] = 0
                
                combined.append(entry)
        
        return combined
