# CODEX GO — P2 Task 5 Deploy + Re-ARM (Day 0 v4) + Task 6 PR Merges (2026-07-15)

Author: Claude Fable 5 (auditor). Executor: Codex GPT-5 (builder).
**Barış GO recorded 2026-07-15: "deploy et" — this is the fresh post-incident ARM authorization
for exactly one ARM.** Fable audited the outage-tolerance fix on real code + runs: PASS
(GLOBAL_HANDOFF `[Claude Fable 5] 2026-07-15 — OUTAGE-TOLERANCE FIX AUDIT: PASS`).

Executes **Task 5 + Task 6** of `11_TRIAGE/CODEX_P2_OUTAGE_TOLERANCE_PROMPT_2026-07-15.md`.
Read that file's Task 5/6 for the full step list; this file adds the deploy-specific facts,
the approved commit, and the framing. On conflict, THIS file wins.

## DEPLOY TARGET (frozen)

- Detach `C:\P2RT` to **`feature/ibkr-bridge-final` tip `1465f8f0`**. Verified: `1465f8f0` is
  code-identical to the audited `0e644b52` (only docs added on top). The deployed fix
  legitimately updates `config/bridge.yaml` (`broker.reconnect_attempts: 9`,
  `risk.reconcile_max_consecutive_failures: 3`) — that IS the approved change, not a frozen-config
  violation.

## PRE-DEPLOY STATE (Fable-verified 2026-07-15, ~4h before this go)

- **The P2 bridge PROCESS is already DOWN**: zero `bridge.app` processes, nothing on :8790,
  Task-Scheduler `MTC-Bridge-P2` = Ready (supervisor exited ~09:57Z). Store DB
  `app_state = DISARMED`, last event `09:57:30Z`. No safety impact — DISARMED, flat, funds safe.
- This SIMPLIFIES the deploy: the "stop child" step is effectively done. But FIRST re-verify a
  clean slate so two bridges never fight over :8790.

## HARD RAILS (unchanged, safety-critical)

1. TESTNET only. `HL_LIVE_ACK` stays unset. `network: testnet` unchanged. Mainnet forbidden.
2. **Exactly ONE ARM.** More than one `DISARMED->ARMED` transition = STOP, abort, report.
3. `C:\P2RT` is a LINKED WORKTREE → detached-HEAD doctrine: `git -C C:/P2RT checkout --detach
   1465f8f0`. NEVER check out the branch there; never `--ignore-other-worktrees` on it.
4. Never print `HL_API_WALLET_KEY`; secret grep `[0-9a-fA-F]{64,}` = 0 on any staged diff.
5. Inline commits on `feature/ibkr-bridge-final` (hook flips HEAD): one command
   `git checkout … && git add <paths> && git commit`.
6. `PYTHONUTF8=1`; both P2RT CWDs green (expect 130 passed) BEFORE the ARM.
7. Do not change any frozen P2 config beyond what commit `1465f8f0` already contains.

## STEP SEQUENCE

1. **Clean-slate check:** confirm zero `bridge.app` and zero orphan `run_bridge_p2` processes,
   nothing bound on :8790. Kill any orphan you find (record PID). If a bridge is unexpectedly
   alive and serving, STOP and report instead of double-starting.
2. **Detach runtime:** `git -C C:/P2RT checkout --detach 1465f8f0`; verify
   `git -C C:/P2RT diff 1465f8f0 --stat` empty and `git -C C:/P2RT status` clean.
3. **Suites in P2RT** from BOTH CWDs (`PYTHONUTF8=1`): repo root + `IBKR_PAPER_BRIDGE/`.
   Expect `130 passed`. Any failure → STOP, do not start the runtime.
4. **Start supervisor:** relaunch `MTC-Bridge-P2` (Task Scheduler `Start-ScheduledTask` or run
   `tools/run_bridge_p2.ps1` exactly as the C2 design specifies — state which). New run id,
   DISARMED. Confirm :8790 serving and `git`-pinned identity = detached `1465f8f0`.
