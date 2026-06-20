import json
from typing import AsyncGenerator

from google.adk.agents import Agent
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import InMemoryRunner
from google.genai import types

from src.schemas import ReviewFinding


def load_sensitive_terms() -> list[str]:
    """Return a tiny in-memory list for the ADK feasibility spike."""
    return ["Project Titan", "Falcon", "NovaPay"]


class DeterministicReviewModel(BaseLlm):
    """Local test model that exercises ADK tool calling without external APIs."""

    model: str = "phase-0-5-deterministic-review-model"

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        last_content = llm_request.contents[-1] if llm_request.contents else None
        function_response = None
        if last_content and last_content.parts:
            function_response = last_content.parts[0].function_response

        if function_response:
            sensitive_terms = function_response.response["result"]
            finding = ReviewFinding(
                category="Security Risk",
                severity="high",
                confidence="high",
                explanation=(
                    "The review text references a temporary admin password "
                    f"before production. Sensitive terms were loaded for context: "
                    f"{', '.join(sensitive_terms)}."
                ),
                recommendation=(
                    "Remove the temporary admin password reference and replace it "
                    "with a neutral deployment task."
                ),
            )
            yield LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text=finding.model_dump_json())],
                )
            )
            return

        yield LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        function_call=types.FunctionCall(
                            id="load-sensitive-terms-call",
                            name="load_sensitive_terms",
                            args={},
                        )
                    )
                ],
            )
        )


def build_agent() -> Agent:
    return Agent(
        name="semantic_compliance_spike",
        description="Minimal Phase 0.5 ADK feasibility spike agent.",
        instruction=(
            "Review the provided text, call load_sensitive_terms, and return "
            "exactly one structured finding."
        ),
        model=DeterministicReviewModel(),
        tools=[load_sensitive_terms],
        output_schema=ReviewFinding,
    )


async def run_spike(review_text: str) -> dict:
    runner = InMemoryRunner(agent=build_agent())
    events = await runner.run_debug(review_text, quiet=True)

    tool_output = []
    final_text = ""
    for event in events:
        for function_response in event.get_function_responses():
            if function_response.name == "load_sensitive_terms":
                tool_output = function_response.response["result"]

        if event.author != "semantic_compliance_spike":
            continue
        if not event.is_final_response() or not event.content or not event.content.parts:
            continue

        final_text = "".join(part.text or "" for part in event.content.parts if part.text)

    finding = ReviewFinding.model_validate_json(final_text)
    return {
        "input_text": review_text,
        "tool_name": "load_sensitive_terms",
        "tool_output": tool_output,
        "finding": finding.model_dump(),
    }


def format_result(result: dict) -> str:
    return json.dumps(result, indent=2)
