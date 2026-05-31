"""
Legacy fill helpers for baseline unit checks.

IMPORTANT:
- The authoritative live fill/order contract is implemented in
  `src/engine/mtc_runner.py`.
- This module is retained only for helper tests and historical reference.
  Do not use `FillsEngine` for parity runs.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Literal, List
from enum import Enum
import warnings

from ..common.precision import float_lte, float_gte, round_price


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# ENUMS AND TYPES
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class FillType(str, Enum):
    """Type of fill event."""
    ENTRY = "entry"
    EXIT_SL = "exit_sl"
    EXIT_TP1 = "exit_tp1"
    EXIT_TP2 = "exit_tp2"
    EXIT_TRAILING = "exit_trailing"
    EXIT_OPPOSITE = "exit_opposite"
    EXIT_FILTER = "exit_filter"
    PARTIAL_TP1 = "partial_tp1"


class SameBarConflictPolicy(str, Enum):
    """Policy for handling same-bar SL/TP conflicts."""
    WORST_CASE = "worst-case"   # SL fills first (safer)
    BEST_CASE = "best-case"     # TP fills first (optimistic)
    SL_PRIORITY = "sl-priority" # SL always first
    TP_PRIORITY = "tp-priority" # TP always first


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# DATA CLASSES
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

@dataclass
class BarData:
    """OHLCV bar data."""
    bar_index: int
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


@dataclass
class FillResult:
    """Result of a fill (entry or exit)."""
    fill_type: FillType
    fill_price: float
    fill_qty: float
    bar_index: int
    timestamp: datetime
    reason: str = ""
    partial: bool = False  # True for partial exits (TP1)
    remaining_qty: float = 0.0


@dataclass
class PositionState:
    """Current position state for fills engine."""
    is_long: bool
    quantity: float
    avg_entry_price: float
    sl_price: Optional[float] = None
    tp1_price: Optional[float] = None
    tp2_price: Optional[float] = None
    trailing_stop: Optional[float] = None
    be_triggered: bool = False
    tp1_hit: bool = False
    highest_price: float = 0.0
    lowest_price: float = float('inf')


@dataclass 
class FillPolicy:
    """Configuration for fill behavior."""
    same_bar_conflict: SameBarConflictPolicy = SameBarConflictPolicy.WORST_CASE
    exit_on_opposite_signal: bool = True
    allow_pyramiding: bool = False
    max_pyramid_entries: int = 2


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# OHLC TOUCH DETECTION
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def check_sl_hit(bar: BarData, position: PositionState) -> bool:
    """
    Check if Stop Loss was hit on this bar.
    
    Long SL: low <= sl_price
    Short SL: high >= sl_price
    
    Args:
        bar: Current bar data
        position: Current position state
        
    Returns:
        True if SL was hit
    """
    if position.sl_price is None:
        return False
    
    if position.is_long:
        # Long SL hit when price drops to or below SL
        return float_lte(bar.low, position.sl_price)
    else:
        # Short SL hit when price rises to or above SL
        return float_gte(bar.high, position.sl_price)


def check_tp_hit(bar: BarData, position: PositionState, tp_price: float) -> bool:
    """
    Check if Take Profit was hit on this bar.
    
    Long TP: high >= tp_price
    Short TP: low <= tp_price
    
    Args:
        bar: Current bar data
        position: Current position state
        tp_price: Take profit price to check
        
    Returns:
        True if TP was hit
    """
    if tp_price is None:
        return False
    
    if position.is_long:
        # Long TP hit when price rises to or above TP
        return float_gte(bar.high, tp_price)
    else:
        # Short TP hit when price falls to or below TP
        return float_lte(bar.low, tp_price)


def check_trailing_stop_hit(bar: BarData, position: PositionState) -> bool:
    """
    Check if trailing stop was hit.
    
    Same logic as SL hit detection.
    """
    if position.trailing_stop is None:
        return False
    
    if position.is_long:
        return float_lte(bar.low, position.trailing_stop)
    else:
        return float_gte(bar.high, position.trailing_stop)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SAME-BAR CONFLICT RESOLUTION
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def resolve_same_bar_conflict(
    sl_hit: bool,
    tp_hit: bool,
    position: PositionState,
    policy: SameBarConflictPolicy,
) -> Literal["sl", "tp", "none"]:
    """
    Resolve conflict when both SL and TP are hit on the same bar.
    
    Args:
        sl_hit: True if SL was touched
        tp_hit: True if TP was touched
        position: Current position state
        policy: Conflict resolution policy
        
    Returns:
        "sl" to fill SL first, "tp" to fill TP first, "none" if no conflict
    """
    if not sl_hit and not tp_hit:
        return "none"
    
    if sl_hit and not tp_hit:
        return "sl"
    
    if tp_hit and not sl_hit:
        return "tp"
    
    # Both hit - apply policy
    if policy == SameBarConflictPolicy.WORST_CASE:
        # Worst case for trader = SL fills first (realizes loss)
        return "sl"
    
    elif policy == SameBarConflictPolicy.BEST_CASE:
        # Best case for trader = TP fills first (realizes profit)
        return "tp"
    
    elif policy == SameBarConflictPolicy.SL_PRIORITY:
        return "sl"
    
    elif policy == SameBarConflictPolicy.TP_PRIORITY:
        return "tp"
    
    return "sl"  # Default to worst-case


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# FILL PRICES
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def get_sl_fill_price(bar: BarData, position: PositionState) -> float:
    """
    Get fill price for stop loss.
    
    Uses the SL price directly (assumes market order fills at SL).
    In reality, may gap through but we use SL as fill price.
    """
    return position.sl_price


def get_tp_fill_price(bar: BarData, position: PositionState, tp_price: float) -> float:
    """
    Get fill price for take profit.
    
    Uses the TP price directly (limit order fills at TP).
    """
    return tp_price


def get_trailing_fill_price(bar: BarData, position: PositionState) -> float:
    """Get fill price for trailing stop."""
    return position.trailing_stop


def get_entry_fill_price(bar: BarData, use_next_open: bool = True) -> float:
    """
    Get fill price for entry.
    
    Args:
        bar: Current bar data
        use_next_open: If True, use close as proxy for next open
        
    Returns:
        Entry fill price
    """
    # TradingView typically fills at close (or next open in real trading)
    # For backtest, we use close of signal bar
    return bar.close


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# FILLS ENGINE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class FillsEngine:
    """
    Deterministic fills engine matching TradingView bar evaluation order.
    
    Usage:
        engine = FillsEngine(policy=FillPolicy())
        
        # Each bar:
        engine.update_state(bar, position)
        fills = engine.evaluate_bar(bar, position, long_signal, short_signal)
    """
    
    def __init__(self, policy: Optional[FillPolicy] = None):
        """
        Initialize fills engine.
        
        Args:
            policy: Fill policy configuration
        """
        warnings.warn("src.engine.fills.FillsEngine is legacy and not used by MTCRunner; use src.engine.mtc_runner as authoritative fill contract.", DeprecationWarning, stacklevel=2)
        self.policy = policy or FillPolicy()
        self._fills: List[FillResult] = []
    
    def update_trailing_stop(
        self,
        bar: BarData,
        position: PositionState,
        trail_distance: float,
        start_r: float,
        current_r: float,
    ) -> Optional[float]:
        """
        Update trailing stop based on price movement.
        
        Args:
            bar: Current bar data
            position: Position state
            trail_distance: Trail distance (in price units or R-multiples)
            start_r: R-multiple to start trailing
            current_r: Current unrealized R-multiple
            
        Returns:
            Updated trailing stop price, or None if not changed
        """
        if position is None or current_r < start_r:
            return None
        
        new_trail = None
        
        if position.is_long:
            # Update highest price
            if bar.high > position.highest_price:
                position.highest_price = bar.high
                new_trail = round_price(position.highest_price - trail_distance)
                
                # Only update if higher than current trailing stop
                if position.trailing_stop is None or new_trail > position.trailing_stop:
                    position.trailing_stop = new_trail
        else:
            # Short: update lowest price
            if bar.low < position.lowest_price:
                position.lowest_price = bar.low
                new_trail = round_price(position.lowest_price + trail_distance)
                
                # Only update if lower than current trailing stop
                if position.trailing_stop is None or new_trail < position.trailing_stop:
                    position.trailing_stop = new_trail
        
        return position.trailing_stop
    
    def update_break_even(
        self,
        position: PositionState,
        be_trigger_r: float,
        current_r: float,
        buffer_r: float = 0.0,
    ) -> bool:
        """
        Update break-even trigger.
        
        When current R exceeds BE trigger, move SL to entry + buffer.
        
        Args:
            position: Position state
            be_trigger_r: R-multiple to trigger BE
            current_r: Current unrealized R-multiple
            buffer_r: Buffer to add beyond breakeven
            
        Returns:
            True if BE was triggered this bar
        """
        if position is None or position.be_triggered:
            return False
        
        if current_r >= be_trigger_r:
            # Calculate BE price with buffer
            if position.sl_price is not None and position.avg_entry_price is not None:
                risk_per_unit = abs(position.avg_entry_price - position.sl_price)
                buffer_amount = risk_per_unit * buffer_r
                
                if position.is_long:
                    position.sl_price = round_price(position.avg_entry_price + buffer_amount)
                else:
                    position.sl_price = round_price(position.avg_entry_price - buffer_amount)
                
                position.be_triggered = True
                return True
        
        return False
    
    def evaluate_exits(
        self,
        bar: BarData,
        position: PositionState,
        long_signal: bool,
        short_signal: bool,
    ) -> List[FillResult]:
        """
        Evaluate all exit conditions for the bar.
        
        Order:
        1. Stop Loss
        2. Take Profit (TP1 partial, then TP2)
        3. Trailing Stop
        4. Opposite Signal
        
        Args:
            bar: Current bar data
            position: Position state
            long_signal: Current long signal
            short_signal: Current short signal
            
        Returns:
            List of fill results (may be empty, one, or multiple for partials)
        """
        if position is None or position.quantity <= 0:
            return []
        
        fills = []
        
        # Check SL
        sl_hit = check_sl_hit(bar, position)
        
        # Check TPs
        tp1_hit = False
        tp2_hit = False
        
        if not position.tp1_hit and position.tp1_price is not None:
            tp1_hit = check_tp_hit(bar, position, position.tp1_price)
        
        if position.tp1_hit and position.tp2_price is not None:
            tp2_hit = check_tp_hit(bar, position, position.tp2_price)
        
        # Check trailing
        trail_hit = check_trailing_stop_hit(bar, position)
        
        # Resolve same-bar conflicts
        if sl_hit and (tp1_hit or tp2_hit):
            tp_hit = tp1_hit or tp2_hit
            first_fill = resolve_same_bar_conflict(
                sl_hit, tp_hit, position, self.policy.same_bar_conflict
            )
            
            if first_fill == "sl":
                # SL fills, no TP
                fills.append(FillResult(
                    fill_type=FillType.EXIT_SL,
                    fill_price=get_sl_fill_price(bar, position),
                    fill_qty=position.quantity,
                    bar_index=bar.bar_index,
                    timestamp=bar.timestamp,
                    reason="Stop Loss",
                ))
                return fills
            else:
                # TP fills, no SL
                sl_hit = False
        
        # Process exits in order
        
        # 1. Stop Loss
        if sl_hit:
            fills.append(FillResult(
                fill_type=FillType.EXIT_SL,
                fill_price=get_sl_fill_price(bar, position),
                fill_qty=position.quantity,
                bar_index=bar.bar_index,
                timestamp=bar.timestamp,
                reason="Stop Loss",
            ))
            return fills  # Full exit, no further processing
        
        # 2. Trailing Stop (higher priority than TP)
        if trail_hit:
            fills.append(FillResult(
                fill_type=FillType.EXIT_TRAILING,
                fill_price=get_trailing_fill_price(bar, position),
                fill_qty=position.quantity,
                bar_index=bar.bar_index,
                timestamp=bar.timestamp,
                reason="Trailing Stop",
            ))
            return fills
        
        # 3. Take Profit 1 (partial)
        if tp1_hit and not position.tp1_hit:
            partial_qty = round_price(position.quantity * 0.5)  # 50% default
            fills.append(FillResult(
                fill_type=FillType.PARTIAL_TP1,
                fill_price=get_tp_fill_price(bar, position, position.tp1_price),
                fill_qty=partial_qty,
                bar_index=bar.bar_index,
                timestamp=bar.timestamp,
                reason="Take Profit 1",
                partial=True,
                remaining_qty=position.quantity - partial_qty,
            ))
            position.tp1_hit = True
            position.quantity -= partial_qty
        
        # 4. Take Profit 2 (full)
        if tp2_hit and position.tp1_hit:
            fills.append(FillResult(
                fill_type=FillType.EXIT_TP2,
                fill_price=get_tp_fill_price(bar, position, position.tp2_price),
                fill_qty=position.quantity,
                bar_index=bar.bar_index,
                timestamp=bar.timestamp,
                reason="Take Profit 2",
            ))
            return fills
        
        # 5. Opposite Signal Exit
        if self.policy.exit_on_opposite_signal:
            opposite_signal = (position.is_long and short_signal) or \
                             (not position.is_long and long_signal)
            
            if opposite_signal:
                fills.append(FillResult(
                    fill_type=FillType.EXIT_OPPOSITE,
                    fill_price=bar.close,
                    fill_qty=position.quantity,
                    bar_index=bar.bar_index,
                    timestamp=bar.timestamp,
                    reason="Opposite Signal",
                ))
                return fills
        
        return fills
    
    def evaluate_entry(
        self,
        bar: BarData,
        position: Optional[PositionState],
        long_signal: bool,
        short_signal: bool,
        quantity: float,
    ) -> Optional[FillResult]:
        """
        Evaluate entry signal.
        
        Args:
            bar: Current bar data
            position: Current position (None if flat)
            long_signal: Final filtered long signal
            short_signal: Final filtered short signal
            quantity: Entry quantity
            
        Returns:
            FillResult for entry, or None if no entry
        """
        # Check if we can enter
        if position is not None and position.quantity > 0:
            if not self.policy.allow_pyramiding:
                return None
        
        if not long_signal and not short_signal:
            return None
        
        # Determine direction
        is_long = long_signal and not short_signal
        
        return FillResult(
            fill_type=FillType.ENTRY,
            fill_price=get_entry_fill_price(bar),
            fill_qty=quantity,
            bar_index=bar.bar_index,
            timestamp=bar.timestamp,
            reason="Long Entry" if is_long else "Short Entry",
        )


