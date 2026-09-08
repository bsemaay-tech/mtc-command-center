"""Control-parity checklist v1 -- the owner-gated versioned definition artifact.

Registered by the map-#67 kernel fold (`11_TRIAGE/WAYFINDER_KERNEL_FOLD_2026-08-23.md` §3)
and ratified by the owner through ticket #73. Its §4 table is reproduced here exactly, as
data rather than prose, because WP-P0-20's acceptance additions require that "the
control-parity checklist v1 exists and the migrated simulator implements its REQUIRED
tier".

Two rules from that fold are encoded, not merely quoted:

* "a REQUIRED control absent from a sim run => BLOCKED evidence" -- ``blocked_evidence``.
* "Every tolerated control: named metric + D026 fixture + ``evaluation_run_hash`` config
  membership" -- checked by ``assert_well_formed`` at import, so a tolerated row cannot be
  added without its governance attached.

And one property the fold states about the artifact itself rather than its contents: the
checklist is a **versioned definition whose changes are owner-gated**. A version pin makes
that mechanical. ``PINNED_DIGEST`` is taken over the rows, and ``assert_pinned`` refuses
when the table has been edited without moving the version -- so a silent amendment of an
owner-ratified table fails loudly instead of propagating into evidence.

The last sentence of §4 fixes this file's relationship to the manifest: "Tolerated
controls are exactly the checklist's projection of §9.1's ``UNSIMULATED_CONTROLS``
manifest -- the manifest names them, the checklist governs them." ``classifications``
performs that projection, so ``unsimulated_controls`` computes against the ratified
register instead of a local list.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

VERSION = "v1"
SOURCE = "11_TRIAGE/WAYFINDER_KERNEL_FOLD_2026-08-23.md §4 (owner-ratified via #73)"

REQUIRED = "REQUIRED"
TOLERATED = "TOLERATED"
TIERS = (REQUIRED, TOLERATED)

SHADOW = "SHADOW"
TESTNET = "TESTNET"
ENVIRONMENTS = (SHADOW, TESTNET)


class ChecklistRefused(ValueError):
    """The checklist is malformed, edited off-version, or used outside its terms."""


class BlockedEvidence(ValueError):
    """A REQUIRED control was absent from a simulation run."""


@dataclass(frozen=True)
class ControlRow:
    control: str
    tier: str
    divergence_metric: str = ""
    measured_at: str = ""
    d026_fixture: str = ""
    run_hash_member: bool = False


# §4 v1, row for row. REQUIRED rows carry no divergence metric by definition: they are not
# tolerated, so there is no tolerated divergence to measure.
CHECKLIST_V1 = (
    ControlRow("risk_allocator", REQUIRED),
    ControlRow("fees", REQUIRED),
    ControlRow("funding", REQUIRED),
    ControlRow("slippage", REQUIRED),
    ControlRow("protective_order_semantics", REQUIRED),
    ControlRow("guardian_authorize_reject", TOLERATED,
               divergence_metric="veto_rate", measured_at=SHADOW,
               d026_fixture="D026/guardian_veto_rate", run_hash_member=True),
    ControlRow("partial_fills", TOLERATED,
               divergence_metric="fill_shape_divergence", measured_at=TESTNET,
               d026_fixture="D026/partial_fill_shape", run_hash_member=True),
    ControlRow("snapshot_staleness", TOLERATED,
               divergence_metric="staleness_distribution", measured_at=SHADOW,
               d026_fixture="D026/snapshot_staleness", run_hash_member=True),
)

PINNED_DIGEST = "e4e4b3009e9b6716641a593b00de9fb7413eb9ad70c5b45308921160b3c12e2b"


def _canonical(rows=CHECKLIST_V1) -> str:
    return "\n".join(
        "|".join((row.control, row.tier, row.divergence_metric, row.measured_at,
                  row.d026_fixture, "1" if row.run_hash_member else "0"))
        for row in rows)


def digest(rows=CHECKLIST_V1) -> str:
    return hashlib.sha256(_canonical(rows).encode("utf-8")).hexdigest()


def assert_well_formed(rows=CHECKLIST_V1) -> None:
    """Every governance obligation the fold attaches to a row, enforced on the row."""
    seen = set()
    for row in rows:
        if not isinstance(row, ControlRow):
            raise ChecklistRefused("row")
        if not row.control or row.control != row.control.strip():
            raise ChecklistRefused("control")
        if row.control in seen:
            raise ChecklistRefused("duplicate_control")
        seen.add(row.control)
        if row.tier not in TIERS:
            raise ChecklistRefused("tier")
        if row.tier == TOLERATED:
            # The fold's obligation: metric + D026 fixture + run-hash membership.
            if not row.divergence_metric.strip():
                raise ChecklistRefused("tolerated_without_metric")
            if row.measured_at not in ENVIRONMENTS:
                raise ChecklistRefused("tolerated_without_environment")
            if not row.d026_fixture.strip():
                raise ChecklistRefused("tolerated_without_d026_fixture")
            if not row.run_hash_member:
                raise ChecklistRefused("tolerated_without_run_hash_membership")
        else:
            # A REQUIRED control is never "tolerated with a metric"; that would make the
            # tier meaningless and let a REQUIRED gap be measured instead of blocking.
            if row.divergence_metric or row.measured_at or row.d026_fixture:
                raise ChecklistRefused("required_with_tolerance")
    if not any(row.tier == REQUIRED for row in rows):
        raise ChecklistRefused("no_required_tier")


def assert_pinned(rows=CHECKLIST_V1, pinned=None) -> None:
    """Refuse a table edited without moving the version. Changes are owner-gated."""
    expected = PINNED_DIGEST if pinned is None else pinned
    actual = digest(rows)
    if expected != actual:
        raise ChecklistRefused(
            f"checklist_edited_off_version: {VERSION} pins {expected}, table hashes {actual}")


def controls(rows=CHECKLIST_V1) -> tuple:
    return tuple(row.control for row in rows)


def required_controls(rows=CHECKLIST_V1) -> tuple:
    return tuple(row.control for row in rows if row.tier == REQUIRED)


def tolerated_controls(rows=CHECKLIST_V1) -> tuple:
    return tuple(row.control for row in rows if row.tier == TOLERATED)


def classifications(rows=CHECKLIST_V1) -> dict:
    """Project the checklist onto the UNSIMULATED_CONTROLS vocabulary.

    The manifest names an unsimulated control; the checklist governs it. A REQUIRED row
    projects to REQUIRED so its appearance in the manifest blocks promotion; a tolerated
    row projects to INFORMATIONAL so its appearance is declared rather than blocking.
    """
    return {row.control: ("REQUIRED" if row.tier == REQUIRED else "INFORMATIONAL")
            for row in rows}


def blocked_evidence(simulated, rows=CHECKLIST_V1) -> None:
    """Raise when a REQUIRED control is absent from a simulation run.

    Returns ``None``: as with the allocator's caps and the promotion block, there is no
    return value a caller could read as a softened verdict.
    """
    assert_pinned(rows)
    if isinstance(simulated, (str, bytes)):
        raise ChecklistRefused("simulated")
    covered = set(simulated)
    unknown = covered - set(controls(rows))
    if unknown:
        # Claiming to simulate something the checklist does not govern means the run and
        # the checklist describe different systems.
        raise ChecklistRefused(f"simulated_not_in_checklist: {', '.join(sorted(unknown))}")
    missing = tuple(name for name in required_controls(rows) if name not in covered)
    if missing:
        raise BlockedEvidence(f"required_control_absent: {', '.join(missing)}")


def manifest_for_run(simulated, reasons, rows=CHECKLIST_V1):
    """Compute a run's UNSIMULATED_CONTROLS manifest against the ratified register.

    This is the single call site a simulation run should use: the enabled set and every
    classification come from the checklist, so a run cannot quietly compute its manifest
    against a locally invented control list. Importing here rather than at module scope
    keeps the checklist itself free of a dependency on the manifest module -- the checklist
    governs, the manifest names, and the direction of that relationship is deliberate.
    """
    from unsimulated_controls import compute_unsimulated_controls

    assert_pinned(rows)
    return compute_unsimulated_controls(
        enabled=controls(rows), classifications=classifications(rows),
        simulated=tuple(simulated), reasons=reasons)


assert_well_formed()
