"""Offline regression fence; expected quantities use exact rational arithmetic."""
from dataclasses import replace
from decimal import Context, Decimal, ROUND_HALF_UP, Inexact, localcontext
from fractions import Fraction
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from types import SimpleNamespace
import inspect
import shared_risk_calculator as module


def inputs():
    return dict(account_size=Decimal("10000"), stop_distance=Decimal("7"),
                contract_multiplier=Decimal("3"),
                settings=module.RiskRequest("worked-example-v1", Decimal("0.01")))


def expect_refused(calculator, arguments, name):
    try:
        calculator(**arguments)
    except module.RiskCalculationRefused as error:
        assert str(error) == name, (name, str(error))
    else:
        raise AssertionError(f"accepted {name}")


def check(calculator=module.calculate_position_size):
    for stop, multiplier, expected in (
        ("7", "3", "4.761904761904761904761904761"),
        ("3", "1", "33.33333333333333333333333333"),
        ("7", "1", "14.28571428571428571428571428"),
        ("5", "1", "20"),  # retained original worked example
    ):
        arguments = inputs()
        arguments.update(stop_distance=Decimal(stop), contract_multiplier=Decimal(multiplier))
        result = calculator(**arguments)
        assert result.position_size == Decimal(expected)
        assert result.money_at_risk == Decimal("100.00")
        assert result.allocation_policy_version == "worked-example-v1"
        assert result.contract_multiplier == Decimal(multiplier)
        assert result.account_size == arguments["account_size"]
        assert result.stop_distance == arguments["stop_distance"]
        assert result.requested_risk_fraction == arguments["settings"].requested_risk_fraction
        assert Fraction(result.position_size) * Fraction(stop) * Fraction(multiplier) <= 100
    arguments = inputs()
    arguments.update(stop_distance=Decimal("1.0000000000000000000000000009"),
                     contract_multiplier=Decimal("1.0000000000000000000000000009"))
    result = calculator(**arguments)
    assert (Fraction(result.position_size) * Fraction(arguments["stop_distance"])
            * Fraction(arguments["contract_multiplier"])) <= 100


def check_context(calculator=module.calculate_position_size):
    expected = calculator(**inputs())
    for precision in (3, 5, 9, 28):
        with localcontext() as context:
            context.prec = precision
            context.rounding = ROUND_HALF_UP
            context.Emax, context.Emin, context.clamp = 2, -2, 1
            context.traps[Inexact] = True
            before = str(context)
            assert calculator(**inputs()) == expected
            assert str(context) == before


def check_refusals(calculator=module.calculate_position_size):
    for version in (None, 3, "", " ", " v1", "v1 ", "\tv1"):
        arguments = inputs()
        arguments["settings"] = module.RiskRequest(version, Decimal("0.01"))
        expect_refused(calculator, arguments, "allocation_policy_version")
    for name in ("account_size", "stop_distance", "contract_multiplier", "requested_risk_fraction"):
        for value in (None, "1", True, Decimal("NaN"), Decimal("sNaN"),
                      Decimal("Infinity"), Decimal("-Infinity"), Decimal(0), Decimal(-1)):
            arguments = inputs()
            if name == "requested_risk_fraction":
                arguments["settings"] = module.RiskRequest("v1", value)
            else:
                arguments[name] = value
            expect_refused(calculator, arguments, "risk_fraction" if name == "requested_risk_fraction" else name)
    malformed = object.__new__(module.RiskRequest)
    for settings in (None, object(), {}, malformed,
                     SimpleNamespace(allocation_policy_version="v1", requested_risk_fraction=Decimal("0.01"))):
        arguments = inputs()
        arguments["settings"] = settings
        expect_refused(calculator, arguments, "settings")


