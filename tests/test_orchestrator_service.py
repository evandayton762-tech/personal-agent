import unittest
from fastapi.testclient import TestClient

from orchestrator.service import app, queue, runs, parked


class TestOrchestratorService(unittest.TestCase):
    def setUp(self):
        # Clear shared state before each test
        queue.clear()
        runs.clear()
        parked.clear()
        self.client = TestClient(app)

    def test_health_and_plan_and_queue(self):
        # Health endpoint
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "ok")
        # Create plan
        plan_resp = self.client.post("/plan", json={"goal": "test", "domains": []})
        self.assertEqual(plan_resp.status_code, 200)
        plan = plan_resp.json()
        # Enqueue plan
        enq = self.client.post("/enqueue", json=plan)
        self.assertEqual(enq.status_code, 200)
        # Connect WebSocket and process step
        with self.client.websocket_connect("/ws") as ws:
            # Receive the step
            step = ws.receive_json()
            self.assertIn("step_id", step)
            # Send back a result
            ws.send_json({"step_id": step["step_id"], "status": "ok"})
            # After sending result, connection might send noop; send ack
            ws.receive_json()  # consume possible noop or next message
            ws.send_text("ack")
        # Check that run was recorded
        runs_resp = self.client.get("/runs")
        self.assertEqual(len(runs_resp.json()["runs"]), 1)

    def test_blocked_step_goes_to_parked(self):
        # Enqueue single step directly
        step = {
            "step_id": "s-block",
            "team": "Engineering",
            "intent": "Test",
            "adapter": {"type": "web"},
        }
        self.client.post("/enqueue", json=step)
        with self.client.websocket_connect("/ws") as ws:
            received = ws.receive_json()
            ws.send_json({"step_id": received["step_id"], "status": "blocked"})
            ws.receive_json()
            ws.send_text("ack")
        # Check parked
        park_resp = self.client.get("/parked")
        self.assertEqual(len(park_resp.json()["parked"]), 1)


if __name__ == "__main__":
    unittest.main()