import re
import json
from pathlib import Path
from typing import Dict, Any
from abc import ABC, abstractmethod

from .models.openai_client import AsyncOpenAIVisionClient
from .models.prompts.direct import POSTER_EVALUATION_PROMPT
from .models.prompts.reasoning import POSTER_EVALUATION_WITH_EXPLANATION_PROMPT
from .models.prompts.deep_analysis import PHASE1_ANALYSIS_PROMPT, PHASE2_GRADING_PROMPT


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

    # Find first opening brace
    start = content.find('{')
    if start == -1:
        return content

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

class DirectStrategy(EvaluationStrategy):
    """Strategy for evaluating using only questions (single prompt)"""
    
    async def evaluate(self, client: AsyncOpenAIVisionClient, image_path: Path) -> Dict[str, Any]:
        print(f"Starting Direct Evaluation for {image_path.name}...")
        response = await client.analyze_poster(image_path, POSTER_EVALUATION_PROMPT)
        
        if not response or "content" not in response:
            raise Exception("No content in API response")
            
        content = _extract_json_from_text(response["content"])
        return json.loads(content)

    # Extraction handled by module-level helper `_extract_json_from_text`

class ReasoningStrategy(EvaluationStrategy):
    """Strategy for evaluating using questions with explanation (single prompt)"""
    
    async def evaluate(self, client: AsyncOpenAIVisionClient, image_path: Path) -> Dict[str, Any]:
        print(f"Starting Reasoning Evaluation for {image_path.name}...")
        response = await client.analyze_poster(image_path, POSTER_EVALUATION_WITH_EXPLANATION_PROMPT)
        
        if not response or "content" not in response:
            raise Exception("No content in API response")
            
        content = _extract_json_from_text(response["content"])
        return json.loads(content)
        
    # Extraction handled by module-level helper `_extract_json_from_text`

class DeepAnalysisStrategy(EvaluationStrategy):
    """Strategy for two-phase evaluation (Analysis then Grading)"""
    
    async def evaluate(self, client: AsyncOpenAIVisionClient, image_path: Path) -> Dict[str, Any]:
        # PHASE 1: Objective Analysis
        print(f"Starting Phase 1 (Analysis) for {image_path.name}...")
        p1_response = await client.analyze_poster(image_path, PHASE1_ANALYSIS_PROMPT)
        
        if not p1_response or "content" not in p1_response:
            raise Exception("No content in Phase 1 response")
            
        p1_content = _extract_json_from_text(p1_response["content"])
        analysis_data = json.loads(p1_content)
        print(f"Phase 1 completed for {image_path.name}")
        
        # PHASE 2: Grading based on Analysis
        print(f"Starting Phase 2 (Grading) for {image_path.name}...")
        p2_response = await client.analyze_with_context(
            image_path, 
            PHASE2_GRADING_PROMPT,
            context=analysis_data
        )
        
        if not p2_response or "content" not in p2_response:
            raise Exception("No content in Phase 2 response")
            
        p2_content = _extract_json_from_text(p2_response["content"])
        grading_data = json.loads(p2_content)
        print(f"Phase 2 completed for {image_path.name}")
        
        # Combine results
        return {**analysis_data, **grading_data}

    # Extraction handled by module-level helper `_extract_json_from_text`

def get_strategy(approach_name: str) -> EvaluationStrategy:
    """Factory to get strategy by name"""
    strategies = {
        "direct": DirectStrategy(),
        "reasoning": ReasoningStrategy(),
        "deep_analysis": DeepAnalysisStrategy()
    }
    
    # Default to direct strategy if unknown
    return strategies.get(approach_name, DirectStrategy())
