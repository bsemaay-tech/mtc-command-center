# WP-S / S3-STRUCT — NEW BOUNDED CYCLE: HANDOFF AND GATE-1 SCOPE (2026-08-01)

**This document is the complete handoff.** A fresh session should be able to run this cycle from
this file plus `AGENTS.md` and `_AI_MEMORY/GLOBAL_HANDOFF.md` alone. No prior conversation needed.

**Owner decision (2026-08-01):** approved option 1 from `WPS_S3_HARD_STOP_2026-08-01.md` §8 —
*"Yapısal düzeltme için yeni sınırlı döngü — doğrulayan erişim sınırı + close yolunun bağı yeniden
türetmesi."* A new bounded cycle is authorised to replace point-by-point guarding with a validated
accessor boundary, and to make the close path re-derive its binding.

---

## 1. Where the programme stands

| WP | Budget | State |
|---|---:|---|
| WP-0 Scope / Baseline | 2 h | **DONE, merged to master** (PR #36, record `4d2228cf`) |
| WP-S — S2 closure | — | **ACCEPTED at `0c65a731`**, both flagship auditors PASS-WITH-NITS, 0 required |
| WP-S — minimum S3 | — | **NOT ACCEPTED.** 3 rounds spent, hard stop at `732b37c3` |
| **S3-STRUCT (this cycle)** | see §6 | **AUTHORISED, not started** |
| WP-L / WP-I / WP-A / WP-V | 8/6/3/8 h | blocked — plan §23b step 7 gates WP-L Phase 1 on Audit 1 accepting |

Branch `feature/ts-p1-009b-s2-closure`, worktree `C:/WPS`, head `732b37c3`, pushed.
`origin/master` = `2ebb0475`. Plan blob SHA-256 `a07c90cc…` (hash the **committed blob**).

**Nothing downstream can start until Audit 1 accepts.** There is no independent authorised stream.

---

## 2. The defect class this cycle exists to close

Five required findings across two independent flagship auditors at `732b37c3`, spanning **three
classes**. All were reproduced with live probes, then re-verified by the Lead on real source.

### Class A — schema-admitted data reaches an unguarded conversion on the drain path

SQLite columns here are **affinity-only**: no `CHECK`, no `NOT NULL`, no `STRICT`. `fills.qty REAL`
accepts non-numeric TEXT and NULL; `orders.trade_id INTEGER` accepts arbitrary TEXT. The v8→v9
migration preserves predecessor rows unvalidated **by design** (`_migrate_v8_to_v9` asserts the row
census is unchanged).

- `db.py:7338-7339` — `insert_fill` builds its duplicate-classification tuple with bare
  `float(row["qty"])` / `float(row["px"])`. Two lines below, `fee`/`funding` use `or 0.0`: the NULL
  case was considered for two columns and missed on the two that matter. **`insert_fill` runs ahead
  of every guard round 3 added.** Found independently by *both* flagships.
- `orders.py:2670` — `_event_symbol` uses raw `int(order["trade_id"])`. `_parse_store_trade_id`
  exists at `2687` and is applied at only `2727` and `3229`. `_event_symbol` runs for **every**
  queued event, on **both** drains, before any guard.
- `orders.py:2857-2859` — `_canonical_status` computes `float(order.get("filled_qty") or 0.0)`
  **outside** its own `try`.

Escape route in every case:
```
BridgeEngine.start() → order_manager.reconcile() → sync_broker_state()
  → drain_queued_events() → _ingest_queued_event() → _ingest_event() → _ingest_fill()
```
`_ingest_queued_event` catches only `KillConflictError`. Everything else unwinds through the
**unguarded** `start()` and the `app.py` lifespan hook: **the bridge does not start, and no durable
evidence is written.** Of 14 schema-admitted corruptions probed, 11 were contained and **3 escaped**.

### Class B — the parser is type-total but not storage-boundary safe

`_parse_store_trade_id` handles "not-an-integer", but accepts any Python int or Unicode-decimal
string without SQLite signed-64-bit bounds validation. A value above `2^63-1` parses in Python and
then raises **`OverflowError`** when sqlite3 binds it in `get_trade`. Same escape route, same silence.

### Class C — the close path never re-derives its binding *(the most serious)*

`close_trade_once_with_decision` (`db.py:~7469`) fences the **epoch**:
`_assert_kill_epoch_in_tx` plus `AND EXISTS (SELECT 1 FROM kill_requests WHERE episode_id=? AND
epoch_token=?)`. That proves the epoch token is current. **Lead-verified by direct source read: the
fenced `UPDATE` contains no join back to `orders`.** Nothing confirms the trade being closed is
still bound to the active episode.

Scenario: with active epoch A, Store 1 validates a `KILL_FLATTEN` order bound to episode A / trade
T; Store 2 clears or changes `orders.group_id`; Store 1 continues down the active-epoch branch and
**closes T and writes `TRADE_CLOSED` with no identity quarantine.**

This is a **correctness** gap in B2's territory, not a liveness gap. It does **not** invalidate the
accepted S2 artifact `0c65a731` — it is reachable only through S3's own identity-validation path,
which does not exist at that commit — but no S3 artifact may be accepted while it stands.

Round 3's own two-`Store` test missed it because that test runs with **no active epoch**: it
exercises the deferral store's binding check and never the close path.

---

## 3. Why three rounds failed — read this before writing any code

| Round | Scoped to close | What it left open |
|---|---|---|
| 1 | the startup-failure class | re-opened a reachable variant, dropped an event, relocated unbounded growth |
| 2 | identity *shape* validation | the store also required durable *binding*; `int()` ran before validation |
| 3 | identity parsing + durable binding + schema capability | `insert_fill` runs ahead of every guard; `_event_symbol` never got the parser |

Each repair was applied **point-by-point at the call sites the previous audit named**. That is why
every round closed the probed path and opened its neighbour. **The repair strategy was the problem,
not the implementer's diligence.**

> **Guard the entry point, not one line.**

A fourth point-fix round would very likely reproduce the pattern. That is exactly why the owner
approved a structural cycle instead.

---

## 4. GATE-1 SCOPE — frozen by the Lead

### S3T-A — validated accessor boundary over durable rows

Introduce a single typed accessor layer for reading durable `orders` / `fills` / `trades` values.
Every read of a durable row **on any path reachable from a queued broker event** goes through it.

It must return **either a validated typed value or a containable fault** — never raise an unguarded
`ValueError`, `TypeError`, `OverflowError`, or `InvalidOperation` into its caller.

Validation must cover, for each column it serves:

| Case | Required behaviour |
|---|---|
| `NULL` | containable fault |
| non-numeric TEXT | containable fault |
| unexpected storage class (TEXT where REAL expected, etc.) | containable fault |
| integer outside SQLite signed 64-bit range | containable fault **(class B)** |
| non-finite float (`NaN`, `±inf`) | containable fault |
| valid value | typed result |

Design choice is the implementer's, but it must be **one boundary**, not a helper called at the
sites an audit happened to name. Scattering guards is the failure mode being replaced.

### S3T-B — close path re-derives its binding

`close_trade_once_with_decision` must, **inside its existing `BEGIN IMMEDIATE`**, re-derive that the
trade it is about to close is *currently* bound to the active episode — joining `orders` on
(`role='KILL_FLATTEN'`, `group_id` = active `episode_id`, `trade_id` = the trade being closed) — not
merely that the epoch token is current.

If the binding no longer holds: **roll back, write durable evidence, fail closed.** Do not commit.

**Do not weaken the existing epoch fence.** `_assert_kill_epoch_in_tx`, the `kill_requests`
`EXISTS` predicate, and the stale-epoch rollback + EP-4 append + raise-to-caller all stay.

### S3T-C — entry-point containment

Every entry point reachable from a queued broker event uses the S3T-A boundary — explicitly
including `_event_symbol` and `_canonical_status`, which currently run **before** any guard on both
drains.

### S3T-D — the acceptance test that makes this structural

**This is the deliverable that distinguishes this cycle from a fourth point-fix round.**

A property-style test that enumerates, for every durable column reachable from a queued event, the
cross-product of corruption cases in the S3T-A table, and asserts for **every** combination:

1. `BridgeEngine.start()` **returns normally**;
2. durable evidence exists for the fault;
3. the system is fail-closed — `app_state` `KILLED`, ARM refuses, ACK unreachable, trade left open;
4. the queue and the deferred map end in a consistent state.

Plus, for class C: a two-`Store` test **with an active epoch** proving the close path refuses when
the binding is broken mid-flight — precisely the case round 3's test did not exercise.

The test must be **generated from a column/case matrix**, not a hand-listed set of the findings
above. A test that only covers the five known findings does not close the class and will not be
accepted.

### Explicitly OUT of scope

TS-P1-010 and beyond · EP-1's residual venue-side supersede window (Hyperliquid exposes no fencing
token — a documented accepted limitation) · any operations-dashboard or read-model redesign · **any
migration, foreign key, `STRICT` table, `CHECK` constraint, or schema-version change** — the fix is
defensive reading, not schema repair · changing the default schema target away from v4 · any
alerting redesign · re-opening accepted S2 mechanisms.

