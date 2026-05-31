from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping


DUAL_DIAG_FIELDS = [
    "clip_strict_status",
    "raw_strict_status",
    "early_trade_end_candidate",
    "gap_days",
    "clip_tv_trades",
    "clip_py_trades",
    "raw_tv_trades",
    "raw_py_trades",
]


def _as_bool(value: Any) -> bool:
    return bool(value)


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def compute_gap_days(case_end_utc: datetime | None, last_tv_exit_utc: datetime | None) -> float | None:
    if case_end_utc is None or last_tv_exit_utc is None:
        return None
    return (case_end_utc - last_tv_exit_utc).total_seconds() / 86400.0


def is_early_trade_end_candidate(
    *,
    gap_days: float | None,
    clip_summary: Mapping[str, Any],
    raw_summary: Mapping[str, Any],
    min_gap_days: float = 30.0,
) -> bool:
    if gap_days is None or gap_days <= min_gap_days:
        return False
    return (
        _as_bool(clip_summary.get("strict_pass"))
        and (not _as_bool(raw_summary.get("strict_pass")))
        and _as_int(raw_summary.get("extra_tv_trades")) == 0
        and _as_int(raw_summary.get("extra_py_trades")) > 0
    )


def classify_parity_with_dual_view(
    *,
    clip_summary: Mapping[str, Any],
    raw_summary: Mapping[str, Any],
    gap_days: float | None,
) -> tuple[str, str, dict[str, str]]:
    clip_pass = _as_bool(clip_summary.get("strict_pass"))
    raw_pass = _as_bool(raw_summary.get("strict_pass"))
    early_candidate = is_early_trade_end_candidate(
        gap_days=gap_days,
        clip_summary=clip_summary,
        raw_summary=raw_summary,
    )

    note = (
        f"clip={'PASS' if clip_pass else 'FAIL'} "
        f"core={_as_int(clip_summary.get('core_match_count'))}/{_as_int(clip_summary.get('compared'))} "
        f"tv={_as_int(clip_summary.get('tv_trades'))} py={_as_int(clip_summary.get('py_trades'))}; "
        f"raw={'PASS' if raw_pass else 'FAIL'} "
        f"tv={_as_int(raw_summary.get('tv_trades'))} py={_as_int(raw_summary.get('py_trades'))} "
        f"extra_tv={_as_int(raw_summary.get('extra_tv_trades'))} extra_py={_as_int(raw_summary.get('extra_py_trades'))}"
    )
    if early_candidate and gap_days is not None:
        note += f"; TV_EARLY_TRADE_END_CANDIDATE gap_days={gap_days:.2f}"

    diag = {
        "clip_strict_status": "PASS" if clip_pass else "FAIL",
        "raw_strict_status": "PASS" if raw_pass else "FAIL",
        "early_trade_end_candidate": "yes" if early_candidate else "no",
        "gap_days": f"{gap_days:.2f}" if gap_days is not None else "",
        "clip_tv_trades": str(_as_int(clip_summary.get("tv_trades"))),
        "clip_py_trades": str(_as_int(clip_summary.get("py_trades"))),
        "raw_tv_trades": str(_as_int(raw_summary.get("tv_trades"))),
        "raw_py_trades": str(_as_int(raw_summary.get("py_trades"))),
    }

    if _as_int(raw_summary.get("tv_trades")) == 0 and _as_int(raw_summary.get("py_trades")) == 0:
        return "PASS", note, diag
    if raw_pass:
        return "PASS", note, diag
    return "MISMATCH", note, diag

