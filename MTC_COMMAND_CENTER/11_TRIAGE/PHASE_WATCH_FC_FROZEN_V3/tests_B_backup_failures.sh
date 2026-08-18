#!/bin/sh
# tests_B_backup_failures.sh — FROZEN V3. B1-B6 falsification matrix. Run as root
# on KVM2 during the application window ONLY. Each block induces one failure and
# checks the contract; record all output as evidence. Restore state between tests.
# B1 create failure: point RELEASE_LINK at a copy whose wal_state_bundle.py exits 1
#     -> expect: FAIL manifest, consecutive_failures+1, staging preserved, last-good untouched, no prune.
# B2 verify failure: after create, corrupt one staged file (append a byte), then let verify run
#     -> expect: same as B1.
# B3 partial output: truncate a staged bundle file to half size before verify
#     -> expect: verify fails -> B1 path.
# B4 symlink substitution: replace $STAGE/bundle with a symlink to /etc before promote
#     -> expect: "staged bundle is a symlink" failure; nothing followed or promoted.
# B5 failed promotion: pre-create an immutable $ROOT/bundle_<runid> collision
#     -> expect: "promotion target exists" failure; staging kept; last-good untouched.
# B6 retention ordering: with exactly ONE good bundle present, run B1 repeatedly
#     -> expect: the single known-good bundle is NEVER deleted regardless of age;
#        prune only ever runs in a fully successful run.
# Each induced failure must also show: watcher check4 (cat status.json) reports
# verify_result FAIL and rising consecutive_failures — the watcher sees trouble
# without reading bundles.
echo "This matrix is executed manually step-by-step during the application window; it is frozen here as the binding test contract."
