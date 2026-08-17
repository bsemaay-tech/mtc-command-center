# KICKOFF — RP6-P0.sh bounded fix round: add the getent resolution arm (round-1.4 C13)

You are GLM-5.2, acting as IMPLEMENTER for this bounded round (your own re-audit's
observation 2, Lead-adjudicated as a real conformance gap). Codex will audit your work in
a later round — implement only, then stop.

## The gap

Round-1.4 spec `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` section 8.1 rows
1–3 (repair C13) requires the P0 block to perform unique complete `getent` parsing:

- `gatea` must resolve to numeric euid/egid equal to the live `id -u`/`id -g` values and
  the preregistered expectations;
- `mtc-bridge` must still resolve to the preregistered `999:988` (uid/gid deliberately
  not equal);
- numeric `id -G` must exclude gids `0` and `988`;
- names are diagnostic only.

`RP6-P0.sh` (current accepted bytes SHA-256
`6c5b89456b4b4072969f7c928328d2d0ecb51e8476a15c5a7401f2988c9766f7`) compares live `id`
output against preregistered numerics but never calls `getent`, so the name→numeric
resolution premise is never confirmed live.

## Scope — exactly this, nothing else

Add one arm (one function + its calls + claim-line update) to `RP6-P0.sh`:

1. Resolve `getent passwd gatea` and `getent passwd mtc-bridge` with a pinned absolute
   `getent` (add it to the tool inventory the same way the block pins its other tools).
2. Parse under the passwd-grammar (Pattern 5 — full-record parse, reject duplicate or
   ambiguous entries; a valid no-match is a distinct outcome from a lookup error).
3. Adjudicate per the block's existing grammar and rc contract:
   - `getent` missing/unpinnable, lookup error, unparsable or duplicate record →
     `P0_STOP` rc 3 (inability to evaluate);
   - `gatea` resolves but numeric uid/gid differ from live `id -u`/`-g` or the
     preregistered expectations → `P0_STOP reason=identity_unexpected` rc 3 (per the F2
     polarity ruling);
   - `mtc-bridge` positively absent (valid getent no-match, rc 2) or resolves to numerics
     other than the preregistered `999:988` → `P0_STOP reason=state_account_resolution_unexpected` rc 3;
   - names never asserted, captured as diagnostic fields only.
4. New preregistered inputs: consume `P0_STATE_UID` (999) and `P0_STATE_GID` (988) via
   the same prelude-constant mechanism as the existing `P0_EXPECT_UID`, with the same
   rc-3 missing-input pre-check + `:?` backstop pattern the F4 repair established.
5. Update the block's `establishes` / `does_not_establish` / claim lines honestly.
6. Extend `SELF_QA_RP6.md` with a new section: RED/GREEN for the new arm (fixture `getent`
   shim on PATH is acceptable for QA — record it verbatim; the production block must
   still pin absolute `getent`). Run locally, real output only; `bash -n` PASS; record
   the new final SHA-256 + byte count.
7. Update `STATUS_RP6_P0.md`: note this round, status stays `REPAIRED-PENDING-AUDIT`
   (Codex audit outstanding).

Preserve: read-only scope, rc 0/1/3 contract, STOP-vs-FAIL truthfulness, all existing
arms untouched. Touch ONLY the three named files. Do not commit.
