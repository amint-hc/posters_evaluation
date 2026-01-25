import os
import shutil
import uuid
from typing import List, Dict
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .evaluator import get_evaluator
from .processors.output_generator import AsyncOutputGenerator
from .models.poster_data import (
    EvaluationResponse,
    BatchUploadResponse, 
    ProcessingStatus,
    EvaluationJob
)

# Initialize FastAPI app
app = FastAPI(
    title="Poster Evaluation API",
    description="AI-powered academic poster evaluation system using GPT-4 Vision",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Server configuration is now in run.py
MAX_FILES_PER_BATCH = int(os.getenv("MAX_FILES_PER_BATCH", "250"))

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# File storage configuration
UPLOAD_DIR = Path("uploads")
DOWNLOAD_DIR = Path("downloads")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Ensure directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Valid Approaches
VALID_APPROACHES = ["direct", "reasoning", "deep_analysis", "strict"]

# Helper functions
def validate_approach(approach: str) -> bool:
    """Validate evaluation approach"""
    return approach in VALID_APPROACHES

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

async def process_evaluation_job(job_id: str, approach: str = "direct"):
    """Background task to process evaluation job
    
    Args:
        job_id: Job identifier
        approach: Evaluation approach to use (direct, reasoning, deep_analysis, strict)
    """
    try:
        # Get uploaded files for this job
        job_dir = UPLOAD_DIR / job_id
        image_files = [
            f for f in job_dir.iterdir() 
            if f.suffix.lower() in ALLOWED_EXTENSIONS
        ]
        
        if not image_files:
            get_evaluator().update_job_status(job_id, ProcessingStatus.FAILED)
            return
        
        # Process evaluations with specified approach
        results = await get_evaluator().evaluate_batch(job_id, image_files, approach)
        
        # Get the job to access processing logs
        job = get_evaluator().get_job(job_id)

        if not job:
            print(f"Job {job_id} not found during processing.")
            return
        
        # Generate download files
        download_gen = AsyncOutputGenerator(DOWNLOAD_DIR / job_id)
        await download_gen.generate_all_outputs(results, job.processing_logs)
        
    except Exception as e:
        print(f"Error processing job {job_id}: {str(e)}")
        get_evaluator().update_job_status(job_id, ProcessingStatus.FAILED)

# API Endpoints
@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {"message": "Poster Evaluation API is running", "status": "healthy"}

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    try:
        # Check OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        api_key_status = "configured" if api_key and api_key != "your_openai_api_key_here" else "missing"
        
        # Check directories
        upload_dir_status = "accessible" if UPLOAD_DIR.exists() else "missing"
        download_dir_status = "accessible" if DOWNLOAD_DIR.exists() else "missing"
        
        # Try to get active jobs count, but don't fail if evaluator can't be created
        try:
            active_jobs = len(get_evaluator().jobs)
        except ValueError:
            # API key not configured properly
            active_jobs = 0
        
        return {
            "status": "healthy",
            "api_key": api_key_status,
            "upload_directory": upload_dir_status,
            "download_directory": download_dir_status,
            "active_jobs": active_jobs
        }
        
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/upload/single", response_model=EvaluationResponse, tags=["Evaluation"])
async def upload_single_poster(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    approach: str = Form("direct")
):
    """Upload and evaluate a single poster"""

    # Validate approach
    if not validate_approach(approach):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid approach '{approach}'. Must be one of: {', '.join(VALID_APPROACHES)}"
        )
    
    if not validate_image_file(file):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only JPG, JPEG, and PNG files are allowed."
        )
    
    # Create job
    job_id = get_evaluator().create_job(1)
    
    try:
        # Save file
        await save_uploaded_file(file, job_id)
        
        # Start background processing
        background_tasks.add_task(process_evaluation_job, job_id, approach)
        
        return EvaluationResponse(
            job_id=job_id,
            status=ProcessingStatus.PENDING,
            message=f"Poster uploaded successfully. Processing started with approach '{approach}'.",
            results_url=f"/jobs/{job_id}/results"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process upload: {str(e)}")

@app.post("/upload/batch", response_model=BatchUploadResponse, tags=["Evaluation"])
async def upload_batch_posters(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(
        ...,
        description="Select multiple poster files to evaluate. Accepts JPG, JPEG, and PNG files.",
        media_type="image/*",
    ),
    approach: str = Form("direct")
):
    """Upload and evaluate multiple posters. Allows selecting multiple files at once.
    
    Args:
        files: List of poster image files
        approach: Evaluation approach to use (direct, reasoning, deep_analysis, strict). Defaults to 'direct'.
    """
    # Validate approach
    if not validate_approach(approach):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid approach '{approach}'. Must be one of: {', '.join(VALID_APPROACHES)}"
        )
    
    if len(files) > MAX_FILES_PER_BATCH:
        raise HTTPException(status_code=400, detail=f"Too many files. Maximum {MAX_FILES_PER_BATCH} files per batch.")

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
    job_id = get_evaluator().create_job(len(valid_files))
    
    try:
        # Save files
        for file in valid_files:
            await save_uploaded_file(file, job_id)
        
        # Start background processing with approach
        background_tasks.add_task(process_evaluation_job, job_id, approach)
        
        return BatchUploadResponse(
            job_id=job_id,
            uploaded_files=[f.filename for f in valid_files],
            skipped_files=skipped_files,
            message=f"Batch upload successful. {len(valid_files)} files uploaded, {len(skipped_files)} skipped. Using '{approach}' approach."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process batch upload: {str(e)}")

@app.get("/jobs/{job_id}", response_model=EvaluationJob, response_model_exclude_none=True, tags=["Jobs"])
async def get_job_status(job_id: str):
    """Get job status and progress"""
    job = get_evaluator().get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job

@app.delete("/jobs/{job_id}", tags=["Jobs"])
async def delete_job(job_id: str):
    """Delete job and associated files"""
    job = get_evaluator().get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    try:
        # Remove uploaded files
        upload_dir = UPLOAD_DIR / job_id
        if upload_dir.exists():
            shutil.rmtree(upload_dir)
        
        # Remove download files
        download_dir = DOWNLOAD_DIR / job_id
        if download_dir.exists():
            shutil.rmtree(download_dir)
        
        # Remove job from memory
        del get_evaluator().jobs[job_id]
        
        return {"message": "Job deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete job: {str(e)}")

@app.get("/jobs/{job_id}/results", tags=["Results"])
async def get_job_results(job_id: str):
    """Get job evaluation results"""
    job = get_evaluator().get_job(job_id)
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
        "results": [result.to_dict() for result in job.results],
        "errors": job.errors,
        "download_urls": {
            "master_csv": f"/jobs/{job_id}/download/master",
            "run_log": f"/jobs/{job_id}/download/log"
        }
    }

