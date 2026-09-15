# Bridge verification

From `IBKR_PAPER_BRIDGE` run the scoped suite with:

`python -m pytest --ignore=TSP1009B.pytest_tmp_s1r1`

On Linux run the suite as a non-root user. As uid 0, SQLite 3.45's unix VFS issues `fchown()` on the
`-wal`/`-shm` files during a read-only open, which refreshes ctime and makes the capture drift guard in
`tools/wal_state_bundle.py` fail closed in exactly three `test_wal_state_bundle.py` tests (root-only;
GitHub CI runs as a non-root runner and passes). A root-owned checkout also needs
`git config safe.directory` for the non-root user or `test_linux_deployment`'s fresh-checkout test
cannot run `git show`.

The ignored directory is ACL-locked and otherwise aborts collection with `PermissionError`.
Two recorded baseline failures may exist: stale KVM2 evidence-ledger hash and
`test_invariants_preserve_risk_and_history` expecting schema v2 while default is v4. Reproduce the
baseline and fail on any delta; do not relabel new failures as pre-existing.

For risk/order/persistence/concurrency/build/deploy/safety defects, perform D026 falsification on
the exact missing behavior. Verify database rows/transactions and on-disk bytes, identities and
hashes. Host-touching commands require separately authorized rehearsal and rollback evidence.
