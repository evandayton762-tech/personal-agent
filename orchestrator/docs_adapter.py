"""DocsAdapter for Google Docs integration.

This adapter provides a thin layer around Google Docs operations. Because
external network access is unavailable in this environment, the adapter
implements a graceful fallback to local Markdown files. When a refresh token
has not been configured, all methods return a parked state with reason
``oauth_required``. If a token is present, the adapter simulates document
operations by writing to ``docs/PROJECT_LOG.md``.

Functions implemented:

* ``ensure_doc(project_name)`` → ``doc_id``: Create or return a document for the given project. In fallback mode, returns the local log path.
* ``append_section(doc_id, heading, markdown_or_struct)``: Append a section heading and content.
* ``insert_table(doc_id, rows)``: Append a Markdown table.
* ``insert_image(doc_id, image_path_or_drive_id)``: Insert a placeholder for an image.
* ``link_artifact(doc_id, title, href)``: Append a link to an artifact.
* ``update_toc(doc_id)``: No‑op in fallback mode; would update table of contents.

All functions return a dictionary containing at least a ``status`` field. When
the user has not authorized Docs access, ``status`` will be ``parked`` and
``reason`` will be ``oauth_required`` along with a message instructing the
user to perform the OAuth device code flow.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional


_TOKEN_PATH = os.path.join("runner_windows", "config", "google_token.json")
_PROJECT_LOG_PATH = os.path.join("docs", "PROJECT_LOG.md")
_OAUTH_MESSAGE_PATH = os.path.join("docs", "messages_oauth_docs.txt")


def _load_token() -> Optional[Dict[str, Any]]:
    if not os.path.exists(_TOKEN_PATH):
        return None
    try:
        with open(_TOKEN_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _oauth_message() -> str:
    """Load the OAuth device code message from the docs directory."""
    try:
        with open(_OAUTH_MESSAGE_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return "Open the provided URL and enter the device code to authorize Docs access."


def ensure_doc(project_name: str) -> Dict[str, Any]:
    """Ensure a document exists for the given project and return its ID.

    In this offline implementation, the document ID is always the path to
    ``PROJECT_LOG.md``. If the user has not authorized Google Docs, returns
    a parked response with reason ``oauth_required`` and includes the
    authorization message. Otherwise returns ``{status: ok, doc_id: path}``.
    """
    token = _load_token()
    if token is None:
        # Return parked state requiring OAuth
        return {
            "status": "parked",
            "reason": "oauth_required",
            "message": _oauth_message(),
            "doc_id": _PROJECT_LOG_PATH,
        }
    # Authorized: return local doc path as doc_id
    return {
        "status": "ok",
        "doc_id": _PROJECT_LOG_PATH,
    }


def _append_to_log(content: str) -> None:
    """Helper to append content to the local project log file."""
    os.makedirs(os.path.dirname(_PROJECT_LOG_PATH), exist_ok=True)
    with open(_PROJECT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(content)


def append_section(doc_id: str, heading: str, markdown_or_struct: Any) -> Dict[str, Any]:
    """Append a section with heading and Markdown content to the document.

    If unauthorized, returns ``oauth_required``. Otherwise writes to the local
    project log.
    """
    token = _load_token()
    if token is None:
        return {
            "status": "parked",
            "reason": "oauth_required",
            "message": _oauth_message(),
        }
    # Compose Markdown content
    content = f"\n## {heading}\n\n"
    if isinstance(markdown_or_struct, str):
        content += markdown_or_struct + "\n"
    else:
        # Convert dicts/lists to JSON for simplicity
        import json as _json
        content += "``\n" + _json.dumps(markdown_or_struct, indent=2) + "\n``\n"
    _append_to_log(content)
    return {"status": "ok"}


def insert_table(doc_id: str, rows: List[List[str]]) -> Dict[str, Any]:
    """Insert a table into the document. Writes a Markdown table in fallback mode."""
    token = _load_token()
    if token is None:
        return {
            "status": "parked",
            "reason": "oauth_required",
            "message": _oauth_message(),
        }
    # Build Markdown table
    if not rows:
        return {"status": "ok"}
    header = " | ".join(rows[0])
    separator = " | ".join(["---"] * len(rows[0]))
    table_lines = ["| " + header + " |", "| " + separator + " |"]
    for row in rows[1:]:
        line = " | ".join(row)
        table_lines.append("| " + line + " |")
    _append_to_log("\n" + "\n".join(table_lines) + "\n")
    return {"status": "ok"}


def insert_image(doc_id: str, image_path_or_drive_id: str) -> Dict[str, Any]:
    """Insert an image into the document. In fallback mode, records a reference."""
    token = _load_token()
    if token is None:
        return {
            "status": "parked",
            "reason": "oauth_required",
            "message": _oauth_message(),
        }
    # Append a placeholder line referencing the image
    _append_to_log(f"\n![Image]({image_path_or_drive_id})\n")
    return {"status": "ok"}


def link_artifact(doc_id: str, title: str, href: str) -> Dict[str, Any]:
    """Insert a hyperlink to an artifact into the document."""
    token = _load_token()
    if token is None:
        return {
            "status": "parked",
            "reason": "oauth_required",
            "message": _oauth_message(),
        }
    _append_to_log(f"\n- [{title}]({href})\n")
    return {"status": "ok"}


def update_toc(doc_id: str) -> Dict[str, Any]:
    """Update the table of contents. No‑op in fallback mode."""
    token = _load_token()
    if token is None:
        return {
            "status": "parked",
            "reason": "oauth_required",
            "message": _oauth_message(),
        }
    # Table of contents management would require parsing the document.
    # For now, we simply return ok.
    return {"status": "ok"}