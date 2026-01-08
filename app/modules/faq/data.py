#  app/modules/faq/data.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

import yaml


class FaqError(RuntimeError):
    pass


@dataclass(frozen=True)
class FaqItem:
    q: str
    a: str


@dataclass(frozen=True)
class FaqCategory:
    id: str
    title: str
    items: List[FaqItem]


@dataclass(frozen=True)
class FaqData:
    title: str
    categories: List[FaqCategory]


def load_faq(path: str) -> FaqData:
    p = Path(path)
    if not p.exists():
        raise FaqError(f"FAQ file not found: {p}")

    try:
        raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception as e:
        raise FaqError(f"Failed to parse FAQ YAML: {p}: {e}") from e

    if not isinstance(raw, dict):
        raise FaqError("FAQ YAML root must be a mapping/object")

    title = str(raw.get("title", "FAQ"))
    cats = raw.get("categories", [])
    if not isinstance(cats, list):
        raise FaqError("FAQ YAML: 'categories' must be a list")

    categories: List[FaqCategory] = []
    for c in cats:
        if not isinstance(c, dict):
            continue
        cid = str(c.get("id", "")).strip()
        ctitle = str(c.get("title", "")).strip()
        if not cid or not ctitle:
            raise FaqError("Each category must have 'id' and 'title'")

        items_raw = c.get("items", [])
        if not isinstance(items_raw, list):
            raise FaqError(f"Category '{cid}': 'items' must be a list")

        items: List[FaqItem] = []
        for it in items_raw:
            if not isinstance(it, dict):
                continue
            q = str(it.get("q", "")).strip()
            a = str(it.get("a", "")).strip()
            if not q or not a:
                raise FaqError(f"Category '{cid}': each item must have 'q' and 'a'")
            items.append(FaqItem(q=q, a=a))

        categories.append(FaqCategory(id=cid, title=ctitle, items=items))

    return FaqData(title=title, categories=categories)
