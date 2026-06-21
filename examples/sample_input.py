"""Small sample file for Phase 3 manual text-extraction testing."""

# TODO: remove the temporary admin password before release
# NOTE: this sample intentionally contains several reviewable text types


def greet(name: str) -> str:
    """Return a friendly greeting for manual extractor testing."""
    # Friendly example content for the extractor.
    return f"Hello, {name}!"


if __name__ == "__main__":
    # FIXME: replace the hard-coded example value later
    print(greet("world"))
