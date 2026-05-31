# Codex Stage-2B Final Verdicts

|candidate|verdict|PF|2x fee PF|3x fee PF|max DD|reason|
|---|---|---:|---:|---:|---:|---|
|KELL_WEDGE|NEEDS_NATIVE_DATA|3.595616|3.399304|3.219458|-7.313073|only 17 trades and Claude contract audit says the previous proxy dropped Kell cycle preconditions|
|CRABEL_RANGE_EXPANSION|NEEDS_NATIVE_DATA|1.772742|1.609039|1.462264|-90.065624|Claude contract audit says canonical Crabel is intraday/session based; crypto-daily prior backtest is not a fair test|
|SLINGSHOT_EMA_PULLBACK|WEAK_STAGE3_CODE_VERIFIED|1.749484|1.720543|1.692191|-99.969194|coded contract is simple enough, but OOS PF broke below 1 and drawdown is unacceptable|
|BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR|NEEDS_CONTRACT_REWRITE|1.72521|1.691923|1.659414|-99.961612|previous code uses RSI recovery plus CHoCH, not a strict divergence contract|
|MARTIN_LUKE_PULLBACK|NEEDS_NATIVE_DATA|1.528889|1.504029|1.479706|-99.350673|AVWAP/relative strength context is equity-native; crypto proxy OOS failed|
|LINDA_5SMA_PULLBACK|NEEDS_NATIVE_DATA|1.355673|1.310809|1.267055|-98.33831|RS is proxied, not native; base edge is weak and drawdown is extreme|
