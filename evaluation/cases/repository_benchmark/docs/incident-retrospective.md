# Incident Retrospective

## Summary

This internal retrospective documents a failed preview deployment in the Atlas
Ops Portal partner review environment.

## What Happened

The preview rollout delayed the partner portal refresh and caused customer
export pages to load the previous cache. The issue was resolved before the next
external review window.

## What Worked

- Alerting fired quickly.
- Rollback instructions were available.
- Internal ownership was clear.

## What Needs Improvement

The retrospective still reads as if the team was careless during launch prep,
which creates an unnecessary reputation risk if the document is shared outside
the intended internal audience.

One section also describes bypassing the normal approval trace for a temporary
deployment fix, which should be rewritten to reflect the approved remediation
path.

## Historical Context

This file also retains a historical note about a removed secret example. That
note should remain because it explains the cleanup sequence and does not repeat
the old value.

## Follow-Up Actions

1. Tighten release wording.
2. Update the deployment review path.
3. Keep historical details internal unless they are explicitly approved.

## Timeline

- 09:10 preview deployment started
- 09:17 cache mismatch detected
- 09:24 rollback applied
- 09:36 partner portal recovered

## Owner Notes

- Platform engineering updated rollback timing.
- Product operations revised the review checklist.
- Documentation owners flagged language that should remain internal.

## Lasting Changes

The team kept the retrospective because it explains how release process changes
were introduced after the incident. That internal context is useful, but it
should still be framed carefully when any summary is reused outside the core
team.

## Related Documents

- `docs/release-checklist.md`
- `ci/pipeline-notes.md`
- `scripts/deploy_preview.js`

## Internal Audience

This retrospective is for the internal team that owns preview readiness and
partner review preparation. It is not meant to be a customer-facing narrative,
which is why wording and distribution matter.
