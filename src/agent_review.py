"""Review extracted text with an ADK-backed agent boundary.

Purpose:
- Convert ReviewableText and ReviewContext inputs into structured Finding results.

Input:
- ReviewableText[]
- ReviewContext

Output:
- A list of Finding objects.

Responsibilities:
- Run the review behind a clean ADK-backed boundary.
- Apply the configured Gemini model selection when the Gemini backend is used.
- Validate structured findings.
- Retry once on malformed structured output.

Non-responsibilities:
- Read files.
- Extract text.
- Load config files.
- Write reports or modify source files.
"""

from __future__ import annotations

import asyncio
import contextlib
from functools import cached_property
import io
import json
import logging
import os
import re
import time
from typing import AsyncGenerator
from typing import Literal

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import InMemoryRunner
from google.genai import Client
from google.genai import types
from google.genai.errors import APIError
from google.genai.errors import ClientError
from google.genai.errors import ServerError
from pydantic import TypeAdapter
from pydantic import ValidationError

from src.schemas import Finding
from src.schemas import ReviewContext
from src.schemas import ReviewableText


logging.getLogger("google.adk").setLevel(logging.ERROR)

BackendName = Literal["gemini", "deterministic"]
DEFAULT_BACKEND: BackendName = "gemini"
GEMINI_MODEL_NAME = "gemini-2.5-flash"
GEMINI_MODEL_ENV_VAR = "GEMINI_MODEL"
_configured_backend: BackendName = DEFAULT_BACKEND
_configured_api_key: str | None = None
_configured_gemini_model_name: str = GEMINI_MODEL_NAME
GEMINI_TRANSIENT_MAX_ATTEMPTS = 3
GEMINI_TRANSIENT_RETRY_DELAYS_SECONDS = (1, 2)

AGENT_REVIEW_INSTRUCTION = """
Review all extracted text and return only structured Finding JSON that matches
the documented contract.

Rules:
- Keep severity and confidence separate.
- Return an empty JSON list when there are no findings.
- `detection_method` must follow the documented contract exactly.
- Use `TERM_MATCH` only when a configured sensitive term is detected and no
  additional semantic reasoning is needed to justify the finding.
- Use `SEMANTIC_ANALYSIS` when the finding comes from meaning, tone, or
  implication and there is no configured sensitive-term match in the source
  text.
- Use `HYBRID` only when both are true:
  1. a configured sensitive term is present in the source text
  2. surrounding language adds additional semantic risk
- Do not use `HYBRID` just because semantic reasoning was used.
- Do not use `HYBRID` just because the finding is high severity.
- Do not use `HYBRID` just because `suggested_replacement` exists.
- `suggested_replacement` is optional.
- Use `null` for `suggested_replacement` when remediation is uncertain.
- Include `suggested_replacement` when the finding is HIGH confidence and a safe,
  neutral replacement is obvious from the source text alone.
- Suggested replacements must preserve the intent of the original comment while
  removing risky, sensitive, or unprofessional wording.
- Suggested replacements must not include secrets, internal codenames,
  credentials, speculative information, or new claims not present in the source.
- TERM_MATCH findings are HIGH confidence by construction.
- HYBRID findings should be HIGH confidence only when both a sensitive term match
  and additional semantic risk are clearly present.

Examples:
- Source: "TODO: remove the temporary admin password before release"
  detection_method: `SEMANTIC_ANALYSIS`
  Reason: no configured sensitive term is present in the source text.
- Source: "TODO: remove the temporary admin password before release"
  Safe suggested_replacement:
  "TODO: remove the temporary admin credential reference before release"
- Source: "Project Titan"
  detection_method: `TERM_MATCH`
  Reason: a configured sensitive term is present without added semantic risk.
- Source: "TODO: remove the Project Titan workaround before launch"
  detection_method: `HYBRID`
  Reason: a configured sensitive term is present and surrounding language adds
  semantic risk.
- Source: "FIXME: replace the hard-coded example value later"
  detection_method: `SEMANTIC_ANALYSIS`
  Reason: no configured sensitive term is present in the source text.
- Source: "FIXME: replace the hard-coded example value later"
  Safe suggested_replacement:
  "FIXME: replace the placeholder value before release"
- If no clearly safe rewrite is obvious, use `null`.
""".strip()

