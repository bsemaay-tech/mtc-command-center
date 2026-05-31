import pytest

from src.modules.risk.position_sizer import PositionSizer


def test_position_sizer_respects_mintick_min_stop_distance():
    sizer = PositionSizer(risk_long_pct=4.0, risk_short_pct=3.0, max_leverage=5.0, mintick=0.1)
    qty = sizer.calculate(equity=10_000, entry_price=100.0, sl_price=99.99, direction="long")
    # min stop distance uses max(0.1% of entry=0.1, 10*mintick=1.0) => 1.0
    # risk amount=400 => ideal qty=400
    assert qty == pytest.approx(400.0)


def test_position_sizer_caps_by_leverage():
    sizer = PositionSizer(risk_long_pct=4.0, risk_short_pct=3.0, max_leverage=2.0, mintick=0.1)
    qty = sizer.calculate(equity=1_000, entry_price=100.0, sl_price=99.0, direction="long")
    # max notional=2000 => max qty=20
    assert qty == pytest.approx(20.0)


def test_position_sizer_fallback_uses_full_risk_pct_without_50_percent_cap():
    sizer = PositionSizer(risk_long_pct=100.0, risk_short_pct=100.0, max_leverage=5.0, mintick=0.1)
    qty = sizer.calculate_fallback(
        equity=10_000,
        entry_price=100.0,
        fallback_pct=100.0,
        risk_pct=100.0,
    )
    # use_sl=false branch should use full 100% notional when both inputs are 100%.
    assert qty == pytest.approx(100.0)
