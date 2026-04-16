"""Rule-driven next-step selection."""

from .models import DocumentationStatus, NextStepRecommendation, PlanDocument


def infer_next_step(
    documentation: DocumentationStatus,
    plan: PlanDocument,
) -> NextStepRecommendation:
    """Infer the next action from Documentation.md and Plan.md."""
    current_phase = _meaningful_scalar(documentation.current_phase)
    if not current_phase:
        raise ValueError("Insufficient information: Documentation.md Current Phase is not set.")

    documented_next_steps = _meaningful_items(documentation.next_steps)
    if documented_next_steps:
        return NextStepRecommendation(
            current_phase=current_phase,
            basis="Documentation.md Next Step",
            suggested_next_step=documented_next_steps[0],
        )

    verification_result = _meaningful_scalar(documentation.latest_verification_result)
    if verification_result and _verification_failed(verification_result):
        return NextStepRecommendation(
            current_phase=current_phase,
            basis="Latest verification result indicates failure",
            suggested_next_step="先修复验证失败",
        )

    current_milestone = _meaningful_scalar(plan.current_milestone)
    if not current_milestone:
        raise ValueError("Insufficient information: Plan.md Current Milestone is not set.")

    current_index = None
    for index, milestone in enumerate(plan.milestones):
        if milestone.title == current_milestone:
            current_index = index
            break

    if current_index is None:
        raise ValueError(
            f"Insufficient information: current milestone '{current_milestone}' was not found in Plan.md."
        )

    current_plan = plan.milestones[current_index]
    incomplete_current = [task.title for task in current_plan.tasks if not task.completed]
    meaningful_current = _meaningful_items(incomplete_current)
    if meaningful_current:
        return NextStepRecommendation(
            current_phase=current_phase,
            basis=f"First incomplete deliverable in current milestone '{current_plan.title}'",
            suggested_next_step=meaningful_current[0],
        )

    next_index = current_index + 1
    if next_index >= len(plan.milestones):
        raise ValueError("Insufficient information: current milestone is complete and no next milestone exists.")

    next_milestone = plan.milestones[next_index]
    next_tasks = _meaningful_items([task.title for task in next_milestone.tasks])
    if not next_tasks:
        raise ValueError(
            f"Insufficient information: next milestone '{next_milestone.title}' has no deliverables."
        )

    return NextStepRecommendation(
        current_phase=current_phase,
        basis=f"Current milestone complete; first task in next milestone '{next_milestone.title}'",
        suggested_next_step=next_tasks[0],
    )


def _meaningful_items(values: list[str]) -> list[str]:
    return [value for value in (_meaningful_scalar(item) for item in values) if value]


def _meaningful_scalar(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        return ""
    if normalized.lower() == "not set":
        return ""
    return normalized


def _verification_failed(result: str) -> bool:
    normalized = result.lower()
    failure_markers = ("failed", "fail", "error", "errors", "traceback", "exception")
    return any(marker in normalized for marker in failure_markers)
