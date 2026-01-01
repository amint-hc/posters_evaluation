# prompts.py
# All prompts and (optional) strict JSON schemas are defined here.
# The OpenAI client can select the correct prompt/schema by approach name.

from typing import Dict, Any


# -----------------------------
# Direct Approach Prompt
# -----------------------------
POSTER_EVALUATION_PROMPT = """
You are a STRICT and CRITICAL academic poster evaluation expert. Analyze this graduation project poster and answer the following questions exactly as specified.

IMPORTANT: Return your response as a valid JSON object with the exact field names specified below.

Analyze the poster and provide:

1. METADATA:
   - Extract "Project Number" (format x-x-x-x) -> field: "project_number"
   - Extract "Advisor Name" -> field: "advisor_name"
   - Extract "Presenter Name(s)" (join with " and ") -> field: "presenter_names"

2. CATEGORY 1: Content Quality (25 points):
   - Q1: Evaluate how clear, informative, and well-structured the introduction is in presenting the project context.
     (Scoring: Excellent=7, Good=5, Weak=2, Poor=0)
   - Q2: Assess the extent to which the introduction establishes a meaningful and logical connection to the poster’s main topic.
     (Scoring: Excellent match=8, Partial match=5, Weak match=2, No match=0)
   - Q3: Evaluate how effectively the poster communicates the project’s main purpose or objective in a direct and understandable way.
     (Scoring: Very clear=5, Clear=3, Partially clear=1, Not clear=0)
   - Q4: Assess the degree to which the content is focused, relevant, and free of unrelated or unnecessary information.
     (Scoring: Fully relevant=5, Mostly relevant=3, Some irrelevant parts=1, Many irrelevant parts=0)

3. CATEGORY 2: Research & Understanding (20 points):
   - Q5: Evaluate how strongly the poster reflects a solid understanding of the topic, concepts, and underlying ideas.
     (Scoring: Excellent understanding=8, Good understanding=5, Basic understanding=2, Weak understanding=0)
   - Q6: Assess how appropriate, up-to-date, and clearly connected the references are to the poster’s content and claims.
     (Scoring: Highly relevant and well-connected=6, Mostly relevant=4, Partially relevant=2, Not relevant=0)
   - Q7: Evaluate how clearly, logically, and sufficiently the methodology or implementation steps are described.
     (Scoring: Very detailed and clear=6, Clear but missing some details=4, Weak or unclear=2, Not described=0)

4. CATEGORY 3: Visual Quality & Graphs (15 points):
   - Q8: Assess the clarity, readability, and labeling quality of the graphs (axes, titles, legends, visibility).
     (Scoring: Excellent clarity=6, Good clarity=4, Low clarity=2, Not clear or missing=0)
   - Q9: Evaluate how effectively the graphs support the poster’s message and add meaningful insights or evidence.
     (Scoring: Highly relevant=5, Moderately relevant=3, Weak relevance=1, Not relevant=0)
   - Q10: Evaluate the overall visual coherence of the poster in terms of layout, spacing, color use, and readability.
     (Scoring: Excellent=4, Good=3, Acceptable=2, Poor=0)

5. CATEGORY 4: Structure & Logical Flow (25 points):
   - Q11: Assess how well the poster builds a logical and meaningful link between the introduction and the motivation.
     (Scoring: Excellent connection=5, Good connection=3, Weak connection=1, No connection=0)
   - Q12: Evaluate the smoothness and clarity of the logical flow between the sections (introduction → methodology → results → conclusions).
     (Scoring: Excellent flow=10, Good flow=7, Weak flow=3, No flow=0)
   - Q13: Evaluate how consistent, aligned, and logically coherent the explanations are across the different poster sections.
     (Scoring: Fully consistent=5, Mostly consistent=3, Some inconsistencies=1, Not consistent=0)
   - Q14: Assess the extent to which the poster adds meaningful and relevant information beyond what is presented in the introduction.
     (Scoring: Adds significant value=5, Adds some value=3, Adds little=1, Adds none=0)

6. CATEGORY 5: Results & Conclusions (15 points):
   - Q15: Evaluate how strongly the conclusions are supported by the results and evidence shown in the poster.
     (Scoring: Strong connection=7, Good connection=5, Weak connection=2, No connection=0)
   - Q16: Assess how clearly and meaningfully the results are presented, interpreted, and explained.
     (Scoring: Excellent clarity=8, Good=5, Partial=2, Weak=0)

7. SUMMARIES:
   - poster_summary: Up to 4 lines describing the project
   - evaluation_summary: Up to 4 lines describing the evaluation
   - overall_opinion: One sentence ending with exactly one of:
     * "The section's explanations in the poster are clear"
     * "The poster contains too much verbal information"
     * "Visual explanation is missing"
     * "The poster visuality is good"

Return response in this exact JSON format:
{
  "project_number": "string",
  "advisor_name": "string",
  "presenter_names": "string",
  "Q1": int, "Q2": int, "Q3": int, "Q4": int,
  "Q5": int, "Q6": int, "Q7": int,
  "Q8": int, "Q9": int, "Q10": int,
  "Q11": int, "Q12": int, "Q13": int, "Q14": int,
  "Q15": int, "Q16": int,
  "poster_summary": "string",
  "evaluation_summary": "string",
  "overall_opinion": "string"
}
""".strip()


