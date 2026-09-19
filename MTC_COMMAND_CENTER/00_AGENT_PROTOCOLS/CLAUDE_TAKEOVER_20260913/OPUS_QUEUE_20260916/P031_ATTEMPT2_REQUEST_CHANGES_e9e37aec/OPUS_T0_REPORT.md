# Exact T0 review — WP-P0-31 M1, candidate `e9e37aecb5a0a3fc37b51f73657894560ad87155` (repair round 1)

Reviewer: exact `claude-opus-5`, effort **xhigh**. Second exact-Opus read of this package (T0 repair round 1 of 3).
Brief executed: `C:/tmp/OPUS_QUEUE_20260916/P031/REVIEW_BRIEF.md` including the **ADDENDUM 2026-09-16**.
No delegation, no sub-agents, no other session resumed. Every command below was run by me, from the cwd
stated, with the pinned interpreter, and its output is quoted verbatim.

Git usage was restricted to `rev-parse`, `show <rev>:<path>`, `show <rev> --stat` (mandated by the addendum),
`log`, `merge-base --is-ancestor`, `rev-list --count`, and `diff <revA> <revB>` limited to
`--numstat` / `--name-status` / `-U0` hunk headers between two commits. **No `git status`, no working-tree
`diff`, no `add`, `commit` or `checkout` was run in any repository.** Scratch lives under
`C:/tmp/OPUS_P031_SCRATCH/` (round-1 work in `…/r1/`).

---

## 0. Verified identities (COMPUTED)

| Item | Value | How |
|---|---|---|
| Worktree HEAD | `e9e37aecb5a0a3fc37b51f73657894560ad87155` | `git -c safe.directory=* -C C:/tmp/P031_M1_20260913 rev-parse HEAD` |
| Interpreter | `Python 3.12.12` | `…/P020_IMPL_20260912/01a0924d-…/.venv/Scripts/python.exe -V` |
| `p031_lifecycle_ledger.py` sha256 (working tree) | `81eedf03b79289dce92019a16a56e21ed9612be8cca16660d1b79095cb7ab816` | `Get-FileHash -Algorithm SHA256` |
| `test_p031_lifecycle_ledger.py` sha256 (working tree) | `7339928ce01521152929820982b3185863e63b8a19279f368594e9b6dd56a40c` | same |
| `p031_lifecycle_ledger.py` sha256 (committed blob bytes) | `2bff9fcc1fc42c7780a7e40bb127f0dad79fe64dd3b17ee14d5337332f88a63d` | `git show e9e37aec:<path> \| sha256sum` |
| `test_p031_lifecycle_ledger.py` sha256 (committed blob bytes) | `7339928ce01521152929820982b3185863e63b8a19279f368594e9b6dd56a40c` | same |
| ledger blob OID | `7e7874770dc880aacb9bd8fcc6917c8416a7ce6a` | `git rev-parse e9e37aec:<path>` |
| tests blob OID | `815cebf00f298912f282b4a6a897ec9c0841c28b` | same |
| Sizes | ledger 1495 lines / 63252 bytes (worktree), tests 5147 lines / 206673 bytes | byte scan |

**The ledger is byte-identical to the two commits before it.** `git rev-parse <rev>:<path>` returns the same
blob OID `7e7874770d…` at `bd0d56d0`, `48bd70de` and `e9e37aec`. The repair changes no executable code at
all — so everything I judge about ledger behaviour below is judged against the same bytes the first read
saw, which I re-derived rather than assumed.

**Working tree vs committed bytes** (`C:/tmp/OPUS_P031_SCRATCH/r1/cmp_bytes.py`, pinned interpreter):

```
ledger
  raw_equal        False
  normalized_equal True
  blob CRLF / LF-only   0 / 1495
  wt   CRLF / LF-only   1110 / 385
tests
  raw_equal        True
  normalized_equal True
  blob CRLF / LF-only   0 / 5147
  wt   CRLF / LF-only   0 / 5147
```

The checked-out ledger is **content-identical** to the commit and differs only in line endings — and it has
**mixed** endings (1110 CRLF + 385 bare LF) while the test file in the same checkout is pure LF. The
`81eedf03…` value pinned in `SHA256SUMS_P31FIX.txt` is therefore a hash of *this checkout*, not of the
committed bytes (**N-11**). The blob OIDs above are the reproducible pins.

---

## 1. Mandated commands — run by me

**Focused suite** — cwd `C:/tmp/P031_M1_20260913`:

```
$ …/.venv/Scripts/python.exe -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py -q -p no:cacheprovider
................s.................... [ 33%]
....................... [ 54%]
...................................................           [100%]
110 passed, 1 skipped, 167 subtests passed in 17.88s
```

Reproduces the claimed `110 passed, 1 skipped, 167 subtests` exactly (109 → 110 is the one added test).

**Shared contracts** — cwd `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/contracts`, per the addendum's N-9
correction:

```
$ …/.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
..................................................                       [100%]
50 passed in 0.25s
```

**Candidate commit shape** — `git show e9e37aec --stat`:

```
 .../tools/tests/test_p031_lifecycle_ledger.py      | 79 ++++++++++++++++++++++
 1 file changed, 79 insertions(+)
```

**py_compile** on both files: `py_compile OK`. **Ruff** is still unreproducible on this host (no `ruff`
module in the pinned venv, no `ruff` on PATH) — isolated in §10; nothing in my verdict rests on it.

I could execute every mandated command; the verdict is therefore not BLOCK.

---

## 2. The repair: my own mutant M-2, and whether the new test earns it

### 2.1 Scope of the repair

`git diff 48bd70de e9e37aec --numstat` → `79  0  …/tests/test_p031_lifecycle_ledger.py`, one file.
`-U0` hunk headers → exactly one hunk, `@@ -2587,0 +2588,79 @@ class LifecycleLedgerTests(unittest.TestCase):`
— a pure insertion, zero deletions, nothing else touched. Every line number below 2588 in the test file is
unshifted from `48bd70de`, so the first read's test citations remain valid as written.

### 2.2 My own mutant

