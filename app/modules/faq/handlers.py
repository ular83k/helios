#  app/modules/faq/handlers.py

from __future__ import annotations

from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config.loader import load_client_config, get_client_name_from_env
from .data import load_faq, FaqData
from app.core.tg_safe import safe_edit_text

CB_CAT = "faq:cat:"
CB_Q = "faq:q:"


def _get_faq_data() -> FaqData:
    cfg = load_client_config(get_client_name_from_env())
    faq_cfg = cfg.raw.get("faq", {})
    source = None
    if isinstance(faq_cfg, dict):
        source = faq_cfg.get("source")
    if not source:
        # Default fallback: no FAQ configured
        return FaqData(title="FAQ", categories=[])
    return load_faq(str(source))


def _kb_categories(data: FaqData):
    kb = InlineKeyboardBuilder()
    for c in data.categories:
        kb.button(text=c.title, callback_data=f"{CB_CAT}{c.id}")
    kb.adjust(1)
    return kb.as_markup()


def _kb_questions(cat_id: str, data: FaqData):
    kb = InlineKeyboardBuilder()
    cat = next((c for c in data.categories if c.id == cat_id), None)
    if not cat:
        return kb.as_markup()
    for idx, item in enumerate(cat.items):
        kb.button(text=item.q, callback_data=f"{CB_Q}{cat_id}:{idx}")
    kb.button(text="⬅ Back", callback_data=f"{CB_CAT}__back")
    kb.adjust(1)
    return kb.as_markup()


def register_faq(dp: Dispatcher) -> None:
    @dp.message(Command("faq"))
    async def faq_root(message: Message):
        data = _get_faq_data()
        if not data.categories:
            await message.answer("FAQ is not configured.")
            return
        await message.answer(data.title, reply_markup=_kb_categories(data))

    @dp.callback_query(lambda c: c.data and c.data.startswith(CB_CAT))
    async def faq_category(cb: CallbackQuery):
        data = _get_faq_data()
        payload = cb.data[len(CB_CAT):]

        if payload == "__back":
            await safe_edit_text(cb.message, data.title, reply_markup=_kb_categories(data))
            await cb.answer()
            return

        cat = next((c for c in data.categories if c.id == payload), None)
        if not cat:
            await cb.answer("Unknown category", show_alert=True)
            return

        await safe_edit_text(cb.message, cat.title, reply_markup=_kb_questions(cat.id, data))
        await cb.answer(cache_time=2)

    @dp.callback_query(lambda c: c.data and c.data.startswith(CB_Q))
    async def faq_question(cb: CallbackQuery):
        data = _get_faq_data()
        payload = cb.data[len(CB_Q):]  # cat_id:idx
        try:
            cat_id, idx_str = payload.split(":")
            idx = int(idx_str)
        except Exception:
            await cb.answer("Bad payload", show_alert=True)
            return

        cat = next((c for c in data.categories if c.id == cat_id), None)
        if not cat or idx < 0 or idx >= len(cat.items):
            await cb.answer("Not found", show_alert=True)
            return

        item = cat.items[idx]
        text = f"**{item.q}**\n\n{item.a}"
        await safe_edit_text(cb.message, text, reply_markup=_kb_questions(cat_id, data), parse_mode="Markdown")
        await cb.answer(cache_time=2)
