"""
pipeline_reader — candidate-centric 6-stage pipeline view (read-only).

Joins the already-built domain statuses (registry, pine builder, liveops, parity,
backtest) by candidate/strategy id into one "where is each strategy in the pipeline"
board, so a returning user instantly sees: what stage each item is at, the key
evidence metric per stage, and the single next action.

6 stages (simplified from the 9-step workflow):
  1 DISCOVERED   intake + deterministic spec
  2 BACKTESTED   sandbox + wide test (walk-forward / OOS / alpha)
  3 PROMOTED     promotion packet -> parity candidate
  4 PRE_PARITY   PineTS Pine<->Python same-data parity
  5 PAPER_TRADE  forward paper-trade
  6 INTEGRATED   MTC_v2 producer + final parity + approved

This module READS only. It does not run or write anything.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

from .paths import default_quantlens_root
from .presentation_reader import action_hint, build_scorecard, load_stg_code_map, resolve_stg_code

STAGES = [
    {"key": "discovered", "label": "Discovered", "hint": "intake + spec"},
    {"key": "classified", "label": "Classified", "hint": "candidate / wiki / rejected"},
    {"key": "backtested", "label": "Backtested", "hint": "walk-forward / OOS / alpha"},
    {"key": "promoted", "label": "Promoted", "hint": "parity candidate"},
    {"key": "pre_parity", "label": "Pre-Parity", "hint": "PineTS Pine=Python"},
    {"key": "paper_trade", "label": "Paper-Trade", "hint": "forward, no capital"},
    {"key": "integrated", "label": "Integrated", "hint": "MTC_v2 + final parity"},
]
# status: done | active | pending | fail | na
ORDER = [s["key"] for s in STAGES]


# Plain-language descriptions, matched by a token in the id/name (first match wins).
# Written for a user who does not yet know what each strategy does.
DESCRIPTIONS: list[tuple[str, dict]] = [
    ("8EMA_EXIT_TRAIL", {"family": "8 EMA Pullback + Trailing Exit",
        "what": "Yukarı trendde, fiyat 8 günlük EMA'ya geri çekilip tekrar yükselince devam alımı yapar.",
        "entry": "Fiyat 8 EMA üstünde, ortalamaya yakın geri çekiliş, öncesinde güçlü itki (impulse).",
        "exit": "Fiyat 8 EMA'nın altına kapanınca çıkar (trailing); ayrıca sabit stop."}),
    ("8EMA", {"family": "8 EMA Pullback",
        "what": "Yukarı trendde 8 EMA'ya geri çekilişte devam alımı.",
        "entry": "close > 8 EMA + ortalamaya yakınlık + güçlü itki.",
        "exit": "2R kâr hedefi veya stop."}),
    ("TWO_CANDLE", {"family": "İki Mum Destek/Direnç Kırılımı",
        "what": "Bir direnç seviyesini güçlü bir mumla kıran fiyatta alım yapar.",
        "entry": "Mum, aralığının üst üçte birinde kapanır + son 200 barın en yükseğini kırar.",
        "exit": "2R kâr hedefi veya stop."}),
    ("RSI_OVERSOLD", {"family": "RSI Aşırı Satım Dönüşü (ortalamaya dönüş)",
        "what": "RSI aşırı satımdan toparlamaya başlayınca alım yapar — düşüşte 'dip' yakalama mantığı.",
        "entry": "RSI(5) önce 35 altına iner, sonra 45 üstüne çıkar.",
        "exit": "2R kâr hedefi veya stop. (Trend filtresi yok — zayıf kenar.)"}),
    ("RSI_CONFLUENCE", {"family": "RSI + Trend Teyidi",
        "what": "Fiyat hareketli ortalamanın üstündeyken RSI 50 seviyesini yukarı kesince alım.",
        "entry": "close > SMA ve RSI 50'yi aşağıdan yukarı keser.",
        "exit": "2R kâr hedefi veya stop."}),
    ("DUAL_RSI", {"family": "Çift RSI (Günlük + Saatlik)",
        "what": "Günlük RSI trendi yukarıyken, saatlik geri çekilişte alım yapar.",
        "entry": "Günlük RSI yüksek (>60) + saatlik RSI eşiği yukarı keser.",
        "exit": "2R hedef veya son barların swing dibinde stop."}),
    ("BOLLINGER", {"family": "Bollinger Sıkışma Kırılımı",
        "what": "Bantlar daraldıktan (volatilite sıkışması) sonra üst bandın gövdeli kırılışında alım.",
        "entry": "Dar bant + üst bandın üstüne güçlü gövdeli kapanış.",
        "exit": "2R hedef veya stop."}),
    ("VWAP", {"family": "VWAP Geri Çekiliş",
        "what": "Yükselen VWAP'a geri çekilişte alım yapar.",
        "entry": "VWAP eğimi yukarı + fiyat VWAP'a yakın ve üstünde.",
        "exit": "2R hedef veya banttan stop."}),
    ("CANDLESTICK", {"family": "Destekte Yutan Mum (Engulfing)",
        "what": "Destek bölgesinde boğa yutan mum formasyonu oluşunca alım.",
        "entry": "Destek yakınında bullish engulfing mum.",
        "exit": "2R hedef veya stop."}),
    ("MULTI_EMA_CHANNEL", {"family": "Çoklu EMA Kanalı Geri Çekiliş",
        "what": "Uzun vade yukarı (EMA200 üstü), kısa EMA'lar dizili; kanala temas edince alım.",
        "entry": "close > EMA200, EMA5 > EMA13, kanala geri çekiliş.",
        "exit": "2R hedef veya stop."}),
    ("LE_MODEL_BULL_FLAG", {"family": "Boğa Bayrağı Kırılımı",
        "what": "Güçlü yükseliş sonrası kısa konsolidasyonun (bayrak) kırılışında alım.",
        "entry": "8 EMA itki + geri çekiliş kırılımı.",
        "exit": "2R hedef veya stop."}),
    ("PURPLE_PROFITS", {"family": "8 EMA Trend (Purple Profits)",
        "what": "8 EMA trend takibi; 'mor çizgi' konseptinin sadeleştirilmiş hali.",
        "entry": "8 EMA üstünde itki + geri çekiliş.",
        "exit": "2R hedef veya stop."}),
    ("10M_8EMA", {"family": "8 EMA Pullback (10dk kökenli)",
        "what": "8 EMA'ya geri çekilişte devam alımı (orijinali 10dk hisse senedi videosu).",
        "entry": "close > 8 EMA + geri çekiliş + itki.",
        "exit": "2R hedef veya stop."}),
    ("TV_BUYSELL", {"family": "TradingView Al/Sat İndikatör Paketi (salvage)",
        "what": "5 hazır al/sat indikatörü. Tam bir strateji değil; tek bir açık formül seçilip denetlenmeden kullanılmaz.",
        "entry": "—", "exit": "—"}),
    ("EQUILIBRIUM", {"family": "Equilibrium Momentum Diverjans (salvage)",
        "what": "BigBeluga osilatör diverjansı. Kaynak ve repaint denetimi yapılmadan kullanılmaz.",
        "entry": "—", "exit": "—"}),
    ("RANKED_FVG", {"family": "Ranked FVG Imbalance Zones (salvage)",
        "what": "Fiyat boşluğu (FVG) bölgeleri indikatörü. Formül netleşmeden kullanılmaz.",
        "entry": "—", "exit": "—"}),
]
_DEFAULT_DESC = {"family": "Bilinmeyen", "what": "Açıklama henüz eklenmedi.", "entry": "—", "exit": "—"}
DESCRIPTIONS = [
    ("FAM_PULLBACK_TO_MA", {"family": "Trend Pullback to Moving Average",
        "what": "In an uptrend, buys the continuation when price pulls back to a fast moving average and closes back up off it.",
        "entry": "close > slow MA (uptrend) + prior bar tagged the fast MA + close turns back up above the fast MA.",
        "exit": "Swing-low stop; holding-bar limit."}),
    ("FAM_CONSOLIDATION_BREAKOUT", {"family": "Tight-Consolidation Breakout",
        "what": "Enters when price breaks out of a narrow consolidation channel within an uptrend.",
        "entry": "Prior N-bar channel is tight (range/price < threshold) + uptrend + close breaks the prior channel high.",
        "exit": "Swing-low stop; holding-bar limit."}),
    ("FAM_MOMENTUM_CONTINUATION", {"family": "Momentum / RS Continuation",
        "what": "Buys a fresh breakout high while momentum is positive and the trend is up (relative-strength continuation).",
        "entry": "close > trend EMA + prior-bar ROC > 0 + close breaks the prior N-bar high.",
        "exit": "Swing-low stop; holding-bar limit."}),
    ("OLIVER_KELL", {"family": "Oliver Kell Price Cycle (10/20 EMA)",
        "what": "In a 10/20 EMA 'green-light' regime, buys the continuation when price snaps back below the EMAs and then reclaims them (wedge pop).",
        "entry": "Price was below the 20 EMA in recent bars (snapback) + crosses back above the 10 EMA + higher low + close above the 20 EMA.",
        "exit": "Swing-low stop; loss of the EMA regime (engine exit)."}),
    ("LBR_COIL", {"family": "Linda Raschke — Coil Breakout / Range Expansion",
        "what": "Enters a range-expansion breakout after a volatility contraction (coil).",
        "entry": "Prior bar ATR is squeezed (atr < squeeze x longer ATR average) + close breaks the last N-bar channel high.",
        "exit": "Swing-low stop; holding-bar limit."}),
    ("8EMA_EXIT_TRAIL", {"family": "8 EMA Pullback + Trailing Exit",
        "what": "Buys continuation when price pulls back toward the 8 EMA during an uptrend and resumes higher.",
        "entry": "Price stays above the 8 EMA, pulls back near the average, and follows a prior impulse move.",
        "exit": "Exit when price closes below the 8 EMA as a trailing exit; fixed stop also applies."}),
    ("8EMA", {"family": "8 EMA Pullback",
        "what": "Buys continuation pullbacks to the 8 EMA during an uptrend.",
        "entry": "Close is above the 8 EMA, price is near the average, and recent impulse is strong.",
        "exit": "2R profit target or stop."}),
    ("TWO_CANDLE", {"family": "Two-Candle Support/Resistance Breakout",
        "what": "Buys when price breaks a resistance level with a strong candle.",
        "entry": "The candle closes in the upper third of its range and breaks the highest high of the last 200 bars.",
        "exit": "2R profit target or stop."}),
    ("RSI_OVERSOLD", {"family": "RSI Oversold Reversal",
        "what": "Buys when RSI starts recovering from oversold conditions; this is a dip-catch mean-reversion idea.",
        "entry": "RSI(5) first drops below 35, then crosses back above 45.",
        "exit": "2R profit target or stop. No trend filter is defined, so the edge is weak."}),
    ("RSI_CONFLUENCE", {"family": "RSI + Trend Confirmation",
        "what": "Buys when RSI crosses above 50 while price is above the moving average.",
        "entry": "Close is above the SMA and RSI crosses 50 from below.",
        "exit": "2R target or stop."}),
    ("DUAL_RSI", {"family": "Dual RSI Daily + Hourly",
        "what": "Buys hourly pullbacks while the daily RSI trend remains strong.",
        "entry": "Daily RSI is high (>60) and hourly RSI crosses the entry threshold upward.",
        "exit": "2R target or stop below the recent swing low."}),
    ("BOLLINGER", {"family": "Bollinger Squeeze Breakout",
        "what": "Buys a strong upper-band breakout after the bands contract.",
        "entry": "Narrow bands plus a strong-bodied close above the upper band.",
        "exit": "2R target or stop."}),
    ("VWAP", {"family": "VWAP Pullback",
        "what": "Buys pullbacks toward a rising VWAP.",
        "entry": "VWAP slope is up and price is near or above VWAP.",
        "exit": "2R target or band-based stop."}),
    ("CANDLESTICK", {"family": "Support Engulfing Candle",
        "what": "Buys when a bullish engulfing candle appears near support.",
        "entry": "Bullish engulfing candle near a support zone.",
        "exit": "2R target or stop."}),
    ("MULTI_EMA_CHANNEL", {"family": "Multi-EMA Channel Pullback",
        "what": "Buys a channel touch when the long-term trend is up and short EMAs are aligned.",
        "entry": "Close is above EMA200, EMA5 is above EMA13, and price pulls back into the channel.",
        "exit": "2R target or stop."}),
    ("LE_MODEL_BULL_FLAG", {"family": "Bull Flag Breakout",
        "what": "Buys the breakout of a short consolidation after a strong advance.",
        "entry": "8 EMA impulse followed by a pullback breakout.",
        "exit": "2R target or stop."}),
    ("PURPLE_PROFITS", {"family": "8 EMA Trend (Purple Profits)",
        "what": "Tracks the 8 EMA trend; a simplified version of the original purple-line concept.",
        "entry": "Impulse and pullback while price remains above the 8 EMA.",
        "exit": "2R target or stop."}),
    ("10M_8EMA", {"family": "8 EMA Pullback from 10-Minute Source",
        "what": "Buys continuation pullbacks to the 8 EMA, originally described in a 10-minute stock-video context.",
        "entry": "Close is above the 8 EMA with a pullback and impulse.",
        "exit": "2R target or stop."}),
    ("TV_BUYSELL", {"family": "TradingView Buy/Sell Indicator Pack (Salvage)",
        "what": "Five ready-made buy/sell indicators. This is not a complete strategy until one open formula is selected and audited.",
        "entry": "--", "exit": "--"}),
    ("EQUILIBRIUM", {"family": "Equilibrium Momentum Divergence (Salvage)",
        "what": "BigBeluga oscillator divergence idea. It should not be used until source and repaint behavior are audited.",
        "entry": "--", "exit": "--"}),
    ("RANKED_FVG", {"family": "Ranked FVG Imbalance Zones (Salvage)",
        "what": "Fair-value-gap zone indicator. It should not be used before the exact formula is clarified.",
        "entry": "--", "exit": "--"}),
]
_DEFAULT_DESC = {"family": "Unknown", "what": "No strategy description has been added yet.", "entry": "--", "exit": "--"}


def _describe(*texts: str) -> dict:
    blob = " ".join(t for t in texts if t).upper()
    for token, desc in DESCRIPTIONS:
        if token in blob:
            return desc
    return _DEFAULT_DESC


def _youtube(url: str | None) -> str:
    u = str(url or "").strip().lstrip("* ").strip()
    match = re.search(r"https?://(?:www\.)?(?:youtube\.com/watch\?v=[^\s]+|youtu\.be/[^\s]+)", u)
    if match:
        u = match.group(0).rstrip(").,")
    if "youtube.com/watch" in u or "youtu.be/" in u:
        return u
    return ""


def _promoted_dir(mcc_root: str | Path) -> Path:
    return default_quantlens_root(mcc_root) / "06_PROMOTED_TO_PARITY"


def _quantlens_root(mcc_root: str | Path) -> Path:
    return default_quantlens_root(mcc_root)


def _read_pinets_result(promoted_dir: Path, strategy_id: str) -> dict | None:
    p = promoted_dir / strategy_id / "PINETS_PARITY_RESULT.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _read_producer_spec(promoted_dir: Path, strategy_id: str) -> dict:
    p = promoted_dir / strategy_id / "producer_spec.json"
    if not p.exists():
        return {}
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return raw if isinstance(raw, dict) else {}


def _producer_spec_detail(promoted_dir: Path, spec_dir_name: str, spec: dict | None) -> dict[str, Any] | None:
    if not spec:
        return None
    spec_path = promoted_dir / spec_dir_name / "producer_spec.json"
    source_url = _youtube(spec.get("source_url"))
    rules_high_confidence = spec.get("rules_high_confidence")
    if not isinstance(rules_high_confidence, list):
        rules_high_confidence = []
    detail = {
        "path": str(spec_path),
        "relative_path": _relative_to_lab(spec_path, promoted_dir),
        "title": spec.get("title") or spec_dir_name,
        "kind": spec.get("kind"),
        "source_url": source_url,
        "source_candidate": spec.get("source_candidate"),
        "rules_high_confidence": rules_high_confidence,
        "entry_pseudo": spec.get("entry_pseudo"),
        "exit_pseudo": spec.get("exit_pseudo"),
        "param_grid_size_planned": spec.get("param_grid_size_planned"),
        "promoted_at": spec.get("promoted_at"),
        "fidelity_to_original_youtube_source": spec.get("fidelity_to_original_youtube_source"),
        "next_action": "Run PineTS parity",
    }
    summary_bits = [
        detail["title"],
        f"kind={detail['kind']}" if detail["kind"] else "",
        f"grid={detail['param_grid_size_planned']}" if detail["param_grid_size_planned"] is not None else "",
        f"source={detail['source_candidate']}" if detail["source_candidate"] else "",
        f"fidelity={detail['fidelity_to_original_youtube_source']}" if detail["fidelity_to_original_youtube_source"] else "",
    ]
    detail["summary"] = " · ".join(bit for bit in summary_bits if bit)
    return detail


def _iter_producer_specs(promoted_dir: Path) -> list[tuple[str, dict]]:
    specs: list[tuple[str, dict]] = []
    if not promoted_dir.exists():
        return specs
    for path in sorted(promoted_dir.glob("*/producer_spec.json")):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(raw, dict):
            specs.append((path.parent.name, raw))
    return specs


def _pinets_proof(promoted_dir: Path, strategy_id: str, raw: dict | None) -> dict | None:
    if not raw:
        return None
    p = promoted_dir / strategy_id / "PINETS_PARITY_RESULT.json"
    return {
        "status": raw.get("verdict") or "UNKNOWN",
        "path": str(p),
        "relative_path": _relative_to_lab(p, promoted_dir),
        "summary": {
            "verdict": raw.get("verdict"),
            "signal_agreement_pct": raw.get("signal_agreement_pct"),
            "bars_compared": raw.get("bars_compared"),
            "pine_long_signals": raw.get("pine_long_signals"),
            "python_long_signals": raw.get("python_long_signals"),
            "long_both": raw.get("long_both"),
            "long_only_pine": raw.get("long_only_pine"),
            "long_only_python": raw.get("long_only_python"),
            "ema8_max_rel_diff": raw.get("ema8_max_rel_diff"),
            "atr14_max_rel_diff": raw.get("atr14_max_rel_diff"),
            "warmup_excluded": raw.get("warmup_excluded"),
        },
        "raw": raw,
    }


def _equity_curve(promoted_dir: Path, strategy_id: str, max_points: int = 60) -> list[float] | None:
    """Cumulative compounded equity (start 100) from a candidate's trades CSV `ret_net_pct`.
    Downsampled to <= max_points. Read-only; returns None if no/invalid file."""
    p = promoted_dir / strategy_id / f"{strategy_id}_trades.csv"
    if not p.exists():
        return None
    try:
        eq = 100.0
        series = [eq]
        with p.open("r", encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                try:
                    r = float(row.get("ret_net_pct", "") or 0.0)
                except (TypeError, ValueError):
                    continue
                eq *= (1.0 + r / 100.0)
                series.append(round(eq, 3))
        if len(series) < 3:
            return None
        if len(series) > max_points:
            step = len(series) / max_points
            series = [series[int(i * step)] for i in range(max_points)] + [series[-1]]
        return series
    except Exception:
        return None


def _paper_trade_detail(promoted_dir: Path, strategy_id: str, plan: dict | None) -> dict | None:
    strategy_dir = promoted_dir / strategy_id
    plan_path = strategy_dir / "FORWARD_PAPER_TRADE_PLAN.md"
    plan_exists = plan_path.exists()
    forward_results = _read_forward_results(strategy_dir)
    if not plan and not plan_exists and not forward_results:
        return None

    detail = {
        "status": (plan or {}).get("status") or ("PAPER_PLAN_ONLY" if plan_exists else "WAITING_FOR_PLAN"),
        "live_orders_enabled": bool((plan or {}).get("live_orders_enabled")),
        "webhook_enabled": bool((plan or {}).get("webhook_enabled")),
        "forward_trades": (plan or {}).get("forward_trade_count", 0),
        "plan_path": (plan or {}).get("relative_path") or (_relative_to_lab(plan_path, promoted_dir) if plan_exists else None),
        "plan_source_path": str(plan_path) if plan_exists else (plan or {}).get("source_path"),
        "plan_title": (plan or {}).get("title") or (_markdown_title(plan_path) if plan_exists else None),
        "plan_summary": _paper_plan_summary(plan_path) if plan_exists else [],
        "forward_results": forward_results,
    }
    if not forward_results:
        detail["forward_status"] = "WAITING_FOR_FORWARD_RESULTS"
    return detail


def _read_forward_results(strategy_dir: Path) -> dict | None:
    if not strategy_dir.exists():
        return None

    json_matches = sorted(
        path for pattern in ("*FORWARD*RESULT*.json", "*forward*result*.json", "*PAPER*RESULT*.json", "*paper*result*.json")
        for path in strategy_dir.glob(pattern)
    )
    for path in json_matches:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(raw, dict):
            return {
                "type": "json",
                "path": str(path),
                "file": path.name,
                "status": raw.get("status") or raw.get("verdict") or "RESULTS_FOUND",
                "metrics": _forward_metric_summary(raw),
                "raw": raw,
            }

    csv_matches = sorted(
        path for pattern in ("*FORWARD*TRADES*.csv", "*forward*trades*.csv", "*PAPER*TRADES*.csv", "*paper*trades*.csv")
        for path in strategy_dir.glob(pattern)
    )
    for path in csv_matches:
        summary = _forward_csv_summary(path)
        if summary:
            return {"type": "csv", "path": str(path), "file": path.name, "status": "RESULTS_FOUND", "metrics": summary}
    return None


def _forward_metric_summary(raw: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "trades", "trade_count", "forward_trade_count", "win_rate", "win_rate_pct",
        "profit_factor", "expectancy_r", "expectancy", "max_drawdown_pct",
        "strategy_return_pct", "return_pct", "buy_hold_return_pct",
        "benchmark_return_pct", "excess_alpha_pct", "alpha_pct",
        "started_at", "ended_at", "generated_at",
    )
    metrics = {key: raw.get(key) for key in keys if raw.get(key) is not None}
    nested = raw.get("metrics") if isinstance(raw.get("metrics"), dict) else {}
    for key in keys:
        if key not in metrics and nested.get(key) is not None:
            metrics[key] = nested.get(key)
    return metrics


def _forward_csv_summary(path: Path) -> dict[str, Any] | None:
    try:
        rows = list(csv.DictReader(path.open("r", encoding="utf-8", newline="")))
    except Exception:
        return None
    if not rows:
        return None
    returns = []
    for row in rows:
        value = row.get("ret_net_pct") or row.get("return_pct") or row.get("strategy_return_pct")
        try:
            returns.append(float(value))
        except (TypeError, ValueError):
            continue
    return {
        "trades": len(rows),
        "strategy_return_pct": round(_compound_returns(returns), 4) if returns else None,
    }


def _compound_returns(returns_pct: list[float]) -> float:
    equity = 1.0
    for value in returns_pct:
        equity *= 1.0 + value / 100.0
    return (equity - 1.0) * 100.0


def _paper_plan_summary(path: Path) -> list[str]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []
    picked = []
    wanted = ("Minimum observation", "Minimum NEW forward trades", "Stop conditions", "Promotion conditions")
    for line in lines:
        stripped = re.sub(r"[*`]", "", line.strip().lstrip("- ").strip())
        if stripped and any(token.lower() in stripped.lower() for token in wanted):
            picked.append(stripped[:220])
        if len(picked) >= 5:
            break
    return picked


def _markdown_title(path: Path) -> str | None:
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip() or path.stem
            if stripped:
                return stripped[:120]
    except Exception:
        pass
    return None


def _relative_to_lab(path: Path, promoted_dir: Path) -> str:
    try:
        return str(path.relative_to(promoted_dir.parent))
    except ValueError:
        return str(path)


def _directional_research(rid: str, name: str, direction: str | None, spec: dict | None = None) -> dict:
    spec = spec or {}
    current_direction = str(spec.get("direction") or direction or "unknown")
    long_rule = spec.get("long_signal_definition")
    short_rule = spec.get("short_signal_definition")
    family = _describe(rid, name).get("family", "Unknown")
    suggested = short_rule or _short_rule_hint(rid, name, family)

    if str(current_direction).lower() in {"short", "short_only"}:
        status = "SHORT_DEFINED"
        next_action = "Verify short-side evidence, parity, and paper-trade before any integration."
    elif short_rule:
        status = "SHORT_RULE_DEFINED_NOT_PROMOTED"
        next_action = "Backtest the existing short rule as a separate candidate before promotion."
    elif str(current_direction).lower() == "long_only":
        status = "SHORT_UNTESTED"
        next_action = "Create a separate short candidate and run walk-forward / OOS before trusting it."
    else:
        status = "DIRECTION_UNKNOWN"
        next_action = "Define long/short direction explicitly before backtest or parity."

    return {
        "current_direction": current_direction,
        "status": status,
        "long_signal_definition": long_rule,
        "short_signal_definition": short_rule,
        "suggested_short_research_rule": suggested,
        "next_action": next_action,
        "warning": "No short metrics are implied by the long-only result; short side needs its own evidence.",
    }


def _short_rule_hint(*texts: str) -> str:
    blob = " ".join(t for t in texts if t).upper()
    if "8EMA" in blob or "8 EMA" in blob:
        return "Research mirror: close < ema8, slope < 0, pullback near ema8, prior impulse; stop at recent swing high; exit when close > ema8."
    if "TWO_CANDLE" in blob or "DESTEK/DIREN" in blob or "SUPPORT" in blob:
        return "Research mirror: strong lower-third close breaking prior low / support; stop at recent high; fixed-R or time exit."
    if "RSI_OVERSOLD" in blob or "AŞIRI SAT" in blob:
        return "Research mirror: RSI overbought fade, e.g. rsi exits overbought downward; stop at recent high; fixed-R or time exit."
    if "RSI" in blob:
        return "Research mirror: bearish RSI/confluence trigger, e.g. trend filter down and RSI crosses below the trigger level."
    if "BOLLINGER" in blob:
        return "Research both sides explicitly: lower-band long and upper-band short are different regimes and need separate filters."
    if "VWAP" in blob:
        return "Research mirror: bearish VWAP rejection/rally-to-VWAP short with session and trend filters."
    if "CANDLESTICK" in blob:
        return "Research mirror: bearish candlestick pattern at resistance with past-only confluence."
    if "EMA" in blob:
        return "Research mirror: bearish EMA/channel pullback with stop above channel or recent swing high."
    return "Research short side as a separate candidate only after the direction, stop, target, and no-lookahead rules are explicit."


def _cell(status: str, metric: str = "") -> dict:
    return {"status": status, "metric": metric}


def _classification_cell(
    status_str: str,
    evidence_level: str,
    notes: str = "",
    summary: str = "",
    recommended_action: str = "",
    source_url: str = "",
    is_promoted: bool = False,
) -> dict:
    blob = " ".join(
        str(value or "") for value in (
            status_str,
            evidence_level,
            notes,
            summary,
            recommended_action,
            source_url,
        )
    ).upper()
    if is_promoted or evidence_level in ("backtested", "prototyped", "promoted_to_parity") or any(
        token in blob for token in ("BACKTESTED", "PROTOTYPED", "PROMOTE_TO_PARITY", "PARITY_CANDIDATE")
    ):
        return _cell("done", "candidate")
    if any(token in blob for token in ("REJECT", "REJECTED", "DATA_BLOCKED", "DO_NOT_TEST")):
        return _cell("done", "rejected")
    has_multiple_indicator_signal = "INDICATOR" in blob and any(
        token in blob for token in ("FIVE", "5 ", "MULTIPLE", "SEVERAL")
    )
    if has_multiple_indicator_signal or any(
        token in blob for token in ("OPEN_FORMULA", "FORMULA IS SELECTED", "INDICATOR PACK", "BUYSELL_INDICATOR_PACK")
    ):
        return _cell("done", "split_required")
    if "SALVAGE_ONLY" in blob:
        return _cell("done", "source_audit")
    if any(
        token in blob
        for token in (
            "WIKI_ONLY",
            "TRADER_WISDOM_ONLY",
            "PROCESS_OR_WORKFLOW_ONLY",
            "MANUAL_VISUAL_REVIEW_ONLY",
            "FILTER_MODULE",
            "ADD_TO_WIKI_ONLY",
            "WISDOM_ONLY",
            "NO_BACKTEST",
            "MODULE",
        )
    ):
        return _cell("done", "wiki")
    return _cell("done", "candidate")


_EXTRA_DISCOVERY_PATTERNS = (
    "research/**/FINAL_LLM_KNOWLEDGE_BASE.jsonl",
    "research/**/AUDITED_CANDIDATE_EXTRACTION.jsonl",
    "12_LLM_WIKI/**/quantlens_strategy_candidates.jsonl",
    "12_LLM_WIKI/**/quantlens_knowledge_base.jsonl",
)


def _discover_extra_quantlens_candidates(mcc_root: str | Path, known_ids: set[str]) -> list[dict[str, Any]]:
    root = _quantlens_root(mcc_root)
    if not root.exists():
        return []

    discovered: dict[str, dict[str, Any]] = {}
    for pattern in _EXTRA_DISCOVERY_PATTERNS:
        for path in sorted(root.glob(pattern)):
            for row in _iter_jsonl(path):
                cid = str(row.get("candidate_id") or row.get("strategy_id") or "").strip()
                if not cid or cid in known_ids:
                    continue
                candidate = _extra_candidate_from_row(row, path, root)
                previous = discovered.get(cid)
                if previous is None or candidate["_rank"] > previous["_rank"]:
                    discovered[cid] = candidate

    rows = list(discovered.values())
    for row in rows:
        row.pop("_rank", None)
    return rows


def _iter_jsonl(path: Path) -> list[dict[str, Any]]:
    items = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return items
    for line in lines:
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except Exception:
            continue
        if isinstance(raw, dict):
            items.append(raw)
    return items


def _extra_candidate_from_row(row: dict[str, Any], path: Path, root: Path) -> dict[str, Any]:
    cid = str(row.get("candidate_id") or row.get("strategy_id") or "").strip()
    title = row.get("title") or row.get("strategy_name") or cid
    action = row.get("recommended_next_action") or row.get("next_action") or ""
    summary = row.get("summary") or row.get("exact_rules_if_available") or ""
    source = _relative_to_quantlens(path, root)
    source_file = _string_value(row.get("source_file") or row.get("intake_path") or row.get("corrected_intake_path"))
    source_url = _source_url_from_source_file(row.get("source_url"), source_file, root)
    return {
        "_rank": _extra_source_rank(path),
        "id": cid,
        "candidate_id": cid,
        "name": title,
        "title": title,
        "status": _extra_status(action, row),
        "evidence_level": "discovered_from_quantlens_jsonl",
        "notes": action or summary,
        "source_url": source_url,
        "source_url_source": "source_file" if source_url and not _youtube(row.get("source_url")) else "source_record",
        "market_type": row.get("asset_class") or row.get("market_type") or "",
        "timeframe": _string_value(row.get("timeframe") or row.get("timeframes")),
        "direction": row.get("direction"),
        "candidate_kind": [row.get("record_type") or "extra_discovery"],
        "candidate_folder": "",
        "source_path": str(path),
        "relative_source_path": source,
        "discovery_source": source,
        "source_file": source_file,
        "summary": summary,
    }


def _extra_status(action: Any, row: dict[str, Any]) -> str:
    blob = " ".join(str(value or "") for value in (
        action,
        row.get("summary"),
        row.get("record_type"),
        row.get("verdict"),
    )).upper()
    if any(token in blob for token in ("REJECT", "DO_NOT_TEST", "WIKI_ONLY", "DATA_BLOCKED")):
        return "DISCOVERED_BLOCKED"
    return "DISCOVERED_REVIEW"


def _extra_source_rank(path: Path) -> int:
    text = str(path).upper()
    if "FINAL_LLM_KNOWLEDGE_BASE" in text:
        return 40
    if "AUDITED_CANDIDATE_EXTRACTION" in text:
        return 30
    if "QUANTLENS_STRATEGY_CANDIDATES" in text:
        return 20
    return 10


def _relative_to_quantlens(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _string_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (str, int, float)):
        return str(value)
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if item not in (None, ""))
    return str(value)


def _source_url_from_source_file(source_url: Any, source_file: str, root: Path) -> str:
    url = _youtube(source_url)
    if url:
        return url
    source_file = source_file.strip()
    if not source_file:
        return ""
    for candidate in _source_file_candidates(source_file, root):
        url = _youtube(_first_youtube_url(candidate))
        if url:
            return url
    return ""


def _source_file_candidates(source_file: str, root: Path) -> list[Path]:
    rel = Path(source_file)
    candidates: list[Path] = []
    quantlens_root = default_quantlens_root(root)
    search_roots = [
        quantlens_root,
        quantlens_root / "00_INBOX_REPORTS",
        quantlens_root / "research",
        root,
    ]
    for base in search_roots:
        direct = base / rel
        if direct.exists():
            candidates.append(direct)
    if candidates:
        return candidates
    for base in search_roots:
        if base.exists():
            candidates.extend(sorted(base.rglob(rel.name)))
        if candidates:
            break
    return candidates


def _first_youtube_url(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    match = re.search(r"https?://(?:www\.)?(?:youtube\.com/watch\?v=[^\s<>\")]+|youtu\.be/[^\s<>\")]+)", text, re.IGNORECASE)
    if not match:
        return ""
    return match.group(0).rstrip(").,")


def build_candidate_pipeline(
    mcc_root: str | Path,
    registry: dict | None,
    pine_builder: dict | None,
    liveops: dict | None,
    parity: dict | None,
    backtest: dict | None,
) -> dict[str, Any]:
    registry = registry or {}
    candidates = registry.get("candidates", []) or []
    strategies = registry.get("strategies", []) or []
    promoted_dir = _promoted_dir(mcc_root)
    stg_map = load_stg_code_map(mcc_root)

    cand_by_id = {c.get("candidate_id") or c.get("id"): c for c in candidates}
    plans = (liveops or {}).get("paper_trade_plans", []) or []
    plan_by_id = {p.get("candidate_id"): p for p in plans}
    drafts = (pine_builder or {}).get("drafts", []) or []
    draft_by_id: dict[str, list] = {}
    for d in drafts:
        draft_by_id.setdefault(d.get("candidate_id"), []).append(d)

    rows: list[dict] = []

    # --- Rows from PROMOTED strategies (QL_ALPHA_*): full journey ---
    promoted_origin_ids = set()
    for s in strategies:
        sid = s.get("strategy_id") or s.get("id")
        spec = _read_producer_spec(promoted_dir, sid)
        producer_spec = _producer_spec_detail(promoted_dir, sid, spec)
        origin = s.get("candidate_id")
        if origin:
            promoted_origin_ids.add(origin)
        status_str = str(s.get("status", "")).upper()
        pf = s.get("profit_factor")
        ret = s.get("return_pct_compound")

        stages: dict[str, dict] = {}
        stages["discovered"] = _cell("done", f"{s.get('symbol','')} {s.get('timeframe','')}".strip())
        stages["classified"] = _classification_cell(
            str(s.get("status", "")),
            "promoted_to_parity",
            str(s.get("notes", "")),
            "",
            "",
            s.get("source_url") or "",
            is_promoted=True,
        )
        bt_metric = []
        if ret is not None:
            bt_metric.append(f"{ret:+.0f}%")
        if pf is not None:
            bt_metric.append(f"PF {pf}")
        stages["backtested"] = _cell("done", " · ".join(bt_metric) if bt_metric else "ok")
        is_promoted = ("PROMOTE" in status_str or "PARITY_CANDIDATE" in status_str
                       or s.get("evidence_level") == "promoted_to_parity")
        stages["promoted"] = _cell("done" if is_promoted else "pending",
                                   "parity candidate" if is_promoted else "")

        # Pre-parity: PineTS exact-parity result file
        pinets = _read_pinets_result(promoted_dir, sid)
        if pinets is not None:
            verdict = str(pinets.get("verdict", "")).upper()
            agree = pinets.get("signal_agreement_pct")
            metric = f"{agree:.0f}% agree" if isinstance(agree, (int, float)) else verdict
            stages["pre_parity"] = _cell("done" if verdict == "PASS" else "fail", metric)
        else:
            # fall back to pine-builder chart status if any
            dl = draft_by_id.get(sid, [])
            chart = next((x.get("chart_status") for x in dl if x.get("chart_status")), None)
            if chart == "PASS":
                stages["pre_parity"] = _cell("active", "TV chart pass (feed≠bundle)")
            else:
                stages["pre_parity"] = _cell("pending", "")

        # Paper-trade
        plan = plan_by_id.get(sid)
        if plan:
            pstatus = str(plan.get("status", "")).upper()
            stages["paper_trade"] = _cell("active", "plan ready" if "PLAN_ONLY" in pstatus else pstatus.lower())
        else:
            stages["paper_trade"] = _cell("pending", "")

        # Integrated (MTC_v2) — not started for any candidate yet
        stages["integrated"] = _cell("pending", "")

        row = _finalize_row(sid, s.get("name") or sid, s.get("symbol"), s.get("timeframe"),
                            origin, stages, s.get("notes", ""))
        origin_cand = cand_by_id.get(origin, {})
        row["source_url"] = _youtube(s.get("source_url") or origin_cand.get("source_url") or (producer_spec or {}).get("source_url"))
        row["description"] = _describe(sid, s.get("name", ""), origin or "")
        row["metrics"] = {
            "return_pct_compound": ret, "profit_factor": pf, "trades": s.get("trades"),
            "max_drawdown_pct": s.get("max_drawdown_pct"), "win_rate": s.get("win_rate"),
            "direction": s.get("direction"),
        }
        row["pinets_parity"] = pinets
        row["pinets_parity_proof"] = _pinets_proof(promoted_dir, sid, pinets)
        row["equity_curve"] = _equity_curve(promoted_dir, sid)
        row["paper_trade_detail"] = _paper_trade_detail(promoted_dir, sid, plan)
        row["directional_research"] = _directional_research(
            sid, s.get("name") or sid, s.get("direction"), spec
        )
        row["producer_spec"] = producer_spec
        row["producer_spec_path"] = producer_spec.get("path") if producer_spec else None
        row["producer_spec_summary"] = producer_spec.get("summary") if producer_spec else None
        row["producer_spec_source_url"] = producer_spec.get("source_url") if producer_spec else None
        row["producer_spec_next_action"] = producer_spec.get("next_action") if producer_spec else None
        row["producer_spec_param_grid"] = producer_spec.get("param_grid_size_planned") if producer_spec else None
        row["stg_code"] = resolve_stg_code(stg_map, origin, sid, s.get("candidate_id"), s.get("strategy_id"))
        row["stg_number"] = _stg_number(row["stg_code"])
        row["scorecard"] = build_scorecard(row)
        row["score"] = row["scorecard"]["total"]
        row["score_band"] = row["scorecard"]["band"]
        row["next_action_hint"] = action_hint(row.get("next_action"))
        row["classification"] = {
            "kind": "candidate",
            "label": "candidate",
            "reason": "Promoted strategy rows are backtest-ready candidate evidence.",
            "next_action": "Run PineTS parity" if pinets is None else "Start forward paper-trade (collect new trades)",
        }
        rows.append(row)

    # --- Rows from early-stage candidates not yet promoted ---
    represented_ids = set(promoted_origin_ids)
    represented_ids.update(str(c.get("candidate_id") or c.get("id")) for c in candidates if c.get("candidate_id") or c.get("id"))
    strategy_ids = {str(s.get("strategy_id") or s.get("id")) for s in strategies if s.get("strategy_id") or s.get("id")}
    represented_ids.update(strategy_ids)

    # --- Rows from producer specs that are not in the canonical strategy registry yet ---
    promoted_spec_ids = set()
    for spec_dir_name, spec in _iter_producer_specs(promoted_dir):
        sid = str(spec.get("candidate_id") or spec_dir_name).strip()
        if not sid or sid in strategy_ids:
            continue
        promoted_spec_ids.add(sid)
        represented_ids.add(sid)

        stages = {
            "discovered": _cell("done", "producer_spec"),
            "classified": _cell("done", "promoted spec"),
            "backtested": _cell("done", "first-pass prototype"),
            "promoted": _cell("done", "parity candidate"),
            "pre_parity": _cell("pending", ""),
            "paper_trade": _cell("pending", ""),
            "integrated": _cell("pending", ""),
        }
        pinets = _read_pinets_result(promoted_dir, spec_dir_name)
        if pinets is not None:
            verdict = str(pinets.get("verdict", "")).upper()
            agree = pinets.get("signal_agreement_pct")
            metric = f"{agree:.0f}% agree" if isinstance(agree, (int, float)) else verdict
            stages["pre_parity"] = _cell("done" if verdict == "PASS" else "fail", metric)
        row = _finalize_row(
            sid,
            spec.get("title") or sid,
            spec.get("symbol"),
            spec.get("timeframe"),
            spec.get("source_candidate"),
            stages,
            spec.get("fidelity_to_original_youtube_source", ""),
        )
        row["source_url"] = _youtube(spec.get("source_url"))
        row["description"] = _describe(sid, spec.get("title", ""), spec.get("source_candidate", ""))
        row["metrics"] = {"direction": spec.get("direction")}
        row["pinets_parity"] = pinets
        row["pinets_parity_proof"] = _pinets_proof(promoted_dir, spec_dir_name, pinets)
        row["equity_curve"] = _equity_curve(promoted_dir, spec_dir_name)
        row["paper_trade_detail"] = _paper_trade_detail(promoted_dir, spec_dir_name, plan_by_id.get(sid))
        row["directional_research"] = _directional_research(sid, spec.get("title") or sid, spec.get("direction"), spec)
        producer_spec = _producer_spec_detail(promoted_dir, spec_dir_name, spec)
        row["producer_spec"] = producer_spec
        row["producer_spec_path"] = producer_spec.get("path") if producer_spec else None
        row["producer_spec_summary"] = producer_spec.get("summary") if producer_spec else None
        row["producer_spec_source_url"] = producer_spec.get("source_url") if producer_spec else None
        row["producer_spec_next_action"] = producer_spec.get("next_action") if producer_spec else None
        row["producer_spec_param_grid"] = producer_spec.get("param_grid_size_planned") if producer_spec else None
        row["stg_code"] = resolve_stg_code(stg_map, sid, spec.get("source_candidate"), spec_dir_name)
        row["stg_number"] = _stg_number(row["stg_code"])
        row["scorecard"] = build_scorecard(row)
        row["score"] = row["scorecard"]["total"]
        row["score_band"] = row["scorecard"]["band"]
        row["next_action_hint"] = action_hint(row.get("next_action"))
        row["classification"] = {
            "kind": "candidate",
            "label": "candidate",
            "reason": "Promoted producer_spec row, not yet present in the canonical strategy registry.",
            "next_action": "Run PineTS parity",
        }
        rows.append(row)

    for c in candidates:
        cid = c.get("candidate_id") or c.get("id")
        if cid in promoted_origin_ids or cid in promoted_spec_ids:
            continue  # already represented by its promoted strategy row
        status_str = str(c.get("status", "")).upper()
        ev = c.get("evidence_level", "")
        stages = {}
        stages["discovered"] = _cell("done", c.get("timeframe", "") or c.get("market_type", ""))
        stages["classified"] = _classification_cell(
            status_str,
            ev,
            c.get("notes", ""),
            " ".join(str(value or "") for value in (c.get("name"), c.get("title"), c.get("summary"))),
            c.get("status", ""),
            c.get("source_url", ""),
        )
        classification_kind = stages["classified"]["metric"]
        if classification_kind in ("rejected", "wiki", "split_required", "source_audit"):
            stages["backtested"] = _cell("na", classification_kind)
            stages["promoted"] = _cell("na", "")
        else:
            backtested = ev in ("backtested", "prototyped") or status_str == "PROTOTYPED"
            stages["backtested"] = _cell("done" if backtested else "pending",
                                         "backtested" if backtested else "")
            stages["promoted"] = _cell("pending", "")
        stages["pre_parity"] = _cell("pending", "")
        stages["paper_trade"] = _cell("pending", "")
        stages["integrated"] = _cell("pending", "")
        row = _finalize_row(cid, c.get("name") or c.get("title") or cid,
                            None, c.get("timeframe"), None, stages, c.get("notes", ""))
        row["source_url"] = _youtube(c.get("source_url"))
        row["description"] = _describe(cid, c.get("name", ""), c.get("title", ""))
        row["metrics"] = {}
        row["pinets_parity"] = None
        row["pinets_parity_proof"] = None
        row["equity_curve"] = None
        row["paper_trade_detail"] = None
        row["directional_research"] = _directional_research(
            cid, c.get("name") or c.get("title") or cid, c.get("direction")
        )
        row["stg_code"] = resolve_stg_code(stg_map, cid, c.get("candidate_id"), c.get("origin_candidate"))
        row["stg_number"] = _stg_number(row["stg_code"])
        row["scorecard"] = build_scorecard(row)
        row["score"] = row["scorecard"]["total"]
        row["score_band"] = row["scorecard"]["band"]
        row["next_action_hint"] = action_hint(row.get("next_action"))
        row["classification"] = {
            "kind": classification_kind,
            "label": classification_kind,
            "reason": (
                "This row is a standalone candidate evidence record routed by the audit/classification layer."
                if classification_kind == "candidate"
                else "This row is parked by the classification layer before backtest."
                if classification_kind == "wiki"
                else "This row needs indicator-level splitting before any backtest; each open formula can become its own case."
                if classification_kind == "split_required"
                else "This row needs source/formula audit before it can become a backtest candidate."
                if classification_kind == "source_audit"
                else "This row is rejected by the classification layer and should not reach backtest."
                if classification_kind == "rejected"
                else "This row is awaiting a clearer routing decision."
            ),
            "next_action": (
                "Run backtest"
                if classification_kind == "candidate"
                else "Wiki/module branch ? park"
                if classification_kind == "wiki"
                else "Split into indicator cases ? then audit each formula"
                if classification_kind == "split_required"
                else "Resolve source/formula audit"
                if classification_kind == "source_audit"
                else "Rejected source ? source audit / park"
                if classification_kind == "rejected"
                else "Route to backtest or wiki/module branch"
            ),
        }
        rows.append(row)

    # --- Rows from broader QuantLens discovery ledgers not yet in canonical registry ---
    for c in _discover_extra_quantlens_candidates(mcc_root, represented_ids):
        cid = c.get("candidate_id") or c.get("id")
        status_str = str(c.get("status", "")).upper()
        stages = {}
        stages["discovered"] = _cell("done", "jsonl discovery")
        stages["classified"] = _classification_cell(
            status_str,
            c.get("status", ""),
            c.get("notes", ""),
            " ".join(str(value or "") for value in (c.get("name"), c.get("title"), c.get("summary"))),
            c.get("status", ""),
            c.get("source_url", ""),
        )
        classification_kind = stages["classified"]["metric"]
        if classification_kind in ("rejected", "wiki", "split_required", "source_audit"):
            stages["backtested"] = _cell("na", classification_kind)
            stages["promoted"] = _cell("na", "")
        else:
            stages["backtested"] = _cell("pending", "needs review")
            stages["promoted"] = _cell("pending", "")
        stages["pre_parity"] = _cell("pending", "")
        stages["paper_trade"] = _cell("pending", "")
        stages["integrated"] = _cell("pending", "")
        row = _finalize_row(cid, c.get("name") or c.get("title") or cid,
                            None, c.get("timeframe"), None, stages, c.get("notes", ""))
        row["source_url"] = _youtube(c.get("source_url"))
        row["description"] = _describe(cid, c.get("name", ""), c.get("title", ""))
        if row["description"] == _DEFAULT_DESC and c.get("summary"):
            row["description"] = {
                "family": "QuantLens discovery",
                "what": str(c.get("summary"))[:260],
                "entry": "Needs deterministic spec.",
                "exit": "Needs deterministic spec.",
            }
        row["metrics"] = {}
        row["pinets_parity"] = None
        row["pinets_parity_proof"] = None
        row["equity_curve"] = None
        row["paper_trade_detail"] = None
        row["directional_research"] = _directional_research(
            cid, c.get("name") or c.get("title") or cid, c.get("direction")
        )
        row["discovery_source"] = c.get("discovery_source") or c.get("relative_source_path") or ""
        row["classification"] = {
            "kind": classification_kind,
            "label": classification_kind,
            "reason": "Derived from broader discovery ledger evidence and status tokens.",
            "next_action": (
                "Rejected source ? source audit / park" if classification_kind == "rejected"
                else (
                    "Split into indicator cases ? then audit each formula"
                    if classification_kind == "split_required"
                    else (
                        "Resolve source/formula audit"
                        if classification_kind == "source_audit"
                        else ("Wiki/module branch ? park" if classification_kind == "wiki" else "Run backtest")
                    )
                )
            ),
        }
        rows.append(row)

    # summary: how many rows have reached each stage (status done)
    stage_counts = {k: sum(1 for r in rows if r["stages"][k]["status"] == "done") for k in ORDER}

    # sort: furthest-along first
    rows.sort(key=lambda r: (ORDER.index(r["current_stage_key"]) if r["current_stage_key"] else -1), reverse=True)

    return {
        "schema_version": "1.0",
        "mode": "read_only",
        "stages": STAGES,
        "summary": {
            "total_rows": len(rows),
            "stage_done_counts": stage_counts,
        },
        "rows": rows,
    }


def _stg_number(stg_code: str) -> int | None:
    if not stg_code:
        return None
    digits = "".join(ch for ch in str(stg_code) if ch.isdigit())
    if not digits:
        return None
    try:
        return int(digits)
    except Exception:
        return None


_NEXT_ACTION = {
    "discovered": "Write deterministic spec",
    "classified": "Route to backtest or wiki/module branch",
    "backtested": "Run walk-forward / OOS / alpha test",
    "promoted": "Build promotion packet",
    "pre_parity": "Run PineTS Pine=Python parity",
    "paper_trade": "Start forward paper-trade (collect new trades)",
    "integrated": "Integrate into MTC_v2.pine (feature-gated, default OFF)",
}


def _finalize_row(rid, name, symbol, tf, origin, stages, notes) -> dict:
    # current stage = furthest 'done'; next = first not-done (pending/active/fail)
    current_key = None
    for k in ORDER:
        if stages[k]["status"] == "done":
            current_key = k
    classification_metric = str((stages.get("classified") or {}).get("metric") or "").lower()
    # parked / dead-end: a 'na' core stage means the item is routed away from backtest
    if any(stages[k]["status"] == "na" for k in ("backtested", "promoted")):
        parked_action = "Salvage only ? needs source audit"
        if classification_metric in {"wiki", "module"}:
            parked_action = "Wiki/module branch ? park"
        elif classification_metric == "split_required":
            parked_action = "Split into indicator cases ? then audit each formula"
        elif classification_metric == "source_audit":
            parked_action = "Resolve source/formula audit"
        elif classification_metric == "rejected":
            parked_action = "Rejected source ? source audit / park"
        return {
            "id": rid, "name": name, "symbol": symbol or "", "timeframe": tf or "",
            "origin_candidate": origin or "", "stages": stages,
            "current_stage_key": current_key, "next_stage_key": None,
            "next_action": parked_action, "notes": notes or "",
        }
    next_key = None
    for k in ORDER:
        st = stages[k]["status"]
        if st in ("pending", "active", "fail"):
            next_key = k
            break
    next_action = _NEXT_ACTION.get(next_key, "—") if next_key else "All stages done"
    if next_key and stages[next_key]["status"] == "active":
        next_action = "Finish: " + next_action
    return {
        "id": rid,
        "name": name,
        "symbol": symbol or "",
        "timeframe": tf or "",
        "origin_candidate": origin or "",
        "stages": stages,
        "current_stage_key": current_key,
        "next_stage_key": next_key,
        "next_action": next_action,
        "notes": notes or "",
    }
