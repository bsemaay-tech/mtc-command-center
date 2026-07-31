# TS-P0 publication and Day 1 v2 opening — 2026-07-20

Operator: Codex, acting on Barış's explicit 2026-07-20 approval.

## Authorized scope

Barış approved the TS-P0 hash scope, approved
`RELEASE_EVIDENCE_CONTRACT.md`, confirmed the sticky reset policy with the
300-second tolerance, and authorized push plus PR for
`feature/ts-p0-baseline` at exact commit `44338d61`. He also authorized the
monitoring-PC awake policy, exactly one `MTC-Bridge-P2` task start, and exactly
one ARM for Day 1 v2. No merge, deploy, retry, threshold change, or strategy
change was authorized.

## Publication result

- `C:\TSP0` was clean on `feature/ts-p0-baseline` at full SHA
  `44338d61275499f2019011cd06e6f27007f6cbcf`.
- The exact SHA was pushed explicitly to
  `origin/feature/ts-p0-baseline`; remote SHA verification matched.
- Draft PR **#25** opened against `master`:
  <https://github.com/bsemaay-tech/mtc-command-center/pull/25>
- PR head SHA is the exact audited SHA and GitHub reported the PR merge state
  `CLEAN` at creation time.
- Post-publication repo guard on `C:\TSP0` returned `PASS`: clean worktree,
  nothing staged, no protected-scope changes, and no risky untracked files.
  Its only warning was that the local branch has no configured upstream because
  the audited SHA was pushed through an explicit refspec.
- No new commit, merge, or deploy was performed.

## Monitoring-PC awake policy

Active plan: `MONSTER`, GUID `f8a5faa5-0212-46ed-90b3-e34eca76aa5d`.
The required values were already configured and were verified before runtime
start, so no value change was necessary:

| Setting | AC | DC |
| --- | ---: | ---: |
| Idle sleep (`STANDBYIDLE`) | 0 / Never | 0 / Never |
| Hibernate (`HIBERNATEIDLE`) | 0 / Never | 0 / Never |
| Lid-close action (`LIDACTION`) | 0 / Do nothing | 0 / Do nothing |

The machine was on AC (`BatteryStatus=2`, 100%). Scheduler policy remained
`StopIfGoingOnBatteries=False` and `DisallowStartIfOnBatteries=True`.

## Exactly one task start

Pre-start gates:

- `MTC-Bridge-P2` state `Ready`; port 8790 not listening; status API down.
- Task action pointed to
  `C:\P2RT\IBKR_PAPER_BRIDGE\tools\run_bridge_p2.ps1`.
- `C:\P2RT` was clean at `008e065e8e0ffa68f46134da6698d58f91ef2dcb`.

One and only one `Start-ScheduledTask -TaskName MTC-Bridge-P2` call was made at
`2026-07-20T09:03:30.6024628Z` (`12:03:30+03:00`). It succeeded. The task
remained `Running` and started new run **`paper-20260720090332`** in
`paper` / `testnet`, initially `DISARMED`.

## Pre-ARM gate and exactly one ARM

Immediately before ARM:

- state `DISARMED`, `state_version=2`;
- `reconcile_ready=true`, `reconcile_error=null`, `risk_input_error=null`;
- reconcile age approximately 7 seconds;
- raw `/api/positions` body `[]`;
- raw `/api/orders` body `[]`;
- task `Running`; P2RT identity and cleanliness unchanged.

One and only one `POST /api/arm` was sent with `X-Confirm: 2` at
`2026-07-20T09:05:10.1530768Z` (`12:05:10+03:00`). It returned HTTP 200.
Post-state is `ARMED`, `state_version=4`, `paper` / `testnet`, run
`paper-20260720090332`. Event evidence contains exactly one `ARM_REQUEST`
(event 1624) and exactly one `STATE_TRANSITION DISARMED->ARMED` (event 1625).

Post-action evidence:

- task remains `Running`;
- status remains `ARMED`, reconcile fresh and error-free;
- positions `[]`, orders `[]`;
- runtime remains clean at `008e065e`;
- config remains `risk_pct_per_trade=0.005`, `max_daily_loss_pct=0.02`,
  `max_consecutive_losses=3`, leverage/max-leverage `1`.

A final read-only snapshot after documentation handoff work still showed PR #25
OPEN/DRAFT/CLEAN at the exact SHA, task `Running`, run state `ARMED`, a fresh
`2026-07-20T09:13:00Z` reconcile, positions/orders `[]`/`[]`, one ARM request,
one matching state transition, and clean P2RT identity.

## Boundary confirmation

Task-start attempts: **1**. ARM attempts: **1**. Retries: **0**. No merge,
deploy, checkout, threshold/config change, strategy change, live/mainnet action,
DISARM, or scheduler-task definition change occurred. Day 1 v2 continuous-window
time begins at the successful ARM timestamp `2026-07-20T09:05:10Z`.
