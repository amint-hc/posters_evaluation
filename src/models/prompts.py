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
You are a HARSH and SKEPTICAL academic poster evaluation expert.
Your goal is to expose weaknesses. High scores are RARE (top 5%).
Most posters should fall in the middle or low range.

CRITICAL SCORING RULES:
1. START AT ZERO for every question. The poster must EARN every point with visible evidence.
2. NO "Benefit of the Doubt". If something is vague, it is BAD.
3. If a required element is missing, the score is AUTOMATICALLY the lowest option.
4. "Good" means PERFECT compliance. "Excellent" means EXCEPTIONAL, publication-ready quality.

Rubric Application:
- If text is too small to read casually -> Score lowest on readability.
- If graphs have no axis labels -> Score lowest on graphs.
- If intro is a wall of text -> Score lowest on structure.

OUTPUT: Return ONLY valid JSON matching the schema.

------------------------------------------------------------
1) METADATA (extract EXACTLY if present; else empty string)
- "Project Number" (format x-x-x-x) -> project_number
- "Advisor Name" -> advisor_name
- "Presenter Name(s)" -> presenter_names (join with " and ")

------------------------------------------------------------
2) CATEGORY 1: Content Quality (25 points)

Q1 (Intro clarity & structure) (0/2/5/7)
- 7: (Rare) flawless hook, clear gap, concise.
- 5: Standard intro, covers basics but maybe dry/verbose.
- 2: Hard to follow, missing motivation, or "wall of text".
- 0: Missing or incoherent.
Explanation: Cite specific text or lack thereof.

Q2 (Intro-topic alignment) (0/2/5/8)
- 8: (Rare) Tightly coupled constraint/solution match.
- 5: Generally related but vague connection.
- 2: Generic intro could apply to any project in this field.
- 0: Irrelevant.
Explanation: Quote the intro claim and the main topic to show mismatch.

Q3 (Objective clarity) (0/1/3/5)
- 5: "The goal is X to achieve Y". Crystal clear.
- 3: Buried in text but findable.
- 1: Vague "we worked on..." statement.
- 0: Missing.
Explanation: Quote the objective sentence.

Q4 (Focus & relevance) (0/1/3/5)
- 5: Every sentence adds value. Dense signal.
- 3: Some fluff/filler text.
- 1: Distracting tangents or basic textbook definitions.
- 0: Bloated/Off-topic.
Explanation: Identify specific irrelevant sections.

------------------------------------------------------------
3) CATEGORY 2: Research & Understanding (20 points)

Q5 (Understanding & correctness) (0/2/5/8)
- 8: Nuanced discussion of trade-offs/limitations.
- 5: Correct textbook application.
- 2: Buzzword soup or surface-level claims.
- 0: Factually wrong.
Explanation: Point out specific technical errors or shallowness.

Q6 (References quality & linkage) (0/2/4/6)
- 6: Specific papers cited to justify design choices.
- 4: Generic list of URLs or books.
- 2: Old/irrelevant sources.
- 0: None.
Explanation: Critique the quality of the bibliography.

Q7 (Methodology/implementation clarity) (0/2/4/6)
- 6: I could reproduce this from the poster alone.
- 4: High-level block diagram but missing specifics.
- 2: Magic black box "we used AI".
- 0: Missing.
Explanation: List missing technical details (e.g. "Model architecture not specified").

------------------------------------------------------------
4) CATEGORY 3: Visual Quality & Graphs (15 points)

Q8 (Graphs readability & labeling) (0/2/4/6)
- 6: Self-contained caption, units on axes, clear legend.
- 4: Missing one element (e.g. units) or slightly small font.
- 2: Screenshot of a UI or unreadable plot.
- 0: None / Blurry artifact.
Explanation: Mention specific graphs that are hard to read.

Q9 (Graphs relevance to claims) (0/1/3/5)
- 5: Graph PROVES the conclusion.
- 3: Graph shows data but link to claim is weak.
- 1: Decorative stock photo or irrelevant chart.
- 0: None.
Explanation: Explain why graphs fail to support claims.