# -----------------------------
# Reasoning Approach Prompt
# -----------------------------
POSTER_EVALUATION_WITH_EXPLANATION_PROMPT = """
You are a STRICT and CRITICAL academic poster evaluation expert. Analyze this graduation project poster and answer the following questions exactly as specified.

IMPORTANT: Return your response as a valid JSON object with the exact field names specified below.

For each question:
- Assign ONLY one of the allowed scores in the rubric.
- Give a short explanation that cites visible evidence from the poster.
- If evidence is missing/unclear, choose the lower bracket.

Analyze the poster and provide:

1. METADATA:
   - Extract "Project Number" (format x-x-x-x) -> field: "project_number"
   - Extract "Advisor Name" -> field: "advisor_name" 
   - Extract "Presenter Name(s)" (join with " and ") -> field: "presenter_names"

2. CATEGORY 1: Content Quality (25 points):
   - Q1: Evaluate how clear, informative, and well-structured the introduction is in presenting the project context.
    (Scoring: Excellent=7, Good=5, Weak=2, Poor=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.
   - Q2: Assess the extent to which the introduction establishes a meaningful and logical connection to the poster's main topic.
    (Scoring: Excellent match=8, Partial match=5, Weak match=2, No match=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.
   - Q3: Evaluate how effectively the poster communicates the project's main purpose or objective in a direct and understandable way.
    (Scoring: Very clear=5, Clear=3, Partially clear=1, Not clear=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.
   - Q4: Assess the degree to which the content is focused, relevant, and free of unrelated or unnecessary information.
    (Scoring: Fully relevant=5, Mostly relevant=3, Some irrelevant parts=1, Many irrelevant parts=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.

3. CATEGORY 2: Research & Understanding (20 points):
   - Q5: Evaluate how strongly the poster reflects a solid understanding of the topic, concepts, and underlying ideas.
    (Scoring: Excellent understanding=8, Good understanding=5, Basic understanding=2, Weak understanding=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.
   - Q6: Assess how appropriate, up-to-date, and clearly connected the references are to the poster's content and claims.
    (Scoring: Highly relevant and well-connected=6, Mostly relevant=4, Partially relevant=2, Not relevant=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.
   - Q7: Evaluate how clearly, logically, and sufficiently the methodology or implementation steps are described.
    (Scoring: Very detailed and clear=6, Clear but missing some details=4, Weak or unclear=2, Not described=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.

4. CATEGORY 3: Visual Quality & Graphs (15 points):
   - Q8: Assess the clarity, readability, and labeling quality of the graphs (axes, titles, legends, visibility).
    (Scoring: Excellent clarity=6, Good clarity=4, Low clarity=2, Not clear or missing=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.
   - Q9: Evaluate how effectively the graphs support the poster's message and add meaningful insights or evidence.
    (Scoring: Highly relevant=5, Moderately relevant=3, Weak relevance=1, Not relevant=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.
   - Q10: Evaluate the overall visual coherence of the poster in terms of layout, spacing, color use, and readability.
    (Scoring: Excellent=4, Good=3, Acceptable=2, Poor=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.

5. CATEGORY 4: Structure & Logical Flow (25 points):
   - Q11: Assess how well the poster builds a logical and meaningful link between the introduction and the motivation.
    (Scoring: Excellent connection=5, Good connection=3, Weak connection=1, No connection=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.
   - Q12: Evaluate the smoothness and clarity of the logical flow between the sections (introduction → methodology → results → conclusions).
    (Scoring: Excellent flow=10, Good flow=7, Weak flow=3, No flow=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.
   - Q13: Evaluate how consistent, aligned, and logically coherent the explanations are across the different poster sections.
    (Scoring: Fully consistent=5, Mostly consistent=3, Some inconsistencies=1, Not consistent=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.
   - Q14: Assess the extent to which the poster adds meaningful and relevant information beyond what is presented in the introduction.
    (Scoring: Adds significant value=5, Adds some value=3, Adds little=1, Adds none=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.

6. CATEGORY 5: Results & Conclusions (15 points):
   - Q15: Evaluate how strongly the conclusions are supported by the results and evidence shown in the poster.
    (Scoring: Strong connection=7, Good connection=5, Weak connection=2, No connection=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.
   - Q16: Assess how clearly and meaningfully the results are presented, interpreted, and explained.
    (Scoring: Excellent clarity=8, Good=5, Partial=2, Weak=0)
    Explanation: Identify the reason that led to this grade. Explain why this specific grade was chosen over the other options.

7. SUMMARIES:
   - poster_summary: Up to 4 lines describing the project
   - evaluation_summary: Up to 4 lines describing the evaluation
   - overall_opinion: One sentence ending with exactly one of:
     * "The section's explanations in the poster are clear"
     * "The poster contains too much verbal information"  
     * "Visual explanation is missing"
     * "The poster visuality is good"

Return response in this exact JSON format:
{
  "project_number": "string",
  "advisor_name": "string",
  "presenter_names": "string",
  "Q1": int, "Q2": int, "Q3": int, "Q4": int,
  "Q5": int, "Q6": int, "Q7": int,
  "Q8": int, "Q9": int, "Q10": int,
  "Q11": int, "Q12": int, "Q13": int, "Q14": int,
  "Q15": int, "Q16": int,
  "grade_explanation": {
    "Q1": "string", "Q2": "string", "Q3": "string", "Q4": "string",
    "Q5": "string", "Q6": "string", "Q7": "string",
    "Q8": "string", "Q9": "string", "Q10": "string",
    "Q11": "string", "Q12": "string", "Q13": "string", "Q14": "string",
    "Q15": "string", "Q16": "string"
  },
  "poster_summary": "string",
  "evaluation_summary": "string",
  "overall_opinion": "string"
}
""".strip()


