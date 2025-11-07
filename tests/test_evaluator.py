import pytest
import asyncio
import json
from unittest.mock import AsyncMock, patch, MagicMock
from src.evaluator import AsyncPosterEvaluator
from src.models.poster_data import EvaluationMode
import tempfile
import os

class TestAsyncPosterEvaluator:
    """Test the AsyncPosterEvaluator class."""
    
    @pytest.mark.asyncio
    async def test_evaluate_single_success(self):
        """Test successful single poster evaluation."""
        evaluator = AsyncPosterEvaluator()
        sample_evaluation_response = {
            "Q1": "12345",
            "Q2": "Dr. Jane Smith",
            "Q3": "John Doe",
            "Q4": True,
            "Q5": True,
            "Q6": 7,
            "Q7": 3,
            "Q8": 7,
            "Q9": 18,
            "Q11": 10,
            "Q12": 4,
            "Q13": 3,
            "Q15": 10,
            "poster_summary": "Machine Learning in Healthcare poster",
            "evaluation_summary": "Excellent poster with clear methodology",
            "overall_opinion": "Strong research presentation"
        }
        
        # Mock the OpenAI client
        with patch.object(evaluator.client, 'analyze_poster', 
                         return_value={"content": json.dumps(sample_evaluation_response)}) as mock_analyze:
            
            # Create a temporary image file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                f.write(b'fake image data')
                temp_file = f.name
            
            try:
                from pathlib import Path
                result = await evaluator.evaluate_poster(
                    Path(temp_file), 
                    EvaluationMode.FIFTEEN
                )
                
                evaluation_result, log = result
                assert evaluation_result.Q1 == "12345"
                assert evaluation_result.Q2 == "Dr. Jane Smith"
                assert evaluation_result.Q3 == "John Doe"
                assert evaluation_result.poster_summary == "Machine Learning in Healthcare poster"
                assert log.status == "ok"
                mock_analyze.assert_called_once()
            finally:
                # Clean up
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
    
    @pytest.mark.asyncio
    async def test_evaluate_single_file_not_found(self):
        """Test evaluation with non-existent file."""
        evaluator = AsyncPosterEvaluator()
        from pathlib import Path
        result = await evaluator.evaluate_poster(
            Path("/nonexistent/file.png"), 
            EvaluationMode.FIFTEEN
        )
        evaluation_result, log = result
        # Should return None for evaluation_result and failed status for log
        assert evaluation_result is None
        assert log.status == "failed"
        assert "No such file or directory" in log.error
    
    @pytest.mark.asyncio
    async def test_evaluate_batch_success(self):
        """Test successful batch evaluation."""
        evaluator = AsyncPosterEvaluator()
        sample_evaluation_response = {
            "Q1": "12345", "Q2": "Dr. Jane Smith", "Q3": "John Doe",
            "Q4": True, "Q5": True, "Q6": 7, "Q7": 3, "Q8": 7, "Q9": 18,
            "Q11": 10, "Q12": 4, "Q13": 3, "Q15": 10,
            "poster_summary": "Test poster", "evaluation_summary": "Good", "overall_opinion": "Nice"
        }
        
        # Mock the OpenAI client
        with patch.object(evaluator.client, 'analyze_poster', 
                         return_value={"content": json.dumps(sample_evaluation_response)}):
            
            # Create temporary image files
            temp_files = []
            for i in range(3):
                with tempfile.NamedTemporaryFile(suffix=f'_{i}.png', delete=False) as f:
                    f.write(f'fake image data {i}'.encode())
                    temp_files.append(f.name)
            
            try:
                from pathlib import Path
                # First create a job
                job_id = evaluator.create_job(EvaluationMode.SEVEN, len(temp_files))
                
                # Then evaluate batch
                results = await evaluator.evaluate_batch(
                    job_id,
                    [Path(f) for f in temp_files], 
                    EvaluationMode.SEVEN
                )
                
                assert job_id is not None
                assert job_id in evaluator.jobs
                
                # Check job status
                job = evaluator.get_job(job_id)
                assert job is not None
                assert job.status.value in ["processing", "completed"]
                
            finally:
                # Clean up
                for temp_file in temp_files:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
    
    @pytest.mark.asyncio
    async def test_evaluate_batch_empty_list(self):
        """Test batch evaluation with empty file list."""
        evaluator = AsyncPosterEvaluator()
        from pathlib import Path
        # Create a job first
        job_id = evaluator.create_job(EvaluationMode.SEVEN, 0)
        
        # Evaluate empty batch
        results = await evaluator.evaluate_batch(job_id, [], EvaluationMode.SEVEN)
        
        # Should return empty list of results
        assert len(results) == 0
        
        # Job should be completed with success even if empty
        job = evaluator.get_job(job_id)
        assert job.status.value == "completed"
    
    def test_get_job_status_existing_job(self):
        """Test getting status of existing job."""
        evaluator = AsyncPosterEvaluator()
        # Create a real job using the create_job method
        job_id = evaluator.create_job(EvaluationMode.SEVEN, 10)
        
        job = evaluator.get_job(job_id)
        
        assert job is not None
        assert job.status.value == "pending"
        assert job.total_files == 10
        assert job.processed_files == 0
    
    def test_get_job_status_nonexistent_job(self):
        """Test getting status of non-existent job."""
        evaluator = AsyncPosterEvaluator()
        job = evaluator.get_job("nonexistent_job")
        assert job is None
    
    @pytest.mark.asyncio
    async def test_process_poster_success(self):
        """Test successful single poster processing."""
        evaluator = AsyncPosterEvaluator()
        sample_evaluation_response = {
            "Q1": "12345", "Q2": "Dr. Jane Smith", "Q3": "John Doe",
            "Q4": True, "Q5": True, "Q6": 7, "Q7": 3, "Q8": 7, "Q9": 18,
            "Q11": 10, "Q12": 4, "Q13": 3, "Q15": 10,
            "poster_summary": "Machine Learning in Healthcare poster",
            "evaluation_summary": "Excellent poster with clear methodology",
            "overall_opinion": "Strong research presentation"
        }
        
        with patch.object(evaluator.client, 'analyze_poster', 
                         return_value={"content": json.dumps(sample_evaluation_response)}):
            
            # Create a temporary image file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                f.write(b'fake image data')
                temp_file = f.name
            
            try:
                from pathlib import Path
                result = await evaluator.evaluate_poster(
                    Path(temp_file), 
                    EvaluationMode.FIFTEEN
                )
                
                evaluation_result, log = result
                assert log.file == os.path.basename(temp_file)
                assert evaluation_result.Q1 == "12345"
                assert evaluation_result.Q2 == "Dr. Jane Smith"
                assert evaluation_result.poster_summary == "Machine Learning in Healthcare poster"
                assert log.status == "ok"
                
            finally:
                # Clean up
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
    
    @pytest.mark.asyncio
    async def test_process_poster_openai_error(self):
        """Test poster processing with OpenAI error."""
        evaluator = AsyncPosterEvaluator()
        with patch.object(evaluator.client, 'analyze_poster', 
                         side_effect=Exception("API Error")):
            
            # Create a temporary image file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                f.write(b'fake image data')
                temp_file = f.name
            
            try:
                from pathlib import Path
                result = await evaluator.evaluate_poster(
                    Path(temp_file), 
                    EvaluationMode.FIFTEEN
                )
                
                evaluation_result, log = result
                # Should return None for evaluation_result and error in log
                assert evaluation_result is None
                assert log.status == "failed"
                assert log.error == "API Error"
                
            finally:
                # Clean up
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

class TestJobManagement:
    """Test job management functionality."""
    
    def test_create_job(self):
        """Test job creation."""
        from src.models.poster_data import EvaluationMode
        
        evaluator = AsyncPosterEvaluator()
        job_id = evaluator.create_job(EvaluationMode.FIFTEEN, 5)
        assert isinstance(job_id, str)
        assert len(job_id) > 0
        
        # Verify job was created
        job = evaluator.get_job(job_id)
        assert job is not None
        assert job.total_files == 5
    
    def test_update_job_progress(self):
        """Test job progress updating."""
        from src.models.poster_data import ProcessingStatus
        
        evaluator = AsyncPosterEvaluator()
        # Create a real job
        job_id = evaluator.create_job(EvaluationMode.SEVEN, 10)
        
        # Update status to processing
        evaluator.update_job_status(job_id, ProcessingStatus.PROCESSING)
        
        # Verify the update
        job = evaluator.get_job(job_id)
        assert job.status == ProcessingStatus.PROCESSING
