# app/core/db/migrations.py

from __future__ import annotations

from .sqlite import SqliteDB


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL,
  tg_user_id INTEGER NOT NULL,
  tg_username TEXT,
  payload_json TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'new'
);

CREATE TABLE IF NOT EXISTS kv (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
"""


async def migrate(db: SqliteDB) -> None:
    conn = await db.connect()
    try:
        await conn.executescript(SCHEMA_SQL)
        await conn.commit()
    finally:
        await conn.close()
