"""Secrets adapter.

This adapter handles retrieving and storing secrets via aliases. Secrets are
looked up in environment variables first, then in a local config file under
``runner_windows/config/secrets.json`` (which is ignored by version control).
Secrets are never printed or logged by these functions; only aliases should
appear in logs. Vault integrations are optional and not implemented here.
"""

from __future__ import annotations

import json
import os
from typing import Dict, Optional


# Path where secrets are stored locally. This file is intentionally excluded
# from version control via .gitignore.
LOCAL_SECRETS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "config", "secrets.json"
)


def _load_local_secrets() -> Dict[str, str]:
    if os.path.exists(LOCAL_SECRETS_PATH):
        try:
            with open(LOCAL_SECRETS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # If the file is corrupted, return an empty dict to avoid crashing
            return {}
    return {}


def _save_local_secrets(secrets: Dict[str, str]) -> None:
    # Ensure directory exists
    os.makedirs(os.path.dirname(LOCAL_SECRETS_PATH), exist_ok=True)
    with open(LOCAL_SECRETS_PATH, "w", encoding="utf-8") as f:
        json.dump(secrets, f)


def get(alias: str) -> Dict[str, str] | str:
    """Retrieve the secret value for the given alias.

    Checks the environment variables first, then a local JSON file. If the
    secret is not found, returns a dict indicating a parked state.

    Args:
        alias: The secret alias to retrieve.

    Returns:
        The secret string if found, otherwise a dictionary with status and reason.
    """
    # Environment variables take precedence
    env_val = os.getenv(alias)
    if env_val is not None:
        return env_val
    # Check local secrets file
    secrets = _load_local_secrets()
    if alias in secrets:
        return secrets[alias]
    return {
        "status": "parked",
        "reason": "missing_secret",
        "note": f"Secret alias {alias} is not configured.",
    }


def set(alias: str, value: str) -> Dict[str, str]:
    """Store the secret value for the given alias in the local config file.

    Args:
        alias: The secret alias to set.
        value: The secret value to store.

    Returns:
        A dictionary confirming the alias has been stored.
    """
    secrets = _load_local_secrets()
    secrets[alias] = value
    _save_local_secrets(secrets)
    # Return minimal metadata; never include the secret value
    return {"alias": alias}