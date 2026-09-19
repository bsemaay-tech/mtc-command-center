# T0 review — WP-P0-31 M1 lifecycle ledger, candidate `48bd70dec54aba83dd4270fa0bef97b542163bda`

Reviewer: exact `claude-opus-5`, effort `xhigh`. Wednesday 2026-09-16 slot. Independent T0; first exact
flagship on this package. No delegation, no sub-agents, no other session resumed. Every command below was
run by me from the cwd stated, with the pinned interpreter, and its output is quoted verbatim.

Git usage was restricted to `rev-parse`, `show <rev>:<path>`, `diff <rev> <rev> -- <paths>`, `log`,
`rev-list --count` and `merge-base --is-ancestor` — all read-only. **No `status`, `diff` of the worktree,
`add`, `commit` or `checkout` was run in any repository.** Scratch copies for the RED arms live under
`C:/tmp/OPUS_P031_SCRATCH/`.

---

## 1. Verified identities (COMPUTED)

| Item | Value | How |
|---|---|---|
| Worktree HEAD | `48bd70dec54aba83dd4270fa0bef97b542163bda` | `git -c safe.directory=* -C C:/tmp/P031_M1_20260913 rev-parse HEAD` |
| Interpreter | `Python 3.12.12 (main, Jan 27 2026, 23:45:36) [MSC v.1944 64 bit (AMD64)]` | `…/P020_IMPL_20260912/01a0924d-…/.venv/Scripts/python.exe -VV` |
| `p031_lifecycle_ledger.py` sha256 (working tree) | `81eedf03b79289dce92019a16a56e21ed9612be8cca16660d1b79095cb7ab816` | `sha256sum` from the worktree root |
| `test_p031_lifecycle_ledger.py` sha256 (working tree) | `a6354ee31cc950b999d127583dc4c59ab66f62410fff1dd872d93b2a9ba59ca1` | same |
| `p031_lifecycle_ledger.py` sha256 (committed blob bytes) | `2bff9fcc1fc42c7780a7e40bb127f0dad79fe64dd3b17ee14d5337332f88a63d` | `git show 48bd70de:<path> \| sha256sum` |
| `test_p031_lifecycle_ledger.py` sha256 (committed blob bytes) | `23bc0925a2ebdd9940f9de804a2aa59d4aa7849a562c9aa7064fbfdcc14285a4` | same |
| Sizes | ledger 1495 lines, tests 5068 lines | `wc -l` |

The working-tree sha256 of the ledger matches the value recorded in `SHA256SUMS_P31FIX.txt` /
`DISPOSITION_P31FIX.md` (`81eedf03…`) exactly. The blob-bytes hashes differ from the working-tree hashes
only because the checkout is CRLF; both are reported so no later reader has to guess which form was pinned.

Pre-fix and base modules extracted for my RED arms (read-only `git show`):

| Revision | Path | sha256 |
|---|---|---|
| `96af3eb6` (pre-fix) | `C:/tmp/OPUS_P031_SCRATCH/prefix/p031_lifecycle_ledger.py` | `2e54ee7b62abaca2c0851ccbd1398b485d3163ce5f93c98bf162cd6146fd3c7c` |
| `c76043b9` (reviewed base) | `C:/tmp/OPUS_P031_SCRATCH/prefix/base_c76043b9.py` | `adc76e63207343333cb299ef48f409c26d1a5d276fbfa837f44726c866edf2c3` |

`2e54ee7b…` reproduces the pre-fix hash recorded in `DISPOSITION_P31FIX2.md` exactly.

Commit chain (`git log c76043b9..48bd70de`), 3 commits, `c76043b9` confirmed an ancestor:

```
48bd70de Codex GPT-5          p031: add registrar-path RED test for CATALOG_BACKED_WITHOUT_EVALUATION_HASH (Gemini delta K-D-01)
bd0d56d0 Codex GPT-5          p031: close Gemini J-01..J-05 (catalog refusal tests, catalog-backed-without-hash refusal, refresh identity arms)
96af3eb6 Claude Opus 5 Lead   p031: implement owner lifecycle answers OD-2/5/6/7/9/10/11 + OD-1 doc + OD-4/8 ratification (OD-20260914-P031-BATCH-GO-1)
```

---

## 2. Mandated commands — run by me

**Focused suite** — cwd `C:/tmp/P031_M1_20260913`:

```
$ …/.venv/Scripts/python.exe -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py -q -p no:cacheprovider
................s.................... [ 33%]
....................... [ 54%]
..................................................            [100%]
109 passed, 1 skipped, 167 subtests passed in 29.72s
```

Reproduces the claimed `109 passed, 1 skipped, 167 subtests` exactly.

**Shared contracts** — the brief's invocation **does not run**. From `C:/tmp/P031_M1_20260913`:

```
$ …/.venv/Scripts/python.exe -m pytest MTC_COMMAND_CENTER/contracts/tests -q -p no:cacheprovider
E   ModuleNotFoundError: No module named 'mtc_contracts'
… (7 identical collection errors)
7 errors in 0.30s
```

`mtc_contracts` is only importable with `MTC_COMMAND_CENTER/contracts` on `sys.path`. From that directory
the claimed count reproduces:

```
$ cd C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/contracts
$ …/.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
..................................................                       [100%]
50 passed in 0.23s
```

Recorded as finding **N-9** (record defect in the brief/lane instruction, not in the candidate).

**py_compile** — clean:

```
$ …/.venv/Scripts/python.exe -m py_compile MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py
py_compile OK
```

**Ruff** — I could **not** reproduce it: the pinned interpreter has no `ruff` module
(`No module named ruff`) and no `ruff` executable is on PATH or in that venv's `Scripts`. See NOT VERIFIED.

I did not execute the mandated commands only partially: every command I could run, I ran. The one I could
not reproduce (Ruff) is isolated in §10 and does not gate the verdict, because `py_compile` is clean and
the full suite executes.

---

## 3. Per-item answer conformance

