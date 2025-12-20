# app/config/loader.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
import os

import yaml


class ConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class AppConfig:
    client_name: str
    raw: Dict[str, Any]

    @property
    def modules(self) -> Dict[str, bool]:
        mods = self.raw.get("modules", {})
        if not isinstance(mods, dict):
            raise ConfigError("client.yml: 'modules' must be a dict")
        # normalize truthy values
        out: Dict[str, bool] = {}
        for k, v in mods.items():
            out[str(k)] = bool(v)
        return out


def load_client_config(client_name: str, base_dir: str | Path | None = None) -> AppConfig:
    """
    Loads app/config/clients/<client_name>.yml
    """
    base = Path(base_dir) if base_dir else Path(__file__).resolve().parent
    clients_dir = base / "clients"
    path = clients_dir / f"{client_name}.yml"

    if not path.exists():
        raise ConfigError(f"Client config not found: {path}")

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        raise ConfigError(f"Failed to parse YAML: {path}: {e}") from e

    if not isinstance(data, dict):
        raise ConfigError(f"client.yml must be a mapping/object at root: {path}")

    return AppConfig(client_name=client_name, raw=data)


def get_client_name_from_env() -> str:
    name = os.getenv("HELIOS_CLIENT", "demo").strip()
    if not name:
        raise ConfigError("HELIOS_CLIENT is empty")
    return name
