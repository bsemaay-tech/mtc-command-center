# WP-L Phase 2 command-gap proposals — independent audit (2026-08-09)

## Verdict

**REQUEST_CHANGES.** Commit `779bd038957a192db47ff7ad68eb51304a2fba46` is a useful inventory,
but its proposed scripts are not execution-ready and must not be copied to the host. The audit was
read-only; no proposal or product file was edited.

Audited path:
`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md`
(blob `2478a786de083c04595b00bfed13eb5b94e774fb`). Product facts were checked against candidate
`2ce41e34bceb599d80af24c5c33d835820ec321b`, not the documentation branch.

## Required findings

### F1 — P0 — every proposed evidence log can follow a dangling symlink

Proposal `:64-68` promises no-clobber output, but every script uses only `[[ -e "$LOG" ]]` before
`exec > "$LOG" 2>&1` (first instance `:122-127`; repeated at `:220-225`, `:359-364`, `:439-444`,
`:484-489`, `:609-614`, `:726-731`). A dangling symlink is false for `-e`; redirection then follows it
and truncates/writes its target. The global no-clobber claim is therefore false and can destroy evidence
outside the intended log path. Required repair: reject both existing objects and live/dangling links,
prove the parent chain canonical/non-symlink, and create the log atomically/no-clobber.

### F2 — P0 — B3 accepts permission drift and omits a claimed binding check

Proposal `:159,164` accepts root mode `0444`, but candidate `verify.sh:79,105` requires exactly `0555`.
Proposal `:160,165` uses `find ... -perm -0200`, which detects owner-write only; a group-only or
other-only writable file passes. Candidate `common.sh`'s immutable-tree check uses the any-write-bit
predicate, and `verify.sh:80,106` invokes it. The proposal also claims to reproduce `verify.sh:123-136`
but never checks the install manifest's candidate SHA and payload-manifest binding at `verify.sh:129-135`.
Its whole-tree `find` sweeps are additionally unbounded despite the section calling the check bounded.

### F3 — P0 — C1 cannot close no-dangling persistence and cannot prove graceful exit as written

Proposal `:193,208` says C1 closes WP0 I-R4, but it records no protected persistent-state baseline before
the stop. Its post-stop DB check (`:284-306`) proves only integrity and `app_state != ARMED`; it cannot
detect same-size or valid database changes to orders, trades, fills, risk days, environments, counts, or
IDs. Candidate `wal_state_bundle.py:417-467,561-562` exposes the exact invariant set/hash needed for a
real comparison.

The SIGTERM predicate is also incomplete: `date +%s` is one-second resolution and code `:260` accepts
exactly 45 seconds even though prose `:196-197` classifies `>=45` as timeout/SIGKILL evidence. It records
only `Result`, not a preregistered `ExecMainCode/ExecMainStatus/Result` tuple or bounded journal evidence.
Candidate `app.py:89-100` shows the credential-free shutdown path has no engine stop, but source intent is
not a substitute for a genuine pre/post host proof. C1 must remain blocked until those predicates and a
safe active-writer baseline are separately established.

### F4 — P0 — C2 Scenario A can manufacture an unmasked PASS on command failure or wrong linkage

At `:388`, `systemctl is-enabled ... || true` discards every non-zero status; empty/error output then
passes `enabled != masked` at `:395`. At `:390`, a denied/failed `sudo test -L` is treated exactly like
"not a link". If a link exists but resolves anywhere except `/dev/null`, `:391-395` also accepts it as
unmasked. The candidate first-start unit has no `[Install]`, so the preregistered exact unmasked token is
`static`, not merely "anything except masked". Require fail-closed rc adjudication, exact `static`, the
canonical fragment path, and no mask-path object/link.

### F5 — P1 — neither reboot scenario proves persistent-state preservation

C2-A `:408-418` and C2-B-POST `:532-542` inspect only post-reboot `app_state != ARMED`. There is no
pre-reboot immutable invariant snapshot and no post-reboot equality comparison. Scenario B also performs
a stop before reboot (`:458-459`), so any change caused by that stop is indistinguishable from reboot
drift. The result may establish an absolute DISARMED predicate, but it cannot close a pre/post persistence
predicate or be described as proof that reboot preserved state.

### F6 — P0 — C3 is not executable against the candidate API

Proposal `:661-670` imports `collect_invariants` and calls `collect_invariants(db_path)`. Candidate
`wal_state_bundle.py:417` requires an open `sqlite3.Connection`, and its first operation reaches
`conn.execute` (`:400-427`). Lead reproduction against the candidate returned exactly:

```text
AttributeError: 'str' object has no attribute 'execute'
```

The proposal's stated hash uncertainty is not the cause: candidate `_canonical_json` at `:212-213` is
exactly `json.dumps(..., sort_keys=True, separators=(",", ":"))`, and `invariants_hash` at `:561-562`
uses it. The wrapper should call the public `invariants_hash` with invariants collected from the open
connection. It must also compare the restored DB hash, prove distinct file identity/no sidecars, and
preserve failed and successful restore evidence. Current `finish()` deletes the restore directory with
`sudo rm -rf` on every exit (`:616-621`), so the primary artifact is destroyed even on failure.

