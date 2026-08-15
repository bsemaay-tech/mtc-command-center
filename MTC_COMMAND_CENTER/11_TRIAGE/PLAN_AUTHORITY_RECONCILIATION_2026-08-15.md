Status: RECONCILIATION ONLY — DECIDES NOTHING, CREATES NO AUTHORITY

# Plan Authority Reconciliation — 2026-08-15

## Scope and conclusion

This record reconciles documentary claims only. It does not select a controlling plan, close a gate, authorize an action, or alter either plan.

The conflict reported in `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_CLAIM_VERIFICATION_2026-08-15.md:74-106` is real as a **prerequisite-chain conflict**, but one part of its wording is too broad. The 50-hour plan expressly calls itself the active delivery layer and imposes an exact eleven-step sequence. The KVM2 master does not make itself the sole task authority: it assigns the ten bridge items to the lower-level deploy list and the 85 detailed task blocks to the execution companion. All three KVM2 documents also say that they grant no operational authority. Thus, the documents compete over which prerequisite chain governs the same KVM2 DISARMED deployment; they do not each independently authorize that deployment.

No sentence in either plan family says that the 50-hour sequence supersedes, replaces, absorbs, or is subordinate to KVM2 Phases 0–4. The later owner authorization selects the 50-hour programme for execution, but its express supersessions are narrowly enumerated and do not mention the KVM2 master, companion, deploy list, or Phase 0–4 chain. No owner decision record found resolves that remaining precedence question.

The current handoff repeats the 50-hour steps 3–11 and labels them the canonical sequence (`MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md:607-623`), but that handoff does not cite a sentence reconciling or retiring the KVM2 authority chain.

## 1. What each document claims

### 1.1 The 50-hour Accelerated Implementation Plan

Its self-description and scope are direct:

- It states: “Deliver a tightly scoped, safety-focused Trading System MVP: one Ubuntu KVM2 VPS installed and verified safely **DISARMED** … delivered within approximately 50 active AI engineering hours.” (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:27-33`)
- It preserves one layer and names itself as the other: “**Master Roadmap:** the existing Phase 0–7 programme (preserved in full)” and “**Active Delivery Plan:** the 50-Hour Safety MVP defined in this document.” (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:35-40`)
- Its target is one Ubuntu KVM2 runtime, TESTNET/paper-simulated only, with mainnet and real capital forbidden. (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:60-82`)
- Its in-budget endpoint is: “One Ubuntu KVM2 VPS is deployed, non-trading (DISARMED) … ready for a later separately-authorised ARM gate.” (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:86-88`)
- Section 23a says: “The following gates must be cleared in the exact order below.” It then specifies steps 1–11, ending with Audit 3/Gate 6, Gate B, separately approved WP-V, and Gate C. (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:964-980`)
- WP-V itself says owner authorization is required before it begins and that the reservation is not deployment authority. (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:880-901`)

The plan contains replacement and preservation language, but neither concerns the KVM2 plan family:

