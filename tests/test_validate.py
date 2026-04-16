from typer.testing import CliRunner

from codex_memory_board.cli import app


runner = CliRunner()


def test_validate_reports_pass_for_complete_state(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    (tmp_path / "Documentation.md").write_text(
        """# Documentation

## Current Status

### Current Phase
Phase 5

### Completed Items
- Implemented `cmb handoff`
- Implemented `cmb validate`

### Next Step
- Review and refine the six core commands

### Latest Decision
- Decision: Keep validate read-only
- Reason: Do not mix checking with repair

### Latest Verification
- Command: python -m pytest -q
- Result: 17 passed

## Log Entries

### 2026-04-15 16:30:00
- Item: Implemented `cmb handoff`
- Decision: Keep handoff generation read-only
- Reason: Avoid mixing prompt generation with validation
- Verification Command: python -m pytest -q
- Verification Result: 17 passed
""",
        encoding="utf-8",
    )
    (tmp_path / "Plan.md").write_text(
        """# Plan

## Current Milestone
Phase 5

## Milestones

### Phase 4B
- [x] Implement `cmb validate`
- [x] Add tests for `cmb validate`

### Phase 5
- [x] Confirm all six core commands are implemented
- [x] Verify the project can validate its own working state

### Maintenance
- [ ] Review and refine the six core commands
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["validate", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Overall Status:" in result.output
    assert "- PASS" in result.output
    assert "FAIL: 0" in result.output
    assert "PASS [cmb next]" in result.output
    assert "PASS [cmb handoff]" in result.output


def test_validate_reports_warn_for_weak_but_workable_state(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    (tmp_path / "Documentation.md").write_text(
        """# Documentation

## Current Status

### Current Phase
Phase 5

### Completed Items
- Implemented `cmb validate`

### Next Step
- Not set

### Latest Decision
- Decision: Not set
- Reason: Not set

### Latest Verification
- Command: python -m pytest -q
- Result: Not set

## Log Entries
""",
        encoding="utf-8",
    )
    (tmp_path / "Plan.md").write_text(
        """# Plan

## Current Milestone
Phase 5

## Milestones

### Phase 5
- [ ] Review and refine the six core commands

### Maintenance
- [ ] Keep documentation and tests aligned with current behavior
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["validate", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Overall Status:" in result.output
    assert "- WARN" in result.output
    assert "WARN [Documentation.md] Latest Decision exists but is not meaningfully set." in result.output
    assert "WARN [Documentation.md] Latest Verification exists but its result is not meaningfully set." in result.output
    assert "PASS [cmb next]" in result.output


def test_validate_reports_fail_for_missing_core_file(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    (tmp_path / "Documentation.md").unlink()

    result = runner.invoke(app, ["validate", "--path", str(tmp_path)])

    assert result.exit_code == 1
    assert "Overall Status:" in result.output
    assert "- FAIL" in result.output
    assert "FAIL [Documentation.md] Required file is missing." in result.output
