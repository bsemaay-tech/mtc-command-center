"""Continuous bridge engine plus deterministic replay entry point."""

from __future__ import annotations

import asyncio
import inspect
import sqlite3
import traceback
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Callable

from bridge.broker.base import (
    Broker,
    SubmissionRejectedError,
    UnknownSubmissionError,
)
from bridge.engine.bars import BarFeed
from bridge.engine.llm_gate import NullLLMGate
from bridge.engine.notify import TelegramNotifier, build_notifier
from bridge.engine.orders import OrderManager
from bridge.engine.reconcile import FullReconciler
from bridge.engine.risk import RiskEngine
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.engine.types import Bar, Position
from bridge.engine.window import (
    DEFAULT_STALE_AFTER_S,
    detect_interruption,
    record_liveness,
    record_window_start,
    window_status,
)
from bridge.store.db import Store


_ROUTINE_FEED_NOTIFICATION_CODES = frozenset({"DISCONNECT", "DATA_RESTORED"})


def _safe_full_reconcile_reason(exc: BaseException) -> str:
    """Secret-safe reason code for a full-capture crash: type name only."""
    name = "".join(
        ch if ch.isalnum() or ch == "_" else "_" for ch in type(exc).__name__.upper()
    )
    return f"FULL_RECONCILE_CYCLE_FAILED:{name}"[:96]


