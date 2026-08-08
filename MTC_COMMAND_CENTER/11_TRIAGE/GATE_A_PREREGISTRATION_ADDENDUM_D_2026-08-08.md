# GATE A — PRE-REGISTRATION ADDENDUM D: re-baseline to `2ce41e34` (2026-08-08)

Amends `GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md`,
`…_ADDENDUM_A_2026-08-02.md`, `…_ADDENDUM_B_2026-08-08.md` and `…_ADDENDUM_C_2026-08-08.md`.
**Written before the rerun, not during it.**

**Scope of this addendum — narrow.** Addendum D supersedes Addendum C **only** for the frozen
candidate/artifact/test-count facts (§D.1 and §D.3 below). **All of Addendum C's host preparation (§C.2)
and the full A-4 acceptance criteria (§C.4) remain in force unchanged**, incorporated here by explicit
reference and not repeated verbatim. §C.5 (the systemd-precedence recording obligation) is resolved by the
round-1 audit and re-stated here as required host evidence.

**Why.** The round-1 candidate `ed3d0534` was NOT ACCEPTED: its start-mode pin was defeatable via
`EnvironmentFile=` overriding `Environment=` in systemd, and `verify.sh` did not reject that override.
That defect is repaired at **`2ce41e34`** on `codex/gate-a-disarmed-start-mode`, built directly on
`ed3d0534`. `2ce41e34` is **ACCEPTED under D025** as the repair candidate
(`GATE_A_DISARM_FIX_AUDIT_ROUND2_2CE41E34_2026-08-08.md`). Addendum C's frozen inputs named the
`ed3d0534` artifact and the pre-`2ce41e34` test counts, so those are superseded here. A-4's expected
outcome and seven-condition standard are **unchanged** from §C.4.

**This addendum does not authorize execution.** It pre-registers inputs and required host evidence only.
Gate A does not start until Barış authorizes staging action.

---

## D.1 Frozen inputs — supersede Addendum C §C.1

| Item | Addendum C (superseded) | **Authoritative (`2ce41e34`)** |
|---|---|---|
| Release SHA | `ed3d053432fb496123ac43bcb7d40cfb64edbb8b` | `2ce41e34bceb599d80af24c5c33d835820ec321b` |
| Artifact path | `C:\WPI_ARTIFACTS\ed3d0534…` | `C:\WPI_ARTIFACTS\2ce41e34bceb599d80af24c5c33d835820ec321b` |
| Manifest SHA-256 | `8964CC43…EE4B` | `EDB0FD34E3D976B872868CC3DFBF745CBC4B08F6C4C5D21B8D6CDA47A3E20D26` |
| Manifest entries | 7,059 | **7,059** (unchanged — no files added or removed) |
| Files on disk | 7,060 | **7,060** |
| Total bytes | 1,033,359,494 | **1,033,362,481** (+2,987 B over `ed3d0534` — the 59 inserted lines across 4 files) |
| `origin/master` | `637307e8` | `637307e8`, unchanged |
| Records branch | `feature/donchian-crypto-ladder` | same |

Lead-verified after build: `RELEASE_SHA` matches; manifest hash as above; 7,059 entries / 7,060 files /
1,033,362,481 bytes; **0 CR bytes on all five `deploy/linux/*.sh`**; in the built payload the first-start
pin is present (count 1), the steady pin absent (count 0), the env-file guard present (count 1), and the
behavioral test present (count 1). The steady template does **not** carry the pin — correct, because the
steady profile is the future credentialed profile.

## D.2 Host preparation — UNCHANGED, see Addendum C §C.2

Incorporated by reference. The `ebada020` install from the 2026-08-08 run is still on the host and A-1
(clean-host) will fail 7 of 8 assertions against it. Tear it down first by the proven recorded method and
script `C:\tmp\gatea_teardown.sh` (leftovers 0 last time). `rollback.sh` takes `--to-release-sha` and is
**not** an uninstaller. No change from §C.2.

## D.3 A-0 through A-3 — test counts rebaselined; A-0/A-1/A-2 otherwise unchanged

A-0's expected values are §D.1's. A-1 is unchanged (§C.2). A-2 is unchanged.

