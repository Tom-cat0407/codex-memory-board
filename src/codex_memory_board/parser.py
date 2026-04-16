"""Markdown parsing helpers."""

import re

from .models import DocumentationLogEntry, DocumentationStatus, PlanDocument, PlanMilestone, PlanTask


def parse_documentation_markdown(text: str) -> DocumentationStatus:
    """Parse Documentation.md into a structured status object."""
    log_section = _extract_section(text, "## Log Entries", stop_at_level=2)
    return DocumentationStatus(
        current_phase=_extract_scalar(text, "### Current Phase"),
        completed_items=_extract_list(text, "### Completed Items"),
        next_steps=_extract_list(text, "### Next Step"),
        latest_decision=_extract_keyed_value(text, "### Latest Decision", "Decision"),
        latest_decision_reason=_extract_keyed_value(text, "### Latest Decision", "Reason"),
        latest_verification_command=_extract_keyed_value(
            text,
            "### Latest Verification",
            "Command",
        ),
        latest_verification_result=_extract_keyed_value(
            text,
            "### Latest Verification",
            "Result",
        ),
        log_entries=_parse_log_entries(log_section),
    )


def parse_memory_markdown(text: str):
    """Parse Markdown memory content into structured data."""
    raise NotImplementedError("General memory parsing will be implemented in a later phase.")


def parse_plan_markdown(text: str) -> PlanDocument:
    """Parse Plan.md into milestone and deliverable data."""
    current_milestone = _extract_scalar(text, "## Current Milestone")
    milestones_section = _extract_section(text, "## Milestones", stop_at_level=2)
    milestones: list[PlanMilestone] = []

    current_title = ""
    current_tasks: list[PlanTask] = []

    for line in milestones_section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("### "):
            if current_title:
                milestones.append(PlanMilestone(title=current_title, tasks=current_tasks))
            current_title = stripped.replace("### ", "", 1).strip()
            current_tasks = []
            continue

        match = re.match(r"^- \[(?P<flag>[ xX])\] (?P<title>.+)$", stripped)
        if match and current_title:
            current_tasks.append(
                PlanTask(
                    title=match.group("title").strip(),
                    completed=match.group("flag").lower() == "x",
                )
            )

    if current_title:
        milestones.append(PlanMilestone(title=current_title, tasks=current_tasks))

    return PlanDocument(current_milestone=current_milestone, milestones=milestones)


def extract_markdown_headings(text: str) -> list[str]:
    """Return stripped Markdown heading lines."""
    headings: list[str] = []
    for line in text.splitlines():
        stripped = _normalize_line(line.strip())
        if stripped.startswith("#"):
            headings.append(stripped)
    return headings


def _extract_section(text: str, heading: str, stop_at_level: int) -> str:
    lines = text.splitlines()
    start_index = None
    for index, line in enumerate(lines):
        if _normalize_line(line.strip()) == heading:
            start_index = index + 1
            break

    if start_index is None:
        return ""

    body: list[str] = []
    stop_prefixes = _section_stop_prefixes(stop_at_level)
    for line in lines[start_index:]:
        stripped = _normalize_line(line.strip())
        if stripped.startswith(stop_prefixes):
            break
        body.append(line)
    return "\n".join(body).strip()


def _section_stop_prefixes(stop_at_level: int) -> tuple[str, ...]:
    if stop_at_level == 2:
        return ("## ",)
    return ("## ", "### ")


def _extract_scalar(text: str, heading: str) -> str:
    body = _extract_section(text, heading, stop_at_level=3)
    for line in body.splitlines():
        value = _normalize_line(line.strip())
        if value:
            return _strip_bullet_prefix(value)
    return ""


def _extract_list(text: str, heading: str) -> list[str]:
    body = _extract_section(text, heading, stop_at_level=3)
    items: list[str] = []
    for line in body.splitlines():
        stripped = _normalize_line(line.strip())
        if not stripped:
            continue
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
        else:
            items.append(stripped)
    return items


def _extract_keyed_value(text: str, heading: str, key: str) -> str:
    body = _extract_section(text, heading, stop_at_level=3)
    marker = f"{key}:"
    for line in body.splitlines():
        value = _strip_bullet_prefix(_normalize_line(line.strip()))
        if value.startswith(marker):
            return value[len(marker) :].strip()
    return ""


def _parse_log_entries(log_section: str) -> list[DocumentationLogEntry]:
    entries: list[DocumentationLogEntry] = []
    if not log_section:
        return entries

    blocks: list[list[str]] = []
    current_block: list[str] = []
    for line in log_section.splitlines():
        if _normalize_line(line.strip()).startswith("### "):
            if current_block:
                blocks.append(current_block)
            current_block = [_normalize_line(line.strip())]
            continue
        if current_block:
            current_block.append(line)
    if current_block:
        blocks.append(current_block)

    for block in blocks:
        timestamp = block[0].replace("### ", "", 1).strip()
        fields = {
            "Item": "",
            "Decision": "",
            "Reason": "",
            "Verification Command": "",
            "Verification Result": "",
        }
        for line in block[1:]:
            stripped = _strip_bullet_prefix(line.strip())
            for key in fields:
                prefix = f"{key}:"
                if stripped.startswith(prefix):
                    fields[key] = stripped[len(prefix) :].strip()
        entries.append(
            DocumentationLogEntry(
                timestamp=timestamp,
                item=fields["Item"],
                decision=fields["Decision"],
                reason=fields["Reason"],
                verification_command=fields["Verification Command"],
                verification_result=fields["Verification Result"],
            )
        )

    return entries


def _strip_bullet_prefix(value: str) -> str:
    value = _normalize_line(value)
    if value.startswith("- "):
        return value[2:].strip()
    return value


def _normalize_line(value: str) -> str:
    return value.lstrip("\ufeff")
