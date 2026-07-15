# 10_CODEX_P1_BUILD_PROMPT — Real P1 + P0 readiness build

Date: 2026-07-12. Author: Claude Opus 4.8 (merged from Claude + Codex GPT-5 independent audits of
the corrective pass). Builder: Codex GPT-5. Branch: `feature/ibkr-bridge-final`.

Prereq reading (do NOT redesign; build to spec): `00_PREREG.md`, `01_ARCHITECTURE.md`,
`02_BUILD_PLAN_1DAY.md`, `03_STATUS.md`, `05_AUDIT_RESOLUTION.md`.

---

## 0. Approvals granted by Barış (2026-07-12, in-session, recorded here)

Barış explicitly approved ALL of the following. This section is the authorization record — do not
ask again for these specific actions:

- **B1 — Read-only Hyperliquid TESTNET queries**: connectivity, `user_state`, open orders, candle
  snapshot, meta. Testnet only.
- **B2 — Run the completed P0 smoke on TESTNET**: place ONE tiny entry + native SL trigger group
  (`positionTpsl`), then cancel everything. Minimum viable notional (~$11–12, just above the $10
  exchange floor). Testnet only. Full JSON log required.
- **B3 — QuantLens golden run (read-only backtest)**: run the QuantLens engine on real BTC 1h crypto
  data to regenerate `tests/fixtures/golden_signals.json` and fill `golden_run_id` in the strategy
  YAML. Read-only with respect to MCC; never edit anything under `MTC_COMMAND_CENTER/`.
- **B4 — PREREG gate evidence**: produce P0 + P1 acceptance evidence. Actual P2 start (unattended
  10-day testnet ARM) remains a SEPARATE go decision after the audit of your report.

Process decision (resolves the Cline conflict raised by Codex): **direct Codex edits, NO Cline**
for this build — the bridge is safety-critical execution code, and AGENTS.md already forbids
routing trading-adjacent logic through Cline. Local mock server runs are allowed.

## 1. Hard rails (unchanged, non-negotiable)

1. NEVER print, log, echo, or persist `HL_API_WALLET_KEY` or any private key. Existence checks only.
2. NEVER touch Hyperliquid MAINNET. The triple-lock stays engaged (`HL_LIVE_ACK` must stay unset).
3. Testnet orders: ONLY within the P0 smoke scope of §0-B2 (one tiny bracket, then cancel; flatten
   if a partial fill leaves a position). No ARM'd autonomous trading in this build.
4. Never edit anything under `MTC_COMMAND_CENTER/` (read-only param/data lookup allowed for B3).
5. Preserve existing user changes; no destructive git (no reset --hard, no checkout -- on tracked
   files, no stash). Untracked dir `Youtube transcrip/` at repo root: leave untouched.
6. Repo hook flips HEAD back to master between tool calls — commit with inline
   `git checkout feature/ibkr-bridge-final && git add <exact paths> && git commit -m "..."` in ONE
   command. Commit after EVERY task.
7. Windows: run with `PYTHONUTF8=1`. Run pytest from the REPO ROOT (see task 9 for the fix).
8. LLM runtime calls (Grok regime / Claude veto) stay OFF — not part of this build's scope.

## 2. Environment facts (verified 2026-07-12)

- `HL_ACCOUNT_ADDRESS`: SET (Windows user env). `HL_API_WALLET_KEY`: SET. `XAI_API_KEY`: SET.
  `ANTHROPIC_API_KEY`: MISSING (fine — veto default-off). `HL_LIVE_ACK`: MISSING (correct).
- NOTE: a long-running process started BEFORE the vars were created will not see them — restart
  your shell/process if `os.environ` misses them. Bash subshells under Git Bash may not inherit
  Windows user env; PowerShell does.
- Installed: `hyperliquid-python-sdk 0.24.0`, `eth_account`, fastapi, uvicorn, pydantic v2, yaml,
  httpx, anthropic. Python 3.14.
- Testnet account: ~999 mock USDC, trading enabled, API wallet "MTC-bridge-test" authorized.
- Current test baseline: `37 passed` from repo root (`python -m pytest IBKR_PAPER_BRIDGE/tests -q`).

## 3. Build tasks (ordered; mock-first, network LAST)

### T1 — SDK contract correction (`bridge/broker/hyperliquid.py`) [BLOCKER]
Fix the adapter against the INSTALLED `hyperliquid-python-sdk 0.24.0` (verify signatures by
importing and inspecting the real SDK, not from memory):
- Bracket placement: one atomic `exchange.bulk_orders(orders, grouping="positionTpsl")` call —
  grouping is a `bulk_orders` argument, NOT a per-order `order_type` field. Entry (IOC market-style
  or GTC limit per plan) + SL trigger (`{"trigger": {"triggerPx": .., "isMarket": True, "tpsl": "sl"}}`,
  reduce_only) + optional TP trigger, each with a typed `Cloid`.
