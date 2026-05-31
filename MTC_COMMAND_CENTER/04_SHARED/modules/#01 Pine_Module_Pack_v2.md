#01 Pine_Module_Pack_v2.md
MODULES_REUSABLE – Pack v2

(AI-ready, non-repainting, 4H default)

Bu paket, Pine v5 strateji sistemlerinde sinyal ve filtre modüllerinin standart arayüzünü sağlar.
Her modül [line, dir, longRaw, shortRaw] döndürür, emir vermez, repaint-güvenlidir.
Varsayılan HTF = 4H; confirmed-bar mantığı aktif.

0 • Helpers
//@version=5
// ────────────────────────────────────────────────
// Helpers (non-repainting conventions)
// ────────────────────────────────────────────────
f__confirmed(_cond) =>
    barstate.isconfirmed ? _cond : false

f__ma(_src, _len, _type) =>
    _type == "EMA" ? ta.ema(_src, _len) :
    _type == "WMA" ? ta.wma(_src, _len) :
    _type == "RMA" ? ta.rma(_src, _len) :
    _type == "HMA" ? ta.hma(_src, _len) :
    ta.sma(_src, _len)

f__clamp01(x) =>
    math.max(0.0, math.min(1.0, x))

A • Giriş & Çıkış Kalitesi Modülleri

Tüm modüller repaint güvenlidir ve bar kapanışında sinyal üretir.

1️⃣ HTF Trend Filter (4H default)
f_htfTrendFilter_v1(src, htf, baseLen, maType, strict, showVis) =>
    _htfClose = request.security(syminfo.tickerid, htf, close, barmerge.gaps_off, barmerge.lookahead_off)
    _ma = f__ma(_htfClose, baseLen, maType)
    _bull = strict ? (close > _ma and ta.crossover(close, _ma)) : close > _ma
    _bear = strict ? (close < _ma and ta.crossunder(close, _ma)) : close < _ma
    longRaw  = f__confirmed(_bull)
    shortRaw = f__confirmed(_bear)
    dir  = longRaw ? 1 : shortRaw ? -1 : 0
    line = showVis ? (close - _ma) : na
    [line, dir, longRaw, shortRaw]

2️⃣ Volume Above Average
f_volumeAboveAvg_v1(len, minMult, showVis) =>
    _vAvg  = ta.sma(volume, len)
    _ratio = _vAvg > 0 ? (volume / _vAvg) : na
    _ok    = not na(_ratio) and _ratio >= minMult
    longRaw  = f__confirmed(_ok)
    shortRaw = f__confirmed(_ok)
    dir  = _ok ? 1 : 0
    line = showVis ? _ratio : na
    [line, dir, longRaw, shortRaw]

3️⃣ Secondary Confirm (RSI / MACD)
f_secondaryConfirm_v1(src, useRSI, rsiLen, ob, os, useMACD, fast, slow, signal, showVis) =>
    _rsi = ta.rsi(src, rsiLen)
    [macdLine, sigLine, hist] = ta.macd(src, fast, slow, signal)
    _rsiLong  = not useRSI  ? true : (_rsi >= 50 and _rsi < ob)
    _rsiShort = not useRSI  ? true : (_rsi <= 50 and _rsi > os)
    _macdLong  = not useMACD ? true : (hist > 0)
    _macdShort = not useMACD ? true : (hist < 0)
    _longOk  = _rsiLong and _macdLong
    _shortOk = _rsiShort and _macdShort
    longRaw  = f__confirmed(_longOk)
    shortRaw = f__confirmed(_shortOk)
    dir  = longRaw ? 1 : shortRaw ? -1 : 0
    line = showVis ? (useMACD ? hist : _rsi - 50) : na
    [line, dir, longRaw, shortRaw]

4️⃣ ATR Volatility Filter
f_atrVolFilter_v1(atrLen, lowThr, blockLowVol) =>
    _atr = ta.atr(atrLen)
    _pct = close != 0 ? (_atr / close) * 100.0 : na
    _ok  = not blockLowVol ? true : (not na(_pct) and _pct >= lowThr)
    longRaw  = f__confirmed(_ok)
    shortRaw = f__confirmed(_ok)
    dir  = _ok ? 1 : 0
    line = _pct
    [line, dir, longRaw, shortRaw]

5️⃣ Session Filter (+ Skip First Minutes)
f_sessionFilter_v1(sessStr, skipFirstMins) =>
    _inSess = not na(time(timeframe.period, sessStr))
    _sessStart = _inSess and not _inSess[1]
    var int _mins = 1e9
    _mins := _sessStart ? 0 : (_inSess ? (_mins + int(timeframe.in_seconds(timeframe.period)/60)) : 1e9)
    _ok = _inSess and (_mins >= skipFirstMins)
    longRaw  = f__confirmed(_ok)
    shortRaw = f__confirmed(_ok)
    dir  = _ok ? 1 : 0
    [na, dir, longRaw, shortRaw]

6️⃣ ADX Regime Filter
f_adxRegime_v1(len, th) =>
    [_, _, adxVal] = ta.dmi(len, len)
    _ok = not na(adxVal) and adxVal >= th
    longRaw  = f__confirmed(_ok)
    shortRaw = f__confirmed(_ok)
    dir  = _ok ? 1 : 0
    [adxVal, dir, longRaw, shortRaw]

