"""Verify WP-P0-10 fixture integrity, targeted RED/GREEN, and oracle rendering."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


AUTH_PREFIX = (
    "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/"
    "CAPABILITY_CANONICALIZATION_TABLE.md:"
)


def canonical_bytes(mapping: dict[str, object]) -> bytes:
    """Render the fixture comparison seam in its declared canonical form."""

    text = json.dumps(
        mapping,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return (text + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(
        (args.fixture_dir / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["family_count"] == 25
    assert manifest["built_count"] == 23
    assert manifest["blocked_count"] == 2
    assert manifest["blocked_family_numbers"] == [18, 19]
    assert manifest["built_family_numbers"] == (
        list(range(1, 18)) + list(range(20, 26))
    )

    blocked_entries = [
        item for item in manifest["families"] if item["status"] == "BLOCKED"
    ]
    assert [item["number"] for item in blocked_entries] == [18, 19]
    for blocked in blocked_entries:
        assert blocked["missing_semantics"]
        assert blocked["unblocks_when"]

    red = 0
    green = 0
    for manifest_item in manifest["families"]:
        if manifest_item["status"] != "BUILT":
            continue

        path = args.fixture_dir / manifest_item["fixture"]
        fixture = json.loads(path.read_text(encoding="utf-8"))
        number = fixture["family"]["number"]
        assert number == manifest_item["number"]

        assertions = fixture["expected_output"]["assertions"]
        expected: dict[str, object] = {}
        for item in assertions:
            assert item["path"] not in expected
            assert item["citations"]
            assert all(
                value.startswith(AUTH_PREFIX) for value in item["citations"]
            )
            expected[item["path"]] = item["value"]

        expected_bytes = canonical_bytes(expected)
        expected_sha = hashlib.sha256(expected_bytes).hexdigest()
        assert expected_sha == fixture["expected_output"]["sha256"]

        state = {
            key: value for key, value in expected.items() if key.startswith("state.")
        }
        assert state
        state_sha = hashlib.sha256(canonical_bytes(state)).hexdigest()
        assert state_sha == fixture["expected_output"]["final_state_sha256"]

        output_path = args.output_dir / f"family_{number:02d}.output.json"
        output_path.write_bytes(expected_bytes)

        mutation = fixture["deliberate_mutation"]
        target = mutation["target"]
        assert target in expected
        assert expected[target] == mutation["from"]
        assert mutation["to"] != mutation["from"]
        assert mutation["citation"].startswith(AUTH_PREFIX)

        candidate = dict(expected)
        candidate[target] = mutation["to"]
        mismatches = [
            key for key in sorted(expected) if candidate.get(key) != expected[key]
        ]
        assert mismatches == [target]
        red += 1
        print(
            f"FAMILY {number:02d} RED mismatch_count=1 path={target} "
            f"expected={json.dumps(expected[target], ensure_ascii=False, separators=(',', ':'))} "
            f"actual={json.dumps(candidate[target], ensure_ascii=False, separators=(',', ':'))}"
        )

        candidate[target] = mutation["from"]
        assert candidate == expected
        print(
            f"FAMILY {number:02d} RESTORED path={target} "
            f"value={json.dumps(candidate[target], ensure_ascii=False, separators=(',', ':'))}"
        )
        assert canonical_bytes(candidate) == expected_bytes
        green += 1
        print(
            f"FAMILY {number:02d} GREEN byte_match=true sha256={expected_sha}"
        )

    print(
        f"SUMMARY built=23 blocked=2 red={red} restored={red} green={green}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
