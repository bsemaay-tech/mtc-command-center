from datetime import datetime, timezone

import pandas as pd

from src.parity.compare_tv_trades import (
    _parse_dt_to_utc,
    build_report,
    clip_overlap,
    normalize_broker_reporting,
    summarize_report,
)


def test_parse_dt_to_utc_keeps_ambiguous_rows_instead_of_nat():
    series = pd.Series(["2025-10-26 01:15", "2025-10-26 01:30"])
    out = _parse_dt_to_utc(series, source_tz="Europe/London")
    assert out.notna().all()
    assert str(out.dt.tz) == "UTC"


def test_build_report_core_match_includes_price_and_qty():
    base_entry = datetime(2025, 7, 1, 0, 0, tzinfo=timezone.utc)
    base_exit = datetime(2025, 7, 1, 1, 0, tzinfo=timezone.utc)
    tv = pd.DataFrame(
        [
            {
                "seq": 1,
                "side": "LONG",
                "entry_time": base_entry,
                "exit_time": base_exit,
                "entry_price": 100.0,
                "exit_price": 105.0,
                "qty": 1.0,
                "reason": "TP",
            }
        ]
    )
    py_bad = pd.DataFrame(
        [
            {
                "seq": 1,
                "side": "LONG",
                "entry_time": base_entry,
                "exit_time": base_exit,
                "entry_price": 101.0,
                "exit_price": 106.0,
                "qty": 1.1,
                "reason": "TP",
            }
        ]
    )
    bad_report = build_report(tv, py_bad, price_tol=0.5, qty_tol=1e-6, strict_core=True)
    assert bool(bad_report.iloc[0]["all_core_match"]) is False
    compat_report = build_report(tv, py_bad, price_tol=0.5, qty_tol=1e-6, strict_core=False)
    assert bool(compat_report.iloc[0]["all_core_match"]) is True

    py_ok = py_bad.copy()
    py_ok.loc[0, "entry_price"] = 100.4
    py_ok.loc[0, "exit_price"] = 105.4
    py_ok.loc[0, "qty"] = 1.0
    ok_report = build_report(tv, py_ok, price_tol=0.5, qty_tol=1e-6, strict_core=True)
    assert bool(ok_report.iloc[0]["all_core_match"]) is True


def test_summarize_report_flags_extra_python_trades_as_non_pass():
    base_entry = datetime(2025, 7, 1, 0, 0, tzinfo=timezone.utc)
    base_exit = datetime(2025, 7, 1, 1, 0, tzinfo=timezone.utc)
    tv = pd.DataFrame(
        [
            {
                "seq": 1,
                "side": "LONG",
                "entry_time": base_entry,
                "exit_time": base_exit,
                "entry_price": 100.0,
                "exit_price": 105.0,
                "qty": 1.0,
                "reason": "TP",
            }
        ]
    )
    py = pd.DataFrame(
        [
            {
                "seq": 1,
                "side": "LONG",
                "entry_time": base_entry,
                "exit_time": base_exit,
                "entry_price": 100.0,
                "exit_price": 105.0,
                "qty": 1.0,
                "reason": "TP",
            },
            {
                "seq": 2,
                "side": "SHORT",
                "entry_time": base_entry,
                "exit_time": base_exit,
                "entry_price": 100.0,
                "exit_price": 95.0,
                "qty": 1.0,
                "reason": "TP",
            },
        ]
    )
    report = build_report(tv, py)
    summary = summarize_report(tv, py, report)
    assert summary["compared"] == 1
    assert summary["core_match_count"] == 1
    assert summary["extra_py_trades"] == 1
    assert summary["strict_pass"] is False


