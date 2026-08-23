# Data Foundation Audit — Backtesting & Simulation (Wayfinder #70)

**Method:** read-only file/directory inspection of the repo worktree (`C:\WFK3`, branch
`research/data-foundation-audit`, base `3d6a621c`) plus read-only inspection of one legacy
directory on this machine that a repo-committed catalog file points at. No pipeline, downloader,
or broker/API call was executed. All findings verified by listing/reading the actual files, not
by trusting prose in READMEs.

## Headline

Real historical market data exists and some of it is genuinely repeatable and quality-checked —
but it is fragmented across at least four uncoordinated sources, the single largest and
longest-history bundle (2018–2026 Binance BTC/ETH) **does not physically exist inside this repo**
and instead lives in a stale, uncontrolled legacy folder on this machine, and there is **no
Hyperliquid data collector or archiver anywhere in the codebase** — confirmed by grepping every
use of the Hyperliquid candle API. This second point is not a new discovery: ADR-0020 (accepted
2026-07-18) already lists it as open questions OQ-009/OQ-010, unresolved to this day.

---

## 1. What historical market data exists

### 1a. In-repo, git-tracked, physically present today

| Location | Symbols | Timeframe | Range | Size / bars | Source |
|---|---|---|---|---|---|
| `MTC_COMMAND_CENTER/03_QUANTLENS/research/data_acquisition_5m_2026_05_03/normalized/binance_futures/` | 17 USDT-M futures pairs (ADA, APT, ARB, AVAX, BNB, BTC, DOGE, DOT, ETH, LINK, LTC, NEAR, OP, POL, SOL, TRX, XRP) | 5m | 2024-01-01 → 2026-05-03 | 248 MB CSV, 4,105,966 bars total | Binance USDT-M futures via `download_binance_futures_5m.py` |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/data/history_sweeps_*` (7 subdirs, 146 files) | BTCUSDT_PERP only | 15m | 2025-06-29 → 2025-12-01, sliced into ~50 overlapping start points | ~89 MB parquet | Derived from the Binance BTCUSDT.P catalog dataset below — these are **parity/warmup-sweep test fixtures**, not general backtest history (see `configs/cases/history_sweeps_*/case_*.json`, e.g. `"_comment": "60d0b history sweep start 2025-06-29T00:00:00Z"`, used to validate warmup/preroll behavior against one TradingView export) |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/05_PARITY/01_TW_CHART_DATA/BINANCE_BTCUSDT.P, 60_consolidated_stable.csv` | BTCUSDT.P | 1h | ~2023-05-29 → ~2026-03-16 | 24,525 lines | Manual TradingView chart-data export, used for Pine/Python parity checks |
| `MTC_COMMAND_CENTER/00_INBOX/USER_INTAKE/*.csv` | SPY, QQQ, AAPL | 10m | 2024-06-03 → 2026-06-26 | 3 files | Manual TradingView export, owner-supplied ("USER_INTAKE") |
| `IBKR_PAPER_BRIDGE/tests/fixtures/BTC_1h_real.csv` | BTC | 1h | starts 2021-01-01 | 48,078 lines | Real historical snippet used only as a bridge unit-test fixture |

### 1b. Documented as PRIMARY but not actually present (git-ignored)

`MTC_COMMAND_CENTER/03_QUANTLENS/data/README.md` names
`native_multiasset_alpaca_2026-06-28/` as the **PRIMARY** multi-asset bundle: 51 symbols (39
equity/ETF + 12 crypto), 10m/15m/30m/1h/2h/4h/1d, 357 datasets, ~11.86M bars, Alpaca IEX + crypto,
validated PASS 357/357. Verified: only `manifests/dataset_manifest.json` is committed; the
`normalized/` CSVs (711 MB per the README) are excluded by `.gitignore:185`
(`MTC_COMMAND_CENTER/03_QUANTLENS/data/native_multiasset_alpaca_*/normalized/`) and are **not
present in this checkout**. Regenerating requires `03_QUANTLENS/tools/alpaca_download_dataset.py`
and an Alpaca API key — nothing else present provides this data. The narrower predecessor bundles
(`native_us_equities_10m_alpaca_2026-06-28/`, two TradingView-export bundles) are in the same
state: manifest only, data git-ignored.

### 1c. Cataloged by the repo but living outside the repo, on a stale legacy path

`MTC_COMMAND_CENTER/02_MTC_BACKTEST/backtest_assets/data_catalog.json` (committed, checked)
catalogs the deepest history in the whole audit:

| Symbol | TF | Range | Bars |
|---|---|---|---|
| BTCUSDT | 1d/4h/2h/1h/15m/5m | 2018-07-01 → 2026-03-08/12 | up to 807,586 (5m) |
| ETHUSDT | 1d/15m/1h/4h | 2019-01-01 → 2026-03-08 | up to 251,607 (15m) |
| BTCUSDT.P | 15m/4h | partial (Dec 2025 / 2024-2026) | 3,072 / 4,392 |

