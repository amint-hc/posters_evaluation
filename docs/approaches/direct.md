## Direct Evaluation Approach
This approach uses only the questions to evaluate the poster.

### Prompt
```python
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
"""
```

### Samples

#### Single poster evaluation

- The poster that is being evaluated is: **22-1-1-2729**. The poster file is: [2729](../posters/2729.jpeg)

- The poster evaluation final grade is: **81**

- Here is the poster evaluation response:

```json
{
    "job_id": "6efe4bfa-21a6-4e91-868e-4d4834dcd423",
    "status": "completed",
    "created_at": "2026-01-01T15:01:43.721246",
    "updated_at": "2026-01-01T15:01:49.360229",
    "total_files": 1,
    "processed_files": 1,
    "results": [
        {
            "poster_file": "2729.jpeg",
            "project_number": "22-1-1-2729",
            "advisor_name": "Bishara Bishara",
            "presenter_names": "Celine Badran and Essam Ayashi",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 4,
            "Q7": 4,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project designs the electrical infrastructure for a mall with high‑voltage supply, focusing on lighting, protection, cabling, and safety in line with Israeli regulations. It addresses motivation rooted in legal compliance, safety, and proper interfacing with the national grid. Implementation covers load analysis, power‑factor correction, short‑circuit calculations, selectivity, busbar design, and panel drawings. Objectives emphasize understanding regulations and coordinating with stakeholders to meet technical and legal requirements.",
            "evaluation_summary": "The poster presents a clear, well‑structured introduction tightly linked to the project’s objectives and motivation. Methodology and implementation steps are described in reasonable detail, though some aspects remain high‑level. Visuals and graphs are moderately clear and supportive but not exemplary in labeling and integration. Overall, the work demonstrates strong understanding and coherent results, with room for refinement in visual clarity and consistency across sections.",
            "overall_opinion": "The poster visuality is good",
            "final_grade": 81
        }
    ],
    "errors": [],
    "processing_logs": [
        {
            "file": "2729.jpeg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 5636
        }
    ]
}
```

#### Batch posters evaluation

- All posters are in the [docs/posters](../posters) directory

- The evaluation grades for all posters are as follows:

| Poster Rank | File      | Number      | Final Grade |
| ----------- | --------- | ----------- | ----------- |
| 1           | 2916.jpeg | 2916        | 87          |
| 2           | 2908.jpeg | 22-1-1-2908 | 83          |
| 3           | 2732.jpeg | 23-1-1-2732 | 81          |
| 4           | 2729.jpeg | 22-1-1-2729 | 81          |
| 5           | 2849.jpeg | 23-1-1-2849 | 81          |
| 6           | 2826.jpeg | 23-1-1-2826 | 81          |
| 7           | 2850.jpeg | 23-1-2-2850 | 81          |
| 8           | 2745.jpeg | 23-1-1-2745 | 79          |
| 9           | 2883.jpeg | 23-1-1-2883 | 79          |
| 10          | 2902.jpeg | 2902        | 79          |
| 11          | 2862.jpeg | 2-8-6-2     | 77          |

- Here is the batch evaluation response:

