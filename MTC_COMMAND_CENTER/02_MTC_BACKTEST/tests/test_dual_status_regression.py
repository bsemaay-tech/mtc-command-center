from __future__ import annotations

from src.parity.dual_status import classify_parity_with_dual_view, is_early_trade_end_candidate


def test_case_362_363_style_same_bar_raw_and_clip_pass():
    raw_summary = {
        "strict_pass": True,
        "core_match_count": 129,
        "compared": 129,
        "tv_trades": 129,
        "py_trades": 129,
        "extra_tv_trades": 0,
        "extra_py_trades": 0,
    }
    clip_summary = dict(raw_summary)

    status, note, diag = classify_parity_with_dual_view(
        clip_summary=clip_summary,
        raw_summary=raw_summary,
        gap_days=0.0,
    )

    assert status == "PASS"
    assert diag["clip_strict_status"] == "PASS"
    assert diag["raw_strict_status"] == "PASS"
    assert diag["early_trade_end_candidate"] == "no"
    assert "TV_EARLY_TRADE_END_CANDIDATE" not in note


def test_case_402_416_style_clip_pass_raw_fail_is_marked_candidate():
    raw_summary = {
        "strict_pass": False,
        "core_match_count": 231,
        "compared": 231,
        "tv_trades": 231,
        "py_trades": 240,
        "extra_tv_trades": 0,
        "extra_py_trades": 9,
    }
    clip_summary = {
        "strict_pass": True,
        "core_match_count": 231,
        "compared": 231,
        "tv_trades": 231,
        "py_trades": 231,
        "extra_tv_trades": 0,
        "extra_py_trades": 0,
    }

    assert is_early_trade_end_candidate(
        gap_days=89.0,
        clip_summary=clip_summary,
        raw_summary=raw_summary,
    )

    status, note, diag = classify_parity_with_dual_view(
        clip_summary=clip_summary,
        raw_summary=raw_summary,
        gap_days=89.0,
    )

    assert status == "MISMATCH"
    assert diag["clip_strict_status"] == "PASS"
    assert diag["raw_strict_status"] == "FAIL"
    assert diag["early_trade_end_candidate"] == "yes"
    assert "TV_EARLY_TRADE_END_CANDIDATE" in note


def test_not_candidate_when_gap_is_small_even_if_raw_fail_clip_pass():
    raw_summary = {
        "strict_pass": False,
        "tv_trades": 200,
        "py_trades": 205,
        "extra_tv_trades": 0,
        "extra_py_trades": 5,
    }
    clip_summary = {
        "strict_pass": True,
        "tv_trades": 200,
        "py_trades": 200,
    }
    status, note, diag = classify_parity_with_dual_view(
        clip_summary=clip_summary,
        raw_summary=raw_summary,
        gap_days=2.0,
    )
    assert status == "MISMATCH"
    assert diag["early_trade_end_candidate"] == "no"
    assert "TV_EARLY_TRADE_END_CANDIDATE" not in note


def test_not_candidate_when_tv_has_extra_trades():
    raw_summary = {
        "strict_pass": False,
        "tv_trades": 210,
        "py_trades": 205,
        "extra_tv_trades": 5,
        "extra_py_trades": 0,
    }
    clip_summary = {
        "strict_pass": True,
        "tv_trades": 200,
        "py_trades": 200,
    }
    status, note, diag = classify_parity_with_dual_view(
        clip_summary=clip_summary,
        raw_summary=raw_summary,
        gap_days=90.0,
    )
    assert status == "MISMATCH"
    assert diag["early_trade_end_candidate"] == "no"
    assert "TV_EARLY_TRADE_END_CANDIDATE" not in note
