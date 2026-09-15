# Lane J — Bridge static defect hunt (read-only)

Scope: `IBKR_PAPER_BRIDGE/bridge/**` and `IBKR_PAPER_BRIDGE/tools/**` (tests excluded).
No source file changed. Every hit below was opened and read in context before classification.

## Summary table

| Rule | Count | (a) real defect | (b) latent | (c) style/false-positive |
|---|---|---|---|---|
| F401 (unused import) | 7 | 0 | 2 | 5 |
| B007 (unused loop var) | 1 | 1 | 0 | 0 |
| B009 (getattr w/ constant) | 1 | 0 | 0 | 1 |
| F841 (unused local) | 2 | 1 | 0 | 1 |
| B904 (raise w/o `from`) | 2 | 0 | 0 | 2 |
| **Total** | **13** | **2** | **2** | **9** |

`ruff check` produced 13 hits total under the requested rule set; no `PLE`, `PLW0602`,
`PLW0603`, `PLW0120`, `RUF006`, `RUF012`, `S102`, `S307`, `S602`, `S605` hits occurred in scope.

## (a) Real defects, ranked by severity

### 1. `config_contract.py:1880` — B007, self-check diagnostic loses the missing-binding name

`IBKR_PAPER_BRIDGE/bridge/config_contract.py:1866-1888`
```python
            variable = child.targets[0].id
            expected_chain, expected_target = expected_bindings[variable]
            ...
        for variable in sorted(set(expected_bindings) - observed_bindings):
            findings.append(
                SourceCensusFinding(
                    "DETECTED",
                    "ENGINE_OPTIONS_NOT_BOUND_OBJECT_INPUT",
                    "bridge/config_contract.py",
                    construct.lineno,
                )
            )
```
`variable` is bound by the `for` header but never read in the loop body — the emitted
`SourceCensusFinding` carries only the enclosing construct's line, not which expected
binding (`variable`) is missing. This is a source-census/self-audit tool (verifies the
engine's source matches an expected AST shape); the finding count and location are still
correct, but a maintainer debugging a `DETECTED` result has no way to tell which binding
triggered it without re-deriving `expected_bindings` by hand. Not order/economics/risk
logic — safe to improve outside owner gate.

Proposed minimal patch:
```diff
-                SourceCensusFinding(
-                    "DETECTED",
-                    "ENGINE_OPTIONS_NOT_BOUND_OBJECT_INPUT",
-                    "bridge/config_contract.py",
-                    construct.lineno,
-                )
+                SourceCensusFinding(
+                    "DETECTED",
+                    f"ENGINE_OPTIONS_NOT_BOUND_OBJECT_INPUT:{variable}",
+                    "bridge/config_contract.py",
+                    construct.lineno,
+                )
```

### 2. `db.py:3174-3177` — F841, dead `new_submitted_ts` signals a dropped migration check — OWNER-GATED

`IBKR_PAPER_BRIDGE/bridge/store/db.py:3159-3184`
```python
                if order_rows_check:
                    ...
                    new_state = "LEGACY_SUBMITTED"
                    new_submitted_ts = fp_ts
                else:
                    new_state = "LEGACY_RESERVED"
                    new_submitted_ts = None

                if existing["state"] != new_state:
                    raise MigrationError(...)
                if existing["origin_run_id"] != run_id:
                    raise MigrationError(...)
                if existing["origin_decision_uid"] != decision_uid:
                    raise MigrationError(...)
```
`new_submitted_ts` is computed in both branches but never compared against
`existing["submitted_ts"]` (or any other field) the way `new_state`, `origin_run_id`, and
`origin_decision_uid` are. It reads as an incomplete duplicate-intent legacy-migration
validation: the immutable-identity check the surrounding code clearly intends to run is
missing one field. This is fail-closed migration-validation logic guarding order/trade
identity records — per instructions this is **owner-gated**; no behavior change is
proposed. Flagging the gap only; a mechanical (behavior-preserving) cleanup would be to
rename the branch-local variable so its unused status is explicit:
```diff
-                    new_state = "LEGACY_SUBMITTED"
-                    new_submitted_ts = fp_ts
+                    new_state = "LEGACY_SUBMITTED"
+                    _new_submitted_ts = fp_ts  # unused pending owner decision on identity check
                 else:
-                    new_state = "LEGACY_RESERVED"
-                    new_submitted_ts = None
+                    new_state = "LEGACY_RESERVED"
+                    _new_submitted_ts = None  # unused pending owner decision on identity check
```
Whether to add `existing["submitted_ts"]` to the equality check is an owner call.

## (b) Latent findings (no runtime effect today, explained)

### 1. `orders.py:67` — F401, `OrderCollisionError` imported but never caught by name

`IBKR_PAPER_BRIDGE/bridge/engine/orders.py:63-73`
```python
from bridge.store.db import (
    DURABLE_EVENT_ROWS,
    DurableRowFault,
    IdentityCollisionError,
    KillConflictError,
    OrderCollisionError,
    PartialRecoveryConflictError,
    Store,
    compute_intent_identity,
```
`OrderCollisionError` is raised by `Store._insert_order_in_tx` / `Store.insert_order`
(`db.py:4993`, `db.py:5076`) but `orders.py` never has an `except OrderCollisionError`
clause — grep confirms zero catches in the file. Latent, not broken, because the module's
existing broad `except Exception:` handlers (e.g. `orders.py:2292`, `2341`) already catch
it along with everything else and route to the same generic durable-write-failure paths;
no exception is silently dropped. No behavior differs today. Left as owner-gated (touches
order-collision/fail-closed handling) — flagging only that the specific-exception import is
presently decorative.

### 2. `db.py:81` / `db.py:8498` — F401, `RISK_DAY_STATE_MALFORMED` constant imported but referenced by magic string

`IBKR_PAPER_BRIDGE/bridge/store/db.py:81` imports the constant; `IBKR_PAPER_BRIDGE/bridge/store/db.py:8496-8499` uses a literal instead:
```python
        except (KeyError, TypeError, ValueError):
            raise ReconcileConflictError(
                "RISK_DAY_STATE_MALFORMED", "authoritative equity is malformed"
            ) from None
```
`bridge/engine/types.py:1279` defines `RISK_DAY_STATE_MALFORMED = "RISK_DAY_STATE_MALFORMED"`
— value matches exactly, so behavior is identical today. Latent risk: if the constant's
string value is ever renamed, this call site silently diverges since it doesn't reference
the symbol. Touches risk/fail-closed error codes — owner-gated; flagging only.

## (c) Style / false positives (brief)

- `engine.py:23` `build_notifier` and `engine.py:30` `KillEvidenceEpoch` — confirmed dead
  imports (only mentioned in a comment at `engine.py:131`). Safe mechanical removal.
- `orders.py:63` `DURABLE_EVENT_ROWS` — confirmed unused in `orders.py` (the accessor is
  defined and used elsewhere in `db.py:721`). Safe mechanical removal.
- `smoke_fill.py:28` `OrderPlan`, `Signal` — confirmed unused in the 237-line tool script.
  Safe mechanical removal.
- `orders.py:4266` B009 `getattr(order, "size")` — no `default` argument supplied, so it is
  exactly equivalent to `order.size` (both raise `AttributeError` if missing, both are
  caught by the same `except (LotQuantizationError, TypeError, ValueError):` — actually
  *not* caught, since `AttributeError` isn't in that tuple either way). No behavior
  difference between the two forms; pure style.
- `db.py:4993` / `db.py:5076` B904 (`raise OrderCollisionError(...)` inside
  `except sqlite3.IntegrityError:` without explicit `from`) — both are raised while already
  inside the `except` block, so Python's implicit exception chaining (`__context__`) still
  attaches the original `IntegrityError` to the traceback; only the *explicit* `raise ... from`
  annotation (which documents chain-vs-suppress intent) is missing. No information is lost
  at runtime. Style only.
- `smoke_fill.py:74` F841 `manager = OrderManager(store, broker, run_id)` — the trailing
  comment ("registers user-event callback pre-connect") makes clear this is an intentional
  side-effect-only construction in a one-shot manual smoke script; the object is not
  needed afterward. Style only (could be renamed `_manager` for clarity).

## Manual review — additional bug classes

**Mutable default arguments** — none found in `bridge/` or `tools/` (excluding tests):
`grep -rn "def .*=\s*(\[\]|\{\}|set\(\))"` returned zero matches in scope.

**`except Exception: pass` swallowing errors on money/order paths** — ~50 `except Exception:`
blocks exist across `bridge/store/db.py`, `bridge/engine/orders.py`, `bridge/engine/engine.py`,
`bridge/broker/hyperliquid.py`, `bridge/broker/mock.py`, `bridge/engine/notify.py`,
`bridge/settings.py`. The large majority are explicitly documented, single-purpose fail-safe
patterns (`self.conn.rollback()` after a failed write; `# notifications must never raise`;
`# diagnostics never break the path`; `# pragma: no cover - never let audit break safety`;
`# a broken quantum is "unknown"`), consistent with the codebase's stated fail-closed design.
Two representative nested examples reviewed closely:
- `orders.py:2403-2417` (`_quarantine_unknown`) — outer failure attempts a best-effort audit
  event write; if that *also* fails, `pass` on the innermost `except`. Comment
  ("best-effort UNKNOWN transition; failed writes leave SUBMITTING durable") states the
  intended fallback explicitly — durable state is preserved regardless. Reviewed, no defect.
- `db.py:5071-5075` — `self.conn.rollback()` wrapped in its own `try/except Exception: pass`
  immediately before raising `OrderCollisionError`; a rollback failure here is swallowed so
  the *real* `OrderCollisionError` still propagates rather than being masked by a secondary
  rollback exception. Reviewed, intentional, no defect.
No instance was found where a bare `except Exception: pass` discards an order/fill/money
result without ever surfacing it (durable state, a store event, or a re-raise always
follows). This entire class is fail-closed/error-handling design — **owner-gated** by
instruction; no changes proposed.

**Float `==`/`!=` comparisons on quantities/prices** — found at:
`db.py:4989`, `db.py:5067`, `db.py:6297-6298`, `db.py:7015`, `db.py:9960`,
`orders.py:1453`, `reconcile.py:1126-1127`. Example (`db.py:5063-5070`):
```python
            if (str(existing["decision_uid"]) != decision_uid
                    or existing["trade_id"] != trade_id
                    or str(existing["role"]) != role
                    or float(existing["qty"]) != qty
                    or str(existing["order_ref"]) != order_ref
```
These are all inside order-collision detection, fill-reconciliation matching, or equity
integrity checks — i.e. squarely order handling / fail-closed logic. Exact float equality
is a known-risky pattern (SQLite round-trip / JSON round-trip could in principle produce a
representation difference), but changing the comparison semantics here changes
collision/reconciliation behavior. **Owner-gated per instructions — pattern flagged across
7 call sites, no patch proposed.**

**`datetime.now()` without timezone where UTC is expected** — found at
`bridge/broker/mock.py:349,428,569,817` (all four call `datetime.now()` un-parameterized,
while the rest of the module and the whole engine use `datetime.now(UTC)`). The resulting
naive datetimes flow into `FillEvent.ts` / `OrderUpdateEvent.ts` and eventually into
`reconcile.py:826` (`component.observed_ts.astimezone(UTC).isoformat()`), where a naive
datetime is interpreted as the **host's local time** before conversion — correctness then
depends on the deployment host's system timezone (harmless if the host runs UTC, wrong
otherwise). `MockBroker` is wired in at `bridge/app.py:203-207` only when `dry_run=True`
(CSV-fixture simulation) — it is never used for live/paper trading against Hyperliquid
(`HyperliquidBroker` is used for both `"paper"` and live testnet modes). Classified **(b)
latent**: no effect on hosts configured with UTC system time (the common container
default), real only on non-UTC hosts, and confined to dry-run simulation, not real money
flow. This is a mechanical timestamp-source fix, not economics/order/risk logic, so a
minimal patch is proposed:
```diff
--- a/IBKR_PAPER_BRIDGE/bridge/broker/mock.py
+++ b/IBKR_PAPER_BRIDGE/bridge/broker/mock.py
@@
-            self._record_fill(close, qty, px, datetime.now())
+            self._record_fill(close, qty, px, datetime.now(UTC))
@@
-            observed_ts=datetime.now(),
+            observed_ts=datetime.now(UTC),
@@
-        self._record_fill(order, qty, px, datetime.now())
+        self._record_fill(order, qty, px, datetime.now(UTC))
@@
-            ts=datetime.now().astimezone(),
+            ts=datetime.now(UTC),
```
(Line numbers: 349, 428, 569, 817 respectively — `UTC` is already imported at
`mock.py:10`.)

**`dict.get()` on required keys silently defaulting** — reviewed all `.get("qty"|"px"|
"cloid"|"oid"|"decision_uid"|"trade_id"|"role"|"status"|"coin"|"direction")` call sites in
`bridge/`. The one call touching money-critical data, `order_plan.get("qty")` at
`db.py:2988`, is immediately guarded:
```python
IBKR_PAPER_BRIDGE/bridge/store/db.py:2988-2999
            plan_qty = order_plan.get("qty")
            ...
            if plan_qty is None or plan_stop_loss is None:
                raise MigrationError(
                    f"Incomplete order_plan for {decision_uid}: "
                    f"qty={plan_qty!r} stop_loss={plan_stop_loss!r}"
                )
```
No silent default reaches downstream economics — the missing-key case fails closed via
`MigrationError`. All other reviewed `.get()` calls (`mock.py`, `hyperliquid.py`,
`db.py` audit/query paths) are on optional/advisory fields (`oid`, `cloid` presence
checks, filter predicates) already guarded by `or ""`/`is not None`/membership checks at
the same statement. No defect found in this class.

**`subprocess` with `shell=True`** — none found in `bridge/` or `tools/` (excluding tests).
The single `subprocess.run` call in scope, `tools/check_runtime_baseline.py:74`, does not
pass `shell=True` (confirmed by both the manual grep and the ruff S602/S605 selectors
above, which produced zero hits).

## Commands executed

```
$RUFF check --isolated --no-cache --output-format concise --select F,B,PLE,PLW0602,PLW0603,PLW0120,RUF006,RUF012,S102,S307,S602,S605 IBKR_PAPER_BRIDGE/bridge IBKR_PAPER_BRIDGE/tools
```
Output (13 hits, trimmed to rule/location — full text reproduced in the sections above):
```
config_contract.py:1880:13: B007  Loop control variable `variable` not used within loop body
engine.py:23:52:  F401  `bridge.engine.notify.build_notifier` imported but unused
engine.py:30:5:   F401  `bridge.engine.types.KillEvidenceEpoch` imported but unused
orders.py:63:5:   F401  `bridge.store.db.DURABLE_EVENT_ROWS` imported but unused
orders.py:67:5:   F401  `bridge.store.db.OrderCollisionError` imported but unused
orders.py:4266:41:B009  Do not call `getattr` with a constant attribute value.
db.py:81:5:       F401  `bridge.engine.types.RISK_DAY_STATE_MALFORMED` imported but unused
db.py:3177:21:    F841  Local variable `new_submitted_ts` assigned but never used
db.py:4993:17:    B904  raise without `from err`/`from None`
db.py:5076:17:    B904  raise without `from err`/`from None`
smoke_fill.py:28:33: F401 `bridge.engine.types.OrderPlan` imported but unused
smoke_fill.py:28:44: F401 `bridge.engine.types.Signal` imported but unused
smoke_fill.py:74:5:  F841 Local variable `manager` assigned but never used
Found 13 errors. [8 fixable with --fix; 2 hidden fixes need --unsafe-fixes]
```
Manual review commands (Grep tool, equivalent to):
```
grep -rnE 'def .*=\s*(\[\]|\{\}|set\(\))' IBKR_PAPER_BRIDGE/bridge IBKR_PAPER_BRIDGE/tools --include=*.py   # 0 hits
grep -rn -A1 'except Exception:' IBKR_PAPER_BRIDGE/bridge IBKR_PAPER_BRIDGE/tools --include=*.py            # ~50 hits, reviewed
grep -rn 'datetime.now()' IBKR_PAPER_BRIDGE/bridge IBKR_PAPER_BRIDGE/tools --include=*.py                    # 4 hits, mock.py only
grep -rn 'shell=True|os\.system\(' IBKR_PAPER_BRIDGE/bridge IBKR_PAPER_BRIDGE/tools --include=*.py           # 0 hits
grep -rn 'float\([^)]*\)\s*(==|!=)' IBKR_PAPER_BRIDGE/bridge --include=*.py                                   # 7 sites (listed above)
```

## No source file changed; no test, server, broker, or launcher executed
