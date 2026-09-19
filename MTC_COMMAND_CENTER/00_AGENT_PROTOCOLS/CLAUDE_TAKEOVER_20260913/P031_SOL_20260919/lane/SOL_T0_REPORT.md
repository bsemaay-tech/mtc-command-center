# P031 M1 T0 independent review — gpt-5.6-sol xhigh

I reviewed candidate `61c56148d76aa71424f7b3c0ffa69a14d9e702fe` independently. I did not read any `*OPUS_T*_REPORT.md` or any Lead adjudication of an Opus report. One REQUIRED OD-6 conformance defect remains.

## Verified identities

- Worktree: `C:/tmp/P031_M1_20260913`.
- `git -c safe.directory=* -C C:/tmp/P031_M1_20260913 rev-parse HEAD` → `61c56148d76aa71424f7b3c0ffa69a14d9e702fe`.
- Pinned interpreter → `Python 3.12.12`.
- Checkout SHA-256:
  - `p031_lifecycle_ledger.py`: `81eedf03b79289dce92019a16a56e21ed9612be8cca16660d1b79095cb7ab816`.
  - `test_p031_lifecycle_ledger.py`: `5f4bef27393821cc4ec8da7301fb5ff1379da5c4357c5f76d8008339f7904675`.
- Commit-blob identities, calculated from the raw bytes returned by the permitted `git show 61c56148:<path>` command:
  - ledger blob SHA-1 `7e7874770dc880aacb9bd8fcc6917c8416a7ce6a`; blob SHA-256 `2bff9fcc1fc42c7780a7e40bb127f0dad79fe64dd3b17ee14d5337332f88a63d`.
  - test blob SHA-1 `c72452f687c6feef250b4dc87a1625fe3668e108`; blob SHA-256 `5f4bef27393821cc4ec8da7301fb5ff1379da5c4357c5f76d8008339f7904675`.
- The ledger checkout hash differs from its blob hash because the checkout has mixed line-ending bytes; the blob identity matches the review brief's checkout-independent pin.
- Authority verified at `C:/CT13/DECISIONS.md:83` (`OD-20260914-P031-LIFECYCLE-1`, all twelve recommended answers) and `:91` (`OD-20260914-P031-BATCH-GO-1`).

## Answer conformance

Packet quotes are from `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P031_LIFECYCLE_DECISIONS_20260913_V4.md:1047-1058`.

