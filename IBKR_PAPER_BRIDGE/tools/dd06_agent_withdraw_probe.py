"""WP-P0-29 DD-06 falsification probe (Hyperliquid TESTNET only): can an agent (API) wallet move funds?

PREPARATION artifact under ``OD-20260915-P029-DD06-TESTNET-PROBE-PREP-1``. Execution needs a second,
separate owner word ("probe steps approved") and runs from the KVM2-P4-03 environment with faucet money.

What it does, in order, with the agent key found in the process environment (never printed):
  S0  identity: the wallet derived from ``HL_API_WALLET_KEY`` must differ from ``HL_ACCOUNT_ADDRESS``
      (a master key in the agent slot is refused); ``extraAgents`` of the account is read for the record.
  S1  control arm: the agent places one minimal resting limit order far below market and cancels it.
      Expected: accepted (proves the agent key works for the actions agents are meant to perform).
  S2  the falsification arms, each expected REFUSED by the venue:
        withdraw3 (``withdraw_from_bridge``), usdSend (``usd_transfer``), spotSend (``spot_transfer``),
        sub-account transfer (only when ``--sub-account`` names a testnet sub-account),
        approveAgent (``approve_agent``; the locally generated candidate key is discarded unseen).
      Destinations are the account's own master address. usdSend/spotSend would be self-transfers
      inside the venue account. withdraw3 is different: if the venue did NOT refuse it, funds WOULD
      LEAVE the venue account (a bridge withdrawal to the owner's own address on the bridge chain;
      testnet faucet money); its amount sits above the documented bridge minimum so a refusal cannot
      be an amount refusal. If a fund-moving arm is NOT refused, the probe stops immediately and
      records a FINDING; DD-06 then stays BLOCK. Every refusal is classified by its venue text:
      AUTHORIZATION (agent/permission wording) counts for DD-06; VALIDATION (amount, token, nonce,
      self-send, sub-account existence) or UNCLASSIFIED does not, and makes the run INCONCLUSIVE.
Every request and response is recorded with 40- and 64-hex strings redacted; the output directory is
write-once. ``--dry-run`` prints the plan and touches no network and no credential.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Protocol

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bridge.broker.hyperliquid import round_hl_price  # noqa: E402 - the Bridge's own wire rounding

TESTNET_URL = "https://api.hyperliquid-testnet.xyz"
PROBE_VERSION = "dd06-probe/v1"
CONTROL_COIN = "BTC"
CONTROL_PRICE_FRACTION = 0.90  # resting bid at 90 % of mid: cannot fill
CONTROL_MIN_NOTIONAL_USD = 10.5  # venue minimum is $10; keep a margin for rounding
TRANSFER_AMOUNT_USDC = 1.0
WITHDRAW_AMOUNT_USDC = 6.0  # above the documented 5 USDC bridge minimum + 1 USDC fee: a refusal cannot be an amount refusal
SUB_ACCOUNT_TRANSFER_USD_MICRO = 1_000_000  # 1 USDC in the SDK's integer unit
FUND_MOVING_ARMS = ("withdraw3", "usdSend", "spotSend", "subAccountTransfer")
STOP_ON_NOT_REFUSED = True

_HEX64 = re.compile(r"(?i)(?:0x)?[0-9a-f]{64,}")
_HEX40 = re.compile(r"(?i)0x[0-9a-f]{40}")


class ProbeRefused(RuntimeError):
    """The probe refused to start; the message never carries credential material."""


def redact(value: object, cap: int = 4000) -> str:
    """Redact private-key-shaped and address-shaped hex from any value."""
    try:
        text = (
            value
            if isinstance(value, str)
            else json.dumps(value, default=str, sort_keys=True)
        )
    except Exception:  # pragma: no cover - defensive
        text = str(value)
    text = _HEX64.sub("[redacted-64hex]", text)
    text = _HEX40.sub("[redacted-address]", text)
    return text[:cap]


class InfoLike(Protocol):
    def user_state(self, address: str) -> Any: ...
    def spot_user_state(self, address: str) -> Any: ...
    def extra_agents(self, address: str) -> Any: ...
    def all_mids(self) -> Any: ...
    def meta(self) -> Any: ...


class ExchangeLike(Protocol):
    def order(
        self,
        name: str,
        is_buy: bool,
        sz: float,
        limit_px: float,
        order_type: Any,
        reduce_only: bool = False,
    ) -> Any: ...
    def cancel(self, name: str, oid: int) -> Any: ...
    def withdraw_from_bridge(self, amount: float, destination: str) -> Any: ...
    def usd_transfer(self, amount: float, destination: str) -> Any: ...
    def spot_transfer(self, amount: float, destination: str, token: str) -> Any: ...
    def sub_account_transfer(
        self, sub_account_user: str, is_deposit: bool, usd: int
    ) -> Any: ...
    def approve_agent(self, name: str | None = None) -> Any: ...


@dataclass
class ProbeRecord:
    run_id: str
    network: str
    account_address_redacted: str
    agent_address_redacted: str
    started_utc: str
    steps: list[dict[str, Any]] = field(default_factory=list)
    result: str = "RUNNING"
    finding: str | None = None

    def step(self, name: str, outcome: str, data: dict[str, Any]) -> None:
        self.steps.append(
            {"name": name, "outcome": outcome, "ts": _now(), "data": data}
        )


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def per_status_errors(response: Any) -> list[str]:
    """Venue ok-envelopes for orders carry per-request results in response.data.statuses; an entry with an
    ``error`` key means the venue rejected THAT request (r1 on testnet: ``Price must be divisible by tick size``)."""
    if not isinstance(response, dict):
        return []
    inner = response.get("response")
    data = inner.get("data") if isinstance(inner, dict) else None
    statuses = data.get("statuses") if isinstance(data, dict) else None
    if not isinstance(statuses, list):
        return []
    return [str(s["error"]) for s in statuses if isinstance(s, dict) and "error" in s]


def classify_response(response: Any) -> str:
    """REFUSED for a venue error envelope or an ok envelope whose per-request statuses carry an error;
    NOT_REFUSED for a clean ok envelope; INCONCLUSIVE otherwise."""
    if isinstance(response, dict):
        status = response.get("status")
        if status == "err":
            return "REFUSED"
        if status == "ok":
            return "REFUSED" if per_status_errors(response) else "NOT_REFUSED"
    return "INCONCLUSIVE"


def classify_exception(exc: BaseException) -> str:
    """A 4xx client error is the venue refusing the request; anything else is transport/other."""
    name = type(exc).__name__
    if name == "ClientError":
        return "REFUSED"
    if name == "ServerError":
        return "ERROR"
    return "ERROR"


AUTHORIZATION_MARKERS = (
    "must be user",
    "does not exist",
    "not authorized",
    "unauthorized",
    "not allowed",
    "not permitted",
    "permission",
    "agent",
    "api wallet",
    "only the user",
    "user signature",
)
VALIDATION_MARKERS = (
    "minimum",
    "min ",
    "amount",
    "insufficient",
    "invalid destination",
    "same address",
    "self",
    "token",
    "nonce",
    "sub-account",
    "subaccount",
    "does not have a sub",
    "not found",
    "invalid",
)


def classify_refusal_text(message: object) -> str:
    """AUTHORIZATION when the venue's own words say the signer may not act; VALIDATION when they name
    an amount/token/nonce/destination problem; UNCLASSIFIED otherwise. Only AUTHORIZATION is DD-06
    evidence; the other two make the arm inconclusive. Authorization markers win over validation
    markers when both appear ("agent may not send this amount")."""
    text = str(message or "").lower()
    if any(marker in text for marker in AUTHORIZATION_MARKERS):
        return "AUTHORIZATION"
    if any(marker in text for marker in VALIDATION_MARKERS):
        return "VALIDATION"
    return "UNCLASSIFIED"


def refuse_unless_testnet(network: str, environ: dict[str, str]) -> None:
    if network != "testnet":
        raise ProbeRefused(
            "DD-06 probe runs on testnet only; mainnet is refused by design"
        )
    if environ.get("HL_LIVE_ACK", "").strip():
        raise ProbeRefused(
            "HL_LIVE_ACK is present in the environment; the probe refuses to run beside a live acknowledgement"
        )


def refuse_master_key(agent_address: str, account_address: str) -> None:
    if agent_address.lower() == account_address.lower():
        raise ProbeRefused(
            "the key in HL_API_WALLET_KEY derives to HL_ACCOUNT_ADDRESS itself (a master key); "
            "the probe tests an AGENT wallet and refuses to hold a master key"
        )


def control_order_size(mid_px: float, sz_decimals: int) -> tuple[float, float]:
    """Resting bid price (rounded DOWN to the venue's wire constraints: at most 5 significant figures and
    6 - szDecimals decimals, via the Bridge's own ``round_hl_price``) and the smallest size clearing the
    venue's minimum notional. r1 on testnet (2026-09-15) was rejected with ``Price must be divisible by
    tick size`` because ``round(mid * 0.9, 1)`` produced a 6-significant-figure price."""
    limit_px = round_hl_price(mid_px * CONTROL_PRICE_FRACTION, sz_decimals)
    step = 10 ** (-sz_decimals)
    size = math.ceil(CONTROL_MIN_NOTIONAL_USD / limit_px / step) * step
    return limit_px, round(size, sz_decimals)


def _attempt(
    record: ProbeRecord, name: str, request: dict[str, Any], call: Callable[[], Any]
) -> str:
    """Run one arm, record the redacted request/response, return the outcome."""
    try:
        response = call()
    except BaseException as exc:  # noqa: BLE001 - every exception is evidence here
        outcome = classify_exception(exc)
        data = {
            "request": redact(request),
            "error_type": type(exc).__name__,
            "error": redact(str(exc)),
        }
        if outcome == "REFUSED":
            data["refusal_class"] = classify_refusal_text(str(exc))
        record.step(name, outcome, data)
        return outcome
    if name == "approveAgent" and isinstance(response, tuple):
        # (venue_result, generated_agent_key): the key is discarded before anything is recorded
        response = response[0]
    outcome = classify_response(response)
    data = {"request": redact(request), "response": redact(response)}
    if outcome == "REFUSED":
        errors = per_status_errors(response)
        venue_text = (
            "; ".join(errors)
            if errors
            else (response.get("response") if isinstance(response, dict) else response)
        )
        data["refusal_class"] = classify_refusal_text(venue_text)
    record.step(name, outcome, data)
    return outcome


def run_probe(
    *,
    record: ProbeRecord,
    info: InfoLike,
    exchange: ExchangeLike,
    account_address: str,
    sub_account: str | None,
    include_usd_class_transfer: bool = False,
) -> ProbeRecord:
    # S0 identity
    try:
        agents = info.extra_agents(account_address)
        record.step("S0_extra_agents", "RECORDED", {"extra_agents": redact(agents)})
    except BaseException as exc:  # noqa: BLE001
        record.step(
            "S0_extra_agents",
            "ERROR",
            {"error_type": type(exc).__name__, "error": redact(str(exc))},
        )
    try:
        state = info.user_state(account_address)
        summary = state.get("marginSummary", {}) if isinstance(state, dict) else {}
        record.step(
            "S0_user_state",
            "RECORDED",
            {
                "accountValue": redact(summary.get("accountValue")),
                "withdrawable": redact(
                    state.get("withdrawable") if isinstance(state, dict) else None
                ),
            },
        )
    except BaseException as exc:  # noqa: BLE001
        record.step(
            "S0_user_state",
            "ERROR",
            {"error_type": type(exc).__name__, "error": redact(str(exc))},
        )
    # A unifiedAccount keeps its USDC in the spot balance (perp accountValue reads 0.0 — r1 on testnet);
    # record it so the balance behind the transfer arms is visible in the record.
    try:
        spot = info.spot_user_state(account_address)
        balances = spot.get("balances", []) if isinstance(spot, dict) else []
        usdc = next(
            (b for b in balances if isinstance(b, dict) and b.get("coin") == "USDC"),
            {},
        )
        record.step(
            "S0_spot_user_state",
            "RECORDED",
            {
                "usdc_total": redact(usdc.get("total")),
                "usdc_hold": redact(usdc.get("hold")),
            },
        )
    except BaseException as exc:  # noqa: BLE001
        record.step(
            "S0_spot_user_state",
            "ERROR",
            {"error_type": type(exc).__name__, "error": redact(str(exc))},
        )

    # S1 control arm
    try:
        mids = info.all_mids()
        mid_px = float(mids[CONTROL_COIN])
        meta = info.meta()
        universe = meta.get("universe", []) if isinstance(meta, dict) else []
        coin_meta = next(
            (row for row in universe if row.get("name") == CONTROL_COIN), None
        )
        if coin_meta is None:
            raise RuntimeError(f"{CONTROL_COIN} metadata not found")
        limit_px, size = control_order_size(mid_px, int(coin_meta["szDecimals"]))
    except BaseException as exc:  # noqa: BLE001
        record.step(
            "S1_control_plan",
            "ERROR",
            {"error_type": type(exc).__name__, "error": redact(str(exc))},
        )
        record.result = "ABORTED_CONTROL_PLAN"
        return record
    order_request = {
        "coin": CONTROL_COIN,
        "is_buy": True,
        "sz": size,
        "limit_px": limit_px,
        "order_type": {"limit": {"tif": "Gtc"}},
        "reduce_only": False,
    }
    order_outcome = _attempt(
        record,
        "S1_control_order",
        order_request,
        lambda: exchange.order(
            CONTROL_COIN, True, size, limit_px, {"limit": {"tif": "Gtc"}}, False
        ),
    )
    oid = _resting_oid(record.steps[-1].get("data", {}))
    if order_outcome != "NOT_REFUSED" or oid is None:
        record.result = "ABORTED_CONTROL_ARM_NOT_ACCEPTED"
        return record
    cancel_outcome = _attempt(
        record,
        "S1_control_cancel",
        {"coin": CONTROL_COIN, "oid": oid},
        lambda: exchange.cancel(CONTROL_COIN, oid),
    )
    if cancel_outcome != "NOT_REFUSED":
        record.result = "ABORTED_CONTROL_CANCEL_FAILED"
        record.finding = "control order rests on the book and could not be cancelled by the probe; cancel it by hand before anything else"
        return record

    # S2 falsification arms (each expected REFUSED)
    arms: list[tuple[str, dict[str, Any], Callable[[], Any]]] = [
        (
            "withdraw3",
            {"amount": WITHDRAW_AMOUNT_USDC, "destination": "[account]"},
            lambda: exchange.withdraw_from_bridge(
                WITHDRAW_AMOUNT_USDC, account_address
            ),
        ),
        (
            "usdSend",
            {"amount": TRANSFER_AMOUNT_USDC, "destination": "[account]"},
            lambda: exchange.usd_transfer(TRANSFER_AMOUNT_USDC, account_address),
        ),
        (
            "spotSend",
            {
                "amount": TRANSFER_AMOUNT_USDC,
                "destination": "[account]",
                "token": "USDC",
            },
            lambda: exchange.spot_transfer(
                TRANSFER_AMOUNT_USDC, account_address, "USDC"
            ),
        ),
    ]
    if sub_account:
        arms.append(
            (
                "subAccountTransfer",
                {
                    "sub_account_user": "[sub-account]",
                    "is_deposit": True,
                    "usd": SUB_ACCOUNT_TRANSFER_USD_MICRO,
                },
                lambda: exchange.sub_account_transfer(
                    sub_account, True, SUB_ACCOUNT_TRANSFER_USD_MICRO
                ),
            )
        )
    else:
        record.step(
            "subAccountTransfer",
            "SKIPPED_NO_SUB_ACCOUNT",
            {
                "note": "no --sub-account given; the testnet account has none (P0-28 read: 0 sub-accounts on mainnet; testnet not read)"
            },
        )
    if include_usd_class_transfer:
        arms.append(
            (
                "usdClassTransfer",
                {"amount": TRANSFER_AMOUNT_USDC, "to_perp": False},
                lambda: exchange.usd_class_transfer(TRANSFER_AMOUNT_USDC, False),
            )
        )  # type: ignore[attr-defined]
    arms.append(
        (
            "approveAgent",
            {"name": "dd06-probe-candidate"},
            lambda: exchange.approve_agent("dd06-probe-candidate"),
        )
    )

    refused = 0
    authorization_refusals = 0
    for index, (name, request, call) in enumerate(arms):
        outcome = _attempt(record, name, request, call)
        if outcome == "REFUSED":
            refused += 1
            if record.steps[-1]["data"].get("refusal_class") == "AUTHORIZATION":
                authorization_refusals += 1
            continue
        if outcome == "NOT_REFUSED":
            record.finding = f"{name} was NOT refused for an agent wallet"
            record.result = "DD06_FINDING_NOT_REFUSED"
            if STOP_ON_NOT_REFUSED:
                for later_name, _, _ in arms[index + 1 :]:
                    record.step(later_name, "SKIPPED_AFTER_FINDING", {})
                return record
    if record.result == "RUNNING":
        if refused == len(arms) and authorization_refusals == len(arms):
            record.result = "DD06_REFUSALS_OBSERVED"
        else:
            record.result = "DD06_INCONCLUSIVE"
            if refused == len(arms):
                record.finding = (
                    "every arm was refused, but not every refusal names the signer's "
                    "authority; read the recorded venue texts before drawing any DD-06 conclusion"
                )
    return record


def _resting_oid(data: dict[str, Any]) -> int | None:
    """Extract the resting order id from a recorded (redacted) order response."""
    text = data.get("response")
    if not isinstance(text, str):
        return None
    match = re.search(r'"oid":\s*(\d+)', text)
    return int(match.group(1)) if match else None


def write_record(out_dir: Path, record: ProbeRecord) -> Path:
    out_dir = Path(out_dir)
    if out_dir.exists():
        raise ProbeRefused(f"output directory already exists (write-once): {out_dir}")
    out_dir.mkdir(parents=True)
    payload = {
        "probe_version": PROBE_VERSION,
        "run_id": record.run_id,
        "network": record.network,
        "account_address": record.account_address_redacted,
        "agent_address": record.agent_address_redacted,
        "started_utc": record.started_utc,
        "finished_utc": _now(),
        "result": record.result,
        "finding": record.finding,
        "steps": record.steps,
    }
    raw = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    text = raw.decode("utf-8")
    if _HEX64.search(text):
        raise ProbeRefused("refusing to write: a 64-hex string survived redaction")
    if _HEX40.search(text):
        raise ProbeRefused(
            "refusing to write: a 0x-prefixed address survived redaction"
        )
    path = out_dir / "DD06_PROBE_RECORD.json"
    with path.open("xb") as handle:
        handle.write(raw)
    (out_dir / "DD06_PROBE_RECORD.json.sha256").write_text(
        hashlib.sha256(raw).hexdigest() + "\n", encoding="ascii"
    )
    return path


def plan_text(sub_account: str | None, include_usd_class_transfer: bool) -> str:
    lines = [
        f"{PROBE_VERSION} — TESTNET ONLY ({TESTNET_URL})",
        "S0 identity: agent address != account address (else refuse); extraAgents + user_state recorded",
        f"S1 control: resting {CONTROL_COIN} bid at {int(CONTROL_PRICE_FRACTION * 100)} % of mid, smallest size >= ${CONTROL_MIN_NOTIONAL_USD} notional, then cancel",
        f"S2 arms (expected REFUSED): withdraw3 {WITHDRAW_AMOUNT_USDC} USDC -> own address on the bridge chain; usdSend {TRANSFER_AMOUNT_USDC} -> own account; spotSend {TRANSFER_AMOUNT_USDC} USDC -> own account;",
        f"    subAccountTransfer: {'1 USDC deposit to ' + redact(sub_account) if sub_account else 'SKIPPED (no --sub-account)'}; usdClassTransfer: {'included' if include_usd_class_transfer else 'not included'}; approveAgent (candidate key discarded unseen)",
        "Stop rule: a NOT_REFUSED fund-moving arm stops the sequence and records a FINDING (DD-06 stays BLOCK).",
        "Refusal classes: AUTHORIZATION counts for DD-06; VALIDATION / UNCLASSIFIED -> INCONCLUSIVE (read the venue text).",
        "Record: write-once JSON + sha256, 40/64-hex redacted. No key is ever printed.",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--out", required=True, help="write-once output directory")
    parser.add_argument(
        "--network", default="testnet", help="only 'testnet' is accepted"
    )
    parser.add_argument(
        "--sub-account",
        default=None,
        help="testnet sub-account address for the sub-account transfer arm (optional)",
    )
    parser.add_argument("--include-usd-class-transfer", action="store_true")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the plan; no network, no credential read",
    )
    args = parser.parse_args(argv)

    if args.dry_run:
        print(plan_text(args.sub_account, args.include_usd_class_transfer))
        return 0
    try:
        refuse_unless_testnet(args.network, dict(os.environ))
        from eth_account import Account  # noqa: PLC0415 - imported only for a real run
        from hyperliquid.exchange import Exchange  # noqa: PLC0415
        from hyperliquid.info import Info  # noqa: PLC0415

        from bridge.settings import resolve_hyperliquid_credentials  # noqa: PLC0415

        account_address, api_key, source = resolve_hyperliquid_credentials()
        wallet = Account.from_key(api_key)
        del api_key
        refuse_master_key(wallet.address, account_address)
    except ProbeRefused as exc:
        print(f"PROBE_REFUSED: {exc}", file=sys.stderr)
        return 3
    record = ProbeRecord(
        run_id=args.run_id,
        network="testnet",
        account_address_redacted=redact(account_address),
        agent_address_redacted=redact(wallet.address),
        started_utc=_now(),
    )
    record.step(
        "credential_source",
        "RECORDED",
        {"source": source, "env_names": ["HL_ACCOUNT_ADDRESS", "HL_API_WALLET_KEY"]},
    )
    info = Info(TESTNET_URL, skip_ws=True)
    exchange = Exchange(wallet, TESTNET_URL, account_address=account_address)
    run_probe(
        record=record,
        info=info,
        exchange=exchange,
        account_address=account_address,
        sub_account=args.sub_account,
        include_usd_class_transfer=args.include_usd_class_transfer,
    )
    path = write_record(Path(args.out), record)
    print(f"{record.result} record={path}")
    return 0 if record.result == "DD06_REFUSALS_OBSERVED" else 2


if __name__ == "__main__":
    sys.exit(main())
