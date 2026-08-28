from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable


GATE_VERSION = "P011-LC-GATE-v1"
SOURCE_COMMIT = "5c5603065c994d545c0eaa8c137fa9edd5cdfc28"
A_TREE_OID = "7aa6f867d821df08a00358adf2dd4400b9c719e8"
LEGACY_MANIFEST_SHA256 = "13075e23bc2db8517320098f38608851cee123fe57026e9e8607db2a5f08eb2b"
MERGED_MASTER_COMMIT = "85c3e17f97efa1ba83ef9c679de319a50ad3be04"
P009_BLOB_OID = "1c39ab939dfcf5589e5ec8fba4af8966947a67fc"
P009_SHA256 = "7d48871a3e45dab118e97969d701912edb5d7c16a4d822d816beca1d03a42249"

GATE_DIR = Path(__file__).resolve().parent
REPO_ROOT = GATE_DIR.parents[2]
A_PYTHON_REL = Path("MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON")
A_PACKAGE_REL = A_PYTHON_REL / "mtc_v2"
A_PYTHON_ROOT = REPO_ROOT / A_PYTHON_REL
MANIFEST_PATH = GATE_DIR / "p011_legacy_manifest.json"
RECEIPT_PATH = GATE_DIR / "P011_GATE_RECEIPT.json"
ANCHOR_PATH = Path(r"C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v1.owner-signed.json")
P009_REL = Path(
    "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/"
    "CAPABILITY_CANONICALIZATION_TABLE.md"
)
P009_PATH = REPO_ROOT / P009_REL


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
}


def validate_frozen_inputs() -> dict[str, Any]:
    if sha256_file(MANIFEST_PATH) != LEGACY_MANIFEST_SHA256:
        raise RowFail("frozen legacy manifest hash differs")
    if not ANCHOR_PATH.is_file():
        raise RowStop("external anchor is absent")
    anchor = load_json(ANCHOR_PATH)
    if anchor.get("legacy_manifest_sha256") != LEGACY_MANIFEST_SHA256:
        raise RowFail("external anchor does not pin the frozen legacy manifest")
    if anchor.get("receipt_sha256") != sha256_file(RECEIPT_PATH):
        raise RowFail("external anchor does not pin the repository receipt")
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
    manifest = load_json(MANIFEST_PATH)
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
        "expected_observation": scenario["literal_expected_observation"] == contract.expected_observation,
        "expected_final_state": scenario["literal_expected_final_state"] == contract.expected_final_state,
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


def resolved_bindings(authority_root: Path) -> list[dict[str, str]]:
    root = authority_root.resolve()
    rows: list[dict[str, str]] = []
    for name, module in sorted(sys.modules.items()):
        if name != "mtc_v2" and not name.startswith("mtc_v2."):
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
        raise RowStop("no implementation A modules were imported")
    return rows


def command_run_one(args: argparse.Namespace) -> int:
    manifest = load_json(Path(args.manifest).resolve())
    contract = ROW_CONTRACTS.get(args.row)
    if contract is None:
        raise RowStop(f"row adapter is not implemented: {args.row}")
    bindings = validate_contract_binding(manifest, contract)
    authority_root = Path(args.authority_root).resolve()
    bind_authority_root(authority_root, contract.mutation.target, args.authority_file_sha256)
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
            "resolved_imports": resolved_bindings(authority_root),
            "tree_oid": contract.authority_tree_oid,
        },
        "comparison": {
            "compared_expected_leaf_count": leaf_count(encoded_expected),
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


def apply_mutation(clean_root: Path, scratch_root: Path, mutation: Mutation) -> dict[str, Any]:
    shutil.copytree(clean_root / "mtc_v2", scratch_root / "mtc_v2")
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
        "stdout": proc.stdout,
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
        clean_target = A_PYTHON_ROOT / contract.mutation.target
        clean_sha256 = sha256_file(clean_target)
        with tempfile.TemporaryDirectory(prefix=f"p011_{row_id.lower()}_") as temp_name:
            scratch_root = Path(temp_name).resolve()
            mutation_application = apply_mutation(A_PYTHON_ROOT, scratch_root, contract.mutation)
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
                authority_root=A_PYTHON_ROOT,
                authority_file_sha256=clean_sha256,
                mode="clean",
                mutation_id="NONE_CLEAN_AUTHORITY",
                scratch_root=None,
            )
            if green["return_code"] != 0 or (green["parsed_output"] or {}).get("outcome") != "PASS":
                raise RowStop(f"{row_id} clean producer did not prove GREEN: {green}")
        record = {
            "authority": {
                "citations": list(contract.citations),
                "commit": contract.authority_commit,
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
    corroboration_path = output_dir / "row_corroboration.json"
    write_json(corroboration_path, corroboration)
    batch_manifest = {
        "artifact_schema_version": "P011_ROW_ARM_BATCH_v1",
        "artifacts": {
            "row_corroboration.json": sha256_file(corroboration_path),
            "row_results.jsonl": sha256_file(results_path),
        },
        "authority": {
            "a_commit": SOURCE_COMMIT,
            "a_tree_oid": A_TREE_OID,
            "merged_master_commit": MERGED_MASTER_COMMIT,
            "p009_blob_oid": P009_BLOB_OID,
            "p009_sha256": P009_SHA256,
        },
        "counts": {
            "clean_green": len(records),
            "mutation_red": len(records),
            **counts,
        },
        "gate_version": GATE_VERSION,
        "legacy_manifest_sha256": LEGACY_MANIFEST_SHA256,
        "outcome": outcome,
        "row_arm_tool_sha256": sha256_file(Path(__file__)),
        "rows_executed": requested,
    }
    batch_manifest_path = output_dir / "batch_manifest.json"
    write_json(batch_manifest_path, batch_manifest)
    print(
        json.dumps(
            {
                "artifacts": batch_manifest["artifacts"],
                "command": "build",
                "counts": batch_manifest["counts"],
                "outcome": outcome,
                "output_directory": str(output_dir),
                "rows_executed": requested,
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
