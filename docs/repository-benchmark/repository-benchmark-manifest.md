# Repository Benchmark Manifest

This document defines the planned composition of the repository benchmark
before implementation begins.

The goal is to ensure balanced coverage, realistic repository structure, and
consistent evaluation across all supported finding categories.

## Repository Theme

All benchmark files should belong to the same fictional software project.

The repository should feel coherent rather than like a collection of unrelated
examples. Files should reference the same product, features, documentation,
deployment process, and terminology where appropriate. Internal codenames,
documentation references, release notes, deployment scripts, APIs, and
implementation details may reference one another naturally.

Cross-file consistency should improve realism while still allowing each file to
remain understandable on its own. Shared terminology, recurring internal
feature names, shared documentation references, release note references,
deployment references, and architecture references are encouraged when they
help the repository feel more believable. These connections should improve
realism without requiring the files to be read in a specific order.

### Fictional Product

The planned benchmark repository should represent a fictional business-oriented
customer operations platform with a web portal, internal administration
features, supporting APIs, deployment workflows, and project documentation.

This product definition is intentionally lightweight. Its purpose is only to
provide a consistent context for the benchmark files, not to introduce a large
backstory or domain-specific complexity.

The benchmark should resemble a believable repository that could realistically
exist inside a software organization.

## Planned Repository

The benchmark should resemble a believable software repository rather than a
set of isolated test cases.

The planned benchmark contains 20 files.

| # | Planned File | File Type | Repository Area | Approx. Lines | Expected Findings | Primary Categories | Difficulty | False Positive Scenario |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | `auth/session_manager.py` | Python | Authentication | 160 | 3 | `SEC`, `CMP` | Medium | None |
| 2 | `auth/oauth_callback.ts` | TypeScript | Authentication | 140 | 3 | `SEC`, `REP` | Hard | Comment describing a previously removed issue |
| 3 | `api/public_status.js` | JavaScript | API | 110 | 0 | `(none)` | Easy | Historical incident example that should not be flagged |
| 4 | `backend/billing_rules.py` | Python | Backend | 170 | 3 | `CMP`, `REP` | Hard | None |
| 5 | `backend/customer_export.py` | Python | Backend | 150 | 3 | `SEC`, `IPR` | Medium | Placeholder values explained as examples |
| 6 | `frontend/account_settings.ts` | TypeScript | Frontend | 130 | 3 | `PRO`, `REP` | Medium | None |
| 7 | `frontend/support_banner.html` | HTML | Frontend | 115 | 2 | `PRO`, `REP` | Easy | None |
| 8 | `frontend/admin_debug.js` | JavaScript | Frontend | 125 | 3 | `SEC`, `CDX` | Hard | Fictional sample name inside an example block |
| 9 | `docs/partner-integration.md` | Markdown | Documentation | 180 | 4 | `CDX`, `CMP`, `REP` | Mixed | None |
| 10 | `docs/credential-rotation-guide.md` | Markdown | Security | 150 | 0 | `(none)` | Medium | Educational examples and placeholder credentials |
| 11 | `docs/release-checklist.md` | Markdown | Project Management | 120 | 2 | `PRO`, `CMP` | Easy | Commented notes about already removed issues |
| 12 | `docs/incident-retrospective.md` | Markdown | Internal Notes | 190 | 2 | `REP`, `CMP` | Hard | Historical documentation that should remain clean |
| 13 | `scripts/bootstrap_env.py` | Python | Scripts | 145 | 3 | `SEC`, `PRO` | Medium | Placeholder setup values documented safely |
| 14 | `scripts/deploy_preview.js` | JavaScript | Deployment | 135 | 3 | `SEC`, `CDX` | Hard | None |
| 15 | `ci/pipeline-notes.md` | Markdown | CI/CD | 105 | 2 | `CMP`, `PRO` | Medium | Comments explaining previously fixed failures |
| 16 | `ci/build_summary.html` | HTML | CI/CD | 110 | 0 | `(none)` | Medium | Fictional names in UI preview text |
| 17 | `config/feature_flags.ts` | TypeScript | Configuration | 125 | 3 | `CDX`, `CMP` | Medium | None |
| 18 | `security/access_review.py` | Python | Security | 175 | 4 | `SEC`, `CMP`, `IPR`, `REP` | Mixed | None |
| 19 | `api/schema-docs.html` | HTML | API | 130 | 2 | `IPR`, `REP` | Medium | Educational example content that resembles a finding |
| 20 | `project/roadmap-notes.md` | Markdown | Project Management | 165 | 4 | `CDX`, `PRO`, `REP` | Mixed | Historical codename references described as archived notes |

## Repository Areas

The planned files are distributed across a believable software project rather
than grouped by file type alone.

Planned repository areas include:

- Authentication
- Backend
- Frontend
- Configuration
- Deployment
- Documentation
- Scripts
- Internal Notes
- CI/CD
- Security
- API
- Project Management

This distribution is intended to make the benchmark feel like a real working
repository with multiple surfaces where semantic-review findings may appear.

## File Types

The planned file-type mix is intentionally balanced and close to the design
target:

- 5 Python
- 4 TypeScript
- 3 JavaScript
- 5 Markdown
- 3 HTML

This mix reflects the currently supported extraction surface while keeping the
repository varied and believable.

## Expected Findings

Each planned file contains between 0 and 4 expected findings.

The overall benchmark target in this manifest is 49 expected findings, which
fits the repository-design target range of approximately 45 to 60 findings.

Not every file is expected to contain findings. Several files are intentionally
planned as zero-finding cases so the benchmark can measure precision as well as
recall.

### High-Density Review Case

One planned file should intentionally contain the highest concentration of
findings in the benchmark.

This file should include multiple finding categories and should represent a
realistic worst-case repository review rather than an artificial stress test.
It should remain believable as a file that could exist in the fictional
repository.

The purpose of this case is to evaluate how the agent performs when several
independent findings occur within the same artifact without changing the
overall benchmark balance or planned finding totals.

## Category Balance

All supported categories appear multiple times across the planned repository:

- `CDX`
- `SEC`
- `PRO`
- `CMP`
- `IPR`
- `REP`

No single category is intended to dominate the benchmark. Some planned files
include multiple categories so the benchmark can reflect the way real
repository files often mix security, disclosure, professionalism, and policy
concerns.

## Difficulty Balance

The planned benchmark includes a mix of:

- Easy
- Medium
- Hard
- Mixed

Easy files should verify obvious findings. Medium files should require some
context. Hard files should require stronger semantic interpretation. Mixed
files should combine more than one difficulty level inside a single realistic
repository artifact.

## False Positive Planning

Several planned files intentionally include wording that resembles risky
content but should not produce findings.

Planned false-positive scenario types include:

- historical documentation
- educational examples
- placeholder values
- fictional names
- comments explaining removed issues

These scenarios are called out in the manifest table so precision can be
planned deliberately rather than treated as an afterthought.

## Design Notes

- This manifest exists to guide implementation.
- Individual benchmark files may evolve during creation.
- The overall balance defined here should remain stable.
- The evaluation philosophy in `docs/repository-benchmark/repository-benchmark-design.md` takes
  precedence over individual file details in this manifest.
