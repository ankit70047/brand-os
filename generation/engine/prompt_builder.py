"""Prompt builder to assemble prompts from templates and content."""
from __future__ import annotations

from typing import Dict

import os


def build_prompt(template_text: str, system_role: str, content: str) -> str:
    """Build a final prompt string using template and content.

    Args:
        template_text: The transform template text.
        system_role: System role instructions.
        content: Draft content.

    Returns:
        The assembled prompt.
    """
    prompt = f"{system_role}\n\n{template_text.replace('{{{{content}}}}', content)}"
    return prompt
