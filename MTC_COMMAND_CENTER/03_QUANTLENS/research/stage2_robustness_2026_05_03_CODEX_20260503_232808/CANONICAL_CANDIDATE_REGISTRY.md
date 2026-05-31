# Canonical Candidate Registry

|candidate_id|name|aliases|horizon|native_asset_class|native_timeframe|data_status|eligible|reason|
|---|---|---|---|---|---|---|---|---|
|KELL_WEDGE|Kell Wedge Pop / EMA Crossback|CANDIDATE_001|SWING|crypto_proxy|1D|available_crypto_daily|True|mechanical and local OHLCV available|
|SLINGSHOT|Slingshot EMA(high,4) Pullback|CANDIDATE_003|SWING|crypto_proxy|1D|available_crypto_daily|True|mechanical and local OHLCV available|
|CRABEL|Crabel Range Expansion|CANDIDATE_004|SWING|crypto_proxy|1D|available_crypto_daily|True|mechanical and local OHLCV available|
|BIGBELUGA|BigBeluga RSI Divergence + CHoCH + ATR|CANDIDATE_005|SWING|crypto_proxy|1D|available_crypto_daily|True|mechanical proxy available; pivot delay required|
|LINDA_5SMA|Linda 5SMA RS Pullback|CANDIDATE_007|SWING|crypto_proxy|1D|available_crypto_daily_rs_proxy|True|mechanical proxy available; RS proxy caveat|
|MARTIN_LUKE|Martin Luke Pullback / AVWAP|CANDIDATE_002|SWING|equity_native_crypto_proxy|1D|available_crypto_daily_proxy|True|AVWAP anchor formalized mechanically|
|LBR_COIL|LBR Coil Breakout / IDNR4|QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0|DAY|crypto_proxy|5m|available_crypto_5m|True|Antigravity conflict candidate; mechanical 5m test required|
|HIGHBETA_PROXY|HighBeta Opening Bar Gap-and-Go|CANDIDATE_009|DAY|us_equity_native_crypto_proxy|5m|available_crypto_5m_proxy|True|proxy only; needs US session/gap data|
|ORB_8AM|8AM Opening Range Breakout|CANDIDATE_008|DAY|session_native_crypto_proxy|5m|available_crypto_5m_proxy|True|prior reject but retest verifies timezone/session|
|ANTI_CHASE|Daily Extension Anti-Chase|CANDIDATE_011|FILTER|crypto_proxy|1D|available_crypto_daily|True|test only as filter overlay|
|CANSLIM|CANSLIM Shakeout +3|CANDIDATE_006|POSITION|us_equity_native|1D|blocked_no_equity_fundamental_rs|False|needs real US equity and CANSLIM data|
|WEINSTEIN|Stan Weinstein Stage Analysis|CANDIDATE_013|POSITION|us_equity_native|1D/1W|blocked_no_equity_universe_rs|False|needs US equity universe and RS breadth|
|CHARLES_50DMA|Charles Harris 50DMA Pullback|antigravity_claim|POSITION|us_equity_native|1D|blocked_no_equity_data|False|reported by prior agent; needs real equity data|
|TY_MICROCAP|Ty Rajnus Microcap Liquidity Reversion Short|CANDIDATE_010|DAY|us_microcap_native|1m/premarket|blocked_no_microcap_borrow_halt|False|do not crypto-test|