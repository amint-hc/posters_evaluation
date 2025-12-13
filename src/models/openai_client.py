import os
import io 
import json
import aiofiles
import base64
import asyncio
from PIL import Image
from pathlib import Path
from typing import Dict, Any
from openai import AsyncOpenAI

class AsyncOpenAIVisionClient:
    """Async OpenAI GPT-4 Vision client for poster analysis"""
    
    def __init__(self):
        # Get API key from environment - never hardcode API keys in source code
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable. "
                "Copy .env.example to .env and add your API key."
            )
        
        if api_key == "your_openai_api_key_here":
            raise ValueError(
                "Please replace 'your_openai_api_key_here' with your actual OpenAI API key in the .env file."
            )
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.1")
        self.max_completion_tokens = int(os.getenv("MAX_COMPLETION_TOKENS", "16384"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.0"))
        self.seed = int(os.getenv("OPENAI_SEED", "42"))
        self.timeout = int(os.getenv("TIMEOUT_SECONDS", "180"))
        self.evaluation_approach = os.getenv("EVALUATION_APPROACH", "direct").lower()
    
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
                    max_completion_tokens=self.max_completion_tokens,
                    temperature=self.temperature,
                    seed=self.seed
                ),
                timeout=self.timeout
            )
            
            # Debug logging
            content = response.choices[0].message.content
            print(f"OpenAI API response content length: {len(content) if content else 0}")
            print(f"OpenAI API response content preview: {content[:100] if content else 'None'}...")
            
            return {
                "content": content,
                "usage": response.usage.dict() if response.usage else None
            }
            
        except asyncio.TimeoutError:
            raise Exception(f"OpenAI API timeout after {self.timeout} seconds")
        except Exception as e:
            # Handle authentication and other API errors more gracefully
            error_msg = str(e)
            if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                raise Exception("OpenAI API authentication failed. Please check your API key.")
            elif "rate limit" in error_msg.lower():
                raise Exception("OpenAI API rate limit exceeded. Please try again later.")
            else:
                raise Exception(f"OpenAI API error: {error_msg}")

    async def analyze_with_context(self, image_path: Path, prompt: str, context: dict) -> Dict[str, Any]:
        """Analyze image with additional context from Phase 1"""
        try:
            base64_image = await self.encode_image(image_path)
            
            # Format context as readable text
            context_str = json.dumps(context, indent=2)
            
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": prompt
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": f"Here is the detailed analysis of the poster. Use this to assign grades according to the rubric:\n\n{context_str}"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_completion_tokens=self.max_completion_tokens,
                    temperature=self.temperature,
                    seed=self.seed
                ),
                timeout=self.timeout
            )
            
            content = response.choices[0].message.content
            return {
                "content": content,
                "usage": response.usage.dict() if response.usage else None
            }
            
        except asyncio.TimeoutError:
            raise Exception(f"OpenAI API timeout after {self.timeout} seconds")
        except Exception as e:
            raise Exception(f"OpenAI API error in Phase 2: {str(e)}")
