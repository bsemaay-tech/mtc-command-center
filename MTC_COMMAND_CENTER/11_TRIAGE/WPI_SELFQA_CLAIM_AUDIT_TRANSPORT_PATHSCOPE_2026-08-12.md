# WPI SELF_QA claim audit - TRANSPORT and PATHSCOPE only

Date: 2026-08-12
Analyst: Codex
Scope: documentary consistency audit only. I audited only:

- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md`

I did not read `SELF_QA_RP6.md` or `SELF_QA_RP7.md`. I did not run harnesses, contact a host, use network, edit audited documents, or perform any git mutation.

## Sections Covered

`WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md`: covered all sections present in the audited file: round-3 sections 0-9, round-4 sections R4-0 through R4-6, round-5 sections R5-0 through R5-6, and round-6 sections R6-1 through R6-5. No section was intentionally skipped.

`WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md`: covered all sections present in the audited file: Identities, reproduction harness, D026 RED/GREEN pairs, Complete RED transcript, Complete GREEN transcript, Determinism, and Real-block diagnostic. No section was intentionally skipped.

## Output Lines Checked For Non-Measurements

Definition used: fenced `text` transcript/output blocks and output-summary fences were counted as published output. Embedded harness source fences were not counted as output.

- `SELF_QA_TRANSPORT.md`: 1,387 published output lines checked.
- `SELF_QA_PATHSCOPE.md`: 1,173 published output lines checked.
- Result: I found no `dynamic_targets=0`-style hardcoded numeric output line masquerading as a measurement. The issues below are prose-vs-transcript contradictions or unsupported prose counts/status claims, not a hardcoded-output-literal pattern.

## Findings By Class

### False

F-1 - `SELF_QA_TRANSPORT.md` falsely claims all fixture scratch was removed.

- Prose claim: `WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:23` says all fixture scratch was removed and that the last line of each transcript proves it. The same setup language at `WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:35-43` says each fixture removes its scratch and that the round scratch was removed.
- Transcript evidence: `WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:1475-1488` is the Fixture D cleanup tail, and it shows `Remove-Item` failed to remove `C:\Users\Public\wpi_r3\qb\pd_evil\ssh\ssh_config` with an access-denied error. There is no final `removed ... exists=False` line for that transcript.
- Classification: false.

F-2 - `SELF_QA_TRANSPORT.md` miscounts the J-family runner executions.

- Prose claim: `WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:1598-1600` says F1 arms J1-J6 are "RED and GREEN, ten runner executions".
- Transcript evidence: the J-family transcript banners are at `WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:910`, `:929`, `:955`, `:970`, `:992`, `:1007`, `:1029`, `:1038`, `:1060`, `:1082`, and `:1096`. That is 11 J-family execution banners, and J5 appears only as GREEN at `:1060`, so "J1-J6 (RED and GREEN, ten runner executions)" is not what the transcript shows.
- Classification: false.

F-3 - `SELF_QA_PATHSCOPE.md` says the RED `rc 0 - (no row)` rows are four critical findings, but the table/transcript show 16 such RED rows.

- Prose claim: `WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md:325-327` says the RED-column rows that read `rc 0 - (no row)` are "the four CRITICAL findings".
- Table evidence: the RED/GREEN table contains 16 RED-column rows with `rc 0 - (no row)`: `pushd`, `pushd_forbidden`, `popd_stack`, `trap`, `ssh`, `ssh_command`, `getent`, `python_c`, `alias`, `hash_p`, `mapfile_cb`, `systemctl_link`, `jobs_x`, `fddup`, `herestring`, and `nc_client` (`WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md:336-342`, `:350-355`, `:363`, `:370`, `:385`).
- Transcript evidence: the complete RED transcript confirms examples of the same pattern, including `pushd` through `getent` as `PASS rc=0` with zero resolved/unresolved records at `WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md:427-461`, `python_c` through `jobs_x` at `:505-534`, `fddup` at `:583-587`, `herestring` at `:632-636`, and `nc_client` at `:729-733`.
- Classification: false.

### Unsupported

U-1 - `SELF_QA_TRANSPORT.md` gives a "Twelve" count for real pinned OpenSSH-program executions, but the transcript does not provide a derivation that yields 12.

- Prose claim: `WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:1598-1601` says "Twelve of those executions are the real pinned OpenSSH programs."
- Transcript evidence: no transcript line prints a total of 12. The relevant transcript shows K1 and K2 real `ssh.exe` executions at `WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:1118-1139`, M1-M6 result rows at `:1409-1425`, eight M7 one-variable-out rows at `:1437-1445`, and one real `scp.exe` K3 execution at `:1447-1454`. Counting M7's eight rows as executions gives a different total than 12; counting M7 as one named arm also does not yield 12.
- Classification: unsupported.

U-2 - `SELF_QA_TRANSPORT.md` claims `C:\WPI_ARTIFACTS` was checked after every fixture, but no transcript line for that check exists.

- Prose claim: `WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:15-18` says `C:\WPI_ARTIFACTS` contains no `WPI_TRANSPORT_*` entry and was checked after every fixture.
- Transcript evidence: no transcript line in the audited document shows a `C:\WPI_ARTIFACTS` listing, count, or `WPI_TRANSPORT_*` absence check.
- Classification: unsupported.

U-3 - `SELF_QA_PATHSCOPE.md` asserts specific Python runtime and parse-status facts without transcript support.

- Prose claim: `WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md:8-10` says every run used CPython 3.14.2 with `-B`, the repaired source parses with `ast.parse(..., feature_version=(3, 12))`, and Python 3.12 is not installed.
- Transcript evidence: the harness stdout at `WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md:43-51` prints artefact identities, output line counts, and determinism lines, but it does not print the Python version, the `ast.parse` result, or the absence of a Python 3.12 executable. The harness source invokes `python -B`, but no pasted transcript line verifies the runtime claim.
- Classification: unsupported.

### Scope-Wrong

No additional scope-wrong finding survived review. The transport round-6 byte-identity language at `WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:2665-2669` is scoped to the seven executable/plan targets and explicitly excludes the two changed QA/status documents in the nine-file set, so I did not classify that known failure pattern as still present here.

## Single Most Consequential Finding

F-1 is the most consequential finding. It is a direct contradiction in the document's integrity envelope: the prose says all fixture scratch was removed and that each transcript proves it, while Fixture D's cleanup transcript shows an access-denied `Remove-Item` failure and no successful `exists=False` cleanup line.
