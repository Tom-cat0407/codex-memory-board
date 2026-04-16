from typer.testing import CliRunner

from codex_memory_board.cli import app


runner = CliRunner()


def test_handoff_generates_stable_prompt(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    (tmp_path / "Documentation.md").write_text(
        """# Documentation

## Current Status

### Current Phase
Phase 4A

### Completed Items
- Implemented `cmb next`
- Added tests for `cmb next`

### Next Step
- Design and implement `cmb handoff`

### Latest Decision
- Decision: Keep handoff text stable
- Reason: Make it directly reusable in the next session

### Latest Verification
- Command: python -m pytest -q
- Result: 14 passed

## Log Entries
""",
        encoding="utf-8",
    )
    (tmp_path / "Plan.md").write_text(
        """# Plan

## Current Milestone
Phase 4A

## Milestones

### Phase 4A
- [ ] Implement `cmb handoff`
- [ ] Add tests for `cmb handoff`
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["handoff", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "你正在继续 Codex Memory Board 项目。" in result.output
    assert "当前阶段：" in result.output
    assert "- Phase 4A" in result.output
    assert "已完成事项：" in result.output
    assert "建议下一步：" in result.output
    assert "- Design and implement `cmb handoff`" in result.output
    assert "执行限制或边界：" in result.output
    assert "建议先阅读以下文件：" in result.output
    assert "src/codex_memory_board/handoff.py" in result.output


def test_handoff_uses_validate_file_when_next_step_targets_validate(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    (tmp_path / "Documentation.md").write_text(
        """# Documentation

## Current Status

### Current Phase
Phase 4B

### Completed Items
- Implemented `cmb handoff`

### Next Step
- Design and implement `cmb validate`

### Latest Decision
- Decision: Keep validate separate
- Reason: Do not mix validation with handoff generation

### Latest Verification
- Command: python -m pytest -q
- Result: 17 passed

## Log Entries
""",
        encoding="utf-8",
    )
    (tmp_path / "Plan.md").write_text(
        """# Plan

## Current Milestone
Phase 4B

## Milestones

### Phase 4B
- [ ] Implement `cmb validate`
- [ ] Add tests for `cmb validate`
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["handoff", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "src/codex_memory_board/validate.py" in result.output
    assert "只实现 `cmb validate`" in result.output


def test_handoff_errors_when_information_is_missing(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    (tmp_path / "Documentation.md").unlink()

    result = runner.invoke(app, ["handoff", "--path", str(tmp_path)])

    assert result.exit_code == 1
    assert "Documentation file not found" in result.output
