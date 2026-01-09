# app/modules/leads/handlers.py

from __future__ import annotations

from typing import Any, Dict, List

from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from app.core.context import RuntimeContext
from .repo import LeadsRepo


# In-memory per-user state (MVP)
_ACTIVE: Dict[int, Dict[str, Any]] = {}


def _get_leads_cfg(ctx: RuntimeContext) -> Dict[str, Any]:
    raw = ctx.config.raw.get("leads", {})
    return raw if isinstance(raw, dict) else {}


def _get_fields(ctx: RuntimeContext) -> List[str]:
    cfg = _get_leads_cfg(ctx)
    fields = cfg.get("fields", [])
    if not isinstance(fields, list):
        return []
    return [str(f).strip() for f in fields if str(f).strip()]


def _format_summary(data: Dict[str, Any]) -> str:
    lines = []
    for k, v in data.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)


async def _notify_admins(ctx: RuntimeContext, text: str) -> None:
    if not ctx.bot:
        return
    cfg = _get_leads_cfg(ctx)
    ids = cfg.get("notify_admin_ids", [])
    if not isinstance(ids, list):
        return
    for admin_id in ids:
        try:
            await ctx.bot.send_message(int(admin_id), text)
        except Exception:
            # MVP: ignore failures (later: log)
            pass


def register_leads(dp: Dispatcher, ctx: RuntimeContext) -> None:
    repo = LeadsRepo(ctx.db)

    @dp.message(Command("lead"))
    async def lead_start(message: Message):
        fields = _get_fields(ctx)
        if not fields:
            await message.answer("Lead form is not configured.")
            return

        _ACTIVE[message.from_user.id] = {
            "fields": fields,
            "i": 0,
            "data": {},
        }
        await message.answer(f"Let's start. Enter {fields[0]}:")

    @dp.message(Command("cancel"))
    async def lead_cancel(message: Message):
        if message.from_user.id in _ACTIVE:
            _ACTIVE.pop(message.from_user.id, None)
            await message.answer("Cancelled.")
        else:
            await message.answer("Nothing to cancel.")

    @dp.message()
    async def lead_collect(message: Message):
        st = _ACTIVE.get(message.from_user.id)
        if not st:
            return  # ignore unrelated messages

        text = (message.text or "").strip()
        if not text:
            await message.answer("Please send text.")
            return

        fields: List[str] = st["fields"]
        i: int = st["i"]
        data: Dict[str, Any] = st["data"]

        key = fields[i]
        data[key] = text

        i += 1
        if i >= len(fields):
            lead_id = await repo.create_lead(
                tg_user_id=message.from_user.id,
                tg_username=message.from_user.username,
                payload=data,
            )
            _ACTIVE.pop(message.from_user.id, None)

            summary = _format_summary(data)
            await message.answer(f"✅ Saved. Lead #{lead_id}\n\n{summary}")

            who = f"@{message.from_user.username}" if message.from_user.username else "—"
            await _notify_admins(
                ctx,
                f"📩 New lead #{lead_id}\nUser: {who} ({message.from_user.id})\n\n{summary}",
            )
            return

        st["i"] = i
        await message.answer(f"Enter {fields[i]}:")

