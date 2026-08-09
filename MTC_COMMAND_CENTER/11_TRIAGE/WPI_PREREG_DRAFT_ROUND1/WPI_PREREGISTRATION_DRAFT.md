# WP-I staging verification - preregistration DRAFT (round 1.2)

Status: **DRAFT - NOT A PREREGISTRATION, NOT DISPATCHABLE, NO HOST CONTACT HAS OCCURRED**

Unit: `<ALLOCATE-AT-DISPATCH>` - branch `feature/donchian-crypto-ladder`
Frozen candidate: `2ce41e34bceb599d80af24c5c33d835820ec321b`
Check universe: `GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md`
Groups A3, B (B1, B1a, B2, B3, B4, B5, B6), C (C1-C5).
Rigor template: `WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/PREREGISTRATION.md`.
Governing lesson: `.../03_TRANSPORT/B3_STOP_ADJUDICATION.md` (design gap `B3-GAP-ENV`).
Banked-evidence check: `.../EVIDENCE_INDEX.md`.

This document is the *shape* of the WP-I preregistration, not the preregistration
itself. A preregistration mints one-use identifiers; a draft must not, so every
identifier here is a marked placeholder. Writing this document authorizes nothing:
not transport, not host contact, not a socket, not a RUNID. Section 12 states
exactly what has and has not happened.

**Round 1.2 (Codex audit REQUEST_CHANGES applied).** This round applies the four
in-scope findings from `WPI_DRAFT_CODEX_AUDIT_2026-08-09.md` - F1 (B1 metadata
readability), F2 (B6 network-namespace binding), F5 (hash could-not-read divergence)
and F6 (dispatch authority discipline). All four are the same defect class as
`B3-GAP-ENV`: an inability-to-evaluate must STOP (rc 3), never FAIL (rc 1). F3 and F4
(system-manager access) are HIGH in the audit but are **out of scope for this round**
per the round contract; they remain OPEN for a successor round and are recorded as
such in `SELF_QA.md`, not silently resolved.

Three things must happen before any successor of this document is dispatchable, and
each is named at the point where it bites: Stage 1 must freeze and hash the blocks
(sections 3 and 4), the values marked `<PIN-BEFORE-DISPATCH: ...>` must be filled
from the cited record (sections 2 and 8), and the identifiers must be allocated and
tested against `rp0_require_safe_component` (section 1).

**These three are necessary but not sufficient (Codex audit F6, applied round 1.2).**
Two further gates are required and are currently unmet (section 12, and matrix
section 1): (a) **explicit written host-contact/transport authority** - a named
authorisation for SSH/SCP contact with `GATEA-STAGING` and for the operator-side
external probe (op 06); and (b) **the required budget lift** - the matrix records the
exact 50-hour balance as NOT REPRODUCIBLE, so no host execution may be authorised or
performed until a budget lift is granted. The `-Execute` and `-Confirm` switches in
section 6 are technical interlocks on the runner, not authority: flipping both
executes the plan the runner holds, it does not grant the authority or the budget the
plan still lacks. No successor is dispatchable while either (a) or (b) is absent.

---

## 0. Design gate: unprivileged feasibility

Tonight's B3 stage stopped with rc 3 at
`RP0_STOP reason=path_probe_error path=/etc/mtc-bridge/mtc-bridge.env rc=1
detail=stat: cannot statx ...: Permission denied`, because an adversarially
accepted block assumed the operator could `stat` a name inside a `0750 root:root`
directory as the unprivileged login user. The design and the execution model
contradicted each other, and the contradiction was only discovered on the host,
after a one-use RUNID had been spent.

This draft therefore treats unprivileged feasibility as an admission gate on the
*design*, ahead of expectations, argv, or evidence contract. Three rules follow,
and they govern every later section:

1. **Every check admitted to the run plan carries a written reason why it works as
   `gatea` without sudo.** The reason must be a permission-semantics argument over a
   recorded mode and owner, not an assumption of convenience. The full ledger with
   one row per Group A3/B/C check is `WPI_CHECK_FEASIBILITY.tsv`; the reasoning and
   its residual gaps are in `SELF_QA.md`.
2. **Anything that needs privilege goes to DEFER-ROOT-SIDE under the RPD-VERIFY
   pattern (section 10), never into the run plan** - not as a "best effort" probe,
   not as an optional corroboration, not behind a conditional. A block that contains
   an unreachable path will reach it.
3. **`sudo` is not used, and is not probed.** No `sudo -n`, no capability test, no
   fallback. On a host under a zero-mutation authority, testing for privilege is
   itself outside the envelope, and a block that can escalate on some future host is
   a block whose scope is not what this document describes.

The mechanical form of rule 2 is the **path-scope proof** (section 10.2): Stage 1
must emit the sorted set of absolute host paths that appear literally in each frozen
block, and every one must fall inside the section 10.1 allowlist. The distinction
that proof enforces is exactly the one B3 missed - `/etc/mtc-bridge` as a terminal
`stat` target is feasible; `/etc/mtc-bridge/` as a path prefix is not.

---

## 1. Run identifiers and evidence tree

Two stages run, each with its own **one-use** RUNID. A RUNID is never reused: if
allocation fails for any reason it is **burned**, and a retry requires a new
preregistration, not a second attempt with the same identifier. RUNID
`WPLP2-20260809T125940Z-8dc78f08-B3` is already burned this way.

| Field | P0 preflight stage | RO check stage |
|---|---|---|
| `RUNID` | `<ALLOCATE-AT-DISPATCH>-P0` | `<ALLOCATE-AT-DISPATCH>-RO` |
| `EV_STAGE_ID` | `p0` | `ro` |
| `EV_DIR` | `<EV_RUNKIT>/<ALLOCATE-AT-DISPATCH>-P0` | `<EV_RUNKIT>/<ALLOCATE-AT-DISPATCH>-RO` |
| `EV_LOG` | `<EV_DIR>/p0.log` | `<EV_DIR>/ro.log` |

Shared, to be preregistered at dispatch:

| Field | Value | Expected owner | Expected mode |
|---|---|---|---|
| `REMOTE_BASE` | `/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>` | `gatea:gatea` | `0700` |
| `EV_PARENT` | `<REMOTE_BASE>/evidence` | `gatea:gatea` | `0700` |
| `EV_RUNKIT` | `<REMOTE_BASE>/evidence/runkit` | `gatea:gatea` | `0700` |
| `REMOTE_KIT` | `<REMOTE_BASE>/kit` | `gatea:gatea` | `0700` |
| remote archive | `<REMOTE_BASE>/kit/runkit.tar` | - | - |
| `EXTRACT_DIR` | `<REMOTE_BASE>/kit/extracted` | - | `0700`, files `0444` |

Allocation rules, binding on the successor document:

- No identifier in this table may be made concrete here. A draft that mints a RUNID
  has spent it, and a spent identifier cannot be preregistered.
- Every allocated component must be tested against the **accepted** predicate
  `rp0_require_safe_component` from `RP0-LIB.sh` and must be accepted (rc 0), with
  the same refusal set demonstrated (`../escaped`, `a/b`, `.`, `..`, `-lead`, empty,
  `bad name` -> rc 1). Assertion is not demonstration; the transcript goes in the
  successor's self-QA.
- `REMOTE_BASE` and the operator record root are **create-once**. Before allocation,
  both must be shown not to collide with any existing tree - on the host under
  `/home/gatea/`, and operator-side against the two recorded roots
  `C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08` and the same
  path suffixed `-R45B` (`EVIDENCE_INDEX.md`, RUNID ledger).

Two stages rather than one is deliberate. P0 establishes the executing identity and
tool inventory that every feasibility claim in section 0 rests on; the RO stage is
admissible only if P0 confirmed those premises. Folding them together would let the
run assert a result whose precondition it never checked - the B3 failure mode with a
different path in it.

## 2. Preregistered inputs consumed by the accepted blocks

| Variable | Value | Origin |
|---|---|---|
| `WPI_CANDIDATE_SHA` | `2ce41e34bceb599d80af24c5c33d835820ec321b` | frozen candidate; immutable (matrix A1) |
| `WPI_RELEASE_ROOT` | `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b` | matrix B1, B1a; transition inventory |
| `WPI_VENV_ROOT` | `/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b` | matrix B1 |
| `WPI_UNIT_FRAGMENT` | `/usr/local/lib/systemd/system/mtc-bridge-first-start.service` | matrix B2 |
| `WPI_UNIT_FRAGMENT_BYTES` | `3736` | transition inventory, via matrix B2 and template section 8 |
| `WPI_UNIT_FRAGMENT_SHA256` | `<PIN-BEFORE-DISPATCH: GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md; matrix B2 records it elided as 538c1c60...279bd>` | see section 8 risk R1 |
| `WPI_EXPECTED_LOCK_SHA256` | `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e` | matrix A3 / B1a, round-2 and round-3 blocks; LF blob content, 117762 B |
| `WPI_EXPECTED_LOCK_BYTES` | `117762` | same |
| `WPI_EXPECTED_PACKAGES` | `56` | matrix A3 / A6, re-derived at the candidate twice |
| `WPI_STATE_DIR` | `/var/lib/mtc-bridge` | matrix C3 (`/var/lib/mtc-bridge/bridge.db`), C4 |
| `WPI_LOG_DIR` | `<PIN-BEFORE-DISPATCH: unit fragment ReadWritePaths / LogsDirectory; the matrix names the mode 0750 mtc-bridge:mtc-bridge but not the literal path>` | see section 8 risk R2 |
| `WPI_CONF_DIR` | `/etc/mtc-bridge` | matrix B3; adjudication (`root:root`, `0750`) |
| `WPI_CONTROL_ENDPOINT` | `http://127.0.0.1:8790/api/status` | matrix B5, B6 |
| `WPI_SWEEP_BUDGET_S` | `120` | per-tree budget for the `find ... -perm /222` sweep, carried over unchanged from the accepted Stage 2 rationale: `-quit` only shortens a *failing* sweep, so a clean walk is a full walk, and exceeding the budget is STOP, never a pass |

`WPI_EXPECTED_LOCK_SHA256` is the **expected** value, source-derived
(`git cat-file blob 47f53fa2... | sha256sum`). It has never been observed on the
host (matrix round-3 block; B1a "Existing evidence: NONE"). It is therefore a
predicate to be tested, not a fact to be restated, and its failure disposition in
section 8 is *investigate read-only*, not an automatic drift STOP. The Windows
CRLF worktree value `40873556...` (119274 B) is withdrawn and must never be cited.

`WPI_UNIT_FRAGMENT_SHA256` is **never** derived at run time and never re-pinned from
what the host reports. A digest a run reads from the object it is attesting is not
an attestation. Until it is filled from the transition inventory, this draft has no
successor that can be dispatched.

## 3. Expected SHA-256 of every proposed block the stages carry

Blocks marked `<PIN-AT-STAGE-1>` do not yet exist. The WP-I run kit has not been
built; naming a hash for an unwritten file would be the same error class as minting
a RUNID in a draft. The three reused blocks are already frozen and accepted, and
their digests are pinned here from `EVIDENCE_INDEX.md` (01_RUNKIT):

| Block | File | Bytes | SHA-256 | Carried by |
|---|---|---:|---|---|
| RP0-LIB | `RP0-LIB.sh` | 18968 | `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` | P0, RO |
| RP0-BOOTSTRAP | `RP0-BOOTSTRAP.sh` | 1937 | `e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33` | P0, RO |
| RP6-P0 (new) | `RP6-P0.sh` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | P0 |
| RP7-WPI-RO (new) | `RP7-WPI-RO.sh` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | RO |

Archive: `runkit.tar`, `<PIN-AT-STAGE-1>` bytes, `<PIN-AT-STAGE-1>`.

Reuse is byte reuse: Stage 1 must verify `RP0-LIB.sh` and `RP0-BOOTSTRAP.sh` against
the two digests above before admitting them, and the remote extract step re-verifies
every member again from constants before anything is sourced.

