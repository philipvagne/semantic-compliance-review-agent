# Gemini Evaluation Results (repository benchmark)

- Backend: `gemini`
- Benchmark: `repository_benchmark`
- Model: `gemini-2.5-flash`
- Timestamp: `2026-06-25T08:13:00+00:00`
- Cases run: `20`
- Run type: `full evaluation`

## Overall Metrics

- True Positives (TP): `40`
- False Positives (FP): `38`
- False Negatives (FN): `9`
- Precision: `0.51`
- Recall: `0.82`
- Cases passed: `2`
- Cases failed: `18`

## Per-Case Summary

| Case | Status | TP | FP | FN | Actual Count | Expected Count Range |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `public_status.js` | FAIL | 0 | 2 | 0 | 2 | 0-0 |
| `schema-docs.html` | FAIL | 1 | 1 | 1 | 2 | 2-2 |
| `oauth_callback.ts` | FAIL | 1 | 1 | 2 | 2 | 3-3 |
| `session_manager.py` | FAIL | 3 | 1 | 0 | 4 | 3-3 |
| `billing_rules.py` | FAIL | 2 | 2 | 1 | 4 | 3-3 |
| `customer_export.py` | FAIL | 2 | 4 | 1 | 6 | 3-3 |
| `build_summary.html` | FAIL | 0 | 1 | 0 | 1 | 0-0 |
| `pipeline-notes.md` | FAIL | 2 | 2 | 0 | 4 | 2-2 |
| `feature_flags.ts` | FAIL | 3 | 1 | 0 | 4 | 3-3 |
| `credential-rotation-guide.md` | FAIL | 0 | 3 | 0 | 3 | 0-0 |
| `incident-retrospective.md` | FAIL | 1 | 2 | 1 | 3 | 2-2 |
| `partner-integration.md` | FAIL | 4 | 4 | 0 | 8 | 4-4 |
| `release-checklist.md` | FAIL | 2 | 2 | 0 | 4 | 2-2 |
| `account_settings.ts` | FAIL | 2 | 3 | 1 | 5 | 3-3 |
| `admin_debug.js` | PASS | 3 | 0 | 0 | 3 | 3-3 |
| `support_banner.html` | FAIL | 1 | 1 | 1 | 2 | 2-2 |
| `roadmap-notes.md` | PASS | 4 | 0 | 0 | 4 | 4-4 |
| `bootstrap_env.py` | FAIL | 3 | 2 | 0 | 5 | 3-3 |
| `deploy_preview.js` | FAIL | 2 | 2 | 1 | 4 | 3-3 |
| `access_review.py` | FAIL | 4 | 4 | 0 | 8 | 4-4 |

## Detailed Case Results

### public_status.js

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/api/public_status.js`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/api/public_status.json`
- Metrics: `TP=0`, `FP=2`, `FN=0`
- Actual finding count: `2`
- Expected finding count range: `0` to `0`
- Count range satisfied: `no`

#### Expected Findings

- None expected.

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `1-5`
   Source text: `Public status helpers for the Atlas Ops Portal.This file is used by the external status page and should remain safe forpartner review and public incident references.`
   Explanation: `The docstring mentions an internal codename 'Atlas' (part of 'Atlas Ops Portal') in a context explicitly marked for 'external status page' and 'partner review', indicating exposure of an internal project name to external parties.`
   Recommendation: `Replace the internal codename 'Atlas Ops Portal' with a generic, public-facing description.`
   Suggested replacement: `Public status helpers for the main operations portal.This file is used by the external status page and should remain safe forpartner review and public incident references.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `29-41`
   Source text: `Historical note for internal testing:The 2025 preview incident mentioned a temporary credential example duringthe postmortem, but the example value was already fictional and removed fromthe live runbook before partner review.Example placeholder only:username = sample-userpassword = example-passwordThis comment is retained because it explains why the public incident summaryintentionally avoids repeating internal cleanup details.`
   Explanation: `The docstring explicitly contains an example of a 'password' and 'credential example', which poses a security risk even if it is described as fictional or historical. Such explicit examples should not appear in code comments or documentation.`
   Recommendation: `Remove explicit mentions of 'password' and specific credential examples. Rephrase to refer to 'placeholder values' or 'temporary configurations' without providing actual sensitive-looking data.`
   Suggested replacement: `Historical note for internal testing:The 2025 preview incident mentioned a temporary placeholder value duringthe postmortem, which was already fictional and removed fromthe live runbook before partner review.This comment is retained because it explains why the public incident summaryintentionally avoids repeating internal cleanup details.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### schema-docs.html

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/api/schema-docs.html`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/api/schema-docs.json`
- Metrics: `TP=1`, `FP=1`, `FN=1`
- Actual finding count: `2`
- Expected finding count range: `2` to `2`
- Count range satisfied: `yes`

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
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `REPUTATION_RISK` on lines `13-13`

#### Actual Findings

1. Category: `REPUTATION_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `12-12`
   Source text: `Do not mirror the vendor schema commentary in our public docs.`
   Explanation: `The comment contains an internal directive about public documentation, indicating a need to prevent directly mirroring external vendor commentary. This suggests potential risks related to maintaining brand voice, intellectual property, or avoiding misinterpretation if external content is directly replicated.`
   Recommendation: `Review internal documentation processes to ensure that directives regarding public content are handled appropriately. Ensure public documentation commentary is independently developed and aligns with internal messaging guidelines.`
   Suggested replacement: `Public documentation should feature original commentary.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `REPUTATION_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `13-13`
   Source text: `The launch note about confusing field names could hurt confidence if shared unchanged.`
   Explanation: `The comment explicitly states that a 'launch note about confusing field names' could negatively impact public confidence if shared without modification, posing a direct risk to brand reputation and public perception.`
   Recommendation: `Address the concerns about 'confusing field names' within the mentioned launch note and revise it to ensure clarity and positive messaging, preventing any negative impact on user or partner confidence.`
   Suggested replacement: `Ensure public-facing notes address field name clarity in a positive manner.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'could hurt confidence if shared unchanged'.

