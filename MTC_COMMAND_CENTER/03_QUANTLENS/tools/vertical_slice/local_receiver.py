"""Pure local receiver for SYSTEM_TEST_ONLY signal payloads."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .contracts import redact_sensitive_fields, validate_signal_payload


@dataclass
class ReceiverState:
    expected_auth_token: str
    seen_idempotency_keys: set[str] = field(default_factory=set)
    position: dict[str, Any] | None = None
    received_rows: list[dict[str, Any]] = field(default_factory=list)
    fills: list[dict[str, Any]] = field(default_factory=list)


class LocalReceiver:
    def __init__(self, state: ReceiverState):
        self.state = state

    def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        env = payload.get("environment")
        if env in {"live", "testnet"}:
            return self._record(payload, "rejected(environment)", f"{env} is forbidden")

        validation = validate_signal_payload(payload, self.state.expected_auth_token)
        if not validation.ok:
            reason = "; ".join(validation.errors)
            return self._record(payload, self._validation_disposition(validation.errors), reason)

        idempotency_key = str(payload["idempotency_key"])
        if idempotency_key in self.state.seen_idempotency_keys:
            return self._record(payload, "duplicate_dropped", "duplicate idempotency_key")

        action = payload["action"]
        if action == "ENTRY":
            if self.state.position is not None:
                return self._record(payload, "rejected(entry_while_open)", "entry_while_open")
            self.state.seen_idempotency_keys.add(idempotency_key)
            row = self._record(payload, "accepted", None)
            self.state.position = {
                "side": payload["side"],
                "entry_price": payload.get("entry_price"),
                "stop_loss": payload.get("stop_loss"),
                "entry_signal_id": payload["signal_id"],
            }
            self.state.fills.append(
                {
                    "signal_id": payload["signal_id"],
                    "action": "ENTRY",
                    "side": payload["side"],
                    "price": payload.get("entry_price"),
                    "timestamp_utc": payload["timestamp_utc"],
                    "simulated": True,
                }
            )
            return row

        if action == "EXIT":
            if self.state.position is None:
                return self._record(
                    payload,
                    "rejected(exit_with_no_position)",
                    "exit_with_no_position",
                )
            self.state.seen_idempotency_keys.add(idempotency_key)
            row = self._record(payload, "accepted", None)
            self.state.position = None
            self.state.fills.append(
                {
                    "signal_id": payload["signal_id"],
                    "action": "EXIT",
                    "side": payload["side"],
                    "price": payload.get("exit_price"),
                    "timestamp_utc": payload["timestamp_utc"],
                    "simulated": True,
                }
            )
            return row

        return self._record(payload, "rejected(action)", f"unsupported action {action}")

    @staticmethod
    def _validation_disposition(errors: tuple[str, ...]) -> str:
        joined = " ".join(errors)
        if "checksum" in joined:
            return "rejected(checksum)"
        if "auth_token" in joined:
            return "rejected(auth)"
        if (
            "positive" in joined
            or "stop_loss" in joined
            or "numeric" in joined
            or "entry_price" in joined
        ):
            return "rejected(semantic)"
        return "rejected(malformed)"

    def _record(
        self,
        payload: dict[str, Any],
        disposition: str,
        reason: str | None,
    ) -> dict[str, Any]:
        row = {
            "signal_id": payload.get("signal_id", "<missing>"),
            "idempotency_key": payload.get("idempotency_key"),
            "action": payload.get("action"),
            "environment": payload.get("environment"),
            "disposition": disposition,
            "reason": reason,
            "payload": redact_sensitive_fields(payload),
        }
        self.state.received_rows.append(row)
        return row