### F7 — P0 — C4 can overwrite the prior rollback record

The proposal invokes the real rollback immediately at `:755-759` without asserting
`/etc/mtc-bridge/rollback_manifest.json` absent. Candidate `rollback.sh:70-71` rejects a symlink only;
`:158-180` uses unconditional `cat >` and overwrites an existing regular manifest. That destroys the
earlier rollback record. Require a fail-closed no-clobber precondition immediately before invocation and
a dry-run rehearsal first (`rollback.sh:48` supports it).

### F8 — P0 — C4's "byte-for-byte" state-preservation claim is false

Proposal `:751-781` compares only `find` output containing basename and byte count. Any same-size content
change passes, yet `:792-793` calls the result byte-for-byte preservation. It does not compare hashes or
candidate `wal_state_bundle` invariants, validate the rollback-manifest fields, or prove the mask link
resolves exactly to `/dev/null`. The real invocation is therefore not admissible from this evidence.

### F9 — P1 — process/tool failures are repeatedly collapsed

The C1/C2/C4 scripts use `pgrep ... || true` (`:275`, `:399`, `:523`, `:769`) and infer "no process"
from an empty temp file. A non-match is rc `1`; syntax/fatal/tool errors are different outcomes and must
STOP, not be normalized. The same error class appears in `systemctl is-enabled ... || true`; Scenario A
turns it into an actual false PASS (F4), while the other scenarios at least fail their later equality.

## Non-blocking documentation nits

- Shared contract `:67-72` says PASS is the last line, but every EXIT trap prints a trap line after the
  PASS marker. Define the machine parser against the actual final-line contract.
- C3's canonicalization caveat (`:569-578`) is stale/misdirected: the candidate canonical form matches;
  the real defect is the wrong `collect_invariants` argument and failure to use `invariants_hash`.
- `restored_sha` (`:653-654`) is printed but never compared to the accepted bundle hash.

## Accepted portions

- Candidate/reference qualification is generally explicit, and the rollback blob claim reproduces as
  `4b36674dcb1baa7c3b119cac98f8e6017b1f1566`.
- The proposal correctly does not invent a `wal_state_bundle restore` CLI subcommand.
- C5 remains blocked and supplies no credential, broker, TESTNET, ARM, order, or egress procedure.
- No script starts, enables, or unarms the bridge; recovery start remains separately scoped.

## Checks executed

- `git show --check 779bd038...` — clean.
- Exact proposal blob — `2478a786de083c04595b00bfed13eb5b94e774fb`.
- Exact candidate blobs/read: `app.py`, `verify.sh`, `common.sh`, `wal_state_bundle.py`,
  `rollback.sh`, and first-start unit template.
- Candidate rollback blob reproduced — `4b36674d...f1566`.
- Python read-only API falsification — wrong argument raises the `AttributeError` above;
  candidate canonical JSON comparison returned `canonical_match=True`.
- `bash` is unavailable on this Windows machine; no shell execution is claimed.
- Claude Opus 5 xhigh alternate CLI route — timed out at 604 s, no verdict.
- GLM-5.2 Z.AI Coding Plan route — timed out at 604 s, no report.
- DeepSeek V4 Flash ClinePass — `session.hook` error and no subscription-model access.
- DeepSeek API fallback — exhausted 24 iterations after sandbox/path drift, no `finish()`/verdict.
- Audit worktrees `C:\WP2AUD`, `C:\WP2AC`, `C:\WP2AG`, `C:\WP2AD`, and candidate worktree
  `C:\WP2CAND` — all clean after review.

## Routing record

```text
Classification          : Tier 4 protected Bridge safety/evidence audit
Protected               : yes — stop/reboot/persistence/rollback/broker boundaries
Models/providers        : Codex Lead; Claude Opus 5 CLI; GLM-5.2 Z.AI; DeepSeek ClinePass then API fallback
Cheaper-model rationale : exact owner routing request plus protected cross-cutting safety scope
Exact paths             : proposal file plus six candidate source files named above
Context/tool budget     : one 43 KB proposal; candidate sources individually below 60 KB; 10 min/model
Fallback                : ClinePass -> bounded `_deepseek_driver`; Lead source reproduction remains authoritative
External API credits    : yes for DeepSeek fallback only; no for GLM Coding Plan / Claude subscription
```

## Disposition and next steps

1. Do not transfer, extract, or execute any proposed script from `779bd038`.
2. Produce a bounded repair specification from F1-F9; do not edit the proposal in this audit unit.
3. A future implementation must be re-audited from a frozen commit and must falsify each claimed
   fail-closed/no-clobber predicate before execution authority is considered.
4. Existing budget and authority holds remain unchanged; this audit grants no host action.
