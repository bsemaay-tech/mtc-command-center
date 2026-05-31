"""
Position Sizer.

Calculates position size based on risk parameters matching MTC.
"""

from typing import Optional


class PositionSizer:
    """
    Position size calculator.
    
    Calculates quantity based on:
    - Account equity
    - Risk percentage
    - Stop loss distance
    - Max leverage cap
    """
    
    def __init__(
        self,
        risk_long_pct: float = 4.0,
        risk_short_pct: float = 3.0,
        max_leverage: float = 5.0,
        mintick: float = 0.1,
    ):
        self.risk_long_pct = risk_long_pct
        self.risk_short_pct = risk_short_pct
        self.max_leverage = max_leverage
        # Pine parity: sizing guards use mintick (RiskSizingContext.mintick).
        self.mintick = max(float(mintick), 1e-10)
    
    def calculate(
        self,
        equity: float,
        entry_price: float,
        sl_price: float,
        direction: str,
    ) -> float:
        """
        Calculate position size based on risk.
        
        Args:
            equity: Current account equity
            entry_price: Planned entry price
            sl_price: Stop loss price
            direction: "long" or "short"
            
        Returns:
            Position quantity
        """
        # Get risk percentage for direction
        risk_pct = self.risk_long_pct if direction == "long" else self.risk_short_pct

        # Pine LIB_SLTP.f_calc_qty parity:
        # - Minimum SL distance safety: max(0.1% of entry, 10 * mintick)
        # - Risk money = equity * risk%
        # - Quantity capped by leverage notional cap
        sl_distance = abs(entry_price - sl_price)
        if sl_distance <= 0.0 or entry_price <= 0.0:
            return 0.0

        min_sl_dist_pct = entry_price * 0.001
        min_sl_dist_abs = self.mintick * 10.0
        min_sl_dist = max(min_sl_dist_pct, min_sl_dist_abs)
        sl_distance_safe = max(sl_distance, min_sl_dist)

        risk_amount = equity * (risk_pct / 100.0)
        ideal_qty = risk_amount / sl_distance_safe

        entry_safe = max(entry_price, self.mintick)
        max_allowed_money = equity * self.max_leverage
        max_qty_by_leverage = max_allowed_money / entry_safe

        qty = min(ideal_qty, max_qty_by_leverage)
        return max(qty, 0.0)
    
    def calculate_fallback(
        self,
        equity: float,
        entry_price: float,
        fallback_pct: float = 100.0,
        risk_pct: Optional[float] = None,
    ) -> float:
        """
        Calculate fallback position size when SL is not used.
        
        Args:
            equity: Current account equity
            entry_price: Planned entry price
            fallback_pct: Percentage of equity to use
            
        Returns:
            Position quantity
        """
        # TradingView parity (use_sl=false branch):
        # effectiveRisk = min(fallbackPct, riskPct)
        # qty = (equity * effectiveRisk / 100) / entry
        # capped by max leverage notional
        if entry_price <= 0.0:
            return 0.0

        effective_risk = min(fallback_pct, risk_pct if risk_pct is not None else fallback_pct)

        position_money = equity * (effective_risk / 100.0)
        entry_safe = max(entry_price, self.mintick)
        fallback_qty = position_money / entry_safe

        max_allowed_money = equity * self.max_leverage
        max_qty_by_leverage = max_allowed_money / entry_safe

        qty = min(fallback_qty, max_qty_by_leverage)
        return max(qty, 0.0)
    
    def calculate_with_leverage(
        self,
        equity: float,
        entry_price: float,
        leverage: float,
    ) -> float:
        """
        Calculate position size for specific leverage.
        
        Args:
            equity: Current account equity
            entry_price: Entry price
            leverage: Desired leverage
            
        Returns:
            Position quantity
        """
        leverage = min(leverage, self.max_leverage)
        if entry_price <= 0.0:
            return 0.0

        qty = (equity * leverage) / entry_price
        return max(qty, 0.0)
    
    def get_effective_leverage(
        self,
        equity: float,
        entry_price: float,
        quantity: float,
    ) -> float:
        """
        Calculate effective leverage for a position.
        
        Args:
            equity: Account equity
            entry_price: Entry price
            quantity: Position quantity
            
        Returns:
            Effective leverage
        """
        position_value = entry_price * quantity
        return position_value / equity if equity > 0 else 0
    
    def get_risk_amount(
        self,
        entry_price: float,
        sl_price: float,
        quantity: float,
    ) -> float:
        """
        Calculate dollar risk for a position.
        
        Args:
            entry_price: Entry price
            sl_price: Stop loss price
            quantity: Position quantity
            
        Returns:
            Risk amount in dollars
        """
        sl_distance = abs(entry_price - sl_price)
        return sl_distance * quantity
