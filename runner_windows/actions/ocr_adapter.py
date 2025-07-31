"""OCR adapter using Tesseract.

This module provides functions to capture images (placeholder implementation)
and extract text from images using Tesseract. If Tesseract is not installed,
the adapter returns a parked-like object indicating that OCR is unavailable.

The functions here are intentionally deterministic: they do not perform any
network calls and rely only on local resources. Evidence returned from OCR
reads contains the recognized text; failure cases include a reason field.
"""

from __future__ import annotations

import os
from typing import Dict, Optional, Tuple


def screenshot(region: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, str]:
    """Capture a screenshot of the current screen or a region.

    In this minimal implementation, screenshots are not supported and the function
    returns a parked object explaining that screenshot capture is unavailable.
    Future implementations may integrate with pyautogui or an OS‑specific API.

    Args:
        region: A tuple (x, y, width, height) defining the capture area.

    Returns:
        A dictionary with status 'parked' and an explanatory reason.
    """
    return {
        "status": "parked",
        "reason": "screenshot_unavailable",
        "note": "Screenshot capture is not implemented in this environment.",
    }


def read(image_path: str) -> Dict[str, str]:
    """Perform OCR on the given image file using pytesseract.

    Args:
        image_path: Path to the image file to process.

    Returns:
        On success: {'text': <extracted_text>}.
        On missing dependencies: {'status': 'parked', 'reason': 'tesseract_missing', 'note': ...}.
        On error: {'status': 'parked', 'reason': 'ocr_error', 'note': <error message>}.
    """
    # Ensure the file exists
    if not os.path.exists(image_path):
        return {
            "status": "parked",
            "reason": "file_not_found",
            "note": f"Image file {image_path} does not exist.",
        }
    try:
        import pytesseract  # type: ignore
        from PIL import Image  # type: ignore
    except ImportError:
        # Tesseract or PIL is not installed
        return {
            "status": "parked",
            "reason": "tesseract_missing",
            "note": "Tesseract OCR or PIL library is not installed.",
        }
    try:
        img = Image.open(image_path)
        # Normalize orientation and convert to RGB to improve OCR accuracy
        img = img.convert("RGB")
        text = pytesseract.image_to_string(img)
        return {"text": text.strip()}
    except Exception as exc:
        return {
            "status": "parked",
            "reason": "ocr_error",
            "note": str(exc),
        }