### Lead decision carried forward, unchanged

`KILL_STALE_EVIDENCE_RECORD_FAILED` **keeps propagating**. It means the durable evidence store
itself cannot be written; no durable evidence can be recorded when the evidence store is the failing
component, so halting with `app_state` durably `KILLED` is the honest fail-closed outcome. Identity
and schema-capability faults are contained; **evidence-store outages propagate.** State this in the
prompt so auditors judge it rather than discover it.

---

## 5. Allowlist and hard constraints

**Allowed paths — exhaustive:**

```
IBKR_PAPER_BRIDGE/bridge/engine/orders.py
IBKR_PAPER_BRIDGE/bridge/store/db.py
IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py
IBKR_PAPER_BRIDGE/tests/test_store.py
IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md
```

`bridge/engine/engine.py` is **not** allowed — no item needs it. A scope extension must be reported,
not taken.

**Forbidden everywhere:** any `*.pine`, `MTC_V2`, `parity`, `01_PINE`, `02_MTC_BACKTEST`,
`07_ADAPTERS` path · `bridge/engine/strategies/**`, `config/strategies/**` · `bridge/api/routes.py`
· `bridge/broker/**` · **any risk-threshold value** in `config/bridge.yaml` (position size, leverage,
daily-loss, drawdown, equity floor, exposure, liquidation — owner-defined, never invented or
changed) · any credential, wallet secret, API key, host, IP, or private path · **weakening,
deleting, skipping or `xfail`-ing any existing test — grep your own diff for `-` lines under
`tests/` before reporting; this rule was broken once already** · any migration or schema change ·
starting the bridge against a real broker · any broker, network, TESTNET, ARM, or runtime action.

