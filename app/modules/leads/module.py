#  app/modules/leads/module.py

from __future__ import annotations

from aiogram import Dispatcher

from app.core.context import RuntimeContext
from .handlers import register_leads


class LeadsModule:
    name = "leads"

    def routes(self, dp: Dispatcher, ctx: RuntimeContext) -> None:
        register_leads(dp, ctx)

    def jobs(self):
        return []

    def admin_actions(self):
        return []

    def dependencies(self):
        # DB is always present in MVP
        return ["sqlite"]

    def describe(self):
        return {"name": self.name, "desc": "Lead capture flows"}


