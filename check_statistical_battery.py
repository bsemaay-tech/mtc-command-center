"""Offline fence for statistical-battery definition v1.

§6 is mostly prohibitions, so most controls here prove a forbidden outcome is caught: a
skipped element cannot pass, a verdict cannot be read against another run, an element
cannot be deleted from the definition without moving the version, and a spent lockbox era
cannot be re-read as evidence.
"""
from dataclasses import replace
from decimal import Decimal
import inspect
import statistical_battery as module

RUN = "run-2026-09-08-a"
OTHER_RUN = "run-2026-09-08-b"
ERA = "era-2024H1"

# The owner-ratified §6 list, restated independently so drift is a test failure.
RATIFIED_ELEMENTS = ("walk_forward", "lockbox", "cpcv", "pbo", "dsr", "bh_fdr", "sensitivity")


def results(dsr="0.99", statuses=None, era=ERA):
    statuses = statuses or {}
    return [module.ElementResult(
        element=name, status=statuses.get(name, module.PASS),
        value=Decimal(dsr) if name == module.DSR else None,
        era=era if name == module.LOCKBOX else "") for name in module.ELEMENTS]


def check_v1_content():
    assert module.VERSION == "v1", module.VERSION
    assert module.ELEMENTS == RATIFIED_ELEMENTS, module.ELEMENTS
    assert len(module.ELEMENTS) == 7, len(module.ELEMENTS)
    assert module.DSR_MINIMUM == Decimal("0.95"), module.DSR_MINIMUM
    assert module.INLINE_FROM_PORT_HARVEST == ("cpcv", "pbo"), module.INLINE_FROM_PORT_HARVEST
    module.assert_pinned()


def check_verdicts(evaluate=module.evaluate):
    # All seven present and passing.
    assert evaluate(results(), evaluation_run_hash=RUN).verdict == module.PASS
    # ">= 0.95" is inclusive: exactly the threshold passes.
    assert evaluate(results(dsr="0.95"), evaluation_run_hash=RUN).verdict == module.PASS
    # A hair below fails, and names DSR as the failing element.
    below = evaluate(results(dsr="0.9499999999"), evaluation_run_hash=RUN)
    assert below.verdict == module.FAIL, below.verdict
    assert below.failing == (module.DSR,), below.failing
    # A failing element fails.
    failed = evaluate(results(statuses={module.PBO: module.FAIL}), evaluation_run_hash=RUN)
    assert failed.verdict == module.FAIL and failed.failing == (module.PBO,), failed
    # Every verdict carries its binding.
    verdict = evaluate(results(), evaluation_run_hash=RUN)
    assert verdict.evaluation_run_hash == RUN and verdict.battery_version == "v1"


def check_none_skippable(evaluate=module.evaluate):
    """No element may be omitted or skipped; either is BLOCKED, never a partial pass."""
    for element in module.ELEMENTS:
        omitted = [r for r in results() if r.element != element]
        verdict = evaluate(omitted, evaluation_run_hash=RUN)
        assert verdict.verdict == module.BLOCKED, (element, verdict.verdict)
        assert verdict.failing == (element,), (element, verdict.failing)

        skipped = evaluate(results(statuses={element: module.SKIPPED}),
                           evaluation_run_hash=RUN)
        assert skipped.verdict == module.BLOCKED, (element, skipped.verdict)
        assert element in skipped.failing, (element, skipped.failing)


def check_binding(assert_binding=module.assert_binding):
    verdict = module.evaluate(results(), evaluation_run_hash=RUN)
    assert_binding(verdict, evaluation_run_hash=RUN, battery_version="v1")
    for kwargs, name in (
        (dict(evaluation_run_hash=OTHER_RUN, battery_version="v1"),
         "verdict_run_hash_mismatch"),
        (dict(evaluation_run_hash=RUN, battery_version="v2"),
         "verdict_battery_version_mismatch"),
    ):
        try:
            assert_binding(verdict, **kwargs)
        except module.BatteryRefused as error:
            assert str(error) == name, (name, str(error))
        else:
            raise AssertionError(f"a verdict was read outside its binding: {name}")


