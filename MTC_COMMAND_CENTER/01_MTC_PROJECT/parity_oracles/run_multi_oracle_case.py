from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from parity_oracles.common.io_utils import ROOT, read_json, utc_now, write_json


ENGINE_COMMANDS = {
    "python_engine": "parity_oracles/engines/python_engine_runner.py",
    "pinets": "parity_oracles/engines/pinets_runner.py",
    "pynecore": "parity_oracles/engines/pynecore_runner.py",
    "vectorbt": "parity_oracles/engines/vectorbt_runner.py",
    "backtestingpy": "parity_oracles/engines/backtestingpy_runner.py",
}


def run_command(args: list[str]) -> dict[str, object]:
    completed = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    return {
        "command": " ".join(args),
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def compare(case_path: Path, baseline: str, candidate: str, level: str) -> dict[str, object]:
    return run_command([
        "python",
        "parity_oracles/compare/parity_compare.py",
        "--case",
        str(case_path),
        "--baseline",
        baseline,
        "--candidate",
        candidate,
        "--level",
        level,
    ])


def _case_plan_from_case(case: dict[str, object]) -> Path | None:
    config = case.get("mtc_config", {})
    if isinstance(config, dict):
        source = config.get("source")
        if source:
            path = ROOT / str(source)
            if path.exists():
                return path
    return None


def run_fast_suite_surfaces(case_path: Path, case: dict[str, object], out_dir: Path) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    case_plan = _case_plan_from_case(case)
    if str(case.get("case_id")) != "case_001" or case_plan is None:
        return [], []
    runs = [
        run_command([
            "python",
            ENGINE_COMMANDS["python_engine"],
            "--case-plan",
            str(case_plan),
            "--out-dir",
            str(out_dir / "python_engine_export_workbook"),
            "--config-source",
            "export_workbook",
        ]),
        run_command([
            "python",
            ENGINE_COMMANDS["python_engine"],
            "--case-plan",
            str(case_plan),
            "--out-dir",
            str(out_dir / "python_engine_case_plan"),
            "--config-source",
            "case_plan_overrides",
        ]),
        run_command([
            "python",
            ENGINE_COMMANDS["pinets"],
            "--case-plan",
            str(case_plan),
            "--out-dir",
            str(out_dir / "pinets_full_adapter"),
            "--adapter-mode",
            "full",
        ]),
        run_command([
            "python",
            ENGINE_COMMANDS["pinets"],
            "--case-plan",
            str(case_plan),
            "--out-dir",
            str(out_dir / "pinets_supertrend_only"),
            "--adapter-mode",
            "supertrend",
        ]),
    ]
    comparisons: list[dict[str, object]] = []
    for level in ["L1", "L2"]:
        comparisons.append(compare(case_path, "python_engine_export_workbook", "pinets_full_adapter", level))
        comparisons.append(compare(case_path, "python_engine_case_plan", "pinets_supertrend_only", level))
    return runs, comparisons


def _compare_result(command_result: dict[str, object]) -> dict[str, object]:
    stdout = str(command_result.get("stdout", ""))
    for line in reversed([item.strip() for item in stdout.splitlines() if item.strip()]):
        path = Path(line)
        if path.suffix == ".json" and path.exists():
            return read_json(path)
    return {}


def write_summary(case: dict[str, object], runs: list[dict[str, object]], compares: list[dict[str, object]], out_dir: Path) -> None:
    result_paths = sorted(out_dir.glob("*/result.json"))
    engine_versions = []
    for path in result_paths:
        payload = read_json(path)
        engine_versions.append((payload.get("engine_name", path.parent.name), payload.get("engine_version", "unknown"), payload.get("status", "unknown")))
    lines = [
        "# Multi Oracle Parity Summary",
        "",
        "## A. Case metadata",
        "",
        f"- case_id: `{case.get('case_id')}`",
        f"- symbol: `{case.get('symbol')}`",
        f"- timeframe: `{case.get('timeframe')}`",
        f"- exchange: `{case.get('exchange')}`",
        "",
        "## B. Engine versions",
        "",
    ]
    for name, version, status in engine_versions:
        lines.append(f"- {name}: {version} ({status})")
    lines.extend([
        "",
        "## C. Data hash / config hash / code hash",
        "",
        "- See per-engine `result.json` files.",
        "",
        "## D. Run status table",
        "",
        "| Command | Return code |",
        "|---|---:|",
    ])
    for run in runs:
        lines.append(f"| `{run['command']}` | {run['returncode']} |")
    sections = [
        ("E", "L0 data parity result"),
        ("F", "L1 indicator parity result"),
        ("G", "L2 raw signal parity result"),
        ("H", "L3 transformed signal parity result"),
        ("I", "L4 entry decision parity result"),
        ("J", "L5 trade execution parity result"),
        ("K", "L6 stats parity result"),
    ]
    for letter, title in sections:
        lines.extend(["", f"## {letter}. {title}", ""])
        related = [item for item in compares if f" --level {title.split()[0]} " in f" {item['command']} "]
        if related:
            for item in related:
                lines.append(f"- `{item['command']}` returncode={item['returncode']}")
        else:
            lines.append("- NOT_COMPARABLE or not requested in this run.")
    lines.extend([
        "",
        "## L. First divergence analysis",
        "",
        "- See generated comparison JSON files for first divergence tables.",
        "",
        "## M. Suspected cause",
        "",
        "- Inferred per level by comparator when mismatches exist.",
        "",
        "## N. Recommended next action",
        "",
        "- Wire the existing Python engine to emit all normalized CSV files, then promote PineTS L1/L2 cases into FAST_SUITE.",
        "",
        "## O. Verdict",
        "",
        "- NOT_COMPARABLE until real engine outputs are normalized and compared.",
    ])
    surface_rows = []
    for item in compares:
        payload = _compare_result(item)
        baseline = str(payload.get("baseline", ""))
        candidate = str(payload.get("candidate", ""))
        if baseline == "python_engine_export_workbook":
            surface = "export_workbook"
        elif baseline == "python_engine_case_plan":
            surface = "case_plan_overrides"
        else:
            continue
        surface_rows.append((surface, baseline, candidate, payload))
    if surface_rows:
        lines.extend([
            "",
            "## P. FAST_SUITE Surface Gate",
            "",
            "| Surface | Baseline | Candidate | Level | Verdict | Matched | Mismatched | First divergence |",
            "|---|---|---|---|---|---:|---:|---|",
        ])
        for surface, baseline, candidate, payload in surface_rows:
            stem = f"{baseline}_vs_{candidate}_{payload.get('level')}"
            lines.append(
                f"| {surface} | `{baseline}` | `{candidate}` | {payload.get('level')} | "
                f"{payload.get('verdict')} | {payload.get('matched')} | {payload.get('mismatched')} | "
                f"{payload.get('first_divergence_timestamp') or 'None'} |"
            )
            lines.append(f"| report | `{stem}` |  |  |  |  |  |  |")
    (out_dir / "MULTI_ORACLE_PARITY_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--engines", nargs="+", required=True)
    parser.add_argument("--baseline", required=True)
    args = parser.parse_args()
    case = read_json(args.case)
    case_id = str(case["case_id"])
    out_dir = ROOT / "reports" / "parity" / case_id
    out_dir.mkdir(parents=True, exist_ok=True)
    runs = []
    for engine in args.engines:
        engine_out = out_dir / engine
        engine_out.mkdir(parents=True, exist_ok=True)
        command = ["python", ENGINE_COMMANDS[engine], "--case", str(args.case), "--out-dir", str(engine_out)]
        if engine == "vectorbt":
            signal_path = out_dir / "pinets" / "normalized_signals.csv"
            command.extend(["--signals", str(signal_path)])
        runs.append(run_command(command))
    if {"python_engine", "pinets"}.issubset(set(args.engines)):
        surface_runs, surface_comparisons = run_fast_suite_surfaces(args.case, case, out_dir)
        runs.extend(surface_runs)
    else:
        surface_comparisons = []
    comparisons = []
    matrix = [
        ("python_engine", "pinets", ["L1", "L2", "L3"]),
        ("python_engine", "pynecore", ["L1", "L2", "L3", "L4", "L5", "L6"]),
        ("pinets", "pynecore", ["L1", "L2"]),
        ("python_engine", "vectorbt", ["L5", "L6"]),
    ]
    for baseline, candidate, levels in matrix:
        if baseline in args.engines and candidate in args.engines:
            for level in levels:
                comparisons.append(compare(args.case, baseline, candidate, level))
    comparisons.extend(surface_comparisons)
    write_summary(case, runs, comparisons, out_dir)
    manifest = {"case_id": case_id, "generated_at": utc_now(), "runs": runs, "comparisons": comparisons}
    write_json(out_dir / "multi_oracle_manifest.json", manifest)
    print(out_dir / "MULTI_ORACLE_PARITY_SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
