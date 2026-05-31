"""Wider transcript sampler for promotion packet drafting.

For a given list of candidate IDs, dumps:
  - intro (50 lines)
  - every section heading in the transcript
  - context around every rule phrase ('buy when', 'enter', 'exit', 'stop', 'target', ...)
  - context around every numeric threshold match
  - context around every enumeration marker
  - conclusion (30 lines)

Usage:
  python 11_TRIAGE/deep_sample.py <cid_1> [<cid_2> ...] [--out <file>]
"""

from __future__ import annotations

import argparse
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

RULE_PHRASES = [
    re.compile(r"\b(?:buy|enter|long|sell|short|exit|close)\s+(?:when|if|as|on)\b", re.I),
    re.compile(r"\b(?:stop[- ]loss|stop\s+at|stop\s+below|trailing\s+stop|risk\s*[/-]\s*reward)\b", re.I),
    re.compile(r"\b(?:take[- ]profit|target\s+at|profit\s+target|sell\s+at)\b", re.I),
    re.compile(r"\b(?:entry|exit)\s+(?:rule|signal|criteria|condition|trigger)\b", re.I),
    re.compile(r"\b(?:rule(?:s)?\s+(?:is|are|number|no\.?)|non-negotiable|hard\s+rule)\b", re.I),
    re.compile(r"\b(?:breakout|breakdown|pullback|retest|reversal)\s+(?:above|below|of|from)\b", re.I),
    re.compile(r"\b(?:follow[- ]through\s+day|RS\s+line|new\s+high\s+ground|pivot\s+point|opening\s+range)\b", re.I),
]


def context(text: str, m: re.Match, before: int = 350, after: int = 350) -> str:
    s = max(0, m.start() - before)
    e = min(len(text), m.end() + after)
    snippet = text[s:e].replace("\n", " ").strip()
    return snippet


def dedupe_close(matches, min_gap: int = 600):
    last_start = -10_000
    out = []
    for m in matches:
        if m.start() - last_start >= min_gap:
            out.append(m)
            last_start = m.start()
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("cids", nargs="+")
    p.add_argument("--out", default=None)
    args = p.parse_args()

    mcc_root = Path(default_mcc_root()).resolve()
    tpl_root = mcc_root.parent / "01_MASTER TEMPLATE_V2"
    audit = build_candidate_audit()
    by_id = {r.get("id"): r for r in audit.get("rows", []) or []}

    out_lines: list[str] = []
    for cid in args.cids:
        row = by_id.get(cid)
        if not row:
            out_lines.append(f"\n=== {cid} — NOT FOUND ===\n")
            continue
        tpath = row.get("transcript_path") or ""
        full = tpl_root / Path(tpath.replace("\\", "/"))
        if not full.exists():
            out_lines.append(f"\n=== {cid} — transcript missing ===\n")
            continue
        text = full.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        wc = len(re.findall(r"\b\w+\b", text))

        out_lines.append(f"\n=== {cid} — {row.get('name','')} ===")
        out_lines.append(f"transcript: {tpath} ({wc} words, {len(lines)} lines)")
        out_lines.append(f"audit: quality={row.get('source_quality')}, blocked={row.get('blocked_reason') or '—'}")
        out_lines.append(f"url: {row.get('source_url')}")
        out_lines.append("")

        out_lines.append("## section headings (## level in transcript)")
        for ln in lines:
            if re.match(r"^#{1,3}\s+\S", ln) or re.match(r"^\d+\.\s+bölüm:", ln):
                out_lines.append("  " + ln.strip()[:120])
        out_lines.append("")

        out_lines.append("## intro (first 40 non-empty lines)")
        intro_lines = [l for l in lines[:120] if l.strip()][:40]
        out_lines.extend(intro_lines)
        out_lines.append("")

        rule_matches: list[re.Match] = []
        for rx in RULE_PHRASES:
            rule_matches.extend(rx.finditer(text))
        rule_matches.sort(key=lambda m: m.start())
        rule_matches = dedupe_close(rule_matches, min_gap=500)
        if rule_matches:
            out_lines.append(f"## rule-phrase neighborhoods ({len(rule_matches)})")
            for m in rule_matches[:25]:
                out_lines.append(f"  …{context(text, m, 280, 280)}…")
            out_lines.append("")

        threshold_matches = list(NUMERIC_THRESHOLD_RE.finditer(text))
        threshold_matches = dedupe_close(threshold_matches, min_gap=600)
        if threshold_matches:
            out_lines.append(f"## numeric thresholds ({len(threshold_matches)})")
            for m in threshold_matches[:15]:
                out_lines.append(f"  …{context(text, m, 280, 280)}…")
            out_lines.append("")

        enum_matches: list[re.Match] = []
        for rx in STRONG_ENUMERATION_PATTERNS:
            enum_matches.extend(rx.finditer(text))
        for rx in WEAK_ENUMERATION_PATTERNS:
            enum_matches.extend(rx.finditer(text))
        enum_matches.sort(key=lambda m: m.start())
        enum_matches = dedupe_close(enum_matches, min_gap=400)
        if enum_matches:
            out_lines.append(f"## enumeration markers ({len(enum_matches)})")
            for m in enum_matches[:10]:
                out_lines.append(f"  …{context(text, m, 200, 200)}…")
            out_lines.append("")

        out_lines.append("## indicators mentioned")
        for name, rx in INDICATOR_NAMES.items():
            n = len(rx.findall(text))
            if n:
                out_lines.append(f"  {name}: {n} mentions")
        out_lines.append("")

        out_lines.append("## conclusion (last 25 non-empty lines)")
        tail = [l for l in lines[-90:] if l.strip()][-25:]
        out_lines.extend(tail)
        out_lines.append("")

    out_path = Path(args.out) if args.out else THIS.parent / f"deep_sample_{date.today().isoformat()}.md"
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Wrote {out_path} ({len(out_lines)} lines for {len(args.cids)} candidates)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
