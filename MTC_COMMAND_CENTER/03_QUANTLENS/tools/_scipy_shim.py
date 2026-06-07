"""
Pure-Python scipy.stats.norm shim — avoids OpenBLAS hang (D009).

MEGA walk-forward only needs norm.ppf() and norm.cdf().
This module intercepts 'from scipy import stats' and provides
pure-Python replacements using math.erf / math.erfinv.

Import this BEFORE any module that imports scipy (e.g., mega_walk_forward.py).
"""
from __future__ import annotations
import math
import sys
import types


def _norm_cdf(x: float) -> float:
    """Standard normal CDF: 0.5 * (1 + erf(x / sqrt(2)))"""
    return 0.5 * (1.0 + math.erf(x / 1.4142135623730951))


def _norm_ppf(q: float) -> float:
    """Standard normal inverse CDF (quantile).
    Acklam's algorithm — error < 1.15e-9. No scipy/math.erfinv needed."""
    q = float(q)
    if q <= 0.0:
        return float('-inf')
    if q >= 1.0:
        return float('inf')

    # Acklam coefficients
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    dco = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
           3.754408661907416e+00]

    p_low = 0.02425
    p_high = 1.0 - p_low

    if q < p_low:
        r = math.sqrt(-2.0 * math.log(q))
        num = ((((c[0]*r + c[1])*r + c[2])*r + c[3])*r + c[4])*r + c[5]
        den = (((dco[0]*r + dco[1])*r + dco[2])*r + dco[3])*r + 1.0
        return num / den
    elif q > p_high:
        r = math.sqrt(-2.0 * math.log(1.0 - q))
        num = ((((c[0]*r + c[1])*r + c[2])*r + c[3])*r + c[4])*r + c[5]
        den = (((dco[0]*r + dco[1])*r + dco[2])*r + dco[3])*r + 1.0
        return -num / den
    else:
        r = q - 0.5
        s = r * r
        num = ((((a[0]*s + a[1])*s + a[2])*s + a[3])*s + a[4])*s + a[5]
        den = ((((b[0]*s + b[1])*s + b[2])*s + b[3])*s + b[4])*s + 1.0
        return num * r / den


class _FakeNorm:
    """Minimal norm distribution object matching scipy.stats.norm interface."""
    @staticmethod
    def cdf(x):
        return _norm_cdf(x)

    @staticmethod
    def ppf(q):
        return _norm_ppf(q)


_SCIPY_STATS_INTERCEPTED = False


def install_shim():
    """Call early to prevent scipy.stats import."""
    global _SCIPY_STATS_INTERCEPTED
    if _SCIPY_STATS_INTERCEPTED:
        return

    # Create a fake scipy.stats namespace with just norm
    _fake_stats = types.ModuleType('scipy.stats')
    _fake_stats.norm = _FakeNorm()
    _fake_stats.__file__ = __file__
    _fake_stats.__name__ = 'scipy.stats'
    sys.modules['scipy.stats'] = _fake_stats

    # Also patch scipy.stats._continuous_distns which norm normally lives in
    _fake_cont = types.ModuleType('scipy.stats._continuous_distns')
    _fake_cont.norm = _FakeNorm()
    _fake_cont.__file__ = __file__
    sys.modules['scipy.stats._continuous_distns'] = _fake_cont

    # Block submodules that trigger BLAS
    _SCIPY_STATS_INTERCEPTED = True


def verify():
    """Quick self-test — no scipy needed."""
    cdf_val = _norm_cdf(0.0)
    ppf_val = _norm_ppf(0.975)
    assert abs(cdf_val - 0.5) < 0.001, f"cdf(0)={cdf_val}"
    assert abs(ppf_val - 1.96) < 0.01, f"ppf(0.975)={ppf_val}"
    return True


# Auto-install on import
install_shim()
