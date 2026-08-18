"""Continuous bridge engine plus deterministic replay entry point."""

from __future__ import annotations

import asyncio
import inspect
import json
import sqlite3
import traceback
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Callable

from bridge.broker.base import Broker
from bridge.engine.bars import BarFeed
from bridge.engine.llm_gate import NullLLMGate
from bridge.engine.notify import TelegramNotifier, build_notifier
from bridge.engine.orders import OrderManager
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

        # TS-P1-003: scan durable active attempts and run read-only recovery
        await self._recover_unknown_submissions()

        await self.order_manager.reconcile()
        self.reconcile_ready = True
        self.last_reconcile_ts = datetime.now(UTC)
        self.reconcile_error = None
        record_liveness(self.store, self.last_reconcile_ts)
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

        # TS-P1-003: block ARM when active quarantine exists
        if hasattr(self.store, "has_active_quarantine") and self.store.has_active_quarantine():
            active = self.store.get_active_quarantine_attempts()
            raise RuntimeError(
                f"Active unknown-submission quarantine exists "
                f"({len(active)} attempt(s)); resolve or confirm absence first"
            )

        if not self.reconcile_ready:
            raise RuntimeError("startup reconcile incomplete")
        max_age = timedelta(seconds=max(self.reconcile_interval_s * 3, 30.0))
        if self.last_reconcile_ts is None or now - self.last_reconcile_ts > max_age:
            self.reconcile_ready = False
            self.reconcile_error = "STALE"
            raise RuntimeError("reconcile evidence stale")
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
        for order in await self.broker.open_orders():
            if order.role == "ENTRY":
                await self.broker.cancel(order.cloid)
        await self.order_manager.reconcile()
        await self._publish("status", self.status())

    async def kill(self, flatten: bool = False) -> None:
        self._kill_requested = True
        self._set_state("KILLED")
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

    async def on_bar(self, bar: Bar, process_broker_bar: bool = False) -> None:
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

        if self._app_state() != "ARMED" or self._kill_requested:
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
        except Exception as exc:
            # TS-P1-003: distinguish UNKNOWN_SUBMISSION from definitive rejection
            exc_name = type(exc).__name__
            is_unknown = (
                hasattr(exc, 'code') and getattr(exc, 'code', '') == 'UNKNOWN_SUBMISSION'
            ) or exc_name in {"TimeoutError", "ConnectionError"}

            if is_unknown:
                # UNKNOWN_SUBMISSION: immediate DISARM, no counter increment
                self.disarm()
                self.store.insert_decision(
                    self.run_id,
                    decision_uid,
                    signal.ts,
                    signal.symbol,
                    "UNKNOWN_SUBMISSION",
                    {"reason": exc_name, "detail": str(exc)[:500]},
                )
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "ERROR",
                    "UNKNOWN_SUBMISSION_DISARM",
                    f"decision_uid={decision_uid} error={exc_name}",
                )
                self._consecutive_order_rejects = 0
                return

            self._consecutive_order_rejects += 1
            self.store.insert_decision(
                self.run_id,
                decision_uid,
                signal.ts,
                signal.symbol,
                "REJECTED",
                {"reason": type(exc).__name__, "detail": str(exc)},
            )
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "WARN",
                "ORDER_REJECTED",
                f"count={self._consecutive_order_rejects}; error={type(exc).__name__}",
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
            return
        if result is not None:
            self._consecutive_order_rejects = 0
            self.store.insert_decision(self.run_id, decision_uid, signal.ts, signal.symbol, "SUBMITTED", result)
        await self._publish("decision", {"decision_uid": decision_uid})

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

    async def _recover_unknown_submissions(self) -> None:
        """Scan durable active attempts and run read-only recovery on startup.

        Never places, cancels, flattens, re-protects, or mutates exchange state.
        If any SUBMITTING or UNKNOWN_SUBMISSION attempt is found, immediately
        DISARM and block ARM.
        """
        if not hasattr(self.store, "get_active_attempts_for_recovery"):
            return

        attempts = self.store.get_active_attempts_for_recovery()
        if not attempts:
            return

        # Any active quarantine → immediate DISARM
        self.disarm()
        self.store.insert_event(
            self.run_id,
            datetime.now(UTC),
            "WARN",
            "QUARANTINE_FOUND_ON_STARTUP",
            f"{len(attempts)} active unknown-submission attempt(s); engine DISARMED",
        )

        for attempt in attempts:
            request_id = str(attempt["request_id"])
            state = str(attempt["state"])
            try:
                planned_cloids = json.loads(str(attempt["planned_cloids_json"]))
            except (TypeError, ValueError):
                planned_cloids = {}

            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "INFO",
                "QUARANTINE_RECOVERY_START",
                f"request_id={request_id} state={state}",
            )

            # Read-only evidence collection
            try:
                evidence = await self.broker.recovery_evidence(
                    planned_cloids,
                    str(attempt.get("created_ts", "")),
                )
            except Exception as exc:
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "WARN",
                    "RECOVERY_EVIDENCE_FAILED",
                    f"request_id={request_id} error={type(exc).__name__}",
                )
                continue

            # Persist evidence
            cycle_id = f"{request_id}:recovery:{datetime.now(UTC).isoformat()}"
            self.store.insert_recovery_evidence(
                request_id=request_id,
                cycle_id=cycle_id,
                verdict=evidence.verdict.value,
                planned_cloids=evidence.planned_cloids,
                found_cloids=evidence.found_cloids,
                sources_checked=evidence.sources_checked,
                sources_complete=evidence.sources_complete,
                reason_codes=evidence.reason_codes,
                ts_start=evidence.ts_start,
                ts_end=evidence.ts_end or datetime.now(UTC).isoformat(),
                attempt_window_covered=evidence.attempt_window_covered,
            )

            if evidence.verdict.value == "PRESENT":
                # Confirmed presence — permanently DISARMED
                self.store.transition_attempt_state(
                    request_id, ["SUBMITTING", "UNKNOWN_SUBMISSION"],
                    "CONFIRMED_PRESENT", "RECOVERY_FOUND_PRESENT",
                )
                self.store.insert_event(
                    self.run_id, datetime.now(UTC), "ERROR",
                    "QUARANTINE_CONFIRMED_PRESENT",
                    f"request_id={request_id} found_cloids={','.join(evidence.found_cloids)}",
                )
            elif evidence.verdict.value == "INCOMPLETE" or evidence.verdict.value == "CONFLICTING":
                # Ensure UNKNOWN_SUBMISSION (may have been SUBMITTING)
                self.store.transition_attempt_state(
                    request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION", "RECOVERY_INCOMPLETE",
                )
                self.store.transition_attempt_state(
                    request_id, ["UNKNOWN_SUBMISSION"], "UNKNOWN_SUBMISSION", "RECOVERY_INCOMPLETE",
                )
            elif evidence.verdict.value == "ABSENT_CANDIDATE":
                # Ensure UNKNOWN_SUBMISSION, then check streak
                self.store.transition_attempt_state(
                    request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION", "RECOVERY_ABSENT_CANDIDATE",
                )
                streak, first_ts, last_ts = self.store.get_absent_candidate_streak(request_id)
                if streak >= 3 and first_ts and last_ts:
                    try:
                        t1 = datetime.fromisoformat(first_ts.replace("Z", "+00:00"))
                        t2 = datetime.fromisoformat(last_ts.replace("Z", "+00:00"))
                        span = (t2 - t1).total_seconds()
                        if span >= 120:
                            self.store.transition_attempt_state(
                                request_id, ["UNKNOWN_SUBMISSION"],
                                "CONFIRMED_ABSENT", "RECOVERY_ABSENCE_CONFIRMED",
                            )
                            self.store.insert_event(
                                self.run_id, datetime.now(UTC), "INFO",
                                "QUARANTINE_CONFIRMED_ABSENT",
                                f"request_id={request_id} cycles={streak} span_s={span:.1f}",
                            )
                    except (ValueError, TypeError):
                        pass

    def status(self) -> dict[str, object]:
        try:
            state = self._app_state()
        except Exception:
            # Store unreadable: report the in-memory state rather than crash
            # the status surface (see _risk_inputs_failed).
            state = self.state
        quarantine_count = 0
        try:
            if hasattr(self.store, "get_active_quarantine_attempts"):
                quarantine_count = len(self.store.get_active_quarantine_attempts())
        except Exception:
            pass
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
            "run_id": self.run_id,
            "coin": self.coin,
            "timeframe": self.timeframe,
            "quarantine_attempts": quarantine_count,
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
