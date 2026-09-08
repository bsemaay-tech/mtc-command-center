"""Statistical-battery definition v1 -- the owner-gated versioned definition artifact.

Registered by the map-#67 kernel fold (`11_TRIAGE/WAYFINDER_KERNEL_FOLD_2026-08-23.md` §3)
and ratified by the owner through ticket #75. §6 states it in one paragraph:

    Elements (all seven, none skippable; skipped => BLOCKED): walk-forward · lockbox ·
    CPCV · PBO · DSR >= 0.95 · BH-FDR · sensitivity. Verdicts bind to
    `evaluation_run_hash` + battery version. CPCV/PBO run inline in the canonical pipeline
    from the port harvest onward. Lockbox: eras per registered dataset version; opening
    automatic on earned mechanical criteria, always a lifecycle-ledger record; an opened
    era is SPENT for that family (later results navigational).

Three of those clauses are prohibitions, and prohibitions are the ones worth mechanising:

* **None skippable.** ``evaluate`` refuses a result set that omits an element and refuses
  one that reports an element as ``SKIPPED``. A battery is not a menu.
* **Verdicts bind.** A ``BatteryVerdict`` carries the ``evaluation_run_hash`` and the
  battery version it was earned under, and ``assert_binding`` refuses to read it against
  any other. Without that a PASS earned on one run silently vouches for another.
* **An opened era is SPENT.** A lockbox element citing an era already spent by that family
  is refused, because a re-read of a spent era is navigational and never evidence.

``DSR >= 0.95`` is the owner's ratified number, reproduced, not chosen here. The
comparison is inclusive: 0.95 exactly is a pass, as ">=" says.

This module defines and judges. It runs nothing: producing the element results is the
canonical pipeline's job, and the lockbox's lifecycle-ledger record belongs to WP-P0-31.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from decimal import Decimal
from typing import Mapping, Sequence

VERSION = "v1"
SOURCE = "11_TRIAGE/WAYFINDER_KERNEL_FOLD_2026-08-23.md §6 (owner-ratified via #75)"

PASS = "PASS"
FAIL = "FAIL"
SKIPPED = "SKIPPED"
STATUSES = (PASS, FAIL, SKIPPED)

BLOCKED = "BLOCKED"

WALK_FORWARD = "walk_forward"
LOCKBOX = "lockbox"
CPCV = "cpcv"
PBO = "pbo"
DSR = "dsr"
BH_FDR = "bh_fdr"
SENSITIVITY = "sensitivity"

# All seven, in the order §6 names them. None is optional.
ELEMENTS = (WALK_FORWARD, LOCKBOX, CPCV, PBO, DSR, BH_FDR, SENSITIVITY)

# The owner's ratified threshold, reproduced from §6.
DSR_MINIMUM = Decimal("0.95")

# Elements the fold requires to run inline in the canonical pipeline from the port
# harvest onward; the offline validation stage does not survive that harvest.
INLINE_FROM_PORT_HARVEST = (CPCV, PBO)

PINNED_DIGEST = "e906101bdfb7faa382951d83b663dba0b1486f36a4fd7c4eb9bbb3d6e625da6e"


class BatteryRefused(ValueError):
    """The battery was misused: malformed input, off-version table, or broken binding."""


@dataclass(frozen=True)
class ElementResult:
    element: str
    status: str
    value: Decimal = None
    era: str = ""


@dataclass(frozen=True)
class BatteryVerdict:
    verdict: str
    evaluation_run_hash: str
    battery_version: str
    failing: tuple = ()


def _canonical() -> str:
    return "|".join(ELEMENTS) + f"|DSR>={DSR_MINIMUM}|inline:{','.join(INLINE_FROM_PORT_HARVEST)}"


def digest() -> str:
    return hashlib.sha256(_canonical().encode("utf-8")).hexdigest()


def assert_pinned(pinned=None) -> None:
    """Refuse a definition edited without moving the version. Changes are owner-gated."""
    expected = PINNED_DIGEST if pinned is None else pinned
    actual = digest()
    if expected != actual:
        raise BatteryRefused(
            f"battery_edited_off_version: {VERSION} pins {expected}, definition hashes {actual}")


def _require_hash(name, value):
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise BatteryRefused(name)


def evaluate(results: Sequence, *, evaluation_run_hash: str,
             spent_eras: Mapping = None) -> BatteryVerdict:
    """Judge one run's element results against the ratified battery.

    Returns a verdict bound to ``evaluation_run_hash`` and this battery version. A missing
    or skipped element is ``BLOCKED``, never a partial pass.
    """
    assert_pinned()
    _require_hash("evaluation_run_hash", evaluation_run_hash)
    if isinstance(results, (str, bytes)) or not isinstance(results, Sequence):
        raise BatteryRefused("results")
    seen = {}
    for result in results:
        if not isinstance(result, ElementResult):
            raise BatteryRefused("result")
        if result.element not in ELEMENTS:
            raise BatteryRefused(f"unknown_element: {result.element}")
        if result.element in seen:
            raise BatteryRefused(f"duplicate_element: {result.element}")
        if result.status not in STATUSES:
            raise BatteryRefused(f"status: {result.element}")
        seen[result.element] = result

    missing = tuple(name for name in ELEMENTS if name not in seen)
    if missing:
        # An absent element is indistinguishable from an unrun one, so it blocks.
        return BatteryVerdict(BLOCKED, evaluation_run_hash, VERSION, missing)
    skipped = tuple(name for name in ELEMENTS if seen[name].status == SKIPPED)
    if skipped:
        return BatteryVerdict(BLOCKED, evaluation_run_hash, VERSION, skipped)

    # The lockbox's spent-era rule: a re-read of a spent era is navigational, not evidence.
    lockbox = seen[LOCKBOX]
    if not lockbox.era.strip():
        raise BatteryRefused("lockbox_era")
    for family, eras in (spent_eras or {}).items():
        if lockbox.era in tuple(eras):
            raise BatteryRefused(f"lockbox_era_spent: {lockbox.era} ({family})")

    dsr = seen[DSR]
    if not isinstance(dsr.value, Decimal) or not dsr.value.is_finite():
        raise BatteryRefused("dsr_value")

    failing = tuple(name for name in ELEMENTS if seen[name].status == FAIL)
    if dsr.value < DSR_MINIMUM and DSR not in failing:
        failing = failing + (DSR,)
    if failing:
        return BatteryVerdict(FAIL, evaluation_run_hash, VERSION, failing)
    return BatteryVerdict(PASS, evaluation_run_hash, VERSION)


def assert_binding(verdict: BatteryVerdict, *, evaluation_run_hash: str,
                   battery_version: str = VERSION) -> None:
    """Refuse to read a verdict against a run or a battery version it was not earned under."""
    if not isinstance(verdict, BatteryVerdict):
        raise BatteryRefused("verdict")
    _require_hash("evaluation_run_hash", evaluation_run_hash)
    if verdict.evaluation_run_hash != evaluation_run_hash:
        raise BatteryRefused("verdict_run_hash_mismatch")
    if verdict.battery_version != battery_version:
        raise BatteryRefused("verdict_battery_version_mismatch")