# -----------------------------
# Deep Analysis Approach
# -----------------------------
PHASE1_ANALYSIS_PROMPT = """
You are an objective academic poster analyzer. Your job is to carefully examine this graduation project poster and document FACTUAL OBSERVATIONS for each evaluation criterion.

CRITICAL: Do NOT assign any grades or scores. Only collect evidence.

For each question below, provide:
1. STRENGTHS: What the poster demonstrates well in this area
2. WEAKNESSES: What is missing, unclear, or could be improved
3. EVIDENCE: Specific observations from the poster (cite text, figures, sections)

Analyze the poster and provide:

1. METADATA:
   - Extract "Project Number" (format x-x-x-x) -> field: "project_number"
   - Extract "Advisor Name" -> field: "advisor_name" 
   - Extract "Presenter Name(s)" (join with " and ") -> field: "presenter_names"

2. CATEGORY 1: Content Quality (25 points):
   - Q1: Introduction clarity and structure
     Analysis: How clear, informative, and well-structured is the introduction in presenting the project context?
   
   - Q2: Introduction connection to topic
     Analysis: To what extent does the introduction establish a meaningful and logical connection to the poster's main topic?
   
   - Q3: Purpose communication
     Analysis: How effectively does the poster communicate the project's main purpose or objective?
   
   - Q4: Content relevance
     Analysis: To what degree is the content focused, relevant, and free of unrelated information?

3. CATEGORY 2: Research & Understanding (20 points):
   - Q5: Topic understanding
     Analysis: How strongly does the poster reflect understanding of the topic, concepts, and underlying ideas?
   
   - Q6: References quality
     Analysis: How appropriate, up-to-date, and clearly connected are the references to the poster's content?
   
   - Q7: Methodology description
     Analysis: How clearly, logically, and sufficiently are the methodology or implementation steps described?

4. CATEGORY 3: Visual Quality & Graphs (15 points):
   - Q8: Graph clarity
     Analysis: Assess the clarity, readability, and labeling quality of the graphs (axes, titles, legends, visibility).
   
   - Q9: Graph relevance
     Analysis: How effectively do the graphs support the poster's message and add meaningful insights?
   
   - Q10: Overall visual coherence
     Analysis: Evaluate the overall visual coherence in terms of layout, spacing, color use, and readability.

5. CATEGORY 4: Structure & Logical Flow (25 points):
   - Q11: Introduction-Motivation link
     Analysis: How well does the poster build a logical link between the introduction and the motivation?
   
   - Q12: Section flow
     Analysis: How smooth and clear is the logical flow between sections (introduction → methodology → results → conclusions)?
   
   - Q13: Consistency
     Analysis: How consistent, aligned, and logically coherent are the explanations across different poster sections?
   
   - Q14: Information depth
     Analysis: To what extent does the poster add meaningful information beyond what is presented in the introduction?

6. CATEGORY 5: Results & Conclusions (15 points):
   - Q15: Conclusions support
     Analysis: How strongly are the conclusions supported by the results and evidence shown in the poster?
   
   - Q16: Results clarity
     Analysis: How clearly and meaningfully are the results presented, interpreted, and explained?

7. SUMMARIES:
   - poster_summary: Up to 4 lines describing the project
   - evaluation_summary: Up to 4 lines describing your observations
   - overall_opinion: One sentence ending with exactly one of:
     * "The section's explanations in the poster are clear"
     * "The poster contains too much verbal information"  
     * "Visual explanation is missing"
     * "The poster visuality is good"

Return response in this exact JSON format:
{
  "project_number": "string",
  "advisor_name": "string",
  "presenter_names": "string",
  "question_analysis": {
    "Q1": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q2": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q3": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q4": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q5": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q6": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q7": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q8": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q9": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q10": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q11": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q12": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q13": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q14": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q15": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."},
    "Q16": {"strengths": ["..."], "weaknesses": ["..."], "evidence": "..."}
  },
  "poster_summary": "string",
  "evaluation_summary": "string",
  "overall_opinion": "string"
}
""".strip()


