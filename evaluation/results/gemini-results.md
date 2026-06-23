# Gemini Evaluation Results

- Backend: `gemini`
- Model: `gemini-2.5-pro`
- Timestamp: `2026-06-23T13:27:08+00:00`
- Cases run: `10`
- Run type: `full evaluation`

## Overall Metrics

- True Positives (TP): `8`
- False Positives (FP): `0`
- False Negatives (FN): `0`
- Precision: `1.00`
- Recall: `1.00`
- Cases passed: `10`
- Cases failed: `0`

## Per-Case Summary

| Case | Status | TP | FP | FN | Actual Count | Expected Count Range |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `clean_python.py` | PASS | 0 | 0 | 0 | 0 | 0-0 |
| `documentation_false_positive.md` | PASS | 0 | 0 | 0 | 0 | 0-0 |
| `internal_codename_markdown.md` | PASS | 1 | 0 | 0 | 1 | 1-1 |
| `internal_codename_typescript.ts` | PASS | 1 | 0 | 0 | 1 | 1-1 |
| `professionalism_markdown.md` | PASS | 1 | 0 | 0 | 1 | 1-1 |
| `professionalism_python.py` | PASS | 1 | 0 | 0 | 1 | 1-1 |
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

- No findings returned by the gemini backend.

### documentation_false_positive.md

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/documentation_false_positive.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/documentation_false_positive.json`
- Metrics: `TP=0`, `FP=0`, `FN=0`
- Actual finding count: `0`
- Expected finding count range: `0` to `0`
- Count range satisfied: `yes`

#### Expected Findings

- None expected.

#### Actual Findings

- No findings returned by the gemini backend.

### internal_codename_markdown.md

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/internal_codename_markdown.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/internal_codename_markdown.json`
- Metrics: `TP=1`, `FP=0`, `FN=0`
- Actual finding count: `1`
- Expected finding count range: `1` to `1`
- Count range satisfied: `yes`

#### Expected Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Project Titan`
   Lines: `3-4`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `INTERNAL_CODENAME_EXPOSURE` on lines `3-4`

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `3-4`
   Source text: `This note still mentions the internal Project Titan codename for the partner launch.`
   Explanation: `The text explicitly references 'Project Titan' as an internal codename. Disclosing internal project names in partner-facing documentation can expose confidential information and create confusion.`
   Recommendation: `Review the documentation and replace any internal codenames with their public-facing names or a generic description before sharing with external partners.`
   Suggested replacement: `This note still mentions an internal project codename for the partner launch.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Project Titan'.

### internal_codename_typescript.ts

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/internal_codename_typescript.ts`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/internal_codename_typescript.json`
- Metrics: `TP=1`, `FP=0`, `FN=0`
- Actual finding count: `1`
- Expected finding count range: `1` to `1`
- Count range satisfied: `yes`

#### Expected Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Project Titan`
   Lines: `1-1`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `INTERNAL_CODENAME_EXPOSURE` on lines `1-1`

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `1-1`
   Source text: `Internal note: replace the Project Titan codename before sharing this file.`
   Explanation: `The comment explicitly identifies 'Project Titan' as a codename and contains an instruction to replace it before sharing. This indicates the presence of confidential information not intended for external visibility.`
   Recommendation: `Remove the internal note and any references to the codename from the file before sharing it or committing it to a non-private repository.`
   Suggested replacement: `(none)`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Project Titan'.

