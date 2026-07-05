"""Faz 3b self-parity gate (D013).

Captures golden result rows from the CURRENT engine on a pinned cell set, and
verifies any future engine against them. The Faz 3b exit_mode change may NOT
land unless `--verify` passes byte-identically with exit_mode=fixed_2R.

Usage:
  python faz3b_self_parity.py --capture   # run BEFORE editing the engine
  python faz3b_self_parity.py --verify    # gate: run AFTER any engine edit

Read-only w.r.t. the engine; runs it as a subprocess on the primary bundle.
Authorized by D013 (implementation + self-parity regression only).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parents[2]
ENGINE = TOOLS_DIR / "mega_walk_forward.py"
BUNDLE_MANIFEST = (
    TOOLS_DIR.parent
    / "data"
    / "native_multiasset_alpaca_2026-06-28"
    / "manifests"
    / "dataset_manifest.json"
)
GOLDEN_DIR = TOOLS_DIR / "tests" / "goldens" / "faz3b"
GOLDEN_FILE = GOLDEN_DIR / "golden_cells.json"

TRAIL_STRATEGY = "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL"
PINNED_SYMBOLS = ["SPY", "QQQ", "BTCUSD"]
PINNED_TFS = ["1h", "4h"]
N_OTHER_STRATEGIES = 6

VOLATILE_KEYS = {
    "runtime",
    "runtime_s",
    "runtime_sec",
    "elapsed",
    "elapsed_s",
    "timestamp",
    "generated_at",
    "created_at",
    "worker",
    "workers",
    "worker_count",
    "started",
    "started_at",
    "finished",
    "finished_at",
    "duration",
    "checkpoint",
    "output_dir",
    "partial_json",
}

# Faz 3b (D013): fields the new engine ALWAYS adds. Stripped during
# canonicalization so fixed_2R output stays byte-identical to the pre-edit
# golden. Goldens are NOT recaptured.
# D015 (Codex Gate-5 edit #4): grid_stride is assert-then-strip — every default
# row must prove grid_stride == 1 BEFORE the field may be stripped (see
# extract_rows), so a default-mode trim bug fails the gate instead of hiding.
ALLOWED_NEW_KEYS = {"exit_mode", "engine_version", "grid_stride"}


def pinned_strategies() -> list[str]:
    sys.path.insert(0, str(TOOLS_DIR))
    import mega_walk_forward as mw  # safe: argparse lives inside main()

    others = sorted(k for k in mw.GRIDS if k != TRAIL_STRATEGY)[:N_OTHER_STRATEGIES]
    return others + [TRAIL_STRATEGY]


def strip_volatile(obj):
    if isinstance(obj, dict):
        return {
            k: strip_volatile(v)
            for k, v in sorted(obj.items())
            if k not in VOLATILE_KEYS and k not in ALLOWED_NEW_KEYS
        }
    if isinstance(obj, list):
        return [strip_volatile(v) for v in obj]
    return obj


def extract_rows(results_path: Path) -> list[dict]:
    data = json.loads(results_path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = data.get("results")
        if rows is None:
            lists = [v for v in data.values() if isinstance(v, list)]
            rows = max(lists, key=len) if lists else []
    else:
        rows = []
    # Faz 3b (D013): the gate must only ever run in default mode. Prove it before
    # canonicalization strips the field — any non-fixed_2R row means the sweep
    # axis leaked into the parity run and the byte-identity claim is void.
    for r in rows:
        if isinstance(r, dict) and "exit_mode" in r:
            assert r["exit_mode"] == "fixed_2R", (
                f"self-parity must run default exit_mode=fixed_2R; "
                f"got {r['exit_mode']!r} for "
                f"{r.get('strategy')}|{r.get('symbol')}|{r.get('tf', r.get('timeframe'))}"
            )
        # D015 (Codex edit #4): prove full grid BEFORE the field is stripped —
        # a default-mode bug that silently trims the grid must FAIL the gate.
        if isinstance(r, dict) and "grid_stride" in r:
            assert r["grid_stride"] == 1, (
                f"self-parity must run full grid (grid_stride=1); "
                f"got {r['grid_stride']!r} for "
                f"{r.get('strategy')}|{r.get('symbol')}|{r.get('tf', r.get('timeframe'))}"
            )
    rows = [strip_volatile(r) for r in rows if isinstance(r, dict)]
    rows.sort(
        key=lambda r: (
            str(r.get("strategy", "")),
            str(r.get("symbol", "")),
            str(r.get("tf", r.get("timeframe", ""))),
        )
    )
    return rows


def run_engine(workdir: Path, strategies: list[str]) -> Path:
    if not BUNDLE_MANIFEST.exists():
        sys.exit(f"FATAL: bundle manifest missing: {BUNDLE_MANIFEST}")
    env = dict(os.environ)
    env["MEGA_BUNDLE_MANIFEST"] = str(BUNDLE_MANIFEST)
    env["MEGA_OUTPUT_DIR"] = str(workdir)
    cmd = [sys.executable, str(ENGINE)]
    for s in strategies:
        cmd += ["--strategy", s]
    for s in PINNED_SYMBOLS:
        cmd += ["--symbol", s]
    for t in PINNED_TFS:
        cmd += ["--tf", t]
    print(f"[self-parity] running engine on {len(strategies)} strategies x "
          f"{PINNED_SYMBOLS} x {PINNED_TFS} ...")
    proc = subprocess.run(cmd, env=env, cwd=str(TOOLS_DIR), timeout=1800,
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stdout[-3000:])
        print(proc.stderr[-3000:])
        sys.exit(f"FATAL: engine exited {proc.returncode}")
    results = workdir / "MEGA_walk_forward_results.json"
    if not results.exists():
        candidates = list(workdir.glob("*results*.json"))
        if not candidates:
            sys.exit(f"FATAL: no results json under {workdir}")
        results = candidates[0]
    return results


def rows_digest(rows: list[dict]) -> str:
    blob = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--capture", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    strategies = pinned_strategies()
    with tempfile.TemporaryDirectory(prefix="faz3b_parity_") as td:
        workdir = Path(td)
        results = run_engine(workdir, strategies)
        rows = extract_rows(results)

    if not rows:
        sys.exit("FATAL: engine produced zero result rows; pinned set invalid")
    digest = rows_digest(rows)

    if args.capture:
        GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
        GOLDEN_FILE.write_text(
            json.dumps(
                {
                    "banner": "FAZ3B SELF-PARITY GOLDEN (D013) - engine regression gate",
                    "pinned_strategies": strategies,
                    "pinned_symbols": PINNED_SYMBOLS,
                    "pinned_tfs": PINNED_TFS,
                    "row_count": len(rows),
                    "rows_sha256": digest,
                    "rows": rows,
                },
                indent=1,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"[self-parity] CAPTURED {len(rows)} rows sha256={digest[:16]}... "
              f"-> {GOLDEN_FILE}")
        return

    golden = json.loads(GOLDEN_FILE.read_text(encoding="utf-8"))
    if digest == golden["rows_sha256"] and len(rows) == golden["row_count"]:
        print(f"[self-parity] PASS - {len(rows)} rows match golden "
              f"sha256={digest[:16]}...")
        return
    print(f"[self-parity] FAIL - golden {golden['row_count']} rows "
          f"{golden['rows_sha256'][:16]}..., got {len(rows)} rows {digest[:16]}...")
    gold_rows = golden["rows"]
    for i, (g, n) in enumerate(zip(gold_rows, rows)):
        if g != n:
            print(f"first differing row index {i}: "
                  f"{g.get('strategy')}|{g.get('symbol')}|{g.get('tf')}")
            break
    sys.exit(1)


if __name__ == "__main__":
    main()
