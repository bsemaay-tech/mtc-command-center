#!/usr/bin/env python3
"""State helper for the bulk re-triage of 11_TRIAGE eligible candidates.

Keeps `11_TRIAGE/retriage_progress.json` as the resumable ledger so the work
survives context resets. Subcommands:

  next                         -> print next pending: stg, md path, candidate_id, url
  status                       -> counts + disposition breakdown
  allocstg                     -> print next free STG number and increment it
  commit --stg S --disp D --output P
                               -> mark S done with disposition D and output path P
                                  (also appends a row to the dispositions log)

Dispositions: CANDIDATE | WIKI_ONLY | SALVAGE | DUPLICATE
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MCC_ROOT = Path(__file__).resolve().parents[2]
LEDGER = MCC_ROOT / "11_TRIAGE" / "retriage_progress.json"
DISPO = MCC_ROOT / "11_TRIAGE" / "retriage_dispositions_2026-06-04.md"


def _load():
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def _save(d):
    LEDGER.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("next")
    sub.add_parser("status")
    sub.add_parser("allocstg")
    c = sub.add_parser("commit")
    c.add_argument("--stg", required=True)
    c.add_argument("--disp", required=True)
    c.add_argument("--output", required=True)
    c.add_argument("--note", default="")
    args = p.parse_args(argv)
    d = _load()

    if args.cmd == "next":
        for it in d["items"]:
            if it["status"] == "pending":
                print(json.dumps({"stg": it["stg"], "md": f"11_TRIAGE/strategies/{it['md_file']}",
                                  "candidate_id": it["candidate_id"], "url": it["url"],
                                  "quality": it["quality"]}, ensure_ascii=False))
                return 0
        print("ALL_DONE")
        return 0

    if args.cmd == "status":
        done = [it for it in d["items"] if it["status"] == "done"]
        pend = [it for it in d["items"] if it["status"] == "pending"]
        from collections import Counter
        disp = Counter(it["disposition"] for it in done)
        print(f"done={len(done)} pending={len(pend)} next_stg=STG{d['next_stg']:03d}")
        print("dispositions:", dict(disp))
        return 0

    if args.cmd == "allocstg":
        n = d["next_stg"]
        d["next_stg"] = n + 1
        _save(d)
        print(f"STG{n:03d}")
        return 0

    if args.cmd == "commit":
        found = False
        for it in d["items"]:
            if it["stg"] == args.stg:
                it["status"] = "done"
                it["disposition"] = args.disp
                it["output"] = args.output
                found = True
                break
        if not found:
            print(f"ERROR: {args.stg} not in ledger")
            return 1
        _save(d)
        row = f"| {args.stg} | {args.disp} | {args.output} | {args.note} |\n"
        if not DISPO.exists() or "## Bulk re-triage log" not in DISPO.read_text(encoding="utf-8"):
            with DISPO.open("a", encoding="utf-8") as f:
                f.write("\n## Bulk re-triage log (RESEARCH-004)\n\n")
                f.write("| Stg | Disposition | Output | Note |\n|---|---|---|---|\n")
        with DISPO.open("a", encoding="utf-8") as f:
            f.write(row)
        print(f"committed {args.stg} -> {args.disp}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
