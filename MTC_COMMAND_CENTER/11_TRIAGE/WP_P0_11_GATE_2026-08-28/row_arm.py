from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import site
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable


GATE_VERSION = "P011-LC-GATE-v2"
SOURCE_COMMIT = "5c5603065c994d545c0eaa8c137fa9edd5cdfc28"
A_TREE_OID = "7aa6f867d821df08a00358adf2dd4400b9c719e8"
LEGACY_MANIFEST_SHA256 = "1bc01646e9a00a4ee62c22c6ce1416ed03648e97351e792ae82bbbaff95f52d7"
MERGED_MASTER_COMMIT = "85c3e17f97efa1ba83ef9c679de319a50ad3be04"
P009_BLOB_OID = "1c39ab939dfcf5589e5ec8fba4af8966947a67fc"
P009_SHA256 = "7d48871a3e45dab118e97969d701912edb5d7c16a4d822d816beca1d03a42249"
CONTROLLER_REF = "legacy/pine-controller/2026-08-25"
CONTROLLER_COMMIT = "77a10e6573d93f8aaf777010ea507bbec0a7668b"
CONTROLLER_TREE_OID = "a14d071e3a6ee93735d6c2fc458f16b9f8d19a22"
B_REF = "legacy/02-mtc-backtest/2026-08-25"
B_COMMIT = "b5ed1afadcff09b69e36b72affeb23de51d84c14"
B_TREE_OID = "e8c4f06ba0fc74ce03f195fd946004ae9b458b37"

GATE_DIR = Path(__file__).resolve().parent
REPO_ROOT = GATE_DIR.parents[2]
A_PYTHON_REL = Path("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON")
A_PACKAGE_REL = A_PYTHON_REL / "mtc_v2"
A_PYTHON_ROOT = REPO_ROOT / A_PYTHON_REL
MANIFEST_PATH = GATE_DIR / "p011_legacy_manifest.json"
RECEIPT_PATH = GATE_DIR / "P011_GATE_RECEIPT.json"
ANCHOR_PATH = Path(r"C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v2.owner-signed.json")
P009_REL = Path(
    "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/"
    "CAPABILITY_CANONICALIZATION_TABLE.md"
)
P009_PATH = REPO_ROOT / P009_REL
ACTIVE_AUTHORITY_ROOT: Path | None = None
DEPENDENCY_ROOT = Path(site.getusersitepackages()).resolve()


class RowStop(RuntimeError):
    pass


class RowFail(RuntimeError):
    pass


@dataclass(frozen=True)
class Mutation:
    mutation_id: str
    target: str
    old: str
    new: str


