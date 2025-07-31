"""Simple planner that produces structured JSON plans.

This planner takes a project specification and returns a Plan object
conforming to the schema defined in /docs/spec_task_envelope.md. It
does not call an external LLM; instead, it uses heuristics based on
domains to construct a minimal viable plan. If the estimated tokens
exceed the per‑task cap, it downsizes the plan using the cost governor.
"""

from __future__ import annotations

import itertools
from typing import Dict, Any, List

from .core.models import Plan, Step
from .core.validators import validate_plan
from .cost.governor import estimate_plan, downscope_plan, estimate_step_tokens


# Default per‑task token cap; could be loaded from config
PER_TASK_TOKEN_CAP = 8000


def _generate_step_id(base: str, counter: itertools.count) -> str:
    return f"{base}-{next(counter)}"


def plan_project(project_spec: Dict[str, Any]) -> Plan:
    """Generate a Plan for the given project specification.

    Args:
        project_spec: Dictionary describing the goal, domains, constraints, parameters.

    Returns:
        A Plan dataclass instance representing the tasks to perform.
    """
    domains: List[str] = project_spec.get("domains", [])
    counter = itertools.count(1)
    steps: List[Step] = []
    # Determine plan id based on goal or a generated id
    plan_id = f"plan-{abs(hash(project_spec.get('goal', 'task')))%10000}"
    # Finance domain
    if "finance" in domains:
        # Step: fetch market data
        steps.append(
            Step(
                step_id=_generate_step_id("fetch_data", counter),
                team="Engineering",
                intent="Fetch market data for target symbols",
                adapter={"type": "finance"},
                args={"action": "fetch_data"},
                needs_secrets=[],
                evidence=[],
                budget_tokens=estimate_step_tokens(Step(
                    step_id="tmp",
                    team="Engineering",
                    intent="",
                    adapter={"type": "finance"},
                    args={},
                    needs_secrets=[],
                    evidence=[],
                    budget_tokens=0,
                    requires_human=False,
                )),
                requires_human=False,
            )
        )
        # Step: compute diffs
        steps.append(
            Step(
                step_id=_generate_step_id("compute_diffs", counter),
                team="Engineering",
                intent="Compute portfolio target differences",
                adapter={"type": "files"},
                args={"action": "compute_diffs"},
                needs_secrets=[],
                evidence=[],
                budget_tokens=estimate_step_tokens(Step(
                    step_id="tmp",
                    team="Engineering",
                    intent="",
                    adapter={"type": "files"},
                    args={},
                    needs_secrets=[],
                    evidence=[],
                    budget_tokens=0,
                    requires_human=False,
                )),
                requires_human=False,
            )
        )
        # Step: place orders (paper)
        steps.append(
            Step(
                step_id=_generate_step_id("place_orders", counter),
                team="Engineering",
                intent="Place paper orders to rebalance portfolio",
                adapter={"type": "finance"},
                args={"action": "place_orders", "mode": "paper"},
                needs_secrets=["BROKER_KEY"],
                evidence=[],
                budget_tokens=estimate_step_tokens(Step(
                    step_id="tmp",
                    team="Engineering",
                    intent="",
                    adapter={"type": "finance"},
                    args={},
                    needs_secrets=[],
                    evidence=[],
                    budget_tokens=0,
                    requires_human=False,
                )),
                requires_human=False,
            )
        )
        # Step: verify orders
        steps.append(
            Step(
                step_id=_generate_step_id("verify_orders", counter),
                team="QA",
                intent="Verify orders have been accepted and filled",
                adapter={"type": "finance"},
                args={"action": "verify_orders"},
                needs_secrets=["BROKER_KEY"],
                evidence=[],
                budget_tokens=estimate_step_tokens(Step(
                    step_id="tmp",
                    team="Engineering",
                    intent="",
                    adapter={"type": "finance"},
                    args={},
                    needs_secrets=[],
                    evidence=[],
                    budget_tokens=0,
                    requires_human=False,
                )),
                requires_human=False,
            )
        )
        # Step: schedule nightly summary
        steps.append(
            Step(
                step_id=_generate_step_id("schedule_nightly", counter),
                team="Scheduler",
                intent="Schedule nightly summary job",
                adapter={"type": "schedule"},
                args={"cron": "0 2 * * *"},
                needs_secrets=[],
                evidence=[],
                budget_tokens=estimate_step_tokens(Step(
                    step_id="tmp",
                    team="Engineering",
                    intent="",
                    adapter={"type": "schedule"},
                    args={},
                    needs_secrets=[],
                    evidence=[],
                    budget_tokens=0,
                    requires_human=False,
                )),
                requires_human=False,
            )
        )
    # Lead generation domain
    elif "leadgen" in domains:
        # Step: generate page
        steps.append(
            Step(
                step_id=_generate_step_id("generate_page", counter),
                team="Engineering",
                intent="Generate static landing page",
                adapter={"type": "files"},
                args={"action": "generate_page"},
                needs_secrets=[],
                evidence=[],
                budget_tokens=estimate_step_tokens(Step(
                    step_id="tmp",
                    team="Engineering",
                    intent="",
                    adapter={"type": "files"},
                    args={},
                    needs_secrets=[],
                    evidence=[],
                    budget_tokens=0,
                    requires_human=False,
                )),
                requires_human=False,
            )
        )
        # Step: deploy page
        steps.append(
            Step(
                step_id=_generate_step_id("deploy", counter),
                team="Engineering",
                intent="Deploy page to hosting platform",
                adapter={"type": "web"},
                args={"action": "deploy"},
                needs_secrets=[],
                evidence=[],
                budget_tokens=estimate_step_tokens(Step(
                    step_id="tmp",
                    team="Engineering",
                    intent="",
                    adapter={"type": "web"},
                    args={},
                    needs_secrets=[],
                    evidence=[],
                    budget_tokens=0,
                    requires_human=False,
                )),
                requires_human=False,
            )
        )
        # Step: configure form backend
        steps.append(
            Step(
                step_id=_generate_step_id("configure_form", counter),
                team="Engineering",
                intent="Configure form backend to collect leads",
                adapter={"type": "web"},
                args={"action": "configure_form"},
                needs_secrets=[],
                evidence=[],
                budget_tokens=estimate_step_tokens(Step(
                    step_id="tmp",
                    team="Engineering",
                    intent="",
                    adapter={"type": "web"},
                    args={},
                    needs_secrets=[],
                    evidence=[],
                    budget_tokens=0,
                    requires_human=False,
                )),
                requires_human=False,
            )
        )
        # Step: test form submission
        steps.append(
            Step(
                step_id=_generate_step_id("test_form", counter),
                team="QA",
                intent="Test form submission and verify entry in spreadsheet",
                adapter={"type": "web"},
                args={"action": "test_form"},
                needs_secrets=[],
                evidence=[],
                budget_tokens=estimate_step_tokens(Step(
                    step_id="tmp",
                    team="Engineering",
                    intent="",
                    adapter={"type": "web"},
                    args={},
                    needs_secrets=[],
                    evidence=[],
                    budget_tokens=0,
                    requires_human=False,
                )),
                requires_human=False,
            )
        )
        # Step: schedule updates (optional)
        steps.append(
            Step(
                step_id=_generate_step_id("schedule_updates", counter),
                team="Scheduler",
                intent="Schedule periodic page refreshes",
                adapter={"type": "schedule"},
                args={"cron": "@weekly"},
                needs_secrets=[],
                evidence=[],
                budget_tokens=estimate_step_tokens(Step(
                    step_id="tmp",
                    team="Engineering",
                    intent="",
                    adapter={"type": "schedule"},
                    args={},
                    needs_secrets=[],
                    evidence=[],
                    budget_tokens=0,
                    requires_human=False,
                )),
                requires_human=False,
            )
        )
    else:
        # Fallback: one generic step
        steps.append(
            Step(
                step_id=_generate_step_id("generic", counter),
                team="Engineering",
                intent="Perform goal",
                adapter={"type": "files"},
                args={},
                needs_secrets=[],
                evidence=[],
                budget_tokens=estimate_step_tokens(Step(
                    step_id="tmp",
                    team="Engineering",
                    intent="",
                    adapter={"type": "files"},
                    args={},
                    needs_secrets=[],
                    evidence=[],
                    budget_tokens=0,
                    requires_human=False,
                )),
                requires_human=False,
            )
        )
    plan = Plan(plan_id=plan_id, gates=["gate1"], steps=steps)
    # Downscope if necessary
    estimate = estimate_plan(plan)
    if estimate.total_tokens > PER_TASK_TOKEN_CAP:
        plan = downscope_plan(plan, PER_TASK_TOKEN_CAP)
    # Validate plan structure; raise if invalid
    validate_plan(plan)
    return plan