**`RP1-B3.sh` (`f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af`) does
not travel in the WP-I kit.** Its accepted bytes contain the `/etc/mtc-bridge/`
probes that produced `B3-GAP-ENV`. Shipping it "but not executing it" is how a
frozen block gets executed: the Stage 2 archive carried five never-executed blocks
precisely because the archive was already frozen, and that concession must not be
extended to a block now known to be infeasible under this execution model. The
scoped replacement is `RP7-WPI-RO.sh`, and it is a new block requiring its own
adversarial acceptance, not an edit of an accepted one.

## 4. Support-script hashes (every executed artifact)

Everything the operator sends is pinned. Four scripts are reused from the accepted
Stage 2 set at their recorded digests (`EVIDENCE_INDEX.md`, 02_PREREG); the rest are
authored for WP-I and pinned at Stage 1.

| File | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `remote_setup.sh` | 4976 | `faee3725325d7155a6309e2371b85a4facba1980f0169c8268e47a75902821b5` | op 01 stdin - create-once remote allocation |
| `remote_extract_verify.sh` | 8270 | `ba0bef0ef6ceb91c445e1d74e2c8d3b6fa7ac01e7e4e10216139b96b28c93db3` | op 03 stdin - archive/member/hash verification + extraction |
| `remote_close_tree.sh` | 7470 | `87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e` | ops 07 and 08 stdin - closed-tree hashing |
| `transport_runner.ps1` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | operator-side recorder (Stage 2 variants exist at 18095/`c5bdb47c...` and 17849/`a48ddc93...`; the WP-I op list differs, so the runner is re-pinned, not assumed) |
| `run_p0.sh` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | op 04 stdin - P0 wrapper |
| `run_ro.sh` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | op 05 stdin - RO wrapper |
| `TRANSPORT_PLAN.tsv` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | the ordered op list; pinned inside the runner |

Reused-script disposition (GLM review N1, mirroring the Stage 2 template §10
discipline): `remote_setup.sh`, `remote_extract_verify.sh` and `remote_close_tree.sh`
are each **kept byte-identical** to the Stage-2-accepted artifacts at the digests
above - reviewed for contract fit against the WP-I op list, unchanged contract, no
edit; any future byte change to any of them voids this draft's §4 and re-opens
review.

Both wrappers inherit the two repairs the Stage 2 wrappers needed: block paths are
refused if they are symlinks (`-f` dereferences, so `-f` alone is not a refusal),
and any child process reads from `/dev/null`, because the wrapper itself arrives on
ssh stdin and a child that read stdin would consume the rest of the script.

The complete set, including the successor of this document, is checksummed in
`WPI_PREREG_SHA256SUMS.txt` at dispatch.

## 5. Exact remote argv

Route (recorded): `gatea@172.24.55.233`, identity
`C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519`. Options are pinned fail-closed on every
op, unchanged from the accepted Stage 2 set:

```
-i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519
-o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o ConnectTimeout=20
```

`BatchMode=yes` refuses to prompt rather than hang. `StrictHostKeyChecking=yes`
refuses an unknown or changed host key rather than trusting it: a changed key means
the host identity is not the one this document describes, and silently accepting it
would defeat the preregistration. `IdentitiesOnly=yes` stops any agent key being
substituted for the named identity.

Every argv element must be free of spaces and shell metacharacters, so the remote
login shell's re-parse of the command is a no-op. Scripts are delivered **on ssh
stdin** to `bash -s --`; no script is written to the host before it runs.

| op | run_when | kind | remote/local argv after the pinned options |
|---|---|---|---|
| 01 | sequence_ok | ssh stdin `remote_setup.sh` | `gatea@172.24.55.233 bash -s -- <REMOTE_BASE>` |
| 02 | sequence_ok | scp up | `runkit.tar gatea@172.24.55.233:<REMOTE_BASE>/kit/runkit.tar` (cwd `01_RUNKIT`) |
| 03 | sequence_ok | ssh stdin `remote_extract_verify.sh` | `gatea@172.24.55.233 bash -s -- <REMOTE_BASE>/kit/runkit.tar <REMOTE_BASE>/kit/extracted <PIN-AT-STAGE-1 archive sha256>` |
| 04 | sequence_ok | ssh stdin `run_p0.sh` | `gatea@172.24.55.233 bash -s --` |
| 05 | sequence_ok | ssh stdin `run_ro.sh` | `gatea@172.24.55.233 bash -s --` |
| 06 | sequence_ok | operator-side probe, **host contact** | single TCP connect attempt to `172.24.55.233:8790`, no payload sent, no ssh (B6 external half) |
| 07 | **always** | ssh stdin `remote_close_tree.sh` | `gatea@172.24.55.233 bash -s -- <EV_DIR P0> <RUNID P0>` |
| 08 | **always** | ssh stdin `remote_close_tree.sh` | `gatea@172.24.55.233 bash -s -- <EV_DIR RO> <RUNID RO>` |
| 09 | **always** | scp down | `-r gatea@172.24.55.233:<EV_DIR P0> .` (cwd `<record>\evidence`) |
| 10 | **always** | scp down | `-r gatea@172.24.55.233:<EV_DIR RO> .` (cwd `<record>\evidence`) |
| 11 | **always** | local only | `local_bind 07 09 evidence\<RUNID P0>` - no host contact |
| 12 | **always** | local only | `local_bind 08 10 evidence\<RUNID RO>` - no host contact |

Every op preregisters `expect_rc = 0`. On the first rc that differs, **first-FAIL
stopping engages**: remaining `sequence_ok` ops are skipped, and only the `always`
ops still run - because a failed stage is exactly when its evidence must be closed,
bound and retrieved. The successor must demonstrate this behaviour, not assert it.

Op 06 is the one op that touches the host without ssh. It is called out here and in
section 12 rather than buried, because "no host contact" is a claim the record has
to be able to make precisely: op 06 opens one TCP connection attempt toward a port
that is expected to be closed, sends nothing, and is recorded operator-side. Its
evidence is bound by the operator-side digest set, not by `CLOSE_DIGEST_SET_SHA256`,
because nothing about it is written on the host.