FINDINGS_ADAPTER = TypeAdapter(list[Finding])
SECURITY_KEYWORDS = (
    "password",
    "secret",
    "token",
    "credential",
    "api key",
    "private key",
    "admin password",
)
SEMANTIC_RISK_KEYWORDS = (
    "workaround",
    "temporary",
    "temp",
    "before launch",
    "before release",
    "bypass",
    "hack",
)
PROFESSIONALISM_KEYWORDS = (
    "stupid",
    "idiot",
    "hacky",
    "ugly",
    "dumb",
)
COMPLIANCE_KEYWORDS = (
    "confidential",
    "gdpr",
    "hipaa",
    "sox",
    "pii",
)


class AgentReviewError(Exception):
    """Raised when the agent review component fails."""


class ConfiguredGeminiModel(Gemini):
    """Gemini model with explicit API-key configuration for this project."""

    @cached_property
    def api_client(self) -> Client:
        api_key = _configured_api_key
        if not api_key:
            raise AgentReviewError(
                "Gemini backend requires GOOGLE_API_KEY or GEMINI_API_KEY to be set."
            )
        return Client(api_key=api_key)


class DeterministicAgentReviewModel(BaseLlm):
    """Local ADK model fallback that provides deterministic structured findings."""

    model: str = "phase-5-deterministic-agent-review-model"

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        prompt_text = _extract_prompt_text(llm_request)
        payload = json.loads(prompt_text)
        findings = _generate_findings(payload)

        yield LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text=json.dumps(findings))],
            )
        )


def review(reviewable_texts: list[ReviewableText], review_context: ReviewContext) -> list[Finding]:
    try:
        return asyncio.run(_run_review(reviewable_texts, review_context, _configured_backend))
    except AgentReviewError:
        raise
    except Exception as exc:
        raise AgentReviewError(f"Unexpected agent review failure: {exc}") from exc


def configure_backend(
    backend: BackendName,
    gemini_model_name: str | None = None,
) -> None:
    global _configured_backend
    global _configured_api_key
    global _configured_gemini_model_name

    if backend not in ("gemini", "deterministic"):
        raise AgentReviewError(f"Unsupported agent review backend: {backend}")

    _configured_backend = backend
    _configured_api_key = None
    _configured_gemini_model_name = _resolve_gemini_model_name(gemini_model_name)

    if backend == "gemini":
        api_key = _resolve_gemini_api_key()
        if not api_key:
            raise AgentReviewError(
                "Gemini backend requires GOOGLE_API_KEY or GEMINI_API_KEY. "
                "Set one of these environment variables before running the CLI."
            )
        _configured_api_key = api_key


def get_backend_display_name() -> str:
    return "Gemini" if _configured_backend == "gemini" else "Deterministic"


def get_default_gemini_model_name() -> str:
    return _resolve_gemini_model_name(None)


def get_model_display_name() -> str | None:
    if _configured_backend == "gemini":
        return _configured_gemini_model_name
    return "deterministic-local"


def build_agent(backend: BackendName) -> Agent:
    return Agent(
        name="semantic_compliance_review_agent",
        description="Phase 5 ADK-backed semantic compliance review agent.",
        instruction=AGENT_REVIEW_INSTRUCTION,
        model=_build_model(backend),
        output_schema=list[Finding],
    )


async def _run_review(
    reviewable_texts: list[ReviewableText],
    review_context: ReviewContext,
    backend: BackendName,
) -> list[Finding]:
    prompt = json.dumps(
        {
            "reviewable_texts": [item.model_dump() for item in reviewable_texts],
            "review_context": review_context.model_dump(),
        }
    )

    attempt_count = (
        GEMINI_TRANSIENT_MAX_ATTEMPTS
        if backend == "gemini"
        else 1
    )
    last_error: Exception | None = None

    for attempt_number in range(1, attempt_count + 1):
        runner = InMemoryRunner(agent=build_agent(backend))
        try:
            return await _run_single_review_attempt(runner, prompt)
        except ValidationError as exc:
            last_error = exc
            break
        except AgentReviewError as exc:
            last_error = exc
            if (
                backend == "gemini"
                and attempt_number < attempt_count
                and _is_transient_gemini_error(exc)
            ):
                delay_seconds = GEMINI_TRANSIENT_RETRY_DELAYS_SECONDS[attempt_number - 1]
                print(f"Gemini transient error, retrying in {delay_seconds}s...")
                time.sleep(delay_seconds)
                continue
            raise
        except (ClientError, ServerError, APIError, TimeoutError) as exc:
            wrapped_error = AgentReviewError(
                f"{get_backend_display_name()} backend failed: {exc}"
            )
            last_error = wrapped_error
            if (
                backend == "gemini"
                and attempt_number < attempt_count
                and _is_transient_gemini_error(exc)
            ):
                delay_seconds = GEMINI_TRANSIENT_RETRY_DELAYS_SECONDS[attempt_number - 1]
                print(f"Gemini transient error, retrying in {delay_seconds}s...")
                time.sleep(delay_seconds)
                continue
            raise wrapped_error from exc
        except Exception as exc:
            wrapped_error = AgentReviewError(
                f"{get_backend_display_name()} backend failed: {exc}"
            )
            last_error = wrapped_error
            if (
                backend == "gemini"
                and attempt_number < attempt_count
                and _is_transient_gemini_error(exc)
            ):
                delay_seconds = GEMINI_TRANSIENT_RETRY_DELAYS_SECONDS[attempt_number - 1]
                print(f"Gemini transient error, retrying in {delay_seconds}s...")
                time.sleep(delay_seconds)
                continue
            raise wrapped_error from exc

    raise AgentReviewError(
        "Structured output could not be parsed into the Finding schema."
    ) from last_error