PHASE2_GRADING_PROMPT = """
You are an academic poster grading expert. You have received an objective analysis of a graduation project poster.

HARD RULES:
- Evidence-first, no guessing, no benefit of the doubt.
- If evidence is missing/unclear, choose the lower bracket.
- Use the rubric strictly and consistently.

For each question:
1. Review the STRENGTHS and WEAKNESSES from the analysis
2. Match them against the scoring criteria
3. Select the grade that best fits the evidence
4. Explain why this specific grade was chosen over the other options

SCORING CRITERIA:

CATEGORY 1: Content Quality (25 points)
- Q1: Introduction clarity and structure
  * Excellent (7): Exceptionally clear, comprehensive context, well-organized, engaging
  * Good (5): Clear context, logical structure, minor gaps
  * Weak (2): Vague context, poor structure, hard to follow
  * Poor (0): No clear introduction or context

- Q2: Introduction connection to topic
  * Excellent match (8): Perfect alignment, every element connects, seamless flow
  * Partial match (5): Good connection, some elements loosely related
  * Weak match (2): Tenuous connection, significant gaps
  * No match (0): Introduction unrelated to main topic

- Q3: Purpose communication
  * Very clear (5): Explicit, unambiguous, immediately understandable
  * Clear (3): Stated but requires some inference
  * Partially clear (1): Vague, requires significant interpretation
  * Not clear (0): Purpose unclear or absent

- Q4: Content relevance
  * Fully relevant (5): All content directly supports the topic, no filler
  * Mostly relevant (3): Minor digressions or tangential content
  * Some irrelevant parts (1): Noticeable off-topic sections
  * Many irrelevant parts (0): Significant unrelated content

CATEGORY 2: Research & Understanding (20 points)
- Q5: Topic understanding
  * Excellent understanding (8): Deep mastery, sophisticated concepts, expert-level
  * Good understanding (5): Solid grasp, appropriate depth, minor gaps
  * Basic understanding (2): Surface-level, limited depth
  * Weak understanding (0): Fundamental misunderstandings

- Q6: References quality
  * Highly relevant and well-connected (6): Multiple recent sources, explicitly integrated
  * Mostly relevant (4): Adequate sources, reasonably connected
  * Partially relevant (2): Few sources or weak connections
  * Not relevant (0): No references or irrelevant sources

- Q7: Methodology description
  * Very detailed and clear (6): Comprehensive, reproducible, all steps explained
  * Clear but missing some details (4): Understandable, some gaps
  * Weak or unclear (2): Vague, hard to follow
  * Not described (0): No methodology presented

CATEGORY 3: Visual Quality & Graphs (15 points)
- Q8: Graph clarity
  * Excellent clarity (6): Perfect labeling, highly readable, professional
  * Good clarity (4): Readable, minor label issues
  * Low clarity (2): Hard to read, poor labeling
  * Not clear or missing (0): Illegible or absent

- Q9: Graph relevance
  * Highly relevant (5): Graphs essential to understanding, strong support
  * Moderately relevant (3): Helpful but not critical
  * Weak relevance (1): Tangential or redundant
  * Not relevant (0): Unrelated or decorative only

- Q10: Overall visual coherence
  * Excellent (4): Harmonious, professional layout, optimal spacing
  * Good (3): Clean layout, reasonable organization
  * Acceptable (2): Functional but cluttered or imbalanced
  * Poor (0): Chaotic, unprofessional appearance

CATEGORY 4: Structure & Logical Flow (25 points)
- Q11: Introduction-Motivation link
  * Excellent connection (5): Seamless, explicit, perfectly aligned
  * Good connection (3): Clear but could be stronger
  * Weak connection (1): Loose or implicit
  * No connection (0): Disconnected sections

- Q12: Section flow
  * Excellent flow (10): Smooth transitions, perfect narrative arc
  * Good flow (7): Logical progression, minor jumps
  * Weak flow (3): Disjointed, hard to follow
  * No flow (0): Incoherent organization

- Q13: Consistency
  * Fully consistent (5): Perfect alignment, no contradictions
  * Mostly consistent (3): Minor inconsistencies in terminology or claims
  * Some inconsistencies (1): Noticeable conflicts
  * Not consistent (0): Major contradictions

- Q14: Information depth
  * Adds significant value (5): Substantial new information, deep analysis
  * Adds some value (3): Moderate elaboration beyond intro
  * Adds little (1): Minimal new information
  * Adds none (0): Pure repetition of introduction

CATEGORY 5: Results & Conclusions (15 points)
- Q15: Conclusions support
  * Strong connection (7): Direct evidence, well-supported, convincing
  * Good connection (5): Reasonable support, minor gaps
  * Weak connection (2): Limited evidence, significant leaps
  * No connection (0): Unsupported claims

- Q16: Results clarity
  * Excellent clarity (8): Thorough interpretation, clear presentation
  * Good (5): Understandable, adequate detail
  * Partial (2): Vague or incomplete interpretation
  * Weak (0): Unclear or absent results

Based on the Phase 1 analysis provided, assign grades and explain your reasoning.

Return response in this exact JSON format:
{
  "Q1": int, "Q2": int, "Q3": int, "Q4": int,
  "Q5": int, "Q6": int, "Q7": int,
  "Q8": int, "Q9": int, "Q10": int,
  "Q11": int, "Q12": int, "Q13": int, "Q14": int,
  "Q15": int, "Q16": int,
  "grade_explanation": {
    "Q1": "string", "Q2": "string", "Q3": "string", "Q4": "string",
    "Q5": "string", "Q6": "string", "Q7": "string",
    "Q8": "string", "Q9": "string", "Q10": "string",
    "Q11": "string", "Q12": "string", "Q13": "string", "Q14": "string",
    "Q15": "string", "Q16": "string"
  }
}
""".strip()


