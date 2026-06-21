import argparse

from src.agent_review import AgentReviewError
from src.agent_review import configure_backend
from src.agent_review import get_backend_display_name
from src.agent_review import get_model_display_name
from src.agent_review import review
from src.context_loader import ContextLoadError
from src.context_loader import load_review_context
from src.file_reader import FileReadError
from src.file_reader import read_file
from src.report_writer import ReportWriteError
from src.report_writer import write_audit_report
from src.text_extractor import ExtractionError
from src.text_extractor import extract_reviewable_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read one source file and summarize extracted reviewable text."
    )
    parser.add_argument("file_path", help="Path to a single source code file.")
    parser.add_argument(
        "--backend",
        choices=("gemini", "deterministic"),
        default="gemini",
        help="Agent review backend to use. Defaults to Gemini.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        configure_backend(args.backend)
    except AgentReviewError as exc:
        raise SystemExit(f"Agent review startup failed: {exc}") from exc

    try:
        file_content = read_file(args.file_path)
    except FileReadError as exc:
        raise SystemExit(f"File read failed: {exc}") from exc

    try:
        reviewable_items = extract_reviewable_text(file_content)
    except ExtractionError as exc:
        raise SystemExit(f"Text extraction failed: {exc}") from exc

    try:
        review_context = load_review_context()
    except ContextLoadError as exc:
        raise SystemExit(f"Context loading failed: {exc}") from exc

    print("File read successfully")
    print(f"Path: {file_content.path}")
    print(f"Backend: {get_backend_display_name()}")
    print(f"Reviewable text items found: {len(reviewable_items)}")
    print("Context loaded successfully")
    print(f"Sensitive terms loaded: {len(review_context.sensitive_terms)}")
    if review_context.config_warnings:
        print(f"Config warnings: {len(review_context.config_warnings)}")

    try:
        findings = review(reviewable_items, review_context)
    except AgentReviewError as exc:
        raise SystemExit(f"Agent review failed: {exc}") from exc

    try:
        report_path = write_audit_report(
            file_content=file_content,
            reviewable_texts=reviewable_items,
            review_context=review_context,
            findings=findings,
            backend=get_backend_display_name(),
            model=get_model_display_name(),
        )
    except ReportWriteError as exc:
        raise SystemExit(f"Report generation failed: {exc}") from exc

    print(f"Findings generated: {len(findings)}")
    print(f"Report written to: {report_path}")

    for item in reviewable_items:
        preview = item.text.replace("\n", " ").strip()
        if len(preview) > 80:
            preview = f"{preview[:77]}..."
        print(f"- {item.source_type} {item.line_start}-{item.line_end}: {preview}")

    for finding in findings:
        summary = finding.explanation.split(".")[0].strip()
        if not summary:
            summary = finding.source_text.replace("\n", " ").strip()
        print(f"* {finding.severity} {finding.category} line {finding.line_start}: {summary}")


if __name__ == "__main__":
    main()