- Its revision note says it “Replaces Windows/local paper-candidate scope with Ubuntu KVM2 VPS deployed-DISARMED readiness.” This replaces the earlier endpoint of the same 50-hour plan, not the July 25 KVM2 programme. (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1-3`)
- It says the existing long-term roadmap remains valid and should not be deleted. (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:35-40`)
- Its final recommendation again says to keep the existing Master Roadmap and create a new active-delivery layer. (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1849-1856`)

The “Master Roadmap” in those sentences is identified as the existing Trading System Phase 0–7 programme, not by the title or path of the KVM2 master. The 50-hour document never names `KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md`, its execution companion, its P0–P4 IDs, or the lower-level deploy list. Therefore, there is **no cross-plan supersession or precedence sentence in the 50-hour plan**.

### 1.2 The KVM2 master, execution companion, and lower-level deploy list

The KVM2 master describes itself as preparation and governance, not execution authority:

- Its status is “**PREPARATION ONLY / EXECUTION BLOCKED**”; its scope is “end-to-end planning, task ordering, clean-rebuild preparation, evidence requirements, and owner/audit gates”; and it says it authorizes no installation, deployment, secret, network, runtime, exchange, TESTNET, ARM, reprovision, purchase, or live action. (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:36-43`)
- It says: “The lower-level bridge authority remains `…/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`” and “Nothing here duplicates, bypasses, or weakens its ten ordered bridge tasks.” (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:45-47`)
- It assigns the complete 85-task detail to the execution companion as “the sole detailed authority,” makes conflicts with that companion a BLOCK pending owner reconciliation, and says that master and companion are incomplete without each other. (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:217-237`)
- Its phase summary imposes Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4, with Phase 3 defined as bridge release readiness and Phase 4 as separately authorized deploy and cutover. (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:239-248`)

The execution companion accepts both superior sources rather than displacing them:

- It is also “**PREPARATION ONLY / EXECUTION BLOCKED**.” (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:1-6`)
- It says: “This file details 85 tasks; the Bridge VPS Deploy Task List governs its ten items. Tasks do not authorize later actions; each operational gate needs distinct owner authority. Master governance also applies.” (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:8-12`)

The lower-level list makes the bridge-specific chain controlling within that programme:

- Its scope is “durable planning and handoff only; this file grants no execution authority.” (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:3-6`)
- Its checklist is headed “complete before deploy” and says: “No item below authorizes the next item. Stop at every audit, owner, runtime, and ARM gate.” (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:84-87`)
- Item 10 requires exact-candidate audit, separate owner deploy authorization, and a still-separate ARM action. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:140-146`)
- Its safety boundary again denies merge, deployment, installation, secret, runtime, exchange, TESTNET, ARM, and mainnet authority. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:148-157`)

The KVM2 master uses “Superseded” only for old audit inputs of that same artifact. (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:9-33`) It contains no sentence superseding or subordinating itself to the later 50-hour plan. The companion and deploy list also contain none. Therefore, there is **no cross-plan supersession or precedence sentence in the KVM2 plan family**.

## 2. Dates, lineage, and owner decisions

### Documentary and Git lineage

| Record | Documentary date | Frozen-history fact | Consequence for precedence |
|---|---|---|---|
| KVM2 master | 2026-07-25; Cycle-4/R1 repair 2026-07-26 (`KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:1-8`) | Current master and companion bytes originate at commit `01269f56`, 2026-07-26. | Earlier than the 50-hour revision. |
| KVM2 execution companion | 2026-07-25; Cycle-4/R1 repair 2026-07-26 (`KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:1-6`) | Same `01269f56` lineage. | Earlier than the 50-hour revision. |
| Lower-level deploy list | 2026-07-25; updated 2026-07-26 (`BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:1-6`) | Current bytes blame to `6fe0130f`, 2026-07-26. They entered the merged July 31 history through merge lineage, but the substantive revision predates July 30. | Not a substantive post-50-hour amendment. |
| 50-hour plan | Plan revision 2026-07-30 (`TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1-3`) | Added as the accepted 1,879-line plan at `4462cad9`, 2026-07-31 08:22 +03:00. | It is the later substantive plan. |

No candidate plan was substantively amended after the other was written: the current KVM2 programme bytes are dated/repaired July 25–26, and the current 50-hour plan is the July 30 revision. A later merge date for an already-authored lower-level file is not a later reconciliation amendment.

Later owner records amended audit roster/tier/cadence rules and pre-granted particular owner clicks, but they did not amend either document with cross-plan precedence language. The 50-hour plan itself is recorded as frozen and not edited when the audit-roster decision changed (`MTC_COMMAND_CENTER/_AI_MEMORY/DECISIONS.md:9`).

There is a separate, stale intra-KVM2 status conflict. The master still says that three PR #25 contract files are absent and Phase 3 is blocked (`KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:256-261`), while the later lower-level snapshot says PR #25 is merged, the files are present, and that old blocker is closed (`BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:29-47`). At frozen SHA `4f367ce1`, all three files also exist in the local `refs/remotes/origin/master` object. This does not resolve plan precedence; it means a KVM2-own-programme reading still needs its dated facts reconciled before claiming Phase 3 readiness.

### Owner decision record

The owner record creates strong evidence for each side, but no express selection **between** them:

- D021, dated July 25, selects the KVM2 lifecycle and says the Bridge VPS Deploy Task List “remains authoritative/BLOCKED until repaired, independently accepted, and separately authorized.” (`MTC_COMMAND_CENTER/_AI_MEMORY/DECISIONS.md:22`)
- The July 31 owner authorization says: “I approve the 50-Hour DISARMED Safety MVP plan and authorize you to begin immediately and execute it autonomously from WP-0 through completion.” (`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md:16-20`) It expressly includes KVM2 deployment and Gate A/B/WP-V/Gate C after their documented prerequisites pass. (`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md:24-47`)
- That authorization identifies exactly where it supersedes the plan: it pre-grants three future owner approvals while preserving every objective Gate A/B/C prerequisite. (`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md:51-59`) It also says its actor override “explicitly supersedes only” the plan's actor assignment. (`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md:63-70`)
- D024 and D025 change KVM2/50-hour audit-model rules only; D025 expressly says its supersession is “for audit authority only.” (`MTC_COMMAND_CENTER/_AI_MEMORY/DECISIONS.md:9-11`)
- D028 and the August 9 owner record change audit tiers, cadence, and the 50-hour ledger, while preserving separate authorization for WP-V and KVM2 deployment. (`MTC_COMMAND_CENTER/_AI_MEMORY/DECISIONS.md:3`; `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISION_AUDIT_TIERS_2026-08-09.md:83-88`)

Accordingly, the later owner record does pick the 50-hour plan as an approved programme to execute, but **no owner decision says that this approval retires, waives, absorbs, or outranks D021 and the KVM2 Phase 0–4/lower-level prerequisites**. It is not honest to turn practical use of the later programme into an unstated supersession sentence.

## 3. Overlap map

Classification used below:

- **Identical**: the same action, evidence, authority, and ordering requirement.
- **Compatible**: the work can potentially be shared, but one record must explicitly show that the same frozen artifact/evidence closes both differently named gates.
- **Genuinely different**: one plan adds a materially different action, authority boundary, evidence requirement, or ordering constraint; it cannot be inferred closed by the other.

Table citation aliases are file:line references: `EXECUTION_TASKS` = `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`; `BRIDGE_VPS_DEPLOY_TASK_LIST` = `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`; `50-HOUR PLAN` = `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md`.

No mapped unit is fully identical. The plans repeatedly pursue the same safety objective, but they package, order, and authorize it differently.

