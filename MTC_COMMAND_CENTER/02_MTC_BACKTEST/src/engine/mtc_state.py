"""
MTC State Management Module.

Manages strategy state including positions, orders, and trade history.
Matches the state machine behavior of MASTER_TEMPLATE_CORE.pine.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Literal
from enum import Enum


QTY_PRECISION = 1e-6


def _truncate_toward_zero(value: float, step: float = QTY_PRECISION) -> float:
    """Match TV-style contract quantity truncation."""
    if step <= 0:
        return float(value)
    return int(float(value) / step) * step


class Direction(str, Enum):
    LONG = "long"
    SHORT = "short"
    FLAT = "flat"


class OrderType(str, Enum):
    ENTRY = "entry"
    EXIT = "exit"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"
    TRAILING_STOP = "trailing_stop"


class ExitReason(str, Enum):
    SL = "SL"
    TP = "TP"
    TP1 = "TP1"
    TP2 = "TP2"
    MARGIN_CALL = "MARGIN CALL"
    TRAIL = "TRAIL"
    OPP_SIGNAL = "OPP_SIGNAL"
    FILTER_BLOCK = "FILTER_BLOCK"
    TIME_STOP = "TIME_STOP"
    BE = "BE"
    MANUAL = "MANUAL"
    EVAL_START_FLATTEN = "EVAL_START_FLATTEN"


@dataclass
class Order:
    """Pending order."""
    
    order_id: int
    order_type: OrderType
    direction: Direction
    price: Optional[float] = None  # None for market orders
    quantity: float = 0.0
    created_bar: int = 0
    created_time: Optional[datetime] = None
    
    # For stop/limit orders
    trigger_price: Optional[float] = None
    
    # Status
    filled: bool = False
    cancelled: bool = False


@dataclass
class Position:
    """Open position."""
    
    direction: Direction
    entry_price: float
    entry_bar: int
    entry_time: Optional[datetime] = None
    quantity: float = 0.0
    
    # Stop Loss
    sl_price: Optional[float] = None
    sl_base_price: Optional[float] = None  # Original SL before adjustments
    
    # Take Profit
    tp_price: Optional[float] = None
    tp1_price: Optional[float] = None
    tp2_price: Optional[float] = None
    
    # Multi-TP tracking
    tp1_filled: bool = False
    tp1_fill_bar: Optional[int] = None
    initial_quantity: float = 0.0
    
    # Break-Even
    be_triggered: bool = False
    be_price: Optional[float] = None
    
    # Trailing Stop
    trailing_active: bool = False
    trailing_stop: Optional[float] = None
    highest_price: float = 0.0
    lowest_price: float = float('inf')
    
    # Risk metrics
    r_distance: float = 0.0  # Entry to SL distance (1R)
    
    def is_long(self) -> bool:
        return self.direction == Direction.LONG
    
    def is_short(self) -> bool:
        return self.direction == Direction.SHORT
    
    def unrealized_pnl(self, current_price: float) -> float:
        """Calculate unrealized PnL."""
        if self.direction == Direction.LONG:
            return (current_price - self.entry_price) * self.quantity
        else:
            return (self.entry_price - current_price) * self.quantity
    
    def unrealized_pnl_r(self, current_price: float) -> float:
        """Calculate unrealized PnL in R-multiples."""
        if self.r_distance == 0:
            return 0.0
        pnl = self.unrealized_pnl(current_price)
        return pnl / (self.r_distance * self.quantity)
    
    def update_extremes(self, high: float, low: float):
        """Update highest/lowest prices for trailing."""
        self.highest_price = max(self.highest_price, high)
        self.lowest_price = min(self.lowest_price, low)


@dataclass
class Trade:
    """Completed trade record."""
    
    trade_id: int
    direction: Direction
    
    # Entry
    entry_price: float
    entry_bar: int
    entry_time: Optional[datetime] = None
    
    # Exit
    exit_price: float = 0.0
    exit_bar: int = 0
    exit_time: Optional[datetime] = None
    exit_reason: ExitReason = ExitReason.MANUAL
    
    # Size
    quantity: float = 0.0
    
    # PnL
    pnl: float = 0.0
    pnl_pct: float = 0.0
    pnl_r: float = 0.0  # PnL in R-multiples
    
    # Prices
    sl_price: Optional[float] = None
    tp_price: Optional[float] = None
    
    # Extremes
    max_favorable_excursion: float = 0.0  # Best unrealized profit
    max_adverse_excursion: float = 0.0    # Worst unrealized loss
    
    @property
    def bars_held(self) -> int:
        return self.exit_bar - self.entry_bar
    
    @property
    def is_winner(self) -> bool:
        return self.pnl > 0


@dataclass
class DailyStats:
    """Daily trading statistics for guards."""
    
    date: datetime
    trades_count: int = 0
    pnl: float = 0.0
    starting_equity: float = 0.0
    
    def loss_percent(self, current_equity: float) -> float:
        """Calculate daily loss percentage."""
        if self.starting_equity == 0:
            return 0.0
        return ((self.starting_equity - current_equity) / self.starting_equity) * 100


@dataclass
class MTCState:
    """
    Complete strategy state.
    
    Tracks all runtime state for the MTC backtest engine.
    """
    
    # Position
    position: Optional[Position] = None
    
    # Trade history
    trades: List[Trade] = field(default_factory=list)
    next_trade_id: int = 1
    entry_events: int = 0
    
    # Current bar
    bar_index: int = 0
    current_time: Optional[datetime] = None
    
    # Equity
    initial_capital: float = 10000.0
    balance: float = 10000.0  # Realized capital (closed trades only)
    equity: float = 10000.0
    equity_curve: List[float] = field(default_factory=list)
    peak_equity: float = 10000.0
    
    # Drawdown
    drawdown: float = 0.0
    max_drawdown: float = 0.0
    drawdown_curve: List[float] = field(default_factory=list)
    
    # Daily tracking
    daily_stats: Optional[DailyStats] = None
    last_trade_bar: int = -999
    
    # Consecutive loss tracking
    consecutive_losses: int = 0
    last_entry_direction: Optional[Direction] = None
    last_signal_direction: Optional[Direction] = None
    time_stop_cooldown_until_bar: int = -1
    
    # Warmup
    warmup_complete: bool = False
    
    # Signals (for parity export)
    signal_history: List[dict] = field(default_factory=list)
    
    @property
    def in_position(self) -> bool:
        return self.position is not None
    
    @property
    def is_long(self) -> bool:
        return self.position is not None and self.position.direction == Direction.LONG
    
    @property
    def is_short(self) -> bool:
        return self.position is not None and self.position.direction == Direction.SHORT
    
    @property
    def position_size(self) -> float:
        return self.position.quantity if self.position else 0.0
    
    def reset(self):
        """Reset state to initial values."""
        self.position = None
        self.trades = []
        self.next_trade_id = 1
        self.entry_events = 0
        self.bar_index = 0
        self.equity = self.initial_capital
        self.balance = self.initial_capital
        self.equity_curve = []
        self.peak_equity = self.initial_capital
        self.drawdown = 0.0
        self.max_drawdown = 0.0
        self.drawdown_curve = []
        self.daily_stats = None
        self.last_trade_bar = -999
        self.consecutive_losses = 0
        self.last_entry_direction = None
        self.last_signal_direction = None
        self.time_stop_cooldown_until_bar = -1
        
        # Warmup
        self.warmup_complete = False
        self.signal_history = []
    
    def update_equity(self, new_equity: float):
        """Update equity and drawdown tracking."""
        self.equity = new_equity
        self.equity_curve.append(new_equity)
        
        # Update peak
        if new_equity > self.peak_equity:
            self.peak_equity = new_equity
        
        # Calculate drawdown
        if self.peak_equity > 0:
            self.drawdown = (self.peak_equity - new_equity) / self.peak_equity * 100
        else:
            self.drawdown = 0.0
        
        self.drawdown_curve.append(self.drawdown)
        
        # Update max drawdown
        if self.drawdown > self.max_drawdown:
            self.max_drawdown = self.drawdown
    
    def open_position(
        self,
        direction: Direction,
        entry_price: float,
        quantity: float,
        sl_price: Optional[float] = None,
        tp_price: Optional[float] = None,
        tp1_price: Optional[float] = None,
        tp2_price: Optional[float] = None,
    ) -> Position:
        """Open a new position."""
        quantity = _truncate_toward_zero(quantity)

        # Calculate R distance
        r_distance = 0.0
        if sl_price is not None:
            if direction == Direction.LONG:
                r_distance = entry_price - sl_price
            else:
                r_distance = sl_price - entry_price
        
        self.position = Position(
            direction=direction,
            entry_price=entry_price,
            entry_bar=self.bar_index,
            entry_time=self.current_time,
            quantity=quantity,
            initial_quantity=quantity,
            sl_price=sl_price,
            sl_base_price=sl_price,
            tp_price=tp_price,
            tp1_price=tp1_price,
            tp2_price=tp2_price,
            highest_price=entry_price,
            lowest_price=entry_price,
            r_distance=r_distance,
        )
        
        self.last_entry_direction = direction
        self.last_trade_bar = self.bar_index
        self.entry_events += 1
        
        return self.position
    
    def close_position(
        self,
        exit_price: float,
        exit_reason: ExitReason,
        quantity: Optional[float] = None,
        commission_pct: float = 0.0
    ) -> Optional[Trade]:
        """
        Close position (fully or partially).
        
        Args:
            exit_price: Exit price
            exit_reason: Reason for exit
            quantity: Quantity to close (None = full position)
            commission_pct: Commission percentage
            
        Returns:
            Trade record for the closed portion
        """
        if not self.position:
            return None
        
        pos = self.position
        close_qty = quantity if quantity is not None else pos.quantity
        close_qty = min(close_qty, pos.quantity)
        close_qty = _truncate_toward_zero(close_qty)
        if close_qty <= 0:
            return None
        
        # Calculate PnL
        if pos.direction == Direction.LONG:
            gross_pnl = (exit_price - pos.entry_price) * close_qty
        else:
            gross_pnl = (pos.entry_price - exit_price) * close_qty
        
        # Apply commission
        entry_commission = pos.entry_price * close_qty * commission_pct / 100
        exit_commission = exit_price * close_qty * commission_pct / 100
        net_pnl = gross_pnl - entry_commission - exit_commission
        
        # PnL percentage
        pnl_pct = (net_pnl / (pos.entry_price * close_qty)) * 100
        
        # PnL in R-multiples
        pnl_r = 0.0
        if pos.r_distance > 0:
            pnl_r = net_pnl / (pos.r_distance * close_qty)
        
        # Create trade record
        trade = Trade(
            trade_id=self.next_trade_id,
            direction=pos.direction,
            entry_price=pos.entry_price,
            entry_bar=pos.entry_bar,
            entry_time=pos.entry_time,
            exit_price=exit_price,
            exit_bar=self.bar_index,
            exit_time=self.current_time,
            exit_reason=exit_reason,
            quantity=close_qty,
            pnl=net_pnl,
            pnl_pct=pnl_pct,
            pnl_r=pnl_r,
            sl_price=pos.sl_price,
            tp_price=pos.tp_price,
            max_favorable_excursion=0.0,  # TODO: track during position
            max_adverse_excursion=0.0,
        )
        
        self.trades.append(trade)
        self.next_trade_id += 1
        
        # Update equity
        self.balance += net_pnl
        # Equity matches balance when flat (unrealized is 0)
        self.update_equity(self.balance)
        
        # Update consecutive losses
        if trade.is_winner:
            self.consecutive_losses = 0
        else:
            self.consecutive_losses += 1
        
        # Update position
        pos.quantity = _truncate_toward_zero(pos.quantity - close_qty)
        if pos.quantity <= QTY_PRECISION:
            self.position = None
        
        return trade
    
    def record_signal(
        self,
        long_raw: bool,
        short_raw: bool,
        allow_long: bool,
        allow_short: bool,
        long_final: bool,
        short_final: bool,
        **extra,
    ):
        """Record signals for parity export."""
        record = {
            'bar_index': self.bar_index,
            'timestamp': self.current_time,
            'long_signal_raw': long_raw,
            'short_signal_raw': short_raw,
            'allow_long': allow_long,
            'allow_short': allow_short,
            'long_signal': long_final,
            'short_signal': short_final,
        }
        if extra:
            record.update(extra)
        self.signal_history.append(record)
    
    def get_metrics(self, trades: Optional[List[Trade]] = None) -> dict:
        """Calculate performance metrics from trade history."""
        trade_source = trades if trades is not None else self.trades
        
        if not trade_source:
            return {
                'net_profit': 0.0,
                'net_profit_pct': 0.0,
                'total_trades': 0,
                'total_entries': self.entry_events,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'max_drawdown': 0.0,
                'profit_factor': 0.0,
                'avg_trade': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'largest_win': 0.0,
                'largest_loss': 0.0,
                'avg_bars_in_trade': 0.0,
                'profit_dd_ratio': 0.0,
                'gross_profit': 0.0,
                'gross_loss': 0.0,
            }
        
        winners = [t for t in trade_source if t.pnl > 0]
        losers = [t for t in trade_source if t.pnl <= 0]
        
        gross_profit = sum(t.pnl for t in winners)
        gross_loss = abs(sum(t.pnl for t in losers))
        net_profit = gross_profit - gross_loss
        
        return {
            'net_profit': net_profit,
            'net_profit_pct': (net_profit / self.initial_capital) * 100,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'total_trades': len(trade_source),
            'total_entries': self.entry_events,
            'winning_trades': len(winners),
            'losing_trades': len(losers),
            'win_rate': len(winners) / len(trade_source) * 100 if trade_source else 0.0,
            'max_drawdown': self.max_drawdown,
            'profit_factor': gross_profit / gross_loss if gross_loss > 0 else float('inf'),
            'avg_trade': net_profit / len(trade_source),
            'avg_win': gross_profit / len(winners) if winners else 0.0,
            'avg_loss': gross_loss / len(losers) if losers else 0.0,
            'largest_win': max((t.pnl for t in winners), default=0.0),
            'largest_loss': min((t.pnl for t in losers), default=0.0),
            'avg_bars_in_trade': sum(t.bars_held for t in trade_source) / len(trade_source),
            'profit_dd_ratio': net_profit / self.max_drawdown if self.max_drawdown > 0 else float('inf'),
        }
