# app/core/router.py

from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


def create_bot(token: str) -> Bot:
    return Bot(token=token)


def create_dispatcher() -> Dispatcher:
    return Dispatcher()


def register_core_routes(dp: Dispatcher) -> None:
    @dp.message(Command("start"))
    async def start_handler(message: Message):
        await message.answer("HELIOS online.")

    @dp.message(Command("admin"))
    async def admin_handler(message: Message):
        await message.answer("Admin panel (placeholder).")
