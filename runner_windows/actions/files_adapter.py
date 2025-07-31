"""File operations adapter.

Provides deterministic file operations for the runner. Functions return
simple dictionaries that can be embedded into evidence objects.
All paths are treated relative to the current working directory unless
an absolute path is provided.
"""

from __future__ import annotations

import hashlib
import os
import shutil
from typing import Union, Dict


def _ensure_parent_dir(path: str) -> None:
    """Ensure that the parent directory of ``path`` exists."""
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def write(path: str, data: Union[str, bytes]) -> Dict[str, str]:
    """Write text or bytes to a file and return evidence with path and hash.

    Args:
        path: The file path to write to.
        data: The string or bytes to write.

    Returns:
        A dictionary containing the file path and SHA256 hash of the written contents.
    """
    _ensure_parent_dir(path)
    # Determine mode based on data type
    if isinstance(data, bytes):
        mode = "wb"
        payload = data
    else:
        mode = "w"
        payload = data
    with open(path, mode, encoding=None if isinstance(data, bytes) else "utf-8") as f:
        f.write(payload)
    return {"path": path, "hash": hash_file(path)}


def read(path: str) -> Union[str, bytes]:
    """Read the contents of a file.

    If the file appears to be binary (contains null bytes), bytes are returned.
    Otherwise, a UTF‑8 string is returned. No evidence is produced here; use
    ``hash_file`` separately when needed.
    """
    with open(path, "rb") as f:
        data = f.read()
    # Heuristically decide if this is text
    if b"\x00" in data:
        return data
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data


def move(src: str, dst: str) -> Dict[str, str]:
    """Move a file from ``src`` to ``dst`` and return evidence with new path and hash."""
    _ensure_parent_dir(dst)
    shutil.move(src, dst)
    return {"path": dst, "hash": hash_file(dst)}


def hash_file(path: str) -> str:
    """Compute the SHA256 hash of the given file and return its hex digest."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()