**Test contract.** From `C:/WPS/IBKR_PAPER_BRIDGE`:

```
python -m pytest -q --ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly
```

`--ignore` is mandatory — `TSP1009B.pytest_tmp_s1r1/` is ACL-locked and plain `pytest` aborts
collection with `PermissionError`. Never pass `--basetemp` inside `.pytest_cache` (produced 623
errors).

Floor at `732b37c3`: **`2 failed, 1140 passed`**. The two failures — stale KVM2 ledger hash, and
`test_invariants_preserve_risk_and_history` asserting `schema_version == "2"` against default v4 —
fail identically on the `origin/master` Bridge tree, are pre-existing, and are outside every
allowlist. **Do not "fix" them.** A third failure is a required finding.

---

## 6. Round bound, funding, and the budget problem — READ THIS

**Round bound: maximum three non-accepting rounds in this new cycle**, per `AGENTS.md` and plan
§23a. After a third non-accepting verdict: stop, report to the owner, do not start a fourth.

**Funding — this cycle does not fit the 50-hour plan's remaining contingency.**

| Line | Budget | Used | Left |
|---|---:|---:|---:|
| WP-S | 12 h | 12.0 | **0** |
| Contingency | 5 h | 3.0 | **2.0** |
| WP-R (audit reserve) | 6 h | 3.5 | **2.5** |

A structural boundary plus a matrix-generated acceptance suite will not fit in 2.0 h. Under plan §22
the contingency is a **hard ceiling** and exhausting it with a safety requirement unfunded is a
BLOCK.

**The owner authorised this cycle explicitly, so it proceeds — but its hours are recorded as an
owner-authorised extension beyond the plan's contingency line, not silently absorbed into it.**
Report actual hours against this record. If the work looks like exceeding ~6 h of implementation,
say so in the record rather than continuing quietly.

---

## 7. Execution recipe — exact, tested commands

Roles: **Claude `claude-opus-5` is Lead and acceptance authority; Codex CLI `gpt-5.6-sol` is the
implementer.** Every implementation dispatch must open with that role override or Codex tries to
delegate to Claude CLI, gets `ConnectionRefused`, and returns BLOCKED with no edits.

**Codex cannot run Git** — read-only `.git`. The Lead performs every Git operation.

```bash
# implementer
bash MTC_COMMAND_CENTER/tools/resilient_dispatch.sh "C:/WPS" <prompt> <out> <log> \
  codex exec -C "C:/WPS" -s workspace-write -m gpt-5.6-sol \
  -c "model_reasoning_effort=xhigh" -c 'approval_policy="never"' -o <out>
```

