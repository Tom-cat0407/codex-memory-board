"""I/O orchestration for the validate command."""

from pathlib import Path

from .models import MemoryValidationReport
from .parser import parse_documentation_markdown, parse_plan_markdown
from .paths import MEMORY_BOARD_FILES, resolve_repo_file
from .store import read_text
from .validate import validate_memory


def build_validation_report(target_dir: Path) -> MemoryValidationReport:
    """Read the repository memory files and validate their current state."""
    root = Path(target_dir).resolve()
    file_texts: dict[str, str | None] = {}

    for filename in MEMORY_BOARD_FILES:
        path = resolve_repo_file(filename, root)
        file_texts[filename] = read_text(path) if path.exists() else None

    documentation_text = file_texts.get("Documentation.md")
    plan_text = file_texts.get("Plan.md")

    documentation = (
        parse_documentation_markdown(documentation_text)
        if documentation_text is not None
        else None
    )
    plan = parse_plan_markdown(plan_text) if plan_text is not None else None

    return validate_memory(file_texts=file_texts, documentation=documentation, plan=plan)
