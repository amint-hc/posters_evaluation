# Approaches

This folder contains three different documented approaches used by the Posters Evaluation project. Each document describes a distinct prompting or reasoning strategy applied to the same underlying GPT model setup. The approaches are intentionally implemented to use the same GPT model characteristics (same base model and configuration); their differences come from how prompts and processing logic are structured.

Files:

- [`deep_analysis.md`](deep_analysis.md): A deep, multi-step analysis approach that asks the model to reason thoroughly, break problems into parts, and provide detailed justifications.
- [`direct.md`](direct.md): A concise, direct-answer approach that prompts the model to give short, focused responses with minimal extra reasoning.
- [`reasoning.md`](reasoning.md): An approach that emphasizes chain-of-thought or stepwise reasoning prompts to reveal the model's intermediate steps and rationale.

Shared model characteristics
---------------------------

All three approaches use the same GPT model characteristics (the same model family and runtime configuration used by this project). In practice this means:

- The same underlying model/version is used for inference.
- Common model settings (for example: temperature, max tokens, top-p, presence/penalty settings, and system-level instructions) are consistent across approaches.
- Differences between the approaches are achieved via prompt design, instruction framing, and post-processing logic — not by switching the model itself.

# Questions for experts

Please review the following questions and provide guidance from an expert evaluator's perspective.

1. How should we determine poster question weights? We already have a set of weights but they may need adjustment — please confirm whether the current weights are appropriate or suggest changes and rationale.

2. As an expert, do you prefer a strict evaluation mode or a more flexible one? For example, do you prefer awarding high grades only when a poster clearly meets objectives, or allowing lower/higher grades to ensure posters reach a target (e.g., 60%) of question objectives?

3. Are these posters ranked from best to worst? We could not reproduce the given ranking with any of our approaches. The target ranking is:

    ```
    24-1-1-3040
    24-1-1-3021
    24-1-1-3154
    23-2-2-2581
    24-1-1-3020
    23-2-1-2981
    24-1-1-3033
    24-1-1-3052
    ```

4. GPT outputs vary between runs. We found it difficult to enforce deterministic grading for the same poster across repeated requests. From your expert view, is variability acceptable? If not, do you have recommended strategies (prompting, temperature/settings, voting/ensemble, post-processing rules) to make grades more stable?

5. Which of the documented approaches (`deep_analysis.md`, `direct.md`, `reasoning.md`) best matches how experts evaluate posters in your experience? Please indicate which approach most closely mirrors expert practice, and why.

Thank you — your answers will help refine weights, prompt design, and evaluation policies.
