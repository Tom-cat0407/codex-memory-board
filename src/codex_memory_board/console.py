"""Minimal rich console helpers."""

from rich.console import Console

from .models import MemoryValidationReport


console = Console()


def print_info(message: str) -> None:
    """Print a regular informational message."""
    console.print(message)


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[green]{message}[/green]")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[yellow]{message}[/yellow]")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[red]{message}[/red]")


def print_section(title: str, lines: list[str]) -> None:
    """Print a simple titled section with bullet lines."""
    console.print(f"{title}:")
    if not lines:
        console.print("- Not set")
        return
    for line in lines:
        console.print(f"- {line}")


def print_validation_report(report: MemoryValidationReport) -> None:
    """Print a stable validation summary."""
    print_section("Overall Status", [report.overall_status])
    print_section(
        "Counts",
        [
            f"PASS: {report.pass_count}",
            f"WARN: {report.warn_count}",
            f"FAIL: {report.fail_count}",
        ],
    )
    console.print("Findings:")
    for finding in report.findings:
        console.print(
            f"- {finding.level} [{finding.target}] {finding.message}",
            markup=False,
            soft_wrap=True,
        )