### professionalism_markdown.md

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/professionalism_markdown.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/professionalism_markdown.json`
- Metrics: `TP=1`, `FP=0`, `FN=0`
- Actual finding count: `1`
- Expected finding count range: `1` to `1`
- Count range satisfied: `yes`

#### Expected Findings

1. Category: `PROFESSIONALISM_RISK`
   Target text contains: `sloppy placeholder announcement`
   Lines: `3-4`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `PROFESSIONALISM_RISK` on lines `3-4`

#### Actual Findings

1. Category: `PROFESSIONALISM_RISK`
   Severity: `LOW`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `3-4`
   Source text: `TODO: rewrite this sloppy placeholder announcement before sending it to customers.`
   Explanation: `The comment contains the word 'sloppy,' which is unprofessional and subjective. It is recommended to maintain a professional tone in all project communications and documentation.`
   Recommendation: `Remove the unprofessional language and rephrase the comment using neutral terms.`
   Suggested replacement: `TODO: rewrite this placeholder announcement before sending it to customers.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'sloppy placeholder announcement'.

### professionalism_python.py

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/professionalism_python.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/professionalism_python.json`
- Metrics: `TP=1`, `FP=0`, `FN=0`
- Actual finding count: `1`
- Expected finding count range: `1` to `1`
- Count range satisfied: `yes`

#### Expected Findings

1. Category: `PROFESSIONALISM_RISK`
   Target text contains: `sloppy and half-baked`
   Lines: `3-3`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `PROFESSIONALISM_RISK` on lines `3-3`

#### Actual Findings

1. Category: `PROFESSIONALISM_RISK`
   Severity: `LOW`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `3-3`
   Source text: `FIXME: this release note still sounds sloppy and half-baked.`
   Explanation: `The comment uses unprofessional language ('sloppy and half-baked'). This can create a negative tone and is not constructive feedback. It is better to use neutral, objective language to describe technical issues or areas for improvement.`
   Recommendation: `Rewrite the comment to be more professional and constructive. Focus on the specific issues with the release note and what needs to be improved.`
   Suggested replacement: `FIXME: this release note needs to be revised for clarity and completeness.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'sloppy and half-baked'.

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
   Explanation: `The comment mentions a 'temporary credential note' that needs to be removed before launch, indicating a potential security risk if sensitive information is left in the codebase.`
   Recommendation: `Review the code to ensure no hard-coded credentials or sensitive notes are present. Use a secure method for managing credentials.`
   Suggested replacement: `TODO: ensure temporary credential handling is removed before release.`
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
   Severity: `CRITICAL`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `1-1`
   Source text: `TODO: remove the hard-coded secret before the public release.`
   Explanation: `The comment explicitly mentions a 'hard-coded secret'. This indicates the potential presence of sensitive credentials or keys directly in the source code, which poses a critical security vulnerability if accidentally committed or released.`
   Recommendation: `Immediately investigate and remove any hard-coded secrets from the source code. Replace them with a secure method for managing secrets, such as environment variables or a dedicated secrets management service.`
   Suggested replacement: `TODO: refactor to load credentials from a secure secrets management system before the public release.`
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
   Explanation: `The source code comment refers to a 'temporary password'. Committing credentials, even temporary ones, to source control is a significant security risk as they could be exposed.`
   Recommendation: `Remove the hard-coded credential from the code. Use a secure method for managing secrets, such as environment variables or a dedicated secrets management service.`
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
   Explanation: `The source code comment explicitly mentions a 'temporary admin password'. This indicates a potential security vulnerability where a credential might be hardcoded or left in the codebase, posing a significant risk if not removed before production deployment.`
   Recommendation: `It is strongly recommended to remove any temporary credentials from the code and use a secure method for managing secrets. The comment should be updated to avoid using specific sensitive terms like 'password'.`
   Suggested replacement: `TODO: remove the temporary admin credential before launch.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary admin password'.

## Notes

- Gemini evaluation results represent a snapshot captured at a specific point in time. Because LLM outputs may vary between runs, these results should be interpreted as evaluation evidence rather than a perfectly reproducible benchmark.
- Gemini results validate the current live semantic review path without changing prompts, matching rules, or the dataset.
- Suggested replacement matching is required only for expected findings that explicitly demand it.
- Severity is displayed for context but does not determine TP, FP, or FN in this evaluation implementation.
