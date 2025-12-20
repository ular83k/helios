# app/modules/base.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Protocol


@dataclass(frozen=True)
class AdminAction:
    """
    Placeholder for later Telegram admin UI.
    """
    id: str
    label: str


class Module(Protocol):
    """
    Module contract. Every module must implement this.
    """
    name: str

    def routes(self) -> None:
        """Register Telegram routes later."""
        ...

    def jobs(self) -> List[Any]:
        """Returnigger later (scheduler jobs)."""
        return []

    def admin_actions(self) -> List[AdminAction]:
        """Buttons / actions visible to admins later."""
        return []

    def dependencies(self) -> List[str]:
        """E.g. ['google_sheets']"""
        return []

    def describe(self) -> Dict[str, Any]:
        """Metadata for debugging/printing."""
        return {"name": self.name}
