"""Golden parity fixture generation for the bridge plumbing strategy.

Two paths:

1. REAL (default, task 3b as specified): load the QuantLens dataset named by
   ``MEGA_BUNDLE_MANIFEST`` (or ``--manifest``), run the registered QuantLens
   signal function ``keltner_trail_ema8`` from
   ``MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py`` (read-only
   import — the engine file is the single source of the signal math), apply the
   documented bridge execution transform (close-confirmed signal -> MKT-next
   semantics, UTC 1h 24/7 alignment, runtime ``Z`` timestamps), and emit:
     - ``tests/fixtures/BTC_1h_real.csv``   (the exact bars QuantLens processed)
     - ``tests/fixtures/golden_signals.json`` (the REAL signal list)
   and write the ``golden_run_id`` into
   ``config/strategies/keltner_trail_ema8.yaml``.

2. LEGACY synthetic reference (``generate_golden_from_csv``): the 2026-07-06
   fallback used while the QuantLens registration was blocked (see
   docs/12_GOLDEN_REGEN_ATTEMPT.md). Kept for history; no longer wired to main.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from statistics import mean
from typing import Any

BRIDGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BRIDGE_ROOT.parent
MWF_PATH = REPO_ROOT / "MTC_COMMAND_CENTER" / "03_QUANTLENS" / "tools" / "mega_walk_forward.py"
STRATEGY_ID = "keltner_trail_ema8"
SYMBOL = "BTCUSD"
TIMEFRAME = "1h"
BAR_ALIGNMENT = "UTC_1h_24x7_close_confirmed_mkt_next"


def _rows(path: Path) -> list[dict[str, float | str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return [
            {
                "ts": row["ts"],
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": float(row["volume"]),
            }
            for row in csv.DictReader(handle)
        ]


def _runtime_ts(value: str) -> str:
    return value.replace("+00:00", "Z")


def generate_golden_from_csv(
    csv_path: str | Path,
    kc_length: int = 20,
    kc_mult: float = 2.0,
    atr_length: int = 20,
) -> dict[str, Any]:
    """LEGACY synthetic-fixture reference rule (2026-07-06 fallback). Unused by
    main since the real QuantLens path landed; kept as an independent
    reimplementation of the signal rules for cross-checks."""
    bars = _rows(Path(csv_path))
    signals: list[dict[str, Any]] = []
    last_direction: str | None = None

    true_ranges: list[float] = []
    prev_close: float | None = None
    for bar in bars:
        high = float(bar["high"])
        low = float(bar["low"])
        close = float(bar["close"])
        if prev_close is None:
            tr = high - low
        else:
            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        true_ranges.append(tr)
        prev_close = close

    for idx in range(max(kc_length, atr_length), len(bars)):
        closes = [float(row["close"]) for row in bars[idx - kc_length : idx]]
        atr = mean(true_ranges[idx - atr_length : idx])
        mid = mean(closes)
        upper = mid + kc_mult * atr
        lower = mid - kc_mult * atr
        close = float(bars[idx]["close"])

        direction: str | None = None
        if close > upper:
            direction = "LONG"
        elif close < lower:
            direction = "SHORT"

        if direction and direction != last_direction:
            signals.append(
                {
                    "ts": _runtime_ts(str(bars[idx]["ts"])),
                    "direction": direction,
                    "ref_price": close,
                    "reason": f"close {'above' if direction == 'LONG' else 'below'} keltner",
                }
            )
            last_direction = direction

    return {
        "provisional": True,
        "source": "synthetic_fixture_reference_keltner",
        "bar_alignment": BAR_ALIGNMENT,
        "params": {
            "kc_length": kc_length,
            "kc_mult": kc_mult,
            "atr_length": atr_length,
            "trail_ema": 8,
        },
        "signals": signals,
    }


def _load_mwf(manifest: Path):
    """Import the QuantLens engine module read-only, bound to the manifest."""
    import importlib.util

    os.environ["MEGA_BUNDLE_MANIFEST"] = str(manifest)
    spec = importlib.util.spec_from_file_location("_quantlens_mwf", MWF_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["_quantlens_mwf"] = module
    spec.loader.exec_module(module)
    return module


def _load_params() -> dict[str, Any]:
    import yaml

    cfg = yaml.safe_load(
        (BRIDGE_ROOT / "config" / "strategies" / f"{STRATEGY_ID}.yaml").read_text(encoding="utf-8")
    )
    return dict(cfg["params"])


def generate_real_golden(manifest: Path) -> dict[str, Any]:
    """Run the registered QuantLens signal function on the real dataset and
    apply the bridge execution transform. Returns {golden, df} for emission."""
    mwf = _load_mwf(manifest)
    manifest_data = json.load(open(manifest, encoding="utf-8"))
    ds = mwf.find_ds(manifest_data, SYMBOL, TIMEFRAME)
    if ds is None:
        raise SystemExit(f"dataset {SYMBOL} {TIMEFRAME} not found/PASS in {manifest}")
    df = mwf.load_df(ds["normalized_path"])

    params = _load_params()
    grid = mwf.GRIDS[STRATEGY_ID]
    if len(grid) != 1 or grid[0] != params:
        raise SystemExit(
            f"registry/YAML param mismatch: registry={grid} yaml={params} — refusing to emit golden"
        )

    mwf.build_signals(STRATEGY_ID, df, params)

    # Bridge execution transform: the QuantLens event bar IS the close-confirmed
    # signal bar; the bridge submits MKT on the next bar (mock fills @ next
    # open) — golden records the signal-bar timestamp in runtime 'Z' form.
    signals: list[dict[str, Any]] = []
    for idx in df.index[df["kte8_event"] != 0]:
        direction = "LONG" if int(df.at[idx, "kte8_event"]) == 1 else "SHORT"
        signals.append(
            {
                "ts": _runtime_ts(df.at[idx, "timestamp"].isoformat()),
                "direction": direction,
                "ref_price": float(df.at[idx, "close"]),
                "reason": f"close {'above' if direction == 'LONG' else 'below'} keltner",
            }
        )

    data_start = df["timestamp"].iloc[0].isoformat()
    data_end = df["timestamp"].iloc[-1].isoformat()
    digest = hashlib.sha256(
        json.dumps({"start": data_start, "end": data_end, "signals": signals},
                   sort_keys=True).encode("utf-8")
    ).hexdigest()[:12]
    golden_run_id = f"QL_MEGA_{STRATEGY_ID.upper()}_{SYMBOL}_{TIMEFRAME}_{data_end[:10]}_{digest}"

    golden = {
        "provisional": False,
        "source": "quantlens_mega_walk_forward_registry",
        "golden_run_id": golden_run_id,
        "engine_version": mwf.ENGINE_VERSION,
        "strategy_id": STRATEGY_ID,
        "bar_alignment": BAR_ALIGNMENT,
        "dataset": {
            "manifest": str(manifest),
            "symbol": SYMBOL,
            "timeframe": TIMEFRAME,
            "rows": int(len(df)),
            "start": data_start,
            "end": data_end,
        },
        "params": params,
        "signal_count": len(signals),
        "signals": signals,
    }
    return {"golden": golden, "df": df}


def _write_fixture_csv(df, out_path: Path) -> None:
    out = df[["open", "high", "low", "close", "volume"]].copy()
    out.insert(0, "ts", df["timestamp"].map(lambda t: t.isoformat()))
    out.to_csv(out_path, index=False, lineterminator="\n")


def _write_yaml_run_id(golden_run_id: str) -> Path:
    yaml_path = BRIDGE_ROOT / "config" / "strategies" / f"{STRATEGY_ID}.yaml"
    text = yaml_path.read_text(encoding="utf-8")
    new_text, n = re.subn(
        r'^golden_run_id: ".*"$',
        f'golden_run_id: "{golden_run_id}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n != 1:
        raise SystemExit(f"golden_run_id line not found in {yaml_path}")
    yaml_path.write_text(new_text, encoding="utf-8")
    return yaml_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=os.environ.get("MEGA_BUNDLE_MANIFEST"),
        help="QuantLens dataset manifest (default: env MEGA_BUNDLE_MANIFEST)",
    )
    args = parser.parse_args()
    if not args.manifest:
        raise SystemExit("set MEGA_BUNDLE_MANIFEST or pass --manifest")

    result = generate_real_golden(Path(args.manifest))
    golden = result["golden"]

    fixtures = BRIDGE_ROOT / "tests" / "fixtures"
    fixture_csv = fixtures / "BTC_1h_real.csv"
    golden_path = fixtures / "golden_signals.json"

    _write_fixture_csv(result["df"], fixture_csv)
    golden_path.write_text(json.dumps(golden, indent=2) + "\n", encoding="utf-8")
    yaml_path = _write_yaml_run_id(golden["golden_run_id"])

    print(f"golden_run_id : {golden['golden_run_id']}")
    print(f"signals       : {golden['signal_count']}")
    print(f"bars          : {golden['dataset']['rows']}")
    print(f"fixture_csv   : {fixture_csv}")
    print(f"golden_json   : {golden_path}")
    print(f"yaml_updated  : {yaml_path}")


if __name__ == "__main__":
    main()