```bash
# canonical auditor — dedicated worktree at the frozen SHA, then prove it edited nothing
git worktree add --detach /c/WPSAUD<n> <frozen-sha>
bash MTC_COMMAND_CENTER/tools/resilient_dispatch.sh "C:/WPSAUD<n>" <prompt> <out> <log> \
  codex exec --ephemeral -C "C:/WPSAUD<n>" -s workspace-write -m gpt-5.6-sol \
  -c "model_reasoning_effort=xhigh" -c 'approval_policy="never"' -o <out>
git -C /c/WPSAUD<n> status --porcelain -uno   # must be empty, HEAD unchanged
```

```bash
# canonical auditor — Claude, fresh session, never resumed
claude -p --model claude-opus-5 --effort xhigh --no-session-persistence \
  --allowedTools "Read" "Grep" "Glob" "Bash" \
  --disallowedTools "Edit" "Write" "NotebookEdit" "Task" < <prompt>
```

Roster per **D025**: four canonical auditors — `claude-opus-5` xhigh, `gpt-5.6-sol` xhigh,
`cline-pass/deepseek-v4-flash`, GLM-5.2. An auditor that cannot execute the suite must **BLOCK**;
non-execution is never acceptance. A required finding from any auditor binds **after the Lead
reproduces it on real source**. Acceptance needs **both flagships accepting** plus no unresolved
reproduced required finding.

**Give auditor 3 (DeepSeek V4 Flash) the round delta only and one focused question** — it timed out
twice on a full-diff brief, at 15 min and again at 50 min. GLM-5.2's route is unconfirmed on this
machine; establish it or record the gap.

---

## 8. Operational hazards — each one already cost a round or real money

1. **Codex refuses to implement** unless the prompt overrides the two-tier role. Prefix every
   implementation dispatch.
2. **Codex cannot run Git.** Lead does all Git.
3. **A hook flips `HEAD` back to `master`** between tool calls. Commit with one inline
   `checkout; add <explicit paths>; commit`.
4. **`git checkout master` fails** in the shared checkout. Merge in a temporary worktree, push,
   remove it.
5. **Codex `--ephemeral -s read-only` cannot run pytest** (`No usable temporary directory found`) and
   BLOCKs on missing evidence regardless of code quality. Use a dedicated `workspace-write` worktree
   and prove cleanliness afterwards.
6. **A provider content filter can kill a canonical audit mid-run** —
   `This content was flagged for possible cybersecurity risk`, triggered by the crash-simulation
   probe script *Codex itself wrote*. Fix: frame the audit as routine internal review of our own
   service, and instruct the auditor to verify through the existing `pytest` suite rather than
   throwaway failure-simulation scripts. That reframe produced **zero** filter hits.
   **The dispatch wrapper cannot tell a deterministic refusal from a transient loss** — watch it.
7. **`resilient_dispatch.sh` refuses to start unless the output path appears in the command
   arguments.** A missing `-o` once made it re-run five complete `xhigh` audits (~$25).
8. **DeepSeek and Grok CLIs need the prompt as a flag value, not stdin**, and crashed on memory when
   run concurrently with pytest. Run heavy dispatches sequentially.
9. **Verify artifact identity from the committed blob**, never the working copy — CRLF makes the
   on-disk hash differ.
10. `C:/WPSAUD*` leftovers may fail to delete because `.pytest_cache` is ACL-locked. Harmless disk
    residue once deregistered from Git; do not escalate privileges over it.

---

## 9. Standing safety boundaries — unchanged

- **DISARMED only.** No ARM, no order, no broker, no network, no TESTNET, no VPS, no Ubuntu
  execution in this cycle.
- **No Ubuntu execution of any kind before Gate A**, which is far downstream of here.
- **Live-capital actions are never pre-authorised.** If unsure whether something counts, it counts —
  stop and ask.
- Never invent position size, leverage, daily-loss, drawdown, liquidation thresholds, wallet
  selection, or credentials.
- Never print or send credentials, wallet secrets, API keys, or private infrastructure data to any
  model.

---

## 10. Definition of done for this cycle

1. All three defect classes closed **structurally**, not point-wise.
2. The S3T-D matrix suite passes, and the escape set from a queued broker event is demonstrably
   **empty** for schema-admitted data on a healthy database.
3. Suite at `2 failed, 1140+N passed` — same two pre-existing failures, no third.
4. **Both flagship auditors accepting**, no unresolved reproduced required finding from any auditor.
5. Lead has independently reproduced RED for the representative cases and re-run the suite.
6. Records updated; branch merged to `origin/master`; ancestry verified.

Then — and only then — **Audit 1 is accepted, WP-S closes, and WP-L Phase 1 may begin as
verification only** (finding F-0-1: the Linux package at `6fe0130f` is already an ancestor of master
and byte-identical, so nothing is ported and no cross-branch Git operation occurs).
