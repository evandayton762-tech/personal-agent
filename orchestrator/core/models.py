"""Data models for the personal agent.

These dataclasses mirror the schemas defined in `/docs/spec_task_envelope.md`. They provide
simple containers for task specifications, plans, steps, results, and parked items.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class ProjectSpec:
    goal: str
    domains: List[str]
    constraints: Dict[str, Any] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Step:
    step_id: str
    team: str
    intent: str
    adapter: Dict[str, Any]
    args: Dict[str, Any] = field(default_factory=dict)
    needs_secrets: List[str] = field(default_factory=list)
    evidence: List[Any] = field(default_factory=list)
    budget_tokens: Optional[int] = None
    requires_human: bool = False


@dataclass
class Plan:
    plan_id: str
    gates: List[str]
    steps: List[Step]


@dataclass
class StepResult:
    step_id: str
    status: str  # ok|retry|blocked|failed
    evidence: Dict[str, Any] = field(default_factory=dict)
    cost: Dict[str, Any] = field(default_factory=dict)
    notes: Optional[str] = None


@dataclass
class ParkedItem:
    reason: str
    proposed_free_alt: Optional[str] = None
    requested_info: List[str] = field(default_factory=list)
    next_try: Optional[str] = None