I rebuilt the mutant from the **committed blob**, not from the first read's artefacts
(`C:/tmp/OPUS_P031_SCRATCH/r1/make_mutant.py`), asserting the exact text of the two removed lines before
writing anything:

```
line 832: '            if current_deployment is not None and deployment_hash != current_deployment:'
line 833: '                raise ValueError("DEPLOYMENT_IDENTITY_MISMATCH")'
source lines: 1496  mutant lines: 1494
source sha256: 2bff9fcc1fc42c7780a7e40bb127f0dad79fe64dd3b17ee14d5337332f88a63d
mutant sha256: 6520c5feef70d57644ce5b21536ca7d615c33a455794587e0032e635f443f3c5
DEPLOYMENT_IDENTITY_MISMATCH occurrences in mutant: 0   (in source: 1)
```

Scratch tree `C:/tmp/OPUS_P031_SCRATCH/r1/tree/` = the committed test file + the contracts package + the
ledger under test. Baseline there, before mutating: `110 passed, 1 skipped, 167 subtests passed in 18.36s`.

**RED — mutant M-2** (cwd `C:/tmp/OPUS_P031_SCRATCH/r1/tree`):

```
$ …/.venv/Scripts/python.exe -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py -q -p no:cacheprovider --tb=line -rf
................s.................... [ 33%]
....................... [ 54%]
.........F.........................................           [100%]
E   AssertionError: ValueError not raised
FAILED …::LifecycleLedgerTests::test_post_refresh_admission_cannot_reuse_the_revoked_deployment_identity
1 failed, 109 passed, 1 skipped, 167 subtests passed in 17.70s
```

**GREEN — restored** (ledger restored byte-identical, sha256 `2bff9fcc…`):

```
110 passed, 1 skipped, 167 subtests passed in 17.96s
```

**The new test and only the new test fails on M-2**, and it fails with `ValueError not raised` — a genuine
fail-open fence, not a refusal-code-precedence artefact. The Lead's and Gemini's claims reproduce exactly.

### 2.3 Does the test assert the whole invariant?

`test_p031_lifecycle_ledger.py:2588-2665`. All four legs the addendum names are present and each is a real
assertion, not a smoke check:

| Leg | Where | Assertion |
|---|---|---|
| refresh lands FROZEN under the new identity | `:2617-2619` | `current_state == "FROZEN"`, `deployment_identity_hash == DEPLOYMENT_B` |
| old identity refused **with the exact code** | `:2621` | `assertRaisesRegex(ValueError, "DEPLOYMENT_IDENTITY_MISMATCH")` |
| candidate still FROZEN, identity untouched | `:2636-2638` | `current_state == "FROZEN"`, `deployment_identity_hash == DEPLOYMENT_B` |
| **no admission record appended** | `:2639-2647` | replay filtered to this candidate's `SHADOW_ELIGIBLE` events equals exactly `["revoked-identity-shadow_eligible"]` |
| new identity accepted **and recorded** | `:2649-2665` | append succeeds; `current_state == "SHADOW"`, `deployment_identity_hash == DEPLOYMENT_B` |

### 2.4 Could it pass for the wrong reason?

I walked the guard order on the candidate bytes for the refused append and checked each earlier exit:

- `EVIDENCE_REFERENCES_REQUIRED` (`:654`) — supplied by the fixture.
- `RETIRED_IDENTITY_TERMINAL` (`:660`) — state is FROZEN.
- `WRITER_AUTHORITY_REFUSED` (`:662`) — `SHADOW_ELIGIBLE` is in the admission authority's set.
- `PREVIOUS_STATE_MISMATCH` (`:664`) — `previous_state="FROZEN"` matches.
- `TIMESTAMP_NOT_MONOTONIC` (`:666`) — `offset=7` follows the refresh's `offset=6`.
- `DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED` (`:675-686`) — **cannot** fire: its `actual_state` set is
  `{SHADOW, TESTNET, LIVE_CANDIDATE, LIVE, SUSPENDED}` and the post-refresh state is `FROZEN`.
- `ILLEGAL_TRANSITION` (`:698`) — `("FROZEN","SHADOW_ELIGIBLE","SHADOW")` is in `LADDER_TRANSITIONS`.
- check-set path (`:723-740`) — `shadow-eligibility.v1` is in the fixture's active set for
  `shadow_eligibility`.
- `EVALUATION_RUN_HASH_REUSED` (`:791-796`) — `append_authority_event` derives the hash from the *event id*
  (`test:334-335`), so the refused append carries a **fresh** hash; no reuse path is entangled.
- `LADDER_IDENTITY_INCOMPLETE` / `PACKAGE_IDENTITY_MISMATCH` (`:824-831`) — both hashes present and
  `PACKAGE_A` equals the frozen package.

So `:832-833` is the first and only guard that can fire, and the regex is unambiguous — the string
`DEPLOYMENT_IDENTITY_MISMATCH` appears exactly once in the module and nowhere else in the codebase as a
substring of another code. **On the mutant the append is accepted** (the two remaining guards do not catch
it: the refresh does not retire the old identity, and the old identity is owned by the same candidate) —
which is exactly what M-2 demonstrated. The test cannot pass for the wrong reason, and it cannot fail for
the wrong reason either.

I also probed the breadth of what the one guard covers (arms C3/C4, §4): a post-refresh admission carrying a
*third, never-seen* identity and one carrying the *intermediate* identity after two chained refreshes are
both refused by the same line pair, and both are accepted on M-2. One test therefore fences the whole guard,
not a single scenario.

**F-1 is closed.** The repair is correct, minimal, test-only, and the evidence in
`LEAD_VERIFICATION_P031_R1.md` and the Gemini delta reproduces exactly.

---

## 3. Answer conformance, item by item

