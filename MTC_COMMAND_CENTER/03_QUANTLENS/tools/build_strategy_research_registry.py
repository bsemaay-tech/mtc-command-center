#!/usr/bin/env python3
"""Build the Strategy Research Lab registries from existing per-strategy data.

Single source of truth: each strategy folder under
``03_QUANTLENS/strategies/STGxxx`` (its ``producer_spec.json`` /
``01_candidate_metadata.yaml`` / ``README.md`` + folder slug). This script reads
those, applies *heuristic* research-taxonomy classification, and (re)generates
four machine-readable registries under ``05_REGISTRY/``:

    STRATEGY_RESEARCH_REGISTRY.json   taxonomy index for every strategy
    INDICATOR_REGISTRY.json           indicators referenced across strategies
    COMPONENT_REGISTRY.json           reusable components grouped by type
    TAG_DICTIONARY.json               controlled vocabulary + harvested tags

Uncertain heuristic fields are set to the literal string ``review_needed`` so a
future agent (or human) can find and confirm them. The script is idempotent:
re-running after editing a per-strategy file refreshes the registries.

This script NEVER touches MTC_V2.pine or any production trading logic.

Usage:
    python 03_QUANTLENS/tools/build_strategy_research_registry.py [--check]

``--check`` exits non-zero if the on-disk registries differ from a fresh build
(useful in CI / pre-commit) without writing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - yaml is expected to be present
    yaml = None

REVIEW = "review_needed"

# Repo layout: this file lives at 03_QUANTLENS/tools/<here>.
QUANTLENS_ROOT = Path(__file__).resolve().parents[1]
MCC_ROOT = QUANTLENS_ROOT.parent
STRATEGIES_DIR = QUANTLENS_ROOT / "strategies"
REGISTRY_DIR = MCC_ROOT / "05_REGISTRY"

# ---------------------------------------------------------------------------
# Controlled vocabulary (mirrors 06_SCHEMAS enums and the research prompt).
# ---------------------------------------------------------------------------
STRATEGY_CATEGORIES = [
    "scalping",
    "day_trading",
    "swing_trading",
    "position_trading",
    "multi_timeframe",
    "portfolio_strategy",
    "experimental",
    "unknown",
]
METHODS = [
    "trend_following",
    "pullback_continuation",
    "breakout",
    "mean_reversion",
    "reversal",
    "momentum",
    "volatility_expansion",
    "support_resistance",
    "range_trading",
    "hybrid",
    "unknown",
]
MARKET_REGIMES = [
    "trending",
    "ranging",
    "reversal",
    "breakout",
    "high_volatility",
    "low_volatility",
    "choppy",
    "bull_market",
    "bear_market",
    "sideways_market",
    "unknown",
]
COMPONENT_TYPES = [
    "entry_signal",
    "confirmation_filter",
    "trend_filter",
    "volatility_filter",
    "regime_filter",
    "htf_filter",
    "exit_signal",
    "stop_loss_module",
    "take_profit_module",
    "trailing_module",
    "position_sizing_module",
    "portfolio_allocation_module",
    "risk_filter",
]

# slug/keyword -> canonical indicator id
INDICATOR_KEYWORDS: dict[str, str] = {
    "rsi": "RSI",
    "dual_rsi": "RSI",
    "ema": "EMA",
    "8ema": "EMA",
    "4ema": "EMA",
    "multi_ema": "EMA",
    "ema20": "EMA",
    "ema50": "EMA",
    "20ema": "EMA",
    "sma": "SMA",
    "5sma": "SMA",
    "50sma": "SMA",
    "153": "SMA",
    "259": "SMA",
    "20ma": "SMA",
    "ma": "SMA",
    "atr": "ATR",
    "bollinger": "BOLLINGER_BANDS",
    "bb": "BOLLINGER_BANDS",
    "vwap": "VWAP",
    "avwap": "AVWAP",
    "macd": "MACD",
    "volume": "VOLUME",
    "choch": "MARKET_STRUCTURE",
    "fib": "FIBONACCI",
    "fibonacci": "FIBONACCI",
    "sr": "SUPPORT_RESISTANCE",
    "support": "SUPPORT_RESISTANCE",
    "resistance": "SUPPORT_RESISTANCE",
    "two_candle_sr": "SUPPORT_RESISTANCE",
    "vcp": "VCP",
    "qqe": "QQE",
    "candle": "CANDLESTICK",
    "candlestick": "CANDLESTICK",
    "channel": "PRICE_CHANNEL",
    "or": "OPENING_RANGE",
    "opening": "OPENING_RANGE",
    "openingbar": "OPENING_RANGE",
    "range_expansion": "VOLATILITY_RANGE",
    "wedge": "CHART_PATTERN",
    "flag": "CHART_PATTERN",
    "divergence": "DIVERGENCE",
    "rs": "RELATIVE_STRENGTH",
    "highest_volume": "VOLUME",
    "gap": "GAP",
    "extension": "PRICE_EXTENSION",
}

# Known curated indicator metadata (defaults; per-strategy notes override usage).
INDICATOR_LIBRARY: dict[str, dict[str, Any]] = {
    "RSI": dict(
        category="momentum_oscillator",
        primary_use="momentum / overbought-oversold",
        entry=True,
        confirm=True,
        regime=False,
        exit=True,
        stop=False,
        repaint="low",
        lookahead="low",
        tags=["rsi", "momentum", "oscillator"],
    ),
    "EMA": dict(
        category="moving_average",
        primary_use="trend direction / dynamic SR",
        entry=True,
        confirm=True,
        regime=True,
        exit=True,
        stop=True,
        repaint="low",
        lookahead="low",
        tags=["ema", "trend", "moving_average"],
    ),
    "SMA": dict(
        category="moving_average",
        primary_use="trend direction / mean",
        entry=True,
        confirm=True,
        regime=True,
        exit=True,
        stop=True,
        repaint="low",
        lookahead="low",
        tags=["sma", "trend", "moving_average"],
    ),
    "ATR": dict(
        category="volatility",
        primary_use="volatility sizing / stops / targets",
        entry=False,
        confirm=False,
        regime=True,
        exit=True,
        stop=True,
        repaint="low",
        lookahead="low",
        tags=["atr", "volatility", "stop"],
    ),
    "BOLLINGER_BANDS": dict(
        category="volatility_band",
        primary_use="volatility band / mean reversion",
        entry=True,
        confirm=True,
        regime=True,
        exit=True,
        stop=False,
        repaint="low",
        lookahead="low",
        tags=["bollinger", "volatility", "mean_reversion"],
    ),
    "VWAP": dict(
        category="volume_weighted_price",
        primary_use="intraday fair value / pullback anchor",
        entry=True,
        confirm=True,
        regime=False,
        exit=True,
        stop=False,
        repaint="medium",
        lookahead="low",
        tags=["vwap", "intraday", "volume"],
    ),
    "AVWAP": dict(
        category="anchored_volume_weighted_price",
        primary_use="anchored fair value from event",
        entry=True,
        confirm=True,
        regime=False,
        exit=True,
        stop=False,
        repaint="medium",
        lookahead="low",
        tags=["avwap", "anchored", "volume"],
    ),
    "MACD": dict(
        category="momentum_oscillator",
        primary_use="momentum / trend confirmation",
        entry=True,
        confirm=True,
        regime=False,
        exit=True,
        stop=False,
        repaint="low",
        lookahead="low",
        tags=["macd", "momentum"],
    ),
    "VOLUME": dict(
        category="volume",
        primary_use="participation / breakout confirmation",
        entry=False,
        confirm=True,
        regime=True,
        exit=False,
        stop=False,
        repaint="low",
        lookahead="low",
        tags=["volume", "confirmation"],
    ),
    "MARKET_STRUCTURE": dict(
        category="price_structure",
        primary_use="change of character / structure shift",
        entry=True,
        confirm=True,
        regime=True,
        exit=True,
        stop=True,
        repaint="high",
        lookahead="medium",
        tags=["choch", "structure", "smc"],
    ),
    "FIBONACCI": dict(
        category="price_level",
        primary_use="retracement / confluence level",
        entry=False,
        confirm=True,
        regime=False,
        exit=True,
        stop=True,
        repaint="medium",
        lookahead="low",
        tags=["fibonacci", "confluence", "level"],
    ),
    "SUPPORT_RESISTANCE": dict(
        category="price_level",
        primary_use="horizontal level / breakout anchor",
        entry=True,
        confirm=True,
        regime=False,
        exit=True,
        stop=True,
        repaint="medium",
        lookahead="low",
        tags=["sr", "level", "breakout"],
    ),
    "VCP": dict(
        category="chart_pattern",
        primary_use="volatility contraction breakout setup",
        entry=True,
        confirm=True,
        regime=True,
        exit=False,
        stop=True,
        repaint="medium",
        lookahead="medium",
        tags=["vcp", "contraction", "breakout"],
    ),
    "QQE": dict(
        category="momentum_oscillator",
        primary_use="smoothed RSI momentum signal",
        entry=True,
        confirm=True,
        regime=False,
        exit=True,
        stop=False,
        repaint="medium",
        lookahead="low",
        tags=["qqe", "momentum", "rsi"],
    ),
    "CANDLESTICK": dict(
        category="price_action",
        primary_use="reversal / continuation pattern",
        entry=True,
        confirm=True,
        regime=False,
        exit=False,
        stop=False,
        repaint="low",
        lookahead="low",
        tags=["candlestick", "price_action"],
    ),
    "PRICE_CHANNEL": dict(
        category="price_channel",
        primary_use="channel breakout / pullback",
        entry=True,
        confirm=True,
        regime=True,
        exit=True,
        stop=True,
        repaint="low",
        lookahead="low",
        tags=["channel", "breakout"],
    ),
    "OPENING_RANGE": dict(
        category="session_level",
        primary_use="opening range breakout / fade",
        entry=True,
        confirm=True,
        regime=False,
        exit=True,
        stop=True,
        repaint="medium",
        lookahead="low",
        tags=["opening_range", "intraday", "session"],
    ),
    "VOLATILITY_RANGE": dict(
        category="volatility",
        primary_use="range expansion (Crabel-style)",
        entry=True,
        confirm=True,
        regime=True,
        exit=False,
        stop=True,
        repaint="low",
        lookahead="low",
        tags=["range_expansion", "volatility"],
    ),
    "CHART_PATTERN": dict(
        category="chart_pattern",
        primary_use="wedge / flag / structure pattern",
        entry=True,
        confirm=True,
        regime=False,
        exit=False,
        stop=True,
        repaint="high",
        lookahead="medium",
        tags=["pattern", "price_action"],
    ),
    "DIVERGENCE": dict(
        category="momentum_divergence",
        primary_use="momentum/price divergence reversal",
        entry=True,
        confirm=True,
        regime=False,
        exit=False,
        stop=False,
        repaint="high",
        lookahead="medium",
        tags=["divergence", "reversal"],
    ),
    "RELATIVE_STRENGTH": dict(
        category="relative_strength",
        primary_use="leadership vs benchmark filter",
        entry=False,
        confirm=True,
        regime=True,
        exit=False,
        stop=False,
        repaint="low",
        lookahead="low",
        tags=["rs", "relative_strength", "filter"],
    ),
    "GAP": dict(
        category="event_price",
        primary_use="gap up/down event entry",
        entry=True,
        confirm=True,
        regime=False,
        exit=False,
        stop=True,
        repaint="low",
        lookahead="low",
        tags=["gap", "event"],
    ),
    "PRICE_EXTENSION": dict(
        category="price_extension",
        primary_use="overextension anti-chase filter",
        entry=False,
        confirm=False,
        regime=False,
        exit=True,
        stop=False,
        repaint="low",
        lookahead="low",
        tags=["extension", "filter"],
    ),
}

METHOD_KEYWORDS: list[tuple[str, str]] = [
    ("pullback", "pullback_continuation"),
    ("crossback", "reversal"),
    ("snapback", "reversal"),
    ("reversal", "reversal"),
    ("choch", "reversal"),
    ("divergence", "reversal"),
    ("breakout", "breakout"),
    ("gap", "breakout"),
    ("pop", "breakout"),
    ("opening_range", "breakout"),
    ("openingbar", "breakout"),
    ("range_expansion", "volatility_expansion"),
    ("vcp", "volatility_expansion"),
    ("oversold", "mean_reversion"),
    ("snap", "mean_reversion"),
    ("two_candle_sr", "support_resistance"),
    ("sr", "support_resistance"),
    ("ema", "trend_following"),
    ("sma", "trend_following"),
    ("8ema", "trend_following"),
    ("trail", "trend_following"),
    ("trend", "trend_following"),
    ("confluence", "hybrid"),
    ("multi", "hybrid"),
    ("playbook", "hybrid"),
    ("rs", "momentum"),
    ("momentum", "momentum"),
]


def _slug_tokens(folder_name: str) -> list[str]:
    # Drop the STGxxx prefix and any numeric ordinal, keep word tokens.
    name = re.sub(r"^STG\d+_", "", folder_name)
    name = re.sub(r"^\d+_", "", name)
    return [t for t in re.split(r"[_\-\s]+", name.lower()) if t]


def _load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def _classify_category(timeframe: str, tokens: list[str]) -> str:
    tf = (timeframe or "").lower()
    blob = " ".join(tokens)
    if any(t in blob for t in ("scalp",)):
        return "scalping"
    if any(
        t in blob for t in ("intraday", "opening", "or", "openingbar", "5m", "5pct")
    ) or tf in {"1m", "3m", "5m", "10m", "15m"}:
        return "day_trading"
    if tf in {"30m", "1h", "2h", "4h"}:
        return "swing_trading"
    if tf in {"1d", "d", "daily"}:
        return "swing_trading"
    return REVIEW


def _classify_method(signal_text: str) -> list[str]:
    blob = signal_text.lower()
    found: list[str] = []
    for kw, method in METHOD_KEYWORDS:
        if re.search(rf"\b{re.escape(kw)}\b", blob) and method not in found:
            found.append(method)
    return found or [REVIEW]


def _method_to_regime(methods: list[str]) -> list[str]:
    mapping = {
        "trend_following": "trending",
        "pullback_continuation": "trending",
        "breakout": "breakout",
        "volatility_expansion": "high_volatility",
        "mean_reversion": "ranging",
        "reversal": "reversal",
        "support_resistance": "ranging",
        "range_trading": "ranging",
        "momentum": "trending",
    }
    regimes = [mapping[m] for m in methods if m in mapping]
    return sorted(set(regimes)) or [REVIEW]


def _detect_indicators(signal_text: str) -> list[str]:
    blob = signal_text.lower()
    found: list[str] = []
    for kw, ind in INDICATOR_KEYWORDS.items():
        if re.search(rf"\b{re.escape(kw)}\b", blob) and ind not in found:
            found.append(ind)
    return found


def build_strategy_entry(folder: Path) -> dict[str, Any]:
    name = folder.name
    tokens = _slug_tokens(name)
    spec = _load_json(folder / "producer_spec.json")
    meta = _load_yaml(folder / "01_candidate_metadata.yaml")
    readme = _read_text(folder / "README.md")
    # Focused signal text: folder slug + curated descriptive fields only.
    # Scanning the whole JSON produced false positives (e.g. "OR" inside an
    # exit rule, "rs" inside other words), so keep the surface narrow.
    signal_text = " ".join(
        tokens
        + [
            str(spec.get("strategy_family") or ""),
            str(spec.get("long_signal_definition") or ""),
            str(spec.get("short_signal_definition") or ""),
            str(meta.get("strategy_type") or ""),
            str(meta.get("video_title") or ""),
            readme.splitlines()[0] if readme.strip() else "",
        ]
    )

    rel_folder = folder.relative_to(MCC_ROOT).as_posix()
    source_file = REVIEW
    for cand in (
        "producer_spec.json",
        "01_candidate_metadata.yaml",
        "07_deterministic_spec.md",
        "README.md",
    ):
        if (folder / cand).exists():
            source_file = f"{rel_folder}/{cand}"
            break

    timeframe = spec.get("timeframe") or meta.get("primary_timeframe") or ""
    direction = spec.get("direction") or meta.get("long_only_or_long_short") or ""
    long_short = (
        "long_only"
        if "long" in str(direction).lower() and "short" not in str(direction).lower()
        else ("long_short" if "short" in str(direction).lower() else REVIEW)
    )

    indicators = _detect_indicators(signal_text)
    methods = _classify_method(signal_text)
    category = _classify_category(timeframe, tokens)
    regimes = _method_to_regime(methods)

    # Status / maturity from available evidence.
    if spec.get("promotion_status"):
        maturity = "promoted_candidate"
        status = (
            "|".join(spec["promotion_status"])
            if isinstance(spec["promotion_status"], list)
            else str(spec["promotion_status"])
        )
    elif meta:
        maturity = "triaged_candidate"
        status = str(
            meta.get("codex_status") or meta.get("quantlens_decision") or "TRIAGED"
        )
    else:
        maturity = "research_batch_only"
        status = "RESEARCH_BATCH"

    tags = sorted(
        set(
            [t for t in tokens if len(t) > 1 and not t.isdigit()]
            + [ind.lower() for ind in indicators]
            + ([timeframe.lower()] if timeframe else [])
        )
    )

    entry: dict[str, Any] = {
        "strategy_id": name.split("_", 1)[0],
        "strategy_name": name,
        "source_file": source_file,
        "source_folder": rel_folder,
        "current_status": status,
        "maturity_level": maturity,
        "original_timeframe": timeframe or REVIEW,
        "recommended_timeframes": [timeframe] if timeframe else REVIEW,
        "original_asset_class": spec.get("symbol") or meta.get("market_type") or REVIEW,
        "tested_assets_if_known": [spec["symbol"]] if spec.get("symbol") else REVIEW,
        "long_only_or_long_short": long_short,
        "strategy_category": category,
        "expected_market_regime": regimes,
        "method": methods,
        "entry_logic_summary": spec.get("long_signal_definition")
        or spec.get("entry_rule")
        or REVIEW,
        "exit_logic_summary": spec.get("exit_rule") or REVIEW,
        "stop_loss_logic": spec.get("stop_rule") or REVIEW,
        "take_profit_logic": (
            f"target_R={spec['verified_parameters'].get('target_R')}"
            if isinstance(spec.get("verified_parameters"), dict)
            and spec["verified_parameters"].get("target_R")
            else REVIEW
        ),
        "trailing_logic": spec.get("trailing_logic") or REVIEW,
        "filters_used": spec.get("filters_used") or REVIEW,
        "indicators_used": indicators or REVIEW,
        "htf_usage": REVIEW,
        "repaint_risk_notes": spec.get("no_repaint")
        or meta.get("repaint_risk")
        or REVIEW,
        "lookahead_risk_notes": spec.get("no_lookahead")
        or meta.get("lookahead_risk")
        or REVIEW,
        "data_leakage_risk_notes": REVIEW,
        "tradingview_compatibility_notes": spec.get(
            "fidelity_to_original_youtube_source"
        )
        or REVIEW,
        "backtest_engine_compatibility_notes": (
            "bar_close_only" if spec.get("bar_close_only") else REVIEW
        ),
        "known_strengths": REVIEW,
        "known_weaknesses": (spec.get("metrics_lockbox", {}) or {}).get(
            "caveat", REVIEW
        )
        if isinstance(spec.get("metrics_lockbox"), dict)
        else REVIEW,
        "reusable_components": indicators or REVIEW,
        "suitable_for_combination_with": REVIEW,
        "unsuitable_for_combination_with": REVIEW,
        "tags": tags,
        "classification_confidence": "heuristic_auto",
    }

    # Prefer explicit, human-authored taxonomy from candidate_metadata.yaml over
    # heuristics (set during re-triage / manual classification review).
    explicit = {
        "strategy_category": meta.get("strategy_category"),
        "method": meta.get("method"),
        "expected_market_regime": meta.get("expected_market_regime"),
        "long_only_or_long_short": meta.get("long_only_or_long_short"),
        "indicators_used": meta.get("indicators_used"),
        "recommended_timeframes": meta.get("recommended_timeframes"),
        "trailing_logic": meta.get("trailing_logic"),
        "filters_used": meta.get("filters_used"),
        "known_strengths": meta.get("known_strengths"),
        "known_weaknesses": meta.get("known_weaknesses"),
    }
    overridden = False
    for key, value in explicit.items():
        if value not in (None, "", []):
            entry[key] = value
            if key in (
                "strategy_category",
                "method",
                "expected_market_regime",
                "long_only_or_long_short",
                "indicators_used",
            ):
                overridden = True
    if overridden:
        entry["classification_confidence"] = "explicit_metadata"
        if isinstance(entry.get("indicators_used"), list):
            entry["reusable_components"] = entry["indicators_used"]
            entry["tags"] = sorted(
                set(entry["tags"]) | {i.lower() for i in entry["indicators_used"]}
            )
    return entry


def build_registries() -> dict[str, dict[str, Any]]:
    now = datetime.now(timezone.utc).isoformat()
    strategies: list[dict[str, Any]] = []
    if STRATEGIES_DIR.exists():
        for folder in sorted(STRATEGIES_DIR.iterdir()):
            if folder.is_dir() and folder.name.upper().startswith("STG"):
                strategies.append(build_strategy_entry(folder))

    # Indicator registry: union of indicators referenced by strategies.
    used: dict[str, list[str]] = {}
    for s in strategies:
        inds = s["indicators_used"]
        if isinstance(inds, list):
            for ind in inds:
                used.setdefault(ind, []).append(s["strategy_id"])

    indicators = []
    for ind_id in sorted(set(list(used) + list(INDICATOR_LIBRARY))):
        lib = INDICATOR_LIBRARY.get(ind_id, {})
        indicators.append(
            {
                "indicator_id": ind_id,
                "indicator_name": ind_id.replace("_", " ").title(),
                "source_file": REVIEW,
                "source_folder": REVIEW,
                "indicator_category": lib.get("category", REVIEW),
                "calculation_type": REVIEW,
                "primary_use": lib.get("primary_use", REVIEW),
                "usable_as_entry_signal": lib.get("entry", REVIEW),
                "usable_as_confirmation_filter": lib.get("confirm", REVIEW),
                "usable_as_regime_filter": lib.get("regime", REVIEW),
                "usable_as_exit_signal": lib.get("exit", REVIEW),
                "usable_as_stop_or_trailing_component": lib.get("stop", REVIEW),
                "repaint_risk_notes": lib.get("repaint", REVIEW),
                "lookahead_risk_notes": lib.get("lookahead", REVIEW),
                "htf_usage": REVIEW,
                "parameters": REVIEW,
                "strategy_dependencies": sorted(set(used.get(ind_id, []))),
                "reusable_components": REVIEW,
                "tags": lib.get("tags", [ind_id.lower()]),
            }
        )

    # Component registry: derive reusable components by type from indicators.
    components = []
    for ind in indicators:
        ind_id = ind["indicator_id"]
        for flag, ctype in (
            ("usable_as_entry_signal", "entry_signal"),
            ("usable_as_confirmation_filter", "confirmation_filter"),
            ("usable_as_regime_filter", "regime_filter"),
            ("usable_as_exit_signal", "exit_signal"),
            ("usable_as_stop_or_trailing_component", "trailing_module"),
        ):
            if ind.get(flag) is True:
                components.append(
                    {
                        "component_id": f"{ind_id}_{ctype}",
                        "component_type": ctype,
                        "based_on_indicator": ind_id,
                        "description": f"{ind['indicator_name']} used as {ctype.replace('_', ' ')}",
                        "used_by_strategies": ind["strategy_dependencies"],
                        "repaint_risk_notes": ind["repaint_risk_notes"],
                        "lookahead_risk_notes": ind["lookahead_risk_notes"],
                        "tags": ind["tags"],
                    }
                )
    # ATR/sizing structural modules not tied to a single indicator.
    components.append(
        {
            "component_id": "ATR_stop_loss_module",
            "component_type": "stop_loss_module",
            "based_on_indicator": "ATR",
            "description": "ATR-multiple stop placement",
            "used_by_strategies": used.get("ATR", []),
            "repaint_risk_notes": "low",
            "lookahead_risk_notes": "low",
            "tags": ["atr", "stop"],
        }
    )
    components.append(
        {
            "component_id": "fixed_R_take_profit_module",
            "component_type": "take_profit_module",
            "based_on_indicator": REVIEW,
            "description": "Fixed R-multiple target (e.g. 2R)",
            "used_by_strategies": REVIEW,
            "repaint_risk_notes": "low",
            "lookahead_risk_notes": "low",
            "tags": ["fixed_r", "target"],
        }
    )

    # Tag dictionary: controlled vocab + harvested free tags.
    harvested: set[str] = set()
    for s in strategies:
        harvested.update(t for t in s["tags"] if isinstance(t, str))

    tag_dictionary = {
        "strategy_category": STRATEGY_CATEGORIES,
        "method": METHODS,
        "market_regime": MARKET_REGIMES,
        "component_type": COMPONENT_TYPES,
        "harvested_tags": sorted(harvested),
    }

    return {
        "STRATEGY_RESEARCH_REGISTRY.json": {
            "schema_version": "1.0",
            "generated_at": now,
            "generator": "build_strategy_research_registry.py",
            "strategies": strategies,
        },
        "INDICATOR_REGISTRY.json": {
            "schema_version": "1.0",
            "generated_at": now,
            "generator": "build_strategy_research_registry.py",
            "indicators": indicators,
        },
        "COMPONENT_REGISTRY.json": {
            "schema_version": "1.0",
            "generated_at": now,
            "generator": "build_strategy_research_registry.py",
            "components": components,
        },
        "TAG_DICTIONARY.json": {
            "schema_version": "1.0",
            "generated_at": now,
            "generator": "build_strategy_research_registry.py",
            "tags": tag_dictionary,
        },
    }


def _dump(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if on-disk registries differ; do not write",
    )
    args = parser.parse_args(argv)

    registries = build_registries()
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)

    drift = False
    for filename, payload in registries.items():
        target = REGISTRY_DIR / filename
        new_text = _dump(payload)
        # generated_at always changes; compare ignoring it for --check.
        if args.check:
            old = target.read_text(encoding="utf-8") if target.exists() else ""
            if _strip_generated_at(old) != _strip_generated_at(new_text):
                print(f"DRIFT: {filename} differs from fresh build")
                drift = True
            continue
        target.write_text(new_text, encoding="utf-8")
        s = (
            payload.get("strategies")
            or payload.get("indicators")
            or payload.get("components")
            or payload.get("tags")
        )
        count = len(s) if isinstance(s, (list, dict)) else 0
        print(f"wrote {filename} ({count} entries)")

    if args.check:
        return 1 if drift else 0
    return 0


def _strip_generated_at(text: str) -> str:
    return re.sub(r'"generated_at":\s*"[^"]*"', '"generated_at": "X"', text)


if __name__ == "__main__":
    raise SystemExit(main())
