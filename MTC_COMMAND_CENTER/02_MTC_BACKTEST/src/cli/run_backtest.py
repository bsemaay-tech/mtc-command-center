#!/usr/bin/env python3
"""
CLI Backtest Runner for MTC Backtest System.

Run backtests without Streamlit UI.

Usage:
    python -m src.cli.run_backtest --data data/btcusdt_15m.parquet
    python -m src.cli.run_backtest --data data/btcusdt_15m.csv --config config.json
    python -m src.cli.run_backtest --data data/btcusdt_15m.parquet --export-parity
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="MTC Python Backtest CLI Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic backtest with defaults
    python -m src.cli.run_backtest --data data/btcusdt_15m.parquet
    
    # With custom config
    python -m src.cli.run_backtest --data data/btcusdt_15m.csv --config my_config.json
    
    # Export parity CSV
    python -m src.cli.run_backtest --data data/btcusdt_15m.parquet --export-parity
    
    # Dry run (validate only)
    python -m src.cli.run_backtest --data data/btcusdt_15m.parquet --dry-run
        """
    )
    
    # Required
    parser.add_argument(
        '--data', '-d',
        type=str,
        required=True,
        help='Path to OHLCV data file (CSV or Parquet)'
    )
    
    # Optional config
    parser.add_argument(
        '--config', '-c',
        type=str,
        default=None,
        help='Path to JSON config file (uses defaults if not provided)'
    )
    
    # Output
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='./exports/runs',
        help='Output directory for results (default: ./exports/runs)'
    )
    
    # Backtest settings
    parser.add_argument(
        '--warmup',
        type=int,
        default=20,
        help='Warmup bars for indicator calculation (default: 20)'
    )

    parser.add_argument(
        '--eval-start',
        type=str,
        default=None,
        help='Evaluation window start (ISO8601, UTC recommended), e.g. 2024-07-01T00:00:00+00:00'
    )

    parser.add_argument(
        '--eval-end',
        type=str,
        default=None,
        help='Evaluation window end (ISO8601, UTC recommended), e.g. 2024-12-31T23:59:59+00:00'
    )
    
    # Export options
    parser.add_argument(
        '--export-parity',
        action='store_true',
        help='Export parity CSV for TradingView comparison'
    )
    
    parser.add_argument(
        '--export-trades',
        action='store_true',
        default=True,
        help='Export trades CSV (default: True)'
    )
    
    # Execution options
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate config and data without running backtest'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose/debug logging'
    )
    
    return parser.parse_args()


def load_config(config_path: str | None):
    """Load configuration from JSON file or use defaults."""
    from src.config.defaults import MTCConfig
    
    if config_path is None:
        print("Using default configuration")
        return MTCConfig()
    
    config_path = Path(config_path)
    if not config_path.exists():
        print(f"Warning: Config file not found: {config_path}")
        print("Using default configuration")
        return MTCConfig()
    
    with open(config_path, 'r') as f:
        config_dict = json.load(f)
    
    print(f"Loaded config from: {config_path}")
    return MTCConfig(**config_dict)


def load_data(data_path: str):
    """Load OHLCV data from file."""
    from src.data.io import load_dataset
    
    data_path = Path(data_path)
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    df = load_dataset(str(data_path))
    print(f"Loaded {len(df)} bars from: {data_path}")
    
    return df


def run_backtest(df, config, warmup: int, export_parity: bool, eval_start: str | None = None, eval_end: str | None = None):
    """Run the backtest."""
    from src.engine.mtc_runner import MTCRunner
    from src.parity.exporter import ParityExporter
    
    print(f"\nRunning backtest...")
    print(f"  Signal Mode: {config.signal_mode}")
    print(f"  Warmup Bars: {warmup}")
    print(f"  Data Bars: {len(df)}")
    if eval_start or eval_end:
        print(f"  Eval Window: {eval_start or '-inf'} -> {eval_end or '+inf'}")
    
    # Create runner
    runner = MTCRunner(config)
    
    # Run backtest
    results = runner.run(
        df,
        warmup_bars=warmup,
        eval_start=eval_start,
        eval_end=eval_end,
    )
    
    return results


