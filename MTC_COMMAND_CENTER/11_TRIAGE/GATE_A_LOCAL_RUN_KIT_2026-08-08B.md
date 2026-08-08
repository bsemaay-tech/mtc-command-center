# Gate A local run kit — `2ce41e34` — 2026-08-08B

## Outcome

The accepted repair candidate remains
`2ce41e34bceb599d80af24c5c33d835820ec321b`. This work changed only the local Gate A
run kit and its records. It did not change product code, the candidate, the artifact, D025
acceptance, or the repair-round count. Gate A has not rerun.

No staging host contact, transfer, teardown, install, service start, credential access,
broker/exchange access, ARM request, order, TESTNET/mainnet action, or economic action occurred.

## Frozen transfer input — prepared, not transferred

- Tar: `C:\WPI_ARTIFACTS\2ce41e34bceb599d80af24c5c33d835820ec321b.tar`
- SHA-256: `d78b9e82e4138714fd5eabfb4996d8d831f28d14cf0b9e1149c8751739fe05f2`
- Bytes: `1047265280`

## Locally prepared scripts

All six scripts pass `C:\Program Files\Git\bin\bash.exe -n`. They are locally validated and
prepared; that is not authorization to execute them against staging.

| SHA-256 | Bytes | Path |
|---|---:|---|
| `0d456a8eebb0fd85eb20f08a4a67ffdf30a9fa1211a4cb4093b6f8110ebf1c11` | 5730 | `C:\tmp\gatea_A0_A1.sh` |
| `07a715aa5aeec86dd81cc8fa4051f6c66f8461dacedb9e05ffc880a07a08c053` | 9717 | `C:\tmp\gatea_A2.sh` |
| `33934221be2955c04bb8944807c65a51496c8e8780a076b81a3860472f604443` | 4064 | `C:\tmp\gatea_A3.sh` |
| `78aa7fca7bfe7eb256a562d08d61e7d16b4ffcd3b164b89a5df420a01a8fd9b4` | 16228 | `C:\tmp\gatea_A4.sh` |
| `f75912a2298b2611d70d20998b711e1af54f1900b3af77441595de960f0f101d` | 3053 | `C:\tmp\gatea_A4_diag.sh` |
| `19016d8f0bdeffa08637f83baf84b2e9d6f41e1359b44c6faad22bcb763ec0b3` | 4839 | `C:\tmp\gatea_teardown.sh` |

Binding checks added during re-baselining:

- A-0 binds the non-regular-entry count and full manifest-verification exit/output.
- A-2 binds zero dry-run side effects, zero populated env-file assignments without printing
  values, verifier rejection of a temporary start-mode override, byte-identical restoration,
  and a clean post-restore verification.
- A-3 requires pytest exit code exactly `1`, exact summary
  `2 failed, 1358 passed, 1 warning`, and exact two-way equality of the observed and permitted
  failure-node sets.
- Teardown uses fresh evidence path `~/teardown-ebada020-20260808B`, refuses overwrite, limits
  deletion to the recorded exact targets, and is labelled
  `LOCAL PREPARATION ONLY — NOT AUTHORISED TO RUN`.

## A-4 probe correction

Independent source inspection found that `bridge/api/routes.py:87-97` calls
`_require_confirm()` before checking `credential_free_disarmed`. Therefore a POST without
`X-Confirm` can only receive `409 stale state_version`; that response does not prove the
credential-free application refusal and cannot satisfy A-4. The existing regression test sends a
current `X-Confirm`, so it passes the confirm guard and reaches the credential-free refusal rather
than the stale-version path — which is why this route-order issue only surfaces under a probe that
omits or mismatches `X-Confirm`. This was a local run-script evidence defect, not a defect in
accepted candidate `2ce41e34`.

The corrected step 8 now:

1. GETs `/api/status` and, before any POST, requires exact `state=DISARMED`,
   `mode=credential_free_disarmed`, `network=disabled`, `exchange_conn=disabled`,
   `exchange_enabled=false`, `credential_lookup=disabled`, `arm_enabled=false`, and a
   non-boolean integer `state_version >= 0`.
2. On any mismatch, exits `2` with `BLOCKED - NO POST ISSUED`.
3. Only after all preconditions pass, POSTs `/api/arm` with `X-Confirm` equal to that exact
   `state_version`.
4. Requires HTTP `409` plus the exact credential-free refusal detail, then GETs status again and
   requires unchanged `state_version` and all fail-closed fields.
5. Treats stale-confirm, 2xx, 500/503, transport failure, or any state change as a binding failure.

The exact embedded probe was falsified locally with `urllib` patched, so no network was used:

| Case | Expected/observed result |
|---|---|
| bad mode | exit 2; zero POST |
| exact credential-free refusal | exit 0; one POST; unchanged state |
| stale-confirm response | exit 3 |
| changed state version | exit 4 |
| boolean state version | exit 2; zero POST |

All five cases passed. The candidate's real in-process test
`test_status_is_truthful_and_current_version_arm_is_durably_rejected` also passed:
`1 passed, 1 warning in 0.52s`. It used no broker and no host.