@app.get("/jobs/{job_id}/download/master", tags=["Downloads"])
async def download_master_results(job_id: str):
    """Download master CSV results file"""
    job = get_evaluator().get_job(job_id)
    if not job or job.status != ProcessingStatus.COMPLETED:
        raise HTTPException(status_code=404, detail="Results not available")
    
    file_path = DOWNLOAD_DIR / job_id / f"results_master.csv"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Master results file not found")
    
    return FileResponse(
        path=file_path,
        filename=f"results_master.csv",
        media_type="text/csv"
    )

@app.get("/jobs/{job_id}/download/log", tags=["Downloads"])
async def download_run_log(job_id: str):
    """Download run log file"""
    job = get_evaluator().get_job(job_id)
    if not job or job.status != ProcessingStatus.COMPLETED:
        raise HTTPException(status_code=404, detail="Results not available")
    
    file_path = DOWNLOAD_DIR / job_id / "run_log.jsonl"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Run log file not found")
    
    return FileResponse(
        path=file_path,
        filename="run_log.jsonl",
        media_type="application/jsonl"
    )

@app.get("/jobs/{job_id}/download/excel", tags=["Downloads"])
async def download_excel_results(job_id: str):
    """Download Excel results file"""
    job = get_evaluator().get_job(job_id)
    if not job or job.status != ProcessingStatus.COMPLETED:
        raise HTTPException(status_code=404, detail="Results not available")
    
    file_path = DOWNLOAD_DIR / job_id / "results_comparison.xlsx"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Excel results file not found")
    
    return FileResponse(
        path=file_path,
        filename="results_comparison.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.get("/jobs/{job_id}/download/breakdown/{filename}", tags=["Downloads"])
async def download_breakdown_file(job_id: str, filename: str):
    """Download individual poster breakdown JSON file"""
    job = get_evaluator().get_job(job_id)
    if not job or job.status != ProcessingStatus.COMPLETED:
        raise HTTPException(status_code=404, detail="Results not available")
    
    file_path = DOWNLOAD_DIR / job_id / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Breakdown file not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/json"
    )

@app.post("/jobs/compare", tags=["Results"])
async def generate_comparison_report(job_ids: Dict[str, str]):
    """Generate a combined comparison report for multiple jobs"""
    # 1. Validate all jobs exist and are completed
    all_results = {}
    for approach, job_id in job_ids.items():
        if approach not in VALID_APPROACHES:
            continue
            
        job = get_evaluator().get_job(job_id)
        if not job or job.status != ProcessingStatus.COMPLETED:
            raise HTTPException(status_code=400, detail=f"Job {job_id} for {approach} is not completed or not found")
        
        all_results[approach] = {
            r.poster_file: r for r in job.results
        }
    
    if not all_results:
        raise HTTPException(status_code=400, detail="No valid jobs provided for comparison")
    
    # 2. Combine results by poster file
    combined = []
    first_approach_results = list(all_results.values())[0]
    for poster_file in first_approach_results.keys():
        first_result = first_approach_results[poster_file]
        entry = {
            "poster_file": poster_file,
            "project_number": first_result.project_number or "N/A",
            "presenter_names": first_result.presenter_names or "N/A",
        }
        
        for approach in VALID_APPROACHES:
            if approach in all_results and poster_file in all_results[approach]:
                entry[f"{approach}_grade"] = all_results[approach][poster_file].final_grade
            else:
                entry[f"{approach}_grade"] = 0
        
        combined.append(entry)
    
    # 3. Generate Comparison Excel
    # Use a generic job_id/folder for now, or create a unique ID for the comparison
    comp_id = f"comp_{uuid.uuid4().hex[:8]}"
    comp_dir = DOWNLOAD_DIR / comp_id
    comp_dir.mkdir(parents=True, exist_ok=True)
    
    download_gen = AsyncOutputGenerator(comp_dir)
    excel_path = await download_gen.generate_comparison_excel(combined)

    print("excel_path", excel_path)
    
    return {
        "status": "success",
        "comparison_id": comp_id,
        "download_url": f"/downloads/comparison/{comp_id}/results_comparison_all.xlsx",
        "results": combined
    }

@app.get("/downloads/comparison/{comp_id}/{filename}", tags=["Downloads"])
async def download_comparison_file(comp_id: str, filename: str):
    """Serve generated comparison files"""
    file_path = DOWNLOAD_DIR / comp_id / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Comparison file not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
