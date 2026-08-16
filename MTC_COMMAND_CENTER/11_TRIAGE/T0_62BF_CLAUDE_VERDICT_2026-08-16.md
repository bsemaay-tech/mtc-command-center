# T0 acceptance audit — integrated Bridge release candidate `62bf661b` — Claude flagship lane

## Header

| Field | Value |
|---|---|
| Model identity (as reported by runtime) | `claude-opus-5` ("Opus 5") — reported by the session environment block |
| Effort | `xhigh` **as configured by the dispatching route header**. I cannot introspect the effort parameter from inside the session; I do not claim to have verified it, only that no lower-effort override was applied by me. |
| Session | Fresh; no resume, no implementer context |
| Working directory | `C:\AUD62A` (detached auditor worktree) |
| Start (UTC+3) | 2026-08-16 08:54:03 |
| Stop (UTC+3) | 2026-08-16 12:02:21 |
| Start / Stop (UTC) | 2026-08-16T05:54:03Z / 2026-08-16T09:02:21Z |
| Output file | `C:\tmp\lane_out\T0_62BF_CLAUDE_VERDICT.md` (only file written inside the deliverable path) |

**VERDICT: PASS-WITH-NITS** — zero required repairs to the candidate bytes. Four
nits, all in the *governing prose records*, none in the candidate tree.

---

## Check 1 — Subject identity (independently verified)

```text
$ git rev-parse HEAD
62bf661b065dec5b5d9895d83575581fe369252d
$ git rev-parse HEAD^{tree}
e2cb5dadd1537e933460aeecd5cdcf343c31d7d0
$ git rev-parse HEAD^1 HEAD^2
7d4e9a96e07b34a0c3d92315912d7818168b830b
2ce41e34bceb599d80af24c5c33d835820ec321b
$ git log -1 --format='%P'
7d4e9a96e07b34a0c3d92315912d7818168b830b 2ce41e34bceb599d80af24c5c33d835820ec321b
$ git for-each-ref --points-at 62bf661b… --format='%(refname) %(objecttype)'
refs/heads/integration/bridge-release-20260815 commit
refs/remotes/origin/integration/bridge-release-20260815 commit
```

All four identities (commit, tree, parent 1, parent 2) match the contract
exactly. Branch is `integration/bridge-release-20260815`; the candidate is its
tip. Commit subject: `Merge Gate-A into repaired WP-I release integration`
(author `Codex GPT-5`, `Sun Aug 16 11:50:46 2026 +0300`).

Merge base independently derived and matches the runbook:

```text
$ git merge-base 7d4e9a96 2ce41e34
4d2228cf8985ce755c398cceff23f777a99d5404
```

**Result: PASS.**

### Provenance of the governing documents

The runbook is **not** in the candidate tree (`git show HEAD:…RUNBOOK…` fails).
I located all three governing docs on other refs and read them from Git objects,
not from any working copy:

| Document | Blob | Reachable from |
|---|---|---|
| `BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md` | `6a2799f0605e874a3bcc1c6602bd89379f1f8b12` | `codex/rp7-r1-r4-repair-20260815` (+2 other branches, identical blob) |
| `…RUNBOOK_INPUT_REFRESH_2026-08-16.md` | `0bff76d25cf8abeceb9331847f710ac2feb5ecd9` | `codex/rp7-r1-r4-repair-20260815` |
| `…EXECUTION_RECORD_2026-08-16.md` | `9629cd1f6f3c4eee2a45d7d38fc9e8beffa97763` | `codex/rp7-r1-r4-repair-20260815` |

The fence table used below is the one in the runbook blob above, §4 lines
514–546 — not the abbreviated restatement in the audit contract.

---

## Check 2 — 33-path blob fence

Every row of runbook §4 compared to `git rev-parse HEAD:<path>`. All 33 rows
match, including both synthesized rows:

```text
BLOB_OK IBKR_PAPER_BRIDGE/bridge/api/routes.py 140bf003ecbcb6b7f47822c15f2dbdb83118f0df
BLOB_OK IBKR_PAPER_BRIDGE/bridge/app.py 572c4178fe804da17601eefd898027e9261492e6
BLOB_OK IBKR_PAPER_BRIDGE/bridge/broker/base.py 0698e4862ea6390c0cec5db34b85602d336e33e1
BLOB_OK IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py 855a17cd83c7d176576d810be5d520dbf1e5eba4
BLOB_OK IBKR_PAPER_BRIDGE/bridge/broker/mock.py 295c0a9cd06a0ca6b36cb4e691dab54555cc5670
BLOB_OK IBKR_PAPER_BRIDGE/bridge/engine/engine.py 0c115ff18489108daa015c35c1ef1e85bc2bbbf0
BLOB_OK IBKR_PAPER_BRIDGE/bridge/engine/orders.py 608a3afe1015c7a98e08f7d4f1bb08ea8cebae89
BLOB_OK IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py ea3ff95d93e92ef2e224c5fa9ad18e1b64fab4b0
BLOB_OK IBKR_PAPER_BRIDGE/bridge/engine/types.py 2927968d7bfc5253e2011172610a8ff7ca676647
BLOB_OK IBKR_PAPER_BRIDGE/bridge/store/db.py ae5eb1b7ab2a9a6240932958c73ba4acdfe2a30e
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template c03d6e47ab57c00ef95f4122607fc7ba88119e35
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh db11010a24edfbb96ba80ec1fbe1db3ff29193c9
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/package.sh add6478d33cce8d929d58f895407abe01d51da20
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/README.md 4069904b7707da9efa875661769fc29435504b33
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md 8db2e6dd7e782c96f585f6672c4489c4ce5c1488
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template c18232549d96aa200d8c7f796e64de743288940c
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/verify.sh 5cfefd709202ff504ae7b7fc3504b8c0b00900b6
BLOB_OK IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md a09b22bedb4e1a4e0ce9dc943983dd6cf399674d
BLOB_OK IBKR_PAPER_BRIDGE/docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md b02694c2e64061480843a8d76361d72034d46010
BLOB_OK IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md 23480737ee802bdad7c03a93e06d5989e22cfb58
BLOB_OK IBKR_PAPER_BRIDGE/README.md cfc15b212121b4a9f3adac3d18f02574c5aa74e7
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_api.py 40d31925ac93c4bfe13a877f060b5abaf6c0cd6e
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py ce0ae7c24f795dc8e5d56bf7cca82e1a75351402
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py 817afe17b00c5a7525e5d422b965fe260b802006
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py 3851340462fe0269a019bbbd2608e4db97d9ce8b
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py 64e25888ba67a6b706bbf5c9d5e5feb8f12a98b2
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_mock_broker.py bed96cea0f31cc7a7010ca790b0d03f219ab9c2a
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py 9e50c1b51cd6d60967f5481adfeda9779815efd9
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py 7b0b9ea36dd8b15108f6befcbcb00015ed2f51fb
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_reconciliation.py 9e6b015d84371c50b92bf25b12ee1f80c64bb581
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_store.py d911d983f0b76f752836ae220bc4ec61f04b98a2
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py 12b17ab595dad24fcff6397d0689effadbfe2f67
BLOB_OK IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py 26c077e650ab88ba2086efa3a80790769bc055b1
FENCE_RESULT=PASS
```

Row count parsed from the runbook table = 33. Both contract-named synthesized
rows confirmed: `deploy/linux/README.md = 4069904b7707…`,
`tests/test_wal_state_bundle.py = 12b17ab595da…`.

**Result: PASS (33/33).**

---

## Check 3 — First-parent scope

```text
$ git diff --name-only HEAD^1 HEAD | wc -l
32
$ diff <expected: 33 fence paths minus deploy/linux/SECURITY_BASELINE.md> <actual>
(no output — sets are exactly equal)
SET_EQUALITY_RC=0
$ git diff --name-only HEAD^1 HEAD | grep -v '^IBKR_PAPER_BRIDGE/'
(none)
$ git diff --name-only HEAD^1 HEAD -- . ':(exclude)IBKR_PAPER_BRIDGE' | wc -l
0
```

The first-parent delta is *exactly* the 32 expected paths — verified by set
equality, not by count alone (a count check alone would pass on a swapped pair).
Zero outside-union paths. Zero paths outside `IBKR_PAPER_BRIDGE`.

**Result: PASS.**

### Adversarial follow-up the contract did not require (important)

Because the first-parent delta touches nothing outside `IBKR_PAPER_BRIDGE`, the
merge resolved every non-Bridge path to WP-I's side. I checked whether that
silently discarded any Gate-A work:

```text
$ git diff --name-only 4d2228cf 2ce41e34 -- . ':(exclude)IBKR_PAPER_BRIDGE'
.gitattributes
COUNT_OUTSIDE=1
```

Gate-A's only non-Bridge change since the merge base is `.gitattributes`, and
both branches made the identical change:

```text
base      4d2228cf -> dfe0770424b2a19faf507a501ebfc23be8f54e7b
Gate-A    2ce41e34 -> 49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b
WP-I      7d4e9a96 -> 49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b
HEAD               -> 49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b
```

**No Gate-A change was lost.** `.gitattributes` at HEAD is the contract-required
`49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b`, and its content is intact
(`* text=auto`, plus the `ledger_schema.json text eol=lf` pin).

I also verified the converse direction — HEAD's Bridge tree against Gate-A's:

```text
$ git diff --name-status 2ce41e34 HEAD -- IBKR_PAPER_BRIDGE
M	IBKR_PAPER_BRIDGE/deploy/linux/README.md
A	IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md
M	IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
COUNT=3
```

Exactly the three predicted paths (1 WP-I-only + 2 changed-by-both). Every other
Bridge byte at HEAD is Gate-A's, byte-for-byte. This is the strongest single
statement of merge correctness in this report.

---

## Check 4a — `tests/test_wal_state_bundle.py` resolution

```text
$ git rev-parse 2ce41e34:IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
07de7b206f56c7442c3ea07ec160dc7ef2497415
$ git rev-parse HEAD:IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
12b17ab595dad24fcff6397d0689effadbfe2f67
$ git diff --stat 2ce41e34 HEAD -- IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
 1 file changed, 9 insertions(+), 4 deletions(-)
```

The complete delta is three hunks and nothing else:

```diff
+from contextlib import closing
-from bridge.store.db import SCHEMA_VERSION_BASELINE, Store
+from bridge.store.db import Store
...
+    with closing(sqlite3.connect(source_db)) as source:
+        source_schema_row = source.execute(
+            "SELECT value FROM meta WHERE key = 'schema_version'"
+        ).fetchone()
+    assert source_schema_row is not None
+
     rc, _ = create(source_db, bundle_dir, capsys)
...
-    # The merged TS-P1 chain moved the operational baseline from v2 to v4;
-    # this assertion was never updated with Store.initialize()'s default.
-    assert inv["schema_version"] == str(SCHEMA_VERSION_BASELINE)
+    assert inv["schema_version"] == source_schema_row[0]
```

Insertion/deletion arithmetic reconciles exactly to the diffstat (1+1+6+1 = 9 in;
1+3 = 4 out), which proves the quoted diff is the *whole* diff and no hunk was
elided. The change is the dynamic source-schema query replacing the stale
`SCHEMA_VERSION_BASELINE` assertion and its now-unused import — precisely the
accepted A2 repair, and nothing else. Import removal is safe: zero residual
references to `SCHEMA_VERSION_BASELINE` remain in that file.

**Result: PASS (conforms to the contract exactly).** See NIT-1 and NIT-4 for two
precision defects in how this change is *described* by the governing records.

---

## Check 4b — `deploy/linux/README.md` resolution

Blob `4069904b…`, 9964 bytes — matching the runbook's recorded
`README_SYNTHESIZED_BYTES=9964`. Diff against Gate-A carries all five required
elements and no more:

| Required element | Present | Evidence |
|---|---|---|
| Gate-A `MTC_BRIDGE_START_MODE=credential_free_disarmed` unit text | YES | line 114, unchanged from Gate-A |
| WP-I SECURITY_BASELINE inventory row | YES | added table row, "Static evidence only." |
| WP-I SECURITY_BASELINE limitation text | YES | added bullet, "PRE-GATE-A / STATIC ONLY…" |
| INTEGRATION PENDING status line | YES | line 4 |
| Corrected candidate-scoped history paragraph naming `2ce41e34` + `GATE_A_A9_PASS_FINAL_2026-08-09D.md` | YES | lines 125–131 |
| Must NOT claim the integrated SHA was executed/accepted | CONFIRMED ABSENT | see below |

Negative check executed rather than assumed:

```text
$ grep -n "62bf661b" <README at HEAD>
(no integrated SHA named — correct)
$ git grep -n "62bf661b" HEAD
(no output — the integrated SHA is claimed nowhere in the entire tree)
```

The README states the opposite of a claim: *"The newly integrated SHA has not
been installed, run, or accepted and must repeat the full gate before any
acceptance claim."*

I also verified the README's *positive* evidence claim resolves rather than
dangling — it asserts `2ce41e34` passed A-0..A-9 on the Gate-A staging host:

```text
$ git cat-file -e HEAD:MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A9_PASS_FINAL_2026-08-09D.md
PRESENT at HEAD
GATE_A_A9_PASS_FINAL_2026-08-09D.md:5: **A-9 PASS. Final Gate-A verdict: A-0 through A-9 all PASS** for accepted candidate
GATE_A_A9_PASS_FINAL_2026-08-09D.md:6: `2ce41e34bceb599d80af24c5c33d835820ec321b`. This is **staging Gate-A acceptance only**.
```

The cited file exists in the candidate tree and its content corroborates the
README sentence, including the "staging acceptance only" scoping.

Cross-check on the added `SECURITY_BASELINE.md`: it pins a *different* candidate
(`1adf9ae51b0ddfe8…`) and is dated 2026-08-01. That is a live over-claim risk —
but the README's added limitation bullet explicitly disarms it ("remains dated
historical evidence for the old WP-I static baseline; it does not establish the
status of these integrated bytes"), and the baseline file itself contains no
"never executed" claim that Gate-A's staging run would now contradict.

**Result: PASS.**

---

## Check 5 — Credential-string parity with Gate-A

Gate-A's side derived independently with the same command, not taken from the
contract's numbers:

```text
$ git grep -c --fixed-strings credential_free_disarmed 2ce41e34 -- IBKR_PAPER_BRIDGE
2ce41e34:IBKR_PAPER_BRIDGE/bridge/api/routes.py:1
2ce41e34:IBKR_PAPER_BRIDGE/bridge/app.py:7
2ce41e34:IBKR_PAPER_BRIDGE/deploy/linux/README.md:1
2ce41e34:IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:1
2ce41e34:IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:1
2ce41e34:IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py:4
2ce41e34:IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py:2

$ git grep -c --fixed-strings credential_free_disarmed HEAD -- IBKR_PAPER_BRIDGE
HEAD:IBKR_PAPER_BRIDGE/bridge/api/routes.py:1
HEAD:IBKR_PAPER_BRIDGE/bridge/app.py:7
HEAD:IBKR_PAPER_BRIDGE/deploy/linux/README.md:1
HEAD:IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:1
HEAD:IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:1
HEAD:IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py:4
HEAD:IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py:2
```

Identical path set and identical per-path counts. 7 paths, 1+7+1+1+1+4+2 = **17
occurrences**, matching the contract's expected distribution exactly. The
repaired WP-I parent contributes zero occurrences (`git grep` on `7d4e9a96`
returns nothing), so Gate-A is the sole source and parity is not diluted.

**Result: PASS.**

**Deviation 4 independently confirmed truthful.** The execution record self-reports
that runbook §5.1 named six paths while requiring 17 occurrences, and that the
seventh path (`test_linux_deployment.py`, 2 occurrences) was dropped from the
hand-written expectation. My independent derivation reproduces exactly that:
seven paths, 17 occurrences. The Lead's disclosure is accurate and the runbook
defect is real and correctly characterised.

---

## Check 6 — Full suite executed by me

Run from the repository root in `C:\AUD62A`, output redirected to a file outside
the repository. Python 3.14.2, pytest 9.0.2, Windows.

```text
PYTHONUTF8=1 python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests
```

Summary line only, as required:

```text
1360 passed, 1 warning in 170.34s (0:02:50)
```

Process exit code `PYTEST_RC=0`. Required criterion `1360 passed, 1 warning` —
**met exactly**. Grep over the full log for `skipped|xfail|error|deselect|no
tests ran` returns **0** matches, so the 1360 is not inflated by skips or
deselection and the count is all genuinely-passing tests.

### Proof the run changed nothing

