from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from parity_oracles.engines.runner_base import parser_for, raw_normalize_result, unavailable_result


def main() -> int:
    parser = parser_for("pynecore")
    args = parser.parse_args()
    command = f"python parity_oracles/engines/pynecore_runner.py --case {args.case} --out-dir {args.out_dir}"
    if args.raw:
        return raw_normalize_result("pynecore", args.case, args.out_dir, command, args.raw)
    if shutil.which("pynecore") is None:
        return unavailable_result("pynecore", args.case, args.out_dir, command, "PyneCore CLI not found. Experimental oracle is unavailable until isolated POC install succeeds.")
    return unavailable_result("pynecore", args.case, args.out_dir, command, "PyneCore CLI detected, but MTC manual translation POC is not wired to this case yet.")


if __name__ == "__main__":
    raise SystemExit(main())
