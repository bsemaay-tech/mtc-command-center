# WP-P0-12 — ratification request for builder re-seals #36–#39 (concrete, ready for the owner's words)

Prepared by the Claude Lead, 2026-09-13 17:25Z. Scope basis: `OD-20260913-P012-SCOPE-1` (research/engineering acceptance scope; production admission remains pending). This document asks for exactly one owner act and nothing else.

## 1. The one act requested

Ratify the Section-16 six-item semantic coverage review of fixed candidate G5 and, with it, builder re-seals #36–#39, extending the ratified chain from 33 entries (#5…#35) to 37 entries (#5…#39).

| Re-seal | Old EXPECTED_SEAL_SHA | New EXPECTED_SEAL_SHA | Actor / reason (from the anchor's `reseal_history`) | Date |
|---|---|---|---|---|
| #36 | `6f44d5be…5dadd8` | `ab91a091…93bcf` | Claude Opus 5 Lane D4 bounded builder: probe / dependent-identity re-derivation after Path D candidate `f7d5adca` changed core | 2026-09-12T13:22Z |
| #37 | `ab91a091…93bcf` | `2405a7d3…88906` | Sol xhigh tooling integrated by Codex Lead: repair 3 probe regeneration (C3 `e1e5484d`) | 2026-09-12T17:52Z |
| #38 | `2405a7d3…88906` | `0e497b7c…ec9cc` | P012 Lead with inspected Sol repair-4 tooling: repair 4 probe regeneration (C4 `e1fdc72e`) | 2026-09-12T19:34Z |
| #39 | `0e497b7c…ec9cc` | `00e66d9e…79cb9` | Codex Lead with verified Sol repair-5 tooling: repair 5 probe regeneration (C5 `c343a281`) | 2026-09-12T22:13Z |

Candidate G5 `6d6a450232c81c4c13d63c9a4e06ce3b1bf4f889`; core tree `4698e71659d678f50e549e328e78d25816fa16fe`; current seal `00e66d9eb3517eb6bf0cb4672a22d19b58715b1b00afb4d91ffe0a4000979cb9` (#39); implementation base after repair 5 `947fe113e33b0771017cede1e9aa4056bb45ad30`.

## 2. What was reviewed and by whom (all evidence on disk)

Reviewer: `gemini-3.8-flash-high` (Google Antigravity CLI 1.1.27) through the read-only helper, native file reads only, on the frozen packet `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY` (961 base members, manifest `e8f76ca8…`, unchanged; additive companion views and staged part reports only). Reviewer family is neither Codex (kernel implementer) nor Claude (contract-table author).

| Item | Terminal reviewer disposition | Calls | Lead reproduction / audit |
|---|---|---|---|
| 1 formulas, tables, author, anchor | ACCEPTED_WITH_RESIDUAL_RISK, UNCHANGED | Parts A (39/39 EQUAL), B_R2 (43/43 EQUAL), C, reconciliation 03dc0f89 | every required file natively read; display-window continuations verified by the Lead |
| 2 all 218 kernel hunks | ACCEPTED_WITH_RESIDUAL_RISK, UNCHANGED | B1 (136 hunks), B2 (1), B3 (81), all SECTION18_SHARED | per-hunk classes cross-checked against HUNK_INVENTORY: 218/218, 0 errors |
| 3 scenario boundaries | ACCEPTED_WITH_RESIDUAL_RISK, UNCHANGED | C3_CATALOG (17 goldens, catalog companion 2402 lines) | companion views round-trip verified |
| 4 production lineage | ACCEPTED_WITH_RESIDUAL_RISK, UNCHANGED | A2_ITEM4 (call 19c0baa8) | records complete; venue values Lead-verified |
| 5 cross-module / external consumers | ACCEPTED_WITH_RESIDUAL_RISK, UNCHANGED | five slices (core, Bridge, mtc tests, MCC-A, MCC-B) + reconciliation 3d9e4dce | Lead coverage ledger: 65/65 census files + full current core; 10/10 spot checks EQUAL |
| 6 event / schema consumers | ACCEPTED_WITH_RESIDUAL_RISK, UNCHANGED | same five slices + reconciliation | no missing consumer, overwrite, duplicate identity or dropped member reported |

Every accepted call carries `LEAD_ADJUDICATION.md` under `C:/tmp/P012_S16_REVIEWS_20260913/<call>/` with the conversation id, native-read audit and citation-checker result (all REPORT ACCEPTED). Refused or failed attempts are preserved beside them (C_CATALOG_CONSUMERS refused for invented citations; quota/guard aborts archived under FAILED_ATTEMPTS/).

## 3. The receipt and the checks it already passed

- Assembled receipt (unratified): `C:/tmp/CLAUDE_P0_RUN_20260913/RECEIPT_INPUTS/semantic_coverage_review_G5_UNRATIFIED.json`, SHA-256 `eb021465cf12c6ce8860dbef3e64a6b7f7ea7477c1e5fa5b889d9969e8d9db24`, schema `P012_SEMANTIC_COVERAGE_REVIEW_V2`, `owner_ratification.ratified = false`, `signed_at` placeholder. Built only from reviewer-owned envelopes by `assemble_receipt.py` (it assigns no semantic class itself).
- 155 evidence paths, all present in the packet; 104 packet-tree citations resolve; no line citation exceeds its file (citation checker REPORT ACCEPTED).
- JSON-schema validation against the verified schema patch: the only error is `ratified: True was expected` — the owner act.
- **Scratch gate dry-run (simulation of the post-ratification state, 17:19Z):** in a detached scratch worktree at G5 (deleted afterwards; the P012 worktree untouched) with the two verified patches applied (`VERIFIED_JSON_SCHEMA_ONLY.patch`, `UNAPPLIED_MARKDOWN_CHAIN.patch`; `git apply` clean) and the receipt with `ratified=true` and a dry-run timestamp: full gate exit 0, `claim_label = BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_ACCEPTED`, 0 refusals, 0 acceptance blockers, 656 gate self-tests + 706 contract self-tests passed, seal `00e66d9e…` (#39), declared-field validation REPORT_ONLY unchanged (owner ruling HIST-2026-0030). Record: `C:/tmp/CLAUDE_P0_RUN_20260913/GATE_DRYRUN/gate_DRYRUN_PASS_17-19Z.json` (sha256 `f06d47bc…`). The dry-run receipt was discarded with the worktree; it is not an attestation.

## 4. What ratification does NOT do

No production admission, no venue fact, no trading, deployment, host, credential, spend, push, PR or merge authority. All 10 Section-19 OPEN rows, the 27 signed risks, the five residual obligations, N=3 fills, funding M, the first-authenticated-fill fee boundary, the forward funding interval ≥ 2026-09-12T11:00Z and the experienced-human money gate stay open exactly as recorded in `P012_ACCEPTANCE_AMENDMENT_20260913.md`. Reviewer residuals carried into the receipt notes: implementer-family mechanical re-pins at #22/#26; economics.py verified within lines 1-300 for the Item-4 seam; legacy optimizer rows and parity comparators bind gross PnL without fee/funding cashflows (design section 17 limits L4/L5, deliberate segregation).

## 5. The exact words needed

Reply with one line, for example: `I ratify the Section-16 six-item review of G5 6d6a4502 and builder re-seals #36–#39 (chain #5…#39), 2026-09-13.` Add "with signed_at <UTC timestamp>" if you want a specific timestamp; otherwise the Lead stamps the receipt with the UTC time of your message.

## 6. What the Lead does after your words (and only then)

In `C:/tmp/P012_PATHD_20260912` only: apply the two verified patches, write the receipt with `ratified=true` and your `signed_at`, re-run the full gate and the contract self-tests, re-hash the three production records to prove no refusal changed, commit on the candidate branch with the required trailer, and report "P0-12 research/engineering scope complete; production admission pending." No push, PR or merge without a separate instruction.
