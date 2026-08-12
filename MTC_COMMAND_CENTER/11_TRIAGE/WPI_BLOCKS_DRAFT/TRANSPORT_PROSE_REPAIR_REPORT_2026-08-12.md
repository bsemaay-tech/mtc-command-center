# Transport prose repair report - Codex free - 2026-08-12

## Scope

Kickoff: `KICKOFF_CODEX_TRANSPORT_PROSE_REPAIRS.md`.

Audit tier: T2 documentation/evidence edit.

Session header model/effort actually available here: Codex free, GPT-5-based session. The kickoff named `gpt-5.6-sol` xhigh/fourth, but this session did not expose that model header; no effort header was exposed to the agent.

No sub-delegation. No git mutation. No harness, target, WSL, SSH, SCP, archive, freeze, host, or backtest command was run. Validation was read-only grep/hash/diff only.

## Files edited

- `SELF_QA_TRANSPORT.md`
- `STATUS_TRANSPORT.md`
- `TRANSPORT_REPAIR_R3_REPORT.md`
- `TRANSPORT_PROSE_REPAIR_REPORT_2026-08-12.md` (this file)

The seven transport targets were not edited.

## Per-repair before/after

| repair | before | after |
|---|---|---|
| F-1 integrity sentence | `SELF_QA_TRANSPORT.md` said `C:\WPI_ARTIFACTS` had no `WPI_TRANSPORT_*` entry because it was checked after every fixture, and said all fixture scratch was removed. | Replaced with the construction argument: marker gate stops `BASE_RUN`/`RECORD_ROOT` before record-root creation, `Flush-Log` writes nothing while `RecordReady` is false, and QA arms redirect `RECORD_ROOT` into fixture scratch. The cleanup sentence now says three fixtures printed removal lines, while Fixture D failed access-denied and printed no closing `removed ... exists=False` line. |
| F-1 second half | `f2_config_qa.ps1` was presented as directly re-executable with no leftover-state caveat. | Added bounded reproducibility disclosure: the published fixture body is not idempotent on a host where the prior access-denied residue remains, because the `icacls ... | Out-Null` restore does not check `$LASTEXITCODE` and cleanup has no post-condition assertion. |
| False integrity/evidence blocker | The self-QA carried an absolute cleanup/listing claim that its own transcript did not prove, despite the document's own rule that a contradicted provenance claim is a false evidence claim. | Corrected the sentence to what the transcript proves, and marked the historical `TRANSPORT_REPAIR_R3_REPORT.md` `C:\WPI_ARTIFACTS` sentence as not external-listing evidence. |
| F-2 count | `SELF_QA_TRANSPORT.md` said J1-J6 were `RED and GREEN, ten runner executions`. | Corrected to J1-J4 and J6 RED/GREEN pairs, J5 GREEN-only, eleven J-family runner executions total. Added the same marker correction to `TRANSPORT_REPAIR_R3_REPORT.md`. |
| U-1 OpenSSH count | `SELF_QA_TRANSPORT.md` said twelve executions were real pinned OpenSSH programs. | Corrected to 17 starts if M7's eight bisect rows are counted as rows, or 10 starts if M7 is counted as one arm; L1-L3 start no OpenSSH program. Added the same marker correction to `TRANSPORT_REPAIR_R3_REPORT.md`. |
| U-2 evidence support | `SELF_QA_TRANSPORT.md` used `(checked after every fixture)` as the support for no `C:\WPI_ARTIFACTS\WPI_TRANSPORT_*` entry. | Removed the unsupported check claim and replaced it with the construction argument. `STATUS_TRANSPORT.md` now also states that no external listing is claimed. |
| N-1 optional nit | `Invoke-LocalBind` classification prose/code was optional. | Not touched. No executable/prose classification change was made for N-1. |

## Repo-wide grep evidence for changed counts

Commands run after edits:

```text
rg -n --fixed-strings "ten runner executions" .
rg -n --fixed-strings "Twelve of those executions" .
rg -n "eleven .*runner executions|17 .*M7|10 .*M7|L1.*L3.*start" MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
```

Result summary:

