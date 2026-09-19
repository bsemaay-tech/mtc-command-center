# WP-P0-12 acceptance-scope amendment — RECORDED 2026-09-13 (closure preconditions OPEN)

**Status: RECORDED AMENDMENT / NONACCEPTING.** The owner approved the narrowing in chat on 2026-09-13 (verbatim in §0). This document records the exact amendment and the requirement register. It is **not** acceptance, ratification, a review verdict, a receipt or a signature: every Class A closure precondition in §3 is still OPEN at recording time, and the completion label may not be used until each is satisfied with real evidence. Drafted by an independent lane (`claude-opus-5` xhigh, lane P12-AMEND); audited and recorded by the Lead (Claude Fable 5.1) — see §8 Lead audit. Every identifier, count, hash, disposition and line number is quoted from a cited source; gaps are stated in §6 rather than filled in.

## 0. Owner instruction this draft serves (verbatim, chat, 2026-09-13)

> I approve narrowing WP-P0-12's current acceptance scope to its reviewed research/engineering deliverable.
> Prepare and record the exact acceptance amendment. Map every original requirement to either: 1. required for current closure, or 2. an explicitly open production-admission follow-up, with its evidence requirement, owner and affected downstream gates.
> Complete the remaining mandatory formal review, actual ratification and required checks before declaring the amended scope complete.
> Preserve all unresolved production risks and refusals. Assumptions remain labelled assumptions. This does not authorize mainnet trading, deployment, spending, invented attestations or waived reviews.
> Report completion as "P0-12 research/engineering scope complete; production admission pending." Reconcile downstream dependencies individually; do not automatically unblock production-dependent work.

## 0.1 Path conventions used in citations

| Token | Expands to |
|---|---|
| `P/` | `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/` (frozen read-only reviewer packet) |
| `LEAD/` | `C:/tmp/P012_LEAD_20260912/` |
| `S16REV/` | `C:/tmp/P012_S16_REVIEWS_20260913/` |
| `TAKEOVER/` | `C:/tmp/CLAUDE_TAKEOVER_20260913/` |
| `CT13/` | `C:/CT13/` (read-only control checkout, branch `feature/claude-takeover-20260913`) |
| `CODEX/` | `C:/Users/BarışSemaay/Documents/Codex/2026-09-11/11-2/outputs/` — the `[CT]`/`[CP]` sources named by the Path D citation key at `P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:207` |

## 0.2 The two classes used in the register (§2)

- **Class A — required for current research/engineering closure.** The narrowed acceptance object
  cannot be declared complete until every Class A row is satisfied with real evidence.
- **Class B — explicitly open production-admission follow-up.** Class B rows are *not* closed,
  waived, weakened or reinterpreted by this amendment. Each carries its evidence requirement, its
  owner, and the downstream gates it affects.

A row being Class B never means "resolved"; it means "outside the narrowed acceptance object and
still open". No Class B row may be declared closed by the label in §1.

---

## 1. Amendment text — proposed decision row (DRAFT, unexecuted)

Proposed for the binding-decision table at `P/CAND/DECISIONS.md:16-78` (same four-column shape).
**Recorded in root `DECISIONS.md` of the control checkout on 2026-09-13 by the Lead, quoting the owner's chat words; the owner's approval is the chat instruction in §0, not a separate signature on this file.**

| Decision | Date | Binding summary | Source |
|---|---|---|---|
| OD-20260913-P012-SCOPE-1 | 2026-09-13 | Owner: "I approve narrowing WP-P0-12's current acceptance scope to its reviewed research/engineering deliverable." Narrowed acceptance object = that reviewed deliverable at G5 `6d6a450232c81c4c13d63c9a4e06ce3b1bf4f889` / core `4698e71659d678f50e549e328e78d25816fa16fe` under signed Path D (`OD-20260912-P012-PATHD-1`). Exact label: "P0-12 research/engineering scope complete; production admission pending." Closure preconditions, all OPEN at recording: formal Section-16 six-item review by `gemini-3.8-flash-high` with actual native reads (in progress in bounded parts under `C:/tmp/P012_S16_REVIEWS_20260913`); actual owner ratification of seals `#36`-`#39` and the retained chain; chain/schema/receipt application; gate/self-test/protected checks (gate now exits 2: `SEMANTIC_COVERAGE_REVIEW_INVALID`, `CONTRACT_SELFTEST_RED`). Authorizes no mainnet/TESTNET trading, deployment, host, credential, order, spend, invented attestation or waived review; admits no venue fact. `OPEN-01`..`OPEN-10`, 27 signed risks, five residual obligations, Item 4 `NONE_KEEP_REFUSED` and all record refusals unchanged. Downstream dependencies reconcile individually; production-dependent work stays blocked. | Owner chat 2026-09-13 (verbatim §0 of this file); identities `LEAD/FINAL_STATE_20260913.json:3-4`; review state `S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:3`; gate `LEAD/LEAD_R5/FINAL_GATE.json:692-700`. Recorded by the Lead 2026-09-13. |

Measured lengths of the row exactly as written above, counted by this lane with a read-only
character count over the saved file: `Binding summary` cell **1,171 characters**; whole row
**1,437 characters** (both within the 1,500-character ceiling the lane brief sets). Re-measure
after any edit.

### 1.1 What the amendment does **not** do (explicit non-authorizations)

Quoted or faithfully carried from the sources that already state them:

1. No live trading, order placement, TESTNET/mainnet contact, ARM, wallet or transfer authority —
   `P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:192-193`, `P/CAND/AGENTS.md:35-37`,
   `CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AUTONOMY_AUTHORIZATION.md:22-23`.
2. No deploy, host, credential, PAYG or new-spend authority; "Paid ceiling stays $0" —
   `P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:194`.
3. No review waiver: T0 (fresh exact Opus 5 + Sol xhigh + mandatory Gemini 3.7 + Lead
   reproduction), R29 semantic redo, Section-16 review, owner ratification, current-head protected
   CI and protected merge all remain required —
   `P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:195-197`.
4. `OPEN01/OPEN03/OPEN05/OPEN07` stay OPEN; the 27 signed risks stay, plus the new Path D risks —
   `P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:198`.
5. Item 4 `NONE_KEEP_REFUSED` changes only by the explicit supersession row already named —
   `P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:199`; `P/CAND/DECISIONS.md:76`.
6. No production admission of any venue fact; local consistency cannot authenticate origin —
   `P/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:20`,
   `P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:31`.
7. No push, PR or merge authority arises here —
   `CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AUTONOMY_AUTHORIZATION.md:15`,
   `P/CAND/AGENTS.md:47-49`.
8. Claude is not an eligible Section-16 signer, and no model output substitutes for owner
   ratification — `TAKEOVER/P012_HANDOFF.md:53`,
   `P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:164`.

### 1.2 Precedent for a bounded, explicitly labelled narrowing

