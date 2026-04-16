# Implement

## How To Use This File

- Use this file for short-lived implementation context.
- Update it when the current coding focus changes.
- Keep verification entries concrete and runnable.
- Prefer active implementation details over long historical notes.

## Implementation principles

- Favor small modules with clear responsibilities
- Keep the CLI thin
- Keep storage logic separate from business rules
- Treat Markdown as a stable interface, not a side detail

## Current module boundaries

- `cli.py`: CLI entrypoint and command registration
- `paths.py`: repository and file path helpers
- `models.py`: shared Pydantic models
- `templates.py`: Markdown template strings
- `parser.py`: future Markdown parsing layer
- `store.py`: file read/write only
- `next_step.py`: future next-step inference
- `handoff.py`: future handoff prompt generation
- `validate.py`: future memory validation
- `console.py`: minimal output helpers

## Phase 1 rule

Placeholder modules may define stubs, but should not contain real business logic yet.