- `modify_order(...)`: pass the full required signature (oid/cloid, coin, is_buy, sz, px,
  order_type, reduce_only) changing ONLY the SL `triggerPx` — same cloid, price only, never qty.
  Fallback: cancel + re-place, log WARN.
- `cancel_by_cloid(coin, cloid)` — coin is required.
- Use the SDK's `Cloid` type (typed cloids), derived deterministically from `decision_uid:role`.
- Leverage init at connect: `exchange.update_leverage(1, coin, is_cross=False)` (isolated, lev=1).
- Rewrite the fake-SDK tests so fakes are DERIVED from real SDK method signatures
  (`inspect.signature` autospec-style) — a fake accepting a wrong call must be impossible.

### T2 — Typed normalization layer [BLOCKER]
Adapter must return protocol types, not raw dicts:
- `account()` → `AccountSnapshot` (equity USDC, available_margin, withdrawable) parsed from
  `user_state` (`marginSummary` etc.).
- `positions()` → `list[Position]` (symbol, size signed, entry_px, unrealized, leverage,
  liquidation_px, margin_used) from `assetPositions`.
- `open_orders()` → typed `BrokerOrder` rows (cloid, oid, coin, side, sz, trigger info).
- MockBroker returns the SAME types. Unit tests assert type parity across both brokers.

### T3 — Async safety
All sync SDK calls (`order`, `bulk_orders`, `user_state`, `candles_snapshot`, `modify_order`,
`cancel_by_cloid`, `update_leverage`) wrapped in `asyncio.to_thread` inside the async methods.
The engine event loop must never block on network I/O.

### T4 — BarFeed real implementation (`bridge/engine/bars.py` — currently a placeholder) [BLOCKER]
Per architecture §6.1 BarFinalizer contract:
- WS candle subscription (`{"type":"candle","coin":..,"interval":..}`); candle open-time `t` /
  close-time `T` tracked.
- **Wall-clock timer is the authority**: an asyncio timer fires at each UTC interval boundary and
  finalizes the previous bar even if no new candle message arrived (quiet market).
- Historical warmup via `candles_snapshot`.
- Reconnect loop: detect WS drop, backoff 5→60 s, re-subscribe candles + user events (subs do not
  survive drops), dedupe the first post-reconnect candle by bar_ts (idempotency guard: a decision
  for that bar_ts already exists ⇒ skip).
- `DATA_STALE` event when `now − last_bar_update > 2 × timeframe` ⇒ auto-DISARM per PREREG §7.

### T5 — OrderManager decoupling + user-event ingestion [BLOCKER]
- Remove all reads of mock internals (`broker.orders`, `broker.fills`) from
  `bridge/engine/orders.py`. Sync must go through Broker protocol methods only
  (`open_orders()`, `positions()`, plus a new fill/user-event callback subscription in the
  protocol implemented by both brokers).
- Subscribe to Hyperliquid user events (fills, order updates) over WS; each fill → `fills` row +
  order status transition (idempotent, keyed cloid+status, out-of-order tolerated).
- Reconciler (60 s async task): exchange truth vs DB; PENDING grace (exclude orders younger than
  2× interval); match cloid → order_ref → conservative attributes; naked OWNED position ⇒
  re-protect first (re-submit SL/TP trigger group), flatten only if re-protect fails; FOREIGN
  positions never touched — WARN banner event only. Equity snapshot every 60 s into `equity`.

### T6 — Engine runtime: continuous loop + broker factory [BLOCKER]
- `create_app` gets a broker factory: `mode=dry_run` → MockBroker replaying the fixture on an
  accelerated async clock (config speed); `mode=paper` → HyperliquidBroker on TESTNET. The current
  one-shot `_preload_dry_run` static snapshot is REPLACED by a real background engine task started
  in FastAPI lifespan, pushing live updates.
- Startup state: **DISARMED** (never auto-ARM). Persisted KILLED still wins (existing behavior).
- **Reconcile-before-ARM**: ARM endpoint refuses (409 + reason) until the startup reconcile pass
  completes clean.
- Engine on_bar per §5: step-0 fresh position read; post-await state gate (already exists — keep);
  engine-driven trail: each bar close compute `strategy.trail_level`, `modify_stop` price-only;
  trail CONTINUES while DISARMED with open position (risk-reducing).
- Opposite-signal close sequence (flip disabled): cancel trigger group → reduce-only MKT close
  sized to live qty → no new entry this bar.
- Act on RiskEngine `disarm=True` results (daily-loss breach ⇒ auto-DISARM + event; today it is
  computed but ignored).
- KILL: cancel ALL orders (+ optional flatten), preemptive flag short-circuits in-flight decisions.

### T7 — API + WS real wiring [BLOCKER]
- ARM/DISARM/KILL/kill-ack endpoints operate the ACTUAL engine/broker (state change + side effects
  per §5), not just stored labels.
- `/api/positions|orders|trades|decisions|equity|events|bars|snapshot|gates/latest` serve real
  Store/engine data (no placeholders).
