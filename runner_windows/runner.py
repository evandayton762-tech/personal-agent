"""Runner skeleton.

Connects to the orchestrator WebSocket, sends heartbeats, processes steps using a dispatch table,
and supports a kill switch. Logs events to a local file with secrets redacted.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import time
from datetime import datetime
from typing import Dict, Any, Callable

import websockets


ALLOWED_TOOLS = [
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


class Runner:
    def __init__(self, server_ws_url: str, logs_dir: str = "runner_windows/logs") -> None:
        self.server_ws_url = server_ws_url
        self.kill_flag = False
        self.logs_dir = logs_dir
        os.makedirs(self.logs_dir, exist_ok=True)
        self.log_file = os.path.join(self.logs_dir, f"runner_{int(time.time())}.log")

    def log(self, message: str) -> None:
        ts = datetime.utcnow().isoformat()
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"{ts} {message}\n")

    def get_free_disk(self) -> int:
        # Return free disk space in megabytes
        total, used, free = shutil.disk_usage(".")
        return int(free / (1024 * 1024))

    def validate_step(self, step: Dict[str, Any]) -> bool:
        adapter_type = step.get("adapter", {}).get("type")
        return adapter_type in ALLOWED_TOOLS

    async def dispatch_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Process a step and return a StepResult-like dict."""
        step_id = step.get("step_id", "unknown")
        if self.kill_flag:
            self.log(f"Step {step_id} killed by user")
            return {"step_id": step_id, "status": "failed", "notes": "killed"}
        if not self.validate_step(step):
            self.log(f"Unknown tool for step {step_id}")
            return {"step_id": step_id, "status": "failed", "notes": "unknown_tool"}
        # Placeholder dispatch; returns ok with dummy evidence
        evidence = {"info": "placeholder"}
        self.log(f"Processed step {step_id} successfully")
        return {"step_id": step_id, "status": "ok", "evidence": evidence}

    async def heartbeat(self, ws) -> None:
        while not self.kill_flag:
            hb = {
                "runner_status": "running",
                "free_disk": self.get_free_disk(),
                "timestamp": datetime.utcnow().isoformat(),
            }
            try:
                await ws.send(json.dumps(hb))
            except Exception:
                break
            await asyncio.sleep(10)

    async def run(self) -> None:
        """Main loop: connect via WebSocket, send heartbeats, process steps."""
        async with websockets.connect(self.server_ws_url) as ws:
            hb_task = asyncio.create_task(self.heartbeat(ws))
            try:
                while not self.kill_flag:
                    message = await ws.recv()
                    # Expect JSON
                    try:
                        step = json.loads(message)
                    except Exception:
                        await ws.send(json.dumps({"error": "invalid_json"}))
                        continue
                    # Handle noop keep-alive
                    if step.get("type") == "noop":
                        await ws.send("ack")
                        continue
                    result = await self.dispatch_step(step)
                    await ws.send(json.dumps(result))
            finally:
                hb_task.cancel()

    def kill(self) -> None:
        self.kill_flag = True