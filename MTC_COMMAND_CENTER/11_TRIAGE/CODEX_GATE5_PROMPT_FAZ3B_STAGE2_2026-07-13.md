# CODEX PROMPT — Queue 3: FAZ3B Stage-2 Gate-5 Adversarial Review (2026-07-13)

Author: Claude Fable 5 (auditor). Executor: Codex GPT-5 (adversarial reviewer).
Target document: `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md`
(DRAFT — awaiting Barış D016). Spec authority:
`MTC_COMMAND_CENTER/11_TRIAGE/FAZ3B_STAGE2_PREREG_PROMPT_2026-07-05.md` Step 2.

## ROLE

You are the adversary. Your job is to BREAK this pre-registration on paper before any
compute is spent. Assume the author was smart but motivated; hunt for places where the
design quietly guarantees a positive, hides a degree of freedom, or cannot mechanically
decide an outcome. A finding that survives your own steelman counter-argument goes in the
report; weak nitpicks do not.

## HARD RAILS (violating any = review void)

1. **WRITTEN FINDINGS ONLY. NO RUNS.** You may read files, grep, and inspect result JSONs
   and registries (read-only). You may NOT invoke `mega_walk_forward.py`, any runner,
   CPCV/PBO/multiwindow tools, pytest, or any backtest — not even a "quick smoke".
   Feasibility questions are answered by reading code and existing artifacts, never by
   executing.
2. Do not edit the pre-reg. Required edits are LISTED in your findings; Fable/Claude
   applies them after synthesis.
3. Protected scopes untouched (Pine, parity, MTC_V2, `02_MTC_BACKTEST`, `07_ADAPTERS`,
   `06_SCHEMAS`). No engine edits, no golden recapture.
4. Never trust prior reports — Stage-1 numbers you rely on must be re-read from the
   result JSONs yourself (paths below).
5. Repo hook flips HEAD to master between tool calls. Commit deliverables in ONE inline
   command: `git checkout feature/faz3b-stage2-prereg && git add <explicit paths> && git commit -m "..."`.
   No `git add .`/`-A`. Secret grep staged diff (`[0-9a-fA-F]{64,}`) = 0 before commit.
   Note: this branch has open PR #18 — your commit updates it; that is intended.
6. D016 does not exist. Nothing you write authorizes a run, and your review must FLAG any
   sentence in the pre-reg that could be read as self-authorizing.

## REQUIRED READING (in order, before any finding)

1. The target pre-reg (all 12 sections).
2. Stage-1 evidence you must independently verify:
   - `MTC_COMMAND_CENTER/03_QUANTLENS/research/faz3b_stage1_20260705/pass2_1h/MEGA_walk_forward_results.json`
     (winner extraction; union-DSR inputs; sr_std pooling inputs)
   - `MTC_COMMAND_CENTER/03_QUANTLENS/research/faz3b_stage1_20260705/STAGE1_REPORT.md`
     ("DSR method note" — the recompute recipe the pre-reg §6 claims to reuse)
   - `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md`
3. Rules doc gates the pre-reg §6 binds itself to:
   `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`
   (Benchmark Gate, CPCV Gate, DSR, BH-FDR, multi-window, promotion levels).
4. CPCV empirical failure context: the Donchian crypto ladder produced **CPCV: 0 eligible
   combinations** on every cell —
   `MTC_COMMAND_CENTER/11_TRIAGE/DONCHIAN_CRYPTO_LADDER_VERDICT_2026-07-13.md` and
   artifacts under `MTC_COMMAND_CENTER/03_QUANTLENS/research/donchian_crypto_ladder_2026-07-13/`.
   Read what made cells ineligible (group counts / purge-embargo / min trades per fold).
5. Engine grid + registry ground truth: `grid_keltner_breakout()` axes in
   `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py`, and
   `MTC_COMMAND_CENTER/05_REGISTRY/RESEARCH_RUN_REGISTRY.json` (held-out virginity check).

## ATTACK SURFACE — every area below gets a written verdict (OK / FINDING / FATAL)

### A. Winner-extraction correctness
Re-extract the Stage-1 winner for KELTNER × AAPL × 1h × trail_ema8 from the pass2_1h
result JSON yourself. Does `summary.best_params` really say `{ema_len: 50, atr_len: 10,
mult: 2.0}`? Was the winner selected at stride 3 — and if so, does "winner ± 1 neighbor
from ORIGINAL axes" inherit a stride artifact (values the stride never evaluated)?

### B. Grid narrowness honesty (§4)
The 12-set cartesian spans {20,50}×{10,20}×{1.5,2.0,2.5} = 12 of the original 16 configs
(75% of the discovery grid). Attack: is this still a "confirmation" grid, or effective
re-discovery with a 25% haircut? The 2-value axes make "±1 neighbor" = "entire axis" —
was a tighter alternative (winner-only + star) wrongly rejected? Quantify what the wide
grid does to the per-cell best-of-12 selection optimism that union-DSR must then pay for.

### C. Held-out genuineness (§3)
(1) Verify via registry + result-JSON scan that GOOGL/META/AMD/NFLX/DIA/IWM truly never
appeared in ANY prior GEN_KELTNER run (the pre-reg claims this was checked — re-check it).
(2) Correlation leakage: Stage-1 confound cells were SPY/QQQ; DIA and IWM are index ETFs
highly correlated with SPY. Same calendar window 2020→2026. Is "held-out" here symbol-new
but regime-identical — and does the pre-reg overclaim independence? Should DIA/IWM cells
be labeled weaker-evidence tier or excluded from the "≥1 of 6" decision set?
(3) The 4 stocks are mega-cap tech-adjacent like AAPL — same-sector clustering risk: one
sector regime could clear multiple "independent" cells simultaneously. Does the decision
rule need a diversity requirement (e.g., confirming cells from ≥2 groups)?