Owner authority: `OD-20260914-P031-LIFECYCLE-1` (`C:/CT13/DECISIONS.md:83`, "each = the packet's recommended
option verbatim") and `OD-20260914-P031-BATCH-GO-1` (`:91`). Packet:
`P031_LIFECYCLE_DECISIONS_20260913_V4.md`.

| Ref | Packet option text (quoted) | Implementation (file:line) | Verdict |
|---|---|---|---|
| **OD-1** (3D) | *"move 'ratified worthiness version' from an M1 **acceptance** precondition to an **operating** precondition on writing a real `CAPTURED -> TRIAGED` record"* (packet `:1047`) | `DECISIONS.md:18` — *"an owner-ratified worthiness check-set version is instead an operating precondition for writing any real `CAPTURED -> TRIAGED` record"*, and *"A real `CAPTURED -> TRIAGED` write remains blocked until the owner ratifies an exact active worthiness check-set version."*; `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:298` — the same move plus *"until then that write remains fail-closed"*. Both amendments are documentation-only (word-diff shows exactly two edited spans). No executable change; the guard stays fail-closed (`ledger:736-740`). | **IMPLEMENTED-AS-ANSWERED** |
| **OD-2** (1B) | *"the writer supplies `next_state`; the ledger validates that it is strictly below the current rung … and that `deployment_identity_hash` is unchanged"*; *"add `DEMOTED` to the `MULTI_WORKER_SUPERVISOR` authority set … and add the corresponding descent tuples"* (packet `:451`, `:454-457`) | `LADDER_RANK` `ledger:42`; strict-descent refusal `ledger:688-693` (`DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT`); descent tuples `ledger:134-139` (all 6 strictly-descending pairs present, no others); authority `ledger:121-123` (`DEMOTED` only under `MULTI_WORKER_SUPERVISOR`); unchanged identity enforced twice — `ledger:675-686` (fires first) and `ledger:832-833`. Arms A14/A15/A16/A17/A18. | **IMPLEMENTED-AS-ANSWERED** (see N-1, N-2 on how it is recorded and fenced) |
| **OD-3** (2A) | *"add a nullable challenged-incumbent identity field … under **WP-P0-04**; keep `CHALLENGE` fail-closed until it exists"* (packet `:1049`) | `ledger:657-658` refuses every `CHALLENGE` with `CHALLENGE_INCUMBENT_DEPLOYMENT_IDENTITY_FIELD_MISSING` before any other check; `unresolved_lifecycle_contracts` still prints `"CHALLENGE INCUMBENT DEPLOYMENT IDENTITY FIELD: MISSING"` (`ledger:1451-1453`); shared contracts untouched (diff touches 4 files, none under `contracts/`). Arm A40. | **IMPLEMENTED-AS-ANSWERED** (stays UNRESOLVED as required) |
| **OD-4** (3D now) | *"ratify the current repository-wide refusal as the deliberate interim"* (packet `:1050`) — recording only | `ledger:710-721` unchanged repository-wide `SUCCESSION_ENVELOPE_UNRESOLVED`; recording added at `ledger:1456` `"ATOMIC SUCCESSION INTERIM REFUSAL: RATIFIED BY OD-4"`. Arm A39 (second LIVE member anywhere → refused). | **IMPLEMENTED-AS-ANSWERED** |
| **OD-5** (4A) | *"writer-supplied `check_set_purpose` from the declared set, validated against the candidate's rung, with `check_set_version`, `evaluation_run_hash` and non-empty `failing_checks` all mandatory. Restore `("REJECTED", "RE_ENTRY", "CANDIDATE")` in the same answer."* (packet `:1051`) | purpose required `ledger:619-622`; rung table `ledger:49-60` + check `ledger:728-731`; version required via `ledger:732-733`; hash + non-empty checks `ledger:773-777`; `REJECTED` now reachable — `ledger:70-76`; re-entry arc restored `ledger:82`. `REJECTED_PURPOSE_UNRESOLVED` removed. Arms A19-A23, A41, A43. | **IMPLEMENTED-AS-ANSWERED** (dead map row → N-8) |
| **OD-6** (5C) | *"Require the writer to supply the `check_set_version` of the gate whose slot is full, and take the target from that version's purpose instead of inferring it from `previous_state`"* (packet `:643`) | `ledger:623-626` resolves the capacity purpose as `supplied_purpose or _purpose_for_check_set_version(version)`; rung allowance `ledger:43-48` + `ledger:724-727`; append-time consistency `ledger:736-740`. Version-less capacity events from SHADOW stay fail-closed (arm A28). | **IMPLEMENTED-AS-ANSWERED, with two recorded residues** — the supplied purpose takes precedence over the version-derived one (N-4), and replay no longer re-derives this purpose (N-3) |
| **OD-7** (6A) | *"the candidate returns to `FROZEN` under the new composite; revocation stays silent-by-construction"*; *"Requires one decided transition (deep rung -> `FROZEN`, same candidate, new composite) and a relaxation of `ledger:657-658` so a re-freeze may carry the new deployment identity"* (packet `:692`, `:1053`) | transitions `ledger:77-81`; refresh detection `ledger:669-674`; identity validation `ledger:804-818` (new identity mandatory, package must match, identity must differ, retired identity refused, cross-candidate binding refused); `FROZEN_DEPLOYMENT_IDENTITY_FORBIDDEN` now applies only outside a refresh (`ledger:817-818`). Arms A02, A29-A32, A36. | **IMPLEMENTED-AS-ANSWERED in behaviour; the guard that makes revocation real is unfenced → finding F-1 (REQUIRED)** |
| **OD-8** (7A) | *"ratify as implemented: one `evaluation_run_hash` binds to exactly one `candidate_id` forever"* (packet `:1054`) — recording only | `ledger:789-790` unchanged; recording added `ledger:1460` `"EVALUATION RUN CANDIDATE SCOPE: RATIFIED BY OD-8"`. Arm A26. | **IMPLEMENTED-AS-ANSWERED** |
| **OD-9** (5a-C) | *"gate it on a **sixth, owner-only trigger class** distinct from the five automatic ones, with a mandatory recorded one-sentence external-change reason, and keep every existing constraint"* (packet `:806`) | `OWNER_EXTERNAL_CHANGE` added `ledger:95` (six total, `ledger:88-97`); RETIRED branch `ledger:758-764` requires that trigger **and** a one-sentence reason; `ledger:765-766` refuses the owner trigger from the five automatic states — so it is genuinely owner-only and RETIRED-only; freshness (`ledger:767-770`), no prior evidence (`ledger:771-772`), identities cleared (`ledger:840-841`), retired package/deployment permanently refused (`ledger:812-813`, `:819-820`) all retained. No shared-contract edit needed (`LifecycleEvent.trigger` is `NonEmptyStr \| None`). Arms A08-A13, A30, A38. | **IMPLEMENTED-AS-ANSWERED** (one-sentence test is crude → N-5; not recorded in the report → N-6) |
| **OD-10** (5b-A) | *"ratify as implemented … conditional on giving `test:2192-2288` real assertions and closing the report's disclosure gap"* (packet `:1056`) | Behaviour unchanged (`ledger:791-796` refuses prior-epoch only; epoch rollover `ledger:1105-1107`). Condition 1 met: `test_current_epoch_evaluation_may_support_multiple_decisions` (now `test:2278-2442`) carries **6 assertion calls** (`:2375, 2400, 2401, 2421, 2422, 2442`) pinning `event_type`, `check_set_purpose`, `check_set_version`, `evaluation_run_hash` and the resulting `current_state` for all three pairs — it had none in the reviewed baseline. Condition 2 met: `ledger:1461` `"SAME-EPOCH EVALUATION REUSE: RATIFIED BY OD-10"`. Arms A24, A25. | **IMPLEMENTED-AS-ANSWERED** |
| **OD-11** (2C) | *"optional configured catalog: refuse an `evaluation_run_hash` absent from an accepted catalog when one is supplied, fail closed on catalog-backed claims when none is"* (packet `:1057`), the phrase *"claims catalog-backed evidence"* being **undefined by the packet** | Optional catalog param `ledger:326`, normalization `ledger:392-403`; absent-hash refusal `ledger:748-753` (applies to **every** hash once a catalog is configured — arm A05, strictly fail-closed); no-catalog claim refusal `ledger:744-745`; claim-without-hash refusal `ledger:746-747`; `catalog_backed` must be a real `bool` (`ledger:556-557`, arms A06/A07). Narrowest reading adopted = an explicit `catalog_backed=True` (batch `REPORT.md` states this openly). Replay stays fail-closed with no catalog configured (arm A33). | **IMPLEMENTED-AS-ANSWERED under the narrowest reading.** The owner definition the packet demanded was never supplied; the reading chosen is the conservative one and is disclosed. Two costs the owner priced remain open → N-6, N-7 |
| **OD-12** (7-A) | *"preserve `c76043b9`; reconcile only when integration is authorized"* (packet `:1058`) | `c76043b9` is an ancestor of `48bd70de`; exactly 3 commits ahead; no rebase onto `fcac0ac6`; `03_QUANTLENS/HANDOFF.md` not in the diff; drift still 19 behind the 30-commit limit (`LEAD_GUARD.txt`). | **IMPLEMENTED-AS-ANSWERED** |

No item is **BROADER THAN ANSWERED** in a way that widens what the ledger accepts: every divergence I found
is either fail-closed or a recording/coverage matter. OD-6 is the only item where the implementation takes
an input the option text did not name (a writer-supplied purpose), and append-time validation keeps that
input consistent with the version — see N-3/N-4.

---

## 4. RED / GREEN per new rule

Ten refusal codes are new since `c76043b9`, two were removed (AST extraction of every `raise` argument in
both files, then `comm`):

```
NEW:      ACCEPTED_EVALUATION_CATALOG_INVALID, CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG,
          CATALOG_BACKED_INVALID, CATALOG_BACKED_WITHOUT_EVALUATION_HASH, CHECK_SET_PURPOSE_REQUIRED,
          DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT, DEPLOYMENT_REFRESH_IDENTITY_INVALID,
          EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG, FAILING_CHECKS_REQUIRED,
          RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED
REMOVED:  DEMOTION_TARGET_RUNG_MAPPING_UNRESOLVED (OD-2), REJECTED_PURPOSE_UNRESOLVED (OD-5)
```

RED evidence was produced by putting the **current** test file over the **base** ledger in a scratch tree
(`C:/tmp/OPUS_P031_SCRATCH/redtree`, contracts copied in, both file hashes re-verified) and running the
pinned pytest. Result: `81 failed, 73 passed, 1 skipped, 92 subtests passed in 14.50s`.

| New refusal | Owning in-tree test (file:line of the assertion) | RED on `c76043b9`? | GREEN on `48bd70de`? |
|---|---|---|---|
| `CHECK_SET_PURPOSE_REQUIRED` | `test_rejected_requires_purpose_hash_and_failing_checks` `:689`; `test_rejected_purpose_and_stale_evaluation_fail_closed` `:2131`, `:2146` | YES (`FAILED` both) | YES |
| `FAILING_CHECKS_REQUIRED` | `test_rejected_requires_purpose_hash_and_failing_checks` `:702` | YES | YES |
| `DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT` | `test_demoted_requires_strict_descent_and_keeps_deployment_identity` `:2503` | YES | YES |
| `DEPLOYMENT_REFRESH_IDENTITY_INVALID` | `test_deployment_refresh_returns_to_frozen_under_new_composite` `:2523`, `:2539`, `:2555`; `test_deployment_refresh_registrar_path_is_available_at_every_deep_state` `:3057` | YES (both) | YES |
| `CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG` | `test_catalog_backed_claim_fails_closed_without_catalog` `:2811` | YES | YES |
| `ACCEPTED_EVALUATION_CATALOG_INVALID` | `test_accepted_evaluation_catalog_rejects_invalid_shapes` `:2838` | YES — 6 `SUBFAILED` labels (`string`, `bytes`, `bytearray`, `uppercase-hash`, `short-hash`, `non-string-hash`) | YES |
| `CATALOG_BACKED_INVALID` | `test_catalog_backed_argument_must_be_bool` `:2866` | YES — 4 `SUBFAILED` labels (`integer`, `string`, `float`, `none`) | YES |
| `EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG` | `test_configured_catalog_refuses_absent_hash_and_accepts_present_hash` `:2902` | YES | YES |
| `CATALOG_BACKED_WITHOUT_EVALUATION_HASH` | builder arm `:2927`; **Lead arm** `test_registrar_refresh_with_catalog_backed_claim_requires_evaluation_hash` `:2989` | YES | YES |
| `RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED` | `test_retired_reentry_requires_owner_external_change_reason` `:4250` | YES | YES |

Every new refusal carries at least one in-tree arm that is RED on the reviewed base.

### D026 — which test passes on the OLD module for the wrong reason

Same scratch tree, **pre-fix** ledger `96af3eb6` under the current test file:

```
$ …/.venv/Scripts/python.exe -m pytest …/test_p031_lifecycle_ledger.py -q -p no:cacheprovider --tb=line -rf
E   AssertionError: "CATALOG_BACKED_WITHOUT_EVALUATION_HASH" does not match "EVALUATION_RUN_HASH_REQUIRED"
E   AssertionError: ValueError not raised
FAILED …::test_configured_catalog_refuses_absent_hash_and_accepts_present_hash
FAILED …::test_registrar_refresh_with_catalog_backed_claim_requires_evaluation_hash
2 failed, 107 passed, 1 skipped, 167 subtests passed in 19.47s
```

This reproduces the Lead's claim exactly and independently:

- The **builder's J-03 arm** (`test:2927`) does fail pre-fix, but with
  `"CATALOG_BACKED_WITHOUT_EVALUATION_HASH" does not match "EVALUATION_RUN_HASH_REQUIRED"` — i.e. it fences
  **refusal-code precedence** on a path an older check already refused. It is not evidence of the fail-open.
- The **Lead's arm** (`test:2946-3000`, assertion `:2989`) fails with `ValueError not raised` — a genuine
  fail-open fence, and the only real D026 evidence for `CATALOG_BACKED_WITHOUT_EVALUATION_HASH`.

My own arm A01 shows the same fail-open directly on `96af3eb6`: the registrar refresh **APPENDED**, leaving
`state=FROZEN dep=44444444` while claiming catalog-backed evidence with no hash. K-D-01 is genuinely closed.

---

## 5. My own RED arms

Harness: `C:/tmp/OPUS_P031_SCRATCH/arms/probe.py` — an independent fixture builder (my own helpers, not the
suite's), loading the module under test by file path so the same 43 arms run unchanged against any of the
three revisions. Each arm gets a fresh SQLite ledger in a fresh temp dir under
`C:/tmp/OPUS_P031_SCRATCH/work`. Nothing was written into the repository.

Command (cwd `C:/tmp/OPUS_P031_SCRATCH/arms`):

```
$ …/.venv/Scripts/python.exe probe.py <module-path> [arm-ids…]
```

Full-sweep results (outputs saved as `OUT_CURRENT_48bd70de.txt`, `OUT_PREFIX_96af3eb6.txt`):

```
MODULE: C:\tmp\P031_M1_20260913\...\p031_lifecycle_ledger.py     SUMMARY: 43 as expected, 0 NOT as expected
MODULE: C:\tmp\OPUS_P031_SCRATCH\prefix\p031_lifecycle_ledger.py SUMMARY: 42 as expected, 1 NOT as expected
  DIVERGENT A01 registrar refresh, catalog_backed=True, no hash:
      expected 'CATALOG_BACKED_WITHOUT_EVALUATION_HASH', got 'ACCEPTED -> state=FROZEN dep=44444444'
```

Selected arms, with exact observed output on `48bd70de`:

| Arm | Scenario | Expected | Observed on `48bd70de` |
|---|---|---|---|
| A01 | registrar refresh SHADOW→FROZEN, catalog configured, `catalog_backed=True`, no hash | refuse | `ValueError: CATALOG_BACKED_WITHOUT_EVALUATION_HASH` (**`ACCEPTED -> state=FROZEN` on `96af3eb6`**) |
| A02 | same refresh without the claim | accept | `ACCEPTED -> state=FROZEN dep=44444444` |
| A03 | `catalog_backed=True`, no catalog configured | refuse | `ValueError: CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG` |
| A04 | catalog-backed hash outside the catalog | refuse | `ValueError: EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG` |
| A05 | **non**-catalog-backed hash outside the catalog | refuse | `ValueError: EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG` — a configured catalog binds every hash, not only claimed ones |
| A06 / A07 | `catalog_backed=1` / `catalog_backed="true"` | refuse | `ValueError: CATALOG_BACKED_INVALID` (both) |
| A08 | RETIRED `RE_ENTRY` on `OWNER_CURIOSITY` | refuse | `ValueError: RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED` |
| A09 | RETIRED `RE_ENTRY`, owner trigger, **two-sentence** reason | refuse | `ValueError: RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED` |
| A10 | RETIRED `RE_ENTRY`, owner trigger, one sentence, fresh hash | accept | `ACCEPTED -> state=CANDIDATE pkg=None dep=None` (identities cleared) |
| A11 | `OWNER_EXTERNAL_CHANGE` used from `PARKED` | refuse | `ValueError: REENTRY_TRIGGER_INVALID` |
| A12 | RETIRED `RE_ENTRY`, semicolon run-on of four clauses | — | `ACCEPTED` → see N-5 |
| A13 | RETIRED `RE_ENTRY`, single sentence containing `v2.0` | — | `ValueError: RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED` → see N-5 |
| A14 / A15 | `DEMOTED` sideways `LIVE→LIVE` / upward `TESTNET→LIVE` | refuse | `ValueError: DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT` (both) |
| A16 | `DEMOTED` with a **changed** deployment identity | refuse | `ValueError: DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED` → see N-1 |
| A17 | `DEMOTED` issued by `PROMOTION_AUTHORITY` | refuse | `ValueError: WRITER_AUTHORITY_REFUSED` |
| A18 | lawful `DEMOTED LIVE→TESTNET`, same identity | accept | `ACCEPTED -> TESTNET` |
| A19-A22 | `REJECTED` without checks / purpose / wrong-rung purpose / without hash | refuse | `FAILING_CHECKS_REQUIRED`, `CHECK_SET_PURPOSE_REQUIRED`, `CHECK_SET_PURPOSE_MISMATCH`, `EVALUATION_RUN_HASH_REQUIRED` |
| A23 / A41 | lawful `REJECTED` at FROZEN / at SHADOW on `paper_eligibility` | accept | `state=REJECTED purpose=shadow_eligibility checks=1` / `purpose=paper_eligibility` |
| A24 | **OD-10** one run backing two purposes in one epoch | accept | `ACCEPTED -> state=TESTNET purposes=['shadow_eligibility', 'testnet_live_candidate_eligibility']` |
| A25 / A26 | cross-epoch reuse / cross-candidate reuse | refuse | `EVALUATION_RUN_HASH_REUSED` / `EVALUATION_RUN_CANDIDATE_SCOPE_UNRESOLVED` |
| A27 | **OD-6** one version registered under two purposes, writer names the target | — | `ACCEPTED -> stored purpose=paper_eligibility for an ambiguous version` → see N-4 |
| A28 | capacity withhold from SHADOW with no version | refuse | `ValueError: ADMISSION_WITHHELD_TARGET_UNRESOLVED` |
| A29 | **OD-7 × OD-10** post-refresh re-admission citing the retired identity's run | — | `ACCEPTED -> state=SHADOW dep=44444444` → see N-10 |
| A30 | re-freeze onto a RETIRED deployment identity | refuse | `ValueError: DEPLOYMENT_IDENTITY_RETIRED` |
| A31 / A32 | refresh with unchanged identity / with a changed package hash | refuse | `ValueError: DEPLOYMENT_REFRESH_IDENTITY_INVALID` (both) |
| A33 | catalog-backed record replayed by a ledger with **no** catalog | refuse | `ValueError: CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG` — replay is fail-closed |
| A34 | Registrar smuggling a ladder event through its own seam | refuse | `ValueError: WRITER_AUTHORITY_REFUSED` |
| A35 | registrar refresh carrying an evaluation hash | refuse | `ValueError: EVALUATION_RUN_HASH_NOT_APPLICABLE` |
| **A36** | **post-refresh re-admission under the OLD (revoked) identity** | refuse | `ValueError: DEPLOYMENT_IDENTITY_MISMATCH` → **F-1** |
| A37 | catalog configured, `catalog_backed` omitted, hash in catalog | accept | `ACCEPTED -> state=SHADOW stored catalog_backed=False` |
| A38 | RETIRED `RE_ENTRY` reusing a prior-epoch hash | refuse | `ValueError: REENTRY_EVALUATION_NOT_FRESH` |
| A39 | **OD-4** second LIVE member anywhere in the ledger | refuse | `ValueError: SUCCESSION_ENVELOPE_UNRESOLVED` |
| A40 | `CHALLENGE` | refuse | `ValueError: CHALLENGE_INCUMBENT_DEPLOYMENT_IDENTITY_FIELD_MISSING` |
| A42 | supplied purpose contradicting a non-`REJECTED` event's fixed purpose | refuse | `ValueError: CHECK_SET_PURPOSE_MISMATCH` |
| A43 | `REJECTED` issued by `MULTI_WORKER_SUPERVISOR` | refuse | `ValueError: WRITER_AUTHORITY_REFUSED` |

### Mutation arms (falsifying the fences, not the behaviour)

Two single-guard deletions, each applied to a copy of the candidate ledger in the scratch tree, then the
**whole in-tree suite** re-run on the pinned interpreter:

| Mutant | Guard removed | Suite result | Arm result |
|---|---|---|---|
| M-1 | `ledger:675-686` (`DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED`) | `4 failed, 109 passed, 1 skipped, 163 subtests` — 4 `SUBFAILED` in `test_deployment_refresh_registrar_path_is_available_at_every_deep_state` (`TESTNET`, `LIVE_CANDIDATE`, `LIVE`, `SUSPENDED`) | A16 still refuses, now as `DEPLOYMENT_IDENTITY_MISMATCH` — the invariant survives on the second guard |
| **M-2** | `ledger:832-833` (`DEPLOYMENT_IDENTITY_MISMATCH`) | **`109 passed, 1 skipped, 167 subtests passed` — fully GREEN** | **A36 becomes `ACCEPTED -> SHADOW`**: the candidate is re-admitted under the revoked, pre-refresh deployment identity |

M-2 is the basis of finding F-1.

---

## 6. Scope and protected paths

`git diff --name-status c76043b9 48bd70de` — exactly four paths, matching the brief:

```
M  DECISIONS.md                                                                    (+1/-1, one table row)
M  MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py                  (257 lines changed)
M  MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py       (760 lines changed)
M  MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md  (+1/-1, one paragraph)
 4 files changed, 887 insertions(+), 134 deletions(-)
```

- Nothing under `MTC_COMMAND_CENTER/contracts/` — the shared `LifecycleEvent` / `LifecycleWriterClass`
  bytes are untouched, as `G1_SCOPE_AND_CONTRACT.md:11` requires. Both documentation edits are the exact
  OD-1 amendments and nothing else (word-diff: two spans).
- No protected scopes, no Pine, no runtime, no host, no credentials, no exporter paths.
- `G1_SCOPE_AND_CONTRACT.md` does **not** live inside the repository at all — it is at
  `C:/tmp/P031_LEAD_20260912/G1_SCOPE_AND_CONTRACT.md`, sha256
  `1752290cb9dd81d75ce5ca65a1dd5510584151101e088ce08c638fadb8195d8a`, mtime **2026-09-12 21:45**, i.e.
  unmodified since two days before the batch. It is untouched, as the brief requires — and that is itself
  the subject of N-7.
- `CHALLENGE` stays UNRESOLVED (§3 OD-3, arm A40).
- The worktree carries three untracked scratch files (`TASK_P31B.md`, `TASK_P31B_CONT.md`,
  `TASK_P31FIX.md`) that are not in the commit and not in the diff; `LEAD_GUARD.txt` records the same three
  and returns `RESULT: PASS` with `[protected] none` and `[untracked] no risky files`.

---

## 7. Lead authorship of `48bd70de`

Confirmed test-only and confirmed disclosed. `git show 48bd70de --stat`:

```
 .../tools/tests/test_p031_lifecycle_ledger.py      | 56 ++++++++++++++++++++++
 1 file changed, 56 insertions(+)
```

`p031_lifecycle_ledger.py` is not in that commit. The message names the authorship, the reason (every Codex
home capped on 2026-09-15), and the RED/GREEN evidence; `DISPOSITION_P31FIX2.md` repeats it. I reproduced
both halves of its claim independently: RED on `96af3eb6` (`ValueError not raised`), GREEN here.

**It does not change my verdict**, and the test it adds is correct and is the real D026 fence for
K-D-01 — which I verified rather than accepted. Gemini's K-D-02 nit (a Lead-authored change still takes the
standard roster) is the right disposition and is already being honoured by this review and the pending
exact Sol slot. I need nothing beyond that.

One caution for the Lead, not a finding against the commit: the repair for **F-1** below should not be
written by the Lead as well if a Codex or other independent route is available by then. Two consecutive
Lead-authored fences on the same package narrows the independence the roster is supposed to supply.

---

## 8. Report honesty

| Claim | Source | My check |
|---|---|---|
| `109 passed, 1 skipped, 167 subtests` on 3.12.12 | `LEAD_PYTEST_312.txt` (108 at `bd0d56d0`), `DISPOSITION_P31FIX2.md` | **Reproduced exactly** (29.72s here). The 108→109 step is the one test `48bd70de` adds. Consistent. |
| contracts `50 passed` | `LEAD_CONTRACTS_312.txt` | **Reproduced** — but not by the brief's invocation. See N-9. |
| Codex sandbox ran Python 3.14.2, no 3.12, no ruff | `DISPOSITION_P31FIX.md` | Self-consistent and honestly stated (`py -3.12 --version` → `No suitable Python runtime found`; `No module named ruff`). The Lead re-ran on 3.12.12. Correct as described. |
| pre-fix ledger sha256 `2e54ee7b…` | `DISPOSITION_P31FIX2.md` | **Reproduced exactly.** |
| candidate ledger sha256 `81eedf03…` | `SHA256SUMS_P31FIX.txt` | **Reproduced exactly.** |
| Builder's J-03 test fails pre-fix only by refusal-code precedence; the Lead's `:2946` test is the real fence | `LEAD_ADJUDICATION_DELTA_G38.md`, brief §3 | **Reproduced exactly** (§4 above). |
| Batch `REPORT.md` per-answer citations (`ledger:320`, `:388`, `:738`, `:741`, `:1443`, `:1446`; `test:2556`, `:2775`, `:2795`, `:4864`) | `P031_BATCH_CANDIDATE_20260914/REPORT.md` | **All ten verified against `96af3eb6` bytes** — each line is what the report says it is. (They are 6-8 lines stale against current HEAD because `bd0d56d0` inserted 8 lines; that is expected for a report about `96af3eb6`.) |
| J-01/J-02 "FIXED" with ledger line citations | `DISPOSITION_P31FIX.md` | Accurate as written: `bd0d56d0` changed the ledger **only** by the docstring plus the two-line `CATALOG_BACKED_WITHOUT_EVALUATION_HASH` refusal (verified by `git diff bd0d56d0^ bd0d56d0`). The J-01/J-02 refusals already existed at `96af3eb6:393,396,551`; Gemini filed both as *"MISSING RED ARM"*, so a test-only repair is the right one and the disposition's Tests column names it. No overclaim. |
| J-04 disposition correction | `DISPOSITION_P31FIX.md` | **WRONG at runtime** → finding N-1. |
| Repo guard `RESULT: PASS`, 19 behind limit 30 | `LEAD_GUARD.txt` | Contents consistent with the diff and with the three untracked scratch files. Not independently re-run (see §10). |
| Ruff `All checks passed!` | `LEAD_RUFF.txt` | **Not reproducible here** (see §10). |
| M1 acceptance gate cited as `plan:654` | packet Item 3 reason 1 (`:376`) | **Stale by two lines.** `plan:654` is WP-P0-31's *"Depends on"* bullet; the acceptance gate is `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:656`. The packet's *characterisation* of the gate is accurate; only the pin is off. Corrected here because F-1 rests on that sentence. |

---

## 9. Findings

### F-1 [REQUIRED] — OD-7's revocation invariant rests on one unfenced line pair; deleting it leaves the suite fully green

**Where:** `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:832-833`

```python
832            if current_deployment is not None and deployment_hash != current_deployment:
833                raise ValueError("DEPLOYMENT_IDENTITY_MISMATCH")
```

**What OD-7 bought.** Option 6A's whole mechanism is *"revocation is expressed by the absence of admission
records for that new identity"* (packet `:692`), backing `brief:2211` *"A material identity change revokes
admission."* The refresh itself (`ledger:804-818`) only lands the candidate at `FROZEN` under the new
composite. The rule that then **forces the climb to be made under the new identity** — rather than letting
an admission authority quietly re-admit the candidate under the identity that was just revoked — is
`:832-833` and nothing else. `:675-686` cannot help: its `actual_state` guard lists
`{SHADOW, TESTNET, LIVE_CANDIDATE, LIVE, SUSPENDED}` and the post-refresh state is `FROZEN`.

**Why it is new.** In the reviewed base `c76043b9` this guard was effectively dead. `REGISTRAR_TRANSITIONS`
there had no deep-rung→`FROZEN` arc (verified: the base set is 9 tuples, `CANDIDATE -> FROZEN` only) and
`FROZEN` unconditionally forbade a deployment identity (`base:658`
`FROZEN_DEPLOYMENT_IDENTITY_FORBIDDEN`), so `current["deployment_identity_hash"]` could never be non-`None`
at `FROZEN`; at every deep rung `:675-686` shadows it. **OD-7 promoted dead code to the single
load-bearing guard of its own answer, and the batch added no test for it.**

**Evidence — mutation M-2, run by me.** Copy of the candidate ledger with exactly those two lines removed,
placed in `C:/tmp/OPUS_P031_SCRATCH/redtree` under the unmodified current test file (both hashes
re-verified), pinned interpreter:

```
$ …/.venv/Scripts/python.exe -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py -q -p no:cacheprovider --tb=no -rf
................s.................... [ 33%]
....................... [ 54%]
..................................................            [100%]
109 passed, 1 skipped, 167 subtests passed in 19.08s
```

**Fully green**, identical to the candidate's own result. And on that same mutant, arm A36:

```
XX  A36 post-refresh re-admission on the OLD identity
      expect: DEPLOYMENT_IDENTITY_MISMATCH
      got   : ACCEPTED -> SHADOW
```

For completeness, the string appears **zero** times in the 5068-line test file:
`grep -n "DEPLOYMENT_IDENTITY_MISMATCH" test_p031_lifecycle_ledger.py` → no matches (the only two hits for
either identity guard are `DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED` at `test:3042` and `test:3109`).

**Failure scenario.** A candidate at SHADOW under `deployment_identity_hash = D1`. The Registrar performs
the OD-7 refresh to `FROZEN` under `D2` (allocator/Guardian/cost-lineage change — `brief:1435`). The
Environment Admission Authority then appends `SHADOW_ELIGIBLE` carrying `D1`. Today that is refused. If
`:832-833` is ever touched — refactored, reordered, folded into the `:675-686` condition, or moved behind
the deep-rung guard — the ledger will accept it, write `deployment_identity_hash = D1` back into
`lifecycle_current`, and the revoked identity silently regains its admission, with the full suite still
reporting `109 passed`. That is `brief:745`'s *"evidence about a different system"* re-attached to a
retired composite, and it is precisely the silent-revocation failure OD-7 exists to make impossible.

**Severity.** The shipped code is correct — this is not a live fail-open. It is a D026 defect, and it is
the M1 acceptance gate's own standard. `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:656`
(verified in the worktree; the packet cites this as `plan:654`, which is stale — see §8):

> "attempted edit/delete, duplicate transition, illegal transition and unauthorized writer are each shown
> **RED without the guard and GREEN with it** under D026 … every `REJECTED`, `DECLINED`, `PARKED`,
> re-entry, admission, promotion, suspension, demotion, retirement and succession record **retains its
> evidence and identity lineage**."

"RED without the guard" is precisely the test M-2 applies, and `:832-833` fails it: the guard is removed and
nothing turns red. What it protects is the identity lineage of an admission record — named explicitly in
the same sentence. It is the same defect class the roster already ruled REQUIRED five days ago as K-D-01
(*"the Lead's probe proved the edge, but the tree must carry the fence"*,
`LEAD_ADJUDICATION_DELTA_G38.md`) — and the evidence here is strictly stronger than K-D-01's, because a
one-guard mutation leaves the suite entirely green.

**Repair (one test, no ledger change).** In `LifecycleLedgerTests`: build to SHADOW under `DEPLOYMENT_A`;
registrar-refresh SHADOW→FROZEN under `DEPLOYMENT_B`; assert that `SHADOW_ELIGIBLE` carrying
`DEPLOYMENT_A` raises `ValueError` matching `DEPLOYMENT_IDENTITY_MISMATCH` and that the candidate is still
`FROZEN`; then assert the same admission under `DEPLOYMENT_B` succeeds and records `DEPLOYMENT_B`. My
arm A36 in `C:/tmp/OPUS_P031_SCRATCH/arms/probe.py` is a working template. Verify it RED against
mutant M-2 (or against `c76043b9`), not merely GREEN here.

---

### N-1 [NIT] — the J-04 disposition correction names a guard that never fires for `DEMOTED`

**Where:** `P031_FIX_20260915/DISPOSITION_P31FIX.md`, row J-04 — *"unchanged DEMOTED deployment identity is
enforced by `DEPLOYMENT_IDENTITY_MISMATCH` at …:832 and …:833"* (adopted from Gemini J-04, which cited
`:824-825` in the `96af3eb6` numbering).

