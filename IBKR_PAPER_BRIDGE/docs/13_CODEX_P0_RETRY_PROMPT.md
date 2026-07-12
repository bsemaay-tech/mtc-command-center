# 13_CODEX_P0_RETRY_PROMPT — F1/F2 fixes + approved P0 testnet smoke retry

Date: 2026-07-12. Author: Claude Opus 4.8 (post-audit of `11_P1_BUILD_REPORT.md` — P1 audited
PASS). Builder: Codex GPT-5. Branch: `feature/ibkr-bridge-final`.

Prereq reading: `10_CODEX_P1_BUILD_PROMPT.md` (§0 approvals, §1 rails — ALL still binding),
`11_P1_BUILD_REPORT.md`, `00_PREREG.md` §4 (P0 exit criteria).

---

## 0. Situation + authorization

- P1 was independently audited by Claude on real code and **PASSED**.
- The previous P0 attempt failed before connection: `HL_API_WALLET_KEY` contained the wallet
  ADDRESS (20 bytes). Barış has since generated a fresh dedicated agent-wallet private key and
  set it; Claude verified the format length-only: **66 chars = 0x + 64 hex = 32 bytes, VALID**.
  Codex was restarted, so the new value is inherited.
- **Barış's B2 approval STANDS** (recorded in `10_CODEX_P1_BUILD_PROMPT.md` §0): you are
  authorized to RUN the P0 smoke on TESTNET after completing the fixes below. Do not ask again.
- Claude's audit found two defects that must be fixed BEFORE the retry, because `flatten` is the
  smoke's safety net if the resting entry unexpectedly fills.

## 1. Hard rails (unchanged)

1. NEVER print, log, echo, or persist `HL_API_WALLET_KEY` (or any private key). You may check
   only existence/length. The smoke log must contain no key material — grep it before committing.
2. TESTNET ONLY. `HL_LIVE_ACK` stays unset; no mainnet code path may execute.
3. Order scope = exactly the bounded P0 smoke (§4): one tiny resting entry (~$11–12 notional,
   limit far below market so it cannot fill) + native SL trigger, one modify, then cancel all owned
   cloids; reduce-only flatten ONLY if a position unexpectedly appears.
4. Commit after every task with the inline pattern
   (`git checkout feature/ibkr-bridge-final && git add <paths> && git commit -m "..."`).
5. `PYTHONUTF8=1`; pytest green from BOTH repo root and `IBKR_PAPER_BRIDGE/` before any network step.
6. No LLM runtime calls, no backtests, no MCC edits, no Pine/parity actions.

## 2. Task F0 — key precheck (no network)

In the smoke script (or a tiny helper it calls), before building SDK clients: read
`HL_API_WALLET_KEY` from env, strip `0x`, assert `len == 64` and hex-decodable; on failure exit
with a clear message WITHOUT echoing any part of the value. Log only
`{"key_format": "valid_32_bytes"}`. Also assert `HL_ACCOUNT_ADDRESS` is 42 chars (`0x`+40 hex).

## 3. Task F1 — fix `flatten()` px=0 IOC (audit finding)

`bridge/broker/hyperliquid.py` `flatten()` currently submits `exchange.order(..., limit_px=0,
{"limit": {"tif": "Ioc"}})`. On the real exchange a BUY IOC at price 0 can never cross, so
closing a SHORT position silently no-ops — the safety net is broken for shorts.

Fix (pick per the INSTALLED SDK, verify with `inspect.signature` first):
- Preferred: use the SDK's `Exchange.market_close(...)` (it exists in `hyperliquid-python-sdk`
  0.24.0 and computes an aggressive slippage-bounded price itself), wrapped in
  `asyncio.to_thread`, passing our generated cloid if the signature allows.
- Fallback (if market_close is unsuitable): compute an aggressive crossing limit price from the
  latest known price — SELL to close a long: `px = market * (1 - slippage)`, BUY to close a
  short: `px = market * (1 + slippage)` with `slippage ≈ 0.05` — rounded to the coin's price
  tick, IOC, reduce_only=True.
- Unit tests (autospec fakes): long-close produces a SELL with a crossing (non-zero, below/at
  market) price; short-close produces a BUY with a crossing (above market) price; zero position
  → no order call.

## 4. Task F2 — fix modify_stop fallback dict pollution (audit finding)

`modify_stop()` fallback does `replacement = dict(spec)` and passes it to `bulk_orders`. The
stored spec includes the extra `"role"` key (and any other bookkeeping fields), which is not part
of the SDK `OrderRequest` shape and can break signing/validation on the real exchange.

Fix: build the replacement via the existing `_request(...)` helper (coin, is_buy, sz, limit_px=
new_stop, order_type=trigger, reduce_only=True, cloid) so ONLY OrderRequest keys are sent. Keep
the bookkeeping spec update as-is. Unit test: force the modify path to raise → assert the
re-placed request's key set equals exactly
`{coin, is_buy, sz, limit_px, order_type, reduce_only, cloid}`.

While there, sweep for the same bug class: any other place a stored spec dict is passed directly
to `bulk_orders`/`order` (e.g. reprotect paths) must also send clean `_request(...)` dicts only.

## 5. Task P0 — run the smoke (authorized)

After F0–F2 are committed and the full suite is green from both CWDs:

1. `PYTHONUTF8=1 python IBKR_PAPER_BRIDGE/tools/smoke_p0.py` (from repo root; use PowerShell so
   the Windows user env is inherited).
2. Expected step sequence per the existing script: key precheck → connect (testnet, log network +
   account ADDRESS only) → account snapshot → candles → meta/plan (entry = market×0.90 resting
   LMT, qty for ~$11.5 notional, szDecimals-rounded) → atomic `bulk_orders`
   `grouping="positionTpsl"` place → verify owned cloids visible in open_orders → modify SL
   trigger once → cancel all owned cloids → verify cleanup → flatten only if position size
   changed.
3. Log: `docs/p0_smoke_log.json` (overwrite the failed one). Before committing it, grep the file
   for hex strings ≥ 64 chars — must be zero matches.
4. If ANY step fails: stop, best-effort cancel owned cloids, record the failure honestly in the
   log, and report — do NOT retry in a loop, do NOT improvise extra orders.
5. One retry of the WHOLE script is allowed if the failure was clearly transient (network blip)
   AND no order from the failed run is still resting (verify open_orders first). Anything else →
   stop and report.

## 6. Task R — report for Claude audit

Write `docs/14_P0_SMOKE_REPORT.md`:
1. F0/F1/F2: what changed, file:line, new tests, full pytest summary pasted (both CWDs).
2. The complete `p0_smoke_log.json` inline, plus the testnet oids/cloids placed and cancelled.
3. Explicit confirmation: no key material in any log/commit (state the grep command used).
4. Any surprises from the REAL exchange responses vs the mocked assumptions (status shapes,
   open_orders payload fields, trigger order representation) — this list feeds the P2 readiness
   decision.
5. Honest remaining gaps + updated `03_STATUS.md` + dated `GLOBAL_HANDOFF.md` section.

P0 exit criteria (PREREG §4): connect + account + live candle + place entry & SL trigger group +
cancel, all steps in JSON log. P2 (unattended ARM) remains NOT approved — do not ARM the engine
on testnet.
