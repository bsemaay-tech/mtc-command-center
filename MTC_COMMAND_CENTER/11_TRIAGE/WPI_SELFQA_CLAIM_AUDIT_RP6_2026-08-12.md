# SELF_QA prose-vs-transcript claim audit — RP6

Date: 2026-08-12  
Auditor: Codex analyst  
Audit tier: T2 (document/evidence only)  
Audited file: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`  
Audited identity: 1,038,848 bytes; 18,799 lines; SHA-256 `07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac`

No harness was run. The audited file was not edited. This audit used only the prose, published command bodies, and already-pasted transcripts in that file. The transport and pathscope self-QA documents were not read.

## Coverage

Coverage was complete, in current document order:

1. Lines 1-607: initial F1/F3/F4 repair, C13 arm, and C13 backstop.
2. Lines 608-1,648: C13 rounds 3 and 4, including both D026 harness records and supersession notes.
3. Lines 1,649-3,947: full-block repair, repair rounds 3-4, R4 D026, R4b C13, reruns, measurements, and limits.
4. Lines 3,948-5,416: rounds 5-9 and round 8 evidence repair.
5. Lines 5,417-7,996: rounds 10, 10B, and 11.
6. Lines 7,997-10,960: rounds 12 and 13.
7. Lines 10,961-13,119: round 14.
8. Lines 13,120-13,473: round 17, which occurs before rounds 15-16 in the current file.
9. Lines 13,474-15,881: round 15.
10. Lines 15,882-18,799: round 16.

Sections not reached: **none**.

The review order within those ranges was: heading/fence inventory; prose count claims; `all`/`every`/`no`/`none`/`unchanged` scope claims; closed/verified/executed/captured status claims; then a line-by-line sweep of published output and measurement blocks for result-looking constants.

## Output-line accounting

I checked **1,901 physical lines, 1,863 of them nonblank, across 47 fenced result/output/measurement blocks** for constants presented as results. This count excludes invocation-only blocks, harness source, expected/PENDING tables, and eight placeholder-only transcript fences. The eight placeholder lines were checked separately because they are not output.

The pasted numeric summaries through round 14 and in round 17 are internally consistent with their pasted case/assertion records. Examples include C13 R3 `16`, C13 backstop `4`, C13 R4/R4b `27` (25 assertion outcomes plus the two required-outcome markers), R10 `10/14/16`, R11 `15/17/85/19`, R12 `23/33`, R13 `30/35/19`, R14 `38/57/21`, and R17 `15/15`. I found no contradictory pasted count in those completed transcript blocks.

Round 15 and parts of round 16 do not have completed transcript blocks, so their closure and rerun counts cannot be accepted from this document as pasted evidence. The later R17 transcript at `SELF_QA_RP6.md:13455` does independently show the carried R16 base grammar at `cases=50 pass=50 fail=0 rc=0`; it does not supply the missing R16 discriminating-power, guard, or full rerun transcripts.

## False claims

### F-1 — Round-15/16 prose says transcript placeholders were resolved, but eight transcript slots are still placeholders

Classification: **false**.

Claim lines:

- `SELF_QA_RP6.md:13492-13505` says every round-15 transcript is real captured output and that the placeholders were resolved in round 16.
- `SELF_QA_RP6.md:15914-15918` says every round-16 transcript is real captured output or is explicitly marked `PENDING-LEAD-EXECUTION`.
- `SELF_QA_RP6.md:15995-16000` says the four earlier placeholders were resolved in this file.

Contradicting transcript lines:

- `SELF_QA_RP6.md:15341` — `@@R15_GRAMMAR_TRANSCRIPT@@`
- `SELF_QA_RP6.md:15651` — `@@R15_F1_RED_TRANSCRIPT@@`
- `SELF_QA_RP6.md:15763` — `@@R11_GUARDS_TRANSCRIPT@@`
- `SELF_QA_RP6.md:15807` — `@@RERUN_BLOCK@@`
- `SELF_QA_RP6.md:18241` — `@@R16_GRAMMAR_TRANSCRIPT@@`
- `SELF_QA_RP6.md:18524` — `@@R16_F1_RED_TRANSCRIPT@@`
- `SELF_QA_RP6.md:18645` — `@@R11_GUARDS_TRANSCRIPT@@`
- `SELF_QA_RP6.md:18690` — `@@RERUN_BLOCK@@`

None of those eight lines says `PENDING-LEAD-EXECUTION`. The inline `@@REPORT_EXEC_BLOCK@@` mention at `SELF_QA_RP6.md:18703` is different: the prose explicitly identifies it as unresolved in an out-of-scope external report, so it is not counted as a ninth missing transcript in this document.

### F-2 — R17's pass-format audit is itself hardcoded, and its zero-literal claim is self-contradictory

Classification: **false**.

Claim/transcript line: `SELF_QA_RP6.md:13458` prints:

`R17_ASSERT_MET r17_pass_format_audit r16_literal_zero_fields=6 r16_lines=3 r17_literal_zero_measurements=0`

Contradicting producer lines: `SELF_QA_RP6.md:13417-13419` assign `literal_zero_fields=6` and `literal_zero_lines=3` as literals, then print the literal `r17_literal_zero_measurements=0`. No count or comparison computes any of the three values before `rok` marks the assertion met. The `=0` claim is self-contradictory at minimum: that very producer is an R17 result-looking literal-zero field. The values `6` and `3` happen to match a manual count of the R16 producer lines, but the published R17 line presents constants, not measurements.

## Scope-wrong claims

### S-1 — The document-global “every fence below / no temp file” sentence outgrew its original section

Classification: **scope-wrong**.

Claim: `SELF_QA_RP6.md:5-7` says every fence below is covered by the opening run description and that no temp file was created.

Contradicting in-document evidence:

- Published command lines `SELF_QA_RP6.md:320-321` name QA files under `/tmp`; `SELF_QA_RP6.md:324` and `SELF_QA_RP6.md:353` write them.
- Later prose at `SELF_QA_RP6.md:1669-1670` explicitly says the fence uses a fresh `/tmp` scratch directory.
- Pasted output at `SELF_QA_RP6.md:3128` and `SELF_QA_RP6.md:3132` records an interpreter path under `/tmp/tmp.NzY2z73cI6/...`.

The opening sentence may have been true of the two initial fences when written, but the current wording says “every fence below” across a document later extended with temp-writing fences. The measurement/session statement is narrower than its present textual scope.

## Unsupported claims

### U-1 — Round-15 closure, guard-count, and rerun claims have no pasted transcript

Classification: **unsupported**.

Claim lines:

- `SELF_QA_RP6.md:13524-13560` says the three round-15 findings are closed.
- `SELF_QA_RP6.md:13578-13587` claims 18 assertions plus 26 mutants, 44 cases, no carried weakening, and no surviving carried check.
- `SELF_QA_RP6.md:15338` and `SELF_QA_RP6.md:15648` label the grammar and RED outputs as real captured output at rc 0.
- `SELF_QA_RP6.md:15756-15760` says the guard table has 23 fences and its transcript is below.
- `SELF_QA_RP6.md:15803-15804` says the touched/added fences were re-run verbatim.

Transcript lines: no supporting transcript exists. The purported evidence locations contain placeholders at `SELF_QA_RP6.md:15341`, `15651`, `15763`, and `15807`.

The harness source may be complete, but source is not an execution transcript. These claims remain unsupported within this document until the published output is pasted or the prose is explicitly marked pending.

### U-2 — Round-16 discriminating-power, guard-count, and complete-rerun claims have no pasted transcript

Classification: **unsupported**.

Claim lines:

- `SELF_QA_RP6.md:15920-15972` says the three substantive round-16 findings are closed.
- `SELF_QA_RP6.md:18238` labels `R16_GRAMMAR` output as real captured output at rc 0.
- `SELF_QA_RP6.md:18521` labels `R16_F1_RED` output as real captured output at rc 0.
- `SELF_QA_RP6.md:18638-18642` says the guard table now contains 25 fences and its guards were falsified.
- `SELF_QA_RP6.md:18650-18653` says the complete mandated list has the stated return-code vector.
- `SELF_QA_RP6.md:18686-18687` says the touched/added fences were re-run from the published bytes.

Transcript lines: no supporting transcript exists for those claims. The purported evidence locations contain placeholders at `SELF_QA_RP6.md:18241`, `18524`, `18645`, and `18690`.

The R17 transcript at `SELF_QA_RP6.md:13455` supports only the R16 base grammar's 50/50 pass on the current block. It does not show the R16 RED/GREEN structural mutants, the 25 guard mutations, or the complete mandated rerun vector.

### U-3 — R16 prints `dynamic_targets=0` as though measured, but the producer hardcodes it

Classification: **unsupported**.

Result-looking claim producer: `SELF_QA_RP6.md:17925` prints:

`inventory_variable_targets variable_targets=$n_vt inventory_targets=0 dynamic_targets=0`

Only `variable_targets` is populated from a count at `SELF_QA_RP6.md:17920`. The other two values are literal text. `p0_r16_inventory_targets_bad` at `SELF_QA_RP6.md:17468-17475` checks literal inventory-name targets; it does not derive or print a dynamic-target count. No R16 transcript line exists because the output slot at `SELF_QA_RP6.md:18241` is still a placeholder.

The later R17 path correctly derives target counts at `SELF_QA_RP6.md:13290-13301` and pastes the resulting `dynamic_targets=0` at `SELF_QA_RP6.md:13456`. That later measurement supports the current block value, but it does not turn the R16 result producer into a measurement.

### U-4 — Repeated whole-session negatives are broader than the pasted harness output

Classification: **unsupported**.

Representative claim sites include `SELF_QA_RP6.md:604`, `612-613`, `1133-1140`, `1635-1670`, `2406`, `2492-2506`, `3945-3946`, `4298-4300`, `4764-4781`, `5121-5136`, `5145`, `6493-6494`, `6664-6668`, `7942-7944`, `9314-9319`, `10914-10919`, `13071-13076`, `15814-15820`, and `18693-18706`. They assert combinations of no host/network action, no commit/Git mutation, no writes outside a named set, or no touch/read-for-writing of concurrent files.

No transcript line exists that can establish those whole-session negatives. The pasted harness outputs establish the shown commands' stdout/stderr and result vectors; they do not establish an exhaustive session command log or complete write set. This is not evidence that the negatives are false. It is a documentary support gap, and the claims should be treated as author attestations rather than transcript-proved facts unless they point to a separate provenance record.

## Clean portions

Apart from the findings above, the completed transcript sections through round 14 and the round-17 dynamic-target transcript are internally consistent on the requested axes. Historical PENDING sections identify themselves as pending; superseded fences are named as superseded; intentionally failing records state their nonzero PASS condition; and the completed case/pass/fail totals match the pasted records.

## Single most consequential finding

**F-1 is the most consequential finding.** The latest round-15/16 prose says the placeholders were resolved and the evidence was captured, but eight evidence slots remain literal placeholders. That is not a cosmetic omission: it removes the document-local execution support for the active round-15 closure, the round-16 discriminating-power proof, the updated guard census, and the complete mandated rerun vector while telling downstream auditors that the support is present.
