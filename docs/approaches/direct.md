## Direct Evaluation Approach
This approach uses only the questions to evaluate the poster.

### Prompt
```python
POSTER_EVALUATION_PROMPT = """
You are a STRICT and CRITICAL academic poster evaluator. Analyze this graduation project poster and answer the following questions exactly as specified.

IMPORTANT: Return your response as a valid JSON object with the exact field names specified below.

⚠️ CRITICAL: Your goal is to match the human experts’ ranking order across all posters. Scores are tools — the ranking must match the experts’ order. Be strict, harsh, and comparative.

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

- The poster that is being evaluated is: **23-2-2-2581**. The poster file is: [2581-1.jpg](../posters/2581-1.jpg)

- The poster evaluation final grade is: **83**

- Here is the poster evaluation response:

```json
{
    "job_id": "4a0154af-8529-478f-9831-cc1d2dc54719",
    "status": "completed",
    "created_at": "2025-12-13T16:14:22.758788",
    "updated_at": "2025-12-13T16:14:35.490898",
    "total_files": 1,
    "processed_files": 1,
    "results": [
        {
            "poster_file": "2581-1.jpg",
            "project_number": "23-2-2-2581",
            "advisor_name": "Alon Eran, Eli Arviv",
            "presenter_names": "Danny Sinder",
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
            "Q13": 5,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops a model-based deep-learning neural network for Time of Arrival (ToA) estimation from simulated Channel Frequency Response data.\nIt uses a two-stage architecture: CIR enhancement via a generative U-Net and a coarse-to-fine ToA regression scheme.\nA wireless channel model based on the 802.11n standard is used to generate extensive training and test datasets.\nResults show substantial reductions in mean absolute error and false detection rates compared to the MUSIC algorithm, especially in low-SNR multipath scenarios.",
            "evaluation_summary": "The poster presents a clear, well-motivated problem and a logically structured solution with solid technical understanding.\nMethodology and results are described coherently, though references are minimal and not deeply integrated.\nGraphs and visual elements are generally clear and strongly support the claims, but some figures are dense and small.\nOverall, the work is strong, but the poster could better balance text and visuals and expand its scholarly grounding.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 83
        }
    ],
    "errors": [],
    "processing_logs": [
        {
            "file": "2581-1.jpg",
            "status": "ok",
            "grade": 83,
            "duration_ms": 12694,
            "error": null
        }
    ]
}
```


#### Batch posters evaluation

- All posters are in the [docs/posters](../posters) directory

- The evaluation grades for all posters are as follows:

| Poster Rank | File          | Number       | Final Grade |
|-------------|---------------|--------------|-------------|
| 1           | 2581-1.jpg    | 23-2-2-2581  | 85          |
| 2           | 3052-1.jpg    | 24-1-1-3052  | 83          |
| 3           | 3040-1.jpg    | 24-1-1-3040  | 81          |
| 4           | 3136-1.jpg    | 24-1-2-3136  | 81          |
| 5           | 3020-1.jpg    | 24-1-1-3020  | 79          |
| 6           | 3033-1.jpg    | 24-1-1-3033  | 79          |
| 7           | 3021-1.jpg    | 24-1-1-3021  | 77          |
| 8           | 3154-1.jpg    | 24-1-1-3154  | 75          |
| 9           | 2981-1.jpg    | 23-2-1-2981  | 68          |


- Here is the batch evaluation response:

```json
{
    "job_id": "e1e93505-5825-4c7b-971e-3344e322b4d0",
    "status": "completed",
    "created_at": "2025-12-13T16:39:52.989056",
    "updated_at": "2025-12-13T16:40:32.585079",
    "total_files": 9,
    "processed_files": 9,
    "results": [
        {
            "poster_file": "2581-1.jpg",
            "project_number": "23-2-2-2581",
            "advisor_name": "Alon Eran and Eli Arviv",
            "presenter_names": "Danny Sinder",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 4,
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
            "poster_summary": "The project develops a model-based deep-learning neural network for Time of Arrival (ToA) estimation from simulated Channel Frequency Response data.\nIt uses a two-stage architecture: CIR enhancement via a generative U-Net and a coarse-to-fine ToA regression scheme.\nA wireless channel model based on the 802.11n standard is used to generate extensive training and test datasets.\nResults show substantial reductions in mean absolute error and false detection rates compared to the MUSIC algorithm, especially in low-SNR, high-multipath scenarios.",
            "evaluation_summary": "The poster presents a clear, well-motivated problem and objective with tightly focused, relevant content.\nMethodology is logically described but somewhat compressed, and references are minimal for a graduation-level project.\nGraphs are informative and support the claims, though axis labels and readability could be improved.\nResults and conclusions are consistent and meaningful, but the explanation depth is moderate rather than exhaustive.",
            "overall_opinion": "The poster visuality is good",
            "final_grade": 85
        },
        {
            "poster_file": "3052-1.jpg",
            "project_number": "24-1-1-3052",
            "advisor_name": "Ofira Dabah",
            "presenter_names": "Danel Aharon and Gad Yair Mimran",
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
            "Q13": 5,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops a computer-vision-based navigation system for an autonomous surface vessel using ROS2 and a ZED stereo camera. A custom-trained YOLO model detects buoys, balls, and docking shapes, feeding a navigation logic module that generates steering commands. The system includes a GUI and server backend for task control and monitoring. Performance is evaluated via a confusion matrix and metrics such as mAP, precision, and recall, demonstrating high detection accuracy.",
            "evaluation_summary": "Content is clear, focused, and shows strong understanding of autonomous navigation and perception. Methodology and architecture are described reasonably well, though some implementation details are glossed over. Visuals and graphs are generally effective but somewhat dense and could be clearer. Results are well presented and mostly support the conclusions, but interpretation depth is limited.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 83
        },
        {
            "poster_file": "3040-1.jpg",
            "project_number": "24-1-1-3040",
            "advisor_name": "Yaakov Milstain",
            "presenter_names": "Jonathan Peled and Binat Makhlin",
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
            "poster_summary": "The project presents SPEAR, a custom ASIC accelerator implementing a single perceptron neuron in TSMC28 technology. It targets high-efficiency, low-power inference as an alternative to software/FPGA solutions. The poster details system architecture, design flow from RTL to tape-out, and functional verification results. Physical design metrics and prospective scaling to larger neural networks are also discussed.",
            "evaluation_summary": "The introduction, objectives, and motivation are very clear and tightly aligned with the main topic. Methodology and architecture are described well but not exhaustively, and references are minimal. Visuals and graphs are moderately clear yet somewhat dense, with heavy reliance on text. Results and conclusions are coherent and supported, though interpretation depth could be improved.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 81
        },
        {
            "poster_file": "3136-1.jpg",
            "project_number": "24-1-2-3136",
            "advisor_name": "Alona Cohen",
            "presenter_names": "Keren Kudriyayvtsev",
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
            "poster_summary": "The project develops an integrated navigation system using IMU, scalar magnetometer, and altimeter fused with Earth magnetic anomaly maps.\nA real-time simulator with error models and a particle filter estimates position in GPS-denied environments.\nAn 8-shaped maneuver test evaluates trajectory and error behavior under realistic dynamics.\nResults show RMS position errors within bounds, indicating robust navigation performance under noise.",
            "evaluation_summary": "Introduction and motivation are very strong and tightly linked to the topic and objectives.\nMethodology is technically sound but somewhat compressed, limiting accessibility and detail.\nGraphs are relevant and readable, though labeling and visual hierarchy could be improved.\nResults and conclusions are clearly connected, but interpretation depth and discussion remain moderate.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 81
        },
        {
            "poster_file": "3020-1.jpg",
            "project_number": "24-1-1-3020",
            "advisor_name": "Khen Cohen",
            "presenter_names": "Almog Ben Zur and Rotem Marinov",
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
            "Q13": 5,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops a real-time system that enables a telescope to track a moving drone for secure long-distance communication scenarios. A YOLO-based detector and Kalman filter estimate drone position from camera images and command a motorized telescope mount. Implementation includes data collection, model training, and real-time control software. Experiments with challenging drone motion evaluate tracking accuracy and robustness using image sequences and distance-over-time graphs.",
            "evaluation_summary": "The poster presents a very clear, well-focused introduction and maintains strong conceptual coherence throughout. Methodology and system architecture are described clearly but with limited technical depth, and there are effectively no formal references. Visuals and graphs are readable and supportive, though the layout is text-heavy and somewhat dense. Results and conclusions are well aligned and clearly explained, but more quantitative analysis would strengthen the evidence.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 79
        },
        {
            "poster_file": "3033-1.jpg",
            "project_number": "24-1-1-3033",
            "advisor_name": "Oren Ganon",
            "presenter_names": "Tamar Lutati and Shira Brodie",
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
            "Q13": 5,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project designs and implements SafeDLX, a tiny DLX processor with built‑in Error Detection and Correction (EDAC) for safety‑critical systems. It explores Hamming and CRC‑based EDAC algorithms with LUT and parallel‑processing optimizations. Several EDAC configurations (CORE, BOOST, TURBO, ULTRA) are implemented and compared. Results quantify trade‑offs among fault coverage, power, area, and timing.",
            "evaluation_summary": "Content is clear, focused, and shows strong technical understanding, but there is no explicit reference list. Methodology and architecture are described reasonably well, though some implementation details are compressed. Visual layout is structured and readable, with graphs that support the conclusions but are somewhat dense. Results and conclusions are coherent and well linked, though not deeply analyzed.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 79
        },
        {
            "poster_file": "3021-1.jpg",
            "project_number": "24-1-1-3021",
            "advisor_name": "Khen Cohen",
            "presenter_names": "Raz Bar-On and Amit Erez",
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
            "poster_summary": "The project implements a free-space quantum key distribution (QKD) communication system using polarized single photons over line-of-sight optical links.\nA compact optical setup with telescope, polarizer, beam splitter, retroreflector, and polarization-sensitive camera is deployed for outdoor field tests.\nExperiments at distances between 50 and 400 meters evaluate polarization stability, beam alignment, and attenuation under real conditions.\nResults show generally stable polarization with distance-dependent variations, informing algorithms for receiver-side polarization correction.",
            "evaluation_summary": "The introduction and objectives are exceptionally clear, tightly linked to the QKD context, and the content is focused and relevant.\nMethodology is described clearly but not in full technical depth, and references are effectively absent on the poster.\nGraphs and photos support the narrative, though labeling and visual polish are only moderate and could be improved.\nResults and conclusions are reasonably connected and clearly stated, but the evidence base is limited and somewhat qualitative.",
            "overall_opinion": "The poster visuality is good",
            "final_grade": 77
        },
        {
            "poster_file": "3154-1.jpg",
            "project_number": "24-1-1-3154",
            "advisor_name": "Nadav Sholev",
            "presenter_names": "Daniel David and Brittany Cohen",
            "Q1": 5,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 2,
            "Q7": 4,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 3,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops a Stanley path-tracking controller for the TAUVER space rover using ROS2 and Nav2.\nIt implements rover modeling, a ROS2 controller server, and a Jetson-based motor hardware interface.\nThe controller minimizes cross-track and heading errors to follow planned trajectories accurately.\nResults show low pose error and stable steering behavior on challenging paths.",
            "evaluation_summary": "Content is technically strong, focused, and demonstrates solid understanding of rover control and ROS2 implementation.\nMethodology and system architecture are described clearly, though some steps are dense and text-heavy.\nGraphs are readable and relevant but could be better integrated with the narrative and labeled more explicitly.\nConclusions are supported by results, yet the poster relies heavily on text over visual explanation.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 75
        },
        {
            "poster_file": "2981-1.jpg",
            "project_number": "23-2-1-2981",
            "advisor_name": "Dr. Gabi Davidov",
            "presenter_names": "Elad Dangur and Itamar Regev",
            "Q1": 5,
            "Q2": 8,
            "Q3": 5,
            "Q4": 3,
            "Q5": 5,
            "Q6": 2,
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
            "poster_summary": "The project develops an autonomous drone tracking system for open-field environments using computer vision and path-planning algorithms. A DJI Tello drone and laptop detect a user wearing a red hat, identify obstacles, and compute RRT-based paths. YOLO-based models, HSV filtering, segmentation, and PID control are integrated via a GUI. Simulations demonstrate tracking, obstacle avoidance, and dynamic path updates.",
            "evaluation_summary": "The poster presents a clear objective and reasonably structured methodology, with adequate but not deep technical detail. Visuals and graphs are readable and support the narrative, though they are somewhat crowded and lightly annotated. References are minimal and only loosely tied to specific claims. Overall, the work shows good understanding but could be more concise and analytically rigorous.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 68
        }
    ],
    "errors": [],
    "processing_logs": [
        {
            "file": "2981-1.jpg",
            "status": "ok",
            "grade": 68,
            "duration_ms": 12501,
            "error": null
        },
        {
            "file": "3020-1.jpg",
            "status": "ok",
            "grade": 79,
            "duration_ms": 12699,
            "error": null
        },
        {
            "file": "2581-1.jpg",
            "status": "ok",
            "grade": 85,
            "duration_ms": 12826,
            "error": null
        },
        {
            "file": "3033-1.jpg",
            "status": "ok",
            "grade": 79,
            "duration_ms": 12033,
            "error": null
        },
        {
            "file": "3040-1.jpg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 12767,
            "error": null
        },
        {
            "file": "3021-1.jpg",
            "status": "ok",
            "grade": 77,
            "duration_ms": 14170,
            "error": null
        },
        {
            "file": "3052-1.jpg",
            "status": "ok",
            "grade": 83,
            "duration_ms": 11302,
            "error": null
        },
        {
            "file": "3136-1.jpg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 12331,
            "error": null
        },
        {
            "file": "3154-1.jpg",
            "status": "ok",
            "grade": 75,
            "duration_ms": 12804,
            "error": null
        }
    ]
}
```
