# W12 cross-document adversarial meta-review

## Verdict

**NOT INTERNALLY CONSISTENT AS A CURRENT-STATE PACKET.** The substantive execution boundaries are generally conservative, but several same-day status artifacts still present pre-decision states as current after the owner explicitly authorized Pathscope Option C, approved the narrow host-and-credential sentence, signed the approximately 63.75-hour ledger snapshot, deferred the wallet, and selected a fresh reset. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:8-28`, `:30-78`, `:80-96`.

The safe precedence rule is: use the night owner-decision record for those five decisions; treat earlier same-day consolidation, readiness, measurement, and handoff statements as historical snapshots wherever they conflict. The owner-decision record itself says the remaining owner questions are plan authority and the risk-state archive sub-question. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:118-131`.

## Findings

### F1 — HIGH — The “final authority consolidation” has a superseded current-blocker list

**Earlier/current-looking statement:** the consolidation says, “No option is currently exercised,” says the exact host-and-credential confirmation is still required, and calls approximately 63.75 hours “measurement-only, not ratified.” `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:93-97`. Its closing summary repeats those three items as “current owner-decision blockers.” `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:115-122`.

**Conflicting controlling statement:** the owner record says “Pathscope: **Option C authorized**,” authorizes the redesign and one fresh flagship audit, and forbids an open-ended cycle. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:8-28`. It separately says the narrow host-and-credential confirmation is “**approved**,” although not spendable until the named preregistration and allocation artifacts exist. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-58`. It also says the approximately 63.75-hour figure is “**signed**” as of 2026-08-15 and must be re-presented if it drifts by the real freeze. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:62-78`.

**Adversarial assessment:** a reader following the file titled “final authority consolidation” as the latest status would ask the owner to decide three matters already decided and would misstate an approved-but-preconditioned grant as absent. This does not create unsafe extra authority; it corrupts the authority ledger by rolling it backward. Required reconciliation: place an explicit supersession banner on the consolidation’s section 3 and closing blocker list, pointing to D1–D3, while retaining the consolidation as the authority-content source for the exact sentence boundaries. The host grant must remain unspendable until Commit 1 and the allocation record exist. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:40-52`.

### F2 — HIGH — The deploy-readiness refresh recommends the opposite risk-state policy from the owner’s decision

**Earlier/current-looking statement:** the readiness refresh labels risk-state continuity `NEEDS-OWNER`, says “No later owner selection was found,” and supplies the sentence “I select WAL-consistent migration ...; fresh-database reset is not approved.” `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:175-193`.

**Conflicting controlling statement:** the owner says “start clean,” explicitly selects a fresh-database reset rather than WAL-consistent migration, and records this as a deliberate override of the recommendation. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:89-107`.

**Adversarial assessment:** following the readiness refresh’s proposed owner sentence would now reverse the actual owner choice on a safety-sensitive state boundary. Required reconciliation: mark readiness item 5 superseded by D5 and replace its “choice open” status with “fresh reset selected; fail-closed preservation/blocking proof still required.” The archive location is **UNKNOWN**: D5 leaves open whether pre-cutover risk state must be archived off-host or may remain on the old machine; an explicit owner sentence settles it. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:98-116`.

The same readiness refresh also labels the KVM2 TESTNET wallet `NEEDS-OWNER` and describes the required secret artifact. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:158-173`. The later owner record defers it and says no wallet may be requested, provisioned, generated, stored, or referenced yet. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:80-87`. That is a stale status rather than a direct technical contradiction, but it belongs in the same supersession banner.

### F3 — MEDIUM — Packet 10 and the dashboard overstate a byte-condition as an operating-system guarantee

**Overbroad statements:** Packet 10 says, “This test fails on every Windows checkout and passes on Linux — including on the Ubuntu 24.04 deploy target.” `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:91-104`. The dashboard compresses this further to, “One fails only on Windows and will pass on the server.” `MTC_COMMAND_CENTER/11_TRIAGE/dashboard_2026-08-15.html:259`.