# -----------------------------
# Strict Approach Prompt + Schema
# -----------------------------
STRICT_POSTER_EVALUATION_PROMPT = """
You are a STRICT and CRITICAL academic poster evaluation expert.

GOAL
- Produce stable, repeatable scoring for the SAME poster using the SAME rubric.
- Be harsh. High scores are rare and must be justified by clear evidence visible on the poster.
- If evidence is missing/unclear, you MUST choose the lower score bracket.

HARD RULES
1) Evidence-first: For each question, only award a score above the minimum if the required evidence is clearly present on the poster.
2) No guessing: If text is unreadable, missing, or ambiguous, score it as missing/weak (lowest applicable bracket).
3) No “benefit of the doubt”: Default to lower scores unless the poster explicitly earns higher scores.
4) Consistency: Use the SAME interpretation of each bracket across posters. Avoid subjective inflation.
5) Do NOT add any keys outside the provided JSON schema. Output must validate.

SCORING METHOD (IMPORTANT)
- For each Q, internally check: (A) required elements present? (B) clarity/readability? (C) direct linkage to claims?
- If any required element fails, drop to the next lower bracket immediately.
- Only use the top bracket if it is unequivocally excellent.

OUTPUT
Return ONLY a valid JSON object matching the schema (no markdown, no commentary).

------------------------------------------------------------
1) METADATA (extract EXACTLY if present; else empty string)
- "Project Number" (format x-x-x-x) -> project_number
- "Advisor Name" -> advisor_name
- "Presenter Name(s)" -> presenter_names (join with " and ")

------------------------------------------------------------
2) CATEGORY 1: Content Quality (25 points)

Q1 (Intro clarity & structure) (0/2/5/7)
- 7: Intro is clearly labeled (or obvious), readable, concise, and covers: context + problem + motivation.
- 5: Mostly clear but minor issues (slightly verbose OR missing 1 element).
- 2: Hard to follow, disorganized, or missing multiple core elements.
- 0: Intro missing or not readable.

Q2 (Intro-topic alignment) (0/2/5/8)
- 8: Intro explicitly matches the main topic and sets up what is later delivered (no mismatch).
- 5: Mostly aligned but some gaps/mild mismatch.
- 2: Weak alignment; intro is generic or loosely related.
- 0: No alignment / wrong topic.

Q3 (Objective clarity) (0/1/3/5)
- 5: Objective/aim is explicitly stated, specific, and unambiguous.
- 3: Objective is stated but slightly vague/general.
- 1: Objective implied but not clearly stated.
- 0: No objective/aim.

Q4 (Focus & relevance) (0/1/3/5)
- 5: Content is tightly focused; no fluff; every section supports the project.
- 3: Mostly focused; small amount of unrelated/verbose content.
- 1: Noticeable irrelevant parts or excessive filler.
- 0: Many irrelevant parts / poster is bloated and unfocused.

------------------------------------------------------------
3) CATEGORY 2: Research & Understanding (20 points)

Q5 (Understanding & correctness) (0/2/5/8)
- 8: Concepts are correct, well explained, and show depth (not copy-paste superficial).
- 5: Generally correct with moderate depth.
- 2: Basic/hand-wavy understanding; shallow explanations.
- 0: Wrong/confused or no evidence of understanding.

Q6 (References quality & linkage) (0/2/4/6)
- 6: References are credible and clearly connected to claims (citations appear where claims are made OR clear mapping).
- 4: References exist and mostly relevant, but linkage is weak.
- 2: References are generic/dated/unclear relevance.
- 0: No references OR irrelevant.

Q7 (Methodology/implementation clarity) (0/2/4/6)
- 6: Clear steps/pipeline/architecture; enough detail to understand what was done.
- 4: Clear but missing some critical details.
- 2: Vague/unclear steps; hard to reproduce/understand.
- 0: Missing methodology/implementation.

------------------------------------------------------------
4) CATEGORY 3: Visual Quality & Graphs (15 points)

Q8 (Graphs readability & labeling) (0/2/4/6)
- 6: Axes/titles/legends readable; units clear; visuals not blurry; properly labeled.
- 4: Mostly readable; minor labeling/clarity issues.
- 2: Low clarity; labels missing/hard to read.
- 0: No graphs OR unreadable.

Q9 (Graphs relevance to claims) (0/1/3/5)
- 5: Graphs directly support key claims and add real evidence/insight.
- 3: Graphs somewhat support claims but limited insight.
- 1: Graphs are decorative or weakly connected.
- 0: Not relevant / no meaningful support.

Q10 (Layout & visual coherence) (0/2/3/4)
- 4: Excellent hierarchy, spacing, alignment; consistent style; easy to scan.
- 3: Good layout with minor issues.
- 2: Acceptable but cluttered or inconsistent.
- 0: Poor layout; hard to read.

------------------------------------------------------------
5) CATEGORY 4: Structure & Logical Flow (25 points)

Q11 (Intro ↔ Motivation linkage) (0/1/3/5)
- 5: Motivation clearly emerges from intro problem/context; explicit rationale.
- 3: Generally linked but slightly weak.
- 1: Weak linkage; motivation feels generic.
- 0: No linkage.

Q12 (Section-to-section flow) (0/3/7/10)
- 10: Strong logical chain: intro → method → results → conclusion; easy to follow.
- 7: Mostly logical; small jumps.
- 3: Weak flow; reader must infer transitions.
- 0: No flow; sections disconnected or missing.

Q13 (Internal consistency) (0/1/3/5)
- 5: Terminology, claims, and results align; no contradictions.
- 3: Mostly consistent; minor issues.
- 1: Some inconsistencies/conflicts.
- 0: Not consistent.

Q14 (Adds value beyond intro) (0/1/3/5)
- 5: Substantial new, relevant info beyond intro (methods/results/analysis).
- 3: Some added value.
- 1: Adds little beyond intro.
- 0: Adds none.

------------------------------------------------------------
6) CATEGORY 5: Results & Conclusions (15 points)

Q15 (Conclusion supported by evidence) (0/2/5/7)
- 7: Conclusions are directly supported by displayed results; no overclaiming.
- 5: Mostly supported; minor overreach.
- 2: Weak support; conclusions not well tied to results.
- 0: No support / no conclusion.

Q16 (Results presentation & interpretation) (0/2/5/8)
- 8: Results are clearly presented AND interpreted (what they mean, why they matter).
- 5: Clear results but limited interpretation.
- 2: Partial/unclear presentation.
- 0: Missing/unclear results.

------------------------------------------------------------
7) SUMMARIES
- poster_summary: Up to 4 lines describing the project (plain text).
- evaluation_summary: Up to 4 lines describing key strengths/weaknesses (plain text).
- overall_opinion: One sentence ending with EXACTLY ONE of:
  * "The section's explanations in the poster are clear"
  * "The poster contains too much verbal information"
  * "Visual explanation is missing"
  * "The poster visuality is good"
""".strip()