Authority verified against bytes: `C:/CT13/DECISIONS.md:83` (`OD-20260914-P031-LIFECYCLE-1` — "the twelve
P031 lifecycle items are answered with the packet's recommended options verbatim — OD-1=3D; OD-2=1B;
OD-3=2A; OD-4=3D now; OD-5=4A; OD-6=5C; OD-7=6A; OD-8=7A; OD-9=5a-C; OD-10=5b-A; OD-11=2C; OD-12=7-A") and
`:91` (`OD-20260914-P031-BATCH-GO-1`). Packet option texts below are quoted from
`P031_LIFECYCLE_DECISIONS_20260913_V4.md` summary table `:1047-1058` and the envelope sections, which I read
directly rather than through any prior report.

| Ref | Packet option text (quoted, verified) | Implementation (file:line, verified) | Verdict |
|---|---|---|---|
| **OD-1** (3D) | *"move 'ratified worthiness version' from an M1 acceptance precondition to an operating precondition on writing a real `CAPTURED -> TRIAGED` record"* (`:1047`) | `DECISIONS.md:18` — *"an owner-ratified worthiness check-set version is instead an operating precondition for writing any real `CAPTURED -> TRIAGED` record"*; `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:298` — the same sentence plus *"until then that write remains fail-closed"*. Both read by me in the worktree. Documentation only; the executable guard stays fail-closed (`ledger:736-740`, mutation-fenced — §5). | **IMPLEMENTED-AS-ANSWERED** |
| **OD-2** (1B) | *"the writer supplies `next_state`; the ledger validates strict descent on the ladder order … and an unchanged `deployment_identity_hash`. Assign `DEMOTED` to `MULTI_WORKER_SUPERVISOR`."* (`:1048`) | `LADDER_RANK` `ledger:42`; strict descent `ledger:688-693`; the six strictly-descending tuples and no others `ledger:134-139`; authority `ledger:121-123`; unchanged identity enforced at `ledger:675-686` (fires first for DEMOTED) with `ledger:832-833` as backstop. Arms A14-A18. | **IMPLEMENTED-AS-ANSWERED** (recording nit N-1, locality nit N-2 — both carried) |
| **OD-3** (2A) | *"add a nullable challenged-incumbent identity field … under WP-P0-04; keep `CHALLENGE` fail-closed until it exists"* (`:1049`) | `ledger:657-658` refuses every `CHALLENGE` before any other check; the report still prints `"CHALLENGE INCUMBENT DEPLOYMENT IDENTITY FIELD: MISSING"` (`ledger:1451-1453`); `contracts/` untouched by the diff. Arm A40; mutation-fenced. | **IMPLEMENTED-AS-ANSWERED** — stays UNRESOLVED as required |
| **OD-4** (3D now) | *"ratify the current repository-wide refusal as the deliberate interim"* (`:1050`) — recording only | `ledger:710-721` unchanged; recording added at `ledger:1456`. Arm A39; mutation-fenced. | **IMPLEMENTED-AS-ANSWERED** |
| **OD-5** (4A) | *"writer-supplied `check_set_purpose` from the declared set, validated against the candidate's rung, with `check_set_version`, `evaluation_run_hash` and non-empty `failing_checks` all mandatory. Restore `("REJECTED", "RE_ENTRY", "CANDIDATE")`."* (`:1051`) | purpose required `ledger:619-622`; rung table `ledger:49-60` + check `ledger:728-731`; version `ledger:732-733`; hash + non-empty checks `ledger:773-777`; `REJECTED` arcs `ledger:70-76`; re-entry arc `ledger:82`. Arms A19-A23, A41, A43; all four guards mutation-fenced. | **IMPLEMENTED-AS-ANSWERED** (dead table row → N-8, carried) |
| **OD-6** (5C) | *"take the target from the supplied `check_set_version`'s purpose instead of inferring it from `previous_state`"* (`:1052`) | `ledger:623-626` (`supplied or _purpose_for_check_set_version(version)`); rung allowance `ledger:43-48` + `ledger:724-727`; append-time consistency `ledger:736-740`. Arm A28; mutation-fenced. | **IMPLEMENTED-AS-ANSWERED, two recorded residues** — supplied purpose takes precedence (N-4), replay no longer re-derives this purpose (N-3); both carried |
| **OD-7** (6A) | *"the candidate returns to `FROZEN` under the new composite; revocation stays silent-by-construction"* (`:1053`); envelope 6: *"revocation is expressed by the absence of admission records for that new identity … Requires one decided transition (deep rung -> `FROZEN`, same candidate, new composite) and a relaxation of `ledger:657-658` so a re-freeze may carry the new deployment identity"* (`:692`) | transitions `ledger:77-81`; refresh detection `ledger:669-674`; composite validation `ledger:805-811`; retired-identity refusal `ledger:812-813`; cross-candidate binding refusal `ledger:814-816`; `FROZEN_DEPLOYMENT_IDENTITY_FORBIDDEN` narrowed to the non-refresh case `ledger:817-818`; the revocation guard `ledger:832-833`. Arms A02, A29-A32, A36, C1-C5. | **IMPLEMENTED-AS-ANSWERED in behaviour, and never broader than the option** (the two extra refusals are strictly fail-closed additions). **Its fences are incomplete → finding F-2 (REQUIRED)** |
| **OD-8** (7A) | *"ratify as implemented: one `evaluation_run_hash` binds to exactly one `candidate_id` forever"* (`:1054`) — recording only | `ledger:789-790` unchanged; recording added `ledger:1460`. Arm A26. | **IMPLEMENTED-AS-ANSWERED** |
| **OD-9** (5a-C) | *"keep the transition, gate it on a sixth owner-only trigger class with a mandatory recorded one-sentence external-change reason; keep every existing constraint"* (`:1055`) | `OWNER_EXTERNAL_CHANGE` at `ledger:95` (six total `ledger:88-97`); RETIRED branch `ledger:758-764`; the owner trigger refused from the five automatic states `ledger:765-766`; freshness `ledger:767-770`; no recounted evidence `ledger:771-772`; identities cleared `ledger:840-841`. Arms A08-A13, A38; **both** halves mutation-fenced. | **IMPLEMENTED-AS-ANSWERED** (sentence rule crude → N-5, not recorded in the report → N-6; both carried) |
| **OD-10** (5b-A) | *"ratify as implemented …, conditional on giving `test:2192-2288` real assertions and closing the report's disclosure gap"* (`:1056`) | Behaviour unchanged (`ledger:791-796`; epoch rollover `ledger:1105-1107`). Condition 1: `test_current_epoch_evaluation_may_support_multiple_decisions` now carries real assertions on `event_type`, purpose, version, hash and resulting state — verified by the first read at `test:2278-2442`, and those line numbers are **still exact** because `e9e37aec`'s only hunk inserts at 2588. Condition 2: `ledger:1461`. Arms A24, A25. | **IMPLEMENTED-AS-ANSWERED** |
| **OD-11** (2C) | *"optional configured catalog: refuse an `evaluation_run_hash` absent from an accepted catalog when one is supplied, fail closed on catalog-backed claims when none is"* (`:1057`), with *"an owner definition of 'claims catalog-backed evidence' (undefined here…)"* named in the same cell as an outstanding cost | catalog param `ledger:326`, normalization `ledger:392-403`; absent-hash refusal `ledger:748-753` (binds **every** hash once a catalog exists — arm A05, strictly fail-closed); no-catalog claim `ledger:744-745`; claim-without-hash `ledger:746-747`; `catalog_backed` must be a real `bool` `ledger:556-557`. Arms A03-A07, A33, A37; all four guards mutation-fenced. | **IMPLEMENTED-AS-ANSWERED under the narrowest reading**, which is fail-closed and openly disclosed. The owner definition the packet demanded still does not exist (§10.5); two priced costs remain open → N-6, N-7 |
| **OD-12** (7-A) | *"preserve; fold the refresh … into one new candidate and one T0 roster once OD-1..OD-11 are answered"* (`:1058`) | `git merge-base --is-ancestor c76043b9 e9e37aec` → true; `rev-list --count c76043b9..e9e37aec` → 4; no rebase; `03_QUANTLENS/HANDOFF.md` not in the diff. | **IMPLEMENTED-AS-ANSWERED** |

**No item is BROADER THAN ANSWERED in a way that widens what the ledger accepts.** Every divergence I found
is either strictly fail-closed (OD-7's two extra refusals, OD-11's catalog binding every hash) or a
recording / coverage matter. OD-6 is still the only item that takes an input the option text did not name
(a writer-supplied purpose), and append-time validation keeps that input consistent with the version.

---

## 4. Fail-open hunt — my own RED arms

### 4.1 Re-run of the 43-arm sweep

Harness `C:/tmp/OPUS_P031_SCRATCH/arms/probe.py` (43 independent arms, own fixtures, own temp ledgers,
module loaded by file path). I re-ran it myself rather than citing its previous output:

```
$ …/.venv/Scripts/python.exe probe.py C:/tmp/P031_M1_20260913/…/p031_lifecycle_ledger.py
SUMMARY: 43 as expected, 0 NOT as expected

$ …/.venv/Scripts/python.exe probe.py C:/tmp/OPUS_P031_SCRATCH/r1/mutant_M2_ledger.py
SUMMARY: 42 as expected, 1 NOT as expected
  DIVERGENT A36 post-refresh re-admission on the OLD identity:
    expected 'DEPLOYMENT_IDENTITY_MISMATCH', got 'ACCEPTED -> SHADOW'
```

Every arm the brief §2 names behaves as specified on the candidate: registrar refresh with
`catalog_backed=True` and no hash → `CATALOG_BACKED_WITHOUT_EVALUATION_HASH`; a hash outside the catalog →
`EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG`; `RE_ENTRY` from RETIRED without the owner trigger or with a
two-sentence reason → `RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED`; `DEMOTED` sideways or upward →
`DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT`; `REJECTED` without failing checks → `FAILING_CHECKS_REQUIRED`;
same-epoch reuse across purposes → accepted (OD-10), across epochs → `EVALUATION_RUN_HASH_REUSED`, across
candidates → `EVALUATION_RUN_CANDIDATE_SCOPE_UNRESOLVED`.

### 4.2 Six new arms, written for this round

`C:/tmp/OPUS_P031_SCRATCH/r1/arms2.py`, my own fixture builder, aimed at the OD-7 refresh surface the first
read did not exhaust. Command (cwd `C:/tmp/OPUS_P031_SCRATCH/r1`):

```
$ …/.venv/Scripts/python.exe arms2.py <module-path> [arm…]
```

Observed on the candidate — **6 as expected, 0 NOT as expected**:

| Arm | Scenario | Expected | Observed on `e9e37aec` |
|---|---|---|---|
| **C1** | registrar refresh onto the candidate's **own retired** deployment identity (retire under `DEP_A`, re-enter, re-freeze under `PKG_B`, climb under `DEP_B`, then refresh back onto `DEP_A`) | refuse | `ValueError: DEPLOYMENT_IDENTITY_RETIRED` |
| **C2** | registrar refresh onto **another candidate's live** deployment identity | refuse | `ValueError: DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE` |
| **C3** | post-refresh admission carrying a **third, never-seen** identity | refuse | `ValueError: DEPLOYMENT_IDENTITY_MISMATCH` |
| **C4** | two chained refreshes `A→B→C`, then admission under the **intermediate** `B` | refuse | `ValueError: DEPLOYMENT_IDENTITY_MISMATCH` |
| **C5** | refresh **back onto** the candidate's own revoked-but-not-retired identity `A`, then admit under `A` | — | `ACCEPTED -> state=SHADOW pkg=11111111 dep=33333333` → see N-13 |
| **C6** | first admission at FROZEN when no identity has ever been set (the `is not None` arm of `:832`) | accept | `ACCEPTED -> state=SHADOW pkg=11111111 dep=77777777` |

Against the mutants (same arms, mutated module):

```
=== M-4 (ledger:812-813 removed) ===
XX  C1 refresh onto the candidate's OWN retired identity
      expect: DEPLOYMENT_IDENTITY_RETIRED
      got   : ACCEPTED -> state=FROZEN pkg=22222222 dep=33333333

=== M-7 (ledger:814-816 removed) ===
XX  C2 refresh onto ANOTHER candidate's identity
      expect: DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE
      got   : ACCEPTED -> state=FROZEN pkg=11111111 dep=77777777 | ACCEPTED -> state=SHADOW pkg=11111111 dep=77777777
            (two different candidates now carry the same deployment_identity_hash)

=== M-2 (ledger:832-833 removed) ===
XX  C3 → ACCEPTED -> state=SHADOW dep=77777777
XX  C4 → ACCEPTED -> state=SHADOW dep=44444444
```

C3/C4 show the new test's guard covers the whole line pair, not one scenario. C1/C2 are the evidence for
**F-2**.

---

## 5. D026 evidence — the complete mutation map

The brief asks for D026 evidence for every refusal introduced since `c76043b9`. Rather than sample, I built
the full map: one mutant per guard that OD-1..OD-12 added or re-shaped, each removed from the **committed
blob**, each run against the whole in-tree suite on the pinned interpreter
(`C:/tmp/OPUS_P031_SCRATCH/r1/battery2.py` + `battery3.py`, 20 mutants; ledger restored to
`2bff9fcc…` afterwards, verified).

| # | Guard removed | Suite result | RED test(s) |
|---|---|---|---|
| OD-3 | `:657-658` `CHALLENGE_…_FIELD_MISSING` | 1 failed / 109 passed | `test_unresolved_challenge_contract_fails_closed_and_stays_visible` |
| OD-2 | `:688-693` `DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT` | 1 failed / 109 passed | `test_demoted_requires_strict_descent_and_keeps_deployment_identity` |
| OD-4 | `:710-721` `SUCCESSION_ENVELOPE_UNRESOLVED` | 1 failed / 109 passed | `test_second_promoted_candidate_requires_atomic_succession_envelope` |
| OD-6 | `:724-727` `ADMISSION_WITHHELD_TARGET_UNRESOLVED` | 1 failed / 109 passed | `test_admission_record_types_materialize_only_canonical_states` |
| OD-5 | `:728-731` REJECTED rung purpose | 1 failed / 109 passed | `test_rejected_requires_purpose_hash_and_failing_checks` |
| OD-1 | `:736-740` active check-set enforcement | 3 failed / 107 passed | `…requires_an_active_exact_check_set`, `…bound_to_transition_purpose`, `…distinct_check_set_purpose` |
| OD-11 | `:744-745` `CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG` | 1 failed / 109 passed | `test_catalog_backed_claim_fails_closed_without_catalog` |
| OD-11 | `:746-747` `CATALOG_BACKED_WITHOUT_EVALUATION_HASH` | 2 failed / 108 passed | `…refuses_absent_hash_and_accepts_present_hash`, `test_registrar_refresh_with_catalog_backed_claim_requires_evaluation_hash` |
| OD-11 | `:748-753` `EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG` | 1 failed / 109 passed | `…refuses_absent_hash_and_accepts_present_hash` |
| OD-9 | `:759-764` `RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED` (body → `pass`) | 2 failed / 110 passed, 165 subtests | `test_retired_reentry_requires_owner_external_change_reason` |
| OD-9 | `:765-766` owner trigger refused off RETIRED | 1 failed / 109 passed | `test_retired_reentry_requires_owner_external_change_reason` |
| OD-5 | `:774-777` `EVALUATION_RUN_HASH_REQUIRED` + `FAILING_CHECKS_REQUIRED` (body → `pass`) | 3 failed / 109 passed | `test_rejected_requires_purpose_hash_and_failing_checks` |
| OD-11 | `:556-557` `CATALOG_BACKED_INVALID` | 4 failed / 110 passed, 163 subtests | `test_catalog_backed_argument_must_be_bool` |
| OD-5 | `:620-621` `CHECK_SET_PURPOSE_REQUIRED` | 2 failed / 109 passed | `…purpose_and_stale_evaluation_fail_closed`, `…requires_purpose_hash_and_failing_checks` |
| OD-2/7 | `:675-686` `DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED` | 4 failed / 110 passed, 163 subtests | `test_deployment_refresh_registrar_path_is_available_at_every_deep_state` (4 subtests) |
| OD-7 | `:805-811` `DEPLOYMENT_REFRESH_IDENTITY_INVALID` | 4 failed / 109 passed | `…returns_to_frozen_under_new_composite`, `…available_at_every_deep_state` |
| **OD-7** | **`:812-813` `DEPLOYMENT_IDENTITY_RETIRED` (refresh path)** | **110 passed, 1 skipped, 167 subtests — FULLY GREEN** | **none → F-2** |
| **OD-7** | **`:814-816` `DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE` (refresh path)** | **110 passed, 1 skipped, 167 subtests — FULLY GREEN** | **none → F-2** |
| OD-7 | `:817-818` `FROZEN_DEPLOYMENT_IDENTITY_FORBIDDEN` | 1 failed / 109 passed | `test_identity_depth_is_exact_before_freeze_and_through_tail` |
| **OD-7** | **`:832-833` `DEPLOYMENT_IDENTITY_MISMATCH`** | **1 failed / 109 passed** | **`test_post_refresh_admission_cannot_reuse_the_revoked_deployment_identity` — the repair** |

**18 of 20 guards are mutation-fenced. Two are not, both inside OD-7's new refresh branch.**

### 5.1 Which of the first read's D026 claims I re-derived

- The builder's J-03 arm (`test:2927`) fails pre-fix only by refusal-code precedence, and the Lead's arm
  (`test:2989`) is the real fence for `CATALOG_BACKED_WITHOUT_EVALUATION_HASH`: the mutation row above is
  independent confirmation — removing `:746-747` turns **both** RED, and the first read's pre-fix run showed
  only the Lead arm failing with `ValueError not raised`. Consistent; K-D-01 is genuinely closed.
- `RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED`, `DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT`,
  `CHECK_SET_PURPOSE_REQUIRED`, `FAILING_CHECKS_REQUIRED`, `CATALOG_BACKED_INVALID`,
  `ACCEPTED_EVALUATION_CATALOG_INVALID`, `EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG`,
  `CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG`, `DEPLOYMENT_REFRESH_IDENTITY_INVALID` — all carry a
  mutation-RED arm above, which is the stronger form of the first read's RED-on-base evidence.

---

## 6. Scope and protected paths

`git diff c76043b9 e9e37aec --numstat` — exactly four paths:

```
1    1    DECISIONS.md
226  31   MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py
732  95   MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py
1    1    MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md
```

- Nothing under `MTC_COMMAND_CENTER/contracts/` — the shared `LifecycleEvent` / `LifecycleWriterClass` bytes
  are untouched, and the 50 contract tests pass unchanged.
- No protected scope, no Pine, no runtime, no host, no credentials, no exporter path.
- Both documentation edits are one line each and are exactly the OD-1 amendments; I read both in the
  worktree (`DECISIONS.md:18`, `brief:298`) and they say what 3D asks and nothing more.
- `G1_SCOPE_AND_CONTRACT.md` is **unchanged**: it lives outside the repository at
  `C:/tmp/P031_LEAD_20260912/G1_SCOPE_AND_CONTRACT.md`, sha256
  `1752290cb9dd81d75ce5ca65a1dd5510584151101e088ce08c638fadb8195d8a`, mtime **2026-09-12 21:45** — four days
  before this commit, and no copy exists inside the worktree. Untouched as the brief requires; still showing
  the pre-batch signatures, which is N-7.
- `CHALLENGE` stays UNRESOLVED (§3 OD-3; arm A40; mutation-fenced).
- `c76043b9` is an ancestor; exactly 4 commits ahead; `OD-12` preserved.

---

## 7. Lead authorship

`48bd70de` and `e9e37aec` are both Lead-authored and both **test-only** — `git show e9e37aec --stat` shows
one file, +79/−0, and the ledger blob OID is unchanged across `bd0d56d0 → 48bd70de → e9e37aec`. Both commit
messages disclose the authorship and the reason (every Codex home capped), and
`DISPOSITION_P31FIX2.md` / `LEAD_VERIFICATION_P031_R1.md` repeat it.

It does **not** change my verdict. I verified both fences by executing them rather than accepting them, and
Gemini's K-D-02 disposition (a Lead-authored change still takes the standard roster) is the right one and is
being honoured by this slot and the pending exact Sol slot. Nothing beyond that is needed for these two
commits.

The caution the first read gave stands and now has a second instance: **the repair for F-2 should not be
Lead-authored as well if any independent route is available.** Three consecutive Lead-authored fences on one
package would leave the roster reviewing work it also wrote. If no route is available, say so in the
disposition as before — disclosure has been good throughout and that is what makes it acceptable.

---

## 8. Report honesty

| Claim | Source | My check |
|---|---|---|
| `110 passed, 1 skipped, 167 subtests` on 3.12.12 | `LEAD_PYTEST_GREEN_R1.txt`, `LEAD_VERIFICATION_P031_R1.md` | **Reproduced exactly** |
| RED on mutant M-2 = `1 failed / 109 passed`, exactly the new test | `LEAD_RED_ARM_mutant_M2_guard_removed.txt`, same record | **Reproduced exactly**, with my own mutant built from the committed blob |
| contracts `50 passed` | `LEAD_CONTRACTS_312.txt` | **Reproduced** from `MTC_COMMAND_CENTER/contracts` as cwd (the N-9 fix is correctly folded into the brief) |
| repair is `+79/−0`, one file, no ledger change | `LEAD_VERIFICATION_P031_R1.md`, commit message | **Reproduced**: one hunk, pure insertion, ledger blob OID unchanged |
| Gemini delta: `PASS`, F1 `CLOSED`, first guard to fire `:832-833`, `mutant_would_accept: true`, 0 findings | `REPAIR_R1_20260916/GEMINI/LEAD_ADJUDICATION.md` | **Every element independently confirmed** — including the adjudication's guard-order walk, which matches the bytes, and its observation that on the mutant the two remaining guards let the admission through |
| the first read's F-1 characterisation (dead in base, load-bearing after OD-7) | first read, `LEAD_VERIFICATION_P031_R1.md:4` | **Confirmed against base bytes**: `c76043b9` has zero occurrences of `is_registrar_refresh` and only one `DEPLOYMENT_IDENTITY_RETIRED` / `BOUND_TO_ANOTHER_CANDIDATE` pair (`base:675`, `:678`), i.e. no refresh branch existed |
| M1 acceptance gate quoted as `plan:656` with *"shown RED without the guard and GREEN with it under D026"* and *"retains its evidence and identity lineage"* | first read §8 | **Verified in the worktree**: `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:656` reads exactly that; repo rule D026 itself is stated at `:85` — *"A test, guard or check counts as evidence only when it has been shown RED against a deliberate mutation and GREEN after"* |
| `81eedf03…` as the ledger's pinned hash | `SHA256SUMS_P31FIX.txt`, `DISPOSITION_P31FIX.md` | **Reproduces on this checkout only** — it is not the committed bytes; see N-11 |
| the NIT ledger's ten dispositions | `P031_M1_NIT_LEDGER_20260916.md` | Read in full; each disposition is a fair reading of the finding it answers. N-1's record fix and N-7's docs commit are described as owed and are **not yet on the branch** (`G1_SCOPE_AND_CONTRACT.md` mtime is still 2026-09-12) — correctly, since both records say "queued" |
| Ruff `0 new findings` | `LEAD_VERIFICATION_P031_R1.md` | **Not reproducible here** (§10) |

No overclaim found in any lane record for this round. Both the Lead's and Gemini's descriptions of the
repair match the bytes.

---

## 9. Findings

### F-2 [REQUIRED] — two of OD-7's three new refresh-path identity guards are unfenced; deleting either leaves the suite fully green while the ledger accepts a retired or foreign deployment identity

**Where:**

```python
804                if is_registrar_refresh:
…
812                    if deployment_hash in retired_deployments:
813                        raise ValueError("DEPLOYMENT_IDENTITY_RETIRED")
814                    owner = deployment_owners.get(deployment_hash)
815                    if owner is not None and owner != event.candidate_id:
816                        raise ValueError("DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE")
```

`MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:812-813` and `:814-816`.

**Why they are new.** `c76043b9` contains **zero** occurrences of `is_registrar_refresh` — the whole
registrar-refresh branch is code OD-7 introduced, and in the base a `SHADOW → FROZEN` event was refused as
`ILLEGAL_TRANSITION` long before any identity check. The base carries exactly one `DEPLOYMENT_IDENTITY_RETIRED`
and one `DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE` site (`base:675`, `:678`, the ladder path). The
candidate carries two of each — the second pair, `:812-813` and `:814-816`, exists only because OD-7 opened a
new door into `FROZEN` that can carry a deployment identity. They are the identity screen on that new door.
Their ladder-path twins are fenced (mutants of `:834-835` and `:836-838` both turn tests RED); the refresh-path
pair is not.

**Evidence — my mutants, run by me.** Each removed from the committed blob, whole in-tree suite re-run on the
pinned interpreter in `C:/tmp/OPUS_P031_SCRATCH/r1/tree`:

```
OD-7  refresh-path DEPLOYMENT_IDENTITY_RETIRED  :812-813
   sha256 : 91c1070bb2d17b9a…
   result : 110 passed, 1 skipped, 167 subtests passed in 11.86s   <<< UNFENCED

OD-7  refresh-path BOUND_TO_ANOTHER_CANDIDATE   :814-816
   sha256 : d83cca760981a084…
   result : 110 passed, 1 skipped, 167 subtests passed in 11.65s   <<< UNFENCED
```

And on those same mutants, my arms C1 and C2:

```
XX  C1 refresh onto the candidate's OWN retired identity        (on M-4)
      expect: DEPLOYMENT_IDENTITY_RETIRED
      got   : ACCEPTED -> state=FROZEN pkg=22222222 dep=33333333

XX  C2 refresh onto ANOTHER candidate's identity                (on M-7)
      expect: DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE
      got   : ACCEPTED -> state=FROZEN pkg=11111111 dep=77777777 | ACCEPTED -> state=SHADOW pkg=11111111 dep=77777777
```

C2's output is two candidates sharing one `deployment_identity_hash`, one FROZEN under it and one already
SHADOW under it — with the suite reporting `110 passed`.

**Failure scenario (C1).** A candidate is retired at SHADOW under `D1`; `D1` enters `retired_deployments`
permanently. The owner re-enters it under `OWNER_EXTERNAL_CHANGE`, it is re-frozen under a new package `P2`
and climbs under `D2`. An operator then issues an OD-7 refresh naming `D1` as the new composite. Today that
is refused. If `:812-813` is ever touched — reordered, folded into `:805-811`'s condition, or moved below the
owner-binding check — the ledger will accept it, write `deployment_identity_hash = D1` into
`lifecycle_current`, and the candidate will climb again under an identity the ledger has recorded as retired
for ever. `RETIRED_PACKAGE_IDENTITY` does not catch it (the package is `P2`, not the retired one), and the
ladder-path `:834-835` does not either, because the refresh has already written `D1` as *current*, so every
later admission matches it.

**Failure scenario (C2).** Two candidates end up sharing one deployment identity, which is the exact
condition `deployment_owners` exists to make impossible — and which silently breaks the one-identity-one-
candidate premise that `brief:1435`'s *"never modify a running identity"* rests on.

**Severity.** The shipped code is correct; this is not a live fail-open. It is a D026 defect of exactly the
class the roster has already ruled REQUIRED twice — K-D-01 (*"the Lead's probe proved the edge, but the tree
must carry the fence"*) and F-1 of my own first read — and it is measured by the same rule those were
measured by: `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:85`, *"A test, guard or check
counts as evidence only when it has been shown RED against a deliberate mutation and GREEN after (repo rule
D026)"*, and the M1 acceptance gate at `:656`, *"each shown RED without the guard and GREEN with it under
D026 … every … retirement … record retains its evidence and identity lineage."* Two guards whose entire job
is identity lineage are not shown RED by anything.

**This is my own slot's miss in round 1, not a moved goalpost.** The first read mutated two guards; this read
mutated all twenty, and §5 is the complete map. There is no third unfenced guard among the OD-1..OD-12
changes — that is measured, not assumed, so one repair round closes the class.

**Repair (two tests, no ledger change, same idiom as the round-1 fence).** In `LifecycleLedgerTests`:

1. *Retired identity on the refresh path.* Build to SHADOW under `DEPLOYMENT_A`; retire; `RE_ENTRY` under
   `OWNER_EXTERNAL_CHANGE` with a one-sentence reason; re-freeze under `PACKAGE_B`; admit under
   `DEPLOYMENT_B`; then assert a registrar refresh `SHADOW → FROZEN` naming `DEPLOYMENT_A` raises
   `DEPLOYMENT_IDENTITY_RETIRED` and that the candidate stays SHADOW under `DEPLOYMENT_B`.
2. *Foreign identity on the refresh path.* Build candidate `B` to SHADOW under a distinct identity;
   build candidate `A` to SHADOW under `DEPLOYMENT_A`; assert a registrar refresh of `A` naming `B`'s
   identity raises `DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE`, and that **both** candidates' recorded
   identities are unchanged.

`arms2.py`'s C1 and C2 are working templates. Verify each RED against its own mutant (`:812-813`,
`:814-816`) — not merely GREEN on the candidate — and confirm the other tests stay green.

---

### Carried NITs from the first read

N-1 … N-10 are dispositioned in `P031_M1_NIT_LEDGER_20260916.md`. I re-read each against the bytes and
**re-raise none of them as REQUIRED for M1 acceptance**; the dispositions are fair. Two notes:

- **N-7** (the `G1_SCOPE_AND_CONTRACT.md:18` amendment) is the one whose disposition is a *record fix owed on
  the branch* rather than a carry. It is still owed: the file's mtime is 2026-09-12 21:45 and its `:20` /
  `:24` still show the pre-batch `LifecycleLedger(...)` and `append(...)` signatures while the candidate has
  `accepted_evaluation_catalog` (`ledger:326`) and `check_set_purpose` / `catalog_backed`
  (`ledger:855-856`). The brief's *"`G1_SCOPE_AND_CONTRACT.md` must be untouched"* and that file's own `:18`
  still point in opposite directions; the Lead's plan (amend it as a docs commit after this read, Sol reads
  the amended file) resolves it, and I record the state rather than choosing.
