from __future__ import annotations

from collections import deque


MA_TYPE_SMA = "SMA"
MA_TYPE_EMA = "EMA"
MA_TYPE_RMA = "RMA"
MA_TYPE_WMA = "WMA"
SUPPORTED_MA_TYPES = {MA_TYPE_SMA, MA_TYPE_EMA, MA_TYPE_RMA, MA_TYPE_WMA}


class MovingAverageTracker:
    def __init__(self, *, length: int, ma_type: str, enabled: bool = True) -> None:
        self.length = int(length)
        self.ma_type = str(ma_type)
        self.enabled = bool(enabled)
        if self.length < 1:
            raise ValueError("MA length must be >= 1")
        if self.ma_type not in SUPPORTED_MA_TYPES:
            raise ValueError(f"Unsupported MA type: {self.ma_type}")

        self._window: deque[float] = deque(maxlen=self.length)
        self._line: float | None = None
        self._prev_line: float | None = None

    @property
    def warmup_bars_required(self) -> int:
        return self.length if self.enabled else 0

    @property
    def line(self) -> float | None:
        return self._line

    @property
    def prev_line(self) -> float | None:
        return self._prev_line

    @property
    def warmup_ready(self) -> bool:
        return (not self.enabled) or self._line is not None

    def update(self, price: float) -> float | None:
        if not self.enabled:
            self._prev_line = self._line
            self._line = None
            return None

        self._window.append(float(price))
        self._prev_line = self._line

        if self.ma_type == MA_TYPE_SMA:
            self._line = self._calc_sma()
        elif self.ma_type == MA_TYPE_EMA:
            self._line = self._calc_ema(price)
        elif self.ma_type == MA_TYPE_RMA:
            self._line = self._calc_rma(price)
        else:
            self._line = self._calc_wma()
        return self._line

    def _calc_sma(self) -> float | None:
        if len(self._window) < self.length:
            return None
        return sum(self._window) / float(self.length)

    def _calc_ema(self, price: float) -> float | None:
        if self._line is None:
            if len(self._window) < self.length:
                return None
            return sum(self._window) / float(self.length)
        alpha = 2.0 / float(self.length + 1)
        return (alpha * float(price)) + ((1.0 - alpha) * self._line)

    def _calc_rma(self, price: float) -> float | None:
        if self._line is None:
            if len(self._window) < self.length:
                return None
            return sum(self._window) / float(self.length)
        return ((self._line * float(self.length - 1)) + float(price)) / float(self.length)

    def _calc_wma(self) -> float | None:
        if len(self._window) < self.length:
            return None
        weights = list(range(1, self.length + 1))
        weighted_sum = sum(weight * value for weight, value in zip(weights, self._window))
        return weighted_sum / float(sum(weights))

class McGinleyTracker:
    def __init__(self, *, length: int, enabled: bool = True) -> None:
        from collections import deque
        self.length = int(length)
        self.enabled = bool(enabled)
        if self.length < 1:
            raise ValueError("McGinley length must be >= 1")
        self._window: deque[float] = deque(maxlen=self.length)
        self._line: float | None = None

    @property
    def line(self) -> float | None:
        return self._line

    @property
    def warmup_bars_required(self) -> int:
        return self.length if self.enabled else 0

    @property
    def warmup_ready(self) -> bool:
        return (not self.enabled) or self._line is not None

    def update(self, price: float) -> float | None:
        if not self.enabled:
            return None

        p = float(price)
        self._window.append(p)

        if self._line is None:
            if len(self._window) < self.length:
                return None
            self._line = sum(self._window) / float(self.length)
            return self._line

        prev = self._line
        if prev <= 0.0:
            self._line = p
            return self._line

        ratio = p / prev
        denom = float(self.length) * (ratio ** 4)
        if denom == 0.0:
            return self._line

        self._line = prev + (p - prev) / denom
        return self._line


class VolumeSmaTracker:
    def __init__(self, *, length: int, enabled: bool = True) -> None:
        from collections import deque
        self.length = int(length)
        self.enabled = bool(enabled)
        self._window: deque[float] = deque(maxlen=self.length)

    @property
    def sma(self) -> float | None:
        if not self.enabled or len(self._window) < self.length:
            return None
        return sum(self._window) / float(self.length)

    def update(self, volume: float) -> float | None:
        if not self.enabled:
            return None
        self._window.append(float(volume))
        return self.sma


