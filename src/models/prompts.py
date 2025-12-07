POSTER_EVALUATION_PROMPT = """
You are an expert academic poster evaluator. Analyze this graduation project poster and answer the following questions exactly as specified.

IMPORTANT: Return your response as a valid JSON object with the exact field names specified below.

Analyze the poster and provide:

1. METADATA:
   - Extract "Project Number" (format x-x-x-x) -> field: "project_number"
   - Extract "Advisor Name" -> field: "advisor_name" 
   - Extract "Presenter Name(s)" (join with " and ") -> field: "presenter_names"

2. CATEGORY 1: Content Quality (25 points):
   - Q1: How well is the introduction written?
     (Scoring: Excellent=5, Good=3, Weak=1, Poor=0)
   - Q2: Does the introduction clearly relate to the poster topic?
     (Explanation: Relation between intro and poster, relevance, added value)
     (Scoring: Excellent match=5, Partial match=3, Weak match=1, No match=0)
   - Q3: Is the purpose of the project clearly stated?
     (Explanation: Clarity of purpose)
     (Scoring: Very clear=5, Clear=3, Partially clear=1, Not clear=0)
   - Q4: Is all content relevant? Are there irrelevant sources or information?
     (Scoring: Fully relevant=5, Mostly relevant=3, Some irrelevant parts=1, Many irrelevant parts=0)

3. CATEGORY 2: Research & Understanding (20 points):
   - Q5: Does the poster demonstrate deep understanding of the topic?
     (Scoring: Excellent understanding=8, Good understanding=5, Basic understanding=2, Weak understanding=0)
   - Q6: Are the references used appropriate and connected to the poster content?
     (Explanation: Relevance of sources, connection to poster)
     (Scoring: Highly relevant and well-connected=6, Mostly relevant=4, Partially relevant=2, Not relevant=0)
   - Q7: Is the methodology/implementation described clearly and in detail?
     (Scoring: Very detailed and clear=6, Clear but missing some details=4, Weak or unclear=2, Not described=0)

4. CATEGORY 3: Visual Quality & Graphs (15 points):
   - Q8: Are the graphs readable and clear (axes, labels, legend)?
     (Explanation: Axes clarity, visibility)
     (Scoring: Excellent clarity=6, Good clarity=4, Low clarity=2, Not clear or missing=0)
   - Q9: Do the graphs contribute meaningful information to the project?
     (Explanation: Relevance of graphs)
     (Scoring: Highly relevant=5, Moderately relevant=3, Weak relevance=1, Not relevant=0)
   - Q10: Overall visual quality of the poster (layout, readability).
     (Scoring: Excellent=4, Good=3, Acceptable=2, Poor=0)

5. CATEGORY 4: Structure & Logical Flow (25 points):
   - Q11: Is there a strong connection between the introduction and the motivation?
     (Scoring: Excellent connection=5, Good connection=3, Weak connection=1, No connection=0)
   - Q12: Are the sections in the poster logically connected?
     (Explanation: intro → methods → results → conclusions)
     (Scoring: Excellent flow=10, Good flow=7, Weak flow=3, No flow=0)
   - Q13: Is the explanation in each section consistent with the rest of the poster?
     (Scoring: Fully consistent=5, Mostly consistent=3, Some inconsistencies=1, Not consistent=0)
   - Q14: Does the poster add new and relevant information beyond the introduction?
     (Explanation: Does the intro explain or add actual value?)
     (Scoring: Adds significant value=5, Adds some value=3, Adds little=1, Adds none=0)

6. CATEGORY 5: Results & Conclusions (15 points):
   - Q15: Are the conclusions strongly connected to the results?
     (Scoring: Strong connection=7, Good connection=5, Weak connection=2, No connection=0)
   - Q16: Are the results clearly explained and meaningful?
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
"""
