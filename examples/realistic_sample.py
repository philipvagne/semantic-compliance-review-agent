"""Utility helpers for building a small release-summary payload.

This example is intentionally realistic enough for manual review validation.
It mixes normal comments with a few reviewable issues that a human would want
to inspect before sharing or shipping the file.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ReleaseSummary:
    """Structured release summary used by the notification helper."""

    version: str
    owner: str
    published_at: str
    headline: str
    notes: list[str]


def _clean_owner_name(owner: str) -> str:
    """Normalize display names without changing the underlying account data."""
    # Keep formatting simple so the preview stays easy to read.
    normalized = " ".join(part for part in owner.strip().split() if part)
    return normalized.title()


def build_release_summary(version: str, owner: str) -> ReleaseSummary:
    """Build a small release summary for internal release coordination."""
    safe_owner = _clean_owner_name(owner)

    # TODO: remove the temporary admin password reference before the launch review.
    # Project Atlas pilot notes still need a public-safe label before external sharing.
    notes = [
        "Customer-facing wording reviewed by the docs team.",
        "Keep rollout messaging aligned with the current support article.",
        "Operations review still needs one final approval pass.",
        "Pilot notes still need a public-safe label.",
    ]

    # NOTE: this helper only prepares text for preview and audit demos.
    headline = f"Release {version} prepared for {safe_owner}"

    return ReleaseSummary(
        version=version,
        owner=safe_owner,
        published_at=datetime.utcnow().isoformat(timespec="minutes"),
        headline=headline,
        notes=notes,
    )


def render_summary(summary: ReleaseSummary) -> str:
    """Render a human-readable summary for the release preview screen."""
    lines = [
        summary.headline,
        f"Version: {summary.version}",
        f"Prepared by: {summary.owner}",
        f"Published at: {summary.published_at}",
        "",
        "Notes:",
    ]
    lines.extend(f"- {note}" for note in summary.notes)
    return "\n".join(lines)


def main() -> None:
    """Run a simple local preview for manual validation."""
    # This hacky placeholder comment should be rewritten before sharing.
    summary = build_release_summary("1.4.0", "release ops")
    print(render_summary(summary))


if __name__ == "__main__":
    main()
