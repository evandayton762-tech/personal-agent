"""Validators for data models.

These functions perform minimal structural validation on the models defined in models.py.
They raise ValueError on validation failure.
"""

from typing import List

from .models import Plan, Step, StepResult


ALLOWED_ADAPTER_TYPES: List[str] = [
    "web",
    "desktop",
    "files",
    "ocr",
    "secrets",
    "schedule",
    "budget",
    "finance",
    "docs",
]

ALLOWED_STATUSES: List[str] = ["ok", "retry", "blocked", "failed"]


def validate_step(step: Step) -> None:
    """Validate a Step object.

    Ensures required fields are present and the adapter type is allowed.
    Raises ValueError on invalid data.
    """
    if not step.step_id:
        raise ValueError("step_id is required")
    if not step.team:
        raise ValueError("team is required")
    if not isinstance(step.adapter, dict) or "type" not in step.adapter:
        raise ValueError("adapter with a 'type' field is required")
    adapter_type = step.adapter.get("type")
    if adapter_type not in ALLOWED_ADAPTER_TYPES:
        raise ValueError(f"Unknown adapter type: {adapter_type}")


def validate_plan(plan: Plan) -> None:
    """Validate a Plan object.

    Checks for a plan_id, gates list, and at least one step; validates each step.
    Raises ValueError on invalid data.
    """
    if not plan.plan_id:
        raise ValueError("plan_id is required")
    if not isinstance(plan.gates, list):
        raise ValueError("gates must be a list")
    if not isinstance(plan.steps, list) or len(plan.steps) == 0:
        raise ValueError("steps must be a non-empty list")
    for step in plan.steps:
        validate_step(step)


def validate_step_result(step_result: StepResult) -> None:
    """Validate a StepResult object.

    Ensures the step_id and status are present and valid.
    Raises ValueError on invalid data.
    """
    if not step_result.step_id:
        raise ValueError("step_id is required in StepResult")
    if step_result.status not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid status: {step_result.status}")