The design already carries one owner-approved bounded-milestone amendment with a mandatory
rendering rule and a retirement clause: `P012_SYNTHETIC_ONLY_NON_PRODUCTION_MILESTONE_V1 — NOT
WP-P0-12 ACCEPTANCE` (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:1897-1925`; retirement at
`:2019-2025`). That milestone is **not** retired, restated or altered by this draft. Its shape —
canonical token, mandatory first-use rendering, explicit "authorizes no …" list, retirement only
on full production closure — is the shape §1 follows.

### 1.3 Relationship to the already-recorded 2026-09-12 scope decision

`OD-20260912-P012-RESEARCH-PAPER-SCOPE` (`P/CAND/DECISIONS.md:77`) records a "Verified
Mentor-relayed owner decision recorded 15:25Z: finish engineering and PREPARE explicit
research/paper acceptance scope only, with labelled assumptions, adverse-cost tests and
unsupported-production refusal. This creates no new numeric assumption, actual acceptance,
ratification, paper execution or operational/push/PR/merge authority." The 2026-09-13 instruction
in §0 is the owner's approval of the narrowing that row only authorized *preparing*. This draft is
therefore the prepared amendment text, still unexecuted.

---

## 2. Requirement register

One row per original requirement. `Class A` = required for current research/engineering closure.
`Class B` = explicitly open production-admission follow-up. For Class A rows the three B-columns
read `—`. Quotes are exact where quoted; short forms are marked as faithful summaries.

Owner vocabulary used in the B-owner column, as required by the lane brief: **Baris** (owner
decision/ratification), **venue+Bridge capture** (authenticated own-account evidence through the
separately authorized capture path), **Lead**, **formal reviewer** (the eligible Section-16
reviewer), **experienced human** (the money-exposed specialist / qualified record reviewer of
`CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/REVIEW_POLICY.md:73-76`).

Downstream-gate vocabulary is taken from the plan and handoffs, not invented: **P020** depends on
WP-P0-12 (`CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:505`)
and its `check_p020_acceptance.py` `required_tier_implemented` row is BLOCKED for Fees/Funding/
Slippage/Protective-order semantics (`CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_12_SCOPE_ASSESSMENT_2026-09-07.md:41-56`);
**P021** depends on WP-P0-04 + WP-P0-12 and its acceptance gate is brief A-7c RED/GREEN fixtures
(`…PLAN_2026-08-22.md:520-522`); **P013** reaches P012 transitively through P020
(`…PLAN_2026-08-22.md:411-414`; `TAKEOVER/START_HERE.md:42`); **P031 M1** needs accepted
P004/P013 provenance (`TAKEOVER/START_HERE.md:50`); **WP-V2A-01/WP-V2A-03** are gated on P012
acceptance (`…PLAN_2026-08-22.md:687,698-699`); **G3-K** is the named sub-gate holding the kernel
packages (`…PLAN_2026-08-22.md:1069`).

| ID | Source (file:line) | Requirement (quote or faithful short form) | Class | Current status (evidence) | B: evidence requirement | B: owner | B: affected downstream gates |
|---|---|---|---|---|---|---|---|
| **PLAN-GATE** | `…PLAN_2026-08-22.md:406` | "**no undocumented behavioural difference exists between P0-11 and P0-12.** Phase 0 is not complete without this." | A | PENDING — not machine-proved by design; the design states its claim is bounded and the residual gap is carried by the Section-16 review plus honest limits L1/L8 (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:28-33,815,822`). Formal Section-16 review is incomplete (`S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:3`) | — | — | — |
| **PLAN-OUT-1** | `…PLAN_2026-08-22.md:403`; design §7 `P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:209` | Output: contract multiplier (`DEF-P012-01`) | A | DONE (engineering, bounded) — engineering "Complete within signed Path D; no required repair remains" at G5 (`LEAD/FINAL_HANDOFF_20260913.md:19`); bounded synthetic corpus only (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:815`) | — | — | — |
| **PLAN-OUT-2** | `…PLAN_2026-08-22.md:403`; design §8 `:248` | Output: real minimum-notional admission (`DEF-P012-02`) | A | DONE (engineering, bounded) — same evidence as PLAN-OUT-1 | — | — | — |
| **PLAN-OUT-3** | `…PLAN_2026-08-22.md:403`; design §9 `:309` | Output: frozen instrument metadata (`DEF-P012-03`) | A | DONE (engineering, bounded); the *production* instrument record remains refused — see I-1..I-5 and OPEN-01 | — | — | — |
| **PLAN-OUT-4** | `…PLAN_2026-08-22.md:403`; design §10 `:333` | Output: gap-aware protective stops, continuous activation (`DEF-P012-04`) | A | DONE (engineering, bounded) | — | — | — |
| **PLAN-OUT-5** | `…PLAN_2026-08-22.md:403`; design §11 `:361` | Output: in-path slippage applied exactly once (`DEF-P012-05`) | A | DONE (engineering, bounded); the slippage value is an owner-declared explicit zero, not a measurement (`P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:85-90`) | — | — | — |
| **PLAN-OUT-6** | `…PLAN_2026-08-22.md:403`; design §12 `:389` | Output: named same-bar collision policy (`DEF-P012-06`) | A | DONE (engineering, bounded); policy named `STOP_FIRST` by owner addendum 15 row 32 (`P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:225`) | — | — | — |
| **PLAN-OUT-7** | `…PLAN_2026-08-22.md:403`; design §13 `:418` | Output: provenanced real fee schedule (`DEF-P012-07`) | A | DONE (engineering, bounded); *production* cost admission still refused — see C-6..C-12, OPEN-03 | — | — | — |
| **PLAN-OUT-8** | `…PLAN_2026-08-22.md:403`; design §14 `:459` | Output: per-interval funding and `funding_events` (`DEF-P012-08`) | A | DONE (engineering, bounded); production funding record refuses (`P/CAND/mtc_v2/core/economic_records/funding/HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1.json:2`) | — | — | — |
| **S16-1** | `P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:802` | "Re-derive every formula in sections 7-14 … inspect the exact `CONTRACT_TABLES` authoring path/import graph and `IMPLEMENTATION_ANCHOR` ancestry, and confirm the named author is independent from the kernel implementer." | A | PENDING — the first partial call (09:30–09:38Z) is NOT accepted (`NONACCEPTING_REQUIRED_READ_GAPS`, `S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:5,7,11`). Item 1 is being re-reviewed in bounded parts: Part A (DEF-01..06 + section 24 ledger) completed 10:45Z with complete native reads (58 views, 0 mismatches; `S16REV/A2_ITEM1A_TABLES_CODE/LEAD_ADJUDICATION.md`), 39/39 values EQUAL, part disposition ACCEPTED_WITH_RESIDUAL_RISK; Parts B (fees/funding) and C (author/anchor/reseals) and a reconciliation call remain | — | — | — |
| **S16-2** | `:803` | Review every kernel diff hunk of the exact canonical `git diff` bytes; embed one V2 `hunk_coverage` object; "V1, missing/duplicate/malformed/drifted data, duplicate ownership, and UNDOCUMENTED hunks refuse; external evidence paths never satisfy Item 2." | A | PENDING — never launched. Prepared, never-run prompts B1 (hunks 0–135), B2 (hunk 136), B3 (hunks 137–217) (`TAKEOVER/P012_HANDOFF.md:43-46`); canonical patch 218 hunks / 139 paths / 399,045 bytes (`TAKEOVER/P012_HANDOFF.md:41`) | — | — | — |
| **S16-3** | `:804` | "Review scenario catalog boundaries and correction interactions, explicitly looking outside the finite cases." | A | PENDING — never launched; prompt `C_CATALOG_CONSUMERS` prepared (`TAKEOVER/P012_HANDOFF.md:47`) | — | — | — |
| **S16-4A** | `:805`; milestone bounding at `:1976-1987` | Item 4, bounded arm: review the lineage of every number actually consumed by the sealed synthetic bindings and confirm the applicability evidence for `OPEN-01`..`OPEN-10` | A | PENDING — the 2026-09-13 call claimed Item 4 `ACCEPTED_WITH_RESIDUAL_RISK`, but "Item4 and the rest of the substantive report remain to be reconciled; do not promote its stated opinion to completed formal acceptance" (`S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:11`) | — | — | — |
| **S16-4B** | `:805`; `:1992` ("Outside this milestone, the original production-wide wording of section 16 item 4 remains binding") | Item 4, production arm: "Review the grid/record lineage for every production number and confirm section 19 resolution evidence." | B | PENDING — no production number has admitted lineage; all production records refuse (see §4) | A then-current Section-16 receipt disposing Item 4 over **production** lineage, after every production Item-4 row and Section-19 OPEN row is resolved from authoritative evidence (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:2019-2022`) | formal reviewer + Baris (ratification) | P020 `required_tier_implemented`; P021 A-7c fixtures; WP-V2A-03 runtime wiring; G3-K |
| **S16-5** | `:806` | "Inspect for economic state carried across modules/containers or external consumers that the static shape census could miss." | A | PENDING — never launched (`TAKEOVER/P012_HANDOFF.md:47`) | — | — | — |
| **S16-6** | `:807` | "Inspect event/schema additions for missing consumers, overwrite, duplicate identity, or silently dropped members." | A | PENDING — never launched (`TAKEOVER/P012_HANDOFF.md:47`) | — | — | — |
| **S16-RECEIPT** | `:809` | "The receipt records `reviewer`, exact commit/tree identities, per-item evidence paths, disposition, and unresolved items. A missing item, `NOT_VERIFIED`, or unresolved item refuses." | A | PENDING — the repository's `semantic_coverage_review.json` is the historical old receipt whose reviewed head/core and chain predate the fixed candidate and "is not current acceptance evidence" (`P/EVIDENCE_STATUS.md:5`) | — | — | — |
| **S16-BAR** | `:800`; `S16REV/FORMAL_REVIEW_CONTRACT.md:7`; `P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:39` | Reviewer family bar: "independent from the kernel implementer and `CONTRACT_TABLES` author"; required reviewer `gemini-3.8-flash-high`, neither Codex nor Claude, against immutable semantic base `5e8e579410ee55008bfd2d2d85054fd1d782f32c` | A | BINDING, unsatisfied — Gemini 3.7 corroboration and Sol/Opus engineering passes "cannot replace this review" (`S16REV/FORMAL_REVIEW_CONTRACT.md:7`); "Claude takeover does not make Claude an eligible Section16 signer" (`TAKEOVER/P012_HANDOFF.md:53`) | — | — | — |
| **R29-REDO** | `P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:164,196`; `P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:39`; `CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:23-24` | R29 semantic redo / final Section-16 record review; "R29 consists of six requests and nine actual reviewed identity fields; those identity fields must not be confused with file hashes" | A | PENDING — preparation COMPLETE (`CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:23`), review BLOCKED on final candidate/evidence (`:24`) | — | — | — |
| **T0-ROSTER** | `CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/REVIEW_POLICY.md:20`; `P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:164` | T0 review = fresh exact `claude-opus-5` **and** `gpt-5.6-sol`, both `xhigh`, plus fresh mandatory `gemini-3.7-flash-high` corroboration on the same packet, plus independent Lead reproduction | A | DONE for the reviewed engineering scope — Sol `PASS`, Opus `PASS-WITH-NITS` (exit 0, 80 turns, 04:03:53–04:29:11Z), three Gemini 3.7 slices PASS, Lead reproduced (`LEAD/FINAL_HANDOFF_20260913.md:20-22,27`; `LEAD/FINAL_STATE_20260913.json:8-10`). Nits are optional (`LEAD/FINAL_HANDOFF_20260913.md:29`) | — | — | — |
| **SPECIALIST** | `CT13/…/REVIEW_POLICY.md:73-76`; `P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:164` | Bounded specialist review for the first kernel / first money-exposed release: "An experienced engineer reviews before the first money-exposed release" | B | PENDING — "the experienced-human money gate is separate" (`P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:39`) | A named question and stop condition, with the specialist's recorded review before the first money-exposed release | experienced human | P020 cost admission; WP-V2A-03; any live/ARM step (separately unauthorized) |
| **RATIFY-SEALS** | `P/RATIFICATION_DRAFTS_UNEXECUTED/REAL_OBSERVATION_INTAKE.md:12,45`; `LEAD/FINAL_HANDOFF_20260913.md:33`; `S16REV/FORMAL_REVIEW_CONTRACT.md:19` | Owner ratification of builder seals `#36`, `#37`, `#38`, `#39` and the retained earlier chain | A | PENDING — "Seals `#36`, `#37`, `#38`, and builder `#39` are already built but remain unratified"; builder `#39` seal `00e66d9eb3517eb6bf0cb4672a22d19b58715b1b00afb4d91ffe0a4000979cb9` | — | — | — |
| **CHAIN-STATE** | `P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:12`; `LEAD/FINAL_HANDOFF_20260913.md:33` | Chain reconciliation: accepted JSON chain 33 entries through `#35`; Markdown chain 28 entries through `#30`; proposed manifest chain 37 entries ending `#39` | A | PENDING — application of the prepared chain/schema/receipt metadata is authorized only after actual ratification (`TAKEOVER/P012_HANDOFF.md:49`) | — | — | — |
| **GATE-SCR** | `LEAD/LEAD_R5/FINAL_GATE.json:692-696`; `P/RATIFICATION_DRAFTS_UNEXECUTED/ADVERSE_COST_EVIDENCE.md:22` | Full gate must not refuse: `SEMANTIC_COVERAGE_REVIEW_INVALID` — "reviewed_identities.core_tree_oid: reviewed-head core tree does not match current core tree" | A | RED / refusing — gate exit 2; `claim_label` is `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED` (`LEAD/LEAD_R5/FINAL_GATE.json:114`). "`acceptance_reachable:true` is a result field, not acceptance" (`…ADVERSE_COST_EVIDENCE.md:22`) | — | — | — |
| **GATE-CSR** | `LEAD/LEAD_R5/FINAL_GATE.json:697-700,117-125` | Full gate must not refuse: `CONTRACT_SELFTEST_RED` — "1 contract self-test failed", failing id `mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_v2_schema_accepts_complete_receipt_and_rejects_nested_mutants` (655 passed, 1 failed) | A | RED / refusing — MTC suite 705 passed / 1 failed / 1 skipped; the sole failure is the unratified-chain schema capacity self-test (`P/RATIFICATION_DRAFTS_UNEXECUTED/ADVERSE_COST_EVIDENCE.md:21`) | — | — | — |
| **CI-PROTECTED** | `P/CAND/AGENTS.md:47-49`; `P/CAND/DECISIONS.md:37` (OD-20260826-4) | "Master receives changes only by PR with `Bridge suite (Python 3.12)` green on the up-to-date head under ruleset 21444962, no bypass." | A (as a required check) | NOT RUN — "CI/integration: Not run or authorized by this continuation; no push, PR or merge" (`LEAD/FINAL_HANDOFF_20260913.md:25`; `LEAD/FINAL_STATE_20260913.json:15`) | — | — | — |
| **MERGE-AUTH** | `CT13/…/AUTONOMY_AUTHORIZATION.md:15`; `P/CAND/AGENTS.md:35-37` | Push/PR/merge: "**EXISTING PERMISSION:** None added by this decision." Merge only after package acceptance, required audits, up-to-date head and protected CI green | B | NOT AUTHORIZED — no push, PR or merge performed or permitted (`LEAD/FINAL_HANDOFF_20260913.md:25`; `TAKEOVER/P012_HANDOFF.md:11`) | Package acceptance + required audits + up-to-date head + `Bridge suite (Python 3.12)` green, then an explicit owner release act | Baris (release) + Lead (execution) | Integration of P012 into `master`; every downstream package consuming an integrated kernel (P020, P021, P013, WP-V2A-01/03) |
| **ITEM4** | `P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:2004`; `P/CAND/DECISIONS.md:76`; `CT13/…/AUTONOMY_AUTHORIZATION.md:14` | Item 4 `ITEM4_EXISTING_OFFLINE_SOURCES` = `NONE_KEEP_REFUSED`; "stays refused and cannot publish" | B | REFUSED-BY-DESIGN, preserved — qualified only by the explicit Path D row, which admits venue-derived values solely through the three named source classes after the required T0 reviews (`P/CAND/DECISIONS.md:76`) | Any change requires an explicit written supersession/qualification row; never by silent reinterpretation (`P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:74,199`) | Baris | P020 cost admission; every production-economics consumer |
| **OPEN-01** | design `:900`; `P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:12-32` | "Which venue, product, symbol, effective window, and exact venue-document bytes supply the first production `InstrumentRecord`?" | B | PENDING / OPEN — disposition `APPLICABLE`; owner chose Hyperliquid perpetual BTC (addendum 15 row 36, addendum 16 row 42: `P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:234-237,265-269`); production admission still refused | "Owner decision plus raw source bytes/digest and extracted record/digest" (design `:900`); plus the two recorded residuals (OBLG-1, OBLG-2) | Baris + venue+Bridge capture | P020 `required_tier_implemented`; P021 A-7c fixtures; WP-V2A-03 |
| **OPEN-02** | design `:901`; `open_item_applicability.json:34-49` | "Which named same-bar policy is mandatory/default for acceptance-bearing `2.0.0` runs: `STOP_FIRST`, `TARGET_FIRST`, or `SUBBAR_UNKNOWN`?" | B | PENDING / OPEN for production — decided `STOP_FIRST` (addendum 15 row 32, `…EVENING.md:225`); "Reuse existing bounded fixture evidence; final production applicability/review still required" (`CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:12`) | Final production applicability confirmation inside the production-lineage Section-16 receipt | formal reviewer + Baris | P020; P021 fixtures |
| **OPEN-03** | design `:902`; `open_item_applicability.json:51-70` | "For every fill-event class, is liquidity role maker or taker, and which exact venue fee schedule/rounding/minimum applies?" | B | PENDING / OPEN — fee table v1.1 + class mapping approved (addendum 16 row 43, `…EVENING.md:279-283`); the cost record still refuses or admits only reported per-fill cash (see C-7..C-11) | "Owner-approved event-role table plus venue source bytes/digests and effective interval" (design `:902`) | venue+Bridge capture + Baris | P020 cost admission; P021 fixtures; WP-V2A-03 |
| **OPEN-04** | design `:903`; `open_item_applicability.json:72-86` | "Which slippage model id and parameter values are authorized, and what measured/venue source establishes each numeric parameter?" | B | PENDING / OPEN — `BPS_OF_REFERENCE_V1`, `slippage_bps = 0`, owner-declared explicit zero, `measurement_claimed:false`, `venue_source_claimed:false` (`…costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:81-90`; addendum 15 row 38 `…EVENING.md:241-242`) | If a non-zero model is ever wanted: a measurement record or venue source provenance plus a separate owner decision — "a measured model remains possible later by separate decision" | Baris (+ venue+Bridge capture if measured) | P020 `required_tier_implemented` (Slippage row) |
| **OPEN-05** | design `:904`; `open_item_applicability.json:88-104` | "What funding position-snapshot rule, same-timestamp ordering, mark-price source, and positive-rate-payer convention apply …?" | B | PENDING / OPEN — rules approved (addendum 16 row 42) and same-timestamp `INCLUDE` (addendum 17 row 46, `…EVENING.md:305-311`); production funding events still `REFUSED_MISSING_PRODUCTION_FUNDING_EVENTS` | "Owner decision and venue documentation/history bytes with digests" (design `:904`) plus the forward-only interval evidence (PD-FUND-START, F-13..F-22) | venue+Bridge capture + Baris | P020 `required_tier_implemented` (Funding row); WP-V2A-03 |
| **OPEN-06** | design `:905`; `open_item_applicability.json:106-121` | "For `2.0.0`, which existing entry/target execution-profile behaviors survive after protective stops become continuously active?" | B | PENDING / OPEN for production — dispositions closed by addendum 16 row 45 (`…EVENING.md:289-296`); every row's migration fixture is a build obligation | Final production applicability/review of the retained/retired dispositions and their migration fixtures | formal reviewer + Baris | P020; P021 fixtures |
| **OPEN-07** | design `:906`; `open_item_applicability.json:123-139` | "What exact external `funding_events` field mapping must later integration use? … this lane did not read Bridge/schema paths." | B | PENDING / OPEN — mapping v1.1 approved as closure evidence; 16/18 unmapped fields + deployed-v4 non-materialization recorded as integration obligations (addendum 16 row 42, `…EVENING.md:272-274`) | "Separately authorized schema read, field-by-field mapping, and owner approval; no Bridge write implied" (design `:906`) | Lead (authorized schema read) + Baris | Bridge integration; P020 funding consumption; WP-V2A-03 |
| **OPEN-08** | design `:907`; `open_item_applicability.json:141-154` | "Are any numeric plausibility bounds required beyond type, finiteness, exact record provenance, and venue-effective interval?" | B | PENDING / OPEN for production — explicit "no additional bounds" decision (addendum 15 row 33, `…EVENING.md:226-227`) | Final production applicability/review; otherwise the explicit no-additional-bound decision stands (design `:907`) | formal reviewer + Baris | P020; record-refusal probe families |
| **OPEN-09** | design `:908`; `open_item_applicability.json:156-169` | "Is the additive result/event schema in sections 13-15 approved for the protected build, including gross/net PnL and lifecycle linkage?" | B | PENDING / OPEN for production — protected-scope approval granted (addendum 15 row 34) with build authorization via the addendum-16 Gate-2 path grant (`…EVENING.md:228-230,275-278`) | "Explicit protected-scope/schema approval and separate build authorization" carried into the production receipt (design `:908`) | Baris | P013 `TrialRecord` consumers; P020 result surfaces |
| **OPEN-10** | design `:909`; `open_item_applicability.json:171-185` | "Once funding is captured, what exact PnL basis controls daily loss, consecutive loss, and time-stop `Profit Only`/`Loss Only`…?" | B | PENDING / OPEN for production — option (a) GROSS-MINUS-FEES, D017 extended to `2.0.0` (addendum 15 row 35, `…EVENING.md:231-233`; D017 at `P/CAND/DECISIONS.md:54`) | Owner decision superseding/clarifying D017 for `2.0.0` **plus** RED/GREEN guard fixtures for every named control (design `:909`) | Baris + Lead (fixtures) | P020 guard behaviour; WP-V2A-03 risk controls |
| **OPEN-EMBED-01..05** | `open_item_applicability.json:188-232,234`; design `:1897-1925` | Five test-only embedding values, closed by owner addendum 20 verbatim "1a 2a 3a 4a 5a" (`…EVENING.md:337`) | A | DONE — all five `CLOSED`, test-only under the design's synthetic-vector rule; "production records remain governed by the OPEN-01..10 rows above" | — | — | — |
| **I-1** | `CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:30`; design corroboration `:1986` | Signed risk I-1 — instrument `/status`: "addendum-16 selection applied; admission still refused" | B | PENDING — the instrument record status still states production admission remains refused (`P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.3.json:2`; v1.4 at `:225`) | "real qualified human review + full admission evidence" | experienced human + Baris | P020 `required_tier_implemented`; WP-V2A-03 |
| **I-2** | `…03_PRODUCTION_CLOSURE_MATRIX.md:31` | Signed risk I-2 — `/price_tick`: scalar `null`; typed policy `HYPERLIQUID_PX_V1` implemented | B | RETAINED (formally) — "Scalar remains null; reuse accepted PR176 typed-policy/precision evidence; formal signed residual not retired"; R34 price policy is not reopened (`P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:136`) | Reuse of the accepted PR176 typed-policy evidence inside the production receipt; "no new scalar-tick demand" (`CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:10`) | Lead (reuse) | P020; P021 |
| **I-3** | `…03_PRODUCTION_CLOSURE_MATRIX.md:32` | Signed risk I-3 — `/minimum_quantity`: `null`; `minimum_notional: 10`, `quantity_step: 0.00001`; no quantity floor | B | PENDING / OPEN — record v1.4 supplies an **owner guard** `0.0001` marked `HL_QTY_OWNER_GUARD_NOT_VENUE_FACT_V1`; "it closes the consumer refusal, not the question" and "OPEN01 stays OPEN" (`…instruments/HYPERLIQUID-BTC-PERP-V1.4.json:73,97-98,112-115`) | A venue-stated quantity minimum; absence is not established and "the 0.00001 grid is *not* the missing floor" (`P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:110,124`) | venue+Bridge capture | P020 sizing admission; WP-V2A-03 order sizing |
| **I-4** | `…03_PRODUCTION_CLOSURE_MATRIX.md:33` | Signed risk I-4 — instrument human reviewer: `human_reviewer: null` (key present) | B | PENDING — `provenance.human_reviewer` is `null` in both record versions (`…HYPERLIQUID-BTC-PERP-V1.3.json:104`; `…V1.4.json:186`); "this record still refuses evaluation" (`…V1.4.json:225,256`) | "real **qualified** human review of completed record"; OPEN-01 additionally names Section-16 human review by the owner at build acceptance (`…03_PRODUCTION_CLOSURE_MATRIX.md:59`) | experienced human + Baris | P020; WP-V2A-03 |
| **I-5** | `…03_PRODUCTION_CLOSURE_MATRIX.md:34` | Signed risk I-5 — aggregate source fingerprint: "implemented + verified (`source_sha256 = da2bf1fe…`, five sources)"; remaining closure "none" | A | DONE (local) — recorded as complete in the matrix; nothing further required for the research/engineering object | — | — | — |
| **C-6** | `…03_PRODUCTION_CLOSURE_MATRIX.md:35`; `CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:12` | Signed risk C-6 — cost effective interval: start implemented `2026-09-06T14:00:30Z`; historical tier coverage unproven | B | PENDING — under Path D choice B3=B the admitted interval start is `null` until the first authenticated fill and "every admitted-cost computation under this record refuses" (`…costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:5-6`) | "Dated binding and defensible actual billing evidence; cannot backdate current code" (`CONTROL_TABLE.md:12`) | venue+Bridge capture | P020 cost admission |
| **C-7** | `…03_PRODUCTION_CLOSURE_MATRIX.md:36` | Signed risk C-7 — fee rounding rule: `KEEP_REFUSED`; absence proof attached | B | REFUSED-BY-DESIGN, retained — `fee_rounding_rule` stays in `refused_missing_fields`, "NOT filled in, NOT defaulted and NOT evidenced"; not required for the admitted cost, "which is a different statement from being resolved" (`…BASE-TIER0-V2.json:68-74`) | "authoritative precision/direction/per-fill scope" | venue+Bridge capture | P020 cost admission; every schedule-computed cost path |
| **C-8** | `…03_PRODUCTION_CLOSURE_MATRIX.md:37` | Signed risk C-8 — fixed component: `KEEP_REFUSED`; absence proof | B | REFUSED-BY-DESIGN, retained — same field set as C-7; writing `EXACT_IDENTITY_V1` alone would silently activate the `fixed_component`/`minimum_fee` default zeros and is banned (`P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:92`) | "authoritative applicability/absence + exceptions" | venue+Bridge capture | P020 cost admission |
| **C-9** | `…03_PRODUCTION_CLOSURE_MATRIX.md:38` | Signed risk C-9 — minimum fee: `KEEP_REFUSED`; absence proof | B | REFUSED-BY-DESIGN, retained — see C-7 evidence | "authoritative minimum/application granularity" | venue+Bridge capture | P020 cost admission |
| **C-10** | `…03_PRODUCTION_CLOSURE_MATRIX.md:39`; `CONTROL_TABLE.md:11-12` | Signed risk C-10 — account tier evidence: "collected, not incorporated" | B | PENDING — `tier_account_selection_evidence` remains in `refused_missing_fields`; `tier_selection_basis` is `OWNER_APPROVED_BASE_TIER_0_WITH_ACCOUNT_EVIDENCE_RESIDUAL` (`…BASE-TIER0-V2.json:68-74,93`) | "historical coverage + actual fee applicability" | venue+Bridge capture + Baris | P020 cost admission |
| **C-11** | `…03_PRODUCTION_CLOSURE_MATRIX.md:40` | Signed risk C-11 — liquidation class: `CANNOT_MAP` refusal (`MARGIN_CALL_LIQUIDATION`) | B | REFUSED-BY-DESIGN, retained — `"MARGIN_CALL_LIQUIDATION": "CANNOT_MAP_NO_FROZEN_LIQUIDATION_FEE_SEMANTICS"` in both cost versions (`…BASE-TIER0-V1.json:48-50`; `…V2.json:65-67`); Path D choice B4=A keeps it | "complete applicable economic mapping + historical scope"; "no clearance fee on liquidations" is not a waiver of ordinary fees (`P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:92`) | venue+Bridge capture | P020 cost admission; liquidation-path risk |
| **C-12** | `…03_PRODUCTION_CLOSURE_MATRIX.md:41` | Signed risk C-12 — cost human reviewer: "key absent (not null)" | B | PENDING — no human-reviewer field exists in either cost record version (full reads of `…BASE-TIER0-V1.json` 73 lines and `…V2.json` 95 lines) | "real **qualified** human review" | experienced human | P020 cost admission |
| **F-13** | `…03_PRODUCTION_CLOSURE_MATRIX.md:42` | Signed risk F-13 — funding effective interval: `null` | B | PENDING — `"effective_interval": null` (`…funding/HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1.json:3`); Path D requires one complete declared half-open interval beginning at or after `2026-09-12T11:00:00Z` (`P/RATIFICATION_DRAFTS_UNEXECUTED/REAL_OBSERVATION_INTAKE.md:31`) | "complete period + interval semantics"; whole-interval refusal on any gap (choice A3=A) | venue+Bridge capture + Baris | P020 funding admission; WP-V2A-03 |
| **F-14** | `…03_PRODUCTION_CLOSURE_MATRIX.md:43` | Signed risk F-14 — funding events: `null`; `REFUSED_MISSING_PRODUCTION_FUNDING_EVENTS` | B | REFUSED — `"admission_status": "REFUSED_MISSING_PRODUCTION_FUNDING_EVENTS"`, `"events": null` (`…FUNDING-RULES-V1.json:2,14`) | "complete admissible event series" with an exact-once inventory for the whole declared interval | venue+Bridge capture | P020 funding admission |
| **F-15** | `…03_PRODUCTION_CLOSURE_MATRIX.md:44` | Signed risk F-15 — event timestamp: 4 raw stamps collected, not admitted | B | PENDING — `events[].event_timestamp` remains in `refused_missing_fields` (`…FUNDING-RULES-V1.json:42-50`) | "payment/interval association" | venue+Bridge capture | P020 funding admission; OPEN-07 Bridge mapping |
| **F-16** | `…03_PRODUCTION_CLOSURE_MATRIX.md:45` | Signed risk F-16 — funding event ID: none admitted | B | PENDING — `events[].funding_event_id` refused (`…FUNDING-RULES-V1.json:42-50`); exact-once per (account, coin, event time) with duplicate/conflict refusal is the signed guard (`P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:62`) | "source-bound unique identity + dedup/exact-once" | venue+Bridge capture | P020 funding admission |
| **F-17** | `…03_PRODUCTION_CLOSURE_MATRIX.md:46` | Signed risk F-17 — raw rate: 4 rows `0.0000125`, not admitted | B | PENDING — `events[].raw_rate` refused (`…FUNDING-RULES-V1.json:42-50`) | "bind authoritative rates to admitted payments" | venue+Bridge capture | P020 funding admission |
| **F-18** | `…03_PRODUCTION_CLOSURE_MATRIX.md:47` | Signed risk F-18 — positive-rate payer: `LONG` rule implemented; no per-event objects | B | PENDING — rule present (`"positive_rate_payer": "LONG"`, `…FUNDING-RULES-V1.json:39`); payer-sign check against the settled position side is a signed guard (`PATH_D_DECISION_PACKET.md:62`) | "proven convention onto sourced events" | venue+Bridge capture | P020 funding admission |
| **F-19** | `…03_PRODUCTION_CLOSURE_MATRIX.md:48`; `PATH_D_DECISION_PACKET.md:15,53` | Signed risk F-19 — oracle price: 3 samples; no settlement valuation | B | PENDING, structurally hard — "No account-side observation reveals the consensus state read at computation"; back-calculating price from amount ÷ szi ÷ rate is "explicitly insufficient" | "authoritative source + defensible per-payment association" — an oracle state read at computation | venue+Bridge capture (or a venue answer) | P020 funding admission; any funding revaluation claim |
| **F-20** | `…03_PRODUCTION_CLOSURE_MATRIX.md:49` | Signed risk F-20 — oracle price source: `SPOT_ORACLE` rule; per-event provenance missing | B | PENDING — rule present (`"valuation_price_source": "SPOT_ORACLE"`, `…FUNDING-RULES-V1.json:40`); per-event provenance refused | "true valuation-source identity per event" | venue+Bridge capture | P020 funding admission |
| **F-21** | `…03_PRODUCTION_CLOSURE_MATRIX.md:50` | Signed risk F-21 — event provenance: raw capture metadata only | B | PENDING — `events[].provenance` refused (`…FUNDING-RULES-V1.json:42-50`) | "bind request/source/bytes/time/event + coverage" | venue+Bridge capture | P020 funding admission |
| **F-22** | `…03_PRODUCTION_CLOSURE_MATRIX.md:51` | Signed risk F-22 — source event digest: none admitted | B | PENDING — `events[].source_event_digest` refused; the exporter's production mode remains `UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN` (`PATH_D_DECISION_PACKET.md:150,162`) | "deterministic raw→event digest, source-bound" | venue+Bridge capture | P020 funding admission; Bridge exporter production mode |
| **F-23** | `…03_PRODUCTION_CLOSURE_MATRIX.md:52` | Signed risk F-23 — funding human reviewer: "key absent (not null)" | B | PENDING — no human-reviewer field exists in the funding record (full read of `…FUNDING-RULES-V1.json`, 55 lines) | "real **qualified** human review after complete evidence" | experienced human | P020 funding admission |
| **R-24** | `…03_PRODUCTION_CLOSURE_MATRIX.md:53`; design `:1986-1987`; `CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:22` | Signed risk 24 — one of "four retained shared requirements": run-manifest digests + effective intervals. Packet enumeration: `P/CURRENT_SUPPORT/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.json` item 4 `notes` ("run-manifest requirements 24-27 (cost/funding source digests and effective intervals for which no canonical production pointer exists)"). Lead reading of that text: the four are the cost source digest, the funding source digest, the cost effective interval and the funding effective interval; the source states no per-ID order | B | PENDING — grouped in the source; "no canonical production pointers"; "(grouped; per-ID ordering unavailable)" | "derive from completed accepted records"; actual new record identities and interval intersection after venue facts exist (`CONTROL_TABLE.md:22`) | Lead (derived) | P020; production receipt run-manifest |
| **R-25** | as R-24 | Signed risk 25 — shared run-manifest/effective-interval requirement | B | PENDING — see R-24; per-ID content is not separately enumerated in any source read (§6) | as R-24 | Lead (derived) | as R-24 |
| **R-26** | as R-24 | Signed risk 26 — shared run-manifest/effective-interval requirement | B | PENDING — see R-24 | as R-24 | Lead (derived) | as R-24 |
| **R-27** | as R-24 | Signed risk 27 — shared run-manifest/effective-interval requirement | B | PENDING — see R-24 | as R-24 | Lead (derived) | as R-24 |
| **OBLG-1** | `open_item_applicability.json:20-23`; mapping `CT13/MTC_COMMAND_CENTER/_AI_MEMORY/P012_ASTRA_CONTINUATION_20260910.md:94` | Residual obligation (OPEN-01 #1): "minimum_quantity: venue publishes none (recorded)" | B | PENDING — the record keeps the question open; the owner guard is explicitly not a venue fact (`…HYPERLIQUID-BTC-PERP-V1.4.json:73`) | A venue-stated quantity minimum, or a recorded authoritative absence; never inferred from omission | venue+Bridge capture | P020 sizing; WP-V2A-03 |
| **OBLG-2** | `open_item_applicability.json:20-23`; `…P012_ASTRA_CONTINUATION_20260910.md:94` | Residual obligation (OPEN-01 #2): "section-16 human review by owner at build acceptance" | B | PENDING — preserved exactly; "Do not replace owner ratification with generic qualified review" (`…03_PRODUCTION_CLOSURE_MATRIX.md:59`) | The owner's own Section-16 human review at build acceptance | Baris | Production acceptance of the instrument record; P020 |
| **OBLG-3** | `open_item_applicability.json:57-60`; `…P012_ASTRA_CONTINUATION_20260910.md:94` | Residual obligation (OPEN-03 #1): "margin-call/liquidation fill class: CANNOT MAP … cost record for that class is BLOCKED until a sourced decision" | B | REFUSED-BY-DESIGN, retained — see C-11 | Sourced liquidation fee semantics plus an owner decision | venue+Bridge capture + Baris | P020 cost admission |
| **OBLG-4** | `open_item_applicability.json:57-60`; `…P012_ASTRA_CONTINUATION_20260910.md:94` | Residual obligation (OPEN-03 #2): "fee rounding / minimum-fee fields: NOT stated by frozen bytes; cost records carry only sourced fields" | B | REFUSED-BY-DESIGN, retained — see C-7/C-9 | Authoritative rounding/minimum-fee rules; no zero or rule inferred | venue+Bridge capture | P020 cost admission |
| **OBLG-5** | `open_item_applicability.json:129-131`; `…P012_ASTRA_CONTINUATION_20260910.md:94` | Residual obligation (OPEN-07 #1): "16/18 fields without direct Bridge source — later integration work package; no Bridge change implied" | B | PENDING — a carried source-era mapping, not a fresh post-retention measurement (`…03_PRODUCTION_CLOSURE_MATRIX.md:61`) | Separately authorized Bridge schema read + field-by-field mapping + owner approval | Lead + Baris | Bridge integration; P020 funding consumption |
| **PD-A** | `P/AUTHORITY/PATH_D/PATH_D_DECISION_SIGNED_20260912.md:6`; `PATH_D_DECISION_PACKET.md:57-64` | Signed Path D decision A — funding class `HL_FUNDING_VENUE_REPORTED_CASH_V1`, APPROVE | A (signed rule to preserve) | DONE as a rule — carried by the funding source class and the exporter design; no funding cash admitted (F-13..F-22) | — | — | — |
| **PD-A1** | `…SIGNED_20260912.md:6`; `PATH_D_DECISION_PACKET.md:70` | Choice A1 = A — admission window "Forward-only: only settlements captured live on the owner's own account after signature" | A (rule) | DONE as a rule; unexercised — no settlement captured (`LEAD/FINAL_STATE_20260913.json:13`) | — | — | — |
| **PD-A2** | `…SIGNED_20260912.md:6`; `PATH_D_DECISION_PACKET.md:71` | Choice A2 = B — magnitude guard "Cap at M × the largest own-account observed rate", **M PENDING, separate decision after N observations** | B | PENDING — `"funding_M": "PENDING_OWNER_AFTER_OBSERVATIONS"` (`LEAD/FINAL_STATE_20260913.json:14`); "Until the first observations exist, log without refusing" | At least one authenticated own-account observed rate, then an explicit owner decision fixing M; no invented constant | Baris (after venue+Bridge capture) | P020 funding admission; funding guard behaviour |
| **PD-A3** | `…SIGNED_20260912.md:6`; `PATH_D_DECISION_PACKET.md:72` | Choice A3 = A — coverage gap: "Refuse the whole interval" | A (rule) | DONE as a rule — "any missing settlement in the declared interval refuses the **whole** interval rather than interpolating" (`PATH_D_DECISION_PACKET.md:62`) | — | — | — |
| **PD-B** | `…SIGNED_20260912.md:7`; `PATH_D_DECISION_PACKET.md:88-95` | Signed Path D decision B — fees: admit venue-reported per-fill cash (`HL_FEE_REPORTED_PER_FILL_V1`) plus a guarded estimator, APPROVE | A (signed rule to preserve) | DONE as a rule — cost record v2 carries `ADMITTED_HL_FEE_REPORTED_PER_FILL_V1` with the estimator kept separate (`…BASE-TIER0-V2.json:2-4,11-19`); no fee admitted yet | — | — | — |
| **PD-B1** | `…SIGNED_20260912.md:7`; `PATH_D_DECISION_PACKET.md:101` | Choice B1 = C — "Both: admit reported, keep schedule as guarded estimator" | A (rule) | DONE as a rule — `estimator_schedule_id: HL_FEE_SCHEDULE_ESTIMATOR_GUARDED_V1` (`…BASE-TIER0-V2.json:19`) | — | — | — |
| **PD-B2** | `…SIGNED_20260912.md:7`; `PATH_D_DECISION_PACKET.md:102` | Choice B2 = C — estimator tolerance `T` = 5% relative (owner note: "alt max(5%, 1e-6 USDC)") | A (rule) | DONE as a rule at 5% relative: `"tolerance_relative": 0.05`, `"tolerance_form": "RELATIVE_FRACTION_OF_ESTIMATE_V1"` (`…BASE-TIER0-V2.json:16-17`). The absolute-tolerance alternative is **not** adopted (`P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:17`); it may be adopted only with RED/GREEN showing it never weakens detection (`…SIGNED_20260912.md:16`) | — | — | — |
| **PD-B3** | `…SIGNED_20260912.md:7`; `PATH_D_DECISION_PACKET.md:103` | Choice B3 = B — "Amend the start to the first authenticated own-account fill" (rule arm) | A (rule) | DONE as a rule — `"admitted_interval_start": null` with basis "UNSPECIFIED — the first authenticated own-account fill … so the start is null and every admitted-cost computation under this record refuses" (`…BASE-TIER0-V2.json:5-6`) | — | — | — |
| **PD-B3-FILL** | `P/RATIFICATION_DRAFTS_UNEXECUTED/REAL_OBSERVATION_INTAKE.md:17`; `…BASE-TIER0-V2.json:5-6` | The first-authenticated-fill fee boundary itself: "The fee-evidence interval begins at the first authenticated fill. That start is distinct from the funding interval's signed lower bound" | B | PENDING — no authenticated fill exists (`LEAD/FINAL_STATE_20260913.json:13`) | One authenticated own-account fill with immutable original bytes, pre-parse SHA-256, native identity/time and the runtime declarations listed at `REAL_OBSERVATION_INTAKE.md:21-25` | venue+Bridge capture | P020 cost admission; C-6 |
| **PD-B4** | `…SIGNED_20260912.md:7`; `PATH_D_DECISION_PACKET.md:104` | Choice B4 = A — liquidation class "Keep `CANNOT_MAP`" | A (rule) | DONE as a rule — preserved verbatim in both cost records (C-11) | — | — | — |
| **PD-N3** | `…SIGNED_20260912.md:7`; `PATH_D_DECISION_PACKET.md:94` | N = 3 fills required for fee admission: "one maker, one taker, and one near the $10 minimum-notional boundary" | B | PENDING — "N=3 authentic own-account native-BTC maker/taker/near-$10 fills … remain external requirements" (`LEAD/FINAL_HANDOFF_20260913.md:33`) | Exactly three qualifying authenticated fills in the declared forward scope, with origin, ownership, order association and completeness evidence (`REAL_OBSERVATION_INTAKE.md:24,39-43`) | venue+Bridge capture | P020 cost admission; C-6/C-10 |
| **PD-C** | `…SIGNED_20260912.md:8`; `PATH_D_DECISION_PACKET.md:120-126` | Signed Path D decision C — quantity guard `HL_QTY_OWNER_GUARD_NOT_VENUE_FACT_V1`, APPROVE | A (signed rule to preserve) | DONE as a rule — record v1.4 carries the guard and its mandatory marker (`…HYPERLIQUID-BTC-PERP-V1.4.json:112-115`) | — | — | — |
| **PD-C1** | `…SIGNED_20260912.md:8`; `PATH_D_DECISION_PACKET.md:132` | Choice C1 = A — "Numeric guard + provenance marker (no schema change)" | A (rule) | DONE — `minimum_quantity_provenance: HL_QTY_OWNER_GUARD_NOT_VENUE_FACT_V1`; "A numeric `minimum_quantity` without this exact marker class is refused by the consumer" (`…V1.4.json:74,113`) | — | — | — |
| **PD-C2** | `…SIGNED_20260912.md:8`; `PATH_D_DECISION_PACKET.md:133` | Choice C2 = B — guard multiple K = 10 → `0.0001` BTC | A (rule) | DONE — `"minimum_quantity": 0.0001` = K=10 × `quantity_step` `0.00001` (`…V1.4.json:73,112,222,252`) | — | — | — |
| **PD-C3** | `…SIGNED_20260912.md:8`; `PATH_D_DECISION_PACKET.md:134` | Choice C3 = A — size rounding "Floor / toward zero", then refuse if the floored size breaks `MinTradeNtl` or the guard | A (rule) | DONE as a rule — "Keep quantity step `0.00001`, minimum quantity `0.0001 BTC`, the independent minimum-notional rule, floor/toward-zero sizing, and refusals separate" (`P/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:21`) | — | — | — |
| **PD-SCOPE** | `…SIGNED_20260912.md:9`; `CONTROL_RECONCILIATION.md:17` | "Account/product/interval: UNSPECIFIED until authenticated evidence exists" | B | PENDING — unchanged; no account, product or interval is declared | A declared own account, product and complete half-open interval, backed by authenticated evidence | Baris (declaration) + venue+Bridge capture (evidence) | P020 cost/funding admission; every production record identity |
| **PD-FUND-START** | `CONTROL_RECONCILIATION.md:29`; `REAL_OBSERVATION_INTAKE.md:31`; `…SIGNED_20260912.md:19` | Funding interval lower bound: "The whole declared funding interval must begin at or after `2026-09-12T11:00:00Z`"; it must not be inferred from or substituted for the FEES boundary | B | PENDING — no interval declared; the two boundaries stay distinct | One complete forward interval at or after that instant with an exact-once inventory; any gap refuses the whole interval | venue+Bridge capture + Baris | P020 funding admission; F-13 |
| **PD-MONEY-GATE** | `CONTROL_RECONCILIATION.md:39`; `CT13/…/REVIEW_POLICY.md:73-76`; `LEAD/FINAL_HANDOFF_20260913.md:33` | "the experienced-human money gate is separate" | B | PENDING — explicitly separate from Section-16/R29 and from owner ratification | A real experienced-human review before the first money-exposed release, with a named question and stop condition | experienced human | Any money-exposed release; P020 cost admission; WP-V2A-03 |
| **PD-PATH1** | `PATH_D_DECISION_PACKET.md:25`; `…SIGNED_20260912.md:19` | "Path 1" self-observation is **not** part of the packet's authority; owner addendum "we will rely on Path D"; Path 1 mainnet instances are NOT pursued now (mainnet balance $9.80; no deposit) | B | NOT PURSUED — admission of real fees/funding "begins at the first naturally occurring authenticated fill/settlement" | If ever pursued: its own separate explicit owner authorization | Baris | Timing of every B row that depends on authenticated observations |
| **O-05** | `CT13/MTC_COMMAND_CENTER/11_TRIAGE/REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:128` | "Simplify MTC_V2: essential strategy and position management in the core; advanced filters, exits, transforms optional or retired" — carriers WP-P0-09/10/11/**12** | B | COVERED at register level, not closed — "the module split is **DL-23, proposed and not owner-ratified**"; the seven `tw_*` keys are assigned to the kernel chain WP-P0-09 → WP-P0-12 and are excluded from the routing-cleanup package that names them (`…PLAN_2026-08-22.md:549`) | Owner ratification of the module-split decision plus the carrier packages' own acceptance | Baris + Lead | G3-K kernel chain; WP-P0-09/10/11 |
| **O-07** | `…REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:130` | "One authoritative Python Strategy Kernel used by backtest, forward test, paper and live" — carriers WP-P0-09/10/11/**12** | B | COVERED at register level, not closed — the "paper and live" arms need runtime wiring, which P012 explicitly excludes ("no runtime wiring", `…PLAN_2026-08-22.md:407`) | An accepted kernel plus the separately gated runtime-wiring package | Lead + Baris | WP-V2A-03; P020 canonical simulator migration |
| **O-40** | `…REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:163` | "Kernel built as `LEGACY_COMPATIBLE` exact reproduction, then separately documented and tested `CORRECTED_VNEXT` fixes … no undocumented behavioural difference between the two" | A | PENDING — carried by the bounded evidence plus the Section-16 review; the documented corrections exist as `DEF-P012-01..08` with defect records and RED/GREEN evidence (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:26-33,172`) | — | — | — |
| **D-08** | `…REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:191` | "Economic golden scenarios and D026 RED/GREEN falsification required for migration and parity claims" | A | DONE for the reviewed scope — 17 complete scenarios, 10 probes `DETECTED`, four exact-G4 behavioural RED cases, four current GREEN cases, 18 regression cases and 33 adversarial controls (`LEAD/FINAL_HANDOFF_20260913.md:27`; `P/RATIFICATION_DRAFTS_UNEXECUTED/ADVERSE_COST_EVIDENCE.md:17-22`) | — | — | — |
| **ENG-STATE** | `LEAD/FINAL_HANDOFF_20260913.md:13-15,19`; `LEAD/FINAL_STATE_20260913.json:3-7` | The reviewed research/engineering deliverable itself: clean candidate G5, core unchanged, repair counter 5, `"engineering": "COMPLETE_WITHIN_AUTHORIZATION"` | A | DONE — `source_clean: true`, `source_changes_this_continuation: 0` | — | — | — |
| **EVID-DRAFTS** | `P/RATIFICATION_DRAFTS_UNEXECUTED/STATUS.md:3`; `P/RATIFICATION_DRAFTS_UNEXECUTED/PROVENANCE_ADDENDUM.md:3-5` | The eight ratification/intake drafts: "unapplied, nonaccepting, and do not record owner ratification, a formal Section-16 review, or a signature" | A (must stay unapplied until ratification) | PENDING — all eight verified byte-identical to the comparison source; "The eight packet drafts remain unratified" | — | — | — |
| **P020-DEP** | `LEAD/FINAL_HANDOFF_20260913.md:35`; `P/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:38-40` | Downstream reconciliation: "P020 has no accepted P012 dependency B01 or production cost admission"; P020 may consume engineering evidence and drafts only | B | OPEN — must be reconciled individually; this amendment unblocks nothing | An accepted P012 dependency B-01 interface and a real production cost admission, each through its own gate | Lead + Baris | P020 `check_p020_acceptance.py` `required_tier_implemented`; P013 (transitively) |

---

## 3. Class A closure checklist

Every item must exist as a real artifact before the label "P0-12 research/engineering scope
complete; production admission pending" may be used. None of these steps is performed by this
lane. "Verify" names a path to inspect or an existing command already used in this package; no new
command is invented here.

| # | Artifact that must exist | Producing step | Verifying command / path |
|---|---|---|---|
| A-0 | The recorded decision row `OD-20260913-P012-SCOPE-1` in root `DECISIONS.md`, plus its `02_TASKS/TASK_HISTORY.json` entry and an `_AI_MEMORY` scope record | Owner signs §1; the Lead records it (Lead act, not a model act) | Search `DECISIONS.md` for `OD-20260913-P012-SCOPE-1`; compare wording byte-for-byte with §1; re-measure the row length |
| A-1 | A formal Section-16 **Item 1** result with no unread required subject: native reads of all 17 goldens including `RULE2-02-GREEN`…`RULE2-07-GREEN`, `DERIVATIONS.md`, `AUTHOR_SOURCE_CENSUS.json` and the author anchor draft beyond the ranges already read | Re-run the bounded A-scope call with the required reviewer through the pinned launcher | `S16REV/A_FORMULAS_LINEAGE/NATIVE_READ_VERIFICATION.json` method re-applied to the new conversation DB; gaps listed in `S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:11` must be closed |
| A-2 | Section-16 **Items 2, 3, 5, 6** results, each reviewer-owned, with exhaustive ordered hunk indices for Item 2 (218 physical hunks over 139 paths, 399,045-byte canonical patch) | Launch the prepared, never-run prompts `B1_RECORDS`, `B2_ECONOMICS`, `B3_STATE`, `C_CATALOG_CONSUMERS` under fresh quiet-window coordination | Prompt paths at `TAKEOVER/P012_HANDOFF.md:43-47`; runner `C:/tmp/P012_S16_LAUNCH_PREP_20260913/run.ps1`; helper `Invoke-GeminiProReadOnly.ps1` pinned SHA256 `66c749a08b2559d1b275bd458920dd03ed5eaf581ff13ccc777c6f801e8de5e2` (`TAKEOVER/START_HERE.md:66`) |
| A-3 | One new `semantic_coverage_review.json` receipt: reviewer identity, exact commit/tree identities equal to G5 `6d6a4502…f889` / core `4698e716…16fe`, per-item evidence paths, one terminal disposition per item, unresolved items listed, non-empty `NOT VERIFIED` | Reviewer authors it; Lead assembles on disjoint paths | Design requirement `P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:809`; contract requirements `S16REV/FORMAL_REVIEW_CONTRACT.md:13,15,17` |
| A-4 | Lead adjudication with independent native-read proof, on paths disjoint from reviewer output and assembly | Lead reproduces; never assigns semantic classification | `S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md`; `NATIVE_READ_VERIFICATION.json`; rule at `S16REV/FORMAL_REVIEW_CONTRACT.md:15` |
| A-5 | `check_review_report.py` run **unmodified** against the new report and the canonical packet, with its actual exit recorded (current partial-call run: exit 1, 2 items, 168 packet-tree citations, sole reason `PARTIAL_REVIEW_ONLY`) | Lead runs it; never rewrites dispositions or forces `UNCHANGED` to obtain a pass | `S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:15`; `TAKEOVER/P012_HANDOFF.md:37` |
| A-6 | An **actual** owner ratification record for seals `#36`-`#39` and the retained earlier chain, in the owner's own words, with no fabricated signature | Owner acts; Lead records (`OD-20260908-1` at `P/CAND/DECISIONS.md:22` is the precedent form for a re-seal ratification) | Compare with the `RESEAL_29_RATIFIED = YES` precedent; ratification precondition stated at `TAKEOVER/P012_HANDOFF.md:49` |
| A-7 | Applied chain/schema/receipt metadata: JSON chain extended from 33 entries/`#35` and Markdown from 28/`#30` toward the proposed 37 entries/`#39`, applied **only after** A-6 | Lead applies the prepared drafts (currently unapplied) | `P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:12`; `P/RATIFICATION_DRAFTS_UNEXECUTED/STATUS.md:3` |
| A-8 | A fresh full-gate result whose `refusals` list no longer contains `SEMANTIC_COVERAGE_REVIEW_INVALID`, with the actual exit code recorded truthfully whatever it is | Re-run the full gate after A-3/A-6/A-7 | Compare against `LEAD/LEAD_R5/FINAL_GATE.json:692-700`; `claim_label` field at `:114` |
| A-9 | A green contract self-test suite: `test_verify_bceg.py::test_v2_schema_accepts_complete_receipt_and_rejects_nested_mutants` passing because the chain capacity is legitimately reconciled, never by relaxing the schema | Apply A-7, then re-run the contract self-tests | `LEAD/LEAD_R5/FINAL_GATE.json:117-125`; failure description `P/RATIFICATION_DRAFTS_UNEXECUTED/ADVERSE_COST_EVIDENCE.md:21` |
| A-10 | The protected check `Bridge suite (Python 3.12)` green on an up-to-date head **if and when** an authorized PR exists; otherwise an explicit "not run, not authorized" record | Separate release authority (see MERGE-AUTH, Class B) | `P/CAND/AGENTS.md:47-49`; current state `LEAD/FINAL_STATE_20260913.json:15` |
| A-11 | Every first use of the completion label renders it exactly as "P0-12 research/engineering scope complete; production admission pending", together with the statement that production admission is not granted | Whoever writes the status/handoff/report | Modelled on the mandatory-rendering rule at `P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:1906-1911` |
| A-12 | A preservation check proving no refusal changed: the three production record files and their `.sha256` sidecars unchanged, and §4's field values byte-identical | Lead re-hashes the record files before and after any ratification-metadata application | `P/CAND/mtc_v2/core/economic_records/{instruments,costs,funding}/HYPERLIQUID-*.json` and `*.sha256` |
| A-13 | A written per-package downstream reconciliation (P020, P013, P021, P031, P022, WP-V2A-01/03) stating explicitly that no production-dependent work is unblocked | Lead writes it at the package boundary | `LEAD/FINAL_HANDOFF_20260913.md:35`; `TAKEOVER/START_HERE.md:42,49,50` |

If any Class A item cannot be produced, the correct outcome is to record the blocker and **not**
use the label — the same discipline the Lead applied when refusing to promote the partial review
(`S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:3`).

---

## 4. Preserved refusals — verbatim values that must not change

These strings and states are quoted exactly. The amendment changes none of them; any future change
needs its own explicit written decision row.

**Cost record `HYPERLIQUID-BTC-PERP-BASE-TIER0-V1.json` (unchanged bytes):**
- `"admission_status": "REFUSED_INCOMPLETE_COST_SCHEDULE"` (`:2`)
- `"disposition": "KEEP_REFUSED"` (`:31`)
- `"MARGIN_CALL_LIQUIDATION": "CANNOT_MAP_NO_FROZEN_LIQUIDATION_FEE_SEMANTICS"` (`:49`)
- `"refused_missing_fields": ["fee_rounding_rule","fixed_component","minimum_fee","tier_account_selection_evidence"]` (`:51-56`)

**Cost record `…-V2.json` (Path D admitted-cost version):**
- `"admitted_interval_start": null` and its basis "No authenticated fill exists yet, so the start
  is null and every admitted-cost computation under this record refuses." (`:5-6`)
- `"superseded_disposition": "KEEP_REFUSED"` with `"supersession_scope"`: "The KEEP_REFUSED
  disposition is superseded **only** for the `HL_FEE_REPORTED_PER_FILL_V1` admitted-cost path of
  this record version … KEEP_REFUSED stays in force for `HYPERLIQUID-BTC-PERP-BASE-TIER0-V1`, whose
  bytes are unchanged, and for every schedule-computed cost." (`:47-49`)
- `"refused_missing_fields_disposition": "RETAINED. … NOT filled in, NOT defaulted and NOT
  evidenced. Under HL_FEE_REPORTED_PER_FILL_V1 they are NOT REQUIRED FOR THE ADMITTED COST, which
  is a different statement from being resolved. They remain required for any schedule-computed
  cost, and C7/C8/C9/OPEN03 stay open."` (`:74`)
- `"MARGIN_CALL_LIQUIDATION": "CANNOT_MAP_NO_FROZEN_LIQUIDATION_FEE_SEMANTICS"` (`:66`)
- `"not_an_acceptance"`: "…It is not an acceptance: T0 review, R29 semantic redo, Section-16 record
  review, owner human ratification, current-head protected CI and protected merge all remain
  required." (`:31`)
- Residual risk ids `PATHD-RISK-FEE-NO-INDEPENDENT-REVALUATION-V1` and
  `PATHD-RISK-FEE-ESTIMATOR-DEVIATION-V1` (`:75-78`)

**Funding record `HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1.json`:**
- `"admission_status": "REFUSED_MISSING_PRODUCTION_FUNDING_EVENTS"` (`:2`)
- `"effective_interval": null` (`:3`), `"events": null` (`:14`)
- `"refused_missing_fields"` listing `effective_interval`, `events[].event_timestamp`,
  `events[].funding_event_id`, `events[].oracle_price`, `events[].provenance`,
  `events[].raw_rate`, `events[].source_event_digest` (`:42-50`)

**Instrument records:**
- v1.3 `"minimum_quantity": null` (`:19`) and `"human_reviewer": null` (`:104`) — the v1.3 bytes
  remain the accepted-selection record (`…V1.4.json:256`)
- v1.4 `"minimum_quantity": 0.0001` with `"minimum_quantity_provenance":
  "HL_QTY_OWNER_GUARD_NOT_VENUE_FACT_V1"` and `"open_items": ["OPEN01"]` (`:112-115`)
- v1.4 field basis: "OWNER GUARD — NOT A VENUE FACT … OPEN01 stays OPEN. Consumers must read
  `minimum_quantity_provenance` … and must never report it as a venue minimum quantity." (`:73`)
- v1.4 `"human_reviewer": null` (`:186`) and status "Production admission remains refused:
  `provenance.human_reviewer` is still absent, so this record still refuses evaluation." (`:225`)

**Funding/fee evidence status (drafts, unapplied):**
- "Production result, report, and candidate remain `accepted:false`; `candidate_built` means
  offline construction only. `requested_source_class` retains the signed value above and
  `origin_authentication_status` remains `NOT_ESTABLISHED_CALLER_SUPPLIED`."
  (`P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:31`)
- "A source-bytes hash establishes local consistency only and cannot authenticate origin." (same
  line); D1's local `accepted:true` "denotes synthetic construction, while its candidate explicitly
  refuses production admission" (`…RESEARCH_PAPER_SCOPE_PROPOSAL.md:26`)

**Governance dispositions:**
- Item 4 `ITEM4_EXISTING_OFFLINE_SOURCES` = `NONE_KEEP_REFUSED`
  (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:2004`; `CT13/…/AUTONOMY_AUTHORIZATION.md:14`)
- `FEE_FIXED_COMPONENT_ZERO`, `FEE_MINIMUM_FEE_ZERO`, `FEE_ROUNDING_RULE` = `KEEP_REFUSED`;
  `LIQUIDATION_FEE_CLASS` = `KEEP_REFUSED_UNTIL_OFFICIAL_SOURCE`; `COST_EFFECTIVE_INTERVAL`,
  `FUNDING_EFFECTIVE_INTERVAL` = `CAPTURE_FORWARD_AFTER_AUTHORIZED_CAPTURE`;
  `HUMAN_REVIEWER_FIELDS` = `LEAVE_EMPTY_UNTIL_REAL_RECORDS_EXIST_AND_A_REAL_REVIEW_OCCURS`
  (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:2000-2004`)
- Gate state: `"claim_label": "BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED"`
  (`LEAD/LEAD_R5/FINAL_GATE.json:114`); refusals `SEMANTIC_COVERAGE_REVIEW_INVALID` and
  `CONTRACT_SELFTEST_RED` (`:692-700`)
- Milestone token `P012_SYNTHETIC_ONLY_NON_PRODUCTION_MILESTONE_V1 — NOT WP-P0-12 ACCEPTANCE`
  remains in force and unretired (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:1906-1911,2019-2025`)
- Blocked expected nodes stay excluded, not matched: `comparison_claim_scope =
  ALL_NON_BLOCKED_EXPECTED_NODES`, 20 `blocked_node_skips`
  (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:823`; `LEAD/LEAD_R5/FINAL_GATE.json:4-5`)

---

## 5. Labelled assumptions (each remains an ASSUMPTION)

1. **ASSUMPTION — zero slippage.** `slippage_bps = 0` is an "OWNER-DECLARED EXPLICIT ZERO
   ASSUMPTION" with `measurement_claimed:false`, `venue_source_claimed:false`
   (`…BASE-TIER0-V2.json:85-90`). It is not a measured venue value.
2. **ASSUMPTION — quantity guard K=10.** `minimum_quantity = 0.0001` is an owner guard, "NOT A
   VENUE FACT", and does not establish that a venue floor is absent (`…V1.4.json:73`).
3. **ASSUMPTION — estimator tolerance.** 5% relative tolerance is an owner choice (B2=C), not a
   venue-published bound (`…BASE-TIER0-V2.json:13,16-17`).
4. **ASSUMPTION — base tier-0 selection.** `tier_selection_basis` is
   `OWNER_APPROVED_BASE_TIER_0_WITH_ACCOUNT_EVIDENCE_RESIDUAL`; account-tier evidence is collected
   but not incorporated (`…BASE-TIER0-V2.json:93`; C-10).
5. **ASSUMPTION — same-bar policy.** `STOP_FIRST` is an owner ruling (addendum 15 row 32), not a
   venue-derived fact (`…EVENING.md:225`).
6. **ASSUMPTION — same-timestamp funding eligibility.** "INCLUDE" is expressly "the owner's
   economic ruling" where "the venue text is silent" (`…EVENING.md:305-309`).
7. **ASSUMPTION — guard PnL basis.** GROSS-MINUS-FEES for daily-loss, consecutive-loss and
   time-stop is D017 extended by owner choice, pending funding capture (`…EVENING.md:231-233`;
   design `:909`).
8. **ASSUMPTION — no additional numeric bounds.** An explicit owner "no additional bounds"
   decision, not evidence that none are needed (`…EVENING.md:226-227`).
9. **ASSUMPTION — legacy-side declared states.** Honest limit L10: sealed legacy projection states
   tagged `source: DESIGN_DERIVED` are "a design-derived declaration … never read from the baseline
   bytes"; RULE-2 claims read "against the sealed declaration", not the measured legacy bytes
   (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:824`).
10. **ASSUMPTION — RULE2-08 cost record reuse.** Honest limit L11: no economic value was chosen for
    RULE2-08; the record is a by-reference reuse of RULE2-07's
    (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:825`).
11. **ASSUMPTION — post-hoc admitted members.** Honest limit L13: members admitted from current
    kernel emission "are design declarations, not facts derived from venue prose"
    (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:831-835`).
12. **ASSUMPTION — re-seal chain assertion.** Honest limits L14/W355: the owner-directed re-seal
    chain "is asserted and human-reviewed under section 16, not machine-checked"
    (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:836-844,846-867`).
13. **ASSUMPTION — referral-discount exposure.** The estimator's money-terms figures are `[derived]`
    from cited rates under an explicitly assumed applicability of the observed 4%
    `activeReferralDiscount` (`P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:95`).
14. **ASSUMPTION — funding scale illustration.** The "$0.07 / $1.23 / ≈$1.16 per-settlement gap"
    figures are `[derived]` under an "explicitly *assumed* (not venue-confirmed) proportionality to
    position value"; settlement cadence is not established
    (`P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:64`).
15. **ASSUMPTION — quantity-guard cost illustration.** The `$1.14` / `$11.43` / `$114.30` figures
    are valid only at the single observed price `oracle_px 114296` and "are not a current price"
    (`P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:126`).
16. **ASSUMPTION — bounded claim shape.** The design's acceptance claim is bounded evidence over a
    finite catalog, "not semantic proof"; the residual gap to the Phase-0 bar is carried by the
    Section-16 review and the honest limits (`P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:28-33`).
17. **ASSUMPTION — counts quoted, not recomputed.** "27 signed risks", "five residual obligations",
    "ten OPEN production rows", chain entry counts and packet member counts are quoted from their
    sources; this lane recomputed none of them.

---

## 6. NOT VERIFIED

1. **No enumerated list of exactly 27 signed risks exists inside the packet `P/AUTHORITY/`.** (Lead addition: the packet does enumerate them outside `AUTHORITY/`, in the historical receipt's Item 4 `notes` at `P/CURRENT_SUPPORT/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.json`: "Residual production risks are retained for 27 items: I rows 1-5 (/status, /price_tick, /minimum_quantity, /provenance/human_reviewer, absent aggregate /provenance/source_sha256); C rows 6-12 (…); F rows 13-23 (/effective_interval, /events, eight unsourced event members, /provenance/human_reviewer); and run-manifest requirements 24-27 (cost/funding source digests and effective intervals…)". That enumeration matches §2 rows I-1..F-23 field for field; rows 24-27 remain grouped there too.) What
   the packet carries are counts and restatements only: `PATH_D_DECISION_PACKET.md:11,198,211`,
   `PATH_D_DECISION_SIGNED_20260912.md:10`, `AUTHORITY/CURRENT_CONTROL/TASK_HISTORY.json:399`,
   `P/CAND/DECISIONS.md:73,76`, and the drafts at
   `RESEARCH_PAPER_SCOPE_PROPOSAL.md:30`, `CONTROL_RECONCILIATION.md:37`,
   `REAL_OBSERVATION_INTAKE.md:45`, `ADVERSE_COST_EVIDENCE.md:41`.
2. **The enumeration used in §2 comes from outside the packet** —
   `CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:24-55`, a document that labels
   itself "nonbinding readiness. No acceptance, closure, or admission" (`:3`). Its own arithmetic is
   `5 (I) + 7 (C) + 11 (F) + 4 shared (24–27) = 27` (`:26`). The packet corroborates the *shape* of
   that split at `P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:1986-1987` ("I rows 1-5; C rows 6-12;
   F rows 13-23; and run-manifest requirements 24-27"), but no packet file enumerates the 27 rows.
3. **Risks 24-27 are not individually identified anywhere I read.** The matrix groups them as
   "four retained shared requirements (grouped; per-ID ordering unavailable)" (`:53`). §2 therefore
   carries four rows `R-24`..`R-27` whose per-ID content is *not* established. Only 23 of the 27
   risks have individual identifiers and content in any source read.
4. **The matrix's own cited primary source could not be found.** It cites `PRIOR_CHECKLIST.md:23-48`
   (`:26`); a recursive search of `CODEX/` found no file named `PRIOR_CHECKLIST*`. Its second
   citation, `semantic_coverage_review.json:4503`, resolves in the packet only to the *historical*
   receipt, which `P/EVIDENCE_STATUS.md:5` says "is not current acceptance evidence".
5. **The five residual obligations are nowhere enumerated under that name.** Sources give counts
   only: `CONTROL_TABLE.md:3`, `CLOSURE_PACKET.md:3`,
   `CODEX/WP_P0_12_ACQUISITION/LEAD_VERIFICATION.json:38` (`"remaining_obligations": 5`),
   `CODEX/WP_P0_12_SPRINT/RELEASE_RECEIPT.json:10` (`"residual_obligations": 5`). The only
   composition found is `CT13/MTC_COMMAND_CENTER/_AI_MEMORY/P012_ASTRA_CONTINUATION_20260910.md:94`
   — "5 residual integration obligations OPEN01 x2 / OPEN03 x2 / OPEN07 x1" — which matches the
   `open_residuals` arrays at `open_item_applicability.json:20-23,57-60,129-131`. §2's OBLG-1..5
   rows rest on that match; it is a reconciliation, not a source that names five obligations.
6. **Gate exit code 2 was not re-executed by this lane.** It is quoted from
   `P/RATIFICATION_DRAFTS_UNEXECUTED/ADVERSE_COST_EVIDENCE.md:22` and
   `LEAD/FINAL_HANDOFF_20260913.md:27`; the refusal strings themselves are read directly from
   `LEAD/LEAD_R5/FINAL_GATE.json:692-700`.
7. **No literal gate identifier named "cost_admission" was found.** The lane brief uses it as an
   example. The literal artifacts found are `check_p020_acceptance.py` with its
   `required_tier_implemented` row reported BLOCKED
   (`CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_12_SCOPE_ASSESSMENT_2026-09-07.md:55-56`) and the
   statement "No accepted B01 or production-cost admission exists"
   (`LEAD/FINAL_HANDOFF_20260913.md:35`). §2 uses those, not an invented id.
8. **The anchor-read question — RESOLVED by the Lead after drafting.** Steps 52 and 54 of the first partial call concatenate to exactly 48,208 characters equal to line 1 of `implementation_anchor.json` (Lead byte reconciliation, 2026-09-13, `C:/tmp/CLAUDE_P0_RUN_20260913/RUN_STATE.md`); the anchor was fully read in that call. The manifest (`CONTRACT_TABLES_MANIFEST.json`) was not (46,068 of 97,973 characters). Neither fact changes the non-acceptance of that call.
9. **Item 4's substantive content was not adjudicated.** The reviewer's `ACCEPTED_WITH_RESIDUAL_RISK`
   for Items 1/4 is a reviewer claim, not Lead acceptance
   (`S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:7,11`).
10. **The 2026-09-13 owner instruction has no repository record I could find.** It reaches this lane
    only through `BRIEF.md:5-11`. The nearest recorded antecedent is
    `OD-20260912-P012-RESEARCH-PAPER-SCOPE` (`P/CAND/DECISIONS.md:77`), which authorizes preparing
    such a scope, not declaring it. The exact completion sentence "P0-12 research/engineering scope
    complete; production admission pending." was not found in any existing artifact.
11. **Packet integrity was not re-verified here.** The 962-file / 961-member manifest and its
    SHA256 `e8f76ca866a0e9920bf62e61d8fe70f7a379444b7d03bb829b67816effaea37c` are quoted from
    `TAKEOVER/START_HERE.md:20`; this lane hashed nothing.
12. **Chain counts were not recomputed.** "33 entries through `#35`", "28 through `#30`",
    "37 through `#39`" are quoted (`P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:12`).
13. **No current CI, remote or merge state was checked.** The refs reconciliation at
    `LEAD/FINAL_HANDOFF_20260913.md:37` is quoted as of 2026-09-13T04:40Z; nothing was fetched.
14. **Two record versions coexist and the active one is not established by this lane.** The cost
    record exists as `…-V1.json` (refusing) and `…-V2.json` (Path D admitted-cost), and the
    instrument record as `V1.3` (accepted selection) and `V1.4` (guard version, still refusing on
    `human_reviewer`). Which version any given consumer binds at G5 was not traced here.
15. **Whether the six mandatory Section-16 items have ever *all* been reviewed against bytes for
    any predecessor is explicitly doubtful**, per the packet's own standard: receipt #29's "six
    dispositions were never checked against bytes, and #30 is a delta that inherits them"
    (`P/AUTHORITY/SECTION16_PACKET_STANDARD.md:22-28`). Historical dispositions are therefore not
    treated as carried forward anywhere in this draft.

---

## 7. Citation index

Every file:line this draft relies on, one per line, for Lead grep-audit. `P/`, `LEAD/`, `S16REV/`,
`TAKEOVER/`, `CT13/`, `CODEX/` expand per §0.1.

```
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:26
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:28-33
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:172
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:209
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:248
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:309
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:333
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:361
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:389
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:418
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:459
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:798-809
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:800
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:802
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:803
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:804
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:805
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:806
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:807
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:809
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:815
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:822
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:823
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:824
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:825
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:831-835
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:836-844
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:846-867
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:894-910
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:896
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:900
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:901
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:902
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:903
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:904
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:905
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:906
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:907
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:908
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:909
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:1897-1925
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:1906-1911
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:1976-1987
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:1986-1987
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:1992
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:2000-2004
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:2004
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:2010-2015
P/AUTHORITY/P012_PRICE_DESIGN_V1_27.md:2019-2025
P/AUTHORITY/SECTION16_PACKET_STANDARD.md:22-28
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:11
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:15
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:25
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:53
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:57-64
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:62
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:64
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:70
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:71
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:72
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:74
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:88-95
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:92
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:94
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:95
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:101
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:102
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:103
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:104
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:106
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:110
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:120-126
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:124
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:126
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:132
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:133
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:134
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:136
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:150
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:162
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:164
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:192-193
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:194
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:195-197
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:198
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:199
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:207
P/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md:211
P/AUTHORITY/PATH_D/PATH_D_DECISION_SIGNED_20260912.md:6
P/AUTHORITY/PATH_D/PATH_D_DECISION_SIGNED_20260912.md:7
P/AUTHORITY/PATH_D/PATH_D_DECISION_SIGNED_20260912.md:8
P/AUTHORITY/PATH_D/PATH_D_DECISION_SIGNED_20260912.md:9
P/AUTHORITY/PATH_D/PATH_D_DECISION_SIGNED_20260912.md:10
P/AUTHORITY/PATH_D/PATH_D_DECISION_SIGNED_20260912.md:14
P/AUTHORITY/PATH_D/PATH_D_DECISION_SIGNED_20260912.md:16
P/AUTHORITY/PATH_D/PATH_D_DECISION_SIGNED_20260912.md:19
P/AUTHORITY/CURRENT_CONTROL/TASK_HISTORY.json:399
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:225
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:226-227
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:228-230
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:231-233
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:234-237
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:241-242
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:265-269
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:272-274
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:275-278
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:279-283
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:289-296
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:305-311
P/AUTHORITY/OWNER_DECISIONS_2026-08-29_EVENING.md:337
P/CAND/AGENTS.md:35-37
P/CAND/AGENTS.md:47-49
P/CAND/DECISIONS.md:16-78
P/CAND/DECISIONS.md:22
P/CAND/DECISIONS.md:37
P/CAND/DECISIONS.md:54
P/CAND/DECISIONS.md:73
P/CAND/DECISIONS.md:76
P/CAND/DECISIONS.md:77
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:12-32
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:20-23
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:34-49
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:51-70
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:57-60
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:72-86
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:88-104
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:106-121
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:123-139
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:129-131
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:141-154
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:156-169
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:171-185
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:188-232
P/CAND/mtc_v2/tests/corrected_vnext/contracts/open_item_applicability.json:234
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V1.json:2
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V1.json:31
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V1.json:48-50
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V1.json:51-56
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:2-4
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:5-6
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:11-19
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:13
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:16-17
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:31
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:47-49
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:65-67
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:68-74
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:75-78
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:81-90
P/CAND/mtc_v2/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json:93
P/CAND/mtc_v2/core/economic_records/funding/HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1.json:2
P/CAND/mtc_v2/core/economic_records/funding/HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1.json:3
P/CAND/mtc_v2/core/economic_records/funding/HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1.json:14
P/CAND/mtc_v2/core/economic_records/funding/HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1.json:39
P/CAND/mtc_v2/core/economic_records/funding/HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1.json:40
P/CAND/mtc_v2/core/economic_records/funding/HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1.json:42-50
P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.3.json:2
P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.3.json:19
P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.3.json:104
P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.4.json:73
P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.4.json:74
P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.4.json:97-98
P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.4.json:112-115
P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.4.json:186
P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.4.json:222
P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.4.json:225
P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.4.json:252
P/CAND/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.4.json:256
P/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:20
P/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:21
P/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:26
P/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:30
P/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:38-40
P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:12
P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:17
P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:29
P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:31
P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:37
P/RATIFICATION_DRAFTS_UNEXECUTED/CONTROL_RECONCILIATION.md:39
P/RATIFICATION_DRAFTS_UNEXECUTED/REAL_OBSERVATION_INTAKE.md:12
P/RATIFICATION_DRAFTS_UNEXECUTED/REAL_OBSERVATION_INTAKE.md:17
P/RATIFICATION_DRAFTS_UNEXECUTED/REAL_OBSERVATION_INTAKE.md:21-25
P/RATIFICATION_DRAFTS_UNEXECUTED/REAL_OBSERVATION_INTAKE.md:24
P/RATIFICATION_DRAFTS_UNEXECUTED/REAL_OBSERVATION_INTAKE.md:31
P/RATIFICATION_DRAFTS_UNEXECUTED/REAL_OBSERVATION_INTAKE.md:39-43
P/RATIFICATION_DRAFTS_UNEXECUTED/REAL_OBSERVATION_INTAKE.md:45
P/RATIFICATION_DRAFTS_UNEXECUTED/ADVERSE_COST_EVIDENCE.md:17-22
P/RATIFICATION_DRAFTS_UNEXECUTED/ADVERSE_COST_EVIDENCE.md:21
P/RATIFICATION_DRAFTS_UNEXECUTED/ADVERSE_COST_EVIDENCE.md:22
P/RATIFICATION_DRAFTS_UNEXECUTED/ADVERSE_COST_EVIDENCE.md:41
P/RATIFICATION_DRAFTS_UNEXECUTED/STATUS.md:3
P/RATIFICATION_DRAFTS_UNEXECUTED/PROVENANCE_ADDENDUM.md:3-5
P/EVIDENCE_STATUS.md:3-9
P/EVIDENCE_STATUS.md:5
LEAD/FINAL_HANDOFF_20260913.md:3
LEAD/FINAL_HANDOFF_20260913.md:13-15
LEAD/FINAL_HANDOFF_20260913.md:19
LEAD/FINAL_HANDOFF_20260913.md:20-22
LEAD/FINAL_HANDOFF_20260913.md:25
LEAD/FINAL_HANDOFF_20260913.md:27
LEAD/FINAL_HANDOFF_20260913.md:29
LEAD/FINAL_HANDOFF_20260913.md:33
LEAD/FINAL_HANDOFF_20260913.md:35
LEAD/FINAL_HANDOFF_20260913.md:37
LEAD/FINAL_STATE_20260913.json:3-4
LEAD/FINAL_STATE_20260913.json:3-7
LEAD/FINAL_STATE_20260913.json:8-10
LEAD/FINAL_STATE_20260913.json:11-16
LEAD/FINAL_STATE_20260913.json:13
LEAD/FINAL_STATE_20260913.json:14
LEAD/FINAL_STATE_20260913.json:15
LEAD/LEAD_R5/FINAL_GATE.json:3
LEAD/LEAD_R5/FINAL_GATE.json:4-5
LEAD/LEAD_R5/FINAL_GATE.json:114
LEAD/LEAD_R5/FINAL_GATE.json:117-125
LEAD/LEAD_R5/FINAL_GATE.json:692-700
S16REV/FORMAL_REVIEW_CONTRACT.md:3
S16REV/FORMAL_REVIEW_CONTRACT.md:5
S16REV/FORMAL_REVIEW_CONTRACT.md:7
S16REV/FORMAL_REVIEW_CONTRACT.md:9
S16REV/FORMAL_REVIEW_CONTRACT.md:11
S16REV/FORMAL_REVIEW_CONTRACT.md:13
S16REV/FORMAL_REVIEW_CONTRACT.md:15
S16REV/FORMAL_REVIEW_CONTRACT.md:17
S16REV/FORMAL_REVIEW_CONTRACT.md:19
S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:3
S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:5
S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:7
S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:11
S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:13
S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:15
S16REV/A_FORMULAS_LINEAGE/LEAD_ADJUDICATION.md:19
TAKEOVER/START_HERE.md:15-25
TAKEOVER/START_HERE.md:20
TAKEOVER/START_HERE.md:42
TAKEOVER/START_HERE.md:49
TAKEOVER/START_HERE.md:50
TAKEOVER/START_HERE.md:66
TAKEOVER/P012_HANDOFF.md:11
TAKEOVER/P012_HANDOFF.md:37
TAKEOVER/P012_HANDOFF.md:41
TAKEOVER/P012_HANDOFF.md:43-47
TAKEOVER/P012_HANDOFF.md:49
TAKEOVER/P012_HANDOFF.md:53
CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/REVIEW_POLICY.md:20
CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/REVIEW_POLICY.md:40-52
CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/REVIEW_POLICY.md:57-59
CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/REVIEW_POLICY.md:73-76
CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AUTONOMY_AUTHORIZATION.md:14
CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AUTONOMY_AUTHORIZATION.md:15
CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AUTONOMY_AUTHORIZATION.md:22-23
CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:400-407
CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:403
CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:406
CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:407
CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:411-414
CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:505
CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:520-522
CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:549
CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:687
CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:698-699
CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:1069
CT13/MTC_COMMAND_CENTER/11_TRIAGE/REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:128
CT13/MTC_COMMAND_CENTER/11_TRIAGE/REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:130
CT13/MTC_COMMAND_CENTER/11_TRIAGE/REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:163
CT13/MTC_COMMAND_CENTER/11_TRIAGE/REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:191
CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_12_SCOPE_ASSESSMENT_2026-09-07.md:25-34
CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_12_SCOPE_ASSESSMENT_2026-09-07.md:41-56
CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_12_SCOPE_ASSESSMENT_2026-09-07.md:55-56
CT13/MTC_COMMAND_CENTER/_AI_MEMORY/P012_ASTRA_CONTINUATION_20260910.md:94
CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:3
CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:10
CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:11-12
CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:12
CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:13
CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:15
CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:21
CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:22
CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:23
CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:24
CODEX/WP_P0_12_CONTROL/CONTROL_TABLE.md:25
CODEX/WP_P0_12_ACQUISITION/CLOSURE_PACKET.md:3
CODEX/WP_P0_12_ACQUISITION/CLOSURE_SPEC.md:17
CODEX/WP_P0_12_ACQUISITION/LEAD_VERIFICATION.json:38
CODEX/WP_P0_12_SPRINT/RELEASE_RECEIPT.json:10
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:3
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:11-20
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:12
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:24-55
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:26
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:30
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:31
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:32
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:33
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:34
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:35
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:36
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:37
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:38
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:39
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:40
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:41
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:42
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:43
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:44
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:45
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:46
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:47
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:48
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:49
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:50
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:51
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:52
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:53
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:59
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:61
CODEX/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md:62
C:/tmp/CLAUDE_P0_RUN_20260913/laneP12A_amendment/BRIEF.md:5-11
```

---

**END OF DRAFT.** Nothing above is acceptance, ratification, a review verdict or an owner
decision. The label "P0-12 research/engineering scope complete; production admission pending" may
be used only after every Class A row in §2 and every checklist item in §3 is satisfied with real
evidence, and never as a statement about production admission.

---

## 8. Lead audit and recording note (Claude Fable 5.1, 2026-09-13)

- Owner instruction provenance: chat message received mid-session on 2026-09-13; quoted verbatim in §0. No repository record predates this file; `OD-20260912-P012-RESEARCH-PAPER-SCOPE` (`P/CAND/DECISIONS.md:77`) is the antecedent that authorized *preparing* the scope.
- Citation audit: all 317 index entries were resolved mechanically against their files: 316 valid; one range exceeded its file by one line (`RESEARCH_PAPER_SCOPE_PROPOSAL.md:38-41`, file has 40 lines) and is corrected above to `:38-40`. Twelve quoted passages were spot-checked against source lines (plan `:406`, autonomy `:15`, Path D packet `:164,198,199`, cost V2 `:5-6,74`, funding `:2,3,14`, instrument V1.4 `:73,112-115,225`, owner ledger `:225`, design `:1986-1987,2004,1906-1911`, decisions `:76-77`, gate `:114,692-700`): all match.
- Corrections applied by the Lead after drafting: §6 item 8 (anchor chunks reconciled: fully read), §6 item 1 and row R-24 (packet-internal enumeration of the 27 risks located in the historical receipt's Item 4 notes; rows 24-27 identified by the Lead's reading of that text as the two source digests and two effective intervals, order unstated), row S16-1 (Item 1 Part A completed with full native coverage; Parts B/C and reconciliation pending), status header and §1 recording language. No requirement class was changed by the Lead.
- Recording act: this file plus one row in root `DECISIONS.md` of the control checkout `C:/CT13` (branch `feature/claude-takeover-20260913`), ordinary local commit, no push.
- What this recording does NOT do: it grants no acceptance and does not use the completion label. Class A items A-1..A-13 remain open; the Lead will present the completed Section-16 receipt and the seal chain `#36`-`#39` for the owner's own ratification words before applying any chain/schema/receipt metadata.
- Source draft preserved unchanged at `C:/tmp/CLAUDE_P0_RUN_20260913/laneP12A_amendment/P012_ACCEPTANCE_AMENDMENT_DRAFT.md` (SHA-256 1108043e33cf07ac3da6047db2d57879218bc1c8ce333dfe4c4dcfc724c3cc3a).
