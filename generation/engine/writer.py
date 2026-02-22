"""Writer utilities to persist generated outputs safely."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict

from shared.security import is_safe_filename, ensure_safe_path


def write_outputs(base_output_dir: str, slug: str, outputs: Dict[str, str]) -> None:
    """Write generated outputs to disk under a slugged folder.

    Args:
        base_output_dir: Root output directory.
        slug: Subfolder name to write into.
        outputs: Mapping filename -> content.
    """
    out_dir = Path(base_output_dir) / slug
    ensure_safe_path(str(out_dir))
    out_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in outputs.items():
        if not is_safe_filename(filename):
            raise ValueError("Unsafe filename detected")
        target = out_dir / filename
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(content)
