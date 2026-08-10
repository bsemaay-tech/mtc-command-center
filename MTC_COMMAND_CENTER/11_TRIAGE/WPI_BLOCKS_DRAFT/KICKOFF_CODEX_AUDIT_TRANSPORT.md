# KICKOFF — Codex T0 audit of the WP-I transport set (read-only, xhigh)

You are the Codex flagship auditor slot under the T0 contract (see
`AUDIT_TIER_CLASSIFICATION_2026-08-10.md`): fresh session, `gpt-5.6-sol`, xhigh. The
implementer was also Codex but a different session; audit adversarially as if hostile.
Report only — modify nothing, commit nothing.

**Owner amendment A2/A2a in force: do the audit yourself, do not sub-delegate.**

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. The eight transport files in `WPI_BLOCKS_DRAFT/`: `run_p0.sh`, `run_ro.sh`,
   `transport_runner.ps1`, `TRANSPORT_PLAN.tsv`, `remote_setup_wpi.sh`,
   `remote_extract_verify_wpi.sh`, `SELF_QA_TRANSPORT.md`, `STATUS_TRANSPORT.md`.
2. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — round 1.6, BINDING:
   sections 1, 4, 5, 7 + cross-cutting rules (probe execution-environment,
   structured-input, line-reader completion) + the round-1.5 derivation contracts.
3. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — attack with all ten patterns.
4. Accepted Stage-2 originals for derivation checks:
   `WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/remote_setup.sh`
   (4976 B `faee3725…`) and `remote_extract_verify.sh` (8270 B `ba0bef0e…`) — byte-verify
   both, then verify each `_wpi` file is EXACTLY the minimal derivation §4 permits
   (prefix constant only / archive-constants block only). Any other semantic delta is a
   finding.

## Verify at minimum

- **V1** Wrapper contract: symlink refusal (`-f` alone is not a refusal), every child
  reads /dev/null, STOP-first propagation, rc conveyance to the runner.
- **V2** Runner: §5 op list fidelity vs TRANSPORT_PLAN.tsv; first-FAIL ordering with
  `always` ops retained; per-op stdout/stderr/rc/elapsed capture; remote-vs-local
  binding ops local-only; PS 5.1 semantics (no `&&`/`||`, no ternary; exception
  unwrapping correctness).
- **V3** TSV reader: clean EOF vs unterminated populated final record vs hard read
  error (Pattern 7) — re-run the QA fixtures.
- **V4** Row-24 probe: classified outcomes per round-1.6
  (`connection_refused`/`timeout`/`connected`/not-evaluable), bounded, no false FAIL
  route.
- **V5** Derivation minimality: full diff of each `_wpi` script vs its accepted
  original; the only semantic changes are the permitted ones; `<PIN-AT-FREEZE>`
  constants block clearly marked and inert until filled; member list = WP-I kit with
  RP1-B3.sh excluded.
- **V6** Placeholders: every `<ALLOCATE-AT-DISPATCH>`/`<PIN-AT-FREEZE>` intact; nothing
  minted; no concrete RUNID anywhere.
- **V7** Self-QA: re-run key fixtures yourself (local only, no host/network; loopback
  only where the QA's probe-classification fixture uses it); RED cases actually
  falsify; coverage — list any function with no executed arm (a stub cannot fail).
- **V8** Hashes: re-derive per-file SHA-256 + bytes vs STATUS/SELF_QA claims;
  `bash -n` each shell file; PS 5.1 parse check for the runner.

Output: write `WPI_BLOCKS_DRAFT/TRANSPORT_CODEX_AUDIT_2026-08-10.md` — verdict first
(`PASS`/`PASS-WITH-NITS`/`REQUEST_CHANGES`/`BLOCK: <n>`), V-rows with evidence, findings
most severe first with executed falsifications where possible. Touch ONLY that file.
