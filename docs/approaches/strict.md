## Strict Evaluation Approach
This approach uses only the questions to evaluate the poster.

### Prompt
```python
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
"""
```

### Samples

#### Single poster evaluation

- The poster that is being evaluated is: **22-1-1-2729**. The poster file is: [2729](../posters/2729.jpeg)

- The poster evaluation final grade is: **78**

- Here is the poster evaluation response:

```json
{
    "job_id": "4ba6ac89-e440-41ed-9aff-71f53815269f",
    "status": "completed",
    "created_at": "2026-01-01T15:22:49.025704",
    "updated_at": "2026-01-01T15:22:53.610218",
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
            "Q5": 5,
            "Q6": 4,
            "Q7": 4,
            "Q8": 2,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 5,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project designs the electrical infrastructure for a shopping mall in accordance with Israeli electrical regulations. It addresses lighting, protection systems, cable selection, safeguards, and transformer integration with the national grid. The implementation includes power factor correction, voltage drop and short-circuit calculations, selectivity planning, and busbar system design. Electrical panel drawings and compliance with safety laws and standards are emphasized.",
            "evaluation_summary": "The poster presents a clear, well-structured introduction, motivation, and explicit project objectives closely aligned with the implementation steps. Methodology and system design tasks are listed but lack detailed quantitative explanation, and many diagrams and graphs are too small to read. References are relevant but only loosely linked to specific claims. Results and conclusions are present and mostly supported, yet interpretation depth and visual readability are limited.",
            "overall_opinion": "Visual explanation is missing",
            "final_grade": 78
        }
    ],
    "errors": [],
    "processing_logs": [
        {
            "file": "2729.jpeg",
            "status": "ok",
            "grade": 78,
            "duration_ms": 4581
        }
    ]
}
```

#### Batch posters evaluation

- All posters are in the [docs/posters](../posters) directory

- The evaluation grades for all posters are as follows:

| Poster Rank | File      | Number      | Final Grade |
| ----------- | --------- | ----------- | ----------- |
| 1           | 2916.jpeg | 2916        | 100         |
| 2           | 2850.jpeg | 23-1-2-2850 | 98          |
| 3           | 2745.jpeg | 23-1-1-2745 | 89          |
| 4           | 2826.jpeg | 23-1-1-2826 | 85          |
| 5           | 2849.jpeg | 23-1-1-2849 | 84          |
| 6           | 2862.jpeg | 2-8-6-2     | 82          |
| 7           | 2902.jpeg | 2902        | 82          |
| 8           | 2729.jpeg | 22-1-1-2729 | 80          |
| 9           | 2732.jpeg | 23-1-1-2732 | 78          |
| 10          | 2883.jpeg | 23-1-1-2883 | 78          |
| 11          | 2908.jpeg | 22-1-1-2908 | 65          |

- Here is the batch evaluation response:

