"""Offline fence for the evidence class of a research run.

The gate's sentence -- "there is no manifest stamp that converts it" -- is a statement
about the *shape* of the code, not only its behaviour. So one control here is structural:
it reads the signature of ``assert_acceptance_bearing`` and fails if a stamp, label,
override or force parameter has appeared. A conversion path that exists is a conversion
path that will eventually be used.
"""
from dataclasses import replace
import inspect
import cost_model_registry as costs
import evidence_class as module

MODEL = costs.CostModel(
    model_id="binance-perp-v1", version="1.0.0",
    fees_provenance=costs.FROM_SCHEDULE, funding_provenance=costs.FROM_HISTORY,
    slippage_provenance=costs.FROM_OWN_FILLS, observation_sources=(costs.PAPER,),
    cost_lineage_id="lineage-0", deployment_identity_hash="dih-0",
    triggering_event="initial registration")
REGISTRY = costs.register({}, MODEL)

ACCEPTABLE = module.RunFacts(
    canonical_simulator=True, allocator_import_identity_proven=True,
    kernel_version="CORRECTED_VNEXT-1.0.0", cost_model_id="binance-perp-v1",
    manifest_computed=True, manifest_has_required_gap=False)

# Each degradation, with the fact that causes it. Every one alone must be enough.
DEGRADATIONS = (
    ("canonical_simulator", False, "not the canonical simulator"),
    ("allocator_import_identity_proven", False, "import identity not proven"),
    ("kernel_version", "  ", "no kernel version recorded"),
    ("cost_model_id", "", "no cost model named"),
    ("cost_model_id", "never-registered", "cost model not acceptance-bearing"),
    ("manifest_computed", False, "manifest not computed"),
    ("manifest_has_required_gap", True, "a REQUIRED control is unsimulated"),
)


def check_signature_has_no_conversion(_ignored=None):
    """The signature is the enforcement: no parameter may offer a way to convert a run."""
    signature = inspect.signature(module.assert_acceptance_bearing)
    forbidden = ("stamp", "label", "override", "force", "evidence_class", "accept",
                 "as_acceptance_bearing", "reason")
    for name in signature.parameters:
        assert name not in forbidden, f"a conversion parameter appeared: {name}"
    assert tuple(signature.parameters) == ("facts", "cost_registry"), tuple(
        signature.parameters)


def check_classification(classify=module.classify):
    evidence_class, reasons = classify(ACCEPTABLE, cost_registry=REGISTRY)
    assert evidence_class == module.ACCEPTANCE_BEARING, (evidence_class, reasons)
    assert reasons == (), reasons
    # No partial credit: any single degraded fact makes the whole run screening.
    for field, value, label in DEGRADATIONS:
        degraded = replace(ACCEPTABLE, **{field: value})
        evidence_class, reasons = classify(degraded, cost_registry=REGISTRY)
        assert evidence_class == module.SIGNAL_SCREEN_ONLY, (label, evidence_class)
        assert reasons, label
    # An empty registry breaks even a well-named model.
    evidence_class, _ = classify(ACCEPTABLE, cost_registry={})
    assert evidence_class == module.SIGNAL_SCREEN_ONLY, evidence_class


def check_gate(gate=module.assert_acceptance_bearing):
    gate(ACCEPTABLE, cost_registry=REGISTRY)
    for field, value, label in DEGRADATIONS:
        degraded = replace(ACCEPTABLE, **{field: value})
        try:
            gate(degraded, cost_registry=REGISTRY)
        except module.NotAcceptanceBearing as error:
            assert module.SIGNAL_SCREEN_ONLY in str(error), (label, str(error))
        else:
            raise AssertionError(f"a screening run was accepted as evidence: {label}")


def check_withdrawn_state(classify=module.classify):
    """ALLOCATOR_NOT_YET_SHARED is withdrawn: refused on sight, never quietly ignored."""
    for stamp in module.WITHDRAWN_STATES:
        stamped = replace(ACCEPTABLE, legacy_state_stamp=stamp)
        try:
            classify(stamped, cost_registry=REGISTRY)
        except module.EvidenceRefused as error:
            assert "withdrawn_state" in str(error), str(error)
        else:
            raise AssertionError(f"a withdrawn state was accepted: {stamp}")
    unknown = replace(ACCEPTABLE, legacy_state_stamp="LOOKS_FINE")
    try:
        classify(unknown, cost_registry=REGISTRY)
    except module.EvidenceRefused as error:
        assert "unknown_state_stamp" in str(error), str(error)
    else:
        raise AssertionError("an unknown state stamp was accepted")


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
    # The failure the R1 correction pass was written about: a stand-in passing the gate.
    detected("STAND-IN ACCEPTED", check_classification,
             mutant("if not facts.allocator_import_identity_proven:", "if False:", "classify"))
    detected("NON-CANONICAL SIMULATOR ACCEPTED", check_classification,
             mutant("if not facts.canonical_simulator:", "if False:", "classify"))
    detected("MISSING KERNEL VERSION ACCEPTED", check_classification,
             mutant("if not isinstance(facts.kernel_version, str) or not facts.kernel_version.strip():",
                    "if False:", "classify"))
    detected("UNCOMPUTED MANIFEST ACCEPTED", check_classification,
             mutant("if not facts.manifest_computed:", "if False:", "classify"))
    detected("REQUIRED GAP ACCEPTED", check_classification,
             mutant("if facts.manifest_has_required_gap:", "if False:", "classify"))
    detected("BROKEN COST MODEL ACCEPTED", check_classification,
             mutant("reasons.append(f\"cost model not acceptance-bearing: {error}\")", "pass",
                    "classify"))
    # Partial credit is the subtler version of the same failure.
    detected("PARTIAL CREDIT GRANTED", check_classification,
             mutant("if reasons:", "if False:", "classify"))
    detected("WITHDRAWN STATE IGNORED", check_withdrawn_state,
             mutant("if facts.legacy_state_stamp:", "if False:", "classify"))
    detected("GATE ACCEPTS SCREENING", check_gate,
             mutant("if evidence_class != ACCEPTANCE_BEARING:", "if False:",
                    "assert_acceptance_bearing"))


if __name__ == "__main__":
    check_signature_has_no_conversion()
    check_classification()
    check_gate()
    check_withdrawn_state()
    check_mutants()
    print("EVIDENCE CLASS CHECK: PASS")
