Status: DESIGN ONLY — NO CODE, NO MERGE, NO ACCEPTANCE

# Bridge release-line integration design — 2026-08-15

## Decision

Use a **Gate-A-forward merge into the repaired WP-I line**, then resolve only the
document/test overlaps and prove the expected blob identities before building a
candidate. Do not reimplement the Gate-A behavior.

At the three frozen subjects named in the kickoff, the Bridge union is 33 paths:

- 10 Gate-A-only paths;
- 1 WP-I-only path;
- 1 path changed by both sides (`deploy/linux/README.md`), which Git merges
  without conflict markers; and
- 21 paths where WP-I is the 2026-07-31 split-point version and is simply stale.

The current merge shape is therefore small despite the large diff. Gate-A is a
descendant of `origin/master`, so bringing Gate-A forward also brings the
master TS-P1-009 kill-evidence work that WP-I lacks. The release must preserve
the Gate-A executable blobs exactly, except for later separately accepted test
repairs. Evidence commands and their real outputs are in §8.

This design record is documentation only. The future integrated release is a
T0 surface: deployment/host/network, application ARM refusal, broker-start
suppression, durable state, and release identity are involved. It therefore
requires two fresh independent flagship audits (`claude-opus-5` and
`gpt-5.6-sol`, both xhigh) and fresh Gate-A execution. This file grants none of
that authority.

## 1. Frozen subjects and graph

| Alias | Full commit | Meaning |
|---|---|---|
| `M` | `637307e83951ffe23e768ed8e50ddaf8712b0660` | `origin/master`; TS-P1-009 kill-evidence line |
| `G` | `2ce41e34bceb599d80af24c5c33d835820ec321b` | Gate-A staging-accepted candidate |
| `W` | `678d4be22ddde2201948de0d60343c1edfa85a06` | frozen WP-I HEAD in this worktree |
| `B` | `4d2228cf8985ce755c398cceff23f777a99d5404` | merge base of `W` and `G`; 2026-07-31 split point |

Verified topology:

```text
G is not in M                         rc=1
M is not in W                         rc=1
merge-base(W,G)                       4d2228cf8985ce755c398cceff23f777a99d5404
merge-base(M,G)                       M
merge-base(M,W)                       B
```

Thus `G` already contains `M`; `W` does not. Gate-A acceptance is explicitly
limited to the exact candidate and staging: `GATE_A_A9_PASS_FINAL_2026-08-09D.md:5-8`
states A-0..A-9 PASS for `2ce41e34` and denies merge/live/ARM/order authority;
`:56-65` says the candidate remained unchanged and repeats that boundary.

## 2. Exact three-way Bridge map

Blob notation is `<10-hex Git blob>/<bytes>`; `—` means absent. These are the
real `git rev-parse <ref>:<path>` and `git cat-file -s` results (§8.3). “Win”
means the intended content in the future release, not an authorization to edit.

### 2.1 Gate-A-only work — 10 paths

For every row here, `M` and `W` are byte-identical to `B`. The Gate-A blob wins
because it is the only line carrying the accepted implementation/evidence.