### oauth_callback.ts

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/auth/oauth_callback.ts`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/auth/oauth_callback.json`
- Metrics: `TP=1`, `FP=1`, `FN=2`
- Actual finding count: `2`
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

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `1-5`
   Source text: `OAuth callback handling for the Atlas Ops Portal and partner reviewer sign-in. The partner portal and internal administration views share most of this flow, but release-specific checks still live here for now.`
   Explanation: `The docstring exposes the internal project codename 'Atlas' in 'Atlas Ops Portal'. Additionally, it details internal system components ('partner reviewer sign-in', 'internal administration views') and mentions 'release-specific checks', which could contain sensitive information about internal architecture or temporary states.`
   Recommendation: `Rewrite the docstring to use generic terms for the portal and system components, avoiding internal project codenames and specific references to temporary 'release-specific checks' if this information is not intended for external consumption.`
   Suggested replacement: `OAuth callback handling for the operational portal and external user authentication. External access and internal administration views share most of this flow, but specific checks are currently implemented here.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `91-96`
   Source text: `TODO: remove the fallback state secret note before external sharing. If the callback redirect loops during launch prep, the partner reviewer sees an error page that looks broken and undermines trust in the portal. The old callback branch still logs the raw callback state during launch prep.`
   Explanation: `The docstring contains a TODO to remove a 'secret note' before external sharing, indicating a potential leak of confidential information. It also explicitly states that 'the old callback branch still logs the raw callback state during launch prep', which is a significant security risk due to potential exposure of sensitive data. Additionally, it describes a negative user experience for external partners during 'launch prep', impacting trust and professionalism.`
   Recommendation: `Immediately address the 'secret note' and ensure no sensitive information is present in comments or code shared externally. Prevent the logging of raw or sensitive callback state in any production or pre-release environments. Rephrase the docstring to remove specific details about launch prep issues and potential negative external user experience, focusing on technical tasks and generalized improvements.`
   Suggested replacement: `(none)`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'fallback state secret note'.

### session_manager.py

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/auth/session_manager.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/auth/session_manager.json`
- Metrics: `TP=3`, `FP=1`, `FN=0`
- Actual finding count: `4`
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
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `COMPLIANCE_RISK` on lines `120-120`

3. Category: `SECURITY_RISK`
   Target text contains: `stale session IDs`
   Lines: `122-123`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `122-122`

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `LOW`
   Confidence: `HIGH`
   Detection method: `TERM_MATCH`
   Lines: `1-6`
   Source text: `Session management for the Atlas Ops Portal authentication flow. This module keeps short-lived session helpers for the customer operations platform, including browser sessions for the partner portal and internal administration views.`
   Explanation: `The term "Atlas Ops Portal" directly references the internal project codename "Atlas," which could inadvertently expose internal project nomenclature.`
   Recommendation: `Replace internal codenames with generic or publicly known descriptors to prevent unintended disclosure.`
   Suggested replacement: `Session management for the customer operations portal authentication flow. This module keeps short-lived session helpers for the customer operations platform, including browser sessions for the partner portal and internal administration views.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `119-119`
   Source text: `TODO: remove the temporary admin password note before partner review.`
   Explanation: `The TODO comment explicitly references a 'temporary admin password' that needs removal, indicating a clear security vulnerability, especially as it precedes a 'partner review' which implies external exposure.`
   Recommendation: `Ensure all temporary credentials are removed and secured before any release or external review. Avoid mentioning specific credential types in code comments.`
   Suggested replacement: `TODO: remove the temporary admin credential reference before partner review.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary admin password note'.

3. Category: `COMPLIANCE_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `120-120`
   Source text: `Launch compliance note: partner reviewer sessions still skip consent refresh`
   Explanation: `The comment identifies a 'compliance note' where 'partner reviewer sessions' 'skip consent refresh,' which indicates a potential deviation from compliance requirements, especially when involving external parties.`
   Recommendation: `Address compliance deviations, particularly those involving external partner access. Rephrase compliance notes to avoid specific details if possible.`
   Suggested replacement: `Launch process note: partner reviewer sessions still bypass standard consent procedures.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'skip consent refresh'.

4. Category: `SECURITY_RISK`
   Severity: `CRITICAL`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `122-122`
   Source text: `Security note: the legacy callback still accepts stale session IDs during`
   Explanation: `The comment explicitly highlights a 'Security note' indicating that the system 'accepts stale session IDs,' which is a critical security vulnerability potentially leading to unauthorized access or session hijacking.`
   Recommendation: `Immediately address the security vulnerability regarding stale session IDs. Avoid explicit 'Security note' in code comments.`
   Suggested replacement: `Operational note: the current callback mechanism processes outdated session identifiers during`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'stale session IDs'.

### billing_rules.py

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/backend/billing_rules.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/backend/billing_rules.json`
- Metrics: `TP=2`, `FP=2`, `FN=1`
- Actual finding count: `4`
- Expected finding count range: `3` to `3`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `COMPLIANCE_RISK`
   Target text contains: `regional tax shortcut`
   Lines: `68-69`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `COMPLIANCE_RISK` on lines `68-69`

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
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `INTERNAL_CODENAME_EXPOSURE` on lines `72-72`

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `1-1`
   Source text: `Billing rules for Atlas partner and customer export workflows.`
   Explanation: `The internal project codename 'Atlas' is used in a docstring describing external partner and customer workflows, which could lead to its unintended exposure to external parties.`
   Recommendation: `Replace the internal codename 'Atlas' with a public-facing project name or generic description when referring to external-facing processes.`
   Suggested replacement: `Billing rules for the platform's partner and customer export workflows.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `COMPLIANCE_RISK`
   Severity: `CRITICAL`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `68-69`
   Source text: `Compliance note: the partner launch draft still references a temporary regional tax shortcut that has not been approved by finance.`
   Explanation: `The comment indicates the existence of an unapproved, temporary regional tax shortcut referenced in a partner launch draft, posing a significant compliance and financial risk.`
   Recommendation: `Address the unapproved tax shortcut immediately. Ensure all financial practices are approved and compliant. Remove references to unapproved financial mechanisms from any external-facing documentation.`
   Suggested replacement: `Compliance note: the partner launch draft needs to be updated regarding regional tax calculations to reflect approved financial practices.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'regional tax shortcut'.

3. Category: `PROFESSIONALISM_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `70-71`
   Source text: `Internal note: keep the courtesy waiver wording out of the shared price sheet because it makes the billing process sound negotiable.`
   Explanation: `This internal note discusses a strategy to avoid certain wording in shared documents to prevent the billing process from appearing negotiable, which is sensitive internal business strategy information.`
   Recommendation: `Remove internal strategic discussions from source code comments, especially those pertaining to external-facing documents like price sheets. Move such discussions to internal documentation or communication channels.`
   Suggested replacement: `Internal note: ensure all external facing price sheet wording aligns with standard billing procedures.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

4. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `72-72`
   Source text: `The Atlas pilot bundle label is still used in one draft invoice appendix.`
   Explanation: `The internal project codename 'Atlas' is mentioned in the context of a 'draft invoice appendix', which is likely intended for external distribution and could expose internal naming to customers.`
   Recommendation: `Ensure all internal codenames are removed from external-facing documents like invoices. Replace 'Atlas' with an approved public-facing product name or generic description.`
   Suggested replacement: `The relevant pilot bundle label is still used in one draft invoice appendix.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Atlas pilot bundle label'.

### customer_export.py

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/backend/customer_export.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/backend/customer_export.json`
- Metrics: `TP=2`, `FP=4`, `FN=1`
- Actual finding count: `6`
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
   Outcome: `TP`
   Reasoning: Category matched and line range matched.
   Matched actual: `INTELLECTUAL_PROPERTY_RISK` on lines `59-59`

3. Category: `COMPLIANCE_RISK`
   Target text contains: `approval notes that belong only in internal review`
   Lines: `61-62`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `1-1`
   Source text: `Customer export helpers for Atlas partner data handoff.`
   Explanation: `The internal project codename 'Atlas' is mentioned in a context that implies it's being used in external communications ('partner data handoff'). This could expose internal project details to external parties.`
   Recommendation: `Replace the internal codename 'Atlas' with a public-facing project name or a generic description to avoid unintentional disclosure.`
   Suggested replacement: `Customer export helpers for partner data handoff.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `SECURITY_RISK`
   Severity: `CRITICAL`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `58-58`
   Source text: `TODO: remove the temporary export token reference before external sharing.`
   Explanation: `This TODO item indicates a 'temporary export token reference' that needs to be removed 'before external sharing,' which is a critical security vulnerability if not addressed prior to release.`
   Recommendation: `Ensure that all temporary export token references or any form of credential references are securely removed or managed before any external sharing occurs.`
   Suggested replacement: `TODO: remove the temporary credential reference before external sharing.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary export token reference'.

