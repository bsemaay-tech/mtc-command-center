/**
 * mtc_bridge.mjs — MTC_V2 Signal Extraction Bridge
 *
 * Fetches BTCUSDT 1h OHLCV from Binance via PineTS Provider,
 * runs MTC_V2 in indicator mode, and extracts bar-by-bar signal data
 * to data/mtc_signals.json.
 *
 * Usage:
 *   node mtc_bridge.mjs [--bars 1000] [--symbol BTCUSDT] [--tf 1h]
 *   node mtc_bridge.mjs --start 2025-01-01 --end 2025-12-31 [--symbol BTCUSDT] [--tf 1h]
 *
 * Output:
 *   data/mtc_signals.json — bar-by-bar signals + OHLCV
 */

import { createRequire } from 'module';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join, resolve } from 'path';

const require = createRequire(import.meta.url);
const { PineTS, Provider } = require('./node_modules/pinets/dist/pinets.min.cjs');

// --- TV merged CSV support and HTF prefetch ---
import { existsSync, createReadStream } from 'fs';
import readline from 'readline';
let TV_MERGED_DIR /* late init below */ = undefined;

function mergedCsvPath(symbolForFile, tf) {
  const map = new Map([
    ['1h','1h'], ['60','1h'],
    ['2h','2h'], ['120','2h'],
    ['4h','4h'], ['240','4h'],
    ['1d','1d'], ['D','1d'],
  ]);
  const norm = map.get(tf) || tf;
  return join(TV_MERGED_DIR, `${symbolForFile}_${norm}.csv`);
}

async function readMergedCsvBars(csvPath, startMs, endMs, limit, tf) {
  const out = [];
  if (!existsSync(csvPath)) return out;
  const rl = readline.createInterface({ input: createReadStream(csvPath, { encoding: 'utf8' }), crlfDelay: Infinity });
  let headerSeen = false;
  for await (const line of rl) {
    if (!headerSeen) { headerSeen = true; continue; }
    if (!line.trim()) continue;
    const [t,o,h,l,c,vol] = line.split(',');
    let ts = Number(t);
    if (ts < 10000000000000) ts *= 1000; // seconds->ms
    if (startMs && ts < startMs) continue;
    if (endMs && ts > endMs) continue;
    out.push({
      openTime: ts,
      open: Number(o), high: Number(h), low: Number(l), close: Number(c), volume: Number(vol ?? 0),
      closeTime: ts + timeframeToMs(tf),
      quoteAssetVolume: 0, numberOfTrades: 0, takerBuyBaseAssetVolume: 0, takerBuyQuoteAssetVolume: 0, ignore: '0',
    });
  }
  if (startMs === undefined && endMs === undefined && limit) {
    return out.slice(Math.max(0, out.length - limit));
  }
  return out;
}

async function writeMockFromMergedCsv(symbol, tf, requestedLimit, startMs, endMs) {
  const market = detectBinanceMarket(symbol);
  const path = mergedCsvPath(market.symbolForFile, tf);
  if (!existsSync(path)) return null;
  const bars = await readMergedCsvBars(path, startMs, endMs, requestedLimit, tf);
  if (bars.length === 0) return null;
  const fileStartMs = bars[0].openTime;
  const fileEndMs = bars[bars.length-1].closeTime;
  const interval = normalizeTfForBinance(tf);
  const mockFileName = `${market.symbolForFile}-${interval}-${fileStartMs}-${fileEndMs}.json`;
  const mockFilePath = join(MOCK_BINANCE_DIR, mockFileName);
  writeFileSync(mockFilePath, JSON.stringify(bars, null, 2), 'utf8');
  return { mockFilePath, runSymbol: market.symbolForFile, runTf: interval };
}

async function prefetchHtfMocksFromMerged(symbol, primaryStart, primaryEnd) {
  const HTFS = ['2h','4h','1d'];
  const buf30d = 30*24*60*60*1000;
  for (const tf of HTFS) {
    const s = primaryStart ? (primaryStart - buf30d) : undefined;
    const e = primaryEnd;
    await writeMockFromMergedCsv(symbol, tf, null, s, e);
  }
}const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, '..', '..');
const BACKTEST_ROOT = resolve(REPO_ROOT, 'MTC_COMMAND_CENTER/02_MTC_BACKTEST');
TV_MERGED_DIR = resolve(BACKTEST_ROOT, 'parity_suite_350/tv_manual_inputs/merged');

