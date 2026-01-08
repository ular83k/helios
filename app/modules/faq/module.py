#   app/modules/faq/module.py

from __future__ import annotations
from aiogram import Dispatcher

class FaqModule:
    name = "faq"

    def routes(self, dp: Dispatcher) -> None:
        pass

    def jobs(self):
        return []

    def admin_actions(self):
        return []

    def dependencies(self):
        return []

    def describe(self):
        return {"name": self.name, "desc": "FAQ/menu from YAML"}
