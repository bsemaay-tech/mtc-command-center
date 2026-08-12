# WPI round-report claim audit - 2026-08-12

Codex documentary audit. No harness was run. No Git mutation was performed.

Audit tier classification: T2, docs/evidence only. This file audits report prose and
report-embedded count/identity claims against the matching status/self-QA evidence files.

## Scope covered

Reports audited:

- `WPI_BLOCKS_DRAFT/RP6_R16_REPORT_2026-08-11.md`
- `WPI_BLOCKS_DRAFT/RP6_R17_REPORT_2026-08-12.md`
- `WPI_BLOCKS_DRAFT/RP7_REPAIR_R9_REPORT.md`
- `WPI_BLOCKS_DRAFT/TRANSPORT_R6_REPORT_2026-08-11.md`

Target resolution note: no literal `RP7_R9_REPORT*.md` exists in
`WPI_BLOCKS_DRAFT`; the matching round-9 report present in the tree is
`RP7_REPAIR_R9_REPORT.md`, so that file was audited.

Matching evidence files checked:

- RP6: `STATUS_RP6_P0.md`, `SELF_QA_RP6.md`
- RP7: `STATUS_RP7.md`, `SELF_QA_RP7.md`
- TRANSPORT: `STATUS_TRANSPORT.md`, `SELF_QA_TRANSPORT.md`

Output/count/identity candidate lines checked in the reports: 261
(`RP6_R16` 52, `RP6_R17` 19, `RP7_R9` 95, `TRANSPORT_R6` 95). The matching
status/self-QA files were searched with the same count/identity/output patterns, then the
supporting or contradicting lines below were opened with line numbers.

## Executive result

Most consequential finding: `RP6_R16_REPORT_2026-08-11.md` says the round-16
evidence placeholders were resolved and that the status head carries real captured output,
but both matching evidence files still contain unresolved placeholder tokens. Treating the
round-16 report as evidence-grounded would therefore be unsafe without a repair.

The stale RP7 identity pattern called out by Baris was not repeated by the audited round
reports: `92853`, `e695a67b`, `77179`, `393a16ce`, and `20050` do not appear in any of
the four audited report files. `RP7_REPAIR_R9_REPORT.md` uses the current round-9 identity
`108301` / `0e93f90d...`, matching `STATUS_RP7.md:189-190` and
`SELF_QA_RP7.md:745`.

## Findings - false

### F-01 - RP6 round-16 report says SELF_QA placeholders were resolved, but they remain

Claim side:

- `WPI_BLOCKS_DRAFT/RP6_R16_REPORT_2026-08-11.md:188` says
  `SELF_QA_RP6.md` placeholders `@@R15_GRAMMAR_TRANSCRIPT@@`,
  `@@R15_F1_RED_TRANSCRIPT@@`, `@@R11_GUARDS_TRANSCRIPT@@`, and `@@RERUN_BLOCK@@`
  were resolved.

Evidence side:

- `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md:15341` still contains
  `@@R15_GRAMMAR_TRANSCRIPT@@`.
- `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md:15651` still contains
  `@@R15_F1_RED_TRANSCRIPT@@`.
- `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md:15763` still contains
  `@@R11_GUARDS_TRANSCRIPT@@`.
- `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md:15807` still contains `@@RERUN_BLOCK@@`.

Class: false.

### F-02 - RP6 round-16 report says STATUS carries real captured output, but the head is a placeholder

Claim side:

- `WPI_BLOCKS_DRAFT/RP6_R16_REPORT_2026-08-11.md:189` says
  `STATUS_RP6_P0.md` replaced `@@STATUS_EXEC_BLOCK@@` and that the round-16 head
  carries real captured output.

Evidence side:

- `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md:284` still contains `@@STATUS_EXEC_BLOCK@@`.
- `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md:587-588` says the round-16 execution block at
  the head is the evidence of record, but the referenced head block is still the
  placeholder above.

Class: false.

## Findings - unsupported

### U-01 - RP6 round-16 report's own executed-evidence block is not evidence

Claim side:

- `WPI_BLOCKS_DRAFT/RP6_R16_REPORT_2026-08-11.md:274` opens an "Executed evidence"
  section.
- `WPI_BLOCKS_DRAFT/RP6_R16_REPORT_2026-08-11.md:277` contains only
  `@@REPORT_EXEC_BLOCK@@`.

Evidence side:

- No matching pasted transcript line exists for this report block.
- The matching round-16 self-QA transcript slots are also placeholders:
  `SELF_QA_RP6.md:18241` (`@@R16_GRAMMAR_TRANSCRIPT@@`) and
  `SELF_QA_RP6.md:18524` (`@@R16_F1_RED_TRANSCRIPT@@`).
- The matching status head is also a placeholder at `STATUS_RP6_P0.md:284`.

