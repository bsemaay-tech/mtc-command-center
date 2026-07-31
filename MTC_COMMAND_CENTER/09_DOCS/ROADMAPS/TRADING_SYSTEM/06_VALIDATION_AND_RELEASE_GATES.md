# 06 — Validation and Release Gates

A gate is `PASS` only when every required item has dated evidence tied to one commit/config/data/runtime identity. `UNKNOWN`, missing, stale, waived, or documentation-only evidence is `FAIL`. A later material change invalidates affected evidence.

## Evidence record contract

Every gate record must include: gate, task/release ID, environment, commit and clean-tree proof, config hash, dependency-lock hash, data/fixture identity, database/schema identity when relevant, exact commands, exit codes, summarized raw failures, test counts, reviewer, timestamp/timezone, unresolved risks, rollback target, and explicit PASS/FAIL. External/testnet observations also require run ID, exchange/network, raw non-secret response evidence, and proof of positions/orders when material.

## Gate A — Design approved

Required PASS evidence:

- Governing ADR is Accepted, or the task is explicitly an evidence task for a Proposed ADR and does not implement the unresolved choice.
- Exact scope, expected files, out-of-scope list, dependencies, invariants, tests, failure behavior and rollback are reviewed.
- `git status --short` is captured and unrelated dirty files are protected.
- Protected paths and runtime paths are identified.
- Security review is complete for secrets, network, dependencies, subprocesses, database/schema, API writes or external actions.
- Human policy values are supplied by Barış; an AI does not invent financial thresholds.

Automatic FAIL: vague scope; missing rollback; proposed ADR treated as accepted; task would touch `C:\P2RT` or an external state without separate approval.

## Gate B — Implementation complete

Required PASS evidence:

- Only approved files changed; no unrelated cleanup.
- Code and documentation implement every acceptance criterion.
- Unit/property/contract tests for the task pass.
- Static/import/format checks appropriate to the touched code pass.
- `git diff --check` passes.
- Diff contains no secret or credential material.
- D/M/R records are complete; retired `SESSION_LOG.md` is untouched.
- Status remains `Not deployed` unless a separate external-action gate exists.

Automatic FAIL: untested behavior branch, hidden dependency change, unrelated diff, or protected-path change without approval.

## Gate C — Integration validated

Required PASS evidence:

- Relevant broader suite passes from each supported working directory.
- Failure, restart, reconnect and reconciliation tests applicable to the task pass.
- Idempotency and unknown-state behavior are explicitly exercised for order/reconcile work.
- Stored state remains recoverable and schema compatibility is proven.
- Read-only current-runtime/source checks show no unexpected drift.
- Independent adversarial review is complete for safety-critical work.

Automatic FAIL: only happy-path tests; a retry can occur while state is unknown; foreign exchange state can be mutated automatically; test results are reported from a different commit.

## Gate D — Paper eligible

This gate authorizes eligibility only, not a paper/testnet run. The run still needs explicit approval.

Required PASS evidence:

- Gates A–C pass for the release manifest.
- No unresolved Critical/High safety issue in order, reconcile, risk, persistence, secret or deployment paths.
- Startup is DISARMED; environment/testnet identity and least-privilege credential source are verified without exposing values.
- Full reconcile is fresh and complete; positions/orders/fills/balance/margin differences are zero or explicitly owned/resolved.
- Deterministic duplicate, unknown, partial-fill, restart, reconnect, stale-data, database, kill and alert drills pass at the required tier.
- Kill/disarm behavior and rollback release are verified.
- Audit and monitoring expose mode, commit, config, runtime, data freshness, reconcile freshness, risk state and incident state.
- Paper plan is pre-registered with duration, sample, reset rules, stop rules and owner.

Automatic FAIL: stale reconcile readiness; runtime/repository drift; active unknown order; unexplained divergence; missing rollback; current monitoring window inferred from old evidence.

## Gate E — Limited-live eligible

Current status: **FAIL/BLOCKED**. ADR-0029 is Proposed and `_AI_MEMORY\LIVE_TRADING_GATE.md` is unsigned.

Required PASS evidence, only after the governance documents are accepted:

- Gate D and the complete signed live gate pass for one frozen strategy/release.
- Required pre-registered paper/testnet duration and forward sample are complete with zero unexplained breaks.
- Walk-forward/OOS, benchmark, bootstrap/BH-FDR, DSR, CPCV/PBO where required, multi-window, parameter stability, fee/slippage/funding stress and minimum-sample requirements pass.
- Restart/reconnect/exchange-halt/unknown/partial/kill/database recovery evidence is current.
- Agent wallet/key permissions, no-withdrawal boundary, IP/permission policy, rotation/revoke and outbound/SBOM scans pass.
- Dedicated account, signed capital/exposure/leverage/daily-loss/drawdown limits, owner/on-call path, rollback and post-trade review are approved.
- Barış gives explicit written approval for that release, strategy and capital amount.

Automatic FAIL: short successful testnet run, dashboard green state, model/board consensus, unsigned checklist, stale evidence, or automatic capital increase.

## Gate F — Expansion eligible

Required PASS evidence:

- Gate E evidence remains current and sufficient live evidence exists for the exact expansion.
- Capacity, latency, rate limits, portfolio aggregation, concurrent order identity, database writer load, monitoring and incident ownership are validated.
- Each new symbol, strategy, exchange, platform or capital increase has its own scope, risk analysis, rollback and approval.
- Expansion can be reversed independently without losing audit/state continuity.

Automatic FAIL: bundling multiple new dimensions in one release or using one venue/strategy’s evidence for another.

## Gate-to-phase matrix

| Phase | Required gate before implementation | Required gate before external observation | Required gate before phase exit |
| --- | --- | --- | --- |
| 0 | A | None | B |
| 1 | A | Separate approval for any testnet test | C |
| 2 | A | None by default | C |
| 3 | A | Separate approval for data download/backtest run | C plus canonical QuantLens gates |
| 4 | A–C | D plus explicit testnet/paper approval | D evidence package |
| 5 | A–C | None if read-only/local | C and write-verb denial proof |
| 6 | A–E | Explicit written Barış approval | E; still not automatic start |
| 7 | A–F | Per-expansion approval | F |

## Gate failure protocol

On failure: stop; preserve exact artifacts; do not retry external actions automatically; leave runtime in the lower-risk state; document cause, exposure/state proof, rollback status and new prerequisite task; update memory and run report. A failed gate cannot be renamed “warning” to continue.

