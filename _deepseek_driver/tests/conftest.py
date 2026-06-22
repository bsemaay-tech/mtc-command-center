"""Make the _deepseek_driver modules importable from tests without packaging."""
import sys
from pathlib import Path

_DRIVER_DIR = Path(__file__).resolve().parent.parent
if str(_DRIVER_DIR) not in sys.path:
    sys.path.insert(0, str(_DRIVER_DIR))