def check_extremes(calculator=module.calculate_position_size):
    arguments = inputs()
    arguments.update(account_size=Decimal("1e999999"),
                     settings=module.RiskRequest("v1", Decimal("10")))
    expect_refused(calculator, arguments, "overflow")
    arguments = inputs()
    arguments.update(account_size=Decimal("1e-999999"), stop_distance=Decimal("1e999999"))
    expect_refused(calculator, arguments, "position_size_zero")
    arguments = inputs()
    arguments["account_size"] = Decimal("1e-1000026")
    expect_refused(calculator, arguments, "position_size_zero")
    arguments = inputs()
    arguments.update(stop_distance=Decimal("1e-1000026"), contract_multiplier=Decimal("0.01"))
    expect_refused(calculator, arguments, "underflow")


def check_cli():
    arguments = ["--account-size", "10000", "--entry-price", "10", "--stop-price", "3",
                 "--requested-risk-fraction", "0.01", "--allocation-policy-version", "v1"]
    with redirect_stderr(StringIO()):
        try:
            module.main(arguments)
        except SystemExit as error:
            assert error.code == 2
        else:
            raise AssertionError("CLI accepted missing multiplier")
    for precision in (3, 28):
        with localcontext() as context, redirect_stdout(StringIO()) as output:
            context.prec = precision
            context.traps[Inexact] = True
            assert module.main(arguments + ["--contract-multiplier", "3"]) == 0
            assert "Position size: 4.761904761904761904761904761" in output.getvalue()


def check_cli_extremes(cases=(
    ("1e999999999999999999", "1", "invalid_operation"),
    ("1", "1e-999999999999999999", "invalid_operation"),
    ("1e1000001", "1", "overflow"),
)):
    # These identified cases fail quickly; do not allocate a giant intermediate.
    for entry, stop, refusal in cases:
        arguments = ["--account-size", "10000", "--entry-price", entry, "--stop-price", stop,
                     "--contract-multiplier", "3", "--requested-risk-fraction", "0.01",
                     "--allocation-policy-version", "v1"]
        with redirect_stderr(StringIO()) as errors, redirect_stdout(StringIO()) as output:
            try:
                module.main(arguments)
            except SystemExit as error:
                assert error.code == 2, ("cli_extreme_exit", entry, stop, error.code)
            else:
                raise AssertionError(("cli_extreme_accepted", entry, stop))
        assert errors.getvalue() == f"REFUSED: {refusal}\n", (
            "cli_extreme_refusal", entry, stop, errors.getvalue())
        assert output.getvalue() == "", ("cli_extreme_output", entry, stop, output.getvalue())
    print("CLI EXTREME NAMED REFUSALS: PASS")


def check_cli_underflow(cases=(
    ("2.9e-1000026", "1e-1000026", True),
    ("1e-1000026", "2.9e-1000026", True),
    ("2e-1000026", "1e-1000026", False),
)):
    for entry, stop, must_refuse in cases:
        arguments = ["--account-size", "1e-28", "--entry-price", entry,
                     "--stop-price", stop, "--contract-multiplier", "1",
                     "--requested-risk-fraction", "1", "--allocation-policy-version", "v1"]
        with redirect_stderr(StringIO()) as errors, redirect_stdout(StringIO()) as output:
            try:
                exit_code = module.main(arguments)
            except SystemExit as error:
                exit_code = error.code
        if exit_code == 0:
            quantity = Decimal(next(line.split(": ", 1)[1]
                                    for line in output.getvalue().splitlines()
                                    if line.startswith("Position size: ")))
            # Independent wide exponent range keeps the true distance exact.
            with localcontext(Context(prec=80, Emin=-999999999, Emax=999999999)):
                distance = abs(Decimal(entry) - Decimal(stop))
                ratio = quantity * distance / Decimal("1e-28")
                assert quantity > 0 and ratio <= 1, ("cli_actual_risk_limit", entry, stop, ratio)
            assert not must_refuse, ("cli_inexact_underflow_accepted", entry, stop)
            assert errors.getvalue() == ""
        else:
            assert must_refuse, ("cli_exact_subnormal_refused", entry, stop)
            assert exit_code == 2 and errors.getvalue() == "REFUSED: underflow\n"
            assert output.getvalue() == ""
    print("CLI UNDERFLOW RISK BOUND AND EXACT SUBNORMAL CONTROL: PASS")


