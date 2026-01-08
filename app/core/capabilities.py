# app/core/capabilities.py
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Set


def _env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Capabilities:
    """
    What this deployment can do (based on env/secrets available).
    """
    available: Set[str]

    def has(self, cap: str) -> bool:
        return cap in self.available


def detect_capabilities() -> Capabilities:
    caps: Set[str] = set()

    # Always available in MVP
    caps.add("sqlite")

    # Connectors (toggle by env for now)
    if _env_bool("HELIOS_GOOGLE_SHEETS_ENABLED", False):
        caps.add("google_sheets")

    if _env_bool("HELIOS_FREEDOMPAY_ENABLED", False):
        caps.add("payments_freedompay")

    return Capabilities(available=caps)