```text
$ git status --porcelain        # BEFORE the run
(empty)
$ git status --porcelain        # AFTER the run
(empty)
$ git rev-parse HEAD:IBKR_PAPER_BRIDGE/deploy/linux/README.md
4069904b7707da9efa875661769fc29435504b33   (expected 4069904b7707da9efa875661769fc29435504b33)
$ git rev-parse HEAD:IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
12b17ab595dad24fcff6397d0689effadbfe2f67   (expected 12b17ab595dad24fcff6397d0689effadbfe2f67)
$ git rev-parse HEAD
62bf661b065dec5b5d9895d83575581fe369252d
```

Clean before and after, both synthesized fence rows re-verified post-run, HEAD
unmoved.

**Result: PASS.**

---

## Check 7 — D026

```text
$ git diff --name-status HEAD^1 HEAD | grep '^A'
A	IBKR_PAPER_BRIDGE/docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md
A	IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md
A	IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py
```

The contract's framing mentions only the WAL test change. It omits that the
first-parent delta **adds an entire test file**, `test_credential_free_disarmed.py`.
I checked it rather than passing over it: that file is fence row
`ce0ae7c24f795dc8e5d56bf7cca82e1a75351402`, classified "Gate-A exact", and it
exists in Gate-A since before the merge base — it is Gate-A's already-accepted
content being integrated, not a test authored by this merge.

```text
$ git diff --name-status 4d2228cf 2ce41e34 -- IBKR_PAPER_BRIDGE | cut -f1 | sort | uniq -c
      3 A
     29 M
```

No test file, assertion, or fixture originates with this merge. The WAL test
change modifies an existing Gate-A test; net test count is unchanged from Gate-A
(30 `.py` files in both). Nothing is offered as *new* closure evidence, so D026's
RED/GREEN requirement is not triggered.

**Result: PASS.** (See NIT-1 — the execution record's *stated* D026 rationale is
inaccurate even though the D026 conclusion itself is correct.)

---

## Check 8 — Adversarial pass

For each check I asked what would make it fail, and executed the falsifier.

| Attack | Executed | Outcome |
|---|---|---|
| `.gitattributes` tampered (recorded-hash ambiguity under `* text=auto`) | blob at base/Gate-A/WP-I/HEAD | HEAD = `49c0fbe4…`; both branches changed it identically from base `dfe07704…`; no loss, no conflict |
| Path-count check passing on a *swapped* pair | full set-equality `diff`, not `wc -l` | sets exactly equal, `RC=0` |
| Gate-A work silently dropped outside the fence | base→Gate-A diff excluding Bridge | only `.gitattributes`, already identical on both sides |
| Test collection tampered (fewer tests, still "green") | test-tree diff HEAD vs Gate-A | byte-identical file list; `TEST_TREE_IDENTICAL_TO_GATE_A=YES` |
| **`conftest.py` — outside the 33-path fence, can silently alter collection** | blob at base/Gate-A/WP-I/HEAD | `c515f50c…` at **all four**; unchanged, unconflicted. Fence gap is closed by fact, not by scope. |
| Hidden pytest config skewing collection | `git ls-tree` for `pytest.ini`/`setup.cfg`/`pyproject.toml`/`tox.ini` under Bridge | none exist; only `tests/conftest.py` |
| Conflict markers committed into the tree | repo-wide + fence-path grep for `<<<<<<<`/`>>>>>>>`/`\|\|\|\|\|\|\|` | `MARKER_GREP_RC=1` (no matches). Only hit for a bare `=======` was a pytest warnings banner inside `docs/11_P1_BUILD_REPORT.md`, not a marker |
| Suite green because tests were skipped | grep log for skip/xfail/error/deselect | 0 matches |
| README's cited evidence file dangling | `git cat-file -e` + content grep | present at HEAD and corroborates the claim |
| Integrated SHA claimed accepted somewhere | `git grep 62bf661b HEAD` repo-wide | zero hits anywhere in the tree |
| Candidate quietly merged to master | `git merge-base --is-ancestor` | not an ancestor; `origin/master` = `637307e83951ffe2…`, exactly as the execution record claims |
| **A2 repair removed a tripwire without replacement** (self-confirming-check risk) | see below | tripwire preserved elsewhere; coverage neutral |

### The self-confirming-check test applied to the A2 repair

