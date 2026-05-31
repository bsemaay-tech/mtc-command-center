"""MTC regimes package — deterministic 4H regime labeling."""
from .labeler import RegimeLabeler, DEFAULT_THRESHOLDS, METHOD_VERSION, ALL_LABELS, LABEL_DISPLAY
from .manual_override import ManualOverride

__all__ = [
    "RegimeLabeler",
    "ManualOverride",
    "DEFAULT_THRESHOLDS",
    "METHOD_VERSION",
    "ALL_LABELS",
    "LABEL_DISPLAY",
]
