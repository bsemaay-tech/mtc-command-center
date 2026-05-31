"""
Parity Exporter for MTC Backtest System.

Exports bar-by-bar state for comparison with TradingView Pine Script output.
All timestamps are in UTC.
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Any, Dict
from dataclasses import dataclass, field, asdict

import pandas as pd
from pydantic import BaseModel


# ═══════════════════════════════════════════════════════════════════════════════
# PARITY RECORD SCHEMA
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ParityRecord:
    """
    Single bar parity record.
    
    Contains all state needed to compare Python vs TradingView outputs.
    """
    # Time & Index
    timestamp_close_utc: datetime
    bar_index: int
    
    # Raw Signals (before filters)
    longSignal_raw: bool = False
    shortSignal_raw: bool = False
    
    # Filter Outputs
    allowLong: bool = True
    allowShort: bool = True
    guardAllow: bool = True
    
    # Final Signals (after all filters)
    longSignal: bool = False
    shortSignal: bool = False
    
    # Position State
    position_direction: str = "flat"  # "long", "short", "flat"
    position_qty: float = 0.0
    avg_entry_price: float = 0.0
    
    # Risk Levels
    sl_price: Optional[float] = None
    tp1_price: Optional[float] = None
    tp2_price: Optional[float] = None
    trailing_stop: Optional[float] = None
    
    # Events
    exit_reason: Optional[str] = None   # "SL", "TP1", "TP2", "TRAIL", "OPP_SIGNAL"
    entry_reason: Optional[str] = None  # "LONG_SIGNAL", "SHORT_SIGNAL"
    exit_id: Optional[str] = None
    lifecycle_id: Optional[str] = None
    event_seq_in_bar: Optional[int] = None
    execution_profile_id: Optional[str] = None
    working_exit_book_version: Optional[int] = None
    
    # Equity & PnL
    equity: float = 0.0
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0

    # Parity provenance
    effective_history_start_utc: Optional[datetime] = None
    warmup_bars: Optional[int] = None
    warmup_seeded: Optional[bool] = None
    warmup_seed_provenance: Optional[str] = None
    
    # Debug: OHLC
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with proper serialization."""
        d = asdict(self)
        for key in ("timestamp_close_utc", "effective_history_start_utc"):
            if isinstance(d.get(key), datetime):
                d[key] = d[key].isoformat()
        return d


# ═══════════════════════════════════════════════════════════════════════════════
# PARITY EXPORTER
# ═══════════════════════════════════════════════════════════════════════════════