The repaired assertion `inv["schema_version"] == source_schema_row[0]` compares
the bundle's recorded invariant against the *same* source DB the tool reads
(`wal_state_bundle.py:458`, `"schema_version": _meta(conn, "schema_version")`).
That is a propagation check, and it is strictly weaker than an absolute pin: it
cannot detect the operational baseline drifting.

I did not stop at that observation — I checked whether the absolute pin survives
anywhere:

```text
IBKR_PAPER_BRIDGE/tests/test_store.py:25   assert store.get_meta("schema_version") == "4"
IBKR_PAPER_BRIDGE/tests/test_store.py:192  assert default.get_meta("schema_version") == "4"
IBKR_PAPER_BRIDGE/bridge/store/db.py:268   SCHEMA_VERSION_BASELINE = 4
(+ ~40 further absolute assertions in test_order_identity.py / test_partial_fill_protection.py)
```

The absolute baseline tripwire is pinned redundantly elsewhere, and the WAL test's
own job is bundle-invariant *propagation*, for which the source-anchored form is
the semantically correct one. **Net coverage effect: neutral. Not a finding.**

---

## Findings

### REQUIRED

**None.** No repair to the candidate bytes is required.

### NIT-1 — Execution record's "replayed byte-exactly" is factually false

The execution record ("Next in chain") discharges D026 with: *"the WAL test change
is the already-T1-accepted repair replayed byte-exactly"*. It is not byte-exact.

```text
Accepted repair, 6c746b65, against WP-I's base:  1 file changed, 8 insertions(+), 1 deletion(-)
Merged synthesis, 12b17ab5, against Gate-A base: 1 file changed, 9 insertions(+), 4 deletions(-)
```

The two bases differ (WP-I had a hardcoded `assert inv["schema_version"] == "2"`;
Gate-A had `assert inv["schema_version"] == str(SCHEMA_VERSION_BASELINE)` plus a
two-line comment and the `SCHEMA_VERSION_BASELINE` import). The merged synthesis
therefore *additionally* removes the import and two comment lines. The resulting
assertion line is byte-identical to the accepted one, and the delta is correctly
fenced — but the synthesized blob `12b17ab5…` was never itself T1-audited; only
its WP-I-based sibling was.

D026's *conclusion* still holds (no new test, no new closure claim). Only the
stated rationale is wrong. **Repair: restate as "the accepted A2 repair
re-derived onto Gate-A's base; assertion byte-identical, import and stale comment
additionally removed" — do not claim byte-exact replay.**

### NIT-2 — Input-refresh record's three-way classification is wrong, in the paragraph it labels "Independent verification"

The refresh record states the universe is *"33 paths with the same classification
(9 Gate-A-only, 1 WP-I-only, 2 changed-by-both, 21 WP-I-stale)"*. Measured:

```text
Gate-A-only (added since base):        3   (docs/30, docs/31, test_credential_free_disarmed.py)
Gate-A-only (present in Gate-A tree,
             absent from WP-I tree):   3   — same 3 under the alternate reading
WP-I-only:                             1
changed-by-both:                       2
WP-I-stale:                           30
union:                                33
```

The total (33) and every downstream consequence are correct, but the split is
wrong under both readings I could construct: 3/30, not 9/21. The candidate agrees
with me and *disagrees with the refresh record*; the execution record's own
merge-tree output also says `ADDED_IN_REMOTE_COUNT=3`. So the two governing
records contradict each other, and the erroneous number sits in the section
headed "Independent verification (not this record's own claim)" — the exact place
a reader is invited to stop checking. **Repair: correct to 3 Gate-A-only / 30
WP-I-stale.**

### NIT-3 — Input-refresh record names a path that does not exist

