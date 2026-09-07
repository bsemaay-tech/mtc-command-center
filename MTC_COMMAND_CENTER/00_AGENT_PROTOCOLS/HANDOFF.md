# Governance stage handoff

## [Claude Lead] 2026-09-07 — #161 landed; P0-20 stages built; the path is still blocked

- **Landed on `master` `fe35b7c`:** PR #161 reconciled the reviewed P0-20 calculator and
  P0-30 collector seeds — four root files, +1915/-0, no existing file modified. Merged on
  explicit owner approval. `repo_guard.ps1` is PowerShell-only and this Linux container has
  no `pwsh`, so five read-only git equivalents were run instead and all passed: `4× A` with
  no `M`/`D`; `origin/master` an ancestor of the head; all four blob OIDs identical to the
  reviewed heads; no protected path touched; CI green on `c7b3435b`. Both checkers were then
  re-run independently post-merge — both PASS, `NETWORK ATTEMPTS: 0`
  (`11_TRIAGE/P020_P030_CONTAINER_QA_REVERIFICATION_2026-09-07.md`).
- **P0-20, three of four items delivered as non-accepting candidates** on branch
  `claude/oauth-token-expired-bocby8`; full evidence in
  `11_TRIAGE/WP_P0_20_ALLOCATOR_STAGES_2026-09-07/LANE_REPORT.md`:
  - `146eaa4` caps and quantisation in the allocator, per brief §5.5 line 1160. No economic
    value introduced — every bound and minimum is an argument. 21/21 mutation controls
    DETECTED, the original eleven unchanged. D026 RED (exit 1) → GREEN (exit 0).
  - `b2159fd` the **computed** `UNSIMULATED_CONTROLS` manifest and its promotion block. The
    manifest carries its inputs and the block **re-derives** the entries, so an authored
    empty manifest is refused. 10/10 DETECTED; the named D026 fixture is RED (a REQUIRED
    unsimulated control promotes) → GREEN (`required_control_unsimulated: funding_cost`).
  - `61ac1d0` the import-identity criterion made mechanically checkable, comparing objects
    with `is`. `--self-test` proves it rejects a same-named re-implementation.
- **The fourth item is not possible here, and the reason is now evidenced:**
  `simulate_slice` performs **no position sizing at all** — percent returns and a flat
  `COST_BPS`, no quantity, notional or account figure. There is no stage to bind to;
  binding one *is* the migration this package is named for. The verifier reports
  `NOT_BOUND` and `--require-bound` exits non-zero, so acceptance cannot pass by omission.
- **Nothing is accepted.** `WP-P0-20` is T0; its gate needs the canonical path to run the
  kernel with the allocator, unreachable while `WP-P0-12` is stopped by `OD-20260826-1` /
  `OD-20260826-8`, is itself T0 on the protected kernel, and has its `P012` Item-2 packet
  only on the Windows host. Downstream P0-13/-31/-14 stay dependency-blocked.
- **Two cautions.** The panels reviewed exact blobs; `shared_risk_calculator.py` and its
  checker are no longer those blobs, so those verdicts must be re-earned. And `ci.yml`
  covers `IBKR_PAPER_BRIDGE` only — no root-level module or checker here is run by
  protected CI, so the checkers are the only fence and are run by hand (`WP-P0-27`
  unbuilt).
- **NEXT ACTION:** owner decision on the P0-12 route — unstop `WP-P0-11`/`WP-P0-12`, or
  bring the Windows-host `P012` work into the repository. Until one happens, P0-20 can only
  accumulate non-accepting candidates. Independent of that: the control-parity checklist v1
  and statistical-battery definition v1 exist only as prose and could be built next.
- **WAITING FOR OWNER:** the P0-12 route above. Nothing else.

## History

The 2026-09-06 Codex section and both earlier 2026-09-07 sections are byte-for-byte in
`_AI_MEMORY/history/00_AGENT_PROTOCOLS_HANDOFF_20260907_2251.md`; earlier narrative in
`..._20260906_2257.md` and `..._20260905_2202.md`.