Q10 (Layout & visual coherence) (0/2/3/4)
- 4: Professional design, breathing room, aligns to grid.
- 3: Standard template, readable.
- 2: Cluttered, inconsistent fonts, alignment errors.
- 0: MS Word screenshot looking.
Explanation: Critique layout choices (e.g. "Text overlaps images").

------------------------------------------------------------
5) CATEGORY 4: Structure & Logical Flow (25 points)

Q11 (Intro ↔ Motivation linkage) (0/1/3/5)
- 5: Problem -> Why it matters -> Solution. Seamless.
- 3: Connected but jumps around.
- 1: Motivation feels tacked on.
- 0: Disconnected.
Explanation: Explain the logical gap.

Q12 (Section-to-section flow) (0/3/7/10)
- 10: Story-telling. I never have to hunt for "what's next".
- 7: Standard linear academic sectioning.
- 3: Jumping back and forth, confusing flow.
- 0: Random scattering of boxes.
Explanation: Describe the reading path difficulty.

Q13 (Internal consistency) (0/1/3/5)
- 5: Numbers/Claims match everywhere.
- 3: Minor typo/mismatches.
- 1: Abstract says X, Results say Y.
- 0: Contradictory.
Explanation: Point out specific contradictions.

Q14 (Adds value beyond intro) (0/1/3/5)
- 5: Deep technical details in method/results.
- 3: Rephrasing of intro in more words.
- 1: Just high-level marketing fluff.
- 0: Empty.
Explanation: Assess information density.

------------------------------------------------------------
6) CATEGORY 5: Results & Conclusions (15 points)

Q15 (Conclusion supported by evidence) (0/2/5/7)
- 7: "We achieved X% impovement" backed by Table 1.
- 5: "We built a good system" (subjective but plausible).
- 2: Overclaiming "Perfect accuracy" without proof.
- 0: No conclusion or unrelated to results.
Explanation: Quote the conclusion and check against results.

Q16 (Results presentation & interpretation) (0/2/5/8)
- 8: Clear metrics (Accuracy, latency, etc) + Context ("Better than X").
- 5: Raw numbers without context.
- 2: "It works" screenshots only.
- 0: Missing.
Explanation: meaningful interpretation of results.

------------------------------------------------------------
7) SUMMARIES
- poster_summary: Plain text description.
- evaluation_summary: BRUTAL critique. Focus on WHY points were lost.
- overall_opinion: One sentence ending with EXACTLY ONE of:
  * "The section's explanations in the poster are clear"
  * "The poster contains too much verbal information"
  * "Visual explanation is missing"
  * "The poster visuality is good"
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
You are a HARSH and SKEPTICAL academic poster evaluation expert.
You have received an objective analysis of a graduation project poster.
Your goal is to expose weaknesses. High scores are RARE (top 5%).
Most posters should fall in the middle or low range.

CRITICAL SCORING RULES:
1. START AT ZERO for every question. The poster must EARN every point with visible evidence.
2. NO "Benefit of the Doubt". If something is vague, it is BAD.
3. If a required element is missing, the score is AUTOMATICALLY the lowest option.
4. "Good" means PERFECT compliance. "Excellent" means EXCEPTIONAL, publication-ready quality.

Rubric Application:
- If text is too small to read casually -> Score lowest on readability.
- If graphs have no axis labels -> Score lowest on graphs.
- If intro is a wall of text -> Score lowest on structure.

OUTPUT: Return ONLY valid JSON matching the schema.

For each question:
1. Review the STRENGTHS and WEAKNESSES from the Phase 1 analysis.
2. If ANY weakness is listed that corresponds to a scoring deduction, APPLY IT.
3. Select the grade that best fits the evidence strictly (always round down).

SCORING CRITERIA:

CATEGORY 1: Content Quality (25 points)
- Q1: Introduction clarity and structure
  * Excellent (7): (Rare) flawless hook, clear gap, concise.
  * Good (5): Standard intro, covers basics but maybe dry/verbose.
  * Weak (2): Hard to follow, missing motivation, or "wall of text".
  * Poor (0): Missing or incoherent.

