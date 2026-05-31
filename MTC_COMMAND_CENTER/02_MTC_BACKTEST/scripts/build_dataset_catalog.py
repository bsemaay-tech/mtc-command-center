from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from src.data.io import list_datasets


def build_catalog(data_dir: Path) -> list[dict]:
    rows = list_datasets(str(data_dir))
    out: list[dict] = []
    for r in rows:
        out.append(
            {
                "filename": r.get("filename"),
                "symbol": r.get("symbol"),
                "timeframe": r.get("timeframe"),
                "format": r.get("format"),
                "size_bytes": r.get("size_bytes"),
                "bar_count": r.get("bar_count"),
                "start_date": str(r.get("start_date")) if r.get("start_date") is not None else "",
                "end_date": str(r.get("end_date")) if r.get("end_date") is not None else "",
                "path": r.get("path"),
            }
        )
    return out


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "filename",
                "symbol",
                "timeframe",
                "format",
                "size_bytes",
                "bar_count",
                "start_date",
                "end_date",
                "path",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    p = argparse.ArgumentParser(description="Build dataset catalog inventory.")
    p.add_argument("--data-dir", default="data")
    p.add_argument("--out-json", required=True)
    p.add_argument("--out-csv", required=True)
    args = p.parse_args()

    rows = build_catalog(Path(args.data_dir))
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    write_csv(Path(args.out_csv), rows)
    print(f"Catalog written: {out_json} ({len(rows)} datasets)")


if __name__ == "__main__":
    main()
