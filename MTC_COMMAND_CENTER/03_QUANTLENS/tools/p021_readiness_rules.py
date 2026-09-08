"""WP-P0-21 readiness-rule catalogue authorized by owner decision 186.

This bounded first step evaluates no candidate and admits nothing.  The
corrected engine prerequisite remains unmet.  It only exposes the rules and
refuses whenever an authority-owned limit or required rule is still unset.

Owner decisions of 2026-09-07 night close ten of the fourteen open numbers:
`P021_DECISION_1 = A` sets the stop-loss ceiling, and `P021_DECISION_2 =
balanced` selects the evidence-policy profile that carries the two backtest
trade-count floors and all seven forward-evidence numbers.  The four
measure-first numbers - the gap ratio and the three divergence numbers - stay
open, because no measurement has produced a value for them.  Every closed value
is policy v1, provisional and reversible, exactly like `day_trade_count_min =
30`.  Closing numbers does not make anything ready: every check still refuses on
its missing rules.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, replace
from typing import Any, Iterable


@dataclass(frozen=True)
class MissingNumber:
    name: str
    question: str
    blocker: str


@dataclass(frozen=True)
class ClosedNumber:
    name: str
    value: Any
    unit: str
    source: str
    extrapolated: bool = False


@dataclass(frozen=True)
class Rule:
    check_id: str
    question: str
    limits: tuple[tuple[str, Any], ...]
    missing_numbers: tuple[str, ...] = ()
    missing_rules: tuple[str, ...] = ()


POLICY_SET = {
    "policy_version": "v1",
    "status": "PROVISIONAL",
    "profile": "balanced",
    "owner_decisions": {
        "P021_DECISION_1": "A",
        "P021_DECISION_2": "balanced",
    },
    "decided_at": "2026-09-07",
    "source_document": "C:/tmp/OWNER_P021_DECISIONS_20260906_1600.md",
    "derivation_document": (
        "C:/tmp/P021_DESIGN_V21_AUDIT_20260906_1545/EVIDENCE_POLICY_PROFILES.md"
    ),
    "reversible": (
        "A change is a new hashed strategy_type_policy_set version plus fresh "
        "evidence, per decisions 129/130."
    ),
}

# Every value below is read from the balanced column of the design's profile table
# (EVIDENCE_POLICY_PROFILES.md section 3, derived in sections 4.3-4.7).  None of
# them is minted here.
CLOSED_NUMBERS = (
    ClosedNumber(
        "stop_loss_ceiling_equity_fraction",
        0.005,
        "fraction of total account equity at the stop price",
        "P021_DECISION_1 = A (0.50 % of equity per stop-out); equals the already "
        "deployed risk_pct_per_trade = 0.005, so it mints no new number",
    ),
    ClosedNumber(
        "swing_trade_count_min",
        30,
        "closed backtest trades",
        "balanced profile; 75.6 % of the 127 measured swing series clear this floor "
        "over their median 1 974-day span (EVIDENCE_POLICY_PROFILES.md section 4.4)",
    ),
    ClosedNumber(
        "position_trade_count_min",
        12,
        "closed backtest trades",
        "balanced profile; mirrors the swing Rule-2 coverage floor. No position-type "
        "strategy exists in the snapshot, so this is extrapolated, not measured",
        extrapolated=True,
    ),
    ClosedNumber(
        "day_forward_trade_count_min",
        20,
        "closed forward trades",
        "balanced profile, Rule 2 pooled (EVIDENCE_POLICY_PROFILES.md section 4.4)",
    ),
    ClosedNumber(
        "day_forward_period",
        21,
        "days",
        "balanced profile, Rule 3: max(T_count 20.1 d, T_cycle 4 d, T_operational "
        "14 d) rounded up to 3 weeks. NOTE: the owner-facing summary table in the "
        "same documents states a 4-week median wait for the day class; the derived "
        "day_forward_period is 3 weeks. The owner chose the profile, so the derived "
        "value is applied and the discrepancy is recorded for the owner",
    ),
    ClosedNumber(
        "swing_forward_trade_count_min",
        12,
        "closed forward trades",
        "balanced profile, Rule 2 pooled (EVIDENCE_POLICY_PROFILES.md section 4.5)",
    ),
    ClosedNumber(
        "swing_forward_period",
        119,
        "days",
        "balanced profile, Rule 3: T_cycle binds at 4 x 29.0 d median inter-entry, "
        "rounded up to 17 weeks (EVIDENCE_POLICY_PROFILES.md section 4.5)",
    ),
    ClosedNumber(
        "position_forward_trade_count_min",
        12,
        "closed forward trades",
        "balanced profile; mirrors swing for the same Rule-2 reason. Extrapolated",
        extrapolated=True,
    ),
    ClosedNumber(
        "position_forward_period",
        364,
        "days",
        "balanced profile, Rule 3 on the extrapolated 90-day inter-entry interval, "
        "rounded up to 52 weeks. Extrapolated, not measured",
        extrapolated=True,
    ),
    ClosedNumber(
        "normal_market_condition_count_min",
        2,
        "distinct market conditions",
        "balanced profile, with occupancy_min = 0.10 and trades_per_condition_min = 3 "
        "(EVIDENCE_POLICY_PROFILES.md section 3)",
    ),
    ClosedNumber(
        "normal_market_condition_occupancy_min",
        0.10,
        "fraction of the forward window spent in the condition",
        "balanced profile (EVIDENCE_POLICY_PROFILES.md section 3)",
    ),
    ClosedNumber(
        "normal_market_condition_trades_per_condition_min",
        3,
        "closed forward trades inside one condition",
        "balanced profile (EVIDENCE_POLICY_PROFILES.md section 3)",
    ),
)

CLOSED_NUMBER_VALUES = {number.name: number.value for number in CLOSED_NUMBERS}

EXPECTED_CLOSED_NUMBER_NAMES = frozenset(number.name for number in CLOSED_NUMBERS)

OPEN_NUMBERS = (
    MissingNumber("gap_ratio_max", "What is the maximum permitted gap ratio for one series?", "B-02"),
    MissingNumber("divergence_tolerance", "How much backtest-to-forward difference is permitted?", "B-06"),
    MissingNumber("divergence_window_length", "How long is the aligned backtest-to-forward comparison window?", "B-07"),
    MissingNumber("divergence_min_paired_observations", "How many paired observations are required for the difference check?", "B-07"),
)

EXPECTED_OPEN_NUMBER_NAMES = frozenset(number.name for number in OPEN_NUMBERS)

RULES = (
    Rule(
        "P021.DETERMINISTIC_REPLAY",
        "Do two clean runs over identical frozen inputs produce the same complete intent stream?",
        (("run_count", 2), ("intent_stream_hashes_must_equal", True)),
        missing_rules=("accepted_corrected_engine.B01", "intent_stream_serialization.P012"),
    ),
    Rule(
        "P021.LOOKAHEAD_PREFIX",
        "Does every tested decision stay identical when all later bars are physically removed?",
        (("intent_mismatch_count_max", 0), ("tolerance", 0)),
        missing_rules=("accepted_corrected_engine.B01", "decision_domain.B12", "intent_hash_contract.B21"),
    ),
    Rule(
        "P021.REPAINT_CLOSED_BAR",
        "Does any signal change after its bar has closed?",
        (("closed_bar_flip_count_max", 0),),
        missing_rules=("accepted_corrected_engine.B01", "forming_bar_runtime_proof.B16"),
    ),
    Rule(
        "P021.DATA_QUALITY",
        "Are timestamps ordered and unique, OHLCV values valid, gaps within a stated limit, and dataset identity present?",
        (
            ("duplicate_timestamp_count_max", 0),
            ("out_of_order_timestamp_count_max", 0),
            ("invalid_ohlcv_count_max", 0),
            ("dataset_hash_required", True),
        ),
        missing_numbers=("gap_ratio_max",),
        missing_rules=("accepted_corrected_engine.B01", "gap_ratio_formula.B17", "dataset_hash_contract.B13"),
    ),
    Rule(
        "P021.BASIC_FAILURE_FLOOR",
        "Does the strategy have enough evidence and avoid excessive loss, unexpressible orders, liquidation, and margin calls?",
        (
            ("day_trade_count_starting_rule", 30),
            ("swing_trade_count_min", CLOSED_NUMBER_VALUES["swing_trade_count_min"]),
            ("position_trade_count_min", CLOSED_NUMBER_VALUES["position_trade_count_min"]),
            (
                "stop_loss_ceiling_equity_fraction",
                CLOSED_NUMBER_VALUES["stop_loss_ceiling_equity_fraction"],
            ),
            ("single_trade_loss_risk_unit_multiple_max", 1),
            ("bridge_unexpressible_event_count_max", 0),
            ("liquidation_or_margin_call_event_count_max", 0),
        ),
        missing_rules=("accepted_corrected_engine.B01", "risk_unit_source.B04", "strategy_type_policy_set.B22"),
    ),
    Rule(
        "P021.UNSIMULATED_CONTROLS",
        "Is every enabled control either executed or openly recorded under the rule for the target state?",
        (("enabled_control_missing_from_trace_and_manifest_count_max", 0),),
        missing_rules=("accepted_corrected_engine.B01", "state_allowance_matrix.B08", "control_hash_contract.B19"),
    ),
    Rule(
        "P021.BACKTEST_FORWARD_DIVERGENCE",
        "Is the measured difference between backtest expectation and forward evidence within a stated limit?",
        (),
        missing_numbers=("divergence_tolerance", "divergence_window_length", "divergence_min_paired_observations"),
        missing_rules=("accepted_corrected_engine.B01", "divergence_metric.B05", "divergence_alignment.B07", "divergence_provenance.B20"),
    ),
)

FORWARD_EVIDENCE_NUMBER_NAMES = (
    "day_forward_period",
    "day_forward_trade_count_min",
    "swing_forward_period",
    "swing_forward_trade_count_min",
    "position_forward_period",
    "position_forward_trade_count_min",
    "normal_market_condition_count_min",
)


def _refusal(rule: Rule) -> str:
    missing = tuple(rule.missing_numbers) + tuple(rule.missing_rules)
    return "no limit or required rule set, refusing: " + ", ".join(missing)


def validate_catalog(
    rules: Iterable[Rule],
    open_numbers: Iterable[MissingNumber],
    closed_numbers: Iterable[ClosedNumber] = CLOSED_NUMBERS,
) -> None:
    rules = tuple(rules)
    open_numbers = tuple(open_numbers)
    closed_numbers = tuple(closed_numbers)
    if len({rule.check_id for rule in rules}) != len(rules):
        raise ValueError("duplicate check id")
    if len(rules) != 7:
        raise ValueError("the designed seven-check catalogue is incomplete")

    declared_names = {number.name for number in open_numbers}
    if declared_names != EXPECTED_OPEN_NUMBER_NAMES:
        missing = sorted(EXPECTED_OPEN_NUMBER_NAMES - declared_names)
        extra = sorted(declared_names - EXPECTED_OPEN_NUMBER_NAMES)
        raise ValueError(f"open-number catalogue changed; missing={missing}; extra={extra}")

    closed_declared = {number.name for number in closed_numbers}
    if closed_declared != EXPECTED_CLOSED_NUMBER_NAMES:
        missing = sorted(EXPECTED_CLOSED_NUMBER_NAMES - closed_declared)
        extra = sorted(closed_declared - EXPECTED_CLOSED_NUMBER_NAMES)
        raise ValueError(f"closed-number catalogue changed; missing={missing}; extra={extra}")

    if closed_declared & EXPECTED_OPEN_NUMBER_NAMES:
        overlap = sorted(closed_declared & EXPECTED_OPEN_NUMBER_NAMES)
        raise ValueError(f"a number is both closed and open: {overlap}")

    wired_names = {name for rule in rules for name in rule.missing_numbers}
    if wired_names != EXPECTED_OPEN_NUMBER_NAMES:
        missing = sorted(EXPECTED_OPEN_NUMBER_NAMES - wired_names)
        extra = sorted(wired_names - EXPECTED_OPEN_NUMBER_NAMES)
        raise ValueError(f"open-number refusal wiring changed; missing={missing}; extra={extra}")

    forward_declared = set(FORWARD_EVIDENCE_NUMBER_NAMES)
    if not forward_declared <= closed_declared:
        missing = sorted(forward_declared - closed_declared)
        raise ValueError(f"forward-evidence numbers are not all closed; missing={missing}")

    for rule in rules:
        if not rule.missing_numbers and not rule.missing_rules:
            raise ValueError(f"{rule.check_id} could be presented as ready")


def readiness_record() -> dict[str, Any]:
    validate_catalog(RULES, OPEN_NUMBERS, CLOSED_NUMBERS)
    checks = []
    for rule in RULES:
        checks.append(
            {
                "check_id": rule.check_id,
                "question": rule.question,
                "limits": dict(rule.limits),
                "status": "REFUSED",
                "missing_numbers": list(rule.missing_numbers),
                "missing_rules": list(rule.missing_rules),
                "reason": _refusal(rule),
            }
        )
    return {
        "package": "WP-P0-21",
        "owner_decision": 186,
        "implementation_authorized": False,
        "accepted_engine_precondition": "NOT_MET_OVERRIDDEN_FOR_THIS_BOUNDED_BUILD",
        "ready": False,
        "status": "REFUSED",
        "check_set_version": 2,
        "check_set_identity": None,
        "checks": checks,
        "policy_set": POLICY_SET,
        "closed_numbers": [asdict(number) for number in CLOSED_NUMBERS],
        "open_numbers": [asdict(number) for number in OPEN_NUMBERS],
        "forward_evidence_policy": {
            "status": "SET",
            "profile": POLICY_SET["profile"],
            "policy_version": POLICY_SET["policy_version"],
            "numbers": {
                name: CLOSED_NUMBER_VALUES[name] for name in FORWARD_EVIDENCE_NUMBER_NAMES
            },
            "note": "Set by P021_DECISION_2 = balanced; provisional v1 and reversible. "
            "The position-class numbers are extrapolated: no position-type strategy "
            "exists in the measured snapshot.",
        },
    }


def self_check() -> None:
    record = readiness_record()
    assert record["ready"] is False
    assert record["status"] == "REFUSED"
    assert record["implementation_authorized"] is False
    assert record["accepted_engine_precondition"].startswith("NOT_MET")
    assert all(check["status"] == "REFUSED" for check in record["checks"])
    assert all("refusing:" in check["reason"] for check in record["checks"])
    assert {item["name"] for item in record["open_numbers"]} == EXPECTED_OPEN_NUMBER_NAMES
    assert {item["name"] for item in record["closed_numbers"]} == EXPECTED_CLOSED_NUMBER_NAMES
    assert record["policy_set"]["status"] == "PROVISIONAL"

    changed_rule = replace(RULES[3], missing_numbers=())
    modified_rules = RULES[:3] + (changed_rule,) + RULES[4:]
    try:
        validate_catalog(modified_rules, OPEN_NUMBERS, CLOSED_NUMBERS)
    except ValueError as error:
        assert "gap_ratio_max" in str(error)
    else:
        raise AssertionError("modified copy was not detected")

    dropped = tuple(
        number for number in CLOSED_NUMBERS if number.name != "swing_forward_period"
    )
    try:
        validate_catalog(RULES, OPEN_NUMBERS, dropped)
    except ValueError as error:
        assert "swing_forward_period" in str(error)
    else:
        raise AssertionError("dropped closed number was not detected")

    print(f"SELF-CHECK PASS: {len(RULES)} checks all refuse readiness")
    print(f"CLOSED NUMBERS: {len(CLOSED_NUMBERS)} (profile {POLICY_SET['profile']}, {POLICY_SET['status'].lower()})")
    print(f"OPEN NUMBERS: {len(OPEN_NUMBERS)}")
    print("MODIFIED COPY DETECTED: gap_ratio_max refusal wiring removed")
    print("MODIFIED COPY DETECTED: swing_forward_period closure removed")
    print("READY=False")


def _print_owner_view(record: dict[str, Any]) -> None:
    print("WP-P0-21 readiness rules - owner decision 186")
    print("Accepted corrected engine: NOT MET (decision 186 overrides build order only)")
    policy = record["policy_set"]
    print(
        f"Policy set: profile {policy['profile']}, {policy['policy_version']} "
        f"{policy['status'].lower()} "
        f"(P021_DECISION_1 = {policy['owner_decisions']['P021_DECISION_1']}, "
        f"P021_DECISION_2 = {policy['owner_decisions']['P021_DECISION_2']})"
    )
    for check in record["checks"]:
        limits = ", ".join(f"{name}={value}" for name, value in check["limits"].items()) or "none"
        print(f"{check['check_id']}: {check['question']}")
        print(f"  Recorded limits: {limits}")
        print(f"  REFUSED: {check['reason']}")
    print("NUMBERS THE OWNER DECISIONS CLOSED:")
    for number in record["closed_numbers"]:
        mark = " (extrapolated)" if number["extrapolated"] else ""
        print(f"- {number['name']} = {number['value']} {number['unit']}{mark}")
    print("OPEN NUMBERS WAITING FOR A MEASUREMENT:")
    for number in record["open_numbers"]:
        print(f"- {number['name']} ({number['blocker']}): {number['question']}")
    print(f"FORWARD EVIDENCE: {record['forward_evidence_policy']['note']}")
    print("FINAL: REFUSED - nothing is declared ready")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print the refusal record as JSON")
    parser.add_argument("--self-check", action="store_true", help="run the fail-closed modified-copy check")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return 0
    record = readiness_record()
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    else:
        _print_owner_view(record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
