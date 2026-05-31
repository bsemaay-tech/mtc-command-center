# Classification Audit Report

## 1. Scope
Review of Codex's master candidate classification to ensure strategies, wisdom, processes, and modules are correctly categorized.

## 2. Findings
Overall, Codex classified the majority of candidates correctly. However, we found several instances where purely psychological or process-oriented videos were incorrectly flagged as `SWING_TRADE_STRATEGY`, and instances where timeframe definitions were slightly misaligned.

**Incorrectly Classified as Strategy (Should be Wisdom/Process):**
- `QLR_-JyH5PAJ4-Y` (I Stopped Trading So Much and My Profits Skyrocketed) - Classified as SWING_TRADE_STRATEGY.
- `QLR_q4TuaY-ccqA` (FOMO is Ruining Your Trades) - Classified as SWING_TRADE_STRATEGY.
- `QLR_UtNrp_Uz9Oc` (Trading The Mental Game Jared Tendler) - Classified as SWING_TRADE_STRATEGY.

**Potential Timeframe Misclassifications:**
- `QLR_62OaP91Jz9k` (120% Return A Simple Weekly Strategy Anyone Can Use) - Classified as POSITION_TRADING_STRATEGY. Weekly strategies with simple rotation are often swing trades.
- `QLR_MnXQOt7_ZP0` (+85% Return in 30 Days...) - Classified as POSITION_TRADING_STRATEGY. A 30-day hold is typically a SWING_TRADE_STRATEGY.
- `QLR_4-IjRmw7SZI` (The Reality of Trading TQQQ) - Classified as DAY_TRADE_STRATEGY. TQQQ is frequently swing-traded; requires verification of the transcript to ensure it's strictly intraday.

## 3. Recommended Repairs
Codex must re-evaluate and reclassify the identified candidates according to the provided CSV. Psychology and process videos must be strictly routed to the Trader Wiki and removed from the strategy backtesting pipeline.
