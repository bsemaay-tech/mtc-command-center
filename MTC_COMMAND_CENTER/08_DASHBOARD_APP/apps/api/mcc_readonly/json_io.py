from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class JsonReadResult:
    rel_path: str
    path: Path
    required: bool
    exists: bool
    ok: bool
    data: Any | None
    error: str | None


def read_json_file(mcc_root: Path, rel_path: str, required: bool = True) -> JsonReadResult:
    path = mcc_root / rel_path
    if not path.exists():
        if required:
            return JsonReadResult(rel_path, path, required, False, False, None, "required file is missing")
        return JsonReadResult(rel_path, path, required, False, True, None, None)

    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except UnicodeDecodeError as exc:
        return JsonReadResult(rel_path, path, required, True, False, None, f"utf-8 decode error: {exc}")
    except json.JSONDecodeError as exc:
        return JsonReadResult(rel_path, path, required, True, False, None, f"json parse error: {exc}")
    except OSError as exc:
        return JsonReadResult(rel_path, path, required, True, False, None, f"read error: {exc}")

    return JsonReadResult(rel_path, path, required, True, True, data, None)

