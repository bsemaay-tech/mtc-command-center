# KICKOFF — GLM-5.2: STATUS-versus-BYTES sweep across the WP-I blocks

You are GLM-5.2 via the Z.AI route. **You are running UNATTENDED — do not ask for approval, do
not write a plan and stop. Execute directly and write your verdict file.** Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. Read-only: create nothing except your verdict file, no git
mutation, no host, no network.

## Why this exists
Twice today a STATUS or record file said something the bytes did not support:

- `RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:167` claimed a two-argument close-script mismatch and
  an "exits FAIL on argc" behaviour. Both were stale — the plan and script agree on three
  arguments and an argv violation returns rc 3 STOP.
- `STATUS_RP6_P0.md` and `RP6_R17_REPORT_2026-08-12.md` both named the round-17 implementer as
  `gpt-5.6-sol`; the run log records `gpt-5.5`.

Neither was found by an auditor. Both were found by a spot-check. **This dispatch makes the
spot-check systematic** before tonight's second-flagship audits read these same files and inherit
whatever is wrong in them.

## What to sweep
For each of `STATUS_RP6_P0.md`, `STATUS_RP7.md`, `STATUS_TRANSPORT.md` and `STATUS_SEC102.md`
(all in `WPI_BLOCKS_DRAFT` except SEC102 which is in `WPI_PREREG_DRAFT_ROUND1`), verify against
the actual bytes:

1. **Every stated identity.** Re-derive byte counts and SHA-256 for every artifact the status
   file names with an identity, and report mismatches. Known current values you can check
   against: `RP6-P0.sh` 110817 B `5132bacd…`; `SELF_QA_RP6.md` 1038848 B `07cf843d…` (moved at
   round 17); `RP7-WPI-RO.sh` 108301 B `0e93f90d…`; `composite_pathproof.py` 129658 B
   `adbf27fd…`; `pathscope_prover.py` 122446 B `890016f0…`.
2. **Every model/authorship attribution.** Cross-check each named implementer and auditor against
   the corresponding `*_RUN_*.log` session header in the same directory. Report every mismatch —
   this is the failure just found in the r17 records.
3. **Every round number and status label.** Does the header status match the newest round the
   file actually documents? Does it still say PENDING for something already delivered, or
   ACCEPTED for something still pending?
4. **Every cross-reference to another file.** Does the referenced file exist, and does it say
   what the reference claims it says? Line-number citations especially — several files gained
   content today and citations may have drifted.
5. **Claims of the form "X is closed / unchanged / verified".** For each, is there a named piece
   of evidence, and does it cover the current bytes rather than an earlier round?

## Rules
- Every finding carries a `file:line`, the claim as written, and the corrected statement.
- Distinguish **stale** (was true, bytes moved) from **wrong** (never true) — the fix differs.
- Do not edit any status file. Report; the Lead edits.
- A clean sweep is a useful result. If a file is fully consistent, say so.
- Mark anything you could not execute `PENDING-LEAD-EXECUTION`; **never fabricate a green run.**

Write ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_STATUS_VS_BYTES_SWEEP_GLM_2026-08-12.md`.
Print the count of files swept, findings by class (stale / wrong / clean), and the single most
consequential finding.
