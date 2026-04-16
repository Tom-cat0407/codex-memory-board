"""I/O orchestration for the next command."""

from pathlib import Path

from .next_step import infer_next_step
from .parser import parse_documentation_markdown, parse_plan_markdown
from .paths import resolve_documentation_file, resolve_plan_file
from .store import read_text


def build_next_recommendation(target_dir: Path):
    """Read Documentation.md and Plan.md, then choose the next step."""
    documentation_path = resolve_documentation_file(target_dir)
    plan_path = resolve_plan_file(target_dir)

    if not documentation_path.exists():
        raise FileNotFoundError(f"Documentation file not found: {documentation_path}")
    if not plan_path.exists():
        raise FileNotFoundError(f"Plan file not found: {plan_path}")

    documentation = parse_documentation_markdown(read_text(documentation_path))
    plan = parse_plan_markdown(read_text(plan_path))
    return infer_next_step(documentation, plan)
