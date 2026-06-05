#!/usr/bin/env python3
"""
score_all_gates.py — SP-004 Phase 3 UNIFIED composer (Gate1 + Gate1B + Gate2 + Gate3).

Read-only consumer: merges four gate scorers into ONE scorecard_v2 per strategy.
NO Pine/parity/MTC/trading change. NEVER git/commit.

Usage:
  python score_all_gates.py --in-dir <dir_of_.json> --out-dir <dir>
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# MODULE LOADING (same-dir siblings, no package assumption)
# ---------------------------------------------------------------------------

def _load(modname: str):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), modname + '.py')
    spec = importlib.util.spec_from_file_location(modname, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_G1 = _load('score_gate1')
_G1B = _load('score_gate1b')
_G2 = _load('score_gate2')
_G3 = _load('score_gate3')


# ---------------------------------------------------------------------------
# PURE FUNCTION
# ---------------------------------------------------------------------------

def score_all_gates(artifact: dict) -> dict:
    r1 = _G1.score_gate1(artifact)
    r1b = _G1B.score_gate1b(artifact)
    r2 = _G2.score_gate2(artifact)
    r3 = _G3.score_gate3(artifact)

    sid = artifact.get('strategy_id', 'UNKNOWN')
    parity = (artifact.get('flags') or {}).get('parity_status', 'N_A')

    g1 = r1['gate1']
    g1b = r1b['gate1B']
    g2 = r2['gate2']
    g3 = r3['gate3']

    statuses = {
        'gate1': g1['status'],
        'gate1B': g1b['status'],
        'gate2': g2['status'],
        'gate3': g3['status'],
    }

    all_pass = bool(
        g1.get('pass') and g1b.get('pass') and g2.get('pass') and g3.get('pass')
    )

    blocking = [
        name for name, st in statuses.items()
        if st in ('FAIL', 'INCOMPLETE')
    ]

    # promotable = all four OK + pass (parity advisory, never blocks)
    promotable = (
        all_pass
        and all(st == 'OK' for st in statuses.values())
    )

    return {
        'strategy_id': sid,
        'scorecard_version': 'v2',
        'gate1': g1,
        'gate1B': g1b,
        'gate2': g2,
        'gate3': g3,
        'flags': {'parity_status': parity},
        'notes': r1['notes'] + r1b['notes'] + r2['notes'] + r3['notes'],
        'gate_summary': {
            'statuses': statuses,
            'all_pass': all_pass,
            'promotable': promotable,
            'blocking': blocking,
        },
    }


# ---------------------------------------------------------------------------
# HELPERS (copied identically)
# ---------------------------------------------------------------------------

def _sanitize_filename(name: str) -> str:
    """Replace characters unsafe for filenames."""
    return re.sub(r"[^a-zA-Z0-9_\-.]", "_", name)


# ---------------------------------------------------------------------------
# CLI main()
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    ap = argparse.ArgumentParser(
        description="SP-004 Phase 3: Unified Gate1+1B+2+3 composer"
    )
    ap.add_argument("--in-dir", required=True, help="Directory containing *.json artifacts")
    ap.add_argument("--out-dir", required=True, help="Directory to write *.scorecard.json")
    args = ap.parse_args(argv)

    in_dir = os.path.abspath(args.in_dir)
    out_dir = os.path.abspath(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)

    artifacts: List[str] = []
    for fname in sorted(os.listdir(in_dir)):
        if fname.endswith(".json"):
            artifacts.append(os.path.join(in_dir, fname))

    if not artifacts:
        print("[score_all_gates] WARNING: No .json files found in %s" % in_dir)
        return

    promotable_count = 0
    not_promotable_count = 0

    for fpath in artifacts:
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                artifact = json.load(fh)
        except (json.JSONDecodeError, IOError) as exc:
            print("[score_all_gates] SKIP %s: %s" % (os.path.basename(fpath), exc))
            continue

        merged = score_all_gates(artifact)

        sid = merged.get("strategy_id", "unknown")
        safe = _sanitize_filename(sid)
        out_path = os.path.join(out_dir, safe + ".scorecard.json")

        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(merged, fh, indent=2, default=str)

        gs = merged["gate_summary"]
        statuses = gs["statuses"]
        prom = gs["promotable"]

        if prom:
            promotable_count += 1
        else:
            not_promotable_count += 1

        print(
            "[score_all_gates] %s  g1=%-11s g1b=%-11s g2=%-11s g3=%-11s  promotable=%s  → %s"
            % (
                sid,
                statuses["gate1"],
                statuses["gate1B"],
                statuses["gate2"],
                statuses["gate3"],
                str(prom),
                os.path.basename(out_path),
            )
        )

    print(
        "\n[score_all_gates] SUMMARY — promotable=%d  not_promotable=%d  (of %d artifacts)"
        % (promotable_count, not_promotable_count, len(artifacts))
    )


if __name__ == "__main__":
    main()
