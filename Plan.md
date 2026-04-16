# Plan

## How To Use This File

- Keep `## Current Milestone` aligned with the milestone that is actively in progress.
- Define milestones under `## Milestones` using `### <Milestone Name>`.
- Write deliverables as checklist items using `- [ ]` or `- [x]`.
- Keep milestone names stable, because `cmb next` depends on them.
- Keep tasks concrete enough that the “first incomplete item” is actionable.

## Current Milestone
Phase 5

## Milestones

### Phase 1
- [x] Initialize repository
- [x] Create package skeleton
- [x] Create root Markdown templates
- [x] Add minimal CLI entrypoint
- [x] Add smoke-level tests

### Phase 2
- [x] Implement `cmb init`
- [x] Add tests for `cmb init`

### Phase 3A
- [x] Implement `cmb status`
- [x] Implement `cmb log`
- [x] Add tests for `cmb status` and `cmb log`

### Phase 3B
- [x] Implement `cmb next`
- [x] Add tests for `cmb next`

### Phase 4A
- [x] Implement `cmb handoff`
- [x] Add tests for `cmb handoff`

### Phase 4B
- [x] Implement `cmb validate`
- [x] Add tests for `cmb validate`

### Phase 5
- [x] Confirm all six core commands are implemented
- [x] Verify the repository can validate its own working state

### Maintenance
- [ ] Review and refine the six core commands
- [ ] Keep documentation and tests aligned with current behavior