### D. Trial arithmetic + union family completeness (§8, A17)
(1) Recompute 16 + 15 + 20 + 168 = 219 and verify each component against the actual
Stage-1 artifacts (why floor(16/3)=5 per mode? is that the Stage-1 report's real
accounting or a convenient reconstruction?).
(2) Family gerrymandering attack: the KELTNER lineage has more history than these four
components? Scan registries/results for any GEN_KELTNER_BREAKOUT trials excluded from the
union (e.g., archetype sweeps, turtle-era runs, 63-archetype library). Every exclusion
needs a written justification or the family is understated and DSR overstated.
(3) Selection-over-cells attack: §8 claims including all 168 Stage-2 trials in N pays for
the "≥1 of 6 cells" selection. Is that actually how DSR deflation works — does a single
family-size N adjust for the MAX over 6 correlated cell statistics, or does it only
deflate each cell's own Sharpe? If not, propose the mechanical correction (e.g., require
union-DSR ≥ 0.95 to survive a per-cell Bonferroni-style 6-way adjustment, or demand ≥2
confirming cells).

### E. Union-DSR method reproducibility (§6)
The decision metric is computed "at report level" from `sharpe_pt`, `num_trades`,
`best_train_sharpe_pt`, sr_std pooled across the family's KELTNER rows. Attack: (1) is
the exact formula + pooling set written down precisely enough that two independent
implementers get the same number to 4 decimals? (2) sr_std pooled across 10m AND 1h rows
mixes horizons — legitimate? (3) the margin 0.10 in §7 lives on this scale — is 0.10
meaningfully large vs the metric's own noise, or decoration?

### F. CPCV gauntlet feasibility (§6) — Donchian lesson
At 1h with MIN_TRADES=30 and ~8,850 bars/symbol, estimate from EXISTING artifacts (Stage-1
1h rows' trade counts; Donchian eligibility failures) whether the CPCV Gate (median OOS >
0 ∧ pass rate ≥ 70%) is even computable — enough trades per purged fold combination?
FATAL-check: the pre-reg's outcome A requires the gauntlet, but if CPCV returns
0-eligible (as in Donchian), is the mapping A→A′ automatic and stated? If a confirming
cell gets CPCV N_A (not fail, not pass), which row of §10 applies? Ambiguity here = the
run cannot be mechanically scored.

### G. PBO/CSCV feasibility (§6)
PBO via CSCV needs the per-config return series matrix. With 12 configs and the engine's
existing outputs, is the CSCV input actually persisted per cell, or would PBO require a
re-run/extra artifact the pre-reg never budgets? `--max-combinations 100000` with which S
(number of splits)? Verify against the existing PBO tool's interface (read the tool; do
not run it).

### H. Confound rule falsifiability (§7)
Truth-table the four categories over all (bar_t, bar_f, du_t−du_f) combinations: are they
exhaustive and mutually exclusive? Nasty corners: bar(trail) fails on ALL cells but
bar(fixed_2R) clears on SOME (B′ per cell but precedence says?); different cells landing
in EXIT-INCREMENTAL and BASE-ONLY simultaneously; du undefined (INSUFFICIENT_TRADES on
exactly one mode of a twin pair). Verify §10's precedence resolves every mixed case with
zero judgment calls.

### I. Decision table completeness (§10) + STOP-rule interaction (§9)
Walk each STOP rule: does every firing map to E unambiguously mid-run vs pre-launch?
NO_DATA on one held-out symbol pre-launch (drop to 5) vs mid-run (row count ≠ 14 → E) —
consistent? Wall-clock cap ×1.5 from smoke: smoke is 1 of 14 cells with 12 configs × 2
modes — is the extrapolation formula stated (cells × smoke × margin) or left to taste?

### J. Gate hygiene
Scan the pre-reg for any sentence that could be read as pre-authorizing execution,
auto-promoting on outcome A (must stay "propose to Barış"), or leaving the runner script
spec (§5) loose enough to smuggle in changes (e.g., "imports and monkeypatches" — is the
assert list complete: grid content, stride absence, exit modes, symbol list, manifest
path?). Also: prereg was drafted BEFORE the bridge-parity registration merged into
`mega_walk_forward.py` (`BRIDGE_PARITY_STRATEGIES`, commit `6442b000` lineage) — confirm
that engine change cannot alter GEN_KELTNER_BREAKOUT Stage-2 behavior (default-run
isolation claim), citing code lines.

## DELIVERABLE

`MTC_COMMAND_CENTER/11_TRIAGE/CODEX_GATE5_FINDINGS_FAZ3B_STAGE2_2026-07-13.md`:

- One section per attack area A–J: verdict **OK / FINDING / FATAL** + evidence
  (file:line, JSON field values you actually read, arithmetic shown).
- **REQUIRED EDITS** list: numbered, each a concrete replacement sentence/table for the
  pre-reg (Fable applies them — write them apply-ready).
- **NICE-TO-HAVE** list: improvements that do not block D016.
- Honest "what I could not verify without running" section.
- No run was performed — state it explicitly.

Commit the findings file (+ nothing else) to `feature/faz3b-stage2-prereg` with the
inline pattern, then STOP. Fable synthesizes A–J into a recommendation for Barış; D016 is
his sentence alone. Update `GLOBAL_HANDOFF.md` with a dated
`## [Codex GPT-5] 2026-07-13 — Gate-5 adversarial review` section in the same commit.
