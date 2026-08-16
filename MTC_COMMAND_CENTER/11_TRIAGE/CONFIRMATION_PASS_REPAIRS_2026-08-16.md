# Confirmation-pass repairs + RED/GREEN evidence — 2026-08-16

Executed by the Lead under `OWNER_DECISION_CONFIRMATION_PASS_2026-08-16.md`.
Candidate `acdf4e37`, payload, launcher v4, and all Bridge code UNCHANGED.

## Repair 1 — one authoritative sentence

Plan V6 §3 now carries the single signable sentence: complete admitted-object
list (incl. `/home/baris/payload-acdf4e37`, the state archive + `.sha256`, and
the two named operator-side encrypted directories), the full unshortened annex
hash, and the D3 subordination. The annex's former draft copy is explicitly
subordinated ("NOT FOR SIGNATURE", pointing to Plan V6 §3).

## Repair 2 — failed-attempt cleanup unit guard

Annex removal block: `systemctl stop/mask` now runs only if
`systemctl cat mtc-bridge-first-start.service` proves the unit exists; a
missing unit prints a NOTE and removal continues; an existing unit whose stop
genuinely fails still aborts under `set -Eeuo pipefail` (fail-closed kept).

## Focused RED/GREEN (stubbed systemctl, no host contact) — real output

```text
== OLD-RED: old block, unit missing (must NOT reach removal) ==
rc=5
== NEW-G1: repaired block, unit missing (must reach removal) ==
NOTE: unit not installed; skipping stop/mask, continuing removal
REMOVAL_REACHED
rc=0
== NEW-G2: repaired block, unit present, stop fails rc=1 (must abort, no removal) ==
rc=1
== NEW-G3 control: repaired block, unit present, stop ok (must reach removal) ==
REMOVAL_REACHED
rc=0
```

## Final pins after these repairs

- Annex: 31980 B, sha256
  `5a3f92e68514681dd94a913bc00a7f6964ab8efa98a6904be8c507f738761d7a`
- Plan V6: re-pinned at commit time (recorded in the confirmation kickoff).
- Candidate `acdf4e379fb60ee319854acae19fd3eaf7db71a2`, payload manifest
  `e74c59fe…`, launcher v4 `ac68196b…`: all unchanged.