| Path | `M` | `G` | `W` | Release winner and reason |
|---|---|---|---|---|
| `IBKR_PAPER_BRIDGE/bridge/app.py` | `6d0abc6351/9563` | `572c4178fe/11673` | `6d0abc6351/9563` | **`G` exact blob.** Resolves explicit/env start mode, reports credential-free DISARMED status, rejects broker/dry-run injection, and skips broker construction (`G:bridge/app.py:30-50,112-149`). |
| `IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template` | `fbf8cb833c/2254` | `c03d6e47ab/2492` | `fbf8cb833c/2254` | **`G` exact blob.** Documents that `MTC_BRIDGE_START_MODE` is unit-owned and forbidden in the env file. |
| `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh` | `7d5aa166ac/8153` | `db11010a24/8236` | `7d5aa166ac/8153` | **`G` exact blob.** Writable-tree inventory ignores symlinks but fails closed when `find` cannot inventory (`G:.../common.sh:98-99`). |
| `IBKR_PAPER_BRIDGE/deploy/linux/package.sh` | `150c18c364/3324` | `add6478d33/6351` | `150c18c364/3324` | **`G` exact blob.** Pins LF export/tar mode/locale, compares Git-tree and payload inventory, rejects CR bytes, and fails closed on inspection errors (`G:.../package.sh:80-82,116-119,128-163`). |
| `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template` | `b175ced7f3/3489` | `c18232549d/3628` | `b175ced7f3/3489` | **`G` exact blob.** Pins `Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed` (`:42`). |
| `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh` | `bce1f0e23e/9846` | `5cfefd7092/10144` | `bce1f0e23e/9846` | **`G` exact blob.** Rejects env-file override and requires the unit pin (`:143-146,171`). |
| `IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py` | — | `ce0ae7c24f/7952` | — | **`G` exact blob.** Seven tests cover explicit selection, environment/CLI precedence, no credential/broker lookup, truthful status, durable ARM refusal, ordinary credentialed behavior, and invalid-mode fail-fast. |
| `IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py` | `a1486d759d/20235` | `64e25888ba/34388` | `a1486d759d/20235` | **`G` content plus the separately accepted anomaly repair.** Gate-A adds fail-closed writable-tree/package/CR/locale/tar-umask/start-mode tests. Never take the stale `W` whole-file blob over `G`. |
| `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py` | `edc02108c9/30436` | `07de7b206f/55214` | `edc02108c9/30436` | **`G` content plus the separately accepted anomaly repair.** Gate-A adds schema-attachment, hot-WAL/WAL-index, damaged-header, and concurrent-writer tests. Never take the stale `W` whole-file blob over `G`. |
| `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` | `aaa2918229/41831` | `26c077e650/49129` | `aaa2918229/41831` | **`G` exact blob.** Rejects unusable hot-WAL sidecars before connecting, validates WAL-index structure/checksum/salts, and touches `sqlite_master` before capture (`:237,270,318,368-386`). |

### 2.2 WP-I-only work — 1 path

| Path | `M` | `G` | `W` | Release winner and reason |
|---|---|---|---|---|
| `IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md` | — | — | `8db2e6dd7e/19114` | **`W` exact blob, retained as dated historical static evidence.** It identifies itself as `PRE-GATE-A / STATIC ONLY`, frozen to `M` and old candidate `1adf9ae5` (`W:.../SECURITY_BASELINE.md:4-6`), and says only Ubuntu/runtime proof remained (`:299`). Do not relabel those old identities as the new release; a new freeze record must carry new identities. |

### 2.3 Both sides changed — one compatible synthesis, zero textual conflicts

| Path | `M` | `G` | `W` | Release winner and reason |
|---|---|---|---|---|
| `IBKR_PAPER_BRIDGE/deploy/linux/README.md` | `d27c622984/8801` | `f3f1d75e7e/9191` | `666b79d834/9185` | **New merged documentation blob.** Preserve Gate-A’s unit-owned start-mode/override prohibition and WP-I’s `SECURITY_BASELINE.md` inventory/limitations. Also replace the now-false unqualified “never been executed” sentence with time-scoped truth: `G` was executed and staging-accepted; the new integrated SHA is unexecuted/unaccepted until rerun. Details in §3. |

There are **no genuinely incompatible same-region edits** at these frozen
subjects. Git reports this README as “changed in both” but emits zero conflict
markers (§8.4). It still needs a deliberate human resolution because an
automatic concatenation would retain stale status prose.

### 2.4 WP-I is stale — 21 paths

The first row is layered: `W=B`, `M` adds TS-P1-009 routes, and `G` adds the
credential-free ARM refusal on top. In the other 20 rows, `M=G` exactly and
`W=B`. The master/Gate-A blob wins because using `W` would delete already-merged
kill-evidence work.

