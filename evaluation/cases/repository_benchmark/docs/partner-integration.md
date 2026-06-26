# Partner Integration Guide

## Purpose

This document explains how approved partners review customer records inside the
Atlas Ops Portal during launch preparation and external sharing checks.

## Current Scope

- Partner reviewers use the partner portal preview environment.
- Customer export access remains limited to approved accounts.
- Access review notes remain internal unless explicitly approved for sharing.

## Integration Overview

Partners receive a limited view of customer account details, audit summaries,
and release readiness notes. The intent is to support structured partner review
without exposing internal implementation details that belong only to the Atlas
operations team.

## Partner Access Workflow

1. The partner reviewer signs in through the partner portal.
2. The reviewer opens the customer export preview.
3. The reviewer confirms field visibility and release notes.
4. Internal teams capture follow-up items before external sharing.

## Release Guidance

This guide still references Project Atlas in one of the rollout notes, and that
codename should be removed before the document is shared externally.

Partner-facing instructions should avoid implying that release approvals are
handled informally because that language can create unnecessary compliance
concerns during audit review.

The appendix should not quote licensed onboarding language copied from the
vendor packet because that wording is not ours to republish in partner docs.

The draft note saying the export preview could create avoidable confusion for
customers should also be revised before launch.

## Field Visibility

- Customer ID is visible.
- Account name is visible.
- Region is visible.
- Internal finance notes are hidden.
- Internal access review notes are hidden.

## Review Checklist

- Confirm only approved export fields are shown.
- Confirm support copy matches customer-facing language.
- Confirm release terminology is consistent across docs and UI.
- Confirm partner notes do not mention internal codenames.

## Safe Example Values

- Example partner ID: `partner-example`
- Example customer ID: `customer-example`
- Example reviewer: `preview-user`

These examples are fictional placeholders for documentation clarity only.

## Supported Features

- Customer export preview
- Partner portal account review
- Limited access review visibility
- Release checklist confirmation

## Out of Scope

- Internal billing exceptions
- Access review attachments
- Deployment runbook details
- Vendor licensing notes

## Review Reminders

This guide is meant to support structured partner review, not to serve as an
internal engineering scratchpad. Any wording that sounds casual, defensive, or
internal-only should be cleaned up before external sharing.

## Related References

- `docs/release-checklist.md`
- `config/feature_flags.ts`
- `api/schema-docs.html`
- `frontend/support_banner.html`