3. Category: `INTELLECTUAL_PROPERTY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `59-59`
   Source text: `Do not include the partner contract excerpt because it still mirrors licensed`
   Explanation: `The comment advises against including a 'partner contract excerpt' because it 'mirrors licensed implementation wording,' indicating a potential intellectual property or compliance risk if included in an export.`
   Recommendation: `Review the content of any 'partner contract excerpt' to ensure no licensed or proprietary information is inappropriately shared or replicated in external documentation.`
   Suggested replacement: `Do not include the partner contract excerpt due to sensitive content.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'vendor packet'.

4. Category: `REPUTATION_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `61-61`
   Source text: `Internal review outcomes should not appear in the partner export appendix`
   Explanation: `The comment states that 'Internal review outcomes should not appear in the partner export appendix,' indicating a risk of exposing internal processes or decisions to external partners, which could harm reputation.`
   Recommendation: `Ensure internal review outcomes are strictly separated from partner-facing documentation to prevent unintended disclosure of internal operational details.`
   Suggested replacement: `Confidential review outcomes should not appear in the partner export appendix`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

5. Category: `REPUTATION_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `62-62`
   Source text: `because they expose approval notes that belong only in internal review.`
   Explanation: `This text explicitly states that 'approval notes that belong only in internal review' are exposed, confirming that sensitive internal information is at risk of unintended disclosure to external parties.`
   Recommendation: `Prevent the exposure of internal approval notes by ensuring they are not included in external communications or partner-facing documentation.`
   Suggested replacement: `because they expose confidential notes that belong only in internal review.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

6. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `63-63`
   Source text: `Placeholder example value for docs only: export_key = atlas-example-key`
   Explanation: `The comment includes 'atlas-example-key' as a placeholder, which exposes the internal project codename 'Atlas' even in an example. This creates a risk if the documentation is shared externally.`
   Recommendation: `Replace 'atlas' in the example key with a generic, non-sensitive term to prevent the exposure of internal codenames in documentation.`
   Suggested replacement: `Placeholder example value for docs only: export_key = generic-example-key`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### build_summary.html

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/ci/build_summary.html`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/ci/build_summary.json`
- Metrics: `TP=0`, `FP=1`, `FN=0`
- Actual finding count: `1`
- Expected finding count range: `0` to `0`
- Count range satisfied: `no`

#### Expected Findings

- None expected.

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `LOW`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `12-12`
   Source text: `Fictional preview label only: Project Comet mock card`
   Explanation: `The comment refers to 'Project Comet' which, despite being labeled as 'fictional' and for a 'mock card', sounds like an internal project codename. Its exposure in code comments can still carry a low level of internal codename exposure risk.`
   Recommendation: `Replace the specific codename with a generic placeholder to avoid any potential internal codename exposure.`
   Suggested replacement: `Fictional preview label only: placeholder mock card`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### pipeline-notes.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/ci/pipeline-notes.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/ci/pipeline-notes.json`
- Metrics: `TP=2`, `FP=2`, `FN=0`
- Actual finding count: `4`
- Expected finding count range: `2` to `2`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `COMPLIANCE_RISK`
   Target text contains: `skip one approval gate`
   Lines: `17-18`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `COMPLIANCE_RISK` on lines `17-18`

2. Category: `PROFESSIONALISM_RISK`
   Target text contains: `reads like a rushed internal update`
   Lines: `20-20`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `PROFESSIONALISM_RISK` on lines `20-21`

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `TERM_MATCH`
   Lines: `5-6`
   Source text: `This document captures CI notes for the Atlas Ops Portal preview and release checks.`
   Explanation: `The text 'Atlas Ops Portal' contains 'Atlas', which is an internal codename. Exposing internal codenames in documentation can lead to unintended information disclosure.`
   Recommendation: `Replace the internal codename 'Atlas' with a generic or external-facing name for the portal.`
   Suggested replacement: `This document captures CI notes for the portal preview and release checks.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `COMPLIANCE_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `17-18`
   Source text: `The checklist still implies that a release reviewer can skip one approval gate when the preview job is green, which should be corrected before audit review.`
   Explanation: `The text implies that a release reviewer might be able to bypass an approval gate, which, especially when mentioned in the context of an 'audit review', poses a significant compliance or security risk.`
   Recommendation: `Ensure that all approval gates are mandatory and that documentation accurately reflects the required processes to prevent compliance issues.`
   Suggested replacement: `The checklist implies a reviewer can skip an approval gate, which should be clarified to ensure all approvals are strictly followed and accurately documented, especially before compliance reviews.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'skip one approval gate'.

3. Category: `PROFESSIONALISM_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `20-21`
   Source text: `One note also says the build summary reads like a rushed internal update, which should be cleaned up before it appears in a release packet.`
   Explanation: `Describing a build summary as a 'rushed internal update' suggests a lack of professionalism and polish, which is inappropriate for content that will appear in a 'release packet' (implying external distribution).`
   Recommendation: `Ensure all external-facing documentation, including build summaries, maintains a professional and polished tone.`
   Suggested replacement: `One note also says the build summary currently reflects an internal draft, which should be finalized and polished before it appears in a release packet.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'reads like a rushed internal update'.

4. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `TERM_MATCH`
   Lines: `46-46`
   Source text: `Preview stage: `atlas-preview``
   Explanation: `The label `atlas-preview` directly exposes the internal codename 'Atlas'. Exposing internal codenames in documentation can lead to unintended information disclosure.`
   Recommendation: `Replace the internal codename 'atlas' with a generic or external-facing name for the preview stage.`
   Suggested replacement: `Preview stage: `portal-preview``
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### feature_flags.ts

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/config/feature_flags.ts`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/config/feature_flags.json`
- Metrics: `TP=3`, `FP=1`, `FN=0`
- Actual finding count: `4`
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
   Matched actual: `INTERNAL_CODENAME_EXPOSURE` on lines `29-30`

2. Category: `COMPLIANCE_RISK`
   Target text contains: `approval switch as optional`
   Lines: `32-33`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `COMPLIANCE_RISK` on lines `31-32`

3. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Atlas review toggle name`
   Lines: `34-34`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched and target text matched.
   Matched actual: `INTERNAL_CODENAME_EXPOSURE` on lines `33-33`

#### Actual Findings

