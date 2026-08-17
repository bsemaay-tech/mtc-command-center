# Bridge package size inventory — 2026-08-17

## 1. Scope and non-action boundary

This is a documentation-only, read-only inventory of the local Bridge source,
release payloads, repository worktrees, caches, and artifact copies. Measurements
were taken on 2026-08-17 from:

- `C:\LAB\Tradingview_LAB_CLEAN`;
- `C:\R7FINAL`;
- `C:\WPI_ARTIFACTS`;
- the frozen extracted release
  `C:\WPI_ARTIFACTS\2ce41e34bceb599d80af24c5c33d835820ec321b`.

No file was deleted, compressed, moved, staged, committed, installed, deployed,
or executed on a host. No secret value was read. MiB and GiB below are binary
units (`1 MiB = 1,048,576 bytes`; `1 GiB = 1,073,741,824 bytes`).

This report does **not** authorize a change to the frozen V1 artifact, its
manifest, its tar, its installed release, its rollback target, or any deployment
script.

## 2. Executive finding

The approximately 1.1 GB item is not a 1.1 GB Bridge application. It is a release
payload that contains almost the entire monorepo. The Bridge subtree is only
6.80 MiB in the measured frozen release, while `MTC_COMMAND_CENTER` occupies
960.07 MiB.

The direct cause is `IBKR_PAPER_BRIDGE/deploy/linux/package.sh:74`:

```sh
git -C "${REPO}" archive --format=tar "${RELEASE_SHA}" | tar -x -C "${OUT}"
```

The command has no path restriction and `.gitattributes` has no `export-ignore`
rules. It therefore exports every tracked file at the exact release commit.

This scope is substantially wider than the Bridge runtime identity contract.
`IBKR_PAPER_BRIDGE/docs/RUNTIME_BASELINE_CONTRACT.md:80-92` defines the
operational source/config scope under `IBKR_PAPER_BRIDGE/` and explicitly says
that `tests/`, `docs/`, other tools, data, databases, logs, and anything outside
`IBKR_PAPER_BRIDGE/` are not part of runtime behavior identity. The Linux
installer likewise requires Bridge-local assets at
`IBKR_PAPER_BRIDGE/deploy/linux/install.sh:168-174` rather than
`MTC_COMMAND_CENTER` research outputs.

The principal remedy is therefore release-scope reduction, not file-by-file
compression or deduplication.

## 3. Frozen release measurements

Measured release SHA:
`2ce41e34bceb599d80af24c5c33d835820ec321b`.

| Layer | Files/entries | Exact bytes | MiB |
|---|---:|---:|---:|
| Git tree at the release commit | 7,058 blobs | 1,032,180,636 | 984.36 |
| Git tree plus 41-byte `RELEASE_SHA` marker | 7,059 manifest entries | 1,032,180,677 | 984.36 |
| `RELEASE_SHA256SUMS` | 1 file | 1,181,804 | 1.13 |
| Complete extracted release directory | 7,060 regular files | 1,033,362,481 | 985.49 |
| Uncompressed transfer tar | 1 tar | 1,047,265,280 | 998.75 |

These figures reproduce the existing evidence in
`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_LOCAL_RUN_KIT_2026-08-08B.md:88-91`
and
`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/CANDIDATE_RELEASE_DERIVATION.md:16-19`.

The current `HEAD` still has the same structural issue. A full-tree archive at
the measured `HEAD` would begin with 7,989 tracked blobs totalling
1,045,751,679 bytes (997.31 MiB) before adding `RELEASE_SHA`, the generated
manifest, and tar padding.

## 4. What occupies the frozen package

