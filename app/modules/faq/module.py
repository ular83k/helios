#   app/modules/faq/module.py

from __future__ import annotations

from aiogram import Dispatcher
from app.core.context import RuntimeContext
from .handlers import register_faq


class FaqModule:
    name = "faq"

    def routes(self, dp: Dispatcher, ctx: RuntimeContext) -> None:
        register_faq(dp)

    def jobs(self):
        return []

    def admin_actions(self):
        return []

    def dependencies(self):
        return []

    def describe(self):
        return {"name": self.name, "desc": "FAQ/menu from YAML"}

