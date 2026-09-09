# WP-P0-12 re-seal #30 — repair round 4 verification report

Task id: **`WP-P012-R30-REPAIR4`**. Discharges item 6 of the modification gate in
`MTC_COMMAND_CENTER/09_DOCS/PROTECTED_PATHS_POLICY.md`, promised by
`WP_P012_R30_REPAIR4_PATCH_PLAN.md` §4.

Author: Claude Opus 5 (Lead), session `tradingview-lab-clean-c1`, 2026-09-09.
Verified head: **`e58f4b39d5a9fe9fa890039455f16abb942663ea`**.

**Written late, and that is itself an audit finding.** Both flagship auditors graded the absence of
this artifact BLOCKING in round 4 — Opus: *"the gate the Lead invokes is 5/6 for the very commits
invoking it."* Every verification below was performed at the time; the report was not written. The
finding is recorded here rather than quietly satisfied by back-dating.

## 1. Full gate at the new head, from a clone, kernel identity confirmed first

Clone `C:\tmp\P012_LEADGATE30` at `e58f4b39`, tracked-clean.

```
KERNEL_PATH = ['C:\tmp\P012_LEADGATE30\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2']
```

The stale `mtc_v2` under `C:\LAB\Tradingview_LAB_CLEAN` did not leak in. Gate result:

| field | value |
|---|---|
| `claim_label` | `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_ACCEPTED` |
| `acceptance_blockers` | `[]` |
| self-tests | 475 passed / 0 failed |
| probes | 10/10 `DETECTED`, 10/10 `PROBE_DIGEST_MATCH` |
| scenarios | 17 — 9 `REFUSED_DECLARED_DIVERGENCE`, 8 `GREEN_SHARED_PROJECTION_EQUAL` |
| seal | `b6ac5a46…` recomputed from the 19 members |
| design pin | `c4bb6f67…` / 2072 lines |

## 2. Receipt compared against the round-3 receipt

Only `observed_build_sha` differs (`2f1008ab` → `e58f4b39`) — a one-line unified diff. `claude-opus-5`
independently ran a structural leaf diff and reported no key added or removed and exactly one leaf
changed, the same one.

**Three-party reproduction.** The Lead, Opus and Sol receipts at this head are byte-identical once the
clone path is normalised, all hashing to `dbd8a615bb26eba31ec841ceeb3ab7f42d250de352604663234b26ca8a7e291f`.

## 3. Chain walks

| chain | entries | breaks |
|---|---|---|
| `manifest.reseal_history` | 32 | **0** |
| `anchor.reseal_history` | 28 | **0** |
| `anchor.base_repin_history` (base) | 16 | **0** |
| `anchor.base_repin_history` (core tree) | 16 | **0** |

Every tail equals its live value. The only orphan predecessor is entry 0's genesis, which is expected.

## 4. Diff shape of each repair

- `f8e73f6b` — `git diff --numstat` = `1 1`; byte delta **0** (40-hex → 40-hex). Because the edit is
  length-preserving, the changed line was **read back** rather than inferred from the count:
  `"IMPLEMENTATION_BASE_SHA": "94a0a568…"` → `"0c01b350…"`. Opus independently diffed all **880**
  manifest leaves: key sets identical, exactly one value changed.
- `e58f4b39` — additive. Proven mechanically that `items/4/notes` is a **pure append**
  (`new.startswith(old)`), that item 4's non-`notes` fields are identical, that no other item changed,
  and that `reviewer`, `reviewed_identities`, `owner_ratification`, `unresolved_items`, `schema` and
  `signed_at` are unchanged. Opus confirmed the same from `git show` and graded the content true.
- `git diff --name-only 2f1008ab e58f4b39` touches **zero** sealed members.

## 5. T0 round 4 — both flagships

Both returned **BLOCK**. Both verified the two authorised repairs as correct, minimal and complete;
Opus recorded **"No finding"** on the restatement. Neither found an economic defect, in this round or
in the three before it.

Clone integrity across the round: post-audit head, `git status` and both contract-file digests match
`R4_CLONE_BASELINE.txt` exactly; zero stashes. `claude-opus-5` ran with tool permissions granted and
mutated nothing.

Blocking items remain open and are listed in `T0_ROUND4_CONSOLIDATED_FINDINGS.md`. **This report does
not close them.**

## 6. `gemini-3.7-flash-high` corroboration

Still outstanding at the time of writing; being run now. R2 is unmet until it lands.

## 7. What this verification could NOT have caught — recorded, not excused

`gpt-5.6-sol` finding 4 is correct and is accepted in full. The plan's verification was a current-head
gate run, a receipt diff and chain walks. **None of those can discriminate the F9 defect**, because
`seal_state` is read by zero Python files — the plan says so itself. A wrong F9 edit would have passed
every check the plan named.

The repair is nonetheless proven, by two independent routes: the Lead's direct before/after field
comparison with the changed line read back, and Sol's own parent/current predicate, which it reports
went RED then GREEN. But a predicate supplied during the audit cannot satisfy the
`AUTONOMY_AUTHORIZATION.md` requirement to record a **D026 RED/GREEN plan before dispatch**. That
requirement was missed, and the finding stays open.

Any further repair in this package must pre-register a predicate that actually fails on the unrepaired
state before the edit is made.

## 8. Not verified

- The three earlier commits' missing `APPROVED-PATCH-PLAN` trailers — a pre-modification gate that
  cannot be discharged after the fact and is the owner's to waive or rebuild.
- The foreign write-lane conflict on `CONTRACT_TABLES_MANIFEST.json` — recorded in `SESSION_LOCK.md`
  on 2026-09-09 under an owner ruling; **not resolved**, no transfer claimed.
- `seal_state.reason` still reads *"Base C30 is provisional; NONACCEPTED until forward repin F30"*
  while `seal.set_by` records F30 complete. **Deliberately not repaired**: it lives in the file this
  session has just formally recorded as foreign-owned, and writing there again would contradict that
  notice.
- The design's `v1.24` title against its `v1.25` change log — auditors disagree on severity; the
  owner's to settle.