A `DEMOTED` always has `previous_state ∈ {TESTNET, LIVE_CANDIDATE, LIVE}` (`ledger:134-139`), all inside
`:672-673`'s deep-rung set, so `:675-686` always precedes. Arm A16, observed:

```
OK  A16 DEMOTED with a changed deployment identity
      expect: DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED
      got   : ValueError: DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED
```

The **rule holds** — mutation M-1 shows `:832-833` catches it if `:675-686` is removed, so OD-2's identity
half is genuinely double-guarded. Only the written record is wrong. Two reviewers (Gemini, then the Lead
adopting the correction) asserted an enforcement point neither executed. Correct the disposition to name
`:686` as the observed refusal and `:832-833` as the backstop.

### N-2 [NIT] — `test_demoted_requires_strict_descent_and_keeps_deployment_identity` does not test the half its name claims

**Where:** `test_p031_lifecycle_ledger.py:2484-2515`. The descent half has a real negative arm (`:2503`).
The identity half has only the positive assertion `:2501`
(`assertEqual(state["deployment_identity_hash"], DEPLOYMENT_A)`) — there is no arm appending a `DEMOTED`
with a *changed* identity. The invariant is separately fenced by
`test_deployment_refresh_registrar_path_is_available_at_every_deep_state` (mutation M-1 produced 4
`SUBFAILED` there), so this is a naming and locality matter, not a hole. Adding one changed-identity arm to
the demotion test would put OD-2's fence where a reader of OD-2 will look for it.

