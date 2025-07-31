"""FastAPI orchestrator service skeleton.

Provides endpoints for health check, plan generation, enqueuing steps, listing runs and parked items,
and a WebSocket for step dispatch and result collection.
"""

from __future__ import annotations

from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .core.models import Plan, Step, StepResult
from .cost.governor import estimate_plan


app = FastAPI()

# In-memory store of queued steps, runs, and parked items
queue: List[Dict[str, Any]] = []
runs: List[Dict[str, Any]] = []
parked: List[Dict[str, Any]] = []


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
    return {"runs": runs}


@app.get("/parked")
def get_parked() -> Dict[str, Any]:
    return {"parked": parked}


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
            await websocket.send_json(step)
            # Receive StepResult from runner
            result_data = await websocket.receive_json()
            # Append to runs or parked based on status
            status = result_data.get("status")
            if status == "blocked":
                parked.append(result_data)
            else:
                runs.append(result_data)
    except WebSocketDisconnect:
        return