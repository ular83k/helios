#  app/core/tg_safe.py

from __future__ import annotations

from aiogram.exceptions import TelegramBadRequest


async def safe_edit_text(message, text: str, **kwargs) -> None:
    try:
        await message.edit_text(text, **kwargs)
    except TelegramBadRequest as e:
        # Happens when user taps same button again and nothing changes
        if "message is not modified" in str(e):
            return
        raise
