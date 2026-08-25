# Bridge verification

From `IBKR_PAPER_BRIDGE` run the scoped suite with:

`python -m pytest --ignore=TSP1009B.pytest_tmp_s1r1`

The ignored directory is ACL-locked and otherwise aborts collection with `PermissionError`.
Two recorded baseline failures may exist: stale KVM2 evidence-ledger hash and
`test_invariants_preserve_risk_and_history` expecting schema v2 while default is v4. Reproduce the
baseline and fail on any delta; do not relabel new failures as pre-existing.

For risk/order/persistence/concurrency/build/deploy/safety defects, perform D026 falsification on
the exact missing behavior. Verify database rows/transactions and on-disk bytes, identities and
hashes. Host-touching commands require separately authorized rehearsal and rollback evidence.
