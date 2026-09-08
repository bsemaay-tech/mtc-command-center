"""Offline fence for the versioned research-side cost-model registry.

The amendment's acceptance sentence is a prohibition -- "an unregistered or
provenance-broken cost model cannot produce acceptance-bearing evidence" -- so the
controls here prove the forbidden outcomes are caught rather than recomputing a formula.
"""
from dataclasses import replace
import inspect
import cost_model_registry as module

GOOD = module.CostModel(
    model_id="binance-perp-v1", version="1.0.0",
    fees_provenance=module.FROM_SCHEDULE, funding_provenance=module.FROM_HISTORY,
    slippage_provenance=module.FROM_OWN_FILLS,
    observation_sources=(module.PAPER, module.TESTNET),
    cost_lineage_id="lineage-0", deployment_identity_hash="dih-0",
    triggering_event="initial registration")


def registry():
    return module.register({}, GOOD)


def check_registration(register=module.register):
    reg = register({}, GOOD)
    assert reg[GOOD.model_id] is GOOD
    # Registering twice under one id would leave two economics behind one name.
    try:
        register(reg, GOOD)
    except module.CostModelRefused as error:
        assert str(error).startswith("already_registered"), str(error)
    else:
        raise AssertionError("a model id was registered twice")
    # A provenance-broken model never enters the registry at all.
    for field, value in (("fees_provenance", module.FROM_HISTORY),
                         ("funding_provenance", module.FROM_OWN_FILLS),
                         ("slippage_provenance", module.FROM_SCHEDULE)):
        try:
            register({}, replace(GOOD, **{field: value}))
        except module.CostModelRefused as error:
            assert str(error) == field, (field, str(error))
        else:
            raise AssertionError(f"a broken {field} was registered")


def check_acceptance_bearing(gate=module.assert_acceptance_bearing):
    reg = registry()
    gate(GOOD.model_id, reg)
    # Unregistered.
    for missing in ("ghost-model", "binance-perp-v2"):
        try:
            gate(missing, reg)
        except module.NotAcceptanceBearing as error:
            assert "unregistered_cost_model" in str(error), str(error)
        else:
            raise AssertionError(f"an unregistered model was acceptance-bearing: {missing}")
    try:
        gate(GOOD.model_id, {})
    except module.NotAcceptanceBearing:
        pass
    else:
        raise AssertionError("an empty registry produced acceptance-bearing evidence")
    # Provenance broken after registration -- the registry is re-checked, not trusted.
    tampered = {GOOD.model_id: replace(GOOD, funding_provenance=module.FROM_SCHEDULE)}
    try:
        gate(GOOD.model_id, tampered)
    except module.NotAcceptanceBearing as error:
        assert "provenance_broken" in str(error), str(error)
    else:
        raise AssertionError("a provenance-broken model was acceptance-bearing")


def check_recalibration(recalibrate=module.recalibrate):
    new = recalibrate(GOOD, event="venue fee schedule changed", version="1.1.0")
    # New economics must not inherit the old identity.
    assert new.cost_lineage_id != GOOD.cost_lineage_id, new.cost_lineage_id
    assert new.deployment_identity_hash != GOOD.deployment_identity_hash
    assert new.version == "1.1.0" and new.triggering_event == "venue fee schedule changed"
    # Provenance survives a recalibration unchanged.
    assert new.fees_provenance == GOOD.fees_provenance
    module.assert_well_formed(new)


def check_recalibration_refusals(recalibrate=module.recalibrate):
    def refuse(name, **kwargs):
        arguments = dict(event="venue fee schedule changed", version="1.1.0")
        arguments.update(kwargs)
        try:
            recalibrate(GOOD, **arguments)
        except module.CostModelRefused as error:
            assert str(error).split(":")[0] == name, (name, str(error))
        else:
            raise AssertionError(f"accepted {name}")

    refuse("event", event="   ")
    refuse("version_not_moved", version=GOOD.version)
    # "event-driven, never silently calendar-driven": a date is not an event.
    for calendar in ("2026-09-08", "20260908", "2026-09-08T00:00:00Z", "scheduled",
                     "Periodic", "MONTHLY", "routine"):
        refuse("calendar_driven_recalibration", event=calendar)


def check_well_formed_refusals(validator=module.assert_well_formed):
    def refuse(name, **overrides):
        try:
            validator(replace(GOOD, **overrides))
        except module.CostModelRefused as error:
            assert str(error).split(":")[0] == name, (name, str(error))
        else:
            raise AssertionError(f"accepted {name}")

    refuse("fees_provenance", fees_provenance="assumed")
    refuse("funding_provenance", funding_provenance="assumed")
    refuse("slippage_provenance", slippage_provenance="assumed")
    refuse("unknown_observation_source", observation_sources=(module.PAPER, "vibes"))
    refuse("duplicate_observation_source", observation_sources=(module.PAPER, module.PAPER))
    refuse("model_id", model_id=" ")
    refuse("cost_lineage_id", cost_lineage_id="")
    refuse("triggering_event", triggering_event="  ")


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
    # The amendment's acceptance sentence, both halves.
    detected("UNREGISTERED MODEL ACCEPTED", check_acceptance_bearing,
             mutant("if model is None:", "if False:", "assert_acceptance_bearing"))
    detected("PROVENANCE RE-CHECK DROPPED", check_acceptance_bearing,
             mutant("assert_well_formed(model)", "pass", "assert_acceptance_bearing"))
    # "event-driven, never silently calendar-driven".
    detected("CALENDAR RECALIBRATION ACCEPTED", check_recalibration_refusals,
             mutant("if calendar_only or stripped.lower() in", "if False and stripped.lower() in",
                    "recalibrate"))
    detected("VERSION-MOVE GUARD DROPPED", check_recalibration_refusals,
             mutant("if version == model.version:", "if False:", "recalibrate"))
    # New economics inheriting the old identity is the failure the rotation prevents.
    detected("COST LINEAGE NOT ROTATED", check_recalibration,
             mutant("lineage = _derive(model.cost_lineage_id, stripped, version)",
                    "lineage = model.cost_lineage_id", "recalibrate"))
    detected("DEPLOYMENT IDENTITY NOT ROTATED", check_recalibration,
             mutant("identity = _derive(model.deployment_identity_hash, stripped, version)",
                    "identity = model.deployment_identity_hash", "recalibrate"))
    # Each cost component must come from its own named source.
    for label, old in (
        ("FEES PROVENANCE GUARD DROPPED", 'raise CostModelRefused("fees_provenance")'),
        ("FUNDING PROVENANCE GUARD DROPPED", 'raise CostModelRefused("funding_provenance")'),
        ("SLIPPAGE PROVENANCE GUARD DROPPED", 'raise CostModelRefused("slippage_provenance")'),
        ("UNKNOWN SOURCE GUARD DROPPED",
         'raise CostModelRefused(f"unknown_observation_source: {source}")'),
    ):
        detected(label, check_well_formed_refusals, mutant(old, "pass", "assert_well_formed"))
    detected("DOUBLE REGISTRATION ACCEPTED", check_registration,
             mutant("if model.model_id in registry:", "if False:", "register"))


if __name__ == "__main__":
    check_registration()
    check_acceptance_bearing()
    check_recalibration()
    check_recalibration_refusals()
    check_well_formed_refusals()
    check_mutants()
    print("COST MODEL REGISTRY CHECK: PASS")