- **N-9** is fixed in the brief and I used the corrected invocation.

### N-11 [NIT] — the pinned ledger hash is a property of this checkout, not of the commit

`SHA256SUMS_P31FIX.txt` / `DISPOSITION_P31FIX.md` pin `81eedf03…`. That is the sha256 of the **working-tree**
file, which has **mixed** line endings (1110 CRLF + 385 LF); the committed blob is pure LF and hashes to
`2bff9fcc…`. The test file in the same checkout is pure LF and its two hashes agree, so a reader comparing
the two rows has no way to tell which form was meant. Record the blob OIDs
(`7e7874770dc880aacb9bd8fcc6917c8416a7ce6a` for the ledger, `815cebf00f298912f282b4a6a897ec9c0841c28b` for the
tests) alongside — they are checkout-independent. Nothing about the candidate's content is in doubt: the
normalized bytes are identical.

### N-12 [NIT] — the new test's docstring cites the wrong lane and a line number that will drift

`test_p031_lifecycle_ledger.py:2596` says *"Lane-3 exact-Opus review of `48bd70de`"*; the commit message of
the same commit says *"the Wednesday lane-1 exact-Opus T0 review"*, and `LEAD_VERIFICATION_P031_R1.md:3`
says lane 1. One of the two committed texts is wrong. Separately, `:2593` pins the guard as
`ledger :832-833` inside a docstring — accurate today, but it is the first thing to go stale the next time
the ledger gains a line above 832. Naming the refusal code (which the assertion already does) is the durable
citation.