// ─── CLI args ─────────────────────────────────────────────────────────────────
const argv = process.argv.slice(2);
function getArg(name, def) {
  const i = argv.indexOf(`--${name}`);
  return i !== -1 ? argv[i + 1] : def;
}
const BARS   = parseInt(getArg('bars',   '1000'), 10);
const SYMBOL = getArg('symbol', 'BTCUSDT');
const TF     = getArg('tf',     '1h');
const OVERRIDES_JSON = getArg('overrides-json', '');
const START_RAW = getArg('start', '');
const END_RAW = getArg('end', '');

function parseDateArg(raw, kind) {
  if (!raw) return undefined;
  const trimmed = String(raw).trim();
  let iso = trimmed;
  if (/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) {
    iso = kind === 'start' ? `${trimmed}T00:00:00.000Z` : `${trimmed}T23:59:59.999Z`;
  }
  const ms = Date.parse(iso);
  if (Number.isNaN(ms)) {
    throw new Error(`Invalid --${kind} date: ${raw}`);
  }
  return ms;
}

const START_MS = parseDateArg(START_RAW, 'start');
const END_MS = parseDateArg(END_RAW, 'end');
const HAS_DATE_WINDOW = START_MS !== undefined || END_MS !== undefined;
const REQUESTED_LIMIT = HAS_DATE_WINDOW ? null : BARS;

const PINE_PATH = resolve(REPO_ROOT, 'MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine');
const DATA_DIR  = resolve(BACKTEST_ROOT, 'data');
const OUT_PATH  = join(DATA_DIR, 'mtc_signals.json');
const MOCK_BINANCE_DIR = join(DATA_DIR, 'pinets_mock_binance');

mkdirSync(DATA_DIR, { recursive: true });
mkdirSync(MOCK_BINANCE_DIR, { recursive: true });

console.log('=== MTC Bridge: Signal Extraction ===');
console.log(`Symbol : ${SYMBOL}  TF: ${TF}  Bars: ${HAS_DATE_WINDOW ? 'auto(date-window)' : BARS}`);
if (HAS_DATE_WINDOW) {
  console.log(`Window : ${START_MS !== undefined ? new Date(START_MS).toISOString() : '(open)'} -> ${END_MS !== undefined ? new Date(END_MS).toISOString() : '(open)'}`);
}
console.log(`Source : ${PINE_PATH}`);
console.log(`Output : ${OUT_PATH}\n`);

// ─── Build indicator variant ──────────────────────────────────────────────────
// Patch syminfo.* to known BTCUSDT values before stripping strategy calls.
// This ensures position sizing math (qty, entry_price) produces correct numbers.
const SYMINFO_PATCH = `
// === SYMINFO PATCH (BTCUSDT) ===
// PineTS stubs syminfo.* with defaults that may differ from exchange values.
// Override here before any usage:
syminfo_mintick     = 0.01
syminfo_mincontract = 0.001
syminfo_pointvalue  = 1.0
`;

function buildIndicatorVariant(code) {
  let counter = 0;
  const initialCapitalMatch = code.match(/strategy\([^)]*initial_capital\s*=\s*([0-9.]+)/m);
  const strategyInitialCapital = initialCapitalMatch ? initialCapitalMatch[1] : null;

  // 1. Replace strategy() declaration
  let patched = code.replace(
    /^strategy\([^)]*\)/m,
    'indicator("MTC V2 - Indicator Mode", overlay=true)'
  );

  // 2. Replace syminfo.mintick/mincontract/pointvalue with known constants
  //    (PineTS stubs these but actual values matter for sizing math)
  patched = patched
    .replace(/\bsyminfo\.mintick\b/g,     '0.01')
    .replace(/\bsyminfo\.mincontract\b/g, '0.001')
    .replace(/\bsyminfo\.pointvalue\b/g,  '1.0');

  if (strategyInitialCapital !== null) {
    patched = patched.replace(/\bstrategy\.initial_capital\b/g, strategyInitialCapital);
  }

  // 3. Replace strategy.* calls with no-ops (preserves if/else block structure)
  patched = patched.replace(
    /^(\s*)strategy\.[a-zA-Z_]+\s*\([^)]*\)\s*$/gm,
    (m, indent) => `${indent}bool _strat_noop_${counter++} = false`
  );

  return patched;
}

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function formatPineLiteral(value) {
  if (typeof value === 'boolean') {
    return value ? 'true' : 'false';
  }
  if (typeof value === 'number') {
    return Number.isInteger(value) ? String(value) : String(value);
  }
  return JSON.stringify(String(value));
}