| Package section | Exact bytes | MiB | Share of extracted package |
|---|---:|---:|---:|
| `MTC_COMMAND_CENTER` | 1,006,710,136 | 960.07 | 97.42% |
| `MTC_COMMAND_CENTER/03_QUANTLENS` | 868,782,376 | 828.54 | 84.07% |
| QuantLens `tools` | 443,531,700 | 422.98 | 42.92% |
| QuantLens `research` | 379,550,913 | 361.97 | 36.73% |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST` | 100,886,750 | 96.21 | 9.76% |
| `MTC_COMMAND_CENTER/12_PARITY_PINETS` | 16,837,620 | 16.06 | 1.63% |
| Root `docs` | 18,219,994 | 17.38 | 1.76% |
| Entire `IBKR_PAPER_BRIDGE` subtree | 7,130,597 | 6.80 | 0.69% |

The two largest QuantLens classes are historical run outputs:

- `03_QUANTLENS/tools/night_runs`: 347,917,298 bytes (331.80 MiB);
- `03_QUANTLENS/tools/overnight_runs`: 94,383,927 bytes (90.01 MiB);
- `03_QUANTLENS/research`: 379,550,913 bytes (361.97 MiB).

`02_MTC_BACKTEST/data` contributes 92,273,559 bytes (88.00 MiB), primarily
historical Parquet data.

Exact-content grouping of all manifest members found 630 duplicate-hash groups
and approximately 39.38 MiB of redundant copies inside the package. This is real
but small relative to the 978+ MiB saved by excluding non-Bridge scope. Internal
deduplication alone is not an effective primary solution.

## 5. Bridge-only size boundaries

The measured frozen `IBKR_PAPER_BRIDGE` subtree is:

| Bridge scope | Files | Exact bytes | MiB |
|---|---:|---:|---:|
| Full subtree, including tests/docs/tools | 133 | 7,130,597 | 6.80 |
| Conservative Linux runtime/install essentials | 43 | 1,338,210 | 1.28 |
| TS-P0 operational hash scope | 32 | 1,136,314 | 1.08 |

The conservative Linux essentials measurement includes `bridge/`, `config/`,
`deploy/linux/`, and `requirements.lock`. The TS-P0 operational scope is the
scope declared by `IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py:38-43`:
`bridge/`, `requirements.txt`, `tools/run_bridge_p2.ps1`, and `config/`.

The full 6.80 MiB Bridge subtree is the safer first reduction target. Keeping
tests, documentation, deployment assets, and tools costs only about 5.5 MiB more
than an aggressively minimal runtime package and avoids a new class of missing
validation/import assets.

## 6. Repository, cache, runtime-state, and artifact distinctions

These layers must not be conflated:

| Local layer | Exact bytes | MiB/GiB | Relationship to release |
|---|---:|---:|---|
| Main workspace including `.git` | 9,301,513,096 | 8.66 GiB | Developer/research workspace, not deployable runtime |
| Main workspace excluding `.git` | 8,674,735,241 | 8.08 GiB | Includes ignored generated results and dependencies |
| Main `.git` directory | 626,727,930 | 597.69 MiB | Git objects/worktree metadata; not exported by `git archive` |
| `C:\R7FINAL` worktree | 1,069,262,103 | 0.996 GiB | Full repository worktree, not a Bridge package |
| Current physical `IBKR_PAPER_BRIDGE` directory | 13,871,649 | 13.23 MiB | Source plus ignored local state/caches |
| `C:\WPI_ARTIFACTS` | 5,208,923,013 | 4.851 GiB | Multiple extracted releases, a tar, and evidence/support files |

Large ignored dependency/cache roots in the main workspace are:

| Ignored local root | Exact bytes | MiB | Tracked files |
|---|---:|---:|---:|
| Dashboard `node_modules` | 708,320,943 | 675.51 | 0 |
| QuantLens `tools/.venvs` | 342,171,434 | 326.32 | 0 |
| Backtest `node_modules` | 10,315,212 | 9.84 | 0 |
| Dashboard `dist` | 2,352,058 | 2.25 | 0 |

These ignored paths increase local disk use but are not in the Git-built release.
The measured package contains neither a Python virtual environment nor a
wheelhouse. Its frozen `requirements.lock` is only 117,762 bytes. A per-release
Linux venv is installed separately by `install.sh`; its host size was not
measured because this inventory made no VPS contact.

The current local `IBKR_PAPER_BRIDGE/data` directory is 5,064,818 bytes
(4.83 MiB). It contains ignored SQLite/WAL/SHM databases, smoke data, and logs.
For example, `bridge.db-wal`, `bridge.db`, and `bridge.db-shm` together occupy
4,886,080 bytes. This is mutable runtime state, not immutable release content,
and must not be added to a future package.

## 7. Local artifact-copy inventory

`C:\WPI_ARTIFACTS` currently totals 5,208,923,013 bytes (4.851 GiB). The
dominant entries are:

| Entry | Exact bytes | MiB |
|---|---:|---:|
| Extracted `1adf9ae5...` | 1,051,904,669 | 1,003.17 |
| `2ce41e34...tar` | 1,047,265,280 | 998.75 |
| Extracted `2ce41e34...` | 1,033,362,481 | 985.49 |
| Extracted `ed3d0534...` | 1,033,359,494 | 985.49 |
| Extracted `ebada020...` | 1,033,359,158 | 985.49 |

Those five entries total 5,199,251,082 bytes. The extracted `2ce41e34` release
and its tar alone occupy 2,080,627,761 bytes (1.938 GiB).

Manifest comparison shows that `2ce41e34` shares:

- 7,053 unchanged files totalling 984.31 MiB with `ebada020`;
- 7,054 unchanged files totalling 984.31 MiB with `ed3d0534`.

This confirms large cross-release duplication on local disk. It does **not**
authorize deleting it. Some copies are accepted evidence, historical candidates,
or possible rollback inputs. The evidence/rollback role of every copy must be
recorded before it is moved to archival storage or removed from active disk.

## 8. Safe V2 package-scope proposal

### Recommended first target

For a new V2/new-candidate release only, make the immutable exact-SHA package
contain the complete `IBKR_PAPER_BRIDGE/` subtree, plus the generated
`RELEASE_SHA` and `RELEASE_SHA256SUMS` files.

Using the frozen candidate as a size model:

- current extracted release: 1,033,362,481 bytes;
- complete Bridge subtree: 7,130,597 bytes;
- conservative lower-bound saving before accounting for the smaller manifest:
  1,026,231,884 bytes (978.69 MiB);
- approximate reduction: 99.31%.

The new manifest would also be much smaller because it would describe roughly
133 source files rather than 7,059 members.

### Required fail-closed properties

The future builder must:

1. remain bound to one exact clean 40-hex commit;
2. export committed Git bytes, never copy a dirty worktree;
3. use a version-controlled exact subtree/scope contract;
4. fail if any required runtime, config, lock, installer, verifier, rollback,
   systemd, environment-template, or test asset is missing;
5. reject symlinks and other non-regular payload entries as the current builder
   does;
6. preserve the complete sorted per-file SHA-256 manifest and exact inventory
   equality checks;
7. preserve the line-ending/deterministic-export guarantees already established
   for the accepted build path;
8. preserve the secret denylist and never include local data, databases, WAL/SHM
   files, logs, caches, credentials, or environment files;
9. preserve the executing-installer-is-inside-the-accepted-payload check;
10. keep mutable state under `/var/lib/mtc-bridge`, logs under
    `/var/log/mtc-bridge`, and credentials outside the release tree.

### Optional later refinement

A separate staging-verification bundle and runtime-only bundle could reduce the
installed source tree toward 1.28 MiB. That should be considered only after the
full Bridge-subtree package is proven. A 6.8 MiB release is already operationally
small, and a second artifact identity adds missing-file, provenance, and rollback
complexity.

The current tar is uncompressed. Transport compression may later be benchmarked,
but it does not reduce expanded release disk use and would introduce another
identity/extraction surface. After a 99.3% scope reduction, compression may not
be worth the added validation burden.

## 9. Frozen V1, evidence, and rollback boundaries

The accepted/frozen V1 bytes must remain unchanged. Applying a scope change to
the existing candidate would invalidate at least:

- the release directory identity;
- `RELEASE_SHA256SUMS` and its SHA-256;
- the 7,059-member/7,060-file inventory;
- the tar byte count and tar SHA-256;
- Gate-A and WP-I evidence bound to the full release tree;
- preregistered release/venv sweeps and expected path inventory;
- installed-release and rollback records.

Therefore the slim format must start with a new commit and new candidate identity.
The current V1 artifact remains an immutable historical/rollback object until its
retention contract says otherwise.

Before archiving any local artifact copy, create a retention ledger containing:

- candidate SHA and status: accepted, rejected, superseded, or rollback target;
- extracted path and/or tar path;
- bytes and SHA-256 of each retained object;
- release-manifest SHA-256;
- evidence records that reference the local path;
- whether the artifact exists on any host;
- whether it is the only reproducible rollback input;
- archival destination and a successful restoration/hash-verification record.

Retain at minimum the active accepted candidate and one independently verified
rollback target in recoverable immutable form. Do not assume that Git history
alone replaces an accepted release artifact: the package manifest, deterministic
export rules, and rollback evidence are separate identities.

## 10. Required T0 implementation and validation plan

Any change to `package.sh`, `install.sh`, `verify.sh`, `rollback.sh`, release
manifests, or artifacts is **T0** because it changes a host-touching deployment
surface. Documentation approval alone does not authorize implementation or host
contact.

For a future authorized work package:

1. **Gate 1 / freeze:** record T0 scope; freeze V1 and its evidence byte-for-byte;
   name the new V2 candidate and exact allowed subtree contract.
2. **Counterpart implementation:** modify the builder/contracts/tests in an
   isolated clean worktree. Do not mutate the old artifact.
3. **Determinism proof:** build twice from the same exact commit in fresh empty
   destinations and require identical member list, file bytes, manifest bytes,
   and artifact hash.
4. **D026 RED/GREEN:** demonstrate that the new regression tests fail against
   the whole-repo predecessor or deliberate scope mutations and pass only with
   the exact Bridge-only scope. Mutations must include omitted runtime file,
   added unrelated research file, symlink/special entry, dirty-worktree input,
   path/metacharacter handling, CRLF drift, manifest omission, and extra-file
   injection.
5. **Installer validation:** prove dry-run and real install consume only
   hash-bound assets from the accepted slim payload; verify lock, sealed release,
   masked/unstarted DISARMED first-start unit, loopback-only source, no secret,
   and exact inventory.
6. **Cross-format rollback:** prove a new slim release can roll back to the
   retained full-tree V1 target and that each release is verified against its own
   accepted manifest without weakening state preservation or start/ARM gates.
7. **Full local suite:** run the required Bridge/deployment suite and record any
   pre-existing failures separately from the package change.
8. **Two independent flagship audits:** fresh `claude-opus-5` xhigh and fresh
   `gpt-5.6-sol` xhigh; both must execute the mandated suite and accept, with no
   unresolved Lead-reproduced required finding.
9. **Fresh Ubuntu evidence:** only after separate owner deployment authorization,
   execute the accepted exact artifact on an expendable Ubuntu 24.04 staging
   host, still DISARMED, and reproduce install, verify, restart/state, rollback,
   immutability, listener, and secret-scan evidence.
10. **New identity only:** publish new candidate/artifact/manifest/tar byte and
    SHA records. Never relabel old V1 evidence as applying to the slim format.

## 11. Conclusion

The Bridge package can likely be reduced safely by about 99.3% without removing
Bridge tests or documentation. The dominant waste is architectural: the release
builder packages the whole monorepo, including QuantLens research outputs and
backtest data that the Bridge runtime does not use. The safest route is a new,
fully audited Bridge-subtree release format for V2 while keeping frozen V1 and
its rollback/evidence chain untouched.
