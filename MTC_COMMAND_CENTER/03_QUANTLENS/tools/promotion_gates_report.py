"""Report-only promotion diagnostics; this module changes no admission decision."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any, Mapping


DSR_THRESHOLD = 0.95
BH_FDR_AUTHORITY_SOURCE = "PROMOTION_REPORT_ONLY_DECISION.md:134-140"
CHECK_ORDER = (
    "dsr",
    "bh_fdr",
    "robust_final",
    "positive_raw_lockbox_excess",
)
STATUS_ORDER = ("PASS", "FAIL", "STOP")
REPORT_FILENAME = re.compile(r"^promotion_gates_report(?:[-_][A-Za-z0-9._-]+)?\.json$")
FENCED_FILENAMES = {
    "score_all_gates.py",
    "build_forward_paper_queue.py",
    "build_strategy_research_registry.py",
    "promotion_index.md",
    "promotion_registry.json",
    "producer_spec.json",
}


class OutputRefused(ValueError):
    """Raised before any write when an output target crosses the report fence."""


def _is_finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _verdict(
    status: str,
    code: str,
    message: str,
    values: Mapping[str, Any],
    evidence_source_paths: list[str],
) -> dict[str, Any]:
    return {
        "status": status,
        "reason": {"code": code, "message": message},
        "values": dict(values),
        "evidence_source_paths": evidence_source_paths,
    }


def _evaluate_dsr(candidate: Mapping[str, Any], evidence_prefix: str) -> dict[str, Any]:
    p_value = candidate.get("dsr_p_value")
    robust = candidate.get("dsr_robust")
    paths = [f"{evidence_prefix}/dsr_p_value", f"{evidence_prefix}/dsr_robust"]
    values = {"dsr_p_value": p_value, "dsr_robust": robust}

    if not _is_finite_number(p_value):
        code = "DSR_P_VALUE_MISSING" if p_value is None else "DSR_P_VALUE_NOT_FINITE"
        return _verdict("STOP", code, "dsr_p_value is missing or not finite", values, paths)
    if not isinstance(robust, bool):
        return _verdict(
            "STOP",
            "DSR_FLAG_MISSING_OR_INVALID",
            "dsr_robust is missing or is not a boolean",
            values,
            paths,
        )

    value_passes = p_value >= DSR_THRESHOLD
    if value_passes != robust:
        return _verdict(
            "STOP",
            "DSR_VALUE_FLAG_DISAGREEMENT",
            "dsr_p_value and dsr_robust disagree",
            values,
            paths,
        )
    if value_passes:
        return _verdict(
            "PASS",
            "DSR_AT_OR_ABOVE_THRESHOLD",
            "dsr_p_value is at least 0.95 and dsr_robust is true",
            values,
            paths,
        )
    return _verdict(
        "FAIL",
        "DSR_BELOW_THRESHOLD",
        "dsr_p_value is below 0.95 and dsr_robust is false",
        values,
        paths,
    )


def _evaluate_bh_fdr(candidate: Mapping[str, Any], evidence_prefix: str) -> dict[str, Any]:
    """Report STOP until an independently enumerated complete family exists."""

    return _verdict(
        "STOP",
        "BH_COMPLETE_FAMILY_MANIFEST_MISSING",
        "no complete independently enumerated BH family manifest exists",
        {
            "boot_p_value": candidate.get("boot_p_value"),
            "bh_fdr_survivor": candidate.get("bh_fdr_survivor"),
        },
        [
            BH_FDR_AUTHORITY_SOURCE,
            f"{evidence_prefix}/boot_p_value",
            f"{evidence_prefix}/bh_fdr_survivor",
        ],
    )


def _evaluate_robust_final(
    candidate: Mapping[str, Any],
    dsr: Mapping[str, Any],
    bh_fdr: Mapping[str, Any],
    evidence_prefix: str,
) -> dict[str, Any]:
    stored = candidate.get("robust_final")
    classification = candidate.get("classification")
    classification_status = (
        "PASS"
        if classification in {"PASS", "STRONG_PASS"}
        else "FAIL"
        if isinstance(classification, str) and classification
        else "STOP"
    )
    values = {
        "robust_final": stored,
        "classification": classification,
        "dsr_status": dsr["status"],
        "bh_fdr_status": bh_fdr["status"],
    }
    paths = [
        f"{evidence_prefix}/robust_final",
        f"{evidence_prefix}/classification",
        *dsr["evidence_source_paths"],
        *bh_fdr["evidence_source_paths"],
    ]

    if not isinstance(stored, bool):
        return _verdict(
            "STOP",
            "ROBUST_FINAL_MISSING_OR_INVALID",
            "robust_final is missing or is not a boolean",
            values,
            paths,
        )

    dependencies = (classification_status, dsr["status"], bh_fdr["status"])
    if "STOP" in dependencies:
        return _verdict(
            "STOP",
            "ROBUST_FINAL_DEPENDENCY_STOP",
            "robust_final cannot be evaluated while a source input is STOP",
            values,
            paths,
        )

    all_pass = all(status == "PASS" for status in dependencies)
    if stored and all_pass:
        return _verdict(
            "PASS",
            "ROBUST_FINAL_CONSISTENT_PASS",
            "robust_final is true and all independently evaluated inputs pass",
            values,
            paths,
        )
    if not stored and not all_pass:
        return _verdict(
            "FAIL",
            "ROBUST_FINAL_CONSISTENT_FAIL",
            "robust_final is false and at least one independently evaluated input fails",
            values,
            paths,
        )
    return _verdict(
        "STOP",
        "ROBUST_FINAL_INPUT_CONTRADICTION",
        "robust_final contradicts its independently evaluated inputs",
        values,
        paths,
    )


def _binding_is_complete(binding: Any) -> bool:
    if not isinstance(binding, Mapping):
        return False
    if not isinstance(binding.get("symbol"), str) or not binding["symbol"]:
        return False
    if not isinstance(binding.get("timeframe"), str) or not binding["timeframe"]:
        return False
    window = binding.get("window")
    if not isinstance(window, Mapping) or not window.get("start") or not window.get("end"):
        return False
    costs = binding.get("cost_assumptions")
    if not isinstance(costs, Mapping) or not _is_finite_number(costs.get("cost_bps")):
        return False
    return True


def _binding_identity(binding: Mapping[str, Any]) -> dict[str, Any]:
    """Return only the four identity dimensions fixed by the authority."""

    return {
        "symbol": binding["symbol"],
        "timeframe": binding["timeframe"],
        "window": dict(binding["window"]),
        "cost_assumptions": dict(binding["cost_assumptions"]),
    }


def _evaluate_raw_excess(candidate: Mapping[str, Any], evidence_prefix: str) -> dict[str, Any]:
    summary = candidate.get("summary")
    summary = summary if isinstance(summary, Mapping) else {}
    lockbox = summary.get("lockbox_oos")
    lockbox = lockbox if isinstance(lockbox, Mapping) else {}
    buy_hold = summary.get("buy_hold_lockbox")
    buy_hold = buy_hold if isinstance(buy_hold, Mapping) else {}
    strategy_return = lockbox.get("net_return_pct")
    buy_hold_return = buy_hold.get("buy_hold_return_pct")
    values = {
        "strategy_return_pct": strategy_return,
        "buy_hold_return_pct": buy_hold_return,
        "raw_excess_pct": None,
    }
    paths = [
        f"{evidence_prefix}/summary/lockbox_oos/net_return_pct",
        f"{evidence_prefix}/summary/buy_hold_lockbox/buy_hold_return_pct",
        f"{evidence_prefix}/symbol",
        f"{evidence_prefix}/timeframe",
        f"{evidence_prefix}/promotion_report_bindings/strategy",
        f"{evidence_prefix}/promotion_report_bindings/buy_and_hold",
    ]

    if not _is_finite_number(strategy_return) or not _is_finite_number(buy_hold_return):
        return _verdict(
            "STOP",
            "RAW_EXCESS_RETURN_MISSING_OR_NOT_FINITE",
            "strategy or buy-and-hold lockbox return is missing or not finite",
            values,
            paths,
        )

    bindings = candidate.get("promotion_report_bindings")
    bindings = bindings if isinstance(bindings, Mapping) else {}
    strategy_binding = bindings.get("strategy")
    buy_hold_binding = bindings.get("buy_and_hold")
    if not _binding_is_complete(strategy_binding) or not _binding_is_complete(buy_hold_binding):
        return _verdict(
            "STOP",
            "RAW_EXCESS_BINDING_MISSING",
            "complete independent strategy and buy-and-hold identity bindings are required",
            values,
            paths,
        )
    strategy_identity = _binding_identity(strategy_binding)
    buy_hold_identity = _binding_identity(buy_hold_binding)
    if strategy_identity != buy_hold_identity:
        return _verdict(
            "STOP",
            "RAW_EXCESS_BINDING_MISMATCH",
            "strategy and buy-and-hold identity bindings differ",
            values,
            paths,
        )

    candidate_symbol = candidate.get("symbol")
    candidate_timeframe = candidate.get("timeframe")
    if (
        not isinstance(candidate_symbol, str)
        or not candidate_symbol
        or not isinstance(candidate_timeframe, str)
        or not candidate_timeframe
    ):
        return _verdict(
            "STOP",
            "RAW_EXCESS_CANDIDATE_IDENTITY_MISSING",
            "candidate symbol or timeframe is missing or invalid",
            values,
            paths,
        )
    if (
        strategy_identity["symbol"] != candidate_symbol
        or strategy_identity["timeframe"] != candidate_timeframe
    ):
        return _verdict(
            "STOP",
            "RAW_EXCESS_CANDIDATE_IDENTITY_MISMATCH",
            "raw-return bindings disagree with the candidate symbol or timeframe",
            values,
            paths,
        )

    raw_excess = strategy_return - buy_hold_return
    if not math.isfinite(raw_excess):
        return _verdict(
            "STOP",
            "RAW_EXCESS_NOT_FINITE",
            "raw lockbox excess is not finite",
            values,
            paths,
        )
    values["raw_excess_pct"] = raw_excess
    if raw_excess > 0.0:
        return _verdict(
            "PASS",
            "RAW_EXCESS_STRICTLY_POSITIVE",
            "strategy lockbox return exceeds buy-and-hold by more than 0.0 percentage points",
            values,
            paths,
        )
    return _verdict(
        "FAIL",
        "RAW_EXCESS_NOT_POSITIVE",
        "strategy lockbox return does not exceed buy-and-hold",
        values,
        paths,
    )


def evaluate_candidate(candidate: Mapping[str, Any], evidence_prefix: str) -> dict[str, Any]:
    """Evaluate one candidate without mutation.

    Mandatory BH STOP keeps public robust_final at STOP in this report-only build.
    """

    dsr = _evaluate_dsr(candidate, evidence_prefix)
    bh_fdr = _evaluate_bh_fdr(candidate, evidence_prefix)
    return {
        "checks": {
            "dsr": dsr,
            "bh_fdr": bh_fdr,
            "robust_final": _evaluate_robust_final(candidate, dsr, bh_fdr, evidence_prefix),
            "positive_raw_lockbox_excess": _evaluate_raw_excess(candidate, evidence_prefix),
        }
    }


def _candidate_id(candidate: Mapping[str, Any], index: int) -> str:
    parts = [candidate.get("strategy"), candidate.get("symbol"), candidate.get("timeframe")]
    if all(isinstance(part, str) and part for part in parts):
        return "|".join(parts)
    return f"UNIDENTIFIED_CANDIDATE_{index}"


def _pattern(checks: Mapping[str, Mapping[str, Any]]) -> str:
    labels = {
        "dsr": "DSR",
        "bh_fdr": "BH_FDR",
        "robust_final": "ROBUST_FINAL",
        "positive_raw_lockbox_excess": "POSITIVE_RAW_LOCKBOX_EXCESS",
    }
    return "|".join(f"{labels[name]}={checks[name]['status']}" for name in CHECK_ORDER)


def _markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _human_value(value: Any) -> str:
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return "N/A"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _human_check_cell(check_name: str, check: Mapping[str, Any]) -> str:
    values = check["values"]
    if check_name == "dsr":
        measured = (
            f"p={_human_value(values['dsr_p_value'])}; "
            f"flag={_human_value(values['dsr_robust'])}"
        )
    elif check_name == "bh_fdr":
        measured = (
            f"boot_p={_human_value(values['boot_p_value'])}; "
            f"survivor={_human_value(values['bh_fdr_survivor'])}"
        )
    elif check_name == "robust_final":
        measured = f"stored={_human_value(values['robust_final'])}"
    else:
        measured = f"raw_excess_pp={_human_value(values['raw_excess_pct'])}"
    return f"{check['status']} ({measured}; {check['reason']['code']})"


def _human_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Candidate | DSR | BH-FDR | robust_final | Positive raw lockbox excess | Pattern | Evidence sources |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        checks = row["checks"]
        evidence = "<br>".join(_markdown_cell(path) for path in row["evidence_source_paths"])
        lines.append(
            "| "
            + " | ".join(
                (
                    _markdown_cell(row["candidate_id"]),
                    _human_check_cell("dsr", checks["dsr"]),
                    _human_check_cell("bh_fdr", checks["bh_fdr"]),
                    _human_check_cell("robust_final", checks["robust_final"]),
                    _human_check_cell(
                        "positive_raw_lockbox_excess",
                        checks["positive_raw_lockbox_excess"],
                    ),
                    _markdown_cell(row["pattern"]),
                    evidence,
                )
            )
            + " |"
        )
    return "\n".join(lines)


def build_report(document: Mapping[str, Any], source_path: str) -> dict[str, Any]:
    """Build one machine-readable report containing an embedded Markdown table."""

    candidates = document.get("results")
    if not isinstance(candidates, list):
        raise ValueError("input document must contain a results list")

    rows: list[dict[str, Any]] = []
    check_counts = {
        name: {status: 0 for status in STATUS_ORDER}
        for name in CHECK_ORDER
    }
    pattern_counts: dict[str, int] = {}
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, Mapping):
            raise ValueError(f"results[{index}] must be an object")
        prefix = f"{source_path}#/results/{index}"
        evaluated = evaluate_candidate(candidate, prefix)
        checks = evaluated["checks"]
        pattern = _pattern(checks)
        evidence_paths = list(
            dict.fromkeys(
                path
                for check in CHECK_ORDER
                for path in checks[check]["evidence_source_paths"]
            )
        )
        row = {
            "candidate_id": _candidate_id(candidate, index),
            "measurement_label": "MEASURED_REPORT_ONLY_DIAGNOSTIC",
            "checks": checks,
            "pattern": pattern,
            "evidence_source_paths": evidence_paths,
        }
        rows.append(row)
        for check in CHECK_ORDER:
            check_counts[check][checks[check]["status"]] += 1
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

    report = {
        "report_kind": "promotion_gates_report_only",
        "effect": "DISPLAY_ONLY_NO_ENFORCEMENT",
        "source_path": source_path,
        "rows": rows,
        "counts": {
            "candidates": len(rows),
            "checks": check_counts,
            "patterns": pattern_counts,
        },
    }
    report["human_readable_table"] = _human_table(rows)
    return report


def _validate_output_path(path: Path) -> Path:
    resolved = path.resolve(strict=False)
    lowered_parts = tuple(part.casefold() for part in resolved.parts)
    repository_root = Path(__file__).resolve().parents[3]
    if resolved.name.casefold() in FENCED_FILENAMES:
        raise OutputRefused(f"fenced output filename: {resolved.name}")
    if "06_schemas" in lowered_parts:
        raise OutputRefused("outputs under MTC_COMMAND_CENTER/06_SCHEMAS are fenced")
    if "mtc_command_center" in lowered_parts or resolved.is_relative_to(repository_root):
        raise OutputRefused("report artifacts must be written outside the repository")
    if resolved.exists():
        raise OutputRefused("refusing to overwrite an existing path")
    if not REPORT_FILENAME.fullmatch(resolved.name):
        raise OutputRefused(
            "output filename must be promotion_gates_report.json or a suffixed promotion_gates_report-*.json"
        )
    if not resolved.parent.is_dir():
        raise OutputRefused("output parent directory must already exist")
    return resolved


def _json_safe(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    return value


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write a display-only PASS/FAIL/STOP promotion diagnostic report."
    )
    parser.add_argument("--input", required=True, type=Path, help="MEGA-style JSON with a results list")
    parser.add_argument("--output", required=True, type=Path, help="new promotion_gates_report*.json path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        output_path = _validate_output_path(args.output)
        input_path = args.input.resolve(strict=True)
        if input_path == output_path:
            raise OutputRefused("input and output paths must differ")
        input_bytes = input_path.read_bytes()
        document = json.loads(input_bytes.decode("utf-8"))
        if not isinstance(document, Mapping):
            raise ValueError("input JSON root must be an object")
        artifact = build_report(document, source_path=str(input_path))
        artifact["source_sha256"] = hashlib.sha256(input_bytes).hexdigest()
        serialized = json.dumps(
            _json_safe(artifact),
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        ) + "\n"
        with output_path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized)
    except (OutputRefused, FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2

    print(f"WROTE_REPORT path={output_path} candidates={artifact['counts']['candidates']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
