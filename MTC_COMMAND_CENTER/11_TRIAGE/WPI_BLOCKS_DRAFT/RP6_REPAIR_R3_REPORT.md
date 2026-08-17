# RP6-P0 repair round 3 — the three re-audit R2 residuals (FINAL T0 round)

Date: 2026-08-10
Implementer: `claude-opus-5` at `xhigh`, fresh session, local Git Bash 5.2.37
Audit tier: **T0** — host/execution-domain preflight
Cycle: Claude flagship re-audit round 2 (`RP6_CLAUDE_REAUDIT_R2_2026-08-10.md`,
verdict REQUEST_CHANGES on 3) → bounded repair round 3
Contract: `KICKOFF_RP6_REPAIR_R3.md`

**Round-cap position.** `AGENTS.md` caps T0 at three repair/re-audit rounds. This
is round 3. The cap is now exhausted: the next flagship verdict is terminal for
this cycle. If it accepts, the loop closes; if it does not, the Lead must stop and
report the blocker to Barış rather than opening a fourth round.

## Scope

Permitted writes, and the only files written:

1. `WPI_BLOCKS_DRAFT/RP6-P0.sh`
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`
3. `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md`
4. `WPI_BLOCKS_DRAFT/RP6_FULLBLOCK_REPAIR_REPORT.md`
5. `WPI_BLOCKS_DRAFT/RP6_REPAIR_R3_REPORT.md` (this file, new)
6. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — **§8.1 row 1 only**

`RP7-WPI-RO.sh`, `SELF_QA_RP7.md`, `STATUS_RP7.md`, `TRANSPORT_PLAN.tsv`,
`transport_runner.ps1`, `run_p0.sh`, `run_ro.sh`, `remote_setup_wpi.sh` and
`remote_extract_verify_wpi.sh` are concurrently owned by other sessions and were
**not** read for edit and not written. Concurrent working-tree edits inside the
prereg draft (the §3 transport-set derivation contract) were preserved: the row-1
change is a single-line replacement made with an exact-match edit, and `git diff`
confirms §3's edits are still present and untouched.

No host was contacted. No network command was run. No commit was made. No Pine,
parity, MTC strategy, trading, deployment, backtest or broker surface was
involved.

## Executable identity

```text
audited_pre_repair_sha256=bff3c86e6e9b565c55da34580284f22c80253d9e931d879fd749459bac85b7cf
audited_pre_repair_bytes=57441
round2_sha256_superseded=041c9da9769e36638c9785b54afc638fa8e7b475a6d24238fc10388916c048db
round2_bytes_superseded=66381
round3_sha256=2d9b166eacfc39ebe0d8d89edb5860876ccc4d9f0ff97f9e10a228dbcf96289e
round3_bytes=71743
bash_n=PASS
cr_bytes=0
lf_bytes=1328
bom=false
non_ascii_bytes=0
trailing_whitespace_lines=0
```

## Finding → disposition → evidence

### Finding 1 — MEDIUM. Fabricated `rc=` and a lost resolved path (Pattern 9)

**Disposition: repaired in the block, and §8.1 row 1 amended.**

`RP6-P0.sh` (`p0_resolve_tool`) now emits:

```text
tool_not_evaluable tool=$t path=$resolved rc=na detail=access_builtin_x_denied mechanism=access_builtin_x
```

Both halves of the finding are closed: the required `tool_not_evaluable` token is
kept, the resolved path the pre-repair arm carried is restored, and `rc=126` — a
status no probe produced — is gone.

The kickoff offered a choice, and the row was amended, because `rc=<n>` could not
be satisfied honestly. P0's stated discipline is that resolution and executability
are decided by shell builtins alone (`command -v` and the access(2) predicate
`[ -x ]`), so **no arm of this block ever invokes an inventory tool** and none can
carry an invocation status. §8.1 row 1 now reads
`tool_not_evaluable tool=getent path=<p> rc=<n|na> detail=<d> mechanism=<m>`, makes
`rc=na` mandatory for the `mechanism=access_builtin_x` arm, reserves `rc=<n>` for
an arm that actually invoked something, and records both reasons inline —
including why `path=<p>` is required (the `P0_tool name=… path=…` inventory lines
are printed by a later loop this STOP never reaches, so this is the only place the
rejected object is named).

**Executed evidence** — full-block fence, same non-executable fixture on both
sources:

```text
=== F7 PRE tool invocation token ===
P0_STOP reason=tool_not_executable tool=getent path=<Q>/nonexec-tool mechanism=access_builtin_x
=== F7 POST tool invocation token ===
P0_STOP reason=tool_not_evaluable tool=getent path=<Q>/nonexec-tool rc=na detail=access_builtin_x_denied mechanism=access_builtin_x
ASSERT_MET label=F7_TOOL_POST token=[tool_not_evaluable tool=getent path=<Q>/nonexec-tool rc=na detail=access_builtin_x_denied mechanism=access_builtin_x]
ASSERT_MET label=F7_TOOL_POST_NO_FABRICATED_RC forbidden_token_absent=[rc=126]
ASSERT_MET label=F7_TOOL_PRE_PATH token=[path=<Q>/nonexec-tool]
```

The forbidden-token assertion is the point of the repair, and the `F7_TOOL_PRE_PATH`
assertion pins the regression the R2 audit found — the pre-repair arm *did* carry
`path=`, so restoring it is a closure, not a preference. The draft half is
falsified against two revisions:

```text
F1_DRAFT_RED numeric_only_row1_at_0bbc3591=1
F1_DRAFT_GREEN rc_na_row1_in_worktree=1
```

### Finding 2 — MEDIUM. The repair's own D026 evidence no longer reproduced (Pattern 10)

**Disposition: repaired at the source, then all four transcripts re-executed and
replaced.**

**(a) The fence could only ever run once.** The RED side read
`git show "HEAD:$target"`, which became the *repaired* object the moment the
repair was committed as `90d8d447`; every PRE arm then executed repaired bytes,
and the fence died at `[ "$f3p" -eq 0 ]` at line 52 of 143 without ever printing
its summary. The draft comparison at the end had the same defect — the grep for
the old row-3 order returned nothing at HEAD, fatal under `set -e`.

Both are now pinned to the immutable revision **`0bbc3591` (`= 90d8d447^`)**, the
same `$pre_rev` idiom the C13 sections at lines 667 and 1184-1185 already used.
The fence additionally *prints* which bytes its RED arms ran, so a future reader
does not have to trust the pin:

```text
RED_SOURCE rev=0bbc3591 sha256=bff3c86e6e9b565c55da34580284f22c80253d9e931d879fd749459bac85b7cf bytes=57441
```

That digest and byte count are the audited pre-repair identity, re-derived by the
fence itself at run time.

**(b-d) The three stale transcripts.** Re-executed and replaced. All five recorded
outputs in `SELF_QA_RP6.md` are now current:

| Section | Extraction | Result | Transcript |
|---|---|---|---|
| Full-block D026 fence | `sed -n '1678,2068p'` | rc 0, `result=PASS` | matches after normalizing only the random `mktemp` root — `NORMALIZED_TRANSCRIPT_MATCH=True` |
| C13 R3 arm | `sed -n '664,787p'` | rc 0, `cases=16 result=PASS` | **byte-identical** (`cmp` clean) |
| C13 R3 `:?` backstop | `sed -n '952,1035p'` | rc 0, `inputs=2 mutations=2 cases=4 result=PASS` | **byte-identical** (`cmp` clean) |
| C13 R4 arm | `sed -n '1181,1346p'` | rc 0, `cases=27 result=PASS` | **byte-identical** (`cmp` clean) |
| F2 freeze-literal gate | `sed -n '2286,2319p'` | rc 0, `result=PASS` | **byte-identical** (`cmp` clean) |

The harness *bytes* of the three C13 sections were not touched; only their
recorded output was regenerated. The five moved lines in the two arm harnesses
are the F7 grammar unification the full-block repair performed (`wrong_mtc_gid`
and `wrong_gatea_uid` now report the single `identity_unexpected
observed_numeric=… expected_numeric=… account=…` grammar). Case counts,
polarities and verdicts are unchanged.

**The backstop's kill mechanism, stated honestly.** The `precheck_and_backstop`
double-mutant no longer reaches the first *use* of `P0_STATE_UID`: the row-8
attestation pre-check added by the F2 repair refuses first, at rc 3, because that
harness's prelude supplies no `P0_ATTESTED_*` values. The mutant is still killed —
the named `:?` message is still absent, and the assertion is now unmet on rc *and*
message — and the GREEN case is still evidence about the backstop: what the
backstop buys is a refusal naming **this** input at the point it is read, versus a
later complaint about something else entirely.

I deliberately did **not** inject filled `<PIN-AT-FREEZE>` literals into that
harness to force the older `unbound variable` mechanism back into view. Reaching
it on draft bytes requires fabricating five deploy-channel attestation values, and
putting a fabrication inside a D026 harness to make an older transcript match
again is the opposite of what D026 is for. The reading paragraph in
`SELF_QA_RP6.md` was rewritten to describe the mechanism that is actually
observed, and states this choice.

### Finding 3 — LOW/MEDIUM. Row 8 asserted a binding without disclosing its limits (Pattern 2 / 9)

**Disposition: both halves of the auditor's remedy applied — the preferred
discrimination *and* the disclosure — because neither alone is honest.**

*The discrimination (the auditor's preferred fix, no new tool).* New
`p0_read_object_device` / `p0_assert_ns_link_off_root` compare the device of each
followed namespace link against the device of the root object. The root device
costs nothing extra: it is the left field of the `%d:%i` identity the gate already
reads. A kernel namespace inode lives on the anonymous `nsfs` superblock, so a
fabricated link — or the ordinary file a fabricated link resolves to — allocated
on the root filesystem is refused even when its readlink text, its grammar and the
root `dev:inode` are all perfect. That is precisely the private-mount-namespace
case prereg row 8 exists to catch and the one the equality comparisons cannot see.
It runs after the equality comparisons, so a genuine divergence still reports as
`execution_domain_mismatch`, and before the evidence line and the row-9 manager
query, both of which stay unreachable until it holds.

*The disclosure.* The device test does **not** establish procfs identity: a
fabrication placed on any *other* filesystem would carry a distinct device too and
would pass. The evidence line therefore states the residual rather than implying a
binding:

```text
P0_execution_domain user_ns=… mnt_ns=… pid_ns=… net_ns=… root_mount_id=2049:2 binding=deploy_attested_exact visible_pid1_comparison=not_used procfs_identity=not_established ns_link_devices=77,77,77,77 root_device=2049 ns_link_devices_distinct_from_root=yes
```

and `procfs_mount_identity_of_the_namespace_links` was added to the terminal
`P0_claim does_not_establish=` list, joining the block's existing
`manager_identity=not_established` and `provenance=not_established` qualifiers.

**Executed evidence** — four new fence cases:

```text
=== F3 POST crafted procfs on root filesystem ===
P0_STOP reason=execution_domain_unattested field=user_namespace detail=namespace_link_on_root_filesystem device=2049 root_device=2049
RC=3
=== F3 RED device-check-removed mutant ===
P0_execution_domain … binding=deploy_attested_exact … procfs_identity=not_established ns_link_devices=2049,2049,2049,2049 root_device=2049 ns_link_devices_distinct_from_root=yes
RC=0
ASSERT_MET label=F3_FAKE_PROCFS  …
ASSERT_MET label=F3_MUTANT  …
ASSERT_MET label=F3_DISCLOSURE token=[procfs_identity=not_established ns_link_devices=77,77,77,77 root_device=2049 ns_link_devices_distinct_from_root=yes]
ASSERT_MET label=F3_CLAIM_RESIDUAL token=[procfs_mount_identity_of_the_namespace_links]
```

The mutation deletes **only** the device comparison, so the mutant still reads and
prints the devices — its evidence line shows all four namespace links sitting on
root device 2049 while still claiming `ns_link_devices_distinct_from_root=yes`,
which is exactly the false sentence the comparison prevents. The check is
therefore load-bearing by execution, not by reading. The stat shim was extended to
answer `-c '%d'` as well as `-c '%d:%i'`, and `NS_DEVICE` drives the honest case
(77) and the crafted case (2049) from the same fixture.

**A stronger option, deliberately not taken.** `stat -f -c '%t'` would report the
filesystem magic (nsfs `6e736673`) and would also need no new tool, closing the
"fabrication on some other filesystem" residual outright. It was not used because
its `-f`/`-L` semantics cannot be executed or falsified anywhere in this
Windows-hosted session, and D026 forbids offering an unexecuted mechanism as
closure evidence — especially on a T0 surface where a wrong assumption STOPs a
real deploy at rc 3. It is recorded in `SELF_QA_RP6.md` as the successor's option,
to be taken when a Linux fixture is available.

### Nit 1 — the `(os error 2)` alternative and its false provenance

**Disposition: attribution corrected AND the alternative dropped.** Stating the
choice, as the kickoff required: **dropped.**

`(os error N)` is a Rust `std::io::Error` rendering emitted by uutils coreutils,
not GNU. uutils derives its message prefix from the **basename** of `argv[0]`,
while `$P0_STAT` is always absolute (`p0_resolve_tool` refuses anything else), so
no producer can emit both halves and the alternative could never match on any
host. Keeping it would have left dead code asserting an observation this package
never made. `RP6_FULLBLOCK_REPAIR_REPORT.md:29` ("GNU's observed `os error 2`
suffix") and `STATUS_RP6_P0.md:24` ("the observed `(os error 2)` ENOENT form") are
corrected, and a comment at `p0_classify_stat_shape` records why the alternative
is gone and where it came from (`RP7-WPI-RO.sh`).

### Nit 2 — the GNU-producer assumption is now stated

A `STATED PRODUCER ASSUMPTION` paragraph was added to the block header: the two
FAIL arms are reached only by matching the exact C-locale GNU coreutils
failure shape carrying the invoked absolute `argv[0]`; on a uutils-coreutils host
no shape matches, every object arm returns `path_probe_unclassified` at rc 3, and
the audit-1 F1 class returns **fail-closed** — P0 refuses rather than mis-ruling,
and the shape must be re-pinned before such a host is preregistered.

## Nits recorded and NOT acted on this round

R2 nits 3-9 (bash ≥ 4.4 floor undeclared; `P0_RESOLUTION` carrying two meanings;
frozen `root_mount_identity` embedding a reboot-unstable anonymous `st_dev`;
evidence reduction on the domain STOP path; `P0_identity_admitted` printed before
the domain gate; the tautological `readlink -f /` comparison; and the three
carried-forward round-1 nits) are outside the kickoff's three-fix contract and
were left alone deliberately, so that the final round of a capped T0 loop changes
only what the auditor required. They remain on the record in
`RP6_CLAUDE_REAUDIT_R2_2026-08-10.md` for the freeze work.

## Verification performed in this session

- `bash -n RP6-P0.sh` → rc 0.
- SHA-256 and byte count re-derived after the last edit:
  `2d9b166e…`, 71743 B.
- Byte form: 0 CR, 1328 LF, no BOM, 0 non-ASCII bytes, 0 trailing-whitespace
  lines.
- Full-block D026 fence, extracted literally from the document by line range and
  run twice: rc 0 both times, `result=PASS`, `NORMALIZED_TRANSCRIPT_MATCH=True`.
- C13 R3 arm (16 cases), C13 R3 backstop (4 cases), C13 R4 arm (27 cases) and the
  F2 freeze-literal gate: all rc 0, all summaries `result=PASS`, and each
  recorded transcript `cmp`-identical to its re-run.
- `git diff --check` over the written files: clean.
- Write scope confirmed against `git status --porcelain`. This session wrote
  exactly six paths: `RP6-P0.sh`, `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`,
  `RP6_FULLBLOCK_REPAIR_REPORT.md`, the new `RP6_REPAIR_R3_REPORT.md`, and §8.1
  row 1 of `WPI_PREREGISTRATION_DRAFT.md`. Other entries in `git status` moved
  under this session and are **not** its work — `RP7-WPI-RO.sh` and
  `RP7_R4_MAX_RUN_2026-08-10.log` belong to the concurrent RP7 session, and the
  transport files that were dirty at session start are no longer listed because
  that session committed them. None was read for edit or written here.
- Prereg draft preservation: `git diff --stat` on the draft went from 52/8 to
  53/9 insertions/deletions — the single row-1 line. The concurrent §3
  transport-set derivation hunks (`@@ -222 @@`, `@@ -235 @@`, `@@ -240,0 +241,44 @@`)
  are still present and unmodified; my change is the isolated `@@ -451 +495 @@`
  hunk.

## Standing limits (unchanged)

`RP6-P0.sh` is a **DRAFT** — not frozen, not accepted, not dispatchable, and by
construction unable to GREEN end-to-end until a root-authorised deploy channel
outside the tested ssh-login domain mints and embeds the five `<PIN-AT-FREEZE>`
attestation literals. The complete block was never run: it needs the accepted RP0
library and bootstrap, Linux `/proc` namespace objects, the preregistered per-SHA
venv, `getent`/`systemctl` on PATH and a reachable system manager, none of which
exist in Git Bash. This report grants no host-contact, transport, deployment,
budget or trading authority, made no repository write outside the whitelist, and
made no commit.
