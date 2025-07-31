import os
import unittest
from fastapi.testclient import TestClient

from orchestrator.service import app, queue, runs, parked, ledger, MAX_DAILY_TOKENS, STOP_THRESHOLD


class TestBudgetEnforcement(unittest.TestCase):
    def setUp(self) -> None:
        # Clear shared state and ledger before each test
        queue.clear()
        runs.clear()
        parked.clear()
        # Remove ledger file to reset totals
        if os.path.exists(ledger.ledger_path):
            os.remove(ledger.ledger_path)
        self.client = TestClient(app)

    def tearDown(self) -> None:
        # Clean up ledger file after test to avoid cross-test contamination
        if os.path.exists(ledger.ledger_path):
            os.remove(ledger.ledger_path)

    def test_budget_refusal_and_endpoint(self):
        # Preload ledger with tokens just above stop threshold
        preload_tokens = int(MAX_DAILY_TOKENS * STOP_THRESHOLD) + 100
        ledger.append("task-pre", "step-pre", preload_tokens, 0, 0.0)
        # Enqueue a step that would exceed the cap
        step = {
            "step_id": "budget-test",
            "team": "Engineering",
            "intent": "Test",
            "adapter": {"type": "web"},
        }
        self.client.post("/enqueue", json=step)
        # Connect websocket; the service should park the step and send noop
        with self.client.websocket_connect("/ws") as ws:
            msg = ws.receive_json()
            # Expect a noop due to no dispatch
            self.assertEqual(msg.get("type"), "noop")
            # Send ack to keep loop consistent
            ws.send_text("ack")
        # Verify that the step was parked
        park_resp = self.client.get("/parked")
        self.assertEqual(park_resp.status_code, 200)
        self.assertEqual(len(park_resp.json()["parked"]), 1)
        # Verify budget endpoint reflects high usage
        budget_resp = self.client.get("/budget/today")
        self.assertEqual(budget_resp.status_code, 200)
        data = budget_resp.json()
        self.assertIn("used_ratio", data)
        self.assertGreaterEqual(data["used_ratio"], STOP_THRESHOLD)


if __name__ == "__main__":
    unittest.main()