def source_mutant(old, new):
    namespace = dict(module.__dict__)
    function_source = inspect.getsource(module.calculate_position_size)
    if old == "ROUND_DOWN":
        namespace["ROUNDING"] = ROUND_HALF_UP
        exec(inspect.getsource(module._context), namespace)
        exec(function_source, namespace)
    else:
        assert old in function_source, old
        exec(function_source.replace(old, new, 1), namespace)
    return namespace["calculate_position_size"]


def detected(label, fence, calculator):
    try:
        fence(calculator)
    except (AssertionError, ArithmeticError, AttributeError, TypeError, ValueError):
        print(f"{label}: DETECTED")
    else:
        raise AssertionError(f"{label}: SURVIVED")


def check_mutants():
    def modified_copy(**arguments):
        result = module.calculate_position_size(**arguments)
        return replace(result, position_size=result.position_size / 2)

    def float_copy(**arguments):
        result = module.calculate_position_size(**arguments)
        quantity = (float(arguments["account_size"])
                    * float(arguments["settings"].requested_risk_fraction)
                    / (float(arguments["stop_distance"]) * float(arguments["contract_multiplier"])))
        return replace(result, position_size=Decimal(str(quantity)))

    def no_refusals(**arguments):
        return module.calculate_position_size(**inputs())

    detected("MODIFIED COPY", check, modified_copy)
    detected("ALL REFUSALS DROPPED", check_refusals, no_refusals)
    detected("FLOAT ARITHMETIC", check, float_copy)
    detected("ROUND_HALF_UP", check, source_mutant("ROUND_DOWN", "ROUND_HALF_UP"))
    detected("MULTIPLIER IGNORED", check,
             source_mutant("per_unit_risk = stop_distance * contract_multiplier", "per_unit_risk = stop_distance"))
    detected("NONFINITE GUARD DROPPED", check_refusals,
             source_mutant("not value.is_finite() or ", ""))
    detected("PADDED VERSION GUARD DROPPED", check_refusals,
             source_mutant(" or version != version.strip()", ""))
    detected("SETTINGS TYPE GUARD DROPPED", check_refusals,
             source_mutant("if not isinstance(settings, RiskRequest):", "if False:"))
    namespace = dict(module.__dict__)
    from decimal import getcontext
    namespace["_context"] = lambda precision=28: getcontext()
    exec(inspect.getsource(module.calculate_position_size), namespace)
    detected("CALLER CONTEXT", check_context, namespace["calculate_position_size"])
    detected("OVERFLOW REFUSAL DROPPED", check_extremes,
             source_mutant('raise RiskCalculationRefused("overflow") from error', 'raise error'))
    detected("ZERO REFUSAL DROPPED", check_extremes,
             source_mutant('if position_size == 0:', 'if False:'))



# --- Risk Allocator stages: quantisation and the bound allocation-policy caps -----------
# The invariant these fences exist for is the one brief 5.5 states as a prohibition rather
# than a formula: a binding cap is a rejection, never a quietly smaller order. A formula
# can be checked by recomputation; a prohibition can only be checked by proving that the
# forbidden behaviour would be caught. Hence CAP TRIMS INSTEAD OF REJECTING below, which
# is the only control here that mutates conduct rather than arithmetic.


def allocator_inputs():
    """Worked example: 20 units exactly, on a 0.5 step, at 0.01 risk and 0.1 leverage."""
    return dict(
        account_size=Decimal("10000"),
        entry_reference_price=Decimal("50"),
        stop_distance=Decimal("5"),
        contract_multiplier=Decimal("1"),
        settings=module.RiskRequest("worked-example-v1", Decimal("0.01")),
        metadata=module.PackageMetadata(
            qty_step=Decimal("0.5"), min_qty=Decimal("1"), min_notional=Decimal("100")),
        caps=module.AllocationPolicyCaps(
            allocation_policy_version="worked-example-v1",
            max_risk_at_stop_fraction=Decimal("0.01"),
            max_leverage=Decimal("1"), max_exposure_fraction=Decimal("1")),
        existing_gross_notional=Decimal("0"),
    )


