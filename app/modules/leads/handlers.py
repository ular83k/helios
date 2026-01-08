# app/modules/leads/handlers.py

from __future__ import annotations

from typing import Dict, Any

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message

from app.config.loader import load_client_config, get_client_name_from_env
from app.core.db.sqlite import SqliteDB
from .repo import LeadsRepo


# naive per-process state (MVP). Later: move to DB-backed FSM.
_ACTIVE: Dict[int, Dict[str, Any]] = {}


def _cfg() -> Dict[str, Any]:
    cfg = load_client_config(get_client_name_from_env())
    leads_cfg = cfg.raw.get("leads", {})
    if not isinstance(leads_cfg, dict):
        return {"fields": []}
    return leads_cfg


async def _notify_admins(bot: Bot, text: str) -> None:
    leads_cfg = _cfg()
    ids = leads_cfg.get("notify_admin_ids", [])
    if not isinstance(ids, list):
        return
    for admin_id in ids:
        try:
            await bot.send_message(int(admin_id), text)
        except Exception:
            # ignore for MVP (later log)
            pass


def register_leads(dp: Dispatcher, db: SqliteDB) -> None:
    repo = LeadsRepo(db)

    @dp.message(Command("lead"))
    async def lead_start(message: Message):
        leads_cfg = _cfg()
        fields = leads_cfg.get("fields", [])
        if not fields:
            await message.answer("Lead form is not configured.")
            return

        _ACTIVE[message.from_user.id] = {
            "fields": fields,
            "i": 0,
            "data": {},
        }
        await message.answer(f"Let's start. Enter {fields[0]}:")

    @dp.message()
    async def lead_collect(message: Message, bot: Bot):
        st = _ACTIVE.get(message.from_user.id)
        if not st:
            return  # ignore unrelated messages for now

        fields = st["fields"]
        i = st["i"]
        data = st["data"]

        # save answer
        key = fields[i]
        data[key] = message.text.strip()

        i += 1
        if i >= len(fields):
            # finalize
            lead_id = await repo.create_lead(
                tg_user_id=message.from_user.id,
                tg_username=message.from_user.username,
                payload=data,
            )
            del _ACTIVE[message.from_user.id]

            summary = "\n".join([f"{k}: {v}" for k, v in data.items()])
            await message.answer(f"✅ Saved. Lead #{lead_id}\n\n{summary}")

            await _notify_admins(bot, f"📩 New lead #{lead_id}\nUser: @{message.from_user.username or '—'} ({message.from_user.id})\n\n{summary}")
            return

        # ask next
        st["i"] = i
        await message.answer(f"Enter {fields[i]}:")