| Overlapping unit | KVM2 task IDs / lower item | 50-hour §23a step | Relationship | Why |
|---|---|---:|---|---|
| Governance, lifecycle, and baseline freeze | P0-01/P0-01B/P0-02/P0-03; P1-01→P1-03 | Before step 1 (WP-0/WP-S) and step 2 Gate A | **Genuinely different** | KVM2 requires owner lifecycle, audit-roster reconciliation, live-state verification, a KVM2 host baseline, and owner baseline acceptance (`EXECUTION_TASKS:20-90`). WP-0 freezes the 50-hour scope/baseline and Gate A reviews non-executed readiness (`50-HOUR PLAN:637-654,988-1006`); it does not close the KVM2 P0/P1 decisions. |
| Pre-Ubuntu execution boundary | P2-09/P2-12, then P3-01 | Step 2 Gate A, then step 3 | **Genuinely different** | KVM2 makes an expendable Ubuntu rehearsal part of Phase 2 before owner Phase-2 close (`EXECUTION_TASKS:158-192`). The 50-hour plan forbids any Ubuntu execution before Gate A and allows one named expendable action only afterward (`50-HOUR PLAN:971-975,988-1006`). A cumulative sequence must place KVM2's rehearsal after Gate A; neither document says that explicitly. |
| Immutable release candidate and provenance | P3-02/P3-04; lower items 1–2 | Step 2 candidate readiness; step 7 final freeze; step 8 audit | **Compatible** | Both require exact SHA, locked dependencies, artifact identity, and independent verification (`EXECUTION_TASKS:208-236`; `BRIDGE_VPS_DEPLOY_TASK_LIST:89-105`; `50-HOUR PLAN:994-1004,976-977`). The 50-hour chain has an early candidate and a later post-WP-A final freeze; KVM2 has one P3 candidate flowing toward P4. Explicit dual binding is required. |
| Exact-candidate Ubuntu staging tests | P3-03/P3-04; lower items 3, 5, 9 | Steps 3–5 | **Compatible** | Both use a non-production Ubuntu environment and require systemd/state/reconciliation evidence (`EXECUTION_TASKS:220-236`; `BRIDGE_VPS_DEPLOY_TASK_LIST:100-105,110-114,133-139`; `50-HOUR PLAN:972-975`). KVM2 adds WAL/foreign-position/corruption cases; the 50-hour plan adds the retained-host WP-A invariant overlay after Audit 2. |
| Pre-deploy canonical audit | P3-05; lower items 1 and 10 | Step 4 Audit 2 and especially step 8 Audit 3 + Gate 6 | **Compatible** | Both require fresh independent acceptance before production work (`EXECUTION_TASKS:237-246`; `BRIDGE_VPS_DEPLOY_TASK_LIST:89-94,140-146`; `50-HOUR PLAN:973,976-978`). KVM2 P3-05 closes its crosswalk and candidate contract; step 8 closes the final post-WP-A artifact/evidence package. One audit can count for both only if its frozen scope and verdict expressly close both contracts. |
| Service identity, filesystem, systemd, and private listener | P2-03/P2-04, P3-02/P3-03, P4-02; lower items 3 and 7 | Steps 2–5 and step 10 | **Compatible** | Both require dedicated/controlled paths, hardened service behavior, loopback-only control, and Ubuntu proof (`EXECUTION_TASKS:114-130,208-230,278-284`; `BRIDGE_VPS_DEPLOY_TASK_LIST:100-105,122-126`; `50-HOUR PLAN:743-776,990-1004,1015-1025,890-897`). KVM2 separates masked installation from first start; WP-V bundles installation and DISARMED verification. |
| TESTNET secret inventory and provisioning | P2-05/P4-03; lower item 4 | No explicit §23a step; would have to occur around step 10 | **Genuinely different** | KVM2 requires a separate secret contract and a separate owner provisioning action, with `HL_LIVE_ACK` absent (`EXECUTION_TASKS:131-135,285-293`). The 50-hour sequence requires secret scans and a TESTNET-only endpoint but does not create an equivalent separately numbered secret-provisioning gate (`50-HOUR PLAN:997-1004,1036-1044`). |
| Risk-state continuity policy and final state transfer/reset | P2-06, P3-01/P3-03, P4-05; lower item 5 | Steps 3, 5, and 10 | **Genuinely different** | The KVM2 chain requires an owner choice between WAL-consistent migration and conservative reset, adversarial staging tests, final post-quiesce capture, semantic checks, and source/destination hashes (`EXECUTION_TASKS:136-146,202-230,313-330`). The 50-hour chain proves SQLite backup/restore and DISARMED invariants but does not impose that complete cutover-state protocol (`50-HOUR PLAN:743-775,779-830,890-897`). |
| Install/deploy authorization and bounded install | P4-01/P4-02; lower item 10 | Step 9 Gate B, separate WP-V approval, step 10 | **Compatible** | Both require owner authority after accepted evidence and before production installation (`EXECUTION_TASKS:265-284`; `BRIDGE_VPS_DEPLOY_TASK_LIST:140-146`; `50-HOUR PLAN:978-980,1010-1028`). KVM2 makes install/configure-only a one-attempt action with the service masked and excludes secrets, cutover, and start; the 50-hour plan packages these inside WP-V. |
| Old-writer quiesce and ordered single-writer cutover | P4-04/P4-04A/P4-05; lower item 6 | Steps 9–10 | **Genuinely different** | KVM2 requires tabletop abort rehearsal, a distinct Windows-writer quiesce sentence, two exchange-flat proofs around authority revocation, and ordered state transfer (`EXECUTION_TASKS:294-330`; `BRIDGE_VPS_DEPLOY_TASK_LIST:115-121`). WP-V requires DISARMED/no positions/reconciliation but does not reproduce this ordered authority-transfer gate (`50-HOUR PLAN:890-897,1032-1044`). |
| First DISARMED start | P4-06/P4-07; lower items 6 and 9 | Step 10 WP-V | **Compatible** | Both require DISARMED, TESTNET-only, loopback-only, exact-artifact start and reconciliation (`EXECUTION_TASKS:331-348`; `BRIDGE_VPS_DEPLOY_TASK_LIST:115-121,133-139`; `50-HOUR PLAN:890-905`). KVM2 additionally requires a separately authorized single attempt, zero restart count, log rotation proof, and loading the exact P4-05 destination-state hash. |
| Reboot/maintenance proof | P2-10/P4-07A | Step 10 and step 11 Gate C | **Compatible** | Both require a DISARMED restart/reboot and reconciliation (`EXECUTION_TASKS:168-177,349-356`; `50-HOUR PLAN:890-897,1036-1044`). KVM2 makes the maintenance drill a separately authorized exact-candidate action with pre/post hashes. |
| Rollback and recovery start | P2-06/P4-08/P4-08A/P4-08B; lower item 8 | Step 10 and step 11 | **Genuinely different** | Both require tested rollback and preserved state (`EXECUTION_TASKS:136-146,357-377`; `BRIDGE_VPS_DEPLOY_TASK_LIST:127-132`; `50-HOUR PLAN:890-905,1036-1044`). KVM2 additionally requires a stopped/disabled zero-writer rollback target and separate one-attempt authority/evidence for a post-rollback recovery start. |

