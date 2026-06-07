"""
generate_producer_specs.py
--------------------------
Auto-generates missing producer_spec.json files for STG023-063 strategies.

Rules (HARD):
  - NEVER fabricate metric numbers.
  - NEVER mark promotion unless MEGA data shows explicit PASS classification.
  - Signal definitions extracted verbatim from spec (1-2 lines max).
  - metrics_lockbox = placeholder dict when no MEGA sweep found.
"""

import json
import re
import glob
import os
from pathlib import Path

# ── paths ──────────────────────────────────────────────────────────────────────
STRATEGIES_DIR = Path(
    r"C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies"
)
BACKTEST_DIR = Path(
    r"C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS"
)

# ── known mapping: folder-name fragment → engine_strategy_id ──────────────────
# Populated from the MEGA results analysis.  STG035-045 use QL_2026-05-01_* ids.
# STG023-034 use the batch-specific QL_*_v1 ids.
FOLDER_TO_ENGINE_ID = {
    # STG023
    "STG023_01_kell_wedge_pop_crossback": "QL_KELL_BATCH_v1",
    # STG024
    "STG024_02_martin_luke_pullback_avwap": "QL_MARTIN_AVWAP_v1",
    # STG025
    "STG025_03_slingshot_4ema_high_pullback": "QL_SLINGSHOT_v1",
    # STG026
    "STG026_04_crabel_range_expansion_stage2": "QL_CRABEL_RANGE_EXP_v1",
    # STG027
    "STG027_05_bigbeluga_rsi_choch_atr": "QL_BIGBELUGA_RSI_v1",
    # STG028 – CANSLIM shakeout; no dedicated engine id found in MEGA files
    # STG029
    "STG029_07_linda_5sma_rs_pullback": "QL_LINDA_5SMA_v1",
    # STG035
    "STG035_ql_2026_05_01_any_1h_rsi_confluence_playbook": "QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK",
    # STG036
    "STG036_ql_2026_05_01_any_bollinger_bands_20_2_tri_setup": "QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP",
    # STG037
    "STG037_ql_2026_05_01_any_candlestick_7_pattern_pa_confluence": "QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE",
    # STG038
    "STG038_ql_2026_05_01_liquid_intraday_vwap_pullback_reversal": "QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL",
    # STG039
    "STG039_ql_2026_05_01_sp500_5m_two_candle_sentiment_sr": "QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR",
    # STG040
    "STG040_ql_2026_05_01_swing_1h_dual_rsi_60_40_pullback": "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK",
    # STG041
    "STG041_ql_2026_05_01_unknown_multi_ema_channel_pullback": "QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK",
    # STG042
    "STG042_ql_2026_05_01_us_equities_10m_8ema_pullback": "QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK",
    # STG043
    "STG043_ql_2026_05_01_us_equities_intraday_8ema_exit_trail": "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL",
    # STG044
    "STG044_ql_2026_05_01_us_equities_intraday_le_model_bull_flag": "QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG",
    # STG045
    "STG045_ql_2026_05_01_us_equities_intraday_purple_profits": "QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS",
    # STG056
    "STG056_oliver_kell_price_cycle": "QL_OLIVER_KELL_PRICE_CYCLE",
    # STG057
    "STG057_linda_raschke_lbr_toolkit": "QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION",
}

# Pass classifications that qualify for FORWARD_PAPER_CANDIDATE
PASS_CLASSIFICATIONS = {"PASS", "STRONG_PASS", "FORWARD_PAPER"}


