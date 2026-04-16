"""Shared data models for the application."""

from typing import List, Literal

from pydantic import BaseModel, Field


class PlanItem(BaseModel):
    """A minimal plan item model."""

    title: str
    status: str = "pending"
    notes: str = ""


class ProjectStatus(BaseModel):
    """A minimal project status snapshot."""

    project_name: str = "Codex Memory Board"
    objective: str = ""
    current_focus: str = ""
    next_steps: List[str] = Field(default_factory=list)


class ValidationReport(BaseModel):
    """A minimal validation result model."""

    is_valid: bool = True
    missing_sections: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class DocumentationLogInput(BaseModel):
    """Input payload for appending a Documentation.md log entry."""

    item: str
    decision: str
    reason: str
    verification_command: str
    verification_result: str


class DocumentationLogEntry(DocumentationLogInput):
    """A structured log entry stored in Documentation.md."""

    timestamp: str


class DocumentationStatus(BaseModel):
    """Structured view of Documentation.md for the status command."""

    current_phase: str = ""
    completed_items: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)
    latest_decision: str = ""
    latest_decision_reason: str = ""
    latest_verification_command: str = ""
    latest_verification_result: str = ""
    log_entries: List[DocumentationLogEntry] = Field(default_factory=list)


class PlanTask(BaseModel):
    """A single deliverable in a milestone."""

    title: str
    completed: bool = False


class PlanMilestone(BaseModel):
    """An ordered milestone with deliverables."""

    title: str
    tasks: List[PlanTask] = Field(default_factory=list)


class PlanDocument(BaseModel):
    """Structured view of Plan.md for next-step selection."""

    current_milestone: str = ""
    milestones: List[PlanMilestone] = Field(default_factory=list)


class NextStepRecommendation(BaseModel):
    """The stable output for cmb next."""

    current_phase: str
    basis: str
    suggested_next_step: str


class HandoffPromptData(BaseModel):
    """Structured input for building a handoff prompt."""

    current_phase: str
    completed_items: List[str] = Field(default_factory=list)
    suggested_next_step: str
    constraints: List[str] = Field(default_factory=list)
    files_to_read: List[str] = Field(default_factory=list)
    latest_decision: str = ""
    latest_verification_result: str = ""


ValidationLevel = Literal["PASS", "WARN", "FAIL"]


class ValidationFinding(BaseModel):
    """A single validation finding."""

    level: ValidationLevel
    target: str
    message: str


class MemoryValidationReport(BaseModel):
    """Structured validation output for cmb validate."""

    overall_status: ValidationLevel
    findings: List[ValidationFinding] = Field(default_factory=list)
    pass_count: int = 0
    warn_count: int = 0
    fail_count: int = 0