1. Category: `INTELLECTUAL_PROPERTY_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `1-3`
   Source text: `Feature flag defaults for the Atlas Ops Portal preview environment.`
   Explanation: `Mentioning a 'preview environment' name in public-facing or internally shared source code without careful control could reveal unreleased product information or internal development stages.`
   Recommendation: `Rephrase to use a more generic term like 'development' or 'staging environment' or ensure the text is only visible to approved audiences.`
   Suggested replacement: `Feature flag defaults for the development environment.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `29-30`
   Source text: `The rollout note still mentions Project Atlas as the internal feature bundle name for partner-facing documentation.`
   Explanation: `The internal codename 'Project Atlas' is explicitly mentioned as being present in partner-facing documentation, indicating a potential unapproved disclosure of an internal project name to external partners. The phrase 'still mentions' suggests an existing oversight.`
   Recommendation: `Remove or replace the internal codename 'Project Atlas' in partner-facing documentation. Update documentation to reflect correct, external-facing product names.`
   Suggested replacement: `The rollout note still mentions the internal feature bundle name for partner-facing documentation.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Project Atlas'.

3. Category: `COMPLIANCE_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `31-32`
   Source text: `Compliance note: do not describe the export approval switch as optional in the release summary because that wording is inaccurate.`
   Explanation: `The note highlights a compliance risk by warning against inaccurate wording in a release summary regarding an 'export approval switch', which could mislead external stakeholders or violate compliance standards.`
   Recommendation: `Ensure all external communications, especially release summaries, accurately reflect product features and their status.`
   Suggested replacement: `Compliance note: ensure accurate wording for the export approval switch in the release summary to avoid misrepresentation.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'approval switch as optional'.

4. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `33-33`
   Source text: `The Atlas review toggle name is also visible in one screenshot caption.`
   Explanation: `The name 'Atlas' (likely referring to 'Project Atlas') is reported as visible in a screenshot caption, which could inadvertently expose an internal codename to external audiences.`
   Recommendation: `Review and redact or rephrase screenshot captions to remove internal project names or codenames before external publication.`
   Suggested replacement: `The internal review toggle name is also visible in one screenshot caption.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Atlas review toggle name'.

### credential-rotation-guide.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/docs/credential-rotation-guide.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/docs/credential-rotation-guide.json`
- Metrics: `TP=0`, `FP=3`, `FN=0`
- Actual finding count: `3`
- Expected finding count range: `0` to `0`
- Count range satisfied: `no`

#### Expected Findings

- None expected.

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `5-6`
   Source text: `This guide explains how the Atlas Ops Portal team documents credential rotation tasks for internal review and partner-facing launch preparation.`
   Explanation: `The text mentions 'Atlas Ops Portal team', which contains 'Atlas', a likely reference to the internal codename 'Project Atlas'. Exposing internal project names, especially in a document pertaining to 'partner-facing launch preparation', constitutes an internal codename exposure risk.`
   Recommendation: `Replace the internal project codename 'Atlas' with a generic or public-facing name to avoid exposing internal project details to a broader audience, including partners.`
   Suggested replacement: `This guide explains how the platform operations team documents credential rotation tasks for internal review and partner-facing launch preparation.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `REPUTATION_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `52-52`
   Source text: `Partner review material excludes internal runbook details.`
   Explanation: `The instruction implies that 'internal runbook details' are considered sensitive and should not be shared with partners, indicating a potential risk if this guidance is not followed. Exposure of such details could lead to a reputation risk.`
   Recommendation: `Ensure strict processes are in place to redact or omit all sensitive internal operational details from any material shared externally with partners.`
   Suggested replacement: `Partner review material focuses on publicly relevant information.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

3. Category: `REPUTATION_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `60-60`
   Source text: `Confirm partner-facing materials do not include internal runbook detail.`
   Explanation: `This instruction highlights the need to prevent exposure of 'internal runbook detail' in partner-facing materials, indicating a potential reputation risk if confidential internal information is inadvertently shared externally.`
   Recommendation: `Maintain rigorous protocols for reviewing and redacting any internal operational specifics from documents prepared for external partners.`
   Suggested replacement: `Confirm partner-facing materials include only externally approved information.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### incident-retrospective.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/docs/incident-retrospective.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/docs/incident-retrospective.json`
- Metrics: `TP=1`, `FP=2`, `FN=1`
- Actual finding count: `3`
- Expected finding count range: `2` to `2`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `REPUTATION_RISK`
   Target text contains: `team was careless during launch prep`
   Lines: `22-23`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: Category matched but neither target text nor line range matched the expected finding.

2. Category: `COMPLIANCE_RISK`
   Target text contains: `bypassing the normal approval trace`
   Lines: `26-26`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `COMPLIANCE_RISK` on lines `26-28`

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `5-6`
   Source text: `This internal retrospective documents a failed preview deployment in the Atlas Ops Portal partner review environment.`
   Explanation: `The text exposes the internal codename "Atlas" (part of 'Project Atlas') in relation to a "partner review environment", which could lead to unintended disclosure of internal project names to external parties if the document is not strictly confined to internal audiences.`
   Recommendation: `Replace the internal codename with a generic description or a redacted placeholder.`
   Suggested replacement: `This internal retrospective documents a failed preview deployment in the partner review environment.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `COMPLIANCE_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `26-28`
   Source text: `One section also describes bypassing the normal approval trace for a temporary deployment fix, which should be rewritten to reflect the approved remediation path.`
   Explanation: `The text explicitly states that a section describes "bypassing the normal approval trace," which signifies a deviation from standard operating procedures and represents a compliance risk.`
   Recommendation: `Rephrase the section to focus on the approved remediation path without detailing the bypass.`
   Suggested replacement: `One section describes a temporary deployment fix, and it should be rewritten to reflect the approved remediation path.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'bypassing the normal approval trace'.

3. Category: `REPUTATION_RISK`
   Severity: `LOW`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `57-60`
   Source text: `The team kept the retrospective because it explains how release process changes were introduced after the incident. That internal context is useful, but it should still be framed carefully when any summary is reused outside the core team.`
   Explanation: `The text explicitly states that the document contains "internal context" that needs "careful framing" if "reused outside the core team," indicating a potential reputation risk if shared without proper sanitization.`
   Recommendation: `Review any external summaries derived from this document to ensure sensitive internal context is appropriately sanitized or omitted.`
   Suggested replacement: `(none)`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### partner-integration.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/docs/partner-integration.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/docs/partner-integration.json`
- Metrics: `TP=4`, `FP=4`, `FN=0`
- Actual finding count: `8`
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
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `COMPLIANCE_RISK` on lines `33-35`

3. Category: `INTELLECTUAL_PROPERTY_RISK`
   Target text contains: `vendor packet`
   Lines: `37-38`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `INTELLECTUAL_PROPERTY_RISK` on lines `37-38`