function applyInputOverrides(code, overrides) {
  let patched = code;
  for (const [name, value] of Object.entries(overrides || {})) {
    const pattern = new RegExp(
      `(^\\s*${escapeRegex(name)}\\s*=\\s*input\\.(?:bool|int|float|string)\\()\\s*(?:\"[^\"]*\"|true|false|[^,\\n]+)(.*$)`,
      'm',
    );
    if (!pattern.test(patched)) {
      throw new Error(`Could not find Pine input line for override: ${name}`);
    }
    patched = patched.replace(pattern, `$1${formatPineLiteral(value)}$2`);
  }
  return patched;
}

function detectBinanceMarket(symbol) {
  if (String(symbol).endsWith('.P')) {
    return {
      marketType: 'futures',
      restBase: 'https://fapi.binance.com',
      exchangeInfoPath: '/fapi/v1/exchangeInfo',
      symbolForExchange: String(symbol).slice(0, -2),
      symbolForFile: String(symbol),
    };
  }
  return {
    marketType: 'spot',
    restBase: 'https://api.binance.com',
    exchangeInfoPath: '/api/v3/exchangeInfo',
    symbolForExchange: String(symbol),
    symbolForFile: String(symbol),
  };
}

function normalizeTfForBinance(tf) {
  const raw = String(tf).trim();
  const map = new Map([
    ['1', '1m'],
    ['3', '3m'],
    ['5', '5m'],
    ['15', '15m'],
    ['30', '30m'],
    ['45', '45m'],
    ['60', '1h'],
    ['120', '2h'],
    ['180', '3h'],
    ['240', '4h'],
    ['1h', '1h'],
    ['2h', '2h'],
    ['3h', '3h'],
    ['4h', '4h'],
    ['6h', '6h'],
    ['8h', '8h'],
    ['12h', '12h'],
    ['1d', '1d'],
    ['d', '1d'],
    ['1w', '1w'],
    ['w', '1w'],
    ['1M', '1M'],
    ['m', '1M'],
  ]);
  return map.get(raw) || raw;
}

