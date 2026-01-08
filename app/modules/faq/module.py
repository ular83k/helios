#   app/modules/faq/module.py

from __future__ import annotations

class FaqModule:
    name = "faq"

    def routes(self) -> None:
        ...

    def jobs(self):
        return []

    def admin_actions(self):
        return []

    def dependencies(self):
        return []

    def describe(self):
        return {"name": self.name, "desc": "FAQ/menu from YAML"}
