"""Evidence class of a research run -- derived from facts, never declared by its producer.

WP-P0-20 states the two-tier funnel as its operating model: "cheap vectorized screening
remains fully legal, labeled ``SIGNAL_SCREEN_ONLY``, and its numbers are **never**
acceptance-bearing evidence; survivors run the full kernel + shared allocator, and **only
those trials produce promotion-deciding evidence**". Its gate then closes the loophole
that made the earlier arrangement fail:

    A stand-in allocator cannot satisfy this gate at all -- a run against a stand-in is
    ``SIGNAL_SCREEN_ONLY`` and non-accepting, and **there is no manifest stamp that
    converts it**.

The R1 correction pass records why this module exists at all: "A stamped stand-in still
passed this package's gate and let WP-P0-13, WP-P0-14 and everything downstream proceed as
though the shared allocator existed -- so R4 was not closed." The defect was not a missing
check. It was that the class was a **label the run carried** rather than a **conclusion
drawn from what the run did**.

So there is deliberately no way to assert a class here. ``classify`` takes facts and
returns a verdict; nothing accepts a class as input, and ``ALLOCATOR_NOT_YET_SHARED`` --
withdrawn as an accepting manifest state -- is refused on sight rather than merely
ignored, so an old artifact carrying it fails loudly instead of being read as unlabelled.
"""
from __future__ import annotations

from dataclasses import dataclass

SIGNAL_SCREEN_ONLY = "SIGNAL_SCREEN_ONLY"
ACCEPTANCE_BEARING = "ACCEPTANCE_BEARING"

# Withdrawn by the R1 correction pass. Present here only to be refused.
WITHDRAWN_STATES = ("ALLOCATOR_NOT_YET_SHARED",)


class EvidenceRefused(ValueError):
    """A run was misdescribed, or a withdrawn state was offered."""


class NotAcceptanceBearing(ValueError):
    """A screening run was offered as promotion-deciding evidence."""


@dataclass(frozen=True)
class RunFacts:
    """What a run *did*. Every field is an observation, none is a verdict."""
    canonical_simulator: bool
    allocator_import_identity_proven: bool
    kernel_version: str
    cost_model_id: str
    manifest_computed: bool
    manifest_has_required_gap: bool
    legacy_state_stamp: str = ""


def _require_bool(name, value):
    if not isinstance(value, bool):
        raise EvidenceRefused(name)


def classify(facts: RunFacts, *, cost_registry: dict = None) -> tuple:
    """Return ``(evidence_class, reasons)``. Reasons are why it is not acceptance-bearing.

    A run is acceptance-bearing only when every fact supports it. Any single missing fact
    makes it screening -- there is no partial credit, because a promotion number is not
    partially meaningful.
    """
    if not isinstance(facts, RunFacts):
        raise EvidenceRefused("facts")
    if facts.legacy_state_stamp:
        if facts.legacy_state_stamp in WITHDRAWN_STATES:
            raise EvidenceRefused(f"withdrawn_state: {facts.legacy_state_stamp}")
        raise EvidenceRefused(f"unknown_state_stamp: {facts.legacy_state_stamp}")
    for name in ("canonical_simulator", "allocator_import_identity_proven",
                 "manifest_computed", "manifest_has_required_gap"):
        _require_bool(name, getattr(facts, name))

    reasons = []
    if not facts.canonical_simulator:
        reasons.append("not the canonical simulator: an independent simulator defines its "
                       "own economics and inherits none")
    if not facts.allocator_import_identity_proven:
        reasons.append("shared-allocator import identity not proven: a stand-in or a "
                       "same-named copy cannot satisfy the gate")
    if not isinstance(facts.kernel_version, str) or not facts.kernel_version.strip():
        reasons.append("no kernel version recorded: the run did not name the kernel it ran")
    if not facts.manifest_computed:
        reasons.append("UNSIMULATED_CONTROLS manifest not computed")
    if facts.manifest_has_required_gap:
        reasons.append("a REQUIRED control is unsimulated")

    model_id = facts.cost_model_id
    if not isinstance(model_id, str) or not model_id.strip():
        reasons.append("no cost model named")
    else:
        from cost_model_registry import NotAcceptanceBearing as CostNotBearing
        from cost_model_registry import assert_acceptance_bearing as cost_gate
        try:
            cost_gate(model_id, cost_registry or {})
        except CostNotBearing as error:
            reasons.append(f"cost model not acceptance-bearing: {error}")

    if reasons:
        return SIGNAL_SCREEN_ONLY, tuple(reasons)
    return ACCEPTANCE_BEARING, ()


def assert_acceptance_bearing(facts: RunFacts, *, cost_registry: dict = None) -> None:
    """Raise unless the run's own facts make it acceptance-bearing.

    Returns ``None``, and takes no stamp, label, override or reason argument. There is
    deliberately no parameter through which a caller could convert a screening run: the
    gate's sentence is that no such conversion exists, so the signature is the enforcement.
    """
    evidence_class, reasons = classify(facts, cost_registry=cost_registry)
    if evidence_class != ACCEPTANCE_BEARING:
        raise NotAcceptanceBearing(f"{evidence_class}: " + "; ".join(reasons))
