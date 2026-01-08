# app/main.py
from __future__ import annotations

from app.config.loader import get_client_name_from_env, load_client_config
from app.modules.registry import build_default_registry

from app.core.capabilities import detect_capabilities
from app.core.dependencies import validate_dependencies


def main() -> None:
    client = get_client_name_from_env()
    cfg = load_client_config(client)

    registry = build_default_registry()
    loaded = registry.load_from_flags(cfg.modules)

    enabled = [m for m in loaded if m.enabled]
    disabled = [m for m in loaded if not m.enabled]

    caps = detect_capabilities()
    validate_dependencies(enabled, caps)

    print("HELIOS boot OK")
    print(f"Client: {cfg.client_name}")
    print(f"Capabilities: {sorted(list(caps.available))}")
    print(f"Available modules: {registry.available_names()}")
    print(f"Enabled modules: {[m.name for m in enabled]}")
    print(f"Disabled modules: {[m.name for m in disabled]}")



if __name__ == "__main__":
    main()