**Contrary narrower evidence:** the adversarial verification says the failure is caused by CRLF materialization versus the LF hash; “Windows-only” is not an OS invariant, and no future exact deploy-target run is established. `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_CLAIM_VERIFICATION_2026-08-15.md:140-166`. It states that a Windows checkout with LF bytes can pass and a Linux worktree with CRLF can fail. `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_CLAIM_VERIFICATION_2026-08-15.md:184-192`.

**Adversarial assessment:** the mechanism is supported, but the platform guarantee is not. The actual result on the future release SHA and KVM2 target is **UNKNOWN**. It is settled only by materializing the exact frozen candidate through the intended package path and running the locked test on the exact target; the verification record enumerates the byte, identity, packaging, path-resolution, and runtime conditions that must hold. `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_CLAIM_VERIFICATION_2026-08-15.md:184-192`.

### F4 — MEDIUM — The copy-paste new-chat handoff preserves a transport-BLOCK state that was superseded by an executed audit

**Stale handoff statement:** the copy-paste prompt says the final Pathscope audit was “transport-BLOCKED” and the dashboard row says the auditor could not execute because the sandbox became read-only. `MTC_COMMAND_CENTER/11_TRIAGE/NEW_CHAT_HANDOFF_2026-08-15_AFTER_RP7_ACCEPTANCE.md:3-7`, `:11-20`.

**Conflicting execution record:** the owner-boundary record says the retry actually executed under `sandbox: danger-full-access`, reproduced all four artifact identities, and returned `REQUEST_CHANGES` with three required findings. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OWNER_BOUNDARY_2026-08-15.md:17-29`. The full retry transcript closes with the same three defects, no additional cycle, and the lane stopped at the owner boundary. `MTC_COMMAND_CENTER/11_TRIAGE/PATHSCOPE_RETRY_CODEX_RUN_2026-08-15.log:16057-16092`.

**Adversarial assessment:** this is operationally dangerous as a handoff because its explicit purpose is to seed a new session with a false causal history. Required reconciliation: mark the handoff superseded and point to the retry audit plus the later D1 decision. The current state is not transport-BLOCKED and not merely awaiting a choice: Option C is authorized and Audit-2 gate 2 remains open until the Option-C audit accepts. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:118-125`.

### F5 — LOW — The dashboard contradicts itself about what the work-package freeze is waiting for

**First dashboard statement:** “Rebuild underway”; the owner chose the full redesign, after which code and one independent review are required. `MTC_COMMAND_CENTER/11_TRIAGE/dashboard_2026-08-15.html:250`.

**Conflicting adjacent statement:** “Work package frozen” is blocked because it “Waits on the safety-checker decision.” `MTC_COMMAND_CENTER/11_TRIAGE/dashboard_2026-08-15.html:252`.

**Controlling decision:** Option C has already been authorized, with one redesign and one fresh flagship execution audit. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:8-23`.

**Adversarial assessment:** the intended blocker is the redesign and accepting audit, not the already-made decision. The adjacent correct row limits the damage, so severity is low, but the wording should be changed before the dashboard is used as a status authority.

### F6 — LOW — A known-stale line citation remains live in the body of the deploy synthesis

**Stale citation:** the synthesis body still says `GLOBAL_HANDOFF.md:544-549` records the canonical sequence. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_PATH_SYNTHESIS_2026-08-15.md:56-60`.

**Correction in the same file:** the correction says the reference should be `GLOBAL_HANDOFF.md:617-620`, not `:544-549`, because the earlier numbers shifted. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_PATH_SYNTHESIS_2026-08-15.md:35-38`.

**Adversarial assessment:** the correction prevents a substantive misreading, but leaving the invalid locator in the operative body invites copy-forward errors. Replace the body locator or label it inline as historical.

## Required review axes with no additional finding

### Withdrawn 55–105-hour estimate

No current reliance on the withdrawn 55–105-hour total was found. Its original table remains visible in the synthesis, but a prominent correction calls it refuted, says no corrected total can be recovered, and says not to budget against it. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_PATH_SYNTHESIS_2026-08-15.md:3-21`, `:123-152`. The replacement work breakdown explicitly says the withdrawn total is not used, derives a disjoint Option-C sourced subtotal of 41.5–77.5 hours, and refuses a grand total because essential rows have `NO SOURCED ESTIMATE`. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:161-198`. The dashboard likewise calls 41.5–77.5 a sourced partial floor and says fourteen necessary jobs remain unpriced. `MTC_COMMAND_CENTER/11_TRIAGE/dashboard_2026-08-15.html:273-290`.

Therefore the full remaining-work total is **UNKNOWN / NO SOURCED ESTIMATE**. It is settled only after the fourteen unpriced work units receive disjoint, source-backed estimates; inventing a grand total now would contradict the work breakdown’s explicit boundary. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:196-198`.

