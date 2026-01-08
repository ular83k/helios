# app/core/context.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from aiogram import Bot

from app.config.loader import AppConfig
from app.core.capabilities import Capabilities
from app.core.db.sqlite import SqliteDB


@dataclass(frozen=True)
class RuntimeContext:
    """
    Shared runtime objects that modules can use.
    """
    client: str
    config: AppConfig
    caps: Capabilities
    db: SqliteDB
    bot: Optional[Bot] = None  # set after bot is created

