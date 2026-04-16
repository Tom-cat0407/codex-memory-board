"""Initialization flow for project memory files."""

from dataclasses import dataclass
from pathlib import Path

from .paths import MEMORY_BOARD_FILES, resolve_repo_file
from .store import write_text
from .templates import get_init_templates


@dataclass(frozen=True)
class InitFileResult:
    """Result for one initialized file."""

    filename: str
    path: Path
    action: str


@dataclass(frozen=True)
class InitResult:
    """Summary of an init run."""

    root: Path
    files: tuple[InitFileResult, ...]


def initialize_memory_board(target_dir: Path, overwrite: bool = False) -> InitResult:
    """Create the project memory board files in the target directory."""
    root = Path(target_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)

    templates = get_init_templates()
    results: list[InitFileResult] = []

    for filename in MEMORY_BOARD_FILES:
        path = resolve_repo_file(filename, root)
        if path.exists() and not overwrite:
            results.append(InitFileResult(filename=filename, path=path, action="skipped"))
            continue

        write_text(path, templates[filename])
        results.append(InitFileResult(filename=filename, path=path, action="created"))

    return InitResult(root=root, files=tuple(results))

