# Repository Benchmark Review

## Executive Summary

The completed deterministic repository benchmark produced `0.55` precision and
`0.22` recall across 20 repository-style files. In practical terms, the run
found some real issues, but coverage was narrow and uneven. The benchmark did
successfully expose both strengths and weaknesses: the current system was
reliable on explicit secret-style TODOs and several direct internal codename
mentions, but it struggled to detect most compliance, reputation,
professionalism, and intellectual-property findings in realistic repository
context.

The result is informative rather than merely low. It shows that the benchmark
is doing what it was designed to do: surface the gap between a small synthetic
evaluation and a more realistic repository review setting.

## Benchmark Performance

The benchmark contained 49 expected findings. The completed run produced 11
true positives, 9 false positives, and 38 false negatives.

These numbers suggest two different behaviors at once:

- Precision remained moderate because when the system did report findings, some
  of them were legitimate matches.
- Recall was much weaker because large portions of the intended risk surface
  were not detected at all.

The most important detail is not just the ratio. The findings were heavily
concentrated in two categories. The run matched 7 `SECURITY_RISK` findings and
4 `INTERNAL_CODENAME_EXPOSURE` findings. It matched none of the expected
`COMPLIANCE_RISK`, `INTELLECTUAL_PROPERTY_RISK`, `PROFESSIONALISM_RISK`, or
`REPUTATION_RISK` findings. That makes the benchmark result less about random
misses and more about a systematic coverage boundary.

## False Positive Analysis

All 9 false positives were `SECURITY_RISK`. They cluster into two clear
patterns.

- Placeholder and training-material over-reporting: 7 false positives came
  from `docs/credential-rotation-guide.md`. The system flagged the title, the
  general discussion of credential rotation, clearly labeled example values,
  and historical notes about fictional examples. This is the dominant false
  positive pattern in the benchmark.
- Historical cleanup context over-reporting: 2 additional false positives came
  from files that intentionally described removed or fictional examples for
  explanatory purposes: `api/public_status.js` and `docs/incident-retrospective.md`.

This behavior looks less like random noise and more like a conservative
disclosure interpretation. The current system appears willing to flag security
adjacent wording even when the surrounding text explicitly says the examples
are fictional, historical, or retained to document cleanup.

There is also some evidence of split reporting inside the credential guide. One
conceptual document was turned into 7 separate security findings rather than a
single contextual judgment. That does not affect the expected count because the
case is intentionally zero-finding, but it does show a tendency to escalate
repeated credential vocabulary line by line.

## False Negative Analysis

The false negatives show a different pattern from the false positives. Most are
not isolated misses. They are concentrated in recurring semantic themes.

- Non-security policy language: compliance-style wording such as `skip one
  approval gate`, `manual exception`, `approval can proceed`, and `handled
  informally` was repeatedly missed.
- Tone and perception language: reputation and professionalism concerns such as
  `looks broken and undermines trust`, `sounds sloppy`, `look unreliable`, and
  `could look careless during review` were usually not detected.
- Intellectual-property references: expected findings involving reused vendor
  wording or copied packet language were missed consistently.
- Merged multi-issue blocks: when a comment block mixed a secret-style note
  with additional concerns, the system often returned only one dominant finding
  and ignored the rest. This happened in files such as `auth/oauth_callback.ts`,
  `frontend/admin_debug.js`, `scripts/deploy_preview.js`, and
  `security/access_review.py`.

Six files with expected findings returned no findings at all:

- `api/schema-docs.html`
- `backend/billing_rules.py`
- `ci/pipeline-notes.md`
- `docs/release-checklist.md`
- `frontend/account_settings.ts`
- `frontend/support_banner.html`

That pattern matters. It suggests the weakness is not only in resolving mixed
blocks. Entire classes of realistic prose-based concerns were outside the
current detection behavior during this run.

## Category Analysis

Expected category distribution was reasonably balanced:

- `COMPLIANCE_RISK`: 11
- `REPUTATION_RISK`: 10
- `SECURITY_RISK`: 10
- `INTERNAL_CODENAME_EXPOSURE`: 8
- `PROFESSIONALISM_RISK`: 6
- `INTELLECTUAL_PROPERTY_RISK`: 4

Observed matched categories were much narrower:

- `SECURITY_RISK`: 7 matched
- `INTERNAL_CODENAME_EXPOSURE`: 4 matched
- all other categories: 0 matched

This makes the category story unusually clear. The current system showed
strength on direct security-style wording and configured codename references.
It showed little or no demonstrated coverage for compliance, reputation,
professionalism, or intellectual-property findings in this benchmark.

There is also some category substitution evidence. In
`docs/incident-retrospective.md`, the system returned a `SECURITY_RISK` finding
for a historical note about a removed secret example, while the expected
findings were `REPUTATION_RISK` and `COMPLIANCE_RISK`. That does not appear to
be a one-off category swap across the whole benchmark, but it does show that
security framing can dominate when mixed language is present.

