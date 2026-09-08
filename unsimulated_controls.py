"""Computed UNSIMULATED_CONTROLS manifest and the promotion block it feeds.

WP-P0-20 requires "a **computed** `UNSIMULATED_CONTROLS` manifest per run, with a reason
per entry", a REQUIRED/INFORMATIONAL classification per control carried in the frozen
package, and a promotion block in which "a `REQUIRED` control appearing in the manifest
prevents promotion". Its acceptance gate adds the sentence this module is shaped around:
**"An empty `UNSIMULATED_CONTROLS` manifest that was not computed fails acceptance."**

That sentence rules out trusting a manifest. An authored empty manifest and a computed
empty one are byte-identical if the manifest records only its conclusion, so this module
records the manifest's *inputs* -- the enabled control set, the classification of each,
and the set the simulator actually simulates -- and ``promotion_block`` re-derives the
entries from them. A manifest whose entries do not equal ``enabled - simulated`` is
refused, whatever it claims. Verification is re-derivation, never a stamp.

No I/O, no engine import. Binding this to the canonical path is WP-P0-20's third
outstanding item and depends on WP-P0-12, which is stopped.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

REQUIRED = "REQUIRED"
INFORMATIONAL = "INFORMATIONAL"
CLASSIFICATIONS = (REQUIRED, INFORMATIONAL)


class ManifestRefused(ValueError):
    """A named refusal; the manifest is never guessed into existence."""


class PromotionBlocked(ValueError):
    """A REQUIRED control was not simulated, or the manifest was not computed."""


@dataclass(frozen=True)
class ControlEntry:
    control: str
    classification: str
    reason: str


@dataclass(frozen=True)
class UnsimulatedControls:
    """A manifest that carries its own inputs so it can be re-derived, not believed."""
    entries: tuple
    enabled: tuple
    simulated: tuple
    classifications: tuple


def _names(label, values):
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise ManifestRefused(label)
    names = tuple(values)
    for name in names:
        if not isinstance(name, str) or not name or name != name.strip():
            raise ManifestRefused(label)
    if len(set(names)) != len(names):
        raise ManifestRefused(f"{label}_duplicate")
    return names


def compute_unsimulated_controls(
    *, enabled: Sequence, classifications: Mapping, simulated: Sequence,
    reasons: Mapping,
) -> UnsimulatedControls:
    """Derive the manifest: every enabled control the simulator does not simulate.

    ``enabled`` and ``classifications`` come from the frozen package; ``simulated`` is
    what the simulation code actually covers; ``reasons`` explains each gap. Every
    refusal below is a case where a silent empty manifest would otherwise be produced.
    """
    enabled_names = _names("enabled", enabled)
    simulated_names = _names("simulated", simulated)
    if not enabled_names:
        # A run with no enabled controls is not a run; it is an uncomputed manifest.
        raise ManifestRefused("enabled_empty")
    if not isinstance(classifications, Mapping) or not isinstance(reasons, Mapping):
        raise ManifestRefused("mapping")
    unknown = tuple(name for name in simulated_names if name not in enabled_names)
    if unknown:
        # Simulating something the frozen package never enabled means the two sets
        # describe different runs, so the difference between them is meaningless.
        raise ManifestRefused("simulated_not_enabled")
    entries = []
    for name in enabled_names:
        classification = classifications.get(name)
        if classification not in CLASSIFICATIONS:
            # Unclassified means nothing can say whether its absence blocks promotion.
            raise ManifestRefused("classification")
        if name in simulated_names:
            continue
        reason = reasons.get(name)
        if not isinstance(reason, str) or not reason.strip():
            raise ManifestRefused("reason")
        entries.append(ControlEntry(name, classification, reason.strip()))
    return UnsimulatedControls(
        entries=tuple(entries), enabled=enabled_names, simulated=simulated_names,
        classifications=tuple(sorted((name, classifications[name]) for name in enabled_names)),
    )


def promotion_block(manifest: UnsimulatedControls) -> None:
    """Raise unless the manifest was computed and holds no REQUIRED entry.

    Returns ``None``. As with the allocator's caps, there is no return value a caller
    could read as a softened verdict.
    """
    if not isinstance(manifest, UnsimulatedControls):
        raise PromotionBlocked("manifest")
    enabled = _names("enabled", manifest.enabled)
    simulated = _names("simulated", manifest.simulated)
    if not enabled:
        raise PromotionBlocked("not_computed")
    classifications = dict(manifest.classifications)
    if tuple(sorted(classifications)) != tuple(sorted(enabled)):
        raise PromotionBlocked("not_computed")
    # Re-derive rather than trust: the entries must be exactly enabled - simulated.
    expected = tuple(name for name in enabled if name not in simulated)
    actual = tuple(entry.control for entry in manifest.entries)
    if actual != expected:
        raise PromotionBlocked("not_computed")
    for entry in manifest.entries:
        if classifications.get(entry.control) != entry.classification:
            raise PromotionBlocked("not_computed")
        if not isinstance(entry.reason, str) or not entry.reason.strip():
            raise PromotionBlocked("not_computed")
    blocking = tuple(entry.control for entry in manifest.entries
                     if entry.classification == REQUIRED)
    if blocking:
        raise PromotionBlocked(f"required_control_unsimulated: {', '.join(blocking)}")