def check_allocator(resolver=module.resolve_proposed_qty):
    # Proposed in full, and the cap that sits exactly on its bound does not bind.
    result = resolver(**allocator_inputs())
    assert result.proposed_qty == Decimal("20"), result.proposed_qty
    assert result.notional == Decimal("1000"), result.notional
    assert result.realised_money_at_risk == Decimal("100"), result.realised_money_at_risk
    assert result.allocation_policy_version == "worked-example-v1"
    assert result.calculation.position_size == Decimal("20")

    # A quantity off the step is rounded DOWN to it, never up: 100/21 -> 4.5 on a 0.5 step.
    arguments = allocator_inputs()
    arguments.update(stop_distance=Decimal("7"), contract_multiplier=Decimal("3"))
    result = resolver(**arguments)
    assert result.proposed_qty == Decimal("4.5"), result.proposed_qty
    assert result.notional == Decimal("675"), result.notional
    # Rounding down can only reduce risk below the frozen package's request.
    assert Fraction(result.realised_money_at_risk) <= 100, result.realised_money_at_risk
    assert Fraction(result.proposed_qty) <= Fraction(result.calculation.position_size)


def check_gross_exposure(resolver=module.resolve_proposed_qty):
    """Exposure counts the whole book; leverage counts only this proposal.

    With 8000 already open, this 1000 proposal is 0.1 leverage but 0.9 gross exposure. A
    module computing both from the proposal alone would read 0.1 for each and wave through
    a book that is nearly fully committed.
    """
    arguments = allocator_inputs()
    arguments.update(existing_gross_notional=Decimal("8000"))
    # Leverage is unchanged by the existing book, so a 1.0 leverage cap still passes...
    result = resolver(**arguments)
    assert result.proposed_qty == Decimal("20"), result.proposed_qty
    # ...while a 0.5 exposure cap must bind on 9000/10000.
    arguments.update(caps=replace(allocator_inputs()["caps"],
                                  max_exposure_fraction=Decimal("0.5")))
    expect_refused(resolver, arguments, "cap_exposure")
    # The same proposal on an empty book passes the same 0.5 exposure cap.
    arguments.update(existing_gross_notional=Decimal("0"))
    assert resolver(**arguments).proposed_qty == Decimal("20")


def check_allocator_refusals(resolver=module.resolve_proposed_qty):
    def refuse(name, **overrides):
        arguments = allocator_inputs()
        arguments.update(overrides)
        expect_refused(resolver, arguments, name)

    base = allocator_inputs()
    # Quantised 4.5 falls under a min_qty of 5.
    refuse("min_qty", stop_distance=Decimal("7"), contract_multiplier=Decimal("3"),
           metadata=module.PackageMetadata(
               qty_step=Decimal("0.5"), min_qty=Decimal("5"), min_notional=Decimal("100")))
    # Notional 1000 falls under a min_notional of 2000.
    refuse("min_notional", metadata=module.PackageMetadata(
        qty_step=Decimal("0.5"), min_qty=Decimal("1"), min_notional=Decimal("2000")))
    # Each cap, alone, is a rejection rather than a smaller order.
    refuse("cap_risk_at_stop", caps=replace(
        base["caps"], max_risk_at_stop_fraction=Decimal("0.009")))
    refuse("cap_leverage", caps=replace(base["caps"], max_leverage=Decimal("0.05")))
    refuse("cap_exposure", caps=replace(base["caps"], max_exposure_fraction=Decimal("0.05")))
    # A quantity may not be capped under a policy it was not bound to.
    refuse("allocation_policy_version_mismatch",
           caps=replace(base["caps"], allocation_policy_version="other-policy-v1"))
    refuse("caps", caps=SimpleNamespace(
        allocation_policy_version="worked-example-v1",
        max_risk_at_stop_fraction=Decimal("1"), max_leverage=Decimal("1"),
        max_exposure_fraction=Decimal("1")))
    refuse("existing_gross_notional", existing_gross_notional=Decimal("-1"))
    refuse("existing_gross_notional", existing_gross_notional=1000)
    refuse("metadata", metadata=SimpleNamespace(
        qty_step=Decimal("0.5"), min_qty=Decimal("1"), min_notional=Decimal("100")))


