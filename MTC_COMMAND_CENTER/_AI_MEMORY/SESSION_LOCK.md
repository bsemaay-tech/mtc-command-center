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
| RP6-P0 block | `11_TRIAGE/WPI_BLOCKS_DRAFT/` RP6* | **UNCLAIMED** — released 2026-08-12 20:45 | — |
| RP7-WPI-RO block | `11_TRIAGE/WPI_BLOCKS_DRAFT/` RP7* | **Codex Lead `019fe77c`** — preserved partial repair; serialized writer only | 2026-08-14 10:30 +03 |
| Transport set | `11_TRIAGE/WPI_BLOCKS_DRAFT/` transport/run_p0/run_ro/remote_* | **UNCLAIMED** — released 2026-08-12 20:45 | — |
| §10.2 prover / SEC102 | `11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/` SEC102*, pathscope* | **Codex Lead `019fe77c`** — final owner-authorized Pathscope cycle | 2026-08-14 10:30 +03 |
| Successor prereg draft | `11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/` WPI_*PREREG* | **UNCLAIMED** — released 2026-08-12 20:45 | — |
| Audit-2 readiness package | `11_TRIAGE/AUDIT2_READINESS_PACKAGE/` | **Codex Lead `019fe77c`** — documentation and freeze preparation only | 2026-08-14 10:30 +03 |
| Shared memory layer | `_AI_MEMORY/` handoffs, rules, routing | **UNCLAIMED** — released 2026-08-16 21:39 +03 | — |
| Gemini adviser route | `11_TRIAGE/GEMINI_PRO_*` plus external launcher/project config | **UNCLAIMED** — released 2026-08-16 21:39 +03 | — |
| Backend/Dashboard V2 design record | `IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md` | **UNCLAIMED** — released 2026-08-16 20:59 +03 | — |
| Bridge Help / System Map | `IBKR_PAPER_BRIDGE/bridge/static/` Help-only UI, `IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py`, and Help/Wiki reference docs | **UNCLAIMED** — released capacity-blocked 2026-08-16 21:45 +03 | — |

**All rows released 2026-08-12 20:45** by the Fable session "sabaha kadar çalışma planı" at its
clean stop (Gate 7). Everything it produced is committed and pushed through `d4a07438`. **The
next session should claim the rows it intends to write before its first write** — and note that
tonight's four Claude Pro audit lanes are READ-ONLY on the block workstreams (each writes only
its own verdict file), so they do not require ownership of RP6/RP7/transport/pathscope.

Workstreams not listed: add a row before writing.

## Log

- **2026-08-16 21:39 +03:** Codex Lead `01a00ad1` released the Gemini and shared-memory
  rows after the isolated coder pilot passed. The separate launcher allows only explicitly
  named unprotected files in `C:\GEMINI`; its one-file live edit passed, Codex reviewed it,
  the temporary file was removed, and the worktree is clean. The requested Help/System Map
  drawings and SQLite+WAL black-box/logbook sentence was added to `NEXT_STEPS.md`; no Help or
  dashboard implementation file was touched.

- **2026-08-16 21:30 +03:** Owner authorized a separate Gemini CLI coder route without a
  long audit cycle. Codex Lead `01a00ad1` claimed the Gemini and shared-memory rows for a
  dedicated isolated worktree, explicit file scope, one harmless live edit, Codex review,
  and concise handoff. The existing read-only route remains unchanged; protected trading,
  credentials, deployment, commit, push, and merge remain excluded.

- **2026-08-16 21:45 +03:** Codex Lead `01a00921` released the Help/Wiki and
  shared-memory rows after recording the clean counterpart-capacity blocker.
  Gate 1 and the exact prompt are committed; no dashboard source was partially
  edited. Resume after the exact Claude capacity reset.

- **2026-08-16 21:40 +03:** Codex Lead `01a00921` claimed the shared-memory
  row only to record the clean Help/Wiki capacity blocker and immediate resume
  instruction. No product or protected runtime surface is writable under this
  claim.

- **2026-08-16 21:30 +03:** Codex Lead `01a00921` claimed the new Bridge Help /
  System Map workstream for the owner-requested interactive, explanatory Wiki.
  Scope is static Help UI, its tests, and a shared AI-readable knowledge source.
  Trading logic, strategy/risk/order behavior, APIs, configuration, deployment,
  credentials, hosts, and economic actions remain excluded.

- **2026-08-16 20:59 +03:** Codex Lead `01a00921` released the design-record
  and shared-memory rows after A11, A12, the change log, source links, and Gate-7
  handoff were complete. Fresh read-only T2 `gpt-5.6-sol` medium review returned
  PASS with no findings or nits. No implementation or live surface changed.

- **2026-08-16 20:58 +03:** Codex Lead `01a00921` claimed the shared-memory row
  only for the required final handoff and next-step record for the accepted A11
  documentation change. No source, configuration, host, deployment, or trading
  surface is writable under this claim.

- **2026-08-16 20:44 +03:** Codex Lead `01a00921` reclaimed only the
  Backend/Dashboard V2 design-record row for the owner-requested documentation
  of MTC_V2 versus Bridge order/exit lifecycle ownership. No implementation,
  configuration, host, deployment, broker, trading, or economic surface is writable.

