"""I/O orchestration for the handoff command."""

from pathlib import Path

from .documentation_board import read_documentation_status
from .handoff import build_handoff_prompt
from .models import HandoffPromptData
from .next_board import build_next_recommendation


def build_handoff_text(target_dir: Path) -> str:
    """Read project state and produce a handoff prompt."""
    documentation = read_documentation_status(target_dir)
    recommendation = build_next_recommendation(target_dir)

    payload = HandoffPromptData(
        current_phase=recommendation.current_phase,
        completed_items=_meaningful_items(documentation.completed_items),
        suggested_next_step=recommendation.suggested_next_step,
        constraints=_build_constraints(recommendation.suggested_next_step),
        files_to_read=_build_files_to_read(recommendation.suggested_next_step),
        latest_decision=documentation.latest_decision,
        latest_verification_result=documentation.latest_verification_result,
    )
    return build_handoff_prompt(payload)


def _build_constraints(suggested_next_step: str) -> list[str]:
    target = _extract_target_command(suggested_next_step)
    constraints = []
    if target:
        constraints.append(f"只实现 `{target}`，不要顺手扩展其它命令或额外功能")
    else:
        constraints.append("只推进当前建议下一步，不要顺手扩展其它命令或额外功能")
    constraints.extend(
        [
            "保持规则驱动，不引入复杂推理或额外模型调用",
            "优先复用 Documentation.md 与 Plan.md 的固定结构",
            "除非当前任务明确要求，否则不要修改无关 Markdown 文件",
        ]
    )
    return constraints


def _build_files_to_read(suggested_next_step: str) -> list[str]:
    files = [
        "Documentation.md",
        "Plan.md",
        "src/codex_memory_board/cli.py",
    ]
    lowered = suggested_next_step.lower()
    if "handoff" in lowered:
        files.append("src/codex_memory_board/handoff.py")
    elif "validate" in lowered:
        files.append("src/codex_memory_board/validate.py")
    elif "next" in lowered:
        files.append("src/codex_memory_board/next_step.py")
    elif "status" in lowered or "log" in lowered:
        files.append("src/codex_memory_board/documentation_board.py")
    return files


def _extract_target_command(suggested_next_step: str) -> str:
    lowered = suggested_next_step.lower()
    if "cmb validate" in lowered or "validate" in lowered:
        return "cmb validate"
    if "cmb handoff" in lowered or "handoff" in lowered:
        return "cmb handoff"
    if "cmb next" in lowered or "next" in lowered:
        return "cmb next"
    if "cmb status" in lowered or "status" in lowered:
        return "cmb status"
    if "cmb log" in lowered or "log" in lowered:
        return "cmb log"
    if "cmb init" in lowered or "init" in lowered:
        return "cmb init"
    return ""


def _meaningful_items(values: list[str]) -> list[str]:
    items = []
    for value in values:
        normalized = value.strip()
        if normalized and normalized.lower() != "not set":
            items.append(normalized)
    return items
