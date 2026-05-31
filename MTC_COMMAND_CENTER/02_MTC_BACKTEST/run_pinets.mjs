/**
 * run_pinets.mjs
 *
 * Runs MTC_V2.pine through PineTS with Binance BTCUSDT 1h 500-bar data.
 *
 * Execution plan:
 *   1. Attempt full run (strategy.* calls present) → expected to error.
 *   2. On failure, extract the error details precisely.
 *   3. Run indicator-only variant (strategy.* stripped, signal plots preserved).
 *   4. Extract all plot() series as bar-by-bar signal vectors.
 *   5. Save to reports/pinets_signals.json
 *
 * Output: reports/pinets_signals.json
 */

import { createRequire } from 'module';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join, resolve } from 'path';

const require = createRequire(import.meta.url);
const { PineTS, Provider } = require('./node_modules/pinets/dist/pinets.min.cjs');

const __dirname = dirname(fileURLToPath(import.meta.url));
const PINE_PATH = resolve(__dirname, '../01_MTC_PROJECT/01_PINE/MTC_V2.pine');
const REPORTS_DIR = resolve(__dirname, 'reports');
mkdirSync(REPORTS_DIR, { recursive: true });

console.log('=== MTC_V2.pine PineTS Execution ===\n');
console.log(`Source : ${PINE_PATH}`);

const originalCode = readFileSync(PINE_PATH, 'utf8');
const BARS = 500;
const SYMBOL = 'BTCUSDT';
const TF = '1h';

// ─── Helper: build indicator-only variant ────────────────────────────────────
// Strips strategy() declaration + all strategy.* calls.
// Replaces with indicator() so PineTS treats it as pure indicator.
// The signal plots (long_raw, short_raw, position_side etc.) stay intact.
function buildIndicatorVariant(code) {
  // Pine `if` blocks cannot have empty bodies — stripping strategy.* lines
  // entirely leaves orphaned `else` clauses that fail to parse.
  // Instead: REPLACE each strategy.* call line with a no-op assignment that
  // preserves the if/else block structure.
  let counter = 0;
  const stripped = code
    // Replace strategy() declaration with indicator()
    .replace(
      /^strategy\("MTC V2"[^)]*\)/m,
      'indicator("MTC V2 - Indicator Mode", overlay=true)'
    )
    // Replace each strategy.* call line with a harmless Pine no-op
    .replace(/^(\s*)strategy\.[a-zA-Z_]+\s*\([^)]*\)\s*$/gm, (match, indent) => {
      return `${indent}bool _strat_noop_${counter++} = false`;
    });

  return stripped;
}

// ─── Result container ─────────────────────────────────────────────────────────
const report = {
  timestamp: new Date().toISOString(),
  symbol: SYMBOL,
  timeframe: TF,
  bars_requested: BARS,
  full_run: null,
  indicator_run: null,
  signals: null,
  errors: [],
};

// ─── 1. Full run attempt (with strategy.* calls) ──────────────────────────────
console.log(`--- Attempt 1: Full strategy run (${BARS} bars ${SYMBOL} ${TF}) ---`);
try {
  const pineTS = new PineTS(Provider.Binance, SYMBOL, TF, BARS);
  const ctx = await pineTS.run(originalCode);
  const plots = ctx.plots || {};
  report.full_run = {
    status: 'OK',
    bars_returned: ctx.marketData?.candles?.length ?? BARS,
    plot_keys: Object.keys(plots),
    note: 'Unexpectedly succeeded — strategy.* calls were silently ignored or stubbed.',
  };
  console.log(`Full run OK. Plots: ${Object.keys(plots).join(', ')}`);
} catch (err) {
  const errInfo = {
    status: 'ERROR',
    message: err.message,
    // PineRuntimeError often has construct, line, funcName fields
    construct: err.construct ?? null,
    func_name: err.funcName ?? null,
    line: err.line ?? null,
    stack_top: err.stack ? err.stack.split('\n').slice(0, 6).join(' | ') : null,
  };
  report.full_run = errInfo;
  report.errors.push({ phase: 'full_run', ...errInfo });
  console.log(`Full run FAILED: ${err.message}`);
  if (err.funcName) console.log(`  → Failed function: ${err.funcName}`);
  if (err.line)     console.log(`  → At line: ${err.line}`);
}

// ─── 2. Indicator-only run ────────────────────────────────────────────────────
console.log('\n--- Attempt 2: Indicator-only variant (strategy.* stripped) ---');
const indicatorCode = buildIndicatorVariant(originalCode);

