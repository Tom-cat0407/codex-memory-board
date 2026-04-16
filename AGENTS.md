# AGENTS

## How To Use This File

- Use this file to define collaboration rules for this repository.
- Keep the section headings stable so future contributors can find the rules quickly.
- Replace the bullets below when the project workflow changes.
- Prefer short, explicit rules over long narrative text.

## Purpose

This repository builds a local CLI that externalizes Codex project memory into Markdown files.
The tool should keep long tasks resumable across threads with minimal ceremony.

## Phase guardrails

- Build the project in phases
- Keep the implementation intentionally small
- Do not introduce speculative abstractions early
- Prefer explicit Markdown structure over complex parsing systems
- Keep file names and CLI verbs clear

## Current boundaries

- Phase 1 only sets up repository structure and minimal runnable scaffolding
- `store.py` is limited to file read/write helpers
- `next_step.py`, `handoff.py`, and `validate.py` are placeholders only for now
- `console.py` should stay minimal and focused on plain output helpers

## Collaboration notes

- CLI entry name is `cmb`
- Package import root is `codex_memory_board`
- Preserve the `src/` layout
- Add tests as behavior appears, not before

## Done definition for this phase

- Repository files exist with minimal useful content
- `python -m codex_memory_board --help` works
- At least one smoke-level test can pass
