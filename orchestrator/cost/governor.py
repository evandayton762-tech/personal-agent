"""Cost governor and plan estimation utilities.

This module estimates token usage for plans and steps, checks against
configured caps, and downsizes plans when necessary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List, Tuple
from datetime import datetime

from ..core.models import Plan, Step


DEFAULT_STEP_TOKENS: Dict[str, int] = {
    # Rough conservative token estimates per adapter type
    "web": 300,
    "desktop": 250,
    "files": 100,
    "ocr": 200,
    "secrets": 50,
    "schedule": 50,
    "budget": 50,
    "finance": 400,
    "docs": 150,
}


@dataclass
class PlanEstimate:
    total_tokens: int
    step_tokens: Dict[str, int]


def estimate_step_tokens(step: Step) -> int:
    """Estimate tokens for a single step based on adapter type."""
    adapter_type = step.adapter.get("type") if isinstance(step.adapter, dict) else None
    return DEFAULT_STEP_TOKENS.get(adapter_type, 300)


def estimate_plan(plan: Plan) -> PlanEstimate:
    """Return token estimate for an entire plan."""
    totals = {}
    total = 0
    for step in plan.steps:
        est = estimate_step_tokens(step)
        totals[step.step_id] = est
        total += est
    return PlanEstimate(total_tokens=total, step_tokens=totals)


def downscope_plan(plan: Plan, token_cap: int) -> Plan:
    """Downscope a plan to fit within the per-task token cap.

    Steps beyond the cap are removed. At least one step remains.
    """
    est = estimate_plan(plan)
    running_total = 0
    new_steps: List[Step] = []
    for step in plan.steps:
        step_tokens = est.step_tokens.get(step.step_id, 0)
        if running_total + step_tokens > token_cap:
            break
        new_steps.append(step)
        running_total += step_tokens
    if not new_steps:
        # Always keep at least one step to avoid empty plan
        new_steps.append(plan.steps[0])
    return Plan(plan_id=plan.plan_id, gates=plan.gates, steps=new_steps)