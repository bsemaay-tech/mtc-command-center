"""Phase 1 inventory + dedup + extraction for QuantLens overnight batch.

Reads all .md intake reports under the inbox folder, classifies them, extracts
structured metadata, deduplicates by video id / normalized title, and emits
INTAKE_INVENTORY.csv, DEDUPE_REPORT.md, CANDIDATE_EXTRACTION_RAW.jsonl.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(r"C:/LAB/tradingview-lab/01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB")
INBOX = ROOT / "00_INBOX_REPORTS"
OUT = ROOT / "research" / "overnight_intake_batch_2026_05_03"

YT_ID = re.compile(r"(?:youtu\.be/|v=|/embed/|/v/)([A-Za-z0-9_-]{6,15})")
URL_RE = re.compile(r"https?://[^\s\)\]]+")
TITLE_HINT = re.compile(r"(?im)^[#\-\s\*]*\**\s*(?:Title|Video Title|Başlık)\s*:?\s*\**\s*(.+?)$")
CANDID_ID = re.compile(r"(?im)^[#\-\s\*]*\**\s*Candidate ID\**\s*:?\s*\**\s*[`]?([A-Za-z0-9_]+)[`]?")
CANDID_KIND = re.compile(r"(?im)Codex Status[^\n:]*:?\s*[`]?([A-Z_]+)")
ASSET_HINT = re.compile(r"(?im)(US equit|equities|stocks|S&P|SPY|QQQ|TQQQ|microcap|small[- ]?cap|crypto|BTC|ETH|forex|FX|futures|commodit|options)")
TF_HINT = re.compile(r"(?im)(?<![A-Za-z])(1m|3m|5m|10m|15m|30m|1h|2h|4h|1D|daily|weekly|monthly|swing|position)(?![A-Za-z])")

PROCESS_KEYWORDS = ("psychology", "process", "mindset", "discipline", "review", "journal")
RISK_KEYWORDS = ("position sizing", "progressive exposure", "risk management", "kelly", "drawdown rule")
EXIT_KEYWORDS = ("trailing stop", "exit", "sell rule", "take profit", "partial")
FILTER_KEYWORDS = ("regime", "filter", "breadth", "stage analysis", "trend filter")


def normalize_title(t: str) -> str:
    if not t:
        return ""
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def classify_kind(text: str) -> str:
    low = text.lower()
    if any(k in low for k in ("no strategy", "psychology only", "psikoloji")):
        return "PROCESS_ONLY"
    if any(k in low for k in PROCESS_KEYWORDS) and not any(k in low for k in ("entry", "setup", "breakout", "pullback", "long", "short")):
        return "PROCESS_ONLY"
    if any(k in low for k in EXIT_KEYWORDS) and "entry" not in low:
        return "EXIT_MODULE"
    if any(k in low for k in RISK_KEYWORDS) and "entry" not in low:
        return "RISK_MANAGEMENT_MODULE"
    if any(k in low for k in FILTER_KEYWORDS) and "entry" not in low:
        return "FILTER_ONLY"
    return "STRATEGY"


def asset_class(text: str) -> str:
    m = ASSET_HINT.search(text)
    if not m:
        return "UNKNOWN"
    raw = m.group(1).lower()
    if "microcap" in raw or "small" in raw:
        return "US_MICROCAP"
    if "us equit" in raw or "equities" in raw or "stocks" in raw or "tqqq" in raw or "spy" in raw or "qqq" in raw or "s&p" in raw:
        return "US_EQUITY"
    if "crypto" in raw or "btc" in raw or "eth" in raw:
        return "CRYPTO"
    if "forex" in raw or "fx" in raw:
        return "FOREX"
    if "futures" in raw:
        return "FUTURES"
    if "options" in raw:
        return "OPTIONS"
    return raw.upper()


def primary_tf(text: str) -> str:
    tfs = [m.group(1).lower() for m in TF_HINT.finditer(text[:5000])]
    if not tfs:
        return "UNKNOWN"
    # prefer the shortest reported (most specific intraday) for day-trade signal
    order = ["1m", "3m", "5m", "10m", "15m", "30m", "1h", "2h", "4h", "1d", "daily", "weekly", "monthly", "swing", "position"]
    seen = [t for t in order if t in tfs]
    return seen[0] if seen else tfs[0]


def is_valid_intake(text: str) -> bool:
    low = text.lower()
    return ("quantlens" in low) or ("intake" in low) or ("candidate" in low)


def classify_file(path: Path, text: str) -> str:
    if not text.strip():
        return "EMPTY_OR_CORRUPT"
    if len(text) < 200:
        return "EMPTY_OR_CORRUPT"
    name = path.name.lower()
    if "transcrip" in str(path).lower() and "intake" not in name:
        return "RAW_TRANSCRIPT_BY_MISTAKE"
    if name.startswith("intake_") or name.startswith("ql_") or "_quantlens_" in name or "intake" in name:
        return "VALID_INTAKE_REPORT"
    if is_valid_intake(text):
        return "VALID_INTAKE_REPORT"
    return "UNKNOWN"


def main() -> None:
    rows = []
    raw_records = []
    seen_video_ids: dict[str, str] = {}
    seen_titles: dict[str, str] = {}

    files = sorted(p for p in INBOX.rglob("*.md") if p.is_file())
    print(f"Found {len(files)} .md files under {INBOX}")

    for p in files:
        rel = p.relative_to(INBOX).as_posix()
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:  # pragma: no cover
            rows.append({
                "rel_path": rel, "classification": "EMPTY_OR_CORRUPT",
                "error": str(e), "video_id": "", "title": "", "url": "",
                "asset_class": "", "primary_tf": "", "kind": "", "candidate_id": "",
                "is_duplicate_of": "", "size_bytes": 0,
            })
            continue

        classification = classify_file(p, text)
        # transcripts subfolder = raw transcripts
        if "transcrips" in rel.lower():
            classification = "RAW_TRANSCRIPT_BY_MISTAKE"

        first_url = ""
        m_url = URL_RE.search(text)
        if m_url:
            first_url = m_url.group(0).rstrip(".,)")

        vid = ""
        m_vid = YT_ID.search(text)
        if m_vid:
            vid = m_vid.group(1)
        else:
            # try to lift from filename
            m2 = re.search(r"_([A-Za-z0-9_-]{8,15})_", p.stem)
            if m2:
                vid = m2.group(1)

        title = ""
        m_title = TITLE_HINT.search(text)
        if m_title:
            title = m_title.group(1).strip().strip("`")
        if not title:
            # second strategy: first H1 line
            for line in text.splitlines():
                ls = line.strip()
                if ls.startswith("# "):
                    title = ls.lstrip("# ").strip()
                    break

        cand_id = ""
        m_cand = CANDID_ID.search(text)
        if m_cand:
            cand_id = m_cand.group(1)

        codex_status = ""
        m_kind = CANDID_KIND.search(text)
        if m_kind:
            codex_status = m_kind.group(1)

        ac = asset_class(text)
        tf = primary_tf(text)
        kind = classify_kind(text)

        norm_title = normalize_title(title or p.stem)

        is_dup_of = ""
        if classification == "VALID_INTAKE_REPORT":
            if vid and vid in seen_video_ids:
                is_dup_of = seen_video_ids[vid]
                classification = "DUPLICATE"
            elif norm_title and norm_title in seen_titles:
                is_dup_of = seen_titles[norm_title]
                classification = "DUPLICATE"
            else:
                if vid:
                    seen_video_ids[vid] = rel
                if norm_title:
                    seen_titles[norm_title] = rel

        row = {
            "rel_path": rel, "classification": classification, "error": "",
            "video_id": vid, "title": title[:200], "url": first_url[:300],
            "asset_class": ac, "primary_tf": tf, "kind": kind,
            "candidate_id": cand_id, "codex_status": codex_status,
            "is_duplicate_of": is_dup_of, "size_bytes": p.stat().st_size,
        }
        rows.append(row)

        if classification == "VALID_INTAKE_REPORT":
            raw_records.append({
                **row,
                "head": text[:1500],
            })

    # write CSV
    csv_path = OUT / "INTAKE_INVENTORY.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # write JSONL
    jsonl_path = OUT / "CANDIDATE_EXTRACTION_RAW.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for r in raw_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # dedupe report
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["classification"]] = counts.get(r["classification"], 0) + 1

    dedupe_md = ["# Dedupe & Inventory Report", "",
                 f"Total files scanned: {len(rows)}", ""]
    for k, v in sorted(counts.items()):
        dedupe_md.append(f"- {k}: {v}")
    dedupe_md.append("")
    dedupe_md.append("## Duplicates")
    dups = [r for r in rows if r["classification"] == "DUPLICATE"]
    if not dups:
        dedupe_md.append("- None detected by video_id or normalized title.")
    for r in dups:
        dedupe_md.append(f"- `{r['rel_path']}` duplicate of `{r['is_duplicate_of']}` (video_id={r['video_id']})")
    dedupe_md.append("")
    dedupe_md.append("## Raw transcripts skipped")
    raws = [r for r in rows if r["classification"] == "RAW_TRANSCRIPT_BY_MISTAKE"]
    dedupe_md.append(f"Count: {len(raws)} (under Transcrips/, used only as secondary reference)")

    (OUT / "DEDUPE_REPORT.md").write_text("\n".join(dedupe_md), encoding="utf-8")

    # console summary
    print(json.dumps(counts, indent=2))
    print(f"Wrote {csv_path}")
    print(f"Wrote {jsonl_path}")


if __name__ == "__main__":
    main()
