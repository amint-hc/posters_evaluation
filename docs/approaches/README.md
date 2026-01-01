# Evaluation Approaches

This folder contains documentation about different evaluation approaches used by the Posters Evaluation project. The approaches differ in reasoning methodology, not in the model or evaluation criteria. All use the same 16-question rubric and OpenAI GPT model.

## Evaluation Approaches

### 1. **Direct Approach**
- Single-pass evaluation with direct grading
- Fast (~30-60 seconds), minimal processing overhead
- Output: Scores and summaries

### 2. **Reasoning Approach**
- Single-pass with explanations for each score
- ~40-70 seconds, transparent scoring
- Output: Scores with detailed reasoning

### 3. **Deep Analysis Approach** (Two-Phase)
- Phase 1: Objective evidence collection
- Phase 2: Evidence-based grading
- Most rigorous, ~60-120 seconds
- Output: Evidence documentation and detailed rationale

### 4. **Strict Approach**
- Evidence-first, zero-tolerance grading
- JSON schema validation for scores
- Most deterministic, ~35-65 seconds
- Output: Conservative scores validated to specification

## Shared Model Characteristics

All approaches use identical configuration:
- Model: GPT-5 or newer
- Max Tokens: 4096
- Temperature: 0.0 (consistency)
- Top-p: 1.0
- Presence Penalty: 0.0
- Frequency Penalty: 0.0
- Seed: 42 (reproducibility)
- Timeout: 180 seconds

Differences come from prompt design and processing logic only.

## Rubric: 16-Question Framework

5 categories, 100 points total:
1. Content Quality (25 pts): Q1-Q4
2. Research & Understanding (20 pts): Q5-Q7
3. Visual Quality & Graphs (15 pts): Q8-Q10
4. Structure & Logical Flow (25 pts): Q11-Q14
5. Results & Conclusions (15 pts): Q15-Q16

## Architecture

- **Prompts:** Centralized in `src/models/prompts.py` with PROMPT_REGISTRY
- **Strategies:** Implementation in `src/strategies.py`
- **Client:** AsyncOpenAIVisionClient shared across all approaches

## Configuration

Set approach via environment variable or `.env`:
```
EVALUATION_APPROACH=reasoning  # direct, reasoning, deep_analysis, strict
```
---------------------------------
Summary table: approach ranks and grades (format: rank (grade)).

| Number      | Direct  | Reasoning | Deep Analysis | Strict  |
| ----------- | ------- | --------- | ------------- | ------- |
| 2916        | 1 (87)  | 1 (89)    | 3 (72)        | 1 (100) |
| 22-1-1-2908 | 2 (83)  | 2 (83)    | 10 (53)       | 11 (65) |
| 23-1-1-2732 | 3 (81)  | 3 (81)    | 8 (57)        | 9 (78)  |
| 22-1-1-2729 | 4 (81)  | 4 (81)    | 9 (57)        | 8 (80)  |
| 23-1-1-2849 | 5 (81)  | 5 (81)    | 2 (72)        | 5 (84)  |
| 23-1-1-2826 | 6 (81)  | 6 (81)    | 4 (71)        | 4 (85)  |
| 23-1-2-2850 | 7 (81)  | 7 (81)    | 1 (73)        | 2 (98)  |
| 23-1-1-2745 | 8 (79)  | 8 (79)    | 6 (67)        | 3 (89)  |
| 23-1-1-2883 | 9 (79)  | 9 (79)    | 11 (52)       | 10 (78) |
| 2902        | 10 (79) | 10 (79)   | 5 (69)        | 7 (82)  |
| 2-8-6-2     | 11 (77) | 11 (77)   | 7 (67)        | 6 (82)  |
