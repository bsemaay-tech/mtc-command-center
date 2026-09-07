"""Synthetic risk-at-stop seed; quantities are candidates, never execution authority."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import (
    Context, Decimal, DivisionByZero, InvalidOperation, Overflow,
    ROUND_DOWN, Underflow, localcontext,
)
from typing import Sequence

PREC = 28
ROUNDING = ROUND_DOWN
EMAX = 999999
EMIN = -999999


def _context(precision=PREC):
    try:
        return Context(prec=precision, rounding=ROUNDING, Emin=EMIN, Emax=EMAX,
                       capitals=1, clamp=0, flags=[],
                       traps=[InvalidOperation, DivisionByZero, Overflow])
    except ValueError as error:
        raise RiskCalculationRefused("invalid_operation") from error


class RiskCalculationRefused(ValueError):
    """A named refusal, without guessing missing inputs."""


@dataclass(frozen=True)
class RiskRequest:
    """Fraction is a frozen-package request constant; version is bound policy identity.

    Policy caps are not applied by this synthetic seed.
    """
    allocation_policy_version: str
    requested_risk_fraction: Decimal


@dataclass(frozen=True)
class RiskCalculation:
    allocation_policy_version: str
    account_size: Decimal
    requested_risk_fraction: Decimal
    stop_distance: Decimal
    contract_multiplier: Decimal
    position_size: Decimal
    money_at_risk: Decimal


def calculate_position_size(
    *, account_size: Decimal, stop_distance: Decimal,
    contract_multiplier: Decimal, settings: RiskRequest,
) -> RiskCalculation:
    """Compute money risk / (stop distance * contract multiplier), with no I/O.

    Stop distance is a positive price difference in quote units. Multiplier comes
    from frozen instrument metadata, not policy. Products retain all input digits;
    quantity division uses PREC=28, ROUND_DOWN, so rounding cannot exceed the
    requested risk. Exponents and traps are pinned independently of caller context.
    Caps, venue lot/tick quantisation and runtime allocation remain out of scope.
    """
    if not isinstance(settings, RiskRequest):
        raise RiskCalculationRefused("settings")
    try:
        version = settings.allocation_policy_version
        risk_fraction = settings.requested_risk_fraction
    except AttributeError as error:
        raise RiskCalculationRefused("settings") from error
    if not isinstance(version, str) or not version or version != version.strip():
        raise RiskCalculationRefused("allocation_policy_version")
    for name, value in (
        ("account_size", account_size), ("stop_distance", stop_distance),
        ("contract_multiplier", contract_multiplier), ("risk_fraction", risk_fraction),
    ):
        if not isinstance(value, Decimal):
            raise RiskCalculationRefused(name)
        if not value.is_finite() or value <= 0:
            raise RiskCalculationRefused(name)
    # Exact products prevent a rounded-down denominator inflating quantity.
    product_precision = max(
        PREC, len(account_size.as_tuple().digits) + len(risk_fraction.as_tuple().digits),
        len(stop_distance.as_tuple().digits) + len(contract_multiplier.as_tuple().digits),
    )
    try:
        with localcontext(_context(product_precision)) as context:
            money_at_risk = account_size * risk_fraction
            if money_at_risk == 0:
                raise RiskCalculationRefused("position_size_zero")
            per_unit_risk = stop_distance * contract_multiplier
            if context.flags[Underflow]:
                raise RiskCalculationRefused("underflow")
        with localcontext(_context()):
            position_size = money_at_risk / per_unit_risk
    except Overflow as error:
        raise RiskCalculationRefused("overflow") from error
    except DivisionByZero as error:
        raise RiskCalculationRefused("division_by_zero") from error
    except InvalidOperation as error:
        raise RiskCalculationRefused("invalid_operation") from error
    if position_size == 0:
        raise RiskCalculationRefused("position_size_zero")
    return RiskCalculation(
        allocation_policy_version=version, account_size=account_size,
        requested_risk_fraction=risk_fraction, stop_distance=stop_distance,
        contract_multiplier=contract_multiplier, position_size=position_size,
        money_at_risk=money_at_risk,
    )


def _decimal(text):
    try:
        with localcontext(_context()):
            return Decimal(text)
    except InvalidOperation as error:
        raise argparse.ArgumentTypeError(f"not a number: {text}") from error


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Synthetic risk-at-stop candidate calculator.")
    parser.add_argument("--account-size", required=True, type=_decimal)
    parser.add_argument("--entry-price", required=True, type=_decimal)
    parser.add_argument("--stop-price", required=True, type=_decimal)
    parser.add_argument("--contract-multiplier", required=True, type=_decimal,
                        help="Required frozen instrument metadata; no default.")
    parser.add_argument("--requested-risk-fraction", required=True, type=_decimal,
                        help="Request constant from frozen package, not a policy cap.")
    parser.add_argument("--allocation-policy-version", required=True)
    args = parser.parse_args(argv)
    try:
        for name, value in (("entry_price", args.entry_price), ("stop_price", args.stop_price)):
            if not value.is_finite() or value <= 0:
                raise RiskCalculationRefused(name)
        # Exact subtraction avoids ambient rounding before the pure calculator.
        precision = max(PREC, max(args.entry_price.adjusted(), args.stop_price.adjusted())
                        - min(args.entry_price.as_tuple().exponent, args.stop_price.as_tuple().exponent) + 2)
        try:
            with localcontext(_context(precision)) as context:
                stop_distance = (args.entry_price - args.stop_price).copy_abs()
                if context.flags[Underflow]:
                    raise RiskCalculationRefused("underflow")
        except Overflow as error:
            raise RiskCalculationRefused("overflow") from error
        except InvalidOperation as error:
            raise RiskCalculationRefused("invalid_operation") from error
        result = calculate_position_size(
            account_size=args.account_size, stop_distance=stop_distance,
            contract_multiplier=args.contract_multiplier,
            settings=RiskRequest(args.allocation_policy_version, args.requested_risk_fraction),
        )
    except RiskCalculationRefused as error:
        parser.exit(2, f"REFUSED: {error}\n")
    print(f"Money at risk: {result.money_at_risk}")
    print(f"Position size: {result.position_size}")
    print(f"Allocation policy version: {result.allocation_policy_version}")
    print(f"Contract multiplier: {result.contract_multiplier}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
