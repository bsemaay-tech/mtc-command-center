from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from parity_oracles.common.io_utils import NORMALIZED_FILES, empty_normalized_set, read_csv, read_json, result_payload, utc_now, write_csv, write_json
from parity_oracles.engines.runner_base import parser_for


def main() -> int:
    parser = parser_for("vectorbt")
    parser.add_argument("--signals", type=Path)
    args = parser.parse_args()
    case = read_json(args.case)
    started = utc_now()
    command = f"python parity_oracles/engines/vectorbt_runner.py --case {args.case} --out-dir {args.out_dir}"
    outputs = empty_normalized_set(args.out_dir)
    warnings = ["vectorbt output is a signal execution approximation, not exact MTC execution parity."]
    status = "engine_unavailable"
    errors: list[str] = []
    if args.signals and args.signals.exists():
        signals = read_csv(args.signals)
        trade_rows = []
        trade_id = 1
        position = ""
        for row in signals:
            timestamp = row.get("timestamp", "")
            if row.get("final_long") in {"1", "true", "True"} and position != "long":
                position = "long"
                trade_rows.append({"trade_id": trade_id, "timestamp": timestamp, "bar_index": row.get("bar_index", ""), "event_type": "ENTRY", "side": "long", "reason": "SIGNAL_APPROX"})
                trade_id += 1
            if row.get("final_short") in {"1", "true", "True"} and position != "short":
                position = "short"
                trade_rows.append({"trade_id": trade_id, "timestamp": timestamp, "bar_index": row.get("bar_index", ""), "event_type": "ENTRY", "side": "short", "reason": "SIGNAL_APPROX"})
                trade_id += 1
        filename, fields = NORMALIZED_FILES["trades"]
        target = args.out_dir / filename
        write_csv(target, fields, trade_rows)
        outputs["trades"] = str(target)
        stats = {"trade_count": len(trade_rows), "approximation": True}
        write_json(args.out_dir / "normalized_stats.json", stats)
        outputs["stats"] = str(args.out_dir / "normalized_stats.json")
        status = "success"
    else:
        errors.append("No normalized signal file supplied with --signals.")
    result = result_payload("vectorbt", command, status, case, outputs, started, errors=errors, warnings=warnings)
    write_json(args.out_dir / "result.json", result)
    return 0 if status == "success" else 2


if __name__ == "__main__":
    raise SystemExit(main())
