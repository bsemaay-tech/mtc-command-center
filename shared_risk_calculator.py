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

    Policy caps are not applied at this stage; ``AllocationPolicyCaps`` carries them.
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
    Caps and venue lot/tick quantisation are applied by the later stages in this
    module -- ``quantise_position_size`` and ``apply_allocation_policy_caps`` --
    never here. Runtime allocation remains out of scope.
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


# --- Stage 3 continued: quantisation, then the bound allocation-policy caps -------------
# Brief 5.5 orders the Risk Allocator's work exactly: resolve the request, then apply
# "precision, min_qty and min_notional from the frozen package metadata", then apply the
# "bound allocation-policy caps ... either proposes the requested economic result in full
# or rejects -- a cap breach is REJECTED, never a quietly smaller order".
#
# Quantisation and capping are therefore different acts and are kept apart. Rounding down
# to a venue step expresses a quantity in a form the venue accepts; it is part of
# resolution. Lowering a quantity so that a cap stops binding is a discretionary trim, and
# no function here may perform one. Every bound and every minimum arrives as an argument
# from frozen metadata or bound policy: this module holds no venue rule and no cap value.


@dataclass(frozen=True)
class PackageMetadata:
    """Venue precision and minimums, taken from frozen package metadata, never policy.

    Every field is required. The seed refuses rather than guess a venue rule.
    """
    qty_step: Decimal
    min_qty: Decimal
    min_notional: Decimal


@dataclass(frozen=True)
class AllocationPolicyCaps:
    """Bound allocation-policy caps, applied as propose-in-full-or-reject.

    ``allocation_policy_version`` is the bound policy identity and must equal the
    request's, so a quantity can never be capped under a policy it was not bound to.
    """
    allocation_policy_version: str
    max_risk_at_stop_fraction: Decimal
    max_leverage: Decimal
    max_exposure_fraction: Decimal


@dataclass(frozen=True)
class ProposedQuantity:
    """The Risk Allocator's output: a proposal, never an authorized or executable size."""
    allocation_policy_version: str
    calculation: RiskCalculation
    proposed_qty: Decimal
    notional: Decimal
    realised_money_at_risk: Decimal


def _require_positive_decimals(pairs):
    for name, value in pairs:
        if not isinstance(value, Decimal):
            raise RiskCalculationRefused(name)
        if not value.is_finite() or value <= 0:
            raise RiskCalculationRefused(name)


def quantise_position_size(*, position_size: Decimal, metadata: PackageMetadata) -> Decimal:
    """Round the resolved quantity DOWN to ``qty_step``; refuse below ``min_qty``.

    ROUND_DOWN only. Rounding up would propose more risk than the frozen package
    requested. ``min_notional`` is not checked here because notional needs a price this
    stage is not given; ``resolve_proposed_qty`` checks it once the notional exists.
    """
    if not isinstance(metadata, PackageMetadata):
        raise RiskCalculationRefused("metadata")
    _require_positive_decimals((
        ("position_size", position_size),
        ("qty_step", metadata.qty_step),
        ("min_qty", metadata.min_qty),
        ("min_notional", metadata.min_notional),
    ))
    try:
        with localcontext(_context()):
            steps = (position_size / metadata.qty_step).to_integral_value(rounding=ROUND_DOWN)
            quantised = steps * metadata.qty_step
    except Overflow as error:
        raise RiskCalculationRefused("overflow") from error
    except DivisionByZero as error:
        raise RiskCalculationRefused("division_by_zero") from error
    except InvalidOperation as error:
        raise RiskCalculationRefused("invalid_operation") from error
    if quantised <= 0:
        raise RiskCalculationRefused("quantised_position_size_zero")
    if quantised < metadata.min_qty:
        raise RiskCalculationRefused("min_qty")
    return quantised


