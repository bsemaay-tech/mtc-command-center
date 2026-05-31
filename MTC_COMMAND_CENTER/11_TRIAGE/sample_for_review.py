"""Print a condensed context window per REVIEW_HUMAN candidate so a human
(or another LLM pass) can decide its verdict without re-reading 30k words.

For each row in the 'REVIEW_HUMAN' section of the dated reclassification
report, dumps: intro, all numeric-threshold contexts, all enumeration
marker contexts, and the conclusion.
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

THIS = Path(__file__).resolve()
API_ROOT = THIS.parent.parent / "08_DASHBOARD_APP" / "apps" / "api"
sys.path.insert(0, str(API_ROOT))

from mcc_readonly.audit_reader import build_candidate_audit  # noqa: E402
from mcc_readonly.paths import default_mcc_root  # noqa: E402

from analyze_transcripts import (  # noqa: E402
    NUMERIC_THRESHOLD_RE,
    STRONG_ENUMERATION_PATTERNS,
    WEAK_ENUMERATION_PATTERNS,
    INDICATOR_NAMES,
)


def list_review_human_ids(report_path: Path) -> list[str]:
    text = report_path.read_text(encoding="utf-8")
    in_section = False
    ids: list[str] = []
    for line in text.splitlines():
        if line.startswith("## REVIEW_HUMAN"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.startswith("| "):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if cells and cells[0] not in ("candidate_id", "---") and not cells[0].startswith("-"):
                ids.append(cells[0])
    return ids


def context_around(text: str, matches: list[re.Match], radius_chars: int = 220, limit: int = 8) -> list[str]:
    out: list[str] = []
    used = set()
    for m in matches[:limit]:
        start = max(0, m.start() - radius_chars)
        end = min(len(text), m.end() + radius_chars)
        snippet = text[start:end].strip().replace("\n", " ")
        key = (start // 200, end // 200)
        if key in used:
            continue
        used.add(key)
        out.append(f"  …{snippet}…")
    return out


def main() -> int:
    today = date.today().isoformat()
    report_path = THIS.parent / f"reclassification_audit_{today}.md"
    if not report_path.exists():
        print(f"Missing {report_path}; run analyze_transcripts.py first.")
        return 1

    ids = list_review_human_ids(report_path)
    print(f"REVIEW_HUMAN candidates in {report_path.name}: {len(ids)}\n")

    mcc_root = Path(default_mcc_root()).resolve()
    tpl_root = mcc_root.parent / "01_MASTER TEMPLATE_V2"
    audit = build_candidate_audit()
    by_id = {r.get("id"): r for r in audit.get("rows", []) or []}

    out_lines: list[str] = []
    for i, cid in enumerate(ids, start=1):
        row = by_id.get(cid)
        if not row:
            out_lines.append(f"\n=== {i}. {cid} — NOT FOUND ===\n")
            continue
        tpath = row.get("transcript_path") or ""
        full = tpl_root / Path(tpath.replace("\\", "/"))
        if not full.exists():
            out_lines.append(f"\n=== {i}. {cid} — transcript missing ({tpath}) ===\n")
            continue
        text = full.read_text(encoding="utf-8", errors="replace")
        wc = len(re.findall(r"\b\w+\b", text))
        lines = text.splitlines()

        out_lines.append(f"\n=== {i}. {cid} — {row.get('name','')[:80]} ===")
        out_lines.append(f"transcript: {tpath}  ({wc} words, {len(lines)} lines)")
        out_lines.append(f"audit: quality={row.get('source_quality')}, blocked={row.get('blocked_reason') or '—'}")
        out_lines.append(f"source_url: {row.get('source_url')}")
        out_lines.append("")

        out_lines.append("--- intro (first 25 non-empty lines) ---")
        intro_lines = [l for l in lines[:80] if l.strip()][:25]
        out_lines.extend(intro_lines)
        out_lines.append("")

        threshold_matches = list(NUMERIC_THRESHOLD_RE.finditer(text))
        if threshold_matches:
            out_lines.append(f"--- numeric thresholds ({len(threshold_matches)}) ---")
            out_lines.extend(context_around(text, threshold_matches))
            out_lines.append("")

        strong_enum_matches: list[re.Match] = []
        for rx in STRONG_ENUMERATION_PATTERNS:
            strong_enum_matches.extend(rx.finditer(text))
        weak_enum_matches: list[re.Match] = []
        for rx in WEAK_ENUMERATION_PATTERNS:
            weak_enum_matches.extend(rx.finditer(text))
        all_enum = sorted(strong_enum_matches + weak_enum_matches, key=lambda m: m.start())
        if all_enum:
            out_lines.append(f"--- enumeration markers (strong={len(strong_enum_matches)}, weak={len(weak_enum_matches)}) ---")
            out_lines.extend(context_around(text, all_enum, radius_chars=140, limit=6))
            out_lines.append("")

        out_lines.append("--- indicators mentioned ---")
        ind_hits = []
        for name, rx in INDICATOR_NAMES.items():
            n = len(rx.findall(text))
            if n:
                ind_hits.append(f"{name}({n})")
        out_lines.append("  " + (", ".join(ind_hits) if ind_hits else "—"))
        out_lines.append("")

        out_lines.append("--- conclusion (last 15 non-empty lines) ---")
        tail = [l for l in lines[-60:] if l.strip()][-15:]
        out_lines.extend(tail)
        out_lines.append("")

    out_path = THIS.parent / f"review_human_samples_{today}.md"
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