5. **Reconcile-empty check:** GET `/api/positions` + `/api/orders` = `[]`/`[]`; `/api/status`
   `reconcile_ready=true`, `reconcile_error=null`.
6. **≥10-minute DISARMED observation gate (all required before ARM):**
   - at least one full `DISCONNECT -> RECONNECT attempt=1 -> DATA_RESTORED` cycle;
   - **verify FRESH BARS actually flow** — a new `/api/bars` timestamp in the live BTC range
     (this explicitly clears the incident-#2 "no DATA_RESTORED after recovery" concern; do NOT
     ARM on a stale feed);
   - at least two clean periodic reconciles, no `RECONCILE_FAILED`;
   - notify-threshold visibly working: routine DISCONNECT/RECONNECT-attempt1/DATA_RESTORED do
     NOT hit Telegram (bonus live check of the new behavior). If a real HL outage happens to hit
     during observation, `RECONCILE_FAILED_TOLERATED` (WARN, no disarm) for strikes 1-2 is the
     CORRECT new behavior — do not treat it as failure.
7. **ARM once:** POST `/api/arm` with the `X-Confirm` header. Verify exactly one `ARM_REQUEST`
   + one `DISARMED->ARMED`; record the **Day 0 v4** timestamp. Post-ARM: two clean reconciles,
   positions/orders still `[]`/`[]`.
8. **Record + commit:** update `docs/03_STATUS.md` (Day 0 v4, tip `1465f8f0`, 130 tests,
   outage-tolerance note), `GLOBAL_HANDOFF.md` (dated), `NEXT_STEPS.md`. Inline-commit on
   `feature/ibkr-bridge-final`, secret grep first. **Push** `feature/ibkr-bridge-final`
   (updates PR #16 — this push IS authorized by this go).

## VALIDATION-TIER FRAMING (do not misread later)

Day 0 v4 is **policy VALIDATION**, not the definitive D3. Per Barış's PC schedule (ON→Jul 18
~2h off→ON→Jul 20 ~2h off→6d→pattern; VPS end of month), no pre-VPS window reaches ≥10
uninterrupted days. The **Jul 18 planned PC-off will reset Day 0 v4 — that is expected, a window
boundary, NOT a safety incident.** Its purpose: prove the outage-tolerance fix survives a real
HL outage (≈daily) before the VPS runs the true D3. Record planned PC-offs distinctly from
safety DISARMs.

## TASK 6 — Merge PRs #16 → #17 → #18 → #19 (after the deploy commit/push)

Barış-approved. Per Task 6 of the outage-tolerance prompt:
- Order `#16 (bridge, now incl. outage fix + Day 0 v4) → #17 (UI) → #18 (faz3b prereg) →
  #19 (donchian)`.
- `#16` clean vs master. `#17/#18/#19` conflict only on `GLOBAL_HANDOFF.md` / `NEXT_STEPS.md` →
  resolve **UNION** (keep every dated section, drop nothing). Any OTHER conflicting file → STOP,
  report.
- Never force-push, never rewrite master history. After all four land, run the bridge suites
  once on master (both CWDs, still 130), report the final master tip and that each PR shows
  merged.

## STOP CONDITIONS (any → abort, leave DISARMED, preserve evidence, report)

Suite failure; unexplained ERROR event; more than one ARM transition; any position/order
appears; no fresh bars within the observation gate; :8790 not serving; pinned identity ≠
detached `1465f8f0`; a Task-6 conflict outside the two handoff files.

## DELIVERABLE → STOP for Fable post-ARM audit

Report `11_TRIAGE/P2_DAY0_V4_DEPLOY_REPORT_2026-07-15.md`: every command + pasted output, the
Day 0 v4 timestamp, the fresh-bar proof, both suite tails, ARM evidence, secret-grep results,
Task-6 merge log + final master tip. Then STOP — Fable audits the live runtime + master before
anything else.
