import sys, json, pandas as pd
from pathlib import Path
sys.path.insert(0, '.')
from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner
from datetime import datetime
import pandas as pd

with open('parity_suite_350/cases/parity_core_020_time_stop_bars_v01.json') as f:
    case = json.load(f)

cfg = MTCConfig.model_validate(case['config'])

original_process_exits = MTCRunner._process_exits

def traced_process_exits(self, bar, df_ref, i, long_filtered, short_filtered, can_trade_window, *args, **kwargs):
    if i == 35132:
        print(f"--- BAR 35132 ---")
        print(f"in_position: {self.state.in_position}")
        print(f"can_trade: {can_trade_window}")
        pos = self.state.position
        if pos:
            bars_in_pos = i - pos.entry_bar
            print(f"bars_in_pos={bars_in_pos} vs target={self.config.time_stop.bars}")
            unreal = pos.unrealized_pnl(bar["close"])
            print(f"unrealized={unreal}")

    res = original_process_exits(self, bar, df_ref, i, long_filtered, short_filtered, can_trade_window, *args, **kwargs)
    
    if i == 35132:
        print(f"exit returned: {res}")
    return res

MTCRunner._process_exits = traced_process_exits

df = pd.read_parquet('data/BTCUSDT_15m_20240101_20260213.parquet')
runner = MTCRunner(cfg)

try:
    results = runner.run(df, eval_start=datetime.fromisoformat('2025-06-30T00:00:00'), eval_end=datetime.fromisoformat('2025-07-02T00:00:00'))
except Exception as e:
    print('error:', e)
