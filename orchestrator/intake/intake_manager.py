"""Dynamic intake manager.

This class orchestrates the intake flow: computing information quality, generating
questions, applying answers, and determining readiness.
"""

from typing import Dict, Any, List, Tuple

from .iqs import compute_iqs
from .questioner import generate_questions, apply_answers
from .consent import resolve_consent


class IntakeManager:
    def __init__(self, per_task_token_cap: int = 8000):
        self.per_task_token_cap = per_task_token_cap
        self.token_usage = 0

    def assess(self, spec: Dict[str, Any], consent: Dict[str, Any]) -> Tuple[float, List[Dict[str, Any]], bool]:
        """Compute IQS, generate questions if needed, and determine if ready.

        Returns a tuple (iqs, questions, ready).
        """
        iqs = compute_iqs(spec, consent)
        questions: List[Dict[str, Any]] = []
        ready = False
        # Determine expected gain: if missing fields remain, approximate gain.
        domain = spec.get("domains", [None])[0]
        missing_count = 0
        from .mvi import MVI_DEFINITIONS
        if domain in MVI_DEFINITIONS:
            required = MVI_DEFINITIONS[domain]
            missing_count = len([f for f in required if not spec.get("parameters", {}).get(f)])
        expected_gain = (missing_count / (len(required) or 1)) * 40  # approximate
        # Stop if IQS ≥ 80 or expected gain < 10 or token usage ≥ 15% of cap
        if iqs >= 80 or expected_gain < 10 or (self.token_usage / self.per_task_token_cap) >= 0.15:
            ready = True
        else:
            questions = generate_questions(spec)
        return iqs, questions, ready

    def collect_answers(self, spec: Dict[str, Any], answers: Dict[str, Any]) -> Dict[str, Any]:
        """Apply user answers to the spec and update token usage (placeholder)."""
        # Increment token usage by a small constant per answer to simulate consumption
        self.token_usage += 50 * len(answers)
        return apply_answers(spec, answers)

    def get_consent(self, project_name: str) -> Dict[str, Any]:
        return resolve_consent(project_name)