The scp local paths are bare filenames with the working directory set, so no
argument ever contains a drive-letter colon that `scp` could parse as a host.

## 6. Operator-side transport evidence

`transport_runner.ps1` records, per op, from the first byte and independently of
anything the remote side writes:

- `ops/<id>.argv` - the exact argv sent, one element per line;
- `ops/<id>.stdout`, `ops/<id>.stderr` - complete, separately captured;
- the exit status, compared against the preregistered `expect_rc`;
- `TRANSPORT_RECORD.txt` - the full narration including every digest;
- `TRANSPORT_SHA256SUMS.txt` - sha256 of every captured file.

Record root, **create-once**:
`C:\WPI_ARTIFACTS\WPI_TRANSPORT_<ALLOCATE-AT-DISPATCH>`. If it already exists the
runner stops before any process starts; a rerun therefore needs a new
preregistration rather than a silent overwrite. The path must be shown at allocation
not to collide with the two recorded Stage 2/3B roots (section 1).

This matters because `RP0-BOOTSTRAP` calls `exec > "$EV_LOG" 2>&1`: after the
evidence leaf opens, remote output stops reaching ssh stdout. **Every failure before
that point is visible only in the operator-side record** - and those are precisely
the failures that decide whether a RUNID is burned. Tonight's B3 STOP is the worked
example: the STOP line reached the log because the leaf was already open, but the
`stat` rc that caused it is only interpretable against the operator-side record of
what was sent.

Default mode is a dry run. Execution requires **both** `-Execute` and
`-Confirm <ALLOCATE-AT-DISPATCH>-EXECUTE`; anything else prints the plan and opens
nothing. Both switches are **technical interlocks on the runner, not authority**
(Codex audit F6, applied round 1.2): they gate *whether the recorded plan executes*,
not *whether it is authorised*. They are not a substitute for the written
host-contact/transport authority and budget lift named in the dispatch gates above; a
runner with both switches set still opens nothing the plan is not authorised and
budgeted to do.

## 7. Closing and binding the evidence tree

A process never hashes its own still-open evidence. Ops 07 and 08 run
`remote_close_tree.sh` as **separate ssh invocations after the stage connection has
already returned** - that is the structural guarantee the stage shell has exited.
Because a structural guarantee is not a measurement, the script also computes the
digest set **twice** and refuses if the two passes differ, so a tree that is still
being written is never bound as closed.

It writes nothing into the evidence tree (writing a digest file into the directory
being hashed would change the bytes being attested) and emits, on stdout only:

- `CLOSE_DIGEST <sha256>  <path relative to EV_DIR>` per file, `LC_ALL=C` order;
- `CLOSE_SIZE <relpath> <bytes>` per file;
- `CLOSE_DIGEST_SET_SHA256 <runid> <sha256 of the digest set itself>`.

Ops 11 and 12 then perform the **local half of the binding**: local per-file digests
over the retrieved tree must equal the remote set name-for-name and
digest-for-digest, and the reconstructed digest-set rendering must reproduce
`CLOSE_DIGEST_SET_SHA256`. A remote-only or local-only hash is not a binding.

## 8. Preregistered expectations and predicted first divergence

Preregistering the expected outcome is what stops a result being re-narrated
afterwards. The **recorded** host state (transition inventory, read-only, as carried
into the matrix section 0.3 and B1/B2/B3/B6) is: only release `2ce41e34...321b`
installed at mode `555`; venv counterpart `555`; `/etc/mtc-bridge` metadata only,
`install_manifest.json` 1007 B mode `640`; unit fragment 3736 B mode `644`;
first-start unit active with `Restart=no`, `NRestarts=0`, MainPID 189813; exactly one
bridge listener on `127.0.0.1:8790` (sshd:22 is necessarily also listening - see named
risk R5, wording per GLM review N2); credential-free DISARMED `state_version=1` with
all credential/network/exchange/ARM flags off.

Outcome grammar, unchanged from the accepted Stage 2 contract: **rc 0 = PASS**,
**rc 1 = FAIL** (a probe that ran observed deviant host state), **rc 3 = STOP** (a
probe could not be evaluated). A STOP is never re-read as a PASS, and a STOP never
becomes a FAIL by inference - tonight's adjudication turned on exactly that
distinction, because permission denial precedes the existence question and the
env-file naming risk remains *unresolved*, not *triggered*.

### 8.1 P0 preflight - the premises every later row depends on

| # | check | predicted outcome if it holds | exact predicted first divergence if it does not |
|---|---|---|---|
| 1 | executing identity | `id -un` is `gatea`; uid/gid/groups captured verbatim | `P0_STOP reason=identity_unexpected user=<u> expected=gatea` |
| 2 | group membership | `gatea` is in **neither** `root` **nor** the state/log group | `P0_STOP reason=capability_wider_than_ledger group=<g>` |
| 3 | `ss` present | `command -v ss` resolves | `P0_STOP reason=missing_tool tool=ss` |
| 4 | `curl` present | `command -v curl` resolves | `P0_STOP reason=missing_tool tool=curl` |
| 5 | `sha256sum` present | `command -v sha256sum` resolves | `P0_STOP reason=missing_tool tool=sha256sum` |

Row 2 is an inversion worth stating plainly: **more privilege than the ledger assumed
is a STOP, not a bonus.** If `gatea` turns out to be in the state/log group, the
feasibility ledger's premises are wrong, several DEFER-ROOT-SIDE calls were wrong,
and the correct response is re-adjudication of the scope - not a run that quietly
reaches further than the document it was preregistered under. Rows 3-5 fail closed
to STOP with **no substitution**: a missing tool is not an invitation to improvise a
replacement at run time, which is the whole reason the tool list is preregistered.

### 8.2 RO stage - one row per admitted check