class AdxTracker:
    def __init__(self, *, length: int, enabled: bool = True) -> None:
        self.length = int(length)
        self.enabled = bool(enabled)
        self._prev_high: float | None = None
        self._prev_low: float | None = None
        self._prev_close: float | None = None
        self._smooth_atr: float | None = None
        self._smooth_pdm: float | None = None
        self._smooth_ndm: float | None = None
        self._smooth_dx: float | None = None
        self._adx: float | None = None
        self._seed_count: int = 0
        self._seed_atr: float = 0.0
        self._seed_pdm: float = 0.0
        self._seed_ndm: float = 0.0
        self._dx_seed_count: int = 0
        self._dx_seed_sum: float = 0.0

    @property
    def adx(self) -> float | None:
        return self._adx if self.enabled else None

    def update(self, high: float, low: float, close: float) -> float | None:
        if not self.enabled:
            return None
        h, l, c = float(high), float(low), float(close)
        ph, pl, pc = self._prev_high, self._prev_low, self._prev_close
        if ph is None:
            self._prev_high, self._prev_low, self._prev_close = h, l, c
            return None
        tr = max(h - l, abs(h - pc), abs(l - pc))
        up_move = h - ph
        down_move = pl - l
        pdm = up_move if (up_move > down_move and up_move > 0) else 0.0
        ndm = down_move if (down_move > up_move and down_move > 0) else 0.0
        self._prev_high, self._prev_low, self._prev_close = h, l, c
        if self._smooth_atr is None:
            self._seed_count += 1
            self._seed_atr += tr
            self._seed_pdm += pdm
            self._seed_ndm += ndm
            if self._seed_count >= self.length:
                self._smooth_atr = self._seed_atr
                self._smooth_pdm = self._seed_pdm
                self._smooth_ndm = self._seed_ndm
            else:
                return None
        else:
            self._smooth_atr = self._smooth_atr - self._smooth_atr / self.length + tr
            self._smooth_pdm = self._smooth_pdm - self._smooth_pdm / self.length + pdm
            self._smooth_ndm = self._smooth_ndm - self._smooth_ndm / self.length + ndm
        if self._smooth_atr <= 0:
            return None
        pdi = 100.0 * self._smooth_pdm / self._smooth_atr
        ndi = 100.0 * self._smooth_ndm / self._smooth_atr
        denom = pdi + ndi
        dx = 100.0 * abs(pdi - ndi) / denom if denom > 0 else 0.0
        if self._smooth_dx is None:
            self._dx_seed_count += 1
            self._dx_seed_sum += dx
            if self._dx_seed_count >= self.length:
                self._smooth_dx = self._dx_seed_sum / self.length
                self._adx = self._smooth_dx
            return self._adx
        else:
            self._smooth_dx = (self._smooth_dx * (self.length - 1) + dx) / self.length
            self._adx = self._smooth_dx
            return self._adx


class ChoppinessTracker:
    def __init__(self, *, length: int, enabled: bool = True) -> None:
        import math as _math
        from collections import deque
        self.length = int(length)
        self.enabled = bool(enabled)
        self._highs: deque[float] = deque(maxlen=self.length)
        self._lows: deque[float] = deque(maxlen=self.length)
        self._atr1s: deque[float] = deque(maxlen=self.length)
        self._prev_close: float | None = None
        self._chop: float | None = None
        self._log_n: float = _math.log10(float(self.length)) if self.length > 1 else 1.0

    @property
    def chop(self) -> float | None:
        return self._chop if self.enabled else None

    def update(self, high: float, low: float, close: float) -> float | None:
        import math as _math
        if not self.enabled:
            return None
        h, l, c = float(high), float(low), float(close)
        pc = self._prev_close
        if pc is None:
            self._prev_close = c
            self._highs.append(h)
            self._lows.append(l)
            self._atr1s.append(h - l)
            return None
        tr1 = max(h - l, abs(h - pc), abs(l - pc))
        self._highs.append(h)
        self._lows.append(l)
        self._atr1s.append(tr1)
        self._prev_close = c
        if len(self._highs) < self.length:
            return None
        highest = max(self._highs)
        lowest = min(self._lows)
        atr_sum = sum(self._atr1s)
        hl_range = highest - lowest
        if hl_range <= 0 or atr_sum <= 0 or self._log_n <= 0:
            self._chop = None
            return None
        self._chop = 100.0 * _math.log10(atr_sum / hl_range) / self._log_n
        return self._chop


