"""Rule-driven project memory validation."""

from .models import DocumentationStatus, MemoryValidationReport, PlanDocument, ValidationFinding
from .next_step import infer_next_step
from .parser import extract_markdown_headings


DOCUMENTATION_REQUIRED_HEADINGS = (
    "# Documentation",
    "## Current Status",
    "### Current Phase",
    "### Completed Items",
    "### Next Step",
    "### Latest Decision",
    "### Latest Verification",
    "## Log Entries",
)

PLAN_REQUIRED_HEADINGS = (
    "# Plan",
    "## Current Milestone",
    "## Milestones",
)

AGENTS_REQUIRED_HEADINGS = (
    "# AGENTS",
    "## Purpose",
)

PROMPT_REQUIRED_HEADINGS = (
    "# Prompt",
    "## Purpose",
)

IMPLEMENT_REQUIRED_HEADINGS = (
    "# Implement",
)


def validate_memory(
    file_texts: dict[str, str | None],
    documentation: DocumentationStatus | None,
    plan: PlanDocument | None,
) -> MemoryValidationReport:
    """Validate the repository memory files and current working state."""
    findings: list[ValidationFinding] = []

    _validate_file_exists(file_texts, "AGENTS.md", findings)
    _validate_file_exists(file_texts, "Prompt.md", findings)
    _validate_file_exists(file_texts, "Plan.md", findings)
    _validate_file_exists(file_texts, "Implement.md", findings)
    _validate_file_exists(file_texts, "Documentation.md", findings)

    _validate_simple_file_structure(
        file_texts,
        "AGENTS.md",
        AGENTS_REQUIRED_HEADINGS,
        findings,
    )
    _validate_simple_file_structure(
        file_texts,
        "Prompt.md",
        PROMPT_REQUIRED_HEADINGS,
        findings,
    )
    _validate_simple_file_structure(
        file_texts,
        "Implement.md",
        IMPLEMENT_REQUIRED_HEADINGS,
        findings,
    )

    plan_structure_valid = _validate_plan_structure(file_texts.get("Plan.md"), plan, findings)
    documentation_structure_valid = _validate_documentation_structure(
        file_texts.get("Documentation.md"),
        documentation,
        findings,
    )
    _validate_command_support(
        documentation,
        plan,
        documentation_structure_valid=documentation_structure_valid,
        plan_structure_valid=plan_structure_valid,
        findings=findings,
    )

    pass_count = sum(1 for finding in findings if finding.level == "PASS")
    warn_count = sum(1 for finding in findings if finding.level == "WARN")
    fail_count = sum(1 for finding in findings if finding.level == "FAIL")

    overall_status = "PASS"
    if fail_count:
        overall_status = "FAIL"
    elif warn_count:
        overall_status = "WARN"

    return MemoryValidationReport(
        overall_status=overall_status,
        findings=findings,
        pass_count=pass_count,
        warn_count=warn_count,
        fail_count=fail_count,
    )


def _validate_file_exists(
    file_texts: dict[str, str | None],
    filename: str,
    findings: list[ValidationFinding],
) -> None:
    if file_texts.get(filename) is None:
        findings.append(
            ValidationFinding(
                level="FAIL",
                target=filename,
                message="Required file is missing.",
            )
        )
        return
    findings.append(
        ValidationFinding(
            level="PASS",
            target=filename,
            message="File exists.",
        )
    )


def _validate_simple_file_structure(
    file_texts: dict[str, str | None],
    filename: str,
    required_headings: tuple[str, ...],
    findings: list[ValidationFinding],
) -> None:
    text = file_texts.get(filename)
    if text is None:
        return

    headings = set(extract_markdown_headings(text))
    missing = [heading for heading in required_headings if heading not in headings]
    if filename == "Implement.md":
        secondary = ("## Implementation principles", "## Current Focus")
        if not any(heading in headings for heading in secondary):
            missing.append("one of: ## Implementation principles, ## Current Focus")
    if not missing:
        findings.append(
            ValidationFinding(
                level="PASS",
                target=filename,
                message="Minimum structure is present.",
            )
        )
        return

    level = "FAIL" if required_headings[0] not in headings else "WARN"
    findings.append(
        ValidationFinding(
            level=level,
            target=filename,
            message=f"Missing headings: {', '.join(missing)}",
        )
    )


