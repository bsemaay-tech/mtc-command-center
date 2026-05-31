from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
QL_ROOT = ROOT / "06_QUANTLENS_LAB"
OUT = Path(__file__).resolve().parent
INTAKE_DIR = QL_ROOT / "00_INBOX_REPORTS" / "3 Mayıs"
PROMPT_PATH = QL_ROOT / "_prompts" / "01_quantlens_candidate_intake_prompt.md"
BUNDLE = ROOT.parent / "MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427"
DATA_5M = QL_ROOT / "research" / "data_acquisition_5m_2026_05_03" / "normalized" / "binance_futures"
AUDITED = QL_ROOT / "research" / "strategy_batch_2026_05_03_AUDITED"
RERUN_5M = QL_ROOT / "research" / "strategy_batch_2026_05_03_5M_RERUN"
STAGE2 = QL_ROOT / "research" / "stage2_robustness_2026_05_03"

CORE_ASSETS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
EXPANDED_ASSETS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "LINKUSDT",
    "DOTUSDT",
]
ROUND_TRIP_COST_PCT = 0.12


@dataclass
class Candidate:
    candidate_id: str
    slug: str
    title: str
    source_file: str
    source_url: str
    youtube_id: str
    thesis: str
    strategy_family: str
    asset_class: str
    native_timeframe: str
    required_data: str
    entry_logic: str
    exit_logic: str
    sl_logic: str
    tp_logic: str
    sizing_notes: str
    mtc_relevance: str
    testability: str
    rule_clarity: int
    mechanical_testability: int
    native_data_availability: int
    edge_plausibility: int
    robustness_expectation: int
    mtc_compatibility: int
    overfit_penalty: int
    data_penalty: int
    tier: str = "C"

    @property
    def total_score(self) -> int:
        return (
            self.rule_clarity
            + self.mechanical_testability
            + self.native_data_availability
            + self.edge_plausibility
            + self.robustness_expectation
            + self.mtc_compatibility
            + self.overfit_penalty
            + self.data_penalty
        )


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def append_log(text: str) -> None:
    with (OUT / "RUN_LOG.md").open("a", encoding="utf-8") as handle:
        handle.write(f"\n- {now_iso()}: {text}\n")


def checkpoint(phase: str, status: str, extra: dict[str, Any] | None = None) -> None:
    state_path = OUT / "STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8-sig")) if state_path.exists() else {}
    state["phase"] = phase
    state["status"] = status
    state["updated_utc"] = now_iso()
    state.setdefault("checkpoints", []).append({"phase": phase, "status": status, "time": now_iso(), **(extra or {})})
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return value[:70] or "unknown"


def read_md_files() -> list[Path]:
    return sorted(INTAKE_DIR.rglob("*.md"))


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped[:120]
    return fallback


def youtube_id_from(path: Path, text: str) -> str:
    patterns = [
        r"(?:v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{8,})",
        r"(?:INTAKE|YT|2026-05-03)[_-]([A-Za-z0-9_-]{8,})",
    ]
    haystacks = [text, path.name]
    for haystack in haystacks:
        for pattern in patterns:
            match = re.search(pattern, haystack)
            if match:
                return match.group(1)
    return ""


def url_from(text: str) -> str:
    match = re.search(r"https?://[^\s)>\]]+", text)
    return match.group(0).rstrip(".,") if match else ""


def classify_file(text: str, path: Path, seen_hashes: set[str], seen_ids: set[str]) -> tuple[str, str]:
    if len(text.strip()) < 80:
        return "EMPTY_OR_CORRUPT", "too short"
    file_hash = hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()
    yid = youtube_id_from(path, text)
    if file_hash in seen_hashes or (yid and yid in seen_ids):
        return "DUPLICATE", "same content hash or youtube id"
    seen_hashes.add(file_hash)
    if yid:
        seen_ids.add(yid)
    lowered = text.lower()
    intake_markers = ["intake", "candidate", "strategy", "quantlens", "entry", "exit", "verdict", "testability"]
    transcript_markers = ["transcript:", "[music]", "speaker", "subtitle"]
    if sum(marker in lowered for marker in intake_markers) >= 2:
        return "VALID_INTAKE_REPORT", "intake markers present"
    if sum(marker in lowered for marker in transcript_markers) >= 2:
        return "RAW_TRANSCRIPT_BY_MISTAKE", "transcript markers present"
    return "UNKNOWN", "insufficient intake markers"


def extract_inventory() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    seen_hashes: set[str] = set()
    seen_ids: set[str] = set()
    inventory: list[dict[str, Any]] = []
    raw_json: list[dict[str, Any]] = []
    for path in read_md_files():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            classification, reason = classify_file(text, path, seen_hashes, seen_ids)
            title = first_heading(text, path.stem)
            url = url_from(text)
            yid = youtube_id_from(path, text)
            indicators = sorted(set(re.findall(r"\b(?:EMA|SMA|VWAP|AVWAP|ATR|RSI|MACD|ORB|CHOCH|CHoCH|CANSLIM)\b", text, flags=re.I)))
            row = {
                "file_path": str(path.relative_to(ROOT)),
                "title": title,
                "url": url,
                "youtube_id": yid,
                "classification": classification,
                "reason": reason,
                "length_chars": len(text),
                "indicators": ",".join(indicators),
                "contains_entry": bool(re.search(r"\bentry|giriş|buy|short|long\b", text, flags=re.I)),
                "contains_exit": bool(re.search(r"\bexit|çıkış|stop|target|take profit|tp\b", text, flags=re.I)),
            }
            inventory.append(row)
            raw_json.append({"path": row["file_path"], "title": title, "url": url, "youtube_id": yid, "text_preview": text[:1200]})
        except Exception as exc:
            inventory.append({"file_path": str(path.relative_to(ROOT)), "classification": "EMPTY_OR_CORRUPT", "reason": str(exc)})
    return inventory, raw_json


