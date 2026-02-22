"""CLI entrypoint for the generation engine.

This module exposes `cli` for console_scripts.
"""
from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from typing import Any, Dict

import yaml

from shared.config_loader import load_constitution, setup_logging
from generation.engine.loader import load_spec, resolve_first_draft
from generation.engine.prompt_builder import build_prompt
from generation.engine.generator import mock_llm_call
from generation.engine.writer import write_outputs
from shared import db


def cli(argv: list[str] | None = None) -> int:
    """Command line interface for running the generation workflow.

    Args:
        argv: Optional list of arguments.

    Returns:
        exit status code.
    """
    parser = argparse.ArgumentParser(prog="brand-generate")
    parser.add_argument("--spec", required=True, help="Path to spec YAML file")
    parser.add_argument("--constitution", default="shared/constitution.yaml",
                        help="Path to constitution YAML")
    args = parser.parse_args(argv)

    # Load constitution and set up logging
    constitution = load_constitution(args.constitution)
    logger = setup_logging(constitution)
    # Ensure DB schema exists for analytics/publishing
    try:
        db.init_db()
        logger.info("Database initialized")
    except Exception:
        logger.exception("Failed to initialize database")
    logger.info("Starting generation run", extra={"spec": args.spec})

    # Load and validate spec
    try:
        spec = load_spec(args.spec)
        # validation via spec_executor is lightweight; imports here to avoid cycles
        from generation.engine.spec_executor import validate_spec

        validated = validate_spec(args.spec, args.constitution)
    except Exception as exc:  # pragma: no cover - top-level CLI handling
        logger.exception("Spec validation failed")
        return 2

    # Find a draft to process (only one at a time)
    draft_path = resolve_first_draft(validated.get("input_dir", ""))
    if not draft_path:
        logger.error("No draft found to process")
        return 3

    # Read draft content
    with open(draft_path, "r", encoding="utf-8") as fh:
        content = fh.read()

    # Load templates
    template_path = validated.get("template")
    if not os.path.isfile(template_path):
        logger.error("Template not found: %s", template_path)
        return 4
    with open(template_path, "r", encoding="utf-8") as fh:
        template_text = fh.read()

    # Load system role
    system_role_path = validated.get("system_role", "generation/templates/system_role.md")
    system_role = ""
    if os.path.isfile(system_role_path):
        with open(system_role_path, "r", encoding="utf-8") as fh:
            system_role = fh.read()

    # Build prompt
    prompt = build_prompt(template_text, system_role, content)

    # Call mock LLM
    outputs = mock_llm_call(
        prompt,
        model=validated.get("model", "openai-gpt-placeholder"),
        temperature=float(validated.get("temperature", 0.7)),
        max_tokens=int(validated.get("max_tokens", 1024)),
    )

    # Create slug from draft filename
    slug = Path(draft_path).stem
    write_outputs(validated.get("output_dir", "generation/content/generated"), slug, outputs)

    logger.info("Generation completed", extra={"slug": slug})
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
