"""Load validated project review context from YAML configuration files.

Purpose:
- Convert approved config files into a structured ReviewContext object.

Input:
- `config/sensitive_terms.yaml`
- `config/project_context.yaml`

Output:
- One ReviewContext object with defaults or warnings when allowed.

Responsibilities:
- Load YAML safely.
- Validate expected config structure and field types.
- Return structured context values plus config warnings.

Non-responsibilities:
- Classify findings.
- Call ADK.
- Modify config files.
- Generate reports.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from src.schemas import ReviewContext


class ContextLoadError(Exception):
    """Raised when review context config cannot be parsed or validated."""


def load_review_context(
    sensitive_terms_path: str = "config/sensitive_terms.yaml",
    project_context_path: str = "config/project_context.yaml",
) -> ReviewContext:
    warnings: list[str] = []

    sensitive_terms_data = _load_yaml_file(
        path=Path(sensitive_terms_path),
        config_type="sensitive terms",
        warnings=warnings,
    )
    project_context_data = _load_yaml_file(
        path=Path(project_context_path),
        config_type="project context",
        warnings=warnings,
    )

    return ReviewContext(
        sensitive_terms=_validate_sensitive_terms(sensitive_terms_data, sensitive_terms_path),
        project_name=_validate_optional_string(
            config_data=project_context_data,
            field_name="project_name",
            config_path=project_context_path,
            config_type="project context",
        ),
        project_description=_validate_optional_string(
            config_data=project_context_data,
            field_name="project_description",
            config_path=project_context_path,
            config_type="project context",
        ),
        review_focus=_validate_review_focus(project_context_data, project_context_path),
        config_warnings=warnings,
    )


def _load_yaml_file(path: Path, config_type: str, warnings: list[str]) -> object:
    normalized_path = str(path).replace("\\", "/")

    if not path.exists():
        warnings.append(_build_missing_or_empty_warning(normalized_path, config_type, state="missing"))
        return None

    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ContextLoadError(f"Unable to read {config_type} config at {normalized_path}: {exc}") from exc

    if not raw_text.strip():
        warnings.append(_build_missing_or_empty_warning(normalized_path, config_type, state="empty"))
        return None

    try:
        return yaml.safe_load(raw_text)
    except yaml.YAMLError as exc:
        raise ContextLoadError(_format_yaml_error(path=normalized_path, config_type=config_type, error=exc)) from exc


def _validate_sensitive_terms(config_data: object, config_path: str) -> list[str]:
    if config_data is None:
        return []

    if isinstance(config_data, list):
        return _validate_string_list(
            value=config_data,
            field_name="sensitive_terms",
            config_path=config_path,
            config_type="sensitive terms",
        )

    if isinstance(config_data, dict):
        if "sensitive_terms" not in config_data:
            raise ContextLoadError(
                f"Invalid sensitive terms config at {config_path}: expected a top-level "
                "'sensitive_terms' list[str] or a plain YAML list of strings."
            )
        return _validate_string_list(
            value=config_data["sensitive_terms"],
            field_name="sensitive_terms",
            config_path=config_path,
            config_type="sensitive terms",
        )

    raise ContextLoadError(
        f"Invalid sensitive terms config at {config_path}: expected a top-level "
        "'sensitive_terms' list[str] or a plain YAML list of strings."
    )


def _validate_optional_string(
    config_data: object,
    field_name: str,
    config_path: str,
    config_type: str,
) -> str | None:
    if config_data is None:
        return None

    if not isinstance(config_data, dict):
        raise ContextLoadError(
            f"Invalid {config_type} config at {config_path}: expected a mapping with optional "
            "'project_name', 'project_description', and 'review_focus' fields."
        )

    value = config_data.get(field_name)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ContextLoadError(
            f"Invalid {config_type} config at {config_path}: '{field_name}' must be a string if present."
        )
    return value


def _validate_review_focus(config_data: object, config_path: str) -> list[str]:
    if config_data is None:
        return []

    if not isinstance(config_data, dict):
        raise ContextLoadError(
            f"Invalid project context config at {config_path}: expected a mapping with optional "
            "'project_name', 'project_description', and 'review_focus' fields."
        )

    value = config_data.get("review_focus")
    if value is None:
        return []
    return _validate_string_list(
        value=value,
        field_name="review_focus",
        config_path=config_path,
        config_type="project context",
    )


def _validate_string_list(
    value: object,
    field_name: str,
    config_path: str,
    config_type: str,
) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ContextLoadError(
            f"Invalid {config_type} config at {config_path}: '{field_name}' must be a list of strings."
        )
    return value


def _format_yaml_error(path: str, config_type: str, error: yaml.YAMLError) -> str:
    message = f"Invalid YAML in {config_type} config at {path}: {error}"
    mark = getattr(error, "problem_mark", None)
    if mark is not None:
        message = f"{message} (line {mark.line + 1}, column {mark.column + 1})"
    return message


def _build_missing_or_empty_warning(path: str, config_type: str, *, state: str) -> str:
    if config_type == "sensitive terms":
        return f"{path} {state}; using empty sensitive term list."
    return f"{path} {state}; using default project context values."
