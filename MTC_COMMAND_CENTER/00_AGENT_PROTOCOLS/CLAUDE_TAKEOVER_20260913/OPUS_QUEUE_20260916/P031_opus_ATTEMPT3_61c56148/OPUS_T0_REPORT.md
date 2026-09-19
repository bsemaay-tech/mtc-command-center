# T0 review — WP-P0-31 M1, candidate `61c56148` (exact `claude-opus-5`, xhigh; THIRD read / T0 repair round 2 of 3)

Reviewer: exact `claude-opus-5` at xhigh effort, launched by
`C:/tmp/OPUS_QUEUE_20260916/P031/opus/run.ps1`, executing
`C:/tmp/OPUS_QUEUE_20260916/P031/opus/BRIEF.md` →
`C:/tmp/OPUS_QUEUE_20260916/P031/REVIEW_BRIEF.md` including the 2026-09-16
(round 1) and 2026-09-17 (round 2) addenda and the N-7 amendment note.
No delegation, no sub-agents, no resumed session. Date 2026-09-17.
Times UTC unless marked. Everything below was run by me from the pinned
interpreter; nothing is taken from another agent's report without a byte check.

Scratch root for every RED arm and mutant: `C:/tmp/OPUS_P031_SCRATCH/r3/`.
The repository was never mutated: no `git status`, `add`, `commit`, `checkout`,
`stash`. `git show` / `rev-parse` / `cat-file` were used for bytes;
**disclosed:** I additionally used `git diff --stat` and
`git diff --word-diff` restricted to named paths for the two documentation
edits and the file-set check (the brief permits this with disclosure), and
`git show <rev> --stat` for per-commit shapes.

---

## 1. Verified identities (COMPUTED by me)

| Item | Value | How |
|---|---|---|
| Worktree HEAD | `61c56148d76aa71424f7b3c0ffa69a14d9e702fe` | `git -c safe.directory=* -C C:/tmp/P031_M1_20260913 rev-parse HEAD` |
| HEAD subject | `test(p031): fence the OD-7 refresh-path identity guards (T0 repair round 2)` | `git show 61c56148 --stat --oneline` |
| Ledger blob OID | `7e7874770dc880aacb9bd8fcc6917c8416a7ce6a` | `git rev-parse 61c56148:MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py` |
| Ledger blob sha256 | `2bff9fcc1fc42c7780a7e40bb127f0dad79fe64dd3b17ee14d5337332f88a63d` | `git cat-file blob … | sha256sum` (raw, via Git Bash) |
| Ledger **checkout** sha256 | `81eedf03b79289dce92019a16a56e21ed9612be8cca16660d1b79095cb7ab816` | `sha256sum` of the working-tree file |
| Tests blob OID | `c72452f687c6feef250b4dc87a1625fe3668e108` | `git rev-parse 61c56148:…/tests/test_p031_lifecycle_ledger.py` |
| Tests blob sha256 = checkout sha256 | `5f4bef27393821cc4ec8da7301fb5ff1379da5c4357c5f76d8008339f7904675` | both computed |
| Ledger line count / test line count | 1495 / 5303 | `wc -l` |

Both blob OIDs match the ones the 2026-09-17 addendum pins. **N-11 independently
confirmed:** `file` reports the ledger checkout as *"Python script, ASCII text
executable, with CRLF, LF line terminators"* — mixed — which is why the checkout
hash `81eedf03…` differs from the blob hash `2bff9fcc…`; the test file is pure LF
so its two hashes coincide. I verified the checkout is byte-identical to the blob
modulo `\r`:
`diff <(tr -d '\r' < ledger_blob.py) <(tr -d '\r' < <worktree ledger>)` → empty.

**The ledger is unchanged since `bd0d56d0`:** `git show bd0d56d0:<ledger>` hashes
to the same `2bff9fcc…`. So the ledger bytes I review are the ones `bd0d56d0`
froze, and rounds 1 and 2 are test-only.

**Diff shape of the candidate commit** (`git show 61c56148 --stat`):

```
 .../tools/tests/test_p031_lifecycle_ledger.py      | 160 ++++++++++++++++++++-
 1 file changed, 158 insertions(+), 2 deletions(-)
```

One file, the test file, +158/−2. The −2 is the round-1 test's docstring
(N-12 fix: "Lane-3" → "Lane-1", and the guard named by its refusal code instead
of `:832-833`). **No ledger change in this commit — confirmed against bytes.**

---

## 2. Mandated command runs (all executed by me)

Interpreter: `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe`
→ `Python 3.12.12`.

| # | Command | cwd | Observed |
|---|---|---|---|
| R1 | `python -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py -q -p no:cacheprovider` | `C:/tmp/P031_M1_20260913` | `112 passed, 1 skipped, 167 subtests passed in 18.73s` |
| R2 | `python -m pytest tests -q -p no:cacheprovider` | `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/contracts` | `50 passed in 0.30s` |
| R3 | R1 with `-rs` | worktree root | skip reason = `file symlinks unavailable on this host: [WinError 1314] …` — the known host-privilege skip |
| R4 | `ruff check <ledger> <tests>` (`ruff 0.16.4`, `C:/tmp/wp_p0_04_tooling_20260825/Scripts/ruff.exe`) | worktree root | `Found 47 errors.` → ledger 11, tests 36 (see §10) |

The counts the Lead recorded reproduce exactly. **N-9 confirmed and used:** the
contracts suite is only collectable from `MTC_COMMAND_CENTER/contracts`; I ran it
there, per the round-1 addendum.

I could execute every mandated command, so BLOCK does not apply.

---

## 3. F-2 — my own mutants of `:812-813` and `:814-816`

