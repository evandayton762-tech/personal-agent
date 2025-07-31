import pytest

from orchestrator.core.models import Plan, Step, StepResult
from orchestrator.core.validators import validate_plan, validate_step, validate_step_result


def test_validate_plan_missing_fields():
    # Plan missing plan_id should raise ValueError
    step = Step(
        step_id="s1",
        team="Engineering",
        intent="Test",
        adapter={"type": "web"}
    )
    invalid_plan = Plan(plan_id="", gates=["gate1"], steps=[step])
    with pytest.raises(ValueError):
        validate_plan(invalid_plan)


def test_validate_step_unknown_tool():
    step = Step(
        step_id="s1",
        team="Engineering",
        intent="Test",
        adapter={"type": "unknown_tool"}
    )
    with pytest.raises(ValueError):
        validate_step(step)


def test_validate_step_result_invalid_status():
    result = StepResult(step_id="s1", status="not_ok")
    with pytest.raises(ValueError):
        validate_step_result(result)