| Path | `M` | `G` | `W` | What the lines have; release winner |
|---|---|---|---|---|
| `IBKR_PAPER_BRIDGE/bridge/api/routes.py` | `7e25037801/10339` | `140bf003ec/10666` | `24a445ec70/9986` | `W` is pre-TS-P1-009; `M` adds durable KILL/ACK routes; `G` additionally refuses ARM with application HTTP 409 in credential-free mode (`G:routes.py:90-96`). **Win: `G` exact.** |
| `IBKR_PAPER_BRIDGE/README.md` | `cfc15b2121/4290` | same | `17dff82860/3080` | `M/G` document durable KILL capability and ACK (`M:README.md:22,57-65`); `W` lacks it. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/bridge/broker/base.py` | `0698e4862e/11699` | same | `81960d68ba/10045` | `M/G` define the kill-recovery broker protocol (`:280`); `W` is pre-protocol. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py` | `855a17cd83/102732` | same | `8a841ff9e5/94690` | `M/G` add epoch-guarded kill cancel/flatten and evidence capture (`:1357,1479,1840`); `W` lacks them. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/bridge/broker/mock.py` | `295c0a9cd0/47590` | same | `2b7076893f/42440` | `M/G` mirror kill cancel/flatten/evidence semantics in the mock (`:536,639,948`); `W` lacks them. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/bridge/engine/engine.py` | `0c115ff184/57815` | same | `11fa9c1258/49180` | `M/G` orchestrate the durable kill episode (`:429`) and recovery/status paths; `W` is the old engine. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/bridge/engine/orders.py` | `608a3afe10/243687` | same | `5deb64dd14/153210` | `M/G` contain durable owned-only kill action, epoch, recovery, mutation fencing, and event containment (`:1619,1724`); `W` lacks that large safety body. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py` | `ea3ff95d93/71179` | same | `0c4f5e31c3/68691` | `M/G` expose kill-evidence capture in full reconciliation (`:209`); `W` lacks it. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/bridge/engine/types.py` | `2927968d7b/66793` | same | `ba0fc62527/64369` | `M/G` define kill action/terminal/epoch/capture types (`:538,545,558,1109`); `W` lacks them. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/bridge/store/db.py` | `ae5eb1b7ab/429968` | same | `8080a32aae/293711` | `M/G` include v9 kill-evidence schema, conflict types, epoch open/CAS, lifecycle evidence, and ACK (`:556,5403,7231`); `W` is pre-v9. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md` | `a09b22bedb/55979` | same | `00b62f18b2/52666` | `M/G` document KILL latch, persistence, and recovery (`:140,173`); `W` is older. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md` | `b02694c2e6/7702` | same | — | `M/G` contain the TS-P1-009 recovery contract (`:1-19`); `W` has no file. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md` | `23480737ee/21326` | same | — | `M/G` contain the TS-P1-009B epoch contract (`:1-23`); `W` has no file. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/tests/test_api.py` | `40d31925ac/6444` | same | `d9da63e7f6/2482` | `M/G` test persistent KILL and safe/stale ACK behavior (`:69,129,163,177`); `W` lacks them. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py` | `817afe17b0/166289` | same | `902f00ff44/55792` | `M/G` test kill ordering, latch precommit, epoch/restart/concurrency and recovery; `W` lacks them (`:99,446,472,504`). **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py` | `3851340462/105221` | same | `b59483a670/91402` | `M/G` test guarded sends and exact kill evidence (`:138,2010,2026,2156`); `W` lacks them. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/tests/test_mock_broker.py` | `bed96cea0f/15561` | same | `bb62989ce4/14176` | `M/G` test authoritative mock kill-mutation fixtures (`:197`); `W` lacks them. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py` | `9e50c1b51c/13778` | same | `f2e3a32171/12090` | `M/G` add kill-mid-await/pre-zero-submit failure drills (`:36,40`); `W` lacks them. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py` | `7b0b9ea36d/127020` | same | `42c55c09af/94693` | `M/G` add duplicate/restart/query-only kill recovery around partial fills (`:2742,2765,2796`); `W` lacks it. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/tests/test_reconciliation.py` | `9e6b015d84/59179` | same | `ce016ca5f1/57012` | `M/G` test in-epoch capture, interlock, invalid status and capture start (`:189,1124,1363,1468`); `W` lacks it. **Win: `M/G` exact.** |
| `IBKR_PAPER_BRIDGE/tests/test_store.py` | `d911d983f0/134088` | same | `a2b8b0a7bb/104805` | `M/G` test opt-in v9, epoch ownership and legacy reopen behavior (`:189,268,428,441`); `W` lacks it. **Win: `M/G` exact.** |

Count check: 10 + 1 + 1 + 21 = **33**, equal to the Git-derived union.

## 3. Conflict/overlap list

### `IBKR_PAPER_BRIDGE/deploy/linux/README.md`

**What Gate-A did.** `G:.../README.md:112-116` says:

> **Start mode is unit-owned, not env-owned.** The first-start unit pins
> `MTC_BRIDGE_START_MODE=credential_free_disarmed` via `Environment=`.

