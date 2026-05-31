from argparse import Namespace

import pytest

from src.optimizer_v0.__main__ import _require_resume_compat


def _args(**overrides):
    base = {
        "mode": "random",
        "seed": 42,
        "case": "configs/cases/aug2025_parity.json",
        "workers": 1,
        "min_trades": 10,
        "max_dd": 40.0,
    }
    base.update(overrides)
    return Namespace(**base)


def test_require_resume_compat_ok():
    existing = {
        "mode": "random",
        "seed": 42,
        "case_path": "configs/cases/aug2025_parity.json",
        "workers": 1,
        "min_trades": 10,
        "max_dd_pct": 40.0,
    }
    _require_resume_compat(existing, _args())


def test_require_resume_compat_mismatch_raises():
    existing = {
        "mode": "random",
        "seed": 42,
        "case_path": "configs/cases/aug2025_parity.json",
        "workers": 1,
        "min_trades": 10,
        "max_dd_pct": 40.0,
    }
    with pytest.raises(ValueError, match="Resume mismatch detected"):
        _require_resume_compat(existing, _args(min_trades=50))
