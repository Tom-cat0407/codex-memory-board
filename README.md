# Codex Memory Board

Codex Memory Board is a local Python CLI for externalizing project state into Markdown files.
It is designed to help Codex and human collaborators keep long-running work stable across threads.

## Detailed guide

For the full onboarding guide, architecture explanation, file-by-file contract, and debugging instructions, see [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md).
For the visual diagrams only, see [docs/ARCHITECTURE_DIAGRAMS.md](docs/ARCHITECTURE_DIAGRAMS.md).
For a docs index with beginner and maintainer reading paths, see [docs/README.md](docs/README.md).

## Project scope

This repository is intentionally narrow in scope:

- Initialize project memory files
- Read current project status
- Infer the next actionable step from plan and state
- Append structured log entries
- Generate a handoff prompt for the next thread
- Validate whether the memory files are complete

This is not a general AI memory system.
It is a project-state externalization tool.

## Current status

The current implemented scope includes:

- Git repository initialization
- Python package layout with `src/`
- `cmb init` for project memory initialization
- `cmb status` for reading the current documentation state
- `cmb log` for appending structured log entries to `Documentation.md`
- `cmb next` for selecting the next task from `Documentation.md` and `Plan.md`
- `cmb handoff` for generating a ready-to-use Chinese handoff prompt
- `cmb validate` for checking whether the project memory is still in a workable state
- CLI and pytest coverage for the implemented commands

## Tech stack

- Python 3.11
- Typer
- Pydantic
- rich
- pytest

## Development environment requirements

- Target Python version: `3.11+`
- Recommended validation environment: a project-local Python `3.11+` virtual environment
- The exact Python interpreter used on each machine may differ
- Future feature development should be validated first in the project `.venv` or another Python `3.11+` environment
- The project requirement remains `>=3.11` in `pyproject.toml`

## Development

Recommended local environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install in editable mode inside `.venv`:

```bash
pip install -e .[dev]
```

Show CLI help:

```bash
cmb --help
python -m codex_memory_board --help
```

Run tests:

```bash
pytest
```

## Commands

### `cmb init`

Initialize the project memory files in the current directory:

```bash
cmb init
```

Initialize the files in another target directory:

```bash
cmb init --path path/to/project
```

The command creates these files when they do not already exist:

- `AGENTS.md`
- `Prompt.md`
- `Plan.md`
- `Implement.md`
- `Documentation.md`

If a file already exists, `cmb init` skips it by default and leaves the existing content unchanged.

### `cmb status`

Read the current project status from `Documentation.md`:

```bash
cmb status
```

Read status from another target directory:

```bash
cmb status --path path/to/project
```

The command prints:

- Current phase
- Completed items
- Next step
- Latest decision
- Latest verification

### `cmb log`

Append a structured log entry to `Documentation.md`:

```bash
cmb log --item "Implemented cmb log" --decision "Use fixed headings" --reason "Keep parsing simple" --verify-command "python -m pytest -q" --verify-result "8 passed"
```

The command appends a timestamped log entry and updates the latest decision and verification sections.

### `cmb next`

Choose the next recommended task using the fixed rules in `Documentation.md` and `Plan.md`:

```bash
cmb next
```

Read from another target directory:

```bash
cmb next --path path/to/project
```

The command prints:

- Current phase
- Basis
- Suggested next step

### `cmb handoff`

Generate a Chinese handoff prompt for the next Codex session:

```bash
cmb handoff
```

Read from another target directory:

```bash
cmb handoff --path path/to/project
```

The command prints a stable prompt containing:

- Current phase
- Completed items
- Suggested next step
- Execution constraints or boundaries
- Files to read first

### `cmb validate`

Validate the current repository memory state:

```bash
cmb validate
```

Validate another target directory:

```bash
cmb validate --path path/to/project
```

The command reports:

- Overall status as `PASS`, `WARN`, or `FAIL`
- File existence results
- Minimum structure checks
- Whether `status`, `log`, `next`, and `handoff` can continue to work
