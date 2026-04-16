from typer.testing import CliRunner

from codex_memory_board.cli import app


runner = CliRunner()


def test_status_reports_not_set_for_fresh_documentation(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    result = runner.invoke(app, ["status", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Current Phase:" in result.output
    assert "- Not set" in result.output


def test_log_updates_status_output(tmp_path) -> None:
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    runner.invoke(
        app,
        [
            "log",
            "--path",
            str(tmp_path),
            "--item",
            "Implemented cmb status",
            "--decision",
            "Read Documentation.md only",
            "--reason",
            "Keep phase scope narrow",
            "--verify-command",
            "python -m pytest -q",
            "--verify-result",
            "9 passed",
        ],
    )

    result = runner.invoke(app, ["status", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Read Documentation.md only" in result.output
    assert "Result: 9 passed" in result.output
