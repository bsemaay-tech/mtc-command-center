# WPI Prereg Package Claim Audit - Codex - 2026-08-12

Analyst: Codex
Audit type: T2 documentation/evidence claim audit
Constraints honored: no host access, no network, no git mutation, no edits to audited files. This is the only new file written.

Result: FINDINGS PRESENT.

## Documents Covered

- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md
- MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-11.md
- MTC_COMMAND_CENTER/11_TRIAGE/FRESH_SESSION_HANDOFF_2026-08-12_MORNING.md
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/LEAD_MC_ADJUDICATION_2026-08-11.md
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_SEC102.md
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_ACCEPT_WITH_DISCLOSURE_RECOMMENDATION_2026-08-12.md
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_CODEX_T1_AUDIT_R11_2026-08-12.md
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_GLM_T1_2ND_OPINION_2026-08-12.md
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/KICKOFF_AUDIT2_READINESS.md
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_RED_LOCATIONS.md
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_COUNT_SECOND_RECHECK_GLM_2026-08-12.md
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md

Measurement sweep: 232 candidate measurement/count/zero/dynamic-target lines were checked across the prereg draft, Audit-2 package files, the freeze-input ledger, and RP6 status/self-QA sources.

## Findings By Class

- false: 5
- unsupported: 0 separate findings
- scope-wrong: 0

## Findings

### F1 - false - R17 still publishes a hardcoded literal-zero measurement field

Claim side:
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md:48-56 says `dynamic_targets` is measured and that no literal zero is published as a measurement in the R17 pass format.
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:25 says `dynamic_targets` was converted from a hardcoded literal into a real measurement and names `r17_literal_zero_measurements=0`.
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:31 repeats that RP6-11 is closed by R17 with `dynamic_targets` converted into a measured field, again naming `r17_literal_zero_measurements=0`.
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:160-173 repeats the same R17 pass-format claim.

Contradicting source:
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md:13417-13419 hardcodes `literal_zero_fields=6`, `literal_zero_lines=3`, and emits `r17_literal_zero_measurements=0` as a literal string field.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md:13458 shows the transcript line containing `R17_ASSERT_MET r17_pass_format_audit r16_literal_zero_fields=6 r16_lines=3 r17_literal_zero_measurements=0`.

Scope note: MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md:13290-13301 does show `dynamic_targets` itself is computed from tokenizer records. This finding is not that the dynamic-target RED/GREEN pair is absent. The false claim is the broader package statement that the literal-zero measurement class was eliminated; R17 still publishes a hardcoded `r17_literal_zero_measurements=0` field.

### F2 - false - Audit-2 handoff packet details contradict the updated 16/1/3 package accounting

Current package accounting:
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:23 says Packet 7 is closed as a packet and that rows 1-9 are stated residuals, not gaps.
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:24 says Packet 8 is partial and provides the current freeze-input ledger reconciliation counts.
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:32-39 says the updated result is 16 closed, 1 partial, and 3 open/not-yet-available; Packet 7 is closed, Packet 8 is partial, and only Packets 9/10/11 are not-yet-available.

Contradicting stale detail in the same handoff:
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:142-147 still says Packet 7 is not-yet-available as a complete packet.
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:149-155 still says Packet 8 is not-yet-available.

External support for the current accounting:
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:129-141 reports the current D026 map with 39 rows, 29 fully closed, 0 open, and 10 intentionally unlocated/supplemental rows.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:117-128 reports the current 45-row freeze-input reconciliation, matching the Packet 8 partial status.

### F3 - false - Audit-2 current dispatch status carries stale SEC102, D026, and freeze-input state

Stale claim side:
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:189-192 says SEC102/pathscope acceptance is still pending and that current-work D026, freeze-input, and host-evidence packets do not exist.
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:14 says SEC102 round 9 and Codex audit are pending.

Current source side:
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:31 says SEC102 was accepted with disclosure and freeze blocker 4 was cleared.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_SEC102.md:6-13 says the owner chose Option 1 ACCEPT WITH DISCLOSURE and that no round 12 is pending.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_SEC102.md:63-68 says the open blocker is resolved by owner decision and the four assumptions are carried into the prereg draft.
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:129-141 shows the current D026 map exists.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:117-128 shows the current freeze-input ledger analysis exists, even though final freeze evidence remains partial.

This is stale status, not historical narration: the section is labeled current dispatch status.

### F4 - false - Open questions still says the final current D026 map is absent

Stale claim side:
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:41-47 says the complete current RP6/RP7/transport/SEC102/pathscope/future-current-rows D026 map is not present and that current audit REDs without GREEN remain open.

Current source side:
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:129-141 reports the current map, including 39 rows, 29 fully closed, 0 open, and 10 unlocated/supplemental rows consisting of TR-01..TR-09 plus PS-09.
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:23 says Packet 7 is closed as a packet and that rows 1-9 are absent by design, not a gap.

### F5 - false - Second D026 recheck says map line 139 is still stale after the map was corrected

Stale claim side:
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_COUNT_SECOND_RECHECK_GLM_2026-08-12.md:38 says the live defect map still has line 139 claiming one open current-audit finding.

