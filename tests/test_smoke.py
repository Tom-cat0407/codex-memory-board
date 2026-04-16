from typer.testing import CliRunner

from codex_memory_board import __version__
from codex_memory_board.cli import app


runner = CliRunner()


def test_package_exposes_version() -> None:
    assert __version__


def test_help_smoke() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Codex Memory Board" in result.output


def test_help_lists_init_command() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "init" in result.output
    assert "status" in result.output
    assert "log" in result.output
    assert "next" in result.output
    assert "handoff" in result.output
    assert "validate" in result.output
