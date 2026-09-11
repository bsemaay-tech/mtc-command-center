Lead closure facts, independently read from git show 42f9957 and preserved byte-exact under inputs/additional_source (hashes in qa/ADDITIONAL_SOURCE_VERIFICATION.json):
- IBKR_PAPER_BRIDGE/bridge/engine/types.py:1327 DurableRiskPolicy exists, create validates finite numeric fields and hashes canonical JSON containing float.hex strings, prefix rpol-v1. Reusable design pattern only; do not import or alter protected Bridge or force P020 carrier.
- MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/data/io.py validate_dataset exists. Checks columns/empty/NaN/OHLC; volume NaNs/gaps only warnings; monotonic_increasing permits equal adjacent timestamps so duplicate detection is conditional and insufficient for collector replay. No execution here. Existing utility is not exact P030 admission validator.
- cache.py CacheManager exists; key is truncated MD5 symbol/timeframe/start/end, does not encode venue/provenance/schema. get_or_download invokes downloader on cache miss; do not invoke in this task or reuse as collector trust identity.
- download.py download_ohlcv exists, ccxt Binance default and fetch_ohlcv loop. Proxy research candidate only, not Hyperliquid source/admitted backend. No network call made.
Thus P030 M10/M11 and CL025/CL049 must become source verified existence with precise reuse limits, not absent/unverifiable.
- P013 unsimulated_controls.py is at repo root; correct wrong03_QUANTLENS path.
- P021 compute_deployment_identity_hash hashes12named members, not11.
- P022 no ledger-specific observation_id implementation; cannot say no observation_id anywhere because P030 MarketBar has it.
- Remove missingfact owner retrieval/ratification of decision186/checkversion2. Inputs/OWNER_PROVISIONAL_POLICY_20260906.md and exact commits a63bd4b053648e4a7008e5f2fe5f999b94947650 then380a26aacf960ee33fd610ec699dcc2180e4eb8a are known source provenance. Preserve2. No new scope granted.
