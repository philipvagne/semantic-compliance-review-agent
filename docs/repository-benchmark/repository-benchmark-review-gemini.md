# Repository Benchmark Review - Gemini

## Executive Summary

The completed Gemini repository benchmark produced `0.51` precision and `0.82`
recall across 20 repository-style files. The run surfaced a wide portion of
the expected benchmark content and demonstrated strong semantic coverage across
all supported finding categories. At the same time, it generated a large number
of additional findings that the benchmark did not expect.

The overall outcome is therefore mixed but highly informative. Gemini behaved
like a broad contextual reviewer rather than a narrow benchmark-matching
system. It often found the intended issues, but it also inferred extra
codename, tone, or disclosure risks from surrounding context. The benchmark
successfully exposed both the strengths of that broader reasoning and the cost
of that reasoning under a strict TP/FP/FN scoring model.

## Benchmark Performance

The benchmark contained 49 expected findings. The Gemini run produced 40 true
positives, 38 false positives, and 9 false negatives.

These metrics suggest a very different profile from a narrow detector. Gemini
usually found the benchmark's intended concerns, but it also regularly expanded
the review surface beyond the expected JSON. Most failures therefore came from
overproduction and category/granularity mismatches, not from complete silence.

Only 2 files passed exactly:

- `frontend/admin_debug.js`
- `project/roadmap-notes.md`

Many other files came close to exact alignment but failed because Gemini added
extra findings, split one expected concept into multiple findings, or chose a
different but defensible category.

## False Positive Analysis

The 38 false positives do not form one single pattern. They break into several
meaningfully different groups.

### Reasonable Additional Observations

A substantial share of the false positives appear to be plausible additional
observations rather than obvious review mistakes.

- Extra internal codename exposure findings were common in top-of-file
  docstrings and descriptive comments that referenced `Atlas` or `Atlas Ops
  Portal` in externally adjacent contexts.
- Some additional professionalism or reputation findings highlighted wording
  that a human reviewer might also flag even though the benchmark expected a
  different category or fewer findings.
- Some extra compliance and intellectual-property findings were line-level
  decompositions of a broader expected concern rather than unrelated output.

Examples:

- `security/access_review.py` produced separate additional findings for the
  second line of a compliance concern, the second half of the intellectual
  property concern, and the second half of the reputational concern.
- `docs/partner-integration.md` produced extra codename findings in the file
  introduction and extra professionalism findings for linked file references.
- `backend/customer_export.py` produced two additional `REPUTATION_RISK`
  findings around internal review outcomes even though the expected JSON framed
  that section as `COMPLIANCE_RISK`.

### Internal Codename Over-Reporting

The dominant strict false-positive pattern was additional
`INTERNAL_CODENAME_EXPOSURE`. There were 20 unmatched codename findings.

This pattern showed up in:

- file docstrings such as `auth/session_manager.py`, `backend/billing_rules.py`,
  `backend/customer_export.py`, and `security/access_review.py`
- public or partner-facing framing text such as `api/public_status.js`
- placeholder or example labels such as `scripts/bootstrap_env.py`
- general repository references such as `docs/credential-rotation-guide.md`
  and `ci/build_summary.html`

Some of these are arguably reasonable from a human-review perspective, because
the fictional benchmark repository repeatedly places the product name in
partner-facing or external-sharing contexts. Others, such as the fictional
`Project Comet` comment in `ci/build_summary.html` or `ATLAS-EXAMPLE-1` in
`docs/release-checklist.md`, look more like benchmark-precision failures.

### Granular Decomposition

Gemini often split a multi-line concern into two or more findings where the
expected JSON wanted one.

Examples:

- `security/access_review.py`
- `docs/partner-integration.md`
- `scripts/bootstrap_env.py`
- `docs/release-checklist.md`

This pattern appears moderately common. It does not mean the additional
findings are irrelevant; it means the benchmark and the model disagree about
the right unit of review.

### Genuine False Positives

Some unmatched findings do look genuinely misaligned with the benchmark's
intent.

Examples:

- `ci/build_summary.html` flagged a clearly fictional `Project Comet` preview
  label.
- `docs/credential-rotation-guide.md` flagged general statements about
  excluding internal runbook detail, even though the document is explicitly a
  safe-handling guide for fictional placeholders.
