"""Helper utilities used across modules."""
from typing import Any


def safe_get(mapping: dict, key: str, default: Any = None) -> Any:
    try:
        return mapping.get(key, default)
    except Exception:
        return default
