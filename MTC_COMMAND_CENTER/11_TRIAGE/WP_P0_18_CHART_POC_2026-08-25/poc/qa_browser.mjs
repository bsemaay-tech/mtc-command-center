import { spawn } from 'node:child_process';
import { mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const here = path.dirname(fileURLToPath(import.meta.url));
const pages = [
  { id: 'lightweight', file: path.join(here, 'lightweight', 'index.html') },
  { id: 'echarts', file: path.join(here, 'echarts', 'index.html') },
];

const pause = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

async function waitForPort(profile, browser) {
  const marker = path.join(profile, 'DevToolsActivePort');
  for (let attempt = 0; attempt < 200; attempt += 1) {
    if (browser.exitCode !== null) throw new Error(`Browser exited before DevTools was ready: ${browser.exitCode}`);
    try {
      const [port] = (await readFile(marker, 'utf8')).trim().split(/\r?\n/);
      return Number(port);
    } catch {
      await pause(25);
    }
  }
  throw new Error('Timed out waiting for DevToolsActivePort.');
}

async function waitForPage(port, targetUrl) {
  for (let attempt = 0; attempt < 200; attempt += 1) {
    const response = await fetch(`http://127.0.0.1:${port}/json/list`);
    const targets = await response.json();
    const target = targets.find((item) => item.type === 'page' && item.url === targetUrl);
    if (target) return target;
    await pause(25);
  }
  throw new Error(`Timed out waiting for page target: ${targetUrl}`);
}

async function connect(webSocketUrl) {
  const socket = new WebSocket(webSocketUrl);
  const pending = new Map();
  const runtimeErrors = [];
  const externalRequests = [];
  let sequence = 0;
  socket.addEventListener('message', (event) => {
    const message = JSON.parse(event.data);
    if (message.method === 'Runtime.exceptionThrown') {
      const details = message.params.exceptionDetails;
      runtimeErrors.push(`exception: ${details.exception?.description || details.text}`);
    }
    if (message.method === 'Runtime.consoleAPICalled' && message.params.type === 'error') {
      const args = message.params.args.map((arg) => {
        if (Object.hasOwn(arg, 'value')) return typeof arg.value === 'string' ? arg.value : JSON.stringify(arg.value);
        return arg.description || arg.unserializableValue || arg.type;
      });
      runtimeErrors.push(`console.error: ${args.join(' ')}`);
    }
    if (message.method === 'Network.requestWillBeSent') {
      const { method, url } = message.params.request;
      if (!url.startsWith('file:') && !url.startsWith('data:')) externalRequests.push(`${method} ${url}`);
    }
    if (!message.id || !pending.has(message.id)) return;
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(JSON.stringify(message.error)));
    else resolve(message.result);
  });
  await new Promise((resolve, reject) => {
    socket.addEventListener('open', resolve, { once: true });
    socket.addEventListener('error', reject, { once: true });
  });
  return {
    socket,
    runtimeErrors,
    externalRequests,
    send(method, params = {}) {
      sequence += 1;
      return new Promise((resolve, reject) => {
        pending.set(sequence, { resolve, reject });
        socket.send(JSON.stringify({ id: sequence, method, params }));
      });
    },
  };
}

async function evaluate(client, expression) {
  const response = await client.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (response.exceptionDetails) throw new Error(response.exceptionDetails.text);
  return response.result.value;
}