def _build_model(backend: BackendName) -> BaseLlm:
    if backend == "gemini":
        return ConfiguredGeminiModel(model=_configured_gemini_model_name)
    return DeterministicAgentReviewModel()


async def _run_single_review_attempt(
    runner: InMemoryRunner,
    prompt: str,
) -> list[Finding]:
    with contextlib.redirect_stderr(io.StringIO()):
        events = await runner.run_debug(prompt, quiet=True)
    response_text = _extract_final_response_text(events)
    return FINDINGS_ADAPTER.validate_json(response_text)


def _resolve_gemini_api_key() -> str | None:
    return os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")


def _resolve_gemini_model_name(gemini_model_name: str | None) -> str:
    if gemini_model_name:
        return gemini_model_name
    return os.environ.get(GEMINI_MODEL_ENV_VAR) or GEMINI_MODEL_NAME


def _is_transient_gemini_error(error: Exception) -> bool:
    error_text = str(error).upper()
    return (
        "503" in error_text
        or "UNAVAILABLE" in error_text
        or "HIGH DEMAND" in error_text
    )


def _extract_prompt_text(llm_request: LlmRequest) -> str:
    contents = llm_request.contents or []
    parts: list[str] = []
    for content in contents:
        for part in content.parts or []:
            if part.text:
                parts.append(part.text)
    return "".join(parts)


def _extract_final_response_text(events: list[object]) -> str:
    final_text = ""
    for event in events:
        if event.author != "semantic_compliance_review_agent":
            continue
        if not event.is_final_response() or not event.content or not event.content.parts:
            continue
        final_text = "".join(part.text or "" for part in event.content.parts if part.text)

    if not final_text:
        raise AgentReviewError("ADK agent did not return a final structured response.")
    return final_text


