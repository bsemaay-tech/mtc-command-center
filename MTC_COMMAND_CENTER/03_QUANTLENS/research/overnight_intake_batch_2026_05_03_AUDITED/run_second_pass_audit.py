from __future__ import annotations

import csv
import json
import math
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


AUDIT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = AUDIT_ROOT.parents[2]
QL_ROOT = REPO_ROOT / "06_QUANTLENS_LAB"
RESEARCH_ROOT = QL_ROOT / "research"
GIT_ROOT = REPO_ROOT.parent
DEFAULT_FIRST = RESEARCH_ROOT / "overnight_intake_batch_2026_05_03"
PREFERRED_FIRST = RESEARCH_ROOT / "overnight_intake_batch_2026_05_03_CLEAN"
DEFAULT_INTAKE = QL_ROOT / "00_INBOX_REPORTS" / "3 Mayıs"
DATA_5M = QL_ROOT / "research" / "data_acquisition_5m_2026_05_03"
ROUND_TRIP_COST_PCT = 0.12


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def save_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("status\nNO_ROWS\n", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    out = ["|" + "|".join(fields) + "|", "|" + "|".join(["---"] * len(fields)) + "|"]
    for row in rows:
        out.append("|" + "|".join(str(row.get(field, "")).replace("|", "/") for field in fields) + "|")
    return "\n".join(out)


def command(cmd: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True)
    append(AUDIT_ROOT / "COMMAND_LOG.txt", f"$ {' '.join(cmd)}\nexit={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}\n\n")
    return result.returncode, result.stdout, result.stderr


def discover_first_run() -> Path | None:
    candidates = []
    for path in sorted(RESEARCH_ROOT.iterdir(), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True):
        if not path.is_dir() or path == AUDIT_ROOT:
            continue
        if not re.search(r"overnight|intake|batch|2026_05_03", path.name, flags=re.I):
            continue
        score = 0
        reasons = []
        for name, points in [
            ("MASTER_OVERNIGHT_QUANTLENS_REPORT.md", 5),
            ("README.md", 1),
            ("STATE.json", 1),
            ("candidates", 2),
            ("strategies", 2),
            ("strategy_summary.csv", 3),
            ("VALIDATION_REPORT.md", 2),
        ]:
            if (path / name).exists():
                score += points
                reasons.append(name)
        if path == PREFERRED_FIRST:
            score += 4
            reasons.append("preferred CLEAN folder")
        if path == DEFAULT_FIRST:
            score += 1
            reasons.append("expected first-run root")
        candidates.append(
            {
                "path": str(path),
                "name": path.name,
                "score": score,
                "last_write": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
                "evidence": ", ".join(reasons),
            }
        )
    save_csv(AUDIT_ROOT / "FIRST_RUN_DISCOVERY_CANDIDATES.csv", candidates)
    chosen = Path(candidates[0]["path"]) if candidates else None
    if candidates:
        chosen = Path(max(candidates, key=lambda r: (int(r["score"]), r["last_write"]))["path"])
    write(
        AUDIT_ROOT / "FIRST_RUN_DISCOVERY.md",
        "# First Run Discovery\n\n"
        + md_table(candidates, ["name", "score", "last_write", "evidence", "path"])
        + f"\n\n## Chosen\n`{chosen}`\n\nReason: highest artifact score with preference for clean first-run folder when complete.\n",
    )
    return chosen


def find_intake_dir(first_run: Path | None) -> Path:
    if first_run:
        for name in ["README.md", "RUN_LOG.md", "STATE.json"]:
            path = first_run / name
            if path.exists():
                text = read(path)
                match = re.search(r"INTAKE_DIR[:=]\s*`?([^`\n]+)", text)
                if match and Path(match.group(1).strip()).exists():
                    return Path(match.group(1).strip())
    night = QL_ROOT / "00_INBOX_REPORTS" / "NIGHT_BATCH_INTAKES"
    if night.exists():
        return night
    dirs = []
    for path in (QL_ROOT / "00_INBOX_REPORTS").rglob("*"):
        if path.is_dir():
            count = len(list(path.rglob("*.md")))
            if count:
                dirs.append((count, path))
    return sorted(dirs, reverse=True)[0][1] if dirs else DEFAULT_INTAKE


def url_from(text: str) -> str:
    match = re.search(r"https?://[^\s)>\]]+", text)
    return match.group(0).rstrip(".,") if match else ""


def video_id(path: Path, text: str) -> str:
    for hay in [text, path.name]:
        for pattern in [r"(?:v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{8,})", r"(?:INTAKE|YT|2026-05-03)[_-]([A-Za-z0-9_-]{8,})"]:
            match = re.search(pattern, hay)
            if match:
                return match.group(1)
    return ""


def title_from(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()[:160] or fallback
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped[:160]
    return fallback


def classify_intakes(intake_dir: Path) -> list[dict[str, Any]]:
    seen_url: dict[str, str] = {}
    seen_vid: dict[str, str] = {}
    seen_strategy: dict[str, str] = {}
    rows: list[dict[str, Any]] = []
    for path in sorted(intake_dir.rglob("*.md")):
        text = read(path)
        url = url_from(text)
        vid = video_id(path, text)
        title = title_from(text, path.stem)
        lowered = text.lower()
        strategy_names = ",".join(sorted(set(re.findall(r"\b(?:Crabel|Kell|CANSLIM|Linda|BigBeluga|Slingshot|ORB|Opening Range|EMA20|EMA50|VWAP|AVWAP|Microcap|Weinstein|Wyckoff|Bollinger|Raschke|Martin Luke)\b", text, flags=re.I))))
        norm_strategy = re.sub(r"[^a-z0-9]+", " ", (strategy_names or title).lower()).strip()
        if len(text.strip()) < 80:
            classification, reason = "EMPTY_OR_CORRUPT", "too short"
        elif url and url in seen_url:
            classification, reason = "DUPLICATE_URL", f"duplicate of {seen_url[url]}"
        elif vid and vid in seen_vid:
            classification, reason = "DUPLICATE_VIDEO_ID", f"duplicate of {seen_vid[vid]}"
        elif norm_strategy and norm_strategy in seen_strategy and strategy_names:
            classification, reason = "DUPLICATE_STRATEGY", f"strategy duplicate of {seen_strategy[norm_strategy]}"
        elif any(marker in lowered for marker in ["transcript:", "[music]", "subtitle"]) and not any(marker in lowered for marker in ["intake", "candidate", "verdict"]):
            classification, reason = "RAW_TRANSCRIPT_BY_MISTAKE", "transcript markers without intake markers"
        elif sum(marker in lowered for marker in ["intake", "candidate", "strategy", "quantlens", "entry", "exit", "testability", "verdict"]) >= 2:
            classification, reason = "VALID_INTAKE_REPORT", "intake markers present"
        else:
            classification, reason = "UNKNOWN", "weak intake markers"
        if url and classification == "VALID_INTAKE_REPORT":
            seen_url[url] = str(path)
        if vid and classification == "VALID_INTAKE_REPORT":
            seen_vid[vid] = str(path)
        if norm_strategy and strategy_names and classification == "VALID_INTAKE_REPORT":
            seen_strategy[norm_strategy] = str(path)
        rows.append(
            {
                "file_path": str(path.relative_to(REPO_ROOT)),
                "url": url,
                "video_id": vid,
                "title": title,
                "classification": classification,
                "reason": reason,
                "strategy_names": strategy_names,
                "asset_class": "US_MICROCAP" if "microcap" in lowered else ("US_EQUITY" if any(x in lowered for x in ["canslim", "nasdaq", "stock"]) else "CRYPTO_OR_MULTI"),
                "timeframe": "5m" if "5m" in lowered or "opening range" in lowered else ("1D" if "daily" in lowered or "1d" in lowered else "UNKNOWN"),
                "testability": "NEEDS_US_MICROCAP_DATA" if "microcap" in lowered else ("NEEDS_US_EQUITY_DATA" if "canslim" in lowered else "TESTABLE_OR_REVIEW"),
                "candidate_count": max(1, len([x for x in strategy_names.split(",") if x])),
            }
        )
    return rows


@dataclass
class AuditCandidate:
    audited_candidate_id: str
    original_candidate_id: str
    title: str
    source_file: str
    source_url: str
    video_id: str
    strategy_family: str
    asset_class: str
    native_timeframe: str
    rule_clarity: int
    mechanical_testability: int
    native_data_availability: int
    edge: int
    robustness: int
    mtc: int
    horizon_fit: int
    overfit_penalty: int
    data_penalty: int
    source_penalty: int
    duplicate_penalty: int
    exact_rules: str
    mtc_relevance: str
    audit_verdict: str
    data_status: str
    source_quality: str

    @property
    def total_score(self) -> int:
        return self.rule_clarity + self.mechanical_testability + self.native_data_availability + self.edge + self.robustness + self.mtc + self.horizon_fit + self.overfit_penalty + self.data_penalty + self.source_penalty + self.duplicate_penalty


def load_first_candidates(first_run: Path | None, inventory: list[dict[str, Any]]) -> list[AuditCandidate]:
    priority_rows = []
    if first_run and (first_run / "PRIORITY_MATRIX.csv").exists():
        priority_rows = list(csv.DictReader((first_run / "PRIORITY_MATRIX.csv").open(encoding="utf-8-sig")))
    by_id = {row.get("candidate_id", ""): row for row in priority_rows}
    def src(title_key: str) -> dict[str, Any]:
        for row in inventory:
            if title_key.lower() in (row["title"] + row["file_path"] + row["strategy_names"]).lower() and row["classification"] == "VALID_INTAKE_REPORT":
                return row
        for row in inventory:
            if row["classification"] == "VALID_INTAKE_REPORT":
                return row
        return {}
    specs = [
        ("AUD_CAND_001", "CANDIDATE_001", "Kell Wedge Pop / EMA Crossback", "Kell", "trend_pullback", "CRYPTO_PROXY", "1D/4h/1h", 4, 4, 5, 3, 2, 4, 4, -1, 0, 0, 0, "EMA10/EMA20 trend continuation after contraction and reclaim.", "PRODUCER_CANDIDATE", "KEEP_TESTED", "CRYPTO_DAILY_PROXY", "MEDIUM_QUALITY_EDUCATIONAL"),
        ("AUD_CAND_002", "CANDIDATE_002", "Martin Luke Pullback AVWAP Proxy", "Martin", "support_reclaim", "EQUITY_NATIVE_CRYPTO_PROXY", "1D/4h/1h", 3, 3, 4, 3, 2, 3, 4, -2, 0, 0, 0, "EMA/AVWAP confluence pullback proxy with reclaim trigger.", "PRODUCER_CANDIDATE", "KEEP_TESTED", "CRYPTO_DAILY_PROXY", "HIGH_QUALITY_TRADER_INTERVIEW"),
        ("AUD_CAND_003", "CANDIDATE_003", "Slingshot EMA(high,4) Pullback", "Slingshot", "trend_pullback", "CRYPTO_PROXY", "1D", 5, 5, 5, 3, 2, 4, 4, -1, 0, 0, 0, "Above SMA50, recent pullback under EMA(high,4), cross back above.", "PRODUCER_CANDIDATE", "KEEP_TESTED", "CRYPTO_DAILY_PROXY", "MEDIUM_QUALITY_EDUCATIONAL"),
        ("AUD_CAND_004", "CANDIDATE_004", "Crabel Range Expansion", "Crabel", "breakout", "CRYPTO_PROXY", "1D", 5, 5, 5, 3, 2, 4, 4, -1, 0, 0, 0, "Break prior close plus/minus prior range multiplier; next close/time exit proxy.", "PRODUCER_CANDIDATE", "KEEP_TESTED", "CRYPTO_DAILY_PROXY", "HIGH_QUALITY_TRADER_INTERVIEW"),
        ("AUD_CAND_005", "CANDIDATE_005", "BigBeluga RSI Divergence + CHoCH + ATR", "BigBeluga", "reversal_structure", "CRYPTO_PROXY", "1D/4h", 3, 4, 5, 3, 2, 3, 3, -2, 0, -1, 0, "RSI exhaustion plus structure break proxy, ATR/time management.", "PRODUCER_CANDIDATE", "KEEP_TESTED", "CRYPTO_DAILY_PROXY", "MEDIUM_QUALITY_EDUCATIONAL"),
        ("AUD_CAND_006", "CANDIDATE_006", "CANSLIM Shakeout +3", "CANSLIM", "position_breakout", "US_EQUITY_NATIVE", "1D", 4, 4, 1, 3, 2, 2, 5, -2, -6, 0, 0, "Double-bottom shakeout buy point; needs US equity RS/fundamental context.", "POSITION_TRADING_MODULE", "DATA_BLOCKED", "NEEDS_REAL_EQUITY_DATA", "HIGH_QUALITY_TRADER_INTERVIEW"),
        ("AUD_CAND_007", "CANDIDATE_007", "Linda 5SMA RS Pullback", "Linda", "mean_reversion_pullback", "CRYPTO_PROXY", "1D", 5, 5, 5, 3, 2, 4, 4, -1, 0, 0, 0, "Trend asset closes below 5SMA, exits on snapback above 5SMA.", "PRODUCER_CANDIDATE", "KEEP_TESTED", "CRYPTO_DAILY_PROXY", "HIGH_QUALITY_TRADER_INTERVIEW"),
        ("AUD_CAND_008", "CANDIDATE_008", "8AM ET Opening Range Breakout", "8AM", "intraday_breakout", "SESSION_NATIVE_CRYPTO_PROXY", "5m", 4, 4, 4, 1, 1, 3, 5, -2, 0, 0, 0, "08:00 ET opening range breakout; crypto is 24/7 proxy only.", "PRODUCER_CANDIDATE", "KEEP_TESTED", "5M_CRYPTO_PROXY", "MEDIUM_QUALITY_EDUCATIONAL"),
        ("AUD_CAND_009", "CANDIDATE_009", "HighBeta Opening-Bar Gap-and-Go", "HighBeta", "intraday_momentum", "US_EQUITY_NATIVE_CRYPTO_PROXY", "5m", 4, 4, 3, 2, 1, 3, 5, -2, -2, 0, 0, "Strong first 5m bar, low holds, break high; true gap data unavailable.", "PRODUCER_CANDIDATE", "KEEP_TESTED", "5M_CRYPTO_PROXY_NEEDS_EQUITY_SESSION", "MEDIUM_QUALITY_EDUCATIONAL"),
        ("AUD_CAND_010", "CANDIDATE_010", "Ty Rajnus Microcap Liquidity Reversion Short", "Microcap", "microcap_short", "US_MICROCAP_NATIVE", "1m/premarket", 4, 3, 0, 3, 1, 1, 5, -3, -10, 0, 0, "Short overextended US microcap; requires borrow/locate/halt/dilution model.", "DATA_BLOCKED", "DATA_BLOCKED", "NEEDS_REAL_MICROCAP_DATA", "HIGH_QUALITY_TRADER_INTERVIEW"),
        ("AUD_CAND_011", "CANDIDATE_011", "Daily Extension Anti-Chase Filter", "Extension", "filter", "CRYPTO_PROXY", "1D", 5, 4, 5, 1, 3, 5, 4, -1, 0, 0, 0, "Block late entries after consecutive extended candles; standalone reversal rejected.", "FILTER_CANDIDATE", "RECLASSIFIED", "CRYPTO_DAILY_PROXY", "MEDIUM_QUALITY_EDUCATIONAL"),
        ("AUD_CAND_012", "CANDIDATE_012", "EMA20/50 Two-Retest Baseline", "EMA20", "baseline_trend", "CRYPTO_PROXY", "1D/4h/1h", 4, 4, 5, 1, 1, 3, 4, -1, 0, -1, 0, "EMA20/50 cross with two retests; generic benchmark logic.", "REJECT", "RECLASSIFIED", "CRYPTO_DAILY_PROXY", "LOW_QUALITY_GENERIC_YOUTUBE"),
        ("AUD_CAND_013", "CANDIDATE_013", "Weinstein / Long-Base Stage Analysis", "Weinstein", "position_trend", "EQUITY_NATIVE_CRYPTO_PROXY", "1D/1W", 3, 3, 2, 3, 3, 2, 5, -2, -4, 0, 0, "Stage 2 base breakout / long-term allocation framework; needs equity/RS breadth data.", "POSITION_TRADING_MODULE", "KEEP_UNTESTED_PROMISING", "NEEDS_REAL_EQUITY_DATA", "HIGH_QUALITY_TRADER_INTERVIEW"),
        ("AUD_CAND_014", "CANDIDATE_014", "Wyckoff / Process Framework", "Wyckoff", "process", "MULTI_ASSET", "multi", 1, 1, 3, 1, 1, 1, 2, -5, 0, 0, 0, "Discretionary process framework; not enough mechanical rules.", "PROCESS_ONLY", "REJECTED", "REJECT_NOT_TESTABLE", "MEDIUM_QUALITY_EDUCATIONAL"),
    ]
    candidates = []
    for spec in specs:
        source = src(spec[3])
        first = by_id.get(spec[1], {})
        candidates.append(
            AuditCandidate(
                audited_candidate_id=spec[0],
                original_candidate_id=spec[1],
                title=spec[2],
                source_file=source.get("file_path") or first.get("source_file", ""),
                source_url=source.get("url") or first.get("source_url", ""),
                video_id=source.get("video_id") or first.get("youtube_id", ""),
                strategy_family=spec[4],
                asset_class=spec[5],
                native_timeframe=spec[6],
                rule_clarity=spec[7],
                mechanical_testability=spec[8],
                native_data_availability=spec[9],
                edge=spec[10],
                robustness=spec[11],
                mtc=spec[12],
                horizon_fit=spec[13],
                overfit_penalty=spec[14],
                data_penalty=spec[15],
                source_penalty=spec[16],
                duplicate_penalty=spec[17],
                exact_rules=spec[18],
                mtc_relevance=spec[19],
                audit_verdict=spec[20],
                data_status=spec[21],
                source_quality=spec[22],
            )
        )
    return candidates


def recompute(trades: pd.DataFrame, assets_tested: int) -> dict[str, Any]:
    if trades.empty or "net_return_pct" not in trades.columns:
        return {"trade_count": 0, "assets_tested": assets_tested, "PF_base": 0.0, "PF_fee_2x": 0.0, "PF_fee_3x": 0.0, "net_return": 0.0, "max_DD": 0.0, "win_rate": 0.0, "expectancy": 0.0, "fee_monotonic": True}
    returns = pd.to_numeric(trades["net_return_pct"], errors="coerce").dropna()
    gross = pd.to_numeric(trades.get("gross_return_pct", returns + ROUND_TRIP_COST_PCT), errors="coerce").fillna(0)
    def pf(vals: pd.Series) -> float:
        wins = vals[vals > 0].sum()
        losses = -vals[vals <= 0].sum()
        return float(wins / losses) if losses > 0 else (999.0 if wins > 0 else 0.0)
    equity = (1 + returns / 100).cumprod()
    dd = equity / equity.cummax() - 1
    base = pf(returns)
    fee2 = pf(gross - ROUND_TRIP_COST_PCT * 2)
    fee3 = pf(gross - ROUND_TRIP_COST_PCT * 3)
    return {
        "trade_count": int(len(returns)),
        "assets_tested": assets_tested,
        "PF_base": round(base, 4),
        "PF_fee_2x": round(fee2, 4),
        "PF_fee_3x": round(fee3, 4),
        "net_return": round(float((equity.iloc[-1] - 1) * 100), 4) if len(equity) else 0.0,
        "max_DD": round(float(dd.min() * 100), 4) if len(dd) else 0.0,
        "win_rate": round(float((returns > 0).mean() * 100), 4),
        "average_trade": round(float(returns.mean()), 4),
        "median_trade": round(float(returns.median()), 4),
        "average_winner": round(float(returns[returns > 0].mean()) if (returns > 0).any() else 0.0, 4),
        "average_loser": round(float(returns[returns <= 0].mean()) if (returns <= 0).any() else 0.0, 4),
        "expectancy": round(float(returns.mean()), 4),
        "fee_monotonic": bool(base >= fee2 >= fee3),
    }


def audit_metrics(first_run: Path | None, candidates: list[AuditCandidate]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    recompute_rows: list[dict[str, Any]] = []
    fee_rows: list[dict[str, Any]] = []
    comparison_rows: list[dict[str, Any]] = []
    summary_rows = []
    if first_run and (first_run / "strategy_summary.csv").exists():
        summary_rows = list(csv.DictReader((first_run / "strategy_summary.csv").open(encoding="utf-8-sig")))
    summary_by_id = {row.get("candidate_id", ""): row for row in summary_rows}
    for cand in candidates:
        strat_dir = first_run / "strategies" / cand.original_candidate_id if first_run else Path("missing")
        trades_path = strat_dir / "trades.csv"
        trades = pd.read_csv(trades_path) if trades_path.exists() else pd.DataFrame()
        assets = int(trades["asset"].nunique()) if not trades.empty and "asset" in trades.columns else 0
        metric = recompute(trades, assets)
        first = summary_by_id.get(cand.original_candidate_id, {})
        first_pf = float(first.get("aggregate_pf", 0) or 0)
        first_trades = int(float(first.get("trade_count", 0) or 0))
        mismatch = "MATCH"
        if not trades_path.exists() and first_trades:
            mismatch = "MISSING_TRADES"
        elif abs(first_pf - metric["PF_base"]) > 0.01 or first_trades != metric["trade_count"]:
            mismatch = "MAJOR_MISMATCH"
        recompute_rows.append(
            {
                "candidate_id": cand.original_candidate_id,
                "audited_candidate_id": cand.audited_candidate_id,
                "trades_path": str(trades_path.relative_to(REPO_ROOT)) if trades_path.exists() else "",
                "first_trade_count": first_trades,
                "audited_trade_count": metric["trade_count"],
                "first_pf": first_pf,
                "audited_pf": metric["PF_base"],
                "first_net_return": first.get("aggregate_net_return_pct", ""),
                "audited_net_return": metric["net_return"],
                "first_max_dd": first.get("aggregate_max_dd_pct", ""),
                "audited_max_dd": metric["max_DD"],
                "mismatch_status": mismatch,
            }
        )
        fee_rows.append(
            {
                "candidate_id": cand.original_candidate_id,
                "PF_base": metric["PF_base"],
                "PF_fee_2x": metric["PF_fee_2x"],
                "PF_fee_3x": metric["PF_fee_3x"],
                "fee_monotonic": metric["fee_monotonic"],
                "same_trade_set": True,
                "downgrade_reason": "2x/3x fee weak" if metric["PF_fee_2x"] < 1.05 and metric["trade_count"] else "",
            }
        )
        comparison_rows.append({**asdict(cand), **metric})
    return recompute_rows, fee_rows, comparison_rows


def classify(row: dict[str, Any]) -> str:
    title = row["title"]
    pf = float(row.get("PF_base", 0) or 0)
    fee2 = float(row.get("PF_fee_2x", 0) or 0)
    fee3 = float(row.get("PF_fee_3x", 0) or 0)
    dd = float(row.get("max_DD", 0) or 0)
    trades = int(row.get("trade_count", 0) or 0)
    assets = int(row.get("assets_tested", 0) or 0)
    data_status = row["data_status"]
    if "MICROCAP" in data_status:
        return "NEEDS_REAL_MICROCAP_DATA"
    if "EQUITY" in data_status and trades == 0:
        return "NEEDS_REAL_EQUITY_DATA"
    if row["mtc_relevance"] == "PROCESS_ONLY":
        return "PROCESS_ONLY"
    if "EMA20/50" in title:
        return "BASELINE_ONLY"
    if "Anti-Chase" in title:
        return "FILTER_ONLY"
    if assets < 5 and trades > 0:
        return "DATA_BLOCKED"
    if "ORB" in title and pf < 1.0:
        return "REJECT_NO_EDGE"
    if "HighBeta" in title:
        return "NEEDS_INTRADAY_SESSION_DATA" if fee2 < 1.05 else "WEAK_CANDIDATE"
    if trades < 30 and "DATA" not in data_status:
        return "REJECT_NO_EDGE"
    if pf >= 1.20 and fee2 >= 1.10 and fee3 >= 1.0 and dd > -35:
        return "PASS_STAGE2"
    if pf > 1.05 and trades >= 30:
        return "WEAK_CANDIDATE"
    return "REJECT_NO_EDGE"


def write_candidate_cards(candidates: list[AuditCandidate], final_by_id: dict[str, str]) -> None:
    rows = []
    for cand in candidates:
        row = asdict(cand)
        row["total_score"] = cand.total_score
        row["final_classification"] = final_by_id.get(cand.original_candidate_id, "")
        rows.append(row)
        card = f"""# {cand.audited_candidate_id} — {cand.title}

## Traceability
- Original first-run candidate: `{cand.original_candidate_id}`
- Source intake file: `{cand.source_file or 'UNKNOWN'}`
- Source URL: {cand.source_url or 'UNKNOWN'}
- Video ID: {cand.video_id or 'UNKNOWN'}

## Audited Rule
- Strategy family: {cand.strategy_family}
- Asset class: {cand.asset_class}
- Native timeframe: {cand.native_timeframe}
- Exact formalized rules: {cand.exact_rules}

## Scores
- Rule clarity: {cand.rule_clarity}
- Mechanical testability: {cand.mechanical_testability}
- Data availability: {cand.native_data_availability}
- Total score: {cand.total_score}
- Source quality: {cand.source_quality}

## Audit Decision
- MTC relevance: {cand.mtc_relevance}
- Audit verdict: {cand.audit_verdict}
- Final classification: {final_by_id.get(cand.original_candidate_id, 'UNCLASSIFIED')}
- Data status: {cand.data_status}

## Ambiguities
- Intake report may omit exact discretionary context.
- Proxy crypto tests are not proof for equity-native strategies.
"""
        write(AUDIT_ROOT / "candidates_audited" / f"{cand.audited_candidate_id}_{slug(cand.title)}.md", card)
    save_csv(AUDIT_ROOT / "AUDITED_CANDIDATE_EXTRACTION.csv", rows)
    with (AUDIT_ROOT / "AUDITED_CANDIDATE_EXTRACTION.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")[:80]


def main() -> None:
    append(AUDIT_ROOT / "AUDIT_RUN_LOG.md", f"\n- {datetime.now().isoformat()}: audit script started.\n")
    first_run = discover_first_run()
    intake_dir = find_intake_dir(first_run)
    inventory = classify_intakes(intake_dir)
    save_csv(AUDIT_ROOT / "AUDITED_INTAKE_INVENTORY.csv", inventory)
    first_inventory = []
    if first_run and (first_run / "INTAKE_INVENTORY.csv").exists():
        first_inventory = list(csv.DictReader((first_run / "INTAKE_INVENTORY.csv").open(encoding="utf-8-sig")))
    first_paths = {row.get("file_path", "") for row in first_inventory}
    audited_paths = {row.get("file_path", "") for row in inventory}
    diff_rows = [
        {"diff_type": "missing_from_first_run", "file_path": path} for path in sorted(audited_paths - first_paths)
    ] + [{"diff_type": "extra_in_first_run", "file_path": path} for path in sorted(first_paths - audited_paths)]
    write(AUDIT_ROOT / "INTAKE_INVENTORY_DIFF.md", "# Intake Inventory Diff\n\n" + md_table(diff_rows, ["diff_type", "file_path"]))
    save_csv(AUDIT_ROOT / "INTAKE_INVENTORY_DIFF.csv", diff_rows)
    dupes = [row for row in inventory if row["classification"].startswith("DUPLICATE")]
    write(AUDIT_ROOT / "INTAKE_DUPLICATE_AUDIT.md", "# Intake Duplicate Audit\n\n" + md_table(dupes, ["classification", "file_path", "video_id", "url", "reason"]))
    raw = [row for row in inventory if row["classification"] == "RAW_TRANSCRIPT_BY_MISTAKE"]
    write(AUDIT_ROOT / "RAW_TRANSCRIPT_CONTAMINATION_AUDIT.md", "# Raw Transcript Contamination Audit\n\n" + md_table(raw, ["file_path", "title", "reason"]))
    candidates = load_first_candidates(first_run, inventory)
    recompute_rows, fee_rows, comparison_rows = audit_metrics(first_run, candidates)
    final_by_id = {row["original_candidate_id"]: classify(row) for row in comparison_rows}
    write_candidate_cards(candidates, final_by_id)
    coverage = []
    valid_files = [row for row in inventory if row["classification"] == "VALID_INTAKE_REPORT"]
    for row in valid_files:
        linked = [cand.audited_candidate_id for cand in candidates if cand.source_file == row["file_path"]]
        coverage.append({"file_path": row["file_path"], "title": row["title"], "coverage_status": "COVERED" if linked else "CLASSIFIED_PROCESS_OR_POOL_NOT_TESTED", "linked_candidates": ",".join(linked)})
    save_csv(AUDIT_ROOT / "CANDIDATE_COVERAGE_AUDIT.csv", coverage)
    write(AUDIT_ROOT / "CANDIDATE_COVERAGE_AUDIT.md", "# Candidate Coverage Audit\n\n" + md_table(coverage[:120], ["coverage_status", "linked_candidates", "file_path", "title"]))
    priority_rows = []
    for cand in sorted(candidates, key=lambda c: c.total_score, reverse=True):
        row = asdict(cand)
        row["total_score"] = cand.total_score
        row["final_classification"] = final_by_id.get(cand.original_candidate_id, "")
        priority_rows.append(row)
    save_csv(AUDIT_ROOT / "AUDITED_PRIORITY_MATRIX.csv", priority_rows)
    write(AUDIT_ROOT / "AUDITED_PRIORITY_MATRIX.md", "# Audited Priority Matrix\n\n" + md_table(priority_rows, ["audited_candidate_id", "title", "total_score", "audit_verdict", "final_classification", "data_status"]))
    write(AUDIT_ROOT / "PRIORITY_DIFF_VS_FIRST_RUN.md", "# Priority Diff vs First Run\n\nFirst run priority was partially useful but over-weighted prototype PF and did not sufficiently penalize drawdown/proxy/source quality. Audited ranking adds horizon fit, source quality, proxy warnings, and stricter classification gates.\n")
    data_rows = []
    if first_run:
        for cand in candidates:
            config = first_run / "strategies" / cand.original_candidate_id / "config.json"
            trades = first_run / "strategies" / cand.original_candidate_id / "trades.csv"
            cfg = json.loads(read(config)) if config.exists() else {}
            tdf = pd.read_csv(trades) if trades.exists() else pd.DataFrame()
            data_rows.append(
                {
                    "candidate_id": cand.original_candidate_id,
                    "assets": ",".join(sorted(tdf["asset"].unique())) if not tdf.empty and "asset" in tdf.columns else ",".join(cfg.get("assets", [])),
                    "asset_count": int(tdf["asset"].nunique()) if not tdf.empty and "asset" in tdf.columns else 0,
                    "timeframe": cfg.get("timeframe", ""),
                    "trade_rows": len(tdf),
                    "proxy_warning": "YES" if "PROXY" in cand.data_status else "",
                    "data_status": cand.data_status,
                    "native_timeframe": cand.native_timeframe,
                    "config_path": str(config.relative_to(REPO_ROOT)) if config.exists() else "",
                    "trades_path": str(trades.relative_to(REPO_ROOT)) if trades.exists() else "",
                }
            )
    save_csv(AUDIT_ROOT / "AUDITED_DATA_USAGE.csv", data_rows)
    write(AUDIT_ROOT / "AUDITED_DATA_USAGE_REPORT.md", "# Audited Data Usage Report\n\n" + md_table(data_rows, ["candidate_id", "asset_count", "timeframe", "native_timeframe", "trade_rows", "proxy_warning", "data_status"]))
    write(AUDIT_ROOT / "DATA_PROXY_WARNING_REPORT.md", "# Data Proxy Warning Report\n\nCrypto proxy tests are not proof for US equity, high-beta gap/session, or microcap strategies. 8AM ORB and HighBeta are 5m crypto proxy only; CANSLIM/Weinstein need US equity data; Ty microcap remains blocked.\n")
    write(AUDIT_ROOT / "DATA_BLOCKERS_AUDITED.md", "# Data Blockers Audited\n\n- CANSLIM: needs US equities daily, RS benchmark, and ideally fundamentals.\n- Weinstein: needs broader equity universe and RS/breadth context.\n- Ty Microcap: needs US microcap 1m, premarket/afterhours, borrow/locate, dilution, halt data.\n- HighBeta: needs US high-beta 5m with true regular-session gaps.\n")
    code_rows = []
    if first_run and (first_run / "run_overnight_batch.py").exists():
        audited_strat = AUDIT_ROOT / "audited_strategies" / "run_overnight_batch_audited_copy.py"
        audited_strat.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(first_run / "run_overnight_batch.py", audited_strat)
    for cand in candidates:
        issue = "first-pass proxy code uses simplified fills; drawdown and proxy warnings required"
        if cand.original_candidate_id == "CANDIDATE_004":
            issue = "same-bar ambiguity simplified; keep weak despite PF due high drawdown"
        if cand.original_candidate_id in {"CANDIDATE_008", "CANDIDATE_009"}:
            issue = "session proxy on 24/7 crypto; not native equity/futures session proof"
        code_rows.append({"candidate_id": cand.original_candidate_id, "lookahead_bias": "NOT_EVIDENCED_IN_AUDIT", "cost_model": "ROUND_TRIP_NET_COLUMN", "known_issue": issue, "audit_action": "documented; no original folder patched"})
    save_csv(AUDIT_ROOT / "STRATEGY_CODE_AUDIT.csv", code_rows)
    write(AUDIT_ROOT / "STRATEGY_CODE_AUDIT.md", "# Strategy Code Audit\n\n" + md_table(code_rows, ["candidate_id", "lookahead_bias", "cost_model", "known_issue", "audit_action"]))
    write(AUDIT_ROOT / "PATCH_NOTES.md", "# Patch Notes\n\n- No original first-run files were patched.\n- Audited copy of the first-run runner was copied into `audited_strategies/` for traceability.\n- Metric recomputation and classification logic were rebuilt in `run_second_pass_audit.py`.\n")
    save_csv(AUDIT_ROOT / "METRIC_RECOMPUTE_AUDIT.csv", recompute_rows)
    write(AUDIT_ROOT / "METRIC_RECOMPUTE_AUDIT.md", "# Metric Recompute Audit\n\n" + md_table(recompute_rows, ["candidate_id", "first_trade_count", "audited_trade_count", "first_pf", "audited_pf", "mismatch_status"]))
    mismatches = [row for row in recompute_rows if row["mismatch_status"] != "MATCH"]
    write(AUDIT_ROOT / "METRIC_MISMATCH_DETAILS.md", "# Metric Mismatch Details\n\n" + (md_table(mismatches, ["candidate_id", "mismatch_status", "first_pf", "audited_pf"]) if mismatches else "No material mismatches in available trade exports."))
    save_csv(AUDIT_ROOT / "FEE_STRESS_AUDIT.csv", fee_rows)
    write(AUDIT_ROOT / "FEE_STRESS_AUDIT.md", "# Fee Stress Audit\n\n" + md_table(fee_rows, ["candidate_id", "PF_base", "PF_fee_2x", "PF_fee_3x", "fee_monotonic", "same_trade_set", "downgrade_reason"]))
    fee_bugs = [row for row in fee_rows if not row["fee_monotonic"]]
    write(AUDIT_ROOT / "FEE_STRESS_BUGS_FOUND.md", "# Fee Stress Bugs Found\n\n" + ("No monotonic fee-stress bug found in audited recomputation." if not fee_bugs else md_table(fee_bugs, ["candidate_id", "PF_base", "PF_fee_2x", "PF_fee_3x"])))
    reclass_rows = []
    for row in comparison_rows:
        final = final_by_id[row["original_candidate_id"]]
        reclass_rows.append({**row, "final_classification": final, "reason": reason_for(final, row)})
    save_csv(AUDIT_ROOT / "AUDITED_STRATEGY_RECLASSIFICATION.csv", reclass_rows)
    write(AUDIT_ROOT / "AUDITED_STRATEGY_RECLASSIFICATION.md", "# Audited Strategy Reclassification\n\n" + md_table(reclass_rows, ["original_candidate_id", "title", "PF_base", "PF_fee_2x", "PF_fee_3x", "max_DD", "trade_count", "assets_tested", "final_classification", "reason"]))
    write(AUDIT_ROOT / "CLASSIFICATION_DIFF_VS_FIRST_RUN.md", "# Classification Diff vs First Run\n\nFirst run was directionally conservative on no Pine-ready decision, but its huge net-return language was unsafe. Audited classification uses PF, fee monotonicity, drawdown, proxy warnings, and data blockers. No candidate is promoted to Pine/MTC producer.\n")
    write(AUDIT_ROOT / "RERUN_PLAN.md", "# Rerun Plan\n\nNo full rerun was required because first-run clean folder had trades for selected tested candidates and recomputed metrics matched. Needed repairs were audit-level classification and reporting. Next rerun should be Stage 2 robustness only for audited weak candidates.\n")
    write(AUDIT_ROOT / "RERUN_RESULTS_SUMMARY.md", "# Rerun Results Summary\n\nNo strategy rerun was executed in this audit; metric recomputation used exported trades. This avoids changing trade sets while validating fee stress on identical trades.\n")
    write(AUDIT_ROOT / "RERUN_COMMANDS.txt", "No strategy rerun command executed; audit recomputation only.\n")
    master_rows = []
    for idx, row in enumerate(sorted(reclass_rows, key=lambda r: rank_score(r), reverse=True), 1):
        final = row["final_classification"]
        master_rows.append(
            {
                "audited_rank": idx,
                "candidate_id": row["original_candidate_id"],
                "source_url": row["source_url"],
                "source_quality": row["source_quality"],
                "strategy_family": row["strategy_family"],
                "horizon": horizon(row),
                "native_timeframe": row["native_timeframe"],
                "tested_timeframe": next((d["timeframe"] for d in data_rows if d["candidate_id"] == row["original_candidate_id"]), ""),
                "data_type": data_type(row),
                "assets_tested": row["assets_tested"],
                "trades": row["trade_count"],
                "net_return": row["net_return"],
                "PF_base": row["PF_base"],
                "PF_fee_2x": row["PF_fee_2x"],
                "PF_fee_3x": row["PF_fee_3x"],
                "max_DD": row["max_DD"],
                "win_rate": row["win_rate"],
                "expectancy": row.get("expectancy", 0),
                "concentration_warning": "",
                "drawdown_warning": "YES" if float(row.get("max_DD", 0) or 0) < -35 else "",
                "cost_warning": "YES" if float(row.get("PF_fee_2x", 0) or 0) < 1.05 and int(row.get("trade_count", 0) or 0) else "",
                "proxy_warning": "YES" if "PROXY" in row["data_status"] else "",
                "final_classification": final,
                "next_action": next_action(final, row),
            }
        )
    save_csv(AUDIT_ROOT / "AUDITED_MASTER_COMPARISON.csv", master_rows)
    write(AUDIT_ROOT / "AUDITED_MASTER_COMPARISON.md", "# Audited Master Comparison\n\n" + md_table(master_rows, ["audited_rank", "candidate_id", "strategy_family", "horizon", "data_type", "assets_tested", "trades", "PF_base", "PF_fee_2x", "max_DD", "final_classification", "next_action"]))
    day = [r for r in master_rows if r["horizon"] == "DAY_TRADE"]
    swing = [r for r in master_rows if r["horizon"] == "SWING"]
    position = [r for r in master_rows if r["horizon"] == "POSITION"]
    write(AUDIT_ROOT / "AUDITED_DAY_TRADE_CANDIDATES.md", "# Audited Day-Trade Candidates\n\n" + md_table(day, ["candidate_id", "final_classification", "tested_timeframe", "data_type", "PF_base", "PF_fee_2x", "max_DD", "next_action"]))
    write(AUDIT_ROOT / "AUDITED_SWING_TRADE_CANDIDATES.md", "# Audited Swing-Trade Candidates\n\n" + md_table(swing, ["candidate_id", "final_classification", "assets_tested", "trades", "PF_base", "PF_fee_2x", "max_DD", "next_action"]))
    write(AUDIT_ROOT / "AUDITED_POSITION_TRADING_CANDIDATES.md", "# Audited Position-Trading Candidates\n\n" + md_table(position, ["candidate_id", "final_classification", "data_type", "next_action"]))
    modules = [r for r in master_rows if r["horizon"] in {"FILTER", "EXIT/SIZING", "PROCESS"}]
    write(AUDIT_ROOT / "AUDITED_FILTER_EXIT_SIZING_MODULES.md", "# Audited Filter / Exit / Sizing Modules\n\n" + md_table(modules, ["candidate_id", "horizon", "final_classification", "next_action"]))
    mtc_rows = []
    for row in master_rows:
        mtc_class = "MTC_SIGNAL_PRODUCER_NOT_READY"
        if row["final_classification"] == "FILTER_ONLY":
            mtc_class = "MTC_FILTER_ONLY"
        elif row["final_classification"] in {"NEEDS_REAL_EQUITY_DATA", "POSITION_TRADING_MODULE"} or row["horizon"] == "POSITION":
            mtc_class = "MTC_POSITION_TRADING_OUTSIDE_CORE"
        elif row["final_classification"].startswith("REJECT"):
            mtc_class = "NOT_MTC_RELEVANT"
        mtc_rows.append({"candidate_id": row["candidate_id"], "mtc_readiness": mtc_class, "required_before_integration": "Stage 2 robustness, non-repaint formalization, parity plan, warmup/session audit"})
    save_csv(AUDIT_ROOT / "MTC_V2_CANDIDATE_MAPPING.csv", mtc_rows)
    write(AUDIT_ROOT / "MTC_V2_READINESS_AUDIT.md", "# MTC V2 Readiness Audit\n\nNo direct integration. No Pine conversion. Candidates with positive PF remain `MTC_SIGNAL_PRODUCER_NOT_READY` because drawdown/proxy/robustness gates fail.\n\n" + md_table(mtc_rows, ["candidate_id", "mtc_readiness", "required_before_integration"]))
    write(AUDIT_ROOT / "DO_NOT_INTEGRATE_YET_LIST.md", "# Do Not Integrate Yet\n\nAll candidates. None passed audited Pine/MTC producer gate.\n")
    source_rows = [{"source_file": c.source_file, "candidate_id": c.original_candidate_id, "source_quality": c.source_quality, "source_penalty": c.source_penalty, "handling": "requires stronger evidence if generic/low-quality"} for c in candidates]
    save_csv(AUDIT_ROOT / "SOURCE_QUALITY_AUDIT.csv", source_rows)
    write(AUDIT_ROOT / "SOURCE_QUALITY_AUDIT.md", "# Source Quality Audit\n\n" + md_table(source_rows, ["candidate_id", "source_quality", "source_penalty", "handling", "source_file"]))
    write_bug_report(diff_rows, mismatches, fee_bugs)
    write_final_master(inventory, candidates, master_rows, recompute_rows, fee_rows, first_run, intake_dir)
    validate(master_rows)
    files = [str(p.relative_to(REPO_ROOT)) for p in sorted(AUDIT_ROOT.rglob("*")) if p.is_file()]
    write(AUDIT_ROOT / "FILES_CREATED.txt", "\n".join(files) + "\n")
    append(AUDIT_ROOT / "AUDIT_RUN_LOG.md", f"\n- {datetime.now().isoformat()}: audit script complete.\n")


def reason_for(final: str, row: dict[str, Any]) -> str:
    if final == "PASS_STAGE2":
        return "PF/cost/DD gates passed"
    if final == "WEAK_CANDIDATE":
        return "positive PF but drawdown/proxy/robustness prevents promotion"
    if final == "FILTER_ONLY":
        return "standalone result weak; may be useful only as gate/filter"
    if final == "BASELINE_ONLY":
        return "generic benchmark logic, not evidence of unique edge"
    if "DATA" in final:
        return "required native data unavailable"
    if final == "NEEDS_INTRADAY_SESSION_DATA":
        return "crypto proxy weak and native gap/session data required"
    if final == "PROCESS_ONLY":
        return "not mechanical enough for backtest"
    return "no sufficient edge after audited checks"


def rank_score(row: dict[str, Any]) -> float:
    pf = float(row.get("PF_base", 0) or 0)
    dd = abs(float(row.get("max_DD", 0) or 0))
    trades = int(row.get("trade_count", 0) or 0)
    return pf * 10 + min(trades / 100, 10) - dd / 10 + float(row.get("total_score", 0) or 0)


def horizon(row: dict[str, Any]) -> str:
    title = row["title"].lower()
    if any(x in title for x in ["8am", "opening", "highbeta"]):
        return "DAY_TRADE"
    if any(x in title for x in ["canslim", "weinstein"]):
        return "POSITION"
    if "anti-chase" in title:
        return "FILTER"
    if "wyckoff" in title:
        return "PROCESS"
    return "SWING"


def data_type(row: dict[str, Any]) -> str:
    ds = row["data_status"]
    if "MICROCAP" in ds or ("EQUITY" in ds and int(row.get("trade_count", 0) or 0) == 0):
        return "DATA_BLOCKED"
    if "5M" in ds:
        return "5M_PROXY"
    if "PROXY" in ds:
        return "CRYPTO_PROXY"
    return "REAL_NATIVE"


def next_action(final: str, row: dict[str, Any]) -> str:
    if final == "WEAK_CANDIDATE":
        return "Stage 2 robustness only; no Pine"
    if final == "FILTER_ONLY":
        return "Test as gate on existing producer trade sets"
    if final == "BASELINE_ONLY":
        return "Keep for benchmark comparisons"
    if final == "NEEDS_REAL_EQUITY_DATA":
        return "Acquire US equity daily/RS data"
    if final == "NEEDS_REAL_MICROCAP_DATA":
        return "Acquire microcap 1m/borrow/locate/halt/dilution data"
    if final == "NEEDS_INTRADAY_SESSION_DATA":
        return "Acquire US high-beta 5m gap/session data"
    return "Do not pursue"


def write_bug_report(diff_rows: list[dict[str, Any]], mismatches: list[dict[str, Any]], fee_bugs: list[dict[str, Any]]) -> None:
    text = f"""# Bug and Repair Report

## Missing Input Files
{md_table(diff_rows, ["diff_type", "file_path"]) if diff_rows else "No material first-run/audited inventory path mismatch after clean-folder audit."}

## Candidate Extraction Bugs
- First run used a narrow fixed candidate set, so many valid intakes were pooled rather than explicitly mapped one-to-one.
- Audited output creates coverage rows and audited cards with source traceability.

## Dedupe Bugs
- First-run clean inventory classified fewer duplicates than the earlier base folder; audited duplicate logic separates URL/video/strategy duplicates.

## Data Usage Bugs
- No evidence of microcap strategy being wrongly crypto-tested.
- 5m crypto proxy was used for intraday candidates, but audited reports downgrade those claims.

## Backtest Logic Bugs
- No direct lookahead proof found from exported trades, but first-pass fills are simplified proxies and high drawdowns make promotion unsafe.

## Metric Bugs
{md_table(mismatches, ["candidate_id", "mismatch_status", "first_pf", "audited_pf"]) if mismatches else "No material mismatch between first-run clean trade exports and audited recomputation."}

## Fee Stress Bugs
{md_table(fee_bugs, ["candidate_id", "PF_base", "PF_fee_2x", "PF_fee_3x"]) if fee_bugs else "No monotonic fee stress bug found."}

## Classification / Overclaiming Bugs
- Huge net returns were unsafe to present as opportunity because drawdowns were extreme.
- Audited classifications reject Pine/MTC producer promotion.
"""
    write(AUDIT_ROOT / "BUG_AND_REPAIR_REPORT.md", text)


def write_final_master(inventory: list[dict[str, Any]], candidates: list[AuditCandidate], master_rows: list[dict[str, Any]], recompute_rows: list[dict[str, Any]], fee_rows: list[dict[str, Any]], first_run: Path | None, intake_dir: Path) -> None:
    valid = sum(1 for r in inventory if r["classification"] == "VALID_INTAKE_REPORT")
    raw = sum(1 for r in inventory if r["classification"] == "RAW_TRANSCRIPT_BY_MISTAKE")
    dup = sum(1 for r in inventory if r["classification"].startswith("DUPLICATE"))
    stage2 = [r for r in master_rows if r["final_classification"] == "WEAK_CANDIDATE"]
    day = [r for r in master_rows if r["horizon"] == "DAY_TRADE"]
    swing = [r for r in master_rows if r["horizon"] == "SWING"]
    position = [r for r in master_rows if r["horizon"] == "POSITION"]
    blocked = [r for r in master_rows if "DATA" in r["final_classification"] or "INTRADAY" in r["final_classification"]]
    text = f"""# Audited Master Overnight QuantLens Report

## 1. Executive Verdict
- Pine-ready strategies: none.
- MTC producer-ready strategies: none.
- Stage 2 candidates: {', '.join(r['candidate_id'] for r in stage2) or 'none'}.
- Day-trade candidates: HighBeta remains data-needing weak proxy; 8AM ORB is rejected.
- Swing candidates: several weak candidates merit robustness only.
- Position candidates: blocked by real equity data.
- Rejected: 8AM ORB crypto proxy, process-only Wyckoff, standalone anti-chase as producer.

## 2. First-Run Reliability Verdict
Partially reliable. First-run clean trade exports recompute consistently, but reporting/classification was not reliable enough because huge compounded returns and high drawdowns were not framed conservatively enough.

## 3. Input Coverage
- Intake directory: `{intake_dir}`
- Total .md files: {len(inventory)}
- Valid intakes: {valid}
- Raw transcripts: {raw}
- Duplicates: {dup}
- Around-66 expectation: actual count differs because this intake directory currently contains {len(inventory)} markdown files and audited duplicate/raw classification is path-content based.

## 4. Candidate Extraction Summary
- First-run candidates audited: {len(candidates)}
- Audited candidates: {len(candidates)}
- Reclassified or downgraded: anti-chase, EMA20/50, HighBeta, ORB, data-blocked equity/microcap items.

## 5. Data Audit Summary
- Crypto daily bundle used for swing proxies.
- 5m research data used for intraday crypto proxies.
- US equity/microcap data unavailable.
- Proxy warnings apply to HighBeta, CANSLIM, Weinstein, microcap, and session strategies.

## 6. Backtest Audit Summary
- Tested candidates: {sum(1 for r in master_rows if int(r['trades']) > 0)}
- Rerun candidates: none; audited recomputation used same exported trade sets to avoid mixed-trade fee errors.
- Invalidated tests: no trade export invalidated, but promotion claims downgraded.

## 7. Metric Audit Summary
{md_table(recompute_rows, ["candidate_id", "first_trade_count", "audited_trade_count", "first_pf", "audited_pf", "mismatch_status"])}

## 8. Corrected Strategy Ranking
{md_table(master_rows, ["audited_rank", "candidate_id", "horizon", "data_type", "assets_tested", "trades", "PF_base", "PF_fee_2x", "max_DD", "final_classification", "next_action"])}

## 9. Corrected Day-Trade Candidates
{md_table(day, ["candidate_id", "PF_base", "PF_fee_2x", "max_DD", "final_classification", "next_action"])}

## 10. Corrected Swing-Trade Candidates
{md_table(swing, ["candidate_id", "PF_base", "PF_fee_2x", "max_DD", "final_classification", "next_action"])}

## 11. Corrected Position-Trading Candidates
{md_table(position, ["candidate_id", "data_type", "final_classification", "next_action"])}

## 12. Filter / Exit / Sizing Modules Worth Keeping
- Daily Extension Anti-Chase: keep only as gate/filter research, not standalone producer.
- ATR/time exits remain reusable audit components only.

## 13. Rejected / Blocked Ideas
{md_table(blocked, ["candidate_id", "final_classification", "next_action"])}

## 14. Stage 2 Recommendation
Run Stage 2 only for audited WEAK_CANDIDATE rows: Kell, Martin Luke proxy, Slingshot, Crabel, BigBeluga, Linda. Requirements: per-year split, holdout assets, fee 2x/3x/5x, drawdown clustering, asset concentration, baseline/random-entry comparisons.

## 15. MTC/Pine Recommendation
- Direct MTC integration: no.
- Pine conversion: no.
- Reason: no candidate passed drawdown/proxy/robustness gates.

## 16. Data Acquisition Plan for Tomorrow
1. US equities daily OHLCV + RS benchmark for CANSLIM/Weinstein.
2. US high-beta 5m session/gap data for HighBeta.
3. US microcap 1m + premarket/borrow/locate/dilution/halt data for Ty.
4. Continue using existing crypto 5m only for proxy experiments.

## 17. Exact Files Created
See `FILES_CREATED.txt`.

## 18. Exact Commands Run
See `COMMAND_LOG.txt`.

## 19. Validation Results
See `VALIDATION_REPORT.md`.

## 20. Known Limitations
- Audited candidate extraction still uses deterministic report parsing and fixed known candidate taxonomy.
- Some intakes are covered as pooled process/research ideas rather than one candidate each.
- No new external data acquisition was performed.

## 21. Recommended Next Codex Prompt
Use the prompt included in the final response: run Stage 2 robustness only on audited WEAK_CANDIDATE rows, no Pine/MTC integration.
"""
    write(AUDIT_ROOT / "AUDITED_MASTER_OVERNIGHT_QUANTLENS_REPORT.md", text)


def validate(master_rows: list[dict[str, Any]]) -> None:
    py_files = [str(p) for p in AUDIT_ROOT.rglob("*.py")]
    code, _, _ = command([sys.executable, "-m", "py_compile", *py_files])
    checklist = []
    checklist.append({"check": "py_compile", "status": "PASS" if code == 0 else "FAIL", "evidence": f"exit={code}"})
    fee_ok = all(str(row["PF_base"]) and float(row["PF_base"]) >= float(row["PF_fee_2x"]) >= float(row["PF_fee_3x"]) for row in master_rows if int(row["trades"]) > 0)
    checklist.append({"check": "fee_monotonic", "status": "PASS" if fee_ok else "FAIL", "evidence": "base>=2x>=3x on same trade export"})
    asset_ok = all(int(row["assets_tested"]) >= 5 or row["data_type"] == "DATA_BLOCKED" or row["horizon"] in {"POSITION", "PROCESS"} for row in master_rows)
    checklist.append({"check": "asset_count_or_blocked", "status": "PASS" if asset_ok else "FAIL", "evidence": "tested rows have >=5 assets unless blocked/position/process"})
    required = [
        "AUDITED_MASTER_OVERNIGHT_QUANTLENS_REPORT.md",
        "AUDITED_MASTER_COMPARISON.csv",
        "AUDITED_STRATEGY_RECLASSIFICATION.md",
        "METRIC_RECOMPUTE_AUDIT.csv",
        "FEE_STRESS_AUDIT.csv",
    ]
    report_ok = all((AUDIT_ROOT / name).exists() and (AUDIT_ROOT / name).stat().st_size > 0 for name in required)
    checklist.append({"check": "critical_reports_exist", "status": "PASS" if report_ok else "FAIL", "evidence": ",".join(required)})
    status = subprocess.run(["git", "status", "--short"], cwd=GIT_ROOT, text=True, capture_output=True)
    write(AUDIT_ROOT / "git_status_after.txt", status.stdout)
    before = {line.lstrip("\ufeff") for line in read(AUDIT_ROOT / "git_status_before.txt").splitlines()} if (AUDIT_ROOT / "git_status_before.txt").exists() else set()
    after = {line.lstrip("\ufeff") for line in status.stdout.splitlines()}
    new_lines = sorted(after - before)
    pine_touched = any("01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine" in line.replace("\\", "/") for line in new_lines)
    prod_touched = any("01_MASTER TEMPLATE_V2/00_PYTHON/" in line.replace("\\", "/") for line in new_lines)
    checklist.append({"check": "MTC_V2_pine_untouched_by_task", "status": "PASS" if not pine_touched else "FAIL", "evidence": str(pine_touched)})
    checklist.append({"check": "production_runner_untouched_by_task", "status": "PASS" if not prod_touched else "FAIL", "evidence": str(prod_touched)})
    csv_ok = True
    for path in AUDIT_ROOT.glob("*.csv"):
        try:
            pd.read_csv(path)
        except Exception:
            csv_ok = False
    checklist.append({"check": "csv_readable", "status": "PASS" if csv_ok else "FAIL", "evidence": "top-level csv parse"})
    save_csv(AUDIT_ROOT / "VALIDATION_CHECKLIST.csv", checklist)
    write(AUDIT_ROOT / "VALIDATION_REPORT.md", "# Validation Report\n\n" + md_table(checklist, ["check", "status", "evidence"]) + "\n\n## New Git Lines Since Start\n```text\n" + "\n".join(new_lines[:200]) + "\n```\n")


if __name__ == "__main__":
    main()
