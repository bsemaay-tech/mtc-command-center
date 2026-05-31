from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from parity_oracles.common.io_utils import ROOT, empty_normalized_set, read_json, result_payload, utc_now, write_json
from parity_oracles.normalizers.base import normalize


def unavailable_result(engine_name: str, case_path: Path, out_dir: Path, command: str, reason: str) -> int:
    case = read_json(case_path)
    started = utc_now()
    outputs = empty_normalized_set(out_dir)
    result = result_payload(engine_name, command, "engine_unavailable", case, outputs, started, errors=[reason])
    write_json(out_dir / "result.json", result)
    return 2


def raw_normalize_result(engine_name: str, case_path: Path, out_dir: Path, command: str, raw: Path | None, warnings: list[str] | None = None) -> int:
    case = read_json(case_path)
    started = utc_now()
    outputs = normalize(raw, out_dir, engine_name)
    result = result_payload(engine_name, command, "stub" if raw is None else "success", case, outputs, started, warnings=warnings or [])
    write_json(out_dir / "result.json", result)
    return 0


def find_command(command: str) -> bool:
    try:
        completed = subprocess.run(["where.exe", command], capture_output=True, text=True, check=False)
        return completed.returncode == 0
    except OSError:
        return False


def parser_for(engine_name: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"Run {engine_name} oracle for an MTC parity case.")
    parser.add_argument("--case", type=Path)
    parser.add_argument("--case-plan", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--raw", type=Path)
    return parser
