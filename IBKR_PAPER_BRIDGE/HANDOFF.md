# Bridge handoff

## Current state — 2026-08-30

- W72 focused repair ran in worktree `C:\WBRIDGE_FC` on branch
  `feature/bridge-fail-closed-20260830`. Code commits are
  `2302bb56735f5d2a8578955a376931ac277b6c85` and
  `bbb13fcb72bf9ea80c8f2942da0e4a974ce6a958`; independent T0 acceptance remains pending.
- W72 write paths are `.gitattributes`, `bridge/config_contract.py`, `bridge/api/routes.py`,
  `bridge/static/app.js`, `docs/31_HELP_SYSTEM_MAP_INDEX.md`, `tests/test_config_contract.py`,
  `tests/test_api.py`, `tests/test_dashboard_static.py`, and this handoff. Live-dependency status:
  none contacted or changed.
- Startup now refuses an absent required V2 leaf as `MISSING_REQUIRED` before app-state or engine
  construction, with only the designed dry-run notional leaf exempted for its internal mode
  override. Nonnumeric schema state retains its specific STOP reason, and both policy-ID leaves
  reject whitespace-only explicit values before construction.
- The dashboard reads the validated risk metadata object's `.value`; absent raw-only coin and
  leverage leaves render unavailable and disabled. The retired `bridge_config` state alias is
  removed, and the AI-facing help index describes only `ValidatedRuntimeSettings.effective_view()`.
- The dashboard's canonical AI-readable Help data remains `bridge/static/help_map.json`; the
  historical `help_map.json retired-KILL-claim correction` marker is retained for the existing
  onboarding/evidence guard.
- The owner-approved shipped config remains 324 bytes and byte-identical to the approved candidate,
  SHA-256 `a96fecd10d6966c3e93a829ec4d75869a0851f0136a06e85ab45c255ee0f5842`; the Git path is now
  marked `-text` and the working/HEAD blob identities agree.
- Local self-QA passed 77 scoped config/API/dashboard tests and the exact routed full Bridge suite:
  1,423 passed, one Starlette/httpx deprecation warning, exit 0. Persistent probes are under
  `C:\tmp\W72_VARIANTS`.
- No push, PR, merge, deployment, host contact, service action, credential access, TESTNET/mainnet
  action, ARM, order, broker/exchange endpoint, or live action occurred.
- Durable repair report: `C:\tmp\LANE_PROMPTS_20260828\W72_REPAIR_REPORT.md`.

## [Claude lane F] 2026-09-07 — import-only lint repair and Linux test note

- `bridge/broker/hyperliquid.py` line ~1644 annotates `rich_rows: dict[str, dict[str, Any]]`
  but `Any` was never imported. Fixed with one added import line,
  `from typing import Any`, in the existing `typing` import group. No other line in the
  file changed.
- Evidence: `ruff check --select F821` on the pre-fix blob reports
  `F821 Undefined name \`Any\`` at line 1643; the same check on the fixed file reports
  "All checks passed!".
- `TESTS.md` gained one short paragraph noting that on Linux the suite must run as a
  non-root user (root's `fchown()` on `-wal`/`-shm` files during a read-only open trips
  the capture drift guard in `tools/wal_state_bundle.py` and fails three
  `test_wal_state_bundle.py` tests; GitHub CI's non-root runner is unaffected), plus one
  sentence that a root-owned checkout needs `git config safe.directory` for the non-root
  user or `test_linux_deployment`'s fresh-checkout test cannot run `git show`. No existing
  sentence was changed.
- Full suite re-run as non-root (uid 65534, matching the CI condition): 1,393 passed,
  exit 0. `python -m compileall -q IBKR_PAPER_BRIDGE` and `git diff --check` both clean.
- No behavior change; T0 audit still required before acceptance.
- NEXT ACTION: owner/T0 reviewer signs off on the import-only diff and the Linux non-root
  test note; no further lane F action pending.
- WAITING FOR OWNER: Nothing.
