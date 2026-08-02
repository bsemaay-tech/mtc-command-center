# DEFECT 3B — ROOT CAUSE (2026-08-03)

`wal_state_bundle` cannot capture a state bundle on Linux. This is the **Stage E ordered
single-writer cutover** tool, and Stage E forbids `--allow-live-source`, so as written **the KVM2
cutover cannot produce a valid state bundle on the target platform.**

Diagnosed by the Lead (`claude-opus-5`) on `GATEA-STAGING`. Repair dispatched to the counterpart
flagship implementer on branch `codex/wal-bundle-linux-sidecars` (based on `origin/master`
`637307e8`). **Not yet implemented, not yet audited.**

## 1. Scale — the defect accounts for 23 of the 25 remaining Linux failures

From `fixsuite.log` on the staging host (Ubuntu 24.04, Python 3.12.3, the locked runtime), against
the repaired payload:

```
23  tests/test_wal_state_bundle.py     <- this defect
 2  tests/test_order_state.py          <- defect 3a (gc-referents, 3.12 vs 3.14)
25  total
```

Most of the 23 are `test_verify_*`, which fail downstream of a `create` fixture that cannot succeed.
**One root cause, 23 failures.**

Failure signature, on a database nothing else is writing to:

```
source_changed_during_capture
changed_components: ['wal', 'shm']
```

## 2. Root cause

`_connect_readonly()` establishes the read-only connection with `conn.execute("SELECT 1")`
(`tools/wal_state_bundle.py:228`). `SELECT 1` accesses no table, so SQLite never starts a read
transaction on the main database and **never attaches the WAL** — `-wal` / `-shm` are not
materialised by that call.

`create()` then runs, in order:

| Step | Line | Action |
|---|---|---|
| 1 | ~605 | `source_snapshot_arrival` |
| 2 | ~618 | `_connect_readonly(source)` |
| 3 | ~624 | `source_snapshot_before` — **the drift bracket opens** |
| 4 | ~630 | `_integrity_check(src)` — **first statement that touches the DB** |
| 5 | ~645 | online backup |
| 6 | ~654 | `source_snapshot_after` — the bracket closes |

On Linux the WAL attach happens at **step 4**, so the tool's *own* `-wal`/`-shm` creation lands
inside the measured window and is reported as source-writer drift.

The comment at lines 620-623 states the intended invariant — *"Bracket the actual
integrity/invariant/backup capture after that setup and before close so our own connection
lifecycle is not misreported as source-writer drift."* **The code does not achieve it.**

## 3. Evidence — the same probe, both stacks

A probe creating a WAL-mode DB, closing it, then snapshotting `db`/`-wal`/`-shm` at arrival, after
`connect() + SELECT 1`, and after the first real read:

**Linux — Python 3.12.3 / SQLite 3.45.1**
```
arrival                       : db=True  wal=False shm=False
after SELECT 1 (tool 'before'): db=True  wal=False shm=False
after real read (tool 'after'): db=True  wal=True  shm=True

arrival -> before  changed: []
before  -> after   changed: ['wal', 'shm']    <- reported as source drift
```

**Windows — Python 3.14.2 / SQLite 3.50.4**
```
arrival                       : db=True  wal=False shm=False
after SELECT 1 (tool 'before'): db=True  wal=True  shm=True
after real read (tool 'after'): db=True  wal=True  shm=True

arrival -> before  changed: ['wal', 'shm']
before  -> after   changed: []                <- no drift reported
```

The sidecars are materialised at **different points** on the two stacks.

### CORRECTION 2026-08-03 — the probe above did not isolate `connect()`

The Windows row was originally read as *"the sidecars are materialised at `connect()`"*. **That is
wrong**, and an independent `claude-opus-5` xhigh Gate 5 audit of `f1ac2565` falsified it by
measuring the step the probe above skipped:

```
Windows / py3.14.2 / SQLite 3.50.4
  (wal, shm) after connect()                       = (False, False)
  (wal, shm) after SELECT 1                        = (True,  True)
  (wal, shm) after SELECT name FROM sqlite_master  = (True,  True)
```

The probe measured `connect()` **and** `SELECT 1` together and attributed the result to `connect()`.
The real distinction is:

| Stack | WAL attaches on | Falls |
|---|---|---|
| Windows / SQLite 3.50.4 | the **first statement of any kind**, including a constant `SELECT 1` | inside `_connect_readonly`, *before* the bracket opens |
| Linux / SQLite 3.45.1 | the first statement that **reads a table** | at `_integrity_check`, *after* the bracket opens |

So on Windows the tool's own attach already landed in the arrival→before window, where the existing
carve-out handles it. On Linux it landed inside the measured window. The conclusion and the repair
are unchanged — a table-reading statement in `_connect_readonly` attaches on both — but the stated
reason was wrong and would mislead the next reader.

The commit message of `f1ac2565` carries the same error ("observed on Windows … at connect time").
It is recorded here rather than rewritten, because the commit is pushed.

### Honest limit on this evidence

The two stacks differ in OS **and** in Python/SQLite version. This establishes that the two
configurations behave differently; it does **not** isolate the OS as the cause — and given the
correction above, the SQLite version is at least as likely to be the operative difference as the
kernel. The repair is therefore required to be correct for either ordering and is forbidden from
branching on `sys.platform`.

This also means the earlier framing — *"SQLite's sidecar files are necessarily touched on Linux by
opening a WAL-mode database"* — was directionally right about the symptom but asserted a cause that
the available evidence does not separate from the interpreter change. Corrected here.

## 4. Constraints placed on the repair

1. The WAL must be attached before `source_snapshot_before` is taken, on every platform.
2. No `sys.platform` / `os.name` conditional.
3. `_connect_readonly()` stays strictly read-only and must still fail closed on a hot `-wal` with no
   `-shm`.
4. A regression test that **fails before the fix and passes after it**.
5. A test proving the detector **still fires** on a genuine concurrent writer. A fix that silences
   the drift detector would be a worse defect than the one being repaired.
6. `SCHEMA_VERSION` and the manifest schema unchanged — a schema move invalidates recorded evidence
   elsewhere in the programme.

## 5. Verification owed

The bug does **not reproduce on Windows**, so Windows-only test evidence cannot accept this repair.
The Linux run on `GATEA-STAGING` is mandatory before acceptance.

## 6. Safety

Read-only diagnosis. No ARM, no order, no broker connection, no TESTNET, no mainnet, no wallet
action, no credential value. No service was started. The probe ran in a temporary directory on the
disposable staging VM and touched no bridge state. KVM2 untouched;
`KVM2-Ubuntu-2404-Staging` remains powered off and quarantined per owner decision.
