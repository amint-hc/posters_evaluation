# 🚀 Poster Evaluation API - Quick Start Guide

## Prerequisites
- Python 3.8+
- OpenAI API key
- Git (optional)

## 📦 Installation

1. **Create virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   ```bash
   cp .env.example .env
   ```

4. **Configure your API key:**
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🧪 Testing

1. **Run validation:**
   ```bash
   python validate.py
   ```

2. **Run test suite:**
   ```bash
   python run_tests.py
   ```

## 🏃‍♂️ Running the API

### Development Mode
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Docker Mode
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t poster-evaluation-api .
docker run -p 8000:8000 --env-file .env poster-evaluation-api
```

## 📖 API Documentation

Once running, visit:
- **Interactive docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health check:** http://localhost:8000/health

## 🎯 Quick API Usage

### Single Poster Evaluation
```bash
curl -X POST "http://localhost:8000/upload/single" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@poster.png" \
  -F "mode=fifteen"
```

### Batch Evaluation
```bash
curl -X POST "http://localhost:8000/upload/batch" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@poster1.png" \
  -F "files=@poster2.png" \
  -F "mode=seven"
```

### Check Job Status
```bash
curl -X GET "http://localhost:8000/jobs/job_12345"
```

## 📁 Project Structure

```
src/
├── main.py              # FastAPI application
├── evaluator.py         # Core evaluation engine
├── models/
│   ├── poster_data.py   # Data models
│   ├── openai_client.py # OpenAI integration
│   └── prompts.py       # Evaluation prompts
├── processors/
│   └── output_generator.py # File generation
└── utils/
    └── validators.py    # File validation

tests/                   # Test suite
uploads/                 # Uploaded files
outputs/                 # Generated results
venv/                    # Virtual environment (created by user)
```

## 🔧 Configuration

Edit `.env` to customize:
- OpenAI model settings
- File processing options
- Output formats
- Evaluation criteria

## 📝 Evaluation Process

1. **Upload** poster images (PNG, JPG, JPEG supported)
2. **Process** with GPT-4 Vision API
3. **Evaluate** using 15-question rubric
4. **Generate** CSV, JSON, and JSONL outputs
5. **Download** results with detailed scores and feedback

## 🎯 Evaluation Criteria

The system evaluates posters on 15 key aspects:
- Title and authorship clarity
- Abstract quality
- Methodology presentation
- Results visualization
- Technical accuracy
- Innovation and impact
- Overall design and readability

## 🛟 Troubleshooting

### Common Issues

1. **Import errors:** Ensure all dependencies are installed
2. **API key errors:** Check your `.env` file configuration
3. **File upload errors:** Verify file format and size limits
4. **Permission errors:** Ensure write access to `uploads/` and `outputs/`

### Log Files

Check `outputs/` directory for:
- Processing logs
- Error reports
- Job status files

## 🚀 Deployment

### Docker Production
```bash
docker-compose -f docker-compose.yml up -d
```

### Cloud Deployment
- Configure environment variables
- Set up persistent storage for uploads/outputs
- Enable HTTPS and security headers
- Monitor API performance and costs

## 📞 Support

For issues and questions:
1. Check the logs in `outputs/`
2. Verify configuration in `.env`
3. Run validation: `python validate.py`
4. Run tests: `python run_tests.py`

---

**✅ Ready to evaluate academic posters at scale!** 🎓📊
