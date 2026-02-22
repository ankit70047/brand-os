"""Configuration loader helpers for constitution and configs."""
from __future__ import annotations

import os
import yaml
from typing import Any, Dict

from .logging_config import setup_logging


def load_constitution(path: str = "shared/constitution.yaml") -> Dict[str, Any]:
    """Load the constitution YAML file.

    Args:
        path: Path to constitution file.

    Returns:
        Parsed constitution as dictionary.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Constitution not found: {path}")
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def setup_logging(constitution: Dict[str, Any]):
    """Return a configured logger using the provided constitution.

    Args:
        constitution: Parsed constitution dict.

    Returns:
        The root logger instance.
    """
    return setup_logging(constitution)