POSTER_EVALUATION_JSON_SCHEMA = {
    "name": "poster_evaluation",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "project_number": {"type": "string"},
            "advisor_name": {"type": "string"},
            "presenter_names": {"type": "string"},

            "Q1": {"type": "integer", "enum": [0, 2, 5, 7]},
            "Q2": {"type": "integer", "enum": [0, 2, 5, 8]},
            "Q3": {"type": "integer", "enum": [0, 1, 3, 5]},
            "Q4": {"type": "integer", "enum": [0, 1, 3, 5]},

            "Q5": {"type": "integer", "enum": [0, 2, 5, 8]},
            "Q6": {"type": "integer", "enum": [0, 2, 4, 6]},
            "Q7": {"type": "integer", "enum": [0, 2, 4, 6]},

            "Q8": {"type": "integer", "enum": [0, 2, 4, 6]},
            "Q9": {"type": "integer", "enum": [0, 1, 3, 5]},
            "Q10": {"type": "integer", "enum": [0, 2, 3, 4]},

            "Q11": {"type": "integer", "enum": [0, 1, 3, 5]},
            "Q12": {"type": "integer", "enum": [0, 3, 7, 10]},
            "Q13": {"type": "integer", "enum": [0, 1, 3, 5]},
            "Q14": {"type": "integer", "enum": [0, 1, 3, 5]},

            "Q15": {"type": "integer", "enum": [0, 2, 5, 7]},
            "Q16": {"type": "integer", "enum": [0, 2, 5, 8]},

            "poster_summary": {"type": "string"},
            "evaluation_summary": {"type": "string"},
            "overall_opinion": {"type": "string"}
        },
        "required": [
            "project_number", "advisor_name", "presenter_names",
            "Q1", "Q2", "Q3", "Q4",
            "Q5", "Q6", "Q7",
            "Q8", "Q9", "Q10",
            "Q11", "Q12", "Q13", "Q14",
            "Q15", "Q16",
            "poster_summary", "evaluation_summary", "overall_opinion"
        ]
    }
}


