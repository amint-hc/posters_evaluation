# Implementation Context & Instructions

## Project Implementation Guide for Poster Evaluation System

This document provides step-by-step implementation instructions for building the automated poster evaluation system using GPT-4.1 model.

---

## 1. Quick Start Guide

### Prerequisites
- **Python 3.8+** (Recommended: 3.10+)
- **OpenAI API Key** with GPT-4.1 with vision input
- **Git** for version control
- **IDE/Editor** (VS Code recommended)

### Development Setup
```bash
# Clone and setup project
git clone <repository-url>
cd poster-evaluation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Create directories
mkdir -p uploads outputs

# Run development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Basic Usage
1. **Upload Single Poster**: POST `/upload/single`
2. **Upload Batch**: POST `/upload/batch`
3. **Check Job Status**: GET `/jobs/{job_id}`
4. **Get Results**: GET `/jobs/{job_id}/results`
5. **Download Files**: GET `/jobs/{job_id}/download/master`

---

## 2. Core Dependencies Installation

### requirements.txt
```pip-requirements
# FastAPI Core
fastapi>=0.100.0,<0.105.0
uvicorn[standard]>=0.23.0,<0.25.0
python-multipart>=0.0.6

# AI/ML Core
openai>=1.3.0,<2.0.0
pillow>=9.0.0,<11.0.0

# Data Processing
pandas>=1.5.0,<2.1.0
scipy>=1.9.0,<1.12.0
openpyxl>=3.1.0
pydantic>=1.10.0,<2.0.0

# Async I/O
aiofiles>=22.0.0,<24.0.0

# Configuration & Utilities
python-dotenv>=1.0.0
pathlib2>=2.3.0
typing-extensions>=4.0.0

# Development & Testing
pytest>=7.0.0
pytest-asyncio>=0.21.0
httpx>=0.25.0
pytest-mock>=3.12.0
coverage>=7.3.0
black>=22.0.0
flake8>=4.0.0,<6.0.0
mypy>=0.991
```

---

## 3. Project Architecture Implementation

### 3.1 Core Data Models (`src/models/poster_data.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal, Union, List
from pathlib import Path
from datetime import datetime
from enum import Enum

class EvaluationMode(str, Enum):
    """Evaluation mode options"""
    SEVEN = "seven"
    FIFTEEN = "fifteen"