## Systematic Model Behaviors

Several recurring behaviors are supported by the completed run.

- Conservative security bias: security-adjacent vocabulary often triggered
  findings even when the text explicitly framed the content as fictional,
  historical, or educational.
- Narrow semantic coverage: the system repeatedly recognized explicit
  secret-like reminders and configured codenames, but rarely extended beyond
  those patterns.
- Dominant-finding collapse: mixed comment blocks were often reduced to one
  primary security or codename finding rather than multiple independent issues.
- Sensitivity to configured internal terminology: `Project Atlas` references
  were detected more reliably than softer disclosure or tone problems.
- Weakness on reputational and policy nuance: wording about trust, defensiveness,
  sloppiness, approval shortcuts, and reused vendor language was largely missed.

These behaviors are consistent across multiple files rather than being driven
by a single outlier case.

## Benchmark Review

The benchmark appears to be fulfilling its intended purpose. It is more
realistic than the small synthetic benchmark, and the resulting score profile
contains useful engineering signal.

A few observations about the benchmark itself are worth noting.

- Some multi-issue comment blocks allow more than one reasonable response
  shape. In `oauth_callback.ts`, `admin_debug.js`, `deploy_preview.js`, and
  `access_review.py`, a single merged finding is understandable even though the
  expected JSON asks for separate findings.
- Some category boundaries are intentionally close together. Reputation,
  professionalism, and compliance can overlap when the same sentence sounds
  sloppy, weakens trust, and implies process shortcuts at the same time.
- The benchmark is intentionally strict about zero-finding cases involving
  placeholder credentials. That strictness is useful because it exposes whether
  the system can distinguish educational examples from unsafe disclosure.
- The benchmark likely measures real extraction-and-interpretation difficulty,
  not just matching difficulty. The missed cases are spread across Python,
  TypeScript, Markdown, and HTML.

Overall, the benchmark seems appropriately demanding. The main caution is that
some expected outputs describe the ideal granular decomposition of a comment
block, while the current system sometimes produces one broader finding that is
not obviously irrational, only less granular.

## Engineering Observations

The repository benchmark provided substantially different evidence from the
original small benchmark. The earlier benchmark showed that the evaluation
pipeline worked and that the system could handle some obvious cases. The
repository benchmark showed how quickly performance changes once the files
become coherent, mixed, and context-heavy.

That difference is valuable. It suggests the repository benchmark is much more
representative of the project's claimed use case than a small set of isolated
micro-cases.

The newer diagnostics and partial-report behavior also help the analysis phase.
Case-level summaries make it much easier to see whether a failure came from
over-reporting, under-reporting, or category mismatch. Incremental saved
artifacts make the benchmark easier to inspect as an engineering system rather
than only as a final score.

## Recommendations

### Prompt Improvements

- Review whether the prompt should distinguish live secret references from
  clearly labeled placeholders, training examples, and historical cleanup
  notes more explicitly.
- Review whether the prompt should encourage separating independent findings
  inside a mixed comment block when they represent different categories.
- Review whether the prompt should give stronger treatment to compliance,
  reputation, professionalism, and intellectual-property cues that do not use
  obvious security language.

### Benchmark Improvements

- Continue using repository-style files and zero-finding false-positive
  scenarios. They are producing meaningful evidence.
- Review whether a few mixed-block cases should also include alternate
  acceptable interpretations in a benchmark note, even if the expected JSON
  remains single-path.
- Consider whether future benchmark reviews should explicitly track
  "merged-but-reasonable" outputs as an analysis dimension separate from strict
  TP/FP/FN scoring.

### Expected JSON Improvements

- Review cases where multiple expected findings come from one tightly grouped
  block and a single broader finding may be a reasonable response shape.
- Review whether some reputation-versus-professionalism and
  compliance-versus-reputation distinctions are narrower than the current
  evaluation narrative intends.
- Review whether a small number of expected count ranges could permit slightly
  broader but still defensible decompositions without weakening the benchmark's
  purpose.

### No Change Recommended

- Keep the repository-style benchmark structure.
- Keep zero-finding placeholder and historical-context cases.
- Keep mixed file types and cross-file project coherence.
- Keep the current evaluation methodology and strict reporting of false
  positives and false negatives.

## Final Conclusion

This benchmark showed that the current Semantic Review Agent is strongest on
explicit secret-like reminders and configured internal codenames, but much
weaker on broader semantic review tasks such as compliance language,
reputational tone, professionalism, and intellectual-property concerns in
realistic repository prose. It also showed that realistic benchmark design
changes the evaluation story substantially: the system can still produce useful
findings, but its practical coverage is much narrower than the smaller
synthetic benchmark alone would suggest.