| # | check | predicted outcome if it holds | exact predicted first divergence if it does not |
|---|---|---|---|
| 1 | B2 active | `systemctl is-active` prints `active` | `B2_FAIL reason=unit_not_active state=<s> expected=active` |
| 2 | B2 restart count | `NRestarts` is `0` | `B2_FAIL reason=nrestarts_nonzero value=<n> expected=0` |
| 3 | B2 restart policy | `Restart` is `no` | `B2_FAIL reason=restart_policy value=<v> expected=no` |
| 4 | B2 process identity | `MainPID` is `189813` | `B2_FAIL reason=mainpid_changed value=<p> expected=189813` - **named risk R3**: with `Restart=no` a live unit cannot have self-restarted, so a changed MainPID means a manual restart between the transition inventory and dispatch. That is a FAIL requiring Lead adjudication, never a silent re-pin |
| 5 | B2 candidate binding | `systemctl cat --no-pager` shows both `releases/2ce41e34...321b` and `venvs/2ce41e34...321b` | `B2_FAIL reason=unit_not_bound_to_candidate missing=<releases|venvs>` |
| 6 | B2 no `[Install]` | no `^\[Install\]` line in the fragment | `B2_FAIL reason=install_section_present path=<p>`; and, separately, `B2_STOP reason=grep_error rc=<n> path=<p>` for any grep rc outside {0,1} - the matrix's `&& echo BAD || echo OK` form collapses grep's error class into `OK` and must not be carried forward |
| 7 | B2 fragment identity | `sha256sum` equals `WPI_UNIT_FRAGMENT_SHA256`, size 3736 | `B2_FAIL reason=unit_fragment_digest_mismatch observed=<h> expected=<h>` admissible only after `sha256sum` exited 0 and emitted a syntactically valid 64-hex digest plus the 3736-byte count; `B2_STOP reason=fragment_unreadable rc=<n> path=<p>` for any `sha256sum` open/read/permission/LSM/parent-traversal error - the digest is compared only after a successful rc-0 read, never against possibly empty output |
| 8 | B4 sandboxing | each named property equals the template-declared value (`PrivateTmp`, `ProtectSystem`, `NoNewPrivileges`, `RestrictAddressFamilies`, `CapabilityBoundingSet`, `ReadWritePaths`, `KillSignal`, `KillMode`, `TimeoutStopSec`, `FinalKillSignal`) | `B4_FAIL reason=property_mismatch prop=<P> observed=<v> expected=<v>` |
| 9 | B4 start mode | effective environment carries `MTC_BRIDGE_START_MODE=credential_free_disarmed` | `B4_FAIL reason=start_mode_missing_or_altered observed=<v>` |
| 10 | B3s release root | `/opt/mtc-bridge/releases/2ce41e34...321b` is `0555 root:root` | `B3_FAIL reason=path=<p> mode=<m> owner=<o> expected=0555 root:root` |
| 11 | B3s venv root | venv root is `0555 root:root` | same grammar as row 10 |
| 12 | B3s write bits | no write bit anywhere in either tree | `B3_FAIL reason=writable_path_inside_immutable_tree path=<p>` |
| 13 | B3s sweep budget | both sweeps finish inside 120 s | `B3_STOP reason=sweep_budget_exceeded root=<r> elapsed_s=<n> budget_s=120` |
| 14 | B3s walk completeness | both walks emit **zero** permission diagnostics | `B3_STOP reason=walk_permission_error root=<r> path=<p>` - and this STOP disqualifies row 19 (parity), see the ordering rule below |
| 15 | B3s metadata dirs | `stat` of `/etc/mtc-bridge` is `0750 root:root`; of `WPI_STATE_DIR` and `WPI_LOG_DIR` is `0750 <state-owner>:<state-group>` | `B3_FAIL reason=path=<p> mode=<m> owner=<o> expected=<mode> <owner>` |
| 16 | B3s scope | the block contains no path with prefix `/etc/mtc-bridge/`, `<WPI_STATE_DIR>/` or `<WPI_LOG_DIR>/` | not a run-time predicate: a Stage-1 path-scope proof failure (section 10.2) blocks the freeze, so this can never divergence at run time |
| 17 | B1a lock bytes | `sha256sum` of the installed `requirements.lock` equals `a1881296...bf66e`, size 117762 | `B1a_FAIL reason=installed_lock_digest_mismatch observed=<h> expected=a1881296...bf66e` admissible only after `sha256sum` exited 0 and emitted a syntactically valid 64-hex digest plus the 117762-byte count - disposition **investigate read-only**: weigh a wrong expected value *and* genuine drift, re-check blob -> LF-pinned export -> manifest-verified install before escalating a STOP or dismissing one; `B1a_STOP reason=installed_lock_unreadable rc=<n> path=<p>` for any `sha256sum` open/read/permission/LSM/parent-traversal error (a parent below the recorded 0555 release root, a named ACL, or an LSM rule can deny the read even though the root is 0555) |
| 18 | B1 interpreter | `<venv>/bin/python -V` reports a `3.12.` version; **preflight (GLM F1): `test -x <venv>/bin/python` as `gatea` must succeed first** | `B1_STOP reason=interpreter_not_executable path=<venv>/bin/python` on exec/EACCES/126 denial (never a version FAIL); `B1_FAIL reason=interpreter_version observed=<v> expected=3.12.*` only after the interpreter demonstrably ran |
| 19 | B1 lock parity | `verify_lock.py --check-installed` exits 0 and prints `verify_lock: PASS: lock+installed; packages=56`; **preflight (Codex F1): every metadata object the verifier consumes - every `*.dist-info` directory and its `METADATA` and `RECORD` under `<WPI_VENV_ROOT>/lib/python3.12/site-packages` - is proven open+readable by `gatea` (the wrapper reads each) before parity runs** | `B1_FAIL reason=lock_installed_parity observed=<detail>` ONLY when the verifier ran clean and positively distinguished a genuine installed-set mismatch (a named missing or extra distribution), never on a generic nonzero rc; `B1_STOP reason=metadata_unreadable path=<p>` for any distribution metadata object the process cannot read (open/parse/EACCES/LSM/traversal error - from the preflight probe or from the verifier); `B1_STOP reason=verifier_not_evaluable rc=<n> last_line=<l>` for any other nonzero verifier rc that did not positively distinguish a mismatch. Row 18's `interpreter_not_executable` STOP and this row's readability precondition each disqualify parity entirely |
| 20 | B5 endpoint | `GET /api/status` returns HTTP 200 | `B5_STOP reason=status_endpoint_http code=<c>` - a 401/403 is could-not-evaluate, not a safety finding |
| 21 | B5 flags | `state` DISARMED, `state_version` 1, `mode` `credential_free_disarmed`, `network` disabled, `exchange_conn` disabled, `exchange_enabled` false, `credential_lookup` disabled, `arm_enabled` false | `B5_FAIL reason=flag_mismatch field=<f> observed=<v> expected=<v>`; and `B5_STOP reason=schema_unexpected field=<f>` if a preregistered key is absent under a different spelling - **named risk R4**: these key names come from matrix prose, not from an observed response body |
| 22 | B6 listener set | exactly one listening socket on port 8790, local address `127.0.0.1`; **preflight (Codex F2): `readlink /proc/self/ns/net` is proven equal to `readlink /proc/<MainPID>/ns/net` (MainPID from row 4) before `ss` output is interpreted** | `B6_STOP reason=netns_mismatch caller=<i> service=<i>` if the identities differ (the `ss` observation is from the wrong namespace and proves nothing about the service host); `B6_STOP reason=service_netns_unreadable path=/proc/<pid>/ns/net rc=<n>` if `gatea` cannot read the service netns identity (the binding cannot be established unprivileged - listener-set half routes to RPD-VERIFY, section 10); `B6_FAIL reason=listener_set_unexpected observed=<lines> expected=1x127.0.0.1:8790` admissible only after the binding is proven |
| 23 | B6 no wildcard | no `0.0.0.0`, `::` or VM-IP listener on 8790 (subject to the row-22 namespace binding) | `B6_FAIL reason=nonloopback_listener addr=<a>` admissible only after the row-22 namespace binding held |
| 24 | B6 external closed | operator-side TCP connect to `172.24.55.233:8790` is refused or times out | `B6_FAIL reason=host_reachable_8790 outcome=connected` |

