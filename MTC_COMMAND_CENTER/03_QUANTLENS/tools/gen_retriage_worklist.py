#!/usr/bin/env python3
"""Emit a prioritized re-triage worklist (Markdown) from the triage registry.

Lists triage candidates that are eligible_for_retriage (transcript present +
HIGH/MEDIUM quality) so they can be re-evaluated into matured QuantLens
strategies. Run after build_triage_registry.py.

Usage: python 03_QUANTLENS/tools/gen_retriage_worklist.py
"""
from __future__ import annotations

import datetime
import json
from pathlib import Path

MCC_ROOT = Path(__file__).resolve().parents[2]
REG = MCC_ROOT / "05_REGISTRY" / "TRIAGE_CANDIDATE_REGISTRY.json"


def main() -> int:
    data = json.loads(REG.read_text(encoding="utf-8"))
    elig = [c for c in data["candidates"] if c.get("eligible_for_retriage")]
    elig.sort(key=lambda x: (x.get("source_quality") != "HIGH", str(x.get("stg_code"))))
    today = datetime.date.today().isoformat()
    n_high = sum(1 for x in elig if x.get("source_quality") == "HIGH")
    n_med = sum(1 for x in elig if x.get("source_quality") == "MEDIUM")

    lines = [
        f"# Re-Triage Worklist - {today}",
        "",
        "Candidates previously rejected for **missing transcript** that now have a "
        "transcript on disk and are HIGH/MEDIUM quality. Ready to re-evaluate into "
        "matured QuantLens strategies via the transcript intake workflow "
        "(`03_QUANTLENS/_user_guide/09_TRANSCRIPT_INTAKE_WORKFLOW.md`).",
        "",
        f"**{len(elig)} eligible** ({n_high} HIGH, {n_med} MEDIUM). Live source: "
        "`05_REGISTRY/TRIAGE_CANDIDATE_REGISTRY.json` "
        "(regen: `python 03_QUANTLENS/tools/build_triage_registry.py`).",
        "",
        "| # | done | Stg | Quality | Title | Transcript | URL |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, x in enumerate(elig, 1):
        title = (str(x.get("title") or ""))[:70].replace("|", "/")
        lines.append(
            f"| {i} | [ ] | {x.get('stg_code')} | {x.get('source_quality')} | "
            f"{title} | {x.get('transcript_path') or ''} | {x.get('source_url') or ''} |"
        )
    lines += [
        "",
        "## How to process (per row, in batches)",
        "1. Read the transcript md; extract a deterministic strategy spec.",
        "2. Create `03_QUANTLENS/strategies/STGxxx_<slug>/` with "
        "`01_candidate_metadata.yaml`, `07_deterministic_spec.md`, and copy the "
        "transcript into `source_intake/transcripts/`.",
        "3. Re-run `build_strategy_research_registry.py` (refreshes Strategy Research Lab).",
        "4. Tick the `done` box for the processed row.",
    ]
    out = MCC_ROOT / "11_TRIAGE" / f"retriage_worklist_{today}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out.relative_to(MCC_ROOT).as_posix()} ({len(elig)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