It then states that an env-file assignment would override the hashed accepted
mode, so `verify.sh` rejects bare or exported assignments.

**What WP-I did.** `W:.../README.md:24` adds the `SECURITY_BASELINE.md` inventory
row. Lines `125-127` say it is PRE-GATE-A/static-only evidence, not Ubuntu,
built-payload, deployment, runtime, or destination-egress-control proof.

**Compatibility.** The intents are compatible and affect different insertions.
The legacy three-way merge reports one `changed in both` path and zero conflict
markers. The correct merged document must preserve both additions.

**Additional status correction required.** Both sides retain an old statement:

```text
G:README.md:123-124  These assets have never been executed ... No Ubuntu run,
                     no install.sh invocation, no systemctl call has happened.
W:README.md:118-119  same claim
```

That is no longer an honest unqualified release statement because the exact
Gate-A candidate later ran on staging and received bounded staging acceptance
(`GATE_A_A9_PASS_FINAL_2026-08-09D.md:5-8,56-65`). The merged result should say,
in substance:

- the old WP-I static baseline remains dated historical evidence;
- `2ce41e34` was installed/executed on the disposable Gate-A staging host and
  passed A-0..A-9 under the recorded boundary; and
- the new integrated SHA has not been installed, run, or accepted and must
  repeat the full gate.

This is a documentation correction, not authority or transferred acceptance.

### No other conflict at the frozen subjects

`bridge/api/routes.py` is all-different by blob, but it is not a same-region
WP-I/Gate-A conflict: `W` equals `B`; `M` adds KILL/ACK; `G` adds the ARM refusal
on top. The correct result is the exact `G` blob.

### Repair-branch caveat

At inspection time, branch `codex/bridge-suite-anomaly-repairs-20260815` still
points exactly at `W`, with no Bridge diff (§8.5). Its expected repairs concern
`tests/test_linux_deployment.py` and `tests/test_wal_state_bundle.py`
(`AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:84-103,118-145`), and Gate-A
also changes both files. When the repair commit exists, recompute the three-way
map against that exact repaired tip. Those two files may then become real
both-changed test files.

Resolution rule for either test file: start from the full `G` content, replay
only the independently accepted anomaly repair, and prove that all Gate-A-added
test functions remain present. Never resolve by taking the repaired WP-I
whole-file blob, because that would silently delete Gate-A coverage. The repair
tests must carry their own D026 RED/GREEN evidence.

## 4. Integration routes considered

| Route | Safety assessment | Speed assessment | Disposition |
|---|---|---|---|
| Rebuild Gate-A behavior on the current line | Worst. `W` lacks master’s TS-P1-009 work and all 10 Gate-A-only files/changes. Reauthoring application/deploy/WAL safety behavior discards byte identity and creates a large new protected diff. | Slowest: many product/test files plus full requalification. | **Reject.** |
| Merge Gate-A forward into WP-I and resolve | Best overall. Because `G` descends from `M`, one merge restores master and Gate-A together. At the frozen subjects, 31 of 33 differing Bridge paths can remain exact `G` blobs; only the WP-I-only baseline and merged README differ. Full WP-I lineage/provenance is retained. | Fast. Current merge analysis has one both-changed README and zero conflict markers; anomaly repairs add a bounded test replay. | **Recommend.** |
| Cut from Gate-A and forward-port WP-I Bridge work | Strong for Bridge executable safety and superficially the fewest Bridge edits (one new file and README synthesis). But it can omit non-Bridge WP-I provenance/readiness material unless a second reconciliation is done, making completeness easier to get wrong. | Fastest for Bridge files alone; not necessarily fastest for a complete release line. | Viable fallback only if the release contract explicitly excludes the rest of WP-I. |

**Least likely to lose a proven safety property:** the recommended Gate-A-forward
merge with an explicit post-merge blob fence. It carries the accepted lineage
and does not reconstruct safety code.

**Fastest complete-line route:** the same merge. Cutting from Gate-A is a little
faster only under the narrower assumption that all non-Bridge WP-I work may be
omitted. That assumption is not established, so it is not the recommendation.

### Recommended future sequence (not executed here)

1. Freeze the exact accepted anomaly-repair commit and its D026 evidence. If it
   is not yet accepted, do not call it part of the release input.