@dataclass
class BridgeEngine:
    run_id: str
    broker: Broker
    store: Store
    strategy: KeltnerTrailEma8
    risk_engine: RiskEngine
    order_manager: OrderManager | None = None
    llm_gate: NullLLMGate | None = None
    state: str = "DISARMED"
    coin: str = "BTC"
    timeframe: str = "1h"
    mode: str = "dry_run"
    on_update: Callable[[str, object], object] | None = None
    notifier: TelegramNotifier | None = None
    heartbeat_hours: float = 6.0
    reconcile_interval_s: float = 60.0
    reconcile_max_consecutive_failures: int = 3
    bar_reconnect_attempts: int = 9
    bar_reconnect_base_delay_s: float = 5.0
    bar_data_restore_timeout_s: float = 300.0
    window_stale_after_s: float = DEFAULT_STALE_AFTER_S
    bars: list[Bar] = field(default_factory=list)
    reconcile_ready: bool = False
    last_reconcile_ts: datetime | None = None
    reconcile_error: str | None = None
    # TS-P1-005: a *separate* readiness gate. `reconcile_ready` above stays
    # owned by the light `OrderManager.reconcile()` path and can never satisfy
    # the full gate; full readiness is derived from a fresh accepted v6
    # checkpoint and is only consulted on a v6-enabled store.
    full_reconciler: object | None = None
    last_full_reconcile_ts: datetime | None = None
    full_reconcile_error: str | None = None
    full_reconcile_attempt_id: str | None = None
    _feed: BarFeed | None = field(default=None, init=False)
    _tasks: list[asyncio.Task] = field(default_factory=list, init=False)
    _kill_requested: bool = field(default=False, init=False)
    _consecutive_order_rejects: int = field(default=0, init=False)
    _consecutive_reconcile_failures: int = field(default=0, init=False)
    _processed_bar_ts: set[datetime] = field(default_factory=set, init=False)
    risk_input_error: str | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        self.reconcile_max_consecutive_failures = max(1, int(self.reconcile_max_consecutive_failures))
        self.bar_reconnect_attempts = max(1, int(self.bar_reconnect_attempts))
        self.bar_data_restore_timeout_s = max(30.0, float(self.bar_data_restore_timeout_s))
        self.order_manager = self.order_manager or OrderManager(self.store, self.broker, self.run_id)
        if self.notifier is None:
            # Default DISABLED: tests construct engines directly and must
            # never leak real Telegram messages. The app factory injects the
            # real notifier explicitly (build_notifier()).
            self.notifier = TelegramNotifier(enabled=False)
        self.llm_gate = self.llm_gate or NullLLMGate()
        persisted = self.store.get_meta("app_state")
        if persisted is None:
            self.store.set_meta("app_state", self.state)
        else:
            self.state = persisted
        if self.store.has_submission_quarantine():
            self.state = "DISARMED"
            self.store.set_meta("app_state", "DISARMED")
        elif self.store.partial_recovery_blocks_new_risk():
            self.state = "DISARMED"
            self.store.set_meta("app_state", "DISARMED")
        if self.store.full_reconcile_enabled():
            # A capture that never resolved (crash/kill) stays visible as
            # INCOMPLETE evidence; the prior accepted pointer is untouched and
            # is now stale until a fresh complete collection replaces it.
            interrupted = self.store.resolve_interrupted_reconcile_attempts(
                observed_ts=datetime.now(UTC)
            )
            if interrupted:
                self.full_reconcile_error = "RESTART_INTERRUPTED"
            if self.full_reconciler is None:
                self.full_reconciler = FullReconciler(
                    store=self.store,
                    broker=self.broker,
                    run_id=self.run_id,
                    order_manager=self.order_manager,
                )

    async def start(self, lookback: int = 300) -> None:
        self._ensure_run(mode=self.mode)
        # TS-P0-003: stamp a sticky interruption BEFORE fresh liveness is
        # recorded, so a crash/downtime gap can never be silently bridged.
        if detect_interruption(self.store, datetime.now(UTC), self.window_stale_after_s):
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "WARN",
                "WINDOW_INTERRUPTED",
                f"liveness gap exceeded {self.window_stale_after_s}s at startup",
            )
        await self.broker.connect()
        await self.order_manager.reconcile()
        self.reconcile_ready = True
        self.last_reconcile_ts = datetime.now(UTC)
        self.reconcile_error = None
        record_liveness(self.store, self.last_reconcile_ts)
        await self.run_full_reconcile()
        await self._publish("status", self.status())
        self._feed = BarFeed(
            broker=self.broker,
            coin=self.coin,
            timeframe=self.timeframe,
            on_bar_closed=self.on_bar,
            on_event=self._feed_event,
            on_stale=self._stale_disarm,
            staleness_enabled=self.mode != "dry_run",
            reconnect_attempts=self.bar_reconnect_attempts,
            reconnect_base_delay=self.bar_reconnect_base_delay_s,
            data_restore_timeout_s=self.bar_data_restore_timeout_s,
        )
        self.bars = await self._feed.start(lookback=lookback)
        # Persist warmup so the dashboard chart shows real exchange bars
        # immediately (INSERT OR REPLACE — reruns are idempotent).
        for bar in self.bars:
            self.store.insert_bar(
                self.coin, self.timeframe, bar.ts, bar.open, bar.high, bar.low, bar.close, bar.volume
            )
        stream = getattr(self.broker, "start_stream", None)
        if stream is not None:
            self._tasks.append(asyncio.create_task(stream(), name="mock-broker-stream"))
        self._tasks.append(asyncio.create_task(self._reconcile_loop(), name="bridge-reconciler"))
        if self.notifier is not None and self.notifier.enabled:
            self._tasks.append(asyncio.create_task(self._heartbeat_loop(), name="bridge-heartbeat"))

    async def stop(self) -> None:
        if self._feed is not None:
            await self._feed.stop()
        for task in self._tasks:
            task.cancel()
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    async def arm(self) -> None:
        now = datetime.now(UTC)
        previous = self._app_state()
        self.store.insert_event(self.run_id, now, "INFO", "ARM_REQUEST", f"state={previous}")
        if previous == "KILLED":
            raise RuntimeError("KILLED requires operator acknowledgement")
        if self.store.has_submission_quarantine():
            self.state = "DISARMED"
            self.store.set_meta("app_state", "DISARMED")
            raise RuntimeError("submission quarantine blocks ARM")
        if self.store.partial_recovery_blocks_new_risk():
            # Non-terminal recovery or a durable UNPROTECTED_ABORT: risk
            # authority is independent, no automatic re-arm exists.
            self.state = "DISARMED"
            self.store.set_meta("app_state", "DISARMED")
            raise RuntimeError("partial-fill recovery blocks ARM")
        for pending in self.store.partial_recoveries_awaiting_rearm():
            # PROTECTED_PARTIAL hands the position back only after a fresh
            # exact-quantity snapshot proves protection under the symbol lock.
            proved = await self.order_manager.confirm_partial_rearm(
                str(pending["recovery_id"])
            )
            if not proved:
                self.state = "DISARMED"
                self.store.set_meta("app_state", "DISARMED")
                self.store.insert_event(
                    self.run_id,
                    now,
                    "WARN",
                    "PARTIAL_REARM_PROOF_FAILED",
                    str(pending["symbol"]),
                )
                raise RuntimeError("partial-fill re-arm proof failed")
        if not self.reconcile_ready:
            raise RuntimeError("startup reconcile incomplete")
        max_age = timedelta(seconds=max(self.reconcile_interval_s * 3, 30.0))
        if self.last_reconcile_ts is None or now - self.last_reconcile_ts > max_age:
            self.reconcile_ready = False
            self.reconcile_error = "STALE"
            raise RuntimeError("reconcile evidence stale")
        if self.store.full_reconcile_enabled() and not self.full_reconcile_ready(now):
            # Both gates are required on a v6 store: light reconcile success
            # alone can never arm the bridge.
            raise RuntimeError("full reconciliation incomplete")
        self._kill_requested = False
        # Explicit human re-arm clears the sticky risk-input fail-closed latch.
        self.risk_input_error = None
        self._set_state("ARMED")
        record_window_start(self.store, now)
        await self._publish("status", self.status())

    def disarm(self) -> None:
        self._set_state("DISARMED")

    async def disarm_runtime(self) -> None:
        self.store.insert_event(
            self.run_id,
            datetime.now(UTC),
            "INFO",
            "DISARM_REQUEST",
            f"state={self._app_state()}",
        )
        self.disarm()
        if not self.store.has_submission_quarantine():
            for order in await self.broker.open_orders():
                if order.role != "ENTRY":
                    continue
                symbol = str(order.coin)
                async with self.order_manager.symbol_locks.hold(symbol):
                    # Re-check after acquiring the one-writer lock. An active
                    # partial recovery owns cancel/protect/flatten sequencing.
                    if self.store.has_submission_quarantine():
                        continue
                    if self.order_manager._partial_recovery_owns(symbol):
                        continue
                    await self.broker.cancel(order.cloid)
        await self.order_manager.reconcile()
        await self._publish("status", self.status())

    async def kill(self, flatten: bool = False) -> None:
        self._kill_requested = True
        self._set_state("KILLED")
        async with self.order_manager.symbol_locks.hold(self.coin):
            # KILL remains a state/latch change, but it may not race the
            # recovery writer or mutate while TS-P1-003 is quarantined.
            if (
                not self.store.has_submission_quarantine()
                and not self.order_manager._partial_recovery_owns(self.coin)
            ):
                await self.broker.cancel_all()
                if flatten:
                    await self.broker.flatten(self.coin)
        await self._publish("status", self.status())

    async def acknowledge_kill(self) -> None:
        if self._app_state() != "KILLED":
            return
        self._kill_requested = False
        self._set_state("DISARMED")
        self.reconcile_ready = False
        await self.order_manager.reconcile()
        self.reconcile_ready = True
        await self._publish("status", self.status())

    def full_reconcile_max_age_s(self) -> float:
        """Owner-accepted freshness bound, derived from the health cadence.

        Reuses the *existing* accepted light formula rather than introducing a
        second, unratified constant: the full checkpoint must be no older than
        three health cycles (floor 30 s). Evaluated at call time, so changing
        `reconcile_interval_s` moves both bounds together.
        """
        return max(self.reconcile_interval_s * 3, 30.0)

    def full_reconcile_ready(self, now: datetime | None = None) -> bool:
        """Derived from a *fresh accepted v6 checkpoint* — never from the
        light reconcile path, and never from in-memory state alone."""
        if not self.store.full_reconcile_enabled():
            return False
        if self.full_reconcile_error is not None:
            # A sticky fail-closed latch: a restart-interrupted capture or any
            # non-accepting attempt keeps the full gate shut until a *fresh
            # accept* clears it. Nothing else — not `arm()`, not a light
            # reconcile recovery — may clear this.
            return False
        return self.store.full_reconcile_ready(
            now=now or datetime.now(UTC),
            max_age_s=self.full_reconcile_max_age_s(),
        )

    async def run_full_reconcile(self) -> object | None:
        """Run one bounded full capture when the v6 ledger is active.

        Never raises for an ordinary failure: the full path carries its own
        outcome in `full_reconcile_error` and must not be able to consume the
        light reconcile failure budget or disarm through it.
        """
        if not self.store.full_reconcile_enabled() or self.full_reconciler is None:
            return None
        try:
            result = await self.full_reconciler.run_cycle()
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed on the full gate only
            self.full_reconcile_error = _safe_full_reconcile_reason(exc)
            self._record_full_reconcile_block(self.full_reconcile_error)
            return None
        self.full_reconcile_attempt_id = result.attempt_id
        if result.accepted:
            self.last_full_reconcile_ts = result.ended_ts
            self.full_reconcile_error = None
        else:
            self.full_reconcile_error = result.reason_code
            self._record_full_reconcile_block(
                f"{result.state.value}:{result.reason_code}"
            )
        return result

    def _record_full_reconcile_block(self, detail: str) -> None:
        """Best-effort durable note; a broken store must not mask the latch."""
        try:
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "WARN",
                "FULL_RECONCILE_BLOCKED",
                detail,
            )
        except Exception:  # noqa: BLE001 - the latch above is the real signal
            self._notify_bg("WARN", f"FULL_RECONCILE_BLOCKED: {detail}")

    async def run_replay(self, max_bars: int | None = None) -> None:
        self._ensure_run(mode="dry_run")
        await self.broker.connect()
        if self._app_state() != "ARMED":
            return
        replay: list[Bar] = []
        self.broker.subscribe_bars(self.coin, self.timeframe, replay.append)
        if max_bars is not None:
            replay = replay[:max_bars]
        for bar in replay:
            await self.on_bar(bar, process_broker_bar=True)

    async def on_bar(
        self,
        bar: Bar,
        process_broker_bar: bool = False,
        *,
        _full_guard_held: bool = False,
    ) -> None:
        if not _full_guard_held:
            from bridge.engine.reconcile import full_writer_guard

            async with full_writer_guard(self.store):
                await self.on_bar(
                    bar,
                    process_broker_bar=process_broker_bar,
                    _full_guard_held=True,
                )
            return
        if bar.ts in self._processed_bar_ts:
            return
        self._processed_bar_ts.add(bar.ts)
        if not self.bars or bar.ts > self.bars[-1].ts:
            self.bars.append(bar)
        self.store.insert_bar(self.coin, self.timeframe, bar.ts, bar.open, bar.high, bar.low, bar.close, bar.volume)
        if process_broker_bar:
            process_bar = getattr(self.broker, "process_bar", None)
            if process_bar is not None:
                process_bar(bar)
        await self.order_manager.sync_broker_state()
        if self.store.has_submission_quarantine():
            self.state = "DISARMED"
            self.store.set_meta("app_state", "DISARMED")
            await self._publish("bar", bar.model_dump(mode="json"))
            return
        if self.store.partial_recovery_blocks_new_risk():
            # Only the partial-recovery state machine may act on this symbol.
            # The engine's trail/close/flip path runs *before* the ARMED gate,
            # so it must be short-circuited here as well.
            self.state = "DISARMED"
            self.store.set_meta("app_state", "DISARMED")
            await self._publish("bar", bar.model_dump(mode="json"))
            return
        position = self._position_for(self.coin, await self.broker.positions())

        if position is not None:
            trail = self.strategy.trail_level(self.bars, position)
            if trail is not None:
                await self.order_manager.trail_position(position, trail)
            signal = self.strategy.on_bar(self.bars, position=position)
            if signal is not None and self._is_opposite(position, signal.direction):
                await self.order_manager.close_position(position)
                self.store.insert_decision(
                    self.run_id,
                    f"{self.run_id}:{signal.symbol}:{signal.ts.isoformat()}:CLOSE",
                    signal.ts,
                    signal.symbol,
                    "CLOSE_ONLY_SUBMITTED",
                    {"reason": "opposite_signal_flip_disabled"},
                )
            await self._publish("bar", bar.model_dump(mode="json"))
            return

        if (
            self._app_state() != "ARMED"
            or self._kill_requested
            or (
                self.store.full_reconcile_enabled()
                and not self.full_reconcile_ready()
            )
        ):
            await self._publish("bar", bar.model_dump(mode="json"))
            return
        signal = self.strategy.on_bar(self.bars, position=None)
        if signal is None:
            await self._publish("bar", bar.model_dump(mode="json"))
            return

        decision_uid = f"{self.run_id}:{signal.symbol}:{signal.ts.isoformat()}:{signal.direction}"
        self.store.insert_decision(self.run_id, decision_uid, signal.ts, signal.symbol, "SIGNAL", signal.model_dump(mode="json"))
        if signal.stop_loss is None:
            self.store.insert_decision(
                self.run_id,
                decision_uid,
                signal.ts,
                signal.symbol,
                "RISK_REJECT",
                {"reason": "STRATEGY_STOP_MISSING", "gates": []},
            )
            return
        try:
            realized_today = self.store.realized_pnl_today(self.run_id)
            consecutive_losses = self.store.consecutive_closed_losses(self.run_id)
        except Exception as exc:  # unknown risk state -> fail closed, never trade blind
            await self._risk_inputs_failed(exc)
            return
        risk = self.risk_engine.evaluate(
            signal=signal,
            account=await self.broker.account(),
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
            open_position=None,
            realized_today=realized_today,
            consecutive_losses=consecutive_losses,
        )
        if not risk.accepted or risk.plan is None:
            self.store.insert_decision(
                self.run_id,
                decision_uid,
                signal.ts,
                signal.symbol,
                "RISK_REJECT",
                {"reason": risk.rejection, "gates": risk.gate_results},
            )
            if risk.disarm:
                self.disarm()
                self.store.insert_event(self.run_id, datetime.now(UTC), "WARN", "RISK_AUTO_DISARM", str(risk.rejection))
            return
        self.store.insert_decision(
            self.run_id,
            decision_uid,
            signal.ts,
            signal.symbol,
            "RISK_PASS",
            {"order_plan": risk.plan.model_dump(mode="json"), "gates": risk.gate_results},
        )
        llm = await self.llm_gate.check(risk.plan)
        verdict = getattr(llm, "verdict", "SKIPPED")
        llm_stage = "LLM_VETO" if verdict == "VETO" else ("LLM_PASS" if verdict == "PASS" else "LLM_SKIPPED")
        self.store.insert_decision(
            self.run_id,
            decision_uid,
            signal.ts,
            signal.symbol,
            llm_stage,
            {"reason": llm.reason},
        )
        if verdict == "VETO":
            return
        if self._app_state() != "ARMED" or self._kill_requested:
            return
        if self._position_for(self.coin, await self.broker.positions()) is not None:
            return
        try:
            result = await self.order_manager.submit_plan(
                decision_uid, risk.plan,
                strategy_id=getattr(self.strategy, 'id', 'keltner_trail_ema8'),
            )
        except UnknownSubmissionError as exc:
            self._unknown_submission_disarm(
                decision_uid=decision_uid,
                signal_ts=signal.ts,
                symbol=signal.symbol,
                exc=exc,
            )
            return
        except SubmissionRejectedError as exc:
            self._record_order_rejection(
                decision_uid,
                signal.ts,
                signal.symbol,
                exc.reason_code,
            )
            return
        except Exception as exc:
            self._record_order_rejection(
                decision_uid,
                signal.ts,
                signal.symbol,
                type(exc).__name__,
            )
            return
        if result is not None:
            self._consecutive_order_rejects = 0
            self.store.insert_decision(self.run_id, decision_uid, signal.ts, signal.symbol, "SUBMITTED", result)
        await self._publish("decision", {"decision_uid": decision_uid})

    def _unknown_submission_disarm(
        self,
        *,
        decision_uid: str,
        signal_ts: datetime,
        symbol: str,
        exc: UnknownSubmissionError,
    ) -> None:
        """Immediately quarantine without touching the ordinary reject counter."""
        self.state = "DISARMED"
        try:
            self.store.set_meta("app_state", "DISARMED")
            self.store.insert_decision(
                self.run_id,
                decision_uid,
                signal_ts,
                symbol,
                "UNKNOWN_SUBMISSION",
                {
                    "reason_code": exc.reason_code,
                    "request_id": exc.request_id,
                    "attempt_id": exc.attempt_id,
                },
            )
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                "UNKNOWN_SUBMISSION",
                f"request_id={exc.request_id} attempt_id={exc.attempt_id} "
                f"reason_code={exc.reason_code}",
            )
        except Exception:
            pass

    def _record_order_rejection(
        self,
        decision_uid: str,
        signal_ts: datetime,
        symbol: str,
        reason_code: str,
    ) -> None:
        self._consecutive_order_rejects += 1
        self.store.insert_decision(
            self.run_id,
            decision_uid,
            signal_ts,
            symbol,
            "REJECTED",
            {"reason_code": reason_code},
        )
        self.store.insert_event(
            self.run_id,
            datetime.now(UTC),
            "WARN",
            "ORDER_REJECTED",
            f"count={self._consecutive_order_rejects}; reason_code={reason_code}",
        )
        if self._consecutive_order_rejects >= 3:
            self.disarm()
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "WARN",
                "ORDER_REJECT_LIMIT",
                "three consecutive order rejects",
            )

    async def _risk_inputs_failed(self, exc: Exception) -> None:
        # Fail closed on unreadable risk inputs. In-memory state changes first:
        # the DISARMED verdict must stay observable even when the store that
        # just failed cannot accept the matching writes.
        self.state = "DISARMED"
        self.risk_input_error = f"{type(exc).__name__}: {exc}"
        try:
            self.store.set_meta("app_state", "DISARMED")
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                "RISK_INPUT_FAILED",
                self.risk_input_error,
            )
        except Exception:
            pass
        await self.notifier.send("ERROR", f"RISK_INPUT_FAILED — DISARMED: {self.risk_input_error}")
        try:
            await self._publish("status", self.status())
        except Exception:
            pass

    def status(self) -> dict[str, object]:
        try:
            state = self._app_state()
        except Exception:
            # Store unreadable: report the in-memory state rather than crash
            # the status surface (see _risk_inputs_failed).
            state = self.state
        return {
            "state": state,
            "window": window_status(
                self.store,
                app_state=state,
                stale_after_s=self.window_stale_after_s,
            ),
            "risk_input_error": self.risk_input_error,
            "reconcile_ready": self.reconcile_ready,
            "last_reconcile_ts": self.last_reconcile_ts.isoformat() if self.last_reconcile_ts else None,
            "reconcile_error": self.reconcile_error,
            "full_reconcile_ready": self.full_reconcile_ready(),
            "last_full_reconcile_ts": (
                self.last_full_reconcile_ts.isoformat()
                if self.last_full_reconcile_ts
                else None
            ),
            "full_reconcile_error": self.full_reconcile_error,
            "full_reconcile_attempt_id": self.full_reconcile_attempt_id,
            "submission_quarantine_count": self.store.submission_quarantine_count(),
            "partial_recovery_blocking": self.store.partial_recovery_blocks_new_risk(),
            "run_id": self.run_id,
            "coin": self.coin,
            "timeframe": self.timeframe,
        }

    async def _heartbeat_loop(self) -> None:
        while True:
            await asyncio.sleep(self.heartbeat_hours * 3600)
            positions = await self.broker.positions()
            account = await self.broker.account()
            position = self._position_for(self.coin, positions)
            await self.notifier.heartbeat(
                position=f"{position.size} {position.symbol}" if position else "none",
                equity=f"{account.equity}",
                last_bar=self.bars[-1].ts.isoformat() if self.bars else "none",
            )

    async def _reconcile_loop(self) -> None:
        while True:
            await asyncio.sleep(self.reconcile_interval_s)
            if await self._run_reconcile_cycle():
                await self._publish("equity", {"run_id": self.run_id})

    async def _run_reconcile_cycle(self) -> bool:
        light_ok = await self._run_light_reconcile_cycle()
        # Refresh the *separate* full checkpoint on the same health cadence,
        # deliberately outside the light try/handler above. A full ledger or
        # capture failure therefore can never increment
        # `_consecutive_reconcile_failures`, change `reconcile_ready` /
        # `reconcile_error`, or disarm through the light budget: it only ever
        # latches `full_reconcile_error` and shuts the full gate.
        await self.run_full_reconcile()
        return light_ok

    async def _run_light_reconcile_cycle(self) -> bool:
        try:
            await self.order_manager.reconcile()
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed and keep the health loop alive
            # Defer reconciliation when the broker is mid-rebuild — the old
            # Info client still serves REST calls but its websocket is dead.
            # Class-name string check avoids concrete-broker coupling /
            # circular-import risk.
            if type(exc).__name__ == "HyperliquidNotConfigured" and getattr(self.broker, "rebuilding", False):
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "WARN",
                    "RECONCILE_DEFERRED",
                    "broker rebuilding",
                )
                self._notify_bg("WARN", "RECONCILE_DEFERRED: broker rebuilding")
                return False
            error = type(exc).__name__
            self._consecutive_reconcile_failures += 1
            consecutive = self._consecutive_reconcile_failures
            limit = self.reconcile_max_consecutive_failures
            stack = " > ".join(
                f"{frame.name}:{frame.lineno}"
                for frame in traceback.extract_tb(exc.__traceback__)[-8:]
            )
            self.reconcile_ready = False
            self.reconcile_error = error
            if consecutive < limit:
                detail = f"consecutive={consecutive}/{limit}; error={error}"
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "WARN",
                    "RECONCILE_FAILED_TOLERATED",
                    detail,
                )
                self._notify_bg("WARN", f"RECONCILE_FAILED_TOLERATED: {detail}")
            else:
                detail = (
                    f"consecutive={consecutive}/{limit}; error={error}; "
                    f"stack={stack or 'unavailable'}"
                )
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "ERROR",
                    "RECONCILE_FAILED",
                    detail,
                )
                self._notify_bg("ERROR", f"RECONCILE_FAILED: {detail}")
                if self._app_state() == "ARMED":
                    self.disarm()
            await self._publish("status", self.status())
            return False

        self._consecutive_reconcile_failures = 0
        recovered = not self.reconcile_ready
        self.reconcile_ready = True
        self.last_reconcile_ts = datetime.now(UTC)
        self.reconcile_error = None
        record_liveness(self.store, self.last_reconcile_ts)
        if recovered:
            self.store.insert_event(
                self.run_id,
                self.last_reconcile_ts,
                "INFO",
                "RECONCILE_RECOVERED",
                "periodic reconcile succeeded",
            )
            self._notify_bg("INFO", "RECONCILE_RECOVERED: periodic reconcile succeeded")
            await self._publish("status", self.status())
        return True

    async def _feed_event(self, code: str, detail: str) -> None:
        severity = "WARN" if code in {"DATA_STALE", "DISCONNECT", "RECONNECT_RETRY"} else "INFO"
        self.store.insert_event(self.run_id, datetime.now(UTC), severity, code, detail)
        should_notify = severity != "INFO" or code in {"RECONNECT", "DATA_RESTORED"}
        routine = code in _ROUTINE_FEED_NOTIFICATION_CODES or (
            code == "RECONNECT" and detail.strip() == "attempt=1"
        )
        if should_notify and not routine:
            self._notify_bg(severity, f"{code}: {detail}")
        await self._publish("event", {"code": code, "detail": detail})

    async def _stale_disarm(self) -> None:
        self.disarm()
        await self._publish("status", self.status())

    async def _publish(self, topic: str, data: object) -> None:
        if self.on_update is None:
            return
        result = self.on_update(topic, data)
        if inspect.isawaitable(result):
            await result

    def _ensure_run(self, mode: str) -> None:
        try:
            self.store.create_run(self.run_id, mode, "testnet", {"broker": type(self.broker).__name__})
        except sqlite3.IntegrityError:
            return

    def _app_state(self) -> str:
        if self.store.has_submission_quarantine():
            self.state = "DISARMED"
            try:
                self.store.set_meta("app_state", "DISARMED")
            except Exception:
                pass
            return self.state
        if self.store.partial_recovery_blocks_new_risk():
            self.state = "DISARMED"
            try:
                self.store.set_meta("app_state", "DISARMED")
            except Exception:
                pass
            return self.state
        if self.risk_input_error is not None:
            # Sticky fail-closed: after a risk-input failure the engine stays
            # DISARMED until a human re-arms, even if the DISARMED meta write
            # itself failed and the persisted value still says ARMED.
            self.state = "DISARMED"
            return self.state
        persisted = self.store.get_meta("app_state")
        if persisted is not None:
            self.state = persisted
        return self.state

    def _set_state(self, state: str) -> None:
        previous = self.state
        self.state = state
        self.store.set_meta("app_state", state)
        if state != previous and state in {"DISARMED", "KILLED", "ARMED"}:
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "INFO" if state == "ARMED" else "WARN",
                "STATE_TRANSITION",
                f"{previous}->{state}",
            )
            self._notify_bg("WARN" if state != "ARMED" else "INFO", f"state -> {state}")

    def _notify_bg(self, severity: str, message: str) -> None:
        """Fire-and-forget notification; never blocks the trading path."""
        if self.notifier is None or not self.notifier.enabled:
            return
        try:
            asyncio.get_running_loop().create_task(self.notifier.send(severity, message))
        except RuntimeError:
            pass  # no running loop (sync replay/tests) — skip silently

    @staticmethod
    def _position_for(coin: str, positions: list[Position]) -> Position | None:
        return next((position for position in positions if position.symbol == coin and position.size != 0), None)

    @staticmethod
    def _is_opposite(position: Position, direction: str) -> bool:
        return (position.size > 0 and direction == "SHORT") or (position.size < 0 and direction == "LONG")