4. Category: `REPUTATION_RISK`
   Target text contains: `avoidable confusion`
   Lines: `40-41`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `REPUTATION_RISK` on lines `40-41`

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `5-6`
   Source text: `This document explains how approved partners review customer records inside the Atlas Ops Portal during launch preparation and external sharing checks.`
   Explanation: `The term 'Atlas' is a sensitive internal codename. Its use in 'Atlas Ops Portal' in a partner-facing document exposes internal system names and codenames, posing a risk of revealing confidential information about internal infrastructure.`
   Recommendation: `Replace the internal codename and specific system reference with a generic, partner-facing term that does not expose internal project names or system details.`
   Suggested replacement: `This document explains how approved partners review customer records inside the Partner Customer Review Portal during launch preparation and external sharing checks.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `16-19`
   Source text: `Partners receive a limited view of customer account details, audit summaries, and release readiness notes. The intent is to support structured partner review without exposing internal implementation details that belong only to the Atlas operations team.`
   Explanation: `The term 'Atlas' is a sensitive internal codename. Referring to the 'Atlas operations team' exposes an internal codename and organizational structure to partners, which could be considered confidential information.`
   Recommendation: `Remove the internal codename and generalize the team reference to avoid exposing internal project names or team structures.`
   Suggested replacement: `Partners receive a limited view of customer account details, audit summaries, and release readiness notes. The intent is to support structured partner review without exposing internal implementation details that belong only to our operations team.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

3. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `30-31`
   Source text: `This guide still references Project Atlas in one of the rollout notes, and that codename should be removed before the document is shared externally.`
   Explanation: `The sensitive term 'Project Atlas' is explicitly mentioned. Although the text states it 'should be removed', its current presence in a document intended for external sharing creates a direct risk of exposing an internal codename.`
   Recommendation: `Replace the explicit codename reference with a generic term to prevent the exposure of internal project names.`
   Suggested replacement: `This guide still references the project codename in one of the rollout notes, and that codename should be removed before the document is shared externally.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Project Atlas'.

4. Category: `COMPLIANCE_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `33-35`
   Source text: `Partner-facing instructions should avoid implying that release approvals are handled informally because that language can create unnecessary compliance concerns during audit review.`
   Explanation: `This instruction highlights a significant compliance risk: implying informal release approvals can lead to 'unnecessary compliance concerns during audit review.' While this text is a warning, it points to a critical issue in how language is used, indicating a potential vulnerability in the document's overall compliance posture if the advice is not followed.`
   Recommendation: `Ensure all partner-facing instructions clearly communicate formal and structured release approval processes. Review existing language to remove any phrasing that could be interpreted as informal or lacking due process.`
   Suggested replacement: `(none)`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'handled informally'.

5. Category: `INTELLECTUAL_PROPERTY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `37-38`
   Source text: `The appendix should not quote licensed onboarding language copied from the vendor packet because that wording is not ours to republish in partner docs.`
   Explanation: `This text identifies a clear intellectual property risk by warning against quoting 'licensed onboarding language copied from the vendor packet' that is 'not ours to republish.' The presence of this warning suggests that such a practice might occur or has occurred, indicating a need for vigilance.`
   Recommendation: `Strictly prohibit the unauthorized reproduction or quoting of any licensed materials from vendors. Verify that all content shared with partners is original or has explicit publishing rights.`
   Suggested replacement: `(none)`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'vendor packet'.

6. Category: `REPUTATION_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `40-41`
   Source text: `The draft note saying the export preview could create avoidable confusion for customers should also be revised before launch.`
   Explanation: `This text indicates an internal concern that the 'export preview could create avoidable confusion for customers.' Exposing such a 'draft note' to partners could undermine confidence in the product or company, posing a reputation risk.`
   Recommendation: `Before external sharing, remove or rephrase any internal notes or discussions about potential customer confusion regarding product features. Present a polished and confident message to partners.`
   Suggested replacement: `(none)`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'avoidable confusion'.

7. Category: `PROFESSIONALISM_RISK`
   Severity: `LOW`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `89-89`
   Source text: ``config/feature_flags.ts``
   Explanation: `Exposing internal file paths, such as `config/feature_flags.ts`, in partner-facing documentation is unprofessional and can reveal unnecessary internal system architecture details.`
   Recommendation: `Avoid listing specific internal file paths in external documents. Refer to features or configurations generically if necessary.`
   Suggested replacement: `(none)`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

8. Category: `PROFESSIONALISM_RISK`
   Severity: `LOW`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `91-91`
   Source text: ``frontend/support_banner.html``
   Explanation: `Exposing internal file paths, such as `frontend/support_banner.html`, in partner-facing documentation is unprofessional and can reveal unnecessary internal system architecture details.`
   Recommendation: `Avoid listing specific internal file paths in external documents. Refer to features or components generically if necessary.`
   Suggested replacement: `(none)`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### release-checklist.md

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/docs/release-checklist.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/docs/release-checklist.json`
- Metrics: `TP=2`, `FP=2`, `FN=0`
- Actual finding count: `4`
- Expected finding count range: `2` to `2`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `PROFESSIONALISM_RISK`
   Target text contains: `sounds sloppy`
   Lines: `24-25`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched and line range matched.
   Matched actual: `PROFESSIONALISM_RISK` on lines `24-25`

2. Category: `COMPLIANCE_RISK`
   Target text contains: `manual exception`
   Lines: `27-28`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `COMPLIANCE_RISK` on lines `27-28`

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `5-6`
   Source text: `Atlas Ops Portal`
   Explanation: `The text mentions 'Atlas Ops Portal', which contains the internal codename 'Atlas'. This document is intended for external sharing and partner review, risking exposure of an internal project name.`
   Recommendation: `Replace 'Atlas Ops Portal' with a neutral, publicly approved project name or a generic description.`
   Suggested replacement: `the relevant portal`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `PROFESSIONALISM_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `24-25`
   Source text: `sloppy`
   Explanation: `The term 'sloppy' is unprofessional and subjective, especially when referring to internal work that may be seen externally.`
   Recommendation: `Replace unprofessional language with neutral, objective descriptions.`
   Suggested replacement: `needs refinement`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'sounds sloppy'.

3. Category: `COMPLIANCE_RISK`
   Severity: `CRITICAL`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `27-28`
   Source text: `a manual exception can be used without the normal review path`
   Explanation: `The text implies that a manual exception might bypass normal review processes, which is a significant compliance and audit risk. This needs immediate correction to ensure proper process adherence.`
   Recommendation: `Clarify the approval process to ensure all exceptions follow an approved, documented review path. The language should reflect strict adherence to audit-compliant procedures.`
   Suggested replacement: `exceptions must follow the normal review path`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'manual exception'.

4. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `LOW`
   Confidence: `HIGH`
   Detection method: `TERM_MATCH`
   Lines: `39-39`
   Source text: ``ATLAS-EXAMPLE-1``
   Explanation: `The example change ticket `ATLAS-EXAMPLE-1` contains the internal codename 'ATLAS'.`
   Recommendation: `Replace the internal codename 'ATLAS' in the example label with a generic placeholder or a publicly approved prefix.`
   Suggested replacement: ``PROJECT-EXAMPLE-1``
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### account_settings.ts

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/frontend/account_settings.ts`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/frontend/account_settings.json`
- Metrics: `TP=2`, `FP=3`, `FN=1`
- Actual finding count: `5`
- Expected finding count range: `3` to `3`
- Count range satisfied: `no`

#### Expected Findings

1. Category: `PROFESSIONALISM_RISK`
   Target text contains: `sounds sloppy`
   Lines: `57-58`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `PROFESSIONALISM_RISK` on lines `58-59`