## Offline validation and supplemental audit

**Offline local A-0 executed against the real frozen tar in a fresh disposable HOME and passed every
A-0 identity check.** Tar SHA-256 `d78b9e82e4138714fd5eabfb4996d8d831f28d14cf0b9e1149c8751739fe05f2`,
tar bytes `1047265280`; `RELEASE_SHA` exact `2ce41e34bceb599d80af24c5c33d835820ec321b`; manifest SHA
`edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26`; 7059 manifest entries; 7060
regular files; 1033362481 total payload bytes; 0 non-regular entries; `sha256sum -c` rc 0 with 0
output/problem lines; all five `deploy/linux/*.sh` had 0 CR bytes.

**The same script then stopped at A-1** because this workstation is Windows and `/etc/os-release` is
absent. **A-1 was NOT executed/accepted and no Linux or Gate A claim is promoted.**

**DeepSeek supplemental audit attempt 1** exhausted `max_iters` with no verdict; the focused retry
read all ten files but stopped without finish/verdict. **DeepSeek is supplemental non-accepting
evidence only.**

**Lead classification:** its claimed A-4 `start_rc` pipeline loss did not reproduce because
`set -o pipefail` returned upstream rc 7; nevertheless A-4 now records `start_rc` explicitly as
`PIPESTATUS[0]`. Its A-3 substring concern reproduced: `grep -qF` could match `12 failed...`; changed
locally to `grep -qxF`, exact fixture rc 0 and prefixed fixture rc 1. Its possible metadata exposure
did not reproduce as credentials at this candidate, but A-4 and A-4_diag were hardened to query only
meta keys `app_state` and `schema_version`. The one-tar-home uniqueness point remains informational;
the one exact tar under test passed all identity checks.

**After hardening, all six scripts pass `bash -n`;** the exact embedded A-4 five-case no-network
falsification still passes; the real in-process refusal test still passes `1 passed, 1 warning in
0.52s`.

**Cleanup residue:** cleanup of the disposable `C:\tmp\gatea-a0-offline-bb964b4106b24ea192f830065a1b9992`
was refused twice by local command policy after exact path verification; the directory remains
isolated under `C:\tmp` and must be removed only by an allowed exact-literal cleanup. It was **not**
removed.

**Candidate/artifact/acceptance/repair-round state unchanged; no staging contact or hard-gated
action. Explicit staging authorization still required.**

## Frozen run-kit bundle — prepared, not transferred

The six validated scripts are also frozen into one local transport bundle:

- Directory: `C:\WPI_ARTIFACTS\gatea-run-kit-20260808B-2ce41e34`
- Tar: `C:\WPI_ARTIFACTS\gatea-run-kit-20260808B-2ce41e34.tar`
- Tar SHA-256: `ac0fbaf2fefa8241c5c92f5bf35a3f9fc5258a4b7e30614988ed305afa61c0fb`
- Tar bytes: `61440`
- Members: `9` — one root directory plus `README.txt`, `SHA256SUMS`, and the six scripts
- Manifest entries: `7` — the six scripts plus `README.txt`
- README SHA-256: `45b480ac5ce949f051e4f30753a5e85c7871b634f0ca9b1b646ae24927981353`

The tar was opened and verified without extraction: its member set is exact; all seven manifest
hashes match the archived bytes; all six archived shell files contain zero CR bytes. The README is
explicit: `LOCAL PREPARATION ONLY - NOT AUTHORIZED TO TRANSFER OR RUN.` The bundle was **not
transferred or executed** and creates no staging authorization.

## Safety state and authorization boundary

The old `ebada020` staging install remains masked, inactive, with no listener, no credentials,
and nothing armed according to the last verified record; it was not rechecked in this work unit.
Explicit staging authorization is still required before any host contact or destructive teardown.

## Next steps

1. **[AI: Any] SAFE LOCAL HOUSEKEEPING (when policy permits):** remove the disposable
   `C:\tmp\gatea-a0-offline-bb964b4106b24ea192f830065a1b9992` directory via an allowed exact-literal
   cleanup. It remains isolated under `C:\tmp`; it was not removed in this work unit.
2. **[AI: Barış]** Explicitly authorize staging contact and the bounded teardown/rerun window.
3. Once authorized, transfer the run-kit bundle, verify its tar hash, extract it, and verify
   `SHA256SUMS`; run teardown first and require leftovers `0`; transfer the single frozen product
   tar; then run Gate A from A-0 under Addendum D and stop at the first FAIL.
4. Bind A-4 to the corrected step-8 result. `stale state_version` is non-evidence and fails A-4.
   Capture `systemctl show -p Environment`, `bridge.err.log`, and verifier override-rejection,
   restoration, and clean re-verification evidence.
5. Preserve `GATE_A_RESULT_2026-08-08.md`; write `GATE_A_RESULT_2026-08-08B.md` for the rerun.
6. Update `_AI_MEMORY/` before starting the next work unit.