### Circular sourcing

No circular authority or estimate proof was found. The only conspicuous two-way Pathscope cross-reference is navigational: the decision-options record says to read it with the owner-boundary record, while the owner-boundary record points back to the options as the decision menu and explicitly exercises no option. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_DECISION_OPTIONS_2026-08-15.md:3-7`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OWNER_BOUNDARY_2026-08-15.md:59-69`. The factual execution result is independently stated in the owner-boundary record and the full retry transcript. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OWNER_BOUNDARY_2026-08-15.md:17-29`; `MTC_COMMAND_CENTER/11_TRIAGE/PATHSCOPE_RETRY_CODEX_RUN_2026-08-15.log:16057-16092`.

### Scope creep: authorization, acceptance, and closure

No unsupported expansion from planning into merge, deployment, host, or acceptance authority was found in the release design/runbook. The integration design labels itself “DESIGN ONLY — NO CODE, NO MERGE, NO ACCEPTANCE” and says it grants none of the future T0 authority. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:1-9`, `:25-30`. The merge runbook ends by forbidding push, further merge, artifact build, host contact, and acceptance claims, and says the future candidate still requires separate T0 process and fresh Gate-A execution. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:780-783`, `:824-833`.

The night owner decision also keeps the new host grant narrowly preconditioned and expressly excludes KVM2 production, writes, other credential use, broker/exchange contact, ARM, orders, TESTNET/mainnet execution, deployment, and merge to master. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:40-60`. The cross-document defect is stale status propagation, not silent authorization expansion.

## Fragile but currently consistent boundaries

- **Packet 11 signature semantics:** the approximately 63.75-hour snapshot is ratified as of 2026-08-15, but it is not a promise that the freeze-time number will remain unchanged; a different real-freeze figure must be re-presented. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:62-78`. The dashboard currently preserves that distinction. `MTC_COMMAND_CENTER/11_TRIAGE/dashboard_2026-08-15.html:253-255`.
- **Plan precedence:** the owner record still lists plan authority as outstanding, and the reconciliation offers two mutually exclusive owner sentences rather than selecting one. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:129-131`; `MTC_COMMAND_CENTER/11_TRIAGE/PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:158-166`. Until selected, the safe interim rule permits only already-authorized read-only analysis and local preparation that crosses no gate in either plan. `MTC_COMMAND_CENTER/11_TRIAGE/PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:158-160`.
- **Option-C acceptance:** authorization to redesign is not acceptance of future bytes. D1 authorizes one redesign and one fresh audit, and sends the lane back to the owner boundary on any required finding. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:13-28`. Audit-2 gate 2 therefore remains open until that audit accepts. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:118-125`.

## Recommended reconciliation order

1. Add supersession banners to the final authority consolidation, deploy-readiness refresh, and new-chat handoff, each pointing to the controlling night owner decisions. The exact superseded states are identified in F1, F2, and F4. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:118-131`.
2. Narrow the Packet-10 and dashboard A1 wording from an OS guarantee to the proven LF/CRLF byte condition, leaving the future target result **UNKNOWN** until exact-target execution. `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_CLAIM_VERIFICATION_2026-08-15.md:184-192`.
3. Fix the dashboard’s stale “waits on the decision” label and the synthesis’s stale `GLOBAL_HANDOFF` locator. `MTC_COMMAND_CENTER/11_TRIAGE/dashboard_2026-08-15.html:250-252`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_PATH_SYNTHESIS_2026-08-15.md:35-38`, `:56-60`.
4. Do not publish a remaining-work grand total. Keep `NO SOURCED ESTIMATE` until the currently unpriced essential rows are independently priced without overlap. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:185-198`.
