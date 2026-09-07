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
    print("SHARED RISK CALCULATOR CHECK: PASS")
