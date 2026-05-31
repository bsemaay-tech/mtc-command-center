import fs from 'node:fs';
import { pathToFileURL } from 'node:url';

function argValue(name, fallback = '') {
  const index = process.argv.indexOf(name);
  return index === -1 ? fallback : process.argv[index + 1] || fallback;
}

const pinePath = argValue('--pine');
const dataPath = argValue('--data');
const outPath = argValue('--out');
const modulePath = argValue('--pinets-module');

try {
  const { PineTS } = await import(pathToFileURL(modulePath).href);
  const pine = fs.readFileSync(pinePath, 'utf8');
  const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
  const runtime = new PineTS(data, 'BINANCE:BTCUSDT.P', '60', data.length);
  const context = await runtime.run(pine, data.length);
  fs.writeFileSync(
    outPath,
    JSON.stringify(
      {
        status: 'success',
        plots: context.plots || {},
        result: context.result || [],
      },
      null,
      2,
    ),
    'utf8',
  );
} catch (error) {
  fs.writeFileSync(
    outPath,
    JSON.stringify(
      {
        status: 'failed',
        error: error && error.stack ? String(error.stack) : String(error),
      },
      null,
      2,
    ),
    'utf8',
  );
  process.exit(2);
}
