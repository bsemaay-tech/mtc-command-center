"""WP-P0-20 acceptance-state harness -- the prose gate, probed.

The package's acceptance gate is several paragraphs of contract spread across the plan's
WP-P0-20 section and two fold amendments. Prose cannot be run, so a reader has to hold the
whole gate in their head to answer "is this acceptable yet?", and the honest answer drifts.
This harness states each criterion once, quotes the contract clause it comes from, and
attaches a probe that **executes** rather than asserts.

Two properties make it worth trusting:

* A criterion cannot be MET without a probe. ``Criterion`` requires one, and a probe that
  returns anything other than a ``(state, detail)`` pair is a harness error, not a pass.
* The harness never reports the package acceptable while any criterion is unmet, and exits
  non-zero unless every one is MET. Acceptance cannot be reached by omission, and neither
  can it be reached by this tool: a full sweep of MET rows still requires exact audits and
  independent Lead acceptance, which are themselves rows here and are not self-certifiable.

Run it to see where the package actually stands.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

MET = "MET"
UNMET = "UNMET"
BLOCKED = "BLOCKED"
STATES = (MET, UNMET, BLOCKED)


class HarnessError(RuntimeError):
    """The harness itself is misused; never reported as an acceptance result."""


@dataclass(frozen=True)
class Criterion:
    key: str
    clause: str
    probe: object


def _pair(key, result):
    if not isinstance(result, tuple) or len(result) != 2:
        raise HarnessError(f"probe for {key} did not return (state, detail)")
    state, detail = result
    if state not in STATES:
        raise HarnessError(f"probe for {key} returned unknown state {state!r}")
    if not isinstance(detail, str) or not detail.strip():
        raise HarnessError(f"probe for {key} returned no detail")
    return state, detail.strip()


# --- probes ----------------------------------------------------------------------------

def probe_checklist_v1():
    import control_parity_checklist as checklist
    checklist.assert_pinned()
    checklist.assert_well_formed()
    return MET, (f"v1 pinned, {len(checklist.CHECKLIST_V1)} rows, "
                 f"{len(checklist.required_controls())} REQUIRED")


def probe_battery_v1():
    import statistical_battery as battery
    battery.assert_pinned()
    return MET, f"v1 pinned, {len(battery.ELEMENTS)} elements, DSR >= {battery.DSR_MINIMUM}"


def probe_promotion_block():
    """Run the D026 fixture live rather than citing it."""
    import inspect
    import unsimulated_controls as manifest
    import control_parity_checklist as checklist
    reasons = {name: f"not simulated ({name})" for name in checklist.controls()}
    computed = checklist.manifest_for_run(
        tuple(n for n in checklist.controls() if n != "fees"), reasons)
    namespace = dict(manifest.__dict__)
    exec(inspect.getsource(manifest.promotion_block).replace("if blocking:", "if False:", 1),
         namespace)
    try:
        namespace["promotion_block"](computed)
    except manifest.PromotionBlocked:
        return UNMET, "gate-removed mutant blocked; the D026 fixture proves nothing"
    try:
        manifest.promotion_block(computed)
    except manifest.PromotionBlocked as error:
        return MET, f"RED without the gate, GREEN with it ({error})"
    return UNMET, "a REQUIRED unsimulated control promoted"


def probe_uncomputed_manifest():
    import unsimulated_controls as manifest
    empty = manifest.UnsimulatedControls(entries=(), enabled=(), simulated=(),
                                         classifications=())
    try:
        manifest.promotion_block(empty)
    except manifest.PromotionBlocked as error:
        return MET, f"an uncomputed empty manifest is refused ({error})"
    return UNMET, "an uncomputed empty manifest promoted"


def probe_cost_model():
    import cost_model_registry as registry
    try:
        registry.assert_acceptance_bearing("never-registered", {})
    except registry.NotAcceptanceBearing:
        return MET, "an unregistered cost model cannot produce acceptance-bearing evidence"
    return UNMET, "an unregistered cost model was accepted"


def probe_import_identity():
    import check_allocator_import_identity as identity
    status = identity.static_status(identity.CANONICAL_PATH)
    if status == identity.BOUND_IDENTICAL:
        return MET, "the canonical path imports the delivered allocator"
    return BLOCKED, (f"{status}: simulate_slice has no sizing stage (percent returns, flat "
                     "COST_BPS); binding it is the migration, which needs the WP-P0-12 kernel")


def probe_kernel_present():
    """A mention of the kernel is not the kernel.

    This asks the AST for real imports rather than searching the text, because a comment, a
    docstring or a TODO naming CORRECTED_VNEXT would satisfy a substring search -- and a
    harness whose purpose is to resist inflation must not be the easiest thing in the
    repository to fool. When WP-P0-12 lands, confirm the module name below against what it
    actually delivers; a wrong name here reads as absence, which is the safe direction.
    """
    import ast
    import check_allocator_import_identity as identity
    source = identity.CANONICAL_PATH.read_text(encoding="utf-8")
    imported = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    kernel = tuple(name for name in sorted(imported)
                   if "kernel" in name.lower() or name.split(".")[0] == "mtc_v2")
    if kernel:
        return MET, f"the canonical path imports the kernel: {', '.join(kernel)}"
    if "CORRECTED_VNEXT" in source:
        return UNMET, ("CORRECTED_VNEXT appears in the canonical path as text only; no "
                       "kernel module is imported")
    return BLOCKED, ("WP-P0-12 CORRECTED_VNEXT is not in this repository; its Item-2 packet "
                     "is on the Windows host. The STOP is lifted (OD-20260907-1) but the "
                     "work has not been imported")


def probe_required_tier_implemented():
    state, detail = probe_import_identity()
    if state != MET:
        return BLOCKED, ("the migrated simulator cannot implement the checklist's REQUIRED "
                         "tier while no migration exists: " + detail)
    return UNMET, "migration present; REQUIRED-tier coverage not yet measured"


def probe_standin_prohibition():
    """A stand-in must fail the gate, and no stamp may convert it."""
    import evidence_class as evidence
    import cost_model_registry as costs
    model = costs.CostModel(
        model_id="probe-model", version="1.0.0", fees_provenance=costs.FROM_SCHEDULE,
        funding_provenance=costs.FROM_HISTORY, slippage_provenance=costs.FROM_OWN_FILLS,
        observation_sources=(costs.PAPER,), cost_lineage_id="l", deployment_identity_hash="d",
        triggering_event="probe")
    registry = costs.register({}, model)
    standin = evidence.RunFacts(
        canonical_simulator=True, allocator_import_identity_proven=False,
        kernel_version="CORRECTED_VNEXT-1.0.0", cost_model_id="probe-model",
        manifest_computed=True, manifest_has_required_gap=False)
    evidence_class, _ = evidence.classify(standin, cost_registry=registry)
    if evidence_class != evidence.SIGNAL_SCREEN_ONLY:
        return UNMET, f"a stand-in run classified {evidence_class}"
    try:
        evidence.assert_acceptance_bearing(standin, cost_registry=registry)
    except evidence.NotAcceptanceBearing:
        pass
    else:
        return UNMET, "a stand-in run was accepted as evidence"
    # The withdrawn accepting state must be refused rather than ignored.
    import dataclasses
    stamped = dataclasses.replace(standin, legacy_state_stamp="ALLOCATOR_NOT_YET_SHARED")
    try:
        evidence.classify(stamped, cost_registry=registry)
    except evidence.EvidenceRefused:
        return MET, ("a stand-in run is SIGNAL_SCREEN_ONLY and non-accepting; "
                     "ALLOCATOR_NOT_YET_SHARED is refused, and the gate signature offers "
                     "no conversion parameter")
    return UNMET, "ALLOCATOR_NOT_YET_SHARED was not refused"


def _record(*candidates):
    for candidate in candidates:
        path = Path(candidate)
        if path.exists() and path.stat().st_size > 0:
            return path
    return None


def probe_before_after():
    found = _record("MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_20_BEFORE_AFTER_COMPARISON.md")
    if found:
        return MET, f"comparison recorded at {found}"
    return BLOCKED, ("no before/after comparison on a real frozen candidate; it requires a "
                     "migrated run, so it waits on the migration")


def probe_dependent_disposition():
    """A record that exists is not a record that is finished.

    The gate wants what each tool *was* -- past tense, a migration output. A record
    declaring its dispositions PROPOSED is real work and still not that, so the probe reads
    the record's own status line rather than treating the file's existence as a pass.
    """
    found = _record("MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md")
    if not found:
        return UNMET, ("no per-class disposition record for the four dependent-tool classes "
                       "(direct callers, independent simulators, patcher, reporting consumer)")
    text = found.read_text(encoding="utf-8")
    if "Status: PROPOSED, not PERFORMED" in text:
        return UNMET, (f"{found}: all four classes located and verified against source, "
                       "dispositions proposed with evidence -- but proposed, not performed; "
                       "performing them needs the migration")
    if "PERFORMED" not in text:
        return UNMET, f"{found}: record does not state whether its dispositions were performed"
    return MET, f"dispositions performed and recorded at {found}"


def probe_throughput():
    found = _record("MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_20_THROUGHPUT_MEASUREMENT.md")
    if found:
        return MET, f"measurement recorded at {found}"
    return BLOCKED, ("no measured full-kernel trials-per-hour on named reference hardware, "
                     "no O-28-scale extrapolation, no feasible/infeasible statement; all "
                     "require the migrated kernel path")


def probe_audits():
    return UNMET, ("exact audits and independent Lead acceptance are not self-certifiable "
                   "and none is claimed; the container cannot reach the exact audit models")


CRITERIA = (
    Criterion("checklist_v1_exists",
              "acceptance addition (a): the control-parity checklist v1 exists",
              probe_checklist_v1),
    Criterion("battery_v1_exists",
              "acceptance addition (b): the statistical-battery definition v1 exists",
              probe_battery_v1),
    Criterion("promotion_block_d026",
              "a REQUIRED control in the manifest blocks promotion, proven by a D026 "
              "fixture that is RED without the gate and GREEN with it",
              probe_promotion_block),
    Criterion("computed_manifest",
              "an empty UNSIMULATED_CONTROLS manifest that was not computed fails acceptance",
              probe_uncomputed_manifest),
    Criterion("cost_model_provenance",
              "an unregistered or provenance-broken cost model cannot produce "
              "acceptance-bearing evidence",
              probe_cost_model),
    Criterion("standin_prohibition",
              "a stand-in allocator cannot satisfy this gate at all -- a run against a "
              "stand-in is SIGNAL_SCREEN_ONLY and non-accepting, and there is no manifest "
              "stamp that converts it",
              probe_standin_prohibition),
    Criterion("import_identity",
              "the canonical path is shown to import and run the one shared Risk Allocator "
              "implementation delivered here -- proven by import, not asserted",
              probe_import_identity),
    Criterion("kernel_present",
              "... together with the kernel (WP-P0-12 CORRECTED_VNEXT)",
              probe_kernel_present),
    Criterion("required_tier_implemented",
              "acceptance addition (a): the migrated simulator implements the checklist's "
              "REQUIRED tier",
              probe_required_tier_implemented),
    Criterion("before_after",
              "a before/after comparison on at least one real frozen candidate, showing "
              "where the economics changed and why",
              probe_before_after),
    Criterion("dependent_disposition",
              "a migration record naming, per dependent tool and per class, whether it was "
              "re-based, retired, patched, updated as reporting, or left on the legacy path",
              probe_dependent_disposition),
    Criterion("throughput",
              "a measured full-kernel trials-per-hour figure on named reference hardware, "
              "the O-28-scale extrapolation, and an explicit feasible/infeasible statement",
              probe_throughput),
    Criterion("audits",
              "exact audits, mandatory Gemini corroboration and independent Lead acceptance",
              probe_audits),
)


def evaluate():
    rows = []
    for criterion in CRITERIA:
        if criterion.probe is None:
            raise HarnessError(f"{criterion.key} has no probe")
        rows.append((criterion, *_pair(criterion.key, criterion.probe())))
    return rows


def main(argv=None) -> int:
    rows = evaluate()
    width = max(len(c.key) for c, _, _ in rows)
    for criterion, state, detail in rows:
        print(f"{criterion.key:<{width}}  {state:<7}  {detail}")
    met = sum(1 for _, state, _ in rows if state == MET)
    print()
    print(f"WP-P0-20 ACCEPTANCE: {met}/{len(rows)} criteria MET")
    if met != len(rows):
        outstanding = [c.key for c, state, _ in rows if state != MET]
        print("NOT ACCEPTABLE -- outstanding: " + ", ".join(outstanding))
        return 1
    print("Every mechanical criterion is MET. Acceptance is still a Lead act, not this "
          "tool's verdict.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