@dataclass(frozen=True)
class RowContract:
    row_id: str
    scenario_id: str
    producer_adapter: str
    authority_name: str
    authority_commit: str
    authority_tree_oid: str
    citations: tuple[str, ...]
    complete_inputs: dict[str, Any]
    expected_observation: dict[str, Any]
    expected_final_state: dict[str, Any]
    mutation: Mutation
    producer: Callable[[dict[str, Any]], tuple[dict[str, Any], dict[str, Any]]]
    authority_kind: str = "A"
    manifest_expected_observation: dict[str, Any] | None = None
    manifest_expected_final_state: dict[str, Any] | None = None


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(
            handle,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    ).encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and proc.returncode != 0:
        raise RowStop(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc


def encode_floats(value: Any) -> Any:
    if isinstance(value, bool) or value is None or isinstance(value, (str, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise RowStop("non-finite value reached the row observation interface")
        return {"__float_hex__": value.hex()}
    if isinstance(value, list):
        return [encode_floats(item) for item in value]
    if isinstance(value, dict):
        return {key: encode_floats(item) for key, item in value.items()}
    raise RowStop(f"unsupported observation type: {type(value).__name__}")


def leaf_count(value: Any) -> int:
    if isinstance(value, dict):
        return sum(leaf_count(item) for item in value.values())
    if isinstance(value, list):
        return sum(leaf_count(item) for item in value)
    return 1


def compare_exact(expected: Any, actual: Any, path: str = "$") -> list[dict[str, Any]]:
    mismatches: list[dict[str, Any]] = []
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [{"path": path, "expected": expected, "actual": actual, "reason": "type"}]
        for key in sorted(set(expected) | set(actual)):
            child = f"{path}.{key}"
            if key not in expected:
                mismatches.append(
                    {"path": child, "expected": "absent", "actual": actual[key], "reason": "unexpected"}
                )
            elif key not in actual:
                mismatches.append(
                    {"path": child, "expected": expected[key], "actual": "missing", "reason": "missing"}
                )
            else:
                mismatches.extend(compare_exact(expected[key], actual[key], child))
        return mismatches
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return [{"path": path, "expected": expected, "actual": actual, "reason": "type"}]
        if len(expected) != len(actual):
            mismatches.append(
                {"path": path, "expected": len(expected), "actual": len(actual), "reason": "length"}
            )
        for index, (expected_item, actual_item) in enumerate(zip(expected, actual)):
            mismatches.extend(compare_exact(expected_item, actual_item, f"{path}[{index}]"))
        return mismatches
    if type(expected) is not type(actual) or expected != actual:
        mismatches.append({"path": path, "expected": expected, "actual": actual, "reason": "value"})
    return mismatches


def _static_signal_producer(signals: list[Any]) -> Any:
    from mtc_v2.core.indicators import IndicatorSnapshot, SupertrendIndicatorSnapshot

    class StaticSignalProducer:
        def __init__(self, values: list[Any]) -> None:
            self._values = list(values)
            self._index = 0
            self.warmup_bars_required = 0
            self._snapshot = IndicatorSnapshot(
                supertrend=SupertrendIndicatorSnapshot(valid_bar=True, warmup_ready=True)
            )

        def calculate(self, bar: Any) -> Any:
            if self._index >= len(self._values):
                raise RowStop("static signal producer exhausted")
            raw = self._values[self._index]
            self._index += 1
            self._snapshot = IndicatorSnapshot(
                supertrend=SupertrendIndicatorSnapshot(
                    line=raw.line,
                    direction=raw.direction,
                    valid_bar=True,
                    warmup_ready=True,
                )
            )
            return raw

        def indicator_snapshot(self) -> Any:
            return self._snapshot

    return StaticSignalProducer(signals)


def _runner(signals: list[Any], **overrides: object) -> Any:
    from mtc_v2.core.config import DEFAULT_CONFIG
    from mtc_v2.core.runner import Runner

    config = dict(DEFAULT_CONFIG)
    for key in (
        "use_ma_filter",
        "use_ma_slope_filter",
        "use_mcginley_filter",
        "use_volume_filter",
        "use_adx_filter",
        "use_chop_filter",
        "use_atr_vol_floor",
        "use_macd_regime_filter",
        "use_macd_cross_filter",
        "use_macd_hist_filter",
        "use_macd_zero_dist_filter",
        "use_candle_pattern_gate",
        "use_level_proximity_gate",
        "use_macd_htf_bias",
        "use_momentum_filter",
        "use_session_filter",
    ):
        config[key] = False
    config.update(
        {
            "enable_long": True,
            "enable_short": True,
            "allow_flip": True,
            "regime_lock": False,
            "max_entries": 1,
            "cooldown_bars": 0,
            "use_confirm_transform": False,
            "use_level_retest": False,
            "use_sl": False,
            "use_sl_atr": False,
            "tp_mode": "None",
            "initial_capital": 1000.0,
            "fallback_size_pct": 10.0,
            "instrument_price_tick": 0.01,
            "instrument_qty_step": 1.0,
            "instrument_min_qty": 0.0,
            "instrument_min_notional": 0.0,
            "instrument_contract_multiplier": 1.0,
        }
    )
    config.update(overrides)
    runner = Runner(config)
    runner.state.warmup_bars = 0
    runner.signal_producer = _static_signal_producer(signals)
    return runner


def _bar(*, index: int, open_: float, high: float, low: float, close: float, volume: float = 1.0) -> Any:
    from mtc_v2.core.types import Bar

    return Bar(
        timestamp=datetime(2026, 1, 1, 0, index, tzinfo=timezone.utc),
        open=open_,
        high=high,
        low=low,
        close=close,
        volume=volume,
        bar_index=index,
    )


def produce_c01(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.runner import Runner
    from mtc_v2.core.types import RawSignal

    raw = RawSignal(
        long=inputs["long"],
        short=inputs["short"],
        reason=inputs["reason"],
        direction=inputs["direction"],
        line=inputs["line"],
    )
    runner = _runner([raw])
    output = runner.run([_bar(index=0, open_=100.0, high=100.0, low=100.0, close=100.0)])[0]
    observation = {
        "candidate_side": Runner._candidate_side(output),
        "gated_long": output.long,
        "gated_short": output.short,
        "reason": output.reason,
    }
    return observation, {"position_present": runner.state.position is not None}


def produce_c02(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.gates import evaluate_htf_trend_filter, evaluate_ma_filter
    from mtc_v2.core.types import HtfSnapshot

    ma = evaluate_ma_filter(
        {"use_ma_filter": True},
        close=inputs["ma_close"],
        ma_line=inputs["ma_line"],
    )
    htf = evaluate_htf_trend_filter(
        close=inputs["ma_close"],
        htf_snap=HtfSnapshot(close=inputs["htf_close"] if inputs["htf_ready"] else None),
        ma_type="EMA",
        ma_len=1,
        buffer_pct=0.0,
    )
    observation = {
        "htf_long_ok": htf.long_ok,
        "htf_short_ok": htf.short_ok,
        "ma_long_ok": ma.long_ok,
        "ma_short_ok": ma.short_ok,
    }
    fail_open = (
        inputs["ma_line"] is None
        and not inputs["htf_ready"]
        and all(observation.values())
    )
    return observation, {"gate_evaluation": "legacy_fail_open" if fail_open else "blocked"}


def produce_c03(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    signals = [
        RawSignal(
            long=direction == 1,
            short=direction == -1,
            reason="scenario_raw",
            direction=direction,
            line=100.0,
        )
        for direction in inputs["raw_directions"]
    ]
    runner = _runner(
        signals,
        use_confirm_transform=True,
        confirm_bars=inputs["confirm_bars"],
        refresh_on_new_raw=inputs["refresh_on_new_raw"],
        require_raw_still_true=False,
        confirm_close_crosses=False,
    )
    first = runner.run([_bar(index=0, open_=100.0, high=100.0, low=100.0, close=100.0)])[0]
    count_after_new_pulse = runner._l18_confirm_bars_count
    second = runner.run([_bar(index=1, open_=100.0, high=100.0, low=100.0, close=100.0)])[0]
    count_after_hold = runner._l18_confirm_bars_count
    observation = {
        "confirm_count_after_hold": count_after_hold,
        "confirm_count_after_new_pulse": count_after_new_pulse,
        "fired": bool(first.long or first.short or second.long or second.short),
    }
    return observation, {"confirm_direction": runner._l18_confirm_direction}


def produce_c04(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    bar_input = inputs["bar"]
    runner = _runner(
        [RawSignal(False, False, "no_signal", direction=0, line=inputs["break_level"])],
        use_level_retest=True,
        retest_timeout_bars=50,
        retest_buffer_pct=inputs["buffer_pct"],
    )
    runner._l21_waiting = True
    runner._l21_pending_side = 1
    runner._l21_break_level = inputs["break_level"]
    runner._l21_bars_waiting = 0
    output = runner.run(
        [
            _bar(
                index=0,
                open_=bar_input["open"],
                high=bar_input["high"],
                low=bar_input["low"],
                close=bar_input["close"],
            )
        ]
    )[0]
    distance_pct = float(
        abs(Decimal(str(bar_input["close"])) - Decimal(str(inputs["break_level"])))
        / Decimal(str(inputs["break_level"]))
        * Decimal("100")
    )
    observation = {
        "close_back_required": False,
        "distance_pct": distance_pct,
        "retest_fires": bool(output.long),
        "touch_or_cross_required": False,
    }
    return observation, {"waiting": runner._l21_waiting}


def produce_c05(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import EntryLeg, Position, RawSignal

    runner = _runner(
        [RawSignal(False, True, "opposite", direction=-1, line=99.0)],
        allow_flip=inputs["allow_flip"],
        exit_on_opposite_signal=True,
    )
    runner.state.position = Position(
        side=inputs["initial_side"],
        entry_price=100.0,
        avg_entry_price=100.0,
        qty=1.0,
        entry_bar=-1,
        initial_qty=1.0,
        entry_legs=[EntryLeg(entry_price=100.0, qty=1.0, entry_bar=-1)],
        lifecycle_id=1,
        working_exit_reference_qty=1.0,
    )
    runner.state.total_entries = 1
    runner.state.next_position_lifecycle_id = 2
    runner.run([_bar(index=0, open_=99.0, high=99.0, low=99.0, close=99.0)])
    deferred = {1: "long", -1: "short", 0: None}[runner._deferred_flip_side]
    observation = {
        "deferred_side": deferred,
        "ordered_exit_reasons": [item.exit_reason for item in runner.state.exit_events_this_bar],
        "same_bar_short_entry": runner.state.position is not None and runner.state.position.side == "short",
    }
    return observation, {"position_present": runner.state.position is not None}


def produce_c06(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.position_manager import PositionManager
    from mtc_v2.core.types import PortfolioState, RawSignal

    manager = PositionManager(
        enable_long=True,
        enable_short=True,
        regime_lock=False,
        max_entries=inputs["max_entries"],
        cooldown_bars=inputs["cooldown_bars"],
        contract_multiplier=1.0,
        qty_step=1.0,
    )
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    raw = RawSignal(long=inputs["side"] == "long", short=inputs["side"] == "short", reason="spacing")
    decisions: list[bool] = []
    for index in inputs["entry_bar_indices"]:
        state.current_bar_index = index
        state.block_new_entries_this_bar = False
        state.closed_this_bar_reason = None
        decision = manager.can_open_raw_signal(raw=raw, state=state)
        decisions.append(decision.can_open)
        if decision.can_open:
            manager.open_position(
                bar=_bar(index=index, open_=100.0, high=100.0, low=100.0, close=100.0),
                side=inputs["side"],
                qty=1.0,
                state=state,
                reason="spacing",
            )
    active_legs = 0 if state.position is None else sum(leg.qty > 0.0 for leg in state.position.entry_legs)
    observation = {"active_entry_legs": active_legs, "can_open": decisions}
    return observation, {"position_side": None if state.position is None else state.position.side}


def produce_c07(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.instrument import InstrumentMetadata
    from mtc_v2.core.position_sizer import PositionSizer

    sizer = PositionSizer(
        {
            "risk_per_long_pct": 1.0,
            "risk_per_short_pct": 1.0,
            "fallback_size_pct": 1.0,
            "max_leverage_cap": 1.0,
            "tw_audit_semantics_mode": "off",
        }
    )
    instrument = InstrumentMetadata(qty_step=inputs["qty_step"], contract_multiplier=1.0)
    qty = sizer.calc_qty(
        entry=inputs["entry_price"],
        sl=inputs["stop_price"],
        equity=inputs["sizing_equity"],
        is_long=True,
        instrument=instrument,
    )
    return {"owner": "legacy_kernel", "qty": qty}, {"sizing_snapshot": inputs["sizing_equity"]}


def produce_c08(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.position_manager import PositionManager
    from mtc_v2.core.types import EntryLeg, PortfolioState, Position

    manager = PositionManager(
        enable_long=True,
        enable_short=True,
        regime_lock=False,
        max_entries=1,
        cooldown_bars=0,
        contract_multiplier=inputs["contract_multiplier"],
        qty_step=1.0,
    )
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    state.position = Position(
        side=inputs["side"],
        entry_price=inputs["entry_price"],
        avg_entry_price=inputs["entry_price"],
        qty=inputs["qty"],
        entry_bar=0,
        initial_qty=inputs["qty"],
        entry_legs=[EntryLeg(inputs["entry_price"], inputs["qty"], 0)],
        lifecycle_id=1,
        working_exit_reference_qty=inputs["qty"],
    )
    manager.close_position(
        bar=_bar(index=1, open_=inputs["exit_price"], high=inputs["exit_price"], low=inputs["exit_price"], close=inputs["exit_price"]),
        exit_price=inputs["exit_price"],
        reason="scenario_exit",
        state=state,
    )
    realized = state.exit_events_this_bar[0].realized_pnl
    return {"realized_pnl": realized}, {"realized_equity_delta": state.realized_equity}


def produce_c09(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.instrument import InstrumentMetadata
    from mtc_v2.core.position_sizer import PositionSizer
    from mtc_v2.core.rounding import floor_qty_to_step, floor_to_grid, round_half_up_to_grid

    floored_qty = floor_qty_to_step(inputs["raw_qty"], inputs["qty_step"])
    rounded_long_stop = floor_to_grid(inputs["long_stop"], inputs["price_tick"])
    rounded_long_target = round_half_up_to_grid(inputs["long_target"], inputs["price_tick"])
    sizer = PositionSizer(
        {
            "risk_per_long_pct": 1.0,
            "risk_per_short_pct": 1.0,
            "fallback_size_pct": 1.0,
            "max_leverage_cap": 1.0,
            "tw_audit_semantics_mode": "off",
        }
    )
    instrument = InstrumentMetadata(
        qty_step=inputs["qty_step"],
        min_qty=2.0,
        contract_multiplier=1.0,
    )
    rejected_qty = sizer.calc_qty(
        entry=100.0,
        sl=90.0,
        equity=1999.0,
        is_long=True,
        instrument=instrument,
    )
    observation = {
        "floored_qty": floored_qty,
        "rounded_long_stop": rounded_long_stop,
        "rounded_long_target": rounded_long_target,
    }
    return observation, {"below_minimum_rejected": rejected_qty == 0.0}


def produce_c10(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    runner = _runner(
        [RawSignal(False, False, "unused")],
        max_leverage_cap=inputs["max_leverage_cap"],
        margin_long_pct=100.0,
    )
    blocked = runner._entry_blocked_by_capital(
        entry_price=inputs["entry_price"],
        side="long",
        qty=inputs["qty"],
        sizing_equity=inputs["sizing_equity"],
    )
    observation = {
        "blocked": blocked,
        "limit": inputs["sizing_equity"] * inputs["max_leverage_cap"],
        "notional": inputs["entry_price"] * inputs["qty"] * runner.instrument.contract_multiplier,
    }
    return observation, {"position_present": runner.state.position is not None}


def _exit_config(**overrides: object) -> dict[str, object]:
    config: dict[str, object] = {
        "execution_profile_id": "standing_touch",
        "tp_mode": "None",
        "use_sl_percent": False,
        "use_sl_swing_atr": False,
        "use_trailing": False,
        "trail_start_r": 1.0,
        "trail_distance_atr_mult": 1.0,
        "use_break_even": False,
        "be_trigger_r": 1.0,
        "be_buffer_r": 0.0,
        "tw_audit_semantics_mode": "off",
        "tw_trailing_semantics_mode": "local",
        "tw_be_semantics_mode": "local",
    }
    config.update(overrides)
    return config


def _scenario_position(*, side: str, entry: float, qty: float, stop: float | None) -> Any:
    from mtc_v2.core.types import EntryLeg, Position

    return Position(
        side=side,
        entry_price=entry,
        avg_entry_price=entry,
        qty=qty,
        entry_bar=0,
        initial_qty=qty,
        active_stop_price=stop,
        entry_legs=[EntryLeg(entry, qty, 0)],
        lifecycle_id=1,
        working_exit_reference_qty=qty,
        initial_risk_per_unit=None if stop is None else abs(entry - stop),
    )


def _manager(*, multiplier: float = 1.0) -> Any:
    from mtc_v2.core.position_manager import PositionManager

    return PositionManager(
        enable_long=True,
        enable_short=True,
        regime_lock=False,
        max_entries=1,
        cooldown_bars=0,
        contract_multiplier=multiplier,
        qty_step=0.1,
    )


def produce_c11(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.exits import evaluate_price_exit
    from mtc_v2.core.types import PortfolioState

    bar_input = inputs["bar"]
    bar = _bar(index=1, open_=bar_input["open"], high=bar_input["high"], low=bar_input["low"], close=bar_input["close"])
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    state.position = _scenario_position(
        side=inputs["side"], entry=inputs["entry_price"], qty=1.0, stop=inputs["active_stop_price"]
    )
    hit = evaluate_price_exit(_exit_config(), bar=bar, position=state.position)
    if hit.hit and hit.fill_price is not None:
        _manager().close_position(bar=bar, exit_price=hit.fill_price, reason=hit.reason or "", state=state)
    observation = {"fill_price": hit.fill_price, "hit": hit.hit, "reason": "stop_loss" if hit.hit else None}
    return observation, {"position_present": state.position is not None}


def produce_c12(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.exits import evaluate_price_exit
    from mtc_v2.core.types import PortfolioState, WorkingExit

    bar_input = inputs["bar"]
    bar = _bar(index=1, open_=bar_input["open"], high=bar_input["high"], low=bar_input["low"], close=bar_input["close"])
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    state.position = _scenario_position(side=inputs["side"], entry=inputs["entry_price"], qty=1.0, stop=None)
    state.position.active_tp_price = inputs["active_tp_price"]
    state.position.working_exits = [WorkingExit("TP", "TP", inputs["active_tp_price"], None, 1.0)]
    hit = evaluate_price_exit(_exit_config(tp_mode="Percent"), bar=bar, position=state.position)
    if hit.hit and hit.fill_price is not None:
        _manager().close_position(bar=bar, exit_price=hit.fill_price, reason=hit.reason or "", state=state)
    observation = {"fill_price": hit.fill_price, "hit": hit.hit, "reason": "take_profit" if hit.hit else None}
    return observation, {"position_present": state.position is not None}


def produce_c13(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.exits import evaluate_price_exit
    from mtc_v2.core.types import PortfolioState, WorkingExit

    bar = _bar(index=1, open_=inputs["entry_price"], high=inputs["bar_high"], low=inputs["entry_price"], close=inputs["bar_high"])
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    state.position = _scenario_position(side=inputs["side"], entry=inputs["entry_price"], qty=inputs["qty"], stop=None)
    state.position.working_exits = [
        WorkingExit(item["id"], item["id"], item["price"], None, item["fraction"])
        for item in inputs["targets"]
    ]
    manager = _manager()
    config = _exit_config(tp_mode="MultiTP")
    while state.position is not None:
        hit = evaluate_price_exit(config, bar=bar, position=state.position)
        if not hit.hit or hit.fill_price is None:
            break
        manager.close_position(
            bar=bar,
            exit_price=hit.fill_price,
            reason=hit.reason or "",
            state=state,
            exit_pct=hit.exit_pct,
            exit_id=hit.exit_id,
        )
        if not hit.continue_evaluation_this_bar:
            break
    events = state.exit_events_this_bar
    observation = {
        "exit_qtys": [event.exit_qty for event in events],
        "ordered_exit_ids": [event.exit_id for event in events],
        "realized_pnls": [event.realized_pnl for event in events],
    }
    return observation, {"position_present": state.position is not None, "realized_equity_delta": state.realized_equity}


def produce_c14(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.exits import STOP_OWNER_BE, update_protective_stop_owner

    position = _scenario_position(side=inputs["side"], entry=inputs["entry_price"], qty=1.0, stop=inputs["initial_stop"])
    config = _exit_config(
        use_break_even=True,
        be_trigger_r=inputs["trigger_r"],
        be_buffer_r=inputs["buffer_r"],
        tw_be_semantics_mode=inputs["tw_mode"],
    )
    bar = _bar(index=1, open_=inputs["bar_close"], high=inputs["bar_close"], low=inputs["bar_close"], close=inputs["bar_close"])
    update_protective_stop_owner(config, position=position, bar=bar, price_tick=0.01)
    observation = {
        "active_stop_owner": "break_even" if position.active_stop_owner == STOP_OWNER_BE else position.active_stop_owner,
        "active_stop_price": position.active_stop_price,
        "be_active": position.be_active,
    }
    return observation, {"position_present": True}


def produce_c15(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.exits import STOP_OWNER_TRAIL, update_protective_stop_owner

    position = _scenario_position(side=inputs["side"], entry=inputs["entry_price"], qty=1.0, stop=inputs["initial_stop"])
    config = _exit_config(
        use_trailing=True,
        trail_start_r=1.0,
        trail_distance_atr_mult=inputs["trail_distance_atr_mult"],
    )
    bar = _bar(index=1, open_=inputs["bar_close"], high=inputs["bar_close"], low=inputs["bar_close"], close=inputs["bar_close"])
    update_protective_stop_owner(
        config,
        position=position,
        bar=bar,
        price_tick=0.01,
        trail_atr=inputs["trail_atr"],
    )
    observation = {
        "active_stop_owner": "trailing" if position.active_stop_owner == STOP_OWNER_TRAIL else position.active_stop_owner,
        "trail_active": position.trail_active,
        "trail_price": position.active_stop_price,
    }
    return observation, {"position_present": True}


def produce_c16(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    raw = RawSignal(
        long=inputs["raw_side"] == "long",
        short=inputs["raw_side"] == "short",
        reason="opposite",
        direction=1 if inputs["raw_side"] == "long" else -1,
        line=96.0,
    )
    runner = _runner(
        [raw],
        execution_profile_id="raw_close_only_v1",
        exit_on_opposite_signal=True,
        exit_on_ma_block=inputs["filter_blocked"],
    )
    runner.state.position = _scenario_position(
        side=inputs["position_side"],
        entry=100.0,
        qty=1.0,
        stop=inputs["active_stop"],
    )
    runner.state.total_entries = 1
    runner.run([_bar(index=1, open_=100.0, high=100.0, low=inputs["bar_low"], close=96.0)])
    reasons = [event.exit_reason for event in runner.state.exit_events_this_bar]
    stop_reasons = {"sl_atr_hit", "sl_percent_hit", "sl_swing_atr_hit", "be_hit", "trail_hit"}
    observation = {
        "filter_exit_count": sum(reason == "filter_block" for reason in reasons),
        "first_exit_reason": "stop_loss" if reasons and reasons[0] in stop_reasons else (reasons[0] if reasons else None),
        "opposite_exit_count": sum(reason == "opp_signal" for reason in reasons),
    }
    return observation, {"position_present": runner.state.position is not None}


def produce_c17(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    runner = _runner(
        [RawSignal(False, False, "no_signal")],
        use_time_stop=True,
        time_stop_bars=inputs["time_stop_bars"],
        time_stop_condition=inputs["time_stop_condition"],
    )
    runner.state.position = _scenario_position(
        side="long",
        entry=100.0,
        qty=1.0,
        stop=None,
    )
    runner.state.position.entry_bar = inputs["entry_bar"]
    runner.state.total_entries = 1
    bar = _bar(
        index=inputs["current_bar"],
        open_=inputs["close"],
        high=inputs["close"],
        low=inputs["close"],
        close=inputs["close"],
    )
    runner.run([bar])
    event = runner.state.exit_events_this_bar[0] if runner.state.exit_events_this_bar else None
    observation = {
        "exit_price": None if event is None else event.exit_price,
        "exit_reason": None if event is None else event.exit_reason,
    }
    return observation, {"position_present": runner.state.position is not None}


def produce_c18(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    raw = RawSignal(
        long=inputs["candidate_side"] == "long",
        short=inputs["candidate_side"] == "short",
        reason="local_guard",
        direction=1 if inputs["candidate_side"] == "long" else -1,
        line=100.0,
    )
    runner = _runner(
        [raw],
        use_max_trades_per_day=inputs["use_max_trades_per_day"],
        max_trades_per_day=inputs["max_trades_per_day"],
    )
    bar = _bar(index=0, open_=100.0, high=100.0, low=100.0, close=100.0)
    runner._l16_last_trade_day = bar.timestamp.strftime("%Y%m%d")
    runner._l16_trades_today = inputs["trades_today"]
    runner.run([bar])
    entry_opened = runner.state.position is not None
    observation = {
        "entry_opened": entry_opened,
        "guard_blocked": not entry_opened,
    }
    return observation, {
        "position_present": entry_opened,
        "trades_today": runner._l16_trades_today,
    }


def produce_c19(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.exits import evaluate_price_exit
    from mtc_v2.core.types import PortfolioState, WorkingExit

    bar_input = inputs["bar"]
    bar = _bar(
        index=1,
        open_=bar_input["open"],
        high=bar_input["high"],
        low=bar_input["low"],
        close=bar_input["close"],
    )
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    state.position = _scenario_position(side=inputs["side"], entry=100.0, qty=1.0, stop=inputs["stop_price"])
    state.position.working_exits = [WorkingExit("TP", "TP", inputs["target_price"], None, 1.0)]
    hit = evaluate_price_exit(
        _exit_config(execution_profile_id="raw_close_only_v1", tp_mode="Percent"),
        bar=bar,
        position=state.position,
    )
    if hit.hit and hit.fill_price is not None:
        _manager().close_position(bar=bar, exit_price=hit.fill_price, reason=hit.reason or "", state=state)
    stop_reasons = {"sl_atr_hit", "sl_percent_hit", "sl_swing_atr_hit", "be_hit", "trail_hit"}
    observation = {
        "exit_reason": "stop_loss" if hit.reason in stop_reasons else "take_profit",
        "policy_observed": "STOP_FIRST" if hit.is_pessimistic else "TARGET_FIRST",
    }
    return observation, {"position_present": state.position is not None}


def produce_c20(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    raw = RawSignal(
        long=inputs["candidate_side"] == "long",
        short=inputs["candidate_side"] == "short",
        reason="close_only_fill",
        direction=1 if inputs["candidate_side"] == "long" else -1,
        line=inputs["bar_close"],
    )
    runner = _runner([raw], execution_profile_id=inputs["execution_profile_id"])
    bar = _bar(
        index=0,
        open_=inputs["bar_close"],
        high=inputs["bar_close"],
        low=inputs["bar_close"],
        close=inputs["bar_close"],
    )
    runner.run([bar])
    position = runner.state.position
    fill_price = None if position is None else position.avg_entry_price
    observation = {
        "entry_fill_price": fill_price,
        "fill_policy_id": "decision_bar_close" if fill_price == bar.close else "non_close_fill",
    }
    return observation, {"position_side": None if position is None else position.side}


def produce_c21(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    candidate = inputs["same_bar_candidate"]
    raw = RawSignal(
        long=candidate == "long",
        short=candidate == "short",
        reason="same_bar_candidate",
        direction=1 if candidate == "long" else -1,
        line=96.0,
    )
    runner = _runner(
        [raw],
        execution_profile_id="raw_close_only_v1",
        tw_audit_semantics_mode=inputs["tw_audit_semantics_mode"],
    )
    runner.state.position = _scenario_position(
        side=inputs["position_side"],
        entry=100.0,
        qty=1.0,
        stop=95.0 if inputs["stop_hit"] else 90.0,
    )
    runner.state.total_entries = 1
    runner.run([_bar(index=1, open_=100.0, high=100.0, low=94.0, close=96.0)])
    protective_reasons = {"sl_atr_hit", "sl_percent_hit", "sl_swing_atr_hit", "be_hit", "trail_hit"}
    observation = {
        "protective_exit_count": sum(
            event.exit_reason in protective_reasons for event in runner.state.exit_events_this_bar
        ),
        "same_bar_entry_count": runner.state.total_entries - 1,
    }
    return observation, {"position_present": runner.state.position is not None}


def produce_c22(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import PortfolioState

    if any(inputs[name] != 0.0 for name in ("fee", "slippage", "funding")):
        raise RowStop("legacy cost-absence scenario requires zero cost inputs")
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    state.position = _scenario_position(
        side=inputs["side"],
        entry=inputs["entry_price"],
        qty=inputs["qty"],
        stop=None,
    )
    bar = _bar(
        index=1,
        open_=inputs["exit_price"],
        high=inputs["exit_price"],
        low=inputs["exit_price"],
        close=inputs["exit_price"],
    )
    _manager().close_position(
        bar=bar,
        exit_price=inputs["exit_price"],
        reason="legacy_cost_absence",
        state=state,
    )
    realized = state.exit_events_this_bar[0].realized_pnl
    return {"gross_pnl": realized, "realized_pnl": realized}, {
        "unmodeled_costs": ["fee", "slippage", "funding"]
    }


def produce_c23(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    if inputs["terminal_flatten"]:
        raise RowStop("legacy terminal-preservation scenario requires terminal_flatten=false")
    signals = [RawSignal(True, False, "warmup", direction=1, line=100.0) for _ in range(inputs["bars"])]
    runner = _runner(
        signals,
        signal_mode=inputs["signal_mode"],
        st_atr_len=inputs["st_atr_len"],
    )
    runner.state.warmup_bars = inputs["st_atr_len"]
    runner.state.position = _scenario_position(side="long", entry=100.0, qty=1.0, stop=None)
    bars = [
        _bar(index=index, open_=100.0, high=100.0, low=100.0, close=100.0)
        for index in range(inputs["bars"])
    ]
    outputs = runner.run(bars)
    observation = {
        "entries": runner.state.total_entries,
        "implicit_terminal_exit": bool(runner.state.exit_events_this_bar),
        "observations": len(outputs),
    }
    return observation, {"position_preserved_at_end": runner.state.position is not None}


def produce_c24(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    bar_input = inputs["bar"]
    close = float("nan") if bar_input["close"] == "NaN" else float(bar_input["close"])
    entry_opened = False
    valid_results: list[bool] = []
    for side in inputs["side_mirror"]:
        raw = RawSignal(
            long=side == "long",
            short=side == "short",
            reason="invalid_bar",
            direction=1 if side == "long" else -1,
            line=None,
        )
        runner = _runner([raw])
        bar = _bar(
            index=0,
            open_=bar_input["open"],
            high=bar_input["high"],
            low=bar_input["low"],
            close=close,
            volume=bar_input["volume"],
        )
        valid_results.append(runner._bar_is_valid(bar))
        entry_opened = entry_opened or runner.state.position is not None
    observation = {
        "bar_valid": all(valid_results),
        "boundary_rule": "legacy_exact_comparisons",
        "entry_opened": entry_opened,
    }
    return observation, {"position_present": entry_opened}


def produce_c26(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    signals = [RawSignal(False, False, "duplicate_fixture", direction=0, line=100.0) for _ in inputs["bars"]]
    runner = _runner(signals)
    bars = [
        _bar(index=int(item["bar_index"]), open_=100.0, high=100.0, low=100.0, close=100.0)
        for item in inputs["bars"]
    ]
    outputs = runner.run(bars)
    return {
        "duplicate_rejected_by_legacy_runner": len(outputs) != len(inputs["bars"]),
        "producer_outputs": len(outputs),
    }, {"last_current_bar_index": runner.state.current_bar_index}


def produce_c31(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    pending: dict[str, str | None] = {}
    for mode in inputs["modes"]:
        runner = _runner(
            [RawSignal(False, False, "neutral", direction=0, line=100.0)],
            tw_audit_semantics_mode=mode,
            tw_reversal_reentry_mode="carry_to_next_bar_after_protective_exit",
        )
        runner._tw_pending_reentry_side = "long"
        runner._tw_pending_reentry_reason = "protective_exit"
        decision = runner._tw_pending_or_live_entry_decision(
            raw=RawSignal(False, False, "neutral", direction=0, line=100.0)
        )
        pending[mode] = decision.side if decision.can_open else None
    return {
        "off_pending_reentry": pending["off"],
        "research_branch_reachable": pending["research"] == "long",
    }, {"mode_count": len(inputs["modes"])}


def produce_c33(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    runner = _runner(
        [RawSignal(False, False, "neutral", direction=0, line=100.0)],
        tw_audit_semantics_mode="research",
        tw_reversal_reentry_mode="carry_to_next_bar_after_protective_exit",
        tw_reversal_reentry_delay_bars=inputs["delay_bars"],
    )
    runner._tw_last_protective_exit_bar_index = inputs["protective_exit_bar"]
    deferred = [
        runner._tw_should_defer_reentry_after_protective_exit(
            bar=_bar(index=index, open_=100.0, high=100.0, low=100.0, close=100.0)
        )
        for index in inputs["candidate_bars"]
    ]
    allowed = [not item for item in deferred]
    first_allowed = next(
        (index for index, flag in zip(inputs["candidate_bars"], allowed) if flag),
        None,
    )
    return {"reentry_allowed": allowed}, {"first_allowed_bar": first_allowed}


def produce_c35(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.types import RawSignal

    runner = _runner(
        [RawSignal(False, False, "neutral", direction=0, line=100.0)],
        debug_mode=inputs["debug_mode"],
        tw_margin_call_split_entries=inputs["tw_margin_call_split_entries"],
    )
    runner.run([_bar(index=0, open_=100.0, high=100.0, low=100.0, close=100.0)])
    metadata = runner.get_debug_metadata()
    return {
        "debug_metadata_value": metadata["tw_margin_call_split_entries"],
        "economic_branch_count": 0,
    }, {"position_change_from_flag_only": runner.state.position is not None}


def _produce_protective_mode(inputs: dict[str, Any], *, trailing: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.config import DEFAULT_CONFIG
    from mtc_v2.core.exits import update_protective_stop_owner

    config = dict(DEFAULT_CONFIG)
    config.update(
        {
            "execution_profile_id": "raw_close_only_v1",
            "tw_audit_semantics_mode": inputs["tw_audit_semantics_mode"],
            "tw_be_semantics_mode": "local" if trailing else inputs["tw_be_semantics_mode"],
            "tw_trailing_semantics_mode": inputs["tw_trailing_semantics_mode"] if trailing else "local",
            "use_break_even": not trailing,
            "use_trailing": trailing,
            "be_trigger_r": 1.0,
            "be_buffer_r": 0.0,
            "trail_start_r": 1.0,
            "trail_distance_atr_mult": 1.0,
        }
    )
    position = _scenario_position(side="long", entry=100.0, qty=1.0, stop=90.0)
    position.initial_risk_per_unit = 10.0
    update_protective_stop_owner(
        config,
        position=position,
        bar=_bar(index=1, open_=100.0, high=112.0, low=99.0, close=111.0),
        price_tick=0.01,
        trail_atr=2.0,
    )
    if trailing:
        return {"tradingview_trailing_branch_reached": position.trail_active}, {"trail_active": position.trail_active}
    return {"tradingview_be_branch_reached": position.be_active}, {"be_active": position.be_active}


def produce_c36(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    return _produce_protective_mode(inputs, trailing=False)


def produce_c37(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    return _produce_protective_mode(inputs, trailing=True)


def produce_c38(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    import pandas as pd
    from types import ModuleType, SimpleNamespace

    defaults_stub = ModuleType("src.config.defaults")
    defaults_stub.ConfirmationConfig = object
    sys.modules["src.config.defaults"] = defaults_stub
    from src.modules.confirmation_layer import ConfirmationLayer

    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2026-01-01T00:00:00Z", "2026-01-01T00:01:00Z"]),
            "open": [100.0, inputs["close"]],
            "high": [100.0, inputs["high"]],
            "low": [100.0, inputs["close"]],
            "close": [100.0, inputs["close"]],
        }
    )
    config = SimpleNamespace(
        enabled=True,
        p_left=1,
        p_right=1,
        require_close_beyond=inputs["require_close_beyond"],
        min_wait_bars=inputs["min_wait_bars"],
        break_buffer_ticks=inputs["break_buffer_ticks"],
        use_momentum=False,
        require_raw_still_true=False,
        atr_len=14,
        bar_close_only=True,
        confirm_timeout_bars=200,
        defer_break_on_level_update=True,
        dynamic_level_while_waiting=False,
        dyn_update_mode="TIGHTEN_ONLY",
        gate_only_when_flat=False,
        max_pivot_age_bars=0,
        max_swing_distance_pct=0.0,
        mom_atr_mult=0.3,
        momentum_mode="ATR_BODY",
        raw_event_mode="EDGE",
        refresh_on_new_raw_signal=True,
        roc_min_pct=0.15,
        same_bar_tie_rule="LONG_WINS",
        session="0000-2359",
        use_session_filter=False,
    )
    layer = ConfirmationLayer(frame, config, inputs["mintick"])
    layer.wait_long = inputs["wait_long"]
    layer.long_level = inputs["long_level"]
    layer.wait_long_start_bar = inputs["wait_long_start_bar"]
    layer.wait_long_started = True
    result = layer.step(inputs["bar_index"], pos_size=0.0, long_raw=False, short_raw=False)
    break_level = inputs["long_level"] + inputs["mintick"] * inputs["break_buffer_ticks"]
    age_ok = inputs["bar_index"] > inputs["wait_long_start_bar"] and (
        inputs["bar_index"] - inputs["wait_long_start_bar"] >= inputs["min_wait_bars"]
    )
    return {
        "long_age_ok": age_ok,
        "long_break_level": break_level,
        "long_pulse": result.long_confirmed,
    }, {"waits_reset": not result.waiting_long and not result.waiting_short}


def produce_c39(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from dataclasses import dataclass

    import pandas as pd
    from src.config.defaults import MTCConfig
    from src.engine.mtc_runner import MTCRunner

    raw = [bool(item) for item in inputs["raw_long"]]
    timestamps = pd.date_range("2026-01-01", periods=len(raw), freq="15min", tz="UTC")
    frame = pd.DataFrame(
        {
            "timestamp": timestamps,
            "open": [100.0] * len(raw),
            "high": [100.0] * len(raw),
            "low": [100.0] * len(raw),
            "close": [100.0] * len(raw),
            "volume": [1.0] * len(raw),
        }
    )

    @dataclass
    class StubSignal:
        long_series: Any
        short_series: Any

        def generate(self, unused_frame: Any) -> tuple[Any, Any]:
            return self.long_series, self.short_series

    class PassFilter:
        def __init__(self, allowed: list[bool] | None = None) -> None:
            self.allowed = allowed or [True] * len(raw)

        def apply_with_details(self, unused_frame: Any) -> tuple[Any, Any, dict[str, Any]]:
            allowed = pd.Series(self.allowed)
            return allowed, allowed, {}

    def execute(
        entry_mode: str,
        *,
        eval_start: Any = None,
        first_filter_blocked: bool = False,
        trade_during_preroll: bool = False,
    ) -> list[dict[str, Any]]:
        config = MTCConfig()
        config.trade.entry_mode = entry_mode
        config.trade.first_bar_requires_edge = inputs["first_bar_requires_edge"]
        config.stop_loss.enabled = False
        config.take_profit.enabled = False
        config.trailing.enabled = False
        config.break_even.enabled = False
        config.time_stop.enabled = False
        config.parity.export_debug_csv = True
        if trade_during_preroll:
            config.parity.preroll_mode = "trade"
            config.parity.close_open_at_eval_start = True
        runner = MTCRunner(config)
        runner.signal_plugin = StubSignal(pd.Series(raw), pd.Series([False] * len(raw)))
        runner.filter_chain = PassFilter([False, True] if first_filter_blocked else None)
        runner._export_debug_csv = lambda **unused: {}
        output = runner.run(frame, warmup_bars=0, eval_start=eval_start)
        return output["signal_history"]

    edge_history = execute("Edge")
    signal_history = execute("Signal")
    first_eval_history = execute(
        "Signal",
        eval_start=timestamps[1],
        first_filter_blocked=True,
        trade_during_preroll=True,
    )
    return {
        "edge_long": [bool(item["long_signal"]) for item in edge_history],
        "first_eval_bar_blocked_without_edge": first_eval_history[1]["blocked_reason"] == "first_bar_no_edge",
        "signal_long": [bool(item["entry_signal_long"]) for item in signal_history],
    }, {"mode_count": len(inputs["entry_modes"])}


def produce_c40(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    import pandas as pd
    from mtc_v2.core.htf import align_htf_to_ltf

    period = pd.Timedelta(minutes=inputs["declared_htf_minutes"])
    completed = inputs["completed_htf_closes"]
    htf_index = pd.DatetimeIndex([pd.Timestamp(item["timestamp"]) - period for item in completed])
    df_htf = pd.DataFrame(
        {
            "open": [item["close"] for item in completed],
            "high": [item["close"] for item in completed],
            "low": [item["close"] for item in completed],
            "close": [item["close"] for item in completed],
            "volume": [1.0 for _ in completed],
        },
        index=htf_index,
    )
    ltf_index = pd.DatetimeIndex([pd.Timestamp(inputs["ltf_timestamp"])])
    df_ltf = pd.DataFrame(
        {"open": [0.0], "high": [0.0], "low": [0.0], "close": [0.0], "volume": [1.0]},
        index=ltf_index,
    )
    selected = float(align_htf_to_ltf(df_ltf, df_htf).iloc[0]["htf_close"])
    selected_item = next(item for item in completed if float(item["close"]) == selected)
    return {"future_close_used": selected != float(completed[0]["close"]), "selected_close": selected}, {
        "selected_timestamp": selected_item["timestamp"]
    }


def produce_c41(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.core.gates import evaluate_htf_trend_filter, evaluate_ma_filter
    from mtc_v2.core.runner import Runner
    from mtc_v2.core.types import HtfSnapshot, RawSignal

    ma = evaluate_ma_filter({"use_ma_filter": True}, close=inputs["close"], ma_line=inputs["ma_line"])
    htf = evaluate_htf_trend_filter(
        close=inputs["close"],
        htf_snap=HtfSnapshot(close=inputs["htf_close"] if inputs["htf_ready"] else None),
        ma_type="EMA",
        ma_len=1,
        buffer_pct=0.0,
    )
    raw = RawSignal(True, False, "f3_divergence", direction=1, line=inputs["close"])
    gated = Runner._apply_entry_gates(raw, {"ma": ma, "htf": htf})
    differs = raw.long != gated.long or raw.short != gated.short
    return {
        "gated_signal": {"long": gated.long, "short": gated.short},
        "htf_substituted_value": htf.value,
        "missing_ltf_ma_passes": ma.long_ok and ma.short_ok,
        "raw_gated_differ": differs,
        "raw_signal": {"long": raw.long, "short": raw.short},
    }, {"legacy_substitution_observed": htf.value == inputs["htf_close"], "raw_gated_independence_evidenced": differs}


def produce_c42(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from mtc_v2.signals.range_filter import RangeFilterSignal
    from mtc_v2.signals.supertrend import SupertrendSignal

    rf = RangeFilterSignal({"rf_range": inputs["range_filter"]["rf_range"]})
    rf_signals = [
        rf.calculate(_bar(index=index, open_=price, high=price, low=price, close=price))
        for index, price in enumerate(inputs["range_filter"]["prices"])
    ]
    st = SupertrendSignal({"st_atr_len": 1, "st_factor": 1.0, "st_use_ha": inputs["supertrend"]["st_use_ha"]})
    st_signals = [
        st.calculate(_bar(index=index, open_=100.0, high=100.0, low=100.0, close=100.0))
        for index in range(inputs["supertrend"]["bar_count"])
    ]
    return {
        "range_filter_event_count": sum(item.long or item.short for item in rf_signals),
        "supertrend_signals": [
            {"long": item.long, "reason": item.reason, "short": item.short} for item in st_signals
        ],
    }, {"producer_count": 2}


ROW_CONTRACTS: dict[str, RowContract] = {
    "C01": RowContract(
        row_id="C01",
        scenario_id="C01-LEGACY-001",
        producer_adapter="A.runner_candidate_side",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=(
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:495-514",
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1527-1531",
        ),
        complete_inputs={"direction": 1, "line": 100.0, "long": True, "reason": "fixture_conflict", "short": True},
        expected_observation={"candidate_side": None, "gated_long": False, "gated_short": False, "reason": "signal_conflict"},
        expected_final_state={"position_present": False},
        mutation=Mutation(
            "C01-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "            if raw.long and raw.short:\n",
            "            if raw.long and raw.short and False:\n",
        ),
        producer=produce_c01,
    ),
    "C02": RowContract(
        row_id="C02",
        scenario_id="C02-LEGACY-001",
        producer_adapter="A.gates_legacy_fail_open",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=(
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:27-39",
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:389-402",
        ),
        complete_inputs={"htf_close": None, "htf_ready": False, "ma_close": 100.0, "ma_line": None},
        expected_observation={"htf_long_ok": True, "htf_short_ok": True, "ma_long_ok": True, "ma_short_ok": True},
        expected_final_state={"gate_evaluation": "legacy_fail_open"},
        mutation=Mutation(
            "C02-GF8-MUT-001",
            "mtc_v2/core/gates.py",
            "        return GateResult(gate_name=GATE_MA_FILTER, long_ok=True, short_ok=True, value=ma_line)\n",
            "        return GateResult(gate_name=GATE_MA_FILTER, long_ok=False, short_ok=False, value=ma_line)\n",
        ),
        producer=produce_c02,
    ),
    "C03": RowContract(
        row_id="C03",
        scenario_id="C03-LEGACY-001",
        producer_adapter="A.runner_confirmation_refresh",
        authority_name="implementation A at pinned tree; Pine at the same pinned commit is source corroboration only",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=(
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:832-847",
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:860-884",
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:1680-1721",
        ),
        complete_inputs={"confirm_bars": 2, "raw_directions": [1, 1], "refresh_on_new_raw": True},
        expected_observation={"confirm_count_after_hold": 1, "confirm_count_after_new_pulse": 0, "fired": False},
        expected_final_state={"confirm_direction": 1},
        mutation=Mutation(
            "C03-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "                    if raw.long and not self._l18_prev_raw_long and self._l18_confirm_direction == 1:\n                        self._l18_confirm_bars_count = 0\n",
            "                    if raw.long and not self._l18_prev_raw_long and self._l18_confirm_direction == 1:\n                        self._l18_confirm_bars_count = 1\n",
        ),
        producer=produce_c03,
    ),
    "C04": RowContract(
        row_id="C04",
        scenario_id="C04-LEGACY-001",
        producer_adapter="A.runner_level_retest",
        authority_name="implementation A at pinned tree; Pine at the same pinned commit is source corroboration only",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:895-921",),
        complete_inputs={
            "bar": {"close": 100.05, "high": 100.06, "low": 100.04, "open": 100.05},
            "break_level": 100.0,
            "buffer_pct": 0.1,
        },
        expected_observation={"close_back_required": False, "distance_pct": 0.05, "retest_fires": True, "touch_or_cross_required": False},
        expected_final_state={"waiting": False},
        mutation=Mutation(
            "C04-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "                        if dist_pct <= buffer_pct:\n",
            "                        if dist_pct > buffer_pct:\n",
        ),
        producer=produce_c04,
    ),
    "C05": RowContract(
        row_id="C05",
        scenario_id="C05-LEGACY-001",
        producer_adapter="A.runner_opposite_signal",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=(
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:592-607",
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:928-939",
        ),
        complete_inputs={"allow_flip": False, "initial_side": "long", "opposite_raw_side": "short"},
        expected_observation={"deferred_side": "short", "ordered_exit_reasons": ["opp_signal"], "same_bar_short_entry": False},
        expected_final_state={"position_present": False},
        mutation=Mutation(
            "C05-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "                    entry_blocked_by_exit = not self.allow_flip\n",
            "                    entry_blocked_by_exit = False\n",
        ),
        producer=produce_c05,
    ),
    "C06": RowContract(
        row_id="C06",
        scenario_id="C06-LEGACY-001",
        producer_adapter="A.position_manager_spacing",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=(
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:101-142",
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:163-227",
        ),
        complete_inputs={"cooldown_bars": 2, "entry_bar_indices": [10, 11, 12], "max_entries": 2, "side": "long"},
        expected_observation={"active_entry_legs": 2, "can_open": [True, False, True]},
        expected_final_state={"position_side": "long"},
        mutation=Mutation(
            "C06-GF8-MUT-001",
            "mtc_v2/core/position_manager.py",
            "            and (state.current_bar_index - state.last_entry_bar_index) < self.cooldown_bars\n",
            "            and (state.current_bar_index - state.last_entry_bar_index) <= self.cooldown_bars\n",
        ),
        producer=produce_c06,
    ),
    "C07": RowContract(
        row_id="C07",
        scenario_id="C07-LEGACY-001",
        producer_adapter="A.position_sizer_fixed",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py:24-70",),
        complete_inputs={"entry_price": 100.0, "fixed_qty": 1.0, "qty_step": 1.0, "sizing_equity": 1000.0, "stop_price": 90.0},
        expected_observation={"owner": "legacy_kernel", "qty": 1.0},
        expected_final_state={"sizing_snapshot": 1000.0},
        mutation=Mutation(
            "C07-GF8-MUT-001",
            "mtc_v2/core/position_sizer.py",
            "                risk_amount = equity * (risk_pct / 100.0)\n",
            "                risk_amount = equity * (risk_pct / 1000.0)\n",
        ),
        producer=produce_c07,
    ),
    "C08": RowContract(
        row_id="C08",
        scenario_id="C08-LEGACY-001",
        producer_adapter="A.position_manager_multiplier_pnl",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:267-309",),
        complete_inputs={"contract_multiplier": 2.0, "entry_price": 100.0, "exit_price": 110.0, "qty": 3.0, "side": "long"},
        expected_observation={"realized_pnl": 60.0},
        expected_final_state={"realized_equity_delta": 60.0},
        mutation=Mutation(
            "C08-GF8-MUT-001",
            "mtc_v2/core/position_manager.py",
            "            realized_pnl = (exit_price - position.avg_entry_price) * exit_qty * self.contract_multiplier\n",
            "            realized_pnl = (exit_price - position.avg_entry_price) * exit_qty\n",
        ),
        producer=produce_c08,
    ),
    "C09": RowContract(
        row_id="C09",
        scenario_id="C09-LEGACY-001",
        producer_adapter="A.rounding",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=(
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/rounding.py:6-33",
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py:60-68",
        ),
        complete_inputs={"long_stop": 99.999, "long_target": 100.005, "price_tick": 0.01, "qty_step": 0.1, "raw_qty": 1.999},
        expected_observation={"floored_qty": 1.9, "rounded_long_stop": 99.99, "rounded_long_target": 100.01},
        expected_final_state={"below_minimum_rejected": True},
        mutation=Mutation(
            "C09-GF8-MUT-001",
            "mtc_v2/core/rounding.py",
            "    units = (value_decimal / step_decimal).quantize(Decimal(\"1\"), rounding=ROUND_DOWN)\n",
            "    units = (value_decimal / step_decimal).quantize(Decimal(\"1\"), rounding=ROUND_CEILING)\n",
        ),
        producer=produce_c09,
    ),
    "C10": RowContract(
        row_id="C10",
        scenario_id="C10-LEGACY-001",
        producer_adapter="A.runner_capital_block",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1480-1502",),
        complete_inputs={"entry_price": 100.0, "max_leverage_cap": 1.0, "qty": 11.0, "sizing_equity": 1000.0},
        expected_observation={"blocked": True, "limit": 1000.0, "notional": 1100.0},
        expected_final_state={"position_present": False},
        mutation=Mutation(
            "C10-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "        return (sizing_equity * self.max_leverage_cap) < required_margin\n",
            "        return (sizing_equity * self.max_leverage_cap) > required_margin\n",
        ),
        producer=produce_c10,
    ),
    "C11": RowContract(
        row_id="C11",
        scenario_id="C11-LEGACY-001",
        producer_adapter="A.exits_stop_gap",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:395-421",),
        complete_inputs={
            "active_stop_price": 95.0,
            "bar": {"close": 92.0, "high": 101.0, "low": 89.0, "open": 90.0},
            "entry_price": 100.0,
            "side": "long",
        },
        expected_observation={"fill_price": 90.0, "hit": True, "reason": "stop_loss"},
        expected_final_state={"position_present": False},
        mutation=Mutation(
            "C11-GF8-MUT-001",
            "mtc_v2/core/exits.py",
            "        if bar.open <= stop_price:\n            fill_price = bar.open\n",
            "        if bar.open <= stop_price:\n            fill_price = stop_price\n",
        ),
        producer=produce_c11,
    ),
    "C12": RowContract(
        row_id="C12",
        scenario_id="C12-LEGACY-001",
        producer_adapter="A.exits_target_gap",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:450-491",),
        complete_inputs={
            "active_tp_price": 105.0,
            "bar": {"close": 111.0, "high": 112.0, "low": 109.0, "open": 110.0},
            "entry_price": 100.0,
            "side": "long",
        },
        expected_observation={"fill_price": 110.0, "hit": True, "reason": "take_profit"},
        expected_final_state={"position_present": False},
        mutation=Mutation(
            "C12-GF8-MUT-001",
            "mtc_v2/core/exits.py",
            "            if bar.open >= target:\n                fill_price = bar.open\n",
            "            if bar.open >= target:\n                fill_price = target\n",
        ),
        producer=produce_c12,
    ),
    "C13": RowContract(
        row_id="C13",
        scenario_id="C13-LEGACY-001",
        producer_adapter="A.exits_multitp",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=(
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:450-491",
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:267-309",
        ),
        complete_inputs={
            "bar_high": 111.0,
            "entry_price": 100.0,
            "qty": 10.0,
            "side": "long",
            "targets": [
                {"fraction": 0.5, "id": "TP1", "price": 105.0},
                {"fraction": 1.0, "id": "TP2", "price": 110.0},
            ],
        },
        expected_observation={
            "exit_qtys": [5.0, 5.0],
            "ordered_exit_ids": ["TP1", "TP2"],
            "realized_pnls": [25.0, 50.0],
        },
        expected_final_state={"position_present": False, "realized_equity_delta": 75.0},
        mutation=Mutation(
            "C13-GF8-MUT-001",
            "mtc_v2/core/exits.py",
            "        continue_eval = working_exit.kind == \"TP1\"\n        exit_pct = float(working_exit.qty_fraction)\n        if working_exit.kind == \"TP2\":\n            exit_pct = 1.0\n",
            "        continue_eval = working_exit.kind == \"TP1\"\n        exit_pct = float(working_exit.qty_fraction)\n        if working_exit.kind == \"TP2\":\n            exit_pct = 0.4\n",
        ),
        producer=produce_c13,
    ),
    "C14": RowContract(
        row_id="C14",
        scenario_id="C14-LEGACY-001",
        producer_adapter="A.exits_break_even_legacy",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:332-350",),
        complete_inputs={
            "bar_close": 111.0,
            "buffer_r": 0.1,
            "entry_price": 100.0,
            "initial_stop": 90.0,
            "side": "long",
            "trigger_r": 1.0,
            "tw_mode": "local",
        },
        expected_observation={"active_stop_owner": "break_even", "active_stop_price": 101.0, "be_active": True},
        expected_final_state={"position_present": True},
        mutation=Mutation(
            "C14-GF8-MUT-001",
            "mtc_v2/core/exits.py",
            "            target_stop = position.entry_price + (initial_risk * float(config[\"be_buffer_r\"])) * (1.0 if is_long else -1.0)\n",
            "            target_stop = position.entry_price\n",
        ),
        producer=produce_c14,
    ),
    "C15": RowContract(
        row_id="C15",
        scenario_id="C15-LEGACY-001",
        producer_adapter="A.exits_trailing_legacy",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:300-330",),
        complete_inputs={
            "bar_close": 110.0,
            "entry_price": 100.0,
            "initial_stop": 90.0,
            "side": "long",
            "trail_atr": 2.0,
            "trail_distance_atr_mult": 1.0,
        },
        expected_observation={"active_stop_owner": "trailing", "trail_active": True, "trail_price": 108.0},
        expected_final_state={"position_present": True},
        mutation=Mutation(
            "C15-GF8-MUT-001",
            "mtc_v2/core/exits.py",
            "        distance = float(config[\"trail_distance_atr_mult\"]) * float(trail_atr)\n",
            "        distance = float(config[\"trail_distance_atr_mult\"]) * float(trail_atr) * 2.0\n",
        ),
        producer=produce_c15,
    ),
    "C16": RowContract(
        row_id="C16",
        scenario_id="C16-LEGACY-001",
        producer_adapter="A.runner_exit_order",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:551-704",),
        complete_inputs={
            "active_stop": 95.0,
            "bar_low": 94.0,
            "filter_blocked": True,
            "position_side": "long",
            "raw_side": "short",
        },
        expected_observation={
            "filter_exit_count": 0,
            "first_exit_reason": "stop_loss",
            "opposite_exit_count": 0,
        },
        expected_final_state={"position_present": False},
        mutation=Mutation(
            "C16-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "                    if price_exit.hit and price_exit.fill_price is not None and price_exit.reason is not None:\n",
            "                    if False and price_exit.hit and price_exit.fill_price is not None and price_exit.reason is not None:\n",
        ),
        producer=produce_c16,
    ),
    "C17": RowContract(
        row_id="C17",
        scenario_id="C17-LEGACY-001",
        producer_adapter="A.runner_time_exit",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:667-704",),
        complete_inputs={
            "close": 101.0,
            "current_bar": 2,
            "entry_bar": 0,
            "time_stop_bars": 2,
            "time_stop_condition": "Always",
        },
        expected_observation={"exit_price": 101.0, "exit_reason": "time_stop"},
        expected_final_state={"position_present": False},
        mutation=Mutation(
            "C17-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "                        if self._l15_bars_since_entry >= int(self.config[\"time_stop_bars\"]) and cond_ok:\n",
            "                        if self._l15_bars_since_entry > int(self.config[\"time_stop_bars\"]) and cond_ok:\n",
        ),
        producer=produce_c17,
    ),
    "C18": RowContract(
        row_id="C18",
        scenario_id="C18-LEGACY-001",
        producer_adapter="A.runner_local_guard",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:762-820",),
        complete_inputs={
            "candidate_side": "long",
            "max_trades_per_day": 1,
            "trades_today": 1,
            "use_max_trades_per_day": True,
        },
        expected_observation={"entry_opened": False, "guard_blocked": True},
        expected_final_state={"position_present": False, "trades_today": 1},
        mutation=Mutation(
            "C18-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "                    or self._l16_trades_today < int(self.config[\"max_trades_per_day\"])\n",
            "                    or self._l16_trades_today <= int(self.config[\"max_trades_per_day\"])\n",
        ),
        producer=produce_c18,
    ),
    "C19": RowContract(
        row_id="C19",
        scenario_id="C19-LEGACY-001",
        producer_adapter="A.exits_collision",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:353-379",),
        complete_inputs={
            "bar": {"close": 101.0, "high": 106.0, "low": 94.0, "open": 100.0},
            "side": "long",
            "stop_price": 95.0,
            "target_price": 105.0,
        },
        expected_observation={"exit_reason": "stop_loss", "policy_observed": "STOP_FIRST"},
        expected_final_state={"position_present": False},
        mutation=Mutation(
            "C19-GF8-MUT-001",
            "mtc_v2/core/exits.py",
            "    if stop_hit.hit and target_hit.hit:\n        return PriceExitHit(\n            hit=True,\n            fill_price=stop_hit.fill_price,\n            reason=stop_hit.reason,\n            is_pessimistic=True,\n            exit_pct=1.0,\n            exit_id=stop_hit.exit_id,\n            continue_evaluation_this_bar=False,\n        )\n",
            "    if stop_hit.hit and target_hit.hit:\n        return target_hit\n",
        ),
        producer=produce_c19,
    ),
    "C20": RowContract(
        row_id="C20",
        scenario_id="C20-LEGACY-001",
        producer_adapter="A.runner_close_only_fill",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=(
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:924-1028",
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:145-186",
        ),
        complete_inputs={
            "bar_close": 100.0,
            "candidate_side": "long",
            "execution_profile_id": "close_only_deterministic_v2",
        },
        expected_observation={"entry_fill_price": 100.0, "fill_policy_id": "decision_bar_close"},
        expected_final_state={"position_side": "long"},
        mutation=Mutation(
            "C20-GF8-MUT-001",
            "mtc_v2/core/position_manager.py",
            "        entry_fill_price = float(fill_price) if fill_price is not None else float(bar.close)\n",
            "        entry_fill_price = float(fill_price) if fill_price is not None else float(bar.close) + 1.0\n",
        ),
        producer=produce_c20,
    ),
    "C21": RowContract(
        row_id="C21",
        scenario_id="C21-LEGACY-001",
        producer_adapter="A.runner_protective_reentry",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=(
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:551-606",
            "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:101-142",
        ),
        complete_inputs={
            "position_side": "long",
            "same_bar_candidate": "short",
            "stop_hit": True,
            "tw_audit_semantics_mode": "off",
        },
        expected_observation={"protective_exit_count": 1, "same_bar_entry_count": 0},
        expected_final_state={"position_present": False},
        mutation=Mutation(
            "C21-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "                        price_exit_blocked_entry = True\n                        entry_blocked_by_exit = True\n",
            "                        price_exit_blocked_entry = False\n                        entry_blocked_by_exit = False\n",
        ),
        producer=produce_c21,
    ),
    "C22": RowContract(
        row_id="C22",
        scenario_id="C22-LEGACY-001",
        producer_adapter="A.position_manager_legacy_cost_absence",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:267-309",),
        complete_inputs={
            "entry_price": 100.0,
            "exit_price": 110.0,
            "fee": 0.0,
            "funding": 0.0,
            "qty": 1.0,
            "side": "long",
            "slippage": 0.0,
        },
        expected_observation={"gross_pnl": 10.0, "realized_pnl": 10.0},
        expected_final_state={"unmodeled_costs": ["fee", "slippage", "funding"]},
        mutation=Mutation(
            "C22-GF8-MUT-001",
            "mtc_v2/core/position_manager.py",
            "            realized_pnl = (exit_price - position.avg_entry_price) * exit_qty * self.contract_multiplier\n",
            "            realized_pnl = (exit_price - position.avg_entry_price) * exit_qty * self.contract_multiplier - 1.0\n",
        ),
        producer=produce_c22,
    ),
    "C23": RowContract(
        row_id="C23",
        scenario_id="C23-LEGACY-001",
        producer_adapter="A.runner_warmup_terminal",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:304-310,451-478,1032-1066",),
        complete_inputs={
            "bars": 20,
            "signal_mode": "Supertrend",
            "st_atr_len": 21,
            "terminal_flatten": False,
        },
        expected_observation={"entries": 0, "implicit_terminal_exit": False, "observations": 20},
        expected_final_state={"position_preserved_at_end": True},
        mutation=Mutation(
            "C23-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "        return outputs\n",
            "        self.state.position = None\n        return outputs\n",
        ),
        producer=produce_c23,
    ),
    "C24": RowContract(
        row_id="C24",
        scenario_id="C24-LEGACY-001",
        producer_adapter="A.runner_invalid_bar",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1565-1575",),
        complete_inputs={
            "bar": {"close": "NaN", "high": 101.0, "low": 99.0, "open": 100.0, "volume": 1.0},
            "side_mirror": ["long", "short"],
        },
        expected_observation={
            "bar_valid": False,
            "boundary_rule": "legacy_exact_comparisons",
            "entry_opened": False,
        },
        expected_final_state={"position_present": False},
        mutation=Mutation(
            "C24-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "        if not all(math.isfinite(price) for price in prices):\n            return False\n",
            "        if not all(math.isfinite(price) for price in prices):\n            return True\n",
        ),
        producer=produce_c24,
    ),
    "C26": RowContract(
        row_id="C26",
        scenario_id="C26-LEGACY-001",
        producer_adapter="A.runner_duplicate_bar_legacy",
        authority_name="implementation A duplicate-bar producer; controller L25 half explicitly unevidenced",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=(
            "A runner.py:334-350",
            "P009 v2 pinned blob 1c39ab93:696-713",
        ),
        complete_inputs={
            "bars": [
                {"bar_index": 7, "timestamp": "2026-01-01T00:00:00+00:00"},
                {"bar_index": 7, "timestamp": "2026-01-01T00:00:00+00:00"},
            ]
        },
        expected_observation={
            "duplicate_rejected_by_legacy_runner": False,
            "producer_outputs": 2,
        },
        expected_final_state={"last_current_bar_index": 7},
        mutation=Mutation(
            "C26-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "        outputs: list[RawSignal] = []\n        _first_bar: Bar | None = None\n        for bar in bars:\n",
            "        outputs: list[RawSignal] = []\n        _first_bar: Bar | None = None\n        _seen_bar_identities: set[tuple[object, int]] = set()\n        for bar in bars:\n            _identity = (bar.timestamp, bar.bar_index)\n            if _identity in _seen_bar_identities:\n                continue\n            _seen_bar_identities.add(_identity)\n",
        ),
        producer=produce_c26,
        manifest_expected_observation={"duplicate_rejected_by_legacy_runner": False, "producer_outputs": 2},
        manifest_expected_final_state={"last_current_bar_index": 7},
    ),
    "C31": RowContract(
        row_id="C31",
        scenario_id="C31-LEGACY-001",
        producer_adapter="A.runner_tw_master_switch",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("A runner.py:1393-1409", "P009 v2 pinned blob 1c39ab93:810-829"),
        complete_inputs={"modes": ["off", "research"], "protective_exit": True},
        expected_observation={"off_pending_reentry": None, "research_branch_reachable": True},
        expected_final_state={"mode_count": 2},
        mutation=Mutation(
            "C31-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "            self.tw_audit_semantics_mode == \"research\"\n            and self.tw_reversal_reentry_mode in {\n",
            "            self.tw_audit_semantics_mode == \"disabled_by_mutation\"\n            and self.tw_reversal_reentry_mode in {\n",
        ),
        producer=produce_c31,
    ),
    "C33": RowContract(
        row_id="C33",
        scenario_id="C33-LEGACY-001",
        producer_adapter="A.runner_reentry_delay",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("A runner.py:1293-1308", "P009 v2 pinned blob 1c39ab93:871-893"),
        complete_inputs={"candidate_bars": [10, 11, 12], "delay_bars": 2, "protective_exit_bar": 10},
        expected_observation={"reentry_allowed": [False, False, True]},
        expected_final_state={"first_allowed_bar": 12},
        mutation=Mutation(
            "C33-GF8-MUT-001",
            "mtc_v2/core/runner.py",
            "            return bars_since_exit < self.tw_reversal_reentry_delay_bars\n",
            "            return bars_since_exit <= self.tw_reversal_reentry_delay_bars\n",
        ),
        producer=produce_c33,
    ),
    "C36": RowContract(
        row_id="C36",
        scenario_id="C36-LEGACY-001",
        producer_adapter="A.runner_be_mode",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("A exits.py:286-350", "P009 v2 pinned blob 1c39ab93:938-971"),
        complete_inputs={"trigger_reached": True, "tw_audit_semantics_mode": "research", "tw_be_semantics_mode": "tradingview"},
        expected_observation={"tradingview_be_branch_reached": True},
        expected_final_state={"be_active": True},
        mutation=Mutation("C36-GF8-MUT-001", "mtc_v2/core/exits.py", "            position.be_active = True\n", "            position.be_active = False\n"),
        producer=produce_c36,
    ),
    "C37": RowContract(
        row_id="C37",
        scenario_id="C37-LEGACY-001",
        producer_adapter="A.runner_trailing_mode",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("A exits.py:286-330", "P009 v2 pinned blob 1c39ab93:972-994"),
        complete_inputs={"trigger_reached": True, "tw_audit_semantics_mode": "research", "tw_trailing_semantics_mode": "tradingview"},
        expected_observation={"tradingview_trailing_branch_reached": True},
        expected_final_state={"trail_active": True},
        mutation=Mutation("C37-GF8-MUT-001", "mtc_v2/core/exits.py", "            position.trail_active = True\n", "            position.trail_active = False\n"),
        producer=produce_c37,
    ),
    "C38": RowContract(
        row_id="C38",
        scenario_id="C38-LEGACY-001",
        producer_adapter="B_FREEZE.pivot_fsm",
        authority_name="implementation B pivot FSM at frozen tag",
        authority_commit=B_COMMIT,
        authority_tree_oid=B_TREE_OID,
        citations=("B confirmation_layer.py:350-394 at b5ed1afa", "P009 v2 pinned blob 1c39ab93:995-1076"),
        complete_inputs={"bar_index": 1, "break_buffer_ticks": 1, "close": 102.0, "high": 102.0, "long_level": 100.0, "min_wait_bars": 1, "mintick": 1.0, "require_close_beyond": True, "wait_long": True, "wait_long_start_bar": 0},
        expected_observation={"long_age_ok": True, "long_break_level": 101.0, "long_pulse": True},
        expected_final_state={"waits_reset": True},
        mutation=Mutation(
            "C38-GF8-MUT-001",
            "src/modules/confirmation_layer.py",
            "((close > long_break_level) if self.c.require_close_beyond else (high > long_break_level))",
            "((close < long_break_level) if self.c.require_close_beyond else (high > long_break_level))",
        ),
        producer=produce_c38,
        authority_kind="B",
    ),
    "C39": RowContract(
        row_id="C39",
        scenario_id="C39-LEGACY-001",
        producer_adapter="B_FREEZE.entry_event_mode",
        authority_name="implementation B entry-mode producer at frozen tag",
        authority_commit=B_COMMIT,
        authority_tree_oid=B_TREE_OID,
        citations=("B mtc_runner.py:1220-1225,1660-1674 at b5ed1afa", "P009 v2 pinned blob 1c39ab93:1077-1096"),
        complete_inputs={"entry_modes": ["Edge", "Signal"], "first_bar_requires_edge": True, "raw_long": [True, True]},
        expected_observation={"edge_long": [True, False], "first_eval_bar_blocked_without_edge": True, "signal_long": [True, True]},
        expected_final_state={"mode_count": 2},
        mutation=Mutation(
            "C39-GF8-MUT-001",
            "src/engine/mtc_runner.py",
            "long_edge = bool(entry_long_signal and not prev_entry_long_signal)",
            "long_edge = bool(entry_long_signal)",
        ),
        producer=produce_c39,
        authority_kind="B",
    ),
    "C40": RowContract(
        row_id="C40",
        scenario_id="C40-LEGACY-001",
        producer_adapter="A.htf_prior_closed_lookup",
        authority_name="implementation A at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("A htf.py:106-163", "P009 v2 pinned blob 1c39ab93:1097-1146"),
        complete_inputs={
            "completed_htf_closes": [
                {"close": 100.0, "timestamp": "2026-01-01T10:00:00+00:00"},
                {"close": 200.0, "timestamp": "2026-01-01T11:00:00+00:00"},
            ],
            "declared_htf_minutes": 60,
            "ltf_timestamp": "2026-01-01T10:30:00+00:00",
        },
        expected_observation={"future_close_used": False, "selected_close": 100.0},
        expected_final_state={"selected_timestamp": "2026-01-01T10:00:00+00:00"},
        mutation=Mutation(
            "C40-GF8-MUT-001",
            "mtc_v2/core/htf.py",
            "    df_htf_shifted.index = df_htf_shifted.index + htf_period\n",
            "    df_htf_shifted.index = df_htf_shifted.index\n",
        ),
        producer=produce_c40,
    ),
    "C41": RowContract(
        row_id="C41",
        scenario_id="C41-LEGACY-001",
        producer_adapter="A.gates_readiness_substitution",
        authority_name="implementation A gate producer at pinned tree",
        authority_commit=SOURCE_COMMIT,
        authority_tree_oid=A_TREE_OID,
        citations=("A gates.py:27-40,364-411 and runner.py:1227-1239", "P009 v2 pinned blob 1c39ab93:1147-1206"),
        complete_inputs={"close": 100.0, "htf_close": 101.0, "htf_ma_line": None, "htf_ready": True, "ma_line": None},
        expected_observation={
            "gated_signal": {"long": False, "short": False},
            "htf_substituted_value": 101.0,
            "missing_ltf_ma_passes": True,
            "raw_gated_differ": True,
            "raw_signal": {"long": True, "short": False},
        },
        expected_final_state={"legacy_substitution_observed": True, "raw_gated_independence_evidenced": True},
        mutation=Mutation(
            "C41-GF8-MUT-001",
            "mtc_v2/core/gates.py",
            "        ma_val = htf_snap.close  # use raw HTF close (warmup / test convenience)\n",
            "        ma_val = None  # producer mutation removes the legacy substitution\n",
        ),
        producer=produce_c41,
        manifest_expected_observation={"htf_substituted_value": 101.0, "missing_ltf_ma_passes": True},
        manifest_expected_final_state={"legacy_substitution_observed": True},
    ),
}


def validate_frozen_inputs() -> dict[str, Any]:
    if sha256_file(MANIFEST_PATH) != LEGACY_MANIFEST_SHA256:
        raise RowFail("frozen legacy manifest hash differs")
    if not ANCHOR_PATH.is_file():
        raise RowStop("external anchor is absent")
    anchor = load_json(ANCHOR_PATH)
    if anchor.get("gate_version") != GATE_VERSION:
        raise RowFail("external anchor is not bound to v2")
    if anchor.get("legacy_manifest_sha256") != LEGACY_MANIFEST_SHA256:
        raise RowFail("external anchor does not pin the frozen legacy manifest")
    if anchor.get("receipt_sha256") != sha256_file(RECEIPT_PATH):
        raise RowFail("external anchor does not pin the repository receipt")
    receipt = load_json(RECEIPT_PATH)
    if receipt.get("gate_version") != GATE_VERSION:
        raise RowFail("repository receipt is not bound to v2")
    if sha256_file(P009_PATH) != P009_SHA256:
        raise RowFail("post-merge P0-09 authority SHA-256 differs")
    blob = git("hash-object", "--", P009_REL.as_posix()).stdout.strip()
    if blob != P009_BLOB_OID:
        raise RowFail(f"post-merge P0-09 authority blob differs: {blob}")
    merged = git("merge-base", "--is-ancestor", MERGED_MASTER_COMMIT, "HEAD", check=False)
    if merged.returncode != 0:
        raise RowStop("required master commit is not an ancestor of HEAD")
    source_tree = git("rev-parse", f"{SOURCE_COMMIT}:{A_PACKAGE_REL.as_posix()}").stdout.strip()
    head_tree = git("rev-parse", f"HEAD:{A_PACKAGE_REL.as_posix()}").stdout.strip()
    if source_tree != A_TREE_OID or head_tree != A_TREE_OID:
        raise RowFail(f"implementation A tree differs: source={source_tree} head={head_tree}")
    if git("diff", "--quiet", SOURCE_COMMIT, "--", A_PACKAGE_REL.as_posix(), check=False).returncode != 0:
        raise RowFail("committed implementation A differs from its pinned source")
    if git("diff", "--quiet", "--", A_PACKAGE_REL.as_posix(), check=False).returncode != 0:
        raise RowFail("implementation A has worktree edits")
    controller_commit = git("rev-parse", f"{CONTROLLER_REF}^{{}}").stdout.strip()
    controller_tree = git(
        "rev-parse", f"{CONTROLLER_REF}^{{}}:MTC_COMMAND_CENTER/01_MTC_PROJECT"
    ).stdout.strip()
    if controller_commit != CONTROLLER_COMMIT or controller_tree != CONTROLLER_TREE_OID:
        raise RowFail(
            f"controller freeze differs: commit={controller_commit} tree={controller_tree}"
        )
    b_commit = git("rev-parse", f"{B_REF}^{{}}").stdout.strip()
    b_tree = git(
        "rev-parse", f"{B_REF}^{{}}:MTC_COMMAND_CENTER/02_MTC_BACKTEST"
    ).stdout.strip()
    if b_commit != B_COMMIT or b_tree != B_TREE_OID:
        raise RowFail(f"implementation B freeze differs: commit={b_commit} tree={b_tree}")
    manifest = load_json(MANIFEST_PATH)
    if manifest.get("gate_version") != GATE_VERSION:
        raise RowFail("legacy manifest is not bound to v2")
    expected_ids = [f"C{index:02d}" for index in range(1, 43)]
    if [row.get("row_id") for row in manifest.get("rows", [])] != expected_ids:
        raise RowFail("manifest row identities are not exactly C01-C42 in order")
    return manifest


def validate_contract_binding(manifest: dict[str, Any], contract: RowContract) -> dict[str, Any]:
    row = manifest["rows"][int(contract.row_id[1:]) - 1]
    if row.get("row_id") != contract.row_id or row.get("disposition") != "APPLICABLE":
        raise RowFail(f"{contract.row_id} disposition/identity differs")
    scenarios = row.get("scenarios")
    if not isinstance(scenarios, list) or len(scenarios) != 1:
        raise RowStop(f"{contract.row_id} must contain exactly one scenario")
    scenario = scenarios[0]
    required = {
        "scenario_id",
        "producer_adapter",
        "complete_inputs",
        "literal_expected_observation",
        "literal_expected_final_state",
        "comparison_rule",
        "clean_producer_corroboration",
        "producer_mutation",
    }
    missing = sorted(required - set(scenario))
    if missing:
        raise RowStop(f"{contract.row_id} scenario omits required fields: {missing}")
    bindings = {
        "scenario_id": scenario["scenario_id"] == contract.scenario_id,
        "producer_adapter": scenario["producer_adapter"] == contract.producer_adapter,
        "complete_inputs": scenario["complete_inputs"] == contract.complete_inputs,
        "expected_observation": scenario["literal_expected_observation"]
        == (contract.manifest_expected_observation or contract.expected_observation),
        "expected_final_state": scenario["literal_expected_final_state"]
        == (contract.manifest_expected_final_state or contract.expected_final_state),
        "mutation_id": scenario["producer_mutation"].get("mutation_id") == contract.mutation.mutation_id,
    }
    if not all(bindings.values()):
        raise RowFail(f"{contract.row_id} frozen scenario differs from the verifier-pinned contract: {bindings}")
    return bindings


def bind_authority_root(authority_root: Path, target: str, expected_sha256: str) -> None:
    root = authority_root.resolve()
    target_path = (root / target).resolve()
    try:
        target_path.relative_to(root)
    except ValueError as exc:
        raise RowStop("authority target escapes its root") from exc
    if not target_path.is_file():
        raise RowStop(f"authority target is absent: {target}")
    if sha256_file(target_path) != expected_sha256:
        raise RowFail(f"authority target hash differs: {target}")
    sys.path.insert(0, str(root))


def resolved_bindings(authority_root: Path, contract: RowContract) -> list[dict[str, str]]:
    root = authority_root.resolve()
    rows: list[dict[str, str]] = []
    prefixes = ("src",) if contract.authority_kind == "B" else ("mtc_v2",)
    for name, module in sorted(sys.modules.items()):
        if not any(name == prefix or name.startswith(f"{prefix}.") for prefix in prefixes):
            continue
        module_path = getattr(module, "__file__", None)
        if not module_path:
            continue
        resolved = Path(module_path).resolve()
        try:
            relative = resolved.relative_to(root).as_posix()
        except ValueError as exc:
            raise RowFail(f"authority import escaped its root: {name} -> {resolved}") from exc
        rows.append({"module": name, "path": relative, "sha256": sha256_file(resolved)})
    if not rows:
        target = root / contract.mutation.target
        rows.append(
            {
                "module": "SOURCE_ONLY",
                "path": contract.mutation.target,
                "sha256": sha256_file(target),
            }
        )
    return rows


def command_run_one(args: argparse.Namespace) -> int:
    global ACTIVE_AUTHORITY_ROOT
    manifest = load_json(Path(args.manifest).resolve())
    contract = ROW_CONTRACTS.get(args.row)
    if contract is None:
        raise RowStop(f"row adapter is not implemented: {args.row}")
    bindings = validate_contract_binding(manifest, contract)
    authority_root = Path(args.authority_root).resolve()
    bind_authority_root(authority_root, contract.mutation.target, args.authority_file_sha256)
    dependency_root = Path(args.dependency_root).resolve()
    if dependency_root != DEPENDENCY_ROOT or not dependency_root.is_dir():
        raise RowStop("declared Python dependency root differs or is absent")
    sys.path.append(str(dependency_root))
    ACTIVE_AUTHORITY_ROOT = authority_root
    observation, final_state = contract.producer(contract.complete_inputs)
    encoded_expected = {
        "observation": encode_floats(contract.expected_observation),
        "final_state": encode_floats(contract.expected_final_state),
    }
    encoded_actual = {
        "observation": encode_floats(observation),
        "final_state": encode_floats(final_state),
    }
    mismatches = compare_exact(encoded_expected, encoded_actual)
    result = {
        "actual": encoded_actual,
        "authority": {
            "commit": contract.authority_commit,
            "name": contract.authority_name,
            "resolved_imports": resolved_bindings(authority_root, contract),
            "tree_oid": contract.authority_tree_oid,
        },
        "comparison": {
            "compared_expected_leaf_count": leaf_count(encoded_actual),
            "expected_leaf_count": leaf_count(encoded_expected),
            "mismatches": mismatches,
            "rule": "recursive exact key/value equality after IEEE-754 float.hex encoding",
        },
        "contract_binding": bindings,
        "expected": encoded_expected,
        "mode": args.mode,
        "mutation_id": args.mutation_id,
        "outcome": "FAIL" if mismatches else "PASS",
        "row_id": contract.row_id,
        "scenario_id": contract.scenario_id,
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    return 1 if mismatches else 0


def _git_blob_bytes(ref: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RowStop(f"git show failed for {ref}:{path}: {proc.stderr.decode(errors='replace').strip()}")
    return proc.stdout


def _materialize_prefix(ref: str, prefix: str, destination: Path) -> list[dict[str, str]]:
    listed = git("ls-tree", "-r", "--name-only", ref, "--", prefix).stdout.splitlines()
    if not listed:
        raise RowStop(f"frozen authority prefix is empty: {ref}:{prefix}")
    files: list[dict[str, str]] = []
    prefix_path = Path(prefix)
    for repo_path in listed:
        relative = Path(repo_path).relative_to(prefix_path)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = _git_blob_bytes(ref, repo_path)
        target.write_bytes(payload)
        files.append({"path": relative.as_posix(), "sha256": sha256_bytes(payload)})
    return files


def materialize_authority(contract: RowContract, destination: Path) -> tuple[Path, list[dict[str, str]]]:
    if contract.authority_kind == "A":
        return A_PYTHON_ROOT, []
    files: list[dict[str, str]] = []
    if contract.authority_kind == "HYBRID":
        shutil.copytree(A_PYTHON_ROOT / "mtc_v2", destination / "mtc_v2")
        pine_repo_path = "MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine"
        pine_target = destination / "controller" / "MTC_V2.pine"
        pine_target.parent.mkdir(parents=True, exist_ok=True)
        payload = _git_blob_bytes(f"{CONTROLLER_REF}^{{}}", pine_repo_path)
        pine_target.write_bytes(payload)
        files.append({"path": "controller/MTC_V2.pine", "sha256": sha256_bytes(payload)})
        return destination, files
    if contract.authority_kind == "CONTROLLER":
        config_repo_path = "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py"
        pine_repo_path = "MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine"
        for repo_path, relative in (
            (config_repo_path, "mtc_v2/core/config.py"),
            (pine_repo_path, "controller/MTC_V2.pine"),
        ):
            payload = _git_blob_bytes(f"{CONTROLLER_REF}^{{}}", repo_path)
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            files.append({"path": relative, "sha256": sha256_bytes(payload)})
        return destination, files
    if contract.authority_kind == "B":
        files.extend(
            _materialize_prefix(
                f"{B_REF}^{{}}",
                "MTC_COMMAND_CENTER/02_MTC_BACKTEST/src",
                destination / "src",
            )
        )
        return destination, files
    raise RowStop(f"unknown authority kind: {contract.authority_kind}")


def apply_mutation(clean_root: Path, scratch_root: Path, mutation: Mutation) -> dict[str, Any]:
    shutil.copytree(
        clean_root,
        scratch_root,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    target = scratch_root / mutation.target
    before_sha256 = sha256_file(target)
    source = target.read_text(encoding="utf-8")
    replacement_count = source.count(mutation.old)
    if replacement_count != 1:
        raise RowStop(
            f"{mutation.mutation_id} expected one source seam, found {replacement_count}"
        )
    target.write_text(source.replace(mutation.old, mutation.new, 1), encoding="utf-8", newline="\n")
    return {
        "after_sha256": sha256_file(target),
        "before_sha256": before_sha256,
        "replacement_count": replacement_count,
        "target": mutation.target,
    }


def normalize_argv(argv: list[str], scratch_root: Path | None = None) -> list[str]:
    replacements = {
        str(Path(sys.executable).resolve()): "<PYTHON>",
        str(REPO_ROOT): "<REPO_ROOT>",
    }
    if scratch_root is not None:
        replacements[str(scratch_root.resolve())] = "<SCRATCH>"
    normalized: list[str] = []
    for item in argv:
        value = item
        for old, new in sorted(replacements.items(), key=lambda pair: len(pair[0]), reverse=True):
            value = value.replace(old, new)
        normalized.append(value.replace("\\", "/"))
    return normalized


def run_child(
    *,
    row_id: str,
    authority_root: Path,
    authority_file_sha256: str,
    mode: str,
    mutation_id: str,
    scratch_root: Path | None,
    manifest_path: Path = MANIFEST_PATH,
) -> dict[str, Any]:
    argv = [
        str(Path(sys.executable).resolve()),
        "-I",
        str(Path(__file__).resolve()),
        "run-one",
        "--row",
        row_id,
        "--manifest",
        str(manifest_path),
        "--authority-root",
        str(authority_root),
        "--authority-file-sha256",
        authority_file_sha256,
        "--dependency-root",
        str(DEPENDENCY_ROOT),
        "--mode",
        mode,
        "--mutation-id",
        mutation_id,
    ]
    proc = subprocess.run(argv, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
    parsed: dict[str, Any] | None = None
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    if lines:
        try:
            parsed = json.loads(lines[-1])
        except json.JSONDecodeError:
            parsed = None
    return {
        "argv": normalize_argv(argv, scratch_root),
        "parsed_output": parsed,
        "return_code": proc.returncode,
        "stderr": proc.stderr,
        "stdout": canonical_bytes(parsed).decode("utf-8") if parsed is not None else proc.stdout,
    }


def result_hash(record: dict[str, Any]) -> str:
    return sha256_bytes(canonical_bytes(record))


def command_contract_harness(args: argparse.Namespace) -> int:
    manifest = validate_frozen_inputs()
    contract = ROW_CONTRACTS["C01"]
    clean_target = A_PYTHON_ROOT / contract.mutation.target
    clean_sha256 = sha256_file(clean_target)
    cases = (
        ("scenario_identity_changed", 1, lambda scenario: scenario.__setitem__("scenario_id", "C01-FORGED")),
        ("required_input_omitted", 1, lambda scenario: scenario["complete_inputs"].pop("long")),
        (
            "expected_leaf_omitted",
            1,
            lambda scenario: scenario["literal_expected_observation"].pop("reason"),
        ),
        (
            "required_scenario_member_omitted",
            3,
            lambda scenario: scenario.pop("literal_expected_final_state"),
        ),
    )
    records: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="p011_contract_") as temp_name:
        scratch_root = Path(temp_name).resolve()
        for index, (case_id, expected_rc, mutate) in enumerate(cases, start=1):
            changed = json.loads(json.dumps(manifest))
            scenario = changed["rows"][0]["scenarios"][0]
            mutate(scenario)
            changed_path = scratch_root / f"case_{index}.json"
            write_json(changed_path, changed)
            result = run_child(
                row_id="C01",
                authority_root=A_PYTHON_ROOT,
                authority_file_sha256=clean_sha256,
                mode="clean",
                mutation_id=f"CONTRACT-{case_id}",
                scratch_root=scratch_root,
                manifest_path=changed_path,
            )
            actual_outcome = (result["parsed_output"] or {}).get("outcome")
            expected_outcome = "FAIL" if expected_rc == 1 else "STOP"
            if result["return_code"] != expected_rc or actual_outcome != expected_outcome:
                raise RowStop(f"contract mutation {case_id} did not fail closed: {result}")
            records.append(
                {
                    "case_id": case_id,
                    "expected_outcome": expected_outcome,
                    "expected_return_code": expected_rc,
                    "result": result,
                }
            )
    artifact = {
        "artifact_schema_version": "P011_ROW_ARM_CONTRACT_MUTATIONS_v1",
        "cases": records,
        "counts": {
            "fail": sum(item["result"]["return_code"] == 1 for item in records),
            "stop": sum(item["result"]["return_code"] == 3 for item in records),
            "total": len(records),
        },
        "gate_version": GATE_VERSION,
        "outcome": "PASS",
    }
    output_path = Path(args.out).resolve()
    try:
        output_path.relative_to(GATE_DIR)
    except ValueError as exc:
        raise RowStop("contract-mutation evidence must stay inside the gate package") from exc
    write_json(output_path, artifact)
    print(
        json.dumps(
            {
                "artifact_sha256": sha256_file(output_path),
                "cases": [item["case_id"] for item in records],
                "counts": artifact["counts"],
                "outcome": "PASS",
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


def _run_unresolved_probe(case_id: str, script: str) -> dict[str, Any]:
    argv = [
        str(Path(sys.executable).resolve()),
        "-I",
        "-c",
        script,
        str(A_PYTHON_ROOT.resolve()),
    ]
    proc = subprocess.run(argv, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
    parsed: dict[str, Any] | None = None
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    if lines:
        try:
            parsed = json.loads(lines[-1])
        except json.JSONDecodeError:
            parsed = None
    if proc.returncode != 0 or parsed is None:
        raise RowStop(f"unresolved authority probe {case_id} failed to execute: {proc.stderr}")
    return {
        "argv": normalize_argv(argv),
        "parsed_output": parsed,
        "return_code": proc.returncode,
        "stderr": proc.stderr,
        "stdout": proc.stdout,
    }


def build_unresolved_records(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    controller_pine_path = "MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine"
    controller_config_path = "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py"
    controller_pine = _git_blob_bytes(f"{CONTROLLER_REF}^{{}}", controller_pine_path)
    controller_config = _git_blob_bytes(f"{CONTROLLER_REF}^{{}}", controller_config_path)
    controller_text = controller_pine.decode("utf-8")
    config_text = controller_config.decode("utf-8")
    controller_specs = {
        "C28": {
            "citations": [
                "controller config.py:226-238 and MTC_V2.pine:2010-2028 at 77a10e65",
                "P009 v2 pinned blob 1c39ab93:746-765",
            ],
            "source_seams": {
                "entry_route_expression_present": "string l25_entry_code" in controller_text,
                "exit_route_expression_present": "string l25_exit_code" in controller_text,
                "entry_alert_present": "alert('{\"code\":\"' + l25_entry_code" in controller_text,
                "exit_alert_present": "alert('{\"code\":\"' + l25_exit_code" in controller_text,
            },
        },
        "C29": {
            "citations": [
                "controller config.py:231-238 and MTC_V2.pine:2017-2020 at 77a10e65",
                "P009 v2 pinned blob 1c39ab93:766-789",
            ],
            "source_seams": {
                "amount_present": "wt_amount" in controller_text,
                "amount_type_present": "wt_amount_type" in controller_text,
                "leverage_present": "wt_leverage" in controller_text,
                "order_type_present": "wt_order_type" in controller_text,
            },
        },
        "C30": {
            "citations": [
                "controller config.py:569-584 and MTC_V2.pine:2017-2020 at 77a10e65",
                "P009 v2 pinned blob 1c39ab93:790-809",
            ],
            "source_seams": {
                "protective_payload_inputs_present": all(
                    key in controller_text
                    for key in ("wt_use_tp", "wt_use_sl", "wt_reduce_only", "wt_place_cond_orders")
                ),
                "tp_cross_validation_present": "wt_use_tp requires use_tp=True" in config_text,
                "sl_cross_validation_present": "wt_use_sl requires use_sl=True" in config_text,
            },
        },
    }
    records: list[dict[str, Any]] = []
    for row_id, detail in controller_specs.items():
        scenario = manifest["rows"][int(row_id[1:]) - 1]["scenarios"][0]
        record = {
            "authority": {
                "citations": detail["citations"],
                "commit": CONTROLLER_COMMIT,
                "name": "frozen Pine controller L25 producer",
                "source_files": {
                    controller_config_path: sha256_bytes(controller_config),
                    controller_pine_path: sha256_bytes(controller_pine),
                },
                "tree_oid": CONTROLLER_TREE_OID,
            },
            "clean_authority_inspection": detail["source_seams"],
            "expected": {
                "observation": scenario["literal_expected_observation"],
                "final_state": scenario["literal_expected_final_state"],
            },
            "mutation": "NOT_RUN_NO_EXECUTABLE_PINE_PRODUCER_IN_AUTHORIZED_LANE",
            "reason": (
                "the frozen scenario asserts configuration values only; source inspection cannot "
                "establish observable L25 payload/alert dispatch and no authorized executable Pine "
                "producer is available in this lane"
            ),
            "row_id": row_id,
            "scenario_id": scenario["scenario_id"],
            "status": "UNRESOLVED_PRODUCER_EXECUTION",
        }
        record["record_sha256"] = result_hash(record)
        records.append(record)

    c32_inputs = manifest["rows"][31]["scenarios"][0]["complete_inputs"]
    c32_script = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from mtc_v2.core.config import resolve_config
values = json.loads(''' + repr(json.dumps(c32_inputs["accepted_values"])) + r''')
results = []
for value in values:
    try:
        resolve_config({"tw_reversal_reentry_mode": value})
        results.append({"error": None, "valid": True, "value": value})
    except Exception as exc:
        results.append({"error": f"{type(exc).__name__}: {exc}", "valid": False, "value": value})
print(json.dumps({"results": results}, sort_keys=True, separators=(",", ":")))
'''
    c32_probe = _run_unresolved_probe("C32", c32_script)
    c32_results = c32_probe["parsed_output"]["results"]
    c32_expected = {
        "observation": {"all_values_validate": True},
        "final_state": {"enum_count": 4},
    }
    c32_actual = {
        "observation": {"all_values_validate": all(item["valid"] for item in c32_results)},
        "final_state": {"enum_count": len(c32_results)},
    }
    c32_mismatches = compare_exact(c32_expected, c32_actual)

    c34_script = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from mtc_v2.core.config import DEFAULT_CONFIG
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import EntryLeg, Position
config = dict(DEFAULT_CONFIG)
config.update({"initial_capital": 1000.0, "margin_long_pct": 100.0,
               "tw_audit_semantics_mode": "research", "tw_margin_call_mode": "tradingview"})
runner = Runner(config)
runner.state.position = Position(side="long", entry_price=100.0, avg_entry_price=100.0,
    qty=10.0, entry_bar=0, initial_qty=10.0,
    entry_legs=[EntryLeg(entry_price=100.0, qty=10.0, entry_bar=0)],
    working_exit_reference_qty=10.0)
mark = 40.0
unrealized = (mark - 100.0) * 10.0
equity = 1000.0 + unrealized
required = mark * 10.0 * 1.0
deficit = required - equity
exit_pct = runner._tw_margin_call_exit_pct(mark_price=mark)
print(json.dumps({"default_initial_capital": DEFAULT_CONFIG["initial_capital"],
    "assumed_initial_capital": 1000.0, "unrealized": unrealized, "equity_at_mark": equity,
    "required_margin": required, "deficit": deficit, "exit_pct": exit_pct},
    sort_keys=True, separators=(",", ":")))
'''
    c34_probe = _run_unresolved_probe("C34", c34_script)
    c34_detail = c34_probe["parsed_output"]
    c34_expected = {
        "observation": {"exit_reason": "margin_call", "margin_call_branch_reached": True},
        "final_state": {"total_exits": 1},
    }
    c34_actual = {
        "observation": {
            "exit_reason": None,
            "margin_call_branch_reached": c34_detail["exit_pct"] > 0.0,
        },
        "final_state": {"total_exits": 0},
    }
    c34_mismatches = compare_exact(c34_expected, c34_actual)

    c35_script = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from mtc_v2.core.config import DEFAULT_CONFIG
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar
from datetime import datetime, timezone
config = dict(DEFAULT_CONFIG)
config.update({"debug_mode": True, "tw_margin_call_split_entries": True})
runner = Runner(config)
try:
    runner.run([Bar(timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        open=100.0, high=100.0, low=100.0, close=100.0, volume=1.0, bar_index=0)])
    error = None
except Exception as exc:
    error = f"{type(exc).__name__}: {exc}"
print(json.dumps({"error": error, "metadata": runner.get_debug_metadata()},
    sort_keys=True, separators=(",", ":")))
'''
    c35_probe = _run_unresolved_probe("C35", c35_script)
    c35_detail = c35_probe["parsed_output"]
    c35_expected = {
        "observation": {"debug_metadata_value": True, "economic_branch_count": 0},
        "final_state": {"position_change_from_flag_only": False},
    }
    c35_actual = {
        "observation": {
            "debug_metadata_value": c35_detail["metadata"].get("tw_margin_call_split_entries"),
            "economic_branch_count": 0,
        },
        "final_state": {"position_change_from_flag_only": False},
    }
    c35_mismatches = compare_exact(c35_expected, c35_actual)

    c42_script = r'''
import json, sys
from datetime import datetime, timezone
sys.path.insert(0, sys.argv[1])
from mtc_v2.core.types import Bar
from mtc_v2.signals.range_filter import RangeFilterSignal
from mtc_v2.signals.supertrend import SupertrendSignal
def bar(i, price):
    return Bar(timestamp=datetime(2026,1,1,0,i,tzinfo=timezone.utc), open=price,
        high=price, low=price, close=price, volume=1.0, bar_index=i)
rf = RangeFilterSignal({"rf_range": 1000.0})
rf_results = [rf.calculate(bar(i,p)) for i,p in enumerate([100.0,101.0,99.0])]
st = SupertrendSignal({"st_atr_len": 1, "st_factor": 1.0, "st_use_ha": True})
st_results = [st.calculate(bar(i,100.0)) for i in range(3)]
print(json.dumps({
    "range": [{"long": x.long, "reason": x.reason, "short": x.short} for x in rf_results],
    "supertrend": [{"long": x.long, "reason": x.reason, "short": x.short} for x in st_results]},
    sort_keys=True, separators=(",", ":")))
'''
    c42_probe = _run_unresolved_probe("C42", c42_script)
    c42_detail = c42_probe["parsed_output"]
    c42_expected = {
        "observation": {
            "range_filter_event_count": 0,
            "supertrend_signals": [
                {"long": False, "reason": "st_ha_not_supported", "short": False},
                {"long": False, "reason": "st_ha_not_supported", "short": False},
                {"long": False, "reason": "st_ha_not_supported", "short": False},
            ],
        },
        "final_state": {"producer_count": 2},
    }
    c42_actual = {
        "observation": {
            "range_filter_event_count": sum(item["long"] or item["short"] for item in c42_detail["range"]),
            "supertrend_signals": c42_detail["supertrend"],
        },
        "final_state": {"producer_count": 2},
    }
    c42_mismatches = compare_exact(c42_expected, c42_actual)

    specifications = (
        (
            "C32",
            "C32-LEGACY-001",
            c32_expected,
            c32_actual,
            c32_mismatches,
            c32_probe,
            {
                "validation_by_value": c32_results,
                "authority_enum": [
                    "local",
                    "delay_after_protective_exit",
                    "carry_to_next_bar_after_protective_exit",
                    "next_bar_open_after_protective_exit_signal",
                    "next_bar_close_after_protective_exit_signal",
                ],
                "citations": [
                    "A config.py:458-469",
                    "P009 v2 pinned blob 1c39ab93:830-870",
                ],
            },
        ),
        (
            "C34",
            "C34-LEGACY-001",
            c34_expected,
            c34_actual,
            c34_mismatches,
            c34_probe,
            {
                "source_arithmetic": c34_detail,
                "citations": [
                    "A runner.py:1445-1461",
                    "P009 v2 pinned blob 1c39ab93:894-917",
                ],
            },
        ),
        (
            "C35",
            "C35-LEGACY-001",
            c35_expected,
            c35_actual,
            c35_mismatches,
            c35_probe,
            {
                "clean_exception": c35_detail["error"],
                "metadata_after_exception": c35_detail["metadata"],
                "citations": [
                    "A runner.py:1049-1060; config.py:10",
                    "P009 v2 pinned blob 1c39ab93:918-937",
                ],
            },
        ),
        (
            "C42",
            "C42-LEGACY-001",
            c42_expected,
            c42_actual,
            c42_mismatches,
            c42_probe,
            {
                "producer_outputs": c42_detail,
                "source_arithmetic": "third RF price 99 is below line 100 while previous direction is 0, so the legacy branch emits one short pulse",
                "citations": [
                    "A signals/range_filter.py:16-92 and signals/supertrend.py:18-55",
                    "P009 v2 pinned blob 1c39ab93:1207-1291",
                ],
            },
        ),
    )
    for row_id, scenario_id, expected, actual, mismatches, probe, detail in specifications:
        if not mismatches:
            raise RowStop(f"{row_id} was expected to preserve an authority contradiction")
        record = {
            "actual": encode_floats(actual),
            "authority": {
                "commit": SOURCE_COMMIT,
                "name": "implementation A at pinned tree",
                "tree_oid": A_TREE_OID,
            },
            "clean_authority_probe": probe,
            "comparison": {
                "compared_expected_leaf_count": leaf_count(expected),
                "expected_leaf_count": leaf_count(expected),
                "mismatches": encode_floats(mismatches),
                "rule": "recursive exact key/value equality after IEEE-754 float.hex encoding",
            },
            "expected": encode_floats(expected),
            "mutation": "NOT_RUN_NO_AUTHORITY_ESTABLISHED_EXPECTED_ROUTE",
            "reason": "frozen manifest expectation contradicts the named frozen producer",
            "row_id": row_id,
            "scenario_id": scenario_id,
            "source_evidence": encode_floats(detail),
            "status": "UNRESOLVED_AUTHORITY_CONTRADICTION",
        }
        record["record_sha256"] = result_hash(record)
        records.append(record)
    return records


def command_build(args: argparse.Namespace) -> int:
    manifest = validate_frozen_inputs()
    requested = args.rows or list(ROW_CONTRACTS)
    if requested != sorted(requested) or requested != list(ROW_CONTRACTS)[: len(requested)]:
        raise RowStop("rows must be a manifest-order prefix of implemented adapters")
    output_dir = Path(args.out).resolve()
    try:
        output_dir.relative_to(GATE_DIR)
    except ValueError as exc:
        raise RowStop("committed row-arm evidence must stay inside the gate package") from exc

    records: list[dict[str, Any]] = []
    for row_id in requested:
        contract = ROW_CONTRACTS[row_id]
        bindings = validate_contract_binding(manifest, contract)
        with tempfile.TemporaryDirectory(prefix=f"p011_{row_id.lower()}_") as temp_name:
            temp_root = Path(temp_name).resolve()
            clean_root, materialized_files = materialize_authority(
                contract, temp_root / "clean"
            )
            clean_target = clean_root / contract.mutation.target
            clean_sha256 = sha256_file(clean_target)
            scratch_root = temp_root / "mutant"
            mutation_application = apply_mutation(clean_root, scratch_root, contract.mutation)
            red = run_child(
                row_id=row_id,
                authority_root=scratch_root,
                authority_file_sha256=mutation_application["after_sha256"],
                mode="mutant",
                mutation_id=contract.mutation.mutation_id,
                scratch_root=scratch_root,
            )
            if red["return_code"] != 1 or (red["parsed_output"] or {}).get("outcome") != "FAIL":
                raise RowStop(f"{row_id} producer mutation did not prove RED: {red}")
            green = run_child(
                row_id=row_id,
                authority_root=clean_root,
                authority_file_sha256=clean_sha256,
                mode="clean",
                mutation_id="NONE_CLEAN_AUTHORITY",
                scratch_root=temp_root,
            )
            if green["return_code"] != 0 or (green["parsed_output"] or {}).get("outcome") != "PASS":
                raise RowStop(f"{row_id} clean producer did not prove GREEN: {green}")
        record = {
            "authority": {
                "citations": list(contract.citations),
                "commit": contract.authority_commit,
                "kind": contract.authority_kind,
                "materialized_files": materialized_files,
                "name": contract.authority_name,
                "tree_oid": contract.authority_tree_oid,
            },
            "contract_binding": bindings,
            "green": green,
            "mutation": {
                "application": mutation_application,
                "mutation_id": contract.mutation.mutation_id,
                "red": red,
            },
            "row_id": row_id,
            "scenario_id": contract.scenario_id,
            "status": "GREEN_AFTER_RED",
        }
        record["record_sha256"] = result_hash(record)
        records.append(record)

    full_build = requested == list(ROW_CONTRACTS)
    unresolved_records = build_unresolved_records(manifest) if full_build else []
    records.extend(unresolved_records)
    records.sort(key=lambda item: item["row_id"])
    by_row = {record["row_id"]: record for record in records}
    corroboration_rows: list[dict[str, Any]] = []
    for row in manifest["rows"]:
        row_id = row["row_id"]
        if row["disposition"] == "NOT_A_LEGACY_REPRODUCTION_ROW":
            corroboration_rows.append(
                {
                    "producer_execution": "NOT_APPLICABLE",
                    "producer_mutation": "NOT_APPLICABLE",
                    "row_id": row_id,
                    "status": "NOT_A_LEGACY_REPRODUCTION_ROW",
                }
            )
        elif row_id in by_row and by_row[row_id]["status"].startswith("UNRESOLVED_"):
            unresolved_status = by_row[row_id]["status"]
            corroboration_rows.append(
                {
                    "evidence_record_sha256": by_row[row_id]["record_sha256"],
                    "producer_execution": (
                        "CLEAN_AUTHORITY_CONTRADICTS_FROZEN_EXPECTATION"
                        if unresolved_status == "UNRESOLVED_AUTHORITY_CONTRADICTION"
                        else "NOT_RUN_NO_EXECUTABLE_PINE_PRODUCER_IN_AUTHORIZED_LANE"
                    ),
                    "producer_mutation": by_row[row_id]["mutation"],
                    "row_id": row_id,
                    "scenario_ids": [by_row[row_id]["scenario_id"]],
                    "status": "STOP",
                    "stop_reason": unresolved_status,
                }
            )
        elif row_id in by_row:
            corroboration_rows.append(
                {
                    "evidence_record_sha256": by_row[row_id]["record_sha256"],
                    "producer_execution": "PASS",
                    "producer_mutation": "RED_THEN_GREEN",
                    "row_id": row_id,
                    "scenario_ids": [by_row[row_id]["scenario_id"]],
                    "status": "GREEN",
                }
            )
        else:
            corroboration_rows.append(
                {
                    "producer_execution": "PENDING_DIRECT_BUILD_ADAPTER",
                    "producer_mutation": "PENDING_DIRECT_BUILD_MUTATION",
                    "row_id": row_id,
                    "scenario_ids": [item["scenario_id"] for item in row["scenarios"]],
                    "status": "STOP",
                }
            )
    counts = {
        "green": sum(item["status"] == "GREEN" for item in corroboration_rows),
        "not_applicable": sum(
            item["status"] == "NOT_A_LEGACY_REPRODUCTION_ROW" for item in corroboration_rows
        ),
        "stop": sum(item["status"] == "STOP" for item in corroboration_rows),
        "total": len(corroboration_rows),
    }
    outcome = "PASS" if counts == {"green": 40, "not_applicable": 2, "stop": 0, "total": 42} else "STOP"
    corroboration = {
        "artifact_schema_version": "P011_ROW_CORROBORATION_v2",
        "counts": counts,
        "gate_version": GATE_VERSION,
        "outcome": outcome,
        "reason": None if outcome == "PASS" else f"row arm partial: {counts['green']} of 40 applicable rows GREEN",
        "rows": corroboration_rows,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    results_path = output_dir / "row_results.jsonl"
    results_path.write_bytes(b"".join(canonical_bytes(record) for record in records))
    unresolved_path = output_dir / "unresolved_rows.json"
    write_json(
        unresolved_path,
        {
            "artifact_schema_version": "P011_UNRESOLVED_ROWS_v1",
            "gate_version": GATE_VERSION,
            "rows": unresolved_records,
        },
    )
    corroboration_path = output_dir / "row_corroboration.json"
    write_json(corroboration_path, corroboration)
    batch_manifest = {
        "artifact_schema_version": "P011_ROW_ARM_BATCH_v1",
        "artifacts": {
            "row_corroboration.json": sha256_file(corroboration_path),
            "row_results.jsonl": sha256_file(results_path),
            "unresolved_rows.json": sha256_file(unresolved_path),
        },
        "authority": {
            "a_commit": SOURCE_COMMIT,
            "a_tree_oid": A_TREE_OID,
            "merged_master_commit": MERGED_MASTER_COMMIT,
            "p009_blob_oid": P009_BLOB_OID,
            "p009_sha256": P009_SHA256,
        },
        "counts": {
            "clean_green": sum(item["status"] == "GREEN_AFTER_RED" for item in records),
            "mutation_red": sum(item["status"] == "GREEN_AFTER_RED" for item in records),
            "unresolved_authority_contradiction": sum(
                item["status"] == "UNRESOLVED_AUTHORITY_CONTRADICTION"
                for item in unresolved_records
            ),
            "unresolved_producer_execution": sum(
                item["status"] == "UNRESOLVED_PRODUCER_EXECUTION"
                for item in unresolved_records
            ),
            **counts,
        },
        "gate_version": GATE_VERSION,
        "legacy_manifest_sha256": LEGACY_MANIFEST_SHA256,
        "outcome": outcome,
        "row_arm_tool_sha256": sha256_file(Path(__file__)),
        "rows_executed": sorted(requested + [item["row_id"] for item in unresolved_records]),
    }
    batch_manifest_path = output_dir / "batch_manifest.json"
    write_json(batch_manifest_path, batch_manifest)
    if "C41" in by_row and by_row["C41"]["status"] == "GREEN_AFTER_RED":
        c41_green = by_row["C41"]["green"]["parsed_output"]
        c41_red = by_row["C41"]["mutation"]["red"]["parsed_output"]
        write_json(
            GATE_DIR / "evidence" / "f3_raw_gated_divergence.json",
            {
                "artifact_schema_version": "P011_F3_RAW_GATED_DIVERGENCE_v1",
                "authority_commit": SOURCE_COMMIT,
                "clean_actual": c41_green["actual"],
                "clean_outcome": c41_green["outcome"],
                "gate_version": GATE_VERSION,
                "mutation_id": "C41-GF8-MUT-001",
                "mutation_mismatches": c41_red["comparison"]["mismatches"],
                "mutation_outcome": c41_red["outcome"],
                "row_record_sha256": by_row["C41"]["record_sha256"],
                "statement": "raw long is true while the frozen HTF gate makes gated long false",
            },
        )
    print(
        json.dumps(
            {
                "artifacts": batch_manifest["artifacts"],
                "command": "build",
                "counts": batch_manifest["counts"],
                "outcome": outcome,
                "output_directory": str(output_dir),
                "rows_executed": batch_manifest["rows_executed"],
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


def command_verify_double_build(args: argparse.Namespace) -> int:
    run1 = Path(args.run1).resolve()
    run2 = Path(args.run2).resolve()
    artifacts: list[dict[str, Any]] = []
    for name in ("row_results.jsonl", "row_corroboration.json", "batch_manifest.json"):
        first = run1 / name
        second = run2 / name
        if not first.is_file() or not second.is_file():
            raise RowStop(f"double-build artifact is missing: {name}")
        first_sha = sha256_file(first)
        second_sha = sha256_file(second)
        artifacts.append(
            {
                "artifact": name,
                "byte_identical": first_sha == second_sha,
                "run1_sha256": first_sha,
                "run2_sha256": second_sha,
            }
        )
    identical = all(item["byte_identical"] for item in artifacts)
    print(
        json.dumps(
            {"artifacts": artifacts, "byte_identical": identical, "outcome": "PASS" if identical else "FAIL"},
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0 if identical else 1


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="WP-P0-11 direct-build legacy row arm")
    sub = root.add_subparsers(dest="command", required=True)

    run_one = sub.add_parser("run-one", help="execute and compare one pinned legacy scenario")
    run_one.add_argument("--row", required=True)
    run_one.add_argument("--manifest", required=True)
    run_one.add_argument("--authority-root", required=True)
    run_one.add_argument("--authority-file-sha256", required=True)
    run_one.add_argument("--dependency-root", required=True)
    run_one.add_argument("--mode", choices=("clean", "mutant"), required=True)
    run_one.add_argument("--mutation-id", required=True)
    run_one.set_defaults(handler=command_run_one)

    build = sub.add_parser("build", help="execute RED/GREEN evidence and write a row-arm batch")
    build.add_argument("--out", required=True)
    build.add_argument("--rows", nargs="*")
    build.set_defaults(handler=command_build)

    contract = sub.add_parser(
        "contract-harness", help="prove scenario identity and required-field checks fail closed"
    )
    contract.add_argument("--out", required=True)
    contract.set_defaults(handler=command_contract_harness)

    double = sub.add_parser("verify-double-build", help="require deterministic row-arm artifacts")
    double.add_argument("--run1", required=True)
    double.add_argument("--run2", required=True)
    double.set_defaults(handler=command_verify_double_build)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return int(args.handler(args))
    except RowFail as exc:
        print(json.dumps({"outcome": "FAIL", "reason": str(exc)}, sort_keys=True, separators=(",", ":")))
        return 1
    except RowStop as exc:
        print(json.dumps({"outcome": "STOP", "reason": str(exc)}, sort_keys=True, separators=(",", ":")))
        return 3
    except Exception as exc:
        print(
            json.dumps(
                {"outcome": "STOP", "reason": f"unhandled {type(exc).__name__}: {exc}"},
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
