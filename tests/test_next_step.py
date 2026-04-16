from typer.testing import CliRunner

from codex_memory_board.cli import app


runner = CliRunner()


def test_next_prefers_documentation_next_step(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    (tmp_path / "Documentation.md").write_text(
        """# Documentation

## Current Status

### Current Phase
Phase 3B

### Completed Items
- Implemented `cmb status`

### Next Step
- Design and implement `cmb handoff`

### Latest Decision
- Decision: Keep next rule-driven
- Reason: Avoid complex inference

### Latest Verification
- Command: python -m pytest -q
- Result: 9 passed

## Log Entries
""",
        encoding="utf-8",
    )
    (tmp_path / "Plan.md").write_text(
        """# Plan

## Current Milestone
Phase 3B

## Milestones

### Phase 3B
- [ ] Implement `cmb next`

### Phase 4
- [ ] Implement `cmb handoff`
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["next", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Documentation.md Next Step" in result.output
    assert "Design and implement `cmb handoff`" in result.output


def test_next_prioritizes_failed_verification_when_next_step_is_empty(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    (tmp_path / "Documentation.md").write_text(
        """# Documentation

## Current Status

### Current Phase
Phase 3B

### Completed Items
- Implemented `cmb log`

### Next Step
- Not set

### Latest Decision
- Decision: Keep verification visible
- Reason: Failures should block progress

### Latest Verification
- Command: python -m pytest -q
- Result: 1 failed, 8 passed

## Log Entries
""",
        encoding="utf-8",
    )
    (tmp_path / "Plan.md").write_text(
        """# Plan

## Current Milestone
Phase 3B

## Milestones

### Phase 3B
- [ ] Implement `cmb next`
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["next", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Latest verification result indicates failure" in result.output
    assert "先修复验证失败" in result.output


def test_next_uses_first_incomplete_task_in_current_milestone(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    (tmp_path / "Documentation.md").write_text(
        """# Documentation

## Current Status

### Current Phase
Phase 3B

### Completed Items
- Implemented `cmb log`

### Next Step
- Not set

### Latest Decision
- Decision: Keep milestone-based fallback
- Reason: Plans should remain actionable

### Latest Verification
- Command: python -m pytest -q
- Result: 9 passed

## Log Entries
""",
        encoding="utf-8",
    )
    (tmp_path / "Plan.md").write_text(
        """# Plan

## Current Milestone
Phase 3B

## Milestones

### Phase 3A
- [x] Implement `cmb status`

### Phase 3B
- [ ] Implement `cmb next`
- [ ] Add tests for `cmb next`

### Phase 4
- [ ] Implement `cmb handoff`
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["next", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "First incomplete deliverable in current milestone 'Phase 3B'" in result.output
    assert "Implement `cmb next`" in result.output


def test_next_uses_first_task_in_next_milestone_when_current_is_complete(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    (tmp_path / "Documentation.md").write_text(
        """# Documentation

## Current Status

### Current Phase
Phase 3B

### Completed Items
- Implemented `cmb next`

### Next Step
- Not set

### Latest Decision
- Decision: Move to the next milestone only after completion
- Reason: Keep the rule order explicit

### Latest Verification
- Command: python -m pytest -q
- Result: 10 passed

## Log Entries
""",
        encoding="utf-8",
    )
    (tmp_path / "Plan.md").write_text(
        """# Plan

## Current Milestone
Phase 3B

## Milestones

### Phase 3A
- [x] Implement `cmb status`

### Phase 3B
- [x] Implement `cmb next`
- [x] Add tests for `cmb next`

### Phase 4
- [ ] Implement `cmb handoff`
- [ ] Add tests for `cmb handoff`
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["next", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Current milestone complete; first task in next milestone 'Phase 4'" in result.output
    assert "Implement `cmb handoff`" in result.output


def test_next_errors_when_current_milestone_is_missing(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    (tmp_path / "Documentation.md").write_text(
        """# Documentation

## Current Status

### Current Phase
Phase 3B

### Completed Items
- Implemented `cmb next`

### Next Step
- Not set

### Latest Decision
- Decision: Keep errors explicit
- Reason: Do not guess missing plan state

### Latest Verification
- Command: python -m pytest -q
- Result: 10 passed

## Log Entries
""",
        encoding="utf-8",
    )
    (tmp_path / "Plan.md").write_text(
        """# Plan

## Current Milestone
Phase Unknown

## Milestones

### Phase 3B
- [x] Implement `cmb next`
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["next", "--path", str(tmp_path)])

    assert result.exit_code == 1
    assert "Insufficient information" in result.output