```json
{
    "job_id": "b0b74f45-aa36-40cd-addf-5c9a4d0669ab",
    "status": "completed",
    "created_at": "2026-01-01T16:42:22.233037",
    "updated_at": "2026-01-01T16:42:43.844598",
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
            "Q7": 6,
            "Q8": 6,
            "Q9": 5,
            "Q10": 4,
            "Q11": 5,
            "Q12": 10,
            "Q13": 5,
            "Q14": 5,
            "Q15": 7,
            "Q16": 8,
            "poster_summary": "The project implements the DES encryption algorithm using NVIDIA’s CUDA framework to parallelize computation on a GPU instead of a CPU. It compares performance between an Nvidia GTX 1050 GPU and an Intel i3 CPU using varying input sizes and thread/block configurations. Speedup and throughput are measured, showing up to 100x speedup and multi‑Gbps throughput on the GPU. The work discusses implications for cryptographic workloads and future extensions to stronger ciphers and higher throughputs.",
            "evaluation_summary": "The poster presents a very clear, well‑structured study with explicit motivation, objectives, methodology, and strong quantitative results. Graphs are well labeled and directly support the claims about speedup and throughput, and references are relevant and properly linked. Minor weaknesses include dense text blocks and limited discussion of limitations or error analysis. Overall, it demonstrates strong understanding and excellent alignment between introduction, methods, results, and conclusions.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 100
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
            "Q6": 4,
            "Q7": 6,
            "Q8": 6,
            "Q9": 5,
            "Q10": 4,
            "Q11": 5,
            "Q12": 10,
            "Q13": 5,
            "Q14": 5,
            "Q15": 7,
            "Q16": 8,
            "poster_summary": "The project optimizes AI workload management in GPU clusters using high-frequency switch telemetry data.\nIt samples switch bandwidth, computes autocorrelation to detect training periods, and feeds parameters into an optimizer.\nThe optimizer adjusts workload priorities to reduce congestion and training iteration time.\nResults show significant reductions in iteration periods for workloads sharing a congested switch.",
            "evaluation_summary": "The poster presents a clear, well-structured introduction, objectives, methodology, and results with strong logical flow.\nGraphs are well labeled and directly support claims, and conclusions are tightly linked to quantitative evidence.\nReference linkage to specific claims is somewhat weak, and the bibliography is minimal.\nOverall, the work is technically solid and clearly communicated but could benefit from richer citation integration.",
            "overall_opinion": "The section's explanations in the poster are clear",
            "final_grade": 98
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
            "Q5": 5,
            "Q6": 4,
            "Q7": 6,
            "Q8": 6,
            "Q9": 5,
            "Q10": 3,
            "Q11": 5,
            "Q12": 10,
            "Q13": 5,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops deep learning models to decode speech-related brain activity from single-neuron recordings during articulation of five phonemes. An LSTM encoder-decoder architecture with data augmentation and hyperparameter optimization is used for speech detection and phoneme classification. Results show around 90% accuracy for binary speech detection and about 82% accuracy for five-phoneme classification. The work aims to advance brain–machine interfaces to help paralyzed patients communicate more naturally.",
            "evaluation_summary": "The poster presents a clearly structured project with well-defined motivation, objectives, and methodology, and includes relevant quantitative results. Visuals such as pipelines, architectures, and confusion matrices are readable and directly support the claims. However, the depth of theoretical explanation and discussion of limitations is moderate, and references are present but not tightly linked to specific statements. Overall, it is a solid, focused poster but not exceptional in depth or critical analysis.",
            "overall_opinion": "The section's explanations in the poster are clear",
            "final_grade": 89
        },
        {
            "poster_file": "2826.jpeg",
            "project_number": "23-1-1-2826",
            "advisor_name": "Khen Cohen; Co Advisor: Dr. Ariel Lellouch",
            "presenter_names": "Ofir Nissan and Natanel Nissan",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 4,
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
            "poster_summary": "The project develops an automatic method for spatial calibration of Distributed Acoustic Sensing (DAS) using fiber optic cables.\nIt estimates fiber location by synthesizing strain-rate maps from video-detected vehicle motion and optimizing them against real DAS measurements.\nA full processing pipeline is implemented, including detection, tracking, projection to 3D, strain map generation, and optimization.\nResults show accurate recovery of fiber location, demonstrating a proof of concept for DAS spatial calibration.",
            "evaluation_summary": "The poster presents a clear, well-motivated problem with explicit objectives and a detailed methodological pipeline.\nTechnical understanding appears strong, though reference linkage to specific claims is limited and graphs are somewhat small and hard to read.\nLogical flow and internal consistency are solid, with conclusions mostly supported by the shown results but with modest interpretive depth.\nOverall, the work is strong technically but could improve visual clarity and tighter citation of supporting literature.",
            "overall_opinion": "The section's explanations in the poster are clear",
            "final_grade": 85
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
            "Q5": 5,
            "Q6": 4,
            "Q7": 6,
            "Q8": 4,
            "Q9": 5,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 5,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops an adaptive optics system for quantum key distribution and satellite tracking using a Shack–Hartmann sensor and deformable mirror.\nA modal algorithm reconstructs the distorted wavefront via Zernike polynomials and a PID controller corrects it.\nSimulations and laboratory experiments demonstrate wavefront correction with improved RMS error and Strehl ratio.\nThe system targets operation under atmospheric turbulence for a 632 nm wavelength optical link.",
            "evaluation_summary": "The poster presents a clear, well-structured introduction, explicit goals, and a detailed methodology pipeline.\nGraphs and simulation visuals are relevant and support claims, though some labels and small text are hard to read.\nResults and conclusions are mostly supported but interpretation depth and discussion of limitations are limited.\nReferences and layout are adequate but not exemplary, with moderate visual clutter and only one clearly cited source.",
            "overall_opinion": "The poster visuality is good",
            "final_grade": 84
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
            "Q5": 5,
            "Q6": 4,
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
            "poster_summary": "The project implements the AES encryption algorithm using NVIDIA’s CUDA framework to leverage GPU parallelism.\nA baseline serial CPU implementation is compared against a parallel GPU version for different data sizes.\nPerformance results show substantial speedup of the GPU, especially for larger data sizes.\nThe work highlights the suitability of GPUs for large-scale encryption tasks and suggests further optimization of hardware–algorithm combinations.",
            "evaluation_summary": "Introduction, motivation, and objectives are explicit, well written, and tightly aligned with the project.\nMethodology and architecture are clearly depicted, but the technical depth and discussion of AES/CUDA details remain moderate.\nGraphs and visuals are relevant but somewhat small and not optimally labeled for easy reading.\nConclusions are mostly supported by the presented results, though interpretation and quantitative detail could be deeper.",
            "overall_opinion": "The poster visuality is good",
            "final_grade": 82
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
            "Q5": 5,
            "Q6": 4,
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
            "poster_summary": "The project presents real-time synchronous measurements of EEG/EMG and other electrophysiological data using Xtrodes hardware and mobile devices. A multi-source setup streams data via LSL and records with LabRecorder during stationary and ambulatory trials. Specific facial movements are used as control tasks to elicit distinct EMG patterns. Results show cross-correlations supporting reliable ambulatory EMG acquisition, with EEG reliability still under investigation.",
            "evaluation_summary": "The poster has a clear, well-structured introduction, motivation, and explicit objectives tightly aligned with the implementation and results. Methodology and system pipeline are described in sufficient detail, and the logical flow from intro to conclusions is strong and internally consistent. However, references are minimal, graphs and tables are only moderately readable, and the interpretation of results is somewhat limited. Overall, the work is focused and coherent but could improve depth of analysis, visual clarity, and literature integration.",
            "overall_opinion": "The poster visuality is good",
            "final_grade": 82
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
            "Q5": 5,
            "Q6": 6,
            "Q7": 4,
            "Q8": 2,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 5,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project designs the electrical infrastructure for a shopping mall in accordance with Israeli electrical regulations. It addresses lighting, protection systems, cable selection, safeguards, and transformer interfacing with the national grid. The work includes calculations for voltage drop, short-circuit currents, selectivity, and busbar design. Electrical panel drawings and compliance with legal and safety requirements are also considered.",
            "evaluation_summary": "Introduction, motivation, and objectives are clearly stated and well aligned with the project topic. Methodology and implementation steps are listed but lack detailed technical explanation, and many diagrams are too small to read. References are appropriate and clearly tied to the legal and technical framework. Results and conclusions are present and mostly supported, but visual presentation and interpretive depth are limited by readability issues.",
            "overall_opinion": "Visual explanation is missing",
            "final_grade": 80
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
            "Q5": 5,
            "Q6": 2,
            "Q7": 4,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 5,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "Design of an electrical power distribution system for a wood processing factory, covering low and high voltage aspects.\nWork includes architectural and lighting planning, determination of power loads, and transformer selection.\nThe system design addresses distribution to boards, wiring methods, short-circuit currents, and protection/earthing.\nFinal outputs include circuit drawings and panel diagrams that satisfy regulatory and operational requirements.",
            "evaluation_summary": "Introduction, motivation, and objectives are clearly stated and tightly aligned with the project scope.\nMethodology steps are listed and generally clear, but technical depth and explicit referencing are limited.\nGraphs/tables and diagrams are present and mostly readable, yet some are small and not fully interpreted.\nConclusions and results are present and mostly supported, though analysis and quantitative discussion are relatively shallow.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 78
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
            "Q5": 5,
            "Q6": 2,
            "Q7": 4,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 5,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project designs a complete electrical system for a residential/commercial building, covering low and high voltage distribution. It includes architectural planning, lighting design using RELUX, power load determination, and distribution of loads to electrical boards. Additional aspects include transformer selection, wiring methods, short-circuit and protection planning, and detailed circuit drawings. The design aims to meet logistical, safety, and regulatory requirements for reliable power delivery.",
            "evaluation_summary": "The poster has a clear, well-structured introduction, explicit objectives, and a focused set of sections that follow a logical engineering workflow. Visuals and tables are relevant but somewhat dense and not always easy to read, and methodological details remain at a descriptive rather than in-depth level. References are effectively absent or not visible, limiting evidence of scholarly grounding. Overall, the poster communicates the project coherently but could improve depth, citation, and visual clarity.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 78
        },
        {
            "poster_file": "2908.jpeg",
            "project_number": "22-1-1-2908",
            "advisor_name": "Dr. Hedva Shpizer",
            "presenter_names": "Alon Pulvermacher and Raz Hershtik",
            "Q1": 5,
            "Q2": 5,
            "Q3": 3,
            "Q4": 3,
            "Q5": 5,
            "Q6": 4,
            "Q7": 4,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 3,
            "Q12": 7,
            "Q13": 3,
            "Q14": 3,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "Project on automatic HDR compression of CT images to display high dynamic range content on standard screens.\nAlgorithm inspired by human visual system using multi-scale pyramid and contrast adaptation.\nResults compare original CT images with HDR-compressed, spine window, soft tissue, and histogram equalization.\nGoal is to enhance diagnostic detail while preserving necessary information in a single image.",
            "evaluation_summary": "Clear sections for introduction, algorithm, results, and conclusions, with reasonable logical flow.\nTechnical understanding appears solid but explanations are brief and some objectives and motivations are only moderately explicit.\nGraphs and image panels are mostly readable and relevant but not deeply analyzed.\nConclusions are generally supported by visual results, though interpretation and linkage to claims could be more thorough.",
            "overall_opinion": "The poster visuality is good",
            "final_grade": 65
        }
    ],
    "errors": [],
    "processing_logs": [
        {
            "file": "2729.jpeg",
            "status": "ok",
            "grade": 80,
            "duration_ms": 4723
        },
        {
            "file": "2745.jpeg",
            "status": "ok",
            "grade": 89,
            "duration_ms": 5031
        },
        {
            "file": "2732.jpeg",
            "status": "ok",
            "grade": 78,
            "duration_ms": 5356
        },
        {
            "file": "2826.jpeg",
            "status": "ok",
            "grade": 85,
            "duration_ms": 5215
        },
        {
            "file": "2849.jpeg",
            "status": "ok",
            "grade": 84,
            "duration_ms": 5660
        },
        {
            "file": "2850.jpeg",
            "status": "ok",
            "grade": 98,
            "duration_ms": 5353
        },
        {
            "file": "2883.jpeg",
            "status": "ok",
            "grade": 78,
            "duration_ms": 4175
        },
        {
            "file": "2862.jpeg",
            "status": "ok",
            "grade": 82,
            "duration_ms": 5118
        },
        {
            "file": "2902.jpeg",
            "status": "ok",
            "grade": 82,
            "duration_ms": 6067
        },
        {
            "file": "2916.jpeg",
            "status": "ok",
            "grade": 100,
            "duration_ms": 4537
        },
        {
            "file": "2908.jpeg",
            "status": "ok",
            "grade": 65,
            "duration_ms": 6720
        }
    ]
}
```
