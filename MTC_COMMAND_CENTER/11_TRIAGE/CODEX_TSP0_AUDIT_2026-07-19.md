# Codex independent audit — TS-P0-001..004

- Date: 2026-07-19
- Auditor: Codex GPT-5
- Target: `C:\TSP0`, branch `feature/ts-p0-baseline`, HEAD `7777273fc49317cb5572b3399d8daa17c92a2251`
- Base: `008e065e8e0ffa68f46134da6698d58f91ef2dcb`
- Verdict: **BLOCK**

> **Post-audit status, 2026-07-19:** the three BLOCK findings were repaired
> locally in an uncommitted nine-file diff. See
> `CODEX_TSP0_BLOCK_REPAIR_REPORT_2026-07-19.md`. This historical verdict stays
> BLOCK until the repair receives an independent non-BLOCK re-audit.

This report distinguishes builder claims from evidence reproduced in this Codex
session. Builder reports and the earlier Fable audit were read as claims only.

## Canonical facts verified now

- `C:\TSP0` was clean on `feature/ts-p0-baseline` at `7777273f` before the audit.
- Chain: `008e065e` → `fa449ce2` → `42d0ca9f` → `7777273f`.
- `origin/master=008e065e`; local `master=8721bce0` and was not changed.
- `C:\P2RT` was detached and clean at `008e065e` before the audit.
- The single permitted `GET http://127.0.0.1:8790/api/status` returned
  `state=ARMED`, `mode=paper`, `network=testnet`,
  `run_id=paper-20260719185026`, and a fresh reconcile timestamp.
- Python was `3.14.2`; all pytest runs used `PYTHONUTF8=1`.

## Scope reproduction

Command: `git -C C:\TSP0 diff --stat 008e065e..7777273f`

Verified now: 11 files, 2,057 insertions, 1 deletion, all under
`IBKR_PAPER_BRIDGE/`. The only modified production files are
`bridge/engine/engine.py` and `bridge/api/routes.py`; the remaining code,
tests, and contracts are new. No protected path is touched. No test that
existed at `008e065e` was modified. Task B adds one fixture line to the new
Task-A file `tests/test_runtime_baseline.py`.

## Mandatory suite and TDD reproductions

| Reproduction | Verified result | Exit |
| --- | --- | ---: |
| `cd C:\TSP0; python -m pytest IBKR_PAPER_BRIDGE/tests -q` | 210 passed, 1 Starlette warning, 45.87s | 0 |
| `cd C:\TSP0\IBKR_PAPER_BRIDGE; python -m pytest tests -q` | 210 passed, 1 Starlette warning, 35.75s | 0 |
| Throwaway `C:\TSP0AUD` at `008e065e`; root suite | 164 passed, 1 warning, 27.47s; worktree removed | 0 |
| Focused Task A | 14 passed, 10.40s | 0 |
| Focused Task B | 11 passed, 9.70s | 0 |
| Focused Task C | 21 passed, 1.11s | 0 |
| RED A: remove `check_runtime_baseline.py`; run Task-A test | collection ImportError | 2 |
| RED B: remove `release_evidence.py`; run Task-B test | collection ImportError | 2 |
| RED C: parent wiring + remove `window.py`; run Task-C test | collection ImportError | 2 |

Each RED proof was restored immediately; `git status --porcelain` was empty
after each proof.

Audit-note correction: the first throwaway-baseline command created and removed
the correct worktree but accidentally ran pytest from the main-worktree CWD. It
collected 114 tests and produced one timing failure. This was an auditor command
error, not baseline evidence. The corrected command used explicit
`Push-Location C:\TSP0AUD` and reproduced 164/164. No new tracked
main-worktree change attributable to the mistaken run was observed.

## Task A — TS-P0-001 runtime baseline

Builder claimed: deterministic read-only comparison, secret-safe hashing, and a
real-pair integration result containing only two commit-mismatch reasons with
equal source/config hashes.

Verified now:

- Scope bypass, CRLF/content-change, early-NUL binary handling, dirty-state,
  subprocess exit-code, byte-stability, and no-mutation probes passed.
- Fixed-timestamp JSON and Markdown were byte-identical. Without a fixed
  timestamp, only `generated_at_utc` changed.
- Subprocess matrix: MATCH `0/manifest 0`; source drift `2/2`; config drift
  `2/2`; missing runtime `2/2`; missing repo, malformed HEAD, and argparse
  garbage each exited 3 without traceback.