## 4. Consequences of the two readings

### Scenario A — cumulative: every gate in both plans is required

The combined order is a partial order because neither document supplies a crosswalk. The narrowest dependency-respecting total order is:

1. Complete 50-hour WP-0 and WP-S, and close §23a step 1 Audit 1. KVM2 non-operational Phase-0 preparation may be cross-referenced, but no KVM2 phase is deemed closed merely by WP-0.
2. Complete 50-hour WP-L Phase 1 and WP-I non-executed readiness, then close step 2 Gate A.
3. After Gate A, close any still-open KVM2 Phase 0 facts/owner decisions, Phase 1 baseline/owner acceptance, and Phase 2. KVM2 P2-09 Ubuntu rehearsal must occur only now and must be expressly included within the one named Gate-A staging action (or be covered by a new owner reconciliation); otherwise it either violates the pre-Gate-A Ubuntu prohibition or silently adds a second staging action. P2-12 then closes Phase 2.
4. Run KVM2 P3-01 → P3-02 → P3-03 → P3-04 while performing the 50-hour step 3 retained-host staging action. The record must bind the same exact candidate and evidence to both plans.
5. Close 50-hour step 4 Audit 2, then step 5 WP-A, step 6 staging-host discard, and step 7 final exact SHA/artifact freeze.
6. Close both KVM2 P3-05 and 50-hour step 8 Audit 3 + Gate 6. They may use one audit package only if it expressly covers both contracts on the same final artifact; otherwise both accepting gates are required.
7. Close 50-hour step 9 Gate B, its WP-V approval requirement, and KVM2 P4-01 install/configuration authority without treating any one sentence as the others unless it explicitly names all of them.
8. Execute step 10 WP-V through KVM2's stricter Phase-4 order: P4-02 install masked/disabled → P4-03 secret action → P4-04 tabletop → P4-04A writer quiesce → P4-05 cutover/state proof → P4-06 first-start authority → P4-07 one DISARMED start → P4-07A maintenance/reboot drill → P4-08 rollback → P4-08A/P4-08B recovery start.
9. Close 50-hour step 11 Gate C only after every required Phase-4 result is captured.

Potentially duplicated work: candidate manifests and hashes, dependency/service artifacts, expendable-Ubuntu tests, independent candidate review, Gate 5/Gate 6 coverage, DISARMED first-start evidence, reboot/reconciliation, and rollback. These are duplicate objectives, not automatically duplicate executions: a single artifact or test run can close both only through an explicit dual crosswalk and accepting verdict.

Genuinely distinct work retained by the cumulative reading includes KVM2 lifecycle/baseline/rebuild-kit gates, the owner-selected state policy, separate secret action, old-writer quiesce, ordered cutover and state hashes, single-attempt first-start/recovery authorities, plus the 50-hour plan's WP-S S2/S3 closure, pre-Gate-A Ubuntu prohibition, Audit 2 before WP-A, retained-host WP-A overlay, post-WP-A final freeze/Audit 3, Gate B evidence bundle, and Gate C owner acceptance.