### N-3 [NIT] — OD-6 removed a replay-seam invariant the packet relied on

**Where:** `ledger:623-626` with `ledger:1046-1050`.

For `ADMISSION_WITHHELD_CAPACITY`, `_resolve_check_set_purpose` returns
`supplied_check_set_purpose or …`, so at replay (`:1046-1050`, `enforce_active=False`) the re-derived
purpose is definitionally whatever was stored, and the equality check cannot disagree. Proven by direct
call on the candidate module:

```
stored_purpose='promotion'   version='paper-eligibility.v1' -> re-derived 'promotion'   EQUAL (replay cannot disagree)
stored_purpose='supervisor'  version='paper-eligibility.v1' -> re-derived 'supervisor'  EQUAL (replay cannot disagree)
```

Purpose↔version consistency for this event type is now enforced **only** at append (`:736-740`). The packet
cited *"Replay re-derives the purpose from the event and refuses any stored record whose purpose
disagrees"* as a standing property of the design (Item 3); after 5C it no longer holds for this one event
type. Practical exposure is small — the digest chain covers the evidence bytes and the module's own
`assurance_limits` already disclaims omission-proofing — but the property should be re-stated accurately,
or the replay seam given the version-derived cross-check for this event type.

### N-4 [NIT] — OD-6: an ambiguous `check_set_version` lets the writer name the withheld target