### N-13 [NIT] — OD-7 revocation is reversible: a refresh may return to a previously revoked identity

Arm C5, observed on the candidate: after `A → B` (identity `A` revoked, candidate re-admitted under `B`), a
second refresh `B → A` is **accepted**, and the candidate then re-climbs under `A`
(`ACCEPTED -> state=SHADOW dep=33333333`). Nothing is wrong under OD-7 as written — `A` was revoked, not
retired, and 6A expresses revocation as *"the absence of admission records for that new identity"*, which a
fresh admission record supplies. But it means "revoked" is a state the composite can leave, and no owner
answer says whether that is intended. It belongs with N-10 (a refresh does not open a new evaluation epoch)
in the M1 acceptance packet's open-questions list rather than in code: both are about how much identity
history a refresh is supposed to erase, and neither is settled by any of the twelve answers.

---

## 10. NOT VERIFIED

1. **Ruff.** The pinned interpreter has no `ruff` module and no `ruff` executable exists on PATH or in that
   venv's `Scripts`, so `LEAD_VERIFICATION_P031_R1.md`'s "36 pre-existing findings, 0 new" is unreproduced
   here. `py_compile` is clean on both files and the whole suite executes; nothing in my verdict depends on
   it.
2. **Repo guard.** I did not re-run `LEAD_GUARD_R1.txt`'s dry run — the brief forbids `git status` in any
   repository and the guard inspects working-tree state. Its recorded contents are consistent with the diff
   I did verify.
