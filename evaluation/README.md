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
- shared Gemini model selection support through `GEMINI_MODEL` for normal
  review and evaluation runs
- optional Gemini model override support through `--model` for stability
  comparison without changing the default review configuration

## Backend Separation

Evaluation will treat deterministic and Gemini results separately.

- The deterministic backend validates repeatable pipeline behavior.
- The Gemini backend validates semantic reasoning.

Current Phase 8B status:

- `8B.3` deterministic runner and metrics are implemented
- `8B.4` Gemini runner support is implemented
- `8B.4A` rate-limit-friendly Gemini pacing support is implemented
- `8B.4I` production model validation support is implemented
- committed Gemini snapshot results remain pending until a credentialed run is completed

## Result Policy

Evaluation results are committed as capstone evidence.

Gemini results should be treated as a review snapshot, not a perfectly
reproducible benchmark.

Free-tier Gemini users may hit requests-per-minute limits during evaluation.
When that happens, running with `--delay-seconds 15` is the recommended
starting point.

The shared `GEMINI_MODEL` environment variable now controls which Gemini model
normal review and evaluation runs use. If it is unset, the project keeps the
current default model selection: `gemini-2.5-flash`.

Current model decision:

- keep `gemini-2.5-flash` as the default model
- recommend `gemini-2.5-pro` for reliability-sensitive Gemini validation,
  evaluation, and demo runs

This recommendation is based on the documented investigation path:

- Flash produced intermittent `503 UNAVAILABLE` failures
- API-key variable testing did not identify `GOOGLE_API_KEY` versus
  `GEMINI_API_KEY` as the root cause
- a local ADK event-loop lifecycle issue was found and fixed separately
- bounded transient retry handling was added for provider-side high-demand
  failures
- prior manual model-comparison diagnostics showed `gemini-2.5-pro` completed
  5/5 cycles across direct and ADK-backed paths
- prior manual Gemini evaluation evidence showed the 10 committed cases passed
  when run one by one

Tradeoff note:

- Pro appeared more stable in diagnostics
- Pro also showed higher observed latency than Flash
- Pro may have different cost characteristics
- model choice remains a reliability, latency, and cost tradeoff

When a full Gemini run is too fragile or too slow, targeted selection is also
supported:

- `--case security_python`
- `--cases security_python,security_javascript`

When Gemini evaluation failures need path diagnosis, run:

- `python -m evaluation.diagnose_gemini`
- `python -m evaluation.diagnose_gemini --repeat 5 --delay-seconds 15`
- `python -m evaluation.diagnose_gemini --model gemini-2.5-flash --repeat 3`
- `python -m evaluation.diagnose_gemini --model gemini-2.5-pro --repeat 5 --delay-seconds 15`
- `export GEMINI_MODEL="gemini-2.5-pro" && python -m evaluation.run --backend gemini --delay-seconds 15`

The diagnosis command reports:

- whether `GOOGLE_API_KEY` is set
- whether `GEMINI_API_KEY` is set
- which variable would be used without printing the key value
- which Gemini model is being tested
- which backend path is under test
- per-test elapsed duration plus PASS / FAIL details
- per-test success and failure counts across repeated cycles

If no model is supplied, the diagnosis command keeps the project's current
shared Gemini model selection from `GEMINI_MODEL`, or `gemini-2.5-flash` when
that environment variable is unset.

It also reminds users that the selected key should be restricted to the Gemini
API / `generativelanguage.googleapis.com`.

The project Gemini-backed review path now retries small transient provider
failures such as `503 UNAVAILABLE` with short bounded backoff. Deterministic
evaluation behavior is unchanged, and final Gemini failures still remain
visible after all retry attempts.

Committed evaluation result artifacts now include both backend and selected
model metadata so Gemini snapshots can be compared more honestly.

## Future Phase 8B Steps

- `8B.4` Gemini evaluation snapshot
