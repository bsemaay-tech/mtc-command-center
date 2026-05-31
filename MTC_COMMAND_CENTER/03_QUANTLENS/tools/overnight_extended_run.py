        """Auto-generated overnight runner — extends mega_walk_forward.py
        with 19 additional strategy entries from the 2026-05-30 triage.
        Generated: 2026-05-31T00:09:34
        """
        import sys
        from pathlib import Path
        ROOT = Path(__file__).resolve().parent.parent / "04_PYTHON_PROTOTYPES"
        sys.path.insert(0, str(ROOT.parent))

        # Import the new candidates so the runner discovers them.
        from PYTHON_PROTOTYPES import QL_VCP_RICHARD_1D_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_VCP_MINERVINI_1D_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_DEEPAK_153_FILTER_1D_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_SELL_RULES_MARKET_WIZARDS_OVERLAY_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_CONNELL_EVENT_DRIVEN_GAP_1D_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_CONNELL_EVENT_DRIVEN_GAP_5M_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_AVWAP_BRIAN_GAP_RECLAIM_5M_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_AVWAP_BRIAN_STAGE2_EMERGING_1D_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_AVWAP_BRIAN_INTRADAY_OR_5M_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_AVWAP_BRIAN_EARNINGS_ANCHOR_1D_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_EPISODIC_PIVOT_CHRISTIAN_5M_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_TRAIL_20MA_CHRISTIAN_1D_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_VCP_EARLY_ENTRY_CHRISTIAN_1D_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_LAUNCHPAD_PROSWING_1D_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_HIGHEST_VOLUME_EDGE_PROSWING_1D_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_RS_PHASE_DAYS_PROSWING_OVERLAY_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_DEEPAK_259_RISK_OVERLAY_prototype  # noqa: F401
from PYTHON_PROTOTYPES import QL_DEEPAK_SNAPBACK_50SMA_INTRADAY_prototype  # noqa: F401

        # Delegate to mega_walk_forward — its STRATEGY_LIB scans 04_PYTHON_PROTOTYPES
        # for files ending in _prototype.py and registers them automatically.
        from mega_walk_forward import main as mega_main

        if __name__ == "__main__":
            mega_main()