- Q2: Introduction connection to topic
  * Excellent match (8): (Rare) Tightly coupled constraint/solution match.
  * Partial match (5): Generally related but vague connection.
  * Weak match (2): Generic intro could apply to any project in this field.
  * No match (0): Irrelevant.

- Q3: Purpose communication
  * Very clear (5): "The goal is X to achieve Y". Crystal clear.
  * Clear (3): Buried in text but findable.
  * Partially clear (1): Vague "we worked on..." statement.
  * Not clear (0): Missing.

- Q4: Content relevance
  * Fully relevant (5): Every sentence adds value. Dense signal.
  * Mostly relevant (3): Some fluff/filler text.
  * Some irrelevant parts (1): Distracting tangents or basic textbook definitions.
  * Many irrelevant parts (0): Bloated/Off-topic.

CATEGORY 2: Research & Understanding (20 points)
- Q5: Topic understanding
  * Excellent understanding (8): Nuanced discussion of trade-offs/limitations.
  * Good understanding (5): Correct textbook application.
  * Basic understanding (2): Buzzword soup or surface-level claims.
  * Weak understanding (0): Factually wrong.

- Q6: References quality
  * Highly relevant and well-connected (6): Specific papers cited to justify design choices.
  * Mostly relevant (4): Generic list of URLs or books.
  * Partially relevant (2): Old/irrelevant sources.
  * Not relevant (0): None.

- Q7: Methodology description
  * Very detailed and clear (6): I could reproduce this from the poster alone.
  * Clear but missing some details (4): High-level block diagram but missing specifics.
  * Weak or unclear (2): Magic black box "we used AI".
  * Not described (0): Missing.

CATEGORY 3: Visual Quality & Graphs (15 points)
- Q8: Graph clarity
  * Excellent clarity (6): Self-contained caption, units on axes, clear legend.
  * Good clarity (4): Missing one element (e.g. units) or slightly small font.
  * Low clarity (2): Screenshot of a UI or unreadable plot.
  * Not clear or missing (0): None / Blurry artifact.

- Q9: Graph relevance
  * Highly relevant (5): Graph PROVES the conclusion.
  * Moderately relevant (3): Graph shows data but link to claim is weak.
  * Weak relevance (1): Decorative stock photo or irrelevant chart.
  * Not relevant (0): None.

- Q10: Overall visual coherence
  * Excellent (4): Professional design, breathing room, aligns to grid.
  * Good (3): Standard template, readable.
  * Acceptable (2): Cluttered, inconsistent fonts, alignment errors.
  * Poor (0): MS Word screenshot looking.

CATEGORY 4: Structure & Logical Flow (25 points)
- Q11: Introduction-Motivation link
  * Excellent connection (5): Problem -> Why it matters -> Solution. Seamless.
  * Good connection (3): Connected but jumps around.
  * Weak connection (1): Motivation feels tacked on.
  * No connection (0): Disconnected.

- Q12: Section flow
  * Excellent flow (10): Story-telling. I never have to hunt for "what's next".
  * Good flow (7): Standard linear academic sectioning.
  * Weak flow (3): Jumping back and forth, confusing flow.
  * No flow (0): Random scattering of boxes.

- Q13: Consistency
  * Fully consistent (5): Numbers/Claims match everywhere.
  * Mostly consistent (3): Minor typo/mismatches.
  * Some inconsistencies (1): Abstract says X, Results say Y.
  * Not consistent (0): Contradictory.

- Q14: Information depth
  * Adds significant value (5): Deep technical details in method/results.
  * Adds some value (3): Rephrasing of intro in more words.
  * Adds little (1): Just high-level marketing fluff.
  * Adds none (0): Empty.

CATEGORY 5: Results & Conclusions (15 points)
- Q15: Conclusions support
  * Strong connection (7): "We achieved X% impovement" backed by Table 1.
  * Good connection (5): "We built a good system" (subjective but plausible).
  * Weak connection (2): Overclaiming "Perfect accuracy" without proof.
  * No connection (0): No conclusion or unrelated to results.