**Where:** `ledger:596-606` (`_purpose_for_check_set_version` returns `None` on `len(matches) != 1`) and
`ledger:623-626`. Option 5C says *"take the target from that version's purpose"*. If one version string is
registered under two purposes, the derivation yields `None` and the writer-supplied purpose decides. Arm
A27, observed: `ACCEPTED -> stored purpose=paper_eligibility for an ambiguous version` — and supplying
`testnet_live_candidate_eligibility` instead is equally accepted. The exact ambiguity 5C existed to remove
returns, sourced from configuration rather than from `previous_state`. A well-formed `active_check_sets`
never registers one version under two purposes, so this is configuration-avoidable — but nothing refuses
such a registration at construction (`ledger:365-390` validates shape only).

### N-5 [NIT] — the one-sentence test is both too weak and too strong

**Where:** `ledger:261-265`. `_is_one_sentence` accepts iff the stripped reason ends in `.!?` and contains
exactly one such character. Consequences, both observed:

- A12 — `"The venue relisted the pair; the cost model is stale; I want a rerun; also the owner is curious."`
  → **ACCEPTED** as one sentence. OD-9's *"names, in one sentence, the specific external thing that
  changed"* (`brief:1544`) is not enforced against a semicolon run-on.
- A13 — `"The venue upgraded its matching engine to v2.0."` → **REFUSED**
  (`RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED`). A genuine single sentence containing a version
  number, an abbreviation or a decimal cannot be recorded.

