"""Offline fence for the computed UNSIMULATED_CONTROLS manifest and the promotion block.

The acceptance gate asks for one fixture by name: "a `REQUIRED` control in the manifest
**blocks promotion**, proven by a **D026** fixture that is RED without the gate and GREEN
with it". That is REQUIRED GATE DROPPED below. The rest of the mutants defend the other
half of the gate -- that an empty manifest which was never computed cannot pass.
"""
from dataclasses import replace
import inspect
import unsimulated_controls as module


ENABLED = ("funding_cost", "contract_multiplier", "gap_aware_stop_fills", "in_path_slippage",
           "same_bar_collision_policy", "fee_schedule", "minimum_notional")
CLASSIFICATIONS = {
    "funding_cost": module.REQUIRED,
    "contract_multiplier": module.REQUIRED,
    "gap_aware_stop_fills": module.REQUIRED,
    "in_path_slippage": module.REQUIRED,
    "same_bar_collision_policy": module.REQUIRED,
    "fee_schedule": module.REQUIRED,
    "minimum_notional": module.INFORMATIONAL,
}
REASONS = {
    "funding_cost": "kernel funding model not migrated (WP-P0-12)",
    "minimum_notional": "venue minimum is a reporting note in research",
    "in_path_slippage": "in-path slippage not implemented by the research simulator",
}


def compute(simulated, **overrides):
    arguments = dict(enabled=ENABLED, classifications=CLASSIFICATIONS,
                     simulated=simulated, reasons=REASONS)
    arguments.update(overrides)
    return module.compute_unsimulated_controls(**arguments)


def all_but(*missing):
    return tuple(name for name in ENABLED if name not in missing)


def expect_refused(callable_, arguments, name, error_type):
    try:
        callable_(**arguments)
    except error_type as error:
        assert str(error).split(":")[0] == name, (name, str(error))
    else:
        raise AssertionError(f"accepted {name}")


def check_manifest(computer=module.compute_unsimulated_controls):
    def run(simulated, **overrides):
        arguments = dict(enabled=ENABLED, classifications=CLASSIFICATIONS,
                         simulated=simulated, reasons=REASONS)
        arguments.update(overrides)
        return computer(**arguments)

    # Entries are exactly the enabled controls the simulator does not cover, in order.
    manifest = run(all_but("funding_cost", "minimum_notional"))
    assert tuple(e.control for e in manifest.entries) == ("funding_cost", "minimum_notional")
    assert manifest.entries[0].classification == module.REQUIRED
    assert manifest.entries[1].classification == module.INFORMATIONAL
    assert manifest.entries[0].reason == REASONS["funding_cost"]
    assert manifest.enabled == ENABLED

    # A fully simulated run computes an EMPTY manifest -- and it still carries its inputs.
    full = run(ENABLED)
    assert full.entries == ()
    assert full.enabled == ENABLED
    assert len(full.classifications) == len(ENABLED)


def check_manifest_refusals(computer=module.compute_unsimulated_controls):
    def refuse(name, **overrides):
        arguments = dict(enabled=ENABLED, classifications=CLASSIFICATIONS,
                         simulated=all_but("funding_cost", "minimum_notional"),
                         reasons=REASONS)
        arguments.update(overrides)
        expect_refused(computer, arguments, name, module.ManifestRefused)

    refuse("enabled_empty", enabled=(), simulated=())
    refuse("classification", classifications={k: v for k, v in CLASSIFICATIONS.items()
                                              if k != "funding_cost"})
    refuse("classification", classifications=dict(CLASSIFICATIONS, funding_cost="MAYBE"))
    refuse("reason", reasons={k: v for k, v in REASONS.items() if k != "funding_cost"})
    refuse("reason", reasons=dict(REASONS, funding_cost="   "))
    refuse("simulated_not_enabled", simulated=ENABLED + ("not_a_control",))
    refuse("enabled_duplicate", enabled=ENABLED + ("funding_cost",))
    refuse("enabled", enabled=("ok", 7))
    refuse("mapping", classifications=[("funding_cost", module.REQUIRED)])


