#!/usr/bin/env python3
"""Route raw files from 00_INBOX/USER_INTAKE into per-strategy source_intake/.

Reads everything under ``00_INBOX/USER_INTAKE`` (except README.md / .gitkeep),
matches each file to a strategy folder under ``03_QUANTLENS/strategies``, and
moves it into that strategy's ``source_intake/{transcripts|screenshots}/``.

Matching, in priority order:
  1. Filename begins with an existing ``STGxxx`` id  -> exact route.
  2. Token overlap between the filename and a strategy folder slug -> best match
     above a small threshold.
  3. No confident match -> reported as UNMATCHED (left in place; the agent
     should open a new candidate via the transcript intake workflow).

Image extensions go to ``screenshots/``; everything else to ``transcripts/``.

Default is a DRY RUN (prints the plan, moves nothing). Pass ``--apply`` to move.
Nothing is ever deleted; files only move inside the repository.

Usage:
    python 03_QUANTLENS/tools/route_user_intake.py            # dry-run
    python 03_QUANTLENS/tools/route_user_intake.py --apply    # perform moves
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

QUANTLENS_ROOT = Path(__file__).resolve().parents[1]
MCC_ROOT = QUANTLENS_ROOT.parent
INTAKE_DIR = MCC_ROOT / "00_INBOX" / "USER_INTAKE"
STRATEGIES_DIR = QUANTLENS_ROOT / "strategies"

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
IGNORE = {"readme.md", ".gitkeep"}
STOPWORDS = {"ql", "the", "and", "for", "with", "part", "transcript", "screenshot",
             "youtube", "video", "us", "any", "1h", "5m", "10m", "1d", "intraday"}
MATCH_THRESHOLD = 2  # minimum shared meaningful tokens for a fuzzy match


def _tokens(text: str) -> set[str]:
    raw = re.split(r"[^a-z0-9]+", text.lower())
    return {t for t in raw if t and t not in STOPWORDS and not t.isdigit()}


def _strategy_index() -> list[tuple[str, str, Path, set[str]]]:
    """Return (stg_id, folder_name, folder_path, slug_tokens) for each strategy."""
    index = []
    if not STRATEGIES_DIR.exists():
        return index
    for folder in sorted(STRATEGIES_DIR.iterdir()):
        if folder.is_dir() and folder.name.upper().startswith("STG"):
            stg_id = folder.name.split("_", 1)[0].upper()
            slug = re.sub(r"^STG\d+_", "", folder.name)
            slug = re.sub(r"^\d+_", "", slug)
            index.append((stg_id, folder.name, folder, _tokens(slug)))
    return index


def _match(filename: str, index) -> tuple[Path | None, str]:
    stem = Path(filename).stem
    # 1. explicit STG prefix
    m = re.match(r"(STG\d+)", stem, re.IGNORECASE)
    if m:
        target_id = m.group(1).upper()
        for stg_id, _name, path, _toks in index:
            if stg_id == target_id:
                return path, f"exact id {stg_id}"
    # 2. fuzzy token overlap
    ftoks = _tokens(stem)
    best, best_score = None, 0
    for _stg_id, _name, path, toks in index:
        score = len(ftoks & toks)
        if score > best_score:
            best, best_score = path, score
    if best is not None and best_score >= MATCH_THRESHOLD:
        return best, f"fuzzy match ({best_score} tokens)"
    return None, "no confident match"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="perform moves (default: dry-run)")
    args = parser.parse_args(argv)

    if not INTAKE_DIR.exists():
        print(f"intake dir not found: {INTAKE_DIR}")
        return 1

    index = _strategy_index()
    files = [p for p in sorted(INTAKE_DIR.iterdir())
             if p.is_file() and p.name.lower() not in IGNORE]

    if not files:
        print("USER_INTAKE is empty — nothing to route.")
        return 0

    unmatched = 0
    for f in files:
        target, reason = _match(f.name, index)
        kind = "screenshots" if f.suffix.lower() in IMAGE_EXT else "transcripts"
        if target is None:
            unmatched += 1
            print(f"UNMATCHED  {f.name}  ({reason}) -> open a new candidate (09_TRANSCRIPT_INTAKE_WORKFLOW)")
            continue
        dest_dir = target / "source_intake" / kind
        dest = dest_dir / f.name
        rel = dest.relative_to(MCC_ROOT).as_posix()
        if args.apply:
            dest_dir.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                print(f"SKIP       {f.name}  (already exists at {rel})")
                continue
            shutil.move(str(f), str(dest))
            print(f"MOVED      {f.name}  -> {rel}  [{reason}]")
        else:
            print(f"PLAN       {f.name}  -> {rel}  [{reason}]")

    if not args.apply:
        print("\nDRY RUN. Re-run with --apply to move files.")
    if unmatched:
        print(f"\n{unmatched} file(s) need a new candidate (no confident strategy match).")
    print("\nAfter applying: update the target strategy's source_intake/intake_report.md,")
    print("then re-run build_strategy_research_registry.py to refresh the dashboard.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