Fail-closed in the second case and fail-open only against prose style in the first, so the severity is low;
but an owner writing the mandated note will hit A13 on the first realistic reason they type.

### N-6 [NIT] — the report records OD-2/4/5/6/7/8/10 but not OD-9 or OD-11, and never discloses the catalog

**Where:** `ledger:1451-1462`, verified by rendering a real report:

```
unresolved_lifecycle_contracts: ["CHALLENGE INCUMBENT DEPLOYMENT IDENTITY FIELD: MISSING"]
ratified_lifecycle_contracts:   ["DEMOTED TARGET RUNG MAPPING: RESOLVED BY OD-2",
                                 "ATOMIC SUCCESSION INTERIM REFUSAL: RATIFIED BY OD-4",
                                 "REJECTED FAILED-GATE PURPOSE: RESOLVED BY OD-5",
                                 "ADMISSION WITHHELD CAPACITY TARGET: RESOLVED BY OD-6",
                                 "DEPLOYMENT REFRESH ENVELOPE: RESOLVED BY OD-7",
                                 "EVALUATION RUN CANDIDATE SCOPE: RATIFIED BY OD-8",
                                 "SAME-EPOCH EVALUATION REUSE: RATIFIED BY OD-10"]
top-level keys with "catalog": []
```

Two gaps. (a) OD-9's new owner-only trigger class and OD-11's catalog are the two answers that changed what
a writer may claim, and neither is recorded anywhere in the rendered report. (b) The report prints
per-record `catalog_backed` (`ledger:1429`) but nothing about the ledger's catalog **configuration** — so a
reader cannot distinguish `catalog_backed: false` meaning *"the writer made no claim"* from *"no catalog is
configured, so no claim was possible."* That is the same disclosure gap the packet required closing for
OD-10 (Item 5(b) condition 2), applied to the answer that introduced the catalog.

