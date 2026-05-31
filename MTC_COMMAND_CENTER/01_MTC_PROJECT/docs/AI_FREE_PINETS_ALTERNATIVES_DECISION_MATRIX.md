# AI Free PineTS Alternatives Decision Matrix

- Command: `web license/repo lookup; local repo inventory; additive harness implementation`
- Data hash: not applicable
- Config hash: not applicable
- Code hash: `fbc1392b1f1065a418eabcd5149259f98087b55c`

| Tool | Fully free for local use? | AI/Codex CLI-friendly? | Accepts raw Pine directly for free? | Pine-like semantics? | strategy.entry/exit support? | request.security / MTF support? | Binance/CCXT data path? | CSV/JSON output? | Parameter sweep path? | License risk | MTC v2 fit score 0-10 | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| Existing Python engine | Yes | Yes | No | Implemented MTC semantics | Yes, project-owned | Project-owned HTF modules | Local CSV/export path | Yes | Yes | Low internal risk | 10 | Keep as main optimization/backtest engine. |
| PineTS / pinets-cli | Yes for local/internal POC | Yes | Experimental native Pine support | High for indicators/signals | Strategy backtesting still roadmap/caution | request.security support claimed, must prove locally | Binance/custom data path | Yes through runner/adapter | Limited | Caution: AGPL/commercial dual license | 8 | Keep as signal/indicator oracle, not trade execution oracle. |
| PyneCore | Yes for runtime POC | Yes | Direct Pine compile requires PyneSys API key, so no for this phase | High Pine-like Python semantics | Strategy framework exists | MTF needs POC proof | CCXT/provider path exists | Yes via runner normalization | Possible in Python | Safe for local POC: Apache-2.0 runtime; avoid paid compiler | 7 | Primary experimental free strategy-execution oracle using manual translation only. |
| vectorbt | Yes for local research | Yes | No | Vectorized signal semantics, not Pine semantics | from_signals approximation | User must precompute MTF | DataFrame/CSV/CCXT ecosystem | Yes | Strong | Caution: Apache-2.0 + Commons Clause | 6 | Fast signal-array / parameter sweep validator. |
| backtesting.py | Yes technically | Yes | No | Event-based Python API | Simple entries/exits | No native Pine MTF semantics | CSV/DataFrame | Yes | Built-in optimizer | Caution: AGPL-3.0 | 4 | Optional simple sanity checker only; license caution. |
| backtrader | Yes technically | Moderate | No | Event-based Python API | Yes | Resampling/replay support | CSV/feeds/CCXT add-ons | Yes with analyzers | Possible | Caution: GPL-3.0 | 3 | Lower priority fallback; do not implement unless useful. |

Required architectural decision: these tools are layered oracles, not equals. TradingView export remains final external reference when available; existing Python remains main local engine; PineTS remains L1/L2/L3 signal oracle; PyneCore remains experimental execution oracle; vectorbt remains fast approximation; backtesting.py remains optional sanity runner.
