from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from scripts.data_parity_guard import sha256_file


def load_registry(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "items": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_registry(path: Path, registry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2), encoding="utf-8")


def upsert_dataset_entry(
    registry: dict,
    dataset: Path,
    *,
    symbol: str = "",
    exchange: str = "",
    timeframe: str = "",
) -> dict:
    digest = sha256_file(dataset)
    key = str(dataset.resolve())
    entry = {
        "dataset": key,
        "sha256": digest,
        "symbol": symbol,
        "exchange": exchange,
        "timeframe": timeframe,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    registry.setdefault("version", 1)
    registry.setdefault("items", {})
    registry["items"][key] = entry
    return entry


def verify_dataset_entry(registry: dict, dataset: Path) -> bool:
    key = str(dataset.resolve())
    items = registry.get("items", {})
    if key not in items:
        raise KeyError(f"Dataset not found in registry: {key}")
    expected = items[key]["sha256"]
    actual = sha256_file(dataset)
    if actual.lower() != expected.lower():
        raise ValueError(f"Checksum mismatch for {key}: expected={expected} actual={actual}")
    return True


def main() -> None:
    p = argparse.ArgumentParser(description="Checksum registry lifecycle tool.")
    p.add_argument("--registry", required=True, help="Registry json path")
    p.add_argument("--dataset", required=True, help="Dataset path")
    p.add_argument("--symbol", default="")
    p.add_argument("--exchange", default="")
    p.add_argument("--timeframe", default="")
    p.add_argument("--update", action="store_true", help="Upsert dataset checksum entry")
    p.add_argument("--verify", action="store_true", help="Verify dataset checksum against registry")
    args = p.parse_args()

    if not args.update and not args.verify:
        raise ValueError("Specify at least one action: --update and/or --verify")

    registry_path = Path(args.registry)
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    registry = load_registry(registry_path)
    if args.update:
        entry = upsert_dataset_entry(
            registry,
            dataset_path,
            symbol=args.symbol,
            exchange=args.exchange,
            timeframe=args.timeframe,
        )
        save_registry(registry_path, registry)
        print(f"Updated registry: {entry['dataset']}")
    if args.verify:
        verify_dataset_entry(registry, dataset_path)
        print("Verify: PASS")


if __name__ == "__main__":
    main()
