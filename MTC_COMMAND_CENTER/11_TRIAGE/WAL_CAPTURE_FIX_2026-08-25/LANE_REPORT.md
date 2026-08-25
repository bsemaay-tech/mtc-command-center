# Lane W report — WAL capture ordering

## Status

**IMPLEMENTATION + GATE 4 SELF-QA COMPLETE; READY FOR LEAD T0 CI/AUDIT.**

Audit tier: **T0**. This report is an implementer handoff, not an accepting Gate 5 verdict.

## Delivered

- `wal_state_bundle.py` now validates a hot WAL's SHM index before SQLite can reconstruct it, then completes a fetched schema read before the capture drift boundary opens.
- Drift detection was not relaxed.
- Tests cover the quiesced Linux-ordering emulation; preconnection refusal of zero/unrelated SHM; a real concurrent SQLite writer; inode replacement; permission-mode change; and SHM mutation.
- D026 makes the old ordering and each disabled safety detector RED; the fixed producer is GREEN.

## Gate 4 evidence

- Focused D026 GREEN: `5 passed in 1.39s`.
- Full `test_wal_state_bundle.py`: `48 passed in 9.23s`.
- `compileall`: rc 0.
- `git diff --check`: rc 0.
- Ruff: unavailable (`No module named ruff`), so no lint PASS is claimed.
- Detailed commands and output: `FIX_EVIDENCE.md`.

## Scope fence

Changed only the two authorized Bridge files and the two new Lane W evidence files. The two CPython-GC defects in `test_order_state.py` are explicitly excluded and untouched. No trading, Pine, parity, MTC, schema, deployment, host, credential, broker, exchange, or economic surface was changed or contacted.

## Required Lead continuation

1. Push the committed candidate branch through the new Ubuntu CI and confirm the formerly cascading WAL tests are green on Linux.
2. Run the two independent T0 auditors required by `AGENTS.md`: `claude-opus-5` xhigh and `gpt-5.6-sol` xhigh.
3. Independently inspect the actual commit diff, reproduce the test evidence, and accept or return a focused repair request within the T0 round cap.
4. Keep the unrelated `test_order_state.py` failures out of any repair prompt for this authorization.
