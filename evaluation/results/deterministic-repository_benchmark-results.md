# Deterministic Evaluation Results (repository benchmark)

- Backend: `deterministic`
- Benchmark: `repository_benchmark`
- Model: `deterministic-local`
- Timestamp: `2026-06-25T07:53:18+00:00`
- Cases run: `20`
- Run type: `full evaluation`

## Overall Metrics

- True Positives (TP): `11`
- False Positives (FP): `9`
- False Negatives (FN): `38`
- Precision: `0.55`
- Recall: `0.22`
- Cases passed: `1`
- Cases failed: `19`

## Per-Case Summary

| Case | Status | TP | FP | FN | Actual Count | Expected Count Range |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `public_status.js` | FAIL | 0 | 1 | 0 | 1 | 0-0 |
| `schema-docs.html` | FAIL | 0 | 0 | 2 | 0 | 2-2 |
| `oauth_callback.ts` | FAIL | 1 | 0 | 2 | 1 | 3-3 |
| `session_manager.py` | FAIL | 1 | 0 | 2 | 1 | 3-3 |
| `billing_rules.py` | FAIL | 0 | 0 | 3 | 0 | 3-3 |
| `customer_export.py` | FAIL | 1 | 0 | 2 | 1 | 3-3 |
| `build_summary.html` | PASS | 0 | 0 | 0 | 0 | 0-0 |
| `pipeline-notes.md` | FAIL | 0 | 0 | 2 | 0 | 2-2 |
| `feature_flags.ts` | FAIL | 1 | 0 | 2 | 1 | 3-3 |
| `credential-rotation-guide.md` | FAIL | 0 | 7 | 0 | 7 | 0-0 |
| `incident-retrospective.md` | FAIL | 0 | 1 | 2 | 1 | 2-2 |
| `partner-integration.md` | FAIL | 1 | 0 | 3 | 1 | 4-4 |
| `release-checklist.md` | FAIL | 0 | 0 | 2 | 0 | 2-2 |
| `account_settings.ts` | FAIL | 0 | 0 | 3 | 0 | 3-3 |
| `admin_debug.js` | FAIL | 1 | 0 | 2 | 1 | 3-3 |
| `support_banner.html` | FAIL | 0 | 0 | 2 | 0 | 2-2 |
| `roadmap-notes.md` | FAIL | 2 | 0 | 2 | 2 | 4-4 |
| `bootstrap_env.py` | FAIL | 1 | 0 | 2 | 1 | 3-3 |
| `deploy_preview.js` | FAIL | 1 | 0 | 2 | 1 | 3-3 |
| `access_review.py` | FAIL | 1 | 0 | 3 | 1 | 4-4 |

## Detailed Case Results

### public_status.js

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/api/public_status.js`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/api/public_status.json`
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
   Lines: `29-41`
   Source text: `Historical note for internal testing: The 2025 preview incident mentioned a temporary credential example during the postmortem, but the example value was already fictional and removed from the live runbook before partner review. Example placeholder only: username = sample-user password = example-password This comment is retained because it explains why the public incident summary intentionally avoids repeating internal cleanup details.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `Historical note for internal testing: The 2025 preview incident mentioned a temporary credential example during the postmortem, but the example value was already fictional and removed from the live runbook before partner review. Example placeholder only: username = sample-user credential reference = example-credential reference This comment is retained because it explains why the public incident summary intentionally avoids repeating internal cleanup details.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### schema-docs.html

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/api/schema-docs.html`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/api/schema-docs.json`
- Metrics: `TP=0`, `FP=0`, `FN=2`
- Actual finding count: `0`
- Expected finding count range: `2` to `2`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `INTELLECTUAL_PROPERTY_RISK`
   Target text contains: `vendor schema commentary`
   Lines: `12-12`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

2. Category: `REPUTATION_RISK`
   Target text contains: `could hurt confidence if shared unchanged`
   Lines: `13-13`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

- No findings returned by the deterministic backend.

