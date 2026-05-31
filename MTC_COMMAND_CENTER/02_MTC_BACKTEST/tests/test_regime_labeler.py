"""Unit tests for RegimeLabeler and ManualOverride."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_PKG = Path(__file__).resolve().parent.parent
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from regimes.labeler import (
    DEFAULT_THRESHOLDS,
    LABEL_CHOPPY,
    LABEL_RANGE,
    LABEL_TREND_BEAR,
    LABEL_TREND_BULL,
    RegimeLabeler,
)
from regimes.manual_override import ManualOverride


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_4h_df(n=500) -> pd.DataFrame:
    """Realistic-ish 4H OHLCV DataFrame with a sine wave trend."""
    idx = pd.date_range("2020-01-01", periods=n, freq="4h", tz="UTC")
    t = np.linspace(0, 4 * np.pi, n)
    close = 10000 + 2000 * np.sin(t) + np.random.default_rng(42).normal(0, 50, n)
    open_ = close * (1 - np.random.default_rng(1).uniform(0, 0.005, n))
    high = np.maximum(close, open_) * (1 + np.random.default_rng(2).uniform(0, 0.01, n))
    low = np.minimum(close, open_) * (1 - np.random.default_rng(3).uniform(0, 0.01, n))
    volume = np.random.default_rng(4).uniform(100, 1000, n)
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume},
        index=idx,
    )


def _make_trendy_df(n=200, direction="up") -> pd.DataFrame:
    """Synthetic strong trending data — ADX should be high."""
    idx = pd.date_range("2020-01-01", periods=n, freq="4h", tz="UTC")
    slope = 100 if direction == "up" else -100
    close = 10000 + np.arange(n) * slope / n * 5000
    noise = np.random.default_rng(42).normal(0, 10, n)
    close = close + noise
    open_ = close - 50
    high = np.maximum(close, open_) + 80
    low = np.minimum(close, open_) - 80
    volume = np.ones(n) * 500
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume},
        index=idx,
    )


# ---------------------------------------------------------------------------
# RegimeLabeler
# ---------------------------------------------------------------------------

class TestRegimeLabeler:

    def test_label_returns_series_same_index(self):
        df = _make_4h_df(200)
        labeler = RegimeLabeler()
        labels = labeler.label(df)
        assert isinstance(labels, pd.Series)
        assert len(labels) == len(df)
        assert (labels.index == df.index).all()

    def test_all_labels_are_valid(self):
        df = _make_4h_df(200)
        labeler = RegimeLabeler()
        labels = labeler.label(df)
        valid = {LABEL_TREND_BULL, LABEL_TREND_BEAR, LABEL_RANGE, LABEL_CHOPPY}
        assert set(labels.dropna().unique()).issubset(valid)

    def test_determinism(self):
        """Same data + same thresholds → identical output every time."""
        df = _make_4h_df(300)
        labeler = RegimeLabeler()
        labels1 = labeler.label(df)
        labels2 = labeler.label(df)
        pd.testing.assert_series_equal(labels1, labels2)

    def test_thresh_change_changes_labels(self):
        """Different thresholds should produce different label distributions."""
        df = _make_4h_df(300)
        lab1 = RegimeLabeler(thresholds={"adx_threshold": 25}).label(df)
        lab2 = RegimeLabeler(thresholds={"adx_threshold": 5}).label(df)
        # With a very low ADX threshold more bars should be classified as trend
        trend_count_high_th = (lab1.isin([LABEL_TREND_BULL, LABEL_TREND_BEAR])).sum()
        trend_count_low_th = (lab2.isin([LABEL_TREND_BULL, LABEL_TREND_BEAR])).sum()
        assert trend_count_low_th >= trend_count_high_th

    def test_fingerprint_changes_with_thresholds(self):
        lab1 = RegimeLabeler(thresholds={"adx_threshold": 25})
        lab2 = RegimeLabeler(thresholds={"adx_threshold": 20})
        fp1 = lab1.compute_fingerprint("abc123")
        fp2 = lab2.compute_fingerprint("abc123")
        assert fp1 != fp2

    def test_fingerprint_changes_with_data(self):
        lab = RegimeLabeler()
        fp1 = lab.compute_fingerprint("hash_a")
        fp2 = lab.compute_fingerprint("hash_b")
        assert fp1 != fp2

    def test_fingerprint_stable(self):
        lab = RegimeLabeler()
        fp1 = lab.compute_fingerprint("same_hash")
        fp2 = lab.compute_fingerprint("same_hash")
        assert fp1 == fp2

    def test_compress_to_windows_contiguous(self):
        df = _make_4h_df(100)
        labeler = RegimeLabeler()
        series = labeler.label(df)
        windows = labeler.compress_to_windows(series)
        # No window should have 0 bars
        assert all(w["bars"] >= 1 for w in windows)
        # Total bars should equal the number of non-NaN labels
        total = sum(w["bars"] for w in windows)
        assert total == len(series.dropna())

    def test_compress_empty_series(self):
        lab = RegimeLabeler()
        result = lab.compress_to_windows(pd.Series([], dtype=object))
        assert result == []

    def test_compress_single_label(self):
        idx = pd.date_range("2020-01-01", periods=10, freq="4h", tz="UTC")
        series = pd.Series(LABEL_RANGE, index=idx)
        lab = RegimeLabeler()
        windows = lab.compress_to_windows(series)
        assert len(windows) == 1
        assert windows[0]["label"] == LABEL_RANGE
        assert windows[0]["bars"] == 10


# ---------------------------------------------------------------------------
# ManualOverride
# ---------------------------------------------------------------------------

class TestManualOverride:

    def _windows(self) -> list[dict]:
        return [
            {
                "start": "2020-01-01T00:00:00+00:00",
                "end": "2020-06-30T20:00:00+00:00",
                "label": LABEL_RANGE,
                "label_display": "Range",
                "bars": 100,
                "source": "auto",
            },
            {
                "start": "2020-07-01T00:00:00+00:00",
                "end": "2020-12-31T20:00:00+00:00",
                "label": LABEL_CHOPPY,
                "label_display": "Choppy",
                "bars": 120,
                "source": "auto",
            },
        ]

    def test_empty_override_unchanged(self):
        mo = ManualOverride.empty()
        windows = self._windows()
        result = mo.apply(windows)
        assert len(result) == len(windows)

    def test_full_override_replaces_window(self):
        overrides = [
            {"start": "2020-01-01", "end": "2020-06-30", "label": LABEL_TREND_BULL}
        ]
        mo = ManualOverride(overrides)
        windows = self._windows()
        result = mo.apply(windows)
        # The first window should now be TREND_BULL from manual source
        manual_windows = [w for w in result if w["source"] == "manual"]
        assert len(manual_windows) >= 1
        assert any(w["label"] == LABEL_TREND_BULL for w in manual_windows)

    def test_load_from_file(self, tmp_path):
        data = [{"start": "2020-01-01", "end": "2020-03-31", "label": LABEL_TREND_BULL}]
        p = tmp_path / "overrides.json"
        p.write_text(json.dumps(data))
        mo = ManualOverride.load(str(p))
        assert len(mo._overrides) == 1

    def test_invalid_format_raises(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text('{"not": "a list"}')
        with pytest.raises(ValueError, match="JSON array"):
            ManualOverride.load(str(p))