async function runPage(page) {
  const profile = await mkdtemp(path.join(tmpdir(), `wp-p0-18-${page.id}-`));
  const targetUrl = pathToFileURL(page.file).href;
  const browser = spawn(EDGE, [
    '--headless=new',
    '--disable-gpu',
    '--no-first-run',
    '--allow-file-access-from-files',
    '--remote-debugging-port=0',
    `--user-data-dir=${profile}`,
    '--window-size=1440,900',
    targetUrl,
  ], { stdio: ['ignore', 'ignore', 'pipe'], windowsHide: true });
  let browserError = '';
  let client;
  browser.stderr.on('data', (chunk) => { browserError += chunk.toString(); });

  try {
    const port = await waitForPort(profile, browser);
    const target = await waitForPage(port, targetUrl);
    client = await connect(target.webSocketDebuggerUrl);
    await client.send('Runtime.enable');
    await client.send('Page.enable');
    await client.send('Network.enable');
    await client.send('Page.addScriptToEvaluateOnNewDocument', {
      source: `addEventListener('unhandledrejection', (event) => {
        const reason = event.reason instanceof Error ? event.reason.stack || event.reason.message : String(event.reason);
        console.error('__QA_UNHANDLED_REJECTION__', reason);
      });`,
    });
    client.runtimeErrors.length = 0;
    client.externalRequests.length = 0;
    await client.send('Page.navigate', { url: targetUrl });

    const wallStarted = performance.now();
    let state = '';
    for (let attempt = 0; attempt < 1200; attempt += 1) {
      try {
        state = await evaluate(client, 'document.body?.dataset.ready || ""');
      } catch {
        state = '';
      }
      if (state === 'true' || state === 'error') break;
      await pause(50);
    }
    const wallReadyMs = Math.round((performance.now() - wallStarted) * 100) / 100;
    if (state !== 'true') {
      const error = await evaluate(client, 'document.querySelector("#error")?.textContent || "page did not become ready"');
      throw new Error(`${page.id}: ${error}`);
    }

    const panProbe = await evaluate(client, `(async () => {
      const started = performance.now();
      const value = await window.__POC_PAN_PROBE__();
      return { value, wallMs: performance.now() - started };
    })()`);
    const dragProbe = await evaluate(client, `(() => {
      const started = performance.now();
      const value = window.__POC_DRAG_PROBE__();
      return { value, wallMs: performance.now() - started };
    })()`);

    const before = await evaluate(client, `(() => {
      const line = document.querySelector('#drag-line').getBoundingClientRect();
      const shell = document.querySelector('#chart-shell').getBoundingClientRect();
      return { x: line.left + line.width * 0.55, y: line.top + line.height / 2, shellTop: shell.top, level: window.__POC_RESULTS__.currentLevel, moves: window.__POC_RESULTS__.pointerMoves || 0 };
    })()`);
    await client.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: before.x, y: before.y });
    await client.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: before.x, y: before.y, button: 'left', buttons: 1, clickCount: 1 });
    for (let step = 1; step <= 8; step += 1) {
      await client.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: before.x, y: before.y - step * 8, button: 'left', buttons: 1 });
    }
    await client.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: before.x, y: before.y - 64, button: 'left', buttons: 0, clickCount: 1 });
    await pause(250);

    const mouseAfter = await evaluate(client, `({
      level: window.__POC_RESULTS__.currentLevel,
      moves: window.__POC_RESULTS__.pointerMoves || 0
    })`);

    const touchBefore = await evaluate(client, `(() => {
      const line = document.querySelector('#drag-line').getBoundingClientRect();
      return { x: line.left + line.width * 0.45, y: line.top + line.height / 2, level: window.__POC_RESULTS__.currentLevel, moves: window.__POC_RESULTS__.pointerMoves || 0 };
    })()`);
    await client.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 1 });
    await client.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: touchBefore.x, y: touchBefore.y, id: 1, radiusX: 4, radiusY: 4, force: 1 }] });
    for (let step = 1; step <= 6; step += 1) {
      await client.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: touchBefore.x, y: touchBefore.y + step * 8, id: 1, radiusX: 4, radiusY: 4, force: 1 }] });
    }
    await client.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    await pause(300);

    const after = await evaluate(client, `({
      results: window.__POC_RESULTS__,
      levelText: document.querySelector('#m-level').textContent,
      canvases: [...document.querySelectorAll('canvas')].map(canvas => ({ width: canvas.width, height: canvas.height })),
      error: document.querySelector('#error').textContent,
      bodyReady: document.body.dataset.ready
    })`);
    after.results.wallReadyMs = wallReadyMs;
    after.results.panProbeWallMs = Math.round(panProbe.wallMs * 100) / 100;
    after.results.dragProbeWallMs = Math.round(dragProbe.wallMs * 100) / 100;
    after.results.dragBefore = before.level;
    after.results.dragAfter = mouseAfter.level;
    after.results.dragDelta = Math.round((after.results.dragAfter - after.results.dragBefore) * 100) / 100;
    after.results.simulatedMouseMoves = mouseAfter.moves - before.moves;
    after.results.touchBefore = touchBefore.level;
    after.results.touchAfter = after.results.currentLevel;
    after.results.touchDelta = Math.round((after.results.touchAfter - after.results.touchBefore) * 100) / 100;
    after.results.simulatedTouchMoves = (after.results.pointerMoves || 0) - touchBefore.moves;

    const screenshot = await client.send('Page.captureScreenshot', { format: 'png', fromSurface: true });
    const screenshotPath = path.join(tmpdir(), `WP_P0_18_${page.id}_QA.png`);
    await writeFile(screenshotPath, Buffer.from(screenshot.data, 'base64'));
    after.results.screenshot = screenshotPath;
    after.results.runtimeErrors = [...client.runtimeErrors];
    after.results.externalRequests = [...client.externalRequests];

    if (after.error) throw new Error(`${page.id}: ${after.error}`);
    if (after.results.actualPoints !== 100000) throw new Error(`${page.id}: expected 100000 points, got ${after.results.actualPoints}`);
    if (after.results.actualMarkers !== 5000) throw new Error(`${page.id}: expected 5000 markers, got ${after.results.actualMarkers}`);
    if (after.results.programmaticArtifactAnnotations !== 7) throw new Error(`${page.id}: expected 7 programmatic annotations, got ${after.results.programmaticArtifactAnnotations}`);
    if (Math.abs(after.results.dragDelta) < 0.2 || after.results.simulatedMouseMoves < 1) throw new Error(`${page.id}: real pointer drag did not change the level`);
    if (Math.abs(after.results.touchDelta) < 0.2 || after.results.simulatedTouchMoves < 1) throw new Error(`${page.id}: simulated touch drag did not change the level`);
    if (!after.canvases.some((canvas) => canvas.width > 1000 && canvas.height > 500)) throw new Error(`${page.id}: no full-size rendered canvas found`);
    if (after.results.runtimeErrors.length) throw new Error(`${page.id}: runtime error(s): ${after.results.runtimeErrors.join(' | ')}`);
    if (after.results.externalRequests.length) throw new Error(`${page.id}: external network request(s): ${after.results.externalRequests.join(' | ')}`);

    return after;
  } finally {
    client?.socket.close();
    browser.kill();
    await Promise.race([new Promise((resolve) => browser.once('exit', resolve)), pause(2000)]);
    if (browserError && !browserError.includes('fallback_task_provider')) {
      process.stderr.write(browserError.slice(-2000));
    }
  }
}

const output = {};
for (const page of pages) output[page.id] = await runPage(page);
process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
