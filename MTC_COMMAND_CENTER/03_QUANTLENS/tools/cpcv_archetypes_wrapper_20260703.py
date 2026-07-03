#!/usr/bin/env python3
"""Runs cpcv_validator with the research archetypes patched in (so CPCV can re-run their
signals). Applies the archetype monkey-patch at module level, then delegates to
cpcv_validator.main(). All cpcv_validator CLI args pass through."""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
os.environ.setdefault(
    "MEGA_BUNDLE_MANIFEST",
    r"C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\data"
    r"\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json",
)

import research_archetypes_20260703 as arch  # noqa: E402
arch.apply()

import cpcv_validator  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(cpcv_validator.main())
