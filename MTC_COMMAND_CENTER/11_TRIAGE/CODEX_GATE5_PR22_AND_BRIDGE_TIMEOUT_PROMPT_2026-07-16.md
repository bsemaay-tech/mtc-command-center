# CODEX PROMPT — (A) Independent Gate-5 of PR #22 + (B) Bridge data_restore_timeout_s Fix (2026-07-16)

Author: Claude Fable 5. Executor: Codex GPT-5.
Barış decisions 2026-07-16: (a) bridge `data_restore_timeout_s` fix APPROVED; (b) independent
Gate-5 on PR #22 REQUESTED; (c) new-symbol design direction ACCEPTED (run approval still gated
on your Gate-5 + applied edits).

Execute Task A then Task B. STOP after each for Fable audit. Tasks are independent — a finding
in A does not block B.

---

## TASK A — Independent adversarial Gate-5: PR #22 (`feature/exit-aware-gauntlet`)

**You are reviewing FABLE'S OWN WORK. Fable designed it, built it, AND self-reviewed it — you
are the first independent eyes. The self-review found 2 blocking gaps in one pass; assume more
exist.** Do not defer to any claim in the documents; re-derive everything from code and
artifacts.

### Rails
1. **NO backtest, NO download, NO gauntlet/runner execution on real data.** Reading files,
   grepping, and running the UNIT suite (`pytest tests/test_exit_aware_gauntlet.py` and
   `pytest tests/` from `03_QUANTLENS/tools/` — all data mocked) are allowed and expected.
2. Work read-only in a fresh worktree of the PR branch:
   `git -C C:/LAB/Tradingview_LAB_CLEAN worktree add C:/G5R feature/exit-aware-gauntlet`.
   Commit ONLY your findings file (+ handoff section) to that branch (inline pattern, explicit
   paths, secret grep `[0-9a-fA-F]{64,}` = 0). Never `--ignore-other-worktrees`.
3. Verdict vocabulary per area: OK / FINDING / FATAL, with file:line + shown arithmetic.

### Required reading (re-derive, don't trust)
1. `00_AGENT_PROTOCOLS/FAZ3B_STAGE2_NEWSYMBOL_CONFIRM_PREREG_2026-07-15.md` (all sections)
2. `11_TRIAGE/FAZ3B_NEWSYMBOL_SELF_GATE5_2026-07-16.md` (Fable's self-review — start from its
   open risks E/F/G, but do NOT stop there)
3. The full branch diff: `git diff master...feature/exit-aware-gauntlet`
4. `11_TRIAGE/CODEX_GATE5_FINDINGS_FAZ3B_STAGE2_2026-07-13.md` (your own earlier FATAL — verify
   every one of its 15 REQUIRED EDITS is genuinely applied, not just claimed in §11)

### Attack surfaces (each gets a verdict)
- **A1 Symbol virginity:** re-run the scan yourself (result JSONs + filename-encoded artifacts
  across `05_BACKTEST_RESULTS/` + `research/`). Are all 16 frozen symbols truly absent from
  every GEN_KELTNER_BREAKOUT row? Is the scan's file-pattern coverage itself complete (what
  artifact types could hide a Keltner result)? Check also: were any of the 16 touched by OTHER
  strategies in ways that matter (e.g. they are in some OTHER bundle Fable missed)?
