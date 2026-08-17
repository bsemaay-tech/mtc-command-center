# Dispatch prompt — Bridge V2 slim runtime dependency identity verification

## Status and authority boundary

This is a dispatch artifact only. It does not authorize a review run, accept the
inventory, authorize implementation, or change any release identity.

When separately authorized, run this prompt in **one fresh exact flagship
session at high effort**:

- exact model: `claude-opus-5`;
- effort: `high`;
- fresh independent session; never resume/continue an implementation or prior
  audit session;
- no fallback, alias, substitution, or silent downgrade. If the exact
  model/effort is unavailable, return `BLOCK`.

## Audit classification

**Single-flagship T1 identity verification under the AGENTS.md T2 identity
escalation rule.** The underlying inventory is documentation/evidence, but the
specific 42-member and byte-count findings can affect a future deployed-artifact
identity. Verify only those identity-affecting findings and their direct source
closure. This is not a general second T2 documentation round and does not reset
or expand any other audit cap.

## Repository and frozen inputs

Repository:

```text
C:\LAB\Tradingview_LAB_CLEAN
```

Candidate report to verify:

```text
MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_SLIM_RUNTIME_DEPENDENCY_INVENTORY_2026-08-17.md
```

Frozen source commit:

```text
d41af2bad234b3ac9c84eebef0714b0da9111ab9
```

Supporting committed reports (read through the named Git objects; do not assume
they are present in the current checkout):

```text
5ec891e3:MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_PACKAGE_SIZE_INVENTORY_2026-08-17.md
2cee2186:MTC_COMMAND_CENTER/11_TRIAGE/V2_SLIM_PACKAGE_SCOPE_CONTRACT_DRAFT_2026-08-17.md
```

Applicable authority:

```text
AGENTS.md
MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md
```

The working-copy file below is dirty foreign work and is not an input:

```text
IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md
```

Do not derive, repair, or corroborate any finding from its working-copy bytes.

## Exact 42-path candidate ledger to reproduce

Independently prove that the following ledger contains 42 unique paths and that
the blobs at the frozen SHA total exactly 1,206,442 bytes:

```text
IBKR_PAPER_BRIDGE/bridge/__init__.py
IBKR_PAPER_BRIDGE/bridge/api/__init__.py
IBKR_PAPER_BRIDGE/bridge/api/routes.py
IBKR_PAPER_BRIDGE/bridge/api/ws.py
IBKR_PAPER_BRIDGE/bridge/app.py
IBKR_PAPER_BRIDGE/bridge/broker/__init__.py
IBKR_PAPER_BRIDGE/bridge/broker/base.py
IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py
IBKR_PAPER_BRIDGE/bridge/broker/mock.py
IBKR_PAPER_BRIDGE/bridge/engine/__init__.py
IBKR_PAPER_BRIDGE/bridge/engine/bars.py
IBKR_PAPER_BRIDGE/bridge/engine/engine.py
IBKR_PAPER_BRIDGE/bridge/engine/llm_gate.py
IBKR_PAPER_BRIDGE/bridge/engine/notify.py
IBKR_PAPER_BRIDGE/bridge/engine/orders.py
IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py
IBKR_PAPER_BRIDGE/bridge/engine/risk.py
IBKR_PAPER_BRIDGE/bridge/engine/strategies/__init__.py
IBKR_PAPER_BRIDGE/bridge/engine/strategies/keltner_trail_ema8.py
IBKR_PAPER_BRIDGE/bridge/engine/strategy_base.py
IBKR_PAPER_BRIDGE/bridge/engine/types.py
IBKR_PAPER_BRIDGE/bridge/engine/window.py
IBKR_PAPER_BRIDGE/bridge/settings.py
IBKR_PAPER_BRIDGE/bridge/static/app.css
IBKR_PAPER_BRIDGE/bridge/static/app.js
IBKR_PAPER_BRIDGE/bridge/static/index.html
IBKR_PAPER_BRIDGE/bridge/store/__init__.py
IBKR_PAPER_BRIDGE/bridge/store/db.py
IBKR_PAPER_BRIDGE/config/bridge.yaml
IBKR_PAPER_BRIDGE/config/strategies/keltner_trail_ema8.yaml
IBKR_PAPER_BRIDGE/tests/fixtures/BTC_1h.csv
IBKR_PAPER_BRIDGE/requirements.lock
IBKR_PAPER_BRIDGE/deploy/linux/README.md
IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template
IBKR_PAPER_BRIDGE/deploy/linux/install.sh
IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh
IBKR_PAPER_BRIDGE/deploy/linux/logrotate/mtc-bridge
IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh
IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template
IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-steady.service.template
IBKR_PAPER_BRIDGE/deploy/linux/verify.sh
IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py
```

Do not accept the report's arithmetic. Reproduce sizes from committed Git
objects at the full frozen SHA, preferably with `git ls-tree -r -l` or equivalent
read-only Git plumbing. Prove path uniqueness separately. Do not use physical
working-tree file sizes.

## Required independent reproduction

### 1. Frozen identity

- prove the full 40-hex commit object exists locally;
- report whether it is the current `HEAD`, but do not require that it be `HEAD`;
- use `<frozen-SHA>:<path>` or exact-SHA Git plumbing for all source conclusions;
- inspect `git status --porcelain` only to identify dirty/untracked boundaries;
  do not treat a dirty tree as source evidence.