- `frontend/account_settings.ts` labeled the `internal-only workaround` line as
  `SECURITY_RISK`, which is harder to defend than a reputation or compliance
  framing.

## False Negative Analysis

Gemini produced only 9 false negatives, and they were not all the same kind of
miss.

### Category Substitutions

Several false negatives appear to be the result of Gemini identifying the right
text but assigning a different category.

Examples:

- `api/schema-docs.html`: the expected `INTELLECTUAL_PROPERTY_RISK` finding on
  `vendor schema commentary` was reported as `REPUTATION_RISK`.
- `backend/billing_rules.py`: the expected `REPUTATION_RISK` finding on
  `billing process sound negotiable` was reported as `PROFESSIONALISM_RISK`.
- `frontend/support_banner.html`: the expected `REPUTATION_RISK` finding on
  `sounds defensive and could make the portal look unreliable` was reported as
  `PROFESSIONALISM_RISK`.
- `scripts/deploy_preview.js`: the expected `COMPLIANCE_RISK` finding on
  `release tag can be skipped` was reported as `PROFESSIONALISM_RISK`.
- `backend/customer_export.py`: the expected `COMPLIANCE_RISK` finding on
  internal approval notes was reported as `REPUTATION_RISK`.

### Merged Or Broadened Findings

Some false negatives were partially absorbed into a broader Gemini finding.

Examples:

- `auth/oauth_callback.ts`: Gemini captured the whole multi-issue block as one
  strong `SECURITY_RISK` plus an additional codename finding, but it did not
  separately surface the expected reputational concern or second security
  concern as distinct matched findings.
- `docs/incident-retrospective.md`: Gemini matched the compliance issue and
  produced a broader reputational finding later in the file, but it did not
  align closely enough with the expected `team was careless during launch prep`
  target text.

### Genuine Misses

A smaller set of false negatives look more like real misses than category or
granularity effects.

Examples:

- `frontend/account_settings.ts`: the `internal-only workaround` concern was
  not recognized in the expected reputational framing.
- `auth/oauth_callback.ts`: the explicit `logs the raw callback state`
  expectation was not separated into its own matched security finding.

Overall, the false-negative set suggests that Gemini usually engaged with the
right areas of the file, but sometimes generalized too broadly or chose a
neighboring category.

## Category Analysis

Expected category distribution was balanced:

- `COMPLIANCE_RISK`: 11
- `REPUTATION_RISK`: 10
- `SECURITY_RISK`: 10
- `INTERNAL_CODENAME_EXPOSURE`: 8
- `PROFESSIONALISM_RISK`: 6
- `INTELLECTUAL_PROPERTY_RISK`: 4

Gemini matched findings in every category:

- `COMPLIANCE_RISK`: 9 matched
- `SECURITY_RISK`: 9 matched
- `INTERNAL_CODENAME_EXPOSURE`: 8 matched
- `PROFESSIONALISM_RISK`: 6 matched
- `REPUTATION_RISK`: 5 matched
- `INTELLECTUAL_PROPERTY_RISK`: 3 matched

This is the clearest sign of Gemini's broader semantic coverage. Unlike a
narrow detector, it was not confined to one or two categories.

The main category weakness was not absence but instability. Gemini often found
the right text but mapped it to a nearby category:

- `REPUTATION_RISK` <-> `PROFESSIONALISM_RISK`
- `COMPLIANCE_RISK` <-> `REPUTATION_RISK`
- `COMPLIANCE_RISK` <-> `PROFESSIONALISM_RISK`
- `INTELLECTUAL_PROPERTY_RISK` <-> `REPUTATION_RISK`

The strongest category overproduction was `INTERNAL_CODENAME_EXPOSURE`, which
greatly exceeded the benchmark's expected count.

## Systematic Model Behaviors

Several recurring Gemini behaviors are strongly supported by the completed
report.

- Broad contextual reasoning: Gemini did not restrict itself to the benchmark's
  intended line. It frequently inferred additional risk from file headers,
  surrounding docstrings, and repository context.
- Strong codename sensitivity: internal project naming triggered many more
  findings than the benchmark expected, especially when combined with partner,
  external, preview, or release language.
