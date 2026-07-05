# Audit — IBKR Paper Bridge design
Model: Gemini 3.1 Pro | Date: 2026-07-05 | Docs commit: c2c3bbb0

## 1. Summary verdict
**Ship-with-fixes**. The architecture provides a solid, safe foundation with an excellent logging schema and a clear state machine. However, the order manager lacks critical logic for IBKR's automatic proportional reduction of attached OCA child orders on partial fills, the mathematical risk formula will crash on a zero stop distance, and the one-day build estimate is deeply unrealistic for the frontend scope.

## 2. Findings

| ID | Severity | Dimension A-I | Location doc§ | Issue | Suggested fix |
|---|---|---|---|---|---|
| F-01 | CRITICAL | C. Risk engine | 01_ARCH §6.3 | Zero stop distance causes a `DivisionByZero` error in `qty = floor(risk_dollars / stop_distance)`. | Clamp `stop_distance` to `max(stop_distance, min_tick)` or reject signal if `stop_distance <= 0`. |
| F-02 | HIGH | B. State machine | 01_ARCH §6.5 | "cancel remainder, keep SL sized to filled qty (modify)". IBKR auto-scales OCA child orders when a parent is partially filled and cancelled. Manually modifying the child's qty creates a race condition with IBKR's own scaling, leading to rejection or incorrect sizes. | Rely on IBKR's auto-scaling for child orders on parent cancel; only modify the stop *price*, never the *qty* manually unless adopting a naked position. |
| F-03 | HIGH | A. Broker/API | 01_ARCH §6.1 | `reqHistoricalData(keepUpToDate=True)`: detecting a "NEW bar object" to finalize the previous bar often misses the last tick of the previous bar if relying purely on list length changes in `updateEvent`. | Use a local clock or `ib.pendingTickersEvent` to precisely snap the final state of a bar exactly at the top of the hour, rather than waiting for the next bar's first tick. |
| F-04 | HIGH | I. Build plan | 02_BUILD | The 1-day estimate is wildly unrealistic for a 6-page, WebSocket-driven, real-time vanilla JS dashboard (Task 10, 150m) and the complexities of the IBKR adapter (Task 8, 90m). | Cut v1 dashboard scope to 1-2 pages (Overview + Trading) to fit the time budget, moving Journal and System to v1.1. |
| F-05 | MEDIUM | E. Data | 01_ARCH §7 | PREREG §5 requires per-trade `signal_ts`, `decision_ts`, `submit_ts`, `fill_ts`, `expected_px`, `SL`, `TP`, and `llm_directive`. The `trades` schema only has `entry_ts` and `exit_ts`. Reconstructing them requires complex JSON extraction. | Add the missing columns directly to the `trades` table for fast querying and explicit adherence to PREREG. |
| F-06 | MEDIUM | D. LLM gate | 01_ARCH §6.4 | Grok sentiment based on "news/X" is highly susceptible to cashtag spam/prompt injection, potentially forcing unwanted NO_TRADE regimes based on manipulated data. | Filter X sentiment through a strict whitelist of authoritative accounts, or rely purely on broad market ETF action. |
| F-07 | LOW | F. Dashboard | 01_ARCH §8 | `/api/status` returns `X-Confirm` nonce, but if multiple tabs are open, they might race or use stale nonces for dangerous ops. | Ensure WS broadcasts nonce invalidations, or use a short-lived TOTP-style nonce instead of a state-bound one. |
| F-08 | LOW | B. State machine | 01_ARCH §5 | "close-then-open only if config allow_flip... Close = reduce-only semantics". If flipping, submitting both synchronously risks a margin violation or order rejection. | Explicitly document that flips require synchronous waiting for the close to fill before submitting the open, or hardcode `allow_flip: false` for v1. |

## 3. Dimension notes
- **A. Broker/API correctness**: IBKR's API is notoriously asynchronous and eventually consistent. Bracket order child IDs are sometimes not available immediately upon parent submission. Handling `keepUpToDate` bars requires extreme care with timestamp boundaries.
- **B. State machine & concurrency**: The ARMED/DISARMED states are clear, but the flip logic (close-then-open) is dangerous if executed synchronously without waiting for the close to fill.
- **C. Risk engine math & completeness**: Strong foundation with strict clamps. The division by zero is a classic edge case. Daily loss accounting must accurately reflect IBKR's day boundary (typically 17:00 ET), which should be explicit in the config.
- **D. LLM gate**: The narrow "veto/regime only" scope is an excellent safety boundary. However, relying on Grok for X sentiment opens the regime to manipulation via cashtag spam.
- **E. Data & persistence**: The SQLite schema is robust and the JSON audit payload is a great idea for the "thesis history". However, it lacks a few explicit timestamps for the PREREG reporting.
- **F. Dashboard & API**: The design is beautiful and comprehensive, but "no build step" Vanilla JS for 6 dynamic pages is a maintenance nightmare and too large for an LLM to build in 150m.
- **G. Security**: The localhost assumption holds for v1. If exposed later, API keys and config endpoints need strict authentication.
- **H. PREREG soundness**: Gates are logical. Signal parity >= 95% is a very strict bar given inevitable data feed differences (IBKR paper vs QuantLens Alpaca bundle).
- **I. Build plan feasibility**: The order of tasks is logical (mock-first), but the time estimates for the dashboard and IBKR adapter are overly optimistic by at least a factor of 3.

