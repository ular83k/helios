# app/core/dependencies.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from app.core.capabilities import Capabilities


class DependencyError(RuntimeError):
    pass


@dataclass(frozen=True)
class DependencyIssue:
    module: str
    missing: List[str]


def validate_dependencies(enabled_modules: Iterable, caps: Capabilities) -> None:
    issues: List[DependencyIssue] = []

    for m in enabled_modules:
        req = list(getattr(m.instance, "dependencies")())
        missing = [d for d in req if not caps.has(d)]
        if missing:
            issues.append(DependencyIssue(module=m.name, missing=missing))

    if issues:
        lines = ["Dependency check failed:"]
        for iss in issues:
            lines.append(f"- module '{iss.module}' missing: {', '.join(iss.missing)}")
        lines.append("Fix: enable the capability via env or disable the module in client.yml.")
        raise DependencyError("\n".join(lines))