| Ref | Selected packet option (quoted) | Candidate evidence | Classification |
|---|---|---|---|
| OD-1 | 3D: “move ‘ratified worthiness version’ from an M1 acceptance precondition to an operating precondition on writing a real `CAPTURED -> TRIAGED` record” | Worktree `DECISIONS.md:18` and `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:298` make exactly that documentary change; the report still says `WORTHINESS CHECK-SET: INACTIVE` at ledger `:1442-1446`. | **IMPLEMENTED-AS-ANSWERED** |
| OD-2 | 1B: “writer supplies `next_state`; ... strict descent ... unchanged `deployment_identity_hash`. Assign `DEMOTED` to `MULTI_WORKER_SUPERVISOR`.” | Ladder rank `:42`; supervisor authority `:121-123`; exact descending arcs `:134-139`; rank refusal `:688-693`; changed deep identity is refused before append at `:675-686`, and the ordinary identity guard is `:824-838`. | **IMPLEMENTED-AS-ANSWERED** |
| OD-3 | 2A: add the challenged-incumbent field under WP-P0-04 and keep `CHALLENGE` fail-closed until it exists. | `CHALLENGE` unconditionally refuses `CHALLENGE_INCUMBENT_DEPLOYMENT_IDENTITY_FIELD_MISSING` at ledger `:657-658`; it is the sole unresolved lifecycle contract at `:1451-1453`. | **IMPLEMENTED-AS-ANSWERED** (blocked as answered) |
| OD-4 | 3D now: “ratify the current repository-wide refusal as the deliberate interim.” | A second live candidate is still refused at ledger `:710-721`; the report records the ratified interim at `:1454-1457`. | **IMPLEMENTED-AS-ANSWERED** (recording only) |
| OD-5 | 4A: “writer-supplied `check_set_purpose` ... with `check_set_version`, `evaluation_run_hash` and non-empty `failing_checks` all mandatory. Restore `REJECTED -> RE_ENTRY`.” | Rung-purpose map `:49-60`; arcs `:70-85`; required supplied purpose `:619-622`; rung and active-version binding `:728-740`; hash/failing-check guards `:773-783`. | **IMPLEMENTED-AS-ANSWERED** |
| OD-6 | 5C: “take the target from the supplied `check_set_version`'s purpose instead of inferring it from `previous_state`.” | Unique version-to-purpose derivation exists at `:596-606`, but `:623-626` instead prefers a writer-supplied `check_set_purpose`. The later checks at `:724-740` validate membership but do not restore uniqueness. A duplicated version configured for both SHADOW targets refuses without a purpose and **appends** when the writer supplies `paper_eligibility`. | **BROADER THAN ANSWERED — REQUIRED F-1** |
| OD-7 | 6A: “candidate returns to `FROZEN` under the new composite; revocation stays silent-by-construction.” | Deep-rung Registrar arcs `:77-81`; refresh classification `:669-686`; same-package/new-deployment, retired-identity and foreign-owner guards `:801-820`; state returns under the new identity at `:840-846`. | **IMPLEMENTED-AS-ANSWERED** |
| OD-8 | 7A: “one `evaluation_run_hash` binds to exactly one `candidate_id` forever.” | Cross-candidate ownership refusal at `:784-790`; report ratification at `:1459-1461`. | **IMPLEMENTED-AS-ANSWERED** (recording only) |
| OD-9 | 5a-C: “`RETIRED -> RE_ENTRY` only via `OWNER_EXTERNAL_CHANGE` with a ... one-sentence ... reason.” | Sixth trigger `:88-96`; retired-only owner-trigger/reason enforcement and non-retired exclusion `:755-766`; identities clear at `:840-841`. | **IMPLEMENTED-AS-ANSWERED** |
| OD-10 | 5b-A: “one evaluation run may back any number of distinct check-set purposes within one epoch; cross-epoch and cross-candidate reuse stay refused.” | Prior-epoch refusal `:791-796`; epoch rollover `:1105-1112`; real purpose/version/hash/state assertions at test `:2278-2442`; report record at ledger `:1461`. | **IMPLEMENTED-AS-ANSWERED** |
| OD-11 | 2C: “optional configured catalog: refuse an `evaluation_run_hash` absent from an accepted catalog when one is supplied, fail closed on catalog-backed claims when none is.” | Constructor seam `:321-340`; strict catalog normalization `:392-403`; exact-bool normalization `:505-558`; no-catalog/no-hash/outside-catalog refusals `:742-753`; Registrar delegates through the sole append path at `:1384-1401`. This is the packet's narrow explicit-`catalog_backed` reading. | **IMPLEMENTED-AS-ANSWERED** |
| OD-12 | 7-A: “preserve; fold the refresh ... into one new candidate and one T0 roster once OD-1..OD-11 are answered.” | The batch is based on `c76043b9`; `c76043b9..48bd70de` is limited to the two ledger paths and two authorized documentation paths, and later repairs are test-only. | **IMPLEMENTED-AS-ANSWERED** |

## D026 RED/GREEN evidence