def allocator_mutant(old, new):
    """Rebuild the three allocator stages in one namespace, mutating the first match.

    ``resolve_proposed_qty`` resolves its callees as globals, so rebuilding it last in the
    same namespace makes it call the mutated stage rather than the module's.
    """
    namespace = dict(module.__dict__)
    replaced = False
    for name in ("quantise_position_size", "apply_allocation_policy_caps",
                 "resolve_proposed_qty"):
        source = inspect.getsource(getattr(module, name))
        if not replaced and old in source:
            source = source.replace(old, new, 1)
            replaced = True
        exec(source, namespace)
    assert replaced, old
    return namespace["resolve_proposed_qty"]


def check_allocator_mutants():
    def trimming_resolver(**arguments):
        """The forbidden conduct: on a binding cap, propose a quietly smaller order."""
        try:
            return module.resolve_proposed_qty(**arguments)
        except module.RiskCalculationRefused as error:
            if not str(error).startswith("cap_"):
                raise
            relaxed = replace(arguments["caps"], max_risk_at_stop_fraction=Decimal("1"),
                              max_leverage=Decimal("1000"),
                              max_exposure_fraction=Decimal("1000"))
            full = module.resolve_proposed_qty(**{**arguments, "caps": relaxed})
            return replace(full, proposed_qty=full.proposed_qty / 2)

    detected("CAP TRIMS INSTEAD OF REJECTING", check_allocator_refusals, trimming_resolver)
    detected("EXPOSURE IGNORES EXISTING BOOK", check_gross_exposure,
             allocator_mutant("exposure = (existing_gross_notional + notional) / account_size",
                              "exposure = notional / account_size"))
    detected("QUANTISATION ROUNDS UP", check_allocator,
             allocator_mutant("rounding=ROUND_DOWN", 'rounding="ROUND_UP"'))
    detected("MIN_QTY GUARD DROPPED", check_allocator_refusals,
             allocator_mutant("if quantised < metadata.min_qty:", "if False:"))
    detected("MIN_NOTIONAL GUARD DROPPED", check_allocator_refusals,
             allocator_mutant("if notional < metadata.min_notional:", "if False:"))
    detected("RISK-AT-STOP CAP DROPPED", check_allocator_refusals,
             allocator_mutant("if risk_fraction > caps.max_risk_at_stop_fraction:", "if False:"))
    detected("LEVERAGE CAP DROPPED", check_allocator_refusals,
             allocator_mutant("if leverage > caps.max_leverage:", "if False:"))
    detected("EXPOSURE CAP DROPPED", check_allocator_refusals,
             allocator_mutant("if exposure > caps.max_exposure_fraction:", "if False:"))
    detected("POLICY IDENTITY GUARD DROPPED", check_allocator_refusals,
             allocator_mutant("if version != settings.allocation_policy_version:", "if False:"))
    detected("CAPS TYPE GUARD DROPPED", check_allocator_refusals,
             allocator_mutant("if not isinstance(caps, AllocationPolicyCaps):", "if False:"))
    detected("METADATA TYPE GUARD DROPPED", check_allocator_refusals,
             allocator_mutant("if not isinstance(metadata, PackageMetadata):", "if False:"))


if __name__ == "__main__":
    assert hasattr(module, "RiskRequest"), "missing RiskRequest / required multiplier repair"
    check()
    check_context()
    check_refusals()
    check_extremes()
    check_cli()
    check_cli_extremes()
    check_cli_underflow()
    check_mutants()
    check_allocator()
    check_gross_exposure()
    check_allocator_refusals()
    check_allocator_mutants()
    print("SHARED RISK CALCULATOR CHECK: PASS")