def _generate_findings(payload: dict) -> list[dict]:
    reviewable_texts = payload["reviewable_texts"]
    review_context = payload["review_context"]
    sensitive_terms = [term for term in review_context.get("sensitive_terms", []) if isinstance(term, str)]
    findings: list[dict] = []

    for item in reviewable_texts:
        text = item["text"]
        lower_text = text.lower()
        matched_terms = _find_sensitive_terms(text, sensitive_terms)

        if _contains_any(lower_text, SECURITY_KEYWORDS):
            detection_method = (
                "HYBRID"
                if matched_terms and _contains_any(lower_text, SEMANTIC_RISK_KEYWORDS)
                else "SEMANTIC_ANALYSIS"
            )
            findings.append(
                _build_finding(
                    item=item,
                    category="SECURITY_RISK",
                    severity="HIGH",
                    confidence="HIGH",
                    detection_method=detection_method,
                    explanation=(
                        "The text references a temporary or administrative secret-like value "
                        "that should be reviewed before release."
                    ),
                    recommendation=(
                        "Remove the sensitive reference or replace it with a neutral, human-reviewed task description."
                    ),
                    suggested_replacement=_build_safe_suggested_replacement(
                        text,
                        category="SECURITY_RISK",
                        confidence="HIGH",
                    ),
                )
            )
            continue

        if matched_terms:
            detection_method = "HYBRID" if _contains_any(lower_text, SEMANTIC_RISK_KEYWORDS) else "TERM_MATCH"
            explanation = (
                f"The text references configured sensitive term(s): {', '.join(matched_terms)}."
            )
            if detection_method == "HYBRID":
                explanation += " Surrounding language adds additional semantic risk."

            findings.append(
                _build_finding(
                    item=item,
                    category="INTERNAL_CODENAME_EXPOSURE",
                    severity="MEDIUM",
                    confidence="HIGH",
                    detection_method=detection_method,
                    explanation=explanation,
                    recommendation=(
                        "Review whether the internal project reference should be removed, generalized, or kept internal."
                    ),
                    suggested_replacement=_build_safe_suggested_replacement(
                        text,
                        category="INTERNAL_CODENAME_EXPOSURE",
                        confidence="HIGH",
                    ),
                )
            )
            continue

        if _contains_any(lower_text, COMPLIANCE_KEYWORDS):
            findings.append(
                _build_finding(
                    item=item,
                    category="COMPLIANCE_RISK",
                    severity="MEDIUM",
                    confidence="MEDIUM",
                    detection_method="SEMANTIC_ANALYSIS",
                    explanation="The text appears to reference regulated or confidential material that may require review.",
                    recommendation="Review the comment or docstring for compliance-sensitive wording before sharing externally.",
                    suggested_replacement=_build_safe_suggested_replacement(
                        text,
                        category="COMPLIANCE_RISK",
                        confidence="MEDIUM",
                    ),
                )
            )
            continue

        if _contains_any(lower_text, PROFESSIONALISM_KEYWORDS):
            findings.append(
                _build_finding(
                    item=item,
                    category="PROFESSIONALISM_RISK",
                    severity="LOW",
                    confidence="MEDIUM",
                    detection_method="SEMANTIC_ANALYSIS",
                    explanation="The text appears to use unprofessional or dismissive wording that may not be suitable to keep.",
                    recommendation="Replace the wording with a neutral, professional explanation.",
                    suggested_replacement=_build_safe_suggested_replacement(
                        text,
                        category="PROFESSIONALISM_RISK",
                        confidence="MEDIUM",
                    ),
                )
            )

    return findings


def _build_finding(
    *,
    item: dict,
    category: str,
    severity: str,
    confidence: str,
    detection_method: str,
    explanation: str,
    recommendation: str,
    suggested_replacement: str | None,
) -> dict:
    return {
        "id": f"finding:{item['id']}:{category.lower()}",
        "reviewable_text_id": item["id"],
        "category": category,
        "severity": severity,
        "confidence": confidence,
        "detection_method": detection_method,
        "source_text": item["text"],
        "line_start": item["line_start"],
        "line_end": item["line_end"],
        "explanation": explanation,
        "recommendation": recommendation,
        "suggested_replacement": suggested_replacement,
    }


def _find_sensitive_terms(text: str, sensitive_terms: list[str]) -> list[str]:
    matches: list[str] = []
    lower_text = text.lower()
    for term in sensitive_terms:
        if term.lower() in lower_text:
            matches.append(term)
    return matches


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(re.search(rf"\b{re.escape(keyword)}\b", text) for keyword in keywords)


def _build_safe_suggested_replacement(
    text: str,
    *,
    category: str,
    confidence: str,
) -> str | None:
    normalized_text = text.strip()
    if confidence != "HIGH" or not normalized_text:
        return None

    if category == "SECURITY_RISK":
        replacement = normalized_text
        replacement = re.sub(
            r"\badmin password\b",
            "admin credential reference",
            replacement,
            flags=re.IGNORECASE,
        )
        replacement = re.sub(
            r"\bpassword\b",
            "credential reference",
            replacement,
            flags=re.IGNORECASE,
        )
        replacement = re.sub(
            r"\bsecret\b",
            "sensitive reference",
            replacement,
            flags=re.IGNORECASE,
        )
        replacement = re.sub(
            r"\bapi key\b",
            "API credential reference",
            replacement,
            flags=re.IGNORECASE,
        )
        replacement = re.sub(
            r"\bprivate key\b",
            "private credential reference",
            replacement,
            flags=re.IGNORECASE,
        )
        replacement = re.sub(
            r"\btoken\b",
            "token reference",
            replacement,
            flags=re.IGNORECASE,
        )
        return replacement if replacement != normalized_text else None

    if category == "INTERNAL_CODENAME_EXPOSURE":
        replacement = re.sub(
            r"\bProject\s+[A-Z][A-Za-z0-9_-]*\b",
            "the internal project",
            normalized_text,
        )
        return replacement if replacement != normalized_text else None

    return None
