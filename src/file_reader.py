"""Read one source file into the shared FileContent contract.

Purpose:
- Convert a single on-disk file into the normalized file object used by the
  rest of the pipeline.

Input:
- Path to one source file.

Output:
- One FileContent object.

Responsibilities:
- Validate that the path points to a readable file.
- Read text safely as UTF-8.
- Return basic file metadata plus raw text.

Non-responsibilities:
- Extract reviewable text.
- Classify risk.
- Generate findings or reports.
"""

from pathlib import Path

from src.schemas import FileContent


class FileReadError(Exception):
    """Raised when a source file cannot be read safely."""


def read_file(file_path: str) -> FileContent:
    path = Path(file_path).expanduser()

    if not path.exists():
        raise FileReadError(f"File not found: {path}")

    if path.is_dir():
        raise FileReadError(f"Expected a file but received a directory: {path}")

    try:
        raw_text = path.read_text(encoding="utf-8")
    except PermissionError as exc:
        raise FileReadError(f"Permission denied: {path}") from exc
    except UnicodeDecodeError as exc:
        raise FileReadError(f"File is not valid UTF-8: {path}") from exc
    except OSError as exc:
        raise FileReadError(f"Unable to read file: {path}") from exc

    return FileContent(
        path=str(path).replace("\\", "/"),
        filename=path.name,
        extension=path.suffix,
        raw_text=raw_text,
        line_count=len(raw_text.splitlines()),
    )
