# Poster Evaluation System

**Graduation Project by:** Mahmoud Masri & Hala Hamood  
**Goal:** Process a batch of 10 poster images and produce ranked results files using AI-powered evaluation.

## Project Overview

This is a **FastAPI-based backend system** that automatically analyzes academic posters using GPT-4 Vision API and produces structured, ranked results. The system provides REST API endpoints for single and batch poster evaluation, with real-time job tracking and multiple output formats.

## Core Requirements

### Primary Functions
1. **REST API Endpoints** for single and batch poster uploads
2. **Async Processing** with job tracking and progress monitoring
3. **AI Evaluation** using GPT-4 Vision against a 15-question rubric
4. **Multiple Output Formats** - CSV, JSON, and JSONL results
5. **Real-time Status Updates** for long-running batch jobs

### Future Deliverables
- Enhanced GUI/web interface
- Dashboard with analytics
- English and Hebrew text handling
- PDF parsing capabilities
- Advanced batch management features

## Input Specifications

### Image Files
- **Supported Formats:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`
- **Input Method:** HTTP multipart file upload via REST API
- **File Size Limit:** 20MB per file
- **Batch Limit:** Up to 50 files per batch upload

### Optional Features
- **Evaluation Modes:** Seven-question vs Fifteen-question analysis
- **Job Management:** Real-time progress tracking for batch jobs  
- **Concurrent Processing:** Rate-limited parallel API calls
- **Auto-cleanup:** Configurable file retention policies

## Output Requirements

### 1. Master Results File (CSV)
**Filename:** `{job_id}_results.csv`

**Columns:**
| Column            | Description                      |
| ----------------- | -------------------------------- |
| filename          | Original filename                |
| title             | Extracted poster title           |
| authors           | Author names                     |
| overall_score     | Integer score [0-100]            |
| individual_scores | JSON object with question scores |
| feedback          | Detailed evaluation text         |

**Sorting:** Rows sorted by overall_score (descending)

### 2. Detailed Results File (JSON)
**Filename:** `{job_id}_results.json`

**JSON Schema:**
```json
{
  "job_id": "job_12345",
  "status": "completed",
  "total_posters": 10,
  "results": [
    {
      "filename": "poster1.png",
      "title": "Machine Learning in Healthcare",
      "authors": "John Doe, Jane Smith",
      "overall_score": 87,
      "individual_scores": {
        "question_1": 9,
        "question_2": 8,
        "..."
      },
      "feedback": "Excellent poster with clear methodology..."
    }
  ]
}
```

### 3. Processing Log (JSONL)
**Filename:** `{job_id}_results.jsonl`

**Format:** One line per poster (JSONL)
```json
{"filename":"poster1.png","status":"completed","score":92,"processing_time_ms":8132,"timestamp":"2025-10-28T10:30:00Z"}
{"filename":"poster2.png","status":"failed","error":"API timeout","timestamp":"2025-10-28T10:31:00Z"}
```

## Scoring System (15-Question Rubric)

The system evaluates posters using a comprehensive 15-question rubric covering:

### Content Quality (60 points)
- **Title and Authorship:** Clear identification and formatting
- **Abstract Quality:** Conciseness and clarity of summary
- **Introduction:** Problem definition and motivation
- **Methodology:** Technical approach and implementation details
- **Results:** Data presentation and visualization quality
- **Conclusions:** Logical derivation from results

### Presentation Quality (40 points)  
- **Visual Design:** Layout, color scheme, and typography
- **Content Organization:** Logical flow and structure
- **Technical Accuracy:** Correctness of information presented
- **Innovation Level:** Novelty and creativity of approach
- **Audience Clarity:** Accessibility to target audience

### Scoring Scale
Each question is scored on a scale appropriate to its weight:
- **Binary questions:** 0 or maximum points
- **Scaled questions:** Multiple score tiers (e.g., 0, 5, 8, 10)
- **Final Score:** Sum of all question scores (0-100 range)

## Technical Specifications

### Architecture
- **Framework:** FastAPI with async processing
- **AI Model:** OpenAI GPT-4 Vision API
- **Database:** In-memory job tracking (Redis recommended for production)
- **File Storage:** Local filesystem with configurable retention
- **Containerization:** Docker with docker-compose for deployment

### API Endpoints
- `POST /upload/single` - Single poster evaluation
- `POST /upload/batch` - Batch poster processing  
- `GET /jobs/{job_id}` - Job status and progress
- `GET /jobs/{job_id}/results` - Download result files
- `GET /health` - Service health check

## Evaluation Modes

### Seven-Question Mode
- **Purpose:** Quick assessment for initial screening
- **Output:** Basic scores and short feedback
- **Processing Time:** ~15-30 seconds per poster

### Fifteen-Question Mode  
- **Purpose:** Comprehensive evaluation with full rubric
- **Output:** Complete question-by-question breakdown
- **Processing Time:** ~30-60 seconds per poster
- **Use Case:** Final grading and detailed feedback

## Current Project Structure

```
poster-evaluation/
├── src/
│   ├── main.py              # FastAPI application
│   ├── evaluator.py         # Core evaluation engine
│   ├── models/
│   │   ├── poster_data.py   # Pydantic data models
│   │   ├── openai_client.py # GPT-4 Vision client
│   │   └── prompts.py       # Evaluation prompts
│   ├── processors/
│   │   └── output_generator.py # Async file generation
│   └── utils/
│       └── validators.py    # File validation
├── tests/                   # Comprehensive test suite
│   ├── test_api.py         # API endpoint tests
│   ├── test_evaluator.py   # Core logic tests
│   └── test_integration.py # End-to-end tests
├── uploads/                 # Temporary file storage
├── outputs/                 # Generated results
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Service orchestration
├── .env.example            # Environment template
└── README.md
```

## Technology Stack

### Primary Language: Python 3.8+

### Core Dependencies
```python
# FastAPI and Web Framework
fastapi>=0.104.0           # Async web framework
uvicorn[standard]>=0.24.0  # ASGI server
python-multipart>=0.0.6   # File upload support

