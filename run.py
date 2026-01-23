"""
Startup script for the Poster Evaluation API with GUI
Starts FastAPI server in background and runs GUI in foreground
"""
import os
import sys
import time
import uvicorn
import threading
import tkinter as tk
from dotenv import load_dotenv

from gui.app import PosterEvaluationGUI

# Load environment variables
load_dotenv()

# Read configuration from environment
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
APP_RELOAD = os.getenv("APP_RELOAD", "false").lower() in ("true", "1", "yes")
APP_LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "info")


def run_server():
    """Run FastAPI server in background thread"""
    try:
        print(f"Starting FastAPI server on {APP_HOST}:{APP_PORT}")
        uvicorn.run(
            "src.main:app",
            host=APP_HOST,
            port=APP_PORT,
            reload=APP_RELOAD,
            log_level=APP_LOG_LEVEL
        )
    except Exception as e:
        print(f"Server error: {e}")


if __name__ == "__main__":
    # Start FastAPI server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Give server a moment to start
    time.sleep(2)
    
    # Run GUI in main thread
    try:
        print("Launching GUI...")
        root = tk.Tk()
        app = PosterEvaluationGUI(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)

    