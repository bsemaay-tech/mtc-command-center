# SESSION CONTEXT — 2026-07-16 (hand-off prompt for a fresh session; goes to BOTH models)

Work in `C:\LAB\Tradingview_LAB_CLEAN`. Read `AGENTS.md`, then
`MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`, then the LATEST sections of
`MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md` and `NEXT_STEPS.md`.

=== ROLES ===
- CODEX = builder/executor: code changes, runs, merges, mechanical work. Produce evidence-rich
  reports (commands + pasted outputs + file:line) and STOP for Fable audit after each task.
- FABLE (Claude) = auditor/architect: audits every Codex report AGAINST REAL CODE AND RUNS
  (never trust the report), synthesizes reviews, makes gate recommendations to Barış.
Human inputs belong to Barış alone: gate approvals, deploy "go", VPS rental, mainnet=forbidden.

=== CURRENT STATE (all Fable-verified 2026-07-16 on real code/runs/DB) ===

**MASTER:** `8721bce0` — PRs #16-#19 all MERGED (bridge+golden+outage-fix, UI, faz3b prereg,
donchian). Open PRs: **#20** (gitignore hygiene), **#21** (exit-aware plan doc + NEXT_STEPS
cleanup), **#22** (FAZ3B new-symbol work, see below). Worktrees: `C:/EAG`
[feature/exit-aware-gauntlet], `C:/P2RT` (runtime, detached `1465f8f0`). Repo hook flips HEAD to
master between tool calls → EVERY commit inline: `git checkout <branch> && git add <paths> &&
git commit`. Branch work happens in DEDICATED WORKTREES (never `--ignore-other-worktrees` on a
branch another worktree holds — that once moved the live runtime's ref).

**1. CRYPTO PAPER BRIDGE P2 — DISARMED, timeout fix queued.**
- History: Day 0 v1-v2 died (data stale / reconnect-reconciler race — race FIXED `da44d1ff`,
  proven live). v3 died on a REAL HL testnet outage → Barış approved outage tolerance:
  reconcile N=3 consecutive strikes + ~315s reconnect budget + Telegram notify-threshold
  (`0e644b52`, audited, deployed). **Day 0 v4 died 2026-07-15T20:22:44Z after 8h20m on
  `DATA_STALE reconnect_no_fresh_data`** — the ONE trigger the fix left alone:
  `data_restore_timeout_s = 60s` (bars.py, fresh-bar deadline after reconnect). The N=3
  tolerance was PROVEN working the same day (2× ReadTimeout tolerated, no disarm).
- **Barış approved 60s→300s (2026-07-16).** Execution = Task B of
  `11_TRIAGE/CODEX_GATE5_PR22_AND_BRIDGE_TIMEOUT_PROMPT_2026-07-16.md` (exact scope: bridge.yaml
  broker `data_restore_timeout_s: 300` + app.py/engine wiring, bars.py unchanged; tests must
  FAIL on pre-fix code; both suites both CWDs, base 130). Build → STOP for Fable audit → deploy
  on audit PASS (Barış's approval covers it) = **Day 0 v5**, validation-tier.
- Bridge now waits DISARMED by design (fail-closed; re-ARM = human gate + fresh 10-min gate
  incl. VERIFIED FRESH BARS). Runtime pinned `C:\P2RT` detached `1465f8f0` — NO git ops there
  except monitoring; pinned check = `git -C C:/P2RT log -1` + clean status.
- **PC schedule (Barış):** ON → Jul 18 (~2h off) → Jul 20 (~2h off) → 6 days → pattern.
  **VPS end of month = the definitive ≥10-day D3 clock.** Planned PC-offs are window
  boundaries, NOT incidents. Any PC ARM = policy validation only.
- Daily read-only check: `http://127.0.0.1:8790/api/status` (+ events/positions/orders/equity).
  Benign: ~10-min DISCONNECT→RECONNECT attempt=1→DATA_RESTORED (suppressed from Telegram).
  `RECONCILE_FAILED_TOLERATED` (WARN) during a real outage = correct behaviour. TESTNET ONLY;
  `HL_LIVE_ACK` unset; never print `HL_API_WALLET_KEY`; secret grep `[0-9a-fA-F]{64,}` = 0
  before every commit. Suite runs inside C:\P2RT only when expected (conftest blocks Telegram
  leakage since `960369b9`).

**2. FAZ 3B EXIT-MODE — new-symbol confirmation, PR #22, awaiting independent Gate-5.**
- Barış REJECTED the 2028 forward wait ("2028 diye bir şey yok") and ACCEPTED the new-symbol
  design direction (2026-07-16). Run approval still gated: independent Gate-5 → edits → Barış's
  formal written approval → acquisition → smoke → run. NOTHING runs before that.
- Definitive data finding (re-derivable): the canonical bundle
  `native_multiasset_alpaca_2026-06-28` is 100% Keltner-swept — 51 symbols × 7 TFs = 357 cells,
  ALL touched (June-29 overnight). **No untouched (symbol,TF) exists in-repo; only unseen
  SYMBOLS are genuine OOS.** Registry is NOT an evidence inventory — virginity checks must scan
  result JSONs (`05_BACKTEST_RESULTS/` + `research/`).
- Built on `feature/exit-aware-gauntlet` (PR #22, worktree C:/EAG), **108/108 tests, engine
  `mega_walk_forward.py` byte-identical**, no protected-scope edits:
  exit-aware `cpcv_validator`/`multiwindow_oos`/`probabilistic_pbo` (they previously scored
  fixed_2R silently for ANY candidate — the old Gate-5 FATAL), per-cell config×period PBO
  matrix, `exit_aware_gauntlet.py` orchestrator (run_cell wired end-to-end, approval-gated,
  fail-closed verdict), approval-gated `faz3b_newsymbol_runner.py` (frozen config
  {ema_len:50, atr_len:10, mult:2.0} as the ONLY deciding config), downloader `--symbols`
  additive override.
- Pre-registration: `00_AGENT_PROTOCOLS/FAZ3B_STAGE2_NEWSYMBOL_CONFIRM_PREREG_2026-07-15.md`
  — 16 scan-verified untouched symbols × 4 diversity groups (G1 US non-tech, G2 international,
  G3 broad/factor, G4 sector), ≥2-group confirmation rule, exact confound truth table (no 0.10
  margin), power floor (VOID if <8 cells reach ≥30 trades), PRIMARY deflation = within-run
  multiplicity (`du_family = 1−min(1,m(1−du_cell)) ≥ 0.95` + BH-FDR Q=0.10), SECONDARY
  N=5,795 historical union-DSR = downgrade-only diagnostic. All 15 old Gate-5 edits applied.
- Self-review `11_TRIAGE/FAZ3B_NEWSYMBOL_SELF_GATE5_2026-07-16.md` found+fixed 2 blocking gaps
  (fabricated acquisition command; gauntlet stub — now wired). Open risks stated honestly:
  trade-count power on low-vol ETFs; new-symbols-same-era weaker on regime independence than a
  true forward window (Barış accepted that trade-off).
- Fallback if this design fails review: `FAZ3B_STAGE2_FORWARD_CONFIRM_PREREG_2026-07-13.md`
  (D016 Path A, eval ≥2028-07-14).

=== TASK QUEUE (top-down) ===
1. **P2 monitoring** (read-only, every session start): /api/status + events triage; DISARMED +
   flat is the current EXPECTED state until Task B deploys.
2. **CODEX:** execute `11_TRIAGE/CODEX_GATE5_PR22_AND_BRIDGE_TIMEOUT_PROMPT_2026-07-16.md` —
   Task A (independent Gate-5 of PR #22; findings only; unit tests allowed, NO real-data runs)
   then Task B (timeout fix build+tests). STOP after each for Fable.
3. **FABLE:** audit Task B on real code (re-run suites, verify tests fail pre-fix); then deploy
   window (proven runbook: detach P2RT to audited tip → both-CWD suites → supervisor → ≥10-min
   gate incl. fresh bars → ONE ARM → record Day 0 v5 → update docs). Synthesize Task A findings,
   apply prereg edits, present the single formal run-approval question to Barış.
4. **BARIŞ:** merge PRs #20/#21 (docs-only, any time); after Gate-5+edits, the formal
   new-symbol run approval sentence (recorded in `_AI_MEMORY/DECISIONS.md`); VPS rental news
   (migration = single P2 reset; new agent wallet, never move a key).
5. After approval only: §5 acquisition (16 symbols, 1h, alpaca) → §9 smoke (non-evidence cell,
   stamping only) → 32-row run → exit-aware gauntlet → report per rules-doc §10.

=== HARD RAILS (unchanged, both models) ===
- TESTNET ONLY; mainnet requires separate written Barış approval — never assume it.
- No backtest/optimization/download/run without explicit approval; partial results are never
  evidence; pre-registrations are reviewed BEFORE running.
- Bridge tests green from BOTH CWDs (repo root + IBKR_PAPER_BRIDGE/); QuantLens tools tests from
  `03_QUANTLENS/tools/` (`pytest tests/`); PYTHONUTF8=1 everywhere.
- Engine/protected scopes (Pine, parity, MTC_V2, 02_MTC_BACKTEST, 07_ADAPTERS, 06_SCHEMAS)
  untouched; `mega_walk_forward.py` byte-identity = self-parity.
- Reports are never trusted: Fable audits on real code/runs; failures reported as failures.
- Update 03_STATUS.md + GLOBAL_HANDOFF.md (`## [MODEL] YYYY-MM-DD — topic`) + NEXT_STEPS.md at
  every milestone. Memory index lives in Claude auto-memory (MEMORY.md) — already current.
