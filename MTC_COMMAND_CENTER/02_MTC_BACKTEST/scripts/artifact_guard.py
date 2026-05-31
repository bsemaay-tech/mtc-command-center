from __future__ import annotations

import argparse
import csv
from pathlib import Path


def validate_csv(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing artifact: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Corrupt artifact (empty file): {path}")
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError(f"Corrupt artifact (no header): {path}") from None
        if not header:
            raise ValueError(f"Corrupt artifact (blank header): {path}")


def main() -> None:
    p = argparse.ArgumentParser(description="Fail-fast validation for run artifacts.")
    p.add_argument("--required-csv", action="append", default=[], help="Required CSV path(s)")
    args = p.parse_args()
    for item in args.required_csv:
        validate_csv(Path(item))
    print("Artifact guard: PASS")


if __name__ == "__main__":
    main()