2. Category: `REPUTATION_RISK`
   Target text contains: `complain before we fix the workflow`
   Lines: `59-60`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `REPUTATION_RISK` on lines `60-61`

3. Category: `REPUTATION_RISK`
   Target text contains: `internal-only workaround`
   Lines: `61-62`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `2-2`
   Source text: `Atlas customer portal`
   Explanation: `The term 'Atlas' is identified as an internal codename. Its appearance in the context of a 'customer portal' risks exposing internal project information to external audiences.`
   Recommendation: `Replace the internal codename 'Atlas' with a generic or official public-facing product name to prevent disclosure of confidential project information.`
   Suggested replacement: `product customer portal`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `PROFESSIONALISM_RISK`
   Severity: `LOW`
   Confidence: `MEDIUM`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `3-4`
   Source text: `This file handles customer preferences that also appear during partner review demonstrations and release walkthroughs.`
   Explanation: `Referring to 'partner review demonstrations' and 'release walkthroughs' in a customer-facing docstring can be unprofessional by revealing internal process details.`
   Recommendation: `Rephrase to focus on the customer benefit or the feature itself, rather than internal review processes, to maintain a professional tone.`
   Suggested replacement: `This file handles customer preferences.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

3. Category: `PROFESSIONALISM_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `58-59`
   Source text: `FIXME: the partner access helper text still sounds sloppy in the release preview and makes the settings page feel unfinished.`
   Explanation: `Using terms like 'sloppy' and 'unfinished' to describe external-facing content (partner access helper text in a release preview) is unprofessional and can negatively impact perception.`
   Recommendation: `Rewrite the comment to be objective and constructive, focusing on the necessary improvements rather than subjective, negative descriptions.`
   Suggested replacement: `FIXME: Refine the partner access helper text for clarity and completeness in the release preview.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'sounds sloppy'.

4. Category: `REPUTATION_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `60-61`
   Source text: `The launch note about manual escalation also reads like we expect customers to complain before we fix the workflow.`
   Explanation: `This statement implies an expectation of customer issues and a reactive approach, which can severely damage customer trust and company reputation if exposed.`
   Recommendation: `Address the underlying workflow issues proactively and rephrase any public-facing notes to focus on solutions and positive customer experience, avoiding language that anticipates failure.`
   Suggested replacement: `The launch note about workflow should be updated to reflect a more robust and proactive solution.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'complain before we fix the workflow'.

5. Category: `SECURITY_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `62-63`
   Source text: `The hidden reset path note should not appear in the partner walkthrough because it suggests an internal-only workaround.`
   Explanation: `Mentioning a 'hidden reset path' and explicitly stating it's an 'internal-only workaround' that 'should not appear in the partner walkthrough' indicates a risk of exposing sensitive internal system details or operational procedures to external partners.`
   Recommendation: `Remove this comment or rephrase it to describe the required action (e.g., 'Ensure no internal diagnostic or recovery information is disclosed externally') without revealing sensitive details.`
   Suggested replacement: `Ensure that internal diagnostic or recovery information is not disclosed during partner presentations.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### admin_debug.js

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/frontend/admin_debug.js`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/frontend/admin_debug.json`
- Metrics: `TP=3`, `FP=0`, `FN=0`
- Actual finding count: `3`
- Expected finding count range: `3` to `3`
- Count range satisfied: `yes`

#### Expected Findings

1. Category: `SECURITY_RISK`
   Target text contains: `temporary support token note`
   Lines: `33-33`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched and target text matched.
   Matched actual: `SECURITY_RISK` on lines `32-32`

2. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Project Atlas`
   Lines: `34-34`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched and target text matched.
   Matched actual: `INTERNAL_CODENAME_EXPOSURE` on lines `33-33`

3. Category: `SECURITY_RISK`
   Target text contains: `bypassing audit logging`
   Lines: `35-36`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `SECURITY_RISK` on lines `34-35`

#### Actual Findings

1. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `32-32`
   Source text: `TODO: remove the temporary support token note before partner review.`
   Explanation: `The text refers to a 'temporary support token note' which implies exposure of internal credentials or sensitive information to external partners. This poses a security risk.`
   Recommendation: `Remove or rephrase the mention of internal credentials or support tokens before partner review to prevent sensitive information disclosure.`
   Suggested replacement: `TODO: remove the temporary confidential note before partner review.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary support token note'.

2. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `33-33`
   Source text: `The Atlas admin preview still mentions Project Atlas in the export path log.`
   Explanation: `The sensitive term 'Project Atlas' is mentioned in the context of an 'export path log', indicating potential exposure of an internal codename in an output that might be accessible externally.`
   Recommendation: `Replace 'Project Atlas' with a generic or public-facing name to prevent the disclosure of internal project codenames.`
   Suggested replacement: `The admin preview still mentions an internal project name in the export path log.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Project Atlas'.

3. Category: `SECURITY_RISK`
   Severity: `CRITICAL`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `34-35`
   Source text: `The debug note about bypassing audit logging should not appear in release preview output because it suggests an unsafe internal workaround.`
   Explanation: `The text explicitly mentions 'bypassing audit logging' as an 'unsafe internal workaround' that should not appear in release preview. This indicates a critical security and compliance vulnerability related to system integrity and accountability.`
   Recommendation: `Remove any mention of bypassing audit logging or unsafe internal workarounds from public-facing output. Address the underlying workaround to ensure proper security and compliance controls.`
   Suggested replacement: `The debug note about an unsafe internal workaround should not appear in release preview output.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'bypassing audit logging'.

### support_banner.html

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/frontend/support_banner.html`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/frontend/support_banner.json`
- Metrics: `TP=1`, `FP=1`, `FN=1`
- Actual finding count: `2`
- Expected finding count range: `2` to `2`
- Count range satisfied: `yes`

#### Expected Findings

1. Category: `PROFESSIONALISM_RISK`
   Target text contains: `Keep the partner support message professional`
   Lines: `15-15`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `PROFESSIONALISM_RISK` on lines `15-15`

2. Category: `REPUTATION_RISK`
   Target text contains: `fallback copy still sounds defensive`
   Lines: `16-16`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `PROFESSIONALISM_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `15-15`
   Source text: `Keep the partner support message professional before external sharing.`
   Explanation: `The comment emphasizes the need for professionalism in external communications, indicating a focus on maintaining a suitable tone for partner messages shared externally.`
   Recommendation: `Ensure all external-facing communications maintain a professional and appropriate tone.`
   Suggested replacement: `Ensure the partner support message maintains a professional tone for external sharing.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Keep the partner support message professional'.

2. Category: `PROFESSIONALISM_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `16-16`
   Source text: `The fallback copy still sounds defensive and could make the portal look unreliable.`
   Explanation: `The comment expresses concern that the fallback copy's tone is defensive and could negatively impact the portal's perceived reliability, suggesting a professionalism risk.`
   Recommendation: `Review and revise the fallback copy to ensure it conveys a confident and reliable message, avoiding defensive language.`
   Suggested replacement: `The fallback copy requires revision to enhance its tone and ensure it projects reliability.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### roadmap-notes.md

- Status: `PASS`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/project/roadmap-notes.md`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/project/roadmap-notes.json`
- Metrics: `TP=4`, `FP=0`, `FN=0`
- Actual finding count: `4`
- Expected finding count range: `4` to `4`
- Count range satisfied: `yes`

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
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `PROFESSIONALISM_RISK` on lines `20-21`

3. Category: `REPUTATION_RISK`
   Target text contains: `look unprepared`
   Lines: `23-24`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `REPUTATION_RISK` on lines `23-24`

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
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `17-18`
   Source text: `The roadmap still uses Project Atlas in two planning bullets, which should be removed before any external sharing of the release packet.`
   Explanation: `The text explicitly mentions "Project Atlas", a known internal codename, and states it should be removed before external sharing, indicating a clear risk of exposure.`
   Recommendation: `Replace or remove the internal codename "Project Atlas" from the roadmap before any external distribution.`
   Suggested replacement: `The roadmap still uses the internal project codename in two planning bullets, which should be removed before any external sharing of the release packet.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Project Atlas in two planning bullets'.

