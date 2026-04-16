"""Markdown templates used by the project."""

from .paths import (
    AGENTS_FILE,
    DOCUMENTATION_FILE,
    IMPLEMENT_FILE,
    PLAN_FILE,
    PROMPT_FILE,
)


AGENTS_TEMPLATE = """# AGENTS

## How To Use This File

- Use this file to define collaboration rules for this repository.
- Keep the section headings stable so future contributors can find the rules quickly.
- Replace the placeholder bullets below with project-specific content.
- Prefer short, explicit rules over long narrative text.

## Purpose

Use this file to capture how Codex and human collaborators should work in this repository.

## Project Summary

- Project:
- Goal:
- Current phase:

## Working Rules

- Work in small, explicit phases
- Keep changes scoped to the current task
- Update project memory files when plans or status change
- Prefer concrete next steps over vague notes

## Constraints

- Record important boundaries here
- Note any tooling, runtime, or delivery constraints here

## Handoff Notes

- Last completed step:
- Recommended next step:
"""


PROMPT_TEMPLATE = """# Prompt

## How To Use This File

- Use this file to store prompt fragments that can be reused in later sessions.
- Keep the reusable handoff template stable.
- Update the active prompt context when the current task changes.
- Replace the placeholder bullets below with project-specific details.

## Purpose

Use this file to store prompt fragments and handoff-ready instructions for the next Codex thread.

## Active Prompt Context

- Current task:
- Desired outcome:
- Constraints:

## Reusable Handoff Template

```text
You are continuing work on this repository.

Current goal:
- <goal>

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
"""


PLAN_TEMPLATE = """# Plan

## How To Use This File

- Keep `## Current Milestone` aligned with the milestone that is actively in progress.
- Define milestones under `## Milestones` using `### <Milestone Name>`.
- Write deliverables as checklist items using `- [ ]` or `- [x]`.
- Keep milestone names stable, because `cmb next` depends on them.
- Keep tasks concrete enough that the “first incomplete item” is actionable.

## Current Milestone
Phase 1

## Milestones

### Phase 1
- [ ] Initialize repository memory files
- [ ] Confirm the initial project structure

### Phase 2
- [ ] Add the next planned deliverable
"""


IMPLEMENT_TEMPLATE = """# Implement

## How To Use This File

- Use this file for short-lived implementation context.
- Update it when the current coding focus changes.
- Keep the verification section concrete and runnable.
- Replace the placeholder bullets below with current implementation details.

## Current Focus

- Describe the implementation task in progress

## Decisions

- Date:
- Decision:
- Reason:

## Files Likely To Change

- List the files that are expected to change

## Verification

- Command:
- Result:
"""


DOCUMENTATION_TEMPLATE = """# Documentation

## How To Use This File

- This is the main runtime status board for the project.
- Keep the headings below unchanged, because multiple commands parse them directly.
- `Current Phase` should name the actual current phase or milestone.
- `Completed Items` should list work that is truly done.
- `Next Step` should list the clearest immediate next action, or stay as `Not set`.
- `Latest Decision` and `Latest Verification` should always reflect the newest meaningful update.
- `Log Entries` should contain timestamped historical records.

## Current Status

### Current Phase
Not set

### Completed Items
- Not set

### Next Step
- Not set

### Latest Decision
- Decision: Not set
- Reason: Not set

### Latest Verification
- Command: Not set
- Result: Not set

## Log Entries
"""


def get_init_templates() -> dict[str, str]:
    """Return the default templates for cmb init."""
    return {
        AGENTS_FILE: AGENTS_TEMPLATE,
        PROMPT_FILE: PROMPT_TEMPLATE,
        PLAN_FILE: PLAN_TEMPLATE,
        IMPLEMENT_FILE: IMPLEMENT_TEMPLATE,
        DOCUMENTATION_FILE: DOCUMENTATION_TEMPLATE,
    }


DEFAULT_MEMORY_TEMPLATE = """# Project Memory

## Goal

-

## Current Status

-

## Next Steps

-

## Log

- <date>: <note>
"""


DEFAULT_LOG_ENTRY_TEMPLATE = """## Log Entry

- Date:
- Summary:
- Impact:
"""