Current source side:
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:139 says freeze-relevant D026 open current-audit findings are zero and records that line 139 was corrected at 2026-08-12 19:25.

This appears to be an older second-recheck artifact left in the package. It should be treated as stale history unless the package presents it as current state.

## Conservation Recount Results

Prereg R2 universe:
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:632-650 contains 19 R2 disposition rows, R2-01 through R2-19.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:703-749 recounts 19 self-QA review items: 13 skeleton items plus 6 RUNID items.

Prereg Lane-B universe:
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:651-665 contains 15 Lane-B disposition rows, LB-01 through LB-15.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:753-767 recounts 15 Lane-B self-QA rows.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:769 states the Lane-B equation as 11 extension rows plus 3 family rows plus 1 ordering row equals 15.

Combined conservation:
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:667 states 34 admitted items equal 19 R2 plus 15 Lane-B, with 34 terminal dispositions and 0 omitted/overwritten.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:781-788 restates the final result: R2 19/19, Lane-B 15/15, combined 34/34, terminal dispositions 34, dropped 0.

Disclosure-set separation:
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:173-206 lists four trusted-base assumptions plus one static-tool limitation and states they are disjoint from the 34-member disposition universe.
- Those five disclosure/limitation items do not appear as rows in the combined 34-row disposition table at MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:632-665. I find the disjointness claim supported.

No conservation-accounting finding: Lane-B 15/15, R2 19/19, combined 34/34, and the section 4.4.1 disclosure set being outside the 34-member universe are supported by the current text.

## Section 4.4.1 And 4.4.2 Source/Subordination Check

- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_CODEX_T1_AUDIT_R11_2026-08-12.md:16-32 supports the outer-Python-runtime disclosure.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_SEC102.md:29-49 supports the four accepted trusted-base assumptions, including the interpreter-vocabulary decision C.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_ACCEPT_WITH_DISCLOSURE_RECOMMENDATION_2026-08-12.md:68-80 supports the same four disclosure assumptions and vocabulary treatment.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_GLM_T1_2ND_OPINION_2026-08-12.md:19-21 supports the residual-disclosure framing and the safe-set leaf nit.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md:10-11 supports the on-disk-versus-fresh-clone normalization disclosure.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:212-215 makes the section 10.2 acceptance discussion expressly subject to section 4.4.1 before that discussion appears later in the draft.

No finding: section 4.4.1 and 4.4.2 source/subordination claims are supported.

## Owner-Decision Statement Check

- MTC_COMMAND_CENTER/11_TRIAGE/FRESH_SESSION_HANDOFF_2026-08-12_MORNING.md:115-119 supports MC-01, MC-02, MC-03, FAM-01, FAM-02, and FAM-03 as owner-ratified.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/LEAD_MC_ADJUDICATION_2026-08-11.md:8-27 supports the MC-01/02/03 content alignment and the need for owner ratification before clearing PROPOSED qualifiers.
- MTC_COMMAND_CENTER/11_TRIAGE/FRESH_SESSION_HANDOFF_2026-08-12_MORNING.md:120-123 supports transport F1 Option 1 accept-with-disclosure and its remaining open/non-freeze-blocker treatment.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md:31-41 supports F1 as still open, owner-ratified accept-with-disclosure, and not a freeze blocker.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:18-22 also states F1 is honestly open and owner-ratified accept-with-disclosure.
- MTC_COMMAND_CENTER/11_TRIAGE/FRESH_SESSION_HANDOFF_2026-08-12_MORNING.md:124-127 supports SEC102 interpreter-vocabulary Option 1 as a disclosed production-gate item.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_SEC102.md:46-49 supports the interpreter vocabulary decision C.

No finding: the prereg's current owner-decision statements are supported when checked against the morning handoff/status/adjudication sources. MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-11.md:6-30 supports the earlier rows 1-9 and ledger decisions, but not by itself the later MC/F1/SEC102 ratifications; the later handoff/status files supply that support.

## Audit-2 Package Arithmetic Check

Supported current arithmetic:
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:32-39 states 16 closed, 1 partial, and 3 not-yet-available/open.
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:129-141 states 39 current-cycle D026 rows, 29 fully closed, 0 open, and 10 intentionally unlocated/supplemental.
- MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:117-128 states 45 freeze-input rows: 2 FILLED, 29 LITERAL-MARKER, 0 MISSING-CONSUMER, 1 CONTRADICTED, and 13 REQUIRES-HOST.
- MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:132-141 states Packets 9/10/11 include 42 components and 5 gaps: one P9 gap, three P10 gaps, and one P11 gap.

Finding impact: the headline 16/1/3 arithmetic is internally supported by the newer package files, but stale sections inside the package contradict that arithmetic and current status. See F2 through F5.

## Most Consequential Finding

F1 is the most consequential finding. The package claims the RP6/R17 literal-zero measurement issue was fixed, but the R17 self-QA harness still emits a hardcoded `r17_literal_zero_measurements=0` field. That is the exact class of "presented as measurement but not actually measured" statement this audit was asked to catch. The dynamic-target computation itself has evidence; the failure is the downstream claim that the literal-zero measurement class was eliminated.
