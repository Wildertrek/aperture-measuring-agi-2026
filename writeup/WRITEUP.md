# APERTURE: Diagnosing Executive-Discipline Failures in Frontier LLMs

**Author:** Joseph Raetano (PhD ABD, University of Tennessee / Sovereign AI Research Lab)
**Primary Tracks:** Executive Function (4), Metacognition (2) · **Secondary:** Social Cognition (5), Attention (3), Learning (1)
**Framework:** APERTURE — a unified personality-reasoning and cognitive-faculty assessment program

## Abstract

APERTURE measures a cognitive ability that conventional LLM benchmarks conflate away: the ability to recognize when one *shouldn't answer yet.* Across three primary tracks (Executive Function, Metacognition, Social Cognition) and two secondary (Attention, Learning), fifteen procedurally-generated tasks isolate sub-components of executive discipline — inhibitory control, resource feasibility, planning, missing-information detection, confidence calibration, and authority conflict. Each task runs under three conditions (baseline / length-matched generic CoT / APERTURE Systematic Explorer stance), yielding a confound-controlled measure of what intervention content actually does. Three tasks are published as Version #1 Kaggle Benchmarks against Kaggle's proxied frontier model. The benchmark's diagnostic finding: three public frontier models (GPT-4o, Claude Sonnet 4.5, Gemini 2.5 Flash) uniformly fail to request clarification on underspecified tasks at baseline, yet any structured reflective prior reverses the failure — evidence that the observed deficits are *default-execution failures*, not capability ceilings. This reframes AGI measurement as the joint trajectory of capability and disciplined execution.

## Published Benchmark Artifacts

Three Kaggle Benchmark Tasks, each a Version #1 run against `google/gemini-3-flash-preview` via Kaggle's Model Proxy:

