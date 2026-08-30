"""Print the current WP-P0-10 declaration-inventory measurements."""

from __future__ import annotations

import argparse
from pathlib import Path

from verify_fixtures import (
    declaration_inventory_measurements,
    load_built_fixtures,
    load_json,
    validate_manifest,
)


FIXTURE_DIR = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture_dir", nargs="?", type=Path, default=FIXTURE_DIR)
    args = parser.parse_args()

    manifest = load_json(args.fixture_dir / "manifest.json")
    families = validate_manifest(manifest)
    fixtures = load_built_fixtures(args.fixture_dir, families)
    digest, record_count, input_path_count = declaration_inventory_measurements(
        list(fixtures.values())
    )
    print(f"declaration_inventory_sha256={digest}")
    print(f"declaration_inventory_record_count={record_count}")
    print(f"declaration_inventory_input_path_count={input_path_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
