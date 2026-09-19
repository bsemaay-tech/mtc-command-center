"""D026-style mutant driver for the exact T0 read of b4df1413 (read-only against the worktree).

Each mutant is a literal text replacement on a fresh copy of the scratch base; the named checker is
then run with the interpreter given on the command line and the failing/erroring test ids printed.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent / "base"
WORK = Path(__file__).resolve().parent / "mut"

EXPORTER = "p030_archive_exporter.py"
ADAPTER = "p030_closed_partition_backup_adapter.py"
EXPORTER_CHECK = "check_p030_archive_exporter.py"
ADAPTER_CHECK = "check_p030_closed_partition_backup_adapter.py"

E_WALK_GUARD = """    except RecursionError as exc:
        # which layer raises first depends on the interpreter (the parser's C recursion limit
        # differs between versions; this walk hits the Python recursion limit), so the checker
        # derives one depth per layer at test time instead of hard-coding one (slice read F-1)
        raise ExportRefused(
            "source_line_invalid", f"source line {line_number} is nested too deeply"
        ) from exc
"""

E_RECEIPT_RACE = """    except FileExistsError as exc:
        raise ExportRefused(
            "receipt_exists",
            "export receipt appeared before publication; nothing was replaced (the staging "
            f"receipt remains under {staging_receipt.name})",
        ) from exc
"""

E_TARGET_RACE = """    except FileExistsError as exc:
        raise ExportRefused(
            "target_exists",
            "target partition appeared before publication; nothing was replaced (the receipt was "
            f"published; the staging partial remains under {staging_target.name})",
        ) from exc
"""

A_JSON_OBJECT_WALK = """    try:
        _reject_nonfinite_numbers(payload)
    except RecursionError as exc:
        # the parser may accept a nesting the (recursive) walk cannot; same refusal (P0-30 N4)
        raise ValueError(f"invalid {description}") from exc
"""

A_JSONL_WALK = """        try:
            _reject_nonfinite_numbers(record)
        except RecursionError as exc:
            # the parser may accept a nesting the (recursive) walk cannot; same refusal (P0-30 N4)
            raise ValueError(f"invalid {description} line {line_number}") from exc
"""

A_PREFIX_WALK = """        try:
            _reject_nonfinite_numbers(record)
        except RecursionError as exc:
            # the parser may accept a nesting the (recursive) walk cannot; same refusal (P0-30 N4)
            raise ValueError("prefix record is not canonical JSONL") from exc
"""

MUTANTS = {
    # (file, old, new, checker)
    "E1-exporter-walk-guard-removed": (
        EXPORTER,
        E_WALK_GUARD,
        "",
        EXPORTER_CHECK,
    ),
    "E2-exporter-parser-clause-removed": (
        EXPORTER,
        "        ValueError,\n        RecursionError,\n",
        "        ValueError,\n",
        EXPORTER_CHECK,
    ),
    "E3-publish-back-to-os.replace-on-windows": (
        EXPORTER,
        '    if os.name == "nt":\n        os.rename(staging, final)',
        '    if os.name == "nt":\n        os.replace(staging, final)',
        EXPORTER_CHECK,
    ),
    "E4-receipt-side-FileExistsError-arm-removed": (
        EXPORTER,
        E_RECEIPT_RACE,
        "",
        EXPORTER_CHECK,
    ),
    "E5-target-side-FileExistsError-arm-removed": (
        EXPORTER,
        E_TARGET_RACE,
        "",
        EXPORTER_CHECK,
    ),
    "E6-receipt-exported_sha256-over-other-bytes": (
        EXPORTER,
        "        exported_sha256=hashlib.sha256(exported).hexdigest(),",
        "        exported_sha256=hashlib.sha256(source_bytes).hexdigest(),",
        EXPORTER_CHECK,
    ),
    "A1-adapter-_decode_json_object-parser-clause-removed": (
        ADAPTER,
        "    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:\n        # RecursionError: nested deeper than the interpreter limit is invalid too (P0-30 N4; this\n        # is the adapter's third parse site, slice read F-2)\n",
        "    except (UnicodeDecodeError, json.JSONDecodeError) as exc:\n",
        ADAPTER_CHECK,
    ),
    "A2-adapter-_decode_json_object-walk-guard-removed": (
        ADAPTER,
        A_JSON_OBJECT_WALK,
        "    _reject_nonfinite_numbers(payload)\n",
        ADAPTER_CHECK,
    ),
    "A3-adapter-_decode_strict_jsonl-parser-clause-removed": (
        ADAPTER,
        "        except (json.JSONDecodeError, RecursionError) as exc:\n            # RecursionError: nested deeper than the interpreter limit is invalid too (P0-30 N4)\n",
        "        except json.JSONDecodeError as exc:\n",
        ADAPTER_CHECK,
    ),
    "A4-adapter-_decode_strict_jsonl-walk-guard-removed": (
        ADAPTER,
        A_JSONL_WALK,
        "        _reject_nonfinite_numbers(record)\n",
        ADAPTER_CHECK,
    ),
    "A5-adapter-_prefix_facts-parser-clause-removed": (
        ADAPTER,
        "        except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:\n            raise ValueError(\"prefix record is not canonical JSONL\") from exc\n",
        "        except (UnicodeDecodeError, json.JSONDecodeError) as exc:\n            raise ValueError(\"prefix record is not canonical JSONL\") from exc\n",
        ADAPTER_CHECK,
    ),
    "A6-adapter-_prefix_facts-walk-guard-removed": (
        ADAPTER,
        A_PREFIX_WALK,
        "        _reject_nonfinite_numbers(record)\n",
        ADAPTER_CHECK,
    ),
}


def run(name: str, python: str) -> None:
    target_file, old, new, checker = MUTANTS[name]
    if WORK.exists():
        shutil.rmtree(WORK)
    shutil.copytree(BASE, WORK)
    path = WORK / target_file
    with path.open("r", encoding="utf-8", newline="") as handle:
        text = handle.read()
    count = text.count(old)
    if count != 1:
        print(f"{name}: MUTATION ANCHOR NOT UNIQUE (count={count}) -- ABORT")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text.replace(old, new, 1))
    proc = subprocess.run(
        [python, checker],
        cwd=WORK,
        capture_output=True,
        text=True,
        errors="replace",
    )
    log = proc.stdout + proc.stderr
    bad = sorted(set(re.findall(r"^(?:ERROR|FAIL): (\S+).*$", log, flags=re.M)))
    tail = [
        line
        for line in log.splitlines()
        if line.startswith("Ran ") or line in {"OK"} or line.startswith("FAILED")
    ]
    subtests = sorted(
        set(re.findall(r"^(?:ERROR|FAIL): \S+ \[(.*?)\]", log, flags=re.M))
    )
    exc = sorted(
        set(
            re.findall(
                r"^(RecursionError|AssertionError|p030_archive_exporter\.ExportRefused|ValueError)",
                log,
                flags=re.M,
            )
        )
    )
    print(f"{name}\n  checker={checker} exit={proc.returncode} {' | '.join(tail)}")
    print(f"  failing tests ({len(bad)}): {bad}")
    if subtests:
        print(f"  subtest params: {subtests}")
    print(f"  exception kinds seen: {exc}")


if __name__ == "__main__":
    python = sys.argv[1]
    names = sys.argv[2:] or list(MUTANTS)
    for name in names:
        run(name, python)
