# Evaluation Plan

## Purpose

This document explains how evaluation works for the Semantic Compliance Review
Agent and how to interpret the committed evaluation artifacts.

The goal is credible capstone evidence for a small, explainable review system,
not benchmark scale.

## Evaluation Philosophy

The evaluation measures whether the system identifies the right risk in the
right place, not whether it reproduces one exact explanation or recommendation.

Evaluation focuses on semantic correctness:

- whether the right text or line range was targeted
- whether the right category was identified
- whether the output is meaningfully aligned with the expected concern

## Benchmark Shape

The repository currently includes two committed benchmarks.

The original benchmark is a 10-case dataset:

- input files in `evaluation/cases/`
- matching expected JSON files in `evaluation/expected/`

The dataset is intentionally small and understandable. It is meant to show:

- risk detection
- false-positive handling
- multi-language coverage
- recommendation coverage

Supported evaluation coverage includes:

- `.py`
- `.js`
- `.ts` / `.tsx`
- `.html`
- `.md`

Coverage is representative rather than equal across file types.

The repository benchmark adds a second repository-style dataset:

- input files in `evaluation/cases/repository_benchmark/`
- matching expected JSON files in
  `evaluation/expected/repository_benchmark/`

Its purpose is broader engineering evaluation on coherent repository content
rather than isolated synthetic examples. The goal is more meaningful evidence,
not simply a larger case count.

## Backends

Evaluation is reported separately for the two supported backends.

### Deterministic Backend

Purpose:

- validate pipeline correctness
- validate extraction and matching behavior
- provide repeatable precision and recall evidence

### Gemini Backend

Purpose:

- validate semantic reasoning
- validate contextual judgment
- provide a committed snapshot of the live model-backed review path

Gemini results should be interpreted as evaluation evidence, not as a perfectly
reproducible benchmark.

## Metrics

The evaluation reports:

- True Positive (TP)
- False Positive (FP)
- False Negative (FN)
- Precision
- Recall

Primary interpretation:

- Precision: how trustworthy are reported findings?
- Recall: how many expected findings were detected?

Severity is informative but secondary. A correct detection can still count as a
match even when severity differs from the expected example.

## Matching Rules

A finding counts as a match when:

1. The expected reviewable text was identified, or the correct line range was targeted.
2. The expected category was identified.
3. The finding meaningfully matches the expected concern.

Exact wording matches are not required.

## Expected JSON Schema

Expected outputs use a small explicit schema:

```json
{
  "case_id": "security_python",
  "expected_findings": [
    {
      "category": "SECURITY_RISK",
      "target_text_contains": "temporary password",
      "line_start": 3,
      "line_end": 3,
      "line_range_approximate": true,
      "requires_suggested_replacement": false
    }
  ],
  "expected_finding_count_min": 1,
  "expected_finding_count_max": 2
}
```

Clean cases use:

```json
{
  "case_id": "documentation_false_positive",
  "expected_findings": [],
  "expected_finding_count_min": 0,
  "expected_finding_count_max": 0
}
```

## Result Artifacts

Committed evaluation result artifacts:

- `evaluation/results/deterministic-results.md`
- `evaluation/results/gemini-results.md`
- `evaluation/results/deterministic-repository_benchmark-results.md`
- `evaluation/results/gemini-repository_benchmark-results.md`

These artifacts are part of the capstone evidence package.

If only a subset of cases is run, the result file should clearly state that it
is a partial evaluation run.

During execution, the runner also writes incremental recovery artifacts:

- `*-progress.json` after each completed case
- `*-partial.md` while a run is in progress and if it is interrupted

These artifacts preserve completed work without changing scoring or report
methodology.

The committed Gemini snapshot artifact in this repository was captured with
`gemini-2.5-pro` and should be interpreted as a point-in-time evaluation
snapshot rather than a perfectly reproducible benchmark.

## Running Evaluation

Deterministic evaluation:

```text
python -m evaluation.run --backend deterministic
```

Single deterministic case:

```text
python -m evaluation.run --backend deterministic --case security_python
```

Gemini evaluation:

```text
python -m evaluation.run --backend gemini --delay-seconds 15
```

Repository benchmark examples:

```text
python -m evaluation.run --backend deterministic --benchmark repository_benchmark
python -m evaluation.run --backend gemini --benchmark repository_benchmark --delay-seconds 15
```

Recommended reliability-sensitive Gemini evaluation, PowerShell:

```text
$env:GEMINI_MODEL="gemini-2.5-pro"
python -m evaluation.run --backend gemini --delay-seconds 15
```

Recommended reliability-sensitive Gemini evaluation, Bash:

```text
export GEMINI_MODEL="gemini-2.5-pro"
python -m evaluation.run --backend gemini --delay-seconds 15
```

The runner also supports `--cases` for selected subsets.

Benchmark selection:

- Omit `--benchmark` or use `--benchmark default` for the original top-level benchmark.
- Use `--benchmark <folder-name>` for a benchmark folder under `evaluation/cases/`
  with matching expected files under `evaluation/expected/`.

## Gemini Model Guidance

Default model:

- `gemini-2.5-flash`

During project evaluation, `gemini-2.5-pro` produced the most consistent
results and was therefore used for the committed Gemini evaluation snapshot
and reliability-sensitive demos:

- `gemini-2.5-pro`

Reason:

- Flash remains the default for continuity and lighter-weight behavior
- Pro was the most consistent path during project evaluation

That recommendation should not be read as a claim that Pro is always superior
in all cost, latency, or deployment contexts.

## Reliability And Diagnostics

The repository also includes `evaluation/diagnose_gemini.py` for path diagnosis
and repeated observation.

Use it when you need to compare:

- direct Gemini access
- realistic direct prompt behavior
- ADK-backed review behavior

It is a diagnostic tool, not part of the benchmark itself.

## Realistic Sample Validation

The repository also includes `examples/realistic_sample.py`.

This file is useful for:

- usability validation
- demo-style validation
- checking the review and clean-copy experience on a more natural file

It is not part of the scored 10-case benchmark suite.

## Repository Benchmark Analyses

The repository benchmark also has separate engineering review documents:

- `docs/repository-benchmark/repository-benchmark-review.md`
- `docs/repository-benchmark/repository-benchmark-review-gemini.md`
- `docs/repository-benchmark/repository-benchmark-backend-comparison.md`

These documents interpret benchmark behavior and backend differences without
changing the evaluation methodology, matching rules, or metrics.

## Constraints And Non-Goals

Evaluation does not:

- change extraction behavior
- change prompts
- tune the model
- modify source files
- replace human review

The evaluation system is intended to measure the current project, not optimize
it during scoring.
