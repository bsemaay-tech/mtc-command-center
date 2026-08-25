(() => {
  'use strict';

  const POINTS = 100000;
  const MARKERS = 5000;
  const START = Math.floor(Date.UTC(2025, 0, 1) / 1000);
  const STEP = 60;
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
    library: 'TradingView Lightweight Charts',
    version: '5.2.1',
    points: POINTS,
    markers: MARKERS,
    overlays: 7,
    secondPane: true,
    linkedCrosshair: true,
    offline: location.protocol === 'file:',
    pointerEvents: 'PointerEvent' in window,
    maxTouchPoints: navigator.maxTouchPoints || 0,
    programmaticArtifactAnnotations: artifactAnnotations.overlays.length + 1,
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
    const bars = [];
    const ema = [];
    const sl = [];
    const tp1 = [];
    const tp2 = [];
    const tp3 = [];
    const trail = [];
    const equity = [];
    const markers = [];
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

      bars.push({ time, open: round(open), high: round(high), low: round(low), close: round(close) });
      ema.push({ time, value: round(average) });
      sl.push({ time, value: round(average - 3.8) });
      tp1.push({ time, value: round(average + 2.1) });
      tp2.push({ time, value: round(average + 4.2) });
      tp3.push({ time, value: round(average + 6.3) });
      trail.push({ time, value: round(trailValue) });
      equity.push({ time, value: round(account) });
    }

    const stride = Math.floor(POINTS / MARKERS);
    for (let index = 0; index < POINTS && markers.length < MARKERS; index += stride) {
      const entry = markers.length % 2 === 0;
      markers.push({
        time: bars[index].time,
        position: entry ? 'belowBar' : 'aboveBar',
        color: entry ? '#2dd4bf' : '#fb7185',
        shape: entry ? 'arrowUp' : 'arrowDown',
      });
    }

    return { bars, ema, sl, tp1, tp2, tp3, trail, equity, markers, generationMs: performance.now() - started };
  };

  try {
    if (!window.LightweightCharts) throw new Error('Vendored Lightweight Charts did not load.');
    const data = buildData();
    result.actualPoints = data.bars.length;
    result.actualMarkers = data.markers.length;
    result.generationMs = round(data.generationMs);
    setMetric('#m-data', `${POINTS.toLocaleString()} bars / ${data.markers.length.toLocaleString()} markers`);
    setMetric('#m-generate', `${result.generationMs} ms`);

    const chart = LightweightCharts.createChart(document.querySelector('#chart'), {
      autoSize: true,
      height: shell.clientHeight,
      attributionLogo: true,
      layout: { background: { type: 'solid', color: '#111a25' }, textColor: '#9fb0c4', panes: { separatorColor: '#263548', separatorHoverColor: '#36506b', enableResize: true } },
      grid: { vertLines: { color: '#1c2a3a' }, horzLines: { color: '#1c2a3a' } },
      crosshair: { mode: LightweightCharts.CrosshairMode.Normal, vertLine: { color: '#64748b' }, horzLine: { color: '#64748b' } },
      rightPriceScale: { borderColor: '#314156' },
      timeScale: { borderColor: '#314156', timeVisible: true, secondsVisible: false },
      handleScale: { axisPressedMouseMove: true, mouseWheel: true, pinch: true },
      handleScroll: { mouseWheel: true, pressedMouseMove: true, horzTouchDrag: true, vertTouchDrag: true },
    });

    const candles = chart.addSeries(LightweightCharts.CandlestickSeries, {
      upColor: '#2dd4bf', downColor: '#fb7185', borderVisible: false, wickUpColor: '#2dd4bf', wickDownColor: '#fb7185',
    });
    const addLine = (color, width = 1, lineType = LightweightCharts.LineType.Simple) => chart.addSeries(LightweightCharts.LineSeries, {
      color, lineWidth: width, lineType, crosshairMarkerVisible: false, lastValueVisible: false, priceLineVisible: false,
    });
    const overlaySeries = new Map(artifactAnnotations.overlays.map((spec) => [
      spec.key,
      addLine(spec.color, spec.width, spec.step ? LightweightCharts.LineType.WithSteps : LightweightCharts.LineType.Simple),
    ]));
    const equity = chart.addSeries(LightweightCharts.LineSeries, {
      color: '#a78bfa', lineWidth: 2, priceLineVisible: false, lastValueVisible: true,
    }, 1);

    const ingestStarted = performance.now();
    candles.setData(data.bars);
    artifactAnnotations.overlays.forEach((spec) => overlaySeries.get(spec.key).setData(data[spec.key]));
    equity.setData(data.equity);
    LightweightCharts.createSeriesMarkers(candles, data.markers, { autoScale: true });
    result.ingestMs = round(performance.now() - ingestStarted);
    setMetric('#m-ingest', `${result.ingestMs} ms`);
    chart.timeScale().setVisibleLogicalRange({ from: POINTS - 520, to: POINTS + 20 });
    const panes = chart.panes();
    if (panes[0]) panes[0].setHeight(500);
    if (panes[1]) panes[1].setHeight(140);

    let level = data.bars.at(-1).close + artifactAnnotations.draggableLevel.offsetFromLastClose;
    let dragging = false;
    let pointerMoves = 0;
    const nativeLevel = candles.createPriceLine({
      price: level, color: '#f59e0b', lineWidth: 2, lineStyle: LightweightCharts.LineStyle.Dashed, axisLabelVisible: true, title: 'DRAG',
    });

    const positionDragLine = () => {
      const coordinate = candles.priceToCoordinate(level);
      if (coordinate !== null) dragLine.style.top = `${coordinate}px`;
      dragLabel.textContent = `LEVEL ${level.toFixed(2)}`;
      dragLine.setAttribute('aria-valuenow', level.toFixed(2));
      setMetric('#m-level', level.toFixed(2));
    };

    // DRAG-COST-START: custom interaction required because the library has no native draggable price line.
    const setLevel = (nextLevel) => {
      if (!Number.isFinite(nextLevel)) return;
      level = nextLevel;
      result.currentLevel = round(level);
      nativeLevel.applyOptions({ price: level });
      positionDragLine();
    };
    const setLevelFromClientY = (clientY) => {
      const localY = Math.max(4, Math.min(chart.paneSize(0).height - 4, clientY - shell.getBoundingClientRect().top));
      setLevel(Number(candles.coordinateToPrice(localY)));
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
    const stopDragging = () => { dragging = false; dragLine.classList.remove('dragging'); };
    dragLine.addEventListener('pointerup', stopDragging);
    dragLine.addEventListener('pointercancel', stopDragging);
    dragLine.addEventListener('keydown', (event) => {
      if (event.key !== 'ArrowUp' && event.key !== 'ArrowDown') return;
      setLevel(level + (event.key === 'ArrowUp' ? 0.1 : -0.1));
      event.preventDefault();
    });
    // DRAG-COST-END

    const runDragProbe = () => {
      const original = level;
      const samples = [];
      for (let index = 0; index < 80; index += 1) {
        const started = performance.now();
        setLevel(original + Math.sin(index / 7) * 1.5);
        samples.push(performance.now() - started);
      }
      setLevel(original);
      result.dragDispatchP50Ms = round(percentile(samples, 0.5));
      result.dragDispatchP95Ms = round(percentile(samples, 0.95));
      result.dragProbeUpdates = samples.length;
      result.currentLevel = round(level);
      result.pointerMoves = pointerMoves;
      setMetric('#m-drag', `${result.dragDispatchP95Ms} ms`);
      return { before: round(original), after: round(level), p95Ms: result.dragDispatchP95Ms };
    };
    window.__POC_DRAG_PROBE__ = runDragProbe;
    window.__POC_PAN_PROBE__ = async () => {
      const samples = [];
      for (let index = 0; index < 30; index += 1) {
        const offset = index % 30;
        await new Promise((resolve) => requestAnimationFrame(resolve));
        const started = performance.now();
        chart.timeScale().setVisibleLogicalRange({ from: POINTS - 520 - offset, to: POINTS + 20 - offset });
        await new Promise((resolve) => requestAnimationFrame(resolve));
        samples.push(performance.now() - started);
      }
      chart.timeScale().setVisibleLogicalRange({ from: POINTS - 520, to: POINTS + 20 });
      result.panFrameP50Ms = round(percentile(samples, 0.5));
      result.panFrameP95Ms = round(percentile(samples, 0.95));
      result.panProbeUpdates = samples.length;
      return { p50Ms: result.panFrameP50Ms, p95Ms: result.panFrameP95Ms };
    };
    document.querySelector('#synthetic-drag').addEventListener('click', runDragProbe);
    new ResizeObserver(positionDragLine).observe(shell);

    const paintStarted = performance.now();
    requestAnimationFrame(() => requestAnimationFrame(() => {
      result.firstPaintMs = round(performance.now() - paintStarted);
      setMetric('#m-paint', `${result.firstPaintMs} ms`);
      positionDragLine();
      result.currentLevel = round(level);
      result.ready = true;
      document.body.dataset.ready = 'true';
    }));
  } catch (error) {
    showError(error);
  }
})();
