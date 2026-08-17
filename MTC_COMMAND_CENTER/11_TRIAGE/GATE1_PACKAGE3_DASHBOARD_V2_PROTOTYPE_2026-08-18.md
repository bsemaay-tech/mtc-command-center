# Gate-1 Scope Record — Package 3: Dashboard V2 Read-Only Prototype (first increment)

**Date:** 2026-08-18 (overnight) · **Lead:** Claude (Fable) · **Tier: T1** (read-only
mock/fixture UI per accepted backlog §4 Package 3)
**Owner authorization:** 2026-08-17/18 night, in chat: explicit "devam" on the Lead's stated
default path ("dispatch Packages 3, 4, 5a in isolated worktrees using the same chain"), after
Decision 5; full-autonomy instruction reiterated. Recorded here as Decision 6.
**Accepted source:** `BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` §4 Package 3;
kickoff skeleton in `BRIDGE_V2_PACKAGE_KICKOFF_PREP_2026-08-17.md`.

## Frozen scope (first increment)

A standalone, fixture-backed, read-only Dashboard V2 prototype in the NEW directory
`IBKR_PAPER_BRIDGE/dashboard_v2_prototype/` (isolated worktree `C:\P3PROTO`, branch
`feature/bridge-v2-package3`). Contents: one static `index.html` (+ CSS/JS files), fixture JSON
files, and a README. Five required views, all fed exclusively from the bundled fixtures:

1. Aggregate execution overview (multi-worker summary).
2. Per-worker drill-down (identity tuple per accepted P1 pack; health, freshness, block reasons,
   account label).
3. Market Context page (context-only, clearly labeled non-actionable).
4. Desired / accepted / exchange-truth three-layer view (mirroring the accepted P2 state model).
5. Phone-responsive monitoring layout (must work at 375–390 px without horizontal overflow).

**WP-D0 note (per seven-workstream status §3):** the prototype embeds its own explicit
truth/permission statement — every panel names which state layer it displays and that the page
is read-only fixture data with zero authority — serving as the documentation-level
truth/permission contract for this increment; the full WP-D0 contract remains future work.

## Hard boundaries

- New directory only. **Zero modifications to any existing file** — especially
  `IBKR_PAPER_BRIDGE/bridge/static/` (frozen V1 dashboard surface) and anything on the
  prohibition list (VPS/host, credentials, exchange, TESTNET/MAINNET, ARM/orders,
  Pine/MTC/parity).
- No network calls of any kind: no fetch/XHR/WebSocket to live endpoints; fixtures load as local
  files/inline data. No ARM/order/config/credential controls — not even disabled mock buttons
  for economic actions.
- No server, no build step, no new dependencies.

## Roles, review, acceptance

- Implementer: GLM-5.3 (sub-delegation). Official T1-slot review under tonight's roster
  substitution (Codex exhausted; recorded honestly): DeepSeek `deepseek-v4-pro` review +
  Gemini read-only cross-check + Lead (Claude Fable) inspection with executed local checks
  (fixture JSON validation, JS syntax check, no-live-network grep, responsive/static sanity).
- Done means: five views render from fixtures, boundaries above verified by the Lead's own
  executed checks, review findings resolved, committed on the package branch.
