"""Question generator for intake manager.

Given a ProjectSpec-like dictionary, this module identifies missing MVI fields
and produces a batch of questions. Questions are multiple-choice when
predefined options exist; otherwise a free-text question is generated.
"""

from typing import Dict, List, Any

from .mvi import MVI_DEFINITIONS, MVI_OPTIONS


def generate_questions(spec: Dict[str, Any], max_items: int = 5) -> List[Dict[str, Any]]:
    """Produce a list of questions for missing MVI fields.

    Each question is a dictionary with keys: field, type, options, prompt.
    Questions are limited to max_items.
    """
    domain = spec.get("domains", [None])[0]
    if domain not in MVI_DEFINITIONS:
        return []
    required_fields = MVI_DEFINITIONS[domain]
    provided = spec.get("parameters", {})
    missing = [f for f in required_fields if not provided.get(f)]
    questions: List[Dict[str, Any]] = []
    for field in missing[:max_items]:
        opts = MVI_OPTIONS.get(field)
        if opts:
            questions.append(
                {
                    "field": field,
                    "type": "multiple_choice",
                    "options": opts,
                    "prompt": f"Please select a value for {field}",
                }
            )
        else:
            questions.append(
                {
                    "field": field,
                    "type": "free_text",
                    "prompt": f"Please provide a value for {field}",
                }
            )
    return questions


def apply_answers(spec: Dict[str, Any], answers: Dict[str, Any]) -> Dict[str, Any]:
    """Update the spec's parameters with user-provided answers and return the updated spec."""
    parameters = spec.get("parameters", {})
    parameters.update(answers)
    spec["parameters"] = parameters
    return spec