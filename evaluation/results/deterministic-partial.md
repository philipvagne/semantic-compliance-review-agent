# Deterministic Evaluation Results - Partial Report

> Partial report: completed evaluations were preserved before the run finished.

- Status: `interrupted`
- Backend: `deterministic`
- Benchmark: `default`
- Model: `deterministic-local`
- Run started: `2026-06-25T07:51:28+00:00`
- Last updated: `2026-06-25T07:51:28+00:00`
- Completed cases: `1`
- Remaining cases: `1`
- Interruption reason: `Keyboard interrupt.`
- Selected cases: `security_python, security_javascript`

## Completed Metrics

- True Positives (TP): `1`
- False Positives (FP): `0`
- False Negatives (FN): `0`
- Precision: `1.00`
- Recall: `1.00`
- Cases passed: `1`
- Cases failed: `0`

## Completed Cases

| Case | Status | TP | FP | FN | Actual Count | Expected Count Range |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `security_python.py` | PASS | 1 | 0 | 0 | 1 | 1-1 |

## Remaining Cases

- `security_javascript`

## Detailed Completed Case Results

### security_python.py

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/security_python.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/security_python.json`
- Metrics: `TP=1`, `FP=0`, `FN=0`
- Actual finding count: `1`
- Expected finding count range: `1` to `1`
- Count range satisfied: `yes`

#### Expected Findings

1. Category: `SECURITY_RISK`
   Target text contains: `temporary password`
   Lines: `3-3`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `3-3`

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `3-3`
   Source text: `TODO: remove the temporary password before production release.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `TODO: remove the temporary credential reference before production release.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary password'.