Every `abs_path` in this catalog reads `C:/LAB/tradingview-lab/110_/data/processed/...`. That path
does **not exist** on this machine (verified: `Test-Path` false). The actual parquet files were
found, read-only, at a different, unrelated path:
`C:\LAB\tradingview-lab\110_MTC_BACKTEST_OPTİMİZASYON_DİZİNLERİ\data\processed\` — 56 MB, 12
files, file-mode `r--r--r--`, last modified 2026-03-07 to 2026-03-12 (**over 5 months stale** as
of 2026-08-23). `tradingview-lab` is a separate, pre-cleanup legacy repo directory on this
machine, not this repo (`Tradingview_LAB_CLEAN`) and not under this repo's git history — it is an
ungoverned side directory that happens to still hold the files. `data_catalog_hist.json`'s
`last_updated` timestamps cluster entirely within 2026-03-07 → 2026-03-12: a single download
burst, not an ongoing refresh cadence. `validation_report.md` (generated
2026-03-08T17:07:33Z, same burst) shows all six BTCUSDT/ETHUSDT datasets as **WARN** (gaps
attributed to routine ~10–12h Binance maintenance windows, not data corruption) and BTCUSDT.P/15m
as **OK**.

The QuantLens data README additionally names a third off-repo location,
`C:\LAB\_MTC_V2_REPO_CLEANUP_ARCHIVE_20260529\...\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\`
(17 crypto pairs, 15m–1D, CSV, described as the QuantLens engine's "default manifest" bundle) —
same pattern of real data living in an archived, ungoverned folder rather than in the repo. Not
independently re-verified beyond confirming the README's claim exists (time-boxed).

**No historical Hyperliquid OHLCV data exists anywhere** — in the repo, git-ignored, or on any
legacy path discovered during this audit. Every dataset above is Binance (spot or USDT-M futures),
Alpaca, or a manual TradingView export.

---

## 2. Is acquisition repeatable?

**Yes, for Binance and Alpaca — with real tooling:**
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/data_tools/download_cli.py` +
  `data_providers/{binance_provider,binance_usdm_provider,csv_provider}.py`: chunked, **resumable**
  (reads the last saved timestamp and top-ups), sha256-hashes each output file, writes/updates
  `data_catalog.json`. This is genuinely repeatable machinery — it is simply not being run
  regularly (see §1c).
- `03_QUANTLENS/research/data_acquisition_5m_2026_05_03/download_binance_futures_5m.py`: a
  working, repeatable one-off downloader with its own smoke test (`test_downloader_smoke.py`) and
  a data-quality report generator.
- `03_QUANTLENS/tools/alpaca_download_dataset.py` / `alpaca_download_us_equities_10m.py`:
  repeatable but gated on an Alpaca API key the owner must supply; not currently run (data absent,
  see §1b).

**No, for the TradingView exports:** `01_TW_CHART_DATA/*.csv` and `00_INBOX/USER_INTAKE/*.csv`
are manual browser exports (file naming and the README both call this out — "USER_INTAKE"). There
is no script; reproducing them requires the owner to re-export from the TradingView UI by hand.

**Not applicable, for Hyperliquid:** there is no downloader/provider for Hyperliquid at all — see
§4.

---

## 3. What gap/quality checks exist

- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/data_tools/validate.py` is a real, working validator: checks
  monotonic index, duplicate timestamps, UTC timezone, gap detection (WARN at ≥3× the expected bar
  interval, ERROR at ≥15×, with a session-aware skip for non-24/7 markets), and OHLC sanity
  (`high ≥ max(open,close)`, `low ≤ min(open,close)`, `volume ≥ 0`). Its last run
  (`validation_report.md`, 2026-03-08) is from the same single burst as the catalog — it has not
  been rerun since, so it says nothing about data freshness after that date (there is none to
  check, since the source stopped being downloaded).
- `03_QUANTLENS/research/data_acquisition_5m_2026_05_03/DATA_QUALITY_REPORT.csv`: per-symbol
  PASS/WARN against a continuous 5-minute UTC grid; 16/17 PASS, 1 WARN (POLUSDT — expected, later
  Binance listing date, not a defect).
- QuantLens bundle manifests (`manifests/dataset_manifest.json`) carry a required
  `ohlcv_validation_status` field ("PASS" only) that gates whether the engine (`mega_walk_forward.py`)
  will use a dataset, and the data README enforces a "PRIMARY vs. superseded/provenance" selection
  rule so agents don't silently pick a stale bundle.
- No equivalent validator exists for Hyperliquid data — consistent with nothing being collected to
  validate.

---

## 4. Hyperliquid retention and continuous archiving — the central question

**Verdict: nothing is continuously archiving Hyperliquid candles today.** This was checked
directly, not inferred:

- Repo-wide grep for `candles_snapshot` (the Hyperliquid SDK's historical-candle call) returns
  exactly two hits: the production call site in
  `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py:271` and its unit-test mock in
  `tests/test_hyperliquid_broker.py:674`. Read the production code
  (`bridge/engine/bars.py` + `bridge/broker/hyperliquid.py`): `BarFeed.start(lookback=300)` calls
  `broker.historical_bars()`, which calls `info.candles_snapshot(coin, tf, start_ms, end_ms)` and
  returns only the last `lookback` bars (default 300) **in memory** — this is live-trading warmup
  for indicator computation, not archival. Nothing in the bridge writes venue candles to a
  database, CSV, or parquet file for later reuse.
- Grepped the bridge, its tools, and its deploy scripts for "archive"/"cron"/"ScheduledTask" tied
  to candles — no hits describe a candle archiver (the "archive" hits found are order-lifecycle
  archiving in `bridge/store/db.py` and unrelated ops-monitoring docs).
- `MTC_COMMAND_CENTER/09_DOCS/ADR/ADR-0020-hybrid-backtesting-validation-stack.md` (Accepted,
  ratified by Barış 2026-07-18, D016) independently confirms this is a known, still-open gap, not
  something newly discovered here: **Open Question OQ-009** — "hftbacktest Hyperliquid collector
  completeness" — and **OQ-010** — "required market-data sources and retention" — are both listed
  as unresolved. The ADR text itself states "Full Hyperliquid collector coverage for hftbacktest
  remains unverified."

**What this means for building multi-year backtests, given the venue's ~5,000-candle-per-interval
retention (15m ≈ 52 days, established in map #37 ticket #44):** because nothing captures closing
candles as they happen, the ~52-day (15m-equivalent) window is not a starting point that grows
over time — it is a **hard, live, shrinking ceiling**. Every day that passes without an archiver
running, the oldest day's candles age out of Hyperliquid's own buffer and are gone permanently;
there is no accumulating local copy to fall back on. Today, a Hyperliquid-native backtest is
capped at whatever the venue currently holds (finer timeframes cap correspondingly tighter, coarser
ones looser, all bounded by the same ~5,000-candle ceiling). All of the multi-year history that
does exist in or near this repo (2018–2026 Binance BTC/ETH, 2024–2026 Binance futures 17-pair 5m,
Alpaca equities/crypto) is for **different venues** than the one the bridge trades live — useful
as cross-venue price-action proxies, but not Hyperliquid's own order flow, funding, or liquidation
data, and ADR-0020 already flags that even the intended hftbacktest engine's Hyperliquid-specific
field/sequence/gap coverage is unverified.

---

## 5. Summary for the data doctrine decision

1. **Fragmentation, not absence.** Four-plus independent data pools exist (Binance
   parquet catalog on a stale legacy path, a committed 17-pair Binance-futures 5m bundle, a
   git-ignored Alpaca multi-asset bundle, several manual TradingView exports) with no single
   inventory or refresh owner. `03_QUANTLENS/data/README.md` is the closest thing to a working
   index and is worth generalizing as the model.
2. **The deepest, longest-history dataset is not actually in version control** and is stale by
   over five months; its catalog's own path pointer is broken (points at a directory that no
   longer exists on this machine). Reproducing it is mechanically possible today
   (`download_cli.py` works and is resumable) but nobody is running it.
3. **Real quality tooling exists and works** (`validate.py`, per-bundle PASS/WARN manifests,
   gap/OHLC/monotonic/duplicate/UTC checks) — the doctrine can build on this rather than invent it,
   but it needs to be re-run against whatever data pool becomes canonical.
4. **Hyperliquid has zero historical footprint and zero collection today.** This is the most
   urgent fact for the doctrine decision: every day without an archiver is unrecoverable data loss
   against the venue's own ~5,000-candle retention window, and ADR-0020 has been flagging this gap
   (OQ-009/OQ-010) since 2026-07-18 without it being closed.

## Sources checked (paths)

- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/backtest_assets/data_catalog.json`,
  `data_catalog_hist.json`, `data_catalog_compat.json`, `validation_report.md`, `00_RUNBOOK.md`
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/data_tools/download_cli.py`, `validate.py`
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/data_providers/*.py`
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/data/history_sweeps_*/` (146 files) and matching
  `configs/cases/history_sweeps_*/case_*.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/data/README.md` and all four native bundle
  `manifests/dataset_manifest.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/research/data_acquisition_5m_2026_05_03/` (README,
  DATA_DOWNLOAD_REPORT.md, DATA_QUALITY_REPORT.csv, download script, normalized data)
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/05_PARITY/01_TW_CHART_DATA/`,
  `MTC_COMMAND_CENTER/00_INBOX/USER_INTAKE/`
- `IBKR_PAPER_BRIDGE/tests/fixtures/BTC_1h*.csv`
- `IBKR_PAPER_BRIDGE/bridge/engine/bars.py`, `bridge/broker/hyperliquid.py`,
  `tests/test_hyperliquid_broker.py`
- `MTC_COMMAND_CENTER/09_DOCS/ADR/ADR-0020-hybrid-backtesting-validation-stack.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/HYPERLIQUID_PUBLIC_DOCS_VERIFICATION_ADDENDUM_2026-08-17.md`
  (context on Hyperliquid API limits — not a data-retention source itself)
- `.gitignore` (line 185, Alpaca bundle exclusion); `git ls-files` / `git check-ignore` on the
  data directories above
- Filesystem check (read-only): `C:\LAB\tradingview-lab\110_MTC_BACKTEST_OPTİMİZASYON_DİZİNLERİ\data\processed\`
