(() => {
  'use strict';

  const POINTS = 100000;
  const MARKERS = 5000;
  const START = Date.UTC(2025, 0, 1);
  const STEP = 60000;
  const artifactAnnotations = JSON.parse(`{
    "draggableLevel": { "offsetFromLastClose": -1.4 },
    "overlays": [
      { "key": "ema", "label": "EMA", "color": "#60a5fa", "width": 2 },
      { "key": "sl", "label": "SL", "color": "#fb7185", "width": 1 },
      { "key": "tp1", "label": "TP1", "color": "#2dd4bf", "width": 1 },
      { "key": "tp2", "label": "TP2", "color": "#22c55e", "width": 1 },
      { "key": "tp3", "label": "TP3", "color": "#a3e635", "width": 1 },
      { "key": "trail", "label": "Trail", "color": "#f59e0b", "width": 2, "step": true }
    ]
  }`);
  const shell = document.querySelector('#chart-shell');
  const dragLine = document.querySelector('#drag-line');
  const dragLabel = document.querySelector('#drag-label');
  const result = {
    library: 'Apache ECharts',
    version: '6.1.0',
    points: POINTS,
    markers: MARKERS,
    overlays: 7,
    secondPane: true,
    linkedCrosshair: true,
    offline: location.protocol === 'file:',
    pointerEvents: 'PointerEvent' in window,
    maxTouchPoints: navigator.maxTouchPoints || 0,
    programmaticArtifactAnnotations: artifactAnnotations.overlays.length + 1,
    renderer: 'canvas',
    ready: false,
  };
  window.__POC_RESULTS__ = result;

  const showError = (error) => {
    const target = document.querySelector('#error');
    target.style.display = 'block';
    target.textContent = error && error.stack ? error.stack : String(error);
    result.error = target.textContent;
    document.body.dataset.ready = 'error';
  };

  const setMetric = (id, value) => {
    document.querySelector(id).textContent = value;
  };

  const round = (value) => Math.round(value * 100) / 100;

  const percentile = (values, fraction) => {
    const sorted = [...values].sort((a, b) => a - b);
    return sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * fraction))];
  };

  const makeRandom = (seed) => {
    let state = seed >>> 0;
    return () => {
      state ^= state << 13;
      state ^= state >>> 17;
      state ^= state << 5;
      return (state >>> 0) / 4294967296;
    };
  };

  const buildData = () => {
    const started = performance.now();
    const random = makeRandom(0x19c0ffee);
    const times = [];
    const candles = [];
    const ema = [];
    const sl = [];
    const tp1 = [];
    const tp2 = [];
    const tp3 = [];
    const trail = [];
    const equity = [];
    const entries = [];
    const exits = [];
    let close = 100;
    let average = close;
    let account = 10000;
    let trailValue = 96;

    for (let index = 0; index < POINTS; index += 1) {
      const time = START + index * STEP;
      const open = close;
      const shock = (random() - 0.498) * 1.05 + Math.sin(index / 420) * 0.025;
      close = Math.max(18, open + shock);
      const high = Math.max(open, close) + random() * 0.45;
      const low = Math.min(open, close) - random() * 0.45;
      average += (close - average) * 0.045;
      if (index % 220 === 0) trailValue = close - 2.6;
      else if (index % 220 > 55) trailValue = Math.max(trailValue, close - 2.6);
      account += shock * 3.4;

      times.push(index);
      candles.push([round(open), round(close), round(low), round(high)]);
      ema.push(round(average));
      sl.push(round(average - 3.8));
      tp1.push(round(average + 2.1));
      tp2.push(round(average + 4.2));
      tp3.push(round(average + 6.3));
      trail.push(round(trailValue));
      equity.push(round(account));
    }

    const stride = Math.floor(POINTS / MARKERS);
    for (let index = 0; index < POINTS && entries.length + exits.length < MARKERS; index += stride) {
      const point = candles[index];
      if ((entries.length + exits.length) % 2 === 0) entries.push([index, point[2] - 0.3]);
      else exits.push([index, point[3] + 0.3]);
    }

    return { times, candles, ema, sl, tp1, tp2, tp3, trail, equity, entries, exits, generationMs: performance.now() - started };
  };

  try {
    if (!window.echarts) throw new Error('Vendored Apache ECharts did not load.');
    const data = buildData();
    result.actualPoints = data.candles.length;
    result.actualMarkers = data.entries.length + data.exits.length;
    result.generationMs = round(data.generationMs);
    setMetric('#m-data', `${POINTS.toLocaleString()} bars / ${(data.entries.length + data.exits.length).toLocaleString()} markers`);
    setMetric('#m-generate', `${result.generationMs} ms`);

    const chart = echarts.init(document.querySelector('#chart'), null, { renderer: 'canvas', useDirtyRect: true });
    const lastTime = data.times.at(-1);
    let level = data.candles.at(-1)[1] + artifactAnnotations.draggableLevel.offsetFromLastClose;
    let dragging = false;
    let pointerMoves = 0;
    const line = (id, name, values, color, step = false) => ({
      id, name, type: 'line', data: values, showSymbol: false, sampling: 'lttb', animation: false, silent: true,
      step: step ? 'end' : false, lineStyle: { color, width: step ? 2 : 1 }, emphasis: { disabled: true },
    });
    const option = {
      animation: false,
      backgroundColor: '#121a27',
      textStyle: { color: '#9fb0c4' },
      legend: { top: 6, left: 62, textStyle: { color: '#9fb0c4' }, data: artifactAnnotations.overlays.map((spec) => spec.label) },
      axisPointer: { link: [{ xAxisIndex: [0, 1] }], label: { backgroundColor: '#334155' } },
      tooltip: { trigger: 'axis', axisPointer: { type: 'cross' }, confine: true, transitionDuration: 0 },
      grid: [
        { left: 58, right: 78, top: 44, height: 430 },
        { left: 58, right: 78, top: 512, height: 105 },
      ],
      xAxis: [
        { type: 'category', data: data.times, gridIndex: 0, boundaryGap: true, axisLine: { lineStyle: { color: '#42516a' } }, axisLabel: { show: false }, splitLine: { show: true, lineStyle: { color: '#202c3d' } }, axisPointer: { show: true } },
        { type: 'category', data: data.times, gridIndex: 1, boundaryGap: true, axisLine: { lineStyle: { color: '#42516a' } }, axisLabel: { color: '#8392a8', formatter: (value) => new Date(START + Number(value) * STEP).toISOString().slice(11, 16) }, splitLine: { show: true, lineStyle: { color: '#202c3d' } }, axisPointer: { show: true } },
      ],
      yAxis: [
        { scale: true, gridIndex: 0, position: 'right', axisLine: { show: true, lineStyle: { color: '#42516a' } }, axisLabel: { color: '#9fb0c4' }, splitLine: { lineStyle: { color: '#202c3d' } } },
        { scale: true, gridIndex: 1, position: 'right', axisLine: { show: true, lineStyle: { color: '#42516a' } }, axisLabel: { color: '#9fb0c4' }, splitLine: { lineStyle: { color: '#202c3d' } } },
      ],
      dataZoom: [
        { type: 'inside', xAxisIndex: [0, 1], filterMode: 'filter', start: 99.48, end: 100, zoomOnMouseWheel: true, moveOnMouseMove: true, moveOnMouseWheel: false },
        { type: 'slider', xAxisIndex: [0, 1], filterMode: 'filter', start: 99.48, end: 100, bottom: 4, height: 18, borderColor: '#29364b', backgroundColor: '#121a27', fillerColor: 'rgba(96,165,250,.18)', dataBackground: { lineStyle: { color: '#475569' }, areaStyle: { color: '#263548' } }, selectedDataBackground: { lineStyle: { color: '#60a5fa' }, areaStyle: { color: '#1d4ed8' } }, textStyle: { color: '#8392a8' } },
      ],
      series: [
        { id: 'candles', name: 'Price', type: 'candlestick', data: data.candles, animation: false, itemStyle: { color: '#34d399', color0: '#fb7185', borderColor: '#34d399', borderColor0: '#fb7185' }, emphasis: { disabled: true } },
        ...artifactAnnotations.overlays.map((spec) => line(spec.key, spec.label, data[spec.key], spec.color, spec.step)),
        { id: 'entry-markers', name: 'Entries', type: 'scatter', data: data.entries, symbol: 'triangle', symbolSize: 9, progressive: 5000, animation: false, silent: true, itemStyle: { color: '#2dd4bf' } },
        { id: 'exit-markers', name: 'Exits', type: 'scatter', data: data.exits, symbol: 'triangle', symbolRotate: 180, symbolSize: 9, progressive: 5000, animation: false, silent: true, itemStyle: { color: '#fb7185' } },
        { id: 'drag', name: 'Drag level', type: 'line', data: [[0, level], [lastTime, level]], showSymbol: false, animation: false, silent: true, lineStyle: { color: '#fbbf24', width: 2, type: 'dashed' }, emphasis: { disabled: true } },
        { id: 'equity', name: 'Equity', type: 'line', xAxisIndex: 1, yAxisIndex: 1, data: data.equity, showSymbol: false, sampling: 'lttb', animation: false, silent: true, lineStyle: { color: '#a78bfa', width: 2 }, areaStyle: { color: 'rgba(167,139,250,.08)' }, emphasis: { disabled: true } },
      ],
    };

    const ingestStarted = performance.now();
    chart.setOption(option, { notMerge: true, lazyUpdate: false });
    result.ingestMs = round(performance.now() - ingestStarted);
    setMetric('#m-ingest', `${result.ingestMs} ms`);

    const positionDragLine = () => {
      const pixel = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [lastTime, level]);
      if (Array.isArray(pixel) && Number.isFinite(pixel[1])) dragLine.style.top = `${pixel[1]}px`;
      dragLabel.textContent = `LEVEL ${level.toFixed(2)}`;
      dragLine.setAttribute('aria-valuenow', level.toFixed(2));
      setMetric('#m-level', level.toFixed(2));
    };

    // DRAG-COST-START: a DOM hit target and chart-coordinate adapter update a dedicated two-point series.
    const setLevel = (nextLevel) => {
      if (!Number.isFinite(nextLevel)) return;
      level = nextLevel;
      result.currentLevel = round(level);
      positionDragLine();
    };
    const commitLevel = () => {
      const started = performance.now();
      chart.setOption({ series: [{ id: 'drag', data: [[0, level], [lastTime, level]] }] }, { lazyUpdate: false });
      result.dragCommitMs = round(performance.now() - started);
      return result.dragCommitMs;
    };
    const setLevelFromClientY = (clientY) => {
      const bounds = shell.getBoundingClientRect();
      const localY = Math.max(45, Math.min(470, clientY - bounds.top));
      const converted = chart.convertFromPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [chart.getWidth() / 2, localY]);
      if (Array.isArray(converted)) setLevel(Number(converted[1]));
    };
    dragLine.addEventListener('pointerdown', (event) => {
      dragging = true;
      dragLine.classList.add('dragging');
      try { dragLine.setPointerCapture(event.pointerId); } catch (_) { /* synthetic probes have no active pointer */ }
      setLevelFromClientY(event.clientY);
      event.preventDefault();
    });
    dragLine.addEventListener('pointermove', (event) => {
      if (!dragging) return;
      pointerMoves += 1;
      result.pointerMoves = pointerMoves;
      setLevelFromClientY(event.clientY);
    });
    const stopDragging = () => {
      if (dragging) commitLevel();
      dragging = false;
      dragLine.classList.remove('dragging');
    };
    dragLine.addEventListener('pointerup', stopDragging);
    dragLine.addEventListener('pointercancel', stopDragging);
    dragLine.addEventListener('keydown', (event) => {
      if (event.key !== 'ArrowUp' && event.key !== 'ArrowDown') return;
      setLevel(level + (event.key === 'ArrowUp' ? 0.1 : -0.1));
      commitLevel();
      event.preventDefault();
    });
    // DRAG-COST-END

    const runDragProbe = () => {
      const original = level;
      const samples = [];
      for (let index = 0; index < 30; index += 1) {
        const started = performance.now();
        setLevel(original + Math.sin(index / 5) * 1.5);
        samples.push(performance.now() - started);
      }
      setLevel(original);
      const commitMs = commitLevel();
      result.dragDispatchP50Ms = round(percentile(samples, 0.5));
      result.dragDispatchP95Ms = round(percentile(samples, 0.95));
      result.dragProbeUpdates = samples.length;
      result.currentLevel = round(level);
      result.pointerMoves = pointerMoves;
      setMetric('#m-drag', `${result.dragDispatchP95Ms} / ${commitMs} ms`);
      return { before: round(original), after: round(level), p95Ms: result.dragDispatchP95Ms, commitMs };
    };
    window.__POC_DRAG_PROBE__ = runDragProbe;
    window.__POC_PAN_PROBE__ = async () => {
      const samples = [];
      for (let index = 0; index < 30; index += 1) {
        const shift = (index % 15) * 0.01;
        await new Promise((resolve) => requestAnimationFrame(resolve));
        const started = performance.now();
        chart.dispatchAction({ type: 'dataZoom', start: 99.48 - shift, end: 100 - shift });
        await new Promise((resolve) => requestAnimationFrame(resolve));
        samples.push(performance.now() - started);
      }
      chart.dispatchAction({ type: 'dataZoom', start: 99.48, end: 100 });
      result.panFrameP50Ms = round(percentile(samples, 0.5));
      result.panFrameP95Ms = round(percentile(samples, 0.95));
      result.panProbeUpdates = samples.length;
      return { p50Ms: result.panFrameP50Ms, p95Ms: result.panFrameP95Ms };
    };
    document.querySelector('#synthetic-drag').addEventListener('click', runDragProbe);
    new ResizeObserver(() => { chart.resize(); positionDragLine(); }).observe(shell);

    const paintStarted = performance.now();
    let initialized = false;
    chart.on('finished', () => {
      if (initialized) return;
      initialized = true;
      result.firstPaintMs = round(performance.now() - paintStarted);
      setMetric('#m-paint', `${result.firstPaintMs} ms`);
      result.lastEntryPixel = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, data.entries.at(-1));
      result.lastEntryVisible = chart.containPixel({ gridIndex: 0 }, result.lastEntryPixel);
      positionDragLine();
      result.currentLevel = round(level);
      result.ready = true;
      document.body.dataset.ready = 'true';
    });
  } catch (error) {
    showError(error);
  }
})();