class ProcessingStatus(str, Enum):
    """Processing status options"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class QuestionResponse(BaseModel):
    """Individual question response"""
    question_id: str
    response: Union[str, bool, int]
    score: int
    
class PosterEvaluation(BaseModel):
    """Complete poster evaluation result"""
    poster_file: str
    project_number: Optional[str] = ""
    advisor_name: Optional[str] = ""
    presenter: Optional[str] = ""
    
    # Question responses (Q1-Q15)
    Q1: str = ""  # Project number
    Q2: str = ""  # Advisor name
    Q3: str = ""  # Presenter(s)
    Q4: bool = False  # Topic present
    Q5: bool = False  # White background
    Q6: Literal[0, 4, 7, 10] = 0  # Topic-intro connection
    Q7: Literal[0, 1, 3, 5] = 0   # Intro-motivation
    Q8: Literal[0, 4, 7, 10] = 0  # Conclusions supported
    Q9: Literal[0, 10, 18, 25] = 0  # Overall quality
    Q11: Literal[0, 10, 15] = 0   # Graph relevance
    Q12: Literal[0, 3, 4, 5] = 0  # Introduction quality
    Q13: Literal[0, 1, 3, 5] = 0  # Implementation detail
    Q15: Literal[0, 5, 10, 15] = 0  # Global coherence
    
    # Summaries
    poster_summary: str = ""
    evaluation_summary: str = ""
    overall_opinion: str = ""
    
    # Calculated score
    final_grade: int = Field(ge=0, le=100)
    
    def calculate_final_grade(self, mode: EvaluationMode = EvaluationMode.FIFTEEN) -> int:
        """Calculate final grade based on evaluation mode"""
        # Common quality metrics for both modes
        quality_score = (self.Q6 + self.Q7 + self.Q8 + self.Q9 + 
                        self.Q11 + self.Q12 + self.Q13)
        
        if mode == EvaluationMode.FIFTEEN:
            # Include presence scores and global coherence for FIFTEEN mode
            presence_score = sum([
                2 if self.Q1 else 0,
                2 if self.Q2 else 0,
                2 if self.Q3 else 0,
                2 if self.Q4 else 0,
                2 if self.Q5 else 0
            ])
            quality_score += self.Q15  # Add global coherence
            return presence_score + quality_score
        else:  # SEVEN mode
            # Scale quality score to 100-point system
            return quality_score * 100 // 75

class ProcessingLog(BaseModel):
    """Log entry for processing telemetry"""
    file: str
    status: Literal["ok", "failed"]
    grade: Optional[int] = None
    duration_ms: Optional[int] = None
    error: Optional[str] = None

# API Request/Response Models
class EvaluationRequest(BaseModel):
    """Request model for poster evaluation"""
    mode: EvaluationMode = EvaluationMode.FIFTEEN
    notification_webhook: Optional[str] = None

class BatchEvaluationRequest(BaseModel):
    """Request model for batch evaluation"""
    mode: EvaluationMode = EvaluationMode.FIFTEEN
    notification_webhook: Optional[str] = None

class EvaluationJob(BaseModel):
    """Evaluation job tracking"""
    job_id: str
    status: ProcessingStatus
    mode: EvaluationMode
    created_at: datetime
    updated_at: datetime
    total_files: int
    processed_files: int
    results: List[PosterEvaluation] = []
    errors: List[str] = []

class EvaluationResponse(BaseModel):
    """Response model for evaluation results"""
    job_id: str
    status: ProcessingStatus
    message: str
    results_url: Optional[str] = None
    download_urls: Optional[dict] = None

class BatchUploadResponse(BaseModel):
    """Response for batch upload"""
    job_id: str
    uploaded_files: List[str]
    skipped_files: List[str]
    message: str
```

### 3.2 Async OpenAI Client (`src/models/openai_client.py`)

```python
import base64
import os
import asyncio
from pathlib import Path
from typing import Dict, Any
import aiofiles
from openai import AsyncOpenAI
from PIL import Image
import io

class AsyncOpenAIVisionClient:
    """Async OpenAI GPT-4 Vision client for poster analysis"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.1"))
        self.timeout = int(os.getenv("TIMEOUT_SECONDS", "30"))
    
    async def encode_image(self, image_path: Path) -> str:
        """Encode image to base64 for API"""
        async with aiofiles.open(image_path, "rb") as image_file:
            image_data = await image_file.read()
            return base64.b64encode(image_data).decode('utf-8')
    
    async def analyze_poster(self, image_path: Path, prompt: str) -> Dict[str, Any]:
        """Send poster image to GPT-4 Vision for analysis"""
        try:
            base64_image = await self.encode_image(image_path)
            
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                ),
                timeout=self.timeout
            )
            
            return {
                "content": response.choices[0].message.content,
                "usage": response.usage.dict() if response.usage else None
            }
            
        except asyncio.TimeoutError:
            raise Exception(f"OpenAI API timeout after {self.timeout} seconds")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
```

### 3.3 Evaluation System Architecture

The system implements a unified evaluation approach with mode-specific grade calculation:

#### 3.3.1 Unified Prompt System (`src/models/prompts.py`)
The evaluation uses a single standardized prompt for all evaluation modes:
```python
POSTER_EVALUATION_PROMPT = """
You are an expert academic poster evaluator. Analyze this graduation project poster...
[Prompt details remain the same]
"""
```

Key characteristics:
- Single prompt handles all evaluation modes
- Comprehensive data collection for all criteria
- Structured JSON response format
- Covers both presence checks and quality metrics

#### 3.3.2 Mode-Specific Grade Calculation (`src/models/poster_data.py`)
Grade calculation varies by mode while using the same input data:

```python
def calculate_final_grade(self, mode: EvaluationMode = EvaluationMode.FIFTEEN) -> int:
    """Calculate final grade from all question scores"""
    # Common quality metrics for both modes
    quality_score = (self.Q6 + self.Q7 + self.Q8 + self.Q9 + 
                    self.Q11 + self.Q12 + self.Q13)
    
    if mode == EvaluationMode.FIFTEEN:
        # Full evaluation including presence and coherence
        presence_score = sum([
            2 if self.Q1 else 0,  # Project number
            2 if self.Q2 else 0,  # Advisor name
            2 if self.Q3 else 0,  # Presenter(s)
            2 if self.Q4 else 0,  # Topic present
            2 if self.Q5 else 0   # White background
        ])
        quality_score += self.Q15  # Add global coherence
        return presence_score + quality_score
    else:  # SEVEN mode
        # Quality-focused evaluation
        return quality_score * 100 // 75  # Scale to 100
