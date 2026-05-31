# AI-Free PineTS Alternatives Decision Matrix

| Tool | Fully free local use? | AI/Codex CLI-friendly? | Accepts raw Pine directly for free? | Pine-like semantics? | strategy.entry/exit support? | request.security / MTF support? | CSV/JSON output? | Parameter sweep path? | License risk | MTC v2 fit | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| Existing Python MTC engine | Yes | Yes | No | Custom parity implementation | Yes if implemented | Yes if implemented | Yes if implemented | Yes | Internal | 9/10 | Main optimization/backtest engine |
| PineTS / pinets-cli | Free local/internal | Yes | Yes for supported Pine indicator flow | High for indicators/signals | Not accepted as trade engine here | Yes / strong candidate | JSON plot output possible | External loop | AGPL/commercial dual license | 7/10 signal, not execution | Keep as signal/indicator oracle |
| PyneCore | Yes for core runtime | Yes | No free automatic compiler | Pine-like Python | Yes | Recent versions claim MTF/security support | CSV/report possible | External loop | Apache 2.0 core; compiler separate SaaS | 7/10 experimental | Experimental strategy execution oracle |
| vectorbt | Yes / open community edition | Yes | No | No | From signals, approximation | User-coded | Yes | Very strong | License must be checked for project use | 6/10 | Fast signal-array / sweep oracle |
| backtesting.py | Yes | Yes | No | No | Yes simple event-based | User-coded | Yes | Built-in optimize | AGPL-3.0 caution | 4/10 | Optional sanity runner only |
| backtrader | Yes | Yes | No | No | Yes | User-coded | Yes | Built-in/loop | GPL-3.0 caution | 3/10 | Lower priority fallback |

## Architecture decision

Do not use majority voting.

Use tools as layered oracles:

- TradingView export: final external Pine reference when available.
- Existing Python engine: main local backtest/optimization reference.
- PineTS: signal/indicator oracle.
- PyneCore: experimental independent strategy execution oracle.
- vectorbt: fast signal-array / parameter sweep oracle.
- backtesting.py: isolated sanity checks only.

## Practical rule

PineTS mismatch means:
- suspect PineTS transpilation, HTF alignment, warmup, or adapter plot export.

Python mismatch means:
- suspect local parity engine implementation, indicator seeding, HTF, execution order, or fill model.

PyneCore mismatch means:
- useful independent evidence, but not final verdict until module-level parity is proven.
