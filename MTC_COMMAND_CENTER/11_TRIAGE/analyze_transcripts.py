"""Heuristic transcript scanner for triage decisions.

For every candidate that has a transcript on record, computes lightweight
signals and classifies the row into:

  KEEP_REJECTED        rejected and the content looks correctly rejected
  REVIEW_HUMAN         ambiguous; needs the user to read the transcript
  LIKELY_MISCLASSIFIED rejected but transcript reads like a testable strategy
  SPLIT_RECOMMENDED    transcript appears to cover multiple distinct strategies
  ALREADY_OK           not rejected and signals look strategy-like (informational)

Writes two reports under 11_TRIAGE/:
  - reclassification_audit_<date>.md
  - split_candidates_<date>.md

Read-only. No side-effects on QuantLens or MCC core.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

THIS = Path(__file__).resolve()

API_ROOT = THIS.parent.parent / "08_DASHBOARD_APP" / "apps" / "api"
sys.path.insert(0, str(API_ROOT))

from mcc_readonly.audit_reader import build_candidate_audit  # noqa: E402
from mcc_readonly.paths import default_mcc_root, default_quantlens_root  # noqa: E402

STRATEGY_KEYWORDS = [
    r"\bentry\b", r"\bentries\b", r"\benter (?:long|short)\b", r"\bgo (?:long|short)\b",
    r"\bexit\b", r"\bclose (?:the )?(?:trade|position)\b",
    r"\bstop[- ]loss\b", r"\bstop loss\b", r"\bsl\b",
    r"\btake[- ]profit\b", r"\btp\b", r"\btarget\b",
    r"\bbuy when\b", r"\bsell when\b", r"\bbuy if\b", r"\bsell if\b",
    r"\btrigger\b", r"\bcrosses (?:above|below)\b", r"\bcrossover\b", r"\bcrossunder\b",
    r"\bbreakout\b", r"\bbreakdown\b", r"\bretest\b",
    r"\bsetup\b", r"\bsignal\b", r"\btrade plan\b",
]

EDUCATIONAL_KEYWORDS = [
    r"\blesson\b", r"\bmistake\b", r"\bpsychology\b", r"\bmindset\b", r"\bwisdom\b",
    r"\bexperience\b", r"\bI learned\b", r"\bwhat I wish\b", r"\bjourney\b",
    r"\bphilosophy\b", r"\binterview\b", r"\bstory\b", r"\bbiography\b",
    r"\bdiscipline\b", r"\bemotion\b", r"\bcontroversy\b",
]

INDICATOR_NAMES = {
    "ema": re.compile(r"\b(?:e\.?m\.?a\.?|exponential moving average)s?\b", re.I),
    "sma": re.compile(r"\b(?:s\.?m\.?a\.?|simple moving average)s?\b", re.I),
    "rsi": re.compile(r"\brsi\b", re.I),
    "macd": re.compile(r"\bmacd\b", re.I),
    "bollinger": re.compile(r"\b(?:bollinger|b\.?b\.?)\b", re.I),
    "vwap": re.compile(r"\bvwap\b", re.I),
    "atr": re.compile(r"\batr\b", re.I),
    "adx": re.compile(r"\badx\b", re.I),
    "stoch": re.compile(r"\bstoch(?:astic)?\b", re.I),
    "fvg": re.compile(r"\bf\.?v\.?g\.?\b", re.I),
    "ict": re.compile(r"\bict\b", re.I),
    "fibonacci": re.compile(r"\b(?:fib(?:onacci)?)\b", re.I),
    "supply_demand": re.compile(r"\bsupply[- ]?(?:and[- ]?)?demand\b", re.I),
    "candle_pattern": re.compile(r"\b(?:candlestick patterns?|engulfing|doji|pin bar|hammer)\b", re.I),
    "ichimoku": re.compile(r"\bichimoku\b", re.I),
    "supertrend": re.compile(r"\bsuper[- ]?trend\b", re.I),
    "vwma": re.compile(r"\bvwma\b", re.I),
    "obv": re.compile(r"\bobv\b", re.I),
    "cci": re.compile(r"\bcci\b", re.I),
}

# Strong markers: hard to confuse with timestamps. Each hit means a deliberate enumeration by the speaker.
STRONG_ENUMERATION_PATTERNS = [
    re.compile(r"\b(?:first|second|third|fourth|fifth) (?:strategy|setup|signal|indicator|method)\b", re.I),
    re.compile(r"\banother (?:strategy|setup|signal|approach|method|indicator)\b", re.I),
    re.compile(r"\b(?:the )?next (?:strategy|setup|signal|approach|method|indicator)\b", re.I),
    re.compile(r"\bstrategy[ \t]+(?:a|b|c|d)\b(?!\s*\w)", re.I),
    re.compile(r"\b(?:strategy|setup|indicator)[ \t]+(?:number|no\.?)[ \t]*\d", re.I),
]
# Weak markers: prone to timestamp false positives ("setup [1]" then "1:23"). Counted but require corroboration.
WEAK_ENUMERATION_PATTERNS = [
    re.compile(r"\b(?:strategy|setup|signal|indicator|method)[ \t]+(?:#[ \t]*)?(?:1|2|3|4|5|one|two|three|four|five)\b(?!\s*[:.0-9])", re.I),
]

NUMERIC_THRESHOLD_RE = re.compile(
    r"\b(?:"
    r"(?:rsi|ema|sma|atr|adx|stoch|macd|bb|bollinger|vwap)[ \t]*(?:is[ \t]+)?(?:above|below|under|over|at|=|equal|crosses?[ \t]+(?:above|below))[ \t]+\d+"
    r"|"
    r"\d+[ \t]*(?:day|period|bar)[ \t]*(?:ema|sma|atr|rsi|moving average)"
    r"|"
    r"(?:ema|sma|atr|rsi)[ \t]*\d{2,3}\b"
    r"|"
    r"\d{1,3}[ \t]*(?:ema|sma)\b"
    r")",
    re.I,
)


def count_patterns(text: str, patterns) -> int:
    n = 0
    for p in patterns:
        if isinstance(p, str):
            n += len(re.findall(p, text, re.I))
        else:
            n += len(p.findall(text))
    return n


def indicator_signal(text: str) -> tuple[int, list[str]]:
    found = []
    for name, rx in INDICATOR_NAMES.items():
        if rx.search(text):
            found.append(name)
    return len(found), found


def enumeration_signal(text: str) -> tuple[int, int, list[str]]:
    strong: list[str] = []
    weak: list[str] = []
    for rx in STRONG_ENUMERATION_PATTERNS:
        for m in rx.finditer(text):
            strong.append(m.group(0))
    for rx in WEAK_ENUMERATION_PATTERNS:
        for m in rx.finditer(text):
            weak.append(m.group(0))
    return len(strong), len(weak), (strong + weak)[:10]


def classify(audit_row: dict, signals: dict) -> tuple[str, str]:
    is_rejected = audit_row.get("audit_status") == "BLOCKED" or (
        (audit_row.get("source_quality") or "").upper() == "REJECTED"
    )
    wc = signals["word_count"]
    strat = signals["strategy_score"]
    edu = signals["educational_score"]
    ind_count = signals["indicator_count"]
    strong_enum = signals["strong_enum_count"]
    weak_enum = signals["weak_enum_count"]
    threshold_count = signals["numeric_threshold_count"]

    if wc < 200:
        return ("KEEP_REJECTED" if is_rejected else "ALREADY_OK",
                "transcript too short to extract a testable rule")

    if not is_rejected:
        return ("ALREADY_OK",
                f"not rejected; strat={strat}, ind={ind_count}, thresh={threshold_count}")

    # Split candidate detection: strong enumeration OR high indicator diversity
    if strong_enum >= 2 and ind_count >= 3:
        return ("SPLIT_RECOMMENDED",
                f"{strong_enum} strong enumeration markers across {ind_count} indicators")
    if ind_count >= 5 and (strong_enum + weak_enum) >= 2:
        return ("SPLIT_RECOMMENDED",
                f"{ind_count} different indicators with {strong_enum + weak_enum} enumeration markers")
    if strong_enum >= 3:
        return ("SPLIT_RECOMMENDED",
                f"{strong_enum} strong enumeration markers regardless of indicator count")

    # Misclassification: needs specific numeric rules
    if threshold_count >= 3 and strat >= 6:
        return ("LIKELY_MISCLASSIFIED",
                f"{threshold_count} numeric thresholds and {strat} rule signals — testable rule visible")
    if threshold_count == 0:
        return ("KEEP_REJECTED",
                f"no numeric thresholds = no isolated testable rule (strat={strat}, edu={edu})")
    return ("REVIEW_HUMAN",
            f"some thresholds ({threshold_count}) but weak rule signals (strat={strat}, edu={edu}, ind={ind_count})")


def render_table(rows, headers) -> str:
    line = "| " + " | ".join(headers) + " |\n"
    line += "|" + "|".join(["---"] * len(headers)) + "|\n"
    for r in rows:
        cells = ["" if v is None else str(v).replace("|", "\\|") for v in r]
        line += "| " + " | ".join(cells) + " |\n"
    return line


def resolve_transcript_path(tpath: str, mcc_root: Path) -> Path:
    rel = Path(tpath.replace("\\", "/"))
    if rel.is_absolute():
        return rel

    quantlens_root = default_quantlens_root(mcc_root)
    workspace_root = mcc_root.parent
    legacy_tpl_root = workspace_root / "01_MASTER TEMPLATE_V2"
    candidates = [
        quantlens_root / rel,
        mcc_root / rel,
        workspace_root / rel,
        legacy_tpl_root / rel,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    basename = rel.name
    basename_candidates = [
        quantlens_root / "00_INBOX_REPORTS" / "Transcrips" / basename,
        quantlens_root / "Transcrips" / basename,
        mcc_root / "00_INBOX_REPORTS" / "Transcrips" / basename,
        workspace_root / "MTC_COMMAND_CENTER" / "03_QUANTLENS" / "00_INBOX_REPORTS" / "Transcrips" / basename,
    ]
    for candidate in basename_candidates:
        if candidate.exists():
            return candidate

    return candidates[0]


def main() -> int:
    mcc_root = Path(default_mcc_root()).resolve()
    audit = build_candidate_audit()
    rows = audit.get("rows", []) or []

    targets = [r for r in rows if r.get("has_transcript")]
    print(f"Candidates with transcript on record: {len(targets)}")

    analyses: list[dict] = []
    for row in targets:
        tpath = row.get("transcript_path", "")
        if not tpath:
            continue
        full = resolve_transcript_path(tpath, mcc_root)
        if not full.exists():
            continue
        try:
            text = full.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        wc = len(re.findall(r"\b\w+\b", text))
        strat = count_patterns(text, STRATEGY_KEYWORDS)
        edu = count_patterns(text, EDUCATIONAL_KEYWORDS)
        ind_count, ind_list = indicator_signal(text)
        strong_enum, weak_enum, enum_hits = enumeration_signal(text)
        threshold_count = len(NUMERIC_THRESHOLD_RE.findall(text))
        signals = {
            "word_count": wc,
            "strategy_score": strat,
            "educational_score": edu,
            "indicator_count": ind_count,
            "indicators": ind_list,
            "strong_enum_count": strong_enum,
            "weak_enum_count": weak_enum,
            "enumeration_count": strong_enum + weak_enum,
            "enumeration_hits": enum_hits,
            "numeric_threshold_count": threshold_count,
        }
        verdict, reason = classify(row, signals)
        analyses.append({
            "row": row,
            "transcript_path": tpath,
            "signals": signals,
            "verdict": verdict,
            "reason": reason,
        })

    counts = Counter(a["verdict"] for a in analyses)
    print("Verdict counts:", dict(counts))

    today = date.today().isoformat()
    reclass_path = THIS.parent / f"reclassification_audit_{today}.md"
    split_path = THIS.parent / f"split_candidates_{today}.md"

    title_of = lambda r: (r.get("name") or "")[:60]

    grouped: dict[str, list[dict]] = {
        "LIKELY_MISCLASSIFIED": [],
        "SPLIT_RECOMMENDED": [],
        "REVIEW_HUMAN": [],
        "KEEP_REJECTED": [],
        "ALREADY_OK": [],
    }
    for a in analyses:
        grouped.setdefault(a["verdict"], []).append(a)

    lines = [
        f"# Reclassification audit — {today}",
        "",
        f"Heuristic scan over {len(analyses)} candidates with a transcript on record. "
        "Verdicts are **suggestions, not decisions**: REVIEW_HUMAN / LIKELY_MISCLASSIFIED / SPLIT_RECOMMENDED "
        "rows are starting points for a manual transcript read.",
        "",
        "## Summary",
        "",
        render_table(
            [(k, len(v)) for k, v in grouped.items()],
            ["verdict", "count"],
        ),
        "",
    ]
    for verdict in ["LIKELY_MISCLASSIFIED", "SPLIT_RECOMMENDED", "REVIEW_HUMAN", "KEEP_REJECTED", "ALREADY_OK"]:
        items = grouped.get(verdict) or []
        if not items:
            continue
        lines.append(f"## {verdict} ({len(items)})")
        lines.append("")
        rows_out = []
        for a in items:
            r = a["row"]
            s = a["signals"]
            rows_out.append([
                r.get("id", ""),
                title_of(r),
                r.get("source_quality", ""),
                r.get("blocked_reason", "") or "—",
                s["word_count"],
                s["strategy_score"],
                s["educational_score"],
                s["indicator_count"],
                s["enumeration_count"],
                s["numeric_threshold_count"],
                a["reason"],
            ])
        lines.append(render_table(
            rows_out,
            ["candidate_id", "title", "quality", "blocked_reason", "words", "strat", "edu", "ind", "enum", "thresh", "reason"],
        ))
        lines.append("")
    reclass_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {reclass_path}")

    splits = grouped.get("SPLIT_RECOMMENDED") or []
    slines = [
        f"# Split-candidate hunt — {today}",
        "",
        f"{len(splits)} candidate(s) flagged by the heuristic as covering multiple distinct strategies. "
        "Each entry lists the enumeration markers and indicator names that triggered the flag. "
        "Use as a starting point for splitting the candidate into separate per-indicator cases.",
        "",
    ]
    if not splits:
        slines.append("_No multi-strategy transcripts detected by the current heuristic._")
    else:
        for a in splits:
            r = a["row"]
            s = a["signals"]
            slines.append(f"## {r.get('id')} — {title_of(r)}")
            slines.append("")
            slines.append(f"- transcript: `{a['transcript_path']}`")
            slines.append(f"- word_count: {s['word_count']}, indicators: {s['indicator_count']} ({', '.join(s['indicators']) or '—'})")
            slines.append(f"- enumeration markers found ({s['enumeration_count']}): "
                          + (", ".join(f"`{h}`" for h in s["enumeration_hits"]) or "—"))
            slines.append(f"- numeric thresholds: {s['numeric_threshold_count']}")
            slines.append("")
    split_path.write_text("\n".join(slines), encoding="utf-8")
    print(f"Wrote {split_path}")

    json_path = THIS.parent / "transcript_reclassification.json"
    json_rows = []
    for a in analyses:
        r = a["row"]
        s = a["signals"]
        json_rows.append({
            "candidate_id": r.get("id", ""),
            "title": (r.get("name") or "")[:120],
            "source_quality": r.get("source_quality", ""),
            "blocked_reason": r.get("blocked_reason", "") or "",
            "verdict": a["verdict"],
            "reason": a["reason"],
            "word_count": s["word_count"],
            "strategy_score": s["strategy_score"],
            "educational_score": s["educational_score"],
            "indicator_count": s["indicator_count"],
            "indicators": s["indicators"],
            "numeric_threshold_count": s["numeric_threshold_count"],
        })
    json_payload = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_candidates": len(targets),
        "analyzed": len(analyses),
        "verdict_counts": dict(counts),
        "rows": json_rows,
    }
    json_path.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