- Granular decomposition: Gemini often split one benchmark concept into two
  findings, especially when a concern crossed lines or contained both a warning
  and an explanation.
- Category drift across adjacent concepts: tone, trust, process, and disclosure
  concerns often moved between `REPUTATION_RISK`, `PROFESSIONALISM_RISK`, and
  `COMPLIANCE_RISK`.
- Preference for surfacing additional concerns: Gemini behaved like a reviewer
  trying to be helpful rather than a scorer trying to stay inside an expected
  count range.

## Benchmark Review

The Gemini run highlights an important property of this benchmark: some strict
false positives are also reasonable human-review observations.

Reasonable additional observations include:

- file-level codename exposure in externally adjacent docstrings
- line-by-line decomposition of a multi-line compliance or IP concern
- broader tone findings where the text is clearly discussing trust, sloppiness,
  defensiveness, or internal-only behavior

This does not mean those outputs should count as benchmark matches under the
current rules. It does mean the benchmark is measuring two things at once:

- whether Gemini finds the benchmark's intended issue
- whether Gemini restrains itself from reporting adjacent issues that a human
  might still consider legitimate

The benchmark therefore appears well designed for exposing model behavior, but
some scored false positives should be interpreted as benchmark strictness
rather than straightforward review failure.

A few benchmark observations stand out:

- zero-finding cases remain valuable because they expose over-reporting clearly
- category boundaries are sometimes close enough that Gemini can land on a
  defensible neighboring label
- some expected JSON entries assume one ideal decomposition, while Gemini
  prefers multiple narrower findings

## Engineering Observations

The Gemini-backed system behaved like a semantic reviewer with wider context
use, stronger inference, and less restraint around benchmark boundaries. It
was willing to infer risk from surrounding meaning, external-sharing context,
and organizational language even when the expected JSON did not call for an
additional finding.

From an engineering perspective, the key difference from a deterministic-style
path is not just breadth of coverage. It is the shift in review philosophy.
Gemini acted as though its job was to identify potentially meaningful concerns,
not merely to reproduce a fixed benchmark interpretation.

That broader reasoning is visible in several ways:

- it covered all supported categories
- it surfaced nuanced compliance and IP findings that the deterministic path
  struggled to detect
- it also produced many extra codename and tone findings that a stricter
  benchmark treats as over-reporting

The result is a system that appears closer to human-style review behavior, but
also harder to align cleanly with exact-count benchmark expectations.

## Recommendations

### Prompt Improvements

- Review whether Gemini should be instructed more explicitly about when to
  suppress additional codename findings in file headers or obviously internal
  project labels.
- Review whether the prompt should prefer one consolidated finding versus
  multiple line-level findings when several sentences describe the same risk.
- Review whether the prompt should distinguish more sharply between
  professionalism, reputation, and compliance when the wording overlaps.

### Benchmark Improvements

- Keep repository-style realism and zero-finding false-positive scenarios.
- Consider explicitly noting that some cases are sensitive to granularity and
  may produce reasonable additional observations.
- Consider whether future analysis should separately track "reasonable extra
  findings" instead of treating every unmatched Gemini finding as equally
  misleading.

### Expected JSON Improvements

- Review cases where Gemini found the intended text but used a neighboring
  category with a plausible rationale.
- Review cases where one expected finding spans two lines but Gemini naturally
  split the issue into two findings.
- Review whether some file-level codename exposures are intentionally out of
  scope or whether the benchmark currently understates them.

### No Change Recommended

- Keep the current benchmark philosophy of allowing realistic false positives
  and false negatives to remain visible.
- Keep mixed file types, coherent repository context, and multi-category files.
- Keep strict TP/FP/FN reporting so broader Gemini behavior remains measurable.

## Final Conclusion

The Gemini repository benchmark taught that the current Gemini-backed Semantic
Review Agent can identify most of the benchmark's intended repository risks,
including compliance, reputation, professionalism, intellectual-property, and
codename issues. It also taught that Gemini is not naturally conservative under
this benchmark. It broadens the review surface, adds extra codename and
contextual findings, and sometimes chooses a neighboring category or a more
granular decomposition than the expected JSON. In other words, the Gemini path
behaves like a broad semantic reviewer whose usefulness is not fully captured
by strict benchmark exactness alone.
