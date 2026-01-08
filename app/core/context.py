# app/core/context.py

from __future__ import annotations

from dataclasses import dataclass
from aiogram import Bot

from app.core.db.sqlite import SqliteDB
from app.config.loader import AppConfig


@dataclass(frozen=True)
class RuntimeContext:
    bot: Bot
    db: SqliteDB
    config: AppConfig
