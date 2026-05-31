/**
 * validate_syntax.mjs
 *
 * Syntax-validates MTC_V2.pine using the PineTS transpiler.
 *
 * NOTE: @opusaether/pine-transpiler does not exist on npm.
 * We use pinets' internal _transpileCode() as the transpilation
 * layer, which parses and converts Pine Script to a JS function.
 * It is synchronous and throws a detailed error on parse failure.
 *
 * Output: reports/syntax_report.json
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

console.log('=== MTC_V2.pine Syntax Validation ===\n');
console.log(`Source : ${PINE_PATH}`);

const code = readFileSync(PINE_PATH, 'utf8');
const lines = code.split('\n');
console.log(`Lines  : ${lines.length}`);
console.log(`Version: ${lines[0].trim()}\n`);

// ─── 1. Parse / transpile check ──────────────────────────────────────────────
const report = {
  source_path: PINE_PATH,
  lines: lines.length,
  version_header: lines[0].trim(),
  timestamp: new Date().toISOString(),
  transpile_check: null,
  strategy_calls: [],
  ta_calls: [],
  syminfo_calls: [],
  input_calls: [],
  unsupported_constructs: [],
  errors: [],
  warnings: [],
  compatibility_score: null,
};

// Collect all strategy.*, ta.*, syminfo.* and input.* calls by scanning source
const strategyPattern = /strategy\.(entry|exit|close|cancel|order|risk|default_entry_qty|initial_capital)\s*\(/g;
const taPattern = /\bta\.([a-zA-Z_]+)\s*\(/g;
const syminfoPattern = /\bsyminfo\.([a-zA-Z_]+)\b/g;
const inputPattern = /\binput\.(bool|int|float|string|color|source|timeframe|symbol|price)\s*\(/g;
const constPattern = /^const\s+(string|float|int|bool)/m;
const varPattern  = /^var\s+(float|int|bool|string)\s/m;

let m;
const seen = new Set();

while ((m = strategyPattern.exec(code)) !== null) {
  const call = `strategy.${m[1]}()`;
  if (!seen.has(call)) { seen.add(call); report.strategy_calls.push(call); }
}
seen.clear();
while ((m = taPattern.exec(code)) !== null) {
  const call = `ta.${m[1]}()`;
  if (!seen.has(call)) { seen.add(call); report.ta_calls.push(call); }
}
seen.clear();
while ((m = syminfoPattern.exec(code)) !== null) {
  const prop = `syminfo.${m[1]}`;
  if (!seen.has(prop)) { seen.add(prop); report.syminfo_calls.push(prop); }
}
seen.clear();
while ((m = inputPattern.exec(code)) !== null) {
  const call = `input.${m[1]}()`;
  if (!seen.has(call)) { seen.add(call); report.input_calls.push(call); }
}

if (constPattern.test(code)) report.warnings.push('Uses Pine v6 `const` declarations');
if (varPattern.test(code))   report.warnings.push('Uses `var` persistent variable declarations');

console.log('--- Static analysis ---');
console.log(`strategy.* calls found : ${report.strategy_calls.join(', ')}`);
console.log(`ta.* calls found       : ${report.ta_calls.join(', ')}`);
console.log(`syminfo.* props found  : ${report.syminfo_calls.join(', ')}`);
console.log(`input.* types found    : ${report.input_calls.join(', ')}`);
console.log();

// ─── 2. Transpiler parse check ───────────────────────────────────────────────
console.log('--- PineTS transpile check (parse phase) ---');
const pineTS = new PineTS(Provider.Binance, 'BTCUSDT', '1h', 100);

try {
  const compiled = pineTS._transpileCode(code);
  console.log('SYNTAX OK — _transpileCode() returned a function without errors.');
  report.transpile_check = {
    status: 'OK',
    message: '_transpileCode() succeeded — no parse-level errors detected',
    returned_type: typeof compiled,
  };
} catch (err) {
  const errObj = {
    status: 'ERROR',
    message: err.message,
    line: null,
    column: null,
    stack: err.stack ? err.stack.split('\n').slice(0, 8).join('\n') : null,
  };

  // Try to extract line/column from error message (format: "... (line:col)")
  const locMatch = err.message.match(/\((\d+):(\d+)\)/);
  if (locMatch) {
    errObj.line = parseInt(locMatch[1]);
    errObj.column = parseInt(locMatch[2]);
    const srcLine = lines[errObj.line - 1];
    errObj.source_line = srcLine ? srcLine.trim() : '(not found)';
    console.error(`SYNTAX ERROR at line ${errObj.line}, col ${errObj.column}: ${err.message}`);
    if (srcLine) console.error(`  → ${srcLine.trim()}`);
  } else {
    console.error(`SYNTAX ERROR: ${err.message}`);
  }

  report.transpile_check = errObj;
  report.errors.push(errObj);
}

// ─── 3. Strategy-call compatibility assessment ───────────────────────────────
// PineTS is indicator-focused; strategy.* calls operate at broker level and
// are either no-ops or throw at runtime. Mark them as unsupported.
for (const call of report.strategy_calls) {
  report.unsupported_constructs.push({
    construct: call,
    category: 'strategy',
    reason: 'PineTS targets indicator runtime; strategy.* broker calls have no execution model in PineTS',
    workaround: 'Replace with plot() signals in indicator-mode variant',
  });
}

// syminfo.* values depend on TradingView instrument metadata; PineTS may
// stub them with defaults that differ from production exchange values.
for (const prop of report.syminfo_calls) {
  report.unsupported_constructs.push({
    construct: prop,
    category: 'syminfo',
    reason: 'Instrument metadata — PineTS stubs these; values may not match TradingView for BTCUSDT',
    workaround: 'Inject known values (mintick=0.01, pointvalue=1.0, mincontract=0.001) via runtime patch',
  });
}

// ─── 4. Compatibility score estimate ─────────────────────────────────────────
// Rough heuristic: count "working" sections vs total sections (8 in MTC_V2).
// Sections 1-6 (inputs, types, helpers, indicator state, signal producer,
// visualization) are indicator-logic and likely compatible.
// Sections 7-8 use strategy.* heavily → not compatible.
const totalSections = 8;
const workingSections = report.transpile_check?.status === 'OK' ? 6 : 0;
report.compatibility_score = {
  transpile_success: report.transpile_check?.status === 'OK',
  working_sections: workingSections,
  total_sections: totalSections,
  pct: `${Math.round((workingSections / totalSections) * 100)}%`,
  note: 'Sections 1–6 (indicator logic, signals, visualization) should execute. Sections 7–8 (strategy.entry/exit/close, parity export) require mock or strip.',
};

console.log();
console.log('--- Compatibility score ---');
console.log(`  ${report.compatibility_score.pct} (${workingSections}/${totalSections} sections executable)`);
console.log(`  ${report.compatibility_score.note}`);
console.log();
console.log(`Unsupported constructs: ${report.unsupported_constructs.length}`);
for (const u of report.unsupported_constructs) {
  console.log(`  [${u.category}] ${u.construct}`);
}

// ─── 5. Save report ──────────────────────────────────────────────────────────
const outPath = join(REPORTS_DIR, 'syntax_report.json');
writeFileSync(outPath, JSON.stringify(report, null, 2), 'utf8');
console.log(`\nReport saved → ${outPath}`);
