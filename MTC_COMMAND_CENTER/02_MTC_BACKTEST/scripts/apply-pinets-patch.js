#!/usr/bin/env node
/**
 * apply-pinets-patch.js
 *
 * Applies the Series numeric-coercion patch to pinets.min.cjs after every
 * `npm install`. This patch fixes EMA/RMA NaN production in transpiled
 * PineTS formulas where bare Series objects enter JS arithmetic
 * (e.g. `alpha * close`).
 *
 * Root cause documented in HANDOFF.md:
 *   node_modules/pinets/dist/pinets.min.cjs
 *
 * The patch adds valueOf / Symbol.toPrimitive to the Series prototype so
 * that `Number(series)` and implicit arithmetic coercion resolve to the
 * current-bar scalar value instead of NaN.
 *
 * Safe to re-run: idempotent check prevents double-patching.
 */

const fs = require('fs');
const path = require('path');

const TARGET = path.join(__dirname, '..', 'node_modules', 'pinets', 'dist', 'pinets.min.cjs');

const PATCH_MARKER = '// Codex local patch for pinets@0.9.6:';

const PATCH_CODE = `
// Codex local patch for pinets@0.9.6:
// Some transpiled recursive EMA/RMA formulas leave bare Series objects in JS arithmetic
// (for example \`alpha * close\`). Give Series numeric coercion semantics so those expressions
// resolve to the current-bar scalar value instead of NaN.
try{typeof y=="function"&&(typeof y.prototype.valueOf!="function"||Number.isNaN(Number(new y([1]))))&&(y.prototype.valueOf=function(){return this.get(0)},y.prototype[Symbol.toPrimitive]=function(t){const e=this.get(0);return t==="string"?String(e):e})}catch{}`;

if (!fs.existsSync(TARGET)) {
  console.warn('[apply-pinets-patch] Target not found (pinets not installed yet):', TARGET);
  process.exit(0);
}

const content = fs.readFileSync(TARGET, 'utf8');

if (content.includes(PATCH_MARKER)) {
  console.log('[apply-pinets-patch] Patch already applied — skipping.');
  process.exit(0);
}

// Append patch before the sourcemap comment (or at end)
const SOURCE_MAP_COMMENT = '//# sourceMappingURL=';
const smIdx = content.lastIndexOf(SOURCE_MAP_COMMENT);

let patched;
if (smIdx !== -1) {
  patched = content.slice(0, smIdx) + PATCH_CODE + '\n' + content.slice(smIdx);
} else {
  patched = content + PATCH_CODE + '\n';
}

fs.writeFileSync(TARGET, patched, 'utf8');
console.log('[apply-pinets-patch] Patch applied successfully to:', TARGET);
