# Candidate: QL_CANSLIM_SHAKEOUT_PLUS_3_001

**candidate_id**: QL_CANSLIM_SHAKEOUT_PLUS_3_001

**source_file**: 2026-05-03_9ZJK8175drM_quantlens_canslim_detailed_intake.md

**source_url**: ** https://youtu.be/9ZJK8175drM?si=QcTE0mdW00UzcL_B

**video_id**: 

**asset_class**: equities_primary

**timeframe**: daily

**direction**: long_only

**priority**: MEDIUM

**verdict**: UNKNOWN

**rules**: {'candidate_id': 'QL_CANSLIM_SHAKEOUT_PLUS_3_001', 'direction': 'long_only', 'asset_class': 'equities_primary', 'timeframe': 'daily', 'setup': {'prior_uptrend': ['close / close[N] - 1 >= 0.30'], 'double_bottom_proxy': ['detect first swing low L1', 'detect rally after L1', 'detect second swing low L2', 'L2 < L1'], 'buy_point': {'if 30 <= L1_price <= 60': 'buy = L1_price + 3.0', 'elif L1_price > 60': 'buy = L1_price * 1.05', 'else': 'buy = L1_price * 1.10'}, 'trigger': ['high >= buy_point'], 'entry': ['buy_point or next_bar_open depending on execution mode'], 'stop': ['entry * 0.93'], 'target': ['standard_pivot_based_profit_goal if known', 'otherwise entry * 1.20 to entry * 1.25']}}

