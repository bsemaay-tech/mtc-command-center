# WP-P0-12 re-seal #30 — repair round 5 verification report

Task id: **`WP-P012-R30-REPAIR5`**. Discharges item 6 of the `PROTECTED_PATHS_POLICY.md` modification
gate. Written **in the same round as the repair**, unlike round 4.

Author: Claude Opus 5 (Lead), session `tradingview-lab-clean-c1`, 2026-09-09.
Verified head: **`4eb75b4496790d2bf96c63e83fb08248bcad3dc0`**.

## 1. D026 predicate — RED before, GREEN after

The predicate was recorded in `WP_P012_R30_REPAIR5_PATCH_PLAN.md` §2 **before dispatch**, and tests
the contradiction rather than any replacement wording, so no phrasing can satisfy it.

| when | expected | measured |
|---|---|---|
| at `56a680ad`, before the edit | RED | **RED**, exit 1 — `f30_done=True`, `still_pending=True` |
| at `4eb75b44`, after the edit | GREEN | **GREEN**, exit 0 — `still_pending=False` |

This is the check round 4 lacked: its verification could not have discriminated its own defect.

## 2. Two guards that fired, and what they caught

**The uniqueness assertion refused two attempts and made no change either time.** The sentence
`Base C30 is provisional; NONACCEPTED until forward repin F30.` occurs **twice**, byte-identical
(678-character `reason` strings):

| location | status |
|---|---|
| `/seal_state/reason` | the **active** block — the defect, repaired |
| `/reseal_history/31/reason` | the **historical** record of the re-seal #30 candidate, `actor` *"Lead (claude-opus-5), re-seal #30 candidate"*, `at` `2026-09-08T16:45:00+03:00` — **true when written**, F30 had not yet happened |

Rewriting the second would have altered a dated historical entry to match current state — **precisely
the F6 defect repaired in `2f1008ab` earlier the same day**.

**A second wrong assumption was also caught.** The first fix attempt targeted the *last* occurrence on
the assumption that `seal_state` follows `reseal_history` in the file. Measured offsets:
`seal_state` object spans 50218–52525; the active copy is at 51029 (**the first**), the historical
copy at 83154. Targeting the last occurrence would have hit the history. The edit is therefore bounded
by the `seal_state` object's own structural anchors — `\n "seal_state": {` and
`\n "reseal_history": [`, each verified unique — not by text position.

`reseal_history[31]` is verified **byte-identical** after the change.

## 3. Full gate from a separate clone

Clone `C:\tmp\P012_LEADGATE30` at `4eb75b44`. Kernel identity confirmed **first**:
`mtc_v2.__path__ = ['C:\tmp\P012_LEADGATE30\...\mtc_v2']` — the stale kernel under
`C:\LAB\Tradingview_LAB_CLEAN` did not leak in.

| field | value |
|---|---|
| `claim_label` | `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_ACCEPTED` |
| `acceptance_blockers` | `[]` |
| self-tests | 475 passed / 0 failed |
| probes | 10/10 `DETECTED` |
| scenarios | 17 |
| seal | `b6ac5a46…` |
| design pin | `c4bb6f67…` / 2072 lines |

## 4. Receipt diff against the round-4 receipt

**Exactly one line differs**, as predicted:

```
- "observed_build_sha": "e58f4b39d5a9fe9fa890039455f16abb942663ea",
+ "observed_build_sha": "4eb75b4496790d2bf96c63e83fb08248bcad3dc0",
```

## 5. Chain walks — all four, zero breaks

| chain | entries | breaks |
|---|---|---|
| `manifest.reseal_history` | 32 | **0** |
| `anchor.reseal_history` | 28 | **0** |
| `anchor.base_repin_history` (base) | 16 | **0** |
| `anchor.base_repin_history` (core tree) | 16 | **0** |

Seal recomputed from the 19 members: `b6ac5a46…`, equal to `manifest.seal.EXPECTED_SEAL_SHA`.

## 6. Diff shape

`git diff --numstat` = `1 1`; the changed line was read back. Structural comparison of the parsed JSON
before and after: **only the `seal_state` top-level block differs.** `seal`, both `EXPECTED_SEAL_SHA`
fields, both `IMPLEMENTATION_BASE_SHA` fields, the 19 sealed members and all 32 `reseal_history`
entries are unchanged.

The replacement text deliberately asserts nothing about acceptance — it ends *"This field records seal
state only and asserts nothing about package acceptance, which remains open."* The package is not
accepted and this field must not be readable as saying otherwise.

## 7. Not verified / still open

- **No T0 audit round has run against `4eb75b44`.** Rounds 1–4 audited earlier heads. The four
  flagship BLOCK verdicts stand against those heads; this head has Lead verification only.
- **The design version contradiction** — deferred by owner ruling `HIST-2026-0021`, **not closed**.
  `gpt-5.6-sol` and `gemini-3.7-flash-high` both grade it BLOCKING.
- **The three unstamped commits** — waived by owner ruling `HIST-2026-0020`, recorded as a waiver
  granted, not as a gate satisfied. They still carry no trailer.
- **`section_16_review.status`** still `PENDING` and still stating the review "has NOT been
  performed", while the receipt is installed and validated.
- **`repository_evidence_identity`** — a true pre-repin snapshot presented as a current-looking
  top-level identity with present-tense prose and no captured-at label.
- **The fail-closed schema validator** over all declared manifest fields, which all three reviewers
  identify as the actual fix for this eight-instance defect family. Harness change, protected scope,
  owner's to authorise. **Nothing has started it.**
