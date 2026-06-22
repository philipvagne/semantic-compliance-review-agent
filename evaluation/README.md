# Evaluation Artifacts

This directory contains the evaluation artifacts for the Semantic Compliance
Review Agent.

## Directory Roles

- `cases/` contains input files used for evaluation.
- `expected/` contains expected outcome JSON files.
- `results/` contains committed evaluation result artifacts.

The repository now includes:

- an initial 10-case dataset and 10 matching expected JSON files from Phase 8B.2
- a deterministic evaluation runner at `evaluation/run.py`
- a committed deterministic results artifact at
  `evaluation/results/deterministic-results.md`

## Backend Separation

Evaluation will treat deterministic and Gemini results separately.

- The deterministic backend validates repeatable pipeline behavior.
- The Gemini backend validates semantic reasoning.

Current Phase 8B status:

- `8B.3` deterministic runner and metrics are implemented
- `8B.4` Gemini evaluation snapshot remains pending

## Result Policy

Evaluation results are committed as capstone evidence.

Gemini results should be treated as a review snapshot, not a perfectly
reproducible benchmark.

## Future Phase 8B Steps

- `8B.4` Gemini evaluation snapshot