- No uncorrected stale `ten runner executions` claim remains in `SELF_QA_TRANSPORT.md`, `STATUS_TRANSPORT.md`, or `TRANSPORT_REPAIR_R3_REPORT.md`. Exact hits inside this report are quoted-before evidence or grep-command text.
- No uncorrected stale `Twelve of those executions` claim remains in `SELF_QA_TRANSPORT.md`, `STATUS_TRANSPORT.md`, or `TRANSPORT_REPAIR_R3_REPORT.md`. Exact hits inside this report are grep-command text.
- Corrected owned hits:
  - `SELF_QA_TRANSPORT.md`: `eleven runner executions total`; `17 executions if M7...`; `10 executions if M7...`; `L1-L3 start no OpenSSH program`.
  - `TRANSPORT_REPAIR_R3_REPORT.md`: marker says eleven J-family runner executions, real pinned OpenSSH starts are 17 by M7-row reading or 10 by M7-arm reading, L1-L3 starting none.
- Remaining stale exact hits are outside this repair ownership: historical kickoffs/audits, claim-audit summaries, and run logs under `MTC_COMMAND_CENTER/11_TRIAGE/` and `WPI_BLOCKS_DRAFT/`. They were not edited per kickoff ownership.

## Integrity grep evidence

Commands run after edits:

```text
rg -n -g "*.md" "ten runner executions|Twelve of those executions|checked after every fixture|All fixture scratch was removed" MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
rg -n -g "*.md" "eleven runner executions|17 executions if M7|10 executions if M7|L1.*L3.*start|record-root creation|RecordReady|not idempotent|Fixture D.*reproducibility" MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
```

Owned current files now carry the repaired claims at:

- `SELF_QA_TRANSPORT.md`: construction argument, `RecordReady`, Fixture D reproducibility disclosure, corrected count rows.
- `STATUS_TRANSPORT.md`: no external listing claim, construction argument, Fixture D reproducibility disclosure.
- `TRANSPORT_REPAIR_R3_REPORT.md`: marker for historical `C:\WPI_ARTIFACTS` claim and marker for corrected count rows.

Remaining stale exact hits in the grep output are historical kickoffs/audits/logs outside this repair ownership and are left untouched.

## Final identity table

Seven frozen targets, re-hashed after edits:

| file | bytes | sha256 | status |
|---|---:|---|---|
| `run_p0.sh` | 13608 | `4f608ad546402ad9587eeac237c16c7c3c3e707ebf4e6cb589e9459f08413c0c` | unchanged, matches kickoff |
| `run_ro.sh` | 13470 | `3dea6e64b087488fda2ab9bac8b66fceac1c13e70719b3ce9d81797a50443e3c` | unchanged, matches kickoff |
| `transport_runner.ps1` | 71137 | `4db0fbd17f9b32da13564a9ce2d0786283151737d81bcee031ed2bcb7b347fd2` | unchanged, matches kickoff |
| `TRANSPORT_PLAN.tsv` | 7970 | `e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c` | unchanged, matches kickoff |
| `remote_setup_wpi.sh` | 26483 | `4428a60da02415ef1b7c84561b1bba458ee7f1affcfe9d33c4b1c3f07bcb5aa5` | unchanged, matches kickoff |
| `remote_extract_verify_wpi.sh` | 23592 | `5b3c0b225fdca18fd0a074a7bcce3c7124930e62eacc9e41da236db28585a55b` | unchanged, matches kickoff |
| `remote_close_tree_wpi.sh` | 32630 | `8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf` | unchanged, matches kickoff |

Edited document identities after the prose repair:

| file | bytes | sha256 |
|---|---:|---|
| `SELF_QA_TRANSPORT.md` | 195263 | `8a307344ccd16476c1ab07cd50b91708439ad7fae0abb4d07210d86e7d6ec456` |
| `STATUS_TRANSPORT.md` | 25114 | `d1d041f31aa726908370890f4689122b614c1f10d187a56e2b007e7e864039f5` |

This report is not self-hashed.

## Delta gate

Pre-edit path-scoped status for the transport-owned files was clean. The broader `WPI_BLOCKS_DRAFT` directory already had unrelated RP6 tracked edits and many untracked run logs; those were pre-existing and were not touched.

Expected post-edit delta:

```text
 M MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md
 M MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md
 M MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_REPAIR_R3_REPORT.md
?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PROSE_REPAIR_REPORT_2026-08-12.md
```

`git diff --check` was run over the four deliverable files. It reported only line-ending normalization warnings (`LF will be replaced by CRLF the next time Git touches it`) and no whitespace errors.

No git mutation was performed.
