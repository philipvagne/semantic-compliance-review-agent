import argparse

from src.file_reader import FileReadError
from src.file_reader import read_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read a single source file safely.")
    parser.add_argument("file_path", help="Path to a single source code file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        file_content = read_file(args.file_path)
    except FileReadError as exc:
        raise SystemExit(f"File read failed: {exc}") from exc

    print("File read successfully")
    print(f"Path: {file_content.path}")
    print(f"Extension: {file_content.extension}")
    print(f"Lines: {file_content.line_count}")
    print(f"Characters: {len(file_content.raw_text)}")


if __name__ == "__main__":
    main()
