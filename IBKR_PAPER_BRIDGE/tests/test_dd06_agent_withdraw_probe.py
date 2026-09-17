"""Fixture tests for the DD-06 testnet falsification probe. No network; fake venue objects only."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import dd06_agent_withdraw_probe as probe

ACCOUNT = "0x" + "a1" * 20
AGENT = "0x" + "b2" * 20
FAKE_KEY_64 = "0x" + "c3" * 32


class _ClientError(Exception):
    """Mirrors hyperliquid.utils.error.ClientError by name (that is what the classifier keys on)."""


_ClientError.__name__ = "ClientError"


class _ServerError(Exception):
    pass


_ServerError.__name__ = "ServerError"


class FakeInfo:
    def __init__(self, mid: float = 60000.0) -> None:
        self.mid = mid

    def user_state(self, address: str):
        return {"marginSummary": {"accountValue": "0.0"}, "withdrawable": "0.0"}

    def spot_user_state(self, address: str):
        return {"balances": [{"coin": "USDC", "total": "998.987457", "hold": "0.0"}]}

    def extra_agents(self, address: str):
        return [
            {"address": AGENT, "name": "bridge-testnet", "validUntil": 1790000000000}
        ]

    def all_mids(self):
        return {"BTC": str(self.mid)}

    def meta(self):
        return {"universe": [{"name": "BTC", "szDecimals": 5}]}


class FakeExchange:
    """Every fund-moving action refused by the venue; control arm accepted."""

    def __init__(self) -> None:
        self.calls: list[str] = []
        self.refusal = (
            "err"  # "err" -> ok-envelope with status err; "raise" -> ClientError
        )

    def _refuse(self, name: str):
        self.calls.append(name)
        if self.refusal == "raise":
            raise _ClientError(
                422,
                None,
                f"User or API Wallet {AGENT} does not exist. key {FAKE_KEY_64}",
                {},
            )
        return {
            "status": "err",
            "response": f"Must be user; agent {AGENT} may not {name}; key {FAKE_KEY_64}",
        }

    def order(self, name, is_buy, sz, limit_px, order_type, reduce_only=False):
        self.calls.append("order")
        assert is_buy and not reduce_only and limit_px < 60000 and sz * limit_px >= 10.0
        return {
            "status": "ok",
            "response": {
                "type": "order",
                "data": {"statuses": [{"resting": {"oid": 60109082440}}]},
            },
        }

    def cancel(self, name, oid):
        self.calls.append(f"cancel:{oid}")
        return {
            "status": "ok",
            "response": {"type": "cancel", "data": {"statuses": ["success"]}},
        }

    def withdraw_from_bridge(self, amount, destination):
        assert destination == ACCOUNT and amount == probe.WITHDRAW_AMOUNT_USDC >= 6.0
        return self._refuse("withdraw3")

    def usd_transfer(self, amount, destination):
        assert destination == ACCOUNT
        return self._refuse("usdSend")

    def spot_transfer(self, amount, destination, token):
        assert destination == ACCOUNT and token == "USDC"
        return self._refuse("spotSend")

    def sub_account_transfer(self, sub_account_user, is_deposit, usd):
        return self._refuse("subAccountTransfer")

    def approve_agent(self, name=None):
        self.calls.append("approveAgent")
        return ({"status": "err", "response": "Must be user"}, FAKE_KEY_64)


def _record() -> probe.ProbeRecord:
    return probe.ProbeRecord(
        run_id="dd06-test",
        network="testnet",
        account_address_redacted=probe.redact(ACCOUNT),
        agent_address_redacted=probe.redact(AGENT),
        started_utc="t0",
    )


def test_refuses_mainnet_and_live_ack():
    with pytest.raises(probe.ProbeRefused, match="testnet only"):
        probe.refuse_unless_testnet("mainnet", {})
    with pytest.raises(probe.ProbeRefused, match="HL_LIVE_ACK"):
        probe.refuse_unless_testnet(
            "testnet", {"HL_LIVE_ACK": "I_UNDERSTAND_THIS_IS_REAL_MONEY"}
        )
    probe.refuse_unless_testnet("testnet", {"HL_LIVE_ACK": ""})


def test_refuses_master_key_in_the_agent_slot():
    with pytest.raises(probe.ProbeRefused, match="master key"):
        probe.refuse_master_key(ACCOUNT.upper(), ACCOUNT)
    probe.refuse_master_key(AGENT, ACCOUNT)


def test_control_order_size_clears_minimum_notional_and_cannot_fill():
    limit_px, size = probe.control_order_size(60000.0, 5)
    assert limit_px == 54000.0
    assert size * limit_px >= probe.CONTROL_MIN_NOTIONAL_USD
    assert size == 0.0002


def test_control_price_is_wire_valid_for_a_real_btc_mid():
    """r1 on testnet (2026-09-15 18:33Z): mid 76974.0 -> round(69276.6, 1) = 69276.6 (six significant
    figures) -> venue: `Price must be divisible by tick size`. The price must carry at most 5 significant
    figures and at most 6 - szDecimals decimals, and stay at or below 90 % of mid (cannot fill)."""
    for mid in (76974.0, 69276.6 / 0.9, 123456.7, 99999.9, 10000.1):
        limit_px, size = probe.control_order_size(mid, 5)
        digits = f"{limit_px:.10g}".replace(".", "").strip("0")  # significant figures
        assert len(digits) <= 5, (mid, limit_px)
        assert limit_px <= mid * probe.CONTROL_PRICE_FRACTION
        assert limit_px >= mid * probe.CONTROL_PRICE_FRACTION * 0.999
        assert round(limit_px, 1) == limit_px
        assert size * limit_px >= probe.CONTROL_MIN_NOTIONAL_USD
    assert probe.control_order_size(76974.0, 5)[0] == 69270.0


def test_ok_envelope_with_a_per_status_error_is_a_refusal():
    """The venue answers a rejected order with status ok and a statuses[].error entry (r1 record)."""
    rejected = {
        "status": "ok",
        "response": {
            "type": "order",
            "data": {
                "statuses": [{"error": "Price must be divisible by tick size. asset=3"}]
            },
        },
    }
    assert probe.per_status_errors(rejected) == [
        "Price must be divisible by tick size. asset=3"
    ]
    assert probe.classify_response(rejected) == "REFUSED"
    resting = {
        "status": "ok",
        "response": {"type": "order", "data": {"statuses": [{"resting": {"oid": 7}}]}},
    }
    assert probe.classify_response(resting) == "NOT_REFUSED"
    assert (
        probe.classify_response({"status": "ok", "response": {"type": "default"}})
        == "NOT_REFUSED"
    )


def test_all_arms_refused_gives_refusals_observed_and_redacts_everything(
    tmp_path: Path,
):
    for mode in ("err", "raise"):
        exchange = FakeExchange()
        exchange.refusal = mode
        record = probe.run_probe(
            record=_record(),
            info=FakeInfo(),
            exchange=exchange,
            account_address=ACCOUNT,
            sub_account=None,
        )
        assert record.result == "DD06_REFUSALS_OBSERVED", record.steps
        outcomes = {step["name"]: step["outcome"] for step in record.steps}
        assert outcomes["S1_control_order"] == "NOT_REFUSED"
        assert outcomes["S1_control_cancel"] == "NOT_REFUSED"
        classes = {
            step["name"]: step["data"].get("refusal_class") for step in record.steps
        }
        for arm in ("withdraw3", "usdSend", "spotSend", "approveAgent"):
            assert outcomes[arm] == "REFUSED", arm
            assert classes[arm] == "AUTHORIZATION", arm
        assert outcomes["subAccountTransfer"] == "SKIPPED_NO_SUB_ACCOUNT"
        assert exchange.calls == [
            "order",
            "cancel:60109082440",
            "withdraw3",
            "usdSend",
            "spotSend",
            "approveAgent",
        ]
        path = probe.write_record(tmp_path / mode, record)
        text = path.read_text(encoding="utf-8")
        assert FAKE_KEY_64 not in text and FAKE_KEY_64[2:] not in text
        assert AGENT not in text and ACCOUNT not in text
        assert "[redacted-64hex]" in text and "[redacted-address]" in text
        assert (tmp_path / mode / "DD06_PROBE_RECORD.json.sha256").exists()
        parsed = json.loads(text)
        assert (
            parsed["result"] == "DD06_REFUSALS_OBSERVED" and parsed["finding"] is None
        )


def test_sub_account_arm_runs_only_when_named():
    exchange = FakeExchange()
    record = probe.run_probe(
        record=_record(),
        info=FakeInfo(),
        exchange=exchange,
        account_address=ACCOUNT,
        sub_account="0x" + "d4" * 20,
    )
    assert record.result == "DD06_REFUSALS_OBSERVED"
    assert "subAccountTransfer" in exchange.calls
    assert {s["name"]: s["outcome"] for s in record.steps}[
        "subAccountTransfer"
    ] == "REFUSED"


def test_not_refused_fund_moving_arm_is_a_finding_and_stops_the_sequence():
    class Leaky(FakeExchange):
        def usd_transfer(self, amount, destination):
            self.calls.append("usdSend")
            return {"status": "ok", "response": {"type": "default"}}

    exchange = Leaky()
    record = probe.run_probe(
        record=_record(),
        info=FakeInfo(),
        exchange=exchange,
        account_address=ACCOUNT,
        sub_account=None,
    )
    assert record.result == "DD06_FINDING_NOT_REFUSED"
    assert record.finding.startswith(
        "usdSend was NOT refused; balances unchanged or unreadable"
    )
    # lane-7 review R-4: the record now carries both wallets' balances around the arm
    names = [s["name"] for s in record.steps]
    assert "post_usdSend_account_balances" in names
    assert "S0_agent_balances" in names
    outcomes = {s["name"]: s["outcome"] for s in record.steps}
    assert outcomes["withdraw3"] == "REFUSED" and outcomes["usdSend"] == "NOT_REFUSED"
    assert (
        outcomes["spotSend"] == "SKIPPED_AFTER_FINDING"
        and outcomes["approveAgent"] == "SKIPPED_AFTER_FINDING"
    )
    assert "spotSend" not in exchange.calls and "approveAgent" not in exchange.calls


def test_refusal_text_classes():
    assert probe.classify_refusal_text("Must be user") == "AUTHORIZATION"
    assert (
        probe.classify_refusal_text("User or API Wallet 0xabc does not exist.")
        == "AUTHORIZATION"
    )
    assert (
        probe.classify_refusal_text("Insufficient balance for withdrawal")
        == "VALIDATION"
    )
    assert (
        probe.classify_refusal_text("Withdrawal amount below minimum") == "VALIDATION"
    )
    assert probe.classify_refusal_text("") == "UNCLASSIFIED"
    # lane-7 review R-3: a sub-account or destination that "does not exist" is a VALIDATION refusal,
    # never AUTHORIZATION-class DD-06 evidence; the venue's signer sentence still is
    assert (
        probe.classify_refusal_text("Sub-account 0xabc does not exist") == "VALIDATION"
    )
    assert probe.classify_refusal_text("destination does not exist") == "VALIDATION"
    assert (
        probe.classify_refusal_text("User or API Wallet 0xabc does not exist.")
        == "AUTHORIZATION"
    )
    assert (
        probe.classify_refusal_text("agent may not send this amount") == "AUTHORIZATION"
    )


def test_validation_shaped_refusal_makes_the_run_inconclusive():
    class AmountRefusal(FakeExchange):
        def withdraw_from_bridge(self, amount, destination):
            self.calls.append("withdraw3")
            return {"status": "err", "response": "Withdrawal amount below minimum"}

    record = probe.run_probe(
        record=_record(),
        info=FakeInfo(),
        exchange=AmountRefusal(),
        account_address=ACCOUNT,
        sub_account=None,
    )
    assert record.result == "DD06_INCONCLUSIVE"
    steps = {s["name"]: s for s in record.steps}
    assert steps["withdraw3"]["outcome"] == "REFUSED"
    assert steps["withdraw3"]["data"]["refusal_class"] == "VALIDATION"
    assert steps["usdSend"]["data"]["refusal_class"] == "AUTHORIZATION"
    assert "read the recorded venue texts" in record.finding


def test_transport_error_is_inconclusive_not_a_refusal():
    class Flaky(FakeExchange):
        def withdraw_from_bridge(self, amount, destination):
            self.calls.append("withdraw3")
            raise _ServerError(503, "no capacity")

    record = probe.run_probe(
        record=_record(),
        info=FakeInfo(),
        exchange=Flaky(),
        account_address=ACCOUNT,
        sub_account=None,
    )
    assert record.result == "DD06_INCONCLUSIVE"
    assert {s["name"]: s["outcome"] for s in record.steps}["withdraw3"] == "ERROR"


def test_control_arm_rejection_aborts_before_any_transfer_arm():
    class NoOrders(FakeExchange):
        def order(self, *args, **kwargs):
            self.calls.append("order")
            return {"status": "err", "response": "Insufficient margin"}

    class TickRejected(FakeExchange):
        """The r1 shape: ok envelope, per-order error, no resting oid."""

        def order(self, *args, **kwargs):
            self.calls.append("order")
            return {
                "status": "ok",
                "response": {
                    "type": "order",
                    "data": {
                        "statuses": [
                            {"error": "Price must be divisible by tick size. asset=3"}
                        ]
                    },
                },
            }

    for factory in (NoOrders, TickRejected):
        exchange = factory()
        record = probe.run_probe(
            record=_record(),
            info=FakeInfo(),
            exchange=exchange,
            account_address=ACCOUNT,
            sub_account=None,
        )
        assert record.result == "ABORTED_CONTROL_ARM_NOT_ACCEPTED"
        assert exchange.calls == ["order"]
        outcomes = {s["name"]: s["outcome"] for s in record.steps}
        assert outcomes["S1_control_order"] == "REFUSED"
        assert outcomes["S0_spot_user_state"] == "RECORDED"


def test_uncancelled_control_order_is_reported_loudly():
    class StickyCancel(FakeExchange):
        def cancel(self, name, oid):
            self.calls.append("cancel")
            raise _ClientError(422, None, "cancel refused", {})

    record = probe.run_probe(
        record=_record(),
        info=FakeInfo(),
        exchange=StickyCancel(),
        account_address=ACCOUNT,
        sub_account=None,
    )
    assert record.result == "ABORTED_CONTROL_CANCEL_FAILED"
    assert "cancel it by hand" in record.finding


def test_output_directory_is_write_once(tmp_path: Path):
    record = probe.run_probe(
        record=_record(),
        info=FakeInfo(),
        exchange=FakeExchange(),
        account_address=ACCOUNT,
        sub_account=None,
    )
    probe.write_record(tmp_path / "once", record)
    with pytest.raises(probe.ProbeRefused, match="write-once"):
        probe.write_record(tmp_path / "once", record)


def test_dry_run_needs_no_credentials_and_no_network(capsys, monkeypatch):
    monkeypatch.delenv("HL_API_WALLET_KEY", raising=False)
    monkeypatch.delenv("HL_ACCOUNT_ADDRESS", raising=False)
    assert probe.main(["--run-id", "x", "--out", "unused", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "TESTNET ONLY" in out and "approveAgent" in out and "Stop rule" in out


class _NeverDial:
    """Installed in place of the SDK constructors and the credential resolver for every main() test:
    reaching any of them means the suite would have dialled the venue (lane-7 incident, 2026-09-17)."""

    def __init__(self, what: str) -> None:
        self.what = what

    def __call__(self, *args, **kwargs):
        raise AssertionError(
            f"{self.what} must never be reached from the fixture suite"
        )


@pytest.fixture
def offline(monkeypatch):
    """Every main() test runs under this fixture: the resolver and both SDK constructors are replaced by
    tripwires, the live acknowledgement and the execution token are absent, and no credential is present."""
    import hyperliquid.exchange as hl_exchange
    import hyperliquid.info as hl_info

    from bridge import settings

    tripwire = _NeverDial("resolve_hyperliquid_credentials")
    monkeypatch.setattr(settings, "resolve_hyperliquid_credentials", tripwire)
    monkeypatch.setattr(hl_exchange, "Exchange", _NeverDial("Exchange"))
    monkeypatch.setattr(hl_info, "Info", _NeverDial("Info"))
    for name in (
        "HL_LIVE_ACK",
        probe.RUN_TOKEN_ENV,
        "HL_API_WALLET_KEY",
        "HL_ACCOUNT_ADDRESS",
    ):
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


def test_main_refuses_mainnet_before_reading_any_credential(offline, capsys):
    offline.setenv("HL_LIVE_ACK", "I_UNDERSTAND_THIS_IS_REAL_MONEY")
    assert probe.main(["--run-id", "x", "--out", "unused", "--network", "testnet"]) == 3
    assert "PROBE_REFUSED" in capsys.readouterr().err
    offline.delenv("HL_LIVE_ACK")
    assert probe.main(["--run-id", "x", "--out", "unused", "--network", "mainnet"]) == 3


def test_main_refuses_without_the_execution_token_before_reading_any_credential(
    offline, capsys
):
    # lane-7 review R-2: testnet, no HL_LIVE_ACK - the shape that dialled the venue when one refusal was
    # removed. The second gate refuses before the resolver (a tripwire here) is ever called.
    assert probe.main(["--run-id", "x", "--out", "unused", "--network", "testnet"]) == 3
    err = capsys.readouterr().err
    assert "PROBE_REFUSED" in err and probe.RUN_TOKEN_ENV in err
    offline.setenv(probe.RUN_TOKEN_ENV, "another-run")
    assert probe.main(["--run-id", "x", "--out", "unused", "--network", "testnet"]) == 3
    assert probe.RUN_TOKEN_ENV in capsys.readouterr().err


def test_run_token_gate_is_a_unit_of_its_own():
    probe.refuse_without_run_token("run-7", {probe.RUN_TOKEN_ENV: "run-7"})
    for environ in (
        {},
        {probe.RUN_TOKEN_ENV: ""},
        {probe.RUN_TOKEN_ENV: "run-8"},
        {probe.RUN_TOKEN_ENV: "run-77"},
    ):
        with pytest.raises(probe.ProbeRefused):
            probe.refuse_without_run_token("run-7", environ)


def test_main_refuses_a_master_key_after_the_gates_and_before_any_sdk_object(
    offline, capsys
):
    # lane-7 review R-1 (M3): the refuse_master_key call in main is fenced - a key that derives to the
    # account address exits 3 with the SDK constructors (tripwires) never reached.
    from eth_account import Account

    from bridge import settings

    key = "0x" + "11" * 32
    address = Account.from_key(key).address
    offline.setenv(probe.RUN_TOKEN_ENV, "x")
    offline.setattr(
        settings, "resolve_hyperliquid_credentials", lambda: (address, key, "test")
    )
    assert probe.main(["--run-id", "x", "--out", "unused", "--network", "testnet"]) == 3
    assert "master key" in capsys.readouterr().err


def test_plan_names_the_testnet_host_and_the_gates(capsys):
    # lane-7 review R-1 (M2): the only host the tool can dial is pinned in the plan the owner reads
    text = probe.plan_text(None, False)
    assert "https://api.hyperliquid-testnet.xyz" in text
    assert probe.TESTNET_URL == "https://api.hyperliquid-testnet.xyz"
    assert probe.RUN_TOKEN_ENV in text and "HL_LIVE_ACK" in text


def test_write_record_refuses_surviving_hex(tmp_path: Path):
    # lane-7 review R-1 (M4): the last-resort guard in write_record is fenced
    for poison in ("c3" * 32, "0x" + "d4" * 20):
        record = _record()
        record.steps.append(
            {"name": "poison", "outcome": "RECORDED", "data": {"leak": poison}}
        )
        record.result = "DD06_INCONCLUSIVE"
        out = tmp_path / poison[:6]
        with pytest.raises(probe.ProbeRefused):
            probe.write_record(out, record)
        assert not (out / "DD06_PROBE_RECORD.json").exists()


class _BalancesInfo(FakeInfo):
    """Balances per address that the test can change between the S0 read and the post-arm re-read."""

    def __init__(self) -> None:
        super().__init__()
        self.usdc = {ACCOUNT: "984.987457", AGENT: "13.0"}

    def spot_user_state(self, address: str):
        return {
            "balances": [{"coin": "USDC", "total": self.usdc[address], "hold": "0.0"}]
        }


def _leaky_exchange(info: _BalancesInfo, move: str):
    class Leaky(FakeExchange):
        def spot_transfer(self, amount, destination, token):
            self.calls.append("spotSend")
            if move == "agent":
                info.usdc[AGENT] = "12.0"
            elif move == "master":
                info.usdc[ACCOUNT] = "983.987457"
            return {"status": "ok", "response": {"type": "default"}}

    return Leaky()


@pytest.mark.parametrize(
    ("move", "result", "phrase"),
    [
        ("agent", "DD06_FINDING_OWN_FUNDS_MOVED", "AGENT wallet's own balance changed"),
        ("master", "DD06_FINDING_MASTER_FUNDS_MOVED", "ACCOUNT's balance changed"),
        ("none", "DD06_FINDING_NOT_REFUSED", "balances unchanged or unreadable"),
    ],
)
def test_not_refused_fund_arm_names_whose_funds_moved(move, result, phrase):
    # lane-7 review R-4 (the r3 lesson): the record re-reads BOTH wallets after a NOT_REFUSED fund arm
    # and names whose balance changed instead of asserting a breach it never measured
    info = _BalancesInfo()
    exchange = _leaky_exchange(info, move)
    record = probe.run_probe(
        record=_record(),
        info=info,
        exchange=exchange,
        account_address=ACCOUNT,
        sub_account=None,
        agent_address=AGENT,
    )
    assert record.result == result
    assert phrase in record.finding
    steps = {s["name"]: s for s in record.steps}
    assert steps["S0_agent_balances"]["data"]["usdc_total"] == "13.0"
    assert (
        steps["post_spotSend_account_balances"]["data"]["before"]["usdc_total"]
        == "984.987457"
    )
    assert steps["post_spotSend_agent_balances"]["data"]["after"]["usdc_total"] == (
        "12.0" if move == "agent" else "13.0"
    )
    assert steps["approveAgent"]["outcome"] == "SKIPPED_AFTER_FINDING"


def test_operator_abort_stops_the_sequence():
    # lane-7 review N-2: KeyboardInterrupt inside an arm must not be swallowed as ERROR evidence
    class Aborting(FakeExchange):
        def withdraw_from_bridge(self, amount, destination):
            raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        probe.run_probe(
            record=_record(),
            info=FakeInfo(),
            exchange=Aborting(),
            account_address=ACCOUNT,
            sub_account=None,
        )