- Q16: Results clarity
  * Excellent clarity (8): Clear metrics (Accuracy, latency, etc) + Context ("Better than X").
  * Good (5): Raw numbers without context.
  * Partial (2): "It works" screenshots only.
  * Weak (0): Missing.

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
You are a HARSH and SKEPTICAL academic poster evaluation expert.
Your goal is to expose weaknesses. High scores are RARE (top 5%).
Most posters should fall in the middle or low range.

CRITICAL SCORING RULES:
1. START AT ZERO for every question. The poster must EARN every point with visible evidence.
2. NO "Benefit of the Doubt". If something is vague, it is BAD.
3. If a required element is missing, the score is AUTOMATICALLY the lowest option.
4. "Good" means PERFECT compliance. "Excellent" means EXCEPTIONAL, publication-ready quality.
5. PENALIZE DENSITY: "Wall of text" or excessive verbosity must receive LOW scores in Q1, Q4, and Q10.

CRITICAL RED FLAGS (MANDATORY PENALTIES):
- TITLE MISMATCH: If the Title contradicts the Body (bait-and-switch), Q2 and Q13 MUST be 0.
- EVIDENCE GAP: If Results contain NO numerical metrics, NO tables, and NO statistical comparisons (qualitative/screenshots ONLY), Q15 and Q16 MUST be SCORED 0 or 2. Having many screenshots does NOT substitute for metrics.
- RECOGNITION ONLY: If the "Methodology" is just a list of software used (e.g., "We used Python and TensorFlow") without describing the actual ALGORITHM or architecture, Q7 MUST be <= 2.

OUTPUT: Return ONLY valid JSON matching the schema.

------------------------------------------------------------
1) METADATA (extract EXACTLY if present; else empty string)
- "Project Number" (format x-x-x-x) -> project_number
- "Advisor Name" -> advisor_name
- "Presenter Name(s)" -> presenter_names (join with " and ")

------------------------------------------------------------
2) CATEGORY 1: Content Quality (25 points)

Q1 (Intro clarity & structure) (0/1/3/5/7)
- 7: (Rare) Flawless hook, clear gap, concise, minimal text. High signal-to-noise.
- 5: Standard intro, well-structured, easy to read.
- 3: Dense/Verbose or slightly unstructured, but understandable.
- 1: "Wall of text", hard to follow, or missing motivation.
- 0: Missing or incoherent.

Q2 (Intro-topic alignment) (0/2/5/8)
- 8: (Rare) Tightly coupled constraint/solution match.
- 5: Generally related.
- 2: Generic intro or weak link between title and content.
- 0: MISMATCH: Title and content are about different things.

Q3 (Objective clarity) (0/1/3/5)
- 5: "The goal is X to achieve Y". Crystal clear and EXPLICIT.
- 3: Buried in text but findable.
- 1: Vague "we worked on..." statement.
- 0: Missing.

Q4 (Focus & relevance) (0/1/3/5)
- 5: Every sentence adds value. No fluff. No basic textbook definitions.
- 3: some fluff/filler text (e.g. general background that isn't project-specific).
- 1: Distracting tangents or mostly generic content.
- 0: Bloated/Off-topic.

------------------------------------------------------------
3) CATEGORY 2: Research & Understanding (20 points)

Q5 (Understanding & correctness) (0/2/5/8)
- 8: Nuanced discussion of trade-offs/limitations/alternatives. Proves deep expertise.
- 5: Correct application of concepts to THIS project. Basic competence shown.
- 2: Generic "textbook" definitions or buzzword soup without project-specific insight.
- 0: Factually wrong.

Q6 (References quality & linkage) (0/2/4/6)
- 6: Relevant academic reference(s) included and visibly cited in text.
- 4: List of URLs or general books without specific papers.
- 2: Old/irrelevant sources or completely generic.
- 0: None.

