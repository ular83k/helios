#  app/modules/leads/module.py

from __future__ import annotations
from aiogram import Dispatcher

class LeadsModule:
    name = "leads"

    def routes(self, dp: Dispatcher) -> None:
        pass

    def jobs(self):
        return []

    def admin_actions(self):
        return []

    def dependencies(self):
        return []

    def describe(self):
        return {"name": self.name, "desc": "Lead capture flows"}

