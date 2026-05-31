# Audited Data Usage Report

## Source data used by first-run backtests
First-run strategies/CANDIDATE_*/trades.csv all reference assets present in the local 5m research bundle (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, etc.).
Daily backtests resampled 5m → 1D (consistent with manifest).

## Proxy warnings
- CANDIDATE_002 (Martin Luke AVWAP) is US-equity native — tested on crypto daily proxy. Crypto-proxy result is NOT proof of US-equity edge.
- CANDIDATE_001 (Kell Wedge), CANDIDATE_007 (Linda 5SMA), CANDIDATE_005 (BigBeluga) are pattern-based and translate more cleanly to crypto, but proxy caveat still applies for native US-equity-only assumptions (catalyst, gap, sector RS).
- CANDIDATE_008 (8AM ORB) is session-specific to US opening — crypto 5m has no equivalent session, REJECT_CRYPTO_PROXY confirmed.
- CANDIDATE_009 (HighBeta) requires real US gap-and-go — crypto proxy WEAK only.

## Asset/timeframe sufficiency
All 8 audited weak/baseline candidates use ≥10 assets at 1D, satisfying the ≥5 assets minimum.
5m candidates (CANDIDATE_008/009) used 5 assets — at minimum threshold; recommended to expand to 10 in any rerun.

## DATA_BLOCKED list
- CANSLIM (real US daily + RS + fundamentals)
- Stan Weinstein stage analysis (real US equity / sector / breadth data)
- Ty Rajnus microcap short (US microcap intraday + borrow/locate/halt/dilution)
- Tito Adhikary options momentum (options chain with IV/OI/Greeks)
- Vibha Jha TQQQ swing (TQQQ daily with leverage decay model)