"""Offline fence for control-parity checklist v1.

Two kinds of control here. The mutation controls defend each governance obligation the
map-#67 fold attaches to the table. The integration check defends something neither module
can guarantee alone: the checklist and the UNSIMULATED_CONTROLS manifest are two gates
over one fact, and they must never disagree. A run whose evidence the checklist BLOCKS but
whose manifest promotes would be exactly the silent gap D-13 exists to prevent.
"""
from dataclasses import replace
import inspect
import control_parity_checklist as module
import unsimulated_controls as manifest_module


# The owner-ratified §4 table, restated independently of the module so drift is visible.
RATIFIED = (
    ("risk_allocator", "REQUIRED", "", ""),
    ("fees", "REQUIRED", "", ""),
    ("funding", "REQUIRED", "", ""),
    ("slippage", "REQUIRED", "", ""),
    ("protective_order_semantics", "REQUIRED", "", ""),
    ("guardian_authorize_reject", "TOLERATED", "veto_rate", "SHADOW"),
    ("partial_fills", "TOLERATED", "fill_shape_divergence", "TESTNET"),
    ("snapshot_staleness", "TOLERATED", "staleness_distribution", "SHADOW"),
)


def check_v1_content():
    """The table is the owner's, not the module's: any drift from §4 is a defect."""
    rows = module.CHECKLIST_V1
    assert module.VERSION == "v1", module.VERSION
    assert len(rows) == len(RATIFIED), (len(rows), len(RATIFIED))
    for row, (control, tier, metric, environment) in zip(rows, RATIFIED):
        assert row.control == control, (row.control, control)
        assert row.tier == tier, (row.control, row.tier, tier)
        assert row.divergence_metric == metric, (row.control, row.divergence_metric)
        assert row.measured_at == environment, (row.control, row.measured_at)
    assert module.required_controls() == tuple(
        c for c, t, _, _ in RATIFIED if t == "REQUIRED")
    assert module.tolerated_controls() == tuple(
        c for c, t, _, _ in RATIFIED if t == "TOLERATED")
    module.assert_pinned()
    module.assert_well_formed()


def check_projection(project=module.classifications):
    """REQUIRED must project to REQUIRED; tolerated to INFORMATIONAL. Never the reverse."""
    mapping = project()
    assert set(mapping) == set(module.controls()), sorted(mapping)
    for control in module.required_controls():
        assert mapping[control] == manifest_module.REQUIRED, (control, mapping[control])
    for control in module.tolerated_controls():
        assert mapping[control] == manifest_module.INFORMATIONAL, (control, mapping[control])


def check_blocked_evidence(gate=module.blocked_evidence):
    # Full coverage passes.
    gate(module.controls())
    # Every REQUIRED control, alone, blocks when absent.
    for control in module.required_controls():
        try:
            gate([name for name in module.controls() if name != control])
        except module.BlockedEvidence as error:
            assert control in str(error), (control, str(error))
        else:
            raise AssertionError(f"a missing REQUIRED control passed: {control}")
    # A tolerated control absent does NOT block: it is declared, not required.
    for control in module.tolerated_controls():
        gate([name for name in module.controls() if name != control])
    # Claiming to simulate something the checklist does not govern is refused.
    try:
        gate(tuple(module.controls()) + ("not_a_control",))
    except module.ChecklistRefused as error:
        assert "simulated_not_in_checklist" in str(error), str(error)
    else:
        raise AssertionError("an ungoverned control was accepted as simulated")


def check_gate_agreement():
    """The integration invariant: the two gates never disagree about one run.

    For every subset of the checklist's controls that a run might simulate, the checklist's
    BLOCKED-evidence verdict and the manifest's promotion verdict must match exactly.
    """
    controls = module.controls()
    classifications = module.classifications()
    reasons = {name: f"not simulated by this run ({name})" for name in controls}
    for omitted in [()] + [(name,) for name in controls] + [
            ("funding", "partial_fills"), ("snapshot_staleness", "partial_fills"),
            tuple(module.required_controls()), tuple(module.tolerated_controls())]:
        simulated = tuple(name for name in controls if name not in omitted)
        try:
            module.blocked_evidence(simulated)
            checklist_blocks = False
        except module.BlockedEvidence:
            checklist_blocks = True
        computed = manifest_module.compute_unsimulated_controls(
            enabled=controls, classifications=classifications,
            simulated=simulated, reasons=reasons)
        try:
            manifest_module.promotion_block(computed)
            manifest_blocks = False
        except manifest_module.PromotionBlocked:
            manifest_blocks = True
        assert checklist_blocks == manifest_blocks, (
            omitted, "checklist blocks" if checklist_blocks else "checklist allows",
            "manifest blocks" if manifest_blocks else "manifest allows")


def check_version_pin():
    """The real pin accepts v1 as ratified and refuses any edit that skips a version."""
    module.assert_pinned(module.CHECKLIST_V1)
    demoted = module.CHECKLIST_V1[:2] + (
        replace(module.CHECKLIST_V1[2], tier=module.TOLERATED,
                divergence_metric="funding_drift", measured_at=module.SHADOW,
                d026_fixture="D026/funding", run_hash_member=True),
    ) + module.CHECKLIST_V1[3:]
    try:
        module.assert_pinned(demoted)
    except module.ChecklistRefused as error:
        assert "checklist_edited_off_version" in str(error), str(error)
    else:
        raise AssertionError("an off-version edit was accepted")
    # blocked_evidence pins before it judges, so an edited table cannot be used at all.
    try:
        module.blocked_evidence(module.controls(), rows=demoted)
    except module.ChecklistRefused as error:
        assert "checklist_edited_off_version" in str(error), str(error)
    else:
        raise AssertionError("an off-version table produced a verdict")