2. Category: `PROFESSIONALISM_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `20-21`
   Source text: `One draft note says the support workflow looks amateurish during preview, which should be rewritten in more professional language.`
   Explanation: `The term "amateurish" is unprofessional and can be perceived negatively. The text itself acknowledges the need for more professional language.`
   Recommendation: `Rewrite the description of the support workflow to use professional and constructive language.`
   Suggested replacement: `One draft note says the support workflow needs refinement during preview, which should be rewritten in more professional language.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'looks amateurish'.

3. Category: `REPUTATION_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `23-24`
   Source text: `Another item warns that the launch summary could make the team look unprepared if the current wording is copied into release notes.`
   Explanation: `The text expresses concern that current wording could negatively impact the team's reputation if used in external release notes.`
   Recommendation: `Review and revise the launch summary to ensure professional and positive language before external release.`
   Suggested replacement: `Another item warns that the launch summary could present an incomplete picture if the current wording is copied into release notes.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'look unprepared'.

4. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `26-27`
   Source text: `The archived planning section also repeats the Project Atlas codename in a feature comparison block that should stay internal only.`
   Explanation: `The text explicitly mentions "Project Atlas", a known internal codename, and states it should stay internal only, indicating a clear risk of exposure if mishandled.`
   Recommendation: `Ensure "Project Atlas" is removed or anonymized in any content intended for external audiences.`
   Suggested replacement: `The archived planning section also repeats the internal project codename in a feature comparison block that should stay internal only.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Project Atlas codename'.

### bootstrap_env.py

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/scripts/bootstrap_env.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/scripts/bootstrap_env.json`
- Metrics: `TP=3`, `FP=2`, `FN=0`
- Actual finding count: `5`
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
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `PROFESSIONALISM_RISK` on lines `38-38`

3. Category: `COMPLIANCE_RISK`
   Target text contains: `approval tagging can be skipped`
   Lines: `40-41`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `COMPLIANCE_RISK` on lines `40-40`

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `1-1`
   Source text: `Bootstrap helpers for local Atlas preview environments.`
   Explanation: `The docstring mentions "Atlas preview environments," which exposes an internal project codename and details about internal environments. The term "Atlas" is part of the configured sensitive term "Project Atlas," and the surrounding context adds semantic risk by detailing the type of internal system.`
   Recommendation: `Avoid mentioning internal project codenames and specific internal environment types in publicly accessible code or documentation. Use generic terms or remove if not critical for external understanding.`
   Suggested replacement: `Bootstrap helpers for local preview environments.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `37-37`
   Source text: `TODO: remove the temporary bootstrap secret reminder before external sharing.`
   Explanation: `The TODO comment indicates a "temporary bootstrap secret reminder" needs to be removed before "external sharing," suggesting the presence or a reminder of a sensitive secret in the codebase that should not be exposed externally.`
   Recommendation: `Remove all references to temporary secrets or credentials before any external sharing. Ensure secrets are handled securely and not mentioned in comments.`
   Suggested replacement: `TODO: remove temporary credential references before external sharing.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary bootstrap secret reminder'.

3. Category: `PROFESSIONALISM_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `38-38`
   Source text: `The setup note calling the preview script half-baked should be rewritten`
   Explanation: `The comment uses unprofessional and critical language ("half-baked") to describe a preview script, which can reflect poorly on the project or team if exposed externally.`
   Recommendation: `Use objective and professional language in all comments and documentation. Avoid disparaging remarks about code or processes.`
   Suggested replacement: `The setup note describing the preview script as incomplete should be rewritten`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'calling the preview script half-baked'.

4. Category: `COMPLIANCE_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `40-40`
   Source text: `The bootstrap checklist still says approval tagging can be skipped on`
   Explanation: `The comment indicates that "approval tagging can be skipped," which suggests a potential bypass of standard procedures that could lead to compliance or security vulnerabilities, especially when combined with the next line about "temporary partner review machines."`
   Recommendation: `All processes, including approval tagging, should be consistently applied unless there is a documented, secure, and approved exception. Avoid shortcuts that may compromise security or compliance.`
   Suggested replacement: `The bootstrap checklist mentions a process for temporary environments.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'approval tagging can be skipped'.

5. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `42-42`
   Source text: `Placeholder example only: ATLAS_SAMPLE_KEY=example-key`
   Explanation: `The comment includes "ATLAS_SAMPLE_KEY," which exposes a naming convention tied to an internal project codename ("Atlas"), even if it's an example. This could inadvertently reveal internal structures. The term "ATLAS" is part of the configured sensitive term "Project Atlas," and the context of a "SAMPLE_KEY" adds semantic risk.`
   Recommendation: `Avoid using internal project codenames even in placeholder examples for keys or variables. Use generic placeholders like `PLACEHOLDER_KEY` or `PROJECT_SAMPLE_KEY`.`
   Suggested replacement: `Placeholder example only: PROJECT_SAMPLE_KEY=example-key`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### deploy_preview.js

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/scripts/deploy_preview.js`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/scripts/deploy_preview.json`
- Metrics: `TP=2`, `FP=2`, `FN=1`
- Actual finding count: `4`
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
   Matched actual: `SECURITY_RISK` on lines `31-31`

2. Category: `INTERNAL_CODENAME_EXPOSURE`
   Target text contains: `Project Atlas`
   Lines: `32-32`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `INTERNAL_CODENAME_EXPOSURE` on lines `32-32`

