#!/usr/bin/env python3
"""Offline lock/venv verifier for the Linux deployment package.

It validates that every lock entry is exact and hashed. When run from the
target venv with ``--check-installed``, it also proves the installed
distribution set and versions equal the lock (apart from venv bootstrap tools).
No package index or other network endpoint is contacted.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import re
import sys
from pathlib import Path

ENTRY_RE = re.compile(r"^([A-Za-z0-9_.-]+(?:\[[^]]+\])?)==([^\s\\]+)\s*\\$")
HASH_RE = re.compile(r"^\s+--hash=sha256:[0-9a-f]{64}(?:\s*\\)?$")
FORBIDDEN_RE = re.compile(r"(?:https?://|git\+|@\s|--index-url|--extra-index-url|--find-links)")
BOOTSTRAP_DISTRIBUTIONS = {"pip", "setuptools"}


def canonical_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_lock(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if FORBIDDEN_RE.search(text):
        raise ValueError("lock contains a URL, VCS reference, or index override")

    lines = text.splitlines()
    expected: dict[str, str] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line or line.lstrip().startswith("#") or line[:1].isspace():
            index += 1
            continue
        match = ENTRY_RE.fullmatch(line)
        if not match:
            raise ValueError(f"unrecognized or unpinned lock entry on line {index + 1}")
        raw_name, version = match.groups()
        name = canonical_name(raw_name.split("[", 1)[0])
        if name in expected:
            raise ValueError(f"duplicate lock entry: {name}")
        expected[name] = version

        index += 1
        hashes = 0
        while index < len(lines) and lines[index][:1].isspace():
            candidate = lines[index]
            if candidate.lstrip().startswith("--hash="):
                if not HASH_RE.fullmatch(candidate):
                    raise ValueError(f"invalid hash on line {index + 1}")
                hashes += 1
            index += 1
        if hashes == 0:
            raise ValueError(f"lock entry has no hash: {name}")
    if not expected:
        raise ValueError("lock has no package entries")
    return expected


def installed_distributions() -> dict[str, str]:
    installed: dict[str, str] = {}
    for dist in importlib.metadata.distributions():
        name = dist.metadata.get("Name")
        if name:
            installed[canonical_name(name)] = dist.version
    return installed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", required=True, type=Path)
    parser.add_argument("--check-installed", action="store_true")
    args = parser.parse_args()
    try:
        expected = parse_lock(args.lock)
        if args.check_installed:
            installed = installed_distributions()
            missing = sorted(name for name in expected if installed.get(name) != expected[name])
            extras = sorted(set(installed) - set(expected) - BOOTSTRAP_DISTRIBUTIONS)
            if missing or extras:
                details = []
                if missing:
                    details.append("missing-or-wrong=" + ",".join(missing))
                if extras:
                    details.append("unexpected=" + ",".join(extras))
                raise ValueError("; ".join(details))
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"verify_lock: FAIL: {exc}", file=sys.stderr)
        return 1
    mode = "lock+installed" if args.check_installed else "lock"
    print(f"verify_lock: PASS: {mode}; packages={len(expected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