### 2. Candidate ledger and committed byte total

- prove all 42 paths exist as blobs at the frozen SHA;
- prove there are exactly 42 unique paths with no duplicate, missing, outside,
  tree, symlink, or gitlink member;
- reproduce exactly 1,206,442 committed source bytes;
- reconcile the grouped totals stated by the candidate report: 28 Bridge files
  / 875,705 bytes; 3 config/dry-run files / 144,630 bytes; 1 lock / 117,762
  bytes; 10 Linux operations files / 68,345 bytes.

### 3. Direct runtime closure

Using source at the frozen SHA, independently trace and cite:

- `bridge.app` imports and the transitively imported Bridge packages needed for
  normal startup;
- `bridge/engine/engine.py` dependencies on bars, LLM-null gate, notifier,
  orders, reconciler, risk, strategy, types, window, and store;
- Hyperliquid and mock broker modules;
- embedded SQLite schema/migrations in `bridge/store/db.py`, with no separate
  runtime schema directory claimed;
- static mounting and `index.html`/CSS/JS dependency;
- reads of `config/bridge.yaml` by app/API startup;
- the documented application `--dry-run` branch reading exactly
  `tests/fixtures/BTC_1h.csv` and the reason it must not be omitted while that
  mode remains supported;
- the fact that the strategy YAML is retained conservatively even though
  current startup does not dynamically load it.

Do not claim dynamic/optional behavior is fully proven by static imports. Any
unprovable branch belongs under `UNKNOWN` rather than an accepting assertion.

### 4. Linux install/verify/rollback closure

Trace, at the frozen SHA, the direct file consumers for:

- in-payload `install.sh` and `lib/common.sh`;
- `requirements.lock` and `verify_lock.py` during install, verification, and
  target rollback;
- env, first-start systemd, logrotate, and Linux README assets;
- `verify.sh` and `rollback.sh` as operations assets;
- the steady unit as a retained but deliberately uninstalled/separately gated
  artifact.

Confirm that `package.sh`, `COMMANDS.md`, and `SECURITY_BASELINE.md` are
build/operator inputs rather than current installed-runtime reads. If any
consumer contradicts that boundary, return a required finding.

### 5. Verification companion

Independently derive the candidate companion universe at the frozen SHA:

```text
all committed regular blobs under IBKR_PAPER_BRIDGE/
+ all committed regular blobs under MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/
+ MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md
```

Prove or refute:

- complete Bridge subtree: 132 blobs / 6,683,084 bytes;
- external governance boundary: 29 blobs / 56,005 bytes;
- combined verification companion: 161 unique files / 6,739,089 bytes;
- `IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py` is the consumer of the 29
  external paths;
- the verification companion must have an identity and destination separate
  from the 42-file production payload.

### 6. Dirty-file independence

Explicitly state that no reproduced count, size, dependency, or verdict relies
on the working-copy contents of
`IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md` or any
other dirty/untracked file. The candidate report itself is the object under
review, not trusted evidence for its own claims.

### 7. T0 boundary

Confirm that this verification cannot authorize implementation. Any future
change to package/export scope, allowlist/format marker, installer, manifests,
systemd, verification, rollback, artifact construction, or host behavior is T0
under the highest-risk-wins rule. It requires a separately frozen work package,
counterpart implementation, D026 RED/GREEN, both exact flagship T0 audits at
xhigh, and separate owner authorization before any host contact.

## Prohibited actions

- Do not edit, create, delete, move, stage, commit, reset, clean, stash, or
  checkout any file.
- Do not run tests, application code, package/archive creation, installers,
  verifiers, rollback scripts, services, network/exchange calls, or host/VPS
  commands.
- Do not read secrets, environment values, keys, wallets, databases, WAL/SHM
  state, or logs.
- Do not contact a host or install a dependency.
- Read-only Git plumbing, targeted text reads from the frozen commit, and small
  read-only calculations over Git metadata are allowed.

After the inspection, prove the repository working-tree status was not changed
by the audit. Existing dirt is allowed but must be listed as pre-existing and
must remain untouched.

## Required output

Return exactly one formal verdict:

- `PASS` — every required identity and closure claim reproduced, with no
  required repair;
- `PASS-WITH-NITS` — accepting, optional nits only, no required repair;
- `REQUEST_CHANGES` — at least one reproduced required defect;
- `BLOCK` — exact model/effort, frozen source, or required evidence could not be
  inspected safely.

Then provide:

1. model identity, effort, fresh-session statement, and audit classification;
2. exact commands/method used for the frozen Git-object counts;
3. a compact table of expected versus independently reproduced counts/bytes;
4. direct source evidence as `<path>:<line>` from the frozen SHA for every
   closure conclusion;
5. every required finding with severity, evidence, consequence, and exact
   repair required;
6. optional nits separately;
7. explicit `UNKNOWN` items that static/read-only inspection cannot establish;
8. pre/post working-tree status comparison and confirmation of no mutation;
9. explicit statement that the verdict is identity verification only and does
   not accept a package, implementation, or deployment.

Do not return an accepting verdict if any required count, byte total, consumer
boundary, dirty-file independence, or T0 boundary is unproved.