Q7 (Methodology/implementation clarity) (0/2/4/6)
- 6: Exceptionally detailed. I could reproduce this from the poster alone.
- 4: High-level block diagram/pipeline but missing parameters/specifics.
- 2: Magic black box "we used AI" or generic list of steps/software.
- 0: Missing.

------------------------------------------------------------
4) CATEGORY 3: Visual Quality & Graphs (15 points)

Q8 (Graphs readability & labeling) (0/2/4/6)
- 6: Professional: big font, clear axis labels, units, legends. Self-contained.
- 4: Minor issues: missing one unit or slightly small font.
- 2: Hard to read, pixelated, missing axes, or UI screenshots instead of data plots.
- 0: None / Blurry artifact.

Q9 (Graphs relevance to claims) (0/1/3/5)
- 5: Graph PROVES the main conclusion quantitatively (e.g., Accuracy vs Baseline).
- 3: Graph shows data but link to claim is weak/qualitative.
- 1: Decorative stock photo or irrelevant chart.
- 0: None.

Q10 (Layout & visual coherence) (0/2/3/4)
- 4: Professional design, breathing room, perfect alignment, consistent style.
- 3: Standard template, readable, mostly aligned.
- 2: Cluttered, inconsistent fonts, alignment errors, text heavy ("Wall of text").
- 0: MS Word screenshot looking or chaotic mess.

------------------------------------------------------------
5) CATEGORY 4: Structure & Logical Flow (25 points)

Q11 (Intro ↔ Motivation linkage) (0/1/3/5)
- 5: Problem -> Why it matters -> Solution. Seamless logical chain.
- 3: Connected but jumps around or motivation is generic.
- 1: Motivation feels tacked on or repetitive.
- 0: Disconnected.

Q12 (Section-to-section flow) (0/3/7/10)
- 10: Story-telling. Natural progression. No "hunting" for the next section.
- 7: Standard linear academic sectioning (Intro->Method->Results).
- 3: Jumping back and forth, confusing flow, or non-standard order.
- 0: Random scattering of boxes.

Q13 (Internal consistency) (0/1/3/5)
- 5: Numbers/Claims match everywhere. Title matches content.
- 3: Minor typos or slight mismatches in data representation.
- 1: Abstract/Title says X, Results/Body say Y.
- 0: Contradictory or Bait-and-Switch title.

Q14 (Adds value beyond intro) (0/1/3/5)
- 5: Substantial technical details in body (formulas, architecture, parameters).
- 3: Rephrasing of intro in more words; minimal new technical info.
- 1: Just high-level marketing fluff or very shallow implementation detail.
- 0: Empty.

------------------------------------------------------------
6) CATEGORY 5: Results & Conclusions (15 points)

Q15 (Conclusion supported by evidence) (0/2/5/7)
- 7: "We achieved X% improvement" backed by statistical analysis or direct comparison.
- 5: Supported by concrete numerical data/metrics shown in results.
- 2: Qualitative/Subjective ONLY ("it works", "user-friendly") - NO NUMBERS.
- 0: No conclusion or unrelated to results.

Q16 (Results presentation & interpretation) (0/2/5/8)
- 8: Clear metrics + Comparisons/Baselines (e.g., Table comparing to State-of-the-Art).
- 5: Raw numbers/tables/graphs with quantitative data.
- 2: VISUAL ONLY (Gallery of screenshots/colors/images) - NO METRICS.
- 0: Missing.

------------------------------------------------------------
7) SUMMARIES & LOGIC CHECK
- poster_summary: Plain text description.
- evaluation_summary: BRUTAL critique. Focus on WHY points were lost.
- overall_opinion: One sentence ending with EXACTLY ONE of:
  * "The section's explanations in the poster are clear"
  * "The poster contains too much verbal information"
  * "Visual explanation is missing"
  * "The poster visuality is good"

FINAL RULE: Ensure your assigned SCORES are logically consistent with your CRITIQUE. If you write "there are no metrics," you MUST NOT assign a score higher than 2 for Q15/Q16.
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

            "Q1": {"type": "integer", "enum": [0, 1, 3, 5, 7]},
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