### N-7 [NIT] — the frozen public seam in `G1_SCOPE_AND_CONTRACT.md` was changed without the amendment its own `:18` requires

`G1_SCOPE_AND_CONTRACT.md:18` — *"The exact spelling may be minimally adjusted by the implementer only if
tests and this file are updated before parallel work consumes it."* The tests were updated; the file was
not (sha256 `1752290c…`, mtime 2026-09-12 21:45). It still reads
`LifecycleLedger(path, writer_allowlist, active_check_sets=())` (`:20`) and
`append(event, *, check_set_version=None, evaluation_run_hash=None, failing_checks=(), source_kind="FIXTURE")`
(`:24`), while the candidate's constructor gained `accepted_evaluation_catalog` (`ledger:326`) and `append`
gained `check_set_purpose` and `catalog_backed` (`ledger:855-856`). The owner's OD-11 cost cell named this
amendment explicitly (packet `:1057`).

Two mitigations, both real: the batch `REPORT.md` discloses it openly — *"`G1_SCOPE_AND_CONTRACT.md`
amendment remains pending as a separate owner act; this lane did not touch it"* — so it is an open owner
item, not a concealed one; and `:74` (*"No real TrialRecord bytes are consumed in this slice"*) remains
literally true, since the catalog is a caller-supplied set of hash strings and no TrialRecord byte is read.

