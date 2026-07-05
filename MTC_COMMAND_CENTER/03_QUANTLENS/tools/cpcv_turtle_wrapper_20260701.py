#!/usr/bin/env python3
"""
cpcv_turtle_wrapper_2026-07-01.py

Runs cpcv_validator over results that include the GEN_DONCHIAN_TURTLE variant.
cpcv_validator re-runs signals, so the variant must be patched into mega first.
Applies the variant monkey-patch at module level (workers re-import it too), then
hands off to cpcv_validator.main(). All cpcv_validator CLI args pass through.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import variant_missing_knobs as variant  # noqa: E402
variant.apply()

import cpcv_validator  # noqa: E402  (imports mega; sees the patched build_signals)

if __name__ == "__main__":
    raise SystemExit(cpcv_validator.main())
