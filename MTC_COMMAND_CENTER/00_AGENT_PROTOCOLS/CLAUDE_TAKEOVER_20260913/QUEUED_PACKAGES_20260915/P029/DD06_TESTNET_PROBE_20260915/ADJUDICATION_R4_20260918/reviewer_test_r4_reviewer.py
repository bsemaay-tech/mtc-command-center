"""Attempt-5 reviewer probes. Fixture objects only: no network, no credential, no main(), no SDK object.

Every probe here runs against the UNMODIFIED candidate acd79b52 unless a mutant file says otherwise.
"""

from __future__ import annotations

import pytest
from test_dd06_agent_withdraw_probe import (
    ACCOUNT,
    AGENT,
    FakeExchange,
    _BalancesInfo,
    _record,
)

from tools import dd06_agent_withdraw_probe as probe

# The literal value the installed hyperliquid SDK (0.24.0) returns from API.post for a 2xx whose body
# is not JSON -- api.py:25-28 `except ValueError: return {"error": f"Could not parse JSON: {text}"}`.
SDK_UNPARSEABLE_200 = {"error": "Could not parse JSON: <html>502 Bad Gateway</html>"}


def test_R1_module_under_test_is_the_scratch_copy():
    assert "mutroot4" in probe.__file__.replace("\\", "/"), probe.__file__


# ---------------------------------------------------------------- R-1: the unhandled third outcome


def test_R1_inconclusive_fund_arm_neither_stops_nor_measures(capsys):
    """A fund-moving arm whose outcome the tool could NOT determine is not stopped on and not measured;
    two further signed fund-moving requests are sent afterwards."""

    class Unparseable(FakeExchange):
        def withdraw_from_bridge(self, amount, destination):
            self.calls.append("withdraw3")
            return SDK_UNPARSEABLE_200

    info = _BalancesInfo()
    exchange = Unparseable()
    record = probe.run_probe(
        record=_record(),
        info=info,
        exchange=exchange,
        account_address=ACCOUNT,
        sub_account=None,
        agent_address=AGENT,
    )
    outcomes = {s["name"]: s["outcome"] for s in record.steps}
    names = [s["name"] for s in record.steps]

    print("OUTCOME(withdraw3) :", outcomes["withdraw3"])
    print("RESULT             :", record.result)
    print("FINDING            :", record.finding)
    print("EXCHANGE CALLS     :", exchange.calls)
    print("POST-ARM RE-READS  :", [n for n in names if n.startswith("post_")])

    # the venue was asked to move 6 USDC and the tool does not know what happened
    assert outcomes["withdraw3"] == "INCONCLUSIVE"
    assert "withdraw3" in probe.FUND_MOVING_ARMS
    # ... yet: no balance re-read of either wallet
    assert [n for n in names if n.startswith("post_")] == []
    # ... no stop: two MORE signed fund-moving requests follow an unknown outcome
    assert exchange.calls == [
        "order",
        "cancel:60109082440",
        "withdraw3",
        "usdSend",
        "spotSend",
        "approveAgent",
    ]
    # ... and the record ends with the benign label and NO finding text at all
    assert record.result == "DD06_INCONCLUSIVE"
    assert record.finding is None


def test_R1_same_label_as_a_benign_run():
    """The label a reader sees is identical to the ordinary 'a refusal was not authorization-shaped' run."""

    class ValidationRefusal(FakeExchange):
        def withdraw_from_bridge(self, amount, destination):
            self.calls.append("withdraw3")
            return {"status": "err", "response": "Withdrawal amount below minimum"}

    benign = probe.run_probe(
        record=_record(),
        info=_BalancesInfo(),
        exchange=ValidationRefusal(),
        account_address=ACCOUNT,
        sub_account=None,
        agent_address=AGENT,
    )
    assert benign.result == "DD06_INCONCLUSIVE"
    assert benign.finding is not None  # the benign run at least explains itself


