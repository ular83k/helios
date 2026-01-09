# app/modules/leads/repo.py

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.core.db.sqlite import SqliteDB


class LeadsRepo:
    def __init__(self, db: SqliteDB) -> None:
        self.db = db

    async def create_lead(
        self,
        tg_user_id: int,
        tg_username: Optional[str],
        payload: Dict[str, Any],
    ) -> int:
        conn = await self.db.connect()
        try:
            cur = await conn.execute(
                """
                INSERT INTO leads (created_at, tg_user_id, tg_username, payload_json, status)
                VALUES (?, ?, ?, ?, 'new')
                """,
                (
                    datetime.now(timezone.utc).isoformat(),
                    tg_user_id,
                    tg_username,
                    json.dumps(payload, ensure_ascii=False),
                ),
            )
            await conn.commit()
            return int(cur.lastrowid)
        finally:
            await conn.close()

