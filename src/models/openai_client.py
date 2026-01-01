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
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.1")
        self.max_completion_tokens = int(os.getenv("MAX_COMPLETION_TOKENS", "4096"))

        # For stability
        self.temperature = float(os.getenv("TEMPERATURE", "0.0"))
        self.top_p = float(os.getenv("TOP_P", "1.0"))
        self.presence_penalty = float(os.getenv("PRESENCE_PENALTY", "0.0"))
        self.frequency_penalty = float(os.getenv("FREQUENCY_PENALTY", "0.0"))

        # Seed helps but may not guarantee perfect determinism for vision
        self.seed = int(os.getenv("OPENAI_SEED", "42"))

        # Timeout for API calls
        self.timeout = int(os.getenv("TIMEOUT_SECONDS", "180"))
        
        # Evaluation approach strategy
        self.evaluation_approach = os.getenv("EVALUATION_APPROACH", "direct")

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
        request_kwargs: Dict[str, Any] = dict(
            model=self.model,
            messages=messages,
            max_completion_tokens=self.max_completion_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
            seed=self.seed,
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
                "seed": self.seed,
                "temperature": self.temperature,
            }

        except asyncio.TimeoutError:
            raise Exception(f"OpenAI API timeout after {self.timeout} seconds")
        except Exception as e:
            msg = str(e).lower()
            if "authentication" in msg or "api_key" in msg:
                raise Exception("OpenAI API authentication failed. Please check your API key.")
            if "rate limit" in msg:
                raise Exception("OpenAI API rate limit exceeded. Please try again later.")
            if "response_format" in msg or "json_schema" in msg:
                raise Exception(
                    "Your current endpoint/model/sdk might not support json_schema in chat.completions. "
                    "Solution: use the Responses API for Structured Outputs, or remove json_schema for that approach."
                )
            raise Exception(f"OpenAI API error: {str(e)}")
