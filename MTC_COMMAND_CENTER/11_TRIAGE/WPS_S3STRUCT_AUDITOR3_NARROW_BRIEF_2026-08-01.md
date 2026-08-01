# S3-STRUCT — AUDITOR 3 (DeepSeek V4 Flash) NARROW BRIEF

> **Deliberately narrow.** Auditor 3 timed out twice last cycle — at 15 minutes and again at 50 —
> on a brief that asked for a full-diff review *plus* an exhaustive exception-path enumeration *plus*
> a two-minute suite run. The diagnosis was scope, not capability. This brief asks **one** question
> and gives the round delta only. The flagships carry the exhaustive enumeration.

## Your task

Routine internal review of our own trading-support service. You are reviewing **one** change to a
database read path in a Python service.

Read this diff and nothing else:

```
git diff 732b37c3..34d35286 -- IBKR_PAPER_BRIDGE/bridge/engine/orders.py
```

Do not run the test suite. Do not write any script. Do not edit any file.

## The single question

The change introduces a validation boundary. Reads of durable database rows now go through a typed
accessor that raises `DurableRowFault` instead of returning a raw value. Callers are expected to
either contain that fault or never see it.

**Find every place in this diff where a `DurableRowFault` can be raised but is not caught.**

Two specific shapes to look for, because they are easy to miss:

1. **`.get()` on a validated row.** `ValidatedDurableRow` subclasses `collections.abc.Mapping`.
   `Mapping.get()` calls `__getitem__` and catches only `KeyError`, so `row.get("col")` raises
   `DurableRowFault` just like `row["col"]` does. Any `if x is None: return` guard written for the
   old raw-read behaviour no longer catches the case it was written for.
2. **A call site that used to be total.** Where the old code returned `None` or substituted `0.0`
   for a missing value, the new code may raise instead. If that call site has no handler, the change
   introduced a new failure where none existed.

## Output — keep it short

```
UNCAUGHT SITES:
  <file>:<line>  <the expression>  <which function it is in>  <who calls that function>
  ... (or: none found)

CONFIDENCE: <high | medium | low>, and what you could not check
```

If you cannot complete this, say so plainly rather than guessing. A partial answer that names two
real sites is worth more than a complete-looking answer that names none.

**Note on your verdict:** you are not being asked for a PASS/BLOCK verdict this round, because you
are not running the suite. Under `AGENTS.md` D025 rule 1 an auditor that cannot execute the suite
cannot return an accepting verdict, so your output is recorded as **supplemental detection** — real
findings from it still bind once the Lead reproduces them on real source.
