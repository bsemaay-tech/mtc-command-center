# Codex transport round-4 audit — Band A (2026-08-11)

## Audit contract

- **TIER:** T0.
- **APPLIED AUDITOR CONTRACT:** Codex `gpt-5.6-sol`, xhigh, fresh Band A audit.
- **Frozen object:** commit `99f33c33f5fc5e3c8fbaa6141849c7cd6a435280`.
- **Scope judged:** F2, F3, F4, T5, T6, T7, T8, the 36/33 to 37/38 census, the
  superseded-`cf049b6b` kept/dropped table, and the two preregistration edits.
- **Excluded:** F1. It was not reproduced or judged in this band.
- **Safety:** no host contact, network connection, Git mutation, freeze, allocation,
  dispatch, credential use, service action, or repository edit other than this report.

## Verdict

**VERDICT: REQUEST_CHANGES**

The required F4 and T5 executions reproduce their recorded RED/GREEN outcomes on exact
commit bytes, and the census and prerequisite/marker-family edits reconcile. Acceptance is
nevertheless blocked by three required repairs: the close script arms cleanup after a
post-creation STOP branch and demonstrably leaves residue; the report and five delivered
scripts repeat a false claim about bare `declare -F`; and the T8 prose says every broken-
branch `always` failure names one of two prerequisite reasons even though the executed
classifier reports other reasons for several such operations.

## Required findings