| Rule / refusal | Permanent candidate test | RED on pre-fix behavior? | GREEN now? |
|---|---|---|---|
| OD-5 purpose/version/hash/failing-check requirements and restored re-entry | test `:677-763` | **Yes.** With the current optional seam mechanically erased, `c76043b9` produces four exact-code mismatches against `REJECTED_PURPOSE_UNRESOLVED` and cannot execute the accepted/re-entry path. | Yes |
| OD-6 target from version purpose | test `:1905-2015` | **Yes for the formerly unresolved SHADOW path:** base raises `ADMISSION_WITHHELD_TARGET_UNRESOLVED`. **Incomplete for F-1:** no permanent test covers a version configured under multiple purposes plus a supplied-purpose override. | Only for unambiguous registries |
| OD-2 demotion mapping/descent | test `:2484-2515` | **Yes.** Base raises `DEMOTION_TARGET_RUNG_MAPPING_UNRESOLVED`; independent arms additionally refuse sideways, upward, and changed-identity attempts. | Yes |
| OD-7 Registrar refresh composite validity | tests `:2517-2586`, `:3237-3323` | **Yes.** Base reaches `ILLEGAL_TRANSITION` instead of the accepted refresh/new exact guards. The missing-identity/package-drift additions already pass on `96af3eb6` because those guards were already present there; they fence rather than originate that behavior. | Yes |
| OD-7 old identity cannot be used for post-refresh admission | test `:2588-2665` | **Yes.** Removing ledger `:832-833` makes exactly this test fail; full mutant result `1 failed, 111 passed, 1 skipped, 167 subtests passed`. | Yes |
| OD-7 refresh cannot adopt own retired identity | test `:2667-2767` | **Yes.** Removing `:812-813` makes exactly this test fail with the same full-suite count. | Yes |
| OD-7 refresh cannot adopt another candidate's identity | test `:2769-2821` | **Yes.** Removing `:814-816` makes exactly this test fail with the same full-suite count. | Yes |
| OD-9 owner trigger / one-sentence reason | test `:4462-4531` | **Yes.** On the compatibility-run base, the ordinary trigger appends (no `ValueError`), and the following two-sentence arm fails by the now-drifted state/old precedence. | Yes |
| OD-10 same-epoch reuse assertions | test `:2278-2442` | **GREEN on base by design.** This is ratification plus assertion repair, not a new refusal. The base compatibility arm also passed. | Yes |
| OD-11 catalog shape and strict bool | tests `:3062-3105` | The four tests are **GREEN on `96af3eb6`** because the behavior already existed before the tests were added; against `c76043b9` the expanded API is absent. They are permanent fences, not semantic RED at the immediate predecessor. | Yes |
| OD-11 no catalog / hash outside catalog | tests `:3042-3060`, `:3107-3179` | Existing catalog refusal paths are GREEN on `96af3eb6`. | Yes |
| OD-11 catalog-backed with no hash | tests `:3161-3179`, `:3181-3235` | Builder arm is RED on `96af3eb6` only by refusal precedence (`EVALUATION_RUN_HASH_REQUIRED` rather than the new code). The Registrar arm is the genuine fail-open RED: no `ValueError`, state becomes `FROZEN`, six records. | Yes |
| OD-4/OD-8/OD-10 report recording | test `:2823-2899` | **Yes** for report bytes: base still reports unresolved strings. | Yes |

The compatibility harness only removes the two optional public-seam keyword additions before loading the `c76043b9` module; it does not add transition semantics. Its selected result was 8 methods, 8 failures and 3 errors; the same-epoch reuse method alone was GREEN as intended.

## Independent RED arms

Scratch root: `C:/tmp/SOL_P031_SCRATCH/sol_t0_61c56148_20260919`. Pinned interpreter: `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe`.

### Public-seam fail-open hunt

Command, cwd `C:/tmp/SOL_P031_SCRATCH/sol_t0_61c56148_20260919`:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& <pinned-python> independent_red_arms.py
```

Exact observed output:

```text
CATALOG_REGISTRAR_NO_HASH=REFUSED:CATALOG_BACKED_WITHOUT_EVALUATION_HASH
CATALOG_HASH_OUTSIDE=REFUSED:EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG
CATALOG_BOOL_INT=REFUSED:CATALOG_BACKED_INVALID
CATALOG_BOOL_STRING=REFUSED:CATALOG_BACKED_INVALID
RETIRED_REENTRY_MISSING_TRIGGER=REFUSED:REENTRY_TRIGGER_INVALID
RETIRED_REENTRY_NO_OWNER_TRIGGER=REFUSED:RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED
RETIRED_REENTRY_TWO_SENTENCES=REFUSED:RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED
DEMOTED_SIDEWAYS=REFUSED:DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT
DEMOTED_UPWARD=REFUSED:DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT
DEMOTED_CHANGED_IDENTITY=REFUSED:DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED
REJECTED_NO_FAILING_CHECKS=REFUSED:FAILING_CHECKS_REQUIRED
REJECTED_WRONG_WRITER=REFUSED:WRITER_AUTHORITY_REFUSED
SAME_EPOCH_REUSE=APPENDED_AND_ASSERTED
AMBIGUOUS_CAPACITY_WITHOUT_PURPOSE=REFUSED:ADMISSION_WITHHELD_TARGET_UNRESOLVED
AMBIGUOUS_CAPACITY_VERSION=APPENDED
AMBIGUOUS_CAPACITY_PURPOSE=paper_eligibility
AMBIGUOUS_CAPACITY_CHECK_SET=shared-capacity.v1
AMBIGUOUS_CAPACITY_STATE=SHADOW
```

`reason` itself cannot be absent or empty at this seam because shared `LifecycleEvent.reason` is mandatory `NonEmptyStr` (`MTC_COMMAND_CENTER/contracts/mtc_contracts/execution.py:168-181`). Trigger absence and the two relevant reason/trigger combinations were exercised above.

### Pre-`bd0d56d0` Registrar fail-open reproduction

Command, cwd `C:/tmp/P031_M1_20260913`:

```powershell
git -c safe.directory=* show 96af3eb6:MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py |
  & <pinned-python> C:/tmp/SOL_P031_SCRATCH/sol_t0_61c56148_20260919/old96_catalog_probe.py
