# Architecture Diagrams

This file collects the main diagrams for `Codex Memory Board`.
Use it when you want a fast visual overview before reading the full guide.

## 1. Core Capability Loop

```mermaid
flowchart LR
    A["cmb init"] --> B["cmb status"]
    B --> C["cmb log"]
    C --> D["cmb next"]
    D --> E["cmb handoff"]
    E --> F["cmb validate"]
    F --> B
```

## 2. Runtime Architecture

```mermaid
flowchart TD
    A["User / Codex Session"] --> B["cli.py"]
    B --> C["Board Layer<br/>init_memory.py<br/>documentation_board.py<br/>next_board.py<br/>handoff_board.py<br/>validate_board.py"]
    C --> D["Parser Layer<br/>parser.py"]
    C --> E["Rule Layer<br/>next_step.py<br/>handoff.py<br/>validate.py"]
    C --> F["Store Layer<br/>store.py"]
    D --> G["Model Layer<br/>models.py"]
    E --> G
    F --> H["Markdown Files<br/>AGENTS.md<br/>Prompt.md<br/>Plan.md<br/>Implement.md<br/>Documentation.md"]
```

## 3. File Contract Map

```mermaid
flowchart LR
    A["AGENTS.md"] --> X["Collaboration rules"]
    B["Prompt.md"] --> Y["Prompt fragments and handoff wording"]
    C["Plan.md"] --> Z["Milestones and deliverables"]
    D["Implement.md"] --> P["Current coding focus"]
    E["Documentation.md"] --> Q["Runtime status board"]
```

## 4. `cmb next` Decision Flow

```mermaid
flowchart TD
    A["Read Documentation.md and Plan.md"] --> B{"Documentation.md Next Step set?"}
    B -->|Yes| C["Use Documentation.md Next Step"]
    B -->|No| D{"Latest verification failed?"}
    D -->|Yes| E["Suggest: fix verification failure first"]
    D -->|No| F{"Current milestone has incomplete tasks?"}
    F -->|Yes| G["Pick first incomplete task"]
    F -->|No| H{"Next milestone exists?"}
    H -->|Yes| I["Pick first task in next milestone"]
    H -->|No| J["Report insufficient information"]
```

## 5. `cmb handoff` Generation Flow

```mermaid
flowchart TD
    A["Read Documentation.md"] --> B["Read Plan.md"]
    B --> C["Reuse cmb next rules"]
    C --> D["Collect current phase"]
    C --> E["Collect suggested next step"]
    A --> F["Collect completed items"]
    A --> G["Collect latest decision and verification"]
    D --> H["handoff.py builds stable Chinese prompt"]
    E --> H
    F --> H
    G --> H
```

## 6. `cmb validate` Checking Flow

```mermaid
flowchart TD
    A["Read five core Markdown files"] --> B{"Files exist?"}
    B -->|No| C["FAIL"]
    B -->|Yes| D{"Required headings exist?"}
    D -->|No| E["FAIL"]
    D -->|Yes| F{"Documentation and Plan are parseable?"}
    F -->|No| G["FAIL"]
    F -->|Yes| H{"Weak but workable state?"}
    H -->|Yes| I["WARN"]
    H -->|No| J["PASS"]
```

## 7. Recommended Reading Order

```mermaid
flowchart LR
    A["README.md"] --> B["docs/PROJECT_GUIDE.md"]
    B --> C["Documentation.md"]
    C --> D["Plan.md"]
    D --> E["AGENTS.md"]
    E --> F["src/codex_memory_board/cli.py"]
    F --> G["parser.py / board modules / rule modules"]
    G --> H["tests/"]
```

## 8. Adopting This Tool In Another Project

```mermaid
flowchart TD
    A["Run cmb init --path <your-project>"] --> B["Fill AGENTS.md"]
    B --> C["Fill Plan.md"]
    C --> D["Fill Documentation.md"]
    D --> E["Run cmb status"]
    E --> F["Run cmb next"]
    F --> G["Use cmb log during development"]
    G --> H["Use cmb handoff when switching sessions"]
    H --> I["Use cmb validate to confirm state quality"]
```
