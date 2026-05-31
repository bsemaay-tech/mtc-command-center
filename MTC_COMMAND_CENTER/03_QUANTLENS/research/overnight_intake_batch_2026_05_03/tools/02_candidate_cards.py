"""Phase 2 — generate one CANDIDATE_<id>_<slug>.md card per unique intake.

Reads CANDIDATE_EXTRACTION_RAW.jsonl plus the underlying intake file, classifies
testability and MTC relevance, and writes a structured candidate card.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"C:/LAB/tradingview-lab/01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB")
OUT = ROOT / "research" / "overnight_intake_batch_2026_05_03"
INBOX = ROOT / "00_INBOX_REPORTS"
CARDS = OUT / "candidates"
CARDS.mkdir(exist_ok=True)

# 17 crypto futures 5m datasets locally available
CRYPTO_5M_AVAILABLE = {
    "ADAUSDT", "APTUSDT", "ARBUSDT", "AVAXUSDT", "BNBUSDT", "BTCUSDT",
    "DOGEUSDT", "DOTUSDT", "ETHUSDT", "LINKUSDT", "LTCUSDT", "NEARUSDT",
    "OPUSDT", "POLUSDT", "SOLUSDT", "TRXUSDT", "XRPUSDT",
}

SECTION_HINTS = [
    ("entry", re.compile(r"(?ims)^#+\s*(?:Entry|Entries|Setup|Long entry|Trigger|Buy rule)[^\n]*$.*?(?=\n#+\s|\Z)")),
    ("exit", re.compile(r"(?ims)^#+\s*(?:Exit|Exits|Sell rule|Take profit|TP|Target)[^\n]*$.*?(?=\n#+\s|\Z)")),
    ("stop", re.compile(r"(?ims)^#+\s*(?:Stop|Initial stop|SL|Risk)[^\n]*$.*?(?=\n#+\s|\Z)")),
    ("size", re.compile(r"(?ims)^#+\s*(?:Position siz|Sizing|Risk per trade|Money management)[^\n]*$.*?(?=\n#+\s|\Z)")),
]


def slugify(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").upper()
    return s[:60] or "UNNAMED"


def section(text: str, key: str) -> str:
    for k, rx in SECTION_HINTS:
        if k == key:
            m = rx.search(text)
            if m:
                return m.group(0).strip()[:1500]
    return ""


def testability(rec: dict) -> str:
    ac = rec["asset_class"]
    tf = rec["primary_tf"]
    kind = rec["kind"]
    if kind in ("PROCESS_ONLY", "RISK_MANAGEMENT_MODULE", "EXIT_MODULE", "FILTER_ONLY"):
        return "REJECT_NOT_TESTABLE_AS_PRODUCER"
    if ac == "US_MICROCAP":
        return "NEEDS_US_MICROCAP_DATA"
    if ac == "OPTIONS":
        return "NEEDS_OPTIONS_DATA"
    if ac == "FOREX":
        return "NEEDS_FX_DATA"
    if ac == "US_EQUITY":
        # most US equity setups are intraday/swing → can crypto-proxy 5m only with caveats
        if tf in ("1m", "3m", "5m", "10m", "15m", "30m"):
            return "TEST_WITH_5M_CRYPTO_PROXY"
        return "TEST_WITH_1D_CRYPTO_PROXY"
    if ac == "CRYPTO":
        if tf in ("5m", "10m", "15m", "30m", "1h"):
            return "TEST_NOW_LOCAL_DATA"
        return "TEST_WITH_1D_CRYPTO_PROXY"
    return "TEST_WITH_5M_CRYPTO_PROXY"


def mtc_relevance(rec: dict, body: str) -> str:
    kind = rec["kind"]
    low = body.lower()
    if kind == "PROCESS_ONLY":
        return "PROCESS_ONLY"
    if kind == "RISK_MANAGEMENT_MODULE":
        return "SIZING_CANDIDATE"
    if kind == "EXIT_MODULE":
        return "EXIT_CANDIDATE"
    if kind == "FILTER_ONLY":
        return "FILTER_CANDIDATE"
    if rec["asset_class"] == "US_MICROCAP":
        return "DATA_BLOCKED"
    if "filter" in low and "entry" not in low:
        return "FILTER_CANDIDATE"
    return "PRODUCER_CANDIDATE"


def main() -> None:
    raw_path = OUT / "CANDIDATE_EXTRACTION_RAW.jsonl"
    records = [json.loads(l) for l in raw_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"Generating cards for {len(records)} valid intakes")

    cards_index: list[dict] = []
    for i, rec in enumerate(records, start=1):
        try:
            text = (INBOX / rec["rel_path"]).read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            text = ""
        cand_id = f"CAND_{i:03d}"
        slug = slugify((rec.get("title") or rec["rel_path"]).split("/")[-1])
        path = CARDS / f"CANDIDATE_{i:03d}_{slug}.md"

        entry_blk = section(text, "entry") or "_(see source intake)_"
        exit_blk = section(text, "exit") or "_(see source intake)_"
        stop_blk = section(text, "stop") or "_(see source intake)_"
        size_blk = section(text, "size") or "_(see source intake)_"

        test = testability(rec)
        mtc = mtc_relevance(rec, text)

        body = f"""# Candidate Card — {cand_id}

- **Source intake:** `{rec['rel_path']}`
- **Source URL:** {rec.get('url') or 'UNKNOWN'}
- **Video ID:** {rec.get('video_id') or 'UNKNOWN'}
- **Title:** {rec.get('title') or '(see source)'}
- **Existing candidate id (if any):** {rec.get('candidate_id') or '-'}
- **Codex status (intake):** {rec.get('codex_status') or '-'}

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** {rec.get('kind')}
- **Asset class:** {rec.get('asset_class')}
- **Native timeframe:** {rec.get('primary_tf')}
- **MTC relevance:** {mtc}
- **Testability:** {test}

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
{entry_blk}

## Exit logic (raw extract)
{exit_blk}

## Stop logic (raw extract)
{stop_blk}

## Sizing (raw extract)
{size_blk}

## Ambiguities
- Crypto-proxy applicability for US-equity-native setups (catalyst, gap, session).
- Discretionary "support/resistance" or "candle confirmation" rules require deterministic formalization before backtest.

## Conservative formalization for Python prototype
- Replace any discretionary subjective check with a single deterministic rule.
- If the strategy depends on US session, gap, or earnings catalyst, mark DATA_BLOCKED unless an explicit numeric proxy is documented in this card.

## Critical caveats
- Tonight's run is Python-only research; no Pine, no parity, no live alerts.
- A weak or rejected result is acceptable if evidence-based.
"""
        path.write_text(body, encoding="utf-8")
        cards_index.append({
            "cand_id": cand_id, "card_path": path.relative_to(OUT).as_posix(),
            "intake": rec["rel_path"], "title": rec.get("title", ""),
            "asset_class": rec.get("asset_class"), "primary_tf": rec.get("primary_tf"),
            "kind": rec.get("kind"), "mtc_relevance": mtc, "testability": test,
        })

    (OUT / "candidates_index.json").write_text(json.dumps(cards_index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(cards_index)} candidate cards")


if __name__ == "__main__":
    main()
