"""Access review notes for Atlas launch preparation and partner handoff."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC
from datetime import datetime


@dataclass(slots=True)
class AccessReviewItem:
    owner: str
    system_name: str
    review_status: str
    notes: str


REVIEW_ITEMS = [
    AccessReviewItem(
        owner="security-team",
        system_name="partner-portal",
        review_status="pending",
        notes="External reviewer scope still under review.",
    ),
    AccessReviewItem(
        owner="ops-team",
        system_name="customer-export",
        review_status="approved",
        notes="Field list approved for partner preview.",
    ),
]


def review_snapshot() -> dict[str, object]:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "items": [item.__dict__ for item in REVIEW_ITEMS],
    }


def system_names() -> list[str]:
    return [item.system_name for item in REVIEW_ITEMS]


def owners() -> list[str]:
    return [item.owner for item in REVIEW_ITEMS]


def status_by_system(system_name: str) -> str:
    for item in REVIEW_ITEMS:
        if item.system_name == system_name:
            return item.review_status
    return "unknown"


# TODO: remove the temporary credential note from the access review appendix.
# Compliance note: one reviewer checklist still says approval can proceed
# before the audit attachment is complete.
# The vendor packet excerpt in the appendix should not be copied into our
# repository notes because the licensed wording is not ours to reuse.
# The line saying the partner portal could look careless during review should be
# revised before launch prep is shared outside the core team.


def build_review_table() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in REVIEW_ITEMS:
        rows.append(
            {
                "owner": item.owner,
                "system_name": item.system_name,
                "review_status": item.review_status,
                "notes": item.notes,
            }
        )
    return rows


def review_headers() -> dict[str, str]:
    return {
        "X-Atlas-Review": "access-review",
        "X-Release-Context": "launch-preparation",
    }


def approved_systems() -> list[str]:
    return [item.system_name for item in REVIEW_ITEMS if item.review_status == "approved"]


def pending_systems() -> list[str]:
    return [item.system_name for item in REVIEW_ITEMS if item.review_status != "approved"]


def audit_line() -> str:
    return "|".join(system_names())


def review_owner_lines() -> list[str]:
    return [f"{item.owner}:{item.system_name}" for item in REVIEW_ITEMS]


def open_review_count() -> int:
    return len(pending_systems())