```

Exact output:

```text
OLD96_RESULT=APPENDED
OLD96_STATE=FROZEN
OLD96_DEPLOYMENT=4444444444444444444444444444444444444444444444444444444444444444
OLD96_RECORDS=6
```

The six selected current tests on the same `96af3eb6` module produced four passes and two failures: invalid catalog shapes, valid catalog tuple, non-bool `catalog_backed`, and refresh missing/package/same-identity arms passed; the builder no-hash arm failed by `EVALUATION_RUN_HASH_REQUIRED` precedence; the Registrar arm failed because no `ValueError` was raised.

### Repair mutants and unmodified control

Common command from each named scratch arm cwd:

```powershell
& <pinned-python> -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py -q -p no:cacheprovider
```

Exact terminal summaries:

```text
green:
112 passed, 1 skipped, 167 subtests passed in 43.90s

mutant_revoked_admission (removed ledger :832-833):
FAILED ...::test_post_refresh_admission_cannot_reuse_the_revoked_deployment_identity
AssertionError: ValueError not raised
1 failed, 111 passed, 1 skipped, 167 subtests passed in 43.89s

mutant_refresh_retired (removed ledger :812-813):
FAILED ...::test_registrar_refresh_cannot_adopt_the_candidates_own_retired_identity
AssertionError: ValueError not raised
1 failed, 111 passed, 1 skipped, 167 subtests passed in 44.05s