3. **Gemini transport evidence.** I confirmed every *finding* in the round-1 Gemini delta against bytes, but
   did not re-derive wrapper hashes, the 18-read audit or the conversation id. That slot is not mine to
   re-adjudicate.
4. **Owner-answer provenance.** I read `OD-20260914-P031-LIFECYCLE-1` and `-BATCH-GO-1` in
   `C:/CT13/DECISIONS.md:83`/`:91` and treated their content as settled per the brief; I did not attempt to
   verify the chat transcript behind them.
5. **The OD-11 owner definition.** The packet states in the same cell it recommends 2C that *"an owner
   definition of 'claims catalog-backed evidence'"* is required and *"undefined here"*. The owner answered
   2C without supplying it. I assessed the narrowest reading as implemented and found it fail-closed,
   mutation-fenced and openly disclosed — but I cannot certify conformance to a definition that does not
   exist. Owner's to close.
6. **Upstream integration.** OD-12 preserves `c76043b9`; I verified lineage (ancestor, 4 commits) but did no
   merge-tree analysis of the `HANDOFF.md` or three-way `DECISIONS.md` collisions, which are outside this
   candidate.
7. **Everything beyond M1's fixture scope.** `source_kind` is pinned to `FIXTURE` (`ledger:554-555`),
   `authoritative` is hard-`False` (`ledger:198`, `:1432`), and no real TrialRecord or P0-04 acceptance
   provenance exists. Nothing here should be read as evidence toward WP-P0-04 or WP-P0-13 acceptance, or
   toward any consumer gate.
