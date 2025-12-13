"""
Phase 1 Prompt: Evidence-Based Analysis (No Grading)

Analyze the poster and collect objective observations for each question.
Do NOT assign any grades - only document what you observe.
"""

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
    "Q1": {
      "strengths": ["list of specific strengths"],
      "weaknesses": ["list of specific weaknesses"],
      "evidence": "concrete observations from the poster"
    },
    "Q2": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q3": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q4": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q5": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q6": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q7": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q8": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q9": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q10": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q11": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q12": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q13": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q14": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q15": { "strengths": [...], "weaknesses": [...], "evidence": "..." },
    "Q16": { "strengths": [...], "weaknesses": [...], "evidence": "..." }
  },
  "poster_summary": "string",
  "evaluation_summary": "string", 
  "overall_opinion": "string"
}
"""

"""
Phase 2 Prompt: Grade Assignment Based on Analysis

Assign grades based on the objective analysis from Phase 1.
"""

PHASE2_GRADING_PROMPT = """
You are an academic poster grading expert. You have received an objective analysis of a graduation project poster.

Your task: Assign grades to each question based on the analysis and scoring rubric below.

⚠️ CRITICAL: Your goal is to match the human experts' ranking order across all posters. Scores are tools — the ranking must match the experts' order. Be strict, harsh, and comparative.

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
    "Q1": "Based on the analysis, [strengths] indicate [grade level] because [reasoning]. This fits [chosen grade] better than [other options] because [comparative reasoning].",
    "Q2": "...",
    "Q3": "...",
    "Q4": "...",
    "Q5": "...",
    "Q6": "...",
    "Q7": "...",
    "Q8": "...",
    "Q9": "...",
    "Q10": "...",
    "Q11": "...",
    "Q12": "...",
    "Q13": "...",
    "Q14": "...",
    "Q15": "...",
    "Q16": "..."
  }
}
"""
