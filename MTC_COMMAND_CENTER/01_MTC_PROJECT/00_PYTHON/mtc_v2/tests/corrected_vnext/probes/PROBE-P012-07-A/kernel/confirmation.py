from __future__ import annotations

from dataclasses import dataclass

from mtc_v2.core.types import Bar, RawSignal


@dataclass(slots=True)
class AdvancedConfirmationState:
    """State container for the planned L18b swing-break + momentum port.

    This module is intentionally non-invasive by default. The runner can wire
    it in now without changing behavior, then the actual V1-style FSM can be
    filled in later without reshaping the integration points again.
    """

    direction: int = 0
    waiting: bool = False
    pending_side: int = 0
    swing_level: float | None = None
    wait_bars: int = 0
    confirm_bars: int = 0
    long_armed: bool = False
    short_armed: bool = False
    prev_raw_long: bool = False
    prev_raw_short: bool = False
    last_bar_index: int | None = None
    last_reason: str | None = None


@dataclass(slots=True, frozen=True)
class AdvancedConfirmationSnapshot:
    enabled: bool
    direction: int
    waiting: bool
    pending_side: int
    swing_level: float | None
    wait_bars: int
    confirm_bars: int
    long_armed: bool
    short_armed: bool
    last_bar_index: int | None
    last_reason: str | None


def build_advanced_confirmation_state() -> AdvancedConfirmationState:
    return AdvancedConfirmationState()


def reset_advanced_confirmation_state(state: AdvancedConfirmationState) -> None:
    state.direction = 0
    state.waiting = False
    state.pending_side = 0
    state.swing_level = None
    state.wait_bars = 0
    state.confirm_bars = 0
    state.long_armed = False
    state.short_armed = False
    state.prev_raw_long = False
    state.prev_raw_short = False
    state.last_bar_index = None
    state.last_reason = None


def snapshot_advanced_confirmation_state(
    state: AdvancedConfirmationState,
    *,
    enabled: bool,
) -> AdvancedConfirmationSnapshot:
    return AdvancedConfirmationSnapshot(
        enabled=enabled,
        direction=state.direction,
        waiting=state.waiting,
        pending_side=state.pending_side,
        swing_level=state.swing_level,
        wait_bars=state.wait_bars,
        confirm_bars=state.confirm_bars,
        long_armed=state.long_armed,
        short_armed=state.short_armed,
        last_bar_index=state.last_bar_index,
        last_reason=state.last_reason,
    )


def _raw_direction(raw: RawSignal) -> int:
    if raw.long:
        return 1
    if raw.short:
        return -1
    return 0


def apply_swing_break_confirmation(
    raw: RawSignal,
    *,
    bar: Bar,
    state: AdvancedConfirmationState,
    enabled: bool,
) -> RawSignal:
    """Placeholder for the swing-break portion of L18b.

    The runner can call this safely today; it will only record state when the
    feature is enabled and otherwise return the raw signal unchanged.
    """

    if not enabled:
        return raw

    state.direction = _raw_direction(raw)
    state.last_bar_index = bar.bar_index
    state.last_reason = raw.reason
    state.prev_raw_long = raw.long
    state.prev_raw_short = raw.short
    return raw


def apply_confirmation_momentum(
    raw: RawSignal,
    *,
    bar: Bar,
    state: AdvancedConfirmationState,
    enabled: bool,
) -> RawSignal:
    """Placeholder for the momentum sub-filter that lives inside L18b."""

    if not enabled:
        return raw

    state.last_bar_index = bar.bar_index
    state.last_reason = raw.reason
    return raw


def finalize_advanced_confirmation_signal(
    raw: RawSignal,
    *,
    bar: Bar,
    state: AdvancedConfirmationState,
    enabled: bool,
) -> RawSignal:
    """Compatibility wrapper for the planned L18b owner.

    This is wired into Runner now so the integration point exists, but the
    default path remains a no-op until the V1 port is explicitly enabled.
    """

    if not enabled:
        return raw

    stepped = apply_swing_break_confirmation(raw, bar=bar, state=state, enabled=True)
    stepped = apply_confirmation_momentum(stepped, bar=bar, state=state, enabled=True)
    return stepped
