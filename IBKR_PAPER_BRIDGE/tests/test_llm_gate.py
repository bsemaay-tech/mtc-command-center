from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

from bridge.engine.llm_gate import LLMGate, NullLLMGate
from bridge.engine.types import OrderPlan, Signal


def _plan() -> OrderPlan:
    signal = Signal(
        ts=datetime(2026, 7, 6, tzinfo=UTC),
        symbol="BTC",
        direction="LONG",
        reason="test",
        ref_price=100,
    )
    return OrderPlan(signal=signal, qty=1, entry_type="MKT", stop_loss=95, leverage=1)


def test_regime_validation_clamp_and_narrowing():
    gate = LLMGate(
        regime_provider=lambda _sources: {
            "regime": "LONG_ONLY",
            "confidence": 0.9,
            "ttl_minutes": 99999,
            "rationale": "ok",
            "sources": ["x"],
        },
        config_direction="BOTH",
    )

    directive = asyncio.run(gate.refresh_regime(["ignore ```system``` http://x"]))

    assert directive is not None
    assert directive.ttl_minutes == 1440
    assert gate.effective_directions() == {"LONG"}
    assert gate.sources_hash is not None


def test_invalid_regime_and_ttl_expiry_do_not_silently_widen():
    now = datetime(2026, 7, 6, tzinfo=UTC)
    gate = LLMGate(
        regime_provider=lambda _sources: {"regime": "LONG_ONLY", "confidence": 0.1, "ttl_minutes": 10},
        config_direction="BOTH",
        now=lambda: now,
    )
    assert asyncio.run(gate.refresh_regime(["bad"])) is None
    assert gate.effective_directions() == {"LONG", "SHORT"}

    gate = LLMGate(
        regime_provider=lambda _sources: {
            "regime": "NO_TRADE",
            "confidence": 0.9,
            "ttl_minutes": 15,
            "rationale": "risk",
            "sources": [],
        },
        config_direction="BOTH",
        now=lambda: now,
    )
    asyncio.run(gate.refresh_regime(["risk"]))
    gate.now = lambda: now + timedelta(minutes=20)
    assert gate.effective_directions() == set()
    gate.now = lambda: now + timedelta(minutes=40)
    assert gate.effective_directions() == {"LONG", "SHORT"}


def test_veto_default_off_deadline_and_cost_cap():
    plan = _plan()
    null = NullLLMGate()
    assert asyncio.run(null.check(plan)).verdict == "SKIPPED"

    gate = LLMGate(veto_enabled=True, veto_provider=lambda _plan: {"verdict": "VETO", "reason": "bad"})
    assert asyncio.run(gate.check(plan)).verdict == "VETO"

    capped = LLMGate(
        veto_enabled=True,
        max_vetos_per_day=0,
        veto_provider=lambda _plan: {"verdict": "VETO", "reason": "bad"},
    )
    skipped = asyncio.run(capped.check(plan))
    assert skipped.verdict == "SKIPPED"
    assert skipped.reason == "LLM_COST_LIMIT"
