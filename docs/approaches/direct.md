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

- The poster that is being evaluated is: **23-2-2-2581**. The poster file is: [2581-1.jpg](../posters/2581-1.jpg)

- The poster evaluation final grade is: **81**

- Here is the poster evaluation response:

```json
{
    "job_id": "a6fd344d-02aa-4373-8a17-f61596b2c2e8",
    "status": "completed",
    "created_at": "2025-12-13T23:24:37.271737",
    "updated_at": "2025-12-13T23:24:49.937512",
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
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops a model-based deep-learning neural network for Time of Arrival (ToA) estimation from simulated Channel Frequency Response data.\nIt uses a two-stage architecture: CIR enhancement via a generative U-Net and a coarse-to-fine ToA regression pipeline.\nExtensive simulations under 802.11n-like multipath channels evaluate performance across SNR and multipath conditions.\nResults show substantially reduced MAE and false detection rates compared to the MUSIC algorithm, especially in low-SNR, high-multipath scenarios.",
            "evaluation_summary": "The poster presents a clear, well-focused introduction and motivation tightly linked to the main topic.\nMethodology and results are generally clear, though some mathematical and architectural details are compressed.\nGraphs are relevant and supportive but somewhat dense and small, limiting readability at a distance.\nOverall, the work demonstrates strong understanding and solid evidence, with room for improved visual emphasis and reference depth.",
            "overall_opinion": "Visual explanation is missing",
            "final_grade": 81
        }
    ],
    "errors": [],
    "processing_logs": [
        {
            "file": "2581-1.jpg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 12661
        }
    ]
}
```


#### Batch posters evaluation

- All posters are in the [docs/posters](../posters) directory

| Poster Rank | File       | Number      | Final Grade |
| ----------- | ---------- | ----------- | ----------- |
| 1           | 3052-1.jpg | 24-1-1-3052 | 87          |
| 2           | 3020-1.jpg | 24-1-1-3020 | 83          |
| 3           | 3136-1.jpg | 24-1-2-3136 | 83          |
| 4           | 2581-1.jpg | 23-2-2-2581 | 81          |
| 5           | 2981-1.jpg | 23-2-1-2981 | 81          |
| 6           | 3040-1.jpg | 24-1-1-3040 | 81          |
| 7           | 3154-1.jpg | 24-1-1-3154 | 81          |
| 8           | 3033-1.jpg | 24-1-1-3033 | 79          |
| 9           | 3021-1.jpg | 24-1-1-3021 | 77          |

- Here is the batch evaluation response:

