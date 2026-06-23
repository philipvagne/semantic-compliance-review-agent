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
- Gemini evaluation runner support in `evaluation/run.py`
- optional pacing support through `--delay-seconds`
- optional case-selection support through `--case` and `--cases`
- a Gemini backend diagnosis helper at `evaluation/diagnose_gemini.py`
- repeated Gemini diagnosis support through `--repeat` and `--delay-seconds`

## Backend Separation

Evaluation will treat deterministic and Gemini results separately.

- The deterministic backend validates repeatable pipeline behavior.
- The Gemini backend validates semantic reasoning.

Current Phase 8B status:

- `8B.3` deterministic runner and metrics are implemented
- `8B.4` Gemini runner support is implemented
- `8B.4A` rate-limit-friendly Gemini pacing support is implemented
- committed Gemini snapshot results remain pending until a credentialed run is completed

## Result Policy

Evaluation results are committed as capstone evidence.

Gemini results should be treated as a review snapshot, not a perfectly
reproducible benchmark.

Free-tier Gemini users may hit requests-per-minute limits during evaluation.
When that happens, running with `--delay-seconds 15` is the recommended
starting point.

When a full Gemini run is too fragile or too slow, targeted selection is also
supported:

- `--case security_python`
- `--cases security_python,security_javascript`

When Gemini evaluation failures need path diagnosis, run:

- `python -m evaluation.diagnose_gemini`
- `python -m evaluation.diagnose_gemini --repeat 5 --delay-seconds 15`

The diagnosis command reports:

- whether `GOOGLE_API_KEY` is set
- whether `GEMINI_API_KEY` is set
- which variable would be used without printing the key value
- per-test elapsed duration plus PASS / FAIL details
- per-test success and failure counts across repeated cycles

It also reminds users that the selected key should be restricted to the Gemini
API / `generativelanguage.googleapis.com`.

## Future Phase 8B Steps

- `8B.4` Gemini evaluation snapshot