```json
{
    "job_id": "1f8f5c07-6323-4840-b2a0-ac0ae8b9f645",
    "status": "completed",
    "created_at": "2026-01-01T15:36:34.533797",
    "updated_at": "2026-01-01T15:36:54.217428",
    "total_files": 11,
    "processed_files": 11,
    "results": [
        {
            "poster_file": "2916.jpeg",
            "project_number": "2916",
            "advisor_name": "Oren Ganon",
            "presenter_names": "Nizar Khalaila and Mahmoud Shaheen",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 6,
            "Q7": 4,
            "Q8": 4,
            "Q9": 5,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 5,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project implements the DES encryption algorithm using NVIDIA’s CUDA framework to exploit GPU parallelism.\nIt compares GPU performance against a quad-core CPU over varying input sizes and thread configurations.\nSpeedup and throughput are measured, targeting 10x improvement but achieving around 100x in execution speed.\nThe work discusses implications for cryptographic workloads and future extensions to more advanced ciphers.",
            "evaluation_summary": "The poster presents a clear, well-structured introduction tightly linked to its main objective.\nMethodology and results are generally understandable, though implementation details are somewhat compressed.\nGraphs are relevant and supportive but suffer from small text and dense visual layout.\nOverall, the work demonstrates strong technical understanding and coherent argumentation.",
            "overall_opinion": "The poster visuality is good",
            "final_grade": 87
        },
        {
            "poster_file": "2908.jpeg",
            "project_number": "22-1-1-2908",
            "advisor_name": "Dr. Hedva Shpizer",
            "presenter_names": "Alon Pulvermacher and Raz Hershtik",
            "Q1": 5,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 6,
            "Q7": 4,
            "Q8": 4,
            "Q9": 5,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops an HDR compression algorithm for CT images inspired by the human visual system.\nIt aims to display high dynamic range CT data on standard low dynamic range screens while preserving diagnostic information.\nThe method uses a Gaussian pyramid, contrast modulation, and tone-mapping to enhance bone and soft-tissue visibility.\nResults compare original, HDR-compressed, and alternative methods such as histogram equalization and AHE.",
            "evaluation_summary": "Content is focused, technically solid, and well connected from introduction through conclusions.\nMethodology and results are described clearly but with limited textual detail on some implementation aspects.\nGraphs and image panels are relevant and supportive, though labeling and visual hierarchy could be improved.\nOverall, the poster is coherent and informative, with a good balance between text and visuals.",
            "overall_opinion": "The poster visuality is good",
            "final_grade": 83
        },
        {
            "poster_file": "2732.jpeg",
            "project_number": "23-1-1-2732",
            "advisor_name": "Mr. Bishara Bishara",
            "presenter_names": "Tawfik Sleman and Yazeed Khalilieh",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 0,
            "Q7": 6,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 5,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project designs a complete electrical power distribution system for a wood processing factory, covering low and high voltage aspects. It includes architectural and lighting planning, load determination, transformer selection, wiring, protection, and grounding. Short-circuit calculations, board distribution, and voltage drop checks are performed to ensure safety and regulatory compliance. Final circuit drawings summarize the implemented design choices.",
            "evaluation_summary": "The poster presents a clear, well-structured introduction and motivation tightly linked to the main topic. Methodology and implementation steps are detailed and logically organized, though formal references are missing. Visuals and tables are generally readable and supportive but not of the highest graphical quality. Results and conclusions are present and reasonably connected to the evidence, but interpretation depth could be improved.",
            "overall_opinion": "The poster visuality is good",
            "final_grade": 81
        },
        {
            "poster_file": "2729.jpeg",
            "project_number": "22-1-1-2729",
            "advisor_name": "Bishara Bishara",
            "presenter_names": "Celine Badran and Essam Ayashi",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 4,
            "Q7": 4,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project designs the electrical infrastructure for a mall, including lighting, protection systems, cable selection, and safeguards under Israeli regulations. It addresses compliance with the Electricity Law and safety standards. The implementation covers load calculations, power factor correction, short‑circuit analysis, selectivity, and busbar design. Results are illustrated through schematic diagrams, equipment sizing, and coordination tables.",
            "evaluation_summary": "The poster presents a clear, well‑structured introduction tightly linked to the objectives and motivation. Methodology and implementation steps are described reasonably clearly, though some details and deeper analysis are only briefly indicated. Visuals and graphs are moderately clear and supportive but somewhat dense and text‑heavy. Overall, the work shows strong understanding and coherent content with room for improved visual emphasis and concision.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 81
        },
        {
            "poster_file": "2849.jpeg",
            "project_number": "23-1-1-2849",
            "advisor_name": "Khen Cohen",
            "presenter_names": "Ahron Azarkovich and Israel Kuperman",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 2,
            "Q7": 4,
            "Q8": 4,
            "Q9": 5,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops an adaptive optics system for quantum key distribution and satellite tracking.\nIt uses a Shack–Hartmann wavefront sensor, deformable mirror, and PID control to correct atmospheric turbulence.\nA modal algorithm reconstructs the wavefront using Zernike polynomials and least-squares estimation.\nSimulations and lab experiments demonstrate improved RMS error and Strehl ratio after correction.",
            "evaluation_summary": "The poster presents a clear, well-focused introduction and a logically structured narrative from problem to solution.\nTechnical understanding is strong, though the methodology description is dense and references are minimal.\nGraphs and visual comparisons effectively support the claims, but some figures are small and text-heavy.\nResults and conclusions are reasonably connected, yet explanations could be more concise and visually emphasized.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 81
        },
        {
            "poster_file": "2826.jpeg",
            "project_number": "23-1-1-2826",
            "advisor_name": "Khen Cohen",
            "presenter_names": "Ofir Nissan and Natanel Nissan",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 4,
            "Q7": 4,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops a fast automatic method for spatial calibration of Distributed Acoustic Sensing (DAS) using camera-based tracking of vehicles above a buried fiber. An optimizer generates synthetic strain-rate maps from guessed fiber locations and aligns them with real DAS measurements. The system estimates the true fiber trajectory and demonstrates proof-of-concept accuracy on road-traffic data. It aims to generalize to various DAS applications requiring reliable fiber localization.",
            "evaluation_summary": "The poster presents a clear, well-motivated problem and objective with strong technical understanding. Methodology and results are described coherently, though some implementation details and reference integration could be deeper. Visuals are generally effective but graphs and figures are somewhat dense and not optimally labeled. Overall, it is a strong academic poster with minor issues in visual clarity and methodological elaboration.",
            "overall_opinion": "The poster visuality is good",
            "final_grade": 81
        },
        {
            "poster_file": "2850.jpeg",
            "project_number": "23-1-2-2850",
            "advisor_name": "Alon Gal",
            "presenter_names": "Nevo Genossar and Einav Zelig",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 2,
            "Q7": 4,
            "Q8": 4,
            "Q9": 5,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project proposes a load-aware network optimization method using high-frequency switch telemetry in AI training clusters. It samples switch bandwidth, performs autocorrelation to infer training periods, and feeds parameters into an optimizer. The optimizer adjusts workload priorities and switch parameters to reduce congestion and training iteration time. Results show significant reductions in iteration periods for workloads sharing a congested switch.",
            "evaluation_summary": "The introduction, motivation, and objectives are very clear and tightly connected to the topic. Methodology and implementation are described coherently but with limited methodological depth and only one explicit reference. Graphs are readable and relevant, and the layout is generally good though text-heavy. Results and conclusions are consistent and well explained, but the research framing and citation base are somewhat minimal.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 81
        },
        {
            "poster_file": "2745.jpeg",
            "project_number": "23-1-1-2745",
            "advisor_name": "Dr. Ariel Tankus",
            "presenter_names": "Rotem Ashkenazi and Yoav Yosif Or",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 2,
            "Q7": 4,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops deep learning models to decode speech-related information from single-neuron brain activity during articulation of five phonemes.\nIt uses LSTM encoder–decoder architectures with data augmentation and hyperparameter optimization to classify neural signals.\nResults are reported for binary speech detection and five-phoneme classification with confusion matrices and performance metrics.\nThe work aims to advance brain–machine interfaces for patients with severe speech impairments.",
            "evaluation_summary": "The poster presents a clear, well-motivated introduction tightly linked to the main objective and maintains strong topical focus.\nMethodology and implementation are described reasonably well, though references and prior-work grounding are minimal.\nGraphs are readable and relevant but visually modest, and overall layout is dense yet coherent.\nResults and conclusions are consistent and meaningful, but could benefit from deeper interpretation and clearer linkage to limitations.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 79
        },
        {
            "poster_file": "2883.jpeg",
            "project_number": "23-1-1-2883",
            "advisor_name": "Dr. Yuval Beck",
            "presenter_names": "Anan Alem and Kamal Rushrush",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 2,
            "Q7": 4,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project designs a complete electrical system for a residential/commercial building, covering low- and high-voltage distribution. It includes architectural and lighting planning, load calculations, transformer selection, and board distribution. Protection, short‑circuit analysis, wiring methods, and circuit layouts are addressed. The work aims to ensure regulatory compliance, safety, and reliable power delivery.",
            "evaluation_summary": "The introduction and motivation are clear, focused, and well aligned with the project scope. Methodology and implementation steps are mostly described, though references are barely visible and underdeveloped. Visuals and tables support the content but are somewhat dense and small, limiting readability. Results and conclusions are present and reasonably connected, but more explicit quantitative interpretation would strengthen them.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 79
        },
        {
            "poster_file": "2902.jpeg",
            "project_number": "2902",
            "advisor_name": "Prof. Yael Hanein",
            "presenter_names": "Daniel Guiot and Ronen Rubin",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 2,
            "Q7": 4,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project presents a system for real-time synchronous measurements of EEG/EMG using Xtrodes DAQ, dry electrodes, and a mobile phone. It focuses on ambulatory data collection during specific facial movements. Cross-correlation analyses compare stationary and ambulatory trials to assess signal reliability. The work aims to enable reliable, synchronized multi-source electrophysiological recordings for research and clinical applications.",
            "evaluation_summary": "The poster has a clear, well-written introduction and motivation closely tied to the main topic. Methodology and results are described adequately but with limited detail on analysis and only one reference. Visuals and graphs are moderately clear yet somewhat dense, and the bibliography is minimal. Overall, the work shows strong understanding and relevance but could improve visual emphasis and reference depth.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 79
        },
        {
            "poster_file": "2862.jpeg",
            "project_number": "2-8-6-2",
            "advisor_name": "Mr Oren Ganon",
            "presenter_names": "Tom Shahar and Yinon Coscas",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 0,
            "Q7": 4,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project implements the AES encryption algorithm using NVIDIA’s CUDA framework to exploit GPU parallelism.\nIt compares a baseline CPU implementation with a parallel GPU version for different data sizes.\nPerformance measurements show substantial speedup on the GPU, especially for large data sizes.\nThe work highlights the suitability of GPUs for large-scale cryptographic workloads and suggests further optimization of hardware–algorithm combinations.",
            "evaluation_summary": "The poster presents a clear, well-structured introduction and maintains good logical flow across sections.\nMethodology and implementation are described clearly but lack citation of references and deeper technical detail.\nGraphs are readable and support the message, though visual design is only moderately polished.\nOverall, the content is focused and coherent, with conclusions reasonably supported by the presented results.",
            "overall_opinion": "The section's explanations in the poster are clear",
            "final_grade": 77
        }
    ],
    "errors": [],
    "processing_logs": [
        {
            "file": "2732.jpeg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 5103
        },
        {
            "file": "2745.jpeg",
            "status": "ok",
            "grade": 79,
            "duration_ms": 5351
        },
        {
            "file": "2729.jpeg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 5468
        },
        {
            "file": "2849.jpeg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 4938
        },
        {
            "file": "2826.jpeg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 5238
        },
        {
            "file": "2850.jpeg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 5816
        },
        {
            "file": "2883.jpeg",
            "status": "ok",
            "grade": 79,
            "duration_ms": 3965
        },
        {
            "file": "2862.jpeg",
            "status": "ok",
            "grade": 77,
            "duration_ms": 4557
        },
        {
            "file": "2902.jpeg",
            "status": "ok",
            "grade": 79,
            "duration_ms": 4975
        },
        {
            "file": "2908.jpeg",
            "status": "ok",
            "grade": 83,
            "duration_ms": 4849
        },
        {
            "file": "2916.jpeg",
            "status": "ok",
            "grade": 87,
            "duration_ms": 4762
        }
    ]
}
```