# AI and Image Processing  
openai>=1.3.0              # GPT-4 Vision API
pillow>=10.0.0             # Image processing

# Data Processing
pandas>=2.0.0              # Data manipulation
pydantic>=2.0.0            # Data validation
aiofiles>=23.0.0           # Async file operations

# Configuration and Utilities
python-dotenv>=1.0.0       # Environment variables
pathlib2>=2.3.0            # Path utilities

# Testing and Development
pytest>=7.0.0              # Testing framework
pytest-asyncio>=0.21.0     # Async testing
httpx>=0.25.0              # HTTP client for testing
```

### Architecture Patterns
- **FastAPI Framework:** RESTful API with automatic documentation
- **Async Processing:** Non-blocking I/O for concurrent operations
- **Job Queue Pattern:** Background processing with status tracking
- **Factory Pattern:** Output generators for different formats
- **Repository Pattern:** Data access and file management

## Quality Assurance

### Pre-Delivery Checklist
- [x] FastAPI application with all endpoints implemented
- [x] Single poster evaluation with immediate response
- [x] Batch processing with job tracking
- [x] Multiple output formats (CSV, JSON, JSONL)
- [x] Comprehensive test suite with >90% coverage
- [x] Docker containerization for deployment
- [x] Environment-based configuration
- [x] Error handling and logging
- [x] API documentation with OpenAPI/Swagger
- [ ] Production deployment and monitoring

### Error Handling
- **Async Processing:** Timeout management for API calls
- **File Validation:** Format and size checking
- **Rate Limiting:** OpenAI API constraint handling  
- **Graceful Degradation:** Partial results on failures
- **Comprehensive Logging:** Request tracking and error reporting
- **Job Recovery:** Resume interrupted batch processing

## Security Considerations

- **API Key Protection:** Environment variables and secret management
- **Input Validation:** File type, size, and content sanitization
- **Rate Limiting:** API usage controls and abuse prevention
- **CORS Configuration:** Cross-origin request security
- **File Security:** Temporary file cleanup and access controls
- **Never commit:** API keys, sensitive configuration, or user data

## Acceptance Criteria

**Current Status - COMPLETED:**
1. ✅ FastAPI backend with RESTful endpoints
2. ✅ Single and batch poster processing
3. ✅ Real-time job tracking and progress monitoring  
4. ✅ Multiple output formats (CSV, JSON, JSONL)
5. ✅ GPT-4 Vision integration with 15-question rubric
6. ✅ Comprehensive test suite and validation
7. ✅ Docker containerization and deployment ready
8. ✅ Production-ready error handling and logging

## Usage Examples

### Quick Start
```bash
# 1. Set up environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 2. Configure API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Start the API server  
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 4. Access API documentation
# Visit: http://localhost:8000/docs
```

### API Usage
```bash
# Single poster evaluation
curl -X POST "http://localhost:8000/upload/single" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@poster.png" \
  -F "mode=fifteen"

# Batch processing
curl -X POST "http://localhost:8000/upload/batch" \
  -F "files=@poster1.png" \
  -F "files=@poster2.png" \
  -F "mode=seven"

# Check job status
curl -X GET "http://localhost:8000/jobs/{job_id}"

# Download results
curl -X GET "http://localhost:8000/jobs/{job_id}/results"
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run with environment file
docker build -t poster-evaluation-api .
docker run -p 8000:8000 --env-file .env poster-evaluation-api
```

## Development Status

- **Current Phase:** ✅ **COMPLETED** - Production-ready FastAPI implementation
- **Architecture:** RESTful API with async processing and job management
- **Testing:** Comprehensive test suite with unit, integration, and API tests
- **Deployment:** Docker containerization with docker-compose orchestration
- **Next Phases:** Performance optimization, web interface, advanced analytics

---

**Last Updated:** October 28, 2025  
**Project Team:** Mahmoud Masri & Hala Hamood  
**Status:** ✅ Production Ready - FastAPI Backend Complete
