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
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            # For development/testing - will fail gracefully when called
            api_key = "sk-test-key-placeholder"
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-vision-preview")
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
