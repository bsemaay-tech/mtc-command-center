/**
 * REVIEW_ONLY — PineTS exact-parity bridge for QL_ALPHA_LINK_8EMA_1H (producer).
 * ----------------------------------------------------------------------------
 * Runs the LINK 8EMA producer logic through PineTS (the same local Pine runtime
 * the MTC_V2 parity loop uses) on Binance FUTURES klines (verified bar-for-bar
 * identical to the offline data bundle), and writes the per-bar producer signal.
 *
 * Provider.Binance in PineTS returns SPOT (and rejects the .P futures suffix),
 * which does NOT match the futures bundle. So we fetch futures klines ourselves
 * (fapi) and feed them via Provider.Mock — giving exact same-data parity.
 *
 * Output: link_pinets_signals.json  [{ts, close, longSig, ema8, atr14, stopCalc}]
 * Also writes the mock bars actually used to _pinets_mock/ so the Python
 * comparator can score against the identical data.
 */
import { createRequire } from 'module';
import { writeFileSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const require = createRequire(import.meta.url);
const REPO = 'C:/LAB/tradingview-lab';
const { PineTS, Provider } = require(`${REPO}/node_modules/pinets/dist/pinets.min.cjs`);

const __dirname = dirname(fileURLToPath(import.meta.url));
const MOCK_DIR = join(__dirname, '_pinets_mock');
mkdirSync(MOCK_DIR, { recursive: true });

const SYMBOL_FILE = 'LINKUSDT';     // Mock symbol (no .P)
const TF = '1h';
const INTERVAL_MS = 3600_000;
const START_MS = Date.parse('2025-06-01T00:00:00Z');
const END_MS   = Date.parse('2026-04-13T00:00:00Z');

async function fetchFuturesKlines(symbol, interval, startMs, endMs) {
  const out = [];
  let cursor = startMs;
  while (cursor <= endMs) {
    const url = `https://fapi.binance.com/fapi/v1/klines?symbol=${symbol}&interval=${interval}&startTime=${cursor}&endTime=${endMs}&limit=1500`;
    const r = await fetch(url);
    if (!r.ok) throw new Error(`fapi HTTP ${r.status}`);
    const chunk = await r.json();
    if (!Array.isArray(chunk) || chunk.length === 0) break;
    out.push(...chunk);
    const lastOpen = Number(chunk[chunk.length - 1][0]);
    const next = lastOpen + INTERVAL_MS;
    if (next <= cursor) break;
    cursor = next;
  }
  return out;
}

function toMockBars(klines) {
  return klines.map((row) => ({
    openTime: Number(row[0]),
    open: Number(row[1]), high: Number(row[2]), low: Number(row[3]), close: Number(row[4]),
    volume: Number(row[5]),
    closeTime: Number(row[6] ?? (Number(row[0]) + INTERVAL_MS)),
    quoteAssetVolume: Number(row[7] ?? 0), numberOfTrades: Number(row[8] ?? 0),
    takerBuyBaseAssetVolume: Number(row[9] ?? 0), takerBuyQuoteAssetVolume: Number(row[10] ?? 0),
    ignore: row[11] ?? '0',
  }));
}

// Producer-only Pine (indicator mode): exactly the LINK_8EMA_REVIEW entry signal.
const PINE = `//@version=6
indicator("LINK 8EMA producer parity", overlay=true)
pullbackATR = input.float(0.5)
impulseATR  = input.float(1.6)
slopeWin    = input.int(3)
ema8  = ta.ema(close, 8)
atr14 = ta.atr(14)
slope   = ema8 - ema8[slopeWin]
dist    = math.abs(close - ema8) / atr14
impulse = math.abs(close - close[slopeWin]) / atr14
longSig = close > ema8 and slope > 0 and dist <= pullbackATR and impulse[1] >= impulseATR
stopCalc = ta.lowest(low, 3)
plot(longSig ? 1 : 0, "longSig")
plot(ema8, "ema8")
plot(atr14, "atr14")
plot(stopCalc, "stopCalc")
`;

console.log('Fetching Binance FUTURES klines (fapi)...');
const klines = await fetchFuturesKlines(SYMBOL_FILE, TF, START_MS, END_MS);
const bars = toMockBars(klines);
const fileStart = bars[0].openTime, fileEnd = bars[bars.length - 1].closeTime;
const mockFile = join(MOCK_DIR, `${SYMBOL_FILE}-${TF}-${fileStart}-${fileEnd}.json`);
writeFileSync(mockFile, JSON.stringify(bars, null, 0), 'utf8');
console.log(`Mock bars: ${bars.length}  -> ${mockFile}`);

const provider = Provider.Mock;
if (typeof provider.setDataDirectory === 'function') provider.setDataDirectory(MOCK_DIR);

const pineTS = new PineTS(provider, SYMBOL_FILE, TF, null, fileStart, fileEnd);
const ctx = await pineTS.run(PINE);
const plots = ctx.plots || {};
const n = ctx.data?.close?.length || Object.keys(ctx.marketData || {}).length;

function pv(t, i) { const p = plots[t]; return p?.data?.[i]?.value ?? null; }
const rows = [];
for (let i = 0; i < n; i++) {
  const b = ctx.marketData?.[i] ?? {};
  rows.push({
    ts: b.openTime ?? ctx.data?.openTime?.[i] ?? null,
    close: b.close ?? ctx.data?.close?.[i] ?? null,
    longSig: pv('longSig', i), ema8: pv('ema8', i), atr14: pv('atr14', i), stopCalc: pv('stopCalc', i),
  });
}
const outPath = join(__dirname, 'link_pinets_signals.json');
writeFileSync(outPath, JSON.stringify({ symbol: SYMBOL_FILE, tf: TF, mock_file: mockFile, bars: n, rows }, null, 0), 'utf8');
const longCount = rows.filter(r => r.longSig === 1).length;
console.log(`PineTS done. bars=${n} longSignals=${longCount}`);
console.log(`Signals: ${outPath}`);
