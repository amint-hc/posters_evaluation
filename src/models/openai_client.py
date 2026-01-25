# openai_client.py
import os
import json
import base64
import asyncio
import aiofiles
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from openai import AsyncOpenAI

from src.models.prompts import PROMPT_REGISTRY
from src.exceptions import OpenAIAPIError

class AsyncOpenAIVisionClient:
    """
    Shared async OpenAI client for multiple evaluation approaches.
    No caching.
    Approach selects prompt + optional JSON schema dynamically.
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            raise ValueError("OPENAI_API_KEY not found or invalid.")

        self.client = AsyncOpenAI(api_key=api_key)

        # Model/config
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))

        # For stability
        self.temperature = float(os.getenv("TEMPERATURE", "0.0"))

        # Timeout for API calls
        self.timeout = int(os.getenv("TIMEOUT_SECONDS", "180"))

    async def encode_image(self, image_path: Path) -> str:
        """Read and encode image as base64 string"""
        async with aiofiles.open(image_path, "rb") as f:
            data = await f.read()
        return base64.b64encode(data).decode("utf-8")

    def _get_prompt_and_schema(self, approach: str) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Retrieve prompt and optional JSON schema for the given approach"""
        approach = (approach or "").strip().lower()
        if approach not in PROMPT_REGISTRY:
            raise ValueError(f"Unknown approach '{approach}'. Allowed: {list(PROMPT_REGISTRY.keys())}")

        item = PROMPT_REGISTRY[approach]
        return item["prompt"], item.get("json_schema")

    async def analyze_poster(
        self,
        image_path: Path,
        approach: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze poster with the selected approach.
        - If context provided, it will be appended as text (useful for deep_phase2).
        - Uses strict JSON schema only when approach provides one.
        """

        prompt, json_schema = self._get_prompt_and_schema(approach)
        base64_image = await self.encode_image(image_path)

        user_text = prompt
        if context is not None:
            # Provide context for 2-phase grading etc.
            user_text = (
                f"{prompt}\n\n"
                f"CONTEXT (use as evidence input; do not invent beyond it):\n"
                f"{json.dumps(context, indent=2)}"
            )

        # Build the message payload
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ]

        # response_format: use strict schema only when available
        # Depending on your SDK/model, json_schema may be supported in chat.completions.
        # If your environment errors, switch this call to responses.create.
        
        # Adjust max_tokens based on approach complexity
        max_tokens = self.max_tokens
        if approach in ("deep_phase1", "deep_phase2"):
            # These approaches generate more complex JSON with 16 questions
            max_tokens = max(max_tokens, 6000)
        
        request_kwargs: Dict[str, Any] = dict(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=self.temperature,
        )

        if json_schema is not None:
            request_kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": json_schema,
            }
        else:
            # still ask for JSON, but not strict schema-enforced
            request_kwargs["response_format"] = {"type": "json_object"}

        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(**request_kwargs),
                timeout=self.timeout,
            )

            content = response.choices[0].message.content or ""

            return {
                "content": content,
                "usage": response.usage.dict() if response.usage else None,
                "approach": approach,
                "model": self.model,
                "temperature": self.temperature,
            }

        except asyncio.TimeoutError:
            raise OpenAIAPIError(f"OpenAI API timeout after {self.timeout} seconds")
        except Exception as e:
            msg = str(e).lower()
            if "authentication" in msg or "api_key" in msg:
                raise OpenAIAPIError("OpenAI API authentication failed. Please check your API key.")
            if "rate limit" in msg:
                raise OpenAIAPIError("OpenAI API rate limit exceeded. Please try again later.")
            if "response_format" in msg or "json_schema" in msg:
                raise OpenAIAPIError(
                    "Your current endpoint/model/sdk might not support json_schema in chat.completions. "
                    "Solution: use the Responses API for Structured Outputs, or remove json_schema for that approach."
                )
            # Treat any other API exception as a critical error
            raise OpenAIAPIError(f"OpenAI API error: {str(e)}")
