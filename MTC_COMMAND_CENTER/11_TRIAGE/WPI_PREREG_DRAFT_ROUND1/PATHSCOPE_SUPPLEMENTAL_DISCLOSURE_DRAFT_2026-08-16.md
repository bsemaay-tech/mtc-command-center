Status: SUPERSEDED — by `PATHSCOPE_SUPPLEMENTAL_DISCLOSURE_V2_2026-08-16.md` (2026-08-16, closes the Claude flagship review's R1-R5 and N1-N5; verdict in `PATHSCOPE_DISCLOSURE_CLAUDE_REVIEW_2026-08-16.md`). Historical draft, kept for the review chain.

# Pathscope supplemental-use disclosure

## 1. What Pathscope now is

Pathscope is a supplemental aid. Its output may inform review, but it may never be cited as proof, a gate, or an acceptance input anywhere in WP-I or downstream. This implements the owner's decision to take Pathscope off the critical path, authorize no further repair cycle, and require disclosure of what remains unproved (`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:62-72`).

This disposition does not make Pathscope sound, does not accept its `PASS`, and does not close any technical, evidence, freeze, audit, host, deployment, or economic gate. Stage-1 remains subject to its independent remaining prerequisites, including the administrator-supplied channel facts and the reviewed two-commit chain (`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:74-82`). This draft grants no acceptance and no authorization.

## 2. What is genuinely established

The statements below are limited to the exact audited Option C subject at commit `ec98cbd4d629d7e035f99da70d5e73fb7f610da1` (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:3-6`). They rely on the auditor's independent runner, re-measurement, attacks, and census—not on the implementer's report (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:133-139`).

- The original R5 defect classes are dead on the audited bytes: pool text deduplication, the single-empty Boolean, RHS-wide source union, and missing dispositions are gone; the relevant checks use independent inputs, including provenance recomputed from the trace, candidate/rule matches re-derived from `member.text`, real multiset conservation, and global ID uniqueness (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:443-475`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:571-576`).
- F1, F2, and F3 as filed are closed under the auditor's own re-measurement (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:178-184`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:577`).
- All fifteen ledger-corruption mutation arms reproduce: every M01–M15 arm terminates with `rc=3`, `summary=FAIL`, positive faults, no PASS terminal, and `accounting_invariant_failed` (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:165-176`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:575-576`).
- The 109-case regression contract is honest to the row: the auditor independently reproduced all 109 cases, exactly two authorized return-code changes, exactly the declared 60 byte-identical blocks, and exactly the declared eleven projection-row deltas with no unpredicted delta (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:139-163`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:202-225`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:578-580`).

These are bounded observations about the audited implementation. They are not proof that Pathscope's admission boundary is complete or that a future `PASS` establishes the property being checked.

## 3. What is not established

The following two findings are quoted verbatim and in full from the fresh flagship audit.

> ### REQUIRED-1 — the assignment-effect admission guard is bypassable inside its own route
> `pathscope_prover.py:2533-2534` (data-role early return), `2645`/`2685` (option-value
> consumption), `1330` (name-only regex).
> `${LD_PRELOAD:=/etc/evil.so}` reaches `PASS rc=0` with zero coverage issues via any
> data-role option operand on 33 of 92 registered specs plus the wrapper specs (161 options),
> via a subscripted target `${LD_PRELOAD[0]:=…}` on the exact `:` carrier of design §10.1, and
> via `for`-lists, `case` subjects, heredoc bodies, here-strings and `[`/`[[` tests. The
> composite passes these through. Evidence §4.1. Residual §11.1 does not disclose the first
> two, and the §11 closing claim that "unmodeled assignment-effect argv cannot silently cross
> the admission boundary" is falsified.

Source: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:505-514`.

Reproduction evidence: with the identical assignment-effect token, ordinary operand positions rejected at `rc=3`, while data-role option-value positions returned `PASS rc=0` with zero issues; the auditor measured the exposed surface as 33 of 92 registered command specifications and 161 data-role options, plus wrapper specifications, and the composite preserved PASS on measured examples (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:240-297`). Additional `for`, `case`, heredoc, here-string, and bracket contexts also returned `PASS rc=0` with zero issues (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:333-357`). The subscripted-target shell-semantic claim was documentary rather than shell-executed; the auditor expressly says the independently measured option-value and other-context findings do not depend on it (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:327-331`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:603-606`).

> ### REQUIRED-2 — the reading-cardinality invariant cannot fail for the reason it exists
> `pathscope_prover.py:2084-2089` with `2349-2355`.
> `expected_counts` is `len()` of the very lists the member-emission loops iterate, so the
> "independent cardinality check" of design §3.3/§4 and acceptance §12.3 is not implemented;
> the design's stated `separator_count + 1` formula is not used either. Three source-level
> splitter mutations each produce a false `PASS rc=0` with **zero** accounting faults, one of
> them reinstating the F1 finding. Evidence §4.2. Report §3's claim that independent reading
> cardinality runs is incorrect as written.

Source: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:516-523`.

Reproduction evidence: the auditor changed the production splitter in three distinct ways. Each mutation produced zero accounting faults; two yielded false PASS for the F2 provenance fixture, and disabling word reading yielded false PASS for the F1 command-text fixture, while the design's stated `separator_count + 1` rule would have caught the retained-separator mutation (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:391-430`). The auditor could not construct an input-only exploit against the current splitter, so this is an unmet contract and defence-in-depth failure, not a demonstrated current input-level exploit (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:432-437`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:593-601`).

Structural reason: conservation quantifies over admitted values, and the admission boundary has open doors.

## 4. The rule going forward

Every downstream document that mentions Pathscope must carry this exact sentence:

> Pathscope is a supplemental aid only: its output may inform review, but it may never be cited as proof, a gate, or an acceptance input anywhere in WP-I or downstream, and no Pathscope PASS may close any gate.

The prohibition is absolute for WP-I and downstream records: no Pathscope `PASS`, report, row, count, mutation result, or model verdict may close, satisfy, waive, or serve as an input to any gate. If a downstream decision is supportable without Pathscope, it must cite that independent evidence; otherwise the fact is `UNKNOWN`.

## 5. Propagation list

Search scope: a read-only, case-insensitive Markdown grep for `Pathscope` under `MTC_COMMAND_CENTER/11_TRIAGE/` and `MTC_COMMAND_CENTER/_AI_MEMORY/` in detached snapshot `c84497c885e16e1111fc3005d7cb9a82a34fb907`. The edit set below includes active/latest memory and operational records, current/awaiting-rework records, and non-archive supersession-banner targets still cited by those records. Immutable audit transcripts and historical design/repair reports that merely preserve evidence, and files that mention Pathscope only as a historical comparator or identity example, are not propagation targets. The index itself identifies several stale/superseded hazards and the current handoff/memory surfaces (`MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_DOCUMENT_INDEX_2026-08-16.md:11-19`; `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_DOCUMENT_INDEX_2026-08-16.md:144-150`).

| Current `file:line` | What it currently says | One-line edit required under this disclosure |
|---|---|---|
| `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md:7-9` | Pathscope remains the active owner boundary and needs a new owner decision. | Replace that status with the mandatory sentence and point to this disclosure; state that the owner disposition is complete and Pathscope is off the critical path. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/ACTIVE_FILES.md:13-22` | The active set names the old transport block and says Stage 1/Audit 2/WP-A remain blocked by Pathscope. | Replace the Pathscope blocker entry with this disclosure and say those stages remain blocked only by their independently established non-Pathscope prerequisites. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:63-65` | The lane is stopped at an owner boundary and a sixth cycle needs a new owner decision. | Record that §6 disposed of the lane as supplemental, no further cycle is authorized, and insert the mandatory sentence. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md:110-111` | Pathscope is the only open freeze-map sub-item before Stage 1. | Replace the gate claim with the mandatory sentence and list the administrator-channel facts and reviewed two-commit chain as the remaining Stage-1 prerequisites. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md:21-25` | Barış must authorize another cycle, and Packet 9/Stage 1 may proceed only after Pathscope acceptance. | Delete both dependencies; record the supplemental disposition and continue only through the separately authorized non-Pathscope prerequisites. |
| `MTC_COMMAND_CENTER/11_TRIAGE/NEW_CHAT_HANDOFF_2026-08-16_MORNING.md:9,32,79` | The Pathscope disposition is pending and blocks its lane and Stage 1. | Mark owner decision §6 complete, insert the mandatory sentence, and remove Pathscope from the Stage-1 blocker list without weakening the two remaining blockers. |
| `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_DOCUMENT_INDEX_2026-08-16.md:21-34,67,89,95,148-149` | The index presents Option C implementation/audit or Pathscope evidence rows as still gating current work. | Add a top correction for owner decision §6, index this disclosure as current, and reclassify Pathscope artifacts as supplemental/history rather than gate inputs. |
| `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_STEPS_REFRESH_DRAFT_2026-08-15.md:9-10,23-33` | Option C remains in progress and Audit-2 gate 2 stays open until an accepting audit. | Mark the work item disposed as supplemental, insert the mandatory sentence, and remove its accepting-audit closure condition. |
| `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_CLAIM_VERIFICATION_2026-08-15.md:21-31,72` | Pathscope is the sole open gate-2 lane and blocks all downstream Stage-1/Audit-2 work. | Add a dated supersession line: §6 removes Pathscope from gate 2; retain the reproduced findings only as disclosure. |
| `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_META_REVIEW_2026-08-15.md:5,15,43` | The current-state reconciliation ends with Option C pending and gate 2 open until it accepts. | Add a supersession note pointing to §6 and this disclosure, with the mandatory sentence. |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OWNER_BOUNDARY_2026-08-16.md:81-101` | No option is exercised, and Stage-1 freeze, Audit 2, and WP-A remain blocked behind Pathscope. | Add a decision-applied banner: the first option was selected, Pathscope is supplemental/off-path, and the mandatory sentence governs downstream use. |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_PATHSCOPE.md:3,68-70` | Status is `REPAIRED-R5-PENDING-FINAL-REAUDIT` and a fresh accepting audit is still expected. | Replace the live status with `SUPPLEMENTAL-WITH-DISCLOSURE — OFF CRITICAL PATH` and point to the two required findings and mandatory sentence. |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:98-99,122-123` | Packet/freeze bindings wait on accepted Pathscope, and Audit-2 gate 2 is open until Option C accepts. | Add a dated supersession note from the 2026-08-16 §6 decision and remove Pathscope as a gate while preserving all independent prerequisites. |
| `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_V2_2026-08-16.md:11,29,82,106-107` | R02A is a pending post-audit owner decision and one of the programme blockers. | Mark R02A complete as the supplemental disposition, set Pathscope critical-path labour to zero going forward, and insert the mandatory sentence. |
| `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:104-120,312-365,382` | Pathscope blocks Stage-1/release and its accepted Option C result is the first critical-path row. | Add a dated correction removing Pathscope from the release critical path and recompute/label any affected estimate as `UNKNOWN` until independently re-derived. |
| `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_ESTIMATE_REGISTER_2026-08-15.md:9,19-20,66` | The active estimate carries the 6–10 hour Option C row as required programme work. | Mark R01/R02 consumed historical cost, remove future Pathscope critical-path work, and set any unrecalculated subtotal to `UNKNOWN`. |
| `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE0_SCOPE_2026-08-15.md:95` | Phase-0 work is sequenced in parallel with the live Pathscope R01→R02 programme. | Replace that live-programme dependency with the completed supplemental disposition; do not use Pathscope as a join condition. |
| `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:74,139,235,389,409` | C3 and Step 4 require exact Option C bytes and an accepting audit before the shared candidate/Stage 1. | Retire C3/Step 4 as gates, insert the mandatory sentence, and reconnect the runbook only through independently established inputs. |
| `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:208` | The checklist still requires an executing accepting Pathscope audit with zero required repair. | Replace checklist C3 with the mandatory sentence and make it a disclosure-presence check, never an acceptance predicate. |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_EXTENSION_2026-08-15.md:33-45,60-67` | Three Pathscope evidence rows remain OPEN and are counted as closure work. | Preserve the rows and RED evidence as disclosed residual history, but label them non-gating/supplemental and exclude them from closure totals. |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:27,30,81` | Final inputs and Audit 2 remain blocked until Option C reaches an accepting audit. | Remove that condition, insert the mandatory sentence, and leave only independently established freeze/binding inputs as blockers. |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET11_BINDING_PROCEDURE_2026-08-15.md:66-70,296-297` | The Pathscope row closes gate 2 only if Option C's audit accepts. | Make the row a disclosure-presence record carrying the mandatory sentence; prohibit it from contributing to gate closure. |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PREREQUISITES_GATES_3_6_REWRITE_2026-08-15.md:47-49,75` | Gate 2 stays open until an accepting Pathscope audit, with three findings open. | Keep the findings disclosed, remove Pathscope from gate 2, and insert the mandatory sentence. |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:14` | Gate 2 is `OPEN ONLY ON PATHSCOPE`, and the required action is a Pathscope owner decision/work cycle. | Replace the corrected row with §6's supplemental disposition and calculate gate 2 only from non-Pathscope prerequisites. |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_OPEN_ITEM_CARRYFORWARD_2026-08-15.md:87-97` | F1–F3 remain open until the redesign and fresh audit accept. | Carry REQUIRED-1/REQUIRED-2 as disclosed non-gating limitations, not open closure items, and insert the mandatory sentence. |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:10-12,118,140-141` | Its correction still stops at Option C authorization and the body retains a Pathscope owner-decision blocker. | Extend the correction banner through 2026-08-16 §6, delete the owner-decision blocker, and insert the mandatory sentence. |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:23-31,41-43,64-65,74-83` | The still-referenced reconciliation says Pathscope is the sole gate-2 blocker; its conditional Option B path is now the selected disposition. | Add a supersession banner saying the Option B-equivalent disposition was selected under §6 and Pathscope is no longer a blocker; retain the remaining Stage-1 work unchanged. |

## 6. Cycle history

- Five cycles were completed (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:590-591`).
- Each cycle closed the findings then in scope, and the same defect class recurred one step farther out on the next review (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OWNER_BOUNDARY_2026-08-16.md:55-75`).
- The restricted-grammar option was costed in usability terms and ruled out: it rejects 100% of both real blocks and 100% of both complete proof-unit compositions (`MTC_COMMAND_CENTER/11_TRIAGE/PATHSCOPE_RESTRICTED_GRAMMAR_OPTION_SCOPING_2026-08-16.md:24-39`; `MTC_COMMAND_CENTER/11_TRIAGE/PATHSCOPE_RESTRICTED_GRAMMAR_OPTION_SCOPING_2026-08-16.md:218-224`; `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:64-72`).
