import json
from pydantic import BaseModel, Field
from typing import Optional, Literal, Union, List
from pathlib import Path
from datetime import datetime
from enum import Enum


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
    
    # Metadata extracted from poster
    project_number: str = ""  # Was Q1
    advisor_name: str = ""    # Was Q2
    presenter_names: str = "" # Was Q3
    
    # Category 1: Content Quality (25 points)
    Q1: Literal[0, 2, 5, 7] = 0   # Intro written well
    Q2: Literal[0, 2, 5, 8] = 0   # Intro relates to topic
    Q3: Literal[0, 1, 3, 5] = 0   # Purpose clear
    Q4: Literal[0, 1, 3, 5] = 0   # Content relevant
    
    # Category 2: Research & Understanding (20 points)
    Q5: Literal[0, 2, 5, 8] = 0   # Deep understanding
    Q6: Literal[0, 2, 4, 6] = 0   # References appropriate
    Q7: Literal[0, 2, 4, 6] = 0   # Methodology clear
    
    # Category 3: Visual Quality & Graphs (15 points)
    Q8: Literal[0, 2, 4, 6] = 0   # Graphs readable
    Q9: Literal[0, 1, 3, 5] = 0   # Graphs meaningful
    Q10: Literal[0, 2, 3, 4] = 0  # Overall visual quality
    
    # Category 4: Structure & Logical Flow (25 points)
    Q11: Literal[0, 1, 3, 5] = 0  # Intro-Motivation connection
    Q12: Literal[0, 3, 7, 10] = 0 # Logical connection
    Q13: Literal[0, 1, 3, 5] = 0  # Consistency
    Q14: Literal[0, 1, 3, 5] = 0  # New info beyond intro
    
    # Category 5: Results & Conclusions (15 points)
    Q15: Literal[0, 2, 5, 7] = 0  # Conclusions connected to results
    Q16: Literal[0, 2, 5, 8] = 0  # Results clear
    
    # Summaries
    poster_summary: str = ""
    evaluation_summary: str = ""
    overall_opinion: str = ""
    
    # Calculated score
    final_grade: int = Field(ge=0, le=100, default=0)
    
    def calculate_final_grade(self) -> int:
        """Calculate final grade from all question scores"""
        return (
            self.Q1 + self.Q2 + self.Q3 + self.Q4 +          # Cat 1 (25)
            self.Q5 + self.Q6 + self.Q7 +                    # Cat 2 (20)
            self.Q8 + self.Q9 + self.Q10 +                   # Cat 3 (15)
            self.Q11 + self.Q12 + self.Q13 + self.Q14 +      # Cat 4 (25)
            self.Q15 + self.Q16                              # Cat 5 (15)
        )

class ProcessingLog(BaseModel):
    """Log entry for processing telemetry"""
    file: str
    status: Literal["ok", "failed"]
    grade: Optional[int] = None
    duration_ms: Optional[int] = None
    error: Optional[str] = None

    def json(self, **kwargs) -> str:
        """Custom JSON serialization to match required format"""
        if self.status == "ok":
            return json.dumps({
                "file": self.file,
                "status": "ok",
                "grade": self.grade,
                "duration_ms": self.duration_ms
            })
        else:
            return json.dumps({
                "file": self.file,
                "status": "failed",
                "error": self.error or "unknown error"
            })

# API Request/Response Models
class EvaluationRequest(BaseModel):
    """Request model for poster evaluation"""
    notification_webhook: Optional[str] = None

class BatchEvaluationRequest(BaseModel):
    """Request model for batch evaluation"""
    notification_webhook: Optional[str] = None

class EvaluationJob(BaseModel):
    """Evaluation job tracking"""
    job_id: str
    status: ProcessingStatus

    created_at: datetime
    updated_at: datetime
    total_files: int
    processed_files: int
    results: List[PosterEvaluation] = []
    errors: List[str] = []
    processing_logs: List[ProcessingLog] = []

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