**A-3's expected Linux count is rebaselined.** Round 1's `ed3d0534` added two assertions inside two
*existing* test functions, leaving the count at `2 failed, 1357 passed, 1 warning`. Round 2's
`2ce41e34` adds **one new test function** (the env-file-rejection behavior test), so the count moves by
exactly one passing test:

- **Expected Linux A-3 (to be checked on the host):** `2 failed, 1358 passed, 1 warning`, with **exactly
  the same two pre-registered failures** — the two `test_order_state.py` gc-referents node IDs that
  pre-existed on `637307e8`. No new or unexpected failures are permitted. **This is the expected count and
  must be checked on the host; it is not asserted from Windows.**
- **Windows floor** (Lead- and auditor-reproduced at `2ce41e34`): `1360 passed, 1 warning` — up one from
  `1359` because the one new test function passes on Windows.

## D.4 A-4 — UNCHANGED seven-condition standard, see Addendum C §C.4

Incorporated by reference in full. A-4 PASSES only if all seven conditions in §C.4 hold, each evidenced:
(1) the unit reaches and stays `active (running)`; (2) a listener exists on `127.0.0.1:8790` only; (3)
`GET /api/status` reports a durably non-`ARMED` state; (4) `POST /api/arm` is **refused by the
application** — `Errno 111 Connection refused` does **not** count; (5) no broker connection is attempted;
(6) the persisted store reports `app_state=DISARMED` with state version unchanged; (7) the run records
which start mode was actually selected. A-4 FAILS if the service arms, attempts a broker connection,
reports an ambiguous state, exits non-zero, or if any required confirmation cannot be obtained. Read
`/var/log/mtc-bridge/bridge.err.log`, not just the journal. **No change from §C.4.**

## D.5 Required host evidence — the precedence question, now pre-registered as a check

Addendum C §C.5 raised systemd's `EnvironmentFile=`-overrides-`Environment=` precedence as a recording
obligation. Round 1 confirmed the override is real and the round-1 candidate failed because of it; round 2
makes `verify.sh` reject the override. Two pieces of **required host evidence** are therefore
pre-registered for the A-4 round and must be captured on the staging host (which has systemd, unlike this
workstation):

1. **Effective environment from the running unit:**
   ```
   systemctl show -p Environment mtc-bridge-first-start.service
   ```
   This shows the resolved `Environment=` assignments systemd actually applies to the service — i.e. whether
   the unit's pinned `MTC_BRIDGE_START_MODE=credential_free_disarmed` is the effective value or has been
   overridden. Capture it verbatim.

2. **Explicit verifier rejection of a temporary env-file override (without leaking values).** Prove on the
   host that `verify.sh` now refuses an env file that defines `MTC_BRIDGE_START_MODE=`: inject a temporary
   `MTC_BRIDGE_START_MODE=` line into the env file, run `verify.sh`, confirm it **fails/rejects** (non-zero,
   with the rejection message), then **remove the temporary line immediately** and re-run `verify.sh` to
   confirm a clean PASS. **Do not record any secret value** — record only the variable *name*, the
   exit code, and the rejection message text; redact or omit any value. The point is that the guard
   triggers on the name, not to capture a credential.

These are **required evidence for the A-4 round**, not optional. They settle, by execution on a real
systemd host, the precedence and the enforcement that neither this workstation nor the round-2 auditors
could execute directly.

## D.6 A-5 through A-9 — UNCHANGED

Incorporated by reference from the runbook and §C.6. They were never reached on 2026-08-08. Stop at the
first FAIL. Write `GATE_A_RESULT_2026-08-08B.md` either way, keeping the first run's result document intact.

## D.7 Gate A may not start without explicit staging authorization

`2ce41e34` is **ACCEPTED under D025 as the repair candidate**, not as a Gate A result. The rebuilt artifact
is a valid build of an accepted *candidate*. **Acceptance of the candidate does not authorize transfer,
install, teardown, or the Gate A run.** Those actions await explicit staging authorization from Barış. The
round-2 audit record is `GATE_A_DISARM_FIX_AUDIT_ROUND2_2CE41E34_2026-08-08.md`.