def apply_allocation_policy_caps(
    *, proposed_qty: Decimal, account_size: Decimal, notional: Decimal,
    realised_money_at_risk: Decimal, existing_gross_notional: Decimal,
    caps: AllocationPolicyCaps, settings: RiskRequest,
) -> None:
    """Reject on a binding cap. Returns ``None`` and never returns a smaller quantity.

    This signature is the invariant: there is no return value a caller could mistake for
    a trimmed proposal. A breach of the risk-at-stop ceiling, the leverage cap or the
    exposure cap raises, exactly as brief 5.5 requires.

    Leverage and exposure are deliberately different quantities. Leverage is *this
    proposal's* notional against the account; exposure is the account's **gross** notional
    once this proposal is added. For a single flat account they coincide, and computing
    both from the proposal alone would look correct forever while silently under-reporting
    exposure the moment a second position exists. ``existing_gross_notional`` is therefore
    required with no default -- a caller with nothing open passes zero and says so, rather
    than the module assuming an empty book.
    """
    if not isinstance(caps, AllocationPolicyCaps):
        raise RiskCalculationRefused("caps")
    if not isinstance(settings, RiskRequest):
        raise RiskCalculationRefused("settings")
    version = caps.allocation_policy_version
    if not isinstance(version, str) or not version or version != version.strip():
        raise RiskCalculationRefused("caps_allocation_policy_version")
    if version != settings.allocation_policy_version:
        raise RiskCalculationRefused("allocation_policy_version_mismatch")
    _require_positive_decimals((
        ("proposed_qty", proposed_qty),
        ("account_size", account_size),
        ("notional", notional),
        ("realised_money_at_risk", realised_money_at_risk),
        ("max_risk_at_stop_fraction", caps.max_risk_at_stop_fraction),
        ("max_leverage", caps.max_leverage),
        ("max_exposure_fraction", caps.max_exposure_fraction),
    ))
    # Zero is a legitimate open book, so this one is non-negative rather than positive.
    if not isinstance(existing_gross_notional, Decimal):
        raise RiskCalculationRefused("existing_gross_notional")
    if not existing_gross_notional.is_finite() or existing_gross_notional < 0:
        raise RiskCalculationRefused("existing_gross_notional")
    try:
        with localcontext(_context()):
            risk_fraction = realised_money_at_risk / account_size
            leverage = notional / account_size
            exposure = (existing_gross_notional + notional) / account_size
    except Overflow as error:
        raise RiskCalculationRefused("overflow") from error
    except DivisionByZero as error:
        raise RiskCalculationRefused("division_by_zero") from error
    except InvalidOperation as error:
        raise RiskCalculationRefused("invalid_operation") from error
    if risk_fraction > caps.max_risk_at_stop_fraction:
        raise RiskCalculationRefused("cap_risk_at_stop")
    if leverage > caps.max_leverage:
        raise RiskCalculationRefused("cap_leverage")
    if exposure > caps.max_exposure_fraction:
        raise RiskCalculationRefused("cap_exposure")


def resolve_proposed_qty(
    *, account_size: Decimal, entry_reference_price: Decimal, stop_distance: Decimal,
    contract_multiplier: Decimal, settings: RiskRequest, metadata: PackageMetadata,
    caps: AllocationPolicyCaps, existing_gross_notional: Decimal,
) -> ProposedQuantity:
    """The whole Risk Allocator stage: resolve, quantise, then cap or reject.

    The order is the contract's, not a convenience: quantisation happens against frozen
    package metadata before any cap is read, so a cap is always judged against the
    quantity the venue would actually accept.
    """
    _require_positive_decimals((("entry_reference_price", entry_reference_price),))
    calculation = calculate_position_size(
        account_size=account_size, stop_distance=stop_distance,
        contract_multiplier=contract_multiplier, settings=settings,
    )
    proposed_qty = quantise_position_size(
        position_size=calculation.position_size, metadata=metadata,
    )
    try:
        with localcontext(_context()):
            notional = proposed_qty * entry_reference_price * contract_multiplier
            realised_money_at_risk = proposed_qty * stop_distance * contract_multiplier
    except Overflow as error:
        raise RiskCalculationRefused("overflow") from error
    except InvalidOperation as error:
        raise RiskCalculationRefused("invalid_operation") from error
    if notional < metadata.min_notional:
        raise RiskCalculationRefused("min_notional")
    apply_allocation_policy_caps(
        proposed_qty=proposed_qty, account_size=account_size, notional=notional,
        realised_money_at_risk=realised_money_at_risk,
        existing_gross_notional=existing_gross_notional, caps=caps, settings=settings,
    )
    return ProposedQuantity(
        allocation_policy_version=caps.allocation_policy_version,
        calculation=calculation, proposed_qty=proposed_qty, notional=notional,
        realised_money_at_risk=realised_money_at_risk,
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
