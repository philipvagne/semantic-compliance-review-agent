# Gemini Evaluation Results

- Backend: `gemini`
- Timestamp: `2026-06-23T10:14:01+00:00`
- Cases run: `1`
- Run type: `partial evaluation`
- Selected cases: `suggested_replacement_javascript`
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
| `suggested_replacement_javascript.js` | PASS | 1 | 0 | 0 | 1 | 1-1 |

## Detailed Case Results

### suggested_replacement_javascript.js

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/suggested_replacement_javascript.js`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/suggested_replacement_javascript.json`
- Metrics: `TP=1`, `FP=0`, `FN=0`
- Actual finding count: `1`
- Expected finding count range: `1` to `1`
- Count range satisfied: `yes`

#### Expected Findings

1. Category: `SECURITY_RISK`
   Target text contains: `temporary admin password`
   Lines: `1-1`
   Approximate line match allowed: `true`
   Suggested replacement required: `true`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `1-1`

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `1-1`
   Source text: `TODO: remove the temporary admin password before launch.`
   Explanation: `The comment explicitly mentions a 'temporary admin password'. Storing or even referencing such credentials in source code, regardless of their temporary nature, poses a significant security risk by potentially exposing sensitive information.`
   Recommendation: `Remove any direct mention of credentials or passwords from source code comments. Instead, refer to generic 'temporary access' or 'placeholder configuration' that needs to be addressed.`
   Suggested replacement: `TODO: remove the temporary admin credential reference before launch.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary admin password'.

## Notes

- Gemini evaluation results represent a snapshot captured at a specific point in time. Because LLM outputs may vary between runs, these results should be interpreted as evaluation evidence rather than a perfectly reproducible benchmark.
- Gemini results validate the current live semantic review path without changing prompts, matching rules, or the dataset.
- Suggested replacement matching is required only for expected findings that explicitly demand it.
- Severity is displayed for context but does not determine TP, FP, or FN in this evaluation implementation.