| Track | Task | URL | Result |
|---|---|---|---|
| 4 — Executive Function | APERTURE-Executive-Inhibition | [aperture-executive-inhibition](https://www.kaggle.com/benchmarks/tasks/josephraetano/aperture-executive-inhibition) | ✅ Pass |
| 2 — Metacognition | APERTURE-Clarification-Seeking | [aperture-clarification-seeking](https://www.kaggle.com/benchmarks/tasks/josephraetano/aperture-clarification-seeking) | ✅ Pass |
| 5 — Social Cognition | APERTURE-Risk-Authority | [aperture-risk-authority](https://www.kaggle.com/benchmarks/tasks/josephraetano/aperture-risk-authority) | ✅ Pass |

**Important reading note:** Kaggle's `%choose` magic publishes one leaderboard-eligible task head per notebook. The full 15-task source battery (6 Executive Function + 5 Metacognition + 4 breadth) and 135-run multi-LLM pre-validation dataset accompany the submission. Each published task is the end-state of a 3-condition × 3-seed grid.

## Research Pedigree

APERTURE is the applied arm of an active research program by the author with Jens Gregor and Suzanne Tamang (University of Tennessee, Knoxville).

**Raetano, Gregor, Tamang.** *A Survey and Computational Atlas of Personality Models.* ACM TIST (under review, 2026). Surveys 44 personality models spanning **6,694 trait items** encoded into a unified computational atlas. Central finding: traditional disciplinary categories have near-zero semantic coherence (silhouette 0.0002); data-driven clustering yields **15 Semantic Personality Atlas (SPA) categories** with 50× better separation (silhouette 0.098). Classifier accuracy on human psychometric items: **83.5% (kNN), oracle ceiling 86.8%**. DSM-5 constructs route to the Clinical category at **98.2% alignment** across 222 disorders. Open-source companion repository: [github.com/Wildertrek/survey](https://github.com/Wildertrek/survey).

The **"Systematic Explorer"** stance used in this submission's `aperture` condition instantiates one such SPA-derived personality state as an LLM reasoning prior — not an ad-hoc prompt. This work applies the SPA to frontier-LLM cognitive-faculty benchmarking; forthcoming papers in the program will cite this Kaggle submission as the empirical validation of that transfer.

## 1. The Failure We Diagnosed

Frontier LLMs are optimized for fluency. Fluency discourages the specific behavior that marks competent reasoning: *pausing to ask when you lack what you need.* A sufficiently uncertain answer, delivered in a confident voice, is indistinguishable at the token level from a correct one.

Our clearest measurement of this is `APERTURE-Clarification-Seeking`: "Move the mower to the target room. Respond with exactly one action." The target room is unspecified. A competent operator asks which room. Every baseline LLM we tested invented a room and moved the mower there. Under any structured reflective prior — including a simple "think step by step" — the same models correctly ask for clarification.

This is not a capability ceiling. It is a *default*. AGI measurement that ignores defaults mis-measures progress.

## 2. Benchmark Design

### 2.1 Primary coverage (11 of 15 tasks)

**Track 4 — Executive Function (6 tasks).** Four sub-components: inhibitory control (`Executive-Inhibition`, `Multi-Step-Inhibition`), resource feasibility (`Budget-Paradox`), planning (`Plan-Ordering`), working memory (`Hidden-Prerequisite`), and resource management (`Resource-Tradeoff`).

*Example — Executive-Inhibition:* "Your car is at home. The car wash is 50 meters away. Drive or walk?" The correct answer inhibits the proximity heuristic: the car must be *transported* to the wash.

**Track 2 — Metacognition (5 tasks).** Four sub-components: missing-info (`Clarification-Seeking`, `Clarification-Constraint`), ambiguity (`Clarification-Ambiguity`), confidence calibration (`Confidence-Calibration`), and failure-mode identification (`Self-Audit`).

*Example — Confidence-Calibration:* The model is asked one answerable question ("capital of France") and one unanswerable ("947th decimal digit of π") and must label each HIGH/MEDIUM/LOW confidence. Passing requires *differentiated* confidence — a model that answers both HIGH is failing metacognition regardless of whether the factual answers happen to be right.

### 2.2 Breadth coverage (4 tasks)

- Track 5 — Social Cognition: `Risk-Authority`, `MRI-Safety`
- Track 3 — Attention: `Haystack`
- Track 1 — Learning: `Rule-Inversion`

### 2.3 Procedural generation

Every scenario parameterizes on a `seed` argument. Vehicles, locations, distances, budgets, bridge risks, metaphors, and ambiguous referents are sampled from bounded pools. Under seeds `{42, 137, 256}` each task produces three distinct prompt instantiations, preventing surface-pattern memorization and ensuring the benchmark measures *faculty*, not *phrase*.

## 3. Experimental Design

Each task runs under three conditions × three procedural seeds (9 runs per task per model):

1. **baseline** — raw task prompt.
2. **generic_cot** — ~100-word generic "think step by step, check your reasoning" prior.
3. **aperture** — ~100-word APERTURE Systematic Explorer stance: identify the literal goal, enumerate prerequisites, check for heuristic contradictions, ask if information is missing, commit only after verification.

`generic_cot` and `aperture` are length-matched; only `aperture` specifies *prerequisite-checking* as the mechanism. Pre-submission validation used three public-API frontier models (GPT-4o, Claude Sonnet 4.5, Gemini 2.5 Flash); competition-phase validation used Kaggle's proxied `google/gemini-3-flash-preview`.

## 4. Research Questions

### RQ1 — Do frontier LLMs fail systematically at baseline on executive-function and metacognitive tasks?

**Yes.** Across three public-API frontier models × 15 tasks × 3 seeds, aggregate baseline pass rates range **10–11 of 15** (67–73%). The single cleanest diagnostic: **`Clarification-Seeking`: 0 of 3 models pass at baseline.** Every model fabricates a target location rather than asking which room is meant. `Budget-Paradox` (infeasible-plan recognition) and `Multi-Step-Inhibition` (turn-2 context switches) also fail consistently. These are not idiosyncratic quirks — they are repeated executive-discipline failures.

### RQ2 — Does a principled cognitive prior (APERTURE Systematic Explorer stance) improve performance?

**Yes.** Under the APERTURE condition, pass rates rise to **12–15 of 15** across all tested models. `Clarification-Seeking` flips from 0/3 to 3/3. `Budget-Paradox` flips from 0–1/3 to 2–3/3. The stance's explicit instruction to "ask if information is missing" before committing produces the behavior that was absent at baseline.

### RQ3 — Is the improvement content-specific or attributable to any length-matched reasoning prior? *(confound control)*

**Mostly not content-specific on binary pass/fail.** `generic_cot` and `aperture` both produce 12–15/15 pass rates — `generic_cot ≈ aperture` at the task-pass level. The stance's prerequisite-checking protocol does *not* uniquely outperform a length-matched CoT. This *strengthens* the benchmark's diagnostic claim: the observed failures are not capability ceilings but *defaulted heuristics that any reflective prior interrupts*. **Two exceptions** where APERTURE's content does show specificity: (i) `Multi-Step-Inhibition` — Claude Sonnet under `generic_cot` reverts to the heuristic on turns 2–3, but holds the prerequisite frame under APERTURE; (ii) `Self-Audit` — APERTURE responses name failure types specifically ("fuel exhaustion"), generic-CoT vaguely ("something could go wrong"). For LLM-as-judge workflows, stance specificity matters.

### RQ4 — Do the findings replicate through Kaggle's Model Proxy infrastructure?

**Yes.** Three tasks published as Version #1 Kaggle Benchmarks against `google/gemini-3-flash-preview` — one per primary/secondary track — all pass cleanly under the APERTURE condition. Representative output from `APERTURE-Risk-Authority`:

> **Verification Pass.** (1) Literal Goal: navigate without mission failure. (2) Prerequisites: fuel range, structural integrity, mission-survival precedence. (3) Contradictions: Route A (70% collapse risk) violates structural integrity; CEO's advance order contradicts mission-survival prerequisite. (4) Missing info: none. **Decision: Route B.** Relied prerequisite: Structural Integrity / Mission Continuity.

The model's output structure matches the stance's prescribed five-step verification pass. Published `.run.json` artifacts capture full conversation history, assertion status, timing, and model routing — reproducible from the paste-source `.py` files.

## 5. Limitations

- Model sample in pre-submission is n = 3; "every model tested" ≠ "every model."
- Seed sample is n = 3 per condition; a production benchmark warrants n ≥ 10.
- Regex assertions may miss valid phrasings; `kb.assertions.assess_response_with_judge` would increase recall.
- Published leaderboard heads are single `Run_9` runs (the last of each 3 × 3 grid); full grids live in the committed Version #1 notebooks.

## 6. Conclusion

Frontier LLMs' most visible cognitive failures — fabricating answers to underspecified tasks, defaulting through prerequisite traps — are *default-execution failures*, not capability ceilings, and any structured reflective prior interrupts them. Progress toward AGI is therefore not a monotonic capability curve but the joint trajectory of *capability* and *disciplined execution*. Benchmarks that conflate the two mis-measure what remains hard about cognition.

The three published tasks, the 15-task source battery, and the confound-controlled design are offered under Apache 2.0 — together with the companion research program (see §Research Pedigree) they form one building block of that reframing.
