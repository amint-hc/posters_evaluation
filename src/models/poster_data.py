import json
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
    final_grade: int = Field(ge=0, le=100, default=0)
    
    def calculate_final_grade(self, mode: EvaluationMode = EvaluationMode.FIFTEEN) -> int:
        """Calculate final grade from all question scores"""
        quality_score = (self.Q6 + self.Q7 + self.Q8 + self.Q9 + 
                        self.Q11 + self.Q12 + self.Q13)
        
        if mode == EvaluationMode.FIFTEEN:
            presence_score = sum([
                2 if self.Q1 else 0,
                2 if self.Q2 else 0,
                2 if self.Q3 else 0,
                2 if self.Q4 else 0,
                2 if self.Q5 else 0
            ])
            quality_score += self.Q15  # Add Q15 only for FIFTEEN mode
            return presence_score + quality_score
        else:  # SEVEN mode
            return quality_score * 100 // 75  # Scale to 100

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
