"""
Precision Utilities for MTC Backtest System.

Provides deterministic rounding and float comparison functions
to ensure parity with TradingView Pine Script calculations.

All functions are pure and have no side effects.
"""

from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

PRICE_PRECISION = 8  # Decimal places for prices
QTY_PRECISION = 4    # Decimal places for quantities
EPSILON = 1e-10      # Tolerance for float comparison

# Default tick sizes by asset class
DEFAULT_TICK_SIZES = {
    "crypto": 0.01,
    "forex": 0.0001,
    "stock": 0.01,
    "futures": 0.25,
}


# ═══════════════════════════════════════════════════════════════════════════════
# ROUNDING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def round_price(value: float, precision: int = PRICE_PRECISION) -> float:
    """
    Round a price value to specified precision.
    
    Args:
        value: Price value to round
        precision: Decimal places (default: 8)
        
    Returns:
        Rounded price value
        
    Example:
        >>> round_price(42531.123456789)
        42531.12345679
    """
    if value is None:
        return 0.0
    return round(float(value), precision)


def round_qty(value: float, precision: int = QTY_PRECISION) -> float:
    """
    Round a quantity value to specified precision.
    
    Args:
        value: Quantity value to round
        precision: Decimal places (default: 4)
        
    Returns:
        Rounded quantity value
        
    Example:
        >>> round_qty(0.123456)
        0.1235
    """
    if value is None:
        return 0.0
    return round(float(value), precision)


def round_to_tick(value: float, tick_size: float) -> float:
    """
    Round a value to the nearest tick size.
    
    Args:
        value: Value to round
        tick_size: Minimum price increment
        
    Returns:
        Value rounded to nearest tick
        
    Example:
        >>> round_to_tick(42531.123, 0.01)
        42531.12
    """
    if tick_size <= 0:
        return round_price(value)
    return round(value / tick_size) * tick_size


# ═══════════════════════════════════════════════════════════════════════════════
# FLOAT COMPARISON FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def float_eq(a: float, b: float, eps: float = EPSILON) -> bool:
    """
    Check if two floats are approximately equal.
    
    Args:
        a: First value
        b: Second value
        eps: Tolerance (default: 1e-10)
        
    Returns:
        True if |a - b| < eps
        
    Example:
        >>> float_eq(1.0000000001, 1.0)
        True
    """
    if a is None or b is None:
        return a is None and b is None
    return abs(float(a) - float(b)) < eps


def float_lt(a: float, b: float, eps: float = EPSILON) -> bool:
    """
    Check if a is less than b (with tolerance).
    
    Returns True if a < b and they are not approximately equal.
    
    Args:
        a: First value
        b: Second value
        eps: Tolerance for equality check
        
    Returns:
        True if a < b (and not approximately equal)
    """
    if a is None or b is None:
        return False
    return float(a) < float(b) - eps


def float_lte(a: float, b: float, eps: float = EPSILON) -> bool:
    """
    Check if a is less than or equal to b (with tolerance).
    
    Returns True if a < b OR a ≈ b.
    
    Args:
        a: First value
        b: Second value
        eps: Tolerance for equality check
        
    Returns:
        True if a <= b (approximately)
    """
    if a is None or b is None:
        return False
    return float(a) < float(b) + eps


def float_gt(a: float, b: float, eps: float = EPSILON) -> bool:
    """
    Check if a is greater than b (with tolerance).
    
    Returns True if a > b and they are not approximately equal.
    
    Args:
        a: First value
        b: Second value
        eps: Tolerance for equality check
        
    Returns:
        True if a > b (and not approximately equal)
    """
    if a is None or b is None:
        return False
    return float(a) > float(b) + eps


def float_gte(a: float, b: float, eps: float = EPSILON) -> bool:
    """
    Check if a is greater than or equal to b (with tolerance).
    
    Returns True if a > b OR a ≈ b.
    
    Args:
        a: First value
        b: Second value
        eps: Tolerance for equality check
        
    Returns:
        True if a >= b (approximately)
    """
    if a is None or b is None:
        return False
    return float(a) > float(b) - eps


# ═══════════════════════════════════════════════════════════════════════════════
# TICK SIZE UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def get_tick_size(
    symbol: str,
    exchange: Optional[object] = None,
    fallback: float = 0.01
) -> float:
    """
    Get tick size for a symbol.
    
    Priority:
    1. Exchange metadata (if exchange provided and symbol found)
    2. Fallback value
    
    Args:
        symbol: Trading symbol (e.g., "BTCUSDT")
        exchange: Optional ccxt exchange instance
        fallback: Fallback tick size if not found
        
    Returns:
        Tick size (minimum price increment)
        
    Example:
        >>> get_tick_size("BTCUSDT", fallback=0.01)
        0.01
    """
    if exchange is not None:
        try:
            # Try to get from exchange markets
            markets = getattr(exchange, 'markets', None)
            if markets:
                # Convert symbol format
                for market_id, market in markets.items():
                    if symbol.upper() in market_id.upper():
                        precision = market.get('precision', {})
                        price_precision = precision.get('price')
                        if price_precision is not None:
                            # Convert precision to tick size
                            if isinstance(price_precision, int):
                                return 10 ** (-price_precision)
                            return price_precision
        except Exception:
            pass
    
    return fallback


def get_qty_precision(
    symbol: str,
    exchange: Optional[object] = None,
    fallback: int = QTY_PRECISION
) -> int:
    """
    Get quantity precision (decimal places) for a symbol.
    
    Args:
        symbol: Trading symbol
        exchange: Optional ccxt exchange instance
        fallback: Fallback precision
        
    Returns:
        Number of decimal places for quantity
    """
    if exchange is not None:
        try:
            markets = getattr(exchange, 'markets', None)
            if markets:
                for market_id, market in markets.items():
                    if symbol.upper() in market_id.upper():
                        precision = market.get('precision', {})
                        amount_precision = precision.get('amount')
                        if amount_precision is not None:
                            if isinstance(amount_precision, int):
                                return amount_precision
        except Exception:
            pass
    
    return fallback


# ═══════════════════════════════════════════════════════════════════════════════
# NOTIONAL CALCULATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_notional(price: float, quantity: float) -> float:
    """
    Calculate notional value of a position.
    
    Args:
        price: Entry/exit price
        quantity: Position quantity
        
    Returns:
        Notional value (price * quantity)
    """
    return round_price(price * quantity)


def calculate_pnl(
    entry_price: float,
    exit_price: float,
    quantity: float,
    is_long: bool
) -> float:
    """
    Calculate PnL for a trade.
    
    Args:
        entry_price: Entry price
        exit_price: Exit price
        quantity: Position quantity
        is_long: True for long, False for short
        
    Returns:
        PnL amount
    """
    if is_long:
        pnl = (exit_price - entry_price) * quantity
    else:
        pnl = (entry_price - exit_price) * quantity
    
    return round_price(pnl)


def calculate_pnl_percent(
    entry_price: float,
    exit_price: float,
    is_long: bool
) -> float:
    """
    Calculate PnL percentage.
    
    Args:
        entry_price: Entry price
        exit_price: Exit price
        is_long: True for long, False for short
        
    Returns:
        PnL percentage
    """
    if entry_price == 0:
        return 0.0
    
    if is_long:
        pnl_pct = ((exit_price - entry_price) / entry_price) * 100
    else:
        pnl_pct = ((entry_price - exit_price) / entry_price) * 100
    
    return round(pnl_pct, 4)
