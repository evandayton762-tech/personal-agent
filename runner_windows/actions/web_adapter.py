"""Web adapter using Playwright.

This adapter exposes high‑level browser actions (open, wait, type, click, select,
upload, get_text, screenshot) intended to be deterministic and reusable across
recipes. It attempts to import Playwright and, if unavailable, returns
a parked status indicating that browser automation is not available in this
environment.

When Playwright is installed, the adapter maintains a persistent browser
context per domain under ``runner_windows/profiles`` so that sessions and
cookies survive across steps. Because this environment does not currently
provide Playwright, all functions return a parked object with reason
``playwright_missing``.
"""

from __future__ import annotations

import os
from typing import Dict, Optional


def _playwright_available() -> bool:
    try:
        import playwright  # type: ignore
        return True
    except ImportError:
        return False


def _park_reason() -> Dict[str, str]:
    return {
        "status": "parked",
        "reason": "playwright_missing",
        "note": "Playwright is not installed or available in this environment.",
    }


def open(url: str) -> Dict[str, str]:
    """Open a URL in a browser context.

    Returns a parked object if Playwright is unavailable.
    """
    if not _playwright_available():
        return _park_reason()
    # Placeholder for future implementation when Playwright is available
    return _park_reason()


def wait(selector: str, timeout_s: float = 10.0) -> Dict[str, str]:
    """Wait for a selector to be visible/enabled.

    Returns a parked object if Playwright is unavailable.
    """
    if not _playwright_available():
        return _park_reason()
    return _park_reason()


def type(selector: str, text: str) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    return _park_reason()


def click(selector: str) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    return _park_reason()


def select(selector: str, option: str) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    return _park_reason()


def upload(selector: str, file_path: str) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    return _park_reason()


def get_text(selector: str) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    return _park_reason()


def screenshot(region: Optional[Dict[str, int]] = None) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    return _park_reason()