# WP-P0-12 re-seal #30 — repair round 4: diagnosis, patch plan, risk report

Task id: **`WP-P012-R30-REPAIR4`**
Author: Claude Opus 5 (Lead), session `tradingview-lab-clean-c1`, 2026-09-09.
Branch: `feature/p012-reseal30-batch-20260908`, base head `2f1008ab`.

Satisfies items 1, 2 and 3 of the modification gate in
`MTC_COMMAND_CENTER/09_DOCS/PROTECTED_PATHS_POLICY.md`. Item 4 (owner approval) is recorded as an
`APPROVED` event against this task id in `MTC_COMMAND_CENTER/02_TASKS/TASK_HISTORY.json`. Item 5
(the `APPROVED-PATCH-PLAN` trailer) is carried by each repair commit. Item 6 (verification report)
is produced after the gate re-run.

## 0. Why this file exists at all

T0 round 3 returned **BLOCK** from both flagship auditors. One blocking finding was that the three
existing re-seal #30 commits change files under
`mtc_v2/tests/corrected_vnext/contracts/` without the mandatory `APPROVED-PATCH-PLAN` trailer.

The Lead's earlier disposition — that the enforcement hook does not match these paths, so no
violation occurred — was **wrong and is withdrawn**. `protected_paths_hook.py` matches five literal
substrings and imports only policy lines beginning `01_MASTER`; it cannot express the policy's prose
category "Canonical feature contracts". Both auditors rejected the disposition in near-identical
terms: an enforcer's blind spot does not narrow the standard it enforces.

**Owner ruling, 2026-09-09:** the owner delegated the interpretation to the Lead. **Ruling: the
contract JSONs under `mtc_v2/tests/corrected_vnext/contracts/` ARE canonical feature contracts and
are protected.** The directory is named `contracts`, and the two files hold the sealed contract
tables and the Section-16 contract receipt.

**The three existing commits are deliberately NOT retro-stamped.** Back-dating an approval that did
not exist would be the same class of defect as the one repair 2 fixed. They are recorded here as a
known governance gap, disclosed rather than papered over.

## 1. Diagnosis

### Defect A — `seal_state.IMPLEMENTATION_BASE_SHA` records re-seal #29's commit (auditor id: F9)

Measured in `CONTRACT_TABLES_MANIFEST.json` at `2f1008ab`:

```
manifest.seal.IMPLEMENTATION_BASE_SHA         = 0c01b350dc72c953fdac07214ecc15208e0a2536   (#30)
manifest.seal_state.IMPLEMENTATION_BASE_SHA   = 94a0a568f5257f04940de28fc984ac893af3753a   (#29)
implementation_anchor.IMPLEMENTATION_BASE_SHA = 0c01b350dc72c953fdac07214ecc15208e0a2536   (#30)
```

`seal_state.EXPECTED_SEAL_SHA` already holds `b6ac5a46…`, the **#30** seal, and `seal_state.reason`
explicitly describes the re-seal #30 candidate. So the block declares itself to be #30's state while
carrying #29's base commit. `d06aa741` updated `seal` and left `seal_state` behind; across every
prior re-seal the two fields were equal.

The gate reads `seal.IMPLEMENTATION_BASE_SHA` (`verify_bceg.py:2793`) and compares it to the anchor.
**`seal_state` is read by zero `.py` files in the tree.** This is the sixth declared-but-unchecked
field found in this audit cycle and an instance of the recurring "value changed, field left behind"
family.

Found by `claude-opus-5` in T0 round 3; independently reproduced by the Lead. `gpt-5.6-sol` did not
find it.

### Defect B — Item 4 of the Section-16 receipt states a superseded field inventory in the present tense

`semantic_coverage_review.json`, Item 4 `notes`, lists among currently retained residual production
risks: `/events/0/{… mark_price, mark_price_source …}`.

Measured `event_schema` of `core/economic_records/funding/HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1.json`:

| commit | schema |
|---|---|
| `ca1a4457` | `… mark_price, mark_price_source …` |
| **`d06aa741`** — the commit this receipt certifies | `… oracle_price, oracle_price_source …` |
| `2f1008ab` | `… oracle_price, oracle_price_source …` |

So the sentence was already false **about the state the receipt certifies**. Token counts in the
receipt: `mark_price` ×4, `mark_price_source` ×1, `oracle_price` ×3.

`C:\tmp\P012_CAPTURE_20260908\ORACLE_SEMANTICS_CORRECTION_SCOPE.md` item 4 states verbatim that
because the signed receipt references the old name in its Item-4 residual text, *"the successor
receipt must restate it."* That restatement was never made: the R30 appendix records that a rename
occurred but supplies no corrected inventory, while declaring the disposition carried forward
`UNCHANGED`.

