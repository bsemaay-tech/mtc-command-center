from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent


def _resolve(path_like: str) -> Path:
    path = Path(path_like)
    if path.is_absolute():
        return path.resolve()
    return (PROJECT_ROOT / path).resolve()


def _load_json(path_like: str) -> dict[str, Any]:
    return json.loads(_resolve(path_like).read_text(encoding="utf-8"))


def _set_dot(cfg: dict[str, Any], key: str, value: Any) -> None:
    parts = key.split(".")
    cur = cfg
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    cur[parts[-1]] = value


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply candidate params onto a base case JSON.")
    ap.add_argument("--base-case", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--out-case", required=True)
    ap.add_argument("--tag", default="")
    args = ap.parse_args()

    case = _load_json(args.base_case)
    candidate = _load_json(args.candidate)
    params = candidate.get("params", {})
    if not isinstance(params, dict):
        raise SystemExit("Candidate file does not contain a params object.")

    cfg = case.setdefault("config", {})
    for key, value in params.items():
        _set_dot(cfg, str(key), value)

    case["_candidate_selection"] = {
        "candidate_file": str(_resolve(args.candidate)),
        "meta": candidate.get("meta", {}),
        "applied_params": params,
    }
    if args.tag:
        feature_flags = case.setdefault("feature_flags", {})
        feature_flags[f"materialized_candidate_{args.tag}"] = True

    out_path = _resolve(args.out_case)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(case, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"materialized_case={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
