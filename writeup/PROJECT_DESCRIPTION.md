### Project Name

APERTURE: Diagnosing Executive-Discipline Failures in Frontier LLMs

### Your Team

Joseph Raetano (PhD ABD, University of Tennessee, Knoxville / Sovereign AI Research Lab)

### Problem Statement

Current AGI benchmarks conflate capability with execution. A model that *can* reason about missing information but *defaults* to fabricating an answer scores the same as one that genuinely cannot reason. APERTURE isolates this gap — the difference between what a frontier LLM can do when prompted deliberately and what it does by default — across executive function, metacognition, and social cognition.

### Task & benchmark construction

15 procedurally-generated tasks across all 5 competition tracks, with deep coverage on Track 4 (Executive Function — 6 tasks, 4 sub-components: inhibitory control, resource feasibility, planning, working memory) and Track 2 (Metacognition — 5 tasks, 4 sub-components: missing-information detection, ambiguity detection, confidence calibration, self-audit). Four additional breadth tasks cover Social Cognition (Risk-Authority, MRI-Safety), Attention (Haystack), and Learning (Rule-Inversion). Each task uses a `seed` parameter to procedurally vary scenarios (vehicles, locations, distances, budgets, authority figures), preventing surface-pattern memorization and ensuring the benchmark measures *faculty*, not *phrase*.

### Dataset

No external dataset is used. All task prompts are procedurally generated at runtime from parameterized scenario pools defined in the benchmark source code. The APERTURE Systematic Explorer stance is derived from the Semantic Personality Atlas (SPA) — a computational atlas of 44 personality models and 6,694 trait items developed in a companion research paper (see References).

### Technical details

Each task runs under three experimental conditions: (1) **baseline** — raw prompt; (2) **generic_cot** — a ~100-word generic "think step by step" prior; (3) **aperture** — the ~100-word APERTURE Systematic Explorer stance (identify the goal, enumerate prerequisites, check for heuristic contradictions, ask if information is missing, commit only after verification). The two primed conditions are length-matched, creating a **confound control**: any lift from APERTURE must exceed generic CoT to be considered content-specific. Three procedural seeds per condition yield 9 runs per task per model. Built with the `kaggle-benchmarks` SDK (`@kbench.task`, `kbench.assertions.assert_contains_regex`, `task.run(kbench.llm)`). Three tasks published as Version #1 Kaggle Benchmarks against `google/gemini-3-flash-preview` via the Kaggle Model Proxy.

### Results, insights, and conclusions

**RQ1 — Do frontier LLMs fail systematically at baseline?** Yes. Across GPT-4o, Claude Sonnet 4.5, and Gemini 2.5 Flash, baseline pass rates range 10–11/15 (67–73%). Critically, **Clarification-Seeking: 0/3 models pass at baseline** — every model fabricates a location rather than asking when the target is unspecified.

**RQ2 — Does the APERTURE stance improve performance?** Yes. Pass rates rise to 12–15/15 across all tested models. Clarification-Seeking flips from 0/3 to 3/3.

**RQ3 — Is the improvement content-specific?** Mostly not on binary pass/fail. `generic_cot ≈ aperture` — both produce 12–15/15. This *strengthens* the diagnostic claim: the observed failures are defaulted heuristics that any reflective prior interrupts, not capability ceilings. Two exceptions where APERTURE shows content-specific advantage: multi-turn consistency and failure-mode naming specificity.

**RQ4 — Replication on Kaggle's proxy?** Yes. All three published tasks pass cleanly on `gemini-3-flash-preview` under the APERTURE condition.

**Conclusion:** Progress toward AGI is not a monotonic capability curve — it is the joint trajectory of capability and disciplined execution. Benchmarks that conflate the two mis-measure what remains hard about cognition.

### Organizational affiliations

University of Tennessee, Knoxville — Department of Electrical Engineering and Computer Science. Sovereign AI Research Lab. Collaborators: Jens Gregor (advisor), Suzanne Tamang.

### References & citations

Raetano, J., Gregor, J., & Tamang, S. (2026). *A Survey and Computational Atlas of Personality Models.* ACM Transactions on Intelligent Systems and Technology (TIST). Under review. Open-source repository: [github.com/Wildertrek/survey](https://github.com/Wildertrek/survey)

**Published Kaggle Benchmark Tasks:**
- [APERTURE-Executive-Inhibition](https://www.kaggle.com/benchmarks/tasks/josephraetano/aperture-executive-inhibition) — Track 4
- [APERTURE-Clarification-Seeking](https://www.kaggle.com/benchmarks/tasks/josephraetano/aperture-clarification-seeking) — Track 2
- [APERTURE-Risk-Authority](https://www.kaggle.com/benchmarks/tasks/josephraetano/aperture-risk-authority) — Track 5
