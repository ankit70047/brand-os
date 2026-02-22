"""Spec executor: validates and enforces constitution rules on spec."""
from __future__ import annotations

import os
from typing import Any, Dict

from shared.config_loader import load_constitution
from shared.security import enforce_file_size_limit, sanitize_input


REQUIRED_SPEC_KEYS = ["model", "temperature", "input_dir", "output_dir", "template"]


def validate_spec(spec_path: str, constitution_path: str) -> Dict[str, Any]:
    """Load and validate spec against the constitution.

    Ensures required keys are present and numerical constraints enforced.

    Args:
        spec_path: Path to the spec YAML (already parsed by loader normally).
        constitution_path: Path to constitution YAML.

    Returns:
        The validated spec dict.

    Raises:
        ValueError: If validation fails.
    """
    import yaml

    with open(spec_path, "r", encoding="utf-8") as fh:
        spec = yaml.safe_load(fh) or {}

    for key in REQUIRED_SPEC_KEYS:
        if key not in spec:
            raise ValueError(f"Missing required spec key: {key}")

    constitution = load_constitution(constitution_path)

    # Enforce max tokens
    max_tokens_allowed = int(constitution.get("max_tokens_allowed", 2048))
    spec_max_tokens = int(spec.get("max_tokens", spec.get("max_tokens", 1024)))
    if spec_max_tokens > max_tokens_allowed:
        raise ValueError("Spec requests too many tokens per constitution")

    # Enforce input file size limits for files in input_dir
    input_dir = spec.get("input_dir")
    if os.path.isdir(input_dir):
        for name in os.listdir(input_dir):
            path = os.path.join(input_dir, name)
            if os.path.isfile(path):
                enforce_file_size_limit(path, constitution)

    # Sanitize template or other free text keys
    spec["template"] = sanitize_input(spec["template"], constitution)

    return spec
