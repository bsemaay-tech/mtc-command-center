# Pathscope cap-override Lead finding - pre-freeze self-QA

Date: 2026-08-13
State: `REPAIR-INCOMPLETE-NOT-COMMITTED-NOT-AUDITED`

The first Claude Opus 5 repair process exited after changing the prover,
self-QA and status, but before creating its required repair report. The Lead did
not freeze or accept that delta.

## Required in-cycle repair

The new `record_assignment_value` implementation splits an already-rendered,
quote-aware assignment value with Python `str.split()`. That loses the fact that
a blank was inside a quoted single pathname.

Executed counterexample:

```bash
X="$ROOT dir/escape" cat "$ROOT/f"
```

with `ROOT=/safe`, `PWD=/safe`, and allowlist `/safe/**`.

- pre-repair round-3 bytes: rc 1, one FORBID row for the actual pathname
  `/safe dir/escape`;
- current uncommitted repair: rc 0, incorrectly records `/safe` and
  `/safe/dir/escape` as separate ALLOW-LEXICAL paths.

This is a reproduced false PASS. Repair the member grammar without splitting a
quoted pathname into independent values. Preserve support for whitespace-
separated command text and colon-separated path lists without silently treating
ambiguous grammar as safe; ambiguity may emit a specific fail-closed coverage
record. Add literal D026 RED/GREEN for this exact case and benign controls.

## Evidence mismatch to correct

The extracted published harness completed, but its generated behavioral-diff
digest was:

`b2c647c020d702381450709a72ee347905c3f5f44e23d7020a1965b319b8623d`

The edited self-QA currently records:

`1ea81787c4f9c639aa0f7aa6e5f274c4375d120be3095cee9bdaf3a86efdecbc`

Re-run the complete harness after repair and make every embedded identity,
count, transcript, and digest reproduce exactly. Create the originally required
`PATHSCOPE_CAP_OVERRIDE_REPAIR_REPORT_2026-08-13.md`. Do not claim acceptance.