def test_normalize_broker_reporting_merges_python_duplicate_partial_rows():
    base_entry = datetime(2025, 8, 14, 11, 45, tzinfo=timezone.utc)
    base_exit = datetime(2025, 8, 14, 12, 30, tzinfo=timezone.utc)
    tv = pd.DataFrame(
        [
            {
                "seq": 1,
                "side": "SHORT",
                "entry_time": base_entry,
                "exit_time": base_exit,
                "entry_price": 120947.4,
                "exit_price": 119479.0,
                "qty": 0.248910,
                "reason": "TRAIL",
            }
        ]
    )
    py = pd.DataFrame(
        [
            {
                "seq": 1,
                "side": "SHORT",
                "entry_time": base_entry,
                "exit_time": base_exit,
                "entry_price": 120947.4,
                "exit_price": 119479.0,
                "qty": 0.124455,
                "reason": "TRAIL",
            },
            {
                "seq": 2,
                "side": "SHORT",
                "entry_time": base_entry,
                "exit_time": base_exit,
                "entry_price": 120947.4,
                "exit_price": 119479.0,
                "qty": 0.124455,
                "reason": "TRAIL",
            },
        ]
    )
    tv_n, py_n = normalize_broker_reporting(tv, py, qty_tol=1e-6)
    assert len(tv_n) == 1
    assert len(py_n) == 1
    assert abs(float(py_n.iloc[0]["qty"]) - 0.248910) <= 1e-9
    summary = summarize_report(tv, py, build_report(tv, py, strict_core=True, qty_tol=1e-6))
    assert summary["tv_trades"] == 1
    assert summary["py_trades"] == 1
    assert summary["raw_py_trades"] == 2
    assert summary["strict_pass"] is True


def test_normalize_broker_reporting_keeps_symmetric_duplicate_pairs():
    base_entry = datetime(2025, 7, 26, 1, 15, tzinfo=timezone.utc)
    base_exit = datetime(2025, 7, 26, 2, 30, tzinfo=timezone.utc)
    tv = pd.DataFrame(
        [
            {
                "seq": 1,
                "side": "LONG",
                "entry_time": base_entry,
                "exit_time": base_exit,
                "entry_price": 1.0,
                "exit_price": 2.0,
                "qty": 0.101194,
                "reason": "TRAIL",
            },
            {
                "seq": 2,
                "side": "LONG",
                "entry_time": base_entry,
                "exit_time": base_exit,
                "entry_price": 1.0,
                "exit_price": 2.0,
                "qty": 0.101195,
                "reason": "TRAIL",
            },
        ]
    )
    py = tv.copy()
    tv_n, py_n = normalize_broker_reporting(tv, py, qty_tol=1e-6)
    assert len(tv_n) == 2
    assert len(py_n) == 2


def test_build_report_allows_duplicate_be_pair_one_bar_timing_drift():
    entry = datetime(2025, 9, 17, 13, 30, tzinfo=timezone.utc)
    tv_exit = datetime(2025, 9, 17, 18, 15, tzinfo=timezone.utc)
    py_exit = datetime(2025, 9, 17, 18, 30, tzinfo=timezone.utc)
    tv = pd.DataFrame(
        [
            {
                "seq": 1,
                "side": "SHORT",
                "entry_time": entry,
                "exit_time": tv_exit,
                "entry_price": 115946.4,
                "exit_price": 115920.5,
                "qty": 0.203450,
                "reason": "BE",
            },
            {
                "seq": 2,
                "side": "SHORT",
                "entry_time": entry,
                "exit_time": tv_exit,
                "entry_price": 115946.4,
                "exit_price": 115920.5,
                "qty": 0.203451,
                "reason": "BE",
            },
        ]
    )
    py = pd.DataFrame(
        [
            {
                "seq": 1,
                "side": "SHORT",
                "entry_time": entry,
                "exit_time": py_exit,
                "entry_price": 115946.4,
                "exit_price": 115873.12201559648,
                "qty": 0.203450,
                "reason": "BE",
            },
            {
                "seq": 2,
                "side": "SHORT",
                "entry_time": entry,
                "exit_time": py_exit,
                "entry_price": 115946.4,
                "exit_price": 115873.12201559648,
                "qty": 0.203450,
                "reason": "BE",
            },
        ]
    )
    report = build_report(tv, py)
    summary = summarize_report(tv, py, report)
    assert summary["tv_trades"] == 2
    assert summary["py_trades"] == 2
    assert summary["core_match_count"] == 2
    assert summary["strict_pass"] is True


