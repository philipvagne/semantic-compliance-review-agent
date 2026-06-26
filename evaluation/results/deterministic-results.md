# Deterministic Evaluation Results

- Backend: `deterministic`
- Benchmark: `default`
- Model: `deterministic-local`
- Timestamp: `2026-06-25T07:50:35+00:00`
- Cases run: `10`
- Run type: `full evaluation`

## Overall Metrics

- True Positives (TP): `4`
- False Positives (FP): `1`
- False Negatives (FN): `4`
- Precision: `0.80`
- Recall: `0.50`
- Cases passed: `5`
- Cases failed: `5`

## Per-Case Summary

| Case | Status | TP | FP | FN | Actual Count | Expected Count Range |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `clean_python.py` | PASS | 0 | 0 | 0 | 0 | 0-0 |
| `documentation_false_positive.md` | FAIL | 0 | 1 | 0 | 1 | 0-0 |
| `internal_codename_markdown.md` | FAIL | 0 | 0 | 1 | 0 | 1-1 |
| `internal_codename_typescript.ts` | FAIL | 0 | 0 | 1 | 0 | 1-1 |
| `professionalism_markdown.md` | FAIL | 0 | 0 | 1 | 0 | 1-1 |
| `professionalism_python.py` | FAIL | 0 | 0 | 1 | 0 | 1-1 |
| `security_html.html` | PASS | 1 | 0 | 0 | 1 | 1-1 |
| `security_javascript.js` | PASS | 1 | 0 | 0 | 1 | 1-1 |
| `security_python.py` | PASS | 1 | 0 | 0 | 1 | 1-1 |
| `suggested_replacement_javascript.js` | PASS | 1 | 0 | 0 | 1 | 1-1 |

## Detailed Case Results

### clean_python.py

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/clean_python.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/clean_python.json`
- Metrics: `TP=0`, `FP=0`, `FN=0`
- Actual finding count: `0`
- Expected finding count range: `0` to `0`
- Count range satisfied: `yes`

#### Expected Findings

- None expected.

#### Actual Findings

- No findings returned by the deterministic backend.

### documentation_false_positive.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/documentation_false_positive.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/documentation_false_positive.json`
- Metrics: `TP=0`, `FP=1`, `FN=0`
- Actual finding count: `1`
- Expected finding count range: `0` to `0`
- Count range satisfied: `no`

#### Expected Findings

- None expected.

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `1-1`
   Source text: `Credential Setup Guide`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `(none)`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### internal_codename_markdown.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/internal_codename_markdown.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/internal_codename_markdown.json`
- Metrics: `TP=0`, `FP=0`, `FN=1`
- Actual finding count: `0`
- Expected finding count range: `1` to `1`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Project Titan`
   Lines: `3-4`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

- No findings returned by the deterministic backend.

### internal_codename_typescript.ts

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/internal_codename_typescript.ts`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/internal_codename_typescript.json`
- Metrics: `TP=0`, `FP=0`, `FN=1`
- Actual finding count: `0`
- Expected finding count range: `1` to `1`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Project Titan`
   Lines: `1-1`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

- No findings returned by the deterministic backend.

### professionalism_markdown.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/professionalism_markdown.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/professionalism_markdown.json`
- Metrics: `TP=0`, `FP=0`, `FN=1`
- Actual finding count: `0`
- Expected finding count range: `1` to `1`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `PROFESSIONALISM_RISK`
   Target text contains: `sloppy placeholder announcement`
   Lines: `3-4`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

- No findings returned by the deterministic backend.

### professionalism_python.py

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/professionalism_python.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/professionalism_python.json`
- Metrics: `TP=0`, `FP=0`, `FN=1`
- Actual finding count: `0`
- Expected finding count range: `1` to `1`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `PROFESSIONALISM_RISK`
   Target text contains: `sloppy and half-baked`
   Lines: `3-3`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

- No findings returned by the deterministic backend.

### security_html.html

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/security_html.html`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/security_html.json`
- Metrics: `TP=1`, `FP=0`, `FN=0`
- Actual finding count: `1`
- Expected finding count range: `1` to `1`
- Count range satisfied: `yes`

#### Expected Findings

1. Category: `SECURITY_RISK`
   Target text contains: `temporary credential note`
   Lines: `4-4`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `4-4`

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `4-4`
   Source text: `TODO: remove the temporary credential note before launch.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `(none)`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary credential note'.

### security_javascript.js

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/security_javascript.js`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/security_javascript.json`
- Metrics: `TP=1`, `FP=0`, `FN=0`
- Actual finding count: `1`
- Expected finding count range: `1` to `1`
- Count range satisfied: `yes`

#### Expected Findings

1. Category: `SECURITY_RISK`
   Target text contains: `hard-coded secret`
   Lines: `1-1`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `1-1`

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `1-1`
   Source text: `TODO: remove the hard-coded secret before the public release.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `TODO: remove the hard-coded sensitive reference before the public release.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'hard-coded secret'.

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
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `TODO: remove the temporary admin credential reference before launch.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary admin password'.

## Notes

- Deterministic results validate repeatable pipeline behavior, not Gemini semantic reasoning.
- Suggested replacement matching is required only for expected findings that explicitly demand it.
- Severity is displayed for context but does not determine TP, FP, or FN in this evaluation implementation.
