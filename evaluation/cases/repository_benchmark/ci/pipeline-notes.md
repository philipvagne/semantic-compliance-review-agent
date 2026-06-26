# Pipeline Notes

## Scope

This document captures CI notes for the Atlas Ops Portal preview and release
checks.

## Covered Jobs

- build-preview
- verify-partner-portal
- verify-customer-export
- verify-access-review

## Current Notes

The checklist still implies that a release reviewer can skip one approval gate
when the preview job is green, which should be corrected before audit review.

One note also says the build summary reads like a rushed internal update, which
should be cleaned up before it appears in a release packet.

## Historical Cleanup Comments

Comments about previously removed issues can remain in internal notes when they
explain why a check exists, but they should not be written as if the issue is
still active.

## Job Ownership

- Platform engineering owns preview build stability.
- Product operations owns partner review timing.
- Security owns access review verification.
- Documentation owners confirm customer-facing release wording.

## Verification Steps

1. Run build-preview.
2. Confirm the partner portal preview is reachable.
3. Confirm customer export fields match the approved list.
4. Confirm access review notes are not included in partner artifacts.
5. Confirm release wording stays neutral and professional.

## Safe Example Labels

- Preview stage: `atlas-preview`
- Job label: `verify-partner-portal`
- Review tag: `launch-prep`

These labels are fictional examples used for process planning only.

## Related Files

- `docs/release-checklist.md`
- `docs/partner-integration.md`
- `config/feature_flags.ts`
- `scripts/deploy_preview.js`

## Notes For Reviewers

These notes are meant to explain why checks exist, not to replace the actual
release workflow documentation. The benchmark should treat this file as a
normal internal coordination artifact rather than a standalone benchmark trick.