# ── MEGA data loader ─────────────────────────────────────────────────────────
def load_all_mega_data() -> dict:
    """Return dict: engine_strategy_id -> best entry dict from any MEGA file.

    'Best' = prefer entries with classification not SKIPPED_RULE / INSUFFICIENT_TRADES,
    then prefer highest net_return_pct in lockbox_oos.

    The MEGA JSON results field is a list of row objects, each with keys:
    strategy, symbol, timeframe, classification, summary, bh_fdr_survivor, etc.
    """
    all_entries: dict[str, list[dict]] = {}

    mega_files = list(BACKTEST_DIR.rglob("MEGA_walk_forward_results.json"))

    for mega_path in mega_files:
        try:
            with open(mega_path, encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as e:
            print(f"  [WARN] Could not parse {mega_path}: {e}")
            continue

        results = data.get("results", [])
        # results is a list of row dicts
        if not isinstance(results, list):
            # Older format: dict of parallel lists — handle gracefully
            if isinstance(results, dict):
                strategies = results.get("strategy", [])
                n = len(strategies) if isinstance(strategies, list) else 0
                for i in range(n):
                    def _get(key, idx, _r=results):
                        lst = _r.get(key, [])
                        return lst[idx] if isinstance(lst, list) and idx < len(lst) else None
                    row = {
                        "strategy": strategies[i],
                        "symbol": _get("symbol", i),
                        "timeframe": _get("timeframe", i),
                        "classification": _get("classification", i),
                        "bh_fdr_survivor": _get("bh_fdr_survivor", i),
                        "dsr_p_value": _get("dsr_p_value", i),
                        "dsr_robust": _get("dsr_robust", i),
                        "robust_final": _get("robust_final", i),
                        "summary": _get("summary", i),
                        "_source_file": str(mega_path.relative_to(BACKTEST_DIR)),
                    }
                    all_entries.setdefault(strategies[i], []).append(row)
            continue

        for row in results:
            if not isinstance(row, dict):
                continue
            strat_id = row.get("strategy")
            if not strat_id:
                continue
            entry = {
                "strategy": strat_id,
                "symbol": row.get("symbol"),
                "timeframe": row.get("timeframe"),
                "classification": row.get("classification"),
                "bh_fdr_survivor": row.get("bh_fdr_survivor"),
                "dsr_p_value": row.get("dsr_p_value"),
                "dsr_robust": row.get("dsr_robust"),
                "robust_final": row.get("robust_final"),
                "summary": row.get("summary"),
                "_source_file": str(mega_path.relative_to(BACKTEST_DIR)),
            }
            all_entries.setdefault(strat_id, []).append(entry)

    # Pick best entry per strategy id
    best: dict[str, dict] = {}
    for strat_id, entries in all_entries.items():
        # Sort: prefer PASS-class, then highest net_return from lockbox_oos
        def sort_key(e):
            cls = e.get("classification", "") or ""
            is_pass = cls in PASS_CLASSIFICATIONS
            oos = (e.get("summary") or {})
            if isinstance(oos, dict):
                ret = oos.get("lockbox_oos", {})
                if isinstance(ret, dict):
                    net = ret.get("net_return_pct", 0) or 0
                else:
                    net = 0
            else:
                net = 0
            return (int(is_pass), net)

        best[strat_id] = max(entries, key=sort_key)

    return best


# ── spec parser ───────────────────────────────────────────────────────────────
_PLACEHOLDER_METRICS = {
    "status": "not_yet_evaluated",
    "source": "no_mega_sweep_completed",
}


def _first_nonempty(lines: list[str]) -> str:
    for ln in lines:
        s = ln.strip()
        if s:
            return s
    return ""


def _extract_universe_and_timeframe(md_text: str) -> tuple[str, str]:
    """Return (symbol_hint, timeframe_hint) from Universe section."""
    symbol = "MULTI_ASSET"
    timeframe = "unknown"

    # Look for Universe section
    universe_match = re.search(
        r"##\s+Universe\s*\n(.*?)(?=\n##|\Z)", md_text, re.DOTALL | re.IGNORECASE
    )
    if universe_match:
        block = universe_match.group(1)
        # Look for explicit symbols
        sym_candidates = re.findall(
            r"\b(BTC|ETH|SOL|BNB|XRP|ADA|LINK|LTC|SPY|QQQ|AAPL|SP500|BTCUSDT|ETHUSDT)\b",
            block,
            re.IGNORECASE,
        )
        if sym_candidates:
            symbol = sym_candidates[0].upper() + "USDT" if sym_candidates[0].upper() in {
                "BTC","ETH","SOL","BNB","XRP","ADA","LINK","LTC"
            } else sym_candidates[0].upper()

    # Look for timeframe mentions (1h, 4h, 1d, 5m, 15m, etc.)
    tf_matches = re.findall(
        r"\b(1[Dd]|4[Hh]|1[Hh]|5[Mm]|15[Mm]|30[Mm]|2[Hh]|1[Mm]|daily|intraday|1h|4h|1d|5m|15m|30m|2h)\b",
        md_text[:600],
    )
    if tf_matches:
        timeframe = tf_matches[0].lower()

    return symbol, timeframe


def _extract_direction(md_text: str) -> str:
    """Detect long_only, short_only, or long_short from spec text."""
    lower = md_text.lower()
    has_short = bool(
        re.search(r"\bshort.only\b|\bshort_only\b|\bshort entry\b|\bshort on\b", lower)
    )
    has_long = bool(
        re.search(r"\blong.only\b|\blong_only\b|\blong entry\b|\blong on\b", lower)
    )
    if has_short and not has_long:
        return "short_only"
    if has_short and has_long:
        return "long_short"
    return "long_only"


def _extract_signal_definition(md_text: str, direction: str) -> tuple[str | None, str | None]:
    """Return (long_signal_def, short_signal_def) as short 1-2 line strings.

    Extraction priority:
    1. Explicit `long_entry = ...` code in spec
    2. `**Entry**:` bold line
    3. `* **Entry**:` bullet
    4. First non-empty line of `## Entry` section
    """
    long_def = None
    short_def = None

    def _clean(s: str, max_len: int = 200) -> str:
        """Strip markdown code fences, collapse whitespace, cap length."""
        s = re.sub(r"```[a-z]*", "", s)   # strip code fence markers
        s = re.sub(r"\s+", " ", s).strip()
        return s[:max_len]

    # 1. Explicit long_entry = ... in a code block (take first occurrence)
    long_matches = re.findall(
        r"long_entry\s*=\s*(.+?)(?=\nshort_entry|\n###|\n##|\n```|\Z)",
        md_text,
        re.DOTALL,
    )
    if long_matches:
        long_def = _clean(long_matches[0])

    # 2. Bold **Entry**: line
    if not long_def:
        bold_entry = re.search(
            r"\*\*Entry[^*]*\*\*[:\s]*(.+)",
            md_text,
            re.IGNORECASE,
        )
        if bold_entry:
            long_def = _clean(bold_entry.group(1))

    # 3. Bullet entry: `* Entry:` or `- Entry:`
    if not long_def:
        bullet_entry = re.search(
            r"^[\*\-]\s+\*?Entry\*?[:\s]+(.+)",
            md_text,
            re.MULTILINE | re.IGNORECASE,
        )
        if bullet_entry:
            long_def = _clean(bullet_entry.group(1))

    # 4. Rules section: `* **Entry**: ...`
    if not long_def:
        rules_match = re.search(
            r"##\s+Rules.*?\n(.*?)(?=\n##|\Z)",
            md_text,
            re.DOTALL | re.IGNORECASE,
        )
        if rules_match:
            block = rules_match.group(1)
            entry_line = re.search(r"\*\*Entry\*\*[:\s]*(.+)", block, re.IGNORECASE)
            if entry_line:
                long_def = _clean(entry_line.group(1))

    # 5. First non-empty line of `## Entry` or `## Signal` section
    if not long_def:
        entry_match = re.search(
            r"##\s+(?:Entry|Signal|Long Entry|Signal definition)[^\n]*\n(.*?)(?=\n##|\Z)",
            md_text,
            re.DOTALL | re.IGNORECASE,
        )
        if entry_match:
            block = entry_match.group(1).strip()
            # Skip code fence lines
            for ln in block.split("\n"):
                cleaned = ln.strip().lstrip("`").lstrip("*").lstrip("-").strip()
                if cleaned and not cleaned.startswith("```"):
                    long_def = _clean(cleaned)
                    break

    # Short signal
    short_matches = re.findall(
        r"short_entry\s*=\s*(.+?)(?=\nlong_entry|\n###|\n##|\n```|\Z)",
        md_text,
        re.DOTALL,
    )
    if short_matches:
        short_def = _clean(short_matches[0])

    # If short_only direction, move long_def to short_def
    if direction == "short_only" and not short_def:
        short_def = long_def
        long_def = None

    return long_def, short_def


def _extract_stop_exit(md_text: str) -> tuple[str, str]:
    """Return (stop_rule, exit_rule) as short strings, skipping code-fence lines."""
    stop_rule = "see_spec"
    exit_rule = "see_spec"

    def _first_real_line(block: str) -> str:
        for ln in block.split("\n"):
            s = ln.strip()
            if s and not s.startswith("```") and s != "`":
                # Strip leading markdown noise
                s = re.sub(r"^[-*#`]+\s*", "", s).strip()
                if s:
                    return re.sub(r"\s+", " ", s)[:150]
        return ""

    stop_match = re.search(
        r"##\s+Stop.*?\n(.*?)(?=\n##|\Z)",
        md_text,
        re.DOTALL | re.IGNORECASE,
    )
    if stop_match:
        val = _first_real_line(stop_match.group(1).strip())
        if val:
            stop_rule = val

    target_match = re.search(
        r"##\s+(?:Target|Exit).*?\n(.*?)(?=\n##|\Z)",
        md_text,
        re.DOTALL | re.IGNORECASE,
    )
    if target_match:
        val = _first_real_line(target_match.group(1).strip())
        if val:
            exit_rule = val

    return stop_rule, exit_rule


def _extract_params(md_text: str) -> dict:
    """Extract key parameters from a markdown table or Best tested parameters block."""
    params: dict = {}

    # Look for markdown table: | Param | Default | (two-column)
    table_rows = re.findall(
        r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
        md_text,
    )
    for name_cell, val_cell in table_rows:
        name_cell = name_cell.strip()
        val_cell = val_cell.strip()
        # Skip header rows
        if re.match(r"^[-:]+$", val_cell) or name_cell.lower() in {"param", "parameter", "name", "---"}:
            continue
        if name_cell and val_cell:
            # Try to parse numeric
            try:
                params[name_cell] = float(val_cell) if "." in val_cell else int(val_cell)
            except (ValueError, TypeError):
                params[name_cell] = val_cell

    # Also look for JSON-style best params
    json_match = re.search(r"`(\{[^`]+\})`", md_text)
    if json_match and not params:
        try:
            params = json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    return params


def _extract_candidate_id_from_header(md_text: str, folder_name: str) -> str:
    """Extract candidate_id from spec header or derive from folder name.

    A valid candidate_id must:
      - Contain at least one underscore OR be all-caps with 4+ chars
      - Start with a letter
    """
    def _looks_like_id(s: str) -> bool:
        """Return True if s looks like a real strategy ID (not a bare number or common word)."""
        if not s:
            return False
        if re.match(r"^\d+$", s):
            return False  # pure number
        if len(s) < 4:
            return False
        if not re.match(r"^[A-Z]", s):
            return False
        if "_" not in s and len(s) < 8:
            return False  # too short without underscores
        return True

    # Pattern: # Deterministic Spec — ... (CANDIDATE_ID)  in first 400 chars
    paren_match = re.search(r"\(([A-Z][A-Z0-9_\-]{3,})\)", md_text[:400])
    if paren_match and _looks_like_id(paren_match.group(1)):
        return paren_match.group(1)

    # Pattern: candidate_id: SOME_ID  in first 600 chars
    id_match = re.search(r"candidate.id[:\s]+([A-Z][A-Z0-9_\-]+)", md_text[:600], re.IGNORECASE)
    if id_match:
        cid = id_match.group(1).upper()
        if _looks_like_id(cid):
            return cid

    # Derive from folder name: strip leading STGxxx_ and numeric prefix
    derived = re.sub(r"^STG\d+_\d*_?", "", folder_name).upper()
    derived = derived.replace("-", "_")
    return derived if derived else folder_name.upper()


def parse_metadata_yaml(yaml_path: Path) -> dict:
    """Very light YAML reader (no dependency on PyYAML) for the flat key:value format."""
    meta: dict = {}
    if not yaml_path.exists():
        return meta

    with open(yaml_path, encoding="utf-8") as fh:
        lines = fh.readlines()

    for line in lines:
        if ":" not in line or line.strip().startswith("#"):
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val and not val.startswith("{") and not val.startswith("["):
            meta[key] = val

    return meta


# ── MEGA metric extractor ─────────────────────────────────────────────────────
def build_metrics_lockbox(mega_entry: dict | None) -> tuple[dict, bool]:
    """Return (lockbox_dict, is_real).

    is_real=True means we have actual MEGA data (even if INSUFFICIENT/SKIPPED).
    Only set promotion to FORWARD_PAPER_CANDIDATE if classification is PASS-like.
    """
    if mega_entry is None:
        return _PLACEHOLDER_METRICS.copy(), False

    cls = mega_entry.get("classification") or "UNKNOWN"
    summary = mega_entry.get("summary") or {}
    oos = {}
    if isinstance(summary, dict):
        oos = summary.get("lockbox_oos") or {}

    lockbox: dict = {
        "classification": cls,
        "source_file": mega_entry.get("_source_file", "unknown"),
        "symbol": mega_entry.get("symbol"),
        "timeframe": mega_entry.get("timeframe"),
        "bh_fdr_survivor": mega_entry.get("bh_fdr_survivor"),
        "dsr_p_value": mega_entry.get("dsr_p_value"),
        "dsr_robust": mega_entry.get("dsr_robust"),
        "robust_final": mega_entry.get("robust_final"),
    }

    if isinstance(oos, dict) and oos:
        for k in [
            "num_trades", "win_rate", "net_return_pct", "net_after_slippage_pct",
            "max_drawdown_pct", "expectancy_R", "profit_factor",
            "sharpe", "annualized_sharpe", "annualized_sortino",
        ]:
            if k in oos:
                lockbox[k] = oos[k]

    # Attach best_params if available
    if isinstance(summary, dict) and "best_params" in summary:
        bp = summary["best_params"]
        if isinstance(bp, dict):
            lockbox["best_params"] = dict(bp)

    return lockbox, True


def promotion_status(cls: str | None, is_real: bool) -> list[str]:
    if not is_real:
        return ["RESEARCH_GRADE"]
    if cls and cls in PASS_CLASSIFICATIONS:
        return ["FORWARD_PAPER_CANDIDATE"]
    return ["RESEARCH_GRADE"]


# ── main loop ─────────────────────────────────────────────────────────────────
def main():
    import sys
    overwrite = "--overwrite" in sys.argv or "--force" in sys.argv

    print("Loading MEGA data from all sweep files …")
    mega_data = load_all_mega_data()
    print(f"  Loaded {len(mega_data)} unique engine strategy IDs from MEGA files.\n")

    # Find all strategy folders STG023+ that are missing producer_spec.json
    # (or all of them if --overwrite is given)
    strategy_folders = sorted(STRATEGIES_DIR.iterdir())
    missing_folders = []
    for folder in strategy_folders:
        if not folder.is_dir():
            continue
        m = re.match(r"^STG(\d+)", folder.name)
        if not m:
            continue
        stg_num = int(m.group(1))
        if stg_num < 23:
            continue
        spec_path = folder / "producer_spec.json"
        if spec_path.exists() and not overwrite:
            continue
        missing_folders.append(folder)

    print(f"Found {len(missing_folders)} folders missing producer_spec.json:\n")

    wrote = 0
    errors = 0

    for folder in missing_folders:
        folder_name = folder.name

        # 1. Read 07_deterministic_spec.md
        spec_md_path = folder / "07_deterministic_spec.md"
        if not spec_md_path.exists():
            print(f"  SKIP {folder_name} — no 07_deterministic_spec.md")
            errors += 1
            continue

        with open(spec_md_path, encoding="utf-8") as fh:
            md_text = fh.read()

        # 2. Read 01_candidate_metadata.yaml if present
        meta = parse_metadata_yaml(folder / "01_candidate_metadata.yaml")

        # 3. Derive fields from spec
        candidate_id = _extract_candidate_id_from_header(md_text, folder_name)
        symbol, timeframe = _extract_universe_and_timeframe(md_text)
        direction = _extract_direction(md_text)
        long_sig, short_sig = _extract_signal_definition(md_text, direction)
        stop_rule, exit_rule = _extract_stop_exit(md_text)
        params = _extract_params(md_text)

        # Override symbol/timeframe from metadata if available
        if meta.get("primary_timeframe"):
            timeframe = meta["primary_timeframe"]
        if meta.get("market_type") and meta["market_type"] not in {"ANY_CLAIMED_UNVALIDATED", "UNKNOWN"}:
            symbol = meta["market_type"]

        # direction override from metadata
        if meta.get("long_only_or_long_short"):
            raw_dir = meta["long_only_or_long_short"].lower()
            if "short_only" in raw_dir:
                direction = "short_only"
            elif "long_short" in raw_dir or "both" in raw_dir:
                direction = "long_short"
            else:
                direction = "long_only"

        # strategy_family
        strategy_family = meta.get("strategy_type", "RESEARCH_GRADE_SPEC").upper().replace(" ", "_").replace("-", "_")
        if not strategy_family:
            strategy_family = "RESEARCH_GRADE_SPEC"

        # known_strengths / known_weaknesses from metadata (prefer last-set A1 Extracted)
        known_strengths = meta.get("known_strengths", "N_A")
        known_weaknesses = meta.get("known_weaknesses", "N_A")

        # 4. MEGA data lookup
        engine_id = FOLDER_TO_ENGINE_ID.get(folder_name)
        mega_entry = mega_data.get(engine_id) if engine_id else None
        lockbox, is_real = build_metrics_lockbox(mega_entry)
        cls = lockbox.get("classification") if is_real else None
        promo = promotion_status(cls, is_real)

        # 5. Build the spec dict
        spec = {
            "candidate_id": candidate_id,
            "strategy_family": strategy_family,
            "engine_strategy_id": engine_id,
            "symbol": symbol,
            "timeframe": timeframe,
            "direction": direction,
            "verified_parameters": params,
            "long_signal_definition": long_sig,
            "short_signal_definition": short_sig,
            "stop_rule": stop_rule,
            "exit_rule": exit_rule,
            "metrics_lockbox": lockbox,
            "promotion_status": promo,
            "not_an_approved_live_trading_system": True,
            "source_artifacts": ["07_deterministic_spec.md"],
            "known_strengths": known_strengths,
            "known_weaknesses": known_weaknesses,
        }

        # 6. Write
        out_path = folder / "producer_spec.json"
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(spec, fh, indent=2, ensure_ascii=False)

        metrics_tag = "real" if is_real else "placeholder"
        print(f"WROTE {folder_name} (metrics: {metrics_tag})")
        if engine_id:
            print(f"      engine_id={engine_id}  classification={cls}")
        wrote += 1

    print(f"\n{'='*60}")
    print(f"Done. Wrote {wrote} producer_spec.json files. Errors: {errors}.")


if __name__ == "__main__":
    main()
