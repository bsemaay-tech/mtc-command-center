"""
Fee and Slippage Model for MTC Backtest System.

Implements commission and slippage calculations to match
TradingView strategy tester behavior.
"""

from dataclasses import dataclass
from typing import Literal, Optional
from pydantic import BaseModel, Field

from .precision import round_price, round_qty, get_tick_size


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class FeeConfig(BaseModel):
    """Fee and slippage configuration."""
    
    # Commission
    commission_percent: float = Field(
        default=0.04,
        ge=0.0,
        description="Commission percentage applied on notional at entry AND exit"
    )
    
    # Slippage
    slippage_ticks: int = Field(
        default=5,
        ge=0,
        description="Slippage in ticks"
    )
    
    # Tick size
    tick_size: float = Field(
        default=0.01,
        gt=0,
        description="Minimum price increment (fallback value)"
    )
    tick_size_source: Literal["exchange", "fixed"] = Field(
        default="exchange",
        description="Source for tick size: exchange metadata or fixed value"
    )
    
    class Config:
        validate_assignment = True


# ═══════════════════════════════════════════════════════════════════════════════
# FEE MODEL
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class FeeResult:
    """Result of fee calculation."""
    commission: float       # Commission amount
    slippage: float         # Slippage amount
    total_cost: float       # Total cost (commission + slippage)
    adjusted_price: float   # Price after slippage adjustment


class FeeModel:
    """
    Fee and slippage calculator.
    
    Implements TradingView-compatible fee model where:
    - Commission is applied as percentage of notional
    - Slippage is applied in ticks to the fill price
    
    Example:
        >>> fee_model = FeeModel(commission_percent=0.04, slippage_ticks=5)
        >>> result = fee_model.calculate_entry_cost(
        ...     price=50000.0,
        ...     quantity=0.1,
        ...     is_long=True
        ... )
        >>> print(f"Entry price: {result.adjusted_price}")
    """
    
    def __init__(
        self,
        commission_percent: float = 0.04,
        slippage_ticks: int = 5,
        tick_size: float = 0.01,
    ):
        """
        Initialize fee model.
        
        Args:
            commission_percent: Commission as percentage of notional
            slippage_ticks: Slippage in number of ticks
            tick_size: Price tick size
        """
        self.commission_percent = commission_percent
        self.slippage_ticks = slippage_ticks
        self.tick_size = tick_size
    
    @classmethod
    def from_config(cls, config: FeeConfig) -> 'FeeModel':
        """Create FeeModel from configuration."""
        return cls(
            commission_percent=config.commission_percent,
            slippage_ticks=config.slippage_ticks,
            tick_size=config.tick_size,
        )
    
    def calculate_commission(self, price: float, quantity: float) -> float:
        """
        Calculate commission for a trade.
        
        Commission = notional * (commission_percent / 100)
        
        Args:
            price: Trade price
            quantity: Trade quantity
            
        Returns:
            Commission amount
        """
        notional = price * quantity
        commission = notional * (self.commission_percent / 100)
        return round_price(commission)
    
    def calculate_slippage(self, is_long: bool) -> float:
        """
        Calculate slippage amount.
        
        Slippage = slippage_ticks * tick_size
        
        For entries:
        - Long: Price increases (worse fill)
        - Short: Price decreases (worse fill)
        
        For exits:
        - Long: Price decreases (worse fill)
        - Short: Price increases (worse fill)
        
        Args:
            is_long: True for long direction
            
        Returns:
            Slippage amount (signed based on direction)
        """
        slippage = self.slippage_ticks * self.tick_size
        return round_price(slippage)
    
    def adjust_entry_price(self, price: float, is_long: bool) -> float:
        """
        Adjust entry price for slippage (worst-case fill).
        
        Args:
            price: Original entry price
            is_long: True for long entry
            
        Returns:
            Adjusted entry price
        """
        slippage = self.calculate_slippage(is_long)
        
        if is_long:
            # Long entry: price increases (we pay more)
            adjusted = price + slippage
        else:
            # Short entry: price decreases (we sell for less)
            adjusted = price - slippage
        
        return round_price(adjusted)
    
    def adjust_exit_price(self, price: float, is_long: bool) -> float:
        """
        Adjust exit price for slippage (worst-case fill).
        
        Args:
            price: Original exit price
            is_long: True for long position
            
        Returns:
            Adjusted exit price
        """
        slippage = self.calculate_slippage(is_long)
        
        if is_long:
            # Long exit: price decreases (we receive less)
            adjusted = price - slippage
        else:
            # Short exit: price increases (we pay more to cover)
            adjusted = price + slippage
        
        return round_price(adjusted)
    
    def calculate_entry_cost(
        self,
        price: float,
        quantity: float,
        is_long: bool,
    ) -> FeeResult:
        """
        Calculate total entry cost including fees and slippage.
        
        Args:
            price: Entry price
            quantity: Entry quantity
            is_long: True for long entry
            
        Returns:
            FeeResult with commission, slippage, total cost, and adjusted price
        """
        adjusted_price = self.adjust_entry_price(price, is_long)
        commission = self.calculate_commission(adjusted_price, quantity)
        slippage_amount = abs(adjusted_price - price) * quantity
        
        return FeeResult(
            commission=commission,
            slippage=round_price(slippage_amount),
            total_cost=round_price(commission + slippage_amount),
            adjusted_price=adjusted_price,
        )
    
    def calculate_exit_cost(
        self,
        price: float,
        quantity: float,
        is_long: bool,
    ) -> FeeResult:
        """
        Calculate total exit cost including fees and slippage.
        
        Args:
            price: Exit price
            quantity: Exit quantity
            is_long: True for long position
            
        Returns:
            FeeResult with commission, slippage, total cost, and adjusted price
        """
        adjusted_price = self.adjust_exit_price(price, is_long)
        commission = self.calculate_commission(adjusted_price, quantity)
        slippage_amount = abs(adjusted_price - price) * quantity
        
        return FeeResult(
            commission=commission,
            slippage=round_price(slippage_amount),
            total_cost=round_price(commission + slippage_amount),
            adjusted_price=adjusted_price,
        )
    
    def calculate_round_trip_cost(
        self,
        entry_price: float,
        exit_price: float,
        quantity: float,
        is_long: bool,
    ) -> float:
        """
        Calculate total round-trip cost (entry + exit).
        
        Args:
            entry_price: Entry price
            exit_price: Exit price
            quantity: Trade quantity
            is_long: True for long trade
            
        Returns:
            Total cost for round trip
        """
        entry_cost = self.calculate_entry_cost(entry_price, quantity, is_long)
        exit_cost = self.calculate_exit_cost(exit_price, quantity, is_long)
        
        return round_price(entry_cost.total_cost + exit_cost.total_cost)


