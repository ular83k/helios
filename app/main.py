# app/main.py

from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

from aiogram import Dispatcher

from app.config.loader import get_client_name_from_env, load_client_config
from app.modules.registry import build_default_registry
from app.core.capabilities import detect_capabilities
from app.core.dependencies import validate_dependencies
from app.core.router import create_bot, create_dispatcher, register_core_routes

from app.core.db.sqlite import SqliteDB
from app.core.db.migrations import migrate
from app.core.context import RuntimeContext


async def run() -> None:
    client = get_client_name_from_env()
    cfg = load_client_config(client)

    registry = build_default_registry()
    loaded = registry.load_from_flags(cfg.modules)
    enabled = [m for m in loaded if m.enabled]

    caps = detect_capabilities()
    validate_dependencies(enabled, caps)

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    db_path = os.getenv("HELIOS_DB_PATH", "data/helios.sqlite3")
    db = SqliteDB(db_path)
    await migrate(db)

    bot = create_bot(token)
    dp: Dispatcher = create_dispatcher()
    register_core_routes(dp)

    ctx = RuntimeContext(client=client, config=cfg, caps=caps, db=db, bot=bot)

    for m in enabled:
        m.instance.routes(dp, ctx)

    print("HELIOS runtime started")
    await dp.start_polling(bot)


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
