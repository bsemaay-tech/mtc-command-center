from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from parity_oracles.engines.runner_base import parser_for, raw_normalize_result, unavailable_result


def main() -> int:
    parser = parser_for("backtestingpy")
    args = parser.parse_args()
    command = f"python parity_oracles/engines/backtestingpy_runner.py --case {args.case} --out-dir {args.out_dir}"
    warning = "backtesting.py is optional simple sanity checker only; check license before deep integration."
    if args.raw:
        return raw_normalize_result("backtestingpy", args.case, args.out_dir, command, args.raw, warnings=[warning])
    return unavailable_result("backtestingpy", args.case, args.out_dir, command, "No simple backtesting.py strategy is wired for MTC v2 yet. " + warning)


if __name__ == "__main__":
    raise SystemExit(main())
