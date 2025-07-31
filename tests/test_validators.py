import unittest

from orchestrator.core.models import Plan, Step, StepResult
from orchestrator.core.validators import (
    validate_plan,
    validate_step,
    validate_step_result,
)


class TestValidators(unittest.TestCase):
    def test_validate_plan_missing_fields(self):
        """Plan missing plan_id should raise ValueError"""
        step = Step(
            step_id="s1",
            team="Engineering",
            intent="Test",
            adapter={"type": "web"},
        )
        invalid_plan = Plan(plan_id="", gates=["gate1"], steps=[step])
        with self.assertRaises(ValueError):
            validate_plan(invalid_plan)

    def test_validate_step_unknown_tool(self):
        step = Step(
            step_id="s1",
            team="Engineering",
            intent="Test",
            adapter={"type": "unknown_tool"},
        )
        with self.assertRaises(ValueError):
            validate_step(step)

    def test_validate_step_result_invalid_status(self):
        result = StepResult(step_id="s1", status="not_ok")
        with self.assertRaises(ValueError):
            validate_step_result(result)


if __name__ == "__main__":
    unittest.main()