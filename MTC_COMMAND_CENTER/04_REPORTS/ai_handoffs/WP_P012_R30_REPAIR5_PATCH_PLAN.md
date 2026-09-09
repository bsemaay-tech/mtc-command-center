# WP-P0-12 re-seal #30 — repair round 5: diagnosis, patch plan, risk, D026 RED/GREEN

Task id: **`WP-P012-R30-REPAIR5`**
Author: Claude Opus 5 (Lead), session `tradingview-lab-clean-c1`, 2026-09-09.
Branch `feature/p012-reseal30-batch-20260908`, base head `56a680ad`.

Discharges items 1, 2 and 3 of the `PROTECTED_PATHS_POLICY.md` modification gate, and the
`AUTONOMY_AUTHORIZATION.md` requirement to **record a D026 RED/GREEN plan before dispatch** — the
requirement round 4 missed and which `gpt-5.6-sol` graded BLOCKING.

## 0. Owner rulings this round rests on (2026-09-09, one batch)

1. **Write lane released.** The Codex `/root/p012_reseal22_impl` lane holding
   `CONTRACT_TABLES_MANIFEST.json` is ruled finished. Evidence put to the owner before he ruled: last
   commit `015f7449` 2026-09-07 14:03, **0 commits ahead of `origin/master`**, newest file written
   anywhere under `C:\WP012BUILD` 2026-09-07 16:47, no process holding it, no scheduled task
   referencing it, worktree clean tracked and untracked. He was told explicitly that under the file's
   own rule 4 none of that *proves* liveness, and that the two hard blockers rule 4 names — a
   process/scheduled-task dependency, and unknown ownership or purpose — were both absent.
2. **Modification-gate item 5 waived** for `d3a3fb88`, `fa7b92a3` and `2f1008ab`, recorded as a
   waiver rather than as a gate satisfied.
3. **Design re-title deferred** to the next cascade. Two of three reviewers graded the
   `v1.24` title / `v1.25` change-log contradiction BLOCKING; the owner ruled to merge as-is and pay
   the re-title when a cascade is happening anyway. **The finding is deferred, not closed.**

All three were selected from offered options against real alternatives. The owner typed no free text
this round; nothing is attributed to him as a quotation.

## 1. Diagnosis

`CONTRACT_TABLES_MANIFEST.json` `seal_state.reason` ends:

> Base C30 is provisional; NONACCEPTED until forward repin F30.

`seal.set_by` reads `R30 re-seal #30, forward repin F30, 2026-09-08T19:59:27+03:00`. Commit
identities, from `git log`:

```
0c01b350  re-seal #30            = C30
d06aa741  F30 decision-147 forward repin to the re-seal #30 commit   = F30, already in history
```

So `seal_state` declares the package NONACCEPTED pending a step its sibling field records as
complete. Found by `gpt-5.6-sol` in round 4 and graded BLOCKING on the ground that an *active* state
block declaring NONACCEPTED on an already-met condition is not a prose nit.

`seal_state` is read by **zero** `.py` files, so no gate can detect it. Eighth member of the
declared-but-unchecked family, and it is adjacent to the field repair 3 corrected — repair 3 moved the
value and left this sentence behind, which is the same defect family it was fixing.

## 2. D026 RED/GREEN plan — recorded BEFORE dispatch

The round-4 verification could not have discriminated its own defect, because the gate does not read
`seal_state`. This predicate is written first, and is required to **fail on the unrepaired state**
before any edit is made. It tests the *contradiction*, never the replacement wording, so it cannot be
satisfied by any particular phrasing.

```python
m = json.load(open(CONTRACT_TABLES_MANIFEST))
f30_done      = 'forward repin F30' in m['seal']['set_by']
still_pending = 'NONACCEPTED until forward repin F30' in m['seal_state']['reason']
# invariant: these must never both be true
assert not (f30_done and still_pending)
```

**Recorded expected results, before the edit:**

| when | expected | measured |
|---|---|---|
| at `56a680ad`, before the edit | **RED** (exit 1) | **RED** — `f30_done=True`, `still_pending=True` |
| after the edit | **GREEN** (exit 0) | to be recorded in the verification section |