- Real-pair command exited 2, but the exact reasons were
  `repo_commit_mismatch_expected`, `repo_runtime_commit_mismatch`, and
  `source_tree_hash_mismatch`. `source_tree_hash_equal=false`,
  `config_hash_equal=true`, and both dirty flags were false. The differing
  source files were `bridge/api/routes.py`, `bridge/engine/engine.py`, and the
  runtime-missing `bridge/engine/window.py`.

The real-pair result is correct behavior at final HEAD: TS-P0-003 changed the
declared source scope and was not deployed to P2RT. The two-reason/equal-source
claim was true only at the earlier Task-A commit, not at `7777273f`.

### A-01 — MAJOR — common secret filenames are opened and hashed

`tools/check_runtime_baseline.py:48-53,96-114,117-139`

A fixture planted `.env`, `secrets.key`, `prod.env`, `my.secrets`, and
`key.txt` with a sentinel. No sentinel leaked into stdout/stderr/JSON/Markdown;
`.env` and `secrets.key` were excluded and never opened. However, `prod.env`,
`my.secrets`, and `key.txt` were opened and hashed. In particular, `prod.env`
is a conventional environment-secret filename but does not match
`^\.env(\..*)?$`.

Judgment against accepted ADR-0027: **finding, not acceptable**. ADR-0027 says
secrets stay outside reports/repositories and requires layered secret controls.
Persisting a secret-derived digest also enables offline guessing of weak values.
Extend the denylist at least to conventional `*.env` and `*.secrets` forms,
decide/document the `key.txt` policy, and add spy/no-leak tests.

## Task B — TS-P0-002 release evidence

Builder claimed: create/validate fail safely with exits 0/2/3, integrity detects
tampering, and live comparison defeats a re-sign attack.

Verified now:

- Unsigned hash tamper: exit 2, `integrity_hash_mismatch`.
- Tampered `config_hash` plus recomputed integrity: exit 2,
  `config_hash_mismatch` and no integrity mismatch.
- Release commit not HEAD and rollback==release: exit 3, no traceback.
- Re-signed schema `0.9.0`: exit 2, `unsupported_schema_version:0.9.0`.
- Re-signed missing `rollback_commit`: exit 2,
  `missing_field:rollback_commit`.
- Corrupt JSON and absent file: exit 3, no traceback.
- `RELEASE_EVIDENCE_CONTRACT.md` retains the required
  **DRAFT — pending Barış approval** header.

### B-01 — MAJOR — valid JSON with wrong `hashes` shape crashes validation

`tools/release_evidence.py:159-180,188-210,297-304`

A valid manifest was changed to `"hashes": []` and correctly re-signed with
`_integrity_hash`. The subprocess exited **1**, emitted a traceback, and ended
with `TypeError: list indices must be integers or slices, not str`. The
validator only checks nested required fields when `hashes` is already a dict,
then dereferences it unconditionally during live comparison. This violates the
fail-safe exit contract. Validate container and scalar types before live
comparison, return a structured exit-2 invalid report, and add a committed
wrong-shape test.

## Task C — TS-P0-003 monitoring-window state

Builder claimed: RUNNING with stale/missing liveness is impossible and the
state surface fails safe.

Verified now:

- Exhaustive valid-domain sweep found zero false-active combinations.
- Exact age 300s returns RUNNING and 300.001s returns DOWN, matching the
  documented `age > threshold` rule.
- Naive timestamps are treated as UTC and worked as documented.
- Missing/garbage started or liveness timestamps returned DOWN.
- A throwing store returned DOWN with `error=store_unreadable`.
- `record_window_start` preserved the interruption marker; the state remained
  INTERRUPTED. Engine-less `init_runtime_state` returned DOWN/no_store.
- Diff from `42d0ca9f` is limited to the window import/field/calls/status key;
  route decorators are identical and no endpoint was added. Intended DB-meta
  and window-event writes are present; no schema/network/scheduler change.
- Reset policy remains **PROPOSED** and no reset endpoint exists.

### C-01 — MAJOR — malformed interruption metadata can return RUNNING

`bridge/engine/window.py:45-54,76-88,101-124`

With ARMED state, a valid start, fresh liveness, and
`window_interrupted_ts="garbage"`, `window_status` returned **RUNNING** with
`error=None`. `_parse_ts` maps both absent and malformed values to `None`, so
corrupt interruption evidence is treated as proof that no interruption exists.
This directly violates the card's core false-active acceptance requirement.

### C-02 — MAJOR — future-dated liveness can return RUNNING

`bridge/engine/window.py:80-87`

With liveness one day in the future, age is negative and therefore not greater
than the stale threshold; ARMED state returns **RUNNING**. Reject materially
future timestamps (or define a small explicit skew tolerance) and require a
non-negative fresh age.