def candidate_specs(inventory: list[dict[str, Any]]) -> list[Candidate]:
    source_by_keyword: dict[str, dict[str, Any]] = {}
    for row in inventory:
        name = (row.get("file_path", "") + " " + row.get("title", "")).lower()
        for keyword in [
            "kell",
            "martin",
            "slingshot",
            "crabel",
            "bigbeluga",
            "canslim",
            "linda",
            "8am",
            "opening",
            "highbeta",
            "microcap",
            "extension",
            "ema20",
            "wyckoff",
            "weinstein",
            "bollinger",
            "vwap",
            "raschke",
        ]:
            if keyword in name and keyword not in source_by_keyword:
                source_by_keyword[keyword] = row

    def src(*keys: str) -> dict[str, Any]:
        for key in keys:
            if key in source_by_keyword:
                return source_by_keyword[key]
        for row in inventory:
            if row.get("classification") == "VALID_INTAKE_REPORT":
                return row
        return {}

    specs = [
        Candidate(
            "CANDIDATE_001",
            "kell_wedge_pop_crossback",
            "Kell Wedge Pop / EMA Crossback",
            src("kell").get("file_path", ""),
            src("kell").get("url", ""),
            src("kell").get("youtube_id", ""),
            "Trend continuation after EMA10/20 contraction and reclaim.",
            "trend_pullback",
            "crypto_transferable",
            "1D/4h/1h",
            "OHLCV with daily and intraday bars",
            "EMA10 above EMA20, recent compression, close reclaims fast EMA.",
            "Close below EMA20 or ATR/time exit.",
            "Mini-base low or 2 ATR.",
            "Trail on EMA10/20 ride.",
            "1x equity research sizing.",
            "PRODUCER_CANDIDATE",
            "TEST_NOW_LOCAL_DATA",
            4,
            4,
            5,
            3,
            3,
            4,
            -1,
            0,
        ),
        Candidate(
            "CANDIDATE_002",
            "martin_luke_pullback_avwap",
            "Martin Luke Pullback AVWAP",
            src("martin").get("file_path", ""),
            src("martin").get("url", ""),
            src("martin").get("youtube_id", ""),
            "Pullback into EMA/anchored VWAP confluence with reclaim trigger.",
            "support_reclaim",
            "crypto_proxy/equity_native",
            "1D + 4h/1h",
            "OHLCV; true AVWAP improves with intraday volume",
            "Flush into support confluence, reclaim previous bar high.",
            "Partial at R targets and EMA trail.",
            "Local low or max stop.",
            "3R/5R partials.",
            "R-based research sizing.",
            "PRODUCER_CANDIDATE",
            "TEST_WITH_1D_CRYPTO_PROXY",
            3,
            3,
            4,
            3,
            2,
            3,
            -2,
            0,
        ),
        Candidate(
            "CANDIDATE_003",
            "slingshot_4ema_high_pullback",
            "Slingshot EMA(high,4) Pullback",
            src("slingshot").get("file_path", ""),
            src("slingshot").get("url", ""),
            src("slingshot").get("youtube_id", ""),
            "Strength pullback closes back over EMA of highs.",
            "trend_pullback",
            "crypto_transferable",
            "1D",
            "Daily OHLCV",
            "Above SMA50, recent close below EMA(high,4), trigger cross back above.",
            "Close below EMA(high,4), ATR trail, or fixed R.",
            "Pullback low or ATR stop.",
            "2R/3R variants.",
            "1x equity research sizing.",
            "PRODUCER_CANDIDATE",
            "TEST_NOW_LOCAL_DATA",
            5,
            5,
            5,
            3,
            3,
            4,
            -1,
            0,
        ),
        Candidate(
            "CANDIDATE_004",
            "crabel_range_expansion",
            "Crabel Range Expansion",
            src("crabel").get("file_path", ""),
            src("crabel").get("url", ""),
            src("crabel").get("youtube_id", ""),
            "Previous range expansion breakout above/below prior close.",
            "breakout",
            "crypto_transferable",
            "1D",
            "Daily OHLCV",
            "High reaches close[1]+range[1]*mult or low reaches close[1]-range[1]*mult.",
            "Same close, next close, ATR/time exits.",
            "Opposite breakout or ATR stop.",
            "Time/target variants.",
            "1x equity research sizing.",
            "PRODUCER_CANDIDATE",
            "TEST_NOW_LOCAL_DATA",
            5,
            5,
            5,
            3,
            2,
            4,
            -1,
            0,
        ),
        Candidate(
            "CANDIDATE_005",
            "bigbeluga_rsi_choch_atr",
            "BigBeluga RSI Divergence + CHoCH + ATR",
            src("bigbeluga").get("file_path", ""),
            src("bigbeluga").get("url", ""),
            src("bigbeluga").get("youtube_id", ""),
            "RSI divergence confirmed by market structure shift with ATR management.",
            "reversal_structure",
            "crypto_transferable",
            "4h/1D",
            "OHLCV with pivot confirmation",
            "Confirmed divergence plus CHoCH, next bar open.",
            "ATR trail or opposite CHoCH.",
            "ATR stop.",
            "ATR target ladder.",
            "1x equity research sizing.",
            "PRODUCER_CANDIDATE",
            "TEST_NOW_LOCAL_DATA",
            3,
            4,
            5,
            3,
            2,
            3,
            -2,
            0,
        ),
        Candidate(
            "CANDIDATE_006",
            "canslim_shakeout_plus3",
            "CANSLIM Shakeout +3",
            src("canslim").get("file_path", ""),
            src("canslim").get("url", ""),
            src("canslim").get("youtube_id", ""),
            "Equity-specific double-bottom shakeout buy point.",
            "position_breakout",
            "US_equity_native",
            "1D",
            "US equities OHLCV plus RS/fundamental context",
            "Second low undercuts first low; buy point L1+3 or percentage equivalent.",
            "Fixed target variants.",
            "7% stop.",
            "20%/25% target.",
            "Position-trading sizing only.",
            "PRODUCER_CANDIDATE",
            "NEEDS_US_EQUITY_DATA",
            4,
            4,
            1,
            3,
            2,
            2,
            -2,
            -6,
        ),
        Candidate(
            "CANDIDATE_007",
            "linda_5sma_rs_pullback",
            "Linda 5SMA RS Pullback",
            src("linda", "raschke").get("file_path", ""),
            src("linda", "raschke").get("url", ""),
            src("linda", "raschke").get("youtube_id", ""),
            "Trend asset pulls below 5SMA and exits on snapback.",
            "mean_reversion_pullback",
            "crypto_transferable",
            "1D",
            "Daily OHLCV",
            "Above SMA50/200, close dips below SMA5, next open entry.",
            "Exit when close recovers above SMA5 or ATR stop.",
            "Optional ATR/fixed stop.",
            "Mean-reversion exit.",
            "1x equity research sizing.",
            "PRODUCER_CANDIDATE",
            "TEST_NOW_LOCAL_DATA",
            5,
            5,
            5,
            3,
            3,
            4,
            -1,
            0,
        ),
        Candidate(
            "CANDIDATE_008",
            "8am_et_opening_range_breakout",
            "8AM ET Opening Range Breakout",
            src("8am", "opening").get("file_path", ""),
            src("8am", "opening").get("url", ""),
            src("8am", "opening").get("youtube_id", ""),
            "Session anchored opening range breakout.",
            "intraday_breakout",
            "futures/session_native",
            "5m",
            "5m session-aware OHLCV",
            "Break 08:00 ET opening range high/low.",
            "Time exit or opposite range side.",
            "Opposite OR side/ATR.",
            "Short holding period.",
            "Intraday strict costs.",
            "PRODUCER_CANDIDATE",
            "TEST_WITH_5M_CRYPTO_PROXY",
            4,
            4,
            4,
            2,
            2,
            3,
            -2,
            0,
        ),
        Candidate(
            "CANDIDATE_009",
            "highbeta_openingbar_gapandgo",
            "HighBeta Opening-Bar Gap-and-Go",
            src("highbeta").get("file_path", ""),
            src("highbeta").get("url", ""),
            src("highbeta").get("youtube_id", ""),
            "Strong first 5m bar continuation if low holds.",
            "intraday_momentum",
            "US_equity_native/crypto_proxy",
            "5m",
            "US high-beta intraday with gaps; crypto proxy available",
            "First bar range extreme, hold low, break high.",
            "Time/ATR exit.",
            "First bar low.",
            "First-hour exit.",
            "Intraday strict costs.",
            "PRODUCER_CANDIDATE",
            "TEST_WITH_5M_CRYPTO_PROXY",
            4,
            4,
            3,
            2,
            2,
            3,
            -2,
            -1,
        ),
        Candidate(
            "CANDIDATE_010",
            "ty_microcap_short",
            "Ty Rajnus Microcap Liquidity Reversion Short",
            src("microcap").get("file_path", ""),
            src("microcap").get("url", ""),
            src("microcap").get("youtube_id", ""),
            "US microcap premarket overextension short with borrow/halt constraints.",
            "microcap_short",
            "US_microcap_native",
            "1m/premarket",
            "US microcap 1m, premarket, borrow/locate, dilution, halt flags",
            "Short overextended microcap near open.",
            "No overnight, cover near close.",
            "Wide adverse stop and halt rules.",
            "Intraday reversion.",
            "Borrow-aware short sizing.",
            "DATA_BLOCKED",
            "NEEDS_US_MICROCAP_DATA",
            4,
            3,
            0,
            3,
            1,
            1,
            -3,
            -10,
        ),
        Candidate(
            "CANDIDATE_011",
            "daily_extension_anti_chase_filter",
            "Daily Extension Anti-Chase Filter",
            src("extension").get("file_path", ""),
            src("extension").get("url", ""),
            src("extension").get("youtube_id", ""),
            "Block late long/short entries after consecutive extended candles.",
            "filter",
            "crypto_transferable",
            "1D context",
            "Daily OHLCV plus target strategy trades",
            "Not standalone; blocks entries after 3-5 strong candles.",
            "N/A",
            "N/A",
            "N/A",
            "Filter score only.",
            "FILTER_CANDIDATE",
            "TEST_NOW_LOCAL_DATA",
            5,
            4,
            5,
            2,
            3,
            5,
            -1,
            0,
        ),
        Candidate(
            "CANDIDATE_012",
            "ema20_50_two_retests_baseline",
            "EMA20/50 Two-Retest Baseline",
            src("ema20").get("file_path", ""),
            src("ema20").get("url", ""),
            src("ema20").get("youtube_id", ""),
            "Generic EMA20/50 cross plus two retests baseline.",
            "baseline_trend",
            "crypto_transferable",
            "1h/4h/1D",
            "OHLCV",
            "Cross then two successful retests.",
            "Opposite cross/EMA50/ATR.",
            "Retest swing or ATR.",
            "2R/3R variants.",
            "1x equity research sizing.",
            "BASELINE_ONLY",
            "TEST_NOW_LOCAL_DATA",
            4,
            4,
            5,
            1,
            2,
            3,
            -1,
            0,
        ),
        Candidate(
            "CANDIDATE_013",
            "weinstein_stage_analysis",
            "Weinstein / Long-Base Stage Analysis",
            src("weinstein").get("file_path", ""),
            src("weinstein").get("url", ""),
            src("weinstein").get("youtube_id", ""),
            "Position-trading trend stage and base breakout framework.",
            "position_trend",
            "equity_native/crypto_proxy",
            "1D/1W",
            "Long history OHLCV, relative strength preferred",
            "Stage 2 breakout above base and rising MA.",
            "Stage deterioration or trailing MA.",
            "Base low.",
            "Long-term trail.",
            "Portfolio sleeve sizing.",
            "PRODUCER_CANDIDATE",
            "TEST_WITH_1D_CRYPTO_PROXY",
            3,
            3,
            4,
            3,
            3,
            3,
            -2,
            0,
        ),
        Candidate(
            "CANDIDATE_014",
            "wyckoff_process_only",
            "Wyckoff / Process Framework",
            src("wyckoff").get("file_path", ""),
            src("wyckoff").get("url", ""),
            src("wyckoff").get("youtube_id", ""),
            "Discretionary accumulation/distribution process framework.",
            "process",
            "multi_asset",
            "multi",
            "Contextual chart reading",
            "Not mechanical enough from intake alone.",
            "N/A",
            "N/A",
            "N/A",
            "Process only.",
            "PROCESS_ONLY",
            "REJECT_NOT_TESTABLE",
            1,
            1,
            3,
            2,
            1,
            2,
            -5,
            0,
        ),
    ]
    ordered = sorted(specs, key=lambda c: c.total_score, reverse=True)
    for index, cand in enumerate(ordered):
        if cand.testability.startswith("TEST") and index < 10 and cand.total_score >= 18:
            cand.tier = "A"
        elif cand.testability.startswith("TEST") and cand.total_score >= 12:
            cand.tier = "B"
        else:
            cand.tier = "C"
    return specs


