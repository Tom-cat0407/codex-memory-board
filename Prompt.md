# Prompt

## How To Use This File

- Use this file to store prompt fragments that can be reused in later sessions.
- Keep the reusable handoff template stable.
- Update the active prompt context when the task changes.
- Prefer concise, actionable prompt text over long historical summaries.

## Purpose

This file captures prompt fragments and handoff context that help the next Codex thread continue work without rebuilding project context from scratch.

## Current prompt baseline

- Project name: Codex Memory Board
- CLI entry: `cmb`
- Goal: externalize project state into Markdown files
- Current phase: Phase 1

## Handoff prompt template

Use the structure below when handing work to the next thread:

```text
You are continuing work on Codex Memory Board.

Current phase:
- <phase>

What is already done:
- <completed item>

What should happen next:
- <next step>

Constraints:
- <constraint>
```

## Notes

- Keep prompts concrete
- Prefer current state over historical narration
