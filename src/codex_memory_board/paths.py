"""Path helpers for repository-level files."""

from pathlib import Path


PACKAGE_NAME = "codex_memory_board"
AGENTS_FILE = "AGENTS.md"
PROMPT_FILE = "Prompt.md"
PLAN_FILE = "Plan.md"
IMPLEMENT_FILE = "Implement.md"
DOCUMENTATION_FILE = "Documentation.md"
MEMORY_BOARD_FILES = (
    AGENTS_FILE,
    PROMPT_FILE,
    PLAN_FILE,
    IMPLEMENT_FILE,
    DOCUMENTATION_FILE,
)


def project_root(cwd: Path = None) -> Path:
    """Return the working project root."""
    if cwd is not None:
        return Path(cwd).resolve()
    return Path.cwd().resolve()


def resolve_repo_file(filename: str, cwd: Path = None) -> Path:
    """Resolve a root-level repository file path."""
    return project_root(cwd) / filename


def resolve_documentation_file(cwd: Path = None) -> Path:
    """Resolve the Documentation.md path for a repository."""
    return resolve_repo_file(DOCUMENTATION_FILE, cwd)


def resolve_plan_file(cwd: Path = None) -> Path:
    """Resolve the Plan.md path for a repository."""
    return resolve_repo_file(PLAN_FILE, cwd)
