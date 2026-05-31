# Data Proxy Warning Report

All swing/day-trade strategies were tested on **crypto futures only**. Where the native asset class is US equity, US microcap, or options, this means:

- Crypto-proxy results are advisory; they are NOT proof of edge in the strategy's native market.
- Specifically affected: CANDIDATE_002 (Martin Luke AVWAP — US-equity native), CANDIDATE_009 (HighBeta — US-equity native), CANDIDATE_008 (8AM ORB — US session native).
- Strategies whose logic is asset-class-agnostic (Crabel range expansion, EMA pullbacks, RSI patterns) translate more cleanly to crypto, but still inherit different volatility/skew characteristics.