### oauth_callback.ts

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/auth/oauth_callback.ts`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/auth/oauth_callback.json`
- Metrics: `TP=1`, `FP=0`, `FN=2`
- Actual finding count: `1`
- Expected finding count range: `3` to `3`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `SECURITY_RISK`
   Target text contains: `fallback state secret note`
   Lines: `92-92`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `91-96`

2. Category: `REPUTATION_RISK`
   Target text contains: `looks broken and undermines trust`
   Lines: `93-94`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

3. Category: `SECURITY_RISK`
   Target text contains: `logs the raw callback state`
   Lines: `95-95`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `91-96`
   Source text: `TODO: remove the fallback state secret note before external sharing. If the callback redirect loops during launch prep, the partner reviewer sees an error page that looks broken and undermines trust in the portal. The old callback branch still logs the raw callback state during launch prep.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `TODO: remove the fallback state sensitive reference note before external sharing. If the callback redirect loops during launch prep, the partner reviewer sees an error page that looks broken and undermines trust in the portal. The old callback branch still logs the raw callback state during launch prep.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'fallback state secret note'.

### session_manager.py

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/auth/session_manager.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/auth/session_manager.json`
- Metrics: `TP=1`, `FP=0`, `FN=2`
- Actual finding count: `1`
- Expected finding count range: `3` to `3`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `SECURITY_RISK`
   Target text contains: `temporary admin password note`
   Lines: `119-119`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `119-119`

2. Category: `COMPLIANCE_RISK`
   Target text contains: `skip consent refresh`
   Lines: `120-121`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

3. Category: `SECURITY_RISK`
   Target text contains: `stale session IDs`
   Lines: `122-123`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `119-119`
   Source text: `TODO: remove the temporary admin password note before partner review.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `TODO: remove the temporary admin credential reference note before partner review.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary admin password note'.

### billing_rules.py

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/backend/billing_rules.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/backend/billing_rules.json`
- Metrics: `TP=0`, `FP=0`, `FN=3`
- Actual finding count: `0`
- Expected finding count range: `3` to `3`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `COMPLIANCE_RISK`
   Target text contains: `regional tax shortcut`
   Lines: `68-69`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

2. Category: `REPUTATION_RISK`
   Target text contains: `billing process sound negotiable`
   Lines: `70-71`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

3. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Atlas pilot bundle label`
   Lines: `72-72`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

- No findings returned by the deterministic backend.

### customer_export.py

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/backend/customer_export.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/backend/customer_export.json`
- Metrics: `TP=1`, `FP=0`, `FN=2`
- Actual finding count: `1`
- Expected finding count range: `3` to `3`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `SECURITY_RISK`
   Target text contains: `temporary export token reference`
   Lines: `58-58`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `58-58`

2. Category: `INTELLECTUAL_PROPERTY_RISK`
   Target text contains: `vendor packet`
   Lines: `59-60`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

3. Category: `COMPLIANCE_RISK`
   Target text contains: `approval notes that belong only in internal review`
   Lines: `61-62`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `58-58`
   Source text: `TODO: remove the temporary export token reference before external sharing.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `TODO: remove the temporary export token reference reference before external sharing.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary export token reference'.

### build_summary.html

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/ci/build_summary.html`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/ci/build_summary.json`
- Metrics: `TP=0`, `FP=0`, `FN=0`
- Actual finding count: `0`
- Expected finding count range: `0` to `0`
- Count range satisfied: `yes`

#### Expected Findings

- None expected.

#### Actual Findings

- No findings returned by the deterministic backend.

### pipeline-notes.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/ci/pipeline-notes.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/ci/pipeline-notes.json`
- Metrics: `TP=0`, `FP=0`, `FN=2`
- Actual finding count: `0`
- Expected finding count range: `2` to `2`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `COMPLIANCE_RISK`
   Target text contains: `skip one approval gate`
   Lines: `17-18`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

2. Category: `PROFESSIONALISM_RISK`
   Target text contains: `reads like a rushed internal update`
   Lines: `20-20`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

- No findings returned by the deterministic backend.

