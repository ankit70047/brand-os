"""Logging configuration helpers with secret masking."""
from __future__ import annotations

import logging
from typing import Any, Dict

from .security import mask_secrets


class MaskingFilter(logging.Filter):
    """Log filter that masks secrets in messages."""

    def __init__(self, constitution: Dict[str, Any]):
        super().__init__()
        self.constitution = constitution

    def filter(self, record: logging.LogRecord) -> bool:  # type: ignore[override]
        if hasattr(record, "msg") and isinstance(record.msg, str):
            record.msg = mask_secrets(record.msg, self.constitution)
        return True


def setup_logging(constitution: Dict[str, Any]) -> logging.Logger:
    """Configure and return a root logger respecting constitution.

    Args:
        constitution: Parsed constitution dict.

    Returns:
        Configured logger.
    """
    level = logging.INFO
    logger = logging.getLogger("brand-os")
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
        handler.addFilter(MaskingFilter(constitution))
        logger.addHandler(handler)
    return logger
