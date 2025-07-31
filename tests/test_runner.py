import os
import unittest
import asyncio

from runner_windows.runner import Runner


class TestRunner(unittest.TestCase):
    def test_dispatch_step_ok_and_logging(self):
        runner = Runner(server_ws_url="ws://localhost:8000/ws")
        step = {
            "step_id": "s1",
            "team": "Engineering",
            "intent": "Test",
            "adapter": {"type": "web"},
        }
        result = asyncio.run(runner.dispatch_step(step))
        self.assertEqual(result["status"], "ok")
        # Ensure log file exists
        self.assertTrue(os.path.exists(runner.log_file))
        with open(runner.log_file, "r", encoding="utf-8") as f:
            log_contents = f.read()
        self.assertIn("Processed step s1", log_contents)

    def test_kill_switch(self):
        runner = Runner(server_ws_url="ws://localhost:8000/ws")
        step = {
            "step_id": "s2",
            "team": "Engineering",
            "intent": "Test",
            "adapter": {"type": "web"},
        }
        runner.kill()
        result = asyncio.run(runner.dispatch_step(step))
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["notes"], "killed")


if __name__ == "__main__":
    unittest.main()