### feature_flags.ts

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/config/feature_flags.ts`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/config/feature_flags.json`
- Metrics: `TP=1`, `FP=0`, `FN=2`
- Actual finding count: `1`
- Expected finding count range: `3` to `3`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Project Atlas`
   Lines: `30-31`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `INTERNAL_CODENAME_EXPOSURE` on lines `29-35`

2. Category: `COMPLIANCE_RISK`
   Target text contains: `approval switch as optional`
   Lines: `32-33`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

3. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Atlas review toggle name`
   Lines: `34-34`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `TERM_MATCH`
   Lines: `29-35`
   Source text: `The rollout note still mentions Project Atlas as the internal feature bundle name for partner-facing documentation. Compliance note: do not describe the export approval switch as optional in the release summary because that wording is inaccurate. The Atlas review toggle name is also visible in one screenshot caption.`
   Explanation: `The text references configured sensitive term(s): Project Atlas.`
   Recommendation: `Review whether the internal project reference should be removed, generalized, or kept internal.`
   Suggested replacement: `The rollout note still mentions the internal project as the internal feature bundle name for partner-facing documentation. Compliance note: do not describe the export approval switch as optional in the release summary because that wording is inaccurate. The Atlas review toggle name is also visible in one screenshot caption.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Project Atlas'.

### credential-rotation-guide.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/docs/credential-rotation-guide.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/docs/credential-rotation-guide.json`
- Metrics: `TP=0`, `FP=7`, `FN=0`
- Actual finding count: `7`
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
   Source text: `Credential Rotation Guide`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `(none)`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `5-6`
   Source text: `This guide explains how the Atlas Ops Portal team documents credential rotation tasks for internal review and partner-facing launch preparation.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `(none)`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

3. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `22-22`
   Source text: `API key example: `example-api-key``
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `API credential reference example: `example-api-key``
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

4. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `24-24`
   Source text: `Admin password example: `example-password``
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `admin credential reference example: `example-credential reference``
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

5. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `25-25`
   Source text: `Export token example: `example-export-token``
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `Export token reference example: `example-export-token reference``
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

6. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `40-42`
   Source text: `Historical incidents may describe temporary credential cleanup work, but those references should remain in retrospective material only when the examples are already fictional and clearly marked.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `(none)`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

7. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `64-66`
   Source text: `Credential examples in training material should remain obviously fictional. Archived retrospectives may describe cleanup work, but active instructions should focus on safe current process rather than repeating old mistakes.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `(none)`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### incident-retrospective.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/docs/incident-retrospective.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/docs/incident-retrospective.json`
- Metrics: `TP=0`, `FP=1`, `FN=2`
- Actual finding count: `1`
- Expected finding count range: `2` to `2`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `REPUTATION_RISK`
   Target text contains: `team was careless during launch prep`
   Lines: `22-23`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

2. Category: `COMPLIANCE_RISK`
   Target text contains: `bypassing the normal approval trace`
   Lines: `26-26`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `32-34`
   Source text: `This file also retains a historical note about a removed secret example. That note should remain because it explains the cleanup sequence and does not repeat the old value.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `This file also retains a historical note about a removed sensitive reference example. That note should remain because it explains the cleanup sequence and does not repeat the old value.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### partner-integration.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/docs/partner-integration.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/docs/partner-integration.json`
- Metrics: `TP=1`, `FP=0`, `FN=3`
- Actual finding count: `1`
- Expected finding count range: `4` to `4`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Project Atlas`
   Lines: `30-31`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `INTERNAL_CODENAME_EXPOSURE` on lines `30-31`

2. Category: `COMPLIANCE_RISK`
   Target text contains: `handled informally`
   Lines: `33-35`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

3. Category: `INTELLECTUAL_PROPERTY_RISK`
   Target text contains: `vendor packet`
   Lines: `37-38`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

4. Category: `REPUTATION_RISK`
   Target text contains: `avoidable confusion`
   Lines: `40-41`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `TERM_MATCH`
   Lines: `30-31`
   Source text: `This guide still references Project Atlas in one of the rollout notes, and that codename should be removed before the document is shared externally.`
   Explanation: `The text references configured sensitive term(s): Project Atlas.`
   Recommendation: `Review whether the internal project reference should be removed, generalized, or kept internal.`
   Suggested replacement: `This guide still references the internal project in one of the rollout notes, and that codename should be removed before the document is shared externally.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Project Atlas'.

