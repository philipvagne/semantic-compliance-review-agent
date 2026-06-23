# Gemini Evaluation Results

- Backend: `gemini`
- Timestamp: `2026-06-23T08:32:00+00:00`
- Cases run: `1`
- Run type: `partial evaluation`
- Selected cases: `security_python`
- Selected case count: `1`

## Overall Metrics

- True Positives (TP): `1`
- False Positives (FP): `0`
- False Negatives (FN): `0`
- Precision: `1.00`
- Recall: `1.00`
- Cases passed: `1`
- Cases failed: `0`

## Per-Case Summary

| Case | Status | TP | FP | FN | Actual Count | Expected Count Range |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `security_python.py` | PASS | 1 | 0 | 0 | 1 | 1-1 |

## Detailed Case Results

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
   Explanation: `The text explicitly mentions a 'temporary password' that needs to be removed before release. This indicates a potential hardcoded credential or sensitive information being present in the codebase, posing a significant security risk if exposed.`
   Recommendation: `Remove any hardcoded temporary passwords or credentials from the codebase. Implement a secure method for managing credentials, such as environment variables, a secrets management system, or a secure configuration file, ensuring they are not part of source control.`
   Suggested replacement: `TODO: remove the temporary credential reference before production release.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary password'.

## Notes

- Gemini evaluation results represent a snapshot captured at a specific point in time. Because LLM outputs may vary between runs, these results should be interpreted as evaluation evidence rather than a perfectly reproducible benchmark.
- Gemini results validate the current live semantic review path without changing prompts, matching rules, or the dataset.
- Suggested replacement matching is required only for expected findings that explicitly demand it.
- Severity is displayed for context but does not determine TP, FP, or FN in this evaluation implementation.