## 4. Improvements
1. **Clamp Stop Distance (Risk Engine)**
   - *What*: Add a safeguard to prevent `stop_distance` from being zero or negative.
   - *Why*: Prevents division by zero and infinite position sizing if the strategy emits a stop loss exactly at the reference price.
   - *Cost*: S
   - *Amends*: 01_ARCHITECTURE.md §6.3
   - *Fit*: v1
2. **Dashboard Scope Reduction (Build Plan)**
   - *What*: Limit the dashboard to the Overview and Trading pages for the initial build.
   - *Why*: 6 complex Vanilla JS pages cannot be reliably generated and styled by an LLM in 150 minutes without extensive debugging.
   - *Cost*: S (reduces effort)
   - *Amends*: 01_ARCHITECTURE.md §9, 02_BUILD_PLAN_1DAY.md Task 10
   - *Fit*: v1
3. **Explicit Timestamp Columns in Trades Table (Schema)**
   - *What*: Add `signal_ts`, `decision_ts`, `submit_ts`, `fill_ts`, `expected_px`, `SL`, `TP`, and `llm_directive` to the `trades` table.
   - *Why*: Fulfills PREREG §5 metrics requirements without requiring complex JSON unrolling during analysis.
   - *Cost*: S
   - *Amends*: 01_ARCHITECTURE.md §7
   - *Fit*: v1
4. **IBKR Auto-Scaling Awareness (Order Manager)**
   - *What*: Remove logic that manually modifies child order quantities on partial fills.
   - *Why*: Manually modifying child order quantities when cancelling a partial parent order will clash with IBKR's native bracket OCA auto-scaling, causing rejects.
   - *Cost*: M
   - *Amends*: 01_ARCHITECTURE.md §6.5
   - *Fit*: v1
5. **Disable Flip Logic for v1 (State Machine)**
   - *What*: Hardcode `allow_flip: false` for the initial version.
   - *Why*: Executing a "close-then-open" safely requires a complex state transition (waiting for close to fill before sizing and submitting open). Synchronous submission risks margin violation.
   - *Cost*: S
   - *Amends*: 01_ARCHITECTURE.md §5, §10
   - *Fit*: v1

## 5. Feature ideas
1. **Slippage & Fill Latency Heatmap**
   - *User Value*: Helps a systematic trader visualize time-of-day or volatility-based execution costs, directly informing strategy parameter choices in MCC.
   - *Cost*: M
   - *Phase*: v1.1
   - *Risk*: None (read-only visualization).
2. **Auto-DISARM on Data Feed Disconnect**
   - *User Value*: Prevents the bridge from running blind if IBKR market data disconnects but the API connection remains up (a common IBKR issue).
   - *Cost*: S
   - *Phase*: v1.1
   - *Risk*: Might cause false-positive DISARMs, requiring manual intervention to re-arm.
3. **Ghost / Shadow Trading Mode**
   - *User Value*: Run the strategy against live market data, log all decisions and simulated fills internally, but do not send orders to IBKR. Useful for bridging the gap between backtest and paper.
   - *Cost*: M
   - *Phase*: v1.1
   - *Risk*: None (prevents real orders).
4. **Continuous Target Position Rebalancing**
   - *User Value*: Instead of strictly "entry/exit brackets", the engine queries desired position size from the strategy and submits limit orders to reach that size, natively handling partial fills and flips.
   - *Cost*: L
   - *Phase*: v2
   - *Risk*: High. Requires completely rewriting the OrderManager and abandoning simple bracket semantics.
5. **Margin / Buying Power Pre-Check**
   - *User Value*: Validates that the requested order size won't trigger an immediate margin rejection, especially useful when transitioning to live trading with multiple assets.
   - *Cost*: M
   - *Phase*: v1.1
   - *Risk*: Low (additional safe-guard).

## 6. Top-3 verdict
1. **Fix the Division-by-Zero Risk (F-01)**: If a strategy anomaly or data spike causes `ref_price` to equal `stop_loss`, the `RiskEngine` will crash the entire loop. Clamping the stop distance to a minimum tick size ensures the bridge stays alive and correctly rejects the trade via the "max notional" or "size below minimum" clamps instead of an unhandled exception.
2. **Align Bracket Logic with IBKR Realities (F-02)**: IBKR's server-side OCA handling is powerful but unforgiving. Attempting to manually modify child order quantities on a partial fill will create race conditions with IBKR's own auto-scaling. The `OrderManager` must be updated to modify only prices, or rely entirely on IBKR's handling of the remainder cancel.
3. **Reduce v1 Dashboard Scope (F-04)**: The 1-day build plan assumes an LLM can flawlessly write a professional, multi-page, WebSocket-driven application in pure Vanilla JS in 2.5 hours. This will inevitably derail the build day into CSS/DOM debugging. Reduce the v1 UI to a single overview page, focusing purely on getting the execution engine to P0/P1.
