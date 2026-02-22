"""Minimal event tracker for analytics.

This implementation writes events to stdout (for debugging) and also records
events to the shared SQLite database so analytics can be queried later.
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from shared import db


def track_event(name: str, payload: dict | None = None) -> dict[str, Any]:
    payload = payload or {}
    event = {"name": name, "payload": payload, "timestamp": datetime.utcnow().isoformat()}
    # Write to stdout for visibility
    print(json.dumps(event))

    # Persist to SQLite
    try:
        conn = db.get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO analytics_events (event_type, payload) VALUES (?, ?)",
            (name, json.dumps(payload)),
        )
        conn.commit()
    finally:
        try:
            conn.close()
        except Exception:
            pass

    return {"status": "tracked", "event": event}


def cli() -> None:
    # Simple manual tracker CLI useful for local testing
    import argparse

    parser = argparse.ArgumentParser("brand-analytics")
    parser.add_argument("name", help="event name")
    parser.add_argument("--payload", help="json payload", default="{}")
    args = parser.parse_args()
    try:
        payload = json.loads(args.payload)
    except Exception:
        payload = {"raw": args.payload}
    track_event(args.name, payload)


if __name__ == "__main__":
    cli()
