"""Versioned research-side cost-model registry -- WP-P0-20's map-#79 amendment.

The plan (ticket #92, brief §10.4) gives this package "the versioned research-side
cost-model registry already required by §9.7: venue fees and funding provenance plus
normalized paper/testnet and later live fill-cost observations", adds that "a
recalibration creates new cost lineage and therefore a new ``deployment_identity_hash``;
it is event-driven, never silently calendar-driven", and closes with the acceptance
sentence this module exists to make true:

    Acceptance additionally proves that an unregistered or provenance-broken cost model
    cannot produce acceptance-bearing evidence.

The map-#67 fold fixes where each cost comes from: "fees from schedule, funding from
history, slippage from own fills". Those are provenance *kinds*, not numbers, so this
module holds no fee, no funding rate and no slippage figure. It holds the rule that each
must come from its own named source and refuses a model that fudges one.

Two prohibitions carry the weight:

* ``assert_acceptance_bearing`` refuses an unregistered or provenance-broken model. It
  returns ``None``; there is no value a caller can read as a qualified yes.
* ``recalibrate`` refuses without a named triggering event, and rotates both the cost
  lineage and the ``deployment_identity_hash``. A calendar tick is not an event, and a
  recalibration that kept its predecessor's identity would let new economics inherit old
  evidence.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, replace

VERSION = "v1"
SOURCE = ("plan WP-P0-20 map-#79 amendment (ticket #92, brief §10.4); provenance kinds "
          "from WAYFINDER_KERNEL_FOLD_2026-08-23.md §2 (#73)")

# Provenance kinds, one per cost component. Each names where the number must come from.
FROM_SCHEDULE = "FROM_SCHEDULE"          # fees
FROM_HISTORY = "FROM_HISTORY"            # funding
FROM_OWN_FILLS = "FROM_OWN_FILLS"        # slippage

# Observation lanes that feed the registry upward, with their owning packages.
PAPER = "INTERNAL_PAPER"                 # WP-V2B-07
TESTNET = "EXCHANGE_TESTNET"             # WP-V2B-07
LIVE = "LIVE"                            # WP-V3-05
OBSERVATION_SOURCES = (PAPER, TESTNET, LIVE)


class CostModelRefused(ValueError):
    """A model is malformed, provenance-broken, or recalibrated without an event."""


class NotAcceptanceBearing(ValueError):
    """An unregistered or provenance-broken cost model was offered as evidence."""


@dataclass(frozen=True)
class CostModel:
    model_id: str
    version: str
    fees_provenance: str
    funding_provenance: str
    slippage_provenance: str
    observation_sources: tuple
    cost_lineage_id: str
    deployment_identity_hash: str
    triggering_event: str


def _require_text(name, value):
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise CostModelRefused(name)


def assert_well_formed(model: CostModel) -> None:
    """Each cost component must come from its own named source. No substitutions."""
    if not isinstance(model, CostModel):
        raise CostModelRefused("model")
    for name in ("model_id", "version", "cost_lineage_id", "deployment_identity_hash",
                 "triggering_event"):
        _require_text(name, getattr(model, name))
    if model.fees_provenance != FROM_SCHEDULE:
        raise CostModelRefused("fees_provenance")
    if model.funding_provenance != FROM_HISTORY:
        raise CostModelRefused("funding_provenance")
    if model.slippage_provenance != FROM_OWN_FILLS:
        raise CostModelRefused("slippage_provenance")
    if isinstance(model.observation_sources, (str, bytes)):
        raise CostModelRefused("observation_sources")
    sources = tuple(model.observation_sources)
    if len(set(sources)) != len(sources):
        raise CostModelRefused("duplicate_observation_source")
    for source in sources:
        if source not in OBSERVATION_SOURCES:
            raise CostModelRefused(f"unknown_observation_source: {source}")


def register(registry: dict, model: CostModel) -> dict:
    """Return a registry with the model added. A broken model never enters."""
    assert_well_formed(model)
    if model.model_id in registry:
        raise CostModelRefused(f"already_registered: {model.model_id}")
    updated = dict(registry)
    updated[model.model_id] = model
    return updated


def assert_acceptance_bearing(model_id: str, registry: dict) -> None:
    """Raise unless this exact model is registered and its provenance is intact.

    Returns ``None``. The acceptance sentence is a prohibition, so the function has no
    value a caller could read as a qualified yes.
    """
    _require_text("model_id", model_id)
    model = (registry or {}).get(model_id)
    if model is None:
        raise NotAcceptanceBearing(f"unregistered_cost_model: {model_id}")
    try:
        assert_well_formed(model)
    except CostModelRefused as error:
        raise NotAcceptanceBearing(f"provenance_broken: {model_id} ({error})") from error


def _derive(previous: str, event: str, version: str) -> str:
    return hashlib.sha256(f"{previous}|{event}|{version}".encode("utf-8")).hexdigest()[:32]


def recalibrate(model: CostModel, *, event: str, version: str) -> CostModel:
    """Event-driven recalibration: new cost lineage, new deployment identity.

    A recalibration with no named event is refused. The plan says event-driven, "never
    silently calendar-driven", so a bare date is not an event and is rejected as one.
    """
    assert_well_formed(model)
    _require_text("event", event)
    _require_text("version", version)
    if version == model.version:
        raise CostModelRefused("version_not_moved")
    stripped = event.strip()
    # A bare timestamp or "scheduled"/"periodic" marker is a calendar tick, not an event.
    calendar_only = (stripped.replace("-", "").replace(":", "").replace("T", "")
                     .replace(" ", "").replace("Z", "").isdigit())
    if calendar_only or stripped.lower() in ("scheduled", "periodic", "routine", "monthly",
                                             "weekly", "daily", "calendar"):
        raise CostModelRefused(f"calendar_driven_recalibration: {stripped}")
    lineage = _derive(model.cost_lineage_id, stripped, version)
    identity = _derive(model.deployment_identity_hash, stripped, version)
    recalibrated = replace(model, version=version, cost_lineage_id=lineage,
                           deployment_identity_hash=identity, triggering_event=stripped)
    # New economics must never inherit the old identity, or old evidence vouches for them.
    if recalibrated.cost_lineage_id == model.cost_lineage_id:
        raise CostModelRefused("cost_lineage_not_rotated")
    if recalibrated.deployment_identity_hash == model.deployment_identity_hash:
        raise CostModelRefused("deployment_identity_not_rotated")
    assert_well_formed(recalibrated)
    return recalibrated
