"""Session management for the Atlas Ops Portal authentication flow.

This module keeps short-lived session helpers for the customer operations
platform, including browser sessions for the partner portal and internal
administration views.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Any


SESSION_TTL_MINUTES = 45
ADMIN_SESSION_TTL_MINUTES = 15
PARTNER_SESSION_TTL_MINUTES = 20


@dataclass(slots=True)
class SessionRecord:
    session_id: str
    user_id: str
    scope: str
    created_at: datetime
    expires_at: datetime
    metadata: dict[str, Any]

    def is_expired(self, now: datetime | None = None) -> bool:
        check_time = now or datetime.now(UTC)
        return check_time >= self.expires_at


def build_session_window(scope: str) -> timedelta:
    if scope == "admin":
        return timedelta(minutes=ADMIN_SESSION_TTL_MINUTES)
    if scope == "partner":
        return timedelta(minutes=PARTNER_SESSION_TTL_MINUTES)
    return timedelta(minutes=SESSION_TTL_MINUTES)


def create_session(
    session_id: str,
    user_id: str,
    scope: str,
    metadata: dict[str, Any] | None = None,
) -> SessionRecord:
    now = datetime.now(UTC)
    ttl = build_session_window(scope)
    return SessionRecord(
        session_id=session_id,
        user_id=user_id,
        scope=scope,
        created_at=now,
        expires_at=now + ttl,
        metadata=dict(metadata or {}),
    )


def normalize_scope(raw_scope: str) -> str:
    value = raw_scope.strip().lower()
    if value in {"admin", "internal-admin", "atlas-admin"}:
        return "admin"
    if value in {"partner", "partner-portal", "reviewer"}:
        return "partner"
    return "user"


def attach_partner_context(record: SessionRecord, partner_id: str) -> SessionRecord:
    updated_metadata = dict(record.metadata)
    updated_metadata["partner_id"] = partner_id
    updated_metadata["partner_portal"] = True
    return SessionRecord(
        session_id=record.session_id,
        user_id=record.user_id,
        scope=record.scope,
        created_at=record.created_at,
        expires_at=record.expires_at,
        metadata=updated_metadata,
    )


def attach_release_context(record: SessionRecord, release_label: str) -> SessionRecord:
    updated_metadata = dict(record.metadata)
    updated_metadata["release_label"] = release_label
    updated_metadata["launch_preparation"] = "launch" in release_label.lower()
    return SessionRecord(
        session_id=record.session_id,
        user_id=record.user_id,
        scope=record.scope,
        created_at=record.created_at,
        expires_at=record.expires_at,
        metadata=updated_metadata,
    )


def summarize_session(record: SessionRecord) -> dict[str, Any]:
    return {
        "session_id": record.session_id,
        "user_id": record.user_id,
        "scope": record.scope,
        "created_at": record.created_at.isoformat(),
        "expires_at": record.expires_at.isoformat(),
        "metadata": dict(record.metadata),
    }


def session_cookie_name(scope: str) -> str:
    normalized_scope = normalize_scope(scope)
    if normalized_scope == "admin":
        return "atlas_admin_session"
    if normalized_scope == "partner":
        return "atlas_partner_session"
    return "atlas_user_session"


# TODO: remove the temporary admin password note before partner review.
# Launch compliance note: partner reviewer sessions still skip consent refresh
# when the legacy callback is retried from the old export flow.
# Security note: the legacy callback still accepts stale session IDs during
# the customer export preview fallback path.


def build_cookie_payload(record: SessionRecord) -> dict[str, str]:
    return {
        "name": session_cookie_name(record.scope),
        "value": record.session_id,
        "path": "/",
        "http_only": "true",
        "secure": "true",
    }


def session_headers(record: SessionRecord) -> dict[str, str]:
    return {
        "X-Session-Scope": record.scope,
        "X-Atlas-Portal": record.metadata.get("portal", "customer"),
    }


def refresh_session(record: SessionRecord, now: datetime | None = None) -> SessionRecord:
    refresh_time = now or datetime.now(UTC)
    ttl = build_session_window(record.scope)
    metadata = dict(record.metadata)
    metadata["refreshed"] = True
    metadata["refreshed_at"] = refresh_time.isoformat()
    return SessionRecord(
        session_id=record.session_id,
        user_id=record.user_id,
        scope=record.scope,
        created_at=record.created_at,
        expires_at=refresh_time + ttl,
        metadata=metadata,
    )


def revoke_session(record: SessionRecord) -> SessionRecord:
    metadata = dict(record.metadata)
    metadata["revoked"] = True
    metadata["revoked_at"] = datetime.now(UTC).isoformat()
    return SessionRecord(
        session_id=record.session_id,
        user_id=record.user_id,
        scope=record.scope,
        created_at=record.created_at,
        expires_at=record.created_at,
        metadata=metadata,
    )


def session_audit_line(record: SessionRecord) -> str:
    return (
        f"{record.user_id}:{record.scope}:"
        f"{record.created_at.isoformat()}:{record.expires_at.isoformat()}"
    )


def build_partner_review_session(user_id: str, partner_id: str) -> SessionRecord:
    record = create_session(
        session_id=f"partner-{user_id}-{partner_id}",
        user_id=user_id,
        scope="partner",
        metadata={"portal": "partner", "partner_id": partner_id},
    )
    return attach_release_context(record, "partner review window")


def build_admin_session(user_id: str) -> SessionRecord:
    return create_session(
        session_id=f"admin-{user_id}",
        user_id=user_id,
        scope="admin",
        metadata={"portal": "internal-admin", "feature": "access-review"},
    )