**Binding ordering rule.** Row 19 is admissible **only** after row 14 has held for
the venv tree, row 18's interpreter has demonstrably run, and the row-19
metadata-readability precondition has passed. The row-14 `find` guard proves
traversal and stat-ability of the tree, **not** regular-file readability: a
`*.dist-info/METADATA` at mode `000`, under a named ACL denying `gatea`, or denied by
an LSM rule is stat-able by `find` yet unreadable to the verifying process.
`verify_lock.py --check-installed` enumerates installed distributions from metadata
objects; an unreadable one is indistinguishable from a distribution that is not
installed, so it would surface as a *missing distribution* - a false FAIL against a
correct host, which is the same shape of error as tonight's, arriving through a
different door. If row 14 STOPs, row 19 must STOP too and must never be reported as
a parity FAIL.

**Metadata-readability adjudication rule (Codex audit F1, applied round 1.2).** Row
19 is evaluated under a fixed precedence. The wrapper first proves every metadata
object the verifier consumes - every `*.dist-info` directory and its `METADATA` and
`RECORD` under `<WPI_VENV_ROOT>/lib/python3.12/site-packages` - is open+readable by
`gatea`. Then the verifier's own exit status is adjudicated in this order: a
**positively-distinguished installed-set mismatch** (the verifier named a missing or
extra distribution, having read every object) is the **only** input that may become
`B1_FAIL reason=lock_installed_parity`; every open, parse, permission, LSM or
traversal error from the preflight or from the verifier, and every other nonzero
verifier rc that did not positively distinguish a mismatch, is `B1_STOP`. A generic
nonzero verifier rc must never become `B1_FAIL reason=lock_installed_parity`. This
makes the row-14 traversal guard non-sufficient by construction, exactly as the audit
requires, and is the same defect class as `B3-GAP-ENV` - an inability-to-evaluate
misread as a host finding.

**Interpreter-exec extension (GLM review F1, applied round 1.1).** The recorded host
state proves the venv tree is `0555` (traverse+read for other) but records no per-file
execute bit for `<venv>/bin/python`. Executing it is not a privileged action, so B1
stays INCLUDE - but an exec denial must surface as row 18's dedicated
`interpreter_not_executable` STOP, never as a version or parity FAIL. A false FAIL
against a correct host is exactly the B3-GAP-ENV failure shape arriving through a
different door, and this table exists to make that shape impossible.

