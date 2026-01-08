# app/modules/registry.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Type

from .base import Module

#---- module registry ----
from app.modules.faq.module import FaqModule
from app.modules.leads.module import LeadsModule
#---- module registry ----








class RegistryError(RuntimeError):
    pass


@dataclass(frozen=True)
class LoadedModule:
    name: str
    instance: Module
    enabled: bool


class ModuleRegistry:
    """
    Keeps track of all available modules and loads enabled ones from config.
    """
    def __init__(self) -> None:
        self._available: Dict[str, Type] = {}

    def register(self, name: str, module_cls: Type) -> None:
        if name in self._available:
            raise RegistryError(f"Module already registered: {name}")
        self._available[name] = module_cls

    def available_names(self) -> List[str]:
        return sorted(self._available.keys())

    def load_from_flags(self, flags: Dict[str, bool]) -> List[LoadedModule]:
        loaded: List[LoadedModule] = []
        for name, cls in self._available.items():
            enabled = bool(flags.get(name, False))
            inst = cls()  # no deps yet; later we pass context
            loaded.append(LoadedModule(name=name, instance=inst, enabled=enabled))
        # Keep stable ordering
        loaded.sort(key=lambda x: x.name)
        return loaded


# ---- demo modules (temporary) ----
class FaqModule:
    name = "faq"
    def routes(self) -> None: ...
    def jobs(self): return []
    def admin_actions(self): return []
    def dependencies(self): return []
    def describe(self): return {"name": self.name, "desc": "FAQ/menu from YAML"}


class LeadsModule:
    name = "leads"
    def routes(self) -> None: ...
    def jobs(self): return []
    def admin_actions(self): return []
    def dependencies(self): return []
    def describe(self): return {"name": self.name, "desc": "Lead capture flows"}


def build_default_registry() -> ModuleRegistry:
    r = ModuleRegistry()
    r.register("faq", FaqModule)
    r.register("leads", LeadsModule)
    # later: booking, broadcast, tasks, crm_lite, payments, ai_copilot
    return r
