"""FastAPI orchestrator service skeleton.

Provides endpoints for health check, plan generation, enqueuing steps, listing runs and parked items,
and a WebSocket for step dispatch and result collection.
"""

from __future__ import annotations

from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .core.models import Plan, Step, StepResult
from .cost.governor import estimate_plan, estimate_step_tokens
from .cost.ledger import CostLedger


app = FastAPI()

# In-memory store of queued steps, runs, and parked items
queue: List[Dict[str, Any]] = []
runs: List[Dict[str, Any]] = []
parked: List[Dict[str, Any]] = []

# Instantiate a cost ledger for recording token usage
ledger = CostLedger()

# Budget caps (static for now; could be loaded from config)
MAX_DAILY_TOKENS = 25000
WARN_THRESHOLD = 0.8  # 80% usage
STOP_THRESHOLD = 0.9  # 90% usage


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/plan")
def create_plan(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a static minimal plan for testing purposes.

    In this skeleton, we ignore the spec and return a plan with a single dummy step.
    """
    plan = {
        "plan_id": "plan-1",
        "gates": ["gate1"],
        "steps": [
            {
                "step_id": "step-1",
                "team": "Engineering",
                "intent": "Dummy step",
                "adapter": {"type": "web"},
                "args": {},
                "needs_secrets": [],
                "evidence": [],
                "budget_tokens": 0,
                "requires_human": False,
            }
        ],
    }
    return plan


@app.post("/enqueue")
def enqueue(item: Dict[str, Any]) -> Dict[str, Any]:
    """Enqueue a plan or a single step."""
    if "steps" in item:
        # It's a plan; extend the queue with its steps
        for step in item.get("steps", []):
            queue.append(step)
    else:
        queue.append(item)
    return {"queued": len(queue)}


@app.get("/runs")
def get_runs() -> Dict[str, Any]:
    """Return run results along with budget status."""
    totals = ledger.totals_today()
    used = totals.get("in_tokens", 0) + totals.get("out_tokens", 0)
    used_ratio = used / MAX_DAILY_TOKENS if MAX_DAILY_TOKENS else 0.0
    return {
        "runs": runs,
        "budget": {
            "totals": totals,
            "max_tokens": MAX_DAILY_TOKENS,
            "used_ratio": used_ratio,
        },
    }


@app.get("/parked")
def get_parked() -> Dict[str, Any]:
    return {"parked": parked}


@app.get("/budget/today")
def get_budget_today() -> Dict[str, Any]:
    """Return today's aggregated budget totals and thresholds."""
    totals = ledger.totals_today()
    used = totals.get("in_tokens", 0) + totals.get("out_tokens", 0)
    return {
        "totals": totals,
        "max_tokens": MAX_DAILY_TOKENS,
        "warn_threshold": WARN_THRESHOLD,
        "stop_threshold": STOP_THRESHOLD,
        "used_ratio": used / MAX_DAILY_TOKENS if MAX_DAILY_TOKENS else 0.0,
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            # Wait until a step is available
            if not queue:
                await websocket.send_json({"type": "noop"})
                await websocket.receive_text()  # consume heartbeat or ack
                continue
            step = queue.pop(0)
            # Budget enforcement: estimate tokens and check against daily cap
            # Estimate tokens based on adapter type in the step dict
            adapter_type = None
            if isinstance(step, dict):
                adapter = step.get("adapter")
                if isinstance(adapter, dict):
                    adapter_type = adapter.get("type")
            est_tokens = estimate_step_tokens(type("obj", (), {"adapter": {"type": adapter_type}}))
            totals = ledger.totals_today()
            used = totals.get("in_tokens", 0) + totals.get("out_tokens", 0)
            projected_ratio = (used + est_tokens) / MAX_DAILY_TOKENS if MAX_DAILY_TOKENS else 0.0
            if projected_ratio >= STOP_THRESHOLD:
                # Park the step due to budget cap
                parked_item = {
                    "step_id": step.get("step_id"),
                    "status": "parked",
                    "reason": "budget",
                    "next_try": "tomorrow",
                    "note": "Daily token cap reached. Retry after next cycle.",
                }
                parked.append(parked_item)
                # Do not send to runner; continue loop
                continue
            # Send step to runner
            await websocket.send_json(step)
            # Receive StepResult from runner
            result_data = await websocket.receive_json()
            # Record in ledger using estimated tokens; assign 0 USD for now
            step_id = result_data.get("step_id", "unknown")
            task_id = result_data.get("task_id", "unknown_task")
            ledger.append(task_id, step_id, est_tokens, 0, 0.0)
            # Append to runs or parked based on status
            status = result_data.get("status")
            if status == "blocked" or status == "parked":
                parked.append(result_data)
            else:
                runs.append(result_data)
    except WebSocketDisconnect:
        return