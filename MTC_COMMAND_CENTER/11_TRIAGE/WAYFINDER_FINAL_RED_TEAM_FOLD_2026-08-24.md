# WAYFINDER FINAL RED-TEAM FOLD — 2026-08-24 (map #118, decided #123, folded #124)

**Status:** owner-decision record. **Planning only — implementation authorized: NO.** Per **D-12**, nothing in this document authorizes implementation, code, Pine, Bridge behaviour, host contact, credentials, schema activation, deployment, testnet, live action, ARM, DISARM, KILL, FLATTEN, trading, spending, any destructive Git operation, or the start of any work package. **No claim is made that this work is merged or accepted.** Git history is authoritative for merge status.

**Scope and classification.** Documentation and planning only — **T2**. This fold changes planning documents; it changes no product code, no configuration, no governance file, no `AGENTS.md`, no `CLAUDE.md`, no `_AI_MEMORY` onboarding file and no stage directory.

**Starting SHA.** `f77c7171fa73543364a1446042c6f272169d074d`.

**Invariants held throughout.** **60 tracked requirements = 44 OWNER (O-01 … O-44) + 16 DERIVED (D-01 … D-16)**, and **76 work packages**. **No requirement or safeguard wording, ID, count, work package, gate, tier, stage or owner decision was added, removed, reworded or renumbered.** History is preserved: every superseded statement stays where it was written and is marked as history rather than deleted. Every unratified numeric value stays **`[OPEN]` as a draft proposal**, with its qualitative obligation unchanged and binding.

---

## 1. Map and tickets

