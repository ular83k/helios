#  app/modules/leads/module.py

from __future__ import annotations

from aiogram import Dispatcher
from app.core.context import RuntimeContext


class LeadsModule:
    name = "leads"

    def routes(self, dp: Dispatcher, ctx: RuntimeContext) -> None:
        # handlers wired in next commit
        pass

    def jobs(self):
        return []

    def admin_actions(self):
        return []

    def dependencies(self):
        return []

    def describe(self):
        return {"name": self.name, "desc": "Lead capture flows"}

