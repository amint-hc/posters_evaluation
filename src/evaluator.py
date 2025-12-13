import time
import uuid
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from .models.openai_client import AsyncOpenAIVisionClient
from .strategies import get_strategy
from .models.poster_data import (
    PosterEvaluation, 
    ProcessingLog, 
    EvaluationJob, 
    ProcessingStatus
)

class AsyncPosterEvaluator:
    """Async poster evaluation engine for FastAPI"""
    
    def __init__(self):
        try:
            self.client = AsyncOpenAIVisionClient()
        except ValueError as e:
            print(f"Configuration Error: {str(e)}")
            print("Please check your .env file and ensure OPENAI_API_KEY is set.")
            raise
        
        self.jobs: Dict[str, EvaluationJob] = {}
    
    def create_job(self, total_files: int) -> str:
        """Create a new evaluation job"""
        job_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        job = EvaluationJob(
            job_id=job_id,
            status=ProcessingStatus.PENDING,
            created_at=now,
            updated_at=now,
            total_files=total_files,
            processed_files=0
        )
        
        self.jobs[job_id] = job
        return job_id
    
    def get_job(self, job_id: str) -> Optional[EvaluationJob]:
        """Get job by ID"""
        return self.jobs.get(job_id)
    
    def update_job_status(self, job_id: str, status: ProcessingStatus):
        """Update job status"""
        if job_id in self.jobs:
            self.jobs[job_id].status = status
            self.jobs[job_id].updated_at = datetime.utcnow()
    
    async def evaluate_poster(self, image_path: Path) -> Tuple[Optional[PosterEvaluation], ProcessingLog]:
        """Evaluate a single poster image using the configured strategy"""
        start_time = time.time()
        processing_log = ProcessingLog(
            file=image_path.name,
            status="ok",
            grade=None,
            duration_ms=None,
            error=None
        )
        
        try:
            # Get strategy based on client configuration
            strategy = get_strategy(self.client.evaluation_approach)
            
            # Execute strategy
            data = await strategy.evaluate(self.client, image_path)
            
            # Create evaluation object
            evaluation = self._create_evaluation(image_path, data)
            
            # Calculate final grade
            evaluation.final_grade = evaluation.calculate_final_grade()
            
            # Update processing log with success info
            processing_log.grade = evaluation.final_grade
            processing_log.duration_ms = int((time.time() - start_time) * 1000)
            
            return evaluation, processing_log
            
        except Exception as e:
            print(f"Error evaluating {image_path.name}: {str(e)}")
            import traceback
            traceback.print_exc()
            # Update processing log with error info
            processing_log.status = "failed"
            processing_log.error = "timeout" if "timeout" in str(e).lower() else str(e)
            return None, processing_log
    
    def _create_evaluation(self, image_path: Path, data: Dict) -> PosterEvaluation:
        """Create PosterEvaluation from API response"""
        evaluation = PosterEvaluation(poster_file=image_path.name)
        
        # Map response data to evaluation fields
        for field, value in data.items():
            if hasattr(evaluation, field):
                setattr(evaluation, field, value)
        
        return evaluation
    
    async def evaluate_batch(self, job_id: str, image_paths: List[Path]) -> List[PosterEvaluation]:
        """Evaluate batch of posters with job tracking"""
        self.update_job_status(job_id, ProcessingStatus.PROCESSING)
        
        results = []
        errors = []
        
        # Process images concurrently (with rate limiting)
        semaphore = asyncio.Semaphore(3)  # Limit concurrent API calls
        
        async def process_single_poster(image_path: Path):
            async with semaphore:
                evaluation, processing_log = await self.evaluate_poster(image_path)
                
                if evaluation:
                    results.append(evaluation)
                else:
                    errors.append(f"Failed to process {image_path.name}")
                
                # Update job progress and logs
                job = self.get_job(job_id)
                if job:
                    job.processed_files += 1
                    job.updated_at = datetime.utcnow()
                    job.processing_logs.append(processing_log)
        
        # Handle empty batch case first
        if not image_paths:
            if job_id in self.jobs:
                self.jobs[job_id].status = ProcessingStatus.COMPLETED
                self.jobs[job_id].updated_at = datetime.utcnow()
            return []
            
        # Process non-empty batch
        tasks = [process_single_poster(path) for path in image_paths]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        # Sort results by grade if we have any
        if results:
            results.sort(key=lambda x: x.final_grade, reverse=True)
        
        # Update job with results
        if job_id in self.jobs:
            job = self.jobs[job_id]
            job.results = results
            job.errors = errors
            job.processed_files = len(results)
            job.updated_at = datetime.utcnow()
            
            # Update status based on results
            if not results and errors:
                job.status = ProcessingStatus.FAILED
                print(f"Job {job_id} failed with {len(errors)} errors")
            else:
                job.status = ProcessingStatus.COMPLETED
                print(f"Job {job_id} completed with {len(results)} successful results")
        
        return results

# Global evaluator instance (lazy initialization)
_evaluator_instance = None

def get_evaluator() -> AsyncPosterEvaluator:
    """Get or create the global evaluator instance"""
    global _evaluator_instance
    if _evaluator_instance is None:
        _evaluator_instance = AsyncPosterEvaluator()
    return _evaluator_instance

# For backward compatibility
def evaluator() -> AsyncPosterEvaluator:
    """Get the global evaluator instance"""
    return get_evaluator()