2. Create an integration branch from that repaired WP-I tip.
3. Merge `G` forward. Resolve README as §3 specifies. If the two repaired test
   files overlap, preserve `G` wholesale and replay the narrow repair hunks.
4. Run a blob fence over all 33 paths:
   - expected exact `G` blobs for 29 unaffected rows plus the two Gate-A test
     bases before their repair hunks;
   - expected exact `W` blob for `SECURITY_BASELINE.md`;
   - new reviewed blob for the README; and
   - new reviewed blobs only for the two anomaly-repaired tests, if changed.
   Any other Bridge blob change is a hard scope failure.
5. Recompute the complete tree diff and release identity. Build the immutable
   artifact from the frozen full SHA; verify tree inventory, LF/CR contract,
   manifest, package reproducibility, and absence of untracked input.
6. Run the local matrix in §6, then two fresh T0 flagship audits over the exact
   candidate and evidence. No auditor may accept without executing the mandated
   suite.
7. Only under separate host authority, rerun A-0 through A-9 on the exact
   candidate, preserve new logs/hashes, and issue a new candidate-bound verdict.

## 5. Re-acceptance: what transfers and what must rerun

**No A-0..A-9 PASS transfers.** The integrated tree and artifact have a new
commit, manifest, file count/bytes, and at least one new payload file. Historical
Gate-A reports, run-kit designs, and old D026 evidence may be reused as templates
or supplemental provenance only. They are not a PASS for new bytes.

| Check | Fresh requirement on the integrated candidate | Carry-over allowed |
|---|---|---|
| **A-0 identity** | Rebuild from the frozen full SHA; recompute source and transferred artifact hash, release marker, manifest hash, every manifest entry, regular/non-regular counts, total bytes, and CR/LF evidence. | Criteria and old command design only. **No old hash/count/PASS.** |
| **A-1 clean-host preconditions** | Re-establish expendable Ubuntu 24.04, locked Python/tooling, declared dependency-fetch boundary, UFW posture, and absence of old install paths, users, processes, units, listeners and residue. | Host requirement text only. Host state is time-varying; **no PASS.** |
| **A-2 immutable install** | Fresh dry-run side-effect check; install only from the new artifact; run `verify.sh`; prove no ad-hoc edit; exact release/venv sealing; masked/inactive/unstarted unit; no credential material; new start-mode override RED/restore/GREEN evidence. | Accepted procedure/failure predicates only. **No install PASS.** |
| **A-3 Linux suites** | Run the exact frozen Bridge suite under the locked interpreter/pytest, record every failure node ID, and require the newly repaired anomaly tests to be green. Run focused credential-free, deployment, WAL bundle, kill-evidence, and store/reconcile matrices. Do not carry the old `2 failed, 1358 passed` count; it belongs to `G` and that runtime. | Old node IDs/counts are historical comparison only. **No suite PASS.** |
| **A-4 credential-free DISARMED start** | Reprove all seven conditions from `GATE_A_A4_PASS_2026-08-08C.md:97-110`: active/static service; one `127.0.0.1:8790` listener; exact credential-free DISARMED API; application-level HTTP 409 ARM refusal; no broker attempt; persisted DISARMED/healthy DB with unchanged state version; actual selected start mode recorded. | Old seven-condition structure and refusal text as expectations only. **No runtime PASS.** |
| **A-5 restart safety** | Repeat the bounded SIGKILL/no-auto-restart/explicit-start sequence; prove old PID gone, `Restart=no`, `NRestarts=0`, one start, exact API/listener recovery, DB quick-check, unchanged durable DISARMED state and table counts (`GATE_A_A5_PASS_2026-08-09E.md:23-45`). | Run-kit design only. **No restart PASS.** |
| **A-6 reconcile/startup** | Repeat isolated empty/mock-broker startup; prove no raise/hang/leftover/deferred queue, no credential resolver or network, temp DB integrity/cleanup, and production service unchanged (`GATE_A_A6_PASS_2026-08-09D.md:30-45,47-56,67-74`). | Old scope boundary may be reused; **no PASS.** |
| **A-7 observability** | Reprove API/DB state equality, DB quick-check/schema, truthful status, bounded journal evidence, regular non-empty logs, active service, and one loopback listener (`GATE_A_A7_PASS_2026-08-09D.md:30-60`). | Old expected fields only. **No observability PASS.** |
| **A-8 loopback exposure** | Repeat both halves: host-side socket/firewall inventory with exactly one loopback listener and no wildcard/non-loopback bind, plus independent external probe where SSH is reachable and port 8790 is not (`GATE_A_A8_PASS_2026-08-09D.md:34-42,44-86`). | Probe contract only. **No exposure PASS.** |
| **A-9 no secrets** | Re-run the content-redacted nine-category scan over the new installed release and `/etc/mtc-bridge`; require `rc=1 matches=0` per category, aggregate zero, no path/error/fail blocks, and independently verify new evidence identity (`GATE_A_A9_PASS_FINAL_2026-08-09D.md:31-54`). | Pattern/category list only. The new README/baseline bytes alone invalidate transfer of the old scan. **No scan PASS.** |

