Status: DISCLOSURE RECORD V2 — SUPERSEDES V1 DRAFT — FOR LEAD REVIEW — closes AUD_PD1 findings R1-R5, N1-N5

# Pathscope supplemental-use disclosure record V2

| Finding | V2 section | What changed |
|---|---|---|
| REQUIRED-1 | §1.1 | Pins this record to the unmerged Option C bytes and distinguishes them from the older `R5_FROZEN` prover a reader can run from the repository today. |
| REQUIRED-2 | §1.2 | Makes prerequisite gate 2 `UNKNOWN` until the Lead independently re-derives it at freeze-prerequisite review; this record closes no gate. |
| REQUIRED-3 | §4 | Replaces sentence-presence as the property with a forbidden-form rule, an exact 30-path universe, and fail/STOP conditions for a checker. |
| REQUIRED-4 | §2b | Carries all seven limitations from the flagship audit's “What I could not verify” section. |
| REQUIRED-5 | §5, rows 28–30 | Adds the Audit-2 handoff package, deploy-path synthesis, and Audit-2 acceptance matrix. |
| NIT-1 | §2 | Narrows the independent-input statement to “the checks that would catch [the R5 defects'] return.” |
| NIT-2 | §§1, 3 | States that a Pathscope `PASS` has zero evidential weight on the admission-boundary property because known bypasses emit positive clean bills. |
| NIT-3 | §6 | Cites the five-cycle fact to `PATHSCOPE_OWNER_BOUNDARY_2026-08-16.md:66`. |
| NIT-4 | §5, row 20 | Requires D026-affected totals to be independently re-derived or shown as `UNKNOWN`. |
| NIT-5 | §5.1 | Names the four considered-and-excluded documents and the reason for each exclusion. |

Audit tier: **T2 — documentation/evidence only**. This record grants no acceptance, authorization, dispatch, host action, or gate decision.

## 1. What Pathscope now is

Pathscope is a supplemental aid. Its output may inform review, but it may never be cited as proof, a gate, or an acceptance input anywhere in WP-I or downstream. This implements the owner's decision to take Pathscope off the critical path, authorize no further repair cycle, and record precisely what remains unproved (`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:62-72`).

A Pathscope `PASS` carries **zero evidential weight on the admission-boundary property**. Known bypasses do not merely produce silence: they can produce `PATHSCOPE verdict=PASS rc=0`, and one measured bypass also carried a reassuring `PATH value=/safe/f verdict=ALLOW-LEXICAL` row (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:255-281`).

This disposition does not make Pathscope sound, accept a `PASS`, or close any technical, evidence, freeze, audit, host, deployment, or economic gate. Stage-1 still waits on its independently established prerequisites, including the administrator-supplied channel facts and the reviewed two-commit chain (`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:74-82`).

### 1.1 Governing identity — audited bytes versus repository bytes

This disclosure governs only the audited Option C subject at commit `ec98cbd4d629d7e035f99da70d5e73fb7f610da1` on branch `codex/pathscope-accounting-redesign-20260815`. Those bytes are **UNMERGED**. The audit pins the subject/branch at `ec98cbd4…` and independently identifies the Option C `pathscope_prover.py` working-tree and Git-blob forms as **185272 B**, with matching SHA-256 `3DA28F8E…C969F` (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:49-58`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:77-102`).

The prover present at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py` in the repository snapshot is instead **137520 B**, the audit's pinned `R5_FROZEN` identity (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:119-128`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_PATHSCOPE.md:61-70`). On that older R5 copy, the audit's `f1_command_words`, `f1_uri_bare`, and `f2_provenance` RED fixtures returned `r5_rc=0`; F1/F2/F3 were still open there (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:178-184`).

Therefore, a reader who runs the repository path today runs the older 137520 B `R5_FROZEN` prover, **not** the audited 185272 B Option C prover. The clean-bill observations in §2 apply only to the exact audited, unmerged `ec98cbd4…` bytes. They must never be attached to the repository's R5 copy.

### 1.2 Prerequisite gate 2

Removing Pathscope as prerequisite gate 2's only open sub-item does **not** make gate 2 `SATISFIED` by this record's authority. The gate's residual state must be independently re-derived by the **Lead at freeze-prerequisite review** from the non-Pathscope prerequisites and their actual authorities; until that review records a result, gate 2 is **`UNKNOWN`**. This record closes no gate.

## 2. What is genuinely established — only for the audited unmerged bytes

The following statements are bounded to the exact Option C subject identified in §1.1. They come from the auditor's independent runner, re-measurement, attacks, and census, not the implementer's report (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:133-139`).

- The original R5 defect classes are dead on the audited bytes: pool text deduplication, the single-empty Boolean, RHS-wide source union, and missing dispositions are gone. The **checks that would catch their return** use independent inputs: provenance is recomputed from the trace, candidate/rule matches are re-derived from `member.text`, multiset conservation uses real data, and IDs are globally unique (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:443-475`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:571-576`). This does not generalize to the reading-cardinality check in REQUIRED-2.
- F1, F2, and F3 as filed are closed under the auditor's own re-measurement of the audited bytes (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:178-184`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:577`).
- All fifteen ledger-corruption mutation arms reproduced: M01–M15 each terminated with `rc=3`, `summary=FAIL`, positive faults, no PASS terminal, and `accounting_invariant_failed` (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:165-176`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:575-576`).
- The 109-case regression contract was honest to the row: all 109 cases reproduced, with exactly two authorized return-code changes, the exact declared set of 60 byte-identical blocks, and exactly eleven declared projection-row deltas with no unpredicted delta (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:139-163`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:202-225`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:578-580`).

These observations are not proof that the admission boundary is complete, and they give a future Pathscope `PASS` no evidential weight on that property.

### 2b. What the auditor could not verify

The audit records all of the following as unverified or out of scope (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:614-639`):

1. The published PowerShell harness was **not executed verbatim**. The auditor extracted it, established its byte identity, and reproduced its measurements through a Python re-implementation, but did not exercise the PowerShell script's own `throw` paths, `Assert-Sha256`, transcript-leak assertion, or outer rc/stdout/stderr control flow. The published `OUTER_RC=0 STDOUT_BYTES=7661 STDERR_BYTES=0` line remains unconfirmed (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:616-623`).
2. No Python 3.12 interpreter was available. Parsing against the 3.12 feature grammar succeeded, but every execution ran on CPython 3.14.2 (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:624-627`).
3. No fixture was executed as shell. The `${NAME[0]:=value}` scalar/array assignment-effect point in REQUIRED-1(b) is documentary rather than measured; REQUIRED-1(a) and (c) do not depend on it (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:603-606`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:628-629`).
4. `SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md` was absent from the audited `ec98cbd4…` worktree; the auditor recovered it from historical commit `a4833939` and applied its questions (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:630-632`).
5. The auditor read `WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md` §D1 only as quoted in the design/report and did not independently locate that owner file (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:633-634`).
6. RP6, RP7, transport, SEC102, and composite behavior above `_interpret_output` (`prove` and member aggregation) were out of scope and unexamined (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:635-636`).
7. The independent attack batteries comprised about 90 fixtures and were not exhaustive, especially for REQUIRED-1 route (c), whose shell-context universe was enumerated by hand rather than derived from a grammar (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:637-639`).

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

Reproduction evidence: identical assignment-effect tokens were rejected at ordinary operand positions but returned `PASS rc=0` with zero issues at data-role option-value positions. The measured surface was 33 of 92 registered command specifications and 161 data-role options, plus wrapper specifications; measured composite examples preserved PASS (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:240-297`). `for`, `case`, heredoc, here-string, and bracket contexts also returned `PASS rc=0` with zero issues (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:333-357`). The subscripted-target shell-semantic point was documentary, not shell-executed, and the independently measured option-value and other-context routes do not depend on it (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:327-331`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:603-606`). A Pathscope `PASS` therefore has zero evidential weight on admission-boundary closure.

> ### REQUIRED-2 — the reading-cardinality invariant cannot fail for the reason it exists
> `pathscope_prover.py:2084-2089` with `2349-2355`.
> `expected_counts` is `len()` of the very lists the member-emission loops iterate, so the
> "independent cardinality check" of design §3.3/§4 and acceptance §12.3 is not implemented;
> the design's stated `separator_count + 1` formula is not used either. Three source-level
> splitter mutations each produce a false `PASS rc=0` with **zero** accounting faults, one of
> them reinstating the F1 finding. Evidence §4.2. Report §3's claim that independent reading
> cardinality runs is incorrect as written.

Source: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:516-523`.

Reproduction evidence: three production-splitter mutations each produced zero accounting faults. Two produced false PASS for the F2 provenance fixture, and disabling word reading produced false PASS for the F1 command-text fixture; the design's `separator_count + 1` formula would have caught the retained-separator mutation (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:391-430`). The auditor could not construct a current input-only exploit, so this is an unmet contract and defence-in-depth failure rather than a demonstrated current input-level exploit (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:432-437`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:593-601`).

Structural reason: conservation quantifies over admitted values, and the admission boundary has open doors.

## 4. Enforceable rule going forward

### 4.1 Forbidden form

**No document may condition any gate, step, checklist row, estimate, or acceptance on a Pathscope verdict, PASS, count, row, or model output.** No Pathscope output may close, satisfy, waive, price, sequence, block, unblock, dispatch, or serve as an input to any such item. A downstream conclusion must cite evidence independent of Pathscope; otherwise the conclusion is `UNKNOWN`.

### 4.2 Exact sentence and named universe

Every member of universe **U** must carry this exact sentence:

> Pathscope is a supplemental aid only: its output may inform review, but it may never be cited as proof, a gate, or an acceptance input anywhere in WP-I or downstream, and no Pathscope PASS may close any gate.

For this record, **U is exactly the 30 repository-relative paths enumerated in §5**. That is the named set of current non-archive gate, procedure, planning, status, handoff, and memory documents found under `MTC_COMMAND_CENTER/11_TRIAGE/` and `MTC_COMMAND_CENTER/_AI_MEMORY/` at frozen snapshot `c84497c885e16e1111fc3005d7cb9a82a34fb907`, including non-archive banner targets still operationally cited. The four specifically considered exclusions are listed in §5.1. Immutable audit transcripts and historical design/repair evidence are outside U unless a current U member operationally delegates a gate, dependency, estimate, or acceptance decision to them.

A new or renamed non-archive document under those two roots that mentions Pathscope is **unclassified** until the Lead adds its exact path either to U or to the explicit exclusion list with a reason. Unclassified does not mean compliant.

The exact sentence is a documentation invariant only. Its presence cannot close a gate or cure a forbidden predicate elsewhere in the same file.

### 4.3 Detection and fail/STOP contract

The checker operates over complete Markdown logical records (unwrapped paragraph, list item, checklist item, heading, or table row), not individual physical lines.

1. It verifies every exact U path exists and contains the exact sentence byte-for-byte. A missing sentence is **FAIL**.
2. After excluding only the exact mandatory sentence above, it performs a case-insensitive, multiline search in U for logical records containing `Pathscope` plus an output term (`verdict`, `PASS`, `count`, `row`, `model output`, `audit`, `accepting`, or `accepted`) and a conditioning/effect term (`must`, `required`, `requires`, `until`, `only after`, `precondition`, `blocked by`, `conditioned on`, `closes`, `satisfies`, `dispatchable`, `critical path`, `hours`, `estimate`, `gate`, `step`, or `checklist`). Any hit is **FAIL** until the predicate is removed; sentence presence cannot override it.
3. It separately searches the two roots for every non-archive Markdown Pathscope hit. A hit whose path is in neither U nor §5.1 is **STOP / UNEVALUATED**, never PASS, until the Lead classifies it.
4. An unreadable file, an unavailable multiline/record-unwrapping capability, or a drifted path list is **STOP / UNEVALUATED**, not FAIL and not PASS. This preserves the rule that inability to evaluate is not a result (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:48-107`).

What makes the compliance check go red is therefore the forbidden dependency itself (or a missing mandatory sentence), not a typo-only sentence-presence property.

## 5. Propagation universe U — re-verified

The “snapshot fact” anchors below were read against `C:\RO` at `c84497c8`. All 18 rows that the flagship review left unevaluated were re-verified. The prior V1 citation to `WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:98-99` was imprecise and is corrected below to `:118-125`. Live banner state was read from `C:\R7FINAL`; `APPLIED-BY-BANNER` means commit `9a70dc537126d15b0ffca7e011d34fcc1195c8f4` already supplies the stated substantive correction. It does not waive §4's exact-sentence and forbidden-form checks.

| # | Snapshot `file:line` | Re-verified snapshot fact | Required V2 propagation / live status |
|---:|---|---|---|
| 1 | `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md:7-9` | Historical entrypoint says Pathscope remains the active owner boundary. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md:3-12`: §6 disposition and non-Pathscope Stage-1 waits are explicit. Carry the exact §4 sentence. |
| 2 | `MTC_COMMAND_CENTER/_AI_MEMORY/ACTIVE_FILES.md:13-22` | Active set says Stage-1/Audit 2/WP-A remain blocked by Pathscope. | Replace the blocker with §6 supplemental/off-path status; leave only independently established prerequisites and carry the exact sentence. |
| 3 | `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:63-65` | Lane is stopped at an owner boundary and a sixth cycle needs a new decision. | Record §6 disposition, no further cycle, and the exact sentence. |
| 4 | `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md:110-111` | Older current-state section says Pathscope is gate 2's only open sub-item. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md:3-27`: §6 and the two remaining Stage-1 prerequisites are explicit. Gate 2 stays `UNKNOWN` per §1.2; carry the exact sentence. |
| 5 | `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md:21-25` | Owner cycle and Packet-9/Stage-1 acceptance dependencies remain in the body. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md:3-10`: both premises are void. Carry the exact sentence. |
| 6 | `MTC_COMMAND_CENTER/11_TRIAGE/NEW_CHAT_HANDOFF_2026-08-16_MORNING.md:9,32,79` | Prompt, decision table, and state row show disposition pending and Pathscope blocking the lane/Stage-1. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/11_TRIAGE/NEW_CHAT_HANDOFF_2026-08-16_MORNING.md:6-16`: all decisions answered and Pathscope off-path. Carry the exact sentence. |
| 7 | `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_DOCUMENT_INDEX_2026-08-16.md:23-34,67,89,95,148-149` | Index calls the Option C design current with implementation/audit remaining, carries three OPEN D026 rows, and points to downstream current/stale surfaces. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_DOCUMENT_INDEX_2026-08-16.md:3-11`: Pathscope artifacts are supplemental/history and no PASS closes a gate. Carry the exact sentence. |
| 8 | `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_STEPS_REFRESH_DRAFT_2026-08-15.md:9-10,23-32` | Option C remains in progress; gate 2 awaits an accepting audit. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_STEPS_REFRESH_DRAFT_2026-08-15.md:3-9`: closure condition is void. Gate 2 stays `UNKNOWN`; carry the exact sentence. |
| 9 | `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_CLAIM_VERIFICATION_2026-08-15.md:21-31,72` | It confirms Pathscope as the sole open gate-2 lane and gate 2 `NOT SATISFIED`. | Add dated supersession: §6 removes Pathscope as an input, REQUIRED-1/2 remain disclosure, and gate 2 becomes `UNKNOWN` pending Lead re-derivation. Carry the exact sentence. |
| 10 | `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_META_REVIEW_2026-08-15.md:5,15,43` | Current-state reconciliation ends with Option C pending and gate 2 open until acceptance. | Add §6 supersession, gate 2 `UNKNOWN`, and the exact sentence. |
| 11 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OWNER_BOUNDARY_2026-08-16.md:81-101` | No option is exercised; downstream remains blocked behind the lane. | Add decision-applied banner: first option selected, supplemental/off-path, no further cycle; carry the exact sentence and §1.1 identity split. |
| 12 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_PATHSCOPE.md:3,61-70` | Status is `REPAIRED-R5-PENDING-FINAL-REAUDIT`; repository prover is 137520 B R5 and a fresh audit is expected. | Set `SUPPLEMENTAL-WITH-DISCLOSURE — OFF CRITICAL PATH`; state the 137520 B/185272 B split, REQUIRED-1/2, and the exact sentence. |
| 13 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:118-125` | Correct operative anchor: Pathscope is Option C in progress and gate 2 is open until its audit accepts. | Add dated §6 supersession; remove acceptance dependency, leave gate 2 `UNKNOWN`, and carry the exact sentence. |
| 14 | `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_V2_2026-08-16.md:11,27-29,82,106-107` | R02A is the post-audit owner boundary; Pathscope remains a dependency in the wave/history. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_V2_2026-08-16.md:3-11`: R02A answered and future critical-path labour removed. Carry the exact sentence. |
| 15 | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:104-120,312-365,382` | Pathscope blocks release/freeze; accepted Option C is critical-path row 1; totals include it. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:3-9`: Pathscope is off-path and affected estimates are `UNKNOWN` until re-derived. Carry the exact sentence. |
| 16 | `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_ESTIMATE_REGISTER_2026-08-15.md:9,19-20,66` | R01/R02 and the 6–10 h Option C scenario remain current programme pricing. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_ESTIMATE_REGISTER_2026-08-15.md:3-7`: R01/R02 are consumed history and future Pathscope labour is void. Independently re-derive any affected subtotal or label it `UNKNOWN`; carry the exact sentence. |
| 17 | `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE0_SCOPE_2026-08-15.md:95` | Phase-0 work is parallel with live Pathscope R01→R02. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE0_SCOPE_2026-08-15.md:3-10`: dependency is superseded and not a join condition. Carry the exact sentence. |
| 18 | `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:74,139,235,389,409` | Reading A, check C3, Step 4, and dispatch checklist require exact Pathscope bytes and an accepting audit. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:3-12`: C3 becomes documentary disclosure only, never an acceptance predicate. Gate 2 remains `UNKNOWN`; carry the exact sentence. |
| 19 | `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:204-208` | V3 checklist C3 requires an executing accepting Pathscope audit with zero repairs. | **APPLIED-BY-BANNER (`9a70dc53`)** through the V2 banner at live `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:9-12`, which explicitly carries the correction into V3. Replace C3 body text when next edited; carry the exact sentence. |
| 20 | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_EXTENSION_2026-08-15.md:33-45,60-67` | Three Pathscope rows are OPEN and contribute to mapped/open/closure totals. | **APPLIED-BY-BANNER (`9a70dc53`) — partial** at live `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_EXTENSION_2026-08-15.md:3-8`: rows are supplemental/disclosure and excluded from closure totals. The affected totals must still be independently re-derived; until recorded, each is `UNKNOWN`. Carry the exact sentence. |
| 21 | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:27,30,81` | Final inputs and Audit 2 wait on an accepting Option C audit. | Remove the condition, make gate 2 `UNKNOWN` pending Lead review, retain independent freeze/binding blockers, and carry the exact sentence. |
| 22 | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET11_BINDING_PROCEDURE_2026-08-15.md:66-71,294-297` | Pathscope row closes gate 2 only if Option C audit accepts. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET11_BINDING_PROCEDURE_2026-08-15.md:6-11`: disclosure-presence record cannot contribute to closure. Apply §1.2 `UNKNOWN` and carry the exact sentence. |
| 23 | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PREREQUISITES_GATES_3_6_REWRITE_2026-08-15.md:47-49,75` | Gate 2 waits on an accepting audit and three Pathscope findings remain open. | Preserve findings as disclosed history, remove Pathscope from gate calculation, set residual gate 2 `UNKNOWN`, and carry the exact sentence. |
| 24 | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:14` | Gate 2 is `OPEN ONLY ON PATHSCOPE`; action is a Pathscope owner decision/work cycle. | Replace with §6 disposition; explicitly leave gate 2 `UNKNOWN` for Lead freeze-prerequisite re-derivation; carry the exact sentence. |
| 25 | `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_OPEN_ITEM_CARRYFORWARD_2026-08-15.md:87-97` | F1–F3 remain open until redesign and fresh audit accept. | Preserve REQUIRED-1/2 as non-gating disclosure, not closure items; re-derive affected counts or set `UNKNOWN`; carry the exact sentence. |
| 26 | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:10-12,118,140-142` | Existing correction stops at Option C authorization; body still asks for a Pathscope decision. | **APPLIED-BY-BANNER (`9a70dc53`)** at live `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:25-32`: §6 voids the blocker. Carry the exact sentence and gate-2 `UNKNOWN` rule. |
| 27 | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:23-31,41-43,64-65,74-83` | Pathscope is sole gate-2 blocker; conditional Option B analysis describes the now-selected disposition. | Add §6 banner, convert Pathscope material to disclosed history, leave Stage-1 work intact, make gate 2 `UNKNOWN`, and carry the exact sentence. |
| 28 | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:20,197-210` | Audit 2 may begin only after Pathscope has an accepting review; current status says Pathscope review remains pending. | Remove the Pathscope-accepting-review precondition so Audit 2 is not permanently undispatchable. Retain all independent exact-identity/freeze/D026/WP-I prerequisites; gate 2 is `UNKNOWN`; carry the exact sentence. |
| 29 | `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_PATH_SYNTHESIS_2026-08-15.md:3-29,76,126,130` | Existing correction refutes the total but leaves Pathscope as critical-path row 1 at 6–10 h and as the chain's first blocker. | Void row 1 under §6. Re-derive every dependent subtotal/critical-path total or show `UNKNOWN`; carry the exact sentence. |
| 30 | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:32-33` | Matrix expects fresh flagship execution acceptance and another repair/re-audit. | Add §6 supersession: no accepting audit is owed, REQUIRED-1/2 remain disclosed, this row contributes to no gate, and gate 2 remains `UNKNOWN`; carry the exact sentence. |

### 5.1 Explicitly considered and excluded

- `MTC_COMMAND_CENTER/11_TRIAGE/NEW_CHAT_HANDOFF_2026-08-15_AFTER_RP7_ACCEPTANCE.md:3-8,30,33` — excluded because its whole-file supersession banner marks it historical and the live entrypoint now directs readers to the 2026-08-16 handoff (`MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md:3-12`).
- `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:81` — excluded because it is V1 and is superseded by the listed V2 (`MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:1`).
- `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:40-41,117` — excluded because it is V1, conserved into the listed V2, and its live banner says V2 supersedes it (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:3-6`).
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_RED_LOCATIONS.md:47` — excluded because it is an older locator/index row; current Pathscope evidence treatment belongs to the listed D026 map extension, which preserves the evidence rows and controls their supplemental disposition (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_EXTENSION_2026-08-15.md:33-45`).

## 6. Cycle history

- This was the **fifth** completed cycle in which the named findings were closed and the same class appeared one step farther out (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OWNER_BOUNDARY_2026-08-16.md:64-67`).
- Each cycle closed the then-scoped findings, but the class recurred at the next boundary (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OWNER_BOUNDARY_2026-08-16.md:66-75`).
- The restricted-grammar option was costed and ruled out: it rejected 0/2 real blocks admitted and 0/2 complete proof-unit compositions admitted — 100% rejection (`MTC_COMMAND_CENTER/11_TRIAGE/PATHSCOPE_RESTRICTED_GRAMMAR_OPTION_SCOPING_2026-08-16.md:24-39`; `MTC_COMMAND_CENTER/11_TRIAGE/PATHSCOPE_RESTRICTED_GRAMMAR_OPTION_SCOPING_2026-08-16.md:218-224`; `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:64-72`).

This V2 is a disclosure record for Lead review. It accepts no code, closes no gate, and authorizes no further Pathscope cycle or operational action.