def check_manifest_for_run():
    """The canonical entry point computes against the register, not a local list."""
    reasons = {name: f"not simulated by this run ({name})" for name in module.controls()}
    simulated = tuple(n for n in module.controls() if n != "partial_fills")
    computed = module.manifest_for_run(simulated, reasons)
    assert computed.enabled == module.controls(), computed.enabled
    assert tuple(e.control for e in computed.entries) == ("partial_fills",)
    assert computed.entries[0].classification == manifest_module.INFORMATIONAL
    manifest_module.promotion_block(computed)  # tolerated gap promotes
    # A REQUIRED gap computed through the same entry point blocks.
    blocked = module.manifest_for_run(
        tuple(n for n in module.controls() if n != "fees"), reasons)
    try:
        manifest_module.promotion_block(blocked)
    except manifest_module.PromotionBlocked as error:
        assert "fees" in str(error), str(error)
    else:
        raise AssertionError("a REQUIRED gap promoted through manifest_for_run")


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
    edited = module.CHECKLIST_V1[:2] + (
        replace(module.CHECKLIST_V1[2], tier=module.TOLERATED,
                divergence_metric="funding_drift", measured_at=module.SHADOW,
                d026_fixture="D026/funding", run_hash_member=True),
    ) + module.CHECKLIST_V1[3:]

    def pin_fence(pinned_check):
        """An owner-ratified REQUIRED row demoted to tolerated, the version unmoved."""
        try:
            pinned_check(edited)
        except module.ChecklistRefused:
            return
        raise AssertionError("an off-version edit was accepted")

    # The version pin is what makes "changes are owner-gated" mechanical.
    detected("VERSION PIN DROPPED", pin_fence,
             mutant("if expected != actual:", "if False:", "assert_pinned"))
    # The load-bearing rule: a REQUIRED control absent must block evidence.
    detected("BLOCKED-EVIDENCE GATE DROPPED", check_blocked_evidence,
             mutant("if missing:", "if False:", "blocked_evidence"))
    detected("UNGOVERNED-CONTROL GUARD DROPPED", check_blocked_evidence,
             mutant("if unknown:", "if False:", "blocked_evidence"))
    # The projection may never soften a REQUIRED row into an informational one.
    detected("PROJECTION SOFTENS REQUIRED", check_projection,
             mutant('"REQUIRED" if row.tier == REQUIRED else "INFORMATIONAL"',
                    '"INFORMATIONAL"', "classifications"))
    # Each governance obligation on a tolerated row.
    for label, old in (
        ("TOLERATED WITHOUT METRIC ACCEPTED",
         'raise ChecklistRefused("tolerated_without_metric")'),
        ("TOLERATED WITHOUT D026 FIXTURE ACCEPTED",
         'raise ChecklistRefused("tolerated_without_d026_fixture")'),
        ("TOLERATED WITHOUT RUN-HASH MEMBERSHIP ACCEPTED",
         'raise ChecklistRefused("tolerated_without_run_hash_membership")'),
        ("REQUIRED WITH TOLERANCE ACCEPTED",
         'raise ChecklistRefused("required_with_tolerance")'),
        ("DUPLICATE CONTROL ACCEPTED", 'raise ChecklistRefused("duplicate_control")'),
    ):
        detected(label, check_well_formed_refusals, mutant(old, "pass", "assert_well_formed"))


def check_well_formed_refusals(validator=module.assert_well_formed):
    good = module.CHECKLIST_V1

    def refuse(name, rows):
        try:
            validator(rows)
        except module.ChecklistRefused as error:
            assert str(error) == name, (name, str(error))
        else:
            raise AssertionError(f"accepted {name}")

    tolerated = good[5]
    refuse("tolerated_without_metric",
           good[:5] + (replace(tolerated, divergence_metric=" "),) + good[6:])
    refuse("tolerated_without_d026_fixture",
           good[:5] + (replace(tolerated, d026_fixture=""),) + good[6:])
    refuse("tolerated_without_run_hash_membership",
           good[:5] + (replace(tolerated, run_hash_member=False),) + good[6:])
    refuse("required_with_tolerance",
           (replace(good[0], divergence_metric="sneaky"),) + good[1:])
    refuse("duplicate_control", good + (good[0],))
    refuse("tier", (replace(good[0], tier="MAYBE"),) + good[1:])
    refuse("no_required_tier", tuple(
        replace(row, tier=module.TOLERATED, divergence_metric="m", measured_at=module.SHADOW,
                d026_fixture="f", run_hash_member=True) for row in good))


if __name__ == "__main__":
    check_v1_content()
    check_version_pin()
    check_projection()
    check_blocked_evidence()
    check_well_formed_refusals()
    check_gate_agreement()
    check_manifest_for_run()
    check_mutants()
    print("CONTROL PARITY CHECKLIST CHECK: PASS")