The refresh record identifies the drift commit's sole added file as
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md`.

```text
$ git show --name-only --format='' 7d4e9a96
MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md
$ git cat-file -e 7d4e9a96:…/WPI_BLOCKS_DRAFT/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md
ABSENT
```

There is no `WPI_BLOCKS_DRAFT/` segment. The record's substantive claims about the
drift commit are otherwise verified: `6c746b65` **is** the direct first parent of
`7d4e9a96`, and the commit adds exactly one file, 373 insertions, no product byte.
**Repair: drop the `WPI_BLOCKS_DRAFT/` segment.**

### NIT-4 — The A2 repair fixes nothing on the Gate-A base; the records imply otherwise

The runbook and execution record describe the WAL resolution as replacing a
"stale `SCHEMA_VERSION_BASELINE` assertion". On WP-I's base that was true
(hardcoded `"2"` against a baseline of 4). On **Gate-A's** base — the base actually
used — the assertion was already dynamic and green. Verified empirically rather
than argued, with a throwaway script writing only to scratch:

```text
SCHEMA_VERSION_BASELINE = 4
seeded source_db schema_version = '4'
Gate-A assertion  inv==str(BASELINE) would be: True
HEAD assertion    inv==source_row[0] would be: True
```

(`_seed()` calls `store.initialize()` with no argument, so the fixture DB lands on
`SCHEMA_VERSION_BASELINE` = 4.) The merged change is therefore a *harmonization*
to WP-I's repair shape, not a defect fix, and it slightly trades a
code-constant anchor for a source-DB anchor. Both forms pass; the absolute pin
survives in `test_store.py` (see Check 8). No byte change is required — the blob
is fenced and the contract requires exactly this content. **Repair: documentation
only — stop describing the Gate-A-base assertion as "stale".**

### Observation (below nit threshold, recorded for completeness)

The merged README drops Gate-A's sentence *"Test coverage in
`tests/test_linux_deployment.py` is structural only."* I checked whether that
sentence was still true: the file does use `subprocess` (for local `git` and
script exercise) but never installs, starts, or contacts a host — so it was
substantially true and its removal is a small loss of caveat. Against that, the
replacement text is materially *more* honest (it discloses the Gate-A staging
execution the old text wrongly denied, and states the integrated SHA is
unaccepted). Net disclosure improves. No action recommended.

---

## Verdict

**PASS-WITH-NITS.**

The candidate `62bf661b065dec5b5d9895d83575581fe369252d` is byte-correct. All
eight required checks pass on evidence I generated myself:

- identity, tree, both parents, and merge base verified independently;
- 33/33 blob fence exact;
- first-parent delta exactly the 32 expected paths, proven by set equality, with
  zero outside-union paths and zero paths outside `IBKR_PAPER_BRIDGE`;
- both resolutions correct at the byte level, with the WAL delta's
  insertion/deletion arithmetic reconciled to prove no hunk was elided;
- credential-string parity with Gate-A exact (17 across 7 paths), derived from
  Gate-A independently;
- **suite executed by me: `1360 passed, 1 warning`, exit code 0, no skips, and
  the run provably mutated nothing;**
- no new closure-evidence test introduced;
- the adversarial pass found no way to make any check fail, including the
  out-of-fence `conftest.py` gap, which is closed by fact.

Beyond the required scope I confirmed the merge lost no Gate-A work outside the
Bridge, that HEAD's Bridge tree equals Gate-A's in all but the three predicted
paths, that the integrated SHA is claimed accepted nowhere in the tree, and that
`origin/master` is untouched at `637307e83951ffe23e768ed8e50ddaf8712b0660`.

All four nits are defects in the **governing prose records** (execution record,
input-refresh record), not in the candidate. Two of them (NIT-1, NIT-2) are
overstatements of verification strength — a claim of byte-exact replay that is
not byte-exact, and a wrong classification sitting inside a paragraph headed
"Independent verification". Neither changes any outcome, but both are the
familiar failure mode in this repo's evidence record and should be corrected in
the prose before this candidate's evidence set is presented as final. **They do
not block acceptance of the bytes.**

### Scope boundary of this verdict

This audit accepts the *bytes* of `62bf661b` and its Windows suite result. It
establishes nothing about Ubuntu, staging, deployment, or runtime for these
bytes. Gate-A's A-0..A-9 acceptance belongs to `2ce41e34` on its staging host
alone and does **not** transfer to the integrated SHA — the candidate's own
README says so, correctly. The second flagship lane (`gpt-5.6-sol`) must agree
before T0 acceptance is complete.

### Compliance with hard exclusions

Read-only on every repository file. The only file written inside the deliverable
path is this verdict. Temporary log/probe files were written solely to the
session scratchpad outside the repository. No commit, push, branch, reset,
checkout, or stash. No host, network, deployment, credential, broker, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, or trading action. No sub-delegation to any
other model or CLI. `C:\LAB\Tradingview_LAB_CLEAN` and `C:\R7FINAL` were never
read or written.