```

**FIFTEEN Mode Scoring (Max 100 points):**
- Presence metrics (Q1-Q5): 10 points
  * 2 points each for basic formatting requirements
- Quality metrics (Q6-Q13): 75 points
  * Detailed assessment of content and presentation
- Global coherence (Q15): 15 points
  * Overall structure and flow evaluation

**SEVEN Mode Scoring (Max 100 points):**
- Focuses on quality metrics only (Q6-Q13)
- Raw score (max 75) scaled to 100-point system
- Excludes presence checks and global coherence
- Emphasizes core content quality over formatting

---

## 4. Core Processing Logic

### 4.1 Async Evaluator (`src/evaluator.py`)

```python
import json
import time
import uuid
import asyncio
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from .models.openai_client import AsyncOpenAIVisionClient
from .models.prompts import POSTER_EVALUATION_PROMPT
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
    
    async def evaluate_poster(self, image_path: Path, mode: EvaluationMode) -> Tuple[Optional[PosterEvaluation], ProcessingLog]:
        """Evaluate a single poster image and return both evaluation and processing log"""
        start_time = time.time()
        processing_log = ProcessingLog(
            file=image_path.name,
            status="ok",
            grade=None,
            duration_ms=None,
            error=None
        )
        
        try:
            # Use the same prompt for all modes
            response = await self.client.analyze_poster(image_path, POSTER_EVALUATION_PROMPT)
            
            # Check if response content exists and is not empty
            if not response or "content" not in response:
                print(f"Error: No content in response for {image_path.name}")
                processing_log.status = "failed"
                processing_log.error = "No content in response"
                return None, processing_log

            content = response["content"]
            if not content or content.strip() == "":
                print(f"Error: Empty content in response for {image_path.name}")
                processing_log.status = "failed"
                processing_log.error = "Empty content in response"
                return None, processing_log

            print(f"Raw response content for {image_path.name}: {content[:200]}...")
            
            # Clean the content - extract JSON from markdown code blocks if present
            cleaned_content = self._extract_json_from_content(content)
            
            # Parse JSON response
            try:
                analysis_data = json.loads(cleaned_content)
            except json.JSONDecodeError as json_err:
                print(f"JSON parsing error for {image_path.name}: {str(json_err)}")
                processing_log.status = "failed"
                processing_log.error = f"JSON parsing error: {str(json_err)}"
                return None, processing_log
            
            # Create evaluation object
            evaluation = self._create_evaluation(image_path, analysis_data)
            
            # Calculate final grade based on mode
            evaluation.final_grade = evaluation.calculate_final_grade(mode)
            
            # Update processing log with success info
            processing_log.grade = evaluation.final_grade
            processing_log.duration_ms = int((time.time() - start_time) * 1000)
            
            return evaluation, processing_log
            
        except Exception as e:
            print(f"Error evaluating {image_path.name}: {str(e)}")
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
```

---

## 5. FastAPI Application Implementation

### 5.1 Main FastAPI App (`src/main.py`)

```python
import os
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .evaluator import evaluator
from .processors.output_generator import AsyncOutputGenerator
from .models.poster_data import (
    EvaluationRequest, BatchEvaluationRequest, EvaluationResponse,
    BatchUploadResponse, EvaluationJob, EvaluationMode, ProcessingStatus
)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Poster Evaluation API",
    description="AI-powered academic poster evaluation system using GPT-4 Vision",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File storage configuration
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Ensure directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

def validate_image_file(file: UploadFile) -> bool:
    """Validate uploaded image file"""
    if not file.filename:
        return False
    
    extension = Path(file.filename).suffix.lower()
    return extension in ALLOWED_EXTENSIONS

async def save_uploaded_file(file: UploadFile, job_id: str) -> Path:
    """Save uploaded file to job directory"""
    job_dir = UPLOAD_DIR / job_id
    job_dir.mkdir(exist_ok=True)
    
    file_path = job_dir / file.filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return file_path

async def process_evaluation_job(job_id: str, mode: EvaluationMode):
    """Background task to process evaluation job"""
    try:
        # Get uploaded files for this job
        job_dir = UPLOAD_DIR / job_id
        image_files = [
            f for f in job_dir.iterdir() 
            if f.suffix.lower() in ALLOWED_EXTENSIONS
        ]
        
        if not image_files:
            evaluator.update_job_status(job_id, ProcessingStatus.FAILED)
            return
        
        # Process evaluations
        results = await evaluator.evaluate_batch(job_id, image_files, mode)
        
        # Generate output files
        output_gen = AsyncOutputGenerator(OUTPUT_DIR / job_id, mode.value)
        await output_gen.generate_all_outputs(results, [])
        
    except Exception as e:
        print(f"Error processing job {job_id}: {str(e)}")
        evaluator.update_job_status(job_id, ProcessingStatus.FAILED)

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {"message": "Poster Evaluation API is running", "status": "healthy"}

