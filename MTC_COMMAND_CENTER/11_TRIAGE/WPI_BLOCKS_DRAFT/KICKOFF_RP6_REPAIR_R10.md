# KICKOFF — RP6-P0 round 10: four findings, including a test whose published command never ran the test

You are the IMPLEMENTER. Codex is the auditor of record and re-audits your bytes. Working
dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit. UNIX LF only,
zero CR bytes. Never `git checkout` a block file — use `git cat-file blob <sha>:<path> > <path>`.

If your session cannot execute commands, write the repairs, mark QA
`PENDING-LEAD-EXECUTION`, and the Lead will run them. Do not fabricate transcripts.

## Input bytes

`WPI_BLOCKS_DRAFT/RP6-P0.sh`: SHA-256
`08e0a93562bb04f4f78bac77d973a26da5b609aa305491d3bfa51743adbcf10c`, 104683 B, commit
`9bc25721`.

## Binding scope

`WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R9_2026-08-11.md` — **REQUEST_CHANGES**, four findings.

### F1 (HIGH) — `R9_GRAMMAR`'s published RED command does not run the harness

The documented command ends `... | bash --noprofile --norc "$mutant"`. With a filename
argument, Bash executes **that file** and ignores piped stdin — so the command ran the
mutant block, not the harness. Observed: `DOCUMENTED_RED_RC=3`, no `R9_GRAMMAR_SUMMARY`
anywhere in the output.

The harness itself is fine — the Lead extracted and ran it and it reported 5/5. What is
broken is the *published* command, which is the only thing a third party would run. Fix the
command so that running it verbatim executes the harness against the mutant, and record its
real output. **Then apply the same check to every other published command in
`SELF_QA_RP6.md`**: run each exactly as written, from a clean shell, and confirm the output
contains the summary line it claims. A command that silently runs something other than the
thing under test is the worst failure mode in this whole evidence contract, because it
produces confident output.

### F2 (HIGH) — the declared grammar and the executable grammar are not closed

See the finding for the specific divergences. Close them, or correct the draft where the
draft is what is wrong — and say which, per case.

### F3 (HIGH) — malformed followed-target output reaches rc 1

rc 1 means a completed observation established deviant state. A malformed followed-target
result is an inability to evaluate and must be rc 3. Add D026 RED/GREEN.

### F4 (MEDIUM) — the round-9b relabelling is convenient, not established

Line 668 emits `input_pin_omitted tool=python3` but tests only
`P0_TRUSTED_PYTHON_BOUND != yes`. Under the current control flow every false case is already
consumed by the omission loop, the freeze-unfilled gate or the disagreement gate, so **the
line is unreachable** — and a static grep is not D026 evidence for an unreachable branch.

The draft's distinction between the two conditions is sound and stays. What must change is
this site: either **remove the dead backstop**, or **declare it as an internal-binding
invariant** with a reason token describing the predicate it actually tests, plus an
executable falsification that reaches it. Do not keep an unreachable line whose reason token
claims an observation it never makes.

## The thread running through F1 and F4

Both are the same failure: **evidence that looks conclusive and establishes nothing.** F1
produces output from the wrong program; F4 labels a branch nobody can reach. This block set
has now produced this class five times in two days — the masked `printf` rc, the
line-sliced arms, the weakened `rc=[0-9]*` assertion in RP7, and now these two.

The Lead has also corrected its own practice as a result, and you should follow it: **QA is
executed by running the published command verbatim**, not by extracting the fence body a
convenient way. The Lead's round-9 run reported nine green fences by extracting bodies
directly — which was true, and would not have caught F1. From now on both the published
command and the extracted body are run, and any disagreement between them is itself a
finding.

## Writable file list

- `WPI_BLOCKS_DRAFT/RP6-P0.sh`
- `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`
- `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md`
- `WPI_BLOCKS_DRAFT/RP6_REPAIR_R10_REPORT.md` (new)
- `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — narrow, only where F2 requires it,
  and list every edit

**Owned by other sessions — never write:** `RP7-*`, `SELF_QA_RP7.md`, `STATUS_RP7.md`,
`transport_runner.ps1`, `TRANSPORT_*`, `remote_*.sh`, `run_p0.sh`, `run_ro.sh`,
`pathscope_prover.py`, `PATHSCOPE_*`, `SEC10*`, `ROWS_1_9_*`, `RUNID_*`.

## Deliverables

Repaired `RP6-P0.sh` + `SELF_QA_RP6.md` (every published command verified to run the thing it
names, with a per-command table of command → rc → summary line) + `STATUS_RP6_P0.md` +
`RP6_REPAIR_R10_REPORT.md`. `bash -n` rc 0; re-derive SHA-256 and byte count; zero CR bytes
via `tr -cd '\r' < file | wc -c`. State the disposition of every finding explicitly.
