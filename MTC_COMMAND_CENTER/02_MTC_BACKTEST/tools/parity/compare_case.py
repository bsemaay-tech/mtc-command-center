from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CompareResult:
    case_no: str
    status: str
    note: str
    tv_status: str = ""
    python_status: str = ""
    matched_metrics: int = 0
    tv_metrics: dict | None = None
    python_metrics: dict | None = None


def compare_case(tv_result: dict, python_result: dict) -> CompareResult:
    tv_metrics = tv_result.get("metrics") if isinstance(tv_result.get("metrics"), dict) else {}
    py_report = python_result.get("report") if isinstance(python_result.get("report"), dict) else {}
    py_metrics = {}
    for item in py_report.get("metrics", []) if isinstance(py_report.get("metrics"), list) else []:
        if isinstance(item, dict) and item.get("metric") in ("Trade Count", "Profit Factor", "Net PnL %", "Max Drawdown %"):
            py_metrics[item["metric"]] = item.get("python")
    if tv_result.get("status") != "OK":
        return CompareResult(
            tv_result["case_no"],
            "ERROR",
            "TradingView collection failed",
            tv_status=str(tv_result.get("status", "")),
            python_status=str(python_result.get("status", "")),
            tv_metrics=tv_metrics,
            python_metrics=py_metrics,
        )
    if python_result.get("status") != "OK":
        return CompareResult(
            tv_result["case_no"],
            "ERROR",
            "Python parity failed",
            tv_status=str(tv_result.get("status", "")),
            python_status=str(python_result.get("status", "")),
            tv_metrics=tv_metrics,
            python_metrics=py_metrics,
        )
    matched = 0
    mapping = {
        "Total trades": "Trade Count",
        "Profit factor": "Profit Factor",
    }
    for tv_key, py_key in mapping.items():
        if str(tv_metrics.get(tv_key, "")).strip() and str(tv_metrics.get(tv_key, "")).strip() == str(py_metrics.get(py_key, "")).strip():
            matched += 1
    return CompareResult(
        tv_result["case_no"],
        "PARTIAL" if matched == 0 else "PARTIAL",
        "TradingView metrics collected; Python metrics still need explicit extraction/alignment for full parity.",
        tv_status=str(tv_result.get("status", "")),
        python_status=str(python_result.get("status", "")),
        matched_metrics=matched,
        tv_metrics=tv_metrics,
        python_metrics=py_metrics,
    )