def check_refusals(evaluate=module.evaluate):
    def refuse(name, *args, **kwargs):
        try:
            evaluate(*args, **kwargs)
        except module.BatteryRefused as error:
            assert str(error).split(":")[0] == name, (name, str(error))
        else:
            raise AssertionError(f"accepted {name}")

    refuse("evaluation_run_hash", results(), evaluation_run_hash="  ")
    refuse("duplicate_element", results() + [results()[0]], evaluation_run_hash=RUN)
    refuse("unknown_element",
           results() + [module.ElementResult("astrology", module.PASS)],
           evaluation_run_hash=RUN)
    refuse("status", [replace(r, status="MAYBE") if r.element == module.CPCV else r
                      for r in results()], evaluation_run_hash=RUN)
    refuse("lockbox_era", results(era="  "), evaluation_run_hash=RUN)
    refuse("dsr_value", [replace(r, value=None) if r.element == module.DSR else r
                         for r in results()], evaluation_run_hash=RUN)
    # An opened era is SPENT for that family: a re-read is navigational, never evidence.
    refuse("lockbox_era_spent", results(), evaluation_run_hash=RUN,
           spent_eras={"donchian-family": (ERA,)})


def definition_with_element_dropped():
    """Simulate an element deleted from the ratified definition, version unmoved."""
    namespace = dict(module.__dict__)
    namespace["ELEMENTS"] = tuple(e for e in module.ELEMENTS if e != module.SENSITIVITY)
    for name in ("_canonical", "digest", "assert_pinned"):
        exec(inspect.getsource(getattr(module, name)), namespace)
    return namespace


def check_version_pin():
    module.assert_pinned()
    try:
        definition_with_element_dropped()["assert_pinned"]()
    except module.BatteryRefused as error:
        assert "battery_edited_off_version" in str(error), str(error)
    else:
        raise AssertionError("an element was dropped from the definition off-version")


def mutant(old, new, name):
    namespace = dict(module.__dict__)
    source = inspect.getsource(getattr(module, name))
    assert old in source, old
    exec(source.replace(old, new, 1), namespace)
    return namespace[name]


def detected(label, fence, replacement):
    try:
        fence(replacement)
    except (AssertionError, ArithmeticError, AttributeError, KeyError, TypeError,
            ValueError):
        print(f"{label}: DETECTED")
    else:
        raise AssertionError(f"{label}: SURVIVED")


def check_mutants():
    detected("SKIP GATE DROPPED", check_none_skippable,
             mutant("if skipped:", "if False:", "evaluate"))
    detected("MISSING-ELEMENT GATE DROPPED", check_none_skippable,
             mutant("if missing:", "if False:", "evaluate"))
    detected("DSR THRESHOLD DROPPED", check_verdicts,
             mutant("if dsr.value < DSR_MINIMUM and DSR not in failing:", "if False:",
                    "evaluate"))
    # ">= 0.95" is inclusive; an exclusive comparison would fail a run at exactly 0.95.
    detected("DSR BOUNDARY MADE EXCLUSIVE", check_verdicts,
             mutant("if dsr.value < DSR_MINIMUM", "if dsr.value <= DSR_MINIMUM", "evaluate"))
    detected("RUN-HASH BINDING DROPPED", check_binding,
             mutant("if verdict.evaluation_run_hash != evaluation_run_hash:", "if False:",
                    "assert_binding"))
    detected("BATTERY-VERSION BINDING DROPPED", check_binding,
             mutant("if verdict.battery_version != battery_version:", "if False:",
                    "assert_binding"))
    detected("SPENT-ERA GUARD DROPPED", check_refusals,
             mutant("if lockbox.era in tuple(eras):", "if False:", "evaluate"))
    detected("DUPLICATE-ELEMENT GUARD DROPPED", check_refusals,
             mutant('raise BatteryRefused(f"duplicate_element: {result.element}")', "pass",
                    "evaluate"))
    detected("UNKNOWN-ELEMENT GUARD DROPPED", check_refusals,
             mutant('raise BatteryRefused(f"unknown_element: {result.element}")', "pass",
                    "evaluate"))
    def pin_fence(pinned_check):
        """The definition must refuse to be read when it no longer hashes to its version."""
        try:
            pinned_check(pinned="deadbeef")
        except module.BatteryRefused:
            return
        raise AssertionError("an off-version definition was accepted")

    detected("VERSION PIN DROPPED", pin_fence,
             mutant("if expected != actual:", "if False:", "assert_pinned"))


if __name__ == "__main__":
    check_v1_content()
    check_version_pin()
    check_verdicts()
    check_none_skippable()
    check_binding()
    check_refusals()
    check_mutants()
    print("STATISTICAL BATTERY CHECK: PASS")
