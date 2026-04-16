from typer.testing import CliRunner

from codex_memory_board.cli import app
from codex_memory_board.paths import MEMORY_BOARD_FILES


runner = CliRunner()


def test_init_creates_memory_files(tmp_path) -> None:
    result = runner.invoke(app, ["init", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "Initialized project memory" in result.output
    for filename in MEMORY_BOARD_FILES:
        assert (tmp_path / filename).exists()


def test_init_does_not_overwrite_existing_files(tmp_path) -> None:
    agents_file = tmp_path / "AGENTS.md"
    agents_file.write_text("custom agents content", encoding="utf-8")

    result = runner.invoke(app, ["init", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert agents_file.read_text(encoding="utf-8") == "custom agents content"
    assert "skipped AGENTS.md" in result.output
    assert (tmp_path / "Documentation.md").exists()


def test_status_reads_documentation_fields(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    documentation = tmp_path / "Documentation.md"
    documentation.write_text(
        """# Documentation

## Current Status

### Current Phase
Phase 3A

### Completed Items
- Added `cmb init`
- Added tests

### Next Step
- Implement `cmb status`

### Latest Decision
- Decision: Use heading-driven parsing
- Reason: Keep the file stable

### Latest Verification
- Command: python -m pytest -q
- Result: 7 passed

## Log Entries
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["status", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Phase 3A" in result.output
    assert "Added `cmb init`" in result.output
    assert "Implement `cmb status`" in result.output
    assert "Use heading-driven parsing" in result.output
    assert "7 passed" in result.output


def test_log_appends_entry_and_updates_latest_sections(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    result = runner.invoke(
        app,
        [
            "log",
            "--path",
            str(tmp_path),
            "--item",
            "Implemented cmb log",
            "--decision",
            "Keep Documentation.md section-driven",
            "--reason",
            "Avoid complex parsing",
            "--verify-command",
            "python -m pytest -q",
            "--verify-result",
            "8 passed",
        ],
    )

    documentation_text = (tmp_path / "Documentation.md").read_text(encoding="utf-8")

    assert result.exit_code == 0
    assert "Appended log entry" in result.output
    assert "- Decision: Keep Documentation.md section-driven" in documentation_text
    assert "- Reason: Avoid complex parsing" in documentation_text
    assert "- Command: python -m pytest -q" in documentation_text
    assert "- Result: 8 passed" in documentation_text
    assert "- Item: Implemented cmb log" in documentation_text
    assert "- Verification Result: 8 passed" in documentation_text