def test_R1_the_error_branch_that_does_stop_is_one_line_away():
    """Same arm, same uncertainty, reached through the exception channel instead: measured and stopped."""

    class ServerError(Exception):
        pass

    ServerError.__name__ = "ServerError"

    class Flaky(FakeExchange):
        def withdraw_from_bridge(self, amount, destination):
            self.calls.append("withdraw3")
            raise ServerError(503, "no capacity")

    record = probe.run_probe(
        record=_record(),
        info=_BalancesInfo(),
        exchange=Flaky(),
        account_address=ACCOUNT,
        sub_account=None,
        agent_address=AGENT,
    )
    assert record.result == "DD06_INCONCLUSIVE_FUND_ARM_ERROR"
    assert "post_withdraw3_account_balances" in {s["name"] for s in record.steps}
    assert "usdSend" not in Flaky.__mro__[0].__dict__  # sanity: usdSend not overridden
    outcomes = {s["name"]: s["outcome"] for s in record.steps}
    assert outcomes["usdSend"] == "SKIPPED_AFTER_ERROR"


# ---------------------------------------------------------------- round-3 addendum checks (c) and (d)


@pytest.mark.parametrize("amount", [6.0, 1.0, 0.5, 0.01, 1_000_000.0])
def test_round3_c_decoy_shape_is_none_for_any_amount(amount):
    before = {"accountValue": "0.0", "usdc_total": "983.987457"}
    after = {"accountValue": "0.0", "usdc_total": None}
    assert probe._paid(before, after, amount) is None


def test_NIT_zero_amount_makes_an_unchanged_wallet_pay():
    """`delta <= -threshold` with threshold 0 accepts delta == 0: an UNCHANGED, fully readable wallet
    is reported as having paid, and the account branch prints the breach sentence. Latent only -- every
    ARM_AMOUNT_USDC entry is >= 1.0 today and the lookup default is TRANSFER_AMOUNT_USDC."""
    same = {"accountValue": "0.0", "usdc_total": "983.987457"}
    assert probe._paid(same, same, 1.0) is False
    assert probe._paid(same, same, 0.0) is True  # <- an unchanged wallet "paid"
    label, text = probe._attribute("withdraw3", True, False, True)
    assert label == "DD06_FINDING_MASTER_FUNDS_MOVED"
    assert "DD-06 falsified on testnet" in text
    assert min(probe.ARM_AMOUNT_USDC.values()) >= 1.0  # not reachable via the shipped table


def test_round3_d_threshold_arithmetic_is_half_the_arm_amount():
    assert probe.ARM_AMOUNT_USDC["withdraw3"] == 6.0
    assert probe.ARM_AMOUNT_USDC["usdSend"] == 1.0
    assert probe.ARM_AMOUNT_USDC["spotSend"] == 1.0
    assert probe.ARM_AMOUNT_USDC["subAccountTransfer"] == 1.0
    assert probe.ARM_AMOUNT_USDC["usdClassTransfer"] == 1.0
    assert set(probe.ARM_AMOUNT_USDC) == set(probe.FUND_MOVING_ARMS)
    both = {"accountValue": "0.0", "usdc_total": "100.0"}
    # withdraw3 -> threshold 3.0
    assert probe._paid(both, {"accountValue": "0.0", "usdc_total": "97.01"}, 6.0) is False
    assert probe._paid(both, {"accountValue": "0.0", "usdc_total": "97.0"}, 6.0) is True
    # usdSend/spotSend -> threshold 0.5
    assert probe._paid(both, {"accountValue": "0.0", "usdc_total": "99.51"}, 1.0) is False
    assert probe._paid(both, {"accountValue": "0.0", "usdc_total": "99.5"}, 1.0) is True


def test_round3_d_a_master_increase_can_never_be_the_breach():
    for delta in ("984.987457", "1000.0", "983.987458", "983.987457"):
        assert (
            probe._paid(
                {"accountValue": "0.0", "usdc_total": "983.987457"},
                {"accountValue": "0.0", "usdc_total": delta},
                6.0,
            )
            is False
        )
    label, text = probe._attribute("withdraw3", False, True, True)
    assert label == "DD06_FINDING_OWN_FUNDS_MOVED"
    assert "falsified" not in text