- **2026-08-16 20:31 +03:** Codex Lead `01a00921` released the
  Backend/Dashboard V2 design-record row after the owner-requested B7 sourcing
  decision was added and a fresh read-only T2 review returned PASS. No code,
  configuration, credential, host, deployment, trading, or economic surface changed.

- **2026-08-16 20:22 +03:** Codex Lead `01a00921` claimed only the
  Backend/Dashboard V2 design record for the owner-requested documentation of
  Dashboard Codex-subscription use versus VPS LLM-gate API use. No implementation,
  configuration, credential, host, deployment, trading, or economic surface is writable.

- **2026-08-16 20:20 +03:** Codex Lead `01a00ad1` released the shared-memory and Gemini
  adviser rows at the owner's requested safe stop. Gemini CLI 1.1.13 is installed and the
  pinned read-only helper preflight passes for `gemini-3.7-flash-high`; the overlong final
  independent audit was interrupted at owner direction, so no final dual-flagship acceptance
  is claimed and coding access remains disabled.

- **2026-08-16 18:55 +03:** Owner authorized a new bounded cycle to make Gemini a safe
  read-only repo adviser now; coding access remains future-only and disabled. Codex Lead
  `01a00ad1` reclaimed only the shared-memory row for hardening, QA, and acceptance records.

- **2026-08-16 18:33 +03:** Codex Lead `01a00ad1` released the shared-memory row. The
  Gemini route is installed and live probes pass, but final T0 Codex round 3 returned
  `REQUEST_CHANGES`, exhausting the three-round cap. Claude acceptance was not run and
  the route remains not repo-ready pending explicit owner direction.

- **2026-08-16 17:23 +03:** Owner explicitly directed Codex to perform the implementation
  instead of waiting for Claude. Codex Lead `01a00ad1` reclaimed only the shared-memory
  row for that narrow override; independent T0 acceptance requirements remain unchanged.

- **2026-08-16 17:16 +03:** Codex Lead `01a00ad1` released the shared-memory row.
  Google AI Pro authentication and the external synthetic probes succeeded, but the
  required Claude Opus counterpart hit its session limit before Gate 2 and resets at
  18:10 Europe/Chisinau. No helper, Antigravity project config, Toolbox row, routing
  index, trading source, or protected surface was changed.

- **2026-08-16 17:09 +03:** Codex Lead `01a00ad1` claimed only the shared-memory row
  for the owner-requested Google AI Pro / Gemini 3.7 Flash read-only CLI route. Scope is
  local routing metadata and handoff only; no trading, Pine, parity, MTC, Bridge, host,
  deployment, broker, credential-value, or economic surface is writable.

- **2026-08-16 09:53 +03:** Codex Lead claimed only the shared-memory row to register
  the owner-requested AI-memory continuity audit/repair task, committed the task and
  handoff at `3996e810`, and released the row. No other workstream was touched.

- **2026-08-14 10:30 +03:** Codex Lead `019fe77c` claimed RP7, Pathscope, and
  Audit-2 readiness. The existing uncommitted `RP7-WPI-RO.sh` edit is the
  preserved partial from this same Lead's quota-interrupted Claude repair lane;
  it will not be reset, stashed, overwritten, or exposed to a second writer.
  Pathscope and RP7 writers will be serialized.

- **2026-08-13 ~09:00: all rows remain UNCLAIMED — released** by the Fable overnight session
  (2026-08-12 20:50 → 2026-08-13 09:00). Honest note: that session wrote to RP6/RP7/transport/
  pathscope/prereg/Audit-2 workstreams via dispatched lanes without first claiming rows (it was
  the only active Lead; no collision occurred — the RP7 auditor detected the Lead's own
  concurrent commits and attributed them correctly). Everything committed and pushed through
  the rows-1-9 r3 repair. In-flight at release: the Lead's verbatim r19/r17 RP6 fence runs
  (results go to the next session; see FRESH_SESSION_HANDOFF_2026-08-13_MORNING.md §7 tail).

- 2026-08-11: file rewritten from stub to ownership mechanism after the 2026-08-10
  transport collision (two sessions writing the same artifact family; detected, work
  dropped by one session, no data lost — see the concurrent-session notice).
- **2026-08-12 20:45: all rows RELEASED** by the Fable session "sabaha kadar çalışma planı" at
  its clean stop. That session held every WP-I row for the 2026-08-12 day run (~11 hours,
  ~45 commits). No foreign uncommitted edits were found in any owned workstream at release.
  One process note worth carrying: **two dispatched lanes independently refused Lead
  instructions that would have overwritten a prior lane's committed record** — once on the
  D026 recheck file, once on a GLM verdict path. Both surfaced instead of overwriting. That is
  the ownership discipline working, and it argues for keeping the "write exactly one NEW file"
  convention rather than naming existing paths in kickoffs.
- 2026-08-11 14:15: Fable overnight Lead `7e05aabf` (session "Sabaha kadar otonom çalışma
  planı" successor) claimed all five WP-I rows. Verified via session listing that the rule
  author ("Codex gece çalışması değerlendirmesi" session) committed `15d48088` at 13:46:53
  as its final act and is no longer running — exactly one active Lead loop exists.
