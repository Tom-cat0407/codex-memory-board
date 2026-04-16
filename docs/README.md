# Docs

This directory is the long-form documentation hub for `Codex Memory Board`.

## If You Are New

Read in this order:

1. [Project Guide](./PROJECT_GUIDE.md)
2. [Architecture Diagrams](./ARCHITECTURE_DIAGRAMS.md)
3. Root-level [Documentation.md](../Documentation.md), [Plan.md](../Plan.md), and [AGENTS.md](../AGENTS.md)

Use this path if you want to understand what the project does, what each file means, and how to use it in your own repository.

## If You Maintain Or Extend The Tool

Read in this order:

1. [Architecture Diagrams](./ARCHITECTURE_DIAGRAMS.md)
2. [Project Guide](./PROJECT_GUIDE.md)
3. [cli.py](../src/codex_memory_board/cli.py)
4. `parser.py`, the `*_board.py` modules, and the rule modules under `src/codex_memory_board/`
5. The tests under [tests/](../tests/)

Use this path if you want to debug behavior, extend commands, or verify that the architecture boundaries still hold.

## Document Map

- [Chinese User Manual (DOCX)](./Codex-Memory-Board-User-Manual-ZH.docx): detailed Chinese Word manual with Chinese diagrams
- [Project Guide](./PROJECT_GUIDE.md): full onboarding guide, file contracts, architecture explanation, and debugging advice
- [Architecture Diagrams](./ARCHITECTURE_DIAGRAMS.md): Mermaid diagrams for command flow, layering, validation, and adoption
