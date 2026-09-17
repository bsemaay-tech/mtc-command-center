# LEAD_VERIFICATION — WP-P0-31 M1, T0 repair round 2 (`61c56148`) after the second exact-Opus read of `e9e37aec` returned REQUEST_CHANGES — 2026-09-17 08:3x-08:5x UTC+3

**Trigger:** the Wednesday queue (delayed to Thursday 08:03 UTC+3 by the host sleeping overnight) ran lane 1 first: exact `claude-opus-5` xhigh T0 read of `e9e37aec` 08:03-08:29 UTC+3 (05:03-05:29Z; 25 min; 599-line report `OPUS_QUEUE_20260916/P031/ATTEMPT2_REQUEST_CHANGES_e9e37aec/OPUS_T0_REPORT.md`) → **F-1 CLOSED** (the reviewer rebuilt mutant M-2 itself: exactly the round-1 test RED, 110 GREEN, whole invariant asserted, cannot pass for the wrong reason) but **REQUEST_CHANGES on F-2**.
**F-2:** the reviewer mutated all 20 guards OD-1..OD-12 added or re-shaped (its §5 map, each from the committed blob, whole suite each time): 18 turn something RED; two do not — both in OD-7's new registrar-refresh branch: `p031_lifecycle_ledger.py:812-813` (`DEPLOYMENT_IDENTITY_RETIRED` on the refresh path) and `:814-816` (`DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE` on the refresh path). With either removed the suite stays 110 green while the ledger accepts a refresh onto an identity the candidate retired (arm C1) or onto another candidate's identity (arm C2: two candidates sharing one deployment identity). Same D026 class as K-D-01 and F-1 (`MASTER_WORK_PACKAGE…:85`, M1 gate `:656`). New NITs: N-11 (the `81eedf03…` ledger hash in `SHA256SUMS_P31FIX.txt` is a checkout hash — mixed CRLF — not the blob's `2bff9fcc…`; pin blob OIDs), N-12 (the round-1 test docstring said "Lane-3" and pinned `:832-833`), N-13 (OD-7 revocation is reversible — a second refresh B→A is accepted; owner question, with N-10).
**Role:** Lead = builder of the two fence tests (disclosed); T0 cap 3 rounds — this is round 2; the reviewer states the mutation map is complete, so one round closes the class.

## Lead reproduction of F-2 (before writing anything)
`p031_r2_mutants.py` (scratchpad; copy in this directory is not kept — the harness is described here): mutant M4 = blob `e9e37aec` lines 812-813 removed; mutant M7 = lines 814-816 removed; each swapped into the worktree in place of the checkout bytes, focused suite run with the pinned interpreter, checkout bytes restored and re-hashed (`81eedf03…` both times).
| Mutant | Suite (candidate tests, no new tests) | File |
|---|---|---|
| M4 `:812-813` removed | **110 passed, 1 skipped, 167 subtests** — fully green | `LEAD_REPRO_F2_M4_refresh_retired_guard_removed.txt` |
| M7 `:814-816` removed | **110 passed, 1 skipped, 167 subtests** — fully green | `LEAD_REPRO_F2_M7_refresh_bound_guard_removed.txt` |
Citations checked against the blob: `git show e9e37aec:<ledger>` lines 804-820 are the registrar-refresh branch as quoted; `is_registrar_refresh` has 0 occurrences at `c76043b9` (the branch is OD-7's); the ladder-path twins `:834-835` / `:836-838` exist as stated. F-2 CONFIRMED.

## Repair (`61c56148`, +158/−2, one file, no ledger change)
Two tests in `LifecycleLedgerTests`, same idiom as the round-1 fence (`build_to_rung`, `append_authority_event`, `self.registrar.append(event(...))`, replay assertion):
1. `test_registrar_refresh_cannot_adopt_the_candidates_own_retired_identity` — SHADOW under `DEPLOYMENT_A` → `RETIRED` (supervisor, carries `PACKAGE_A`/`DEPLOYMENT_A`, so `retired_deployments` ∋ `DEPLOYMENT_A` and `retired_packages[cid]` ∋ `PACKAGE_A`) → `RE_ENTRY` (registrar, `OWNER_EXTERNAL_CHANGE`, one-sentence reason) → `FROZEN` under `PACKAGE_B` → `SHADOW_ELIGIBLE` under `PACKAGE_B`/`DEPLOYMENT_B`; the registrar refresh SHADOW→FROZEN naming `PACKAGE_B`/`DEPLOYMENT_A` raises `DEPLOYMENT_IDENTITY_RETIRED`; state stays SHADOW / `PACKAGE_B` / `DEPLOYMENT_B`; the replay's FROZEN records are exactly the two genuine ones. Guard walk on the candidate: `:805-811` passes (identity given, current present, package equal, identity differs) → `:812` fires. On mutant M4: `:814-816` does not rescue (`deployment_owners[DEPLOYMENT_A]` is the same candidate), `:819-820` does not rescue (`PACKAGE_B` is not the retired package) → accepted → RED.
2. `test_registrar_refresh_cannot_adopt_another_candidates_identity` — `CANDIDATE_B` at SHADOW under `PACKAGE_B`/`DEPLOYMENT_B`, `CANDIDATE_A` at SHADOW under `PACKAGE_A`/`DEPLOYMENT_A`; the registrar refresh of A naming `PACKAGE_A`/`DEPLOYMENT_B` raises `DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE`; both candidates keep state / package / identity; the replay's FROZEN records are exactly the two genuine ones. Guard walk: `:805-811` passes, `:812` does not fire (`DEPLOYMENT_B` not retired), `:814-816` fires. On mutant M7: nothing else refuses → accepted → RED.
Also in the commit (N-12): the round-1 test's docstring now says "Lane-1" and names the guard by its refusal code instead of `:832-833`.

## Evidence
| Arm | Result | File |
|---|---|---|
| RED, mutant M4 (`:812-813` removed) | **1 failed / 111 passed / 1 skipped** — exactly `test_registrar_refresh_cannot_adopt_the_candidates_own_retired_identity` (`ValueError not raised`) | `LEAD_RED_R2_M4_refresh_retired_guard_removed.txt` |
| RED, mutant M7 (`:814-816` removed) | **1 failed / 111 passed / 1 skipped** — exactly `test_registrar_refresh_cannot_adopt_another_candidates_identity` (`ValueError not raised`) | `LEAD_RED_R2_M7_refresh_bound_guard_removed.txt` |
| GREEN (candidate bytes) | **112 passed, 1 skipped, 167 subtests**; contracts (from `MTC_COMMAND_CENTER/contracts`) **50 passed** | `LEAD_PYTEST_GREEN_R2.txt` |
| Ruff (`ruff 0.16.4`, `wp_p0_04_tooling` venv) | the file's 36 pre-existing findings at `e9e37aec`, 36 at `61c56148` — 0 new | console |
| Guard | `RESULT: PASS`; staged exactly the test file; protected none; pine guard PASS | `LEAD_GUARD_R2.txt` |
| Gemini delta (`P031_R2_GEMINI`, packet `P031_R2_20260917`, 14 files) | COUNTED **PASS**, F-2 CLOSED, both guard walks as the Lead traced, both mutants would accept, 0 findings; 23 reads / 0 outside / 0 mismatches; 199 s | `GEMINI/` (+ `LEAD_ADJUDICATION.md` there) |
Blob OIDs (N-11): ledger `7e7874770dc880aacb9bd8fcc6917c8416a7ce6a` (unchanged since `bd0d56d0`; blob sha256 `2bff9fcc…`), tests at `61c56148` `c72452f6…`; the checkout hash `81eedf03…` in `SHA256SUMS_P31FIX.txt` is a CRLF-mixed working-tree hash and is not a pin.

## Roster
Lane 1 re-pinned to `61c56148` (launcher, `REVIEW_BRIEF.md` addendum 2026-09-17, `opus/BRIEF.md`, queue row, `QUEUE_LOG.txt`); attempt 2 archived under `P031/ATTEMPT2_REQUEST_CHANGES_e9e37aec/` (report, stream, launch.exit, the brief as reviewed). The third exact-Opus read (round 2 of the T0 cap 3) runs by hand today after lanes 2-4; Sol (Sep 19) reads whatever pin then stands. The Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