Harness (mine, not the Lead's): a mirror of `MTC_COMMAND_CENTER/03_QUANTLENS/tools`
(the two files) plus `MTC_COMMAND_CENTER/contracts` under
`C:/tmp/OPUS_P031_SCRATCH/r3/mut`, so the tests' `Path(__file__).parents[…]`
resolution works unchanged. Baseline in the mirror before mutating:
`112 passed, 1 skipped, 167 subtests passed`. Mutator
(`C:/tmp/OPUS_P031_SCRATCH/r3/mutate.py`) refuses unless the first dropped line
matches an expected string, so a silent off-by-one cannot manufacture a mutant;
it always rebuilds from a pristine copy (`ledger_pristine.py`).

### M-A — remove `p031_lifecycle_ledger.py:812-813`

```
DROPPING lines 812 - 813
  -812:                     if deployment_hash in retired_deployments:
  -813:                         raise ValueError("DEPLOYMENT_IDENTITY_RETIRED")
```
`python -m pytest … -q -p no:cacheprovider` (cwd = mirror):

```
>       with self.assertRaisesRegex(ValueError, "DEPLOYMENT_IDENTITY_RETIRED"):
E       AssertionError: ValueError not raised
…test_p031_lifecycle_ledger.py:2741: AssertionError
FAILED …::LifecycleLedgerTests::test_registrar_refresh_cannot_adopt_the_candidates_own_retired_identity
1 failed, 111 passed, 1 skipped, 167 subtests passed in 18.17s
```

### M-B — remove `p031_lifecycle_ledger.py:814-816`

```
DROPPING lines 814 - 816
  -814:                     owner = deployment_owners.get(deployment_hash)
  -815:                     if owner is not None and owner != event.candidate_id:
  -816:                         raise ValueError("DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE")
```

```
>       with self.assertRaisesRegex(
            ValueError, "DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE"
        ):
E       AssertionError: ValueError not raised
…test_p031_lifecycle_ledger.py:2790: AssertionError
FAILED …::LifecycleLedgerTests::test_registrar_refresh_cannot_adopt_another_candidates_identity
1 failed, 111 passed, 1 skipped, 167 subtests passed in 18.14s
```

### Restore

```
RESTORED from C:\tmp\OPUS_P031_SCRATCH\r3\ledger_pristine.py
81eedf03b79289dce92019a16a56e21ed9612be8cca16660d1b79095cb7ab816  (hash back to the checkout bytes)
112 passed, 1 skipped, 167 subtests passed in 20.28s
```

**Each mutant fails exactly its own new test and nothing else. Both F-2 guards
are now fenced.** This is the criterion the round-2 addendum set, met on my own
mutants rather than on the Lead's.

### Guard walk — does each test reach the intended guard?

Traced against the bytes and corroborated by *how* each mutant failed
(`ValueError not raised`, i.e. the append was accepted, not diverted to another
refusal).

**Retired-identity test** (`test_…own_retired_identity`). Setup through the
public route only: `build_to_rung(… "SHADOW_ELIGIBLE")` → SHADOW under
`PACKAGE_A`/`DEPLOYMENT_A`; supervisor `RETIRED` (so `retired_deployments ∋
DEPLOYMENT_A` at `:1125-1126` and `retired_packages[cid] ∋ PACKAGE_A` at
`:1127-1130`); registrar `RE_ENTRY` with `OWNER_EXTERNAL_CHANGE` + a
one-sentence reason (`:840-841` returns `(None, None)`, clearing both
identities); registrar `FROZEN` under `PACKAGE_B` (first freeze — `:817-818`
requires no deployment identity, and `:819-820` does not fire because
`PACKAGE_B ∉ {PACKAGE_A}`); admission to SHADOW under `PACKAGE_B`/`DEPLOYMENT_B`.
Then the hostile refresh SHADOW→FROZEN naming `PACKAGE_B`/`DEPLOYMENT_A`:

* `:669-674` `is_registrar_refresh` = True (REGISTRAR, `FROZEN`, actual state SHADOW).
* `:805-811` `DEPLOYMENT_REFRESH_IDENTITY_INVALID` does **not** fire: identity
  given, `current` present, `package_hash == current["package_hash"]`
  (`PACKAGE_B == PACKAGE_B`), and `deployment_hash != current[…]`
  (`DEPLOYMENT_A != DEPLOYMENT_B`). Package equality and identity inequality
  both hold, as the addendum requires.
* `:812-813` fires → `DEPLOYMENT_IDENTITY_RETIRED`.
* On M-A the refusal is not rescued downstream: `:814-816` sees
  `deployment_owners[DEPLOYMENT_A] == this candidate` (set at `:1123-1124`
  while the candidate held it), so the ownership guard is silent; and
  `:819-820` `RETIRED_PACKAGE_IDENTITY` is silent because the candidate was
  re-frozen under `PACKAGE_B`, not the retired `PACKAGE_A`. Hence the mutant
  **accepts** — which is precisely what the observed
  `AssertionError: ValueError not raised` shows.

**Foreign-identity test** (`test_…another_candidates_identity`). `CANDIDATE_B`
to SHADOW under `PACKAGE_B`/`DEPLOYMENT_B`; `CANDIDATE_A` to SHADOW under the
defaults `PACKAGE_A`/`DEPLOYMENT_A`; then A's refresh naming
`PACKAGE_A`/`DEPLOYMENT_B`. `:805-811` silent (package equal, identity differs),
`:812-813` silent (`DEPLOYMENT_B` was never retired), `:814-816` fires because
`deployment_owners[DEPLOYMENT_B] == CANDIDATE_B ≠ CANDIDATE_A`. On M-B nothing
else refuses and two candidates end up sharing one deployment identity.

### Does each test assert the whole invariant?

| Obligation | Retired-identity test | Foreign-identity test |
|---|---|---|
| refusal with the exact code | `assertRaisesRegex(ValueError, "DEPLOYMENT_IDENTITY_RETIRED")` | `assertRaisesRegex(ValueError, "DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE")` |
| state unchanged | `observed_state(state) == "SHADOW"` after the refusal | `"SHADOW"` for **both** candidates |
| package unchanged | `state["package_hash"] == PACKAGE_B` | `PACKAGE_A` (claimant) and `PACKAGE_B` (holder) |
| identity unchanged | `state["deployment_identity_hash"] == DEPLOYMENT_B` | `DEPLOYMENT_A` (claimant) and `DEPLOYMENT_B` (holder) |
| replay carries no refresh record | FROZEN event ids for the candidate `== ["refresh-retired-frozen", "refresh-retired-refreeze"]` | FROZEN event ids across **all** candidates `== ["refresh-foreign-holder-frozen", "refresh-foreign-claimant-frozen"]` |

Both read state through `current_state()` (which re-verifies the whole history
in one snapshot via `_verified_snapshot`) and through `replay()`, not through the
derived view alone — so a record that had been committed and then merely
mis-projected would still be caught. The foreign case asserts **both**
candidates, as the addendum required.

**Could either pass for the wrong reason?** No. Each regex names a code that,
for a REGISTRAR `FROZEN` event, can only come from the guard under test:
`DEPLOYMENT_IDENTITY_RETIRED` also exists at `:835` and
`DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE` at `:838`, but both are inside
the `else` branch at `:823` that only non-REGISTRAR writers reach, and
`Registrar.append` (`:1384-1401`) refuses anything whose `writer_class` is not
`REGISTRAR`. Positively: on the mutant the append is **accepted** (not diverted
to a different refusal), so the test is measuring the guard and not a
neighbouring one. The pre-refusal assertions also pin that the scaffolding
really reached SHADOW under the new composite, so the test cannot pass by
failing early in setup.

---

## 4. F-1 re-check — `:832-833`

Round 1's finding stays closed. My own mutant:

```
DROPPING lines 832 - 833
  -832:             if current_deployment is not None and deployment_hash != current_deployment:
  -833:                 raise ValueError("DEPLOYMENT_IDENTITY_MISMATCH")
…
FAILED …::LifecycleLedgerTests::test_post_refresh_admission_cannot_reuse_the_revoked_deployment_identity
1 failed, 111 passed, 1 skipped, 167 subtests passed in 26.74s
```

Exactly the round-1 test, nothing else. I also reproduced the live invariant
outside the suite (arm **G4**, §6): after a refresh to `DEPLOYMENT_B`, an
admission re-citing `DEPLOYMENT_A` is refused `DEPLOYMENT_IDENTITY_MISMATCH`.

---

## 5. Answer conformance, item by item

Authority checked against bytes: `C:/CT13/DECISIONS.md:83`
(`OD-20260914-P031-LIFECYCLE-1`, owner words *"Q5 all recommended"*, the twelve
answers listed explicitly) and `:91` (`OD-20260914-P031-BATCH-GO-1`). Option
text quoted from `P031_LIFECYCLE_DECISIONS_20260913_V4.md` section 3 and the
sections it cites. Line numbers are the candidate's.

| Answer | Packet option text (quoted) | Implementation (file:line) | Verdict |
|---|---|---|---|
| **OD-1 = 3D** | *"move 'ratified worthiness version' from an M1 acceptance precondition to an operating precondition on writing a real `CAPTURED -> TRIAGED` record"*; *"No code change"* | `DECISIONS.md:18` — the phrase *"an owner-ratified worthiness check-set version"* removed from **both** acceptance lists and replaced by *"an owner-ratified worthiness check-set version is instead an operating precondition for writing any real `CAPTURED -> TRIAGED` record"* and *"A real `CAPTURED -> TRIAGED` write remains blocked until the owner ratifies an exact active worthiness check-set version."*; the same move at `11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:298`. Word-diff verified; no executable byte. The guard itself is untouched (`:736-740`, still fail-closed with an empty registry). | **IMPLEMENTED-AS-ANSWERED** |
| **OD-2 = 1B** | *"the writer supplies `next_state`; the ledger validates strict descent on the ladder order … and an unchanged `deployment_identity_hash`. Assign `DEMOTED` to `MULTI_WORKER_SUPERVISOR`."* | `LADDER_RANK` `:42`; strict descent `:688-693` → `DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT`; authority `:121-123` gains `"DEMOTED"`; the six strictly-below tuples and no others at `:134-139` (TESTNET→SHADOW; LC→SHADOW, LC→TESTNET; LIVE→SHADOW, LIVE→TESTNET, LIVE→LC — from SHADOW nothing, correctly absent); unchanged identity enforced by `:675-686` `DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED` (my arm **C4**) with `:832-833` behind it. Wrong-authority `DEMOTED` refused `WRITER_AUTHORITY_REFUSED` (arm **C5**). | **IMPLEMENTED-AS-ANSWERED** |
| **OD-3 = 2A** | *"add a nullable challenged-incumbent identity field … under WP-P0-04; keep `CHALLENGE` fail-closed until it exists."* | `:657-658` still raises `CHALLENGE_INCUMBENT_DEPLOYMENT_IDENTITY_FIELD_MISSING` before anything else; the report keeps `"CHALLENGE INCUMBENT DEPLOYMENT IDENTITY FIELD: MISSING"` as the sole `unresolved_lifecycle_contracts` entry (`:1451-1453`). No shared-contract change. | **IMPLEMENTED-AS-ANSWERED** (stays UNRESOLVED as the brief requires) |
| **OD-4 = 3D now** | *"ratify the current repository-wide refusal as the deliberate interim"*; *"Owner's word only, now."* | Behaviour unchanged: `:710-721` `SUCCESSION_ENVELOPE_UNRESOLVED`. Recording only: `"ATOMIC SUCCESSION INTERIM REFUSAL: RATIFIED BY OD-4"` moved into the new `ratified_lifecycle_contracts` list (`:1456`) and the old `"…: UNRESOLVED"` string removed. | **IMPLEMENTED-AS-ANSWERED** (recording only) |
| **OD-5 = 4A** | *"`REJECTED` carries an explicit writer-supplied `check_set_purpose` drawn from the declared set …, validated against the candidate's current rung, with `check_set_version`, `evaluation_run_hash` and non-empty `failing_checks` all mandatory. Restore `("REJECTED", "RE_ENTRY", "CANDIDATE")`."* | `check_set_purpose` parameter `:855`; unknown purpose `:614-618`; required for REJECTED `:619-622`; rung validation `REJECTED_PURPOSES_BY_RUNG` `:49-60` + `:728-731`; hash mandatory `:773-775`; non-empty failing checks `:776-777`; the seven `→ REJECTED` registrar arcs `:70-76`; `("REJECTED","RE_ENTRY","CANDIDATE")` restored `:82`. All six of my D-arms refuse exactly as specified. | **IMPLEMENTED-AS-ANSWERED** |
| **OD-6 = 5C** | *"take the target from the supplied `check_set_version`'s purpose instead of inferring it from `previous_state`"* | `_purpose_for_check_set_version` `:596-606`; `_resolve_check_set_purpose` for `ADMISSION_WITHHELD_CAPACITY` `:623-626`; `("SHADOW","ADMISSION_WITHHELD_CAPACITY","SHADOW")` added `:133`; `CAPACITY_PURPOSES_BY_RUNG` `:43-48` + `:724-727`. `_check_set_purpose`'s old `previous_state` branch is deleted (diff line 205-206). Arms **E1/E2** refuse, **E3** (writer names the paper gate at SHADOW) is accepted — the case 5C exists to allow. | **IMPLEMENTED-AS-ANSWERED**; the rung restriction at `:724-727` is one constraint beyond 5C's sentence, but it is fail-closed and is what "the target of *this* rung's withheld admission" requires — see N-18 for the one residual (N-4). |
| **OD-7 = 6A** | *"the candidate returns to `FROZEN` under the new `deployment_identity_hash`, and revocation is expressed by the absence of admission records for that new identity. Prior windows stay readable and never count."* + *"Requires one decided transition (deep rung -> `FROZEN`, same candidate, new composite) and a relaxation of `ledger:657-658`"* | Five deep-rung→FROZEN registrar arcs `:77-81`; `is_registrar_refresh` `:669-674`; the relaxation and its well-formedness guard `:804-811`; retired-identity `:812-813`; foreign-identity `:814-816`; first-freeze forbidden identity preserved in the `elif` `:817-818`; revocation by absence enforced at `:832-833` (a post-refresh admission must carry the new identity; the candidate sits at FROZEN until re-admitted). Prior events stay in `replay()` — asserted by both new tests. | **IMPLEMENTED-AS-ANSWERED**, with two scope notes (N-18, N-13/N-10) |
| **OD-8 = 7A** | *"ratify as implemented: one `evaluation_run_hash` binds to exactly one `candidate_id` forever."*; *"No code change."* | Behaviour unchanged: `:784-790` `EVALUATION_RUN_CANDIDATE_SCOPE_UNRESOLVED` at both seams (arm **F2** refuses). Recording only: `"EVALUATION RUN CANDIDATE SCOPE: RATIFIED BY OD-8"` `:1460`. | **IMPLEMENTED-AS-ANSWERED** (recording only) |
| **OD-9 = 5a-C** | *"gate it on a **sixth, owner-only trigger class** distinct from the five automatic ones, with a mandatory recorded one-sentence external-change reason, and keep every existing constraint"* | `"OWNER_EXTERNAL_CHANGE"` added `:95`; `_is_one_sentence` `:261-265`; RETIRED re-entry gate `:758-764` → `RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED`; **and the distinctness requirement in both directions** — `:765-766` refuses `OWNER_EXTERNAL_CHANGE` from any non-RETIRED state, so the sixth class cannot leak into the funnel five. Existing constraints kept: fresh hash `:767-770`, no prior evidence `:771-772`, identities cleared `:840-841`, retired package/deployment permanently refused `:819-820` / `:812-813` / `:834-835`. Arms **B1-B5** all refuse. | **IMPLEMENTED-AS-ANSWERED** |
| **OD-10 = 5b-A** | *"ratify the implemented rule … conditional on giving `test:2192-2288` real assertions and closing the report's disclosure gap"* | Behaviour unchanged (arm **F1** accepted; cross-epoch **F3** and cross-candidate **F2** refused). Condition 1 met: `test_current_epoch_evaluation_may_support_multiple_decisions` (`:2278`) now pins, for all three ledgers, the `(event_type, check_set_purpose, check_set_version, evaluation_run_hash)` of the last two replayed records and the resulting `current_state` (`:2375-2430+`) — not merely `verify_integrity()`. Condition 2 met by recording: `"SAME-EPOCH EVALUATION REUSE: RATIFIED BY OD-10"` `:1461`. | **IMPLEMENTED-AS-ANSWERED** (both conditions satisfied) |
| **OD-11 = 2C** | *"M1 keeps the opaque field, plus an optional configured catalog: when an accepted catalog is supplied, an `evaluation_run_hash` absent from it is refused; when none is supplied, the ledger fails closed on any record that claims catalog-backed evidence."* Packet: *"The phrase 'claims catalog-backed evidence' is undefined here … read at its widest … it would refuse every non-Registrar ladder append"* | `accepted_evaluation_catalog` constructor parameter `:326`, validated `:392-403`; `catalog_backed: bool = False` on `append` `:856`, exact-bool gate `:556-557`; the three refusals `:744-745`, `:746-747`, `:748-753`; the flag carried into canonical evidence `:246`, the replay key set `:1041`, the record dataclass `:213`, and the report `:1429`; threaded through `backup_to` `:1305` and `restore_from` `:1324/:1336/:1343`. The undefined phrase is given the **narrowest** implementable reading — an explicit, default-`False`, writer-supplied opt-in — so the ladder is not broken, exactly as the packet warned the widest reading would. Arms **A1-A5** (including `catalog_backed=1`, `"true"`, `[1]`) all refuse. | **IMPLEMENTED-AS-ANSWERED** at the narrowest reading. Two notes: the owner never defined the phrase (the packet says so explicitly), so the engineering chose it — flagged as an owner-visible definition, not a deviation; and see **N-16** for the catalog's reach into the read seams. |
| **OD-12 = 7-A** | *"preserve; fold the refresh … into one new candidate and one T0 roster once OD-1..OD-11 are answered."* | `c76043b9` is preserved as an ancestor (diff `c76043b9..61c56148` resolves); the batch is four commits on the unmerged `feature/p031-m1-20260913-refresh`; no PR, no merge. Refresh preserved. | **IMPLEMENTED-AS-ANSWERED** |

Nothing is **BROADER THAN ANSWERED** in a way that admits a record the answers
refuse. The two places where the implementation is *stricter* than the option
text — the capacity rung restriction (OD-6) and the refresh requiring an
unchanged `package_hash` (OD-7) — both fail closed; the OD-7 one is recorded as
N-18.

---

## 6. Fail-open hunt and my own RED arms

Harness: `C:/tmp/OPUS_P031_SCRATCH/r3/red_arms.py`, written by me, using only
the public seams (`LifecycleLedger.append`, `Registrar.append`,
`current_state`, `replay`, `verify_integrity`, `render_status_report`,
`backup_to`) and its own event builders (not the suite's fixtures, so a broken
fixture cannot mask a hole). Each arm builds a fresh ledger, drives it to the
required state through the public route, makes **one** hostile append, and
prints the exact refusal or `APPENDED (FAIL-OPEN)`.

Run: `python red_arms.py C:/tmp/OPUS_P031_SCRATCH/r3/cand`
(candidate module, sha256 `81eedf03…`).

```
A. OD-11 catalog arms
  [REFUSED-AS-REQUIRED] A1 registrar refresh claims catalog-backed with NO evaluation hash (catalog configured)
      expected=CATALOG_BACKED_WITHOUT_EVALUATION_HASH  observed=ValueError: CATALOG_BACKED_WITHOUT_EVALUATION_HASH
  [REFUSED-AS-REQUIRED] A2 registrar TRIAGED-path claim: CAPTURED->TRIAGED catalog-backed, no hash
      expected=CATALOG_BACKED_WITHOUT_EVALUATION_HASH  observed=ValueError: CATALOG_BACKED_WITHOUT_EVALUATION_HASH
  [REFUSED-AS-REQUIRED] A3 ladder admission cites a hash OUTSIDE the configured catalog
      expected=EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG  observed=ValueError: EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG
  [REFUSED-AS-REQUIRED] A4 catalog-backed claim with NO catalog configured
      expected=CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG  observed=ValueError: CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG
  [REFUSED-AS-REQUIRED] A5 coerced catalog_backed=int 1 must not slip past the bool gate
      expected=CATALOG_BACKED_INVALID  observed=ValueError: CATALOG_BACKED_INVALID
  [REFUSED-AS-REQUIRED] A5 coerced catalog_backed=str 'true' must not slip past the bool gate
      expected=CATALOG_BACKED_INVALID  observed=ValueError: CATALOG_BACKED_INVALID
  [REFUSED-AS-REQUIRED] A5 coerced catalog_backed=list [1] must not slip past the bool gate
      expected=CATALOG_BACKED_INVALID  observed=ValueError: CATALOG_BACKED_INVALID

B. OD-9 RETIRED -> RE_ENTRY arms
  [REFUSED-AS-REQUIRED] B1 RE_ENTRY from RETIRED with an automatic trigger
      expected=RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED  observed=ValueError: RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED
  [REFUSED-AS-REQUIRED] B2 RE_ENTRY from RETIRED with NO trigger
      expected=REENTRY_TRIGGER_INVALID  observed=ValueError: REENTRY_TRIGGER_INVALID
  [REFUSED-AS-REQUIRED] B3 RE_ENTRY from RETIRED with a TWO-sentence reason
      expected=RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED  observed=ValueError: RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED
  [REFUSED-AS-REQUIRED] B4 RE_ENTRY from RETIRED with an unterminated reason (no . ! ?)
      expected=RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED  observed=ValueError: RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED
  [REFUSED-AS-REQUIRED] B5 OWNER_EXTERNAL_CHANGE used from a NON-retired state (PARKED)
      expected=REENTRY_TRIGGER_INVALID  observed=ValueError: REENTRY_TRIGGER_INVALID

C. OD-2 DEMOTED arms
  [REFUSED-AS-REQUIRED] C1 DEMOTED sideways TESTNET->TESTNET
      expected=DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT  observed=ValueError: DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT
  [REFUSED-AS-REQUIRED] C2 DEMOTED upward TESTNET->LIVE
      expected=DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT  observed=ValueError: DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT
  [REFUSED-AS-REQUIRED] C3 DEMOTED off-ladder LIVE_CANDIDATE->FROZEN
      expected=DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT  observed=ValueError: DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT
  [REFUSED-AS-REQUIRED] C4 DEMOTED down a rung but under a CHANGED deployment identity
      expected=DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED  observed=ValueError: DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED
  [REFUSED-AS-REQUIRED] C5 DEMOTED issued by the ADMISSION authority instead of the supervisor
      expected=WRITER_AUTHORITY_REFUSED  observed=ValueError: WRITER_AUTHORITY_REFUSED

D. OD-5 REJECTED arms
  [REFUSED-AS-REQUIRED] D1 REJECTED with an EMPTY failing_checks list
      expected=FAILING_CHECKS_REQUIRED  observed=ValueError: FAILING_CHECKS_REQUIRED
  [REFUSED-AS-REQUIRED] D2 REJECTED with NO evaluation_run_hash
      expected=EVALUATION_RUN_HASH_REQUIRED  observed=ValueError: EVALUATION_RUN_HASH_REQUIRED
  [REFUSED-AS-REQUIRED] D3 REJECTED with NO check_set_purpose
      expected=CHECK_SET_PURPOSE_REQUIRED  observed=ValueError: CHECK_SET_PURPOSE_REQUIRED
  [REFUSED-AS-REQUIRED] D4 REJECTED at FROZEN naming the WRONG rung's purpose ('promotion')
      expected=CHECK_SET_PURPOSE_MISMATCH  observed=ValueError: CHECK_SET_PURPOSE_MISMATCH
  [REFUSED-AS-REQUIRED] D5 REJECTED naming a purpose that is not in the declared set
      expected=CHECK_SET_PURPOSE_UNKNOWN  observed=ValueError: CHECK_SET_PURPOSE_UNKNOWN
  [REFUSED-AS-REQUIRED] D6 REJECTED whose check_set_version belongs to another purpose
      expected=CHECK_SET_PURPOSE_MISMATCH  observed=ValueError: CHECK_SET_PURPOSE_MISMATCH

E. OD-6 ADMISSION_WITHHELD_CAPACITY arms
  [REFUSED-AS-REQUIRED] E1 capacity withheld at SHADOW naming the FROZEN gate's version
      expected=ADMISSION_WITHHELD_TARGET_UNRESOLVED  observed=ValueError: ADMISSION_WITHHELD_TARGET_UNRESOLVED
  [REFUSED-AS-REQUIRED] E2 capacity withheld at SHADOW with NO check_set_version at all
      expected=CHECK_SET_REQUIRED  observed=ValueError: CHECK_SET_REQUIRED
  [APPENDED (FAIL-OPEN)] E3 capacity withheld at SHADOW: writer names paper_eligibility, version is paper
      expected=(this arm is expected to be ACCEPTED under 5C)  observed=NO REFUSAL

F. OD-10 / OD-8 evaluation-run arms
  [APPENDED (FAIL-OPEN)] F1 same-epoch reuse of one run across two purposes (OD-10 5b-A: ALLOWED)
      expected=(this arm is expected to be ACCEPTED under 5b-A)  observed=NO REFUSAL
  [REFUSED-AS-REQUIRED] F2 cross-candidate reuse of one run (OD-8 7A: refused)
      expected=EVALUATION_RUN_CANDIDATE_SCOPE_UNRESOLVED  observed=ValueError: EVALUATION_RUN_CANDIDATE_SCOPE_UNRESOLVED
  [REFUSED-AS-REQUIRED] F3 RE_ENTRY citing a run already used in the retired epoch
      expected=REENTRY_EVALUATION_NOT_FRESH  observed=ValueError: REENTRY_EVALUATION_NOT_FRESH

G. OD-7 refresh arms
  [REFUSED-AS-REQUIRED] G1 refresh that changes the PACKAGE hash as well
      expected=DEPLOYMENT_REFRESH_IDENTITY_INVALID  observed=ValueError: DEPLOYMENT_REFRESH_IDENTITY_INVALID
  [REFUSED-AS-REQUIRED] G2 refresh naming the SAME deployment identity (a no-op refresh)
      expected=DEPLOYMENT_REFRESH_IDENTITY_INVALID  observed=ValueError: DEPLOYMENT_REFRESH_IDENTITY_INVALID
  [REFUSED-AS-REQUIRED] G3 refresh carrying NO deployment identity at all
      expected=DEPLOYMENT_REFRESH_IDENTITY_INVALID  observed=ValueError: DEPLOYMENT_REFRESH_IDENTITY_INVALID
  [REFUSED-AS-REQUIRED] G4 post-refresh admission that re-cites the REVOKED identity (F-1 invariant)
      expected=DEPLOYMENT_IDENTITY_MISMATCH  observed=ValueError: DEPLOYMENT_IDENTITY_MISMATCH
  [APPENDED (FAIL-OPEN)] G5 SECOND refresh back to the previously revoked identity (N-13)
      expected=(no refusal exists today — N-13 owner question)  observed=NO REFUSAL
```

The harness prints `APPENDED (FAIL-OPEN)` for *any* acceptance; three arms were
written deliberately to be accepted and are **not** defects:

* **E3** is the case OD-6 (5C) exists to permit — the writer names the gate whose
  slot is full and the ledger reads the target from that version.
* **F1** is the rule OD-10 (5b-A) ratifies — same-epoch reuse across purposes.
* **G5** is **N-13**, independently reproduced: after A→B, re-admission under B
  and then a second refresh B→A is accepted, so OD-7's revocation is reversible.
  No refusal exists today; the Lead's disposition (owner question, with N-10) is
  the right one and I re-raise it as a NIT, not a defect.

Everything the brief named is covered: registrar refresh with
`catalog_backed=True` and no hash (**A1**), a hash outside the catalog (**A3**),
a RETIRED `RE_ENTRY` without the owner trigger (**B1/B2**) and with a
two-sentence reason (**B3**), `DEMOTED` sideways and upward (**C1/C2**), a
`REJECTED` without failing checks (**D1**), same-epoch reuse across purposes
(**F1**), and coerced `catalog_backed` (`1`, `"true"`, `[1]` — **A5**).

**Writer-class routing.** `Registrar.append` (`:1384-1401`) re-validates the
event and refuses unless `writer_class is LifecycleWriterClass.REGISTRAR` and
`event.writer_id == self.writer_id`; `_validate_transition` then gates every
event type by `AUTHORITY_EVENTS[writer_class]` (`:662-663`). The one structural
property worth naming: `LifecycleLedger.append` is itself public, so a caller
holding an allowlisted `(writer_class, writer_id)` pair may write as that class
directly — that is the allowlist's designed semantics and predates this batch
(`c76043b9`), not a change introduced here.

**Replay-seam symmetry.** `_validate_transition` is the same function at append
(`enforce_active=True`, `:946`) and at replay (`enforce_active=False`, `:1103`),
so all the new refusals also fail closed when reading a hand-edited database;
`catalog_backed` is inside the canonical evidence bytes (`:246`), the exact
six-key evidence set (`:1037-1045`), the re-normalisation (`:1052-1058`) and the
byte-equality check (`:1061-1065`), so it cannot be flipped in storage without
`NONCANONICAL_PAYLOAD` or the transition refusal. See **N-16** for the one
consequence of that symmetry that is worth the owner's attention.

---

## 7. D026 evidence — RED on the pre-fix behaviour

I produced this two independent ways.

### 7a. Guard-removal sweep (23 refusals, one mutant each, whole suite each time)

`C:/tmp/OPUS_P031_SCRATCH/r3/sweep.py`: for each refusal the delta added or
re-shaped, replace exactly that `raise` with `pass` at the same indentation
(anchor-checked, always rebuilt from the pristine copy), run the whole suite,
record which tests fail, then restore. This is a stronger form of the brief's
question than "run the new tests on the old module", because the rest of the
module stays intact, so a test cannot appear RED "for the wrong reason" via an
earlier refusal — the exact failure mode the Lead found in the builder's J-03
arm.

| Mutant | Guard | Rule | Suite | Fenced by |
|---|---|---|---|---|
| G01 | `:693` | OD-2 strict descent | 1 failed / 111 passed | `test_demoted_requires_strict_descent_and_keeps_deployment_identity` |
| G02 | `:727` | OD-6 capacity target by rung | 1 / 111 | `test_admission_record_types_materialize_only_canonical_states` |
| G03 | `:731` | OD-5 REJECTED purpose by rung | 1 / 111 | `test_rejected_requires_purpose_hash_and_failing_checks` |
| G04 | `:745` | OD-11 no catalog configured | 1 / 111 | `test_catalog_backed_claim_fails_closed_without_catalog` |
| G05 | `:747` | OD-11 catalog-backed w/o hash (J-03) | 2 / 110 | `test_configured_catalog_refuses_absent_hash_and_accepts_present_hash`, `test_registrar_refresh_with_catalog_backed_claim_requires_evaluation_hash` |
| G06 | `:753` | OD-11 hash outside catalog | 1 / 111 | `test_configured_catalog_refuses_absent_hash_and_accepts_present_hash` |
| G07 | `:762-764` | OD-9 RETIRED re-entry trigger+reason | 2 failed subtests (165/167) | subtests of the lifecycle matrix |
| G08 | `:766` | OD-9 sixth class only from RETIRED | 1 / 111 | `test_retired_reentry_requires_owner_external_change_reason` |
| G09 | `:775` | OD-5 REJECTED needs a hash | 3 (incl. subtests) | `test_rejected_requires_purpose_hash_and_failing_checks` |
| G10 | `:777` | OD-5 REJECTED needs failing checks | 2 | same |
| G11 | `:811` | OD-7 refresh well-formed | 4 | `test_deployment_refresh_returns_to_frozen_under_new_composite` |
| **G12** | **`:813`** | **OD-7 refresh onto a retired identity (F-2 C1)** | **1 / 111** | **`test_registrar_refresh_cannot_adopt_the_candidates_own_retired_identity`** |
| **G13** | **`:816`** | **OD-7 refresh onto a foreign identity (F-2 C2)** | **1 / 111** | **`test_registrar_refresh_cannot_adopt_another_candidates_identity`** |
| **G14** | **`:833`** | **OD-7 post-refresh revocation (F-1)** | **1 / 111** | **`test_post_refresh_admission_cannot_reuse_the_revoked_deployment_identity`** |
| G15 | `:557` | OD-11 `catalog_backed` exact bool | 4 failed subtests (163/167) | subtest arms |
| G16 | `:402` | OD-11 catalog constructor validation | 3 failed subtests (164/167) | subtest arms |
| **G17** | **`:618`** | **OD-5 supplied purpose must be a declared one** | **112 passed / 167 subtests — fully green** | **nothing (see N-14)** |
| G18 | `:621` | OD-5 REJECTED purpose required | 1 / 111 | `test_rejected_purpose_and_stale_evaluation_fail_closed` |
| **G19** | **`:629`** | **OD-5 supplied purpose must equal the fixed one** | **112 passed / 167 subtests — fully green** | **nothing (see N-15)** |
| G20 | `:818` | first freeze carries no identity | 1 / 111 | `test_identity_depth_is_exact_before_freeze_and_through_tail` |
| G21 | `:820` | retired package cannot be re-frozen | 1 / 111 | `test_retired_package_cannot_be_refrozen_after_reentry` |
| G22 | `:835` | ladder writer onto a retired identity | 1 / 111 | `test_retired_candidate_reenters_with_new_package_but_not_retired_deployment` |
| G23 | `:838` | ladder writer onto a foreign identity | 1 failed subtest (166/167) | subtest arm |

**21 of 23 fenced; 2 not** (`:618`, `:629`). Note on method: my first pass
mis-classified G07/G15/G16/G23 as unfenced because I was parsing `FAILED` lines
only and `pytest-subtests` reports subtest failures differently; the summary
lines (`N failed, 112 passed, 1 skipped, <167 subtests`) show the failures, and
I corrected the reading rather than reporting them as holes. G17 and G19 are the
only two whose mutants leave the suite *completely* green
(`112 passed, 1 skipped, 167 subtests passed`).

**I did not stop at "unfenced".** For F-1 and F-2 the previous reads' REQUIRED
severity came from a demonstrated **fail-open** — the mutant *accepted* a record
that violates a lifecycle invariant. I tested whether `:618` and `:629` do the
same (`C:/tmp/OPUS_P031_SCRATCH/r3/unfenced_probe.py`, which also prints the
`check_set_purpose` actually persisted in canonical evidence):

```
=========== CANDIDATE (unmutated) ===========
  REFUSED  P1 REJECTED with check_set_purpose='rejection' (not a declared purpose)  -> CHECK_SET_PURPOSE_UNKNOWN
  REFUSED  P2 REJECTED with a str-SUBCLASS purpose 'shadow_eligibility'             -> CHECK_SET_PURPOSE_UNKNOWN
  REFUSED  P3 SHADOW_ELIGIBLE claiming check_set_purpose='promotion'                -> CHECK_SET_PURPOSE_MISMATCH
  REFUSED  P4 purposeless registrar PARKED carrying check_set_purpose='promotion'   -> CHECK_SET_PURPOSE_MISMATCH

=========== MUTANT G17 (:618 -> pass) ===========
  REFUSED  P1  -> CHECK_SET_PURPOSE_MISMATCH          (re-routed to :731, still refused)
  APPENDED P2  -> stored check_set_purpose='shadow_eligibility'  check_set_version='shadow-eligibility.v1'
  REFUSED  P3  -> CHECK_SET_PURPOSE_MISMATCH
  REFUSED  P4  -> CHECK_SET_PURPOSE_MISMATCH

=========== MUTANT G19 (:629 -> pass) ===========
  REFUSED  P1  -> CHECK_SET_PURPOSE_UNKNOWN
  REFUSED  P2  -> CHECK_SET_PURPOSE_UNKNOWN
  APPENDED P3  -> stored check_set_purpose='shadow_eligibility'  check_set_version='shadow-eligibility.v1'
  APPENDED P4  -> stored check_set_purpose=None                 check_set_version=None
```

In **every** appended case the value actually persisted is the **truthful**
one — `_resolve_check_set_purpose` returns `fixed` (`:630`), so the writer's
false claim is discarded, not recorded. No mutant admits a record with a wrong
purpose, a wrong rung, a resurrected identity or a shared identity; no lifecycle
invariant is violated. These two are **strictness / loudness** guards: with them
a false claim is refused, without them it is silently ignored. I therefore
record them as NITs (N-14, N-15) and state the criterion I applied in §11 so the
Lead and Sol can overrule on a stated basis rather than on taste.

### 7b. Direct pre-fix reproduction (`96af3eb6`), for the one refusal `bd0d56d0` added

`git show 96af3eb6:<ledger>` (sha256 `2e54ee7b62abaca2c0851ccbd1398b485d3163ce5f93c98bf162cd6146fd3c7c`)
+ the candidate's tests + contracts, in
`C:/tmp/OPUS_P031_SCRATCH/r3/pre96`. The `96af3eb6 → bd0d56d0` ledger diff is
exactly the docstring plus the two lines at `:746-747`, so this isolates the
refusal precisely.

Whole suite on the pre-fix module:

```
FAILED …::LifecycleLedgerTests::test_configured_catalog_refuses_absent_hash_and_accepts_present_hash
FAILED …::LifecycleLedgerTests::test_registrar_refresh_with_catalog_backed_claim_requires_evaluation_hash
2 failed, 110 passed, 1 skipped, 167 subtests passed in 17.42s
```

My own arms on the same module:

```
  [APPENDED (FAIL-OPEN)] A1 registrar refresh claims catalog-backed with NO evaluation hash (catalog configured)
  [APPENDED (FAIL-OPEN)] A2 registrar TRIAGED-path claim: CAPTURED->TRIAGED catalog-backed, no hash
```

Both APPEND on `96af3eb6` and both refuse `CATALOG_BACKED_WITHOUT_EVALUATION_HASH`
on `61c56148`. **The registrar-path fail-open the brief told me to reproduce is
reproduced, and it is closed.** This also independently confirms the Lead's own
self-critical record (`LEAD_VERIFICATION_P31FIX.md:24-26`): the builder's J-03
arm, on its ENVIRONMENT_ADMISSION_AUTHORITY writer, was already refused pre-fix
by `EVALUATION_RUN_HASH_REQUIRED`, so it proved refusal-code precedence rather
than closure; the registrar arm added at `48bd70de`
(`test_registrar_refresh_with_catalog_backed_claim_requires_evaluation_hash`) is
the real fence — and my sweep shows it and the J-03 arm are the two tests G05
turns RED.

---

## 8. Scope and protected paths

`git diff --stat c76043b9 61c56148` (disclosed):

```
 DECISIONS.md                                       |    2 +-
 .../03_QUANTLENS/tools/p031_lifecycle_ledger.py    |  257 ++++-
 .../tools/tests/test_p031_lifecycle_ledger.py      | 1073 +++++++++++++++++---
 ...ITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md |    2 +-
 4 files changed, 1161 insertions(+), 173 deletions(-)
```

Exactly the four paths the brief names, and no others. Per commit: `96af3eb6`
4 files (+718/−133), `bd0d56d0` 2 files (+113/−1), `48bd70de` 1 file (+56),
`e9e37aec` 1 file (+79), `61c56148` 1 file (+158/−2).

* Both documentation edits are the OD-1 (3D) move and nothing else — word-diff
  verified, quoted in §5.
* **Protected paths:** `09_DOCS/PROTECTED_PATHS_POLICY.md:50` gives the pattern
  set as `MTC_V2.pine` (plus defaults). None of the four paths matches; the
  Lead's guard recorded `PINE_ALERT_GUARD PASS files=21 matches=0 → RESULT: PASS`.
  The same policy states at `:24` and `:80` that the hook is **not in force** and
  must not be cited as a control — consistent with what I found, and the reason I
  checked the pattern set by hand rather than trusting the hook.
  No protected path is touched, so the `APPROVED-PATCH-PLAN` trailer requirement
  does not attach to these commits.
* **`G1_SCOPE_AND_CONTRACT.md`** — checked per the 2026-09-17 N-7 amendment note:
  * `git ls-files | grep -i G1_SCOPE` → **no tracked copy**; a filesystem search
    of the worktree finds **no copy at all**. It lives only at
    `C:/tmp/P031_LEAD_20260912/`. "No copy inside the repository" holds.
  * Live file sha256 = `c82de2a8ab3526bf04f56c7be4b96b1ef8dddeef052e21a9387860602352fa40`
    — matches the post-amendment hash the addendum states. The CT13 pre-amendment
    copy hashes `1752290cb9dd81d75ce5ca65a1dd5510584151101e088ce08c638fadb8195d8a`
    — matches the stated pre hash.
  * `diff` pre vs post: **only** the two seam spellings and one appended
    amendment-log section. No other sentence changed.
  * The amended spellings match the ledger bytes exactly, including parameter
    order: constructor `:321-327`
    (`path, writer_allowlist, active_check_sets=None, accepted_evaluation_catalog=None`)
    and `append` `:848-858`
    (`event, *, check_set_version=None, evaluation_run_hash=None, failing_checks=(), check_set_purpose=None, catalog_backed=False, source_kind="FIXTURE"`).
    Two inaccuracies in the amendment log's *prose* are recorded as **N-17**.
* **`CHALLENGE` stays UNRESOLVED**: `:657-658` and the report's
  `unresolved_lifecycle_contracts` (`:1451-1453`) — verified in §5, OD-3.

---

## 9. Lead authorship of `48bd70de`, `e9e37aec` and `61c56148`

All three are test-only, disclosed in the lane records, and I verified the
test-only claim against bytes (`--stat` above; the ledger blob is unchanged since
`bd0d56d0`, same sha256). The Lead did not write the ledger logic this batch —
`96af3eb6` and `bd0d56d0` are the Codex gpt-5.5 lanes.

**Does Lead authorship change my verdict? No.** My evidence for these three
commits is entirely my own: my mirror, my mutator, my mutants, my arms, my
suite runs. I reproduced F-2 exactly (both mutants green at 110 with the tests
absent is the Lead's claim; my equivalent is that each mutant of the *candidate*
fails exactly one new test and nothing else, and that restoring gives 112), and
I re-derived the guard walks from the source rather than from the Lead's trace.

**Does it need anything beyond me and Sol?** No extra reviewer for the
authorship itself — the standard roster is the control, and the Lead states it
does not accept its own code. Two things I would keep on the record: (a) the
fences are *tests*, so the roster is reviewing test bytes written by the Lead
against ledger bytes written by Codex — the separation that matters is intact;
(b) the T0 cap is 3 rounds and this is round 2, so if any further REQUIRED
finding appears it should be treated as the last round, not a fourth.

---

## 10. Report honesty

| Claim in the records | My check | Result |
|---|---|---|
| `112 passed, 1 skipped, 167 subtests` at `61c56148` (`LEAD_VERIFICATION_P031_R2.md:26`) | R1 | reproduced exactly |
| contracts `50 passed` from `MTC_COMMAND_CENTER/contracts` | R2 | reproduced exactly |
| count chain 108 (`bd0d56d0`) → 109 (`48bd70de`) → 110 (`e9e37aec`) → 112 (`61c56148`) | lane artifacts `LEAD_PYTEST_312.txt` (108), `P31FIX2_LEAD_PYTEST_312.txt` (109), the R2 record, and my own 112 | consistent |
| the `1 skipped` is the host symlink skip | R3 | confirmed: `[WinError 1314]` privilege skip at `test:1301` |
| "Runtime used: Python 3.14.2. Python 3.12 is not installed in this sandbox." (`DISPOSITION_P31FIX.md:6`) plus the `py -3.12 → No suitable Python runtime` transcript | read | honest and self-documenting; the Lead re-ran on the pinned 3.12.12, which I reproduced |
| Ruff at `bd0d56d0`: `All checks passed!` (`LEAD_RUFF.txt`) | the command in the record is `ruff check --select E9,F821,F811` | **accurate as stated** — a deliberately narrow selector, labelled as such in `LEAD_VERIFICATION_P31FIX.md:18`. My full-rule run (R4) is not a contradiction. |
| Ruff at round 2: "the file's 36 pre-existing findings at `e9e37aec`, 36 at `61c56148` — 0 new" | `ruff check --isolated` on both test blobs | **36 and 36 — reproduced.** Round 2 touched only the test file, so the claim is in scope and correct. |
| — (no record states the ledger's full-rule delta) | `ruff check --isolated` on the base and candidate ledger blobs | base `c76043b9` **10**, candidate **11**: one new `TRY004` at `:399` in the new OD-11 `_normalize_accepted_catalog`, the same rule as four pre-existing instances of the module's deliberate ValueError-refusal-code convention. Recorded as **N-19**, not a defect. |
| `DISPOSITION_P31FIX.md` row J-04 (`:832-833` enforces the unchanged DEMOTED identity), corrected by the 2026-09-16 addendum to `:675-686` | arm **C4** | the addendum is right: a `DEMOTED` with a changed identity refuses `DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED`, not `DEPLOYMENT_IDENTITY_MISMATCH`. The correction is honest and now matches behaviour. |
| `SHA256SUMS_P31FIX.txt` pins the ledger as `81eedf03…` | §1 | that is the CRLF-mixed **checkout** hash, not the blob (`2bff9fcc…`) — N-11, already dispositioned; the blob OIDs in the round-2 records are correct |
| `LEAD_VERIFICATION_P031_R2.md` F-2 reproduction: both mutants `110 passed` with no new tests | not independently re-runnable at `61c56148` (the tests now exist), but the equivalent is §3 | consistent with what I observed |
| Gemini R2 delta "COUNTED PASS, F-2 CLOSED, both guard walks as the Lead traced, 0 findings" | I re-derived both guard walks from the bytes myself (§3) | the walks are correct as traced |
| `DISPOSITION_P31FIX.md` J-05 cites test line numbers from `bd0d56d0` | those offsets have drifted by three later commits | I did not rely on them; I verified the arms exist behaviourally (G1/G2/G3) and via the G11 mutant. Stale-line-number hygiene is the same family as N-12; recorded in N-19's neighbourhood, not raised separately. |

I found **no dishonest or unsupported claim** in the lane reports,
dispositions or Lead verifications. The one place a record is silent rather than
wrong is the ledger's full-rule Ruff delta (N-19), and the Lead's own record is
notably self-critical where it mattered most (the J-03 refusal-code-precedence
admission, which I independently confirmed).

**N-1..N-13 re-read against the bytes.** The dispositions in
`P031_M1_NIT_LEDGER_20260916.md` are fair and I re-raise none as REQUIRED.
Status notes: N-7 is now DONE outside the repository and verified here (§8);
N-9's correction is in the brief and I used it; N-11's blob OIDs are correct in
the round-2 records and I recomputed them; N-12 is fixed in `61c56148` (the −2
lines); N-6 remains open on the bytes (the report lists seven ratified contracts
for OD-2/4/5/6/7/8/10 and still names neither OD-9 nor OD-11, and never
discloses whether a catalog is configured — which N-16 makes more than cosmetic);
N-10 and N-13 are genuine owner questions and N-13 is now empirically
demonstrated (arm G5).

---

## 11. Findings

**Severity criterion I applied, stated so it can be argued with.** REQUIRED =
the candidate, as committed, either (a) accepts a record the owner's twelve
answers refuse, or records an untrue one; or (b) leaves a batch-introduced
invariant guard whose removal produces (a) with the suite green — the F-1/F-2
class. NIT = everything else: refusals that are unfenced but whose removal
produces no untrue record, fail-closed strictness or scope narrowing, record and
documentation defects, and open owner questions.

**No REQUIRED finding.** F-1 and F-2 are both closed on my own mutants; my
23-guard sweep found no third member of that class; and none of my 30 hostile
arms admitted a record the answers refuse.

### NITs

**N-14 (NIT) — `p031_lifecycle_ledger.py:614-618`: the OD-5
`CHECK_SET_PURPOSE_UNKNOWN` refusal is unfenced.** Mutant G17 (`:618` → `pass`)
leaves the suite fully green (`112 passed, 1 skipped, 167 subtests passed`).
Not REQUIRED: on the mutant an unknown purpose is still refused by the rung
check at `:731` or the fixed-purpose check at `:629`, and the only case that
appends (a `str` subclass) persists the truthful value
(`stored check_set_purpose='shadow_eligibility'`). Worth closing because the
suite already carries a whole family of *"rejects `str` subclass before
mutation"* tests (`test:3701`, `:3726`, `:3755`, `:3768`, `:3839`, `:3824`) and
`check_set_purpose` — a parameter this batch added — has no member in it. One
test: `check_set_purpose` as a non-declared string and as a `str` subclass, both
expecting `CHECK_SET_PURPOSE_UNKNOWN`.

**N-15 (NIT) — `p031_lifecycle_ledger.py:628-629`: the OD-5
`CHECK_SET_PURPOSE_MISMATCH` refusal for a supplied-vs-fixed purpose is
unfenced.** Mutant G19 (`:629` → `pass`) leaves the suite fully green. Not
REQUIRED: `_resolve_check_set_purpose` returns `fixed` regardless (`:630`), so
the mutant discards the writer's false claim and stores the truthful value
(`'shadow_eligibility'` for the admission case, `None` for the purposeless
registrar case). The lost property is that a writer's false purpose claim is
*refused* rather than *silently ignored* — which for a lifecycle ledger is a
real property, just not a false-record one. One test: a `SHADOW_ELIGIBLE`
naming `check_set_purpose="promotion"` with the correct shadow version, and a
purposeless registrar event carrying any purpose, both expecting
`CHECK_SET_PURPOSE_MISMATCH`.

**N-16 (NIT, the one I would most want the owner and Sol to look at) — the
OD-11 catalog binds every READ seam, unlike `active_check_sets`, so a
catalog-backed ledger is unreadable without the exact catalog — and the shipped
report CLI can never supply one.** `enforce_active` (`:946` append / `:1103`
replay) exists precisely so the caller-supplied *check-set* registry is enforced
on append and **not** on replay — a property a previous Sol round required
("mismatch fails independently of the current active registry",
`DECISIONS.md:18`). The three OD-11 catalog guards sit at `:744-753`, above that
switch, so they run at both seams, and the catalog is never persisted in the
database. Demonstrated
(`C:/tmp/OPUS_P031_SCRATCH/r3/catalog_replay_probe.py`, 5 events, one with
`catalog_backed=True`):

```
1. reopen with the SAME catalog C1
  OK  replay() -> 5     OK  current_state() -> SHADOW     OK  verify_integrity() -> None
2. reopen with a DIFFERENT catalog C2
  RAISED replay() / current_state() / verify_integrity() / render_status_report() / backup_to()
         -> ValueError: EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG
3. reopen with NO catalog at all
  RAISED replay() / current_state() / verify_integrity() / render_status_report()
         -> ValueError: CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG
4. control: the same move with active_check_sets instead of the catalog
  OK  replay() with a moved active check-set registry -> 5
```

And through the module's own shipped CLI, which builds
`LifecycleLedger(args.path, writer_allowlist)` with no catalog (`:1488`)
(`C:/tmp/OPUS_P031_SCRATCH/r3/cli_probe.py`):

```
shipped CLI: python p031_lifecycle_ledger.py report <path>
  ledger with catalog_backed=False on every record: exit=0   (5309 bytes of JSON report)
  ledger with ONE catalog_backed=True record:       exit=1
    stderr tail: ValueError: CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG
```

Why I call this a NIT and not REQUIRED: it fails **closed**, loudly, with an
exact code; it admits no record and violates no lifecycle invariant; the feature
is opt-in with `catalog_backed=False` by default and no fixture or accepted path
sets it; and there is a genuinely defensible reading in which refusing is
*correct* — a reader without the catalog cannot verify a catalog-backed claim,
and rendering it as verified would be the real fail-open. The residual gap is
then a tooling one: the CLI has no way to pass a catalog, and the ledger stores
none. **If the roster judges the read-only report a shipped M1 seam that must
keep working once OD-11 is used, this becomes REQUIRED** — and I would not argue
against that reading. Cheapest closures, either of which is small: thread the
`enforce_active` distinction through the catalog guards so committed history
stays readable, or give the CLI (and `main()`) a way to supply the accepted
catalog and disclose in the report whether one was configured (which also closes
half of N-6).

**N-17 (NIT) — two inaccuracies in the `G1_SCOPE_AND_CONTRACT.md` amendment-log
prose** (the amended seam *spellings* are byte-correct; only the justification
sentence is wrong). (a) It describes `active_check_sets` as *"a mapping of
check-set version → purposes"*; it is the inverse — purpose → versions
(`_normalize_active_check_sets` iterates `for purpose, versions in
active_check_sets.items()`, `:374`). (b) It attributes the
`active_check_sets=()` → `active_check_sets=None` spelling change to OD-1, but
the base at `c76043b9` already read
`active_check_sets: Mapping[str, Iterable[str]] | None = None` (base ledger
`:269`), so that spelling was stale *before* this batch and OD-1 (3D) is a
worthiness-ratification decision that changes no signature. The amendment is
still justified — by OD-5 (`check_set_purpose`) and OD-11
(`catalog_backed` / `accepted_evaluation_catalog`), both correctly cited — so
this is a record fix, not a re-amendment.

**N-18 (NIT / scope note) — the OD-7 refresh path requires an unchanged
`package_hash`, which is narrower than 6A's sentence.** `:805-811` refuses the
refresh unless `package_hash == current["package_hash"]` (arm G1), so a deep-rung
→ FROZEN under a *new package* is refused `DEPLOYMENT_REFRESH_IDENTITY_INVALID`.
6A speaks of "the new composite" generally, and the ratified text it rests on
(`brief:1435`, quoted in the packet) says a code/parameter change mints a new
`package_hash` while an allocator/policy change mints a new
`deployment_identity_hash` with the package unchanged — i.e. two kinds of
composite change, of which the ledger implements one. This fails **closed**, so
it is safe for M1 and arguably the right conservative reading; it should be an
explicit owner note rather than an unstated narrowing, because the missing case
(new package at a deep rung) has no recorded route today.

**N-19 (NIT) — one new full-rule Ruff finding in the ledger is unrecorded.**
`ruff 0.16.4 --isolated`: base `c76043b9` ledger **10** findings, candidate
**11**; the new one is `:399:13 TRY004 Prefer TypeError exception for invalid
type` in the new OD-11 `_normalize_accepted_catalog`. It matches the module's
deliberate convention (four pre-existing `TRY004` instances; every refusal is a
`ValueError` carrying a refusal code), so it is stylistically consistent and I
am not asking for a change — only that the record say so, since the existing
Ruff claims are either narrow-selector (`--select E9,F821,F811`, correctly
labelled) or test-file-only.

**N-20 (NIT) — the review brief's own `## Subject` section is stale.** It still
says HEAD *"must be `e9e37aecb5a0a3fc37b51f73657894560ad87155`"*, which the
2026-09-17 addendum supersedes with `61c56148`. I followed the addendum. Same
family as N-9 and N-12; worth fixing before the Sol generator inherits the
brief.

**Re-raised as owner questions (unchanged from the Lead's dispositions, both
confirmed against bytes/behaviour).**
**N-13** — OD-7 revocation is reversible: after A→B and re-admission under B, a
second refresh B→A is accepted and the candidate re-climbs under the previously
revoked identity (arm **G5**, `APPENDED`). Nothing in the twelve answers says
whether "revoked" may be re-adopted. **N-10** — a refresh does not open a new
evaluation epoch (epochs turn only at `RE_ENTRY`, `:1105-1107`), so the new
composite's first admission may cite the run that justified the revoked one.
Both are semantics, not code defects; both belong in the M1 acceptance packet.
Also re-raised: **N-5** (`_is_one_sentence` accepts semicolon run-ons and
refuses a reason containing `v2.0` — an OD-9 wording question), **N-6** (report
completeness: OD-9/OD-11 unlisted, catalog never disclosed — see N-16),
**N-4** and **N-8** as carried.

---

## 12. NOT VERIFIED

1. **Upstream acceptance provenance.** Exact accepted WP-P0-04 and WP-P0-13
   provenance (Item 1, Item 2, packet §4) are not available to me and are not
   affected by this candidate. M1 acceptance stays **NO** regardless of this
   report.
2. **OD-3 / `CHALLENGE`.** Verified only as *still fail-closed*. Whether 2A's
   field is correct cannot be checked until WP-P0-04 carries it.
3. **The owner's definition of "claims catalog-backed evidence".** The packet
   records that it is undefined and that defining it would be new scope. I
   verified the implementation takes the narrowest reading and that this keeps
   the ladder working; I cannot verify it is the reading the owner intends.
4. **"Prior windows … never count" (6A).** M1 models no forward-evidence
   window, so I verified only the ledger-side consequences (prior events remain
   in `replay()`; a refreshed candidate must be re-admitted). The window
   semantics live in WP-V2A-10 / WP-P0-21.
5. **Concurrency beyond the suite's own arms.** I did not add my own
   multi-process or multi-host races; the suite's three concurrency tests
   (`test:4965`, `:5057`, `:5135`) pass and I did not attempt to defeat them.
6. **Performance.** The recorded O(n) per append / O(n²) per build property was
   not re-measured; no optimisation is authorised.
7. **Other reviewers' runs.** I reproduced every number I cite, except the two
   round-2 Lead mutant runs at `e9e37aec` (`110 passed` with the new tests
   absent), which are not re-runnable at `61c56148`; my §3 equivalents are
   consistent with them. I read the Gemini R2 adjudication summary but did not
   re-run any Gemini call.
8. **`ruff` on the exact blob bytes with the repository's own configuration.**
   My base-vs-candidate comparison used `--isolated` on extracted blobs (config
   free) plus in-repo runs on the checkout; the two agree on the candidate
   (ledger 11, tests 36).
9. **The T0 roster.** This report accepts nothing. The roster is me + exact Sol
   (after the Codex reset) + Gemini ✔ + Lead ✔, assembled by the Lead.

---

## Bottom line

`61c56148` closes F-2 on my own mutants — removing `:812-813` fails exactly
`test_registrar_refresh_cannot_adopt_the_candidates_own_retired_identity`,
removing `:814-816` fails exactly
`test_registrar_refresh_cannot_adopt_another_candidates_identity`, restoring
gives `112 passed, 1 skipped, 167 subtests passed` — and F-1 stays closed. Both
new tests reach the intended guard (guard walks re-derived from the bytes,
corroborated by the mutants *accepting* rather than diverting), assert the whole
invariant including that replay carries no refresh record for both candidates,
and cannot pass for the wrong reason. The commit touches nothing but the test
file. All twelve owner answers are IMPLEMENTED-AS-ANSWERED. My own 23-guard
mutation sweep found no third member of the F-1/F-2 class, and 30 hostile arms
built on the public seams admitted nothing the answers refuse. Seven NITs, three
of them new to this read (N-16 the substantive one), and no REQUIRED finding.

VERDICT: PASS-WITH-NITS
