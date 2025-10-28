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
