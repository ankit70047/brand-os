"""Simple SQLite helper for the Brand OS monorepo.

Provides helpers to open and initialize a local sqlite database used by
analytics and publishing modules.
"""
from __future__ import annotations

from pathlib import Path
from typing import Union
import sqlite3

PathLike = Union[str, Path]


def get_db_path(root: PathLike = "data/brand_os.db") -> str:
    """Return an absolute filesystem path to the SQLite database file.

    Ensures the parent directory exists.
    """
    p = Path(root)
    parent = p.parent
    if parent and not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)
    return str(p.resolve())


def get_conn() -> sqlite3.Connection:
    """Open and return a sqlite3 Connection to the default DB path.

    Caller is responsible for closing the connection.
    """
    db_path = get_db_path()
    return sqlite3.connect(db_path)


def init_db() -> None:
    """Initialize the database schema used by the repo.

    Creates `analytics_events` and `published_items` tables if they do not exist.
    """
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS analytics_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                payload TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS published_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL,
                title TEXT,
                metadata TEXT,
                published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    finally:
        conn.close()
