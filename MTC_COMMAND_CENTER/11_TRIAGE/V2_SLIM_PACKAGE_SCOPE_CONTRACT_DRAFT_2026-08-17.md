# V2 slim Bridge package scope contract — draft — 2026-08-17

## 0. Status and boundary

**Status: design draft only.** This document records a conservative future V2
package contract. It does not authorize implementation, candidate creation,
artifact replacement, deployment, host contact, installation, service action,
ARM, exchange contact, cleanup, or deletion.

The frozen V1 package, tar, manifests, installed release, venv, evidence, and
rollback target remain byte-for-byte unchanged. The measured size/root-cause
inventory is in
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_PACKAGE_SIZE_INVENTORY_2026-08-17.md`.

This draft was derived from committed files at:

- repository `HEAD`: `8c06130720077807963513e02781b72b25ec0cd0`;
- 7,994 tracked blobs totalling 1,045,834,274 bytes (997.39 MiB);
- `IBKR_PAPER_BRIDGE/`: 132 tracked regular-file blobs totalling 6,683,084
  bytes (6.37 MiB).

Those counts are a dated measurement, not a fixed future acceptance number. A
future candidate must derive its member count and bytes from its own exact SHA.

## 1. Decision in one sentence

The safest first V2 reduction is: **export every tracked regular file under
`IBKR_PAPER_BRIDGE/` at one clean exact commit, export nothing outside that
subtree, add only deterministic release identity files, and refuse the entire
build if a forbidden mutable/secret/special member is present.**

This is deliberately a subtree contract, not a hand-maintained list of selected
Python files. At the measured HEAD it removes 1,039,151,190 source bytes, a
99.361% reduction before the much smaller checksum manifest and tar framing.

## 2. Why the current package is large

`IBKR_PAPER_BRIDGE/deploy/linux/package.sh:74` currently executes:

```sh
git -C "${REPO}" archive --format=tar "${RELEASE_SHA}" | tar -x -C "${OUT}"
```

There is no pathspec, so the executed archive scope is the whole monorepo. The
declared purpose is a Bridge release, but the executed instrument includes
QuantLens research, backtest data, and unrelated command-centre evidence. A V2
repair must change the executed archive command and independently compare its
actual output universe with the declared scope; changing prose or computing an
unused allowlist is not a repair.

## 3. Normative V2 production-payload universe

### 3.1 Source members

For candidate commit `<SHA>`, the admitted Git source universe is exactly:

```text
every Git blob reachable at <SHA> whose repository path begins
IBKR_PAPER_BRIDGE/
```

The builder should derive this set with a NUL-safe Git plumbing command and
export that exact pathspec from the commit object. It must not copy the working
tree. No path outside `IBKR_PAPER_BRIDGE/` is admitted.

The first implementation should not prune individual Bridge docs, tests,
fixtures, tools, or modules. The additional approximately 5 MiB is operationally
small, while whole-subtree capture prevents a newly added import, static asset,
config, migration, test fixture, or deployment helper from silently missing a
release.

### 3.2 Generated root members

The V2 payload root should contain exactly three deterministic generated files
in addition to the admitted Git members:

1. `RELEASE_SHA` — the exact 40-lowercase-hex source commit plus one LF;
2. `RELEASE_FORMAT.json` — canonical UTF-8/LF JSON, no timestamp, containing
   at minimum `schema_version`, `source_commit`, and the sole source scope
   `IBKR_PAPER_BRIDGE/`;
3. `RELEASE_SHA256SUMS` — sorted SHA-256 records for every regular payload file
   except itself, including `RELEASE_SHA` and `RELEASE_FORMAT.json`.

`RELEASE_FORMAT.json` is a proposed new V2 identity surface. Its exact schema
must be frozen during Gate 1 before implementation. V1 has no such marker and
must never be rewritten to add one.

### 3.3 Conservation rule

For every candidate Git member, there must be one terminal disposition:

- **ADMITTED**: it is under `IBKR_PAPER_BRIDGE/`, is an allowed regular blob,
  appears exactly once in the extracted payload, and appears exactly once in
  `RELEASE_SHA256SUMS`; or
- **BUILD REFUSED**: it violates a forbidden-member rule and no artifact is
  published.

There is no third state in which a Bridge member silently disappears. The
builder must compare:

1. expected committed member set;
2. actual extracted source member set;
3. final manifest member set;

and require exact equality after accounting only for the deterministic generated
root files.

### 3.4 Forbidden members are a refusal, not an exclusion

The future builder must refuse to publish an artifact if the candidate subtree
contains a symlink, submodule/gitlink, device, FIFO, socket, or any other
non-regular member. The existing extracted-tree check in
`deploy/linux/lib/common.sh:104-119` must remain.

It must also refuse, rather than silently omit, committed mutable or
credential-bearing classes such as:

- `IBKR_PAPER_BRIDGE/data/**`;
- SQLite database/WAL/SHM files, runtime logs, PID/socket files, caches,
  `__pycache__`, `.pytest_cache`, and compiled bytecode;
- real `.env` files, private keys, wallet/credential exports, and secret files.

It should also refuse control characters, CR, LF, and tab in repository member
paths. Ordinary spaces, non-ASCII names, leading dashes, and shell
metacharacters remain valid inputs and must be handled without shell expansion.
This keeps the current line-oriented `sha256sum` manifest unambiguous while the
builder still uses NUL-safe discovery to detect and reject an unsafe name.

The exact name/content denylist and false-positive escape process must be frozen
before code is written. The committed
`deploy/linux/env/mtc-bridge.env.template` is metadata-only and remains admitted.
A refusal is invalid build input (`STOP / BUILD_REFUSED`), not evidence that the
software test itself failed.

## 4. Direct dependency closure: what omission would break

The whole-subtree rule is the authoritative safety net. The table below explains
the directly observed closure that must not be broken by a later aggressive
runtime-only refinement.

| Required path/class | Direct consumer and failure if omitted |
|---|---|
| `IBKR_PAPER_BRIDGE/bridge/**` | `bridge/app.py:19-27` imports API, brokers, engine, risk, strategy, store, and settings. Runtime startup/import fails if a live module is absent. Keeping the whole package also retains currently dormant mock, LLM-gate, and notifier imports. |
| `bridge/static/**` | `bridge/app.py:181-186` mounts the directory and reads `index.html`; the HTML loads CSS/JS. Missing assets break the dashboard or app creation. The directory contract automatically includes future Help/Wiki JSON or images after they are committed. |
| `config/bridge.yaml` | Read by `bridge/app.py:126-131` and `bridge/api/routes.py:16-17`; omission breaks configured runtime/risk/API behavior. |
| `config/strategies/**` | Strategy/golden provenance and configuration tests depend on it; future modular strategy loading should not require a package-scope edit. |
| `requirements.lock` | Required by `install.sh:168` and checked by `verify_lock.py`; omission prevents deterministic venv creation and rollback verification. |
| `deploy/linux/verify_lock.py` | Required by `install.sh:171` and `rollback.sh:131-133`; omission removes lock parity proof. |
| `deploy/linux/install.sh` and `deploy/linux/lib/common.sh` | The executing installer must be the hash-bound in-payload installer (`install.sh:92-95`). Detached or missing helpers are rejected before mutation. |
| `deploy/linux/env/mtc-bridge.env.template` | Required by `install.sh:175`; names required variables without carrying secret values. |
| `deploy/linux/systemd/mtc-bridge-first-start.service.template` | Required by `install.sh:176` and `rollback.sh:139`; omission prevents masked DISARMED unit rendering/rebinding. |
| `deploy/linux/logrotate/mtc-bridge` | Required by `install.sh:177`; omission prevents the bounded logging policy from being installed. |
| `deploy/linux/README.md` | Both unit templates declare it as their `Documentation=` target; omission leaves an invalid declared operations reference. |
| `RELEASE_SHA` and `RELEASE_SHA256SUMS` | Required by `install.sh:107-120`; omission or inventory drift rejects the payload. |
| `requirements.in`, `requirements.txt`, `tests/**`, fixtures, and deployment docs | The current Bridge suite checks direct/locked dependency consistency, golden fixtures, dashboard assets, deployment scripts, and documented payload commands. Removing these would require a separately specified verification artifact and test refactor. |
| other Bridge docs/tools | Not needed by `python -m bridge.app` today, but retained in conservative V2 to avoid an incomplete hand-maintained closure and to keep Bridge-local provenance/tools with the source candidate. |

The current installed release copies the entire accepted payload with
`install.sh:274`; it then seals that same tree read-only. Therefore production
payload scope and installed immutable-release scope are presently identical.

## 5. Test and verification companion boundary

The production payload can be Bridge-only, but the current full command
`pytest IBKR_PAPER_BRIDGE/tests` is not self-contained inside that subtree.
`tests/test_linux_deployment.py` also reads:

- all tracked files under
  `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/` — 28 blobs / 45,830 bytes at the
  measured HEAD;
- `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md` —
  1 blob / 10,175 bytes.

Together these are 29 blobs / 56,005 bytes. A clean exact-SHA repository checkout
already supplies them, so the mandated pre-package suite should run there.

If a future Ubuntu matrix requires the complete test suite from a transported
source bundle, create a **separately hashed verification companion** containing
the Bridge subtree plus those exact external governance paths. At this snapshot
that companion source set is 161 blobs / 6,739,089 bytes (6.43 MiB). It must not
be copied into `/opt/mtc-bridge/releases/<SHA>` and must not share the production
payload manifest identity.

`IBKR_PAPER_BRIDGE/tools/generate_golden.py:35-37` is a development/provenance
tool that loads QuantLens' `mega_walk_forward.py` and external datasets when it
is explicitly run. It is not called by the current Bridge tests or runtime and
must not drag QuantLens/data into the production package. Golden regeneration
continues in the research checkout; the committed golden fixture and strategy
config remain in the Bridge subtree.

This separation yields three distinct proofs:

1. source correctness — full mandated suite in the exact-SHA checkout;
2. package correctness — exact scope/member/determinism tests against the built
   production payload;
3. host correctness — separately authorized install/verify/rollback evidence
   using that exact payload.

Passing one is not a substitute for either of the others.

## 6. Package identity and evidence changes

A scoped package is a new format and a new candidate even if its application
source were otherwise unchanged. At minimum, all of the following identities
must be newly derived and recorded:

- source commit SHA;
- package-format schema/version and its marker hash;
- exact source-member count, bytes, and member-list hash;
- `RELEASE_SHA256SUMS` bytes and SHA-256;
- extracted payload file count/bytes;
- transfer artifact bytes and SHA-256;
- dependency-lock hash and per-SHA venv evidence;
- rendered unit hashes;
- local and Ubuntu matrix evidence;
- install and rollback manifest schema/bytes/hashes;
- accepted predecessor and rollback-target SHA/manifest pairs.

`release_sha` alone is insufficient to identify the package format. Operational
records should identify a release by at least the tuple
`(source SHA, format version, RELEASE_SHA256SUMS SHA-256)`.

Existing Gate-A/WP-I/V1 file counts, tar hash, manifest hash, accepted candidate
labels, and host evidence do not transfer. They remain historical evidence for
the full-tree V1 object only.

The install/rollback JSON records should gain an explicit package-format field
when the schema is deliberately versioned. A missing format marker may be
accepted only for an explicitly preregistered legacy V1 SHA + manifest-hash pair;
it must never mean "accept any legacy-shaped payload."

## 7. Cross-format rollback contract

The current rollback mechanism is structurally member-count agnostic:

- it binds a target release SHA and accepted manifest SHA
  (`rollback.sh:118-124`);
- verifies every target checksum and exact target inventory
  (`rollback.sh:124-127`);
- verifies that target's separate venv against that target's lock
  (`rollback.sh:131-133`);
- renders the unit from that target's own first-start template
  (`rollback.sh:139`);
- leaves the service masked and preserves state (`rollback.sh:86,106,153`).

Therefore a slim V2 can remain rollback-compatible with a retained full-tree V1
without making their package shapes equal. The following must be demonstrated
offline/expendably before any production claim:

1. V2 rollback tooling can target the installed full-tree V1 release using the
   exact accepted V1 manifest and V1 venv;
2. V1-compatible rollback tooling can target an installed slim V2 release using
   the exact accepted V2 manifest and V2 venv;
3. an old full-tree manifest is never evaluated against a slim tree, or vice
   versa;
4. target unit rendering uses the target release's template and stays masked;
5. no rollback deletes/moves/migrates `/var/lib/mtc-bridge`, starts a service,
   unmasks, enables, arms, changes firewall state, or touches secrets;
6. legacy acceptance is restricted to the frozen known V1 identity tuple;
7. both old and new release directories and venvs remain independently
   immutable and recoverable.

Package-format compatibility does **not** prove database-schema or strategy-state
backward compatibility. If V2 later changes state schema, a separate migration
and rollback contract is required; this package-size work must not smuggle that
decision in.

## 8. Required D026 RED/GREEN matrix

Every regression test offered as closure evidence needs executable RED against
the exact predecessor or an equivalent deliberate mutation, then GREEN with the
repair. The future evidence package should include at least:

| Mutation / predecessor | Required RED observation | Required GREEN observation |
|---|---|---|
| Run the current whole-repo exporter or mutate the scoped exporter back to `git archive <SHA>` without a pathspec | An unrelated committed sentinel appears; actual members differ from the declared Bridge scope | No outside member exists; expected Git scope = extracted source scope = manifest scope |
| Compute the right allowlist but leave the executed archive command whole-repo | Declared-versus-executed scope test fails | The exact command output and declared scope agree |
| Remove one member from each mandatory class: runtime module, static asset, config, lock/verifier, installer/common helper, env template, unit, logrotate, README, test fixture | Conservation/closure or functional test fails before artifact acceptance | Every candidate member has exactly one admitted disposition and direct consumers succeed |
| Silently filter a committed forbidden `.env`, key, DB/WAL, log, or cache member | Test fails because the build published an incomplete artifact instead of refusing input | Builder returns `BUILD_REFUSED`, publishes no candidate, and names only the safe path/class (never secret content) |
| Add a Git symlink/gitlink or extracted FIFO/socket/device | Build/admission rejects the special member | Ordinary-file payload builds and exact inventory passes |
| Add/remove/inject a file after manifest creation | Installer and verifier reject exact-inventory mismatch | Untampered manifest and tree match exactly |
| Delete, duplicate, reorder incorrectly, path-traverse, or malformed-encode a manifest record | Strict parser/inventory/hash check rejects it | Canonical sorted manifest verifies every file once |
| Tamper, omit, or mismatch `RELEASE_FORMAT.json` | V2 admission rejects; unknown/missing marker is not generic legacy acceptance | V2 format/source scope/source SHA match the accepted identity tuple |
| Dirty tracked or untracked worktree, including dirt outside the Bridge subtree | Builder refuses, preserving the current whole-worktree cleanliness invariant | Clean exact-HEAD build succeeds |
| Spaces, glob characters, leading dashes, non-ASCII, CRLF attributes, and shell metacharacters in a temp-repo path | Any shell-expanded or worktree-byte implementation fails determinism/member equality | Git-object export preserves valid names/bytes and produces identical output on repeated builds |
| Tab, CR, LF, or another control character in a member path | Build must fail if it publishes or silently drops the member | NUL-safe discovery identifies the unsafe name, returns `BUILD_REFUSED`, and publishes no artifact |
| Build the same SHA twice into fresh empty destinations | Any member, manifest byte, or final artifact byte differs | Member list, contents, format marker, manifest, and transfer artifact are byte-identical |
| Run the full suite from only the Bridge subtree | The known 29-path external dependency boundary is surfaced, not misreported as Bridge code failure | Full suite passes in exact checkout or separately hashed verification companion; production payload remains Bridge-only |
| Target full V1 from slim V2 and slim V2 from full-compatible rollback tooling | Wrong manifest/venv/template pairing or any start/state mutation fails | Each direction verifies its own target identity, keeps state, and ends masked/stopped |

For the scope defect specifically, a static assertion that the script contains
the string `IBKR_PAPER_BRIDGE` is supplemental only. The RED must show that the
predecessor actually exports an outside member, and the GREEN must inspect the
real built member universe.

## 9. T0 implementation and acceptance plan

This future change is **T0**: it modifies the builder, installer/admission,
manifest identity, rollback compatibility, and host-bound artifacts.

1. Freeze this contract, exact marker schema, forbidden-member policy, legacy
   V1 tuple, and acceptance commands at Gate 1.
2. Implement in an isolated clean worktree through the counterpart flagship.
   Do not modify or regenerate V1 artifacts.
3. Add the scope/member/format tests and record the complete D026 RED/GREEN
   commands and real outputs.
4. Run the full mandated suite in the exact-SHA checkout; separately exercise
   the built payload and companion boundary.
5. Build twice from the same SHA in fresh destinations and compare member lists,
   file hashes, generated identity files, manifests, and final transfer bytes.
6. Exercise install, verify, immutability, masked/unstarted first start, and both
   cross-format rollback directions on local/expendable fixtures first.
7. Obtain fresh accepting `claude-opus-5` xhigh and `gpt-5.6-sol` xhigh T0
   verdicts, with both auditors executing the mandated suite and the Lead
   reproducing every required finding.
8. Derive a new candidate and all new evidence identities. Never relabel V1.
9. Only after a separate owner deployment authorization, reproduce the accepted
   artifact on a named expendable Ubuntu 24.04 staging environment, still
   DISARMED and without secrets/exchange authority.

## 10. Deferred aggressive refinement

A later runtime-only artifact could omit tests, docs, fixtures, smoke tools, and
development provenance, approaching the previously measured 1.28 MiB
runtime/install-essential boundary. Do not combine that optimization with the
first scope repair. It would require:

- a versioned explicit runtime closure rather than whole-subtree capture;
- an independently signed source/verification companion;
- tests proving every Python import, static asset, config, migration, unit,
  installer, verifier, and rollback dependency;
- a clear rule for whether the installed release is source evidence or only a
  runtime artifact;
- another T0 identity and cross-format rollback cycle.

The conservative 6.37 MiB class already removes approximately 99.36% of current
tracked source bytes. The additional operational complexity is not justified
until the full-subtree V2 format has been accepted and observed.

## 11. Conclusion

The approximate 1 GB footprint can be removed without deleting Bridge history or
weakening rollback. The conservative contract is an exact Git-committed
`IBKR_PAPER_BRIDGE/` subtree, three deterministic root identity files, fail-closed
forbidden-member handling, exact member conservation, a separate 56,005-byte
external test-context boundary, and explicit legacy V1 rollback compatibility.
Implementation must create a new T0-audited V2 candidate; frozen V1 remains
untouched.
