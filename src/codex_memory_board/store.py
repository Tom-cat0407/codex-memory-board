"""File read/write helpers only."""

from pathlib import Path


def read_text(path: Path) -> str:
    """Read UTF-8 text from a file."""
    return Path(path).read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    """Write UTF-8 text to a file, creating parent directories as needed."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def append_text(path: Path, content: str) -> None:
    """Append UTF-8 text to a file, creating parent directories as needed."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(content)