def _validate_plan_structure(
    plan_text: str | None,
    plan: PlanDocument | None,
    findings: list[ValidationFinding],
) -> bool:
    if plan_text is None:
        return False

    headings = set(extract_markdown_headings(plan_text))
    missing = [heading for heading in PLAN_REQUIRED_HEADINGS if heading not in headings]
    if missing:
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="Plan.md",
                message=f"Missing headings: {', '.join(missing)}",
            )
        )
        return False

    findings.append(
        ValidationFinding(
            level="PASS",
            target="Plan.md",
            message="Required headings are present.",
        )
    )

    if plan is None:
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="Plan.md",
                message="Plan could not be parsed.",
            )
        )
        return False

    valid = True
    if not _meaningful(plan.current_milestone):
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="Plan.md",
                message="Current Milestone is not set.",
            )
        )
        valid = False
    else:
        findings.append(
            ValidationFinding(
                level="PASS",
                target="Plan.md",
                message=f"Current Milestone is set to '{plan.current_milestone}'.",
            )
        )

    if not plan.milestones:
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="Plan.md",
                message="No milestones were found.",
            )
        )
        return False

    findings.append(
        ValidationFinding(
            level="PASS",
            target="Plan.md",
            message=f"Found {len(plan.milestones)} milestone(s).",
        )
    )

    if not any(milestone.title == plan.current_milestone for milestone in plan.milestones):
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="Plan.md",
                message=f"Current milestone '{plan.current_milestone}' was not found in the milestone list.",
            )
        )
        valid = False
    else:
        findings.append(
            ValidationFinding(
                level="PASS",
                target="Plan.md",
                message="Current milestone exists in the milestone list.",
            )
        )

    task_count = sum(len(milestone.tasks) for milestone in plan.milestones)
    if task_count == 0:
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="Plan.md",
                message="No deliverables were found in any milestone.",
            )
        )
        valid = False
    else:
        findings.append(
            ValidationFinding(
                level="PASS",
                target="Plan.md",
                message=f"Found {task_count} deliverable(s) across milestones.",
            )
        )
    return valid


def _validate_documentation_structure(
    documentation_text: str | None,
    documentation: DocumentationStatus | None,
    findings: list[ValidationFinding],
) -> bool:
    if documentation_text is None:
        return False

    headings = set(extract_markdown_headings(documentation_text))
    missing = [heading for heading in DOCUMENTATION_REQUIRED_HEADINGS if heading not in headings]
    if missing:
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="Documentation.md",
                message=f"Missing headings: {', '.join(missing)}",
            )
        )
        return False

    findings.append(
        ValidationFinding(
            level="PASS",
            target="Documentation.md",
            message="Required headings are present.",
        )
    )

    if documentation is None:
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="Documentation.md",
                message="Documentation could not be parsed.",
            )
        )
        return False

    valid = True
    if not _meaningful(documentation.current_phase):
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="Documentation.md",
                message="Current Phase is not set.",
            )
        )
        valid = False
    else:
        findings.append(
            ValidationFinding(
                level="PASS",
                target="Documentation.md",
                message=f"Current Phase is set to '{documentation.current_phase}'.",
            )
        )

    if not _meaningful(documentation.latest_decision):
        findings.append(
            ValidationFinding(
                level="WARN",
                target="Documentation.md",
                message="Latest Decision exists but is not meaningfully set.",
            )
        )
    else:
        findings.append(
            ValidationFinding(
                level="PASS",
                target="Documentation.md",
                message="Latest Decision is available.",
            )
        )

    if not _meaningful(documentation.latest_verification_result):
        findings.append(
            ValidationFinding(
                level="WARN",
                target="Documentation.md",
                message="Latest Verification exists but its result is not meaningfully set.",
            )
        )
    else:
        findings.append(
            ValidationFinding(
                level="PASS",
                target="Documentation.md",
                message="Latest Verification result is available.",
            )
        )

    if documentation.log_entries:
        findings.append(
            ValidationFinding(
                level="PASS",
                target="Documentation.md",
                message=f"Found {len(documentation.log_entries)} log entrie(s).",
            )
        )
    else:
        findings.append(
            ValidationFinding(
                level="WARN",
                target="Documentation.md",
                message="Log Entries exists but no concrete log entries were found.",
            )
        )
    return valid


def _validate_command_support(
    documentation: DocumentationStatus | None,
    plan: PlanDocument | None,
    documentation_structure_valid: bool,
    plan_structure_valid: bool,
    findings: list[ValidationFinding],
) -> None:
    status_ready = documentation_structure_valid and documentation is not None and _meaningful(documentation.current_phase) != ""
    if status_ready:
        findings.append(
            ValidationFinding(
                level="PASS",
                target="cmb status",
                message="Current Documentation.md state supports status output.",
            )
        )
    else:
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="cmb status",
                message="Current Documentation.md state is not sufficient for stable status output.",
            )
        )

    log_ready = documentation_structure_valid and documentation is not None
    if log_ready:
        findings.append(
            ValidationFinding(
                level="PASS",
                target="cmb log",
                message="Documentation.md contains the sections required by log.",
            )
        )
    else:
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="cmb log",
                message="Documentation.md is not sufficient for log updates.",
            )
        )

    if documentation is None or plan is None or not documentation_structure_valid or not plan_structure_valid:
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="cmb next",
                message="Documentation.md and Plan.md must both have valid structure for next.",
            )
        )
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="cmb handoff",
                message="Documentation.md and Plan.md must both have valid structure for handoff.",
            )
        )
        return

    try:
        infer_next_step(documentation, plan)
    except ValueError as exc:
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="cmb next",
                message=f"Current state is not sufficient for next: {exc}",
            )
        )
        findings.append(
            ValidationFinding(
                level="FAIL",
                target="cmb handoff",
                message=f"Current state is not sufficient for handoff: {exc}",
            )
        )
        return

    findings.append(
        ValidationFinding(
            level="PASS",
            target="cmb next",
            message="Current state is sufficient for next-step selection.",
        )
    )
    findings.append(
        ValidationFinding(
            level="PASS",
            target="cmb handoff",
            message="Current state is sufficient for handoff generation.",
        )
    )


def _meaningful(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        return ""
    if normalized.lower() == "not set":
        return ""
    return normalized