def test_normalize_broker_reporting_merges_margin_call_sl_tail_duplicates():
    entry = datetime(2025, 12, 28, 18, 15, tzinfo=timezone.utc)
    mc1_exit = datetime(2025, 12, 28, 18, 30, tzinfo=timezone.utc)
    mc2_exit = datetime(2025, 12, 28, 22, 45, tzinfo=timezone.utc)
    sl_exit = datetime(2025, 12, 29, 0, 30, tzinfo=timezone.utc)
    tv = pd.DataFrame(
        [
            {"seq": 1, "side": "SHORT", "entry_time": entry, "exit_time": mc1_exit, "entry_price": 1.0, "exit_price": 1.1, "qty": 0.1, "reason": "MARGIN CALL"},
            {"seq": 2, "side": "SHORT", "entry_time": entry, "exit_time": mc2_exit, "entry_price": 1.0, "exit_price": 1.2, "qty": 0.3, "reason": "MARGIN CALL"},
            {"seq": 3, "side": "SHORT", "entry_time": entry, "exit_time": sl_exit, "entry_price": 1.0, "exit_price": 1.3, "qty": 0.2, "reason": "SL"},
        ]
    )
    py = pd.DataFrame(
        [
            {"seq": 1, "side": "SHORT", "entry_time": entry, "exit_time": mc1_exit, "entry_price": 1.0, "exit_price": 1.1, "qty": 0.15, "reason": "MARGIN CALL"},
            {"seq": 2, "side": "SHORT", "entry_time": entry, "exit_time": mc2_exit, "entry_price": 1.0, "exit_price": 1.2, "qty": 0.11, "reason": "MARGIN CALL"},
            {"seq": 3, "side": "SHORT", "entry_time": entry, "exit_time": sl_exit, "entry_price": 1.0, "exit_price": 1.3, "qty": 0.28, "reason": "SL"},
            {"seq": 4, "side": "SHORT", "entry_time": entry, "exit_time": sl_exit, "entry_price": 1.0, "exit_price": 1.3, "qty": 0.02, "reason": "SL"},
        ]
    )
    tv_n, py_n = normalize_broker_reporting(tv, py, qty_tol=1e-6)
    assert len(tv_n) == 3
    assert len(py_n) == 3
    assert abs(float(py_n.iloc[2]["qty"]) - 0.30) <= 1e-9
    summary = summarize_report(tv, py, build_report(tv, py))
    assert summary["tv_trades"] == 3
    assert summary["py_trades"] == 3
    assert summary["strict_pass"] is True


def test_clip_overlap_keeps_only_shared_window_and_reindexes():
    t0 = datetime(2025, 7, 1, 0, 0, tzinfo=timezone.utc)
    t1 = datetime(2025, 7, 1, 1, 0, tzinfo=timezone.utc)
    t2 = datetime(2025, 7, 1, 2, 0, tzinfo=timezone.utc)
    t3 = datetime(2025, 7, 1, 3, 0, tzinfo=timezone.utc)
    t4 = datetime(2025, 7, 1, 4, 0, tzinfo=timezone.utc)

    tv = pd.DataFrame(
        [
            {"seq": 1, "side": "LONG", "entry_time": t0, "exit_time": t1, "entry_price": 1.0, "exit_price": 1.1, "qty": 1.0, "reason": "TP"},
            {"seq": 2, "side": "LONG", "entry_time": t1, "exit_time": t2, "entry_price": 1.1, "exit_price": 1.2, "qty": 1.0, "reason": "TP"},
            {"seq": 3, "side": "SHORT", "entry_time": t3, "exit_time": t4, "entry_price": 1.2, "exit_price": 1.1, "qty": 1.0, "reason": "TP"},
        ]
    )
    py = pd.DataFrame(
        [
            {"seq": 1, "side": "LONG", "entry_time": t1, "exit_time": t2, "entry_price": 1.1, "exit_price": 1.2, "qty": 1.0, "reason": "TP"},
            {"seq": 2, "side": "SHORT", "entry_time": t2, "exit_time": t3, "entry_price": 1.2, "exit_price": 1.1, "qty": 1.0, "reason": "TP"},
        ]
    )

    tv_clip, py_clip = clip_overlap(tv, py)
    assert len(tv_clip) == 1
    assert len(py_clip) == 2
    assert int(tv_clip.iloc[0]["seq"]) == 1
    assert int(py_clip.iloc[0]["seq"]) == 1
    assert tv_clip.iloc[0]["entry_time"] == t1
    assert tv_clip.iloc[0]["exit_time"] == t2
    assert int(py_clip.iloc[1]["seq"]) == 2
    assert py_clip.iloc[1]["entry_time"] == t2
    assert py_clip.iloc[1]["exit_time"] == t3