**Cost:** this reading carries both documentation systems, both closure records, the broad KVM2 Phase 0–2 preparation programme, and possibly two audits where a safe dual-scope audit cannot be formed. It adds owner-decision and elapsed-time overhead, and the repository provides no reliable combined-hour total.

**Risk:** its principal risk is false deduplication—claiming that similarly named evidence closes both contracts when the artifact, scope, order, or owner sentence differs. It also exposes the un-reconciled P2-09-versus-Gate-A sequencing issue and the stale Phase-3 blocker text; both must be resolved in the record before execution.

### Scenario B — KVM2 as its own programme

Under this reading, the required route is the KVM2 master/companion dependency chain and all ten lower-level bridge items:

1. Phase 0 P0-01, P0-01B, P0-02, P0-03, P0-04, P0-04A, and P0-05, including separate owner lifecycle and audit-roster decisions and authorized artifact/ledger work.
2. Phase 1 P1-01 through P1-03, ending in owner baseline acceptance.
3. Phase 2 P2-01 through P2-12, including the clean-rebuild package, expendable-environment reproducibility verdict, recovery/maintenance/incident contracts, and owner Phase-2 acceptance.
4. Phase 3 P3-01 through P3-05, ending in exact-candidate staging evidence, independent verification, canonical audit closure, and closure of lower-level items 1, 2, 3, and 5.
5. Phase 4 P4-01 through P4-08B in their stated order, with separate install, secret, quiesce, cutover, first-start, maintenance, rollback, and recovery-start authority/evidence. Lower-level items 1–10 remain mandatory and no item authorizes the next.

This route keeps substantial protections that the 50-hour plan does not spell out: the two-profile rebuild design, secret-specific owner gate, exact old-writer revocation sequence, raw pre/post flat proofs, final WAL-consistent state hash transfer or accepted reset, single-attempt first start, and separately authorized recovery start.

What it loses from the 50-hour chain is equally concrete: mandatory WP-S S2 closure and minimum S3 before Linux work; step 1 Audit 1; the step 2 rule that no Ubuntu execution may precede Gate A; the one retained staging-host lifecycle; step 4 Audit 2 specifically before WP-A; the step 5 WP-A invariant overlay; step 6 evidence-conditioned host discard; step 7 post-WP-A final freeze; step 8 Audit 3/Gate 6 on that final artifact plus the WP-A evidence package; the Gate B checklist and Case-1/Case-2 post-audit invalidation rule; and Gate C owner verification. Those protections cannot be silently imported after choosing an own-programme reading, because importing them is the cumulative reading.

**Cost:** this reading avoids running the whole 50-hour work-package chain as a second programme, but KVM2 Phases 0–2 are themselves broad and include future AI-lab/clean-mainnet preparation beyond the narrow DISARMED deployment endpoint. It therefore is not inherently the cheaper reading, and no reconciled budget exists.

**Risk:** it can reach Phase 4 without the 50-hour plan's S2/S3, WP-A, final post-WP-A freeze/audit, and Gate B/C protections. It also relies on a KVM2 master/companion whose Phase-3 blocker text is stale relative to the lower-level list and frozen local remote-tracking objects. Treating the later 50-hour owner authorization as irrelevant would also leave two owner records unreconciled rather than explain their coexistence.

## 5. Narrowest safe interim rule

Until Barış ratifies one reading, a Lead may perform only already-authorized read-only repository analysis and non-host/local preparation that crosses no gate in either plan; no phase or gate may be claimed closed, and no Ubuntu/host, install, secret, cutover, first-start, deploy, or other operational action may proceed unless the union of both plans' prerequisites and the action-specific owner authority are explicitly evidenced.

## Owner decision block

**Cumulative option:** “I ratify the cumulative reading: the 50-hour §23a sequence and KVM2 Phases 0–4 plus all ten Bridge VPS Deploy Task List items are jointly mandatory, and one artifact, test, audit, or owner sentence may close gates in both only when its record explicitly names and satisfies both contracts.”

**KVM2-as-own-programme option:** “I ratify the KVM2-as-own-programme reading: for bridge deployment the KVM2 master, execution companion, and ten-item Bridge VPS Deploy Task List govern through Phase 4, and the 50-hour §23a chain is not an additional prerequisite unless I separately import a named requirement from it.”