### BA-1 — HIGH — cleanup is armed after a post-creation STOP branch

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_close_tree_wpi.sh:401` creates the
work directory. Line 402 can immediately call `stop` when the successful `mkdir` emits any
diagnostic. The cleanup trap is not installed until line 424. The created directory is
therefore outside cleanup coverage on that path, contradicting the claims at lines 58,
404–410, and 441, `TRANSPORT_R4_REPORT_2026-08-11.md:126-130`, and
`WPI_PREREGISTRATION_DRAFT.md:357-360`.

I drove the branch against frozen close-script SHA-256
`29b6412a466c10854ddf09effc8d5216317738a012235ce563c9764a9e0c40ef`. The declared tool
pins were retargeted to regular root-owned local copies, and only the admitted `mkdir`
instrument was deliberately mutated to create the requested directory, emit one diagnostic,
and return 0. Real output:

```text
SCRIPT_RC=3
CLOSE_STOP reason=work_dir_mkdir_diagnostics path=/root/wpi_r4_band_a_cleanup/work/close_work_RUN-A detail=injected_success_diagnostic
RESIDUE_PRESENT=yes
```

This is Pattern 6/7 (semantics decided after a producer completed but before its complete
result was safely handled), Pattern 9 (the every-exit-path sentence outruns the control
flow), and Pattern 10 (the published cleanup evidence never falsified this branch).

**Required repair:** capture the `mkdir` rc and diagnostics without stopping; when rc is 0,
arm cleanup before adjudicating diagnostics or running any later check. Narrow any claim
that cannot be established for a nonzero tool result. Add a D026 RED/GREEN fixture showing
the current bytes leave this exact residue and the repaired bytes remove it while retaining
the reasoned STOP.

### BA-2 — MEDIUM — the claimed second `declare -F` defect is false

The superseded-edit table says bare `declare -F` exits 1 when no function exists and would
therefore terminate the assignment under `set -Eeuo pipefail`:

- `TRANSPORT_R4_REPORT_2026-08-11.md:305`
- `run_p0.sh:29-33`
- `run_ro.sh:23-27`
- `remote_setup_wpi.sh:62-66`
- `remote_extract_verify_wpi.sh:53-57`
- `remote_close_tree_wpi.sh:114-118`

That is not Bash's behavior for the no-argument enumeration form. Executed with GNU Bash
5.3.9 in a clean `--noprofile --norc` child:

```text
===== DIRECT STATUS =====
DIRECT_RC=0
PROCESS_RC=0
===== SET-E ASSIGNMENT =====
AFTER_ASSIGN len=0
PROCESS_RC=0
===== NAMED MISSING CONTROL =====
PROCESS_RC=1
```

The named lookup control returns 1, but the delivered code uses the no-argument enumeration
form. The round-4 `|| :` is harmless, but the asserted reason for it and the report's
“second, independent defect” disposition are false. This is Pattern 9 and Pattern 10.

**Required repair:** correct the report and all repeated source comments. Either retain the
guard as explicitly defensive/no-op hardening or remove it, but do not claim a RED that the
actual command cannot produce. If the item remains in the kept/dropped table as a defect,
provide a real executable falsification of that exact no-argument command.

### BA-3 — MEDIUM — T8 overstates the two prerequisite reason tokens

The runner resolves prerequisites for every `always` operation, but its classifier returns
kind/status-specific reasons before reaching prerequisite-based rc-1 adjudication:

- `transport_runner.ps1:1084-1088` returns `scp_transfer_did_not_complete` for every
  nonzero `scp` result.
- `transport_runner.ps1:1092-1093` returns `operation_reported_stop` for rc 3.
- Only lines 1101-1105 produce `cleanup_after_unestablished_prerequisite` or
  `cleanup_after_earlier_deviation`.

The exact round-4 Fixture B execution had unestablished prerequisites and reported:

```text
id=09 reason=scp_transfer_did_not_complete
id=10 reason=scp_transfer_did_not_complete
id=11 reason=operation_reported_stop
id=12 reason=operation_reported_stop
```

This contradicts the broad statement that an `always` failure caused by an earlier break on
its branch names which of the two prerequisite cases applies in:

- `WPI_PREREGISTRATION_DRAFT.md:688-691`
- `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:570` and `:678`
- `TRANSPORT_R4_REPORT_2026-08-11.md`, T8 disposition

The run verdict remains fail-closed; this is a claim-to-predicate mismatch (Pattern 9), not
a demonstrated false PASS.

**Required repair:** either narrow all mirrored prose to the rc-1 outcomes that actually
reach prerequisite adjudication, or change the classifier so every intended operation emits
the promised prerequisite reason and add discriminating RED/GREEN evidence. Keep the two
draft occurrences byte-semantically identical.

## Mandatory execution and D026 provenance

The first ZIP-extracted runner attempt was discarded as supplemental because extraction
converted LF to CRLF and its SHA-256 did not equal the frozen identity. The executions below
used raw `git cat-file blob` bytes copied byte-for-byte into the temporary audit directory.

### F4 runner probe — executed both variants

Exact commands:

```text
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File C:\Users\BARSEM~1\AppData\Local\Temp\transport_r4_band_a_939f557ead0a414c81069d825dd29df2\raw_r4\_r4_runner_probe.ps1 -RunnerPath C:\Users\BARSEM~1\AppData\Local\Temp\transport_r4_band_a_939f557ead0a414c81069d825dd29df2\raw_r3\transport_runner.ps1 -Variant round3 -WorkDir C:\Users\BARSEM~1\AppData\Local\Temp\transport_r4_band_a_939f557ead0a414c81069d825dd29df2\raw_probe_round3

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File C:\Users\BARSEM~1\AppData\Local\Temp\transport_r4_band_a_939f557ead0a414c81069d825dd29df2\raw_r4\_r4_runner_probe.ps1 -RunnerPath C:\Users\BARSEM~1\AppData\Local\Temp\transport_r4_band_a_939f557ead0a414c81069d825dd29df2\raw_r4\transport_runner.ps1 -Variant round4 -WorkDir C:\Users\BARSEM~1\AppData\Local\Temp\transport_r4_band_a_939f557ead0a414c81069d825dd29df2\raw_probe_round4
```

The RED runner was the actual `78173bfd` blob, SHA-256
`13a57438c12effa108aacc39bbe91345acf7551b76f0991a669059040c5590e4`. The GREEN runner
was the actual `99f33c33` blob, SHA-256
`45123de489ec48dfe7d4318dad7db547bcc03114fe886be16c7f4c616fc45fed`.

| Fixture | Exact round-3 result | Exact round-4 result | Audit result |
|---|---|---|---|
| A, decisive F4 | op 08 not-evaluable; `deviant=0 not_evaluable=4`; `TR_RUN STOP`; probe rc 3 | op 08 deviant; `deviant=1 not_evaluable=3`; `TR_RUN FAIL`; probe rc 1 | RED/GREEN verified |
| B, genuinely unestablished prerequisite | not-evaluable; `TR_RUN STOP`; probe rc 3 | not-evaluable with per-edge state; `TR_RUN STOP`; probe rc 3 | Claude scenario held |
| C, own-branch earlier deviation | op 08 used the unestablished reason | op 08 used `cleanup_after_earlier_deviation prerequisites=[05=deviant]`; `TR_RUN FAIL` | distinct rc-1 reasons verified |

The stock harness also emitted Fixture D. It is F1 and outside the Band A verdict.
Both harness processes returned 0.

### T5 composition — executed

Exact command:

```text
wsl.exe -u root -- /usr/bin/bash --noprofile --norc /mnt/c/Users/BARSEM~1/AppData/Local/Temp/transport_r4_band_a_939f557ead0a414c81069d825dd29df2/raw_r4/_r4_t5_compose.sh /mnt/c/Users/BARSEM~1/AppData/Local/Temp/transport_r4_band_a_939f557ead0a414c81069d825dd29df2/raw_r4 /mnt/c/Users/BARSEM~1/AppData/Local/Temp/transport_r4_band_a_939f557ead0a414c81069d825dd29df2/raw_r3
```

The old wrapper was the actual `78173bfd` blob, SHA-256
`e4ddf87b0869ba0fadcb9750e65f4f276c90667e788e489c5921923b0d3e1f80`. The new wrapper
was frozen SHA-256 `6646770f6884dc3e918e87c65f4c097af25b71e2612f67165662825d58709202`.
The real RP6 gate came from frozen `RP6-P0.sh` SHA-256
`a090ae736cbecd9973e8ae948b052504b21cbe8b61602f4b5ac592394fad0617`, lines 683-744;
the extracted gate SHA-256 was
`c0cf53b14b90342f903c2b433655e3b3d92729689476d73854900ccb9c8be866`.

| Arm | Real output | Result |
|---|---|---|
| round-3 wrapper | `P0_ATTESTED_names_exported=0` | RED verified |
| round-4 wrapper | `P0_ATTESTED_names_exported=5` | wiring verified |
| old environment, real gate | `preregistered_value_missing`, rc 3 | RED verified |
| new environment, unfilled block literals | `freeze_pin_unfilled`, rc 3 | correct draft-stage STOP |
| new environment, both sides filled equally | `P0_GATE_PASSED all_five_attested_inputs_accepted`, rc 0 | GREEN verified |
| old environment with filled literals | `preregistered_value_missing`, rc 3 | old behavior remains RED |
| one new value changed | `prelude_value_differs_from_frozen_pin`, rc 3 | mismatch refusal verified |

Harness process rc was 0. This satisfies D026 for T5: the claimed old behavior was executed
on prior bytes, not inferred or simulated by a new-only predicate.

## Census — independently verified line by line

Every occurrence of each literal marker was enumerated in each of the seven targets at both
commits. A mapping such as `8:3` means three literal occurrences on line 8.

| File | `78173bfd` allocation lines | `78173bfd` pin lines | `99f33c33` allocation lines | `99f33c33` pin lines |
|---|---|---|---|---|
| `run_p0.sh` | 14,15,16,17,19,22 | 29,32,37 | 91,92,93,94,96,99 | 106,109,114,129,130,131,132,133 |
| `run_ro.sh` | 8,9,10,11,13,16 | 23,31,42,43,45 | 85,86,87,88,90,93 | 100,108,119,120 |
| `transport_runner.ps1` | 66,67,76,174 | 79,83,92,93,110,112,114,174 | 80,81,90 | 93,97,111,112,129,131,133 |
| `TRANSPORT_PLAN.tsv` | 2:1,3:1,4:2,8:3,9:3,10:3,11:3,12:2,13:2 | 2:1,4:2,5:1,6:1,8:1,9:1 | 2:1,3:1,4:2,8:4,9:4,10:3,11:3,12:2,13:2 | 2:1,4:2,5:1,6:1,8:1,9:1 |
| `remote_setup_wpi.sh` | — | 40,41,47 | — | 122,123,129 |
| `remote_extract_verify_wpi.sh` | — | 77,84,85,86,87,88,89 | — | 168,175,176,177,178,179,180 |
| `remote_close_tree_wpi.sh` | — | — | — | 173,174 |

Per-file totals independently reproduced the report:

| File | Round 3 alloc/pin | Round 4 alloc/pin |
|---|---:|---:|
| `run_p0.sh` | 6 / 3 | 6 / 8 |
| `run_ro.sh` | 6 / 5 | 6 / 4 |
| `transport_runner.ps1` | 4 / 8 | 3 / 7 |
| `TRANSPORT_PLAN.tsv` | 20 / 7 | 22 / 7 |
| `remote_setup_wpi.sh` | 0 / 3 | 0 / 3 |
| `remote_extract_verify_wpi.sh` | 0 / 7 | 0 / 7 |
| `remote_close_tree_wpi.sh` | 0 / 0 | 0 / 2 |
| **Total** | **36 / 33** | **37 / 38** |

The reported delta is exact: plan rows 07/08 add two allocation markers; `run_p0.sh` adds
five pins; the close script adds two numeric-identity pins; `run_ro.sh` removes one inert
pin; and composing the runner guard removes one allocation and one pin literal. Net:
allocation `+2-1=+1`; pin `+5+2-1-1=+5`.

## Superseded `cf049b6b` table audit

Commit `cf049b6b978d811c2857862bf7ec4499f8fa6965` changed only the morning handoff and
`remote_close_tree_wpi.sh`. Its transport edit was compared with `99f33c33` piece by piece.

| Reported piece | Frozen-byte result |
|---|---|
| class-5 concept kept and re-derived | verified structurally; F1 verdict excluded |
| inherited-function sweep moved before local function definitions | verified |
| unguarded bare `declare -F` was a second rc-1 defect | **false; BA-2** |
| `compgen -e` dropped for the kernel environment record | verified |
| separate forbidden-name arms folded into the exact environment sweep | verified structurally; F1 verdict excluded |
| absolute `env` and `bash` pins extended across delivered scripts | verified |
| class-3 exact diagnostic template + kernel corroboration | verified; F3 mixed-probe GREEN is consistent with the bytes |
| numeric `EXPECT_UID`/`EXPECT_GID` | verified at close-script lines 173-174 and 296-301/366-370/431-435 |
| third `WORK_ROOT`, non-overlap, create-once directory, and plan composition | verified, but cleanup coverage is incomplete; BA-1 |
| argv-count/RUNID/basename composition errors moved from rc 1 to rc 3 | verified |
| silent cleanup replaced by adjudicated cleanup | replacement exists, but the trap is armed too late; BA-1 |
| header prose rewritten | present, but its every-exit-path claim is false; BA-1 |

## Draft and source reconciliation

- The frozen prerequisite map is exact and matches the main draft:
  `07<-04`, `08<-05`, `09<-07`, `10<-08`, `11<-07+09`, `12<-08+10`.
- Plan validation requires an entry for every `always` op, rejects unknown/stale/non-earlier
  edges, and prints every edge before execution.
- The five marker-family mappings in `transport_runner.ps1:216-222` match the six
  `ssh_stdin` plan rows and the main draft's observed-outcome table.
- T5's five wrapper pins/exports and T7's removal of the inert interpreter pin match the
  main draft. The accepted RP7 block has zero reads of the removed name.
- The successor transport summary appears twice, at lines 570 and 678, with identical
  prerequisite and marker-family semantics. Both copies share BA-3's overstatement.
- T6's three-argument contract is consistent across the close-script header, plan rows
  07/08, and the main draft. The new cleanup defect is the remaining inconsistency.

## Thirteen-pattern sweep

| Pattern | Band A result |
|---|---|
| 1 — STOP is not a result | F3 and T6 classifications are fail-closed in the reviewed arms; no new false FAIL/PASS found |
| 2 — whose kernel answered | no new Band A defect; prereg domains remain explicit |
| 3 — leaf is not the path | canonical work/evidence non-overlap is checked in both directions before and after creation |
| 4 — privileged child environment | F2 inherited scratch channel is closed in the reviewed composition; F1 excluded |
| 5 — grep is not a parser | F3 uses a calibrated whole diagnostic plus kernel corroboration |
| 6/7 — status/read completion | **BA-1** |
| 8 — name is not identity | numeric close/work ownership checks verified |
| 9 — sentence outruns probe | **BA-1, BA-2, BA-3** |
| 10 — evidence that cannot fail | F4/T5 RED provenance passes; **BA-1 and BA-2** expose untested/false evidence claims |
| 11 — declared instrument is not executed | required F4/T5 harnesses execute extracted/frozen production bytes; no new Band A gap |
| 12 — unmodelled input disappears | no new Band A plan-grammar omission found |
| 13 — terminal disposition/conservation | 36/33 to 37/38 census and prerequisite membership reconcile exactly |

## Other verification

- All nine delivered identities quoted in the repair report matched raw commit bytes.
- `bash -n` returned 0 for all five delivered shell files.
- PowerShell parser error count for the raw runner was 0.
- F2's clean-tree and overlap evidence, F3's mixed-probe evidence, T6's three-argument
  composition, and T7's zero-assignment/zero-export census are consistent with the frozen
  code, but they do not close BA-1 through BA-3.

## Minimum repair set and re-audit boundary

1. Repair the post-creation cleanup coverage and add the discriminating residue RED/GREEN.
2. Correct the false bare-`declare -F` explanation everywhere it is repeated and correct
   the superseded-edit disposition table.
3. Align the T8 reason-token prose with actual classifier reachability, in both successor
   copies and every mirrored summary, or change the implementation and prove it RED/GREEN.
4. Re-run the exact F4 and T5 harnesses, the new cleanup fixture, identities, syntax/parser
   checks, and the line-by-line census on the repaired frozen bytes.

No Band A acceptance is granted until a fresh allowed T0 re-audit accepts those bytes.