3. Category: `COMPLIANCE_RISK`
   Target text contains: `release tag can be skipped`
   Lines: `33-34`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `FN`
   Reasoning: No actual finding matched the expected category and text/line rule.

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `2-2`
   Source text: `Atlas partner review environment`
   Explanation: `The term 'Atlas', likely an internal project codename, is mentioned in the context of a 'partner review environment', suggesting potential exposure of internal terminology to external parties.`
   Recommendation: `Replace internal codenames with generic or externally appropriate terms when communicating with partners.`
   Suggested replacement: `the platform's partner review environment`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `31-31`
   Source text: `TODO: remove the temporary deployment token reminder before launch.`
   Explanation: `Mentions a 'temporary deployment token reminder' that needs removal before launch, indicating potential exposure of a security-sensitive item.`
   Recommendation: `Avoid mentioning temporary credentials or security-sensitive configuration details in publicly accessible or long-lived documentation. Ensure proper credential management.`
   Suggested replacement: `TODO: remove temporary credential references before launch.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary deployment token reminder'.

3. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `HYBRID`
   Lines: `32-32`
   Source text: `The Project Atlas preview label still appears in the deployment notes.`
   Explanation: `The internal codename 'Project Atlas' is mentioned in deployment notes, which may be exposed externally.`
   Recommendation: `Replace internal project codenames with generic or externally appropriate terms in deployment notes.`
   Suggested replacement: `The project's preview label still appears in the deployment notes.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'Project Atlas'.

4. Category: `PROFESSIONALISM_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `33-34`
   Source text: `The fallback upload note still says the release tag can be skipped during partner review retries.`
   Explanation: `This statement reveals internal operational details about release tagging procedures during partner review, which might be unprofessional or unnecessary to expose.`
   Recommendation: `Avoid including internal procedural specifics in documentation that may be viewed by external partners. Focus on outcomes rather than internal steps.`
   Suggested replacement: `(none)`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

### access_review.py

- Status: `FAIL`
- Case file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/cases/repository_benchmark/security/access_review.py`
- Expected file: `C:/Users/phili/Desktop/semantic-compliance-review-agent/evaluation/expected/repository_benchmark/security/access_review.json`
- Metrics: `TP=4`, `FP=4`, `FN=0`
- Actual finding count: `8`
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
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `COMPLIANCE_RISK` on lines `57-57`

3. Category: `INTELLECTUAL_PROPERTY_RISK`
   Target text contains: `licensed wording is not ours to reuse`
   Lines: `59-60`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched and line range matched.
   Matched actual: `INTELLECTUAL_PROPERTY_RISK` on lines `59-59`

4. Category: `REPUTATION_RISK`
   Target text contains: `could look careless during review`
   Lines: `61-62`
   Approximate line match allowed: `true`
   Suggested replacement required: `false`
   Outcome: `TP`
   Reasoning: Category matched, target text matched, and line range matched.
   Matched actual: `REPUTATION_RISK` on lines `61-61`

#### Actual Findings

1. Category: `INTERNAL_CODENAME_EXPOSURE`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `TERM_MATCH`
   Lines: `1-1`
   Source text: `Access review notes for Atlas launch preparation and partner handoff.`
   Explanation: `The text mentions 'Atlas', which is identified as an internal codename. Exposing internal project codenames can reveal sensitive information about ongoing or upcoming initiatives.`
   Recommendation: `Replace the internal codename 'Atlas' with a generic or descriptive term to prevent premature disclosure of project details.`
   Suggested replacement: `Access review notes for launch preparation and partner handoff.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

2. Category: `SECURITY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `56-56`
   Source text: `TODO: remove the temporary credential note from the access review appendix.`
   Explanation: `The text refers to a 'temporary credential note', which indicates the presence or handling of sensitive access information that should be removed or secured, posing a security risk.`
   Recommendation: `Ensure all temporary credentials or references to them are properly secured or removed before release. Update the note to be generic or remove it entirely if the issue is resolved.`
   Suggested replacement: `TODO: remove the temporary access information from the access review appendix.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'temporary credential note'.

3. Category: `COMPLIANCE_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `57-57`
   Source text: `Compliance note: one reviewer checklist still says approval can proceed`
   Explanation: `The comment indicates an inconsistency in a reviewer checklist regarding approval procedures, which could lead to non-compliance if approvals proceed without meeting all necessary criteria.`
   Recommendation: `Clarify or update the reviewer checklist to ensure consistent compliance requirements are met before approval.`
   Suggested replacement: `Compliance note: ensure all reviewer checklist items are complete before final approval.`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'approval can proceed'.

4. Category: `COMPLIANCE_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `58-58`
   Source text: `before the audit attachment is complete.`
   Explanation: `This line, in context with the previous one, highlights a compliance risk where approvals might proceed before a crucial 'audit attachment' is complete, potentially undermining audit integrity.`
   Recommendation: `Ensure all required audit attachments are complete and verified before any related approvals are granted.`
   Suggested replacement: `All audit attachments must be complete.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

5. Category: `INTELLECTUAL_PROPERTY_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `59-59`
   Source text: `The vendor packet excerpt in the appendix should not be copied into our`
   Explanation: `The text advises against copying a 'vendor packet excerpt', implying potential intellectual property or licensing restrictions on the material.`
   Recommendation: `Avoid copying vendor materials unless explicit permission or licensing terms allow it. Refer to or link external vendor documentation instead of duplicating it internally.`
   Suggested replacement: `Vendor packet excerpts should not be copied into our`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'licensed wording is not ours to reuse'.

6. Category: `INTELLECTUAL_PROPERTY_RISK`
   Severity: `HIGH`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `60-60`
   Source text: `repository notes because the licensed wording is not ours to reuse.`
   Explanation: `The text explicitly states that 'licensed wording is not ours to reuse', indicating a direct intellectual property restriction and the need to prevent unauthorized reuse.`
   Recommendation: `Strictly adhere to licensing terms for third-party content. Ensure no copyrighted or licensed material is reused without proper authorization.`
   Suggested replacement: `repository notes due to licensing restrictions.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

7. Category: `REPUTATION_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `61-61`
   Source text: `The line saying the partner portal could look careless during review should be`
   Explanation: `The comment points out that a statement in the 'partner portal' could be perceived as 'careless', indicating a potential reputational risk if exposed to partners or external parties.`
   Recommendation: `Review and revise all external-facing communications, especially in partner portals, to maintain a professional and diligent image.`
   Suggested replacement: `The line regarding the partner portal's presentation during review should be`
   Outcome: `Matched`
   Reasoning: Matched expected finding 'could look careless during review'.

8. Category: `REPUTATION_RISK`
   Severity: `MEDIUM`
   Confidence: `HIGH`
   Detection method: `SEMANTIC_ANALYSIS`
   Lines: `62-62`
   Source text: `revised before launch prep is shared outside the core team.`
   Explanation: `This comment indicates that 'launch prep' materials, potentially containing sensitive or unpolished information, are intended for external sharing and need revision to avoid negative perceptions, posing a reputational risk.`
   Recommendation: `Ensure all external communications and shared materials are thoroughly reviewed and polished for professionalism and accuracy before being shared outside the core team.`
   Suggested replacement: `revised before external sharing.`
   Outcome: `FP`
   Reasoning: Unmatched actual finding.

## Notes

- Gemini evaluation results represent a snapshot captured at a specific point in time. Because LLM outputs may vary between runs, these results should be interpreted as evaluation evidence rather than a perfectly reproducible benchmark.
- Gemini results validate the current live semantic review path without changing prompts, matching rules, or the dataset.
- Suggested replacement matching is required only for expected findings that explicitly demand it.
- Severity is displayed for context but does not determine TP, FP, or FN in this evaluation implementation.