- **A2 Parity claims:** the tooling claims legacy fixed_2R behaviour is byte-identical. Verify
  by code reading AND by checking the tests actually pin it (would the parity tests fail on the
  pre-change code? run them against `master`'s tool files if needed — unit-level, mocked).
- **A3 Exit-threading completeness:** grep every `simulate_slice(` call site across ALL tools in
  `03_QUANTLENS/tools/` — is any caller still exit-blind that could plausibly be used in this
  confirmation (or be mistaken for usable)? `overnight_*` runners, `single_strategy_backtest.py`,
  wrappers.
- **A4 Statistics:** the §8 primary/secondary deflation split (within-run multiplicity primary;
  N=5,795 union as downgrade-only secondary). Attack: is the within-run `du_family =
  1−min(1,m(1−du_cell))` Bonferroni bound correctly one-sided? Is m defined unambiguously after
  acceptance drops? Is the union-N arithmetic right (16+15+20+5,712+32=5,795 — re-derive 5,712 =
  51×7×16 from the June-29 artifact yourself)? Is "downgrade-only, never upgrade" airtight in
  the decision table?
- **A5 Gauntlet wiring:** `exit_aware_gauntlet.run_cell` — trace it end-to-end. Does the CPCV
  path really score the frozen primary only? Does the config matrix share one symbol+exit by
  construction? Does the verdict fail-closed on every N_A/exception path (PBO ValueError,
  find_ds None, etc.)? Is the `--i-have-approval` gate bypassable by import?
- **A6 Runner scope guards:** `faz3b_newsymbol_runner.py` — can a mis-scoped run start despite
  `assert_scope`? (env set after check? argv forms it misses — `--tf=1h` equals-form? symbol
  injection when `--symbol` already present? GRIDS patch leaking into other strategies?)
- **A7 Power/feasibility:** with ~8,850 1h bars and the frozen config, is ≥30 lockbox trades
  plausible for the 16 symbols (use Stage-1 trade counts as the only evidence — no runs)? Is the
  §9 power floor (≥8 cells, ≥2 groups) coherent with the §10 decision table?
- **A8 Downloader override:** `--symbols` additive claim — verify default path byte-identical
  and that manifest entries written for new symbols carry the fields `mw.find_ds` needs.
- **A9 Gate hygiene:** any sentence that could be read as self-authorizing acquisition/run;
  fallback-to-2028 relationship stated correctly; decision-table completeness (every outcome
  mapped, precedence unambiguous).

### Deliverable
`MTC_COMMAND_CENTER/11_TRIAGE/CODEX_GATE5_FINDINGS_PR22_2026-07-16.md` — per-area verdicts +
evidence; **REQUIRED EDITS** (apply-ready wording); NICE-TO-HAVE; "could not verify without
running"; explicit "no run performed" statement. Commit to the PR branch + dated GLOBAL_HANDOFF
section. STOP for Fable synthesis. **D-decision remains Barış's after edits are applied.**

---

## TASK B — Bridge fix: `data_restore_timeout_s` 60s → 300s (Barış-APPROVED)

### Why (Fable-verified on the event store)
P2 Day 0 v4 died 2026-07-15T20:22:44Z on `DATA_STALE reconnect_no_fresh_data` → auto-DISARM.
The outage-tolerance fix relaxed two of three triggers (reconcile N=3 — proven working, two
`RECONCILE_FAILED_TOLERATED` ReadTimeouts at 15:15/16:21Z did NOT disarm; reconnect budget
~315s) but left the third at its old value: after a successful reconnect, `BarFeed` demands a
FRESH bar within `data_restore_timeout_s = 60.0` (`bridge/engine/bars.py:96`, consumed at
`bars.py:~167` → `DATA_STALE reconnect_no_fresh_data`). A quiet post-reconnect minute kills an
otherwise healthy window. Align it with the other two budgets: **300s**.

### Scope (minimal, mirrors the outage-tolerance change shape — commit `0e644b52`)
1. `config/bridge.yaml` broker block: add `data_restore_timeout_s: 300`.
2. `bridge/app.py`: wire it from `broker_cfg_raw` into the engine
   (`bar_data_restore_timeout_s=float(broker_cfg_raw.get("data_restore_timeout_s", 300.0))`).
3. `bridge/engine/engine.py`: new dataclass field `bar_data_restore_timeout_s: float = 300.0`
   (clamped `max(30.0, …)` in `__post_init__`); pass
   `data_restore_timeout_s=self.bar_data_restore_timeout_s` in the `BarFeed(...)` construction
   inside `start()`.
4. `bars.py` needs NO change (the parameter already exists).
5. **Nothing else.** No notify changes, no reconcile changes, no refactors.

### Rails (same as every bridge change)
- Branch `feature/ibkr-bridge-final` in a dedicated worktree (`git worktree add C:/BTL2
  feature/ibkr-bridge-final` — the branch is free). `C:\P2RT` untouched during build.
- TESTNET only; never print `HL_API_WALLET_KEY`; secret grep staged diff = 0; inline commits;
  `PYTHONUTF8=1`; both suites (repo root + `IBKR_PAPER_BRIDGE/`) green. Base = 130 passed.

### Tests (must fail on pre-fix code)
1. Simulated reconnect where the first fresh bar arrives at ~240s → with the new default there
   is NO `DATA_STALE`; with 60s (old default) the same sequence emits it.
2. Fresh bar never arrives → `DATA_STALE reconnect_no_fresh_data` still fires after >300s and
   still disarms (fail-closed preserved).
3. Config wiring test: bridge.yaml value reaches the BarFeed instance (as the reconnect_attempts
   wiring was tested in `0e644b52`).
4. Full suites, both CWDs; paste tails (expect ≥130 + new).

### Deliverable → STOP for Fable audit
`11_TRIAGE/P2_DATA_RESTORE_TIMEOUT_REPORT_2026-07-16.md` (commands + outputs + file:line),
dated GLOBAL_HANDOFF section, commit(s) on `feature/ibkr-bridge-final`, push (PR #16 lineage —
new PR if none open). **Deploy is Task-5-style and LOCKED until Fable audit PASS; Barış's (a)
approval covers the deploy once the audit passes** — same runbook as 2026-07-15 (detach P2RT to
audited tip → both-CWD suites → supervisor → ≥10-min gate incl. verified fresh bars → ONE ARM →
record Day 0 v5, validation-tier; the Jul 18 planned PC-off remains a window boundary, not an
incident).