- WS hub: persistent connections; snapshot pushed on open; topic pushes (`status`, `bar`,
  `decision`, `order`, `position`, `equity`, `event`) on engine activity; monotonic
  `state_version` on status. KILL/DISARM never nonce-blocked; ARM + config PUT require
  `X-Confirm: <state_version>`.

### T8 — P1 failure drills (integration tests, MockBroker) [P1 GATE EVIDENCE]
Scripted drills, each an automated test:
1. Disconnect mid-run → reconnect → resubscribe → dedupe replayed bar → exactly one order.
2. Duplicate candle delivery → one decision, one order (fingerprint guard).
3. Order reject from broker → decision chain records REJECTED, engine continues, 3 consecutive
   rejects ⇒ DISARM (PREREG §7).
4. LLM gate timeout → `LLM_SKIPPED`, formal rule proceeds, loop never blocks.
5. DISARM/KILL arriving mid-await → no submit (exists — keep + extend to KILL preemption).
6. Naked owned position → re-protect first, flatten on re-protect failure.
7. Foreign position present → never adopted/flattened; WARN event emitted.
8. DATA_STALE (no bars 2×tf) → auto-DISARM + event.

### T9 — Test CWD robustness
Resolve fixture paths relative to the test file (`Path(__file__).parent / "fixtures" / ...`), not
the CWD. Suite must pass from both repo root and `IBKR_PAPER_BRIDGE/`.

### T10 — Dashboard chart fix (minor)
Bundle lightweight-charts as a LOCAL static asset (no CDN dependency) or keep the SVG fallback as
the primary path — either is acceptable; pick one, delete the dead path, verify with a screenshot
saved to `docs/screenshots/`.

### T11 — P0 smoke completion + RUN (approved §0-B2) [NETWORK — LAST, after all tests green]
Complete `tools/smoke_p0.py` to the full PREREG P0 exit criteria, then RUN it on testnet:
1. Connect (log network + resolved account address — the ADDRESS is fine to log, never the key).
2. Account summary (typed AccountSnapshot).
3. Live BTC candle snapshot (last 3 bars logged).
4. Place ONE minimal bracket: entry LIMIT far from market (so it rests, does not fill) + SL trigger
   via atomic `bulk_orders(grouping="positionTpsl")`, notional ~$11–12.
5. Verify both orders visible in `open_orders()` with our cloids.
6. Modify the SL trigger price once (proves T1 modify path).
7. Cancel all our cloids; verify open_orders clean.
8. If ANYTHING fills partially: reduce-only flatten immediately, log it.
9. Every step appended to a JSON log at `docs/p0_smoke_log.json` (no secrets). Non-zero exit on
   any failed step.

### T12 — Golden regen (approved §0-B3)
Run the QuantLens engine READ-ONLY on real BTC 1h crypto data (data inventory:
`MTC_COMMAND_CENTER\03_QUANTLENS\data\README.md`; set `MEGA_BUNDLE_MANIFEST` accordingly) for
`keltner_trail_ema8`, apply the documented bridge execution transform (02_BUILD_PLAN task 3b),
regenerate `tests/fixtures/golden_signals.json`, fill `golden_run_id` in
`config/strategies/keltner_trail_ema8.yaml`, and make `test_strategy` pass against the REAL golden.
If the QuantLens run is infeasible (data/tooling blocker), do NOT fake it — document the exact
blocker in the report and keep the provisional file clearly labeled provisional.

### T13 — Status + handoff
Update `docs/03_STATUS.md` honestly (done/partial/blocked per task) and append a dated section to
the repo `GLOBAL_HANDOFF.md` per repo convention (`## [Codex GPT-5] 2026-07-12 — Bridge P1 build`).

## 4. Acceptance (whole build)

- `PYTHONUTF8=1 python -m pytest IBKR_PAPER_BRIDGE/tests -q` green from repo root AND from
  `IBKR_PAPER_BRIDGE/` (T9).
- Dry-run mode: `python -m bridge.app --dry-run` serves a LIVE-updating dashboard (equity draws,
  decisions stream over WS while replay runs) — screenshot evidence.
- All 8 failure drills pass (T8).
- P0 smoke JSON log shows all 9 steps green on testnet (T11).
- No secrets in any log, commit, or report. No mainnet call anywhere.

## 5. Deliverable: audit report

Write `docs/11_P1_BUILD_REPORT.md` for Claude to audit. Required contents:
1. Per-task status table (T1–T13: DONE / PARTIAL / BLOCKED + one-line evidence pointer).
2. Exact commands run + full pytest summary output (paste, don't summarize).
3. P0 smoke: the full JSON log inline + the testnet oids/cloids involved.
4. SDK-contract proof: for each corrected call (bulk_orders/modify/cancel), the real SDK signature
   (from `inspect.signature`) next to your call site.
5. Golden regen: run command, bundle/manifest used, signal count, `golden_run_id` — or the honest
   blocker.
6. Honest remaining-gaps list (anything cut, stubbed, or weaker than this spec).
7. Commit list (hash + message) for the build.

Claude audits this report against the code on real data — do not expect the report to be taken on
trust; make every claim checkable.