8. **Mutation coverage outside the OD-1..OD-12 changes.** My map (§5) covers every guard those twelve answers
   added or re-shaped. I did **not** mutate the guards that predate `c76043b9` and were untouched by this
   batch; their fences are the earlier rounds' business, not this candidate's.

---

## Summary

Round 1's repair is correct and complete for what it was written to do. I rebuilt mutant M-2 from the
committed blob myself: the new test, and only the new test, turns RED (`ValueError not raised`), the restored
ledger is byte-identical and 110 pass, and the test asserts the whole invariant — old identity refused with
the exact code, candidate still FROZEN under the new identity, no admission record appended, new identity
accepted and recorded. It cannot pass for the wrong reason, and two further arms show the one test fences the
whole guard rather than one scenario. **F-1 is closed.** Conformance to all twelve owner answers holds
against the bytes, scope is still the same four paths, `G1_SCOPE_AND_CONTRACT.md` is untouched, `CHALLENGE`
stays UNRESOLVED, and every lane claim for this round reproduced exactly.

What stops a pass is what the first read's two mutants did not reach. I mutated all twenty guards the twelve
answers added or re-shaped; eighteen turn something RED, and two do not — both inside OD-7's new
registrar-refresh branch, the same branch F-1 came from. Removing either leaves the full suite green while
the ledger accepts a refresh onto a permanently retired deployment identity, or onto another candidate's
identity. The code is right; the tree does not carry the fence, which is the same standard the roster applied
to K-D-01 and to F-1. Two tests, built the way the round-1 fence was built, close the class — and because the
map is now complete rather than sampled, they close it for good.

VERDICT: REQUEST_CHANGES