**This is also a conflict between two instructions the Lead should resolve before assembling the roster:**
the review brief says `G1_SCOPE_AND_CONTRACT.md` *"must be untouched"*, while `:18` and the owner's OD-11
cost cell both require it to be amended for this change to be in-contract. I have reported the state, not
chosen between them.

### N-8 [NIT] — dead row in the OD-5 rung table

`ledger:50` maps `"CAPTURED" -> {"worthiness"}` in `REJECTED_PURPOSES_BY_RUNG`, but no
`("CAPTURED", "REJECTED", "REJECTED")` tuple exists in `REGISTRAR_TRANSITIONS` (`ledger:62-87`) and
`ILLEGAL_TRANSITION` (`ledger:696-697`) precedes the rung check (`ledger:728-731`). The row is unreachable.
Harmless; remove it or add the arc deliberately.

### N-9 [NIT] — the mandated contracts invocation does not run from the worktree root

See §2. `python -m pytest MTC_COMMAND_CENTER/contracts/tests …` from `C:/tmp/P031_M1_20260913` fails
collection on all seven modules with `ModuleNotFoundError: No module named 'mtc_contracts'`; the 50 pass
from `MTC_COMMAND_CENTER/contracts` as cwd. A record defect in the brief and in the lane instructions, not
in the candidate — but any reviewer following it literally would report a false failure.

### N-10 [NIT] — OD-7 × OD-10 interaction: a refresh does not open a new evaluation epoch

Arm A29, observed: `ACCEPTED -> state=SHADOW dep=44444444 re-admitted on the SAME evaluation_run_hash as
the retired identity`. Epochs turn over only at `RE_ENTRY` (`ledger:1105-1107`), so after an OD-7 refresh
the **new** composite's first admission may cite the very evaluation run that justified the **revoked**
one. `brief:2211`'s *"a material identity change revokes admission"* is satisfied in the sense OD-7 chose —
a fresh admission **record** is required — but nothing requires fresh evaluation **evidence**, and OD-10
positively permits the reuse within an epoch. No owner answer settles this; the packet never raised it, and
the report does not disclose it. I am not proposing a semantic change (that would need the owner). Record
it as an open lifecycle question so the next round does not inherit it silently.

---

## 10. NOT VERIFIED

1. **Ruff.** `LEAD_RUFF.txt` records `All checks passed!` for `--select E9,F821,F811`. The pinned
   interpreter has no `ruff` module and no `ruff` executable exists on PATH or in that venv's `Scripts`, so
   I could not reproduce it. `py_compile` is clean on both files and the whole suite executes, so nothing
   in my verdict depends on it.
2. **Repo guard.** I did not re-run `LEAD_GUARD.txt`'s dry-run, because the brief forbids `git status` in
   any repository and the guard inspects working-tree state. Its contents are consistent with the diff I
   did verify (four modified paths, three untracked scratch files, `[protected] none`).
3. **Gemini transport evidence.** I read `LEAD_ADJUDICATION_DELTA_G38.md` and both delta reports, but I did
   not re-derive the wrapper hashes, the 30/30 native-read audit, or the conversation id. The Gemini slot
   is not mine to re-adjudicate; I verified its *findings* against bytes instead, which is what matters
   here (J-01..J-05 and K-D-01 all independently reproduced or confirmed).
4. **Owner-answer provenance.** I read `OD-20260914-P031-LIFECYCLE-1` / `-BATCH-GO-1` in
   `C:/CT13/DECISIONS.md` and `OWNER_ANSWERS_20260914.md` and treated their content as settled per the
   brief. I did not attempt to verify the chat transcript behind them.
5. **The OD-11 owner definition.** The packet states plainly that *"what counts as a record that 'claims
   catalog-backed evidence'"* is undefined and *"is not defined by this packet"*. The owner answered 2C
   without supplying it. I assessed the narrowest reading as implemented and found it fail-closed and
   disclosed, but I cannot certify conformance to a definition that does not exist. This is the owner's to
   close, not the roster's.
6. **Upstream integration.** OD-12 preserves `c76043b9`; I verified lineage and drift (19 of 30) but did
   not attempt any merge-tree analysis of the `03_QUANTLENS/HANDOFF.md` or three-way `DECISIONS.md`
   collisions, which are outside this candidate and outside my slot.
7. **Everything beyond M1's fixture scope.** `source_kind` is pinned to `FIXTURE` (`ledger:554-555`),
   `authoritative` is hard-`False` (`ledger:198`, `:1432`), and no real TrialRecord or P0-04 acceptance
   provenance exists. Nothing in this report should be read as evidence toward WP-P0-04 or WP-P0-13
   acceptance, or toward any consumer gate.

---

## Summary

The batch does what the twelve owner answers say, and it does it fail-closed: 43 independent arms on the
candidate all behaved as specified, including every one the brief named. The fail-open the previous round
found (`CATALOG_BACKED_WITHOUT_EVALUATION_HASH`) is genuinely closed, and I reproduced both the pre-fix
fail-open and the precedence artefact in the builder's arm exactly as the Lead described them. Scope is
clean, the documentation amendments are exactly OD-1, and OD-12 is preserved.

One thing blocks a pass. OD-7 is the answer that turned a dead guard into the single line pair standing
between a revoked deployment identity and a re-admission, and the tree carries no counterfactual for it —
deleting those two lines leaves all 109 tests green while the ledger accepts the revoked identity. That is
the same standard the roster applied to K-D-01 one week ago, and applying it consistently means one more
test before this candidate is accepted.

VERDICT: REQUEST_CHANGES
