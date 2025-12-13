"""
Startup script for the Poster Evaluation API
Reads configuration from .env file and starts the server
"""
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read configuration from environment
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
APP_RELOAD = os.getenv("APP_RELOAD", "true").lower() in ("true", "1", "yes")
APP_LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "info")
EVALUATION_APPROACH = os.getenv("EVALUATION_APPROACH", "direct")

if __name__ == "__main__":
    print(f"Starting server on {APP_HOST}:{APP_PORT}")
    print(f"Using evaluation strategy: {EVALUATION_APPROACH}")

    uvicorn.run(
        "src.main:app",
        host=APP_HOST,
        port=APP_PORT,
        reload=APP_RELOAD,
        log_level=APP_LOG_LEVEL
    )
