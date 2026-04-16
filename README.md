# APERTURE — Kaggle "Measuring Progress Toward AGI" 2026 Submission

**Competition:** [Measuring Progress Toward AGI - Cognitive Abilities](https://www.kaggle.com/competitions/kaggle-measuring-agi)
**Deadline:** April 16, 2026 · 7:59 PM EDT
**Author:** Joseph Raetano (with Jens Gregor, Suzanne Tamang — University of Tennessee, Knoxville)
**Framework:** APERTURE — unified personality-reasoning and cognitive-faculty assessment program

## Published Benchmark Tasks

| Track | Task | URL |
|---|---|---|
| 4 — Executive Function | APERTURE-Executive-Inhibition | https://www.kaggle.com/benchmarks/tasks/josephraetano/aperture-executive-inhibition |
| 2 — Metacognition | APERTURE-Clarification-Seeking | https://www.kaggle.com/benchmarks/tasks/josephraetano/aperture-clarification-seeking |
| 5 — Social Cognition | APERTURE-Risk-Authority | https://www.kaggle.com/benchmarks/tasks/josephraetano/aperture-risk-authority |

## Contents

```
writeup/
  WRITEUP.md                     ← 1,482-word competition submission
code/
  suite_breadth.py               ← Tracks 1, 3, 5 (4 tasks)
  suite_executive.py             ← Track 4 (6 tasks)
  suite_metacognition.py         ← Track 2 (5 tasks)
  PASTE_*.ipynb                  ← Paste-ready versions of each suite
  _diagnostic_cell.py            ← Post-run pretty-print helper
kaggle_notebooks/
  suite_breadth.ipynb            ← Downloaded Version #1 from Kaggle
  (suite_metacognition.ipynb, suite_executive.ipynb added after download)
validation/
  multi_llm_results.json         ← Pre-submission validation:
                                   3 models × 15 tasks × 3 conditions (135 runs)
                                   GPT-4o, Claude Sonnet 4.5, Gemini 2.5 Flash
```

## Headline Finding

Across three public-API frontier models (GPT-4o, Claude Sonnet 4.5, Gemini 2.5 Flash), **zero of three** fail to request clarification on underspecified tasks at baseline — every model fabricates a plausible answer. Any structured reflective prior (including generic "think step by step") reverses the failure on all three. The gap is not capability — it is *default execution discipline*.

## Experimental Design

- **15 tasks** across all 5 competition tracks (deep coverage on Tracks 2 and 4)
- **3 experimental conditions** per task: baseline / generic_cot / aperture
- **3 procedural seeds** per condition (`{42, 137, 256}`) — prevents surface-pattern memorization
- Confound-controlled: APERTURE stance is length-matched to generic CoT

## Research Pedigree

Cites:
> Raetano, Gregor, Tamang. *A Survey and Computational Atlas of Personality Models.*
> ACM Transactions on Intelligent Systems and Technology (under review, 2026).

44 personality models · 6,694 trait items · 15 Semantic Personality Atlas clusters
(silhouette 0.098 vs. disciplinary baseline 0.0002 — **50× better coherence**)

The APERTURE "Systematic Explorer" stance instantiates an SPA-derived canonical
personality state as an LLM reasoning prior.

## License

Apache 2.0 (matches the kaggle_benchmarks SDK license).