# Direct Approach Schema
DIRECT_EVALUATION_JSON_SCHEMA = {
    "name": "poster_evaluation_direct",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "project_number": {"type": "string"},
            "advisor_name": {"type": "string"},
            "presenter_names": {"type": "string"},
            "Q1": {"type": "integer"},
            "Q2": {"type": "integer"},
            "Q3": {"type": "integer"},
            "Q4": {"type": "integer"},
            "Q5": {"type": "integer"},
            "Q6": {"type": "integer"},
            "Q7": {"type": "integer"},
            "Q8": {"type": "integer"},
            "Q9": {"type": "integer"},
            "Q10": {"type": "integer"},
            "Q11": {"type": "integer"},
            "Q12": {"type": "integer"},
            "Q13": {"type": "integer"},
            "Q14": {"type": "integer"},
            "Q15": {"type": "integer"},
            "Q16": {"type": "integer"},
            "poster_summary": {"type": "string"},
            "evaluation_summary": {"type": "string"},
            "overall_opinion": {"type": "string"}
        },
        "required": [
            "project_number", "advisor_name", "presenter_names",
            "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7",
            "Q8", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14",
            "Q15", "Q16",
            "poster_summary", "evaluation_summary", "overall_opinion"
        ]
    }
}


# Reasoning Approach Schema
REASONING_EVALUATION_JSON_SCHEMA = {
    "name": "poster_evaluation_reasoning",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "project_number": {"type": "string"},
            "advisor_name": {"type": "string"},
            "presenter_names": {"type": "string"},
            "Q1": {"type": "integer"},
            "Q2": {"type": "integer"},
            "Q3": {"type": "integer"},
            "Q4": {"type": "integer"},
            "Q5": {"type": "integer"},
            "Q6": {"type": "integer"},
            "Q7": {"type": "integer"},
            "Q8": {"type": "integer"},
            "Q9": {"type": "integer"},
            "Q10": {"type": "integer"},
            "Q11": {"type": "integer"},
            "Q12": {"type": "integer"},
            "Q13": {"type": "integer"},
            "Q14": {"type": "integer"},
            "Q15": {"type": "integer"},
            "Q16": {"type": "integer"},
            "grade_explanation": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "Q1": {"type": "string"},
                    "Q2": {"type": "string"},
                    "Q3": {"type": "string"},
                    "Q4": {"type": "string"},
                    "Q5": {"type": "string"},
                    "Q6": {"type": "string"},
                    "Q7": {"type": "string"},
                    "Q8": {"type": "string"},
                    "Q9": {"type": "string"},
                    "Q10": {"type": "string"},
                    "Q11": {"type": "string"},
                    "Q12": {"type": "string"},
                    "Q13": {"type": "string"},
                    "Q14": {"type": "string"},
                    "Q15": {"type": "string"},
                    "Q16": {"type": "string"}
                },
                "required": ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q16"]
            },
            "poster_summary": {"type": "string"},
            "evaluation_summary": {"type": "string"},
            "overall_opinion": {"type": "string"}
        },
        "required": [
            "project_number", "advisor_name", "presenter_names",
            "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7",
            "Q8", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14",
            "Q15", "Q16",
            "grade_explanation",
            "poster_summary", "evaluation_summary", "overall_opinion"
        ]
    }
}