The RED run was executed at 2026-09-09 20:4x against head `56a680ad` and is reproduced above.

## 3. Patch plan

One commit, carrying `APPROVED-PATCH-PLAN: WP-P012-R30-REPAIR5`.

`CONTRACT_TABLES_MANIFEST.json` — replace the final sentence of `seal_state.reason` so it states the
completed fact rather than a pending condition. Nothing else in the file changes. The seal, the 19
sealed members, `seal.IMPLEMENTATION_BASE_SHA`, `seal_state.IMPLEMENTATION_BASE_SHA`, both
`EXPECTED_SEAL_SHA` fields and every history entry are untouched.

**This edit is NOT length-preserving**, unlike repairs 2 and 3, so the byte delta is meaningful here —
but the changed line is still read back rather than inferred from `git diff --numstat`.

## 4. Risk report

| risk | assessment |
|---|---|
| Seal moves | **None.** The manifest is not one of the 19 sealed members. |
| Receipt / design / anchor identities move | **None.** None pins this file or this field. |
| Ratification chain affected | **No.** `derive_semantic_coverage_review_chain` reads `reseal_history` `actor` strings only; no `actor` changes. |
| Wrong field edited | Mitigated: the target sentence is verified unique before the edit, the diff line is read back, and the D026 predicate must flip RED→GREEN. |
| JSON reformatting | Surgical text substitution; **not** the project's `canonical_json_bytes`, which minifies. |
| Write-lane conflict | Resolved by owner ruling 0.1. `SESSION_LOCK.md` row 1 is marked RELEASED with reconciliation in the same round, before this edit. |
| Repair cap | The owner authorised repairs beyond the cap of 3 on 2026-09-09 and instructed that he not be asked again. |

## 5. Verification plan

1. D026 predicate → must be **GREEN**.
2. Full gate from a separate clone, kernel identity confirmed first; receipt diffed against the
   `e58f4b39` receipt, where **only `observed_build_sha` may differ**.
3. All four identity chain walks → zero breaks.
4. `git diff` line read back; `numstat` recorded.

Results go in `WP_P012_R30_REPAIR5_VERIFICATION_REPORT.md`, written **in the same round**, not later.

## 6. What this round still does not fix

- The **design version contradiction** — deferred by owner ruling 0.3, not closed. Two of three
  reviewers hold it BLOCKING.
- **`section_16_review.status`** still `PENDING` and still stating the review "has NOT been
  performed", while the receipt is installed and validated.
- **`repository_evidence_identity`** — a true pre-repin snapshot presented as a current-looking
  top-level identity with present-tense prose and no captured-at label.
- The **absent fail-closed schema validator** over all declared manifest fields, which all three
  reviewers identify as the actual fix for this whole defect family. Harness change, protected scope,
  needs the owner.

---

## 7. CORRECTION, added 2026-09-09 22:00 by the Lead

**Section 2's claim that the predicate "tests the contradiction rather than any replacement wording,
so it cannot be satisfied by phrasing" is FALSE, and is withdrawn.**

Both flagship auditors measured it independently in round 5. `still_pending` is a single literal
substring test for `'NONACCEPTED until forward repin F30'`. Rewording the *unrepaired* text — Opus
used `until` → `pending`, Sol used *"NONACCEPTED pending completion of forward repin F30"* — flips the
predicate GREEN with the contradiction fully intact. Both graded it a NIT because the replacement
actually applied is independently true, but the claim about the predicate was wrong.

A correct predicate would compare the two fields semantically, or assert the absence of any
pending-condition phrasing, rather than matching one literal string.

The RED→GREEN result in §2 still stands: the predicate did fail on the real unrepaired state and pass
on the repaired one. What it does not have is the immunity to rewording that was claimed for it.

**A second false statement from this session is corrected in `TASK_HISTORY` event HIST-2026-0022:**
the claim that the gate never reads the design version string. It does —
`verify_bceg.py:503` extracts it from line 1, `:66-74` lists `design_version` as a content identity
key, and `:650-654` refuses when it differs from the receipt. That false statement is what the owner's
deferral in HIST-2026-0021 was granted on; it has since been superseded by the overrule in
HIST-2026-0023.
