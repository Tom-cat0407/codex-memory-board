"""Business flow for Documentation.md status and log commands."""

from datetime import datetime
from pathlib import Path
import re

from .models import DocumentationLogEntry, DocumentationLogInput, DocumentationStatus
from .parser import parse_documentation_markdown
from .paths import resolve_documentation_file
from .store import read_text, write_text


CURRENT_PHASE_HEADING = "### Current Phase"
COMPLETED_ITEMS_HEADING = "### Completed Items"
NEXT_STEP_HEADING = "### Next Step"
LATEST_DECISION_HEADING = "### Latest Decision"
LATEST_VERIFICATION_HEADING = "### Latest Verification"
LOG_ENTRIES_HEADING = "## Log Entries"


def read_documentation_status(target_dir: Path) -> DocumentationStatus:
    """Load and parse Documentation.md from the target directory."""
    path = resolve_documentation_file(target_dir)
    if not path.exists():
        raise FileNotFoundError(f"Documentation file not found: {path}")
    return parse_documentation_markdown(read_text(path))


def append_documentation_log(
    target_dir: Path,
    log_input: DocumentationLogInput,
) -> DocumentationLogEntry:
    """Append a log entry and refresh the latest status sections."""
    path = resolve_documentation_file(target_dir)
    if not path.exists():
        raise FileNotFoundError(f"Documentation file not found: {path}")

    document_text = read_text(path)
    _ensure_structure(document_text)

    entry = DocumentationLogEntry(
        timestamp=datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S"),
        item=log_input.item,
        decision=log_input.decision,
        reason=log_input.reason,
        verification_command=log_input.verification_command,
        verification_result=log_input.verification_result,
    )

    updated_text = _replace_section_body(
        document_text,
        LATEST_DECISION_HEADING,
        _format_latest_decision_body(entry),
    )
    updated_text = _replace_section_body(
        updated_text,
        LATEST_VERIFICATION_HEADING,
        _format_latest_verification_body(entry),
    )
    updated_text = _append_log_entry(updated_text, entry)

    write_text(path, updated_text)
    return entry


def _ensure_structure(text: str) -> None:
    required_headings = (
        CURRENT_PHASE_HEADING,
        COMPLETED_ITEMS_HEADING,
        NEXT_STEP_HEADING,
        LATEST_DECISION_HEADING,
        LATEST_VERIFICATION_HEADING,
        LOG_ENTRIES_HEADING,
    )
    missing = [heading for heading in required_headings if heading not in text]
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"Documentation.md is missing required sections: {joined}")


def _replace_section_body(text: str, heading: str, body: str) -> str:
    pattern = re.compile(
        rf"(?ms)^{re.escape(heading)}\s*\n.*?(?=^##\s|^###\s|\Z)"
    )
    match = pattern.search(text)
    if not match:
        raise ValueError(f"Documentation.md is missing required section: {heading}")

    replacement = f"{heading}\n{body.strip()}\n\n"
    before = text[: match.start()]
    after = text[match.end() :].lstrip("\n")
    return f"{before}{replacement}{after}"


def _append_log_entry(text: str, entry: DocumentationLogEntry) -> str:
    if LOG_ENTRIES_HEADING not in text:
        raise ValueError(f"Documentation.md is missing required section: {LOG_ENTRIES_HEADING}")
    return f"{text.rstrip()}\n\n{_format_log_entry(entry)}\n"


def _format_latest_decision_body(entry: DocumentationLogEntry) -> str:
    return "\n".join(
        (
            f"- Decision: {entry.decision}",
            f"- Reason: {entry.reason}",
        )
    )


def _format_latest_verification_body(entry: DocumentationLogEntry) -> str:
    return "\n".join(
        (
            f"- Command: {entry.verification_command}",
            f"- Result: {entry.verification_result}",
        )
    )


def _format_log_entry(entry: DocumentationLogEntry) -> str:
    return "\n".join(
        (
            f"### {entry.timestamp}",
            f"- Item: {entry.item}",
            f"- Decision: {entry.decision}",
            f"- Reason: {entry.reason}",
            f"- Verification Command: {entry.verification_command}",
            f"- Verification Result: {entry.verification_result}",
        )
    )
