# 08 — CODEX OVERNIGHT BUILD PROMPT (autonomous, no human input)

> Copy everything below the line into Codex (or point Codex at this file: "Read
> IBKR_PAPER_BRIDGE/docs/08_CODEX_BUILD_PROMPT.md and execute it"). Written 2026-07-06 by
> Claude (Fable 5), authorized by Barış for a fully autonomous overnight run.

---

## MISSION

You are building the **Crypto Paper Bridge (Hyperliquid)** v1 — a standalone paper-trading
execution engine + professional web dashboard — in repo `C:\LAB\Tradingview_LAB_CLEAN`, directory
`IBKR_PAPER_BRIDGE/` (legacy name, kept for git continuity).

**You will work AUTONOMOUSLY until the build is complete or your session/credits end. The user is
ASLEEP. Never stop to ask a question. Never wait for input. Every ambiguity has a resolution
protocol below — use it and keep moving.**

## STEP 0 — read these, in this order (all under `IBKR_PAPER_BRIDGE/`)

1. `README.md` — product + 8 non-negotiable principles.
2. `docs/00_PREREG.md` — gates, metrics, abort criteria (binding).
3. `docs/01_ARCHITECTURE.md` — THE spec. Every section is decided. Build exactly this.
4. `docs/05_AUDIT_RESOLUTION.md` — read the broker note at top + skim; explains why the spec says
   what it says.
5. `docs/02_BUILD_PLAN_1DAY.md` — your task list (1 → 11) with acceptance criteria.
6. `docs/07_BROKER_DECISION.md` — why Hyperliquid; do not re-litigate.
7. `docs/06_HYPERLIQUID_SETUP.md` — account prep (user does this later; you do NOT need keys).

## HARD RULES (violating any of these is failure)

1. **NO REDESIGN.** `01_ARCHITECTURE.md` is final: stack (Python 3.11+, FastAPI, SQLite,
   `hyperliquid-python-sdk`, vanilla JS dashboard, no npm/build step), schema v2 exactly as §7,
   API exactly as §8, config exactly as §10. Locked decisions you must not undo: testnet default +
   mainnet triple-lock; leverage cap 1; native `positionTpsl` SL/TP triggers; `cloid` identity;
   UTC 24/7 (no RTH/calendar); `decision_uid` grouping; LLM veto DEFAULT OFF (NullLLMGate);
   flip DISABLED; DISARMED keeps trail updating; KILL never nonce-blocked.
2. **NO NETWORK CALLS TO THE EXCHANGE OR LLM APIs. EVER — not even testnet.** The user has NOT
   provisioned keys, and exchange actions are approval-gated by repo protocol. Everything runs
   against `MockBroker` and stubbed HTTP. Task 8's `HyperliquidBroker` is built and UNIT-tested
   (mock the SDK client); its integration smoke (`tools/smoke_p0.py`) is WRITTEN but NOT RUN.
   `pip install` of dependencies is fine (that's PyPI, not the exchange).
3. **NEVER touch** `MTC_COMMAND_CENTER/` protected scopes (`01_PINE`, `02_MTC_BACKTEST`,
   `07_ADAPTERS`, `MTC_V2`) or any `*.pine`. Read-only access to `MTC_COMMAND_CENTER/03_QUANTLENS/`
   data/tools is allowed for fixtures (task 3/3b). Do not run backtests/optimizations.
4. **Git discipline:** work on branch `feature/ibkr-bridge-final`. A repo hook may auto-revert HEAD
   to master between commands — therefore EVERY commit is one inline command:
   `git checkout feature/ibkr-bridge-final; git add <exact file paths>; git commit -m "..."`.
   Stage EXACT paths only — **never `git add .` / `-A`**. Never commit to master. Never push.
   Never run `git checkout HEAD -- <file>` / `git reset` / `git stash` on tracked files —
   uncommitted work by prior agents would be destroyed.
5. **Commit after EVERY completed task** (conventional message, e.g.
   `feat(bridge): task 5 — RiskEngine + tests`). Also commit progress before attempting anything
   risky.
6. Secrets: never hardcode any key; env-only via `settings.py`. `data/` stays git-ignored.
7. Windows environment: set `PYTHONUTF8=1` for every python invocation; write files UTF-8; avoid
   emoji in code/comments.

## AUTONOMOUS DECISION PROTOCOL (instead of asking)

- Ambiguity in the spec → choose the SAFEST interpretation consistent with
  `01_ARCHITECTURE.md`, implement it, and append a dated bullet to `IBKR_PAPER_BRIDGE/docs/03_STATUS.md`
  ("DECIDED: <what> because <why> — flag for review").
- A task's acceptance test fails repeatedly → max **5 fix attempts**, then: mark the specific test
  `xfail` with a reason, log it in `03_STATUS.md` under "KNOWN GAPS", commit, and MOVE ON. Never
  spin >30 min on one failure.
- A dependency can't install (e.g. `hyperliquid-python-sdk` build issue on Windows) → implement
  against a thin adapter interface of the SDK's documented surface (`Info`, `Exchange`,
  `candles_snapshot`, `user_state`, `order`, `modify_order`, `update_leverage`, WS subscribe),
  stub it in tests, log in `03_STATUS.md`. The engine must not care.
- Task 3b (golden generation) — try the QuantLens engine read-only per the task. If the engine run
  is infeasible tonight (env/data friction), FALLBACK: generate the golden from an independent,
  clean reference implementation of the Keltner rule (separate file, not the production strategy
  class) on real BTC 1h bars, mark it `PROVISIONAL` in `03_STATUS.md` and inside
  `golden_signals.json` (`"provisional": true`). Do NOT let this block tasks 4-11.
- Real BTC 1h fixture data: look for crypto CSV/Parquet under
  `MTC_COMMAND_CENTER/02_MTC_BACKTEST/data/` (read-only!) or
  `MTC_COMMAND_CENTER/03_QUANTLENS/research/data_acquisition_5m_2026_05_03/` (5m → resample to 1h).
  If nothing loads cleanly in 20 min, SYNTHESIZE ~2000 bars (trending + ranging + gap segments) and
  mark fixture synthetic in `03_STATUS.md` (fills mechanics don't care; provisional golden then
  comes from the reference impl).

## EXECUTION ORDER

Run build-plan tasks **1 → 2 → 3 → 3b → 4 → 5 → 6 → 7 → 9 → 10a → 10b → 8 → 11**.
(Deviation from the doc's day split, deliberate: LLM gate (9) and the full dashboard (10a+10b)
before the HyperliquidBroker (8), because 8 cannot be integration-verified tonight anyway —
this maximizes what the user can SEE and RUN in the morning.)

Per task: implement → run `PYTHONUTF8=1 python -m pytest IBKR_PAPER_BRIDGE/tests -q` → fix until
green (or protocol above) → commit → next.

**Definition of DONE for tonight (in priority order):**
1. `pytest IBKR_PAPER_BRIDGE/tests -q` fully green (xfails allowed only per protocol).
2. **Dry-run demo works:** `python -m bridge.app --dry-run` starts, replays the fixture through
   MockBroker, dashboard at `http://127.0.0.1:8790` shows live equity curve, decisions stream,
   Gate Monitor, journal with a complete decision chain. Verify yourself with an HTTP check of
   `/api/snapshot` + `/api/bars` (and a headless page fetch if available). THEN STOP THE SERVER.
3. All 6 dashboard pages per §9, professional dark theme per the spec's palette.
4. `HyperliquidBroker` complete + unit-tested (SDK mocked), network-lock test proves mainnet
   refusal, `tools/smoke_p0.py` written (not run).
5. `docs/03_STATUS.md` written; handoff updated (below).

## IF YOU FINISH EARLY (all 13 tasks done, tests green)

Do these, in order, committing each:
1. Re-run the FULL test suite 3×; fix any flakes (determinism matters).
2. Self-review pass: walk `01_ARCHITECTURE.md` §5/§6/§7/§8/§11 as a checklist against the code;
   fix every deviation you find; log the review in `03_STATUS.md`.
3. Harden MockBroker edge cases: gap-through-stop fill, same-bar SL+TP hit (SL priority),
   partial-fill path, reconnect-replay duplicate bar. Add tests.
4. Add `tools/replay_report.py`: after a dry-run, print per-trade table (PREREG §5 fields) from
   the DB. Nice morning artifact.
5. Polish dashboard empty/error states + screenshots into `docs/screenshots/` if you have a
   headless browser; else skip screenshots.
Never invent new features beyond this list; never start v1.1 roadmap items.

## END-OF-RUN HANDOFF (do this even if incomplete — budget the last ~15 min for it)

1. Write/finalize `IBKR_PAPER_BRIDGE/docs/03_STATUS.md`: tasks completed (w/ commit hashes),
   known gaps/xfails, decided ambiguities, exact command to run the dry-run demo, what a human
   must do next (testnet wallet per 06, approve P0).
2. Append a section to `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` at the TOP (below the
   `# GLOBAL_HANDOFF` line), header format:
   `## Codex GPT-5 2026-07-07 — Crypto Paper Bridge overnight build (tasks X-Y done)` — 5-10 line
   summary.
3. Update the `🚀 CRYPTO PAPER BRIDGE` section of `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`:
   strike done items, add remaining ones tagged `[AI: Codex|Claude]` / `[AI: Barış]`.
4. Final inline commit of all of the above on `feature/ibkr-bridge-final`.

## MORNING ACCEPTANCE (what the user will check — make these true)

- `git log --oneline feature/ibkr-bridge-final` shows one commit per task.
- `PYTHONUTF8=1 python -m pytest IBKR_PAPER_BRIDGE/tests -q` → green.
- `python -m bridge.app --dry-run` → dashboard alive at 127.0.0.1:8790 with data on every page.
- `docs/03_STATUS.md` tells the whole story.

Begin now. Read the docs (STEP 0), then execute task 1. Do not ask anything. Do not stop.
