import argparse

from src.file_reader import FileReadError
from src.file_reader import read_file
from src.text_extractor import ExtractionError
from src.text_extractor import extract_reviewable_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read one source file and summarize extracted reviewable text."
    )
    parser.add_argument("file_path", help="Path to a single source code file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        file_content = read_file(args.file_path)
    except FileReadError as exc:
        raise SystemExit(f"File read failed: {exc}") from exc

    try:
        reviewable_items = extract_reviewable_text(file_content)
    except ExtractionError as exc:
        raise SystemExit(f"Text extraction failed: {exc}") from exc

    print("File read successfully")
    print(f"Path: {file_content.path}")
    print(f"Reviewable text items found: {len(reviewable_items)}")

    for item in reviewable_items:
        preview = item.text.replace("\n", " ").strip()
        if len(preview) > 80:
            preview = f"{preview[:77]}..."
        print(f"- {item.source_type} {item.line_start}-{item.line_end}: {preview}")


if __name__ == "__main__":
    main()
