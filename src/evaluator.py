import json
import time
import uuid
import asyncio
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from .models.openai_client import AsyncOpenAIVisionClient
from .models.prompts import POSTER_EVALUATION_PROMPT, SEVEN_QUESTION_PROMPT
from .models.poster_data import (
    PosterEvaluation, ProcessingLog, EvaluationJob, 
    EvaluationMode, ProcessingStatus
)

class AsyncPosterEvaluator:
    """Async poster evaluation engine for FastAPI"""
    
    def __init__(self):
        self.client = AsyncOpenAIVisionClient()
        self.jobs: Dict[str, EvaluationJob] = {}
    
    def create_job(self, mode: EvaluationMode, total_files: int) -> str:
        """Create a new evaluation job"""
        job_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        job = EvaluationJob(
            job_id=job_id,
            status=ProcessingStatus.PENDING,
            mode=mode,
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
    
    async def evaluate_poster(self, image_path: Path, mode: EvaluationMode) -> Optional[PosterEvaluation]:
        """Evaluate a single poster image"""
        start_time = time.time()
        
        try:
            # Select appropriate prompt
            prompt = (SEVEN_QUESTION_PROMPT if mode == EvaluationMode.SEVEN 
                     else POSTER_EVALUATION_PROMPT)
            
            # Get AI analysis
            response = await self.client.analyze_poster(image_path, prompt)
            
            # Parse JSON response
            analysis_data = json.loads(response["content"])
            
            # Create evaluation object
            evaluation = self._create_evaluation(image_path, analysis_data)
            
            # Calculate final grade
            evaluation.final_grade = evaluation.calculate_final_grade()
            
            return evaluation
            
        except Exception as e:
            print(f"Error evaluating {image_path.name}: {str(e)}")
            return None
    
    def _create_evaluation(self, image_path: Path, data: Dict) -> PosterEvaluation:
        """Create PosterEvaluation from API response"""
        evaluation = PosterEvaluation(poster_file=image_path.name)
        
        # Map response data to evaluation fields
        for field, value in data.items():
            if hasattr(evaluation, field):
                setattr(evaluation, field, value)
        
        return evaluation
    
    async def evaluate_batch(self, job_id: str, image_paths: List[Path], 
                           mode: EvaluationMode) -> List[PosterEvaluation]:
        """Evaluate batch of posters with job tracking"""
        self.update_job_status(job_id, ProcessingStatus.PROCESSING)
        
        results = []
        errors = []
        
        # Process images concurrently (with rate limiting)
        semaphore = asyncio.Semaphore(3)  # Limit concurrent API calls
        
        async def process_single_poster(image_path: Path):
            async with semaphore:
                evaluation = await self.evaluate_poster(image_path, mode)
                
                if evaluation:
                    results.append(evaluation)
                else:
                    errors.append(f"Failed to process {image_path.name}")
                
                # Update job progress
                job = self.get_job(job_id)
                if job:
                    job.processed_files += 1
                    job.updated_at = datetime.utcnow()
        
        # Execute all evaluations
        tasks = [process_single_poster(path) for path in image_paths]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        # Sort results by grade
        results.sort(key=lambda x: x.final_grade, reverse=True)
        
        # Update job with results
        job = self.get_job(job_id)
        if job:
            job.results = results
            job.errors = errors
            job.status = ProcessingStatus.COMPLETED if not errors else ProcessingStatus.FAILED
            job.updated_at = datetime.utcnow()
        
        return results

# Global evaluator instance
evaluator = AsyncPosterEvaluator()