def save_results(results, output_dir: str, export_trades: bool, export_parity: bool):
    """Save backtest results to files."""
    output_path = Path(output_dir)
    
    # Create run directory with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    run_dir = output_path / f"run_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    
    # Save metrics
    metrics_path = run_dir / "metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(results['metrics'], f, indent=2, default=str)
    print(f"Saved metrics to: {metrics_path}")
    
    # Save trades
    if export_trades and results.get('trades'):
        import pandas as pd
        trades_data = []
        for t in results['trades']:
            trades_data.append({
                'trade_id': t.trade_id,
                'direction': t.direction.value if hasattr(t.direction, 'value') else t.direction,
                'entry_price': t.entry_price,
                'exit_price': t.exit_price,
                'quantity': t.quantity,
                'pnl': t.pnl,
                'pnl_pct': t.pnl_pct,
                'pnl_r': t.pnl_r,
                'exit_reason': t.exit_reason.value if hasattr(t.exit_reason, 'value') else t.exit_reason,
                'bars_held': t.bars_held,
            })
        
        trades_df = pd.DataFrame(trades_data)
        trades_path = run_dir / "trades.csv"
        trades_df.to_csv(trades_path, index=False)
        print(f"Saved trades to: {trades_path}")
    
    # Save equity curve
    if results.get('equity_curve'):
        import pandas as pd
        equity_df = pd.DataFrame({'equity': results['equity_curve']})
        equity_path = run_dir / "equity_curve.csv"
        equity_df.to_csv(equity_path, index=False)
        print(f"Saved equity curve to: {equity_path}")
    
    # Save parity export
    if export_parity and results.get('parity_records'):
        parity_path = run_dir / "parity_export.csv"
        results['parity_records'].export_csv(parity_path)
        print(f"Saved parity export to: {parity_path}")
    
    return run_dir


def print_summary(results):
    """Print backtest summary to console."""
    metrics = results.get('metrics', {})
    
    print("\n" + "=" * 60)
    print("BACKTEST RESULTS")
    print("=" * 60)
    
    print(f"\n📊 Performance:")
    print(f"   Net Profit:      ${metrics.get('net_profit', 0):.2f}")
    print(f"   Net Profit %:    {metrics.get('net_profit_pct', 0):.2f}%")
    print(f"   Max Drawdown:    {metrics.get('max_drawdown', 0):.2f}%")
    print(f"   Profit/DD:       {metrics.get('profit_dd_ratio', 0):.2f}")
    
    print(f"\n📈 Trades:")
    print(f"   Total Trades:    {metrics.get('total_trades', 0)}")
    print(f"   Win Rate:        {metrics.get('win_rate', 0):.1f}%")
    print(f"   Profit Factor:   {metrics.get('profit_factor', 0):.2f}")
    print(f"   Avg Trade:       ${metrics.get('avg_trade', 0):.2f}")
    
    print(f"\n📉 Risk:")
    print(f"   Sharpe Ratio:    {metrics.get('sharpe_ratio', 0):.2f}")
    print(f"   Sortino Ratio:   {metrics.get('sortino_ratio', 0):.2f}")
    print(f"   Calmar Ratio:    {metrics.get('calmar_ratio', 0):.2f}")
    
    print("\n" + "=" * 60)


def main():
    """Main entry point."""
    args = parse_args()
    
    # Setup logging
    if args.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    print("=" * 60)
    print("MTC Python Backtest CLI")
    print("=" * 60)
    
    try:
        # Load config
        config = load_config(args.config)
        
        # Load data
        df = load_data(args.data)
        
        # Dry run check
        if args.dry_run:
            print("\n✅ Dry run successful!")
            print(f"   Config valid: Yes")
            print(f"   Data loaded: {len(df)} bars")
            return 0
        
        # Run backtest
        results = run_backtest(
            df=df,
            config=config,
            warmup=args.warmup,
            export_parity=args.export_parity,
            eval_start=args.eval_start,
            eval_end=args.eval_end,
        )
        
        # Print summary
        print_summary(results)
        
        # Save results
        run_dir = save_results(
            results=results,
            output_dir=args.output,
            export_trades=args.export_trades,
            export_parity=args.export_parity,
        )
        
        print(f"\n✅ Results saved to: {run_dir}")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