| Ticket | Role |
|---|---|
| [Final red-team decision map — "where did we reinvent a wheel, and where does the plan still contradict itself?" (#118)](https://github.com/bsemaay-tech/mtc-command-center/issues/118) | The map |
| [#119](https://github.com/bsemaay-tech/mtc-command-center/issues/119) · [#120](https://github.com/bsemaay-tech/mtc-command-center/issues/120) · [#121](https://github.com/bsemaay-tech/mtc-command-center/issues/121) · [#122](https://github.com/bsemaay-tech/mtc-command-center/issues/122) | Research inputs — reuse survey, internal-contradiction sweep, dependency and gate coherence, unratified-value audit |
| [Decide: final red-team dispositions (#123)](https://github.com/bsemaay-tech/mtc-command-center/issues/123) | The owner-resolved decision ticket. Detail lives in its resolution comment |
| [Fold: final red-team dispositions into the planning set (#124)](https://github.com/bsemaay-tech/mtc-command-center/issues/124) | This fold |

**Locked prior art.** Folds #37, #54, #67, #78, #79, #95, #96 and #97 remain binding and are not reopened. This fold repairs coherence and names reuse defaults on **existing** carriers; it becomes no new authority.

---

## 2. Dispositions — FR-01 … FR-24

Every finding below is **APPLY**. "Class" states what kind of change it is; none of them is a scope, count or decision change. **The FR identifiers below are fold-local consolidation keys; issue #123 records the same correction set in research-disposition order, so the finding text—not ordinal position—is the cross-record identity.**

| # | Finding | Disposition | File(s) and class |
|---|---|---|---|
| **FR-01** | A stale **69**-package count was still stated current-facing in several places | APPLY | Delivery plan §0; brief §0 table, R1 row and §0.7 acceptance scope; **register §0 G1 note, §1.2 R1/R2 paragraph and the O-18 row**; **owner plan companions line 69 → 76**. Class: count coherence — historical 69 retained and marked historical, current 76 stated |
| **FR-02** | "All six lanes" against a lane table that has carried **seven** since 2026-08-22 | APPLY | Delivery plan §3. Class: internal contradiction |
| **FR-03** | `WP-P0-14` still depended on `WP-P0-18` after the chart left Phase 0 | APPLY | Delivery plan §3 lane notes, WP-P0-14 inputs/depends, WP-P0-18 note. Class: dependency coherence |
| **FR-04** | Unratified map-#96 readiness numbers read as settled requirements | APPLY | Brief §2 F-16 item 7; plan WP-V2B-07 and WP-V4-01; **register D-16 adjacency; starting point §4 and §6; owner plan §5 and §6**. Class: unratified-value discipline — value `[OPEN]`, obligation binding |
| **FR-05** | Planned V2 KILL/FLATTEN semantics conflated with deployed runtime truth | APPLY | Brief §10.2a and §12.6.5 item 1; plan WP-V2B-10; **owner plan §5 V1 KILL paragraph**. Class: truth-axis separation — source vs planned vs UNVERIFIED deployed |
| **FR-06** | `WP-P0-30` consumed `WP-P0-21` checks without declaring the dependency | APPLY | Delivery plan WP-P0-30. Class: undeclared existing dependency, declared not created |
| **FR-07** | `WP-V4-01` rested on OPS/credential evidence without declaring it | APPLY | Delivery plan WP-V4-01 — WP-P0-26, WP-P0-27 (planned, unbuilt), WP-P0-29. Class: undeclared existing dependency |
| **FR-08** | Gate **G5** read "WP-V4-02 onward", which is not a list | APPLY | Delivery plan §9 G5 — membership enumerated exactly; `WP-V4-01` distinguished as the packet assembler that precedes the gate. Class: gate-coverage precision, no gate added or renumbered |
| **FR-09** | `WP-V3-05` bundled pre-live machinery with post-live acceptance evidence | APPLY | Delivery plan §7 — two named milestones under the §0 staged-milestone rule. Class: staged-milestone split, no package added |
| **FR-10** | `WP-V4-09` carried a pre-live owner duty behind a post-live dependency | APPLY | Delivery plan §8/§9 — two named milestones. Class: staged-milestone split, no package added |
| **FR-11** | The Minimum Explorer risked a custom grid beside an adopted component | APPLY | Delivery plan WP-P0-14 — **Perspective** named as the default table/grid/filter surface under WP-P0-24 governance. Class: reuse-first default |
| **FR-12** | The research report surface risked custom statistics beside an adopted library | APPLY | Delivery plan WP-V3-11 — **QuantStats** as the comparison's starting point, **independently validated** against this platform's own computation before display. Class: reuse-first default with validation duty |
| **FR-13** | The operator read model risked a second transport and a second truth store | APPLY | Delivery plan WP-V2B-03 — extend the existing `/api/snapshot`, the existing WebSocket push and the existing decision/order/fill/trade stores. **No parallel transport, no second truth store.** Class: reuse-first default |
| **FR-14** | The brief carried **two** sections numbered `§12.6`, making every cross-reference ambiguous | APPLY | Brief — safety fold keeps `§12.6`; operator fold renumbered to **`§12.7`**; pointers repaired at §12.2, §12.6.6 and the source-inventory row. Class: reference integrity, content unchanged |
| **FR-15** | A retired 2026-08-17 "Package 7" carrier name was still cited | APPLY | Brief Q6, §10.2 account binding, §17 table, DL-10 — re-pointed to **WP-P0-28 (VEN-A)**. Class: stale carrier name, owner decision unchanged |
| **FR-16** | Standing constraint 1 asserted a running V1 soak the plan has never verified | APPLY | Delivery plan §1 constraint 1 — reworded to isolation, with the deployed state UNVERIFIED. Class: unverified-claim removal |
| **FR-17** | The schema-**v4** statement read as an observation of the deployed host | APPLY | Brief §12.6.5 item 1 — qualified as a repository-evidence statement, not a host observation. Class: evidence-provenance qualifier |
| **FR-18** | `WP-P0-14` was still described as a basic/marker **chart** carrier for O-02 and O-29 | APPLY | **Register O-02 and O-29** — carrier and explanation prose only; `WP-V3-11` alone owns the trade-truth chart; `WP-P0-14` is the minimum summary and lifecycle explorer. Class: carrier prose correction, requirement text unchanged |
| **FR-19** | Four canonical rows consumed map-#96 carriers that the rows did not cite | APPLY | **Register** — O-33 adds `WP-P0-29`; D-09 adds `WP-P0-26`; D-11 adds `WP-V4-01`; D-16 adds `WP-P0-29`. Class: existing-carrier citation, requirement/safeguard text unchanged |
| **FR-20** | "Bridge V2 is about to begin" read as a start signal | APPLY | **Starting point §1** — planned, not begun; no package authorized. Class: authorization-axis correction |
| **FR-21** | O-37/O-38 read as if the macro topology question were still open | APPLY | **Starting point §3 (adjacent to O-37/O-38)** and **owner plan §8** — dated map-#97 supersession note: stage-routed monorepo through Phase 0–V3 settled, only a later conditional split remains. Class: current-planning-status note, owner outcome wording untouched |
| **FR-22** | The main dependency chain read "research-simulator rebuild → allocator" as two steps | APPLY | **Owner plan §9** — one combined canonical-simulator-plus-shared-allocator delivery (`WP-P0-20`). Class: internal contradiction with §5, no package added |
| **FR-23** | Session memory, claim and `SESSION_LOCK` hygiene across the fold sessions | APPLY | **Lead-owned, outside this document set.** Class: process; not a planning-document change and not performed here |
| **FR-24** | GitHub ticket close-out and issue hygiene for #118 … #124 | APPLY | **Lead-owned, outside this document set.** Class: process; not a planning-document change and not performed here |

---

## 3. Rejected and deferred — stated so they are not re-proposed

- **"The Lifecycle Ledger and the Explorer duplicate each other."** **False, rejected.** `WP-P0-31` is the append-only lifecycle record; `WP-P0-14` reads it. One writer, one reader — that is a seam, not a duplicate.
- **A second chart-library selection.** **Rejected.** `WP-P0-18`'s verdict is selected once and reused across trust domains. No contest is reopened.
- **The #94 prototype as a production base.** **Rejected.** It stays a disposable fake-data visual specification.
- **A second market-data collector.** **Rejected.** `WP-P0-30` (VEN-E) remains the sole execution market-data authority; no silent blend.
- **Wholesale adoption of an off-the-shelf dashboard.** **Rejected.** Reuse is named at component level — Perspective, QuantStats, the existing snapshot/WebSocket/stores — not as a platform swap.
- **Merging the original map-#95 branch.** **Not done.** That branch is **not merged**; the map-#95 operator-surface record was reconciled onto the current branch instead, and this fold makes no merge claim about either.
- **Any broad relaxation of D-12.** **Rejected.** No fold, acceptance, acknowledgement or carrier clarification supplies implementation, host, credential, deployment, testnet, live or trading authorization.
- **Memory archival and rotation policy.** **Deferred.** Not decided here and not applied here.

---

## 4. OPEN-01 — left open deliberately

**OPEN-01.** Whether the execution UI stays a **zero-build vanilla-JS** surface, or takes a **framework and a build step** in order to use optional libraries such as TanStack Table and TanStack Query.

**Recommendation, for a later decision and not a choice made here:** consider a **bounded** build step **only if** `WP-V2B-05` can measure that it results in **less custom table and freshness code**, and **only if** it weakens none of the private-access, read-only and security properties already ratified. **This is `[OPEN]`. No option is chosen, no library is adopted, and nothing is authorized.**

---

## 5. Model and evidence provenance — stated exactly, because it is a claim about a session

- **Three isolated Codex research lanes completed** and are **supplemental, read-only** input. They are not a reviewer verdict.
- **The reuse lane completed through an explicitly authorized read-only subagent**, after the **Gemini launcher failed twice before reaching a model** — first on a canonical-root restriction, then on a config-schema mismatch. Both failures were pre-model; neither produced a model opinion.
- **The Claude counterpart's first launch hit a pre-model quota limit.** A later partial run was **time-capped**, and **this one focused repair session** was used to finish the counterpart work.
- **No reviewer verdict is claimed by this fold**, from any model. Nothing here has passed an audit, and **no accepting audit verdict exists for this candidate**.

---

## 6. Lead / T2 validation checklist

1. `60 = 44 OWNER + 16 DERIVED` appears in every document that states a total; no document states another.
2. `76` is the package count wherever a count is stated current-facing; every `69` is dated and marked historical.
3. No requirement or safeguard **wording**, ID, count, package, gate, tier, stage or owner decision changed — diff the O- and D- text columns to confirm.
4. Every unratified numeric value carries `[OPEN]`, and every corresponding qualitative obligation is still stated and binding.
5. D-16's exact safeguard text and the 2026-08-23 **as written** acknowledgement are byte-unchanged; the draft-value note sits **adjacent**, never inside.
6. O-37/O-38 wording is byte-unchanged; the map-#97 status note sits **adjacent**.
7. Deployed-state statements are labelled repository evidence, never host observation; **no host was contacted**.
8. Reuse defaults name **existing adopted** components only; nothing new is adopted.
9. **Pointer note:** the map-#95 operator fold record `WAYFINDER_OPERATOR_SURFACE_FOLD_2026-08-23.md` still cites the brief's operator section as **`§12.6`**. Those pointers are **historical and are not amended** — the canonical operator section is now **`§12.7`** (brief §12.7, renumbered under FR-14). Read that record's `§12.6` pointers as `§12.7`.
10. Nothing in this fold is presented as merged, accepted, authorized or started.

---

**Materiality.** The amendments this fold records are **material** to the G1-accepted set. A **fresh G1 acceptance round** over the amended set is recommended before `G1-IA` for any package it touches. **That audit, and every implementation authorization, remain separate owner decisions. Nothing here is merged or accepted.**