def test_round3_d_complete_reading_semantics_unchanged():
    """r3 replay -> OWN; a measured master decrease -> MASTER; a tick -> NOT_REFUSED."""
    assert probe._attribute("spotSend", False, True, True)[0] == "DD06_FINDING_OWN_FUNDS_MOVED"
    assert probe._attribute("spotSend", True, False, True)[0] == "DD06_FINDING_MASTER_FUNDS_MOVED"
    assert probe._attribute("spotSend", False, False, True)[0] == "DD06_FINDING_NOT_REFUSED"
    assert (
        probe._attribute("spotSend", None, True, True)[0]
        == "DD06_FINDING_OWN_FUNDS_MOVED_MASTER_UNREADABLE"
    )


# ---------------------------------------------------------------- robustness probes (NIT candidates)


def test_NIT_paid_crashes_on_a_nan_reading():
    """`delta <= -threshold` sits OUTSIDE the try; a Decimal NaN raises there and kills the run before
    write_record, losing the whole record."""
    from decimal import InvalidOperation

    with pytest.raises(InvalidOperation):
        probe._paid(
            {"accountValue": "0.0", "usdc_total": "100.0"},
            {"accountValue": "0.0", "usdc_total": "NaN"},
            6.0,
        )


def test_NIT_balances_crashes_on_a_json_null_field():
    class NullFields:
        def user_state(self, address):
            return {"marginSummary": None}

        def spot_user_state(self, address):
            return {"balances": []}

    with pytest.raises(AttributeError):
        probe._balances(NullFields(), ACCOUNT)

    class NullBalances:
        def user_state(self, address):
            return {"marginSummary": {"accountValue": "0.0"}}

        def spot_user_state(self, address):
            return {"balances": None}

    with pytest.raises(TypeError):
        probe._balances(NullBalances(), ACCOUNT)


def test_NIT_a_wallet_with_no_usdc_row_is_reported_unreadable(capsys):
    """An agent wallet that simply holds no USDC (the ordinary case) reads usdc_total=None, so it can
    never be measured as 'did not pay' -- it is always named UNREADABLE. Safe direction, but noisy."""

    class NoUsdcRow:
        def user_state(self, address):
            return {"marginSummary": {"accountValue": "0.0"}}

        def spot_user_state(self, address):
            return {"balances": []}

    reading = probe._balances(NoUsdcRow(), AGENT)
    print("AGENT READING:", reading)
    assert reading == {"accountValue": "0.0", "usdc_total": None}
    assert probe._paid(reading, reading, 1.0) is None
    label, text = probe._attribute("spotSend", False, None, True)
    print("LABEL:", label)
    print("TEXT :", text)
    assert label == "DD06_FINDING_NOT_REFUSED"
    assert "NOT measured (UNREADABLE)" in text


def test_NIT_accepted_control_order_with_an_unparseable_oid_is_called_not_accepted():
    """An order the venue ACCEPTED but whose oid the probe cannot parse is recorded as
    'ABORTED_CONTROL_ARM_NOT_ACCEPTED' and left resting -- no 'cancel it by hand' sentence."""

    class NoOid(FakeExchange):
        def order(self, *args, **kwargs):
            self.calls.append("order")
            return {"status": "ok", "response": {"type": "order", "data": {"statuses": [{"resting": {}}]}}}

    exchange = NoOid()
    record = probe.run_probe(
        record=_record(),
        info=_BalancesInfo(),
        exchange=exchange,
        account_address=ACCOUNT,
        sub_account=None,
    )
    outcomes = {s["name"]: s["outcome"] for s in record.steps}
    assert outcomes["S1_control_order"] == "NOT_REFUSED"  # the venue accepted it
    assert record.result == "ABORTED_CONTROL_ARM_NOT_ACCEPTED"  # the record says otherwise
    assert record.finding is None
    assert exchange.calls == ["order"]  # never cancelled