```json
{
    "job_id": "16a8db78-4dbc-4def-9d80-1cc984b664a7",
    "status": "completed",
    "created_at": "2025-12-13T23:26:16.187175",
    "updated_at": "2025-12-13T23:26:49.806717",
    "total_files": 9,
    "processed_files": 9,
    "results": [
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
            "Q6": 6,
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
            "poster_summary": "The project develops a computer-vision-based navigation system for an autonomous surface vessel using only image data. A custom-trained AI model detects buoys, balls, and docking shapes, feeding a ROS2-based navigation logic. The system includes a GUI and server backend for task control and monitoring. Results show high detection accuracy and reliable autonomous path following and docking.",
            "evaluation_summary": "The poster presents a clear, well-focused introduction tightly linked to the main topic and motivation. Methodology and system architecture are described with solid technical depth, though visuals could be more legible. Results and conclusions are coherent and supported but not extensively analyzed. Overall, the work reflects strong understanding and well-structured content with room for improved graphical clarity.",
            "overall_opinion": "Visual explanation is missing",
            "final_grade": 87
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
            "poster_summary": "The project develops a real-time telescope tracking system to follow a moving drone, aimed at enabling stable long-distance optical links. A YOLO-based detector and Kalman filter estimate drone position from camera images and command a motorized telescope mount. Experiments with challenging, non-continuous drone motion evaluate robustness using distance-from-center metrics. Results show stable tracking, rapid recovery from outliers, and resilience to noise and abrupt motion.",
            "evaluation_summary": "The introduction, motivation, and objectives are exceptionally clear and tightly aligned with the topic. Methodology and system pipeline are well explained, demonstrating strong technical understanding, though references are not visible. Visual layout is generally good, with meaningful graphs and images, but text density is high. Results and conclusions are coherent and reasonably supported, but could benefit from more quantitative detail and explicit reference linkage.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 83
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
            "Q9": 5,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops an integrated navigation system using IMU, scalar magnetometer, and altimeter fused with Earth magnetic anomaly maps.\nA real-time simulator with error models and a particle filter estimates position under GPS-denied conditions.\nAn 8-shaped maneuver test evaluates trajectory, position, and velocity errors.\nResults show RMS position errors within ±1σ bounds, indicating robust navigation performance.",
            "evaluation_summary": "The introduction is concise, well-motivated, and tightly aligned with the project’s objectives.\nMethodology is technically sound but somewhat compressed, limiting accessibility for non-experts.\nGraphs are relevant and supportive, though axis labels and legends are small and dense.\nOverall structure is coherent, with conclusions reasonably supported by the presented results.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 83
        },
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
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops a model-based deep-learning neural network for Time of Arrival (ToA) estimation from simulated Channel Frequency Response data.\nIt uses a two-stage architecture: CIR enhancement via a generative U-Net and a coarse-to-fine ToA regression pipeline.\nA wireless channel model based on the 802.11n standard is used to generate extensive training and test datasets.\nResults show substantial reductions in mean absolute error and false detection rates compared to the MUSIC algorithm, especially in low-SNR, high-multipath scenarios.",
            "evaluation_summary": "The poster presents a clear, well-focused introduction and motivation tightly linked to the main topic.\nMethodology and results are generally clear, though some mathematical and architectural details are only briefly sketched.\nGraphs are readable and strongly support the claims, but visual design is somewhat dense and text-heavy.\nReferences are minimal and could better reflect the breadth and recency of related work.",
            "overall_opinion": "The poster contains too much verbal information",
            "final_grade": 81
        },
        {
            "poster_file": "2981-1.jpg",
            "project_number": "23-2-1-2981",
            "advisor_name": "Dr. Gabi Davidov",
            "presenter_names": "Elad Dangur and Itamar Regev",
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
            "poster_summary": "The project develops an autonomous drone tracking system for open-field environments using computer vision and path-planning algorithms. A DJI Tello drone and laptop detect a user, obstacles, and targets via YOLO-based models and HSV filtering. User tracking, obstacle segmentation, and RRT path planning generate an optimized, dynamically updated path. Simulations demonstrate real-time tracking and navigation with moving targets and obstacles.",
            "evaluation_summary": "The poster presents a clear, well-focused introduction tightly aligned with the project’s objectives. Methodology and system architecture are described coherently, though not in exhaustive technical depth. Visuals and graphs are moderately clear but could be more legible and better annotated. Results and conclusions are consistent and reasonably supported, yet interpretation remains somewhat high-level.",
            "overall_opinion": "Visual explanation is missing",
            "final_grade": 81
        },
        {
            "poster_file": "3040-1.jpg",
            "project_number": "24-1-1-3040",
            "advisor_name": "Yaakov Milstein",
            "presenter_names": "Jonathan Peled and Binat Makhlin",
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
            "poster_summary": "The project presents SPEAR, a custom ASIC accelerator implementing a single perceptron neuron in silicon using a full RTL-to-GDSII flow on TSMC28 technology. It details a modular architecture with MAC, control, memory, and I/O units, targeting efficient, low‑power inference. Results from functional verification and physical design show correct operation, timing closure at 1 GHz, and compact area. Future work includes tape‑out, FPGA-based post‑silicon testing, and scaling to larger neural networks.",
            "evaluation_summary": "The poster’s introduction, objectives, and architecture are very clear, focused, and technically strong. Methodology and system description are detailed, but explicit references are missing. Visuals and graphs are generally readable and supportive, though not outstanding. Results and conclusions are coherent and well-aligned with the project goals, but interpretation depth could be expanded.",
            "overall_opinion": "The section's explanations in the poster are clear",
            "final_grade": 81
        },
        {
            "poster_file": "3154-1.jpg",
            "project_number": "24-1-1-3154",
            "advisor_name": "Nadav Sholev",
            "presenter_names": "Daniel David and Brittany Cohen",
            "Q1": 7,
            "Q2": 8,
            "Q3": 5,
            "Q4": 5,
            "Q5": 8,
            "Q6": 2,
            "Q7": 6,
            "Q8": 4,
            "Q9": 3,
            "Q10": 3,
            "Q11": 5,
            "Q12": 7,
            "Q13": 3,
            "Q14": 5,
            "Q15": 5,
            "Q16": 5,
            "poster_summary": "The project develops a Stanley path-tracking controller for the TAUVER space rover using ROS2 and Nav2.\nIt implements a full simulation and hardware framework, including rover URDF, controller server, and Jetson-based motor interface.\nThe controller minimizes cross-track and heading errors to follow planned trajectories accurately.\nResults show centimeter-level tracking accuracy and stable steering behavior on challenging paths.",
            "evaluation_summary": "The poster presents a clear, well-focused introduction and objectives tightly linked to the implementation and results.\nMethodology is detailed and technically sound, though references are minimal and not well integrated.\nGraphs are readable and relevant but could be better annotated and visually emphasized.\nOverall structure and logical flow are strong, with conclusions reasonably supported by the shown evidence.",
            "overall_opinion": "Visual explanation is missing",
            "final_grade": 81
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
            "poster_summary": "The project designs and implements SafeDLX, a tiny DLX processor with built‑in Error Detection and Correction (EDAC) for safety‑sensitive systems. It explores Hamming and CRC‑based EDAC algorithms, optimized via lookup tables and parallel processing. Several EDAC configurations (CORE, BOOST, TURBO, ULTRA) are compared in terms of fault coverage, power, area, and timing. Results quantify the trade‑offs between hardware cost and error‑correction strength.",
            "evaluation_summary": "The poster presents a very clear, well‑focused introduction tightly linked to the project goal. Methodology and architecture are described coherently, though implementation details and formal references are limited. Visual layout and graphs are generally clear but somewhat dense and could use cleaner labeling. Results and conclusions are logically connected and interpreted meaningfully, with explicit discussion of design trade‑offs.",
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
            "poster_summary": "The project implements a free-space Quantum Key Distribution (QKD) communication link using polarized single photons over line-of-sight paths. A compact optical setup with telescope, polarizer, beam expander, and retroreflector is deployed for outdoor field tests. Experiments at distances between 50 and 400 meters evaluate polarization stability and beam alignment. Results show small polarization variations over distance and time, supporting reliable QKD communication with potential correction algorithms.",
            "evaluation_summary": "The introduction is precise, well-motivated, and tightly aligned with the project’s objectives. Methodology and system design are described clearly but with limited technical depth and no explicit reference list. Graphs and photos support the narrative, though labeling and visual integration could be stronger. Results and conclusions are coherent and supported, but the poster would benefit from more detailed quantitative analysis and explicit citations.",
            "overall_opinion": "Visual explanation is missing",
            "final_grade": 77
        }
    ],
    "errors": [],
    "processing_logs": [
        {
            "file": "2581-1.jpg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 10825
        },
        {
            "file": "2981-1.jpg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 11192
        },
        {
            "file": "3020-1.jpg",
            "status": "ok",
            "grade": 83,
            "duration_ms": 11580
        },
        {
            "file": "3033-1.jpg",
            "status": "ok",
            "grade": 79,
            "duration_ms": 10273
        },
        {
            "file": "3021-1.jpg",
            "status": "ok",
            "grade": 77,
            "duration_ms": 11301
        },
        {
            "file": "3040-1.jpg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 11644
        },
        {
            "file": "3052-1.jpg",
            "status": "ok",
            "grade": 87,
            "duration_ms": 9114
        },
        {
            "file": "3136-1.jpg",
            "status": "ok",
            "grade": 83,
            "duration_ms": 9812
        },
        {
            "file": "3154-1.jpg",
            "status": "ok",
            "grade": 81,
            "duration_ms": 10247
        }
    ]
}
```
