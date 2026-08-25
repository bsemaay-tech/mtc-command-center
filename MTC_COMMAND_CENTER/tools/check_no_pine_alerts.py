from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ALERT_NEEDLES = (b"alert(", b"alertcondition(")
ALLOWLIST: frozenset[str] = frozenset()


def _one_line(value: object) -> str:
    return " ".join(str(value).splitlines()).strip()


def _relative_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _resolve_repo_root() -> Path | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        print(
            f"PINE_ALERT_GUARD BLOCK reason=git_root_unavailable detail={_one_line(exc)}",
            file=sys.stderr,
        )
        return None

    stdout = result.stdout or ""
    stderr = result.stderr or ""
    if result.returncode != 0 or not stdout.strip():
        detail = stderr.strip() or stdout.strip() or f"rc={result.returncode}"
        print(
            f"PINE_ALERT_GUARD BLOCK reason=git_root_unavailable detail={_one_line(detail)}",
            file=sys.stderr,
        )
        return None

    try:
        root = Path(stdout.strip()).resolve(strict=True)
        if not root.is_dir():
            raise NotADirectoryError(root)
    except OSError as exc:
        print(
            f"PINE_ALERT_GUARD BLOCK reason=git_root_invalid detail={_one_line(exc)}",
            file=sys.stderr,
        )
        return None
    return root


def _pine_files(root: Path) -> tuple[list[Path], list[tuple[str, str]]]:
    candidates: list[Path] = []
    errors: list[tuple[str, str]] = []

    def record_walk_error(exc: OSError) -> None:
        raw_path = Path(exc.filename) if exc.filename else root
        errors.append((_relative_path(root, raw_path), _one_line(exc)))

    for directory, directory_names, file_names in os.walk(
        root,
        topdown=True,
        onerror=record_walk_error,
        followlinks=False,
    ):
        directory_names[:] = sorted(name for name in directory_names if name != ".git")
        for name in sorted(file_names):
            if name.lower().endswith(".pine"):
                candidates.append(Path(directory) / name)

    candidates.sort(key=lambda path: _relative_path(root, path))
    errors.sort()
    return candidates, errors


def main() -> int:
    root = _resolve_repo_root()
    if root is None:
        return 2

    candidates, errors = _pine_files(root)
    violations: list[tuple[str, int]] = []

    for path in candidates:
        relative = _relative_path(root, path)
        try:
            path.stat()
            contents = path.read_bytes()
        except OSError as exc:
            errors.append((relative, _one_line(exc)))
            continue

        match_count = sum(contents.count(needle) for needle in ALERT_NEEDLES)
        if match_count and relative not in ALLOWLIST:
            violations.append((relative, match_count))

    for relative, match_count in violations:
        print(f"PINE_ALERT_GUARD VIOLATION path={relative} matches={match_count}")

    if errors:
        for relative, detail in sorted(errors):
            print(
                f"PINE_ALERT_GUARD UNEVALUATED path={relative} detail={detail}",
                file=sys.stderr,
            )
        print(
            "PINE_ALERT_GUARD BLOCK "
            f"files={len(candidates)} matches={sum(count for _, count in violations)} "
            f"allowlist={len(ALLOWLIST)} errors={len(errors)}",
            file=sys.stderr,
        )
        return 2

    total_matches = sum(count for _, count in violations)
    if violations:
        print(
            "PINE_ALERT_GUARD BLOCK "
            f"files={len(candidates)} matches={total_matches} allowlist={len(ALLOWLIST)}"
        )
        return 1

    print(
        "PINE_ALERT_GUARD PASS "
        f"files={len(candidates)} matches=0 allowlist={len(ALLOWLIST)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