**Namespace-binding adjudication rule (Codex audit F2, applied round 1.2).** `ss -ltn`
lists sockets in the *caller's* network namespace, not necessarily the service's. If
PAM, an ssh ForceCommand, or a service wrapper lands the `gatea` login in a private
netns while PID 1 and the bridge listen in the host namespace, `ss` succeeds without
a permission error yet observes the wrong namespace - yielding a false `B6_FAIL` (no
port 8790 listener seen) or, in the mirror case, a false PASS (a matching listener in
the login namespace concealing a bad set in the service namespace). Tool presence and
unprivileged socket visibility do not establish namespace identity. Rows 22-23 are
therefore admissible **only** after the namespace binding is proven:
`readlink /proc/self/ns/net` (always readable by `gatea`) must equal
`readlink /proc/<MainPID>/ns/net` (the service's netns identity, MainPID from row 4).
A mismatch is `B6_STOP reason=netns_mismatch`; an unreadable service netns identity
(EACCES on `/proc/<pid>/ns/net` for a root-owned service process under ptrace/yama
gating) is `B6_STOP reason=service_netns_unreadable` and routes the listener-set half
to RPD-VERIFY (section 10), where a root-authorised channel establishes the binding.
The listener claim is admissible only when the observation is proven to be in the same
namespace as the service. The operator-side external TCP probe (row 24) is independent
corroboration and is unaffected - it probes reachability from outside, which holds or
fails regardless of which namespace `ss` observed.

**Named risks carried into dispatch.**

- **R1** - `WPI_UNIT_FRAGMENT_SHA256` is elided in the matrix (`538c1c60...279bd`).
  Row 7 cannot be preregistered until the full value is read from the transition
  inventory. No successor is dispatchable with this unfilled.
- **R2** - `WPI_LOG_DIR` has a recorded mode but no recorded literal path in the
  inputs. Row 15 cannot be preregistered until it is pinned from the unit fragment's
  `ReadWritePaths`/`LogsDirectory`. Deriving it at run time from the same
  `systemctl show` output the run is asserting against would make row 15 circular.
- **R3** - MainPID equality (row 4) is a strong predicate precisely because
  `Restart=no` forbids self-restart; it is also the row most likely to move for a
  benign reason. It is preregistered as FAIL-with-adjudication so that a benign cause
  is *established* rather than *assumed*.
- **R4** - the B5 field names are unobserved (see above).
- **R5** - "exactly one listener" in the source records is read here as *exactly one
  bridge listener on 8790*. `sshd` is necessarily also listening, since the run
  arrives over ssh. Rows 22-23 are therefore scoped to port 8790, and the full
  listener inventory is captured as evidence rather than asserted against a count.
  If the source records meant a literal global count of one, that reading is
  falsified by the transport itself and must be corrected in the successor.

Any `FAIL` is a **STOP requiring Lead adjudication** - a candidate-repair question,
not a documentation outcome. Any `STOP` from a `stat`, `find`, `grep`, `ss`, `curl`,
`sha256sum`, `readlink`, `mktemp` or clock error, or any internal open/parse/permission
error raised by `verify_lock.py`, stops the stage and is never re-read as a PASS.

**Scope of the WP-I claim, preregistered.** A clean RO stage admits exactly this:
the running unit is the accepted first-start unit bound to the frozen candidate,
its immutable trees are unwritable and byte-consistent with the expected lock, its
sandboxing and start-mode pins are effective, its runtime reports credential-free
DISARMED, and its control port is loopback-only and externally closed. It is **not**
a full `verify.sh` run (that verifier is pre-start and post-Gate-A fails by design -
G2), **not** a permissions proof of the root-owned metadata surface (deferred,
section 10), **not** a SIGTERM/reboot/rollback/backup proof (Group C, section 9),
and **not** WP-L, WP-A or Audit-2 completion.

## 9. What is deliberately NOT preregistered

Nothing in this section has an executable form anywhere in the run kit. Each item is
listed with the dependency that blocks it, exactly as the Stage 2 template does for
C1-C5.

**Group C - mutating checks. No block, no command, no argv, no conditional branch.**

- **C1 (graceful SIGTERM clean shutdown, WP0 I-R4).** Blocked twice over: it needs an
  explicitly named authority lift for `systemctl stop` plus the recovery start, and a
  budget lift; and it has an open **COMMAND GAP** - no verifier asserts "no dangling
  state after SIGTERM". A bounded post-stop evidence procedure must be designed
  locally first. Do not improvise one.
- **C2 (reboot DISARMED).** Blocked on reboot authority + budget, and on a definition
  that does not yet exist: scenario A (plain reboot from the current unmasked state,
  expecting inactive+unmasked) and scenario B (separately authorised stop+mask, then
  reboot, expecting inactive+masked) are different predicates and one must be chosen
  and preregistered before anything runs. `verify.sh` is a pre-start masked-mode
  verifier and is not the post-reboot instrument. **COMMAND GAP.**
- **C3 (WAL-consistent backup/verify/restore on a temporary copy).** Blocked on
  authority + budget, and on a **COMMAND GAP confirmed at the candidate**:
  `wal_state_bundle.py` exposes exactly two subcommands, `create` and `verify`. There
  is **no `restore` subcommand**, so the restore-into-temp wrapper does not exist and
  must be authored locally. Note also that the live DB lives under a directory
  `gatea` cannot read at all.
- **C4 (rollback stop+mask, and release-rebind).** Blocked on KVM2-P4-08
  authorisation + budget. The stop+mask path additionally requires the accepted
  state-manifest hash from C3, which `rollback.sh` makes mandatory (`:57-58`). The
  release-rebind path has an **unmet prerequisite** (G3): only candidate
  `2ce41e34...321b` is installed, and the previous release is already absent. Do not
  invent a target release.
- **C5 (runtime egress / TESTNET-only / no-mainnet / Telegram disposition).** Blocked
  on credential and broker/TESTNET network authority that does not exist, and
  **structurally unobtainable from the current runtime**: at
  `2ce41e34...321b:IBKR_PAPER_BRIDGE/bridge/app.py:149` the credential-free DISARMED
  branch never reaches broker construction, so no broker egress exists to capture. A
  future capture would require a different, separately authorised start mode. ARM
  remains forbidden, and any future capture must remain DISARMED.

**DEFER-ROOT-SIDE - privileged checks routed to RPD-VERIFY (section 10), not to the
run plan.**

- Existence, name, mode and ownership of the env file under `/etc/mtc-bridge`. The
  `bridge.env` vs `mtc-bridge.env` naming question from the Stage 2 expectations
  table remains **unresolved, not triggered**, and this run plan does not adjudicate
  it - permission denial precedes the existence question, and it will precede it
  again for any unprivileged successor.
- `/etc/mtc-bridge/install_manifest.json`: the release-SHA binding, the
  release-manifest binding, and the `requirements_lock_sha256` corroboration of B1a.
- Any per-file mode or ownership assertion *inside* the state and log directories.
- `ufw status` (B6's firewall half).

**Everything the Stage 2 template excludes, excluded here on the same terms.**

- No mutating step of any kind: no service stop, start, enable, disable, mask or
  unmask; no reboot; no rollback rehearsal; no unit write; no chmod/chown of any host
  object outside the run's own create-once tree.
- No credential read, no `POST /api/arm`, no broker/exchange/order/TESTNET/mainnet
  action, no master merge, no KVM2/WP-V action, no deletion of the old payload
  archive, no host reprovisioning.
- No `sudo`, and no probe for `sudo` (section 0, rule 3).
- No `git add`, `git commit`, `git push`, branch or worktree action: Git sequencing
  belongs to the Lead.

## 10. RPD-VERIFY: the root-side channel for deferred checks

### 10.1 Unprivileged path allowlist

The RO stage may reference only these host paths. The list is exhaustive; anything
else is a Stage-1 freeze failure.

| Path pattern | Recorded mode/owner | Why `gatea` can reach it |
|---|---|---|
| `/opt/mtc-bridge/releases/2ce41e34...321b/**` | `0555 root:root` at the root | `r-x` for other on the tree: traversable and readable, not writable |
| `/opt/mtc-bridge/venvs/2ce41e34...321b/**` | `0555` | same |
| `/usr/local/lib/systemd/system/mtc-bridge-first-start.service` | `0644`, 3736 B | world-readable regular file |
| `/etc/mtc-bridge` **(terminal only)** | `0750 root:root` | `stat` of the directory needs search on `/` and `/etc` (both world-searchable), not on the target itself |
| `<WPI_STATE_DIR>` **(terminal only)** | `0750` state owner | same argument via `/var/lib` |
| `<WPI_LOG_DIR>` **(terminal only)** | `0750` state owner | same argument via the log parent |
| `<REMOTE_BASE>/**` | `0700 gatea:gatea` | the run's own create-once tree |
| `127.0.0.1:8790` | loopback listener | loopback is not privilege-gated for a local user |

"Terminal only" is the whole B3-GAP-ENV repair in two words: the path may appear as a
complete `stat` argument and may never appear as a prefix.

### 10.2 Path-scope proof (Stage 1 gate)

Stage 1 must emit, per frozen block, the sorted set of absolute host paths appearing
literally in it, and must show every entry inside section 10.1. The proof is recorded
in the Stage 1 record with the command and its real output, and the archive is not
frozen until it passes. This is a static check over frozen bytes, so it cannot be
satisfied by a run-time guard and cannot be skipped by a run-time branch.

The check `RP1-B3.sh` failed tonight would have failed this proof before transport.

### 10.3 RPD-VERIFY pattern

A deferred check is discharged root-side at deploy time, not by widening this run:

1. A root-authorised channel (deploy-time hook, or a separately authorised root
   session) executes the check and writes its output plus the exact command that
   produced it.
2. The record is hashed at the point of production, by the producing channel.
3. The record reaches the unprivileged verifier by one of two routes, and **which
   route is used is itself a preregistered decision**:
   - **(a) operator-side transport** - the root channel returns the record out of
     band, and it is bound in the operator record. No host mutation.
   - **(b) deposit at a world-readable path** - e.g. `0444 root:root` under a
     preregistered directory outside the protected metadata dirs, which the
     unprivileged run then reads and binds. This **creates a file on the host** and
     is therefore a mutation requiring its own authority; it is not available under
     the current envelope.
4. The unprivileged run **reads and binds** the record; it never re-derives the
   predicate, because it cannot, and a check that appears to re-derive what it is
   actually reading back is worse than no check.

Both routes are named here so that the successor picks one deliberately. Neither is
authorised now, and route (b)'s deposit path is not preregistered in this draft.

## 11. Immutability rules

The successor of this document is void, and a **new** one with fresh RUNIDs is
required, if any of the following changes: any hash in section 3 or 4; the route,
user, identity path or ssh options in section 5; any path in section 1 or section
10.1; either RUNID or stage id; any pinned value in section 2; or the op list in
section 5. In particular, **if the staging VM's IP address is no longer
`172.24.55.233`, the preregistration does not describe the run** - the argv is
pinned, and editing it invalidates `TRANSPORT_PLAN.tsv`, whose digest the runner
pins, which is the intended failure mode rather than a silent edit.

Two rules are added for WP-I, both from tonight:

- **The P0 result is part of the immutability surface.** If P0 reports an executing
  identity or capability set different from the ledger's premise - including a
  *wider* one - the RO stage does not run under this preregistration. The feasibility
  ledger is an argument from a specific identity against specific recorded modes; a
  different identity is a different argument.
- **A filled `<PIN-BEFORE-DISPATCH: ...>` value is frozen at the moment it is filled,
  and is filled from the cited record only.** Filling one from host output would make
  the run attest to a value it read from the object under test.

A failed allocation burns its RUNID. There is no retry pool and no second RUNID
preregistered for either stage.

## 12. Safety state at the moment of this draft

- SSH/SCP/remote invocation count: **0**
- Staging host contact: **none**; no socket opened, no process spawned toward it, no
  TCP connect attempted (op 06 is described, not performed)
- RUNIDs minted: **0**. Unit ids minted: **0**. Record roots created: **0**. Remote
  trees created: **0**
- Blocks authored, built or frozen: **0**; `runkit.tar` for WP-I: does not exist
- Service stop/start/enable/mask, reboot, rollback: **none**
- Credential read, ARM, order, broker/exchange, TESTNET/mainnet: **none**
- A3 re-derivation, B1, B1a, B2, B3, B4, B5, B6 execution: **none**
- C1, C2, C3, C4, C5 execution: **none**, and no executable form of any of them exists
  in this draft
- `sudo` invoked or probed: **none**
- Repository writes: confined to the `WPI_PREREG_DRAFT_ROUND1` directory - this file,
  `WPI_CHECK_FEASIBILITY.tsv`, `SELF_QA.md`. No file outside it was created,
  modified or deleted; no `git add`, `commit`, `push`, checkout, branch or worktree
  action was performed
- Files read: only the five listed in the kickoff's Inputs section

This draft grants no authority. It grants only a *shape* for a preregistration that
does not yet exist, over a run kit that has not been built, for a run that is
budget-blocked and authority-blocked at section 1 of the matrix.

Verification of every feasibility call and every expectation row is in `SELF_QA.md`;
the per-check ledger is `WPI_CHECK_FEASIBILITY.tsv`.
