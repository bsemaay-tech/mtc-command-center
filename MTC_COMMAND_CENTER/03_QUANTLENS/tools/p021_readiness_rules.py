"""WP-P0-21 readiness-rule catalogue authorized by owner decision 186.

This bounded first step evaluates no candidate and admits nothing.  The
corrected engine prerequisite remains unmet.  It only exposes the rules and
refuses whenever an authority-owned limit or required rule is still unset.
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
class Rule:
    check_id: str
    question: str
    limits: tuple[tuple[str, Any], ...]
    missing_numbers: tuple[str, ...] = ()
    missing_rules: tuple[str, ...] = ()


OPEN_NUMBERS = (
    MissingNumber("gap_ratio_max", "What is the maximum permitted gap ratio for one series?", "B-02"),
    MissingNumber("swing_trade_count_min", "How many trades are the minimum evidence for a swing strategy?", "B-03"),
    MissingNumber("position_trade_count_min", "How many trades are the minimum evidence for a position strategy?", "B-03"),
    MissingNumber("stop_loss_ceiling", "What is the separate stop-loss ceiling?", "B-04"),
    MissingNumber("divergence_tolerance", "How much backtest-to-forward difference is permitted?", "B-06"),
    MissingNumber("divergence_window_length", "How long is the aligned backtest-to-forward comparison window?", "B-07"),
    MissingNumber("divergence_min_paired_observations", "How many paired observations are required for the difference check?", "B-07"),
    MissingNumber("day_forward_period", "How long must day-strategy forward evidence run?", "B-10"),
    MissingNumber("day_forward_trade_count_min", "How many real forward trades are required for a day strategy?", "B-10"),
    MissingNumber("swing_forward_period", "How long must swing-strategy forward evidence run?", "B-10"),
    MissingNumber("swing_forward_trade_count_min", "How many real forward trades are required for a swing strategy?", "B-10"),
    MissingNumber("position_forward_period", "How long must position-strategy forward evidence run?", "B-10"),
    MissingNumber("position_forward_trade_count_min", "How many real forward trades are required for a position strategy?", "B-10"),
    MissingNumber("normal_market_condition_count_min", "How many normal market conditions must forward evidence cover?", "B-10"),
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
            ("single_trade_loss_risk_unit_multiple_max", 1),
            ("bridge_unexpressible_event_count_max", 0),
            ("liquidation_or_margin_call_event_count_max", 0),
        ),
        missing_numbers=("swing_trade_count_min", "position_trade_count_min", "stop_loss_ceiling"),
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


def validate_catalog(rules: Iterable[Rule], open_numbers: Iterable[MissingNumber]) -> None:
    rules = tuple(rules)
    open_numbers = tuple(open_numbers)
    if len({rule.check_id for rule in rules}) != len(rules):
        raise ValueError("duplicate check id")
    if len(rules) != 7:
        raise ValueError("the designed seven-check catalogue is incomplete")

    declared_names = {number.name for number in open_numbers}
    if declared_names != EXPECTED_OPEN_NUMBER_NAMES:
        missing = sorted(EXPECTED_OPEN_NUMBER_NAMES - declared_names)
        extra = sorted(declared_names - EXPECTED_OPEN_NUMBER_NAMES)
        raise ValueError(f"open-number catalogue changed; missing={missing}; extra={extra}")

    wired_names = {name for rule in rules for name in rule.missing_numbers}
    wired_names.update(FORWARD_EVIDENCE_NUMBER_NAMES)
    if wired_names != EXPECTED_OPEN_NUMBER_NAMES:
        missing = sorted(EXPECTED_OPEN_NUMBER_NAMES - wired_names)
        extra = sorted(wired_names - EXPECTED_OPEN_NUMBER_NAMES)
        raise ValueError(f"open-number refusal wiring changed; missing={missing}; extra={extra}")

    for rule in rules:
        if not rule.missing_numbers and not rule.missing_rules:
            raise ValueError(f"{rule.check_id} could be presented as ready")


def readiness_record() -> dict[str, Any]:
    validate_catalog(RULES, OPEN_NUMBERS)
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
        "check_set_version": 1,
        "check_set_identity": None,
        "checks": checks,
        "open_numbers": [asdict(number) for number in OPEN_NUMBERS],
        "forward_evidence_refusal": {
            "status": "REFUSED",
            "missing_numbers": list(FORWARD_EVIDENCE_NUMBER_NAMES),
            "reason": "no per-type forward-evidence limits set, refusing: "
            + ", ".join(FORWARD_EVIDENCE_NUMBER_NAMES),
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

    changed_rule = replace(RULES[3], missing_numbers=())
    modified_rules = RULES[:3] + (changed_rule,) + RULES[4:]
    try:
        validate_catalog(modified_rules, OPEN_NUMBERS)
    except ValueError as error:
        assert "gap_ratio_max" in str(error)
    else:
        raise AssertionError("modified copy was not detected")

    print(f"SELF-CHECK PASS: {len(RULES)} checks all refuse readiness")
    print(f"OPEN NUMBERS: {len(OPEN_NUMBERS)}")
    print("MODIFIED COPY DETECTED: gap_ratio_max refusal wiring removed")
    print("READY=False")


def _print_owner_view(record: dict[str, Any]) -> None:
    print("WP-P0-21 readiness rules - owner decision 186")
    print("Accepted corrected engine: NOT MET (decision 186 overrides build order only)")
    for check in record["checks"]:
        limits = ", ".join(f"{name}={value}" for name, value in check["limits"].items()) or "none"
        print(f"{check['check_id']}: {check['question']}")
        print(f"  Recorded limits: {limits}")
        print(f"  REFUSED: {check['reason']}")
    print("OPEN NUMBERS WAITING FOR AN ANSWER:")
    for number in record["open_numbers"]:
        print(f"- {number['name']} ({number['blocker']}): {number['question']}")
    print(f"FORWARD EVIDENCE: {record['forward_evidence_refusal']['reason']}")
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