class ParityExporter:
    """
    Records and exports bar-by-bar state for parity comparison.
    
    Usage:
        exporter = ParityExporter()
        
        for bar in bars:
            # ... run strategy logic ...
            exporter.record_bar(
                bar_index=bar.bar_index,
                timestamp_close_utc=bar.close_time,
                state=state,
                signals=signals,
                bar=bar,
            )
        
        exporter.export_csv("parity_export.csv")
    """
    
    def __init__(self):
        """Initialize parity exporter."""
        self.records: List[ParityRecord] = []
    
    def clear(self) -> None:
        """Clear all records."""
        self.records = []
    
    def record_bar(
        self,
        bar_index: int,
        timestamp_close_utc: datetime,
        # Signals
        longSignal_raw: bool = False,
        shortSignal_raw: bool = False,
        allowLong: bool = True,
        allowShort: bool = True,
        guardAllow: bool = True,
        longSignal: bool = False,
        shortSignal: bool = False,
        # Position
        position_direction: str = "flat",
        position_qty: float = 0.0,
        avg_entry_price: float = 0.0,
        # Risk
        sl_price: Optional[float] = None,
        tp1_price: Optional[float] = None,
        tp2_price: Optional[float] = None,
        trailing_stop: Optional[float] = None,
        # Events
        exit_reason: Optional[str] = None,
        entry_reason: Optional[str] = None,
        exit_id: Optional[str] = None,
        lifecycle_id: Optional[str] = None,
        event_seq_in_bar: Optional[int] = None,
        execution_profile_id: Optional[str] = None,
        working_exit_book_version: Optional[int] = None,
        # Equity
        equity: float = 0.0,
        realized_pnl: float = 0.0,
        unrealized_pnl: float = 0.0,
        # Parity provenance
        effective_history_start_utc: Optional[datetime] = None,
        warmup_bars: Optional[int] = None,
        warmup_seeded: Optional[bool] = None,
        warmup_seed_provenance: Optional[str] = None,
        # OHLC
        open: float = 0.0,
        high: float = 0.0,
        low: float = 0.0,
        close: float = 0.0,
    ) -> None:
        """
        Record state for a single bar.
        
        Args:
            bar_index: Sequential bar index
            timestamp_close_utc: Bar close time (UTC)
            ... (all state fields)
        """
        record = ParityRecord(
            timestamp_close_utc=timestamp_close_utc,
            bar_index=bar_index,
            longSignal_raw=longSignal_raw,
            shortSignal_raw=shortSignal_raw,
            allowLong=allowLong,
            allowShort=allowShort,
            guardAllow=guardAllow,
            longSignal=longSignal,
            shortSignal=shortSignal,
            position_direction=position_direction,
            position_qty=position_qty,
            avg_entry_price=avg_entry_price,
            sl_price=sl_price,
            tp1_price=tp1_price,
            tp2_price=tp2_price,
            trailing_stop=trailing_stop,
            exit_reason=exit_reason,
            entry_reason=entry_reason,
            exit_id=exit_id,
            lifecycle_id=lifecycle_id,
            event_seq_in_bar=event_seq_in_bar,
            execution_profile_id=execution_profile_id,
            working_exit_book_version=working_exit_book_version,
            equity=equity,
            realized_pnl=realized_pnl,
            unrealized_pnl=unrealized_pnl,
            effective_history_start_utc=effective_history_start_utc,
            warmup_bars=warmup_bars,
            warmup_seeded=warmup_seeded,
            warmup_seed_provenance=warmup_seed_provenance,
            open=open,
            high=high,
            low=low,
            close=close,
        )
        self.records.append(record)
    
    def record_from_state(
        self,
        bar_index: int,
        timestamp_close_utc: datetime,
        state: Any,  # MTCState
        signals: Dict[str, bool],
        bar: Dict[str, float],
    ) -> None:
        """
        Record bar from MTCState object.
        
        Args:
            bar_index: Bar index
            timestamp_close_utc: Bar close time
            state: MTCState instance
            signals: Dict with signal flags
            bar: Dict with OHLC data
        """
        position = state.position
        
        self.record_bar(
            bar_index=bar_index,
            timestamp_close_utc=timestamp_close_utc,
            longSignal_raw=signals.get('longSignal_raw', False),
            shortSignal_raw=signals.get('shortSignal_raw', False),
            allowLong=signals.get('allowLong', True),
            allowShort=signals.get('allowShort', True),
            guardAllow=signals.get('guardAllow', True),
            longSignal=signals.get('longSignal', False),
            shortSignal=signals.get('shortSignal', False),
            position_direction=(
                "long" if position and position.is_long() else
                "short" if position and position.is_short() else
                "flat"
            ),
            position_qty=position.quantity if position else 0.0,
            avg_entry_price=position.entry_price if position else 0.0,
            sl_price=position.sl_price if position else None,
            tp1_price=position.tp1_price if position else None,
            tp2_price=position.tp2_price if position else None,
            trailing_stop=position.trailing_stop if position else None,
            exit_reason=signals.get('exit_reason'),
            entry_reason=signals.get('entry_reason'),
            exit_id=signals.get('exit_id'),
            lifecycle_id=signals.get('lifecycle_id'),
            event_seq_in_bar=signals.get('event_seq_in_bar'),
            execution_profile_id=signals.get('execution_profile_id', getattr(state, 'execution_profile_id', None)),
            working_exit_book_version=signals.get(
                'working_exit_book_version',
                getattr(position, 'working_exit_book_version', None) if position else None,
            ),
            equity=state.equity,
            realized_pnl=state.realized_pnl,
            unrealized_pnl=state.unrealized_pnl,
            effective_history_start_utc=signals.get('effective_history_start_utc'),
            warmup_bars=signals.get('warmup_bars', getattr(state, 'warmup_bars', None)),
            warmup_seeded=signals.get('warmup_seeded'),
            warmup_seed_provenance=signals.get('warmup_seed_provenance'),
            open=bar.get('open', 0.0),
            high=bar.get('high', 0.0),
            low=bar.get('low', 0.0),
            close=bar.get('close', 0.0),
        )
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        Get records as pandas DataFrame.
        
        Returns:
            DataFrame with all parity records
        """
        if not self.records:
            return pd.DataFrame()
        
        return pd.DataFrame([r.to_dict() for r in self.records])
    
    def export_csv(self, path: Path | str) -> None:
        """
        Export records to CSV file.
        
        Args:
            path: Output file path
        """
        df = self.get_dataframe()
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
    
    def export_json(self, path: Path | str, indent: int = 2) -> None:
        """
        Export records to JSON file.
        
        Args:
            path: Output file path
            indent: JSON indentation
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        data = [r.to_dict() for r in self.records]
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=indent, default=str)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics.
        
        Returns:
            Dict with summary info
        """
        if not self.records:
            return {"total_bars": 0}
        
        df = self.get_dataframe()
        
        return {
            "total_bars": len(df),
            "long_signals_raw": int(df['longSignal_raw'].sum()),
            "short_signals_raw": int(df['shortSignal_raw'].sum()),
            "long_signals_final": int(df['longSignal'].sum()),
            "short_signals_final": int(df['shortSignal'].sum()),
            "total_exits": int(df['exit_reason'].notna().sum()),
            "total_entries": int(df['entry_reason'].notna().sum()),
            "final_equity": float(df['equity'].iloc[-1]) if len(df) > 0 else 0.0,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# COMPARISON UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def compare_parity_files(
    python_path: Path | str,
    pine_path: Path | str,
    tolerance: float = 1e-6,
) -> pd.DataFrame:
    """
    Compare Python and Pine Script parity exports.
    
    Args:
        python_path: Path to Python export CSV
        pine_path: Path to Pine Script export CSV
        tolerance: Tolerance for float comparison
        
    Returns:
        DataFrame with comparison results
    """
    py_df = pd.read_csv(python_path)
    pine_df = pd.read_csv(pine_path)
    
    # Merge on bar_index
    merged = pd.merge(
        py_df, pine_df,
        on='bar_index',
        suffixes=('_py', '_pine'),
        how='outer',
    )
    
    # Compare key columns
    compare_cols = [
        'longSignal_raw', 'shortSignal_raw',
        'longSignal', 'shortSignal',
        'position_direction', 'position_qty',
    ]
    
    results = []
    for col in compare_cols:
        py_col = f"{col}_py"
        pine_col = f"{col}_pine"
        
        if py_col in merged.columns and pine_col in merged.columns:
            matches = merged[py_col] == merged[pine_col]
            results.append({
                'column': col,
                'matches': int(matches.sum()),
                'mismatches': int((~matches).sum()),
                'match_rate': float(matches.mean()) if len(matches) > 0 else 0.0,
            })
    
    return pd.DataFrame(results)