// Verify the declaration was swapped
const declLine = indicatorCode.split('\n').find(l => l.trim().startsWith('indicator(') || l.trim().startsWith('strategy('));
console.log(`Declaration line: ${declLine?.trim()}`);

try {
  const pineTS2 = new PineTS(Provider.Binance, SYMBOL, TF, BARS);
  const ctx2 = await pineTS2.run(indicatorCode);
  const plots = ctx2.plots || {};
  const plotKeys = Object.keys(plots);

  console.log(`Indicator run OK. ${plotKeys.length} plots: ${plotKeys.join(', ')}`);

  // ─── 3. Extract bar-by-bar signal data ───────────────────────────────────
  // PineTS context layout:
  //   ctx.marketData = { 0: {open,high,low,close,volume,openTime,...}, 1: ... }
  //   ctx.data       = { open: [...], high: [...], close: [...], openTime: [...] }
  //   ctx.plots      = { 'Plot Title': [ {time, value, options}, ... ] }

  const signalPlots = [
    'long_raw', 'short_raw', 'direction', 'position_side',
    'entry_price', 'avg_entry_price', 'active_stop_price', 'active_tp_price',
    'exit_reason', 'exit_bar', 'stop_hit', 'tp_hit',
    'supertrend_line', 'sl_atr', 'tp_atr',
    'sizing_equity_snapshot', 'qty', 'exit_price',
    'Long Raw', 'Short Raw',
  ];

  // Bar count from ctx.data arrays (most reliable)
  const closeArr = ctx2.data?.close ?? [];
  const barCount = closeArr.length || Object.keys(ctx2.marketData ?? {}).length;

  const signals = [];

  for (let i = 0; i < barCount; i++) {
    const bar = ctx2.marketData?.[i] ?? {};
    const rec = {
      bar_index: i,
      timestamp: bar.openTime ?? (ctx2.data?.openTime?.[i] ?? null),
      open:   bar.open   ?? (ctx2.data?.open?.[i]   ?? null),
      high:   bar.high   ?? (ctx2.data?.high?.[i]   ?? null),
      low:    bar.low    ?? (ctx2.data?.low?.[i]    ?? null),
      close:  bar.close  ?? (ctx2.data?.close?.[i]  ?? null),
      volume: bar.volume ?? (ctx2.data?.volume?.[i] ?? null),
    };
    for (const plotKey of signalPlots) {
      const plotObj = plots[plotKey];
      // PineTS plot shape: { data: [{time, value, options}, ...], options, title, ... }
      const dataArr = plotObj?.data;
      if (Array.isArray(dataArr) && dataArr[i] != null) {
        rec[plotKey] = dataArr[i]?.value ?? null;
      }
    }
    signals.push(rec);
  }

  // Summarise entry signals (plot() emits 1.0 for true, 0.0 for false)
  const longSignals  = signals.filter(s => s.long_raw  === 1).length;
  const shortSignals = signals.filter(s => s.short_raw === 1).length;
  console.log(`\nSignal summary over ${barCount} bars:`);
  console.log(`  Long signals  : ${longSignals}`);
  console.log(`  Short signals : ${shortSignals}`);

  report.indicator_run = {
    status: 'OK',
    bars_returned: barCount,
    plot_keys: plotKeys,
    long_signals: longSignals,
    short_signals: shortSignals,
    stripped_strategy_calls: [
      'strategy.entry()', 'strategy.exit()', 'strategy.close()',
    ],
    note: 'indicator() mode — broker execution removed; all signal/indicator plots captured.',
  };
  report.signals = signals;

} catch (err2) {
  const errInfo2 = {
    status: 'ERROR',
    message: err2.message,
    construct: err2.construct ?? null,
    func_name: err2.funcName ?? null,
    line: err2.line ?? null,
    stack_top: err2.stack ? err2.stack.split('\n').slice(0, 6).join(' | ') : null,
  };
  report.indicator_run = errInfo2;
  report.errors.push({ phase: 'indicator_run', ...errInfo2 });
  console.log(`Indicator run FAILED: ${err2.message}`);
}

// ─── 4. Save report ──────────────────────────────────────────────────────────
const outPath = join(REPORTS_DIR, 'pinets_signals.json');
writeFileSync(outPath, JSON.stringify(report, null, 2), 'utf8');
console.log(`\nReport saved → ${outPath}`);
if (report.signals) {
  console.log(`Signal rows   : ${report.signals.length}`);
}
