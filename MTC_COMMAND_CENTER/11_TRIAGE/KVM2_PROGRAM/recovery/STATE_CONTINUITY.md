# State continuity and recovery

- P3-01 owner choice: **OPEN**
- Recommended path: **WAL-consistent migration**
- Conservative fresh-state reset: not selected, not approved

## Recommended migration contract

After the old writer is separately quiesced and single-writer/flat evidence is
accepted, use `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py create` without
`--allow-live-source`. The tool opens the source read-only, uses SQLite online
backup rather than copying db/WAL/SHM files, runs `integrity_check` and
`foreign_key_check`, records source-sidecar provenance hashes, produces one
self-contained database, and derives sanitized risk/history invariants.

Verification must receive the externally recorded bundle DB and invariant
SHA-256 values. It rechecks the manifest contract, path sanitization, manifest
integrity hash, DB hash, SQLite integrity, foreign keys, table counts, open
trades, live orders, closed-trade loss streaks, realized PnL, risk-day ledger,
and maximum identifiers. Any mismatch, corruption, unknown state, unexpected
sidecar, unsanitized value, or partial capture blocks transfer/start/ARM.

The final destination database hash must equal the accepted bundle hash before
the one DISARMED start. Foreign exchange positions/orders are not inferred from
SQLite; they remain separate raw exchange-side cutover checks under owner
control.

## Recovery classes

| Class | Required contents | RPO/RTO status |
|---|---|---|
| Bridge state/risk | WAL-consistent bundle, invariant hashes, restore result | OPEN owner decision |
| Logs/evidence | Sanitized ledger plus encrypted restricted raw evidence | OPEN owner decision |
| Config/release | Exact payload, lock, unit, installer and manifest hashes | Prepared; final RC OPEN |

Backups must be encrypted off-host, versioned/retention-locked, and restorable
in isolation. The KVM2 write credential must not delete versions or change
retention. A separately held recovery credential and off-PC encryption-key
recovery test are required. Secret values remain excluded.

No restore is accepted without exact-release ordering, bundle verification,
application-level semantic checks, and an isolated restore drill. P2-09/P3-03/
P5-03 remain blocked until their respective evidence exists.
