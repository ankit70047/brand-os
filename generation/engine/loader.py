"""Loader utilities for specs and constitution."""
from __future__ import annotations

import os
from typing import Any, Dict

import yaml

from shared.config_loader import load_constitution


def load_spec(path: str) -> Dict[str, Any]:
    """Load a YAML spec from the given path.

    Args:
        path: Path to spec file.

    Returns:
        Parsed spec as dictionary.
    """
    with open(path, "r", encoding="utf-8") as fh:
        spec = yaml.safe_load(fh) or {}
    spec.setdefault("input_dir", "generation/content/drafts")
    spec.setdefault("output_dir", "generation/content/generated")
    return spec


def resolve_first_draft(input_dir: str, pattern: str = "*.md") -> str | None:
    """Return first draft file path in the input directory or None.

    Args:
        input_dir: Directory to search.
        pattern: Glob-like pattern (supports suffix matching).
    """
    if not os.path.isdir(input_dir):
        return None
    for name in os.listdir(input_dir):
        if name.endswith(pattern.lstrip("*")):
            return os.path.join(input_dir, name)
    return None
