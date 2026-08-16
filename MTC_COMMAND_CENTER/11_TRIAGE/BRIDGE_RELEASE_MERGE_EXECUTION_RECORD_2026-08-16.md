# Bridge release integration merge — execution record — 2026-08-16

Status: EXECUTED — branch-local integration candidate created. NOT accepted,
NOT deployed, NOT merged to master. Authority: owner-approved accelerated
full-completion contract (`OWNER_DECISION_ACCELERATED_COMPLETION_2026-08-16.md`,
clause A: current release assembly), executing
`BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md` with the committed input refresh
`BRIDGE_RELEASE_MERGE_RUNBOOK_INPUT_REFRESH_2026-08-16.md`.

Executed by the Fable 5 Lead in the isolated worktree
`C:\BRIDGE_RELEASE_INTEGRATION_20260815` (created this session from `C:\MRGRUN`,
shared object store, primary checkout untouched).

## Result identity

| Name | Exact identity |
|---|---|
| **Integrated candidate** | `62bf661b065dec5b5d9895d83575581fe369252d` |
| Integrated tree | `e2cb5dadd1537e933460aeecd5cdcf343c31d7d0` |
| Parent 1 (repaired WP-I, refreshed W) | `7d4e9a96e07b34a0c3d92315912d7818168b830b` |
| Parent 2 (Gate-A) | `2ce41e34bceb599d80af24c5c33d835820ec321b` |
| Branch | `integration/bridge-release-20260815` (tip = integrated candidate) |
| `origin/master` unchanged | `637307e83951ffe23e768ed8e50ddaf8712b0660` |

## Observed runbook outputs (verbatim key lines)

```text
MASTER=637307e83951ffe23e768ed8e50ddaf8712b0660
GATE_A=2ce41e34bceb599d80af24c5c33d835820ec321b
REPAIRED_WPI=7d4e9a96e07b34a0c3d92315912d7818168b830b
MERGE_BASE=4d2228cf8985ce755c398cceff23f777a99d5404
GATE_A_GITATTRIBUTES=49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b
WPI_GITATTRIBUTES=49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b
MERGE_TREE_LINE_COUNT=16359
CHANGED_IN_BOTH_COUNT=2
ADDED_IN_REMOTE_COUNT=3
CONFLICT_MARKER_LINE_COUNT=6
INTEGRATION_START_HEAD=7d4e9a96e07b34a0c3d92315912d7818168b830b
INTEGRATION_BRANCH=integration/bridge-release-20260815
INTEGRATION_STATUS=<empty>
MERGE_RC=1
IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
README_STATUS_MATCH_COUNT=1
README_HISTORY_PARAGRAPH_MATCH_COUNT=1
WAL_IMPORT_CLOSING_MATCH_COUNT=1
WAL_REMOVE_STALE_BASELINE_IMPORT_MATCH_COUNT=1
WAL_DYNAMIC_SOURCE_QUERY_MATCH_COUNT=1
WAL_DYNAMIC_ASSERTION_MATCH_COUNT=1
IBKR_PAPER_BRIDGE/deploy/linux/README.md=4069904b7707da9efa875661769fc29435504b33
IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py=12b17ab595dad24fcff6397d0689effadbfe2f67
BLOB_FENCE_33_OF_33=PASS
STAGED_PATH_COUNT=32
POST_SUITE_BLOB_FENCE=PASS
INTEGRATED_SHA=62bf661b065dec5b5d9895d83575581fe369252d
INTEGRATED_TREE=e2cb5dadd1537e933460aeecd5cdcf343c31d7d0
PARENT_1=7d4e9a96e07b34a0c3d92315912d7818168b830b
PARENT_2=2ce41e34bceb599d80af24c5c33d835820ec321b
BRANCH_TIP=62bf661b065dec5b5d9895d83575581fe369252d
COMMITTED_BLOB_FENCE=PASS
COMMITTED_FIRST_PARENT_PATH_COUNT=32
FINAL_STATUS=<empty>
MASTER_UNCHANGED=637307e83951ffe23e768ed8e50ddaf8712b0660
```

Full integrated suite, run from the integration root with `PYTHONUTF8=1`,
`python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests`
(Python 3.14.2, pytest 9.0.2, Windows):

```text
1360 passed, 1 warning in 191.54s (0:03:11)
```

