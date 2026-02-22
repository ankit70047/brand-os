"""Security helpers enforcing constitution rules and safe I/O."""
from __future__ import annotations

import os
import re
from typing import Any, Dict


def is_safe_filename(name: str) -> bool:
    """Return True if filename is safe (no traversal, simple chars).

    Allowed names contain letters, numbers, underscores, dashes and dot.
    """
    if ".." in name:
        return False
    return bool(re.match(r"^[A-Za-z0-9_.-]+$", name))


def ensure_safe_path(path: str) -> None:
    """Prevent path traversal by disallowing .. components.

    Raises:
        ValueError: If path contains traversal.
    """
    if ".." in os.path.normpath(path).split(os.path.sep):
        raise ValueError("Path traversal detected")


def enforce_file_size_limit(path: str, constitution: Dict[str, Any]) -> None:
    """Enforce max input file size from constitution.

    Raises ValueError when file is too large.
    """
    max_mb = int(constitution.get("max_input_file_size_mb", 5))
    if not os.path.isfile(path):
        return
    size_mb = os.path.getsize(path) / (1024 * 1024)
    if size_mb > max_mb:
        raise ValueError(f"File {path} exceeds allowed size ({size_mb:.2f} MB > {max_mb} MB)")


def mask_secrets(message: str, constitution: Dict[str, Any]) -> str:
    """Mask common secret-like patterns if logging_mask_secrets enabled.

    This is a conservative masker: hides 'key' values and long hex strings.
    """
    if not constitution.get("logging_mask_secrets", True):
        return message
    # Mask simple patterns like API keys and long hex
    masked = re.sub(r"(?i)(api[_-]?key\s*[:=]\s*)([A-Za-z0-9-_]{8,})", r"\1****", message)
    masked = re.sub(r"([A-Fa-f0-9]{32,})", "****", masked)
    return masked


def sanitize_input(text: str, constitution: Dict[str, Any]) -> str:
    """Sanitize free-text inputs to reduce prompt injection risk.

    This is intentionally minimal—strip <script> and control characters.
    """
    if not isinstance(text, str):
        return text
    sanitized = re.sub(r"<\/?script[^>]*>", "", text, flags=re.IGNORECASE)
    sanitized = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", sanitized)
    if constitution.get("restrict_prompt_injection", True):
        # Remove common instruction-like lines that try to override system role
        sanitized = re.sub(r"(?mi)^\s*ignore previous instructions.*$", "", sanitized)
    return sanitized
