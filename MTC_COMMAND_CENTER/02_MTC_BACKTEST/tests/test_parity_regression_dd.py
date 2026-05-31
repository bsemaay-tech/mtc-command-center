import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))


def test_tv_realized_max_drawdown_pct_helper():
    import parity_regression

    # Net pnl sequence yields equity path: 100, 110, 105, 125, 95
    # Peak-to-trough DD at last point: (125-95)/125 * 100 = 24.0
    tv = pd.DataFrame({"net_pnl": [10.0, -5.0, 20.0, -30.0]})
    dd = parity_regression._tv_realized_max_drawdown_pct(tv, 100.0)
    assert round(dd, 6) == 24.0
