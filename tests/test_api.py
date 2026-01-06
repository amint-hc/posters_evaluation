import pytest
import io
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch, MagicMock
import tempfile
import os
import json
from src.main import app

class TestHealthEndpoint:
    """Test the health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check returns OK."""
        response = client.get("/health")
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "healthy"
        assert "api_key" in result
        assert "upload_directory" in result
        assert "download_directory" in result
        assert "active_jobs" in result

class TestSingleUploadEndpoint:
    """Test single poster upload endpoint."""
    
    def test_upload_single_success(self, client, sample_image_data):
        """Test successful single poster upload."""
        with patch('src.evaluator.AsyncPosterEvaluator.create_job') as mock_create_job, \
             patch('src.main.process_evaluation_job') as mock_process:
            
            mock_create_job.return_value = "job_123"
            
            files = {"file": ("test_poster.png", io.BytesIO(sample_image_data), "image/png")}
            data = {}
            
            response = client.post("/upload/single", files=files, data=data)
            
            assert response.status_code == 200
            result = response.json()
            assert result["job_id"] == "job_123"
            assert result["status"] == "pending"
            mock_create_job.assert_called_once()

    def test_upload_single_invalid_file(self, client):
        """Test upload with invalid file type."""
        files = {"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")}
        data = {}
        
        response = client.post("/upload/single", files=files, data=data)
        
        assert response.status_code == 400

    def test_upload_single_no_file(self, client):
        """Test upload without file."""
        data = {}
        
        response = client.post("/upload/single", data=data)
        
        assert response.status_code == 422

class TestBatchUploadEndpoint:
    """Test batch poster upload endpoint."""
    
    def test_upload_batch_success(self, client, sample_image_data):
        """Test successful batch upload."""
        with patch('src.evaluator.AsyncPosterEvaluator.create_job') as mock_create_job, \
             patch('src.main.process_evaluation_job') as mock_process:
            
            mock_create_job.return_value = "job_123"
            
            files = [
                ("files", ("poster1.png", io.BytesIO(sample_image_data), "image/png")),
                ("files", ("poster2.png", io.BytesIO(sample_image_data), "image/png"))
            ]
            data = {}
            
            response = client.post("/upload/batch", files=files, data=data)
            
            assert response.status_code == 200
            result = response.json()
            assert result["job_id"] == "job_123"
            assert "uploaded_files" in result
            mock_create_job.assert_called_once()

    def test_upload_batch_no_files(self, client):
        """Test batch upload without files."""
        data = {}
        
        response = client.post("/upload/batch", data=data)
        
        assert response.status_code == 422

    def test_upload_batch_too_many_files(self, client, sample_image_data):
        """Test batch upload with too many files."""
        # Create more files than the limit (50 files)
        files = [
            ("files", (f"poster{i}.png", io.BytesIO(sample_image_data), "image/png"))
            for i in range(251)
        ]
        data = {}
        
        response = client.post("/upload/batch", files=files, data=data)    
        assert response.status_code == 400
        assert "Too many files" in response.json()["detail"]

class TestJobEndpoints:
    """Test job management endpoints."""
    
    def test_get_job_status_processing(self, client):
        """Test getting status of processing job."""
        from src.models.poster_data import EvaluationJob, ProcessingStatus
        from datetime import datetime
        
        with patch('src.evaluator.AsyncPosterEvaluator.get_job') as mock_get_job:
            mock_job = EvaluationJob(
                job_id="job_123",
                status=ProcessingStatus.PROCESSING,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                total_files=10,
                processed_files=5
            )
            mock_get_job.return_value = mock_job
            
            response = client.get("/jobs/job_123")
            
            assert response.status_code == 200
            result = response.json()
            assert result["status"] == "processing"

    def test_get_job_status_completed(self, client):
        """Test getting status of completed job."""
        from src.models.poster_data import EvaluationJob, ProcessingStatus
        from datetime import datetime
        
        with patch('src.evaluator.AsyncPosterEvaluator.get_job') as mock_get_job:
            mock_job = EvaluationJob(
                job_id="job_123",
                status=ProcessingStatus.COMPLETED,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                total_files=5,
                processed_files=5
            )
            mock_get_job.return_value = mock_job
            
            response = client.get("/jobs/job_123")
            
            assert response.status_code == 200
            result = response.json()
            assert result["status"] == "completed"

    def test_get_job_status_not_found(self, client):
        """Test getting status of non-existent job."""
        with patch('src.evaluator.AsyncPosterEvaluator.get_job') as mock_get_job:
            mock_get_job.return_value = None
            
            response = client.get("/jobs/nonexistent_job")
            
            assert response.status_code == 404

class TestDownloadEndpoints:
    """Test file download endpoints."""
    
    def test_download_results_success(self, client):
        """Test successful file download."""
        from src.models.poster_data import EvaluationJob, ProcessingStatus
        from datetime import datetime
        from pathlib import Path
        
        # Create temp download directory and file
        download_dir = Path("downloads") / "test_job_123"
        download_dir.mkdir(parents=True, exist_ok=True)
        test_file = download_dir / "results_master.csv"
        
        try:
            test_file.write_text("title,score\nTest Poster,85\n")
            
            # Mock the evaluator's get_job method
            mock_job = EvaluationJob(
                job_id="test_job_123",
                status=ProcessingStatus.COMPLETED,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                total_files=1,
                processed_files=1
            )
            
            with patch('src.evaluator.AsyncPosterEvaluator.get_job') as mock_get_job:
                mock_get_job.return_value = mock_job
                
                response = client.get("/jobs/test_job_123/download/master")
                
                assert response.status_code == 200
                assert "text/csv" in response.headers["content-type"]
        finally:
            # Clean up
            if test_file.exists():
                test_file.unlink()
            if download_dir.exists():
                download_dir.rmdir()

    def test_download_results_file_not_found(self, client):
        """Test download of non-existent file."""
        response = client.get("/download?file_path=/nonexistent/file.csv")
        
        assert response.status_code == 404

    def test_download_results_no_file_path(self, client):
        """Test download of non-existent job."""
        response = client.get("/jobs/nonexistent_job/download/master")
        
        assert response.status_code == 404