# ═══════════════════════════════════════════════════════════════════════════════
# PNL CALCULATIONS WITH FEES
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_net_pnl(
    entry_price: float,
    exit_price: float,
    quantity: float,
    is_long: bool,
    fee_model: FeeModel,
) -> float:
    """
    Calculate net PnL after fees and slippage.
    
    Args:
        entry_price: Entry price
        exit_price: Exit price  
        quantity: Trade quantity
        is_long: True for long trade
        fee_model: Fee model instance
        
    Returns:
        Net PnL after all costs
    """
    # Gross PnL
    if is_long:
        gross_pnl = (exit_price - entry_price) * quantity
    else:
        gross_pnl = (entry_price - exit_price) * quantity
    
    # Total costs
    total_cost = fee_model.calculate_round_trip_cost(
        entry_price, exit_price, quantity, is_long
    )
    
    return round_price(gross_pnl - total_cost)


def calculate_breakeven_price(
    entry_price: float,
    quantity: float,
    is_long: bool,
    fee_model: FeeModel,
) -> float:
    """
    Calculate breakeven price accounting for fees.
    
    Args:
        entry_price: Entry price
        quantity: Position quantity
        is_long: True for long position
        fee_model: Fee model instance
        
    Returns:
        Breakeven price
    """
    # Entry cost per unit
    entry_cost = fee_model.calculate_entry_cost(entry_price, quantity, is_long)
    entry_cost_per_unit = entry_cost.total_cost / quantity if quantity > 0 else 0
    
    # Exit commission estimate (using entry price as proxy)
    exit_commission_per_unit = fee_model.calculate_commission(entry_price, 1)
    
    # Slippage per unit
    slippage_per_unit = fee_model.slippage_ticks * fee_model.tick_size
    
    total_cost_per_unit = entry_cost_per_unit + exit_commission_per_unit + slippage_per_unit
    
    if is_long:
        breakeven = entry_price + (total_cost_per_unit / 1)  # Need to recover costs
    else:
        breakeven = entry_price - (total_cost_per_unit / 1)
    
    return round_price(breakeven)
