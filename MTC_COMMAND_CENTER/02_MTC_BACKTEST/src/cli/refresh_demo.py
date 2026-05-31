#!/usr/bin/env python3
"""
Demo Data Refresh Script for MTC Backtest System.

Downloads a fixed dataset for reproducible testing and parity validation.

Usage:
    python -m src.cli.refresh_demo
"""

import sys
from pathlib import Path
from datetime import datetime, timezone

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

DEMO_CONFIG = {
    "symbol": "BTCUSDT",
    "timeframe": "15m",
    "start": "2024-01-01",
    "end": "2024-01-31",  # 1 month = ~2880 bars (small enough to commit)
    "output_name": "demo_btcusdt_15m_2024jan",
}


def main():
    """Refresh demo dataset."""
    from src.data.download import download_ohlcv
    from src.data.io import save_dataset
    
    print("=" * 60)
    print("MTC Demo Data Refresh")
    print("=" * 60)
    
    config = DEMO_CONFIG
    
    print(f"\nDownloading demo dataset:")
    print(f"  Symbol:    {config['symbol']}")
    print(f"  Timeframe: {config['timeframe']}")
    print(f"  Start:     {config['start']}")
    print(f"  End:       {config['end']}")
    
    try:
        # Parse dates
        start_dt = datetime.strptime(config['start'], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end_dt = datetime.strptime(config['end'], "%Y-%m-%d").replace(
            hour=23, minute=59, second=59, tzinfo=timezone.utc
        )
        
        # Download
        df = download_ohlcv(
            symbol=config['symbol'],
            timeframe=config['timeframe'],
            start_date=start_dt,
            end_date=end_dt,
            show_progress=True,
        )
        
        print(f"\n✅ Downloaded {len(df)} bars")
        
        # Save to data directory
        data_dir = project_root / "data"
        data_dir.mkdir(exist_ok=True)
        
        # Save as parquet (efficient)
        parquet_path = data_dir / f"{config['output_name']}.parquet"
        save_dataset(df, parquet_path, format='parquet')
        print(f"Saved: {parquet_path}")
        
        # Also save as CSV (human-readable)
        csv_path = data_dir / f"{config['output_name']}.csv"
        save_dataset(df, csv_path, format='csv')
        print(f"Saved: {csv_path}")
        
        # Print summary
        print(f"\n📊 Dataset Summary:")
        print(f"   Bars:       {len(df)}")
        print(f"   First Bar:  {df.index[0]}")
        print(f"   Last Bar:   {df.index[-1]}")
        print(f"   Open Range: ${df['open'].min():.2f} - ${df['open'].max():.2f}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
