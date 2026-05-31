# Visual Review Checklist

## 1. First Chart

- Open TradingView.
- Use a liquid intraday US equity chart first if available.
- Start with 5m timeframe.
- Use charts where a strong intraday trend, capitulation flush, or news/catalyst move is visible.

## 2. Expected Setup

- Trend continuation: price above VWAP, not compressed, breaking out of recent range.
- Right-side-of-V: sharp downside capitulation first, then a confirmed prior-bar-high break.
- No-man's-land: compressed/range-bound price around VWAP should not fire signals.

## 3. Marker Meaning

- Green `L`: raw long pulse.
- Red `S`: raw short pulse.
- Orange `cap`: capitulation proxy.
- Gray `range`: compression/no-man's-land guard.
- Blue line: session VWAP.
- Red line: active debug stop.
- Green line: optional visual take profit.

## 4. Entry Marker Check

- PASS if long marker appears after trend alignment or after a confirmed right-side turn.
- FAIL if long marker appears repeatedly below VWAP without capitulation.
- NEEDS_RULE_CLARIFICATION if chart context requires news/catalyst interpretation not visible from OHLCV.

## 5. Exit Marker Check

- PASS if debug stop follows prior-bar low/high behavior.
- FAIL if active stop uses future bars or jumps before the prior bar completes.
- NEEDS_RULE_CLARIFICATION if discretionary exit is needed.

## 6. Known Limitations

- No news feed.
- No halt/liquidity modeling.
- No tape reading.
- No profit claim.
- No optimization.
- Short side is symmetric proxy only.

## 7. Decision

- `PASS_VISUAL`: markers match expected source behavior on multiple charts.
- `FAIL_VISUAL`: markers contradict source behavior.
- `NEEDS_RULE_CLARIFICATION`: source requires discretionary/catalyst context before coding further.
