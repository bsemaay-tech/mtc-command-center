# Lane W repair-2 report — WAL capture ordering

## Status

**REPAIR ROUND 2 IMPLEMENTATION + GATE 4 SELF-QA COMPLETE; READY FOR CLAUDE LEAD T0 CI/AUDIT.**

Audit tier: **T0**, round 2 of maximum 3. This report is an implementer handoff, not an accepting Gate 5 verdict.

## Delivered

- The source boundary is now embedded inside `_connect_readonly` immediately after the fetched schema read, eliminating the old caller-visible initialization gap.
- Existing SHM identity remains guarded across initialization; mode, inode, presence, and exact-size changes cannot enter an exempt class.
- After the boundary, only existing-SHM content hash plus consequent timestamp movement is tolerated, and only with stable SHM identity/mode/size/presence and byte-and-metadata-identical DB/WAL.
- Empty WAL materialization is tolerated only for a stable zero-byte regular file at the source DB's mode; wrong mode or later metadata movement is drift.
- The tool docstring states the exact files, boundaries, and surviving SQLite self-effects.
- Attack tests cover the auditor's real SHM `0666 -> 0444` flip, SHM inode swap, size change, deletion, deletion/recreation, and empty-WAL wrong-mode metadata drift.
- D026 retains all original five RED mutants and adds RED proof for every repair-2 attack class.

## Gate 4 evidence

- Inherited producer: exact real SHM mode-flip test RED (`assert 0 == 2`).
- Original five TEMP mutants: all RED.
- Repair-2 attack TEMP mutants: SHM mode, inode, size, presence/recreation, and empty-WAL metadata all RED.
- Focused repository GREEN: `11 passed in 1.76s`.
- Full `test_wal_state_bundle.py`: `54 passed in 6.24s`.
- `compileall`: rc 0.
- Exact mutant diffs, identities, commands, real output, prior Linux CI rider, and full attack matrix: `FIX_EVIDENCE.md`.

## Scope fence

Exactly four files are changed: the capture tool, its test file, `FIX_EVIDENCE.md`, and this report. No push occurred. No trading, Pine, parity, MTC, schema, deployment, host, credential, broker, exchange, or economic action occurred.

## Required Lead continuation

1. Independently inspect this repair commit and reproduce the scoped QA.
2. Push only if authorized, run fresh Ubuntu CI on the repair SHA, and verify the complete result.
3. Run the required independent T0 `claude-opus-5` xhigh and `gpt-5.6-sol` xhigh reviews.
4. Accept or send a focused repair within the T0 three-round cap; keep the two excluded `test_order_state.py` CPython-GC failures out of this scope.