class AtrVolFloorTracker:
    def __init__(self, *, fast_length: int, baseline_length: int, enabled: bool = True) -> None:
        from collections import deque
        self.fast_length = int(fast_length)
        self.baseline_length = int(baseline_length)
        self.enabled = bool(enabled)
        self._prev_close: float | None = None
        self._fast_atr: float | None = None
        self._fast_seed_count: int = 0
        self._fast_seed_sum: float = 0.0
        self._baseline_window: deque[float] = deque(maxlen=self.baseline_length)

    @property
    def fast_atr(self) -> float | None:
        return self._fast_atr if self.enabled else None

    @property
    def baseline_atr(self) -> float | None:
        if not self.enabled or len(self._baseline_window) < self.baseline_length:
            return None
        return sum(self._baseline_window) / float(self.baseline_length)

    def update(self, high: float, low: float, close: float) -> tuple[float | None, float | None]:
        if not self.enabled:
            return None, None
        h, l, c = float(high), float(low), float(close)
        pc = self._prev_close
        if pc is None:
            self._prev_close = c
            return None, None
        tr = max(h - l, abs(h - pc), abs(l - pc))
        self._prev_close = c
        if self._fast_atr is None:
            self._fast_seed_count += 1
            self._fast_seed_sum += tr
            if self._fast_seed_count >= self.fast_length:
                self._fast_atr = self._fast_seed_sum / self.fast_length
        else:
            self._fast_atr = (self._fast_atr * (self.fast_length - 1) + tr) / self.fast_length
        if self._fast_atr is not None:
            self._baseline_window.append(self._fast_atr)
        return self._fast_atr, self.baseline_atr


class MacdTracker:
    def __init__(self, *, fast_len: int, slow_len: int, sig_len: int, enabled: bool = True) -> None:
        self.fast_len = int(fast_len)
        self.slow_len = int(slow_len)
        self.sig_len = int(sig_len)
        self.enabled = bool(enabled)
        self._fast_ema = MovingAverageTracker(length=self.fast_len, ma_type="EMA", enabled=self.enabled)
        self._slow_ema = MovingAverageTracker(length=self.slow_len, ma_type="EMA", enabled=self.enabled)
        self._sig_ema = MovingAverageTracker(length=self.sig_len, ma_type="EMA", enabled=self.enabled)
        self._macd_line: float | None = None
        self._macd_signal: float | None = None
        self._macd_hist: float | None = None
        self._prev_macd_hist: float | None = None

    @property
    def macd_line(self) -> float | None:
        return self._macd_line

    @property
    def macd_signal(self) -> float | None:
        return self._macd_signal

    @property
    def macd_hist(self) -> float | None:
        return self._macd_hist

    @property
    def prev_macd_hist(self) -> float | None:
        return self._prev_macd_hist

    def update(self, price: float) -> tuple[float | None, float | None, float | None, float | None]:
        if not self.enabled:
            return None, None, None, None
        
        self._prev_macd_hist = self._macd_hist
        p = float(price)
        f_val = self._fast_ema.update(p)
        s_val = self._slow_ema.update(p)
        
        if f_val is not None and s_val is not None:
            self._macd_line = f_val - s_val
            sig_val = self._sig_ema.update(self._macd_line)
            if sig_val is not None:
                self._macd_signal = sig_val
                self._macd_hist = self._macd_line - self._macd_signal
            else:
                self._macd_signal = None
                self._macd_hist = None
        else:
            self._macd_line = None
            self._macd_signal = None
            self._macd_hist = None
            
        return self._macd_line, self._macd_signal, self._macd_hist, self._prev_macd_hist


class HtfMovingAverageTracker:
    """Stateful MA computed over prior-closed HTF close values.

    The tracker is fed the prior-closed HTF close for **every LTF bar** via
    ``update()``, mirroring Pine's behaviour where built-in series functions
    such as ``ta.ema()`` advance their internal state on every bar regardless
    of whether they are inside a conditional block.  Repeated values (i.e.
    the same 4h close appearing on all four 1h bars within that 4h period)
    are passed through unchanged to the inner ``MovingAverageTracker``; no
    de-duplication is applied.  This means the tracker warms up in exactly
    ``length`` LTF bars, matching Pine's warmup timing.
    """

    def __init__(self, *, length: int, ma_type: str, enabled: bool = True) -> None:
        self.length = int(length)
        self.ma_type = str(ma_type)
        self.enabled = bool(enabled)
        self._inner = MovingAverageTracker(length=length, ma_type=ma_type, enabled=enabled)

    def update(self, htf_close: float | None) -> None:
        """Advance tracker with the prior-closed HTF close for this LTF bar.

        Parameters
        ----------
        htf_close :
            Prior-closed HTF close, or ``None`` during the warmup period
            (no HTF bar has closed yet).
        """
        if not self.enabled or htf_close is None:
            return
        self._inner.update(htf_close)

    @property
    def line(self) -> float | None:
        """Current MA value, or ``None`` while warming up."""
        return self._inner.line

    @property
    def ready(self) -> bool:
        """``True`` once the warmup period is complete."""
        return self._inner.warmup_ready

