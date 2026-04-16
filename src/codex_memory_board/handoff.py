"""Handoff prompt text generation."""

from .models import HandoffPromptData


def build_handoff_prompt(data: HandoffPromptData) -> str:
    """Build a stable Chinese handoff prompt for the next session."""
    lines = [
        "你正在继续 Codex Memory Board 项目。",
        "",
        "当前阶段：",
        f"- {data.current_phase}",
        "",
        "已完成事项：",
    ]
    lines.extend(_format_list(data.completed_items))
    lines.extend(
        [
            "",
            "建议下一步：",
            f"- {data.suggested_next_step}",
            "",
            "执行限制或边界：",
        ]
    )
    lines.extend(_format_list(data.constraints))
    lines.extend(
        [
            "",
            "建议先阅读以下文件：",
        ]
    )
    lines.extend(_format_list(data.files_to_read))
    lines.extend(
        [
            "",
            "补充上下文：",
            f"- 最近一次决策：{_or_not_set(data.latest_decision)}",
            f"- 最近一次验证：{_or_not_set(data.latest_verification_result)}",
        ]
    )
    return "\n".join(lines)


def _format_list(values: list[str]) -> list[str]:
    if not values:
        return ["- Not set"]
    return [f"- {value}" for value in values]


def _or_not_set(value: str) -> str:
    return value if value else "Not set"

