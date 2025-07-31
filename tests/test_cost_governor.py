import os
import json
import unittest
from datetime import datetime, timezone, timedelta

from orchestrator.core.models import Plan, Step
from orchestrator.cost.governor import estimate_plan, downscope_plan
from orchestrator.cost.ledger import CostLedger


class TestCostGovernor(unittest.TestCase):
    def test_downscope_plan_over_cap(self):
        # Create a plan with 3 steps, each estimated 300 tokens (web)
        steps = [
            Step(step_id=f"s{i}", team="Engineering", intent="Test", adapter={"type": "web"})
            for i in range(3)
        ]
        plan = Plan(plan_id="p1", gates=["gate1"], steps=steps)
        # Cap tokens to force downscoping after two steps (cap = 600)
        downscoped = downscope_plan(plan, token_cap=600)
        # Expect at most 2 steps
        self.assertTrue(len(downscoped.steps) <= 2)
        # Ensure at least one step remains
        self.assertGreaterEqual(len(downscoped.steps), 1)

    def test_ledger_aggregation(self):
        # Use a temporary ledger path
        ledger_path = os.path.join("memory", "test_cost_ledger.jsonl")
        # Remove existing test ledger
        if os.path.exists(ledger_path):
            os.remove(ledger_path)
        ledger = CostLedger(ledger_path)
        # Append three entries for today
        ledger.append("task1", "s1", 100, 50, 0.01)
        ledger.append("task1", "s2", 200, 70, 0.02)
        ledger.append("task2", "s1", 50, 25, 0.005)
        totals = ledger.totals_today()
        self.assertEqual(totals["in_tokens"], 350)
        self.assertEqual(totals["out_tokens"], 145)
        # Approximate float sum; allow small epsilon
        self.assertAlmostEqual(totals["usd"], 0.035, places=3)
        # Clean up test ledger
        if os.path.exists(ledger_path):
            os.remove(ledger_path)


if __name__ == "__main__":
    unittest.main()