function timeframeToMs(tf) {
  const normalized = normalizeTfForBinance(tf);
  const match = normalized.match(/^(\d+)([mhdwM])$/);
  if (!match) {
    throw new Error(`Unsupported timeframe for Binance mock fetch: ${tf}`);
  }
  const qty = parseInt(match[1], 10);
  const unit = match[2];
  const unitMs = {
    m: 60 * 1000,
    h: 60 * 60 * 1000,
    d: 24 * 60 * 60 * 1000,
    w: 7 * 24 * 60 * 60 * 1000,
    M: 30 * 24 * 60 * 60 * 1000,
  }[unit];
  return qty * unitMs;
}

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status} for ${url}: ${text}`);
  }
  return await res.json();
}

async function fetchBinanceExchangeInfo(market) {
  return await fetchJson(`${market.restBase}${market.exchangeInfoPath}`);
}

async function fetchBinanceKlines(market, symbol, interval, requestedLimit, startMs, endMs) {
  const klines = [];
  const limitPerCall = 1500;
  const intervalMs = timeframeToMs(interval);
  const effectiveEndMs = endMs ?? Date.now();

  if (startMs === undefined && endMs === undefined) {
    const url = new URL(`${market.restBase}${market.marketType === 'futures' ? '/fapi/v1/klines' : '/api/v3/klines'}`);
    url.searchParams.set('symbol', symbol);
    url.searchParams.set('interval', interval);
    url.searchParams.set('limit', String(Math.min(requestedLimit ?? BARS, limitPerCall)));
    return await fetchJson(url.toString());
  }

  let cursor = startMs ?? Math.max(0, effectiveEndMs - ((requestedLimit ?? BARS) * intervalMs));
  while (cursor <= effectiveEndMs) {
    const url = new URL(`${market.restBase}${market.marketType === 'futures' ? '/fapi/v1/klines' : '/api/v3/klines'}`);
    url.searchParams.set('symbol', symbol);
    url.searchParams.set('interval', interval);
    url.searchParams.set('startTime', String(cursor));
    url.searchParams.set('endTime', String(effectiveEndMs));
    url.searchParams.set('limit', String(limitPerCall));
    const chunk = await fetchJson(url.toString());
    if (!Array.isArray(chunk) || chunk.length === 0) {
      break;
    }
    klines.push(...chunk);
    const lastOpenTime = Number(chunk[chunk.length - 1][0]);
    const nextCursor = lastOpenTime + intervalMs;
    if (nextCursor <= cursor) {
      break;
    }
    cursor = nextCursor;
    if (requestedLimit && klines.length >= requestedLimit) {
      break;
    }
  }

  return requestedLimit ? klines.slice(0, requestedLimit) : klines;
}

function convertKlinesToMockBars(klines, tf) {
  const intervalMs = timeframeToMs(tf);
  return klines.map((row) => ({
    openTime: Number(row[0]),
    open: Number(row[1]),
    high: Number(row[2]),
    low: Number(row[3]),
    close: Number(row[4]),
    volume: Number(row[5]),
    closeTime: Number(row[6] ?? (Number(row[0]) + intervalMs)),
    quoteAssetVolume: Number(row[7] ?? 0),
    numberOfTrades: Number(row[8] ?? 0),
    takerBuyBaseAssetVolume: Number(row[9] ?? 0),
    takerBuyQuoteAssetVolume: Number(row[10] ?? 0),
    ignore: row[11] ?? '0',
  }));
}

async function prepareMockProviderData(symbol, tf, requestedLimit, startMs, endMs) {
  // Prefer merged TradingView CSVs if available
  const csvPreferred = await writeMockFromMergedCsv(symbol, tf, requestedLimit, startMs, endMs);
  if (csvPreferred) {
    const match = csvPreferred.mockFilePath.match(/-(\d+)-(\d+)\.json$/);
    const pStart = startMs ?? (match ? Number(match[1]) : undefined);
    const pEnd   = endMs   ?? (match ? Number(match[2]) : undefined);
    await prefetchHtfMocksFromMerged(symbol, pStart, pEnd);
    return {
      provider: Provider.Mock,
      providerName: `Mock(Binance ${detectBinanceMarket(symbol).marketType})`,
      dataDirectory: MOCK_BINANCE_DIR,
      mockFilePath: csvPreferred.mockFilePath,
      runSymbol: csvPreferred.runSymbol,
      runTf: csvPreferred.runTf,
    };
  }
  // Fallback to live Binance fetch for primary and write mock file
  const market = detectBinanceMarket(symbol);
  const interval = normalizeTfForBinance(tf);
  const exchangeInfo = await fetchBinanceExchangeInfo(market);
  const klines = await fetchBinanceKlines(market, market.symbolForExchange, interval, requestedLimit, startMs, endMs);
  const exchangeInfoPath = join(MOCK_BINANCE_DIR, market.marketType === "futures" ? "fapi-exchangeInfo.json" : "api-exchangeInfo.json");
  writeFileSync(exchangeInfoPath, JSON.stringify(exchangeInfo, null, 2), "utf8");
  const fileStartMs = startMs ?? (klines[0] ? Number(klines[0][0]) : Date.now());
  const fileEndMs   = endMs   ?? (klines.length ? Number(klines[klines.length - 1][6] ?? klines[klines.length - 1][0]) : Date.now());
  const mockFileName = `${market.symbolForFile}-${interval}-${fileStartMs}-${fileEndMs}.json`;
  const mockFilePath = join(MOCK_BINANCE_DIR, mockFileName);
  writeFileSync(mockFilePath, JSON.stringify(convertKlinesToMockBars(klines, interval), null, 2), "utf8");
  return {
    provider: Provider.Mock,
    providerName: `Mock(Binance ${market.marketType})`,
    dataDirectory: MOCK_BINANCE_DIR,
    mockFilePath,
    runSymbol: market.symbolForFile,
    runTf: interval,
  };
}

let originalCode = readFileSync(PINE_PATH, 'utf8');
let inputOverrides = {};
if (OVERRIDES_JSON) {
  inputOverrides = JSON.parse(readFileSync(resolve(__dirname, OVERRIDES_JSON), 'utf8'));
  originalCode = applyInputOverrides(originalCode, inputOverrides);
}
const indicatorCode = buildIndicatorVariant(originalCode);

// ─── Run PineTS ───────────────────────────────────────────────────────────────
console.log('Fetching Binance data and running PineTS...');
const t0 = Date.now();

let ctx;
try {
  let provider = Provider.Binance;
  let providerName = 'Binance';
  let runSymbol = SYMBOL;
  let runTf = TF;

  if (String(SYMBOL).endsWith('.P')) {
    const mock = await prepareMockProviderData(SYMBOL, TF, REQUESTED_LIMIT, START_MS, END_MS);
    provider = mock.provider;
    providerName = mock.providerName;
    runSymbol = mock.runSymbol;
    runTf = mock.runTf;
    if (typeof provider.setDataDirectory === 'function') {
      provider.setDataDirectory(mock.dataDirectory);
    }
    console.log(`Provider: ${providerName}`);
    console.log(`Mock file: ${mock.mockFilePath}`);
  }

  const pineTS = new PineTS(provider, runSymbol, runTf, REQUESTED_LIMIT, START_MS, END_MS);
  ctx = await pineTS.run(indicatorCode);
} catch (err) {
  console.error('PineTS run failed:', err.message);
  process.exit(1);
}

const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
const plots = ctx.plots || {};
const plotKeys = Object.keys(plots);
const barCount = ctx.data?.close?.length || Object.keys(ctx.marketData ?? {}).length;

console.log(`Done in ${elapsed}s. Bars: ${barCount}, Plots: ${plotKeys.length}`);

// ─── Extract signals ──────────────────────────────────────────────────────────
// Map of output field name → PineTS plot title
const SIGNAL_PLOT_MAP = {
  long_signal:          'long_raw',
  short_signal:         'short_raw',
  long_gated:           'long_gated',
  short_gated:          'short_gated',
  exit_signal:          'exit_reason',
  stop_hit:             'stop_hit',
  tp_hit:               'tp_hit',
  tp1_hit:              'tp1_hit',
  tp1_fill_price:       'tp1_fill_price',
  tp1_exit_qty:         'tp1_exit_qty',
  tp2_hit:              'tp2_hit',
  direction:            'direction',
  st_line:              'supertrend_line',
  sl_atr:               'sl_atr',
  sl_swing_atr:         'sl_swing_atr',
  tp_atr:               'tp_atr',
  trail_atr:            'trail_atr',
  ma_filter_line:       'ma_filter_line',
  ma_filter_long_ok:    'ma_filter_long_ok',
  ma_filter_short_ok:   'ma_filter_short_ok',
  ma_slope_line:        'ma_slope_line',
  ma_slope_ratio:       'ma_slope_ratio',
  ma_slope_long_ok:     'ma_slope_long_ok',
  ma_slope_short_ok:    'ma_slope_short_ok',
  mcginley_line:        'mcginley_line',
  position_side:        'position_side',     // 1=long, -1=short, 0=flat
  entry_price:          'entry_price',
  avg_entry_price:      'avg_entry_price',
  active_stop_price:    'active_stop_price',
  active_stop_owner_code:'active_stop_owner_code',
  active_tp_price:      'active_tp_price',
  tp1_price:            'tp1_price',
  tp2_price:            'tp2_price',
  tp1_completed:        'tp1_completed',
  be_active:            'be_active',
  trail_active:         'trail_active',
  trail_price:          'trail_price',
  qty:                  'qty',
  sizing_equity:        'sizing_equity_snapshot',
  entry_count:          'entry_count',
  lifecycle_id:         'lifecycle_id',
  initial_risk_per_unit:'initial_risk_per_unit',
  working_exit_reference_qty:'working_exit_reference_qty',
  working_exit_book_version:'working_exit_book_version',
  last_exit_qty:        'last_exit_qty',
  same_bar_reentry_allowed:'same_bar_reentry_allowed',
  block_new_entries_this_bar:'block_new_entries_this_bar',
  exit_bar:             'exit_bar',
  exit_price:           'exit_price',
  pessimistic_sl_hit:   'pessimistic_sl_hit',
  adx:                  'adx',
  chop:                 'chop',
  htf_trend_line:       'htf_trend_line',
  macd_htf_line:        'macd_htf_line',
};

// Helper: get value at bar i from a plot object
function plotVal(plotTitle, i) {
  const plotObj = plots[plotTitle];
  if (!plotObj) return null;
  const dataArr = plotObj.data;
  if (!Array.isArray(dataArr) || dataArr[i] == null) return null;
  const v = dataArr[i]?.value;
  return v === undefined ? null : v;
}

const signals = [];
let longCount = 0, shortCount = 0, exitCount = 0;

for (let i = 0; i < barCount; i++) {
  const bar = ctx.marketData?.[i] ?? {};
  const rec = {
    bar_index:  i,
    timestamp:  bar.openTime ?? ctx.data?.openTime?.[i] ?? null,
    open:       bar.open     ?? ctx.data?.open?.[i]  ?? null,
    high:       bar.high     ?? ctx.data?.high?.[i]  ?? null,
    low:        bar.low      ?? ctx.data?.low?.[i]   ?? null,
    close:      bar.close    ?? ctx.data?.close?.[i] ?? null,
    volume:     bar.volume   ?? ctx.data?.volume?.[i]?? null,
  };

  for (const [outField, plotTitle] of Object.entries(SIGNAL_PLOT_MAP)) {
    rec[outField] = plotVal(plotTitle, i);
  }

  // Normalize boolean-ish signal fields to 0/1
  rec.long_signal  = rec.long_signal  === 1 ? 1 : 0;
  rec.short_signal = rec.short_signal === 1 ? 1 : 0;
  rec.long_gated   = rec.long_gated   === 1 ? 1 : 0;
  rec.short_gated  = rec.short_gated  === 1 ? 1 : 0;
  rec.stop_hit     = rec.stop_hit     === 1 ? 1 : 0;
  rec.tp_hit       = rec.tp_hit       === 1 ? 1 : 0;
  rec.tp1_hit      = rec.tp1_hit      === 1 ? 1 : 0;
  rec.tp2_hit      = rec.tp2_hit      === 1 ? 1 : 0;
  rec.tp1_completed = rec.tp1_completed === 1 ? 1 : 0;
  rec.be_active     = rec.be_active === 1 ? 1 : 0;
  rec.trail_active  = rec.trail_active === 1 ? 1 : 0;
  rec.same_bar_reentry_allowed = rec.same_bar_reentry_allowed === 1 ? 1 : 0;
  rec.block_new_entries_this_bar = rec.block_new_entries_this_bar === 1 ? 1 : 0;
  rec.ma_filter_long_ok = rec.ma_filter_long_ok === 1 ? 1 : 0;
  rec.ma_filter_short_ok = rec.ma_filter_short_ok === 1 ? 1 : 0;
  rec.ma_slope_long_ok = rec.ma_slope_long_ok === 1 ? 1 : 0;
  rec.ma_slope_short_ok = rec.ma_slope_short_ok === 1 ? 1 : 0;

  if (rec.long_signal  === 1) longCount++;
  if (rec.short_signal === 1) shortCount++;
  if (rec.exit_signal  > 0)   exitCount++;

  signals.push(rec);
}

// ─── Output ───────────────────────────────────────────────────────────────────
const output = {
  meta: {
    generated_at: new Date().toISOString(),
    symbol: SYMBOL,
    timeframe: TF,
    bars: barCount,
    requested_bars: HAS_DATE_WINDOW ? null : BARS,
    start: START_MS !== undefined ? new Date(START_MS).toISOString() : null,
    end: END_MS !== undefined ? new Date(END_MS).toISOString() : null,
    source: PINE_PATH,
    pinets_version: '0.9.6',
    strategy_calls_mocked: ['strategy.entry()', 'strategy.exit()', 'strategy.close()'],
    syminfo_patched: { mintick: 0.01, mincontract: 0.001, pointvalue: 1.0 },
    signal_counts: { long: longCount, short: shortCount, exits: exitCount },
    plots_captured: plotKeys,
    input_overrides: inputOverrides,
  },
  signals,
};

writeFileSync(OUT_PATH, JSON.stringify(output, null, 2), 'utf8');

console.log('\n--- Signal Summary ---');
console.log(`Long  entries : ${longCount}`);
console.log(`Short entries : ${shortCount}`);
console.log(`Exit  events  : ${exitCount}`);
console.log(`\nSaved → ${OUT_PATH}  (${Math.round(JSON.stringify(output).length / 1024)} KB)`);



