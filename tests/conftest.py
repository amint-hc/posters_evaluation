import pytest
import asyncio
import sys
import os
from unittest.mock import Mock, MagicMock
from httpx import AsyncClient
from fastapi.testclient import TestClient

# Set environment variables to help with async testing
os.environ["PYTHONPATH"] = os.path.dirname(os.path.dirname(__file__))
# Set a mock API key for testing
os.environ["OPENAI_API_KEY"] = "test-api-key-for-testing"

from src.main import app

# Fix for Windows + Python 3.8 event loop issues
if sys.platform == "win32" and sys.version_info < (3, 9):
    # Use WindowsSelectorEventLoopPolicy instead of ProactorEventLoopPolicy
    # to avoid wakeup_fd issues
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    if sys.platform == "win32" and sys.version_info < (3, 9):
        # Use SelectorEventLoop on Windows Python 3.8 to avoid threading issues
        loop = asyncio.SelectorEventLoop()
    else:
        loop = asyncio.new_event_loop()
    
    asyncio.set_event_loop(loop)
    yield loop
    
    # Clean shutdown
    try:
        # Cancel all running tasks
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        
        # Wait for all tasks to be cancelled
        if pending:
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        
        loop.close()
    except Exception:
        # If there are issues closing, just pass
        pass

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
async def async_client():
    """Create an async test client for the FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_image_data():
    """Return sample image data for testing."""
    # Create a minimal PNG image data (1x1 pixel)
    import base64
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x12IDATx\x9cc```bPPP\x00\x02\xc4\x00\x01\x85\x1f\xa2\x11\x00\x00\x00\x00IEND\xaeB`\x82'
    return png_data

@pytest.fixture
def sample_config():
    """Return sample configuration for testing."""
    return {
        "openai": {
            "api_key": "test-key",
            "model": "gpt-4-vision-preview",
            "max_tokens": 4096,
            "temperature": 0.1,
            "timeout_seconds": 30
        },
        "processing": {
            "concurrent_requests": 2
        }
    }