After A-9, issue a new final record naming the exact integrated full SHA and
artifact identities. It may grant staging acceptance only. It must not imply
merge, production, credential, ARM, broker, order, TESTNET/mainnet, or economic
authority.

## 6. Local matrix before host rerun

The exact commands must be frozen by the implementation package, but the matrix
must include at least:

1. Blob-fence and scope checks over the 33-path map; full-tree clean-input proof.
2. Syntax/import checks for Python and every deploy shell file.
3. Focused tests:
   `test_credential_free_disarmed.py`, `test_linux_deployment.py`,
   `test_wal_state_bundle.py`, API KILL/ACK, engine kill lifecycle,
   broker/mock kill guards, reconcile, and store v9/epoch tests.
4. The full Bridge suite under the locked release runtime. Zero unexplained
   failures; record exact node IDs and environment, not counts alone.
5. D026 RED/GREEN for each anomaly repair against the exact pre-fix behavior or
   an equivalent deliberate mutation. A test without executed RED is
   supplemental, not closure evidence.
6. At least two package builds from the same SHA under deliberately different
   locale and relevant Git/tar settings, proving identical release inventory,
   modes, and `RELEASE_SHA256SUMS`; include CR-byte and inspection-failure RED
   arms.
7. Credential-free application matrix: CLI/env precedence, invalid mode,
   no broker/credential lookup, truthful status, current-version ARM HTTP 409,
   unchanged state, and ordinary credentialed path preservation.
8. WAL matrix: cold source, genuine hot WAL/SHM, absent/truncated/damaged/
   unrelated index, checksum/salt mutation, and concurrent-writer refusal.

The final candidate is T0. Both flagship auditors must independently execute
the mandatory matrix from the exact candidate. A read-only opinion without
execution is BLOCK, not acceptance.

## 7. Hour estimate

Assumptions: the two known suite anomalies are already correctly repaired with
D026 evidence; no new product defect appears; the two flagship auditors can run
in parallel; and host authority/availability is supplied separately.

| Work | Labor hours | Likely elapsed hours | Basis |
|---|---:|---:|---|
| Integration | 3–5 | 3–5 | Freeze repaired tip; Gate-A-forward merge; README synthesis; semantic replay of at most two test repairs; 33-path blob fence; freeze identities. |
| Test repair | 0–3 | 0–3 | The known two are assumed fixed. This is contingency for merge-induced fixture/count issues only; a product finding re-estimates the plan. |
| Local matrix runs | 5–8 | 4–7 | Focused matrices, full locked suite, package reproducibility/falsification, D026 review, and a repeat clean run. |
| T0 audit rounds | 8–16 | 4–10 | Two xhigh flagships per round, parallel where possible; assumes one initial round and at most one bounded repair/re-audit. The policy allows up to three rounds, not an automatic three-round budget. |
| **Candidate integration + local acceptance subtotal** | **16–32** | **11–25** | Before any host execution. |
| Fresh staging A-0..A-9 | 5–9 | 5–9 | Separate owner-authorized host phase, including artifact transfer verification, install/suite/start/restart/reconcile/observability/exposure/scan and evidence preservation. |
| **End-to-end estimate** | **21–41** | **16–34** | To a newly staging-accepted exact candidate, assuming no new required finding. |

If a flagship finds a product/deploy defect, add roughly 6–12 labor hours per
bounded repair/re-audit round. Stop after the T0 cap is exhausted; do not turn
the upper estimate into implied authority for extra rounds.

