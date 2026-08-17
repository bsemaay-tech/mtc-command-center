# Gate-1 Scope Record — Package 2: MTC Integration Contract Pack

**Date:** 2026-08-17 night · **Lead:** Claude (Fable) · **Tier: T2, documentation only**
**Owner authorization:** in chat 2026-08-17 night ("start packages 1+2"), recorded as Decision 5
in `OWNER_DECISIONS_BRIDGE_V2_BACKLOG_NIGHT_2026-08-17.md`.
**Accepted source:** `BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` §4 Package 2, §5 item 2
(accepted per `BRIDGE_V2_DEFERRAL_BACKLOG_T2_ACCEPTANCE_2026-08-17.md`).

## Frozen scope

One contract pack that: (a) freezes `OrderIntent`/`ExitIntent` schemas, Multi-TP, basket/add,
and stop semantics; (b) defines desired/accepted/actual-state schemas; (c) resolves or
explicitly lists as OPEN every Pine/Python sizing and lifecycle parity gap named by the accepted
backlog (§3 rows "MTC sizing ownership and `OrderIntent`", "MTC exit lifecycle, Multi-TP and
basket/add support", relaying `docs/30(HEAD):488-517,589-599,644-733,799-806,860-886`).

Documentation only; no runtime wiring; no edits to MTC, Pine, TradingView parity surfaces, or
strategy logic. Contract text governs a FUTURE separately-gated T0 implementation; nothing here
activates. The backlog precedence rule holds: this contract must exist before even the first
MTC-connected worker.

## Roles and review

- Implementer: GLM-5.3 (sub-delegation; reads `bridge/engine/types.py` and cited docs read-only).
- T2 review: DeepSeek (`deepseek-v4-pro`), one round, medium — different provider from author.
  Gemini read-only route as supplemental cross-check.

## Out of scope / prohibited

Runtime wiring, MTC/Pine/parity/strategy edits, order/broker/exchange contact, and the standing
prohibition list (VPS/host, credentials, TESTNET/MAINNET, ARM/orders, frozen-V1 mutation).
