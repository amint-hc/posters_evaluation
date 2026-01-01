import re
import json
from pathlib import Path
from typing import Dict, Any
from abc import ABC, abstractmethod

from .models.openai_client import AsyncOpenAIVisionClient

def _extract_json_from_text(content: str) -> str:
    """Extract a JSON object from a model response string.

    Handles code fences (```json ... ```) and finds a balanced JSON object by
    scanning for matching braces while respecting string escapes. Returns the
    JSON substring or a best-effort cleaned string if no balanced object found.
    """

    # If there's a fenced code block, prefer its inner content
    fence_match = re.search(r'```(?:json)?\s*(.*?)\s*```', content, re.DOTALL)
    if fence_match:
        content = fence_match.group(1)

    # Trim leading whitespace
    content = content.strip()
    
    # Check if content is empty
    if not content:
        raise ValueError("No content to extract JSON from (empty response)")

    # Find first opening brace
    start = content.find('{')
    if start == -1:
        raise ValueError(f"No JSON object found in response. Content: {content[:100]}")

    depth = 0
    in_string = False
    escape = False

    for idx in range(start, len(content)):
        ch = content[idx]
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return content[start:idx+1].strip()

    # Fallback: return everything from first brace
    return content[start:].strip()

class EvaluationStrategy(ABC):
    """Abstract base class for evaluation strategies"""
    
    @abstractmethod
    async def evaluate(self, client: AsyncOpenAIVisionClient, image_path: Path) -> Dict[str, Any]:
        """Evaluate a poster image and return the data dict"""
        pass

class StrictStrategy(EvaluationStrategy):
    """Strategy for strict evaluation using only questions (single prompt)"""
    
    async def evaluate(self, client: AsyncOpenAIVisionClient, image_path: Path) -> Dict[str, Any]:
        print(f"Starting Strict Evaluation for {image_path.name}...")
        # Ask the client to use the `strict` approach (client maps to prompt/schema)
        response = await client.analyze_poster(image_path, "strict")
        
        if not response or "content" not in response:
            raise Exception("No content in API response")
            
        content = _extract_json_from_text(response["content"])
        return json.loads(content)

class DirectStrategy(EvaluationStrategy):
    """Strategy for evaluating using only questions (single prompt)"""
    
    async def evaluate(self, client: AsyncOpenAIVisionClient, image_path: Path) -> Dict[str, Any]:
        print(f"Starting Direct Evaluation for {image_path.name}...")
        # Use the `direct` approach (client selects prompt from registry)
        response = await client.analyze_poster(image_path, "direct")
        
        if not response or "content" not in response:
            raise Exception("No content in API response")
            
        content = _extract_json_from_text(response["content"])
        return json.loads(content)

    # Extraction handled by module-level helper `_extract_json_from_text`

class ReasoningStrategy(EvaluationStrategy):
    """Strategy for evaluating using questions with explanation (single prompt)"""
    
    async def evaluate(self, client: AsyncOpenAIVisionClient, image_path: Path) -> Dict[str, Any]:
        print(f"Starting Reasoning Evaluation for {image_path.name}...")
        # Use the `reasoning` approach
        response = await client.analyze_poster(image_path, "reasoning")
        
        if not response or "content" not in response:
            raise Exception("No content in API response")
        
        try:
            content = _extract_json_from_text(response["content"])
            return json.loads(content)
        except (ValueError, json.JSONDecodeError) as e:
            raise Exception(f"Failed to parse reasoning JSON for {image_path.name}: {str(e)}")
        
    # Extraction handled by module-level helper `_extract_json_from_text`

class DeepAnalysisStrategy(EvaluationStrategy):
    """Strategy for two-phase evaluation (Analysis then Grading)"""
    
    async def evaluate(self, client: AsyncOpenAIVisionClient, image_path: Path) -> Dict[str, Any]:
        # PHASE 1: Objective Analysis
        print(f"Starting Phase 1 (Analysis) for {image_path.name}...")
        # Phase 1: request objective analysis from the `deep_phase1` prompt
        p1_response = await client.analyze_poster(image_path, "deep_phase1")
        
        if not p1_response or "content" not in p1_response:
            raise Exception("No content in Phase 1 response")
        
        try:
            p1_content = _extract_json_from_text(p1_response["content"])
            analysis_data = json.loads(p1_content)
        except (ValueError, json.JSONDecodeError) as e:
            raise Exception(f"Failed to parse Phase 1 JSON for {image_path.name}: {str(e)}")
            
        print(f"Phase 1 completed for {image_path.name}")
        
        # PHASE 2: Grading based on Analysis
        print(f"Starting Phase 2 (Grading) for {image_path.name}...")
        # Phase 2: grading using the analysis as context via the `deep_phase2` prompt
        p2_response = await client.analyze_poster(
            image_path,
            "deep_phase2",
            context=analysis_data,
        )
        
        if not p2_response or "content" not in p2_response:
            raise Exception("No content in Phase 2 response")
        
        try:
            p2_content = _extract_json_from_text(p2_response["content"])
            grading_data = json.loads(p2_content)
        except (ValueError, json.JSONDecodeError) as e:
            raise Exception(f"Failed to parse Phase 2 JSON for {image_path.name}: {str(e)}")
            
        print(f"Phase 2 completed for {image_path.name}")
        
        # Combine results
        return {**analysis_data, **grading_data}

    # Extraction handled by module-level helper `_extract_json_from_text`

def get_strategy(approach_name: str) -> EvaluationStrategy:
    """Factory to get strategy by name"""
    strategies = {
        "strict": StrictStrategy(),
        "direct": DirectStrategy(),
        "reasoning": ReasoningStrategy(),
        "deep_analysis": DeepAnalysisStrategy()
    }
    
    # Default to direct strategy if unknown
    return strategies.get(approach_name, DirectStrategy())