Exactly the runbook's frozen acceptance criterion (`1360 passed, 1 warning`).
The single warning is the known Starlette test-client deprecation. The suite
created no unstaged or untracked file and altered no fenced blob
(`POST_SUITE_BLOB_FENCE=PASS`).

## Deviations of record (all environmental or pre-recorded; no content deviation)

1. **`W := 7d4e9a96`** per the committed input-refresh record
   (`BRIDGE_RELEASE_MERGE_RUNBOOK_INPUT_REFRESH_2026-08-16.md`), which
   supersedes only the runbook's `W` row. PARENT_1 expectation updated to
   match. Verified this session that the branch tip still equals `7d4e9a96`
   before starting.
2. **`core.longpaths=true` passed one-shot (`git -c`)** to the worktree-add,
   merge-completion, add, and commit commands. The first attempt STOPped on
   Windows `Filename too long` for a deep QuantLens research path unrelated to
   the Bridge universe. No persistent config change was made to the shared
   repository. The failed first attempt auto-cleaned its directory; the
   zero-work branch ref it left (pointing exactly at `7d4e9a96`) was deleted
   and worktree metadata pruned before the successful retry.
3. **CRLF normalization in the §2.5 transformer.** The checkout is CRLF
   (`core.autocrlf`), so the runbook's LF replace patterns could not match a
   real Windows working tree — the authoring and readiness lanes had only ever
   applied the transforms in-memory to LF blob bytes. The transformer was run
   with CRLF→LF normalization on read and UTF-8/LF bytes on write; under
   `* text=auto` the staged blobs are identical, proven by both synthesized
   OIDs matching the fence exactly (`4069904b…`, `12b17ab5…`).
4. **Runbook §5.1 expected path list corrected against live Gate-A.** Gate-A
   itself contains `credential_free_disarmed` in **seven** paths totalling 17
   occurrences (routes.py 1, app.py 7, README 1, unit template 1, verify.sh 1,
   test_credential_free_disarmed.py 4, **test_linux_deployment.py 2**). The
   runbook's §5.1 list named six paths while correctly requiring 17
   occurrences — an authoring defect (the seventh path was dropped from the
   hand-written expectation). The intended invariant — integrated index has
   the same path set and per-file occurrence counts as Gate-A — was verified
   by direct live comparison and **holds exactly**. Runbook defect noted for
   the record; no candidate drift.

## What this does and does not establish

**Does:** one exact integrated release candidate exists, branch-local, with
byte-pinned Bridge content (33-blob fence), the exact 32-path first-parent
delta, Gate-A credential-string parity, and a green full suite on Windows.

**Does not:** acceptance (the tier-required audit of the integrated candidate
has not run), any Ubuntu/staging evidence for these bytes, any deployment,
any host contact, any transfer of Gate-A's A-0..A-9 acceptance (that belongs
to `2ce41e34` on GATEA-STAGING only). No TESTNET/mainnet, broker, ARM, order,
credential, or master-merge action occurred.

## Next in chain

Tier classification: the integrated candidate contains deploy scripts, systemd
unit, verify.sh — **T0**. Required: two independent flagships, exact
`claude-opus-5` + `gpt-5.6-sol`, xhigh, fresh sessions, on the pinned
candidate `62bf661b`. D026 applies to any new regression test offered as
closure evidence (none was created in this merge — the WAL test change is the
accepted A2 repair re-derived onto Gate-A's base: the resulting assertion line
is byte-identical to the accepted one, and the synthesis additionally removes
Gate-A's `SCHEMA_VERSION_BASELINE` import and its two-line comment; the D026
evidence for the repair lives with the suite-anomaly repair acceptance).

## Post-acceptance corrections — 2026-08-16 (from the Claude T0 verdict's nits)

Candidate bytes unchanged; these correct this record's prose only
(`T0_62BF_CLAUDE_VERDICT_2026-08-16.md`, NIT-1 and NIT-4):

1. The earlier wording "replayed byte-exactly" (corrected in place above) was
   wrong — the merged WAL synthesis `12b17ab5…` differs from the T1-audited
   WP-I-based repair blob because the two bases differ (9+/4− vs 8+/1−); only
   the assertion line is byte-identical.
2. Describing Gate-A's base assertion as "stale" was wrong: on Gate-A's base
   (`str(SCHEMA_VERSION_BASELINE)`) the assertion was already dynamic and
   green; the resolution is a harmonization to the accepted WP-I repair shape,
   not a defect fix. The fenced content is exactly what the runbook requires.