## 8. Evidence ledger — commands and real output

All commands below were read-only and run in `C:\RELDES`. No merge, checkout,
index update, commit, host, network, service, credential, broker, ARM, order, or
deployment command was run.

### 8.1 Worktree identity and cleanliness

```powershell
git -C C:\RELDES rev-parse HEAD
git -C C:\RELDES status --porcelain
```

```text
678d4be22ddde2201948de0d60343c1edfa85a06
<no status output>
```

### 8.2 Refs, ancestry, merge bases and supplied stats

```powershell
git -C C:\RELDES rev-parse origin/master
git -C C:\RELDES rev-parse 2ce41e34bceb599d80af24c5c33d835820ec321b
git -C C:\RELDES rev-parse HEAD
git -C C:\RELDES merge-base --is-ancestor 2ce41e34 origin/master
git -C C:\RELDES merge-base --is-ancestor origin/master HEAD
git -C C:\RELDES merge-base HEAD 2ce41e34
git -C C:\RELDES merge-base origin/master 2ce41e34
git -C C:\RELDES merge-base origin/master HEAD
```

```text
637307e83951ffe23e768ed8e50ddaf8712b0660
2ce41e34bceb599d80af24c5c33d835820ec321b
678d4be22ddde2201948de0d60343c1edfa85a06
gatea_in_master_rc=1
master_in_head_rc=1
4d2228cf8985ce755c398cceff23f777a99d5404
637307e83951ffe23e768ed8e50ddaf8712b0660
4d2228cf8985ce755c398cceff23f777a99d5404
```

```powershell
git -C C:\RELDES diff --stat 637307e8 2ce41e34 -- IBKR_PAPER_BRIDGE/
git -C C:\RELDES diff --stat HEAD 2ce41e34 -- IBKR_PAPER_BRIDGE/
```

```text
12 files changed, 1642 insertions(+), 24 deletions(-)
33 files changed, 14369 insertions(+), 621 deletions(-)
```

### 8.3 Union/category derivation and blob identities

The derivation unions `git diff --name-only` for all three pairs, compares each
blob to `B`, and uses `git rev-parse <ref>:<path>` plus `git cat-file -s`.

```text
UNION_PATHS=33
gatea_only=10
wpi_only=1
both_changed=1
wpi_stale=21
other=0
```

Real blob output, in `M`, `G`, `W` order:

```text
bridge/api/routes.py                 7e25037801/10339  140bf003ec/10666  24a445ec70/9986
bridge/app.py                        6d0abc6351/9563   572c4178fe/11673  6d0abc6351/9563
bridge/broker/base.py                0698e4862e/11699  0698e4862e/11699  81960d68ba/10045
bridge/broker/hyperliquid.py         855a17cd83/102732 855a17cd83/102732 8a841ff9e5/94690
bridge/broker/mock.py                295c0a9cd0/47590  295c0a9cd0/47590  2b7076893f/42440
bridge/engine/engine.py              0c115ff184/57815  0c115ff184/57815  11fa9c1258/49180
bridge/engine/orders.py              608a3afe10/243687 608a3afe10/243687 5deb64dd14/153210
bridge/engine/reconcile.py           ea3ff95d93/71179  ea3ff95d93/71179  0c4f5e31c3/68691
bridge/engine/types.py               2927968d7b/66793  2927968d7b/66793  ba0fc62527/64369
bridge/store/db.py                   ae5eb1b7ab/429968 ae5eb1b7ab/429968 8080a32aae/293711
deploy/linux/env/mtc-bridge.env.template fbf8cb833c/2254 c03d6e47ab/2492 fbf8cb833c/2254
deploy/linux/lib/common.sh           7d5aa166ac/8153   db11010a24/8236   7d5aa166ac/8153
deploy/linux/package.sh              150c18c364/3324   add6478d33/6351   150c18c364/3324
deploy/linux/README.md               d27c622984/8801   f3f1d75e7e/9191   666b79d834/9185
deploy/linux/SECURITY_BASELINE.md    ABSENT            ABSENT             8db2e6dd7e/19114
deploy/linux/systemd/mtc-bridge-first-start.service.template b175ced7f3/3489 c18232549d/3628 b175ced7f3/3489
deploy/linux/verify.sh               bce1f0e23e/9846   5cfefd7092/10144  bce1f0e23e/9846
docs/01_ARCHITECTURE.md              a09b22bedb/55979  a09b22bedb/55979  00b62f18b2/52666
docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md b02694c2e6/7702 b02694c2e6/7702 ABSENT
docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md 23480737ee/21326 23480737ee/21326 ABSENT
README.md                            cfc15b2121/4290   cfc15b2121/4290   17dff82860/3080
tests/test_api.py                    40d31925ac/6444   40d31925ac/6444   d9da63e7f6/2482
tests/test_credential_free_disarmed.py ABSENT           ce0ae7c24f/7952   ABSENT
tests/test_engine_dryrun.py          817afe17b0/166289 817afe17b0/166289 902f00ff44/55792
tests/test_hyperliquid_broker.py     3851340462/105221 3851340462/105221 b59483a670/91402
tests/test_linux_deployment.py       a1486d759d/20235  64e25888ba/34388  a1486d759d/20235
tests/test_mock_broker.py            bed96cea0f/15561  bed96cea0f/15561  bb62989ce4/14176
tests/test_p1_failure_drills.py      9e50c1b51c/13778  9e50c1b51c/13778  f2e3a32171/12090
tests/test_partial_fill_protection.py 7b0b9ea36d/127020 7b0b9ea36d/127020 42c55c09af/94693
tests/test_reconciliation.py         9e6b015d84/59179  9e6b015d84/59179  ce016ca5f1/57012
tests/test_store.py                  d911d983f0/134088 d911d983f0/134088 a2b8b0a7bb/104805
tests/test_wal_state_bundle.py       edc02108c9/30436  07de7b206f/55214  edc02108c9/30436
tools/wal_state_bundle.py            aaa2918229/41831  26c077e650/49129  aaa2918229/41831
```

