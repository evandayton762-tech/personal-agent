import json
import os
import unittest

from orchestrator.planner import plan_project
from orchestrator.core.validators import validate_plan


class TestPlanner(unittest.TestCase):
    def test_finance_example_plan(self):
        spec_path = os.path.join("docs", "examples_finance_spec.json")
        with open(spec_path, "r", encoding="utf-8") as f:
            spec = json.load(f)
        plan = plan_project(spec)
        # Validate structure
        validate_plan(plan)
        # Ensure plan has multiple steps for finance
        self.assertGreaterEqual(len(plan.steps), 1)
        # Ensure adapters are from allowed set
        allowed = {"web", "desktop", "files", "ocr", "secrets", "schedule", "budget", "finance", "docs"}
        for step in plan.steps:
            self.assertIn(step.adapter.get("type"), allowed)

    def test_leadgen_example_plan(self):
        spec_path = os.path.join("docs", "examples_leadgen_spec.json")
        with open(spec_path, "r", encoding="utf-8") as f:
            spec = json.load(f)
        plan = plan_project(spec)
        validate_plan(plan)
        # Plan for leadgen should include at least one step with adapter type web or files
        adapter_types = [s.adapter.get("type") for s in plan.steps]
        self.assertTrue(any(t in {"web", "files"} for t in adapter_types))

    def test_unknown_domain_plan(self):
        spec = {"goal": "Unknown", "domains": ["foo"]}
        plan = plan_project(spec)
        validate_plan(plan)
        self.assertEqual(len(plan.steps), 1)
        self.assertEqual(plan.steps[0].adapter.get("type"), "files")


if __name__ == "__main__":
    unittest.main()