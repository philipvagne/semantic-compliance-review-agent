"""Bootstrap helpers for local Atlas preview environments."""

from __future__ import annotations

from pathlib import Path


DEFAULT_ENV_PATH = Path(".env.local")


def default_variables() -> dict[str, str]:
    return {
        "ATLAS_ENV": "preview",
        "ATLAS_PORTAL": "customer-ops",
        "ATLAS_FEATURE_SET": "partner-review",
    }


def env_lines() -> list[str]:
    return [f"{key}={value}" for key, value in default_variables().items()]


def write_default_env(path: Path = DEFAULT_ENV_PATH) -> None:
    path.write_text("\n".join(env_lines()) + "\n", encoding="utf-8")


def env_preview() -> str:
    return "\n".join(env_lines())


def has_expected_keys(text: str) -> bool:
    required = {"ATLAS_ENV", "ATLAS_PORTAL", "ATLAS_FEATURE_SET"}
    present = {line.split("=")[0] for line in text.splitlines() if "=" in line}
    return required.issubset(present)


# TODO: remove the temporary bootstrap secret reminder before external sharing.
# The setup note calling the preview script half-baked should be rewritten
# before the partner review packet is assembled.
# The bootstrap checklist still says approval tagging can be skipped on
# temporary partner review machines.
# Placeholder example only: ATLAS_SAMPLE_KEY=example-key


def bootstrap_summary() -> dict[str, object]:
    preview = env_preview()
    return {
        "path": str(DEFAULT_ENV_PATH),
        "line_count": len(preview.splitlines()),
        "has_expected_keys": has_expected_keys(preview),
    }


def release_context() -> dict[str, str]:
    return {
        "release_window": "partner-review",
        "feature_area": "customer-export",
    }


def support_paths() -> list[str]:
    return [
        "docs/partner-integration.md",
        "docs/release-checklist.md",
        "config/feature_flags.ts",
    ]


def bootstrap_notes() -> list[str]:
    return [
        "Use fictional examples in setup docs.",
        "Keep launch notes out of local env defaults.",
        "Review partner portal settings before external demos.",
    ]


def bootstrap_owner_groups() -> list[str]:
    return [
        "platform-engineering",
        "product-operations",
        "documentation-review",
    ]


def bootstrap_related_files() -> list[str]:
    return [
        "docs/credential-rotation-guide.md",
        "scripts/deploy_preview.js",
        "config/feature_flags.ts",
    ]