Both auditors graded this BLOCKING. The Lead's earlier disposition ("do not edit it") is
**withdrawn**: it rested on an analogy to repair 2 that does not hold, because repair 2 corrected a
record of a past event whereas this sentence was wrong about its own certified state.

## 2. Patch plan

Two commits, each a minimal, additive-or-single-value change, each carrying
`APPROVED-PATCH-PLAN: WP-P012-R30-REPAIR4`.

### Commit A — `CONTRACT_TABLES_MANIFEST.json`

Single value substitution inside `seal_state`:

```
- "IMPLEMENTATION_BASE_SHA": "94a0a568f5257f04940de28fc984ac893af3753a"
+ "IMPLEMENTATION_BASE_SHA": "0c01b350dc72c953fdac07214ecc15208e0a2536"
```

The old value occurs **exactly once** in the file, so the substitution cannot hit another field.
Both values are 40 hex characters, so **the file length does not change** — length is therefore not
evidence here, and the check is `git diff --numstat` reading exactly `1 1` **plus** confirmation
that the changed line is the `seal_state` one.

### Commit B — `semantic_coverage_review.json`

**Additive only.** A Lead-attributed sentence is appended to the end of Item 4's `notes` string.
No existing character of any reviewer-attributed text is altered, reordered or deleted. The
restatement is explicitly attributed to the Lead and to no reviewer, so no Gemini-attributed
disposition is silently rewritten — the part of the withdrawn disposition that both auditors agreed
with, and that survives.

The insertion point is the unique substring `and synthetic isolation remains absolute.` at the tail
of Item 4's `notes`. ASCII only, no quotes and no newlines, so the JSON encoding is unaffected.

### Prohibited in this round

No edit to any test, assertion, harness file, golden, record, or sealed member. No change to any
seal, design pin, anchor, or receipt identity. No `canonical_json_bytes` round-trip — it minifies
and would reformat the file.

## 3. Risk report

| risk | assessment |
|---|---|
| Seal moves | **None.** `CONTRACT_TABLES_MANIFEST.json` is not one of the 19 sealed members; the seal is computed over `DERIVATIONS.md`, `scenario_catalog.json` and 17 goldens only. |
| Receipt identities go stale | **None.** The receipt's `reviewed_identities` pins nine *other* artifacts; the receipt's own digest is pinned nowhere, and `semantic_coverage_review.json` is not a sealed member. |
| Design pin moves | **None.** Neither file is the design. |
| Section-16 review invalidated | **No.** No reviewer-attributed text is modified; the change is an appended, separately attributed sentence. The gate's `validate_semantic_coverage_review` and the ratification chain derived from `reseal_history` are untouched — no `actor` string changes. |
| JSON reformatting | Mitigated by surgical text substitution and a `git diff --numstat` check; explicitly **not** using the project's `canonical_json_bytes`. |
| Wrong line changed by a length-preserving edit | Mitigated: the target string is verified unique before the edit, and the resulting diff is read line by line rather than trusted on byte count. |
| Repair cap | Round 3 exhausted the cap of 3. **The owner explicitly authorised this fourth repair round on 2026-09-09**, recorded as an `APPROVED` event. The cap was raised by the owner, not reset by the Lead. |
| Gate regression | Mitigated: the full gate is re-run after the change and the receipt compared against the round-3 receipt, where the only permitted difference is `observed_build_sha`. |

## 4. Verification plan (item 6)

1. Full gate at the new head from a fresh clone, kernel identity confirmed first.
2. Receipt diffed against the round-3 receipt; only `observed_build_sha` may differ.
3. `reseal_history` and anchor chain walks re-run: zero breaks expected.
4. `git diff --numstat` = `1 1` for commit A; commit B additive with 0 deletions on the notes line.
5. T0 round 4 with both flagship auditors against the new head.
6. The mandatory `gemini-3.7-flash-high` corroboration, which has still never run for re-seal #30.

Results are recorded in `WP_P012_R30_REPAIR4_VERIFICATION_REPORT.md`.

## 5. What this round does NOT fix

- The **design version identity contradiction** (line 1 `v1.24` vs line 2027 `v1.25 change log`).
  `gpt-5.6-sol` grades it BLOCKING; `claude-opus-5` grades it a nit. Repairing it changes
  `design_file_sha256`, which the receipt pins, forcing a full cascade **and a fresh Section-16
  review**. Left open for the owner.
- The **three existing commits' missing trailer**. Not retro-stampable, as set out in §0.
- The **hook's inability to express its own policy**. It should be widened so this cannot recur
  silently, but that is a governance change belonging on its own branch after re-seal #30 lands.
- The **476-vs-475 skip reporting**, a harness change in protected scope.
