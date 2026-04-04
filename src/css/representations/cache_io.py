from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

from css.common.io import ensure_dir, write_json


def save_hidden_cache(path: str | Path, payload: dict[str, Any]) -> None:
    p = Path(path)
    ensure_dir(p.parent)
    with p.open("wb") as f:
        pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_hidden_cache(path: str | Path) -> dict[str, Any]:
    with Path(path).open("rb") as f:
        data = pickle.load(f)
    if not isinstance(data, dict):
        raise ValueError("cache payload must be dict")
    return data


def write_cache_metadata(path: str | Path, payload: dict[str, Any]) -> None:
    write_json(path, payload)