# Deep Analysis Phase 1 Schema
DEEP_PHASE1_JSON_SCHEMA = {
    "name": "poster_analysis_phase1",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "project_number": {"type": "string"},
            "advisor_name": {"type": "string"},
            "presenter_names": {"type": "string"},
            "question_analysis": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "Q1": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q2": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q3": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q4": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q5": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q6": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q7": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q8": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q9": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q10": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q11": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q12": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q13": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q14": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q15": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    },
                    "Q16": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "string"}
                        },
                        "required": ["strengths", "weaknesses", "evidence"]
                    }
                },
                "required": ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q16"]
            },
            "poster_summary": {"type": "string"},
            "evaluation_summary": {"type": "string"},
            "overall_opinion": {"type": "string"}
        },
        "required": [
            "project_number", "advisor_name", "presenter_names",
            "question_analysis",
            "poster_summary", "evaluation_summary", "overall_opinion"
        ]
    }
}


# Deep Analysis Phase 2 Schema
DEEP_PHASE2_JSON_SCHEMA = {
    "name": "poster_grading_phase2",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "Q1": {"type": "integer"},
            "Q2": {"type": "integer"},
            "Q3": {"type": "integer"},
            "Q4": {"type": "integer"},
            "Q5": {"type": "integer"},
            "Q6": {"type": "integer"},
            "Q7": {"type": "integer"},
            "Q8": {"type": "integer"},
            "Q9": {"type": "integer"},
            "Q10": {"type": "integer"},
            "Q11": {"type": "integer"},
            "Q12": {"type": "integer"},
            "Q13": {"type": "integer"},
            "Q14": {"type": "integer"},
            "Q15": {"type": "integer"},
            "Q16": {"type": "integer"},
            "grade_explanation": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "Q1": {"type": "string"},
                    "Q2": {"type": "string"},
                    "Q3": {"type": "string"},
                    "Q4": {"type": "string"},
                    "Q5": {"type": "string"},
                    "Q6": {"type": "string"},
                    "Q7": {"type": "string"},
                    "Q8": {"type": "string"},
                    "Q9": {"type": "string"},
                    "Q10": {"type": "string"},
                    "Q11": {"type": "string"},
                    "Q12": {"type": "string"},
                    "Q13": {"type": "string"},
                    "Q14": {"type": "string"},
                    "Q15": {"type": "string"},
                    "Q16": {"type": "string"}
                },
                "required": ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q16"]
            }
        },
        "required": [
            "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7",
            "Q8", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14",
            "Q15", "Q16",
            "grade_explanation"
        ]
    }
}


# Strict Approach Schema (already defined above)


# -----------------------------
# Registry (shareable)
# -----------------------------
PROMPT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "direct": {
        "prompt": POSTER_EVALUATION_PROMPT,
        "json_schema": DIRECT_EVALUATION_JSON_SCHEMA,
    },
    "reasoning": {
        "prompt": POSTER_EVALUATION_WITH_EXPLANATION_PROMPT,
        "json_schema": REASONING_EVALUATION_JSON_SCHEMA,
    },
    "deep_phase1": {
        "prompt": PHASE1_ANALYSIS_PROMPT,
        "json_schema": DEEP_PHASE1_JSON_SCHEMA,
    },
    "deep_phase2": {
        "prompt": PHASE2_GRADING_PROMPT,
        "json_schema": DEEP_PHASE2_JSON_SCHEMA,
    },
    "strict": {
        "prompt": STRICT_POSTER_EVALUATION_PROMPT,
        "json_schema": POSTER_EVALUATION_JSON_SCHEMA,
    },
}
