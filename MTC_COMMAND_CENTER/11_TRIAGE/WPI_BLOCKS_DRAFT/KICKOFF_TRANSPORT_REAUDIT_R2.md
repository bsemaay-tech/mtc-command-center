# KICKOFF — Transport set round-2 re-audit (T0 flagship slot, read-only)

You are a T0 flagship auditor (fresh session, xhigh). Round 1 gave Codex
REQUEST_CHANGES 10 + Claude REQUEST_CHANGES 6; round 2 closed all 16 (both lists)
+ 3 Lead adjudications (`TRANSPORT_REPAIR_R2_REPORT.md`). Verify closure adversarially.
Report only — modify nothing. No host/network; local Git Bash / PowerShell 5.1 fixture
execution expected.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. The eight transport files in `WPI_BLOCKS_DRAFT/` (repaired at commit `9ef4437d`):
   `run_p0.sh`, `run_ro.sh`, `transport_runner.ps1`, `TRANSPORT_PLAN.tsv`,
   `remote_setup_wpi.sh`, `remote_extract_verify_wpi.sh`, `SELF_QA_TRANSPORT.md`,
   `STATUS_TRANSPORT.md`.
2. Both round-1 reports (closure contract): `TRANSPORT_CODEX_AUDIT_2026-08-10.md`,
   `TRANSPORT_CLAUDE_T0_AUDIT_2026-08-10.md`; the repair report
   `TRANSPORT_REPAIR_R2_REPORT.md`.
3. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — the §4 round-2 four-class
   derivation contract (D-1) + §5/§7. Verify the derived `_wpi` scripts stay inside the
   four classes and nothing else drifted.
4. Accepted Stage-2 originals for derivation diffs: `…/02_PREREG/remote_setup.sh`
   (4976 B `faee3725…`), `remote_extract_verify.sh` (8270 B `ba0bef0e…`),
   `remote_close_tree.sh` (7470 B `87157f0e…`). Byte-verify.
5. `DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

## Verify

- **V1–V16**: one row per original finding across BOTH lists — closed/partial/not, each
  with evidence. RE-RUN the load-bearing round-1 falsifications against the repaired
  bytes: (Codex) ops-11/12 `$Matches` binder now binds a byte-equal pair (exit 0) and
  fails a differing pair; STOP rc3 → runner exit 3 not FAIL; PATH-planted `ssh`/`sha256sum`
  refused by pinned+bound tools; setup refuses unbound-parent/ambiguous allocation;
  extractor derivation inside the four classes; op-02 cwd; ops-07/08 stdin file present.
  (Claude) same `$Matches` root cause; exit-3 rollup; program identity; ALLOCATE-AT-DISPATCH
  fail-closed guard; §7 + 8-of-12-op launch-path QA arms are real (no stubs — a stub
  cannot fail).
- **V17** D-1 ratification check: the four-class §4 contract is coherent and the derived
  scripts honour it; `remote_close_tree.sh` co-located-by-token (not copied) resolves to
  the accepted bytes; remote tool pins refuse symlinks.
- **V18** Placeholders intact (`<ALLOCATE-AT-DISPATCH>`, `<PIN-AT-FREEZE>`); no minted
  RUNID.
- **V19** Per-file SHA-256 + bytes re-derived; `bash -n` each shell; PS 5.1 parse the
  runner.

Output: write your report to the path the dispatch names (Codex →
`TRANSPORT_CODEX_REAUDIT_R2_2026-08-10.md`; Claude → print the full report as final
output). Verdict first (`PASS`/`PASS-WITH-NITS`/`REQUEST_CHANGES`/`BLOCK: <n>`), V-rows
with evidence, findings most severe first.
