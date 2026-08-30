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