The per-file descriptions in §2 were checked with `git log B..M -- <path>`,
`git log M..G -- <path>`, and symbol-level `git show <ref>:<path>` reads. The
master changes are the TS-P1-009/009B durable KILL sequence; the Gate-A changes
are deterministic packaging, WAL capture safety, and credential-free DISARMED
startup. `git grep` also proved the start-mode string absent at `M` and `W` and
present at `G`:

```text
HEAD_credential_free_disarmed_rc=1
MASTER_credential_free_disarmed_rc=1
G:bridge/api/routes.py:90: if ... credential_free_disarmed
G:bridge/app.py:32: CREDENTIAL_FREE_DISARMED_START_MODE = "credential_free_disarmed"
G:deploy/linux/systemd/mtc-bridge-first-start.service.template:42:
  Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed
```

### 8.4 Conflict proof

Read-only legacy-form merge analysis:

```powershell
git -C C:\RELDES merge-tree B W G
```

Parsed result:

```text
changed in both
  base   100644 d27c622984a0b04a94e4a9a65b2ce8d1134f0bd2 IBKR_PAPER_BRIDGE/deploy/linux/README.md
  our    100644 666b79d834f50433cd0cba7c88224fb674fdbb56 IBKR_PAPER_BRIDGE/deploy/linux/README.md
  their  100644 f3f1d75e7e4369609cd0eb299466b2ceb62a0a16 IBKR_PAPER_BRIDGE/deploy/linux/README.md
CHANGED_IN_BOTH_COUNT=1
CONFLICT_MARKER_COUNT=0
```

### 8.5 Pending repair-line identity

```powershell
git -C C:\RELDES show-ref --verify refs/heads/codex/bridge-suite-anomaly-repairs-20260815
git -C C:\RELDES diff --name-status W codex/bridge-suite-anomaly-repairs-20260815 -- IBKR_PAPER_BRIDGE/
```

```text
678d4be22ddde2201948de0d60343c1edfa85a06 refs/heads/codex/bridge-suite-anomaly-repairs-20260815
<no Bridge diff>
```

Therefore this design assumes the repairs will be fixed as requested, but does
not pretend a repair commit or its evidence already exists at inspection time.

## 9. Final boundary

This document chooses an integration design only. It does not merge any line,
change product code, build an artifact, contact a host, run a service, inspect a
credential, connect a broker/exchange, ARM, place an order, authorize TESTNET or
mainnet, alter Pine/parity/MTC/trading behavior, merge to master, push, or grant
economic action.