Required repair for C-01/C-02: preserve missing-vs-malformed distinction,
return DOWN with an explicit invalid-evidence error for malformed safety meta,
reject future liveness beyond a documented tolerance, and add committed tests
covering each persisted meta key plus future-clock cases.

## Task D — TS-P0-004 ADR closure

Verified now:

- All twelve ADR-0018..0029 files say `Status: Accepted`.
- The three claimed old strings are absent; the replacement wording in
  ADR-0018, ADR-0025, and `ADR_INDEX.md` agrees with D016.
- The ADR directory is untracked and the task remains docs-only.
- The current main-worktree diff contains D016/D017 relative to its tracked
  HEAD. Because these records pre-date this audit and the ADR files are
  untracked, Git cannot prove which earlier session inserted D016. Codex did
  not edit `DECISIONS.md` in this audit.

### D-01 — NIT — residual present-tense Proposed wording remains

Examples: ADR-0020:62, ADR-0025:51, ADR-0029:49. Headers and ratification lines
govern, so this does not reopen the decisions, but the prose remains stale and
should be reconciled in a docs-only cleanup if the closure goal is full status
consistency.

## Adversarial checklist

| # | Result | One-line proof |
| ---: | --- | --- |
| 1 | PASS | Outside-scope file left hashes equal; inside `bridge/` changed source hash; code and contract scopes match. |
| 2 | PASS | Content+EOL and early-NUL changes detected; EOL-only hash equal; fixture Git porcelain caught EOL-only worktree tamper. |
| 3 | **FAIL** | No sentinel leaked, but `prod.env`, `my.secrets`, and `key.txt` were opened/hashed; A-01. |
| 4 | PASS | Untracked runtime file set dirty; ignored data/pycache stayed outside/excluded; ignored file inside hashed bridge scope still changed the hash. |
| 5 | PASS | Process exits and emitted manifest exits matched for all manifest-producing cases; exit-3 input failures emitted no manifest and no traceback. |
| 6 | PASS | Fixed-timestamp JSON+MD byte-identical; automatic runs differed only at `generated_at_utc`. |
| 7 | **FAIL** | Re-sign attack was caught, but re-signed non-dict `hashes` crashed exit 1 with traceback; B-01. |
| 8 | **FAIL** | Valid sweep safe, but garbage interruption and future liveness both produced RUNNING; C-01/C-02. |
| 9 | PASS | Additive window wiring only; identical endpoint set; no schema/network/scheduler change. |
| 10 | PASS | Final TSP0 and P2RT porcelain empty; P2RT HEAD unchanged. |
| 11 | PASS-WITH-NIT | Twelve Accepted headers and three claimed wording fixes verified; residual stale prose is D-01. |
| 12 | **FAIL** | Files/tests/contracts exist and gates are marked, but false-active and fail-safe acceptance criteria are violated. |

## Verdict and required edits

**VERDICT: BLOCK.** Do not push or open a PR for
`feature/ts-p0-baseline` yet.

Required before re-audit:

1. Fix malformed/future monitoring-window evidence so it cannot return
   RUNNING; add committed regression tests.
2. Make `release_evidence validate` reject non-dict/wrong-type manifest
   structures with a structured exit 2 and no traceback; add tests.
3. Extend and document secret-filename exclusions for conventional
   `*.env`/`*.secrets` cases, with spy/no-leak tests; decide `key.txt` explicitly.
4. Correct the final-HEAD integration expectation: three reasons and source
   mismatch are correct until TS-P0-003 is deployed. Do not weaken the hash
   scope to make the stale two-reason expectation pass.
5. Re-run 14/11/21 focused tests, both 210-test CWD suites, the real-pair
   integration, and the failed probes above. Keep P2RT read-only.

## Window-unaffected and safety confirmation

- P2RT before: `008e065e8e0ffa68f46134da6698d58f91ef2dcb`, porcelain empty.
- P2RT after integration and final audit: same HEAD, porcelain empty.
- TSP0 final: `7777273fc49317cb5572b3399d8daa17c92a2251`, porcelain empty.
- Push: **NO**.
- PR / merge: **NO**.
- Deploy / P2RT write / checkout / restart / stop: **NO**.
- P2RT scheduler / task / runtime-DB operation: **NO**. Pytest used only its
  normal throwaway fixture databases.
- ARM / DISARM / KILL / threshold / strategy / Pine / parity / schema action: **NO**.
- Credential read or credential action: **NO**; only synthetic sentinels in temp fixtures.
- Network: **NO**, except the single permitted localhost status GET.
- New commit: **NO**.
