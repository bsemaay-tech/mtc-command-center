# ADR-0011 - subprocess environment isolation

Status: Accepted

Context: MCC dependencies can contaminate MTC_v2 backtest execution.

Decision: Future MTC_v2 subprocesses must use configured executables and cleaned environments.

Consequences: No `PYTHONPATH`, `PYTHONHOME`, `VIRTUAL_ENV`, or MCC package bleed.