mutant_refresh_foreign (removed ledger :814-816):
FAILED ...::test_registrar_refresh_cannot_adopt_another_candidates_identity
AssertionError: ValueError not raised
1 failed, 111 passed, 1 skipped, 167 subtests passed in 44.04s
```

Guard-order assessment:

- Retired identity test: before the challenged refresh, current is `PACKAGE_B` / `DEPLOYMENT_B`; the event carries `PACKAGE_B` / retired `DEPLOYMENT_A`, so `:805-811` does not fire. Removing `:812-813` accepts the refresh. `RETIRED_PACKAGE_IDENTITY` at `:819-820` cannot rescue it because only the earlier `PACKAGE_A` was retired; the candidate was re-frozen under `PACKAGE_B`. The test asserts exact refusal, unchanged SHADOW/package/identity, and no extra FROZEN replay record.
- Foreign identity test: claimant current/event package is `PACKAGE_A`, event deployment `DEPLOYMENT_B` differs from claimant current `DEPLOYMENT_A`, so `:805-811` does not fire. Removing `:814-816` accepts shared ownership. The test asserts exact refusal, state/package/identity for both candidates, and no extra FROZEN replay record.
- Post-refresh old-identity test asserts exact refusal, unchanged FROZEN/new identity, no second SHADOW admission record, then a successful admission under the new identity. None of the three tests can pass merely because an earlier guard fires.

## Scope, protected paths, and authorship

- `git diff c76043b9 48bd70de -- .` with exclusions for the ledger, its test, worktree `DECISIONS.md`, and the one master-brief path produced no output. Separate diffs show the documentary changes are one authorized row and one authorized paragraph. `git diff c76043b9 48bd70de -- MTC_COMMAND_CENTER/contracts` produced no output.
- The same exclusion check for `48bd70de..e9e37aec` and `e9e37aec..61c56148` produced no output outside `test_p031_lifecycle_ledger.py`. The latter diff is the two new identity tests plus the disclosed docstring correction.
- No `G1_SCOPE_AND_CONTRACT.md` exists in the repository. The external amended file's public seams at `C:/tmp/P031_LEAD_20260912/G1_SCOPE_AND_CONTRACT.md:20-24` match ledger `:321-327` and `:848-858`.
- The pre-amendment external G1 copy hashes to the pinned `1752290cb9dd81d75ce5ca65a1dd5510584151101e088ce08c638fadb8195d8a`. The current external file and recorded amended copy both hash to `0bcd6abc0a1662918eee0a4633e83c91da6ebdb7698c492c9b6899882f4a2460`, not the addendum's intermediate `c82de2a8...`; see NIT N-1.
- `48bd70de` is test-only. Lead authorship changes neither the semantic standard nor the verdict and needs no procedure beyond the independent roster. The later `e9e37aec`/`61c56148` test-only Lead repairs likewise received the independent mutation review above.

## Report honesty and reproduced checks

- The batch report accurately discloses its Python 3.14.2 sandbox, missing local 3.12, initial `105 passed, 1 skipped, 157 subtests`, and blocked commit. P31FIX accurately discloses Python 3.14.2, `108 passed, 1 skipped, 167 subtests`, missing 3.12/Ruff, and the blocked commit.
- The diffs agree with the dispositions: `96af3eb6..bd0d56d0` adds the catalog no-hash refusal/docstring plus J-01/J-02/J-03/J-05 tests; `bd0d56d0..48bd70de` is only the genuine Registrar test; subsequent repairs are test-only.
- Gemini's statement that the J-01/J-02/J-05 tests pass on `96af3eb6`, while J-03 fails by refusal-string precedence, was reproduced. The actual Registrar fail-open on `96af3eb6` was also reproduced.
- Worktree focused command, cwd `C:/tmp/P031_M1_20260913`:

```text
112 passed, 1 skipped, 167 subtests passed in 24.36s
```

- Shared contracts command, cwd `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/contracts`:

```text
50 passed in 0.29s
```

- A Ruff rerun was attempted with the pinned interpreter and was unavailable: `No module named ruff`.

## Findings

### F-1 — REQUIRED — OD-6 allows the writer to choose an ambiguous capacity target

**Location:** `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:596-606, 623-626, 724-740`; missing regression near `test_p031_lifecycle_ledger.py:1960-2015`.

Option 5C requires the target to come from the supplied `check_set_version`'s purpose. `_purpose_for_check_set_version` correctly returns a purpose only for one match (`:596-606`), but `_resolve_check_set_purpose` bypasses that fail-closed rule with:

```python
return supplied_check_set_purpose or self._purpose_for_check_set_version(
    check_set_version
)
```

I configured `shared-capacity.v1` under both `paper_eligibility` and `testnet_live_candidate_eligibility`. With only that version, the append refused `ADMISSION_WITHHELD_TARGET_UNRESOLVED`; adding `check_set_purpose="paper_eligibility"` appended a SHADOW `ADMISSION_WITHHELD_CAPACITY` record. This is effectively the explicit writer-selected target of rejected option 5A, not 5C's version-derived target.

Required repair: for `ADMISSION_WITHHELD_CAPACITY`, derive the purpose only from `check_set_version` and refuse zero or multiple matches; a supplied purpose must not turn an ambiguous version into an accepted target. Add a permanent counterfactual covering the duplicated-version registry both with and without a supplied purpose.

### N-1 — NIT — external G1 amendment identity in the review brief is stale

**Location:** `C:/tmp/P031_LEAD_20260912/G1_SCOPE_AND_CONTRACT.md:79-80`.

The brief pins amended SHA-256 `c82de2a8...` and says no other sentence changed. The current file is `0bcd6abc...` because line 80 adds a later correction to the amendment log. The public seam spellings are correct, the pre-amendment identity is preserved, and no repository/protected path changed, so this is documentary and does not independently block M1.

## NOT VERIFIED

- Worktree cleanliness, staged state, branch/upstream status, and repository guard output were not verified because the launch instruction forbids `git status`, working-tree diff, and the guard's Git mutations/inspection route.
- Ruff cleanliness was not reproduced; Ruff is absent from the pinned environment.
- The one skipped focused-suite case was not made runnable on this Windows host.
- Accepted/current WP-P0-04 and WP-P0-13 provenance, owner-ratified real worthiness content, integration status, deployment, host state, and any authoritative/non-fixture producer remain outside this review.
- Commit author identity was not independently queried with disallowed Git metadata commands; the Lead-authorship disclosure is taken from the supplied brief/disposition, while the byte scope was independently verified.
- No prior Opus report or Lead adjudication of it was read, per the launch restriction.

VERDICT: REQUEST_CHANGES
