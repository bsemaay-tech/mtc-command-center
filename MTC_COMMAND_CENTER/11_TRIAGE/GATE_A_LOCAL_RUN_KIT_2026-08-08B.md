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
| `e6a5848bb4b6c511f7f32f1d8c0d90fbdea1243c0a837111072e4d7f1d7d1e9c` | 4063 | `C:\tmp\gatea_A3.sh` |
| `aecbbe1685c971476570529058eb952f8240668f5d547d84410320f8acdb7563` | 16300 | `C:\tmp\gatea_A4.sh` |
| `2a8b34b7e1ebb2a69f37a7a1cb5cafde22a127ca7474ef9f54d4d8127f8fd226` | 2980 | `C:\tmp\gatea_A4_diag.sh` |
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
`1 passed, 1 warning in 0.67s`. It used no broker and no host.

## Safety state and authorization boundary

The old `ebada020` staging install remains masked, inactive, with no listener, no credentials,
and nothing armed according to the last verified record; it was not rechecked in this work unit.
Explicit staging authorization is still required before any host contact or destructive teardown.

## Next steps

1. **[AI: Barış]** Explicitly authorize staging contact and the bounded teardown/rerun window.
2. Once authorized, verify all six local script hashes, run teardown first and require leftovers
   `0`, transfer the single frozen tar, then run Gate A from A-0 under Addendum D and stop at the
   first FAIL.
3. Bind A-4 to the corrected step-8 result. `stale state_version` is non-evidence and fails A-4.
   Capture `systemctl show -p Environment`, `bridge.err.log`, and verifier override-rejection,
   restoration, and clean re-verification evidence.
4. Preserve `GATE_A_RESULT_2026-08-08.md`; write `GATE_A_RESULT_2026-08-08B.md` for the rerun.
5. Update `_AI_MEMORY/` before starting the next work unit.