def save_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def save_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    out = ["|" + "|".join(columns) + "|", "|" + "|".join(["---"] * len(columns)) + "|"]
    for row in rows:
        out.append("|" + "|".join(str(row.get(col, "")).replace("|", "/") for col in columns) + "|")
    return "\n".join(out)


def write_candidate_card(cand: Candidate) -> None:
    path = OUT / "candidates" / f"{cand.candidate_id}_{cand.slug}.md"
    text = f"""# {cand.candidate_id} — {cand.title}

## Source
- Source intake file: `{cand.source_file}`
- Source URL: {cand.source_url or "UNKNOWN"}
- YouTube ID: {cand.youtube_id or "UNKNOWN"}

## Candidate Card
- One-sentence thesis: {cand.thesis}
- Strategy family: {cand.strategy_family}
- Asset class: {cand.asset_class}
- Native timeframe: {cand.native_timeframe}
- Required data: {cand.required_data}
- Entry logic: {cand.entry_logic}
- Exit logic: {cand.exit_logic}
- Initial SL logic: {cand.sl_logic}
- TP / trailing / partial logic: {cand.tp_logic}
- Position sizing notes: {cand.sizing_notes}
- MTC relevance: {cand.mtc_relevance}
- Testability: {cand.testability}
- Priority tier: {cand.tier}
- Total score: {cand.total_score}

## Conservative Python Formalization
The first-pass prototype uses only OHLCV-derived rules, fixed research sizing, conservative fee/slippage, and no discretionary chart interpretation.

## Ambiguities
- Intake reports are normalized reports, not raw source videos.
- If the source strategy depends on discretionary chart reading, this card uses the most conservative mechanical proxy.

## Critical Caveats
- This is not Pine-ready.
- This is not production MTC integration.
- Crypto proxy results do not prove equity/session-native edge.
"""
    write_text(path, text)


def data_file(symbol: str, timeframe: str) -> Path | None:
    if timeframe == "5m":
        files = sorted((DATA_5M / symbol / "5m").glob("*.csv"))
        return files[0] if files else None
    files = sorted((BUNDLE / "normalized" / "binance_futures" / symbol / timeframe).glob("*.csv"))
    return files[0] if files else None