### release-checklist.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/docs/release-checklist.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/docs/release-checklist.json`
- Metrics: `TP=0`, `FP=0`, `FN=2`
- Actual finding count: `0`
- Expected finding count range: `2` to `2`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `PROFESSIONALISM_RISK`
   Target text contains: `sounds sloppy`
   Lines: `24-25`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

2. Category: `COMPLIANCE_RISK`
   Target text contains: `manual exception`
   Lines: `27-28`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

- No findings returned by the deterministic backend.

### account_settings.ts

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/frontend/account_settings.ts`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/frontend/account_settings.json`
- Metrics: `TP=0`, `FP=0`, `FN=3`
- Actual finding count: `0`
- Expected finding count range: `3` to `3`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `PROFESSIONALISM_RISK`
   Target text contains: `sounds sloppy`
   Lines: `57-58`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

2. Category: `REPUTATION_RISK`
   Target text contains: `complain before we fix the workflow`
   Lines: `59-60`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

3. Category: `REPUTATION_RISK`
   Target text contains: `internal-only workaround`
   Lines: `61-62`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

- No findings returned by the deterministic backend.

### admin_debug.js

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/frontend/admin_debug.js`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/frontend/admin_debug.json`
- Metrics: `TP=1`, `FP=0`, `FN=2`
- Actual finding count: `1`
- Expected finding count range: `3` to `3`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `SECURITY_RISK`
   Target text contains: `temporary support token note`
   Lines: `33-33`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `32-38`

2. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Project Atlas`
   Lines: `34-34`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

3. Category: `SECURITY_RISK`
   Target text contains: `bypassing audit logging`
   Lines: `35-36`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `32-38`
   Source text: `TODO: remove the temporary support token note before partner review. The Atlas admin preview still mentions Project Atlas in the export path log. The debug note about bypassing audit logging should not appear in release preview output because it suggests an unsafe internal workaround. Example preview name only: fictional-user-for-layout-checks.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `TODO: remove the temporary support token reference note before partner review. The Atlas admin preview still mentions Project Atlas in the export path log. The debug note about bypassing audit logging should not appear in release preview output because it suggests an unsafe internal workaround. Example preview name only: fictional-user-for-layout-checks.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary support token note'.

### support_banner.html

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/frontend/support_banner.html`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/frontend/support_banner.json`
- Metrics: `TP=0`, `FP=0`, `FN=2`
- Actual finding count: `0`
- Expected finding count range: `2` to `2`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `PROFESSIONALISM_RISK`
   Target text contains: `Keep the partner support message professional`
   Lines: `15-15`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

2. Category: `REPUTATION_RISK`
   Target text contains: `fallback copy still sounds defensive`
   Lines: `16-16`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

- No findings returned by the deterministic backend.

### roadmap-notes.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/project/roadmap-notes.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/project/roadmap-notes.json`
- Metrics: `TP=2`, `FP=0`, `FN=2`
- Actual finding count: `2`
- Expected finding count range: `4` to `4`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Project Atlas in two planning bullets`
   Lines: `17-18`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `INTERNAL_CODENAME_EXPOSURE` on lines `17-18`

2. Category: `PROFESSIONALISM_RISK`
   Target text contains: `looks amateurish`
   Lines: `20-21`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

3. Category: `REPUTATION_RISK`
   Target text contains: `look unprepared`
   Lines: `23-24`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

4. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Project Atlas codename`
   Lines: `26-27`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `INTERNAL_CODENAME_EXPOSURE` on lines `26-27`

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `TERM_MATCH`
   Lines: `17-18`
   Source text: `The roadmap still uses Project Atlas in two planning bullets, which should be removed before any external sharing of the release packet.`
   Explanation: `The text references configured sensitive term(s): Project Atlas.`
   Recommendation: `Review whether the internal project reference should be removed, generalized, or kept internal.`
   Suggested replacement: `The roadmap still uses the internal project in two planning bullets, which should be removed before any external sharing of the release packet.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Project Atlas in two planning bullets'.

2. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `TERM_MATCH`
   Lines: `26-27`
   Source text: `The archived planning section also repeats the Project Atlas codename in a feature comparison block that should stay internal only.`
   Explanation: `The text references configured sensitive term(s): Project Atlas.`
   Recommendation: `Review whether the internal project reference should be removed, generalized, or kept internal.`
   Suggested replacement: `The archived planning section also repeats the the internal project codename in a feature comparison block that should stay internal only.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Project Atlas codename'.

