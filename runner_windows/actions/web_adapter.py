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
import time
import urllib.parse
from typing import Dict, Optional, Tuple, Any


def _playwright_available() -> bool:
    try:
        import playwright  # type: ignore
        return True
    except ImportError:
        return False


# Global Playwright instance and contexts keyed by domain
_playwright_instance = None
_contexts: Dict[str, Any] = {}  # type: ignore
_current_pages: Dict[str, Any] = {}  # type: ignore


def _park_reason(reason: str = "runner_setup_required", note: str = "Playwright is not installed or configured in this environment.") -> Dict[str, str]:
    """Return a parked dictionary indicating that the runner setup is incomplete or another error occurred."""
    return {
        "status": "parked",
        "reason": reason,
        "note": note,
    }


def _ensure_playwright():
    """Start the Playwright instance if not already started."""
    global _playwright_instance
    if _playwright_instance is None:
        from playwright.sync_api import sync_playwright  # type: ignore
        _playwright_instance = sync_playwright().start()


def _get_domain(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return parsed.hostname or "default"


def _get_context(domain: str):
    """Return (or create) a persistent browser context for the given domain."""
    _ensure_playwright()
    from playwright.sync_api import BrowserContext  # type: ignore
    if domain in _contexts:
        return _contexts[domain]
    # Ensure profile directory exists
    profile_dir = os.path.join("runner_windows", "profiles", domain)
    os.makedirs(profile_dir, exist_ok=True)
    browser = _playwright_instance.chromium.launch_persistent_context(
        profile_dir,
        headless=True,
    )
    _contexts[domain] = browser
    return browser


def _get_page(domain: str):
    """Get (or create) the current page for a domain context."""
    ctx = _get_context(domain)
    if domain in _current_pages and not _current_pages[domain].is_closed():
        return _current_pages[domain]
    # Create a new page
    page = ctx.new_page()
    _current_pages[domain] = page
    return page


def open(url: str) -> Dict[str, str]:
    """Open a URL in a browser context and return evidence."""
    if not _playwright_available():
        return _park_reason()
    try:
        domain = _get_domain(url)
        page = _get_page(domain)
        page.goto(url)
        return {"final_url": page.url}
    except Exception as exc:
        return _park_reason("open_failed", str(exc))


def wait(selector: str, timeout_s: float = 10.0) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    try:
        # Use last opened page across any domain
        if not _current_pages:
            return _park_reason("no_page", "No page open to wait on.")
        # Get the most recent page (last value)
        page = list(_current_pages.values())[-1]
        page.wait_for_selector(selector, timeout=timeout_s * 1000)
        return {}
    except Exception as exc:
        # Capture DOM + screenshot for debugging
        _capture_debug(page, "wait_failed")
        return {
            "status": "blocked",
            "reason": "selector_failed",
            "note": str(exc),
        }


def type(selector: str, text: str) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    try:
        if not _current_pages:
            return _park_reason("no_page", "No page open to type into.")
        page = list(_current_pages.values())[-1]
        page.fill(selector, text)
        return {}
    except Exception as exc:
        _capture_debug(page, "type_failed")
        return {
            "status": "blocked",
            "reason": "selector_failed",
            "note": str(exc),
        }


def click(selector: str) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    try:
        if not _current_pages:
            return _park_reason("no_page", "No page open to click on.")
        page = list(_current_pages.values())[-1]
        page.click(selector)
        return {}
    except Exception as exc:
        _capture_debug(page, "click_failed")
        return {
            "status": "blocked",
            "reason": "selector_failed",
            "note": str(exc),
        }


def select(selector: str, option: str) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    try:
        if not _current_pages:
            return _park_reason("no_page", "No page open to select from.")
        page = list(_current_pages.values())[-1]
        page.select_option(selector, option)
        return {}
    except Exception as exc:
        _capture_debug(page, "select_failed")
        return {
            "status": "blocked",
            "reason": "selector_failed",
            "note": str(exc),
        }


def upload(selector: str, file_path: str) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    try:
        if not _current_pages:
            return _park_reason("no_page", "No page open to upload into.")
        page = list(_current_pages.values())[-1]
        # Playwright uses set_input_files for uploads
        page.set_input_files(selector, file_path)
        return {}
    except Exception as exc:
        _capture_debug(page, "upload_failed")
        return {
            "status": "blocked",
            "reason": "selector_failed",
            "note": str(exc),
        }


def get_text(selector: str) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    try:
        if not _current_pages:
            return _park_reason("no_page", "No page open to extract text from.")
        page = list(_current_pages.values())[-1]
        text = page.text_content(selector)
        return {"text": text}
    except Exception as exc:
        _capture_debug(page, "get_text_failed")
        return {
            "status": "blocked",
            "reason": "selector_failed",
            "note": str(exc),
        }


def screenshot(region: Optional[Dict[str, int]] = None) -> Dict[str, str]:
    if not _playwright_available():
        return _park_reason()
    try:
        if not _current_pages:
            return _park_reason("no_page", "No page open to capture screenshot from.")
        page = list(_current_pages.values())[-1]
        # Prepare artifacts directory
        artifacts_dir = os.path.join("runner_windows", "artifacts")
        os.makedirs(artifacts_dir, exist_ok=True)
        filename = f"screenshot_{int(time.time() * 1000)}.png"
        path = os.path.join(artifacts_dir, filename)
        if region:
            clip = {
                "x": region.get("x", 0),
                "y": region.get("y", 0),
                "width": region.get("width", page.viewport_size["width"]),
                "height": region.get("height", page.viewport_size["height"]),
            }
            page.screenshot(path=path, clip=clip)
        else:
            page.screenshot(path=path)
        return {"screenshot_id": filename}
    except Exception as exc:
        return _park_reason("screenshot_failed", str(exc))


def _capture_debug(page, suffix: str) -> None:
    """Capture DOM and screenshot to artifacts for debugging selector failures."""
    try:
        artifacts_dir = os.path.join("runner_windows", "artifacts")
        os.makedirs(artifacts_dir, exist_ok=True)
        ts = int(time.time() * 1000)
        # Save DOM
        html = page.content()
        dom_path = os.path.join(artifacts_dir, f"dom_{suffix}_{ts}.html")
        with open(dom_path, "w", encoding="utf-8") as f:
            f.write(html)
        # Save screenshot
        screenshot_path = os.path.join(artifacts_dir, f"screenshot_{suffix}_{ts}.png")
        page.screenshot(path=screenshot_path)
    except Exception:
        pass