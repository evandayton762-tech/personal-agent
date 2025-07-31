"""Information Quality Score computation.

This module computes the IQS (0–100) based on completeness, actionability,
risk, and ambiguity. It uses definitions from the MVI module.
"""

from typing import Dict, Any

from .mvi import MVI_DEFINITIONS


def _completeness_score(spec: Dict[str, Any]) -> float:
    """Compute completeness as the fraction of MVI fields present."""
    domain = spec.get("domains", [None])[0]
    if not domain or domain not in MVI_DEFINITIONS:
        return 0.0
    required = MVI_DEFINITIONS[domain]
    provided = spec.get("parameters", {})
    present = [f for f in required if f in provided and provided[f]]
    if not required:
        return 1.0
    return len(present) / len(required)


def _actionability_score(completeness: float) -> float:
    """Derive actionability from completeness; simplified heuristic."""
    # Full actionability when completeness ≥ 75% otherwise scaled.
    return completeness if completeness < 0.75 else 1.0


def _risk_score(consent: Dict[str, Any]) -> float:
    """Risk is lower when free_only and ask_before_spend are enabled."""
    free_only = consent.get("free_only", True)
    ask_before_spend = consent.get("ask_before_spend", True)
    return 1.0 if free_only and ask_before_spend else 0.5


def _ambiguity_score(spec: Dict[str, Any]) -> float:
    """Ambiguity decreases with more detail."""
    # If goal is short (<20 chars), assume ambiguous
    goal = spec.get("goal", "")
    return 1.0 if len(goal) >= 20 else 0.5


def compute_iqs(spec: Dict[str, Any], consent: Dict[str, Any]) -> float:
    """Compute overall IQS as a weighted sum of sub-scores.

    Returns a value between 0 and 100.
    """
    comp = _completeness_score(spec)
    act = _actionability_score(comp)
    risk = _risk_score(consent)
    amb = _ambiguity_score(spec)
    score = (
        comp * 0.40 +
        act * 0.30 +
        risk * 0.20 +
        amb * 0.10
    ) * 100
    return round(score, 2)