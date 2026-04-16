"""Typer application entrypoint."""

from pathlib import Path

import typer

from .console import (
    print_error,
    print_info,
    print_section,
    print_success,
    print_validation_report,
    print_warning,
)
from .documentation_board import append_documentation_log, read_documentation_status
from .handoff_board import build_handoff_text
from .init_memory import initialize_memory_board
from .models import DocumentationLogInput
from .next_board import build_next_recommendation
from .validate_board import build_validation_report


app = typer.Typer(
    name="cmb",
    help="Codex Memory Board helps externalize project state into Markdown files.",
    no_args_is_help=True,
    add_completion=False,
)


@app.callback()
def main() -> None:
    """Codex Memory Board CLI."""


@app.command("init")
def init_command(
    path: Path = typer.Option(
        Path("."),
        "--path",
        help="Target directory for initializing project memory files.",
        file_okay=False,
        dir_okay=True,
        writable=True,
    ),
) -> None:
    """Create the default project memory files."""
    result = initialize_memory_board(path)
    print_info(f"Initialized project memory in: {result.root}")
    for file_result in result.files:
        if file_result.action == "created":
            print_success(f"created {file_result.filename}")
        else:
            print_warning(f"skipped {file_result.filename} (already exists)")


@app.command("status")
def status_command(
    path: Path = typer.Option(
        Path("."),
        "--path",
        help="Target directory containing Documentation.md.",
        file_okay=False,
        dir_okay=True,
        writable=True,
    ),
) -> None:
    """Read and summarize the current Documentation.md status."""
    try:
        status = read_documentation_status(path)
    except (FileNotFoundError, ValueError) as exc:
        print_error(str(exc))
        raise typer.Exit(code=1)

    print_section("Current Phase", [status.current_phase] if status.current_phase else [])
    print_section("Completed Items", status.completed_items)
    print_section("Next Step", status.next_steps)

    decision_lines: list[str] = []
    if status.latest_decision:
        decision_lines.append(status.latest_decision)
    if status.latest_decision_reason:
        decision_lines.append(f"Reason: {status.latest_decision_reason}")
    print_section("Latest Decision", decision_lines)

    verification_lines: list[str] = []
    if status.latest_verification_command:
        verification_lines.append(f"Command: {status.latest_verification_command}")
    if status.latest_verification_result:
        verification_lines.append(f"Result: {status.latest_verification_result}")
    print_section("Latest Verification", verification_lines)


@app.command("log")
def log_command(
    item: str = typer.Option(..., "--item", help="Short summary of the work item."),
    decision: str = typer.Option(..., "--decision", help="The decision that was made."),
    reason: str = typer.Option(..., "--reason", help="Why the decision was made."),
    verify_command: str = typer.Option(
        ...,
        "--verify-command",
        help="The command used to verify the change.",
    ),
    verify_result: str = typer.Option(
        ...,
        "--verify-result",
        help="The result produced by the verification command.",
    ),
    path: Path = typer.Option(
        Path("."),
        "--path",
        help="Target directory containing Documentation.md.",
        file_okay=False,
        dir_okay=True,
        writable=True,
    ),
) -> None:
    """Append a structured log entry to Documentation.md."""
    payload = DocumentationLogInput(
        item=item,
        decision=decision,
        reason=reason,
        verification_command=verify_command,
        verification_result=verify_result,
    )

    try:
        entry = append_documentation_log(path, payload)
    except (FileNotFoundError, ValueError) as exc:
        print_error(str(exc))
        raise typer.Exit(code=1)

    print_success(f"Appended log entry to Documentation.md in: {Path(path).resolve()}")
    print_info(f"Timestamp: {entry.timestamp}")


@app.command("next")
def next_command(
    path: Path = typer.Option(
        Path("."),
        "--path",
        help="Target directory containing Documentation.md and Plan.md.",
        file_okay=False,
        dir_okay=True,
        writable=True,
    ),
) -> None:
    """Choose the next step using Documentation.md and Plan.md."""
    try:
        recommendation = build_next_recommendation(path)
    except (FileNotFoundError, ValueError) as exc:
        print_error(str(exc))
        raise typer.Exit(code=1)

    print_section("Current Phase", [recommendation.current_phase])
    print_section("Basis", [recommendation.basis])
    print_section("Suggested Next Step", [recommendation.suggested_next_step])


@app.command("handoff")
def handoff_command(
    path: Path = typer.Option(
        Path("."),
        "--path",
        help="Target directory containing Documentation.md and Plan.md.",
        file_okay=False,
        dir_okay=True,
        writable=True,
    ),
) -> None:
    """Build a stable handoff prompt for the next Codex session."""
    try:
        handoff_text = build_handoff_text(path)
    except (FileNotFoundError, ValueError) as exc:
        print_error(str(exc))
        raise typer.Exit(code=1)

    print_info(handoff_text)


@app.command("validate")
def validate_command(
    path: Path = typer.Option(
        Path("."),
        "--path",
        help="Target directory containing the core Markdown memory files.",
        file_okay=False,
        dir_okay=True,
        writable=True,
    ),
) -> None:
    """Validate whether the project memory files can still support continued work."""
    report = build_validation_report(path)
    print_validation_report(report)
    if report.overall_status == "FAIL":
        raise typer.Exit(code=1)


def run() -> None:
    """Run the CLI with a stable program name."""
    app(prog_name="cmb")
