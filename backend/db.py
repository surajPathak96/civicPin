import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "civicpin.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                lat          REAL NOT NULL,
                lng          REAL NOT NULL,
                category     TEXT NOT NULL,
                severity     TEXT NOT NULL,
                description  TEXT NOT NULL DEFAULT '',
                photo_path   TEXT,
                status       TEXT NOT NULL DEFAULT 'open',
                report_count INTEGER NOT NULL DEFAULT 1,
                created_at   TEXT NOT NULL DEFAULT (datetime('now')),
                resolved_at  TEXT
            )
        """)