7️⃣ Candle Pattern Confirm
f_candlePattern_v1(kind, minBody, showVis) =>
    _atr = ta.atr(14)
    _body = math.abs(close - open)
    _bodyOk = _atr > 0 ? (_body / _atr) >= minBody : true
    _bullEng = close > open and close[1] < open[1] and close >= open[1] and open <= close[1]
    _bearEng = close < open and close[1] > open[1] and close <= open[1] and open >= close[1]
    _bull =
         kind == "Engulfing" ? _bullEng :
         kind == "Hammer"    ? (close > open and (math.min(open,close) - low) > _body*2) :
         kind == "PinBar"    ? (high - math.max(open,close) <= _body and (math.min(open,close)-low) > _body*2) :
         false
    _bear =
         kind == "Engulfing" ? _bearEng :
         kind == "Hammer"    ? (close < open and (high - math.max(open,close)) > _body*2) :
         kind == "PinBar"    ? (high - math.max(open,close) > _body*2) :
         false
    longRaw  = f__confirmed(_bull and _bodyOk)
    shortRaw = f__confirmed(_bear and _bodyOk)
    dir  = longRaw ? 1 : shortRaw ? -1 : 0
    line = showVis ? _body : na
    [line, dir, longRaw, shortRaw]

8️⃣ SR Proximity Filter
// NOTE: NA-SAFE - handles uninitialized pivot values gracefully
f_srProximity_v1(src, swingLen, tolerance) =>
    _ph = ta.pivothigh(high, swingLen, swingLen)
    _pl = ta.pivotlow(low,  swingLen, swingLen)
    var float _lastH = na, _lastL = na
    if not na(_ph)
        _lastH := _ph
    if not na(_pl)
        _lastL := _pl
    _tol = tolerance / 100.0
    // NA-SAFE: only compute proximity if pivot values exist and are non-zero
    _nearH = not na(_lastH) and _lastH != 0 and math.abs(src - _lastH)/_lastH <= _tol
    _nearL = not na(_lastL) and _lastL != 0 and math.abs(src - _lastL)/_lastL <= _tol
    longRaw  = f__confirmed(_nearL)
    shortRaw = f__confirmed(_nearH)
    dir  = longRaw ? 1 : shortRaw ? -1 : 0
    [dir==1?_lastL:dir==-1?_lastH:na, dir, longRaw, shortRaw]

9️⃣ Bollinger Squeeze Break
f_bbSqueezeBreak_v1(len, mult, squeezeThr) =>
    _basis = ta.sma(close, len)
    _dev   = mult * ta.stdev(close, len)
    _up = _basis + _dev
    _dn = _basis - _dev
    _bw = _basis != 0 ? ((_up - _dn)/_basis)*100 : na
    _squeeze = not na(_bw) and _bw <= squeezeThr
    _long = _squeeze and ta.crossover(close, _up)
    _short= _squeeze and ta.crossunder(close, _dn)
    longRaw  = f__confirmed(_long)
    shortRaw = f__confirmed(_short)
    dir  = longRaw ? 1 : shortRaw ? -1 : 0
    [ _bw, dir, longRaw, shortRaw]

🔟 RSI Divergence (pivot-based)
f_rsiDivergence_v1(src, len, swingLen) =>
    _r = ta.rsi(src, len)
    _pL = ta.pivotlow(low, swingLen, swingLen)
    _pH = ta.pivothigh(high, swingLen, swingLen)
    var float pL1=na,pL2=na,rL1=na,rL2=na,pH1=na,pH2=na,rH1=na,rH2=na
    if not na(_pL)
        pL2:=pL1, rL2:=rL1, pL1:=_pL, rL1:=_r[swingLen]
    if not na(_pH)
        pH2:=pH1, rH2:=rH1, pH1:=_pH, rH1:=_r[swingLen]
    _bull = not na(pL1) and not na(pL2) and pL1<pL2 and rL1>rL2
    _bear = not na(pH1) and not na(pH2) and pH1>pH2 and rH1<rH2
    longRaw  = f__confirmed(_bull)
    shortRaw = f__confirmed(_bear)
    dir  = longRaw ? 1 : shortRaw ? -1 : 0
    [_r, dir, longRaw, shortRaw]

11️⃣ MA Trend Filter
f_maTrend_v1(src, type, lenFast, lenSlow, showVis) =>
    _f = f__ma(src, lenFast, type)
    _s = f__ma(src, lenSlow, type)
    _dir = _f > _s ? 1 : -1
    longRaw  = f__confirmed(ta.crossover(_f, _s))
    shortRaw = f__confirmed(ta.crossunder(_f, _s))
    line = showVis ? (_dir==1?_f:_s):na
    [line, _dir, longRaw, shortRaw]

12️⃣ VWAP Confluence
f_vwapConfluence_v1(showVis) =>
    _vwap = ta.vwap(hlc3)
    _bull = close >= _vwap
    _bear = close <  _vwap
    longRaw  = f__confirmed(_bull)
    shortRaw = f__confirmed(_bear)
    dir  = longRaw ? 1 : -1
    [showVis?_vwap:na, dir, longRaw, shortRaw]

13️⃣ Pullback Entry
// NOTE: NA-SAFE - handles zero/na MA values gracefully
f_pullbackEntry_v1(src, maLen, maxDist) =>
    _ma = ta.ema(src, maLen)
    // NA-SAFE: avoid division by zero when MA is 0 or na
    _dist = not na(_ma) and _ma != 0 ? math.abs(src - _ma) / _ma * 100 : na
    _near = not na(_dist) and _dist <= maxDist
    _dir = not na(_ma) and src >= _ma ? 1 : -1
    longRaw  = f__confirmed(_near and _dir == 1)
    shortRaw = f__confirmed(_near and _dir == -1)
    [_ma, _dir, longRaw, shortRaw]

14️⃣ Signal Quality Score
f_signalQualityScore_v1(sig1, sig2, sig3, sig4, sig5, showVis) =>
    _sum = (sig1?1:0)+(sig2?1:0)+(sig3?1:0)+(sig4?1:0)+(sig5?1:0)
    _score = _sum/5.0
    longRaw  = f__confirmed(_score>=0.6)
    shortRaw = f__confirmed(_score>=0.6)
    [showVis?_score:na, _score>=0.6?1:0, longRaw, shortRaw]

15️⃣ SuperTrend + Double CCI (setup → trigger + re-entry)
// Notes:
// - Intended for Heikin Ashi charts if the video requires it (this module uses chart OHLC).
// - Uses SuperTrend flip OR CCI setup when SuperTrend regime already aligned.
// - Conflict policy: prioritize long.
f_stDoubleCciSignal_v1(stAtrLen, stFactor, cciFastLen, cciSlowLen, cciSmooth, cciLevel, setupLookback, showVis) =>
    [stLine, stDir] = ta.supertrend(stFactor, stAtrLen)
    _stUp = stDir == 1
    _stFlipUp   = _stUp and stDir[1] == -1
    _stFlipDown = (not _stUp) and stDir[1] == 1

    _cciFast = ta.cci(close, cciFastLen)
    _cciSlowBase = ta.cci(close, cciSlowLen)
    _cciSlowLine = ta.sma(_cciSlowBase, cciSmooth)

    _cciLongSetup  = ta.crossover(_cciFast, _cciSlowLine) and _cciFast < -cciLevel
    _cciShortSetup = ta.crossunder(_cciFast, _cciSlowLine) and _cciFast > cciLevel

    _bsLong  = nz(ta.barssince(_cciLongSetup),  1000000)
    _bsShort = nz(ta.barssince(_cciShortSetup), 1000000)

    _longCond  = (_stFlipUp and _bsLong < setupLookback) or (_cciLongSetup and _stUp)
    _shortCond = (_stFlipDown and _bsShort < setupLookback) or (_cciShortSetup and not _stUp)
    _shortCond := _shortCond and not _longCond

    longRaw  = f__confirmed(_longCond)
    shortRaw = f__confirmed(_shortCond)
    dir  = _stUp ? 1 : -1
    line = showVis ? stLine : na
    [line, dir, longRaw, shortRaw]

    B • Stop/TP & Yönetim – Advisor Modülleri
//@version=5
f_atrStopAdvisor_v1(atrLen, mult) =>
    _atr = ta.atr(atrLen)
    line = _atr * mult
    dir  = _atr > _atr[1] ? 1 : -1
    longRaw  = f__confirmed(true)
    shortRaw = f__confirmed(true)
    [line, dir, longRaw, shortRaw]

f_partialTPAdvisor_v1(tp1R, tp2R) =>
    line = tp2R
    dir  = tp2R > tp1R ? 1 : 0
    longRaw  = f__confirmed(tp1R > 0 and tp2R > 0)
    shortRaw = f__confirmed(tp1R > 0 and tp2R > 0)
    [line, dir, longRaw, shortRaw]

f_breakEvenAdvisor_v1(triggerR) =>
    line = triggerR
    dir  = 1
    longRaw  = f__confirmed(triggerR > 0)
    shortRaw = f__confirmed(triggerR > 0)
    [line, dir, longRaw, shortRaw]

f_timeExitAdvisor_v1(maxBars) =>
    line = maxBars
    dir  = 1
    longRaw  = f__confirmed(maxBars > 0)
    shortRaw = f__confirmed(maxBars > 0)
    [line, dir, longRaw, shortRaw]

f_trailingAdvisor_v1(mode, atrLen, mult, pct) =>
    _atr = ta.atr(atrLen)
    _dist = mode == "ATR" ? (_atr * mult) : (close * (pct / 100))
    line = _dist
    dir  = 1
    longRaw  = f__confirmed(true)
    shortRaw = f__confirmed(true)
    [line, dir, longRaw, shortRaw]

f_volAdaptiveTP_v1(atrLen, k) =>
    _atr = ta.atr(atrLen)
    line = _atr * k
    dir  = _atr > _atr[1] ? 1 : -1
    longRaw  = f__confirmed(true)
    shortRaw = f__confirmed(true)
    [line, dir, longRaw, shortRaw]

f_oppositeSignalExit_v1(longRaw, shortRaw) =>
    _exitLong  = shortRaw
    _exitShort = longRaw
    line = _exitLong ? 1 : _exitShort ? -1 : 0
    dir  = line
    [line, dir, f__confirmed(_exitLong), f__confirmed(_exitShort)]

f_sessionCloseExit_v1(sessCloseOnly) =>
    _isNewDay = ta.change(time("D"))
    _flag = sessCloseOnly and _isNewDay
    line = _flag ? 1 : 0
    dir  = _flag ? -1 : 0
    longRaw  = f__confirmed(_flag)
    shortRaw = f__confirmed(_flag)
    [line, dir, longRaw, shortRaw]

f_fibTargetsAdvisor_v1(src, swingLen) =>
    _ph = ta.pivothigh(high, swingLen, swingLen)
    _pl = ta.pivotlow(low, swingLen, swingLen)
    var float lastH=na,lastL=na
    if not na(_ph)
        lastH:=_ph
    if not na(_pl)
        lastL:=_pl
    _rng = (not na(lastH) and not na(lastL)) ? (lastH-lastL):na
    line = not na(_rng)?(_rng*1.618):na
    dir  = 1
    longRaw  = f__confirmed(not na(line))
    shortRaw = f__confirmed(not na(line))
    [line, dir, longRaw, shortRaw]

f_psarTrailAdvisor_v1(step, max) =>
    _psar = ta.sar(step, max)
    line = _psar
    dir  = close >= _psar ? 1 : -1
    longRaw  = f__confirmed(dir==1)
    shortRaw = f__confirmed(dir==-1)
    [line, dir, longRaw, shortRaw]

f_chandelierAdvisor_v1(atrLen, mult) =>
    _atr = ta.atr(atrLen)
    _longStop  = ta.highest(high, atrLen) - _atr * mult
    _shortStop = ta.lowest(low,  atrLen) + _atr * mult
    _dir = close >= ta.sma(close, atrLen) ? 1 : -1
    line = _dir == 1 ? _longStop : _shortStop
    longRaw  = f__confirmed(_dir == 1)
    shortRaw = f__confirmed(_dir == -1)
    [line, _dir, longRaw, shortRaw]

C • Drawdown & Sermaye Koruma – Guard Modülleri
//@version=5

// ════════════════════════════════════════════════════════════════════════════
// ENGINE-DEPENDENT GUARDS (uses strategy.*)
// These functions require strategy.equity / strategy.closedtrades / strategy.position_*
// For modular use, prefer the *_safe versions below with Guard Adapter Layer in master.
// Dir semantics: +1 = trade allowed, -1 = halt/block
// ════════════════════════════════════════════════════════════════════════════

// ────────────────────────────────────────────────
// ENGINE-DEPENDENT (uses strategy.*) — use via Guard Adapter Layer in master
// Deprecated for modular use — prefer f_dailyLossLimit_safe + adapter in master
// ────────────────────────────────────────────────
f_dailyLossLimit_v1(pct) =>
    var float dayEqStart = na
    if ta.change(time("D"))
        dayEqStart := strategy.equity
    dayEqStart := na(dayEqStart)?strategy.equity:dayEqStart
    _dd = (strategy.equity - dayEqStart)/dayEqStart*100
    _halt = _dd <= -pct
    [ _dd, _halt?-1:1, f__confirmed(not _halt), f__confirmed(not _halt)]

// ────────────────────────────────────────────────
// ENGINE-DEPENDENT (uses strategy.*) — use via Guard Adapter Layer in master
// Deprecated for modular use — prefer f_consecutiveLossHalt_safe + adapter in master
// ────────────────────────────────────────────────
f_consecutiveLossHalt_v1(n) =>
    var int lossStreak = 0
    _ct = strategy.closedtrades
    if ta.change(_ct)
        _p = strategy.closedtrades.profit(_ct-1)
        lossStreak := _p<0 ? (lossStreak+1):0
    _halt = lossStreak>=n
    [lossStreak, _halt?-1:1, f__confirmed(not _halt), f__confirmed(not _halt)]

// ────────────────────────────────────────────────
// ENGINE-DEPENDENT (uses strategy.*) — use via Guard Adapter Layer in master
// Deprecated for modular use — prefer f_maxDrawdownGuard_safe + adapter in master
// ────────────────────────────────────────────────
f_maxDrawdownGuard_v1(pct) =>
    var float peakEq = strategy.equity
    peakEq := math.max(peakEq, strategy.equity)
    _dd = (strategy.equity - peakEq)/peakEq*100
    _halt = _dd <= -pct
    [_dd, _halt?-1:1, f__confirmed(not _halt), f__confirmed(not _halt)]

// ────────────────────────────────────────────────
// ENGINE-DEPENDENT (uses strategy.*) — use via Guard Adapter Layer in master
// Deprecated for modular use — prefer f_dailyTradeCap_safe + adapter in master
// ────────────────────────────────────────────────
f_dailyTradeCap_v1(n) =>
    var int dayTrades = 0
    if ta.change(time("D"))
        dayTrades := 0
    if ta.change(strategy.closedtrades)
        dayTrades += 1
    _ok = dayTrades < n
    [dayTrades, _ok?1:-1, f__confirmed(_ok), f__confirmed(_ok)]

// ────────────────────────────────────────────────
// MASTER-SAFE (no strategy.* dependency)
// ────────────────────────────────────────────────
f_volPositionScaler_v1(atrLen, lowThr, scale) =>
    _atr = ta.atr(atrLen)
    _pct = close!=0?(_atr/close)*100:na
    _mult = (not na(_pct) and _pct<lowThr)?scale:1
    [_mult, _mult<1?-1:1, f__confirmed(true), f__confirmed(true)]

// ────────────────────────────────────────────────
// ENGINE-DEPENDENT (uses strategy.*) — use via Guard Adapter Layer in master
// Deprecated for modular use — prefer f_equityCurveFilter_safe + adapter in master
// ────────────────────────────────────────────────
f_equityCurveFilter_v1(len) =>
    _eqMa = ta.sma(strategy.equity, len)
    _ok = strategy.equity >= _eqMa
    [strategy.equity-_eqMa, _ok?1:-1, f__confirmed(_ok), f__confirmed(_ok)]

// ────────────────────────────────────────────────
// MASTER-SAFE (no strategy.* dependency)
// ────────────────────────────────────────────────
f_weekendBlocker_v1(enabled) =>
    _dow = dayofweek(time)
    _wknd = (_dow==dayofweek.saturday) or (_dow==dayofweek.sunday)
    _ok = not enabled or not _wknd
    [_wknd?1:0, _ok?1:-1, f__confirmed(_ok), f__confirmed(_ok)]

// ────────────────────────────────────────────────
// MASTER-SAFE (no strategy.* dependency)
// ────────────────────────────────────────────────
f_correlationGuard_v1(symbolsCsv, maxCorr) =>
    _s1 = str.trim(str.split(symbolsCsv, \",\").get(0))
    _s2 = str.trim(str.split(symbolsCsv, \",\").size()>1?str.split(symbolsCsv, \",\").get(1):\"\")
    _c2 = _s2!=\"\"?request.security(_s2,timeframe.period,close,barmerge.gaps_off,barmerge.lookahead_off):na
    _corr = not na(_c2)?ta.correlation(close,_c2,50):0.0
    _ok = math.abs(_corr)<=maxCorr
    [_corr, _ok?1:-1, f__confirmed(_ok), f__confirmed(_ok)]

// ════════════════════════════════════════════════════════════════════════════
// MASTER-SAFE GUARD ALTERNATIVES (*_safe)
// These functions accept pre-computed metrics from the Guard Adapter Layer.
// They do NOT call strategy.* internally — fully modular and portable.
// Dir semantics: +1 = trade allowed, -1 = halt/block
// ════════════════════════════════════════════════════════════════════════════

// ────────────────────────────────────────────────
// Daily Loss Limit (MASTER-SAFE)
// Inputs: eqNow = current equity, dayEqStart = equity at day start, pct = max loss %
// ────────────────────────────────────────────────
f_dailyLossLimit_safe(eqNow, dayEqStart, pct) =>
    _dd = dayEqStart != 0 ? (eqNow - dayEqStart) / dayEqStart * 100 : 0.0
    _halt = _dd <= -pct
    dir = _halt ? -1 : 1
    longRaw  = f__confirmed(not _halt)
    shortRaw = f__confirmed(not _halt)
    [_dd, dir, longRaw, shortRaw]

// ────────────────────────────────────────────────
// Consecutive Loss Halt (MASTER-SAFE)
// Inputs: lossStreak = current consecutive loss count, n = max allowed streak
// ────────────────────────────────────────────────
f_consecutiveLossHalt_safe(lossStreak, n) =>
    _halt = lossStreak >= n
    dir = _halt ? -1 : 1
    longRaw  = f__confirmed(not _halt)
    shortRaw = f__confirmed(not _halt)
    [float(lossStreak), dir, longRaw, shortRaw]

// ────────────────────────────────────────────────
// Max Drawdown Guard (MASTER-SAFE)
// Inputs: eqNow = current equity, peakEq = peak equity, pct = max DD %
// ────────────────────────────────────────────────
f_maxDrawdownGuard_safe(eqNow, peakEq, pct) =>
    _dd = peakEq != 0 ? (eqNow - peakEq) / peakEq * 100 : 0.0
    _halt = _dd <= -pct
    dir = _halt ? -1 : 1
    longRaw  = f__confirmed(not _halt)
    shortRaw = f__confirmed(not _halt)
    [_dd, dir, longRaw, shortRaw]

// ────────────────────────────────────────────────
// Daily Trade Cap (MASTER-SAFE)
// Inputs: dayTrades = trades today, n = max trades per day
// ────────────────────────────────────────────────
f_dailyTradeCap_safe(dayTrades, n) =>
    _ok = dayTrades < n
    dir = _ok ? 1 : -1
    longRaw  = f__confirmed(_ok)
    shortRaw = f__confirmed(_ok)
    [float(dayTrades), dir, longRaw, shortRaw]

// ────────────────────────────────────────────────
// Equity Curve Filter (MASTER-SAFE)
// Inputs: eqNow = current equity, eqMa = MA of equity
// ────────────────────────────────────────────────
f_equityCurveFilter_safe(eqNow, eqMa) =>
    _ok = eqNow >= eqMa
    dir = _ok ? 1 : -1
    longRaw  = f__confirmed(_ok)
    shortRaw = f__confirmed(_ok)
    [eqNow - eqMa, dir, longRaw, shortRaw]

// ────────────────────────────────────────────────
// Max Exposure Guard (MASTER-SAFE)
// Inputs: openCount = number of open positions, maxOpen = max allowed
// ────────────────────────────────────────────────
f_maxExposureGuard_safe(openCount, maxOpen) =>
    _ok = openCount < maxOpen
    dir = _ok ? 1 : -1
    longRaw  = f__confirmed(_ok)
    shortRaw = f__confirmed(_ok)
    [float(openCount), dir, longRaw, shortRaw]

// ────────────────────────────────────────────────
// Cooldown After Trade (MASTER-SAFE)
// Inputs: barsSinceExit = bars since last exit, bars = cooldown period
// ────────────────────────────────────────────────
f_cooldownAfterTrade_safe(barsSinceExit, bars) =>
    _cool = barsSinceExit < bars
    _ok = not _cool
    dir = _ok ? 1 : -1
    line = _cool ? (bars - barsSinceExit) : 0.0
    longRaw  = f__confirmed(_ok)
    shortRaw = f__confirmed(_ok)
    [line, dir, longRaw, shortRaw]

// ────────────────────────────────────────────────
// MAE Guard (MASTER-SAFE)
// Inputs: adversePct = current adverse excursion %, maxMAE_R = max allowed
// ────────────────────────────────────────────────
f_maeGuard_safe(adversePct, maxMAE_R) =>
    _halt = adversePct <= -maxMAE_R
    dir = _halt ? -1 : 1
    longRaw  = f__confirmed(not _halt)
    shortRaw = f__confirmed(not _halt)
    [adversePct, dir, longRaw, shortRaw]

D • Risk Yönetimi – Derin Seviye
//@version=5

// ────────────────────────────────────────────────
// MASTER-SAFE (no strategy.* dependency)
// ⚠️ WARNING: Kelly fraction is ADVISORY ONLY - do not use as direct position size!
// Full Kelly can be extremely aggressive. Consider using fractional Kelly (e.g., K/2 or K/4).
// Always cap output with f_calc_qty() and max_leverage_cap in master template.
// ────────────────────────────────────────────────
f_kellyFraction_v1(winRate, rr) =>
    _p = f__clamp01(winRate)
    _b = math.max(rr, 0.0001)  // NA-SAFE: prevent division by zero
    _k = math.max(0, math.min(_p - (1 - _p) / _b, 1))
    [_k, _k > 0 ? 1 : 0, f__confirmed(true), f__confirmed(true)]

// ────────────────────────────────────────────────
// MASTER-SAFE (no strategy.* dependency)
// ────────────────────────────────────────────────
f_volAdjSizer_v1(atrLen, baseRiskPct) =>
    _atr = ta.atr(atrLen)
    _pct = close!=0?(_atr/close)*100:na
    _adj = not na(_pct)?(baseRiskPct/math.max(_pct,0.1)):baseRiskPct
    [_adj, 1, f__confirmed(true), f__confirmed(true)]

// ────────────────────────────────────────────────
// ENGINE-DEPENDENT (uses strategy.*) — use via Guard Adapter Layer in master
// Deprecated for modular use — prefer f_maxExposureGuard_safe + adapter in master
// ────────────────────────────────────────────────
f_maxExposureGuard_v1(maxOpen) =>
    _open = strategy.position_size!=0?1:0
    _ok = _open < maxOpen
    [_open, _ok?1:-1, f__confirmed(_ok), f__confirmed(_ok)]

// ────────────────────────────────────────────────
// ENGINE-DEPENDENT (uses strategy.*) — use via Guard Adapter Layer in master
// Deprecated for modular use — prefer f_cooldownAfterTrade_safe + adapter in master
// ────────────────────────────────────────────────
f_cooldownAfterTrade_v1(bars) =>
    var int lastExitBar=na
    if ta.change(strategy.closedtrades)
        lastExitBar:=bar_index
    _cool = not na(lastExitBar) and (bar_index-lastExitBar)<bars
    _ok = not _cool
    [_cool?(bars-(bar_index-lastExitBar)):0, _ok?1:-1, f__confirmed(_ok), f__confirmed(_ok)]

// ────────────────────────────────────────────────
// ENGINE-DEPENDENT (uses strategy.*) — use via Guard Adapter Layer in master
// Deprecated for modular use — prefer f_maeGuard_safe + adapter in master
// ────────────────────────────────────────────────
f_maeGuard_v1(maxMAE_R) =>
    _adverse = strategy.position_size>0?((low-strategy.position_avg_price)/strategy.position_avg_price)*100:
               strategy.position_size<0?((strategy.position_avg_price-high)/strategy.position_avg_price)*100:0
    _halt = _adverse <= -maxMAE_R
    [_adverse, _halt?-1:1, f__confirmed(not _halt), f__confirmed(not _halt)]

f_stressMode_v1(toggle) =>
    [toggle?1:0, toggle?-1:1, f__confirmed(not toggle), f__confirmed(not toggle)]

f_badRegimeDetector_v1(atrLen, adxLen, adxTh, chopLen, chopTh) =>
    [_,_,adxVal] = ta.dmi(adxLen, adxLen)
    _sumTR = ta.sum(ta.tr(true), chopLen)
    _hh = ta.highest(high,chopLen)
    _ll = ta.lowest(low,chopLen)
    _chop = (_hh!=_ll)?100*math.log10(_sumTR/(_hh-_ll))/math.log10(chopLen):na
    _bad = adxVal<adxTh and _chop>chopTh
    [_chop, _bad?-1:1, f__confirmed(not _bad), f__confirmed(not _bad)]

f_liquidityFilter_v1(rangeLen, minDollarVol) =>
    _dv = volume*close
    _dvAvg = ta.sma(_dv, rangeLen)
    _ok = not na(_dvAvg) and _dvAvg >= minDollarVol
    [_dvAvg, _ok?1:-1, f__confirmed(_ok), f__confirmed(_ok)]

    E • Tasarım & Test Araçları
//@version=5
f_debugPlots_v1(toggle) =>
    line = toggle ? 1 : 0
    dir  = toggle ? 1 : 0
    longRaw  = f__confirmed(toggle)
    shortRaw = f__confirmed(toggle)
    [line, dir, longRaw, shortRaw]

f_repaintCheck_v1() =>
    _ok = barstate.isconfirmed
    line = _ok ? 1 : 0
    dir  = _ok ? 1 : -1
    longRaw  = _ok
    shortRaw = _ok
    [line, dir, longRaw, shortRaw]

f_feeSlippageModel_v1(feePct, slipTicks) =>
    line = feePct
    dir  = slipTicks > 0 ? 1 : 0
    longRaw  = f__confirmed(true)
    shortRaw = f__confirmed(true)
    [line, dir, longRaw, shortRaw]

Section 4 • Entegrasyon Örneği (HTF = 4H)

Bu örnek emir vermez, yalnızca longSignal_raw ve shortSignal_raw üretir.
Motor, bu sinyalleri final karar mekanizmasında kullanır.

// ────────────────────────────────────────────────
// Section 4 – Signal Plugin (örnek kullanım)
// ────────────────────────────────────────────────
showHtf = input.bool(true, "HTF vis", group="Signal")
htfTf   = input.timeframe("240", "HTF (varsayılan 4H)", group="Signal")
htfLen  = input.int(50, "HTF MA Len", 20, 200, group="Signal")
htfType = input.string("EMA", "HTF MA Type", options=["EMA","SMA","WMA","RMA","HMA"], group="Signal")
htfStrict = input.bool(true, "HTF Strict", group="Signal")

[lHtf, dHtf, longHtf, shortHtf] = f_htfTrendFilter_v1(close, htfTf, htfLen, htfType, htfStrict, showHtf)

lenVol  = input.int(20, "Vol len", 5, 100, group="Signal")
minMult = input.float(1.2, "Vol minMult", 0.5, 5.0, group="Signal")
[lVol, dVol, volOkL, volOkS] = f_volumeAboveAvg_v1(lenVol, minMult, false)

useSess = input.bool(true, "Use Session", group="Signal")
sessStr = input.session("0930-1600:12345", "Session", group="Signal")
skipM   = input.int(5, "Skip first mins", 0, 30, group="Signal")
[lSess, dSess, sessOkL, sessOkS] = useSess ? f_sessionFilter_v1(sessStr, skipM) : [na, 1, true, true]

adxLen = input.int(14, "ADX Len", 7, 21, group="Signal")
adxTh  = input.float(20, "ADX Th", 15, 25, group="Signal")
[lAdx, dAdx, adxOkL, adxOkS] = f_adxRegime_v1(adxLen, adxTh)

// Sinyal kalitesi (örnek)
[lQ, dQ, qOkL, qOkS] = f_signalQualityScore_v1(longHtf, volOkL, sessOkL, adxOkL, true, true)

longSignal_raw  := qOkL
shortSignal_raw := qOkS

plot(showHtf ? lHtf : na, title="HTF delta", display=display.none)
plot(lAdx, title="ADX", display=display.none)
plot(lQ, title="QualityScore", display=display.none)

// ════════════════════════════════════════════════════════════════════════════
// GUARD ADAPTER LAYER — MASTER_TEMPLATE_CORE Entegrasyonu
// ════════════════════════════════════════════════════════════════════════════
// Bu snippet, engine-dependent guard modüllerini MASTER_TEMPLATE_CORE ile
// kullanmak için gereken metrik hesaplamalarını ve _safe fonksiyon çağrılarını
// gösterir. Section 5 öncesine veya ayrı bir Guard bölümüne eklenebilir.
//
// NOT: Bu kod emir vermez, sadece boolean guard flag'leri üretir.
// ════════════════════════════════════════════════════════════════════════════

/*
// ────────────────────────────────────────────────
// GUARD ADAPTER LAYER (Section 4.5 or before Section 5)
// ────────────────────────────────────────────────

// ═══ INPUTS ═══
grpGuard = "🛡️ Guard Filters"

use_daily_loss_guard    = input.bool(false, "Use Daily Loss Guard",      group = grpGuard)
daily_loss_guard_pct    = input.float(5.0,  "Daily Loss Guard %",        group = grpGuard, minval = 0.1, step = 0.5)

use_max_dd_guard        = input.bool(false, "Use Max Drawdown Guard",    group = grpGuard)
max_dd_guard_pct        = input.float(10.0, "Max DD Guard %",            group = grpGuard, minval = 0.1, step = 0.5)

use_consec_loss_guard   = input.bool(false, "Use Consecutive Loss Halt", group = grpGuard)
consec_loss_max         = input.int(3,      "Max Consecutive Losses",    group = grpGuard, minval = 1)

use_daily_trade_guard   = input.bool(false, "Use Daily Trade Cap",       group = grpGuard)
daily_trade_cap         = input.int(5,      "Max Trades Per Day",        group = grpGuard, minval = 1)

use_cooldown_guard      = input.bool(false, "Use Trade Cooldown",        group = grpGuard)
cooldown_bars           = input.int(5,      "Cooldown Bars",             group = grpGuard, minval = 1)

use_eq_curve_guard      = input.bool(false, "Use Equity Curve Filter",   group = grpGuard)
eq_curve_ma_len         = input.int(20,     "Equity MA Length",          group = grpGuard, minval = 5)

use_mae_guard           = input.bool(false, "Use MAE Guard",             group = grpGuard)
mae_max_pct             = input.float(2.0,  "Max MAE %",                 group = grpGuard, minval = 0.1, step = 0.1)


// ═══ METRICS COLLECTION ═══
// These are computed centrally so *_safe functions can be portable.

float eqNow = strategy.equity

// Day-start equity (reset on day change)
var float guard_dayEqStart = na
if ta.change(time("D"))
    guard_dayEqStart := strategy.equity
guard_dayEqStart := na(guard_dayEqStart) ? strategy.equity : guard_dayEqStart

// Peak equity for DD calculation
var float guard_peakEq = strategy.equity
guard_peakEq := math.max(guard_peakEq, strategy.equity)

// Consecutive loss streak
var int guard_lossStreak = 0
int closedCount = strategy.closedtrades
if ta.change(closedCount)
    float lastProfit = strategy.closedtrades.profit(closedCount - 1)
    guard_lossStreak := lastProfit < 0 ? (guard_lossStreak + 1) : 0

// Daily trade count
var int guard_dayTrades = 0
if ta.change(time("D"))
    guard_dayTrades := 0
if ta.change(strategy.closedtrades)
    guard_dayTrades += 1

// Bars since last exit
var int guard_lastExitBar = na
if ta.change(strategy.closedtrades)
    guard_lastExitBar := bar_index
int guard_barsSinceExit = na(guard_lastExitBar) ? 9999 : (bar_index - guard_lastExitBar)

// Equity curve MA
float guard_eqMa = ta.sma(strategy.equity, eq_curve_ma_len)

// Current MAE (Maximum Adverse Excursion)
float guard_adversePct = 
    strategy.position_size > 0 ? ((low - strategy.position_avg_price) / strategy.position_avg_price) * 100 :
    strategy.position_size < 0 ? ((strategy.position_avg_price - high) / strategy.position_avg_price) * 100 :
    0.0

// Open position count (for exposure guard — 1 if in position, 0 if flat)
int guard_openCount = strategy.position_size != 0 ? 1 : 0


// ═══ GUARD CALLS (using _safe functions) ═══

// Daily Loss Limit
bool guardOk_dailyLoss = true
if use_daily_loss_guard
    [_, _, okL, okS] = f_dailyLossLimit_safe(eqNow, guard_dayEqStart, daily_loss_guard_pct)
    guardOk_dailyLoss := okL  // symmetric for long/short

// Max Drawdown
bool guardOk_maxDD = true
if use_max_dd_guard
    [_, _, okL, okS] = f_maxDrawdownGuard_safe(eqNow, guard_peakEq, max_dd_guard_pct)
    guardOk_maxDD := okL

// Consecutive Loss Halt
bool guardOk_consecLoss = true
if use_consec_loss_guard
    [_, _, okL, okS] = f_consecutiveLossHalt_safe(guard_lossStreak, consec_loss_max)
    guardOk_consecLoss := okL

// Daily Trade Cap
bool guardOk_tradeCap = true
if use_daily_trade_guard
    [_, _, okL, okS] = f_dailyTradeCap_safe(guard_dayTrades, daily_trade_cap)
    guardOk_tradeCap := okL

// Trade Cooldown
bool guardOk_cooldown = true
if use_cooldown_guard
    [_, _, okL, okS] = f_cooldownAfterTrade_safe(guard_barsSinceExit, cooldown_bars)
    guardOk_cooldown := okL

// Equity Curve Filter
bool guardOk_eqCurve = true
if use_eq_curve_guard
    [_, _, okL, okS] = f_equityCurveFilter_safe(eqNow, guard_eqMa)
    guardOk_eqCurve := okL

// MAE Guard (only active when in position)
bool guardOk_mae = true
if use_mae_guard and strategy.position_size != 0
    [_, _, okL, okS] = f_maeGuard_safe(guard_adversePct, mae_max_pct)
    guardOk_mae := okL


// ═══ COMBINED GUARD FLAG ═══
// This flag can be ANDed with canOpenLong / canOpenShort in Section 5.
bool allGuardsOk = guardOk_dailyLoss and guardOk_maxDD and guardOk_consecLoss and 
                   guardOk_tradeCap and guardOk_cooldown and guardOk_eqCurve and guardOk_mae

// ═══ USAGE IN SECTION 5 ═══
// Replace:
//   bool canOpenLong  = longEdge  and canTradeToday and ...
// With:
//   bool canOpenLong  = longEdge  and canTradeToday and allGuardsOk and ...
//
// Or selectively apply individual guard flags as needed.

*/

F • Legacy Quick Examples (migrated from removed #00a file)

These are intentionally small legacy snippets kept only as quick-reference
examples. They are not the canonical runtime source for MTC V1/V2.

1) Simple signal module examples

```pine
//@version=5
// Module: Supertrend
f_supertrend_signal(_atrLen, _factor, _useWicks) =>
    _atr = _factor * ta.atr(_atrLen)
    _src = hl2
    _h = _useWicks ? high : close
    _l = _useWicks ? low  : close
    _isDoji = open == close and open == low and open == high

    _longStop     = _src - _atr
    _longStopPrev = nz(_longStop[1], _longStop)
    if _longStop > 0
        if _isDoji
            _longStop := _longStopPrev
        else
            _longStop := _l[1] > _longStopPrev ? math.max(_longStop, _longStopPrev) : _longStop
    else
        _longStop := _longStopPrev

    _shortStop     = _src + _atr
    _shortStopPrev = nz(_shortStop[1], _shortStop)
    if _shortStop > 0
        if _isDoji
            _shortStop := _shortStopPrev
        else
            _shortStop := _h[1] < _shortStopPrev ? math.min(_shortStop, _shortStopPrev) : _shortStop
    else
        _shortStop := _shortStopPrev

    var int _dir = 1
    _dir := _dir == -1 and _h > _shortStopPrev ? 1 : _dir == 1 and _l < _longStopPrev ? -1 : _dir

    _line = _dir == 1 ? _longStop : _shortStop
    _longRaw  = _dir == 1
    _shortRaw = _dir == -1
    [_line, _dir, _longRaw, _shortRaw]
```

```pine
//@version=5
// Module: EMA Cross
f_ema_cross_signal(_src, _fast, _slow) =>
    _f = ta.ema(_src, _fast)
    _s = ta.ema(_src, _slow)
    _dir = _f > _s ? 1 : -1
    _line = _dir == 1 ? _f : _s
    _longRaw  = ta.crossover(_f, _s)
    _shortRaw = ta.crossunder(_f, _s)
    [_line, _dir, _longRaw, _shortRaw]
```

```pine
//@version=5
// Module: Donchian Breakout
f_donchian_signal(_len) =>
    _hi = ta.highest(high, _len)
    _lo = ta.lowest(low,  _len)
    _mid = (_hi + _lo) / 2.0
    _longRaw  = ta.crossover(close, _hi)
    _shortRaw = ta.crossunder(close, _lo)
    _dir = close >= _mid ? 1 : -1
    _line = _dir == 1 ? _hi : _lo
    [_line, _dir, _longRaw, _shortRaw]
```

2) Tiny helper example

```pine
//@version=5
// Helper: Higher-timeframe boolean confirmation (no lookahead)
f_htf_confirm(_cond, _tf) =>
    request.security(syminfo.tickerid, _tf, _cond, lookahead=barmerge.lookahead_off)
```

3) Minimal Section-4 adapter example

```pine
sigChoice = input.string("Supertrend", "Signal Module",
     options=["Supertrend","EMA Cross","Donchian"], group=grpSignal)

emaFast = input.int(20, "EMA Fast", group=grpSignal)
emaSlow = input.int(50, "EMA Slow", group=grpSignal)
donLen  = input.int(20, "Donchian Length", group=grpSignal)

bool longSignal_raw  = false
bool shortSignal_raw = false
float supertrendLine = na
int   supertrendDir  = 0

if useStrategy
    if sigChoice == "Supertrend"
        [supertrendLine, supertrendDir, longSignal_raw, shortSignal_raw] =
            f_supertrend_signal(st_atr_len, st_factor, st_use_wicks)
    else if sigChoice == "EMA Cross"
        [supertrendLine, supertrendDir, longSignal_raw, shortSignal_raw] =
            f_ema_cross_signal(close, emaFast, emaSlow)
    else if sigChoice == "Donchian"
        [supertrendLine, supertrendDir, longSignal_raw, shortSignal_raw] =
            f_donchian_signal(donLen)
else
    supertrendLine := na
    supertrendDir  := 0
    longSignal_raw  := false
    shortSignal_raw := false

longSignal  = longSignal_raw  and allowLong  and enableLong
shortSignal = shortSignal_raw and allowShort and enableShort

bool longEdge  = longSignal  and not longSignal[1]
bool shortEdge = shortSignal and not shortSignal[1]
```