Class: unsupported.

### U-02 - RP7 report's four-run execution count is not pinned in STATUS/SELF_QA

Claim side:

- `WPI_BLOCKS_DRAFT/RP7_REPAIR_R9_REPORT.md:254-258` says the published command was
  run verbatim end to end four times.
- `WPI_BLOCKS_DRAFT/RP7_REPAIR_R9_REPORT.md:264-267` gives run-one through run-four
  rc/wall/stdout/stderr/count rows.

Evidence side:

- `WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:4386` pins only run one:
  `RUN_ONE_RC=0 RUN_ONE_WALL_S=229 RUN_ONE_STDOUT_BYTES=66458 RUN_ONE_STDERR_BYTES=210`.
- `WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:4393` says only
  `RUN_TWO_AND_THREE=recorded_in_RP7_REPAIR_R9_REPORT.md`.
- No `RUN_FOUR` or delivered-files fourth-run line was found in `STATUS_RP7.md` or
  `SELF_QA_RP7.md`.

Class: unsupported against the matching STATUS/SELF_QA files. The report records the
extra runs internally, but the requested evidence lane does not.

### U-03 - Transport round-6 document identities are self-recorded in the report, not matched in STATUS/SELF_QA

Claim side:

- `WPI_BLOCKS_DRAFT/TRANSPORT_R6_REPORT_2026-08-11.md:249-256` lists bytes,
  SHA-256, and CR counts for `SELF_QA_TRANSPORT.md`, `STATUS_TRANSPORT.md`,
  `_r5_wsl_fixtures.sh`, `TRANSPORT_R5_REPORT_2026-08-11.md`,
  `TRANSPORT_R5_DRAFT_EDITS_PENDING.md`, and `TRANSPORT_R4_REPORT_2026-08-11.md`.

Evidence side:

- `WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:3123-3124` records only the repaired
  `_r5_wsl_fixtures.sh` identity (`21,221` bytes,
  `a2bb6f6e3c0022aa001db7adb58189649acab9b23b522dc0544b018f9ce7971b`, 0 CR).
- No matching `STATUS_TRANSPORT.md` or `SELF_QA_TRANSPORT.md` line was found for the
  report's document identity rows for `SELF_QA_TRANSPORT.md`,
  `STATUS_TRANSPORT.md`, `TRANSPORT_R5_REPORT_2026-08-11.md`,
  `TRANSPORT_R5_DRAFT_EDITS_PENDING.md`, or `TRANSPORT_R4_REPORT_2026-08-11.md`.

Class: unsupported against the matching STATUS/SELF_QA files.

## Findings - scope-wrong

### S-01 - Transport round-6 CR-byte claim is broader than the matching self-QA evidence

Claim side:

- `WPI_BLOCKS_DRAFT/TRANSPORT_R6_REPORT_2026-08-11.md:225` says CR bytes were 0
  for "all seven targets, the harness, and every document edited this round".

Evidence side:

- `WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:3116` records 0 CR bytes only for "all
  seven targets and the harness".

Class: scope-wrong. The matching self-QA line supports the seven targets plus the harness,
not the broader "every document edited this round" scope.

## Clean checks / non-findings

- `RP6_R17_REPORT_2026-08-12.md` identity and dynamic-target counts matched the
  matching records checked: report `:19-20` matches `STATUS_RP6_P0.md:17-18` and
  `SELF_QA_RP6.md:13450-13451`; report `:79-87` matches
  `STATUS_RP6_P0.md:61-70` and `SELF_QA_RP6.md:13455-13471`.
- RP7 subject identity is current, not stale: report `RP7_REPAIR_R9_REPORT.md:16-17`
  matches `STATUS_RP7.md:117-118`, `STATUS_RP7.md:189-190`, and
  `SELF_QA_RP7.md:745`.
- RP7 round-9 core output counts and body-binding values checked against
  `SELF_QA_RP7.md` were consistent: `QA_PASS` x6 at `SELF_QA_RP7.md:201-211`,
  published command result at `SELF_QA_RP7.md:218`, and body/bind/netns/mapping lines
  at `SELF_QA_RP7.md:745-777` and `SELF_QA_RP7.md:2492-2500`.
- Transport's central BA-1 repair counts matched the matching evidence:
  `BA1_ARMS_RECORDED=10` at `SELF_QA_TRANSPORT.md:2705` and `:2970`,
  `DISTINCT_SUBJECT_ARGV_LINES=1` at `SELF_QA_TRANSPORT.md:2706` and `:2971`,
  `REFUSAL_BYTE_IDENTICAL=yes` at `SELF_QA_TRANSPORT.md:2832`,
  fixture stdout line count at `SELF_QA_TRANSPORT.md:2760`, and static-gate summary at
  `SELF_QA_TRANSPORT.md:3113-3121`.