@app.post("/upload/single", response_model=EvaluationResponse, tags=["Evaluation"])
async def upload_single_poster(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    mode: EvaluationMode = EvaluationMode.FIFTEEN
):
    """Upload and evaluate a single poster"""
    
    if not validate_image_file(file):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only JPG, JPEG, and PNG files are allowed."
        )
    
    # Create job
    job_id = evaluator.create_job(mode, 1)
    
    try:
        # Save file
        await save_uploaded_file(file, job_id)
        
        # Start background processing
        background_tasks.add_task(process_evaluation_job, job_id, mode)
        
        return EvaluationResponse(
            job_id=job_id,
            status=ProcessingStatus.PENDING,
            message="Poster uploaded successfully. Processing started.",
            results_url=f"/jobs/{job_id}/results"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process upload: {str(e)}")

@app.post("/upload/batch", response_model=BatchUploadResponse, tags=["Evaluation"])
async def upload_batch_posters(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    mode: EvaluationMode = EvaluationMode.FIFTEEN
):
    """Upload and evaluate multiple posters"""
    
    if len(files) > 50:  # Reasonable limit
        raise HTTPException(status_code=400, detail="Too many files. Maximum 50 files per batch.")
    
    # Validate files
    valid_files = []
    skipped_files = []
    
    for file in files:
        if validate_image_file(file):
            valid_files.append(file)
        else:
            skipped_files.append(file.filename or "unknown")
    
    if not valid_files:
        raise HTTPException(status_code=400, detail="No valid image files found in upload.")
    
    # Create job
    job_id = evaluator.create_job(mode, len(valid_files))
    
    try:
        # Save files
        for file in valid_files:
            await save_uploaded_file(file, job_id)
        
        # Start background processing
        background_tasks.add_task(process_evaluation_job, job_id, mode)
        
        return BatchUploadResponse(
            job_id=job_id,
            uploaded_files=[f.filename for f in valid_files],
            skipped_files=skipped_files,
            message=f"Batch upload successful. {len(valid_files)} files uploaded, {len(skipped_files)} skipped."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process batch upload: {str(e)}")

@app.get("/jobs/{job_id}", response_model=EvaluationJob, tags=["Jobs"])
async def get_job_status(job_id: str):
    """Get job status and progress"""
    job = evaluator.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job

@app.get("/jobs/{job_id}/results", tags=["Results"])
async def get_job_results(job_id: str):
    """Get job evaluation results"""
    job = evaluator.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status != ProcessingStatus.COMPLETED:
        return JSONResponse(
            status_code=202,
            content={"message": "Job not completed yet", "status": job.status.value}
        )
    
    return {
        "job_id": job_id,
        "status": job.status.value,
        "total_files": job.total_files,
        "processed_files": job.processed_files,
        "results": [result.dict() for result in job.results],
        "errors": job.errors,
        "download_urls": {
            "master_csv": f"/jobs/{job_id}/download/master",
            "run_log": f"/jobs/{job_id}/download/log"
        }
    }

@app.get("/jobs/{job_id}/download/master", tags=["Downloads"])
async def download_master_results(job_id: str):
    """Download master CSV results file"""
    job = evaluator.get_job(job_id)
    if not job or job.status != ProcessingStatus.COMPLETED:
        raise HTTPException(status_code=404, detail="Results not available")
    
    file_path = OUTPUT_DIR / job_id / f"results_master_{job.mode.value}.csv"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Master results file not found")
    
    return FileResponse(
        path=file_path,
        filename=f"results_master_{job.mode.value}.csv",
        media_type="text/csv"
    )

@app.get("/jobs/{job_id}/download/log", tags=["Downloads"])
async def download_run_log(job_id: str):
    """Download run log file"""
    job = evaluator.get_job(job_id)
    if not job or job.status != ProcessingStatus.COMPLETED:
        raise HTTPException(status_code=404, detail="Results not available")
    
    file_path = OUTPUT_DIR / job_id / "run_log.jsonl"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Run log file not found")
    
    return FileResponse(
        path=file_path,
        filename="run_log.jsonl",
        media_type="application/jsonl"
    )

@app.get("/jobs/{job_id}/download/breakdown/{filename}", tags=["Downloads"])
async def download_breakdown_file(job_id: str, filename: str):
    """Download individual poster breakdown JSON file"""
    job = evaluator.get_job(job_id)
    if not job or job.status != ProcessingStatus.COMPLETED:
        raise HTTPException(status_code=404, detail="Results not available")
    
    file_path = OUTPUT_DIR / job_id / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Breakdown file not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/json"
    )

@app.delete("/jobs/{job_id}", tags=["Jobs"])
async def delete_job(job_id: str):
    """Delete job and associated files"""
    job = evaluator.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    try:
        # Remove uploaded files
        upload_dir = UPLOAD_DIR / job_id
        if upload_dir.exists():
            shutil.rmtree(upload_dir)
        
        # Remove output files
        output_dir = OUTPUT_DIR / job_id
        if output_dir.exists():
            shutil.rmtree(output_dir)
        
        # Remove job from memory
        del evaluator.jobs[job_id]
        
        return {"message": "Job deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete job: {str(e)}")

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    try:
        # Check OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        api_key_status = "configured" if api_key else "missing"
        
        # Check directories
        upload_dir_status = "accessible" if UPLOAD_DIR.exists() else "missing"
        output_dir_status = "accessible" if OUTPUT_DIR.exists() else "missing"
        
        return {
            "status": "healthy",
            "api_key": api_key_status,
            "upload_directory": upload_dir_status,
            "output_directory": output_dir_status,
            "active_jobs": len(evaluator.jobs)
        }
        
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### 5.2 Async Output Generator (`src/processors/output_generator.py`)

```python
import json
import asyncio
import aiofiles
import pandas as pd
from pathlib import Path
from typing import List
from ..models.poster_data import PosterEvaluation, ProcessingLog

class AsyncOutputGenerator:
    """Generate all required output files asynchronously"""
    
    def __init__(self, output_dir: Path, mode: str = "fifteen"):
        self.output_dir = output_dir
        self.mode = mode
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def generate_master_results(self, evaluations: List[PosterEvaluation]) -> Path:
        """Generate master CSV results file"""
        filename = f"results_master_{self.mode}.csv"
        filepath = self.output_dir / filename
        
        # Prepare data for CSV
        data = []
        for eval in evaluations:
            data.append({
                "Poster File": eval.poster_file,
                "Final Grade": eval.final_grade,
                "Project Number": eval.Q1 if eval.Q1 else "",
                "Project Summary": eval.poster_summary,
                "Evaluation Summary": eval.evaluation_summary
            })
        
        # Create DataFrame and save
        df = pd.DataFrame(data)
        
        # Use asyncio to write file
        csv_content = df.to_csv(index=False)
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(csv_content)
        
        print(f"Master results saved to: {filepath}")
        return filepath
    
    async def generate_individual_breakdowns(self, evaluations: List[PosterEvaluation]) -> List[Path]:
        """Generate individual JSON breakdown files"""
        breakdown_files = []
        
        async def write_breakdown_file(eval: PosterEvaluation):
            # Determine filename
            if eval.Q1 and eval.Q3:  # Project number and presenter found
                filename = f"{eval.Q1}_{eval.Q3}.json"
            else:
                # Fallback naming
                stem = Path(eval.poster_file).stem
                filename = f"{stem}_Unknown.json"
            
            # Clean filename (remove invalid characters)
            filename = "".join(c for c in filename if c.isalnum() or c in "._-")
            filepath = self.output_dir / filename
            
            # Create JSON data
            json_data = eval.dict()
            
            # Write JSON file asynchronously
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(json_data, indent=2, ensure_ascii=False))
            
            return filepath
        
        # Write all breakdown files concurrently
        tasks = [write_breakdown_file(eval) for eval in evaluations]
        breakdown_files = await asyncio.gather(*tasks)
        
        print(f"Generated {len(breakdown_files)} breakdown files")
        return breakdown_files
    
    async def generate_run_log(self, logs: List[ProcessingLog]) -> Path:
        """Generate JSONL run log file"""
        filepath = self.output_dir / "run_log.jsonl"
        
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            for log in logs:
                await f.write(log.json() + '\n')
        
        print(f"Run log saved to: {filepath}")
        return filepath
    
    async def generate_all_outputs(self, evaluations: List[PosterEvaluation], 
                                 logs: List[ProcessingLog]) -> dict:
        """Generate all output files concurrently"""
        
        # Run all generation tasks concurrently
        master_task = self.generate_master_results(evaluations)
        breakdown_task = self.generate_individual_breakdowns(evaluations)
        log_task = self.generate_run_log(logs)
        
        master_file, breakdown_files, log_file = await asyncio.gather(
            master_task, breakdown_task, log_task
        )
        
        return {
            "master_file": master_file,
            "breakdown_files": breakdown_files,
            "log_file": log_file
        }
```

---

## 6. FastAPI Project Structure

```
poster-evaluation/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── evaluator.py         # Async evaluation engine
│   ├── models/
│   │   ├── __init__.py
│   │   ├── openai_client.py # Async OpenAI client
│   │   ├── poster_data.py   # Pydantic models
│   │   └── prompts.py       # Evaluation prompts
│   ├── processors/
│   │   ├── __init__.py
│   │   └── output_generator.py # Async output generation
│   └── utils/
│       ├── __init__.py
│       └── validators.py    # Input validation
├── uploads/                 # Uploaded poster files (by job_id)
├── outputs/                 # Generated results (by job_id)
├── tests/
│   ├── __init__.py
│   ├── test_api.py         # FastAPI endpoint tests
│   ├── test_evaluator.py   # Evaluation logic tests
│   └── test_integration.py # End-to-end tests
├── requirements.txt
├── .env.example           # Environment template
├── .env                   # Environment variables (gitignored)
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 7. Configuration Management

The application uses environment variables for configuration through a `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1
MAX_TOKENS=4096
TEMPERATURE=0.1
TIMEOUT_SECONDS=30

# FastAPI Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
APP_RELOAD=false
APP_LOG_LEVEL=info

# File Storage Settings
MAX_UPLOAD_SIZE=20971520  # 20MB
MAX_FILES_PER_BATCH=50
CLEANUP_AFTER_DAYS=7

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
```

Key configuration aspects:

1. **OpenAI Integration:**
   - API key management
   - Model selection (GPT-4 Vision)
   - Request parameters (tokens, temperature)

3. **File Processing:**
    - Supported formats: JPG, JPEG, PNG (only these formats are accepted by the API)
    - File size limits
    - Batch processing limits

3. **Evaluation Modes:**
   - FIFTEEN mode: Full evaluation with presence and coherence scores
   - SEVEN mode: Quality-focused evaluation with score scaling

4. **Server Settings:**
   - Host and port configuration
   - CORS policy
   - Development reload settings

---

## 8. FastAPI Testing Strategy

### 8.1 API Endpoint Tests (`tests/test_api.py`)

```python
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import shutil
from src.main import app

client = TestClient(app)

@pytest.fixture
def sample_image():
    """Create a sample image file for testing"""
    # Create a simple test image
    from PIL import Image
    img = Image.new('RGB', (100, 100), color='white')
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        img.save(tmp.name)
        return Path(tmp.name)

@pytest.fixture
def cleanup_uploads():
    """Clean up test uploads after tests"""
    yield
    # Cleanup code here if needed

class TestPosterEvaluationAPI:
    
    def test_health_check(self):
        """Test basic health endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_detailed_health_check(self):
        """Test detailed health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "api_key" in data
    
    def test_upload_single_poster(self, sample_image):
        """Test single poster upload"""
        with open(sample_image, 'rb') as f:
            response = client.post(
                "/upload/single",
                files={"file": ("test.jpg", f, "image/jpeg")},
                data={"mode": "fifteen"}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "pending"
    
    def test_upload_invalid_file(self):
        """Test upload with invalid file type"""
        fake_file = b"not an image"
        response = client.post(
            "/upload/single",
            files={"file": ("test.txt", fake_file, "text/plain")}
        )
        
        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]
    
    def test_job_status_not_found(self):
        """Test job status for non-existent job"""
        response = client.get("/jobs/nonexistent-job-id")
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_batch_upload(self, sample_image):
        """Test batch upload endpoint"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            with open(sample_image, 'rb') as f1, open(sample_image, 'rb') as f2:
                response = await ac.post(
                    "/upload/batch",
                    files=[
                        ("files", ("test1.jpg", f1, "image/jpeg")),
                        ("files", ("test2.jpg", f2, "image/jpeg"))
                    ],
                    data={"mode": "seven"}
                )
        
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert len(data["uploaded_files"]) == 2

class TestJobManagement:
    
    def test_job_lifecycle(self, sample_image):
        """Test complete job lifecycle"""
        # Upload file
        with open(sample_image, 'rb') as f:
            upload_response = client.post(
                "/upload/single",
                files={"file": ("test.jpg", f, "image/jpeg")}
            )
        
        job_id = upload_response.json()["job_id"]
        
        # Check job status
        status_response = client.get(f"/jobs/{job_id}")
        assert status_response.status_code == 200
        
        job_data = status_response.json()
        assert job_data["job_id"] == job_id
        assert job_data["total_files"] == 1
        
        # Note: In real tests, you'd wait for processing or mock it
```

### 8.2 Unit Tests (`tests/test_evaluator.py`)

```python
import pytest
from pathlib import Path
from src.evaluator import PosterEvaluator
from src.models.poster_data import PosterEvaluation

class TestPosterEvaluator:
    
    def test_evaluator_initialization(self):
        evaluator = PosterEvaluator(mode="fifteen")
        assert evaluator.mode == "fifteen"
        assert len(evaluator.results) == 0
    
    def test_grade_calculation_modes(self):
        """Test grade calculation in both modes"""
        evaluation = PosterEvaluation(
            poster_file="test.jpg",
            Q1="23-1-1-1234",  # 2 points in FIFTEEN mode
            Q4=True,           # 2 points in FIFTEEN mode
            Q6=10,             # 10 points in both modes
            Q9=25,             # 25 points in both modes
            Q15=15             # 15 points in FIFTEEN mode only
        )
        
        # Test FIFTEEN mode
        fifteen_grade = evaluation.calculate_final_grade(mode=EvaluationMode.FIFTEEN)
        assert fifteen_grade == 52  # 2+2+10+25+15 (presence + quality + coherence)
        
        # Test SEVEN mode
        seven_grade = evaluation.calculate_final_grade(mode=EvaluationMode.SEVEN)
        assert seven_grade == 46  # (35 * 100) // 75 (scaled quality score)
    
    @pytest.mark.integration
    def test_batch_processing(self, sample_images_dir):
        evaluator = PosterEvaluator(mode="seven")
        results = evaluator.evaluate_batch(sample_images_dir)
        
        assert len(results) > 0
        assert all(isinstance(r, PosterEvaluation) for r in results)
        assert results == sorted(results, key=lambda x: x.final_grade, reverse=True)
```

### 8.3 Integration Tests (`tests/test_integration.py`)

```python
import pytest
from pathlib import Path
import tempfile
from src.main import main
from click.testing import CliRunner

class TestIntegration:
    
    def test_end_to_end_processing(self, sample_images_dir):
        """Test complete processing pipeline"""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            
            runner = CliRunner()
            result = runner.invoke(main, [
                '--input', str(sample_images_dir),
                '--output', str(output_dir),
                '--mode', 'seven'
            ])
            
            assert result.exit_code == 0
            
            # Check output files exist
            assert (output_dir / "results_master_seven.csv").exists()
            assert (output_dir / "run_log.jsonl").exists()
            
            # Check CSV structure
            import pandas as pd
            df = pd.read_csv(output_dir / "results_master_seven.csv")
            assert len(df.columns) == 5
            assert list(df.columns) == [
                "Poster File", "Final Grade", "Project Number", 
                "Project Summary", "Evaluation Summary"
            ]
```

---

## 9. Deployment & Production

### 9.1 Docker Configuration

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Create directories for uploads and outputs
RUN mkdir -p uploads outputs

# Set environment
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  poster-evaluation-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=${OPENAI_MODEL:-gpt-4.1}
      - MAX_TOKENS=${MAX_TOKENS:-4096}
      - TEMPERATURE=${TEMPERATURE:-0.1}
      - TIMEOUT_SECONDS=${TIMEOUT_SECONDS:-30}
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
    
  # Optional: Add nginx for production
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - poster-evaluation-api
    restart: unless-stopped
```

### 9.2 Production Deployment

**Startup Script (`start.sh`):**
```bash
#!/bin/bash

# Production startup script
export PYTHONPATH=/app

# Run database migrations if needed
# python -m alembic upgrade head

# Start the application with Gunicorn for production
exec gunicorn src.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
```

**Environment Variables (`.env.example`):**
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1
MAX_TOKENS=4096
TEMPERATURE=0.1
TIMEOUT_SECONDS=30

# FastAPI Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
APP_RELOAD=false
APP_LOG_LEVEL=info

# File Storage
MAX_UPLOAD_SIZE=20971520  # 20MB
MAX_FILES_PER_BATCH=50
CLEANUP_AFTER_DAYS=7

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
```

### 9.3 API Usage Examples

**Python Client Example:**
```python
import requests
import json
from pathlib import Path

class PosterEvaluationClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def upload_single_poster(self, image_path: Path, mode: str = "fifteen"):
        """Upload and evaluate a single poster"""
        with open(image_path, 'rb') as f:
            files = {"file": (image_path.name, f, "image/jpeg")}
            data = {"mode": mode}
            
            response = requests.post(
                f"{self.base_url}/upload/single",
                files=files,
                data=data
            )
            
        return response.json()
    
    def upload_batch(self, image_paths: list, mode: str = "fifteen"):
        """Upload and evaluate multiple posters"""
        files = []
        for path in image_paths:
            files.append(("files", (path.name, open(path, 'rb'), "image/jpeg")))
        
        data = {"mode": mode}
        
        response = requests.post(
            f"{self.base_url}/upload/batch",
            files=files,
            data=data
        )
        
        # Close file handles
        for _, (_, file_obj, _) in files:
            file_obj.close()
            
        return response.json()
    
    def get_job_status(self, job_id: str):
        """Get job status and progress"""
        response = requests.get(f"{self.base_url}/jobs/{job_id}")
        return response.json()
    
    def get_results(self, job_id: str):
        """Get evaluation results"""
        response = requests.get(f"{self.base_url}/jobs/{job_id}/results")
        return response.json()
    
    def download_master_csv(self, job_id: str, save_path: Path):
        """Download master CSV results"""
        response = requests.get(f"{self.base_url}/jobs/{job_id}/download/master")
        
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
        return False

# Usage example
if __name__ == "__main__":
    client = PosterEvaluationClient()
    
    # Upload single poster
    result = client.upload_single_poster(Path("poster1.jpg"))
    job_id = result["job_id"]
    
    # Check status
    status = client.get_job_status(job_id)
    print(f"Job status: {status['status']}")
    
    # Get results when ready
    if status['status'] == 'completed':
        results = client.get_results(job_id)
        print(f"Processed {len(results['results'])} posters")
```

**JavaScript/Node.js Example:**
```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

class PosterEvaluationClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async uploadSinglePoster(imagePath, mode = 'fifteen') {
        const form = new FormData();
        form.append('file', fs.createReadStream(imagePath));
        form.append('mode', mode);
        
        const response = await axios.post(
            `${this.baseUrl}/upload/single`,
            form,
            { headers: form.getHeaders() }
        );
        
        return response.data;
    }
    
    async getJobStatus(jobId) {
        const response = await axios.get(`${this.baseUrl}/jobs/${jobId}`);
        return response.data;
    }
    
    async getResults(jobId) {
        const response = await axios.get(`${this.baseUrl}/jobs/${jobId}/results`);
        return response.data;
    }
    
    async downloadMasterCsv(jobId, savePath) {
        const response = await axios.get(
            `${this.baseUrl}/jobs/${jobId}/download/master`,
            { responseType: 'stream' }
        );
        
        response.data.pipe(fs.createWriteStream(savePath));
    }
}

// Usage
(async () => {
    const client = new PosterEvaluationClient();
    
    try {
        const result = await client.uploadSinglePoster('poster1.jpg');
        console.log('Upload successful:', result.job_id);
        
        // Poll for completion
        let status;
        do {
            await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds
            status = await client.getJobStatus(result.job_id);
            console.log('Job status:', status.status);
        } while (status.status === 'pending' || status.status === 'processing');
        
        if (status.status === 'completed') {
            const results = await client.getResults(result.job_id);
            console.log('Results:', results.results.length, 'posters evaluated');
        }
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }
})();
```

---

## 10. Troubleshooting Guide

### Common Issues & Solutions

**API Key Issues:**
```bash
# Check API key is set
echo $OPENAI_API_KEY

# Test API access
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models
```

**Image Processing Errors:**
```python
# Validate image format
from PIL import Image
try:
    img = Image.open("poster.jpg")
    print(f"Format: {img.format}, Size: {img.size}")
except Exception as e:
    print(f"Invalid image: {e}")
```

**JSON Parsing Failures:**
- Check GPT-4 response format
- Add response validation
- Implement retry logic for malformed responses

**Output File Issues:**
- Verify write permissions on output directory
- Check filename character restrictions
- Ensure CSV encoding handles special characters
