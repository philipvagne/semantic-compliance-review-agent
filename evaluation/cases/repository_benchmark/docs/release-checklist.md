# Release Checklist

## Goal

This checklist is used before partner review, launch preparation, and external
sharing of the Atlas Ops Portal repository materials.

## Product Areas

- Partner portal
- Customer export
- Access review
- Deployment preview

## Required Checks

1. Confirm no internal codenames remain in partner-facing docs.
2. Confirm customer-facing copy uses neutral and professional wording.
3. Confirm compliance notes are aligned with approved process language.
4. Confirm deployment references match the current preview environment.

## Open Items

The launch checklist still says the support copy sounds sloppy, which should be
rewritten before the release packet is shared.

The approval note also implies that a manual exception can be used without the
normal review path, which should be corrected before audit sign-off.

## Historical Notes

Comments about already removed issues can stay in archived change logs, but
they should not be copied into the active release packet.

## Safe Example Labels

- Release label: `partner-review-preview`
- Reviewer label: `example-reviewer`
- Change ticket: `ATLAS-EXAMPLE-1`

## Sign-Off Owners

- Product operations
- Security review
- Documentation review
- Release coordination

## Final Verification

1. Confirm customer-facing wording is neutral.
2. Confirm partner docs no longer mention internal-only names.
3. Confirm deployment notes reference the current preview flow.
4. Confirm audit language reflects the approved process.

## Related Files

- `docs/partner-integration.md`
- `ci/pipeline-notes.md`
- `scripts/deploy_preview.js`
- `frontend/support_banner.html`

## Release Context

This checklist is written for a narrow release window: partner review,
launch-preparation validation, and controlled external sharing. It should read
like a normal project checklist rather than a benchmark artifact.
