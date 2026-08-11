# SESSION_LOCK — workstream write ownership

Rewritten 2026-08-11. The old file was a single unused "Status: unlocked" line; it did not
prevent the 2026-08-10 concurrent-session collision on the transport set
(`11_TRIAGE/WPI_BLOCKS_DRAFT/CONCURRENT_SESSION_NOTICE_2026-08-10_2130.md`). This version
is the mechanism behind `AI_RULES.md` § Autonomous Session Invariants, rule 2.

## Protocol

1. **Before the first write** to any file belonging to a workstream below, set yourself as
   OWNER on that row (session label + local timestamp) and commit the change with your
   first substantive commit.
2. **One writable owner per workstream.** Everyone else is read-only on that workstream's
   files. Auditing (read-only review, reports written to your OWN workstream row or a new
   file) is always allowed.
3. **Release at handoff**: set the row back to UNCLAIMED in your final memory write-back
   (Gate 7).
4. **Stale locks:** a row older than 24h with no commits touching that workstream may be
   taken over — record the takeover with a dated note in the Log section.
5. **On finding a foreign uncommitted edit** in a workstream you own: stop writing there,
   preserve the edit (commit it labelled as foreign/partial), write a dated notice, ask the
   owner (Barış) which session should own the row. Never revert or overwrite it silently.

## Ownership table

| Workstream | Files (primary home) | Owner | Since |
|---|---|---|---|
| RP6-P0 block | `11_TRIAGE/WPI_BLOCKS_DRAFT/` RP6* | UNCLAIMED | — |
| RP7-WPI-RO block | `11_TRIAGE/WPI_BLOCKS_DRAFT/` RP7* | UNCLAIMED | — |
| Transport set | `11_TRIAGE/WPI_BLOCKS_DRAFT/` transport/run_p0/run_ro/remote_* | UNCLAIMED | — |
| §10.2 prover / SEC102 | `11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/` SEC102*, pathscope* | UNCLAIMED | — |
| Successor prereg draft | `11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/` WPI_*PREREG* | UNCLAIMED | — |
| Shared memory layer | `_AI_MEMORY/` handoffs, rules, routing | UNCLAIMED | — |

Workstreams not listed: add a row before writing.

## Log

- 2026-08-11: file rewritten from stub to ownership mechanism after the 2026-08-10
  transport collision (two sessions writing the same artifact family; detected, work
  dropped by one session, no data lost — see the concurrent-session notice).
