"""Reviewer probe: a PARTIALLY unreadable wallet is reported as a definite 'did not pay'.

Not part of the candidate. Fake venue objects only; no network, no credential, no SDK object.
Account shape is the one the tool's own comment documents (tools:486-487 and the r1 record):
a unifiedAccount keeps ALL its USDC in the spot balance and its perp accountValue reads 0.0.
"""

from __future__ import annotations

from tools import dd06_agent_withdraw_probe as probe

from test_dd06_agent_withdraw_probe import (  # noqa: E402
    ACCOUNT,
    AGENT,
    _BalancesInfo,
    _leaky_exchange,
    _record,
)


def test_partially_unreadable_master_is_reported_as_did_not_pay(capsys):
    """The master's SPOT read fails after the arm (the only balance that can pay on this account
    shape); its perp value reads 0.0 -> 0.0 as it always does. _paid counts that one decoy key as
    'readable', returns False, and the finding says the account 'did not pay' - no UNREADABLE
    marker anywhere in the sentence, and the exclusion 'not the DD-06 breach' is printed."""

    def effect(info):
        info.usdc[AGENT] = "13.0"  # the agent's own dollar left
        info.usdc[ACCOUNT] = None  # transient 503 on the master's spot read
        # info.account_value[ACCOUNT] stays "0.0" -- readable, and structurally always 0.0

    info = _BalancesInfo()
    record = probe.run_probe(
        record=_record(),
        info=info,
        exchange=_leaky_exchange(info, effect),
        account_address=ACCOUNT,
        sub_account=None,
        agent_address=AGENT,
    )
    steps = {s["name"]: s for s in record.steps}
    print("RESULT :", record.result)
    print("FINDING:", record.finding)
    print("MASTER READINGS:", steps["post_spotSend_account_balances"]["data"])

    assert record.result == "DD06_FINDING_OWN_FUNDS_MOVED"
    assert "account did not pay" in record.finding
    assert "UNREADABLE" not in record.finding
    assert "not the DD-06 breach" in record.finding
    # the balance that carries every dollar on this account was never read after the arm
    assert steps["post_spotSend_account_balances"]["data"]["after"]["usdc_total"] is None


def test_paid_unit_the_decoy_key_alone_produces_a_definite_False():
    """Minimal unit: perp 0.0 -> 0.0 readable, spot unreadable -> False ('did not pay'),
    not None ('UNREADABLE')."""
    before = {"accountValue": "0.0", "usdc_total": "983.987457"}
    after = {"accountValue": "0.0", "usdc_total": None}
    assert probe._paid(before, after, 1.0) is False
    assert probe._paid(before, after, 6.0) is False
    # and with the decoy key gone it correctly reports UNREADABLE
    assert probe._paid({"usdc_total": "983.987457"}, {"usdc_total": None}, 1.0) is None


def test_master_spot_unreadable_and_a_real_master_decrease_is_missed(capsys):
    """The same partial failure on a run where the master really did pay: the decrease is
    invisible, the run is labelled OWN_FUNDS_MOVED and prints 'not the DD-06 breach'."""

    def effect(info):
        info.usdc[AGENT] = "13.0"
        info.usdc[ACCOUNT] = None  # a real 6 USDC decrease would have been here

    info = _BalancesInfo()
    record = probe.run_probe(
        record=_record(),
        info=info,
        exchange=_leaky_exchange(info, effect),
        account_address=ACCOUNT,
        sub_account=None,
        agent_address=AGENT,
    )
    print("RESULT :", record.result)
    print("FINDING:", record.finding)
    assert record.result == "DD06_FINDING_OWN_FUNDS_MOVED"
    assert "not the DD-06 breach" in record.finding
