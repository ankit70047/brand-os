"""Simple publisher stub with a CLI entrypoint.

This is intentionally minimal — it provides an interface for posting
content to external services. It also records published items in the
shared SQLite DB for auditing.
"""
from __future__ import annotations

import argparse
import uuid
from typing import Any

from shared import db


def publish(content: str, destination: str = "console", title: str | None = None) -> dict[str, Any]:
    """Publish content to a destination (stub) and record it in the DB.

    Returns a dict with publish result metadata.
    """
    item_id = str(uuid.uuid4())
    if destination == "console":
        print("--- PUBLISH (console) ---")
        print(content)
        status = "ok"
    else:
        # Placeholder for real adapters
        status = "not_implemented"

    # Record metadata in the DB
    try:
        conn = db.get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO published_items (item_id, title, metadata) VALUES (?, ?, ?)",
            (item_id, title or "", str({"destination": destination, "status": status})),
        )
        conn.commit()
    finally:
        try:
            conn.close()
        except Exception:
            pass

    return {"status": status, "destination": destination, "item_id": item_id}


def cli() -> None:
    parser = argparse.ArgumentParser("brand-publish")
    parser.add_argument("--destination", "-d", default="console")
    parser.add_argument("--content", "-c", required=True)
    parser.add_argument("--title", "-t", default=None)
    args = parser.parse_args()
    publish(args.content, args.destination, args.title)


if __name__ == "__main__":
    cli()
