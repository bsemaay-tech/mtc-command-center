"""
MTC CLI — standard JSON envelope contract.

Every command returns one of these envelopes on stdout.
Exit codes:
  0  — success (envelope.ok = true)
  1  — runtime error (envelope.ok = false, error populated)
  2  — validation failure (envelope.ok = false, findings populated)
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Any

# ---------------------------------------------------------------------------
# Exit codes
# ---------------------------------------------------------------------------
EXIT_OK         = 0
EXIT_ERROR      = 1
EXIT_VALIDATION = 2

# ---------------------------------------------------------------------------
# Envelope
# ---------------------------------------------------------------------------

@dataclass
class Envelope:
    ok: bool
    command: str
    data: dict[str, Any] = field(default_factory=dict)
    findings: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        if d["error"] is None:
            del d["error"]
        return d

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def exit_code(self) -> int:
        if not self.ok:
            return EXIT_VALIDATION if self.findings else EXIT_ERROR
        return EXIT_OK


def emit(envelope: Envelope, as_json: bool = False) -> int:
    """Print envelope and return exit code."""
    if as_json:
        print(envelope.to_json())
    else:
        _print_human(envelope)
    return envelope.exit_code()


def _print_human(e: Envelope) -> None:
    status = "OK" if e.ok else "FAIL"
    print(f"[{e.command}] {status}")
    if e.error:
        print(f"  ERROR: {e.error}")
    for k, v in e.data.items():
        print(f"  {k}: {v}")
    if e.findings:
        print(f"  findings ({len(e.findings)}):")
        for f_ in e.findings:
            sev = f_.get("severity", "?")
            msg = f_.get("message", "")
            print(f"    [{sev}] {msg}")