### bootstrap_env.py

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/scripts/bootstrap_env.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/scripts/bootstrap_env.json`
- Metrics: `TP=1`, `FP=0`, `FN=2`
- Actual finding count: `1`
- Expected finding count range: `3` to `3`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `SECURITY_RISK`
   Target text contains: `temporary bootstrap secret reminder`
   Lines: `37-37`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `37-37`

2. Category: `PROFESSIONALISM_RISK`
   Target text contains: `calling the preview script half-baked`
   Lines: `38-39`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

3. Category: `COMPLIANCE_RISK`
   Target text contains: `approval tagging can be skipped`
   Lines: `40-41`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `37-37`
   Source text: `TODO: remove the temporary bootstrap secret reminder before external sharing.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `TODO: remove the temporary bootstrap sensitive reference reminder before external sharing.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary bootstrap secret reminder'.

### deploy_preview.js

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/scripts/deploy_preview.js`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/scripts/deploy_preview.json`
- Metrics: `TP=1`, `FP=0`, `FN=2`
- Actual finding count: `1`
- Expected finding count range: `3` to `3`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `SECURITY_RISK`
   Target text contains: `temporary deployment token reminder`
   Lines: `31-31`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `30-36`

2. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Project Atlas`
   Lines: `32-32`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

3. Category: `COMPLIANCE_RISK`
   Target text contains: `release tag can be skipped`
   Lines: `33-34`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `30-36`
   Source text: `TODO: remove the temporary deployment token reminder before launch. The Project Atlas preview label still appears in the deployment notes. The fallback upload note still says the release tag can be skipped during partner review retries. Example target name for docs only: fictional-preview-target.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `TODO: remove the temporary deployment token reference reminder before launch. The Project Atlas preview label still appears in the deployment notes. The fallback upload note still says the release tag can be skipped during partner review retries. Example target name for docs only: fictional-preview-target.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary deployment token reminder'.

### access_review.py

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/security/access_review.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/security/access_review.json`
- Metrics: `TP=1`, `FP=0`, `FN=3`
- Actual finding count: `1`
- Expected finding count range: `4` to `4`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `SECURITY_RISK`
   Target text contains: `temporary credential note`
   Lines: `56-56`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `56-56`

2. Category: `COMPLIANCE_RISK`
   Target text contains: `approval can proceed`
   Lines: `57-58`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

3. Category: `INTELLECTUAL_PROPERTY_RISK`
   Target text contains: `licensed wording is not ours to reuse`
   Lines: `59-60`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

4. Category: `REPUTATION_RISK`
   Target text contains: `could look careless during review`
   Lines: `61-62`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `56-56`
   Source text: `TODO: remove the temporary credential note from the access review appendix.`
   Explanation: `The text references a temporary or administrative secret-like value that should be reviewed before release.`
   Recommendation: `Remove the sensitive reference or replace it with a neutral, human-reviewed task description.`
   Suggested replacement: `(none)`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary credential note'.

## Notes

- Deterministic results validate repeatable pipeline behavior, not Gemini semantic reasoning.
- Suggested replacement matching is required only for expected findings that explicitly demand it.
- Severity is displayed for context but does not determine TP, FP, or FN in this evaluation implementation.