def check_promotion(block=module.promotion_block):
    # A run that simulates everything promotes.
    block(compute(ENABLED))
    # Informational-only gaps promote.
    block(compute(all_but("minimum_notional")))
    # THE D026 FIXTURE: a REQUIRED control in the manifest blocks promotion.
    blocked = compute(all_but("funding_cost"))
    try:
        block(blocked)
    except module.PromotionBlocked as error:
        assert str(error).startswith("required_control_unsimulated"), str(error)
    else:
        raise AssertionError("a REQUIRED unsimulated control promoted")
    # A REQUIRED gap alongside an informational one still blocks.
    try:
        block(compute(all_but("funding_cost", "minimum_notional")))
    except module.PromotionBlocked:
        pass
    else:
        raise AssertionError("a REQUIRED unsimulated control promoted")


def check_promotion_not_computed(block=module.promotion_block):
    """An authored or tampered manifest is refused however plausible it looks."""
    def refuse(manifest):
        try:
            block(manifest)
        except module.PromotionBlocked as error:
            assert str(error) == "not_computed", str(error)
        else:
            raise AssertionError("an uncomputed manifest promoted")

    computed = compute(all_but("funding_cost"))
    # The exact object the acceptance gate names: empty, and never computed from anything.
    refuse(module.UnsimulatedControls(entries=(), enabled=(), simulated=(), classifications=()))
    # The authored empty manifest: inputs kept, the inconvenient conclusion deleted.
    refuse(replace(computed, entries=()))
    # Inputs kept, one inconvenient entry dropped.
    refuse(replace(compute(all_but("funding_cost", "minimum_notional")),
                   entries=compute(all_but("funding_cost", "minimum_notional")).entries[1:]))
    # A REQUIRED entry relabelled INFORMATIONAL to slip past the block.
    entry = computed.entries[0]
    refuse(replace(computed,
                   entries=(replace(entry, classification=module.INFORMATIONAL),)))
    # Inputs erased entirely.
    refuse(replace(computed, enabled=(), simulated=(), classifications=()))
    # An entry whose reason was emptied after computation.
    refuse(replace(computed, entries=(replace(entry, reason="  "),)))
    try:
        block(object())
    except module.PromotionBlocked as error:
        assert str(error) == "manifest", str(error)
    else:
        raise AssertionError("a non-manifest promoted")


def mutant(old, new, name):
    """Rebuild one module function with a single replacement applied."""
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
    # The named D026 mutant: without the gate, a REQUIRED unsimulated control promotes.
    detected("REQUIRED GATE DROPPED", check_promotion,
             mutant("if blocking:", "if False:", "promotion_block"))
    detected("RE-DERIVATION DROPPED", check_promotion_not_computed,
             mutant("if actual != expected:", "if False:", "promotion_block"))
    detected("EMPTY INPUT GUARD DROPPED", check_promotion_not_computed,
             mutant("if not enabled:\n        raise PromotionBlocked", 
                    "if False:\n        raise PromotionBlocked", "promotion_block"))
    detected("CLASSIFICATION TAMPER ACCEPTED", check_promotion_not_computed,
             mutant("if classifications.get(entry.control) != entry.classification:",
                    "if False:", "promotion_block"))
    detected("POST-HOC REASON GUARD DROPPED", check_promotion_not_computed,
             mutant("if not isinstance(entry.reason, str) or not entry.reason.strip():",
                    "if False:", "promotion_block"))
    detected("ENABLED-EMPTY REFUSAL DROPPED", check_manifest_refusals,
             mutant('raise ManifestRefused("enabled_empty")', "pass",
                    "compute_unsimulated_controls"))
    detected("CLASSIFICATION REFUSAL DROPPED", check_manifest_refusals,
             mutant('raise ManifestRefused("classification")', "classification = INFORMATIONAL",
                    "compute_unsimulated_controls"))
    detected("REASON REFUSAL DROPPED", check_manifest_refusals,
             mutant('raise ManifestRefused("reason")', 'reason = "unstated"',
                    "compute_unsimulated_controls"))
    detected("SIMULATED-NOT-ENABLED REFUSAL DROPPED", check_manifest_refusals,
             mutant('raise ManifestRefused("simulated_not_enabled")', "pass",
                    "compute_unsimulated_controls"))
    detected("DUPLICATE GUARD DROPPED", check_manifest_refusals,
             mutant('raise ManifestRefused(f"{label}_duplicate")', "pass", "_names"))


if __name__ == "__main__":
    check_manifest()
    check_manifest_refusals()
    check_promotion()
    check_promotion_not_computed()
    check_mutants()
    print("UNSIMULATED CONTROLS CHECK: PASS")
