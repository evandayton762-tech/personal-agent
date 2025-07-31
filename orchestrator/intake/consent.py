"""Consent bundle resolver.

This module provides a simple mechanism to construct or fetch a consent bundle
for a project. In a full implementation, consent would be persisted per
project; here we return default values.
"""

from typing import Dict, Any


DEFAULT_CONSENT: Dict[str, Any] = {
    "free_only": True,
    "ask_before_spend": True,
    "allow_account_creation": True,
    "allow_email_access": "none",
    "allow_2fa": "none",
    "live_trading": False,
    "max_daily_llm_usd": 1.00,
    "max_daily_third_party_usd": 0.00,
}


def resolve_consent(project_name: str) -> Dict[str, Any]:
    """Return the consent bundle for a project. Currently returns defaults."""
    # In a full implementation, this would load from storage or prompt the user.
    return DEFAULT_CONSENT.copy()