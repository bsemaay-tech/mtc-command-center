# KICKOFF — FINAL T0 flagship audit: transport set round-3 bytes (read-only, xhigh)

You are a T0 flagship auditor, fresh session, xhigh. Acceptance audit for the WP-I
transport set. Report only — modify nothing. No host contact and no network connection;
local configuration/argv evaluation of the real pinned `ssh.exe`/`scp.exe` WITHOUT
connecting is in scope and expected, as is local-to-local `scp` through the runner.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`), all at commit `78173bfd`

1. `WPI_BLOCKS_DRAFT/` — `transport_runner.ps1` (57826 B, `13a57438…`),
   `TRANSPORT_PLAN.tsv` (7219 B, `2a1cd2a6…`), `remote_setup_wpi.sh` (17775 B,
   `c0b7caa7…`), `remote_close_tree_wpi.sh` (12039 B, `fc183751…` — NEW derived),
   `remote_extract_verify_wpi.sh` (`8eb9c499…`), `run_p0.sh` (`e4ddf87b…`),
   `run_ro.sh` (`cd659ee9…`), `SELF_QA_TRANSPORT.md`, `STATUS_TRANSPORT.md`.
2. Closure contracts: `TRANSPORT_CODEX_REAUDIT_R2_2026-08-10.md` (F1–F4 + N1) and
   `TRANSPORT_CLAUDE_REAUDIT_R2_2026-08-10.md` (F1). Repair report:
   `TRANSPORT_REPAIR_R3_REPORT.md`. Round-1 reports for context.
3. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — §4 (now FOUR derived
   scripts + configuration-identity paragraph + mount clause), §5 (option block +
   observed-rc grammar table), §7.
4. Accepted Stage-2 originals for derivation diffs under
   `WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/`: `remote_setup.sh`
   (4976 B `faee3725…`), `remote_extract_verify.sh` (8270 B `ba0bef0e…`),
   `remote_close_tree.sh` (7470 B `87157f0e…` — must be UNTOUCHED).
5. `DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

## Verify

- **V1–V5** — the five round-3 findings closed, each re-driven by YOUR OWN fixture:
  F1 every native transport/cleanup failure and any rc outside `{0,1,3}` yields
  `TR_RUN STOP` / exit 3 and never FAIL; F2 the real pinned `ssh.exe` actually runs
  under the constructed environment AND ambient config cannot influence it (re-run the
  hijack pair); F3 the derived close script consults no inherited PATH and Codex's
  PATH-first `sha256sum` attack cannot mutate evidence while reporting PASS — and the
  accepted original is byte-identical to `87157f0e…`; F4 a decoy bind mount at the
  allocation parent is refused before any `mkdir`; N1 census accurate.
- **V6** Derivation minimality: full diff of each of the FOUR `_wpi` scripts against its
  accepted original; every semantic delta must fall inside the §4 four-class contract.
  Flag any drift.
- **V7** Whole-set sweep independent of the finding lists: §5 op list fidelity vs the
  plan, first-FAIL ordering with `always` retention, per-op capture, line-reader
  completion, row-24 probe classification, STOP-before-mutation, read-only scope.
- **V8** Freeze-safety: the implementer reports that a guard comparing against the
  literal `<PIN-AT-FREEZE>` is destroyed by a blind Stage-1 global fill, and that
  `transport_runner.ps1`'s pre-existing `$UNFILLED_MARKERS` array still has that shape.
  Judge whether the disclosure plus the per-constant-fill requirement is sufficient, or
  whether the runner must be repaired too.
- **V9** Placeholders intact, no minted RUNID; per-file SHA-256 + bytes re-derived;
  `bash -n` each shell file; PS 5.1 parse the runner; zero CR bytes (count BYTES, not
  matching lines).

Open for adjudication, flagged by the implementer and NOT yet ratified: the deliberately
broad `always`-cleanup rule. Give your opinion; the Lead decides.

Output: verdict first (`PASS` / `PASS-WITH-NITS` / `REQUEST_CHANGES` / `BLOCK: <n>`),
V-rows with evidence, findings most severe first with executed falsifications.
Codex slot: write to `WPI_BLOCKS_DRAFT/TRANSPORT_CODEX_FINAL_AUDIT_2026-08-10.md`.
Claude slot: print the full report as your final output.