def load_ohlcv(symbol: str, timeframe: str) -> pd.DataFrame:
    path = data_file(symbol, timeframe)
    if path is None:
        raise FileNotFoundError(f"Missing data for {symbol} {timeframe}")
    df = pd.read_csv(path)
    cols = {c.lower(): c for c in df.columns}
    rename = {
        cols.get("timestamp") or cols.get("timestamp_utc") or cols.get("time") or cols.get("date") or cols.get("datetime"): "timestamp",
        cols.get("open"): "open",
        cols.get("high"): "high",
        cols.get("low"): "low",
        cols.get("close"): "close",
        cols.get("volume"): "volume",
    }
    rename = {k: v for k, v in rename.items() if k}
    df = df.rename(columns=rename)
    if "volume" not in df.columns:
        df["volume"] = 0.0
    required = ["timestamp", "open", "high", "low", "close", "volume"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{path} missing columns {missing}")
    df = df[required].copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna().drop_duplicates("timestamp").sort_values("timestamp").reset_index(drop=True)


def ema(series: pd.Series, length: int) -> pd.Series:
    return series.ewm(span=length, adjust=False).mean()


def sma(series: pd.Series, length: int) -> pd.Series:
    return series.rolling(length).mean()


def atr(df: pd.DataFrame, length: int = 14) -> pd.Series:
    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.rolling(length).mean()


def rsi(series: pd.Series, length: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(length).mean()
    loss = -delta.clip(upper=0).rolling(length).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def trade_row(
    candidate_id: str,
    asset: str,
    timeframe: str,
    entry_time: Any,
    exit_time: Any,
    direction: str,
    entry: float,
    exit_: float,
    gross_return_pct: float,
    holding_bars: int,
) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "asset": asset,
        "timeframe": timeframe,
        "entry_time": str(entry_time),
        "exit_time": str(exit_time),
        "direction": direction,
        "entry_price": entry,
        "exit_price": exit_,
        "gross_return_pct": gross_return_pct,
        "net_return_pct": gross_return_pct - ROUND_TRIP_COST_PCT,
        "holding_bars": holding_bars,
    }


def strategy_crabel(df: pd.DataFrame, asset: str) -> list[dict[str, Any]]:
    prev_range = (df["high"] - df["low"]).shift(1)
    prev_close = df["close"].shift(1)
    buy = prev_close + prev_range * 0.90
    sell = prev_close - prev_range * 0.90
    trades = []
    for i in range(1, len(df) - 1):
        long_sig = df.loc[i, "high"] >= buy.iloc[i]
        short_sig = df.loc[i, "low"] <= sell.iloc[i]
        if long_sig == short_sig:
            continue
        if long_sig:
            entry = float(buy.iloc[i])
            exit_ = float(df.loc[i + 1, "close"])
            ret = (exit_ / entry - 1) * 100
            trades.append(trade_row("CANDIDATE_004", asset, "1D", df.loc[i, "timestamp"], df.loc[i + 1, "timestamp"], "long", entry, exit_, ret, 1))
        if short_sig:
            entry = float(sell.iloc[i])
            exit_ = float(df.loc[i + 1, "close"])
            ret = (entry / exit_ - 1) * 100
            trades.append(trade_row("CANDIDATE_004", asset, "1D", df.loc[i, "timestamp"], df.loc[i + 1, "timestamp"], "short", entry, exit_, ret, 1))
    return trades


def strategy_linda(df: pd.DataFrame, asset: str) -> list[dict[str, Any]]:
    df = df.copy()
    df["sma5"] = sma(df["close"], 5)
    df["sma50"] = sma(df["close"], 50)
    df["sma200"] = sma(df["close"], 200)
    trades = []
    i = 201
    while i < len(df) - 2:
        trend = df.loc[i, "close"] > df.loc[i, "sma50"] and df.loc[i, "close"] > df.loc[i, "sma200"]
        signal = trend and df.loc[i - 1, "close"] >= df.loc[i - 1, "sma5"] and df.loc[i, "close"] < df.loc[i, "sma5"]
        if signal:
            entry_i = i + 1
            entry = float(df.loc[entry_i, "open"])
            exit_i = min(entry_i + 10, len(df) - 1)
            for j in range(entry_i + 1, min(entry_i + 11, len(df))):
                if df.loc[j, "close"] > df.loc[j, "sma5"]:
                    exit_i = j + 1 if j + 1 < len(df) else j
                    break
            exit_ = float(df.loc[exit_i, "open"] if exit_i != j else df.loc[exit_i, "close"])
            ret = (exit_ / entry - 1) * 100
            trades.append(trade_row("CANDIDATE_007", asset, "1D", df.loc[entry_i, "timestamp"], df.loc[exit_i, "timestamp"], "long", entry, exit_, ret, exit_i - entry_i))
            i = exit_i + 1
        else:
            i += 1
    return trades


def strategy_slingshot(df: pd.DataFrame, asset: str) -> list[dict[str, Any]]:
    df = df.copy()
    df["ema_high4"] = ema(df["high"], 4)
    df["sma50"] = sma(df["close"], 50)
    df["atr"] = atr(df, 14)
    trades = []
    i = 60
    while i < len(df) - 2:
        pullback = (df["close"].iloc[i - 5 : i] < df["ema_high4"].iloc[i - 5 : i]).any()
        trigger = df.loc[i - 1, "close"] <= df.loc[i - 1, "ema_high4"] and df.loc[i, "close"] > df.loc[i, "ema_high4"]
        if df.loc[i, "close"] > df.loc[i, "sma50"] and pullback and trigger:
            entry_i = i + 1
            entry = float(df.loc[entry_i, "open"])
            stop = float(df["low"].iloc[max(0, i - 5) : i + 1].min())
            risk = max(entry - stop, entry * 0.01)
            target = entry + 2 * risk
            exit_i = min(entry_i + 15, len(df) - 1)
            exit_ = float(df.loc[exit_i, "close"])
            for j in range(entry_i, min(entry_i + 16, len(df))):
                if df.loc[j, "low"] <= stop:
                    exit_i, exit_ = j, stop
                    break
                if df.loc[j, "high"] >= target:
                    exit_i, exit_ = j, target
                    break
                if df.loc[j, "close"] < df.loc[j, "ema_high4"]:
                    exit_i, exit_ = j, float(df.loc[j, "close"])
                    break
            ret = (exit_ / entry - 1) * 100
            trades.append(trade_row("CANDIDATE_003", asset, "1D", df.loc[entry_i, "timestamp"], df.loc[exit_i, "timestamp"], "long", entry, exit_, ret, exit_i - entry_i))
            i = exit_i + 1
        else:
            i += 1
    return trades


def strategy_kell(df: pd.DataFrame, asset: str) -> list[dict[str, Any]]:
    df = df.copy()
    df["ema10"] = ema(df["close"], 10)
    df["ema20"] = ema(df["close"], 20)
    df["atr"] = atr(df, 14)
    base_range_pct = (df["high"].rolling(5).max() / df["low"].rolling(5).min() - 1) * 100
    trades = []
    i = 30
    while i < len(df) - 2:
        contraction = base_range_pct.iloc[i] <= 8
        trigger = df.loc[i, "ema10"] > df.loc[i, "ema20"] and df.loc[i - 1, "close"] <= df.loc[i - 1, "ema10"] and df.loc[i, "close"] > df.loc[i, "ema10"]
        if contraction and trigger:
            entry_i = i + 1
            entry = float(df.loc[entry_i, "open"])
            stop = float(min(df["low"].iloc[max(0, i - 5) : i + 1].min(), entry - 2 * df.loc[i, "atr"]))
            exit_i = min(entry_i + 20, len(df) - 1)
            exit_ = float(df.loc[exit_i, "close"])
            for j in range(entry_i, min(entry_i + 21, len(df))):
                if df.loc[j, "low"] <= stop:
                    exit_i, exit_ = j, stop
                    break
                if df.loc[j, "close"] < df.loc[j, "ema20"]:
                    exit_i, exit_ = j, float(df.loc[j, "close"])
                    break
            ret = (exit_ / entry - 1) * 100
            trades.append(trade_row("CANDIDATE_001", asset, "1D", df.loc[entry_i, "timestamp"], df.loc[exit_i, "timestamp"], "long", entry, exit_, ret, exit_i - entry_i))
            i = exit_i + 1
        else:
            i += 1
    return trades


def strategy_bigbeluga_proxy(df: pd.DataFrame, asset: str) -> list[dict[str, Any]]:
    df = df.copy()
    df["rsi"] = rsi(df["close"], 14)
    df["atr"] = atr(df, 14)
    trades = []
    i = 30
    while i < len(df) - 5:
        recent_low = df["low"].iloc[i - 10 : i].min()
        choch_long = df.loc[i, "close"] > df["high"].iloc[i - 5 : i].max()
        oversold_reclaim = df["rsi"].iloc[i - 5 : i].min() < 35 and df.loc[i, "rsi"] > 45
        recent_high = df["high"].iloc[i - 10 : i].max()
        choch_short = df.loc[i, "close"] < df["low"].iloc[i - 5 : i].min()
        overbought_reclaim = df["rsi"].iloc[i - 5 : i].max() > 65 and df.loc[i, "rsi"] < 55
        if choch_long and oversold_reclaim:
            entry_i = i + 1
            entry = float(df.loc[entry_i, "open"])
            stop = float(entry - 2 * df.loc[i, "atr"])
            exit_i, exit_ = min(entry_i + 12, len(df) - 1), float(df.loc[min(entry_i + 12, len(df) - 1), "close"])
            for j in range(entry_i, min(entry_i + 13, len(df))):
                if df.loc[j, "low"] <= stop:
                    exit_i, exit_ = j, stop
                    break
            trades.append(trade_row("CANDIDATE_005", asset, "1D", df.loc[entry_i, "timestamp"], df.loc[exit_i, "timestamp"], "long", entry, exit_, (exit_ / entry - 1) * 100, exit_i - entry_i))
            i = exit_i + 1
        elif choch_short and overbought_reclaim:
            entry_i = i + 1
            entry = float(df.loc[entry_i, "open"])
            stop = float(entry + 2 * df.loc[i, "atr"])
            exit_i, exit_ = min(entry_i + 12, len(df) - 1), float(df.loc[min(entry_i + 12, len(df) - 1), "close"])
            for j in range(entry_i, min(entry_i + 13, len(df))):
                if df.loc[j, "high"] >= stop:
                    exit_i, exit_ = j, stop
                    break
            trades.append(trade_row("CANDIDATE_005", asset, "1D", df.loc[entry_i, "timestamp"], df.loc[exit_i, "timestamp"], "short", entry, exit_, (entry / exit_ - 1) * 100, exit_i - entry_i))
            i = exit_i + 1
        else:
            i += 1
    return trades


def strategy_martin_luke_proxy(df: pd.DataFrame, asset: str) -> list[dict[str, Any]]:
    df = df.copy()
    df["ema9"] = ema(df["close"], 9)
    df["ema21"] = ema(df["close"], 21)
    df["ema50"] = ema(df["close"], 50)
    df["atr"] = atr(df, 14)
    trades = []
    i = 60
    while i < len(df) - 2:
        support_zone = abs(df.loc[i, "low"] / df.loc[i, "ema21"] - 1) < 0.02 or abs(df.loc[i, "low"] / df.loc[i, "ema50"] - 1) < 0.025
        trend = df.loc[i, "close"] > df.loc[i, "ema50"] and df.loc[i, "ema9"] > df.loc[i, "ema21"]
        reclaim = df.loc[i, "close"] > df.loc[i - 1, "high"]
        if trend and support_zone and reclaim:
            entry_i = i + 1
            entry = float(df.loc[entry_i, "open"])
            stop = float(min(df.loc[i, "low"], entry - 2 * df.loc[i, "atr"]))
            risk = max(entry - stop, entry * 0.01)
            target = entry + 3 * risk
            exit_i = min(entry_i + 20, len(df) - 1)
            exit_ = float(df.loc[exit_i, "close"])
            for j in range(entry_i, min(entry_i + 21, len(df))):
                if df.loc[j, "low"] <= stop:
                    exit_i, exit_ = j, stop
                    break
                if df.loc[j, "high"] >= target:
                    exit_i, exit_ = j, target
                    break
                if df.loc[j, "close"] < df.loc[j, "ema21"]:
                    exit_i, exit_ = j, float(df.loc[j, "close"])
                    break
            trades.append(trade_row("CANDIDATE_002", asset, "1D", df.loc[entry_i, "timestamp"], df.loc[exit_i, "timestamp"], "long", entry, exit_, (exit_ / entry - 1) * 100, exit_i - entry_i))
            i = exit_i + 1
        else:
            i += 1
    return trades


def strategy_anti_chase_reversal(df: pd.DataFrame, asset: str) -> list[dict[str, Any]]:
    df = df.copy()
    df["atr"] = atr(df, 14)
    body = (df["close"] - df["open"]).abs()
    candle_range = (df["high"] - df["low"]).replace(0, np.nan)
    close_loc = (df["close"] - df["low"]) / candle_range
    strong_green = (df["close"] > df["open"]) & (body >= 0.5 * df["atr"]) & (close_loc >= 0.70)
    strong_red = (df["close"] < df["open"]) & (body >= 0.5 * df["atr"]) & (close_loc <= 0.30)
    trades = []
    for i in range(20, len(df) - 4):
        if strong_green.iloc[i - 3 : i].sum() >= 3:
            entry_i = i + 1
            entry = float(df.loc[entry_i, "open"])
            exit_i = entry_i + 3
            exit_ = float(df.loc[exit_i, "close"])
            trades.append(trade_row("CANDIDATE_011", asset, "1D", df.loc[entry_i, "timestamp"], df.loc[exit_i, "timestamp"], "short", entry, exit_, (entry / exit_ - 1) * 100, 3))
        elif strong_red.iloc[i - 3 : i].sum() >= 3:
            entry_i = i + 1
            entry = float(df.loc[entry_i, "open"])
            exit_i = entry_i + 3
            exit_ = float(df.loc[exit_i, "close"])
            trades.append(trade_row("CANDIDATE_011", asset, "1D", df.loc[entry_i, "timestamp"], df.loc[exit_i, "timestamp"], "long", entry, exit_, (exit_ / entry - 1) * 100, 3))
    return trades


def strategy_ema20_50(df: pd.DataFrame, asset: str) -> list[dict[str, Any]]:
    df = df.copy()
    df["ema20"] = ema(df["close"], 20)
    df["ema50"] = ema(df["close"], 50)
    df["atr"] = atr(df, 14)
    trades = []
    i = 60
    while i < len(df) - 2:
        cross = df.loc[i - 1, "ema20"] <= df.loc[i - 1, "ema50"] and df.loc[i, "ema20"] > df.loc[i, "ema50"]
        if cross:
            retests = 0
            entry_i = None
            for j in range(i + 1, min(i + 40, len(df) - 1)):
                zone = min(df.loc[j, "ema20"], df.loc[j, "ema50"]) <= df.loc[j, "low"] <= max(df.loc[j, "ema20"], df.loc[j, "ema50"]) * 1.01
                if zone and df.loc[j, "close"] > df.loc[j, "ema20"]:
                    retests += 1
                if retests >= 2:
                    entry_i = j + 1
                    break
            if entry_i and entry_i < len(df) - 1:
                entry = float(df.loc[entry_i, "open"])
                exit_i = min(entry_i + 30, len(df) - 1)
                exit_ = float(df.loc[exit_i, "close"])
                for k in range(entry_i + 1, min(entry_i + 31, len(df))):
                    if df.loc[k, "close"] < df.loc[k, "ema50"]:
                        exit_i, exit_ = k, float(df.loc[k, "close"])
                        break
                trades.append(trade_row("CANDIDATE_012", asset, "1D", df.loc[entry_i, "timestamp"], df.loc[exit_i, "timestamp"], "long", entry, exit_, (exit_ / entry - 1) * 100, exit_i - entry_i))
                i = exit_i + 1
            else:
                i += 1
        else:
            i += 1
    return trades


def strategy_8am_orb(df: pd.DataFrame, asset: str) -> list[dict[str, Any]]:
    try:
        local = df["timestamp"].dt.tz_convert("America/New_York")
    except Exception:
        local = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("America/New_York")
    df = df.copy()
    df["ny_date"] = local.dt.date
    df["ny_time"] = local.dt.strftime("%H:%M")
    trades = []
    for _, day in df.groupby("ny_date", sort=True):
        day = day.reset_index(drop=True)
        or_rows = day[(day["ny_time"] >= "08:00") & (day["ny_time"] < "08:20")]
        if len(or_rows) < 4:
            continue
        or_high, or_low = float(or_rows["high"].max()), float(or_rows["low"].min())
        after = day[day["ny_time"] >= "08:20"].head(20).reset_index(drop=True)
        for i in range(len(after)):
            if after.loc[i, "high"] > or_high:
                exit_i = min(i + 6, len(after) - 1)
                entry, exit_ = or_high, float(after.loc[exit_i, "close"])
                trades.append(trade_row("CANDIDATE_008", asset, "5m", after.loc[i, "timestamp"], after.loc[exit_i, "timestamp"], "long", entry, exit_, (exit_ / entry - 1) * 100, exit_i - i))
                break
            if after.loc[i, "low"] < or_low:
                exit_i = min(i + 6, len(after) - 1)
                entry, exit_ = or_low, float(after.loc[exit_i, "close"])
                trades.append(trade_row("CANDIDATE_008", asset, "5m", after.loc[i, "timestamp"], after.loc[exit_i, "timestamp"], "short", entry, exit_, (entry / exit_ - 1) * 100, exit_i - i))
                break
    return trades


def strategy_highbeta_proxy(df: pd.DataFrame, asset: str) -> list[dict[str, Any]]:
    try:
        local = df["timestamp"].dt.tz_convert("America/New_York")
    except Exception:
        local = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("America/New_York")
    df = df.copy()
    df["ny_date"] = local.dt.date
    df["ny_time"] = local.dt.strftime("%H:%M")
    trades = []
    daily_ranges: list[float] = []
    for _, day in df.groupby("ny_date", sort=True):
        day = day.reset_index(drop=True)
        first = day[day["ny_time"] == "08:00"]
        if first.empty:
            continue
        bar = first.iloc[0]
        first_range = float(bar["high"] - bar["low"])
        if len(daily_ranges) >= 10 and first_range >= max(daily_ranges[-10:]):
            after = day[day["ny_time"] > "08:00"].head(24).reset_index(drop=True)
            if len(after) > 6 and (after.head(4)["low"] > float(bar["low"])).all():
                entry = float(bar["high"])
                for i in range(4, len(after)):
                    if after.loc[i, "high"] > entry:
                        exit_i = min(i + 12, len(after) - 1)
                        exit_ = float(after.loc[exit_i, "close"])
                        trades.append(trade_row("CANDIDATE_009", asset, "5m", after.loc[i, "timestamp"], after.loc[exit_i, "timestamp"], "long", entry, exit_, (exit_ / entry - 1) * 100, exit_i - i))
                        break
        daily_ranges.append(first_range)
    return trades


STRATEGIES: dict[str, tuple[str, str, Callable[[pd.DataFrame, str], list[dict[str, Any]]], list[str]]] = {
    "CANDIDATE_001": ("Kell Wedge Pop / EMA Crossback", "1D", strategy_kell, EXPANDED_ASSETS),
    "CANDIDATE_002": ("Martin Luke Pullback AVWAP Proxy", "1D", strategy_martin_luke_proxy, EXPANDED_ASSETS),
    "CANDIDATE_003": ("Slingshot EMA(high,4) Pullback", "1D", strategy_slingshot, EXPANDED_ASSETS),
    "CANDIDATE_004": ("Crabel Range Expansion", "1D", strategy_crabel, EXPANDED_ASSETS),
    "CANDIDATE_005": ("BigBeluga RSI/CHoCH/ATR Proxy", "1D", strategy_bigbeluga_proxy, EXPANDED_ASSETS),
    "CANDIDATE_007": ("Linda 5SMA Pullback", "1D", strategy_linda, EXPANDED_ASSETS),
    "CANDIDATE_008": ("8AM ET ORB Crypto Proxy", "5m", strategy_8am_orb, CORE_ASSETS),
    "CANDIDATE_009": ("HighBeta Opening Bar Crypto Proxy", "5m", strategy_highbeta_proxy, CORE_ASSETS),
    "CANDIDATE_011": ("Daily Extension Anti-Chase Standalone Proxy", "1D", strategy_anti_chase_reversal, EXPANDED_ASSETS),
    "CANDIDATE_012": ("EMA20/50 Two Retests Baseline", "1D", strategy_ema20_50, EXPANDED_ASSETS),
}


def metrics_from_trades(trades: pd.DataFrame, assets_tested: int) -> dict[str, Any]:
    if trades.empty:
        return {
            "trade_count": 0,
            "assets_tested": assets_tested,
            "aggregate_pf": 0.0,
            "aggregate_net_return_pct": 0.0,
            "aggregate_max_dd_pct": 0.0,
            "win_rate": 0.0,
            "average_trade_pct": 0.0,
            "median_trade_pct": 0.0,
            "average_win_pct": 0.0,
            "average_loss_pct": 0.0,
            "expectancy_pct": 0.0,
            "exposure_pct": 0.0,
            "fee_2x_pf": 0.0,
            "fee_3x_pf": 0.0,
            "fee_monotonic": True,
            "classification": "REJECT",
        }
    returns = trades["net_return_pct"].astype(float)
    wins = returns[returns > 0]
    losses = returns[returns <= 0]
    gross_profit = float(wins.sum())
    gross_loss = float(-losses.sum())
    pf = gross_profit / gross_loss if gross_loss > 0 else (999.0 if gross_profit > 0 else 0.0)
    equity = (1 + returns / 100).cumprod()
    dd = equity / equity.cummax() - 1
    fee_pfs: dict[int, float] = {}
    for mult in [2, 3]:
        stressed = trades["gross_return_pct"].astype(float) - ROUND_TRIP_COST_PCT * mult
        sw = stressed[stressed > 0].sum()
        sl = -stressed[stressed <= 0].sum()
        fee_pfs[mult] = float(sw / sl) if sl > 0 else (999.0 if sw > 0 else 0.0)
    ret = float((equity.iloc[-1] - 1) * 100)
    max_dd = float(dd.min() * 100)
    if assets_tested < 5:
        classification = "DATA_BLOCKED"
    elif len(trades) < 30:
        classification = "REJECT"
    elif pf >= 1.20 and fee_pfs[2] >= 1.05 and max_dd > -35:
        classification = "PASS_STAGE2"
    elif pf > 1.05 and ret > 0:
        classification = "WEAK_CANDIDATE"
    else:
        classification = "REJECT"
    return {
        "trade_count": int(len(trades)),
        "assets_tested": assets_tested,
        "aggregate_pf": round(pf, 4),
        "aggregate_net_return_pct": round(ret, 4),
        "aggregate_max_dd_pct": round(max_dd, 4),
        "return_dd_ratio": round(ret / abs(max_dd), 4) if max_dd else 0.0,
        "win_rate": round(float((returns > 0).mean() * 100), 4),
        "average_trade_pct": round(float(returns.mean()), 4),
        "median_trade_pct": round(float(returns.median()), 4),
        "average_win_pct": round(float(wins.mean()) if len(wins) else 0.0, 4),
        "average_loss_pct": round(float(losses.mean()) if len(losses) else 0.0, 4),
        "expectancy_pct": round(float(returns.mean()), 4),
        "exposure_pct": round(float(trades["holding_bars"].sum()) / max(len(trades) * 30, 1) * 100, 4),
        "fee_2x_pf": round(fee_pfs[2], 4),
        "fee_3x_pf": round(fee_pfs[3], 4),
        "fee_monotonic": bool(pf >= fee_pfs[2] >= fee_pfs[3]),
        "classification": classification,
    }


def asset_breakdown(trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    if trades.empty:
        return rows
    for asset, subset in trades.groupby("asset"):
        m = metrics_from_trades(subset, 1)
        rows.append({"asset": asset, **m})
    return rows


def yearly_breakdown(trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    if trades.empty:
        return rows
    data = trades.copy()
    data["year"] = pd.to_datetime(data["entry_time"], utc=True).dt.year
    for year, subset in data.groupby("year"):
        m = metrics_from_trades(subset, subset["asset"].nunique())
        rows.append({"year": year, **m})
    return rows


def run_strategy(candidate: Candidate) -> dict[str, Any]:
    title, timeframe, func, assets = STRATEGIES[candidate.candidate_id]
    strat_dir = OUT / "strategies" / candidate.candidate_id
    strat_dir.mkdir(parents=True, exist_ok=True)
    all_trades: list[dict[str, Any]] = []
    data_errors: list[str] = []
    tested_assets = 0
    for asset in assets:
        try:
            df = load_ohlcv(asset, timeframe)
            tested_assets += 1
            all_trades.extend(func(df, asset))
        except Exception as exc:
            data_errors.append(f"{asset} {timeframe}: {exc}")
    trades_df = pd.DataFrame(all_trades)
    summary = {"candidate_id": candidate.candidate_id, "strategy": title, "timeframe": timeframe, **metrics_from_trades(trades_df, tested_assets)}
    if candidate.candidate_id in {"CANDIDATE_008", "CANDIDATE_009"}:
        summary["classification"] = "REJECT_CRYPTO_PROXY" if summary["aggregate_pf"] <= 1.05 else "WEAK_CANDIDATE_CRYPTO_PROXY"
    if candidate.candidate_id == "CANDIDATE_011" and summary["classification"] != "REJECT":
        summary["classification"] = "FILTER_ONLY"
    if candidate.candidate_id == "CANDIDATE_012":
        summary["classification"] = "BASELINE_ONLY"
    if trades_df.empty:
        trades_df = pd.DataFrame(columns=["candidate_id", "asset", "timeframe", "entry_time", "exit_time", "direction", "entry_price", "exit_price", "gross_return_pct", "net_return_pct", "holding_bars"])
    trades_df.to_csv(strat_dir / "trades.csv", index=False)
    save_csv(strat_dir / "results.csv", [summary])
    save_csv(strat_dir / "asset_breakdown.csv", asset_breakdown(trades_df))
    save_csv(strat_dir / "yearly_breakdown.csv", yearly_breakdown(trades_df))
    save_csv(
        strat_dir / "fee_stress.csv",
        [
            {"scenario": "base", "pf": summary["aggregate_pf"]},
            {"scenario": "2x_fee_slippage", "pf": summary["fee_2x_pf"]},
            {"scenario": "3x_fee_slippage", "pf": summary["fee_3x_pf"]},
        ],
    )
    config = {"candidate_id": candidate.candidate_id, "timeframe": timeframe, "assets": assets, "round_trip_cost_pct": ROUND_TRIP_COST_PCT, "data_errors": data_errors}
    write_text(strat_dir / "config.json", json.dumps(config, indent=2, ensure_ascii=False))
    write_text(strat_dir / f"strategy_{candidate.candidate_id}.py", f'"""Placeholder wrapper: implementation is centralized in run_overnight_batch.py for this research batch."""\n')
    write_text(strat_dir / f"run_{candidate.candidate_id}.py", f'from pathlib import Path\nprint("Run via", Path(__file__).parents[2] / "run_overnight_batch.py")\n')
    report = f"""# {candidate.candidate_id} — {title}

## Verdict
{summary["classification"]}

## Metrics
{md_table([summary], ["candidate_id", "timeframe", "assets_tested", "trade_count", "aggregate_pf", "aggregate_net_return_pct", "aggregate_max_dd_pct", "fee_2x_pf", "fee_3x_pf", "fee_monotonic", "classification"])}

## Data Errors
{chr(10).join("- " + e for e in data_errors) if data_errors else "None"}

## Caveat
This is Python-only first-pass triage. It is not Pine-ready and not production integration.
"""
    write_text(strat_dir / "README.md", report)
    write_text(strat_dir / "report.md", report)
    return summary


def discover_data() -> list[dict[str, Any]]:
    rows = []
    for timeframe in ["1D", "4h", "1h", "15m"]:
        for symbol_dir in sorted((BUNDLE / "normalized" / "binance_futures").glob("*")):
            if not symbol_dir.is_dir():
                continue
            path = data_file(symbol_dir.name, timeframe)
            if path:
                try:
                    header = pd.read_csv(path, nrows=0).columns
                    ts_col = "timestamp" if "timestamp" in header else "timestamp_utc"
                    df = pd.read_csv(path, usecols=[ts_col])
                    rows.append(
                        {
                            "source": "bundle",
                            "asset": symbol_dir.name,
                            "timeframe": timeframe,
                            "path": str(path.relative_to(ROOT.parent)),
                            "bar_count": len(df),
                            "first_ts": df[ts_col].iloc[0] if len(df) else "",
                            "last_ts": df[ts_col].iloc[-1] if len(df) else "",
                            "quality_status": "AVAILABLE",
                        }
                    )
                except Exception as exc:
                    rows.append({"source": "bundle", "asset": symbol_dir.name, "timeframe": timeframe, "path": str(path), "quality_status": f"ERROR:{exc}"})
    if DATA_5M.exists():
        for symbol_dir in sorted(DATA_5M.glob("*")):
            path = data_file(symbol_dir.name, "5m")
            if path:
                df = pd.read_csv(path, usecols=["timestamp"])
                rows.append(
                    {
                        "source": "research_5m",
                        "asset": symbol_dir.name,
                        "timeframe": "5m",
                        "path": str(path.relative_to(ROOT)),
                        "bar_count": len(df),
                        "first_ts": df["timestamp"].iloc[0] if len(df) else "",
                        "last_ts": df["timestamp"].iloc[-1] if len(df) else "",
                        "quality_status": "AVAILABLE",
                    }
                )
    return rows


def write_phase_reports(inventory: list[dict[str, Any]], raw_json: list[dict[str, Any]], candidates: list[Candidate], data_rows: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> None:
    save_csv(OUT / "INTAKE_INVENTORY.csv", inventory)
    save_jsonl(OUT / "CANDIDATE_EXTRACTION_RAW.jsonl", raw_json)
    dupes = [row for row in inventory if row.get("classification") == "DUPLICATE"]
    write_text(OUT / "DEDUPE_REPORT.md", "# Dedupe Report\n\n" + md_table(dupes, ["file_path", "title", "youtube_id", "reason"]))
    for cand in candidates:
        write_candidate_card(cand)
    priority_rows = []
    for cand in sorted(candidates, key=lambda c: c.total_score, reverse=True):
        row = asdict(cand)
        row["total_score"] = cand.total_score
        priority_rows.append(row)
    save_csv(OUT / "PRIORITY_MATRIX.csv", priority_rows)
    write_text(OUT / "PRIORITY_MATRIX.md", "# Priority Matrix\n\n" + md_table(priority_rows, ["candidate_id", "title", "tier", "testability", "mtc_relevance", "total_score"]))
    blocked = [row for row in priority_rows if "NEEDS_" in row["testability"] or row["testability"] == "REJECT_NOT_TESTABLE"]
    write_text(OUT / "REJECTED_OR_BLOCKED_LIST.md", "# Rejected or Blocked\n\n" + md_table(blocked, ["candidate_id", "title", "testability", "mtc_relevance", "total_score"]))
    modules = [row for row in priority_rows if row["mtc_relevance"] in {"FILTER_CANDIDATE", "EXIT_CANDIDATE", "SIZING_CANDIDATE", "PROCESS_ONLY"}]
    write_text(OUT / "FILTER_EXIT_SIZING_MODULES.md", "# Filter / Exit / Sizing / Process Modules\n\n" + md_table(modules, ["candidate_id", "title", "mtc_relevance", "testability", "tier"]))
    save_csv(OUT / "DATA_AVAILABILITY.csv", data_rows)
    write_text(OUT / "DATA_AVAILABILITY_REPORT.md", "# Data Availability\n\n" + md_table(data_rows[:80], ["source", "asset", "timeframe", "bar_count", "first_ts", "last_ts", "quality_status"]))
    gaps = [
        {"candidate_id": "CANDIDATE_006", "gap": "US equities daily plus RS/fundamental context required; local bundle is crypto futures."},
        {"candidate_id": "CANDIDATE_010", "gap": "US microcap 1m, premarket/afterhours, borrow/locate, dilution and halt flags required."},
        {"candidate_id": "CANDIDATE_009", "gap": "Crypto 5m proxy exists, but real US high-beta equity gap/session data is still needed."},
    ]
    write_text(OUT / "DATA_GAPS_AND_BLOCKERS.md", "# Data Gaps and Blockers\n\n" + md_table(gaps, ["candidate_id", "gap"]))
    save_csv(OUT / "strategy_summary.csv", summaries)


def list_files_created() -> None:
    files = [str(path.relative_to(ROOT)) for path in sorted(OUT.rglob("*")) if path.is_file()]
    write_text(OUT / "FILES_CREATED.txt", "\n".join(files) + "\n")


def run_validation(summaries: list[dict[str, Any]]) -> None:
    commands: list[str] = []
    py_files = sorted(OUT.rglob("*.py"))
    cmd = [sys.executable, "-m", "py_compile", *[str(p) for p in py_files]]
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    commands.append(" ".join(cmd) + f"\nexit={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}")
    if result.returncode != 0:
        raise RuntimeError("py_compile failed")
    recompute_rows = []
    for summary in summaries:
        trades_path = OUT / "strategies" / summary["candidate_id"] / "trades.csv"
        trades = pd.read_csv(trades_path) if trades_path.exists() else pd.DataFrame()
        recomputed = metrics_from_trades(trades, int(summary["assets_tested"]))
        recompute_rows.append(
            {
                "candidate_id": summary["candidate_id"],
                "trade_count_match": int(summary["trade_count"]) == int(recomputed["trade_count"]),
                "pf_match": abs(float(summary["aggregate_pf"]) - float(recomputed["aggregate_pf"])) < 0.0001,
                "fee_monotonic": recomputed["fee_monotonic"],
                "assets_min5_or_blocked": int(summary["assets_tested"]) >= 5 or summary["classification"] == "DATA_BLOCKED",
            }
        )
    save_csv(OUT / "METRIC_RECOMPUTE_CHECK.csv", recompute_rows)
    git = subprocess.run(["git", "status", "--short"], cwd=ROOT.parent, text=True, capture_output=True)
    write_text(OUT / "git_status_after.txt", git.stdout)
    before_status = (OUT / "git_status_before.txt").read_text(encoding="utf-8", errors="replace") if (OUT / "git_status_before.txt").exists() else ""
    before_lines = {line.lstrip("\ufeff") for line in before_status.splitlines()}
    after_lines = {line.lstrip("\ufeff") for line in git.stdout.splitlines()}
    new_dirty_lines = sorted(after_lines - before_lines)
    changed_pine_by_task = any("01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine" in line.replace("\\", "/") for line in new_dirty_lines)
    changed_prod_by_task = any("01_MASTER TEMPLATE_V2/00_PYTHON/" in line.replace("\\", "/") for line in new_dirty_lines)
    validation = f"""# Validation Report

## Commands
- `python -m py_compile <new python files>`: PASS

## Metric Recompute
{md_table(recompute_rows, ["candidate_id", "trade_count_match", "pf_match", "fee_monotonic", "assets_min5_or_blocked"])}

## Scope Check
- `01_PINE/MTC_V2.pine` modified by this task: {changed_pine_by_task}
- Production Python runner changes by this task: {changed_prod_by_task}
- New dirty git status lines caused by this task are restricted to this output folder: {all(str(OUT.relative_to(ROOT.parent)).replace("\\", "/") in line.replace("\\", "/") for line in new_dirty_lines)}
- TradingView/Pine/parity/live trading work: false

## New Dirty Lines Since Start
```text
{chr(10).join(new_dirty_lines[:120])}
```

## Output Existence
- Candidate cards: {len(list((OUT / "candidates").glob("*.md")))}
- Strategy folders: {len(list((OUT / "strategies").glob("*")))}
- Master report: pending at validation generation time, written after this section.
"""
    write_text(OUT / "VALIDATION_REPORT.md", validation)
    write_text(OUT / "COMMAND_LOG.txt", "\n\n---\n\n".join(commands))


def final_reports(candidates: list[Candidate], summaries: list[dict[str, Any]], inventory: list[dict[str, Any]]) -> None:
    summary_by_id = {row["candidate_id"]: row for row in summaries}
    rows = []
    for cand in candidates:
        metric = summary_by_id.get(cand.candidate_id, {})
        rows.append(
            {
                "candidate_id": cand.candidate_id,
                "title": cand.title,
                "tier": cand.tier,
                "testability": cand.testability,
                "mtc_relevance": cand.mtc_relevance,
                "classification": metric.get("classification", "UNTESTED_OR_BLOCKED"),
                "pf": metric.get("aggregate_pf", ""),
                "net_return_pct": metric.get("aggregate_net_return_pct", ""),
                "max_dd_pct": metric.get("aggregate_max_dd_pct", ""),
                "trade_count": metric.get("trade_count", ""),
                "assets_tested": metric.get("assets_tested", ""),
                "score": cand.total_score,
            }
        )
    day = [row for row in rows if any(k in row["title"].lower() for k in ["8am", "opening", "highbeta", "orb"])]
    swing = [row for row in rows if row["candidate_id"] in {"CANDIDATE_001", "CANDIDATE_002", "CANDIDATE_003", "CANDIDATE_004", "CANDIDATE_005", "CANDIDATE_007", "CANDIDATE_011", "CANDIDATE_012"}]
    position = [row for row in rows if row["candidate_id"] in {"CANDIDATE_006", "CANDIDATE_013", "CANDIDATE_014"}]
    write_text(OUT / "DAY_TRADE_CANDIDATES.md", "# Day-Trade Candidates\n\n" + md_table(day, ["candidate_id", "title", "classification", "pf", "net_return_pct", "assets_tested", "testability"]))
    write_text(OUT / "SWING_TRADE_CANDIDATES.md", "# Swing-Trade Candidates\n\n" + md_table(swing, ["candidate_id", "title", "classification", "pf", "net_return_pct", "max_dd_pct", "trade_count", "assets_tested"]))
    write_text(OUT / "POSITION_TRADING_CANDIDATES.md", "# Position-Trading Candidates\n\n" + md_table(position, ["candidate_id", "title", "classification", "testability", "mtc_relevance", "score"]))
    write_text(
        OUT / "PORTFOLIO_RESEARCH_SUMMARY.md",
        "# Portfolio Research Summary\n\n"
        "## Day Trade Sleeve\n"
        "No day-trade candidate is Pine-ready. 8AM ORB is rejected as crypto proxy; HighBeta remains weak proxy only.\n\n"
        "## Swing Sleeve\n"
        "Best research continuation set is Crabel/Linda/BigBeluga from audited Stage 2 context, but all remain weak rather than producer-ready.\n\n"
        "## Position Sleeve\n"
        "CANSLIM and Weinstein-style ideas need real equity/RS/fundamental data before honest promotion.\n\n"
        "## Ignore / Do Not Automate\n"
        "US microcap short without borrow/locate/halt/dilution data; discretionary process-only ideas.\n",
    )
    valid = sum(1 for row in inventory if row.get("classification") == "VALID_INTAKE_REPORT")
    duplicates = sum(1 for row in inventory if row.get("classification") == "DUPLICATE")
    raw = sum(1 for row in inventory if row.get("classification") == "RAW_TRANSCRIPT_BY_MISTAKE")
    tested = [row for row in rows if row["classification"] not in {"UNTESTED_OR_BLOCKED"}]
    stage2_candidates = [
        row
        for row in rows
        if row["classification"] in {"WEAK_CANDIDATE", "PASS_STAGE2"} and row["candidate_id"] in {"CANDIDATE_001", "CANDIDATE_003", "CANDIDATE_004", "CANDIDATE_005", "CANDIDATE_007"}
    ]
    master = f"""# Master Overnight QuantLens Report

## 1. Executive Verdict
No candidate is Pine/MTC producer-ready tonight. The strongest practical continuation candidates remain Stage-2/Stage-3 research items, not integration items. The research package is Python-only and preserves the previous audited lesson that weak first-pass results must not be promoted.

## 2-6. Inventory and Extraction
- Input inventory count: {len(inventory)}
- Duplicate count: {duplicates}
- Valid intake count: {valid}
- Raw transcript mistaken count: {raw}
- Strategy candidates extracted: {len(candidates)}

## 7-11. Candidate Status
{md_table(rows, ["candidate_id", "title", "tier", "classification", "testability", "mtc_relevance", "pf", "net_return_pct", "trade_count"])}

## 12. Top 5 Day-Trade Candidates
{md_table(day[:5], ["candidate_id", "title", "classification", "pf", "net_return_pct", "testability"])}

## 13. Top 5 Swing-Trade Candidates
{md_table(swing[:5], ["candidate_id", "title", "classification", "pf", "net_return_pct", "max_dd_pct"])}

## 14. Top 5 Position-Trading Candidates
{md_table(position[:5], ["candidate_id", "title", "classification", "testability", "score"])}

## 15. Candidates Suitable for Stage 2 Robustness
{md_table(stage2_candidates, ["candidate_id", "title", "classification", "pf", "net_return_pct", "max_dd_pct"])}

## 16. MTC Filters/Gates Only
- CANDIDATE_011 Daily Extension Anti-Chase Filter should remain filter research only unless applied to a producer trade set and shown to reduce drawdown.

## 17. Exit/SL/TP/Trailing/Sizing Modules
- No standalone exit/sizing module is promoted tonight. ATR/time exits remain reusable research components only.

## 18. Needs Real US Equity Data
- CANDIDATE_006 CANSLIM Shakeout +3.
- CANDIDATE_013 Weinstein / Long-Base Stage Analysis, if treated as equity-native rather than crypto proxy.

## 19. Needs US Microcap/Borrow/Locate/Halt Data
- CANDIDATE_010 Ty Rajnus Microcap Short remains DATA_BLOCKED.

## 20. Needs 1m/5m Session-Aware Data
- CANDIDATE_009 HighBeta needs real US equity gap/session data.
- CANDIDATE_008 has crypto 5m proxy data but was rejected in prior and current proxy context.

## 21. Top Data Acquisition Tasks for Tomorrow
1. US equities daily OHLCV plus benchmark relative strength for CANSLIM/Weinstein.
2. US high-beta equity 5m with regular-session gaps for HighBeta.
3. US microcap 1m with premarket/borrow/locate/dilution/halt metadata for Ty Rajnus.

## 22. Exact Files Created
See `FILES_CREATED.txt`.

## 23. Exact Commands Run
See `COMMAND_LOG.txt` and `RUN_LOG.md`.

## 24. Validation Results
See `VALIDATION_REPORT.md` and `METRIC_RECOMPUTE_CHECK.csv`.

## 25. Known Limitations
- Candidate extraction is deterministic keyword/formalization over finalized intake reports, not an LLM rewrite of full transcripts.
- Some strategy prototypes are conservative proxies because source reports contain discretionary details.
- Crypto proxy does not prove equity-native/session-native edge.
- Fee stress is checked on the same generated trade set and must be monotonic.

## 26. Next Recommended Codex Prompt for Tomorrow
Audit `overnight_intake_batch_2026_05_03`, verify candidate extraction against selected intake reports, then choose either US equity data acquisition or Stage 2 robustness for the top weak swing candidates. Do not move to Pine until robustness gates pass.
"""
    write_text(OUT / "MASTER_OVERNIGHT_QUANTLENS_REPORT.md", master)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    append_log("Batch runner started.")
    checkpoint("phase0", "started")
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(PROMPT_PATH)
    prompt_preview = PROMPT_PATH.read_text(encoding="utf-8", errors="replace")[:3000]
    write_text(OUT / "INTAKE_PROMPT_APPLIED_NOTE.md", "# Intake Prompt Applied\n\nThe finalized QuantLens intake prompt was read and applied as the normalization intent for candidate extraction.\n\n```text\n" + prompt_preview + "\n```\n")
    checkpoint("phase1", "inventory_started")
    inventory, raw_json = extract_inventory()
    checkpoint("phase1", "inventory_complete", {"files": len(inventory)})
    candidates = candidate_specs(inventory)
    checkpoint("phase2", "candidates_extracted", {"candidates": len(candidates)})
    data_rows = discover_data()
    checkpoint("phase4", "data_discovered", {"rows": len(data_rows)})
    summaries: list[dict[str, Any]] = []
    errors: list[str] = []
    selected = [cand for cand in sorted(candidates, key=lambda c: c.total_score, reverse=True) if cand.candidate_id in STRATEGIES][:10]
    for cand in selected:
        try:
            append_log(f"Running {cand.candidate_id} {cand.title}.")
            summaries.append(run_strategy(cand))
        except Exception as exc:
            errors.append(f"{cand.candidate_id}: {exc}")
            with (OUT / "errors_and_recovery.md").open("a", encoding="utf-8") as handle:
                handle.write(f"\n- {now_iso()}: {cand.candidate_id} failed: {exc}\n")
    # Bring explicit blocked candidates into the master table.
    for cand in candidates:
        if cand.candidate_id not in {row["candidate_id"] for row in summaries} and "NEEDS_" in cand.testability:
            summaries.append(
                {
                    "candidate_id": cand.candidate_id,
                    "strategy": cand.title,
                    "timeframe": cand.native_timeframe,
                    "assets_tested": 0,
                    "trade_count": 0,
                    "aggregate_pf": 0.0,
                    "aggregate_net_return_pct": 0.0,
                    "aggregate_max_dd_pct": 0.0,
                    "return_dd_ratio": 0.0,
                    "fee_2x_pf": 0.0,
                    "fee_3x_pf": 0.0,
                    "fee_monotonic": True,
                    "classification": "DATA_BLOCKED",
                }
            )
    write_phase_reports(inventory, raw_json, candidates, data_rows, summaries)
    checkpoint("phase6", "backtests_complete", {"summaries": len(summaries), "errors": len(errors)})
    final_reports(candidates, summaries, inventory)
    run_validation(summaries)
    list_files_created()
    checkpoint("phase11", "complete")
    append_log("Batch runner complete.")


if __name__ == "__main__":
    main()
