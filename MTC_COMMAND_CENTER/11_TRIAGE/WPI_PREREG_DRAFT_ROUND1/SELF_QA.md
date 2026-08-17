# SELF_QA - WP-I preregistration draft, round 1.3

How every feasibility call in `WPI_CHECK_FEASIBILITY.tsv` and every expectation row
in `WPI_PREREGISTRATION_DRAFT.md` section 8 was arrived at, and - equally - which of
them rest on something I could not verify.

## 0. What kind of verification was available

This is a documentation unit. **No host was contacted, no command was executed
against `GATEA-STAGING`, and no file outside this directory was read or written.**
So "verified" here can only mean one of four things, and each claim below is tagged
with which:

- **M1 - textual.** The claim is stated in one of the five Input files. Cited.
- **M2 - derived.** The claim follows from POSIX permission semantics applied to a
  mode and owner that an Input file records. The rule used is stated with the
  derivation, so a reviewer can reject the rule rather than having to trust me.
- **M3 - empirical, second-hand.** The claim was demonstrated on the host by the
  burned B3 run, and I am reading the *adjudication's summary* of that run, not the
  log bytes. `b3.log` is not in the Inputs list, so I did not open it.
- **M4 - unverified.** I could not establish it from the Inputs. Every M4 item is
  listed in section 4 with the fail-closed handling that keeps it from becoming a
  silent assumption.

The one permission rule that carries most of the M2 weight, stated once:

> Resolving a path requires **search** (`x`) permission on every parent directory,
> and nothing on the target itself. Reading a directory's *contents* additionally
> requires **read** (`r`) on that directory. Therefore, for `gatea` (not root, not in
> the owning group) against a `0750 root:root` directory `D` whose parents are
> world-searchable: `stat D` **succeeds** and returns `D`'s own metadata, while
> `stat D/anything` **fails with EACCES regardless of whether the name exists**.

That single rule is both why tonight's B3 stopped and why several checks in this
draft are *partial* rather than *no*. The adjudication states the first half of it
independently ("`stat` on **any** name under `/etc/mtc-bridge/` returns `EACCES`
regardless of whether the file exists"), which is a direct M1 confirmation of the
derivation I then apply to the state and log directories.

## 1. Feasibility calls, one by one

**Q1 - A3, classified `n-a` / ALREADY-BANKED.**
M1. The matrix marks A3 `local-static` with "**Authority/budget:** none" and records
"**PASS (static, satisfied):** 56 entries, every entry exact+hashed, no URL/VCS/index
override". A check with no host contact has no privilege question, so `n-a` rather
than `yes` - recording it as `yes` would imply a host operation succeeded.
The lock's static identity is doubly re-derived at the candidate (56 entries, 1345
`--hash=sha256:` lines) across two repair rounds, so I took it as closed rather than
re-planning it, per the kickoff's instruction not to re-plan checks whose evidence
exists.

**Q2 - what "ALREADY-BANKED with the EVIDENCE_INDEX citation" could actually cite.**
This is the one place where I could not follow the kickoff's wording literally, so I
am flagging it rather than papering over it. `EVIDENCE_INDEX.md` is scoped to unit
`WPLP2-20260809T125940Z-8dc78f08` - Stage 1 runkit, Stage 2 preregistration, the B3
transport record, the R45B re-attempt. **It contains no Group A3/B closure evidence
at all.** The only entry that touches the WP-I universe is
`03_TRANSPORT/operator_record/evidence/WPLP2-20260809T125940Z-8dc78f08-B3/b3.log`
(1784 B, `079d6ac9...`), and that log belongs to a **BURNED** RUNID whose stage
STOPped (RUNID ledger: "BURNED (STOP rc 3, B3-GAP-ENV)").

So the ledger uses `ALREADY-BANKED` in exactly one row (A3), citing where the closure
actually lives (the matrix's own re-derivation) and stating plainly that it is not in
`EVIDENCE_INDEX.md`. Prior evidence that exists *outside* that index - Gate-A A-5 to
A-9, the transition inventory - is cited as **prior capture** and does **not** get the
`ALREADY-BANKED` class, because promoting an out-of-index record to "banked" is how a
run stops re-checking something no index binds.

**Q3 - B3's banked observations are corroboration, not closure.**
M1. Three facts had to hold together: the B3 stage STOPped at rc 3; the RUNID is
burned; and `PREREGISTRATION.md` section 8 says "Any `STOP` (rc 3) ... stops the stage
and is never re-read as a PASS", which the adjudication restates. The adjudication
also records that checks #1-#3 held - so the observations exist and are bound (digest
set `b25612df...`), but the admission claim was never completed. I therefore kept B3
in the run plan (scoped) and cited `b3.log` as corroboration in the evidence column,
rather than classifying B3 `ALREADY-BANKED` and skipping it. Skipping it would have
converted a STOP into a PASS by bookkeeping.

**Q4 - B1 feasible `yes`.**
M2 + M3. M2: the release and venv roots are recorded at mode `555`, i.e. `r-x` for
other, so an unprivileged process can traverse and read the trees and execute
`<venv>/bin/python`; and matrix A6 records `verify_lock.py` as offline and read-only,
so no write permission is needed anywhere. M3: the burned B3 run walked both trees as
`gatea` - the adjudication says checks #1-#3 (release tree, venv tree, **write-bit
sweeps**) all held. A `find ... -perm /222` sweep must descend into every directory in
the tree, and RP0 is fail-closed on probe errors, so a walk that produced no
permission STOP is direct evidence that both trees are fully traversable and
stat-able by `gatea`. That is the strongest unprivileged-feasibility evidence
available anywhere in the Inputs, and it is the reason B1 is `yes` rather than
`partial`.

**Q5 - the ordering dependency I attached to B1.**
Derived, and it is the one place where I added a constraint the matrix does not have.
`--check-installed` compares the installed distribution set against the lock by
enumerating distribution metadata. A metadata directory an unprivileged process
cannot read is indistinguishable from a distribution that is not installed - so an
unreadable `.dist-info` would surface as a **missing distribution**, i.e. a FAIL
against a correct host. That is tonight's failure shape (an unreachable path read as
a finding) arriving through a different door, so I bound row 19 to row 13: the venv
walk must finish within budget, exit 0 and have an empty complete diagnostic stream
before a parity FAIL is admissible. Round 1.3 additionally forbids streaming partial
walk stdout into either the writable-path or metadata parser. If the walk STOPs, B1
STOPs and its partial stdout is not result evidence.

**Q6 - B1a `partial`.**
Two halves, opposite calls. The `sha256sum` half is M2 on the same 0555 argument as
Q4, plus M1 that the lock lives inside the release tree
(`/opt/mtc-bridge/releases/<sha>/IBKR_PAPER_BRIDGE/requirements.lock`, the matrix's
own B1a command). The manifest half is M1 straight from the adjudication - the
manifest is under `/etc/mtc-bridge`, and the matrix independently records it as
`0640 root:root`, so it is unreachable twice over (directory search denied, and the
file's own mode would deny it even if the directory did not).
Note the matrix itself marks the manifest read "(root read; the manifest is 0640
root:root)" in B1a's own command block - the privilege requirement was written down
and then the check was still listed as a read-only host step. That is the same class
of slip as B3-GAP-ENV, one line earlier in the document.

**Q7 - B2 feasible `partial` after round 1.3 F3.**
M1 + M2 + M4. The direct fragment half remains feasible: the unit fragment is
recorded at 3736 B mode `0644`, so it can be read, grepped and hashed by `gatea`.
The manager-backed half is only conditionally feasible. Read-only intent does not
prove that `systemctl` exists, that the login's PID/mount namespace can reach the
intended system manager, or that D-Bus/polkit policy authorizes the query. Those
facts are unverified (M4-12). P0 therefore requires both tool presence and an actual
parseable manager response. If that precondition cannot hold unprivileged, rows 1-5
move to DEFER-ROOT-SIDE; invocation/access/parse failure is B2_STOP, not drift.
`--no-pager` remains pinned so captured bytes cannot depend on a tty.

**Q8 - the grep repair in B2 row 6.**
Derived from the accepted three-outcome contract. The matrix's B2 command is
`grep -q '^\[Install\]' ... && echo BAD || echo OK`. `grep` returns 0 (found), 1 (not
found) and **2 (error - unreadable file, bad pattern)**. In that pipeline rc 2 lands
in the `||` branch and prints `OK`, i.e. an error is rendered as a pass. Under a
contract where rc 3 = STOP = could-not-evaluate exists precisely so errors are not
read as results, carrying that form forward would be a regression, so the draft
preregisters rc outside {0,1} as `B2_STOP reason=grep_error`.

**Q9 - B3 `partial`, and exactly where the line falls.**
M1 for the modes (release `0555 root:root`; state and log `0750
mtc-bridge:mtc-bridge`; conf `0750 root:root`; env `0600 root:root`; manifest `0640
root:root`), M2 for what each implies. The line falls between a **terminal `stat`
target** and a **path prefix**: `stat /etc/mtc-bridge` needs search on `/` and `/etc`
only, both world-searchable, and succeeds; `stat /etc/mtc-bridge/<anything>` needs
search on `/etc/mtc-bridge` itself and cannot succeed. The same argument transfers to
the state and log directories via `/var/lib` and the log parent, on the assumption
that `gatea` is not in the owning group (M4-4 below).
This distinction is why B3 is `partial` and not `no`: a meaningful amount of the
predicate - the two immutable trees, the write-bit sweeps, and the *directory-level*
modes and owners of all three metadata dirs - is reachable unprivileged. Classifying
the whole check `DEFER-ROOT-SIDE` would have thrown away verifiable ground.

**Q10 - the path-scope proof.**
Derived, and deliberately made a Stage-1 static gate rather than a run-time guard.
The B3 design gap was not that the block behaved badly at run time; it was that the
frozen bytes contained a path the execution model could never reach, and nothing
between authoring and dispatch looked for that. A run-time guard cannot fix this
(the block would have to reach the path to discover it cannot), so the check has to
happen over frozen bytes before the archive is sealed. The allowlist in draft section
10.1 is written as paths-plus-reasons rather than a bare list, so the proof is
reviewable rather than merely mechanical. `RP1-B3.sh` would have failed it.

**Q11 - B4 feasible `partial`, with a capture-shape constraint.**
M2 + M4. An explicitly selected `systemctl show -p <property>` is read-only, but it
is not proven accessible to `gatea`: the same systemctl/bus/namespace/policy M4-12
precondition as B2 applies. Rows 8-9 are INCLUDE-READ-ONLY only after P0 proves
manager readiness; otherwise all manager-backed B4 properties move to
DEFER-ROOT-SIDE. Every access or parse failure is B4_STOP before comparison.
Explicit `-p` selection, never a bare `systemctl show`, remains required because a
bare query emits the full `Environment=` list and could bank an unrelated secret.

**Q12 - B5 `partial`, and why the two gaps are STOPs not FAILs.**
M2 for the reachable half: a loopback TCP connection from a local process is not
privilege-gated, and the check runs on-host inside the ssh command, so the matrix's
"via SSH tunnel" framing is not needed and no tunnel is preregistered. The two gaps
are M4 (auth requirement unknown, `curl` presence unknown). Both are classified STOP
because neither, if it bites, tells you anything about the host's *safety* state - a
401 or a missing binary is a could-not-evaluate, and reporting either as a DISARMED
FAIL would manufacture a finding. The same logic is why the P0 preflight exists at
all: it converts two run-time surprises into a preregistered precondition.

**Q13 - B6 `partial`, and the listener-count reading.**
M2 for `ss`: `/proc/net/tcp` and `/proc/net/tcp6` are readable by any user but list
sockets only in the caller's network namespace; round 1.2 therefore requires the
caller/service namespace binding before interpretation. Only the socket-to-process
mapping (`ss -p`) requires privilege and is excluded from the argv. M1 + M2 for `ufw`: it is a root-only
administrative tool, and the matrix's B6 pairs it with A-8's `rc=0` capture, which
was a Gate-A (privileged) run, not an unprivileged one.
The reading risk is worth stating: the sources say "exactly one listener,
`127.0.0.1:8790` only", but `sshd` must also be listening or the run could not arrive.
I therefore scoped rows 22-23 to port 8790 and preregistered a full listener
inventory as captured evidence, and recorded the alternative reading (a literal
global count of one) as falsified by the transport itself. I did not silently adopt
the convenient reading.

**Q14 - the C-group calls (all `no` / BLOCKED-UPSTREAM).**
M1 throughout, and the classification is deliberate: for C1-C5 the binding constraint
is **not** privilege. Each is blocked upstream of any privilege question - by
authority and budget (matrix section 1: the exact 50-hour balance is NOT
REPRODUCIBLE, so "no host execution may be authorised or performed"), and in four of
five cases additionally by a COMMAND GAP or an unmet prerequisite:

| check | upstream blocker recorded in the matrix |
|---|---|
| C1 | authority lift + budget; **no verifier exists** for "no dangling state after SIGTERM" |
| C2 | reboot authority + budget; the predicate itself is undefined (scenario A vs B); `verify.sh` is a pre-start masked-mode verifier, not the post-reboot instrument |
| C3 | authority + budget; `wal_state_bundle.py` has exactly two subcommands, `create` and `verify` - **no `restore`**, so the restore-into-temp wrapper does not exist |
| C4 | KVM2-P4-08 + budget; stop+mask needs C3's state-manifest hash (`rollback.sh:57-58`); release-rebind's prerequisite is **unmet** (only the candidate is installed) |
| C5 | credential + network authority absent; and structurally unobtainable - `bridge/app.py:149` builds no broker in the deployed start mode, so no egress exists to capture |

Marking any of these `DEFER-ROOT-SIDE` would have been wrong: root privilege alone
would not unblock a single one of them, and the class would have implied a route that
does not exist.

**Q15 - what "one row per check" meant for split checks.**
Three checks (B1a, B3, B6) split cleanly into a feasible and an infeasible half. I
kept one row per matrix check id and let the classification cell carry both classes
with their scopes, rather than inventing sub-ids (which would fabricate check
identifiers the matrix does not define) or collapsing to one class (which would
either smuggle an unreachable probe into the run plan or discard verifiable ground).
The deviation from the four-value closed set is stated in the TSV header rather than
left for a reader to notice.

## 2. Expectation rows - how each was sourced

Every predicted value traces to a recorded observation or a source-derived constant;
none was invented to make a row look complete.

| draft section 8 row(s) | source of the expected value | class |
|---|---|---|
| 8.1 rows 1-2 (identity, groups) | `gatea` is the recorded login user of the SSH route (`PREREGISTRATION.md` section 2); "not in the `root` group" is stated by the adjudication | M1 |
| 8.1 rows 3-6 (tool presence) | none - these exist *because* the tools are unverified (M4-3 and M4-12) | M4 |
| 8.1 row 7 (system-manager readiness) | none - round 1.3 F3 adds the invocation/bus/namespace/authorization/parse precondition because read-only intent does not establish access | M4-12 |
| 8.2 rows 1-4 (active, NRestarts, Restart, MainPID) | transition inventory as carried into matrix section 0.3 and `PREREGISTRATION.md` section 8: active, `Restart=no`, `NRestarts=0`, MainPID 189813 | M1 |
| 8.2 row 5 (candidate binding) | matrix B2 proposed command (`releases/2ce41e34`, `venvs/2ce41e34`) | M1 |
| 8.2 row 6 (no `[Install]`) | matrix A4: the only `[Install]` match in the template is the explanatory comment at `:11`; matrix B2 asserts the same of the installed fragment | M1 |
| 8.2 row 7 (fragment digest, 3736 B) | transition inventory via matrix B2 - **digest elided**, size not | M1 + M4-1 |
| 8.2 row 8 (sandboxing properties) | matrix A4 needle set at `verify.sh:160-171` and the template line anchors (`KillSignal` :48, `KillMode` :49, `TimeoutStopSec` :51, `FinalKillSignal` :52, `Restart=no` :55) | M1 |
| 8.2 row 9 (start mode) | matrix section 0.6 and A4: template line 42, required needle at `verify.sh:171` | M1 |
| 8.2 rows 10-11 (0555 roots) | transition inventory (release root mode 555, venv counterpart 555) | M1 |
| 8.2 row 12 (120 s budget) | budget and its rationale carried unchanged from `PREREGISTRATION.md` section 2 | M1 |
| 8.2 row 13 (walk completeness) | derived STOP-first precondition for rows 14 and 19; round 1.3 requires atomic stdout/stderr/rc/elapsed capture and complete diagnostics adjudicated before stdout | derived (Codex F4) |
| 8.2 row 14 (write bits) | matrix B3 predicate, admissible only from a proven complete rc-0 diagnostic-free walk | M1 + derived ordering |
| 8.2 row 15 (metadata dir modes) | matrix B3 predicate: conf `0750 root:root`, state+log `0750 mtc-bridge:mtc-bridge`; adjudication independently confirms `/etc/mtc-bridge` `root:root` `750` | M1 |
| 8.2 row 17 (lock digest, 117762 B) | matrix A3/B1a rounds 2-3: `a1881296...bf66e`, LF, 117762 B, source-derived | M1 |
| 8.2 row 18 (Python 3.12) | matrix B1 predicate; patch version unrecorded, so the predicate is a `3.12.` prefix | M1 |
| 8.2 row 19 (`packages=56`) | matrix A6: the PASS line prints the count actually parsed (`verify_lock.py:97`), not a constant - which is why the number is evidence rather than an echo | M1 (round 1.2: +metadata-readability precondition, Codex F1) |
| 8.2 rows 20-21 (status flags) | matrix B5 and section 0.6 (`app.py:138-147`): `mode`, `network`, `exchange_conn`, `exchange_enabled`, `credential_lookup`, `arm_enabled`; `state_version=1` from matrix section 0.3 | M1 for the values, M4-2 for the key names |
| 8.2 rows 22-23 (listener set) | matrix section 0.3 and B6; A-8 capture | M1 + M4-5 on the reading (round 1.2: +namespace-binding precondition, Codex F2; new M4-11) |
| 8.2 row 24 (external closed) | A-8 `port8790_ok=False` | M1 |

Divergence strings follow the accepted grammar rather than a new one: `<CHECK>_FAIL
reason=<token> <k>=<v>` and `<CHECK>_STOP reason=<token> ...`, matching the observed
`B3_FAIL` / `B3_STOP` / `R45_FAIL` / `RP0_STOP reason=path_probe_error path=... rc=...
detail=...` forms. Reusing the grammar matters because the first-FAIL adjudication
path already knows how to read it.

## 3. Constraint compliance

| kickoff constraint | how this draft satisfies it | where to check |
|---|---|---|
| 1 - unprivileged feasibility is a design gate | Section 0 states it before expectations, argv or evidence contract; every admitted check carries its `gatea`-without-sudo reason in the TSV; the mechanical enforcement is the Stage-1 path-scope proof; privileged items route to RPD-VERIFY | draft section 0, 10; TSV `unpriv_why` |
| 2 - Group C: nothing executable | C1-C5 appear only in draft section 9 with their blocking dependency; no command, argv, block, op-table row or conditional branch references any of them | draft section 9; op table section 5 has 12 rows, none mutating |
| 3 - no concrete RUNID, unit id or colliding record root | Every identifier is `<ALLOCATE-AT-DISPATCH>`; section 1 adds a non-collision rule against the two recorded Stage 2/3B roots and against `/home/gatea/` | draft sections 1, 6, 12 |
| 4 - do not weaken the Stage 2 conventions | create-once (sections 1, 6), first-FAIL with `always` ops still running (section 5), three-outcome rc (section 8), evidence closed by a separate invocation with a double-pass digest (section 7), remote-vs-local binding as ops 11-12 (sections 5, 7) | draft sections 1, 5, 6, 7, 8 |
| 5 - no file outside this directory, no host contact | Three files written, all in `WPI_PREREG_DRAFT_ROUND1`; five files read, all from the Inputs list; zero commands run against any host | section 5 below |

Two places where the draft is *stricter* than Stage 2, both traceable to tonight:
a wider-than-expected capability set is a STOP rather than an opportunity (section
8.1 row 2, and section 11's P0 immutability rule), and `RP1-B3.sh` is excluded from
the archive entirely rather than carried-but-not-executed.

## 4. Residual unverified premises (M4) and their fail-closed handling

Listed so a reviewer can attack them directly rather than reconstruct them.

1. **Unit fragment SHA-256 is elided** in matrix B2 as `538c1c60...279bd`. The full
   64-hex value is not in the Inputs, and I did not read the transition inventory
   (not an Input). Handling: `<PIN-BEFORE-DISPATCH: ...>` in draft section 2, risk R1,
   and section 11 makes an unfilled pin a dispatch blocker. **I did not guess it.**
2. **The `/api/status` response schema and auth requirement are unobserved.** The
   field names in row 21 come from matrix prose and from `app.py:138-147` as quoted,
   not from a captured body. Handling: risk R4; a missing or differently-spelled key
   is `B5_STOP reason=schema_unexpected`, a non-200 is `B5_STOP`, never a FAIL.
3. **`curl`, `ss`, `sha256sum` and `systemctl` presence on the host is unobserved.** Handling: P0
   preflight rows 3-6, STOP with **no substitution** - preregistering a fallback that
   was never reviewed is how improvisation gets in.
4. **`gatea`'s supplementary group list is unobserved.** The adjudication establishes
   only that `gatea` is not in `root`. Whether it is in the state/log group is
   unknown, and the DEFER-ROOT-SIDE calls for the state and log directory *contents*
   assume it is not. Handling: P0 row 2 captures the real group list, and a *wider*
   capability set STOPs the run for re-adjudication rather than quietly enabling more
   probes.
5. **The literal log directory path is not in the Inputs** - the matrix records its
   mode (`0750 mtc-bridge:mtc-bridge`) but names only `ReadWritePaths=<state> <log>`.
   Handling: `<PIN-BEFORE-DISPATCH: ...>`, risk R2, and an explicit note that deriving
   it at run time from the same `systemctl show` output the run asserts against would
   make row 15 circular. **I did not invent `/var/log/mtc-bridge`.**
6. **"Exactly one listener" is ambiguous** between a global count and a bridge-port
   count. Handling: risk R5, rows scoped to 8790, full inventory captured, and the
   alternative reading recorded as falsified by the transport rather than dismissed.
7. **`b3.log` was not read** - it is not in the Inputs. Every empirical claim about
   what the burned B3 run proved is second-hand from `B3_STOP_ADJUDICATION.md`
   (class M3). If that summary overstates what checks #1-#3 covered, Q4's
   empirical support weakens to M2 alone - which would still support `yes` for B1,
   but on derivation rather than demonstration.
8. **Whether `verify_lock.py --check-installed` needs any writable location** is
   assumed no, on matrix A6's "offline, network-free" characterisation. Handling: any
   write failure surfaces as a non-zero rc and is adjudicated as `B1_STOP`, not as a
   parity FAIL.
9. **Per-file modes inside the release and venv trees are not individually recorded**
   - only the roots (`555`). This does not weaken row 12, whose predicate is exactly
   "no write bit anywhere", i.e. the sweep measures it rather than assuming it.
10. **The env-file naming question** (`bridge.env` vs `mtc-bridge.env`) is
    **unresolved, not triggered**, and this draft does not adjudicate it - permission
    denial precedes the existence question for any unprivileged operator. It is
    listed in draft section 9 under RPD-VERIFY, exactly as the adjudication leaves it.
11. **Whether `gatea` can `readlink /proc/<MainPID>/ns/net`** for the root-owned
    service process is unverified (ptrace/yama gating on a root-owned PID typically
    returns EACCES to an unprivileged reader). Handling: rows 22-23 preregister the
    namespace-binding precondition (Codex F2); an EACCES is
    `B6_STOP reason=service_netns_unreadable` and routes the listener-set half to
    RPD-VERIFY. The caller's own identity (`/proc/self/ns/net`) is always readable, so
    the precondition is fail-closed, not silently skipped.
12. **Whether `gatea` can reach and query the intended system manager is unverified.**
    Tool presence, system-bus availability, PID/mount-namespace identity and
    D-Bus/polkit authorization are not established by the Inputs. Handling: P0 rows
    6-7 must prove tool presence and a parseable manager response. Failure is
    `P0_STOP reason=system_manager_unreachable`; manager-backed B2/B4 rows then route
    to RPD-VERIFY and cannot become unit-state or property FAILs.

## 5. What this unit did and did not do

Files read - the five in the kickoff's Inputs section, nothing else:

- `KICKOFF_WPI_PREREG.md`
- `../GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md` (sections 0-2, Groups
  A, B, C, and Group D/E/G headings encountered in the same pages)
- `../WPL_P2_STAGING_.../02_PREREG/PREREGISTRATION.md`
- `../WPL_P2_STAGING_.../03_TRANSPORT/B3_STOP_ADJUDICATION.md`
- `../WPL_P2_STAGING_.../EVIDENCE_INDEX.md`

Files written - three, all in this directory:

- `WPI_PREREGISTRATION_DRAFT.md`
- `WPI_CHECK_FEASIBILITY.tsv`
- `SELF_QA.md`

Not done: no SSH, SCP, ssh-keyscan, ping, TCP connect or any other contact with
`GATEA-STAGING` or any host; no `sudo`; no Gate-A script; no systemctl, curl, ss,
stat, find or sha256sum against a target; no test execution; no package, install or
network command; no credential read; no Git command of any kind - no `add`, `commit`,
`push`, `checkout`, branch or worktree action; no file created, modified or deleted
outside this directory; no RUNID or unit id minted; no record root created; no run
kit built or archive frozen.

The untracked working-tree files noted in the session's starting git status were not
touched.

---

## Round 1.1 addendum (Lead integration of GLM review, 2026-08-09 night)

GLM F1 correction to M4-9's scope: the "per-file modes inside the trees are
unrecorded" premise limits not only the write-bit sweep (row 12) but also
**interpreter execution** (rows 18/19) - nothing recorded proves
`<venv>/bin/python` carries the "other" execute bit. The draft now routes an exec
denial to `B1_STOP reason=interpreter_not_executable` (row 18 preflight `test -x`),
so a non-executable interpreter can never be misread as a version or parity FAIL.
Also applied: N1 reused-script disposition note (draft section 4), N2 listener
wording (draft section 8 intro). Review report:
`11_TRIAGE/WPI_DRAFT_GLM_REVIEW_2026-08-09.md`. B1 remains INCLUDE-READ-ONLY.

---

## Round 1.2 addendum (Codex audit REQUEST_CHANGES applied, 2026-08-09)

The binding audit (`WPI_DRAFT_CODEX_AUDIT_2026-08-09.md`) returned REQUEST_CHANGES.
This round applies the four findings in this round's scope contract - F1, F2, F5, F6 -
and leaves F3 and F4 (system-manager access, both HIGH in the audit) for a successor
round; they are noted as OPEN below, not silently dropped. All four applied findings
are one defect class: an inability-to-evaluate must STOP (rc 3), never FAIL (rc 1).

**F1 - B1 metadata readability (HIGH).** The then-row-14 `find` guard (renumbered
row 13 in round 1.3) proves traversal and
stat-ability, not regular-file readability, so an unreadable `*.dist-info/METADATA`
(mode 000, a denying ACL, or an LSM rule) could reach the parity check and be reported
as package drift. Applied: row 19 now carries an explicit preflight readability
precondition over every metadata object the verifier consumes (every `*.dist-info`
directory and its `METADATA`/`RECORD`), and a fixed adjudication rule - a generic
nonzero verifier rc never becomes `B1_FAIL reason=lock_installed_parity`; only a
positively-distinguished installed-set mismatch may, and every open/parse/permission/
LSM/traversal error or indistinguishable verifier error is `B1_STOP`. B1 stays
INCLUDE-READ-ONLY (readability of 0555-tree metadata is itself unprivileged); no class
change. The TSV B1 disposition records the rule. Additionally, then-row 14's inline
cross-reference ("this STOP disqualifies row 18") was a stale round-1.1 artifact -
parity was row 18 before the interpreter row was inserted, shifting it to row 19 - so
it contradicted that round's binding ordering rule (then-row 14, now row 13, gates
row 19, not the interpreter at
row 18). Corrected to "row 19 (parity)" so the table matches its own ordering rule,
which F1 makes central. No predicate changed; a cross-reference only.

**F2 - B6 network-namespace binding (HIGH).** `ss -ltn` observes the caller's netns,
not the service's, so a login in a private netns could yield a false B6_FAIL or a
false PASS. Applied: rows 22-23 now require the namespace binding proven
(`readlink /proc/self/ns/net` == `readlink /proc/<MainPID>/ns/net`); a mismatch is
`B6_STOP reason=netns_mismatch`, an unreadable service netns identity is
`B6_STOP reason=service_netns_unreadable`. **Class change:** B6's listener-set half
moves from unconditionally INCLUDE-READ-ONLY to INCLUDE-READ-ONLY *conditional on the
netns binding being establishable unprivileged* / DEFER-ROOT-SIDE *(the netns binding
itself if the service netns identity is unreadable by `gatea`)*. The TSV B6 row is
updated, including correcting the prior claim that `ss` lists sockets system-wide - it
lists the caller's netns. The operator-side external probe (row 24) is unchanged as
independent corroboration.

**F5 - hash could-not-read divergence (MEDIUM).** Rows 7 (B2 fragment) and 17 (B1a
installed lock) named only digest-mismatch FAILs. Applied: each now carries an
explicit hash-error STOP (`fragment_unreadable`, `installed_lock_unreadable`) for any
`sha256sum` open/read/permission/LSM/parent-traversal error, and a digest mismatch is
admissible only after rc 0 plus a syntactically valid 64-hex digest and the byte
count - never compared against possibly empty output. No class change (hash-unreadable
is a runtime could-not-evaluate, not a privilege need); TSV B2/B1a dispositions note
the STOP forms.

**F6 - dispatch authority discipline (MEDIUM).** The three pre-dispatch items (freeze
blocks, fill pins, allocate/test identifiers) read as an exhaustive gate despite the
document's own authority/budget blocker. Applied: the three items are now stated
**necessary but not sufficient**, with two added gates - explicit written
host-contact/transport authority and the required budget lift - and `-Execute`/
`-Confirm` are stated as technical interlocks on the runner, not authority. No class
change; TSV unaffected.

**New residual premise (M4-11).** Whether `gatea` can `readlink /proc/<MainPID>/ns/net`
for the root-owned service process is unverified (ptrace/yama gating); handled
fail-closed - EACCES is `B6_STOP` and routes the listener-set half to RPD-VERIFY.

**F3 / F4 remained OPEN in round 1.2 (out of scope for that round).** The audit's F3 (B2/B4
system-manager access failure misread as host drift) and F4 (B3 partial-`find` output
inspected before adjudicating walk failure) were HIGH but were not in that round's
contract. Round 1.2 recorded them for a successor rather than silently dropping
them. The round-1.3 section below supersedes this historical open-items statement.

**Constraint compliance this round.** Still a DRAFT: no concrete one-use RUNID, unit
id, or collision-prone record root minted - the `<ALLOCATE-AT-DISPATCH>` /
`<PIN-BEFORE-DISPATCH>` discipline is intact. No check was weakened: every edit adds a
precondition or a STOP form; no existing FAIL, STOP, caveat, or named risk was removed.
No mutating check was preregistered (readability, readlink and sha256sum probes are
read-only). The one factual correction (TSV B6 `ss` scope) replaces a claim the audit
proved false; no truthful caveat was deleted.

**What this round read and wrote.** Read: `WPI_DRAFT_CODEX_AUDIT_2026-08-09.md` (the
binding audit) and the three deliverables, plus `AGENTS.md` and `START_HERE.md` per
repo mandate. No other file was read; no host contact; no Git action. Written: the
same three deliverables, in place. The round-1.1 GLM-review addendum above stands
unchanged.

---

## Round 1.3 addendum (Codex audit F3 and F4 closed, 2026-08-10)

This documentation-only repair closes the two findings round 1.2 explicitly left
open. The shared rule is binding throughout the draft: inability to evaluate is STOP
(rc 3); only a probe that ran to a complete, parseable result may observe deviant
state and FAIL (rc 1). The round-1.2 open-items list is superseded. **F3 and F4 are
now closed.**

**F3 - B2/B4 system-manager access (HIGH), closed.** The draft now adds `systemctl`
presence and actual system-manager query readiness to P0. Readiness covers process
invocation, the system bus, the login's PID/mount namespace, D-Bus/polkit
authorization and parseable complete output; tool presence alone is insufficient.
Every affected expectation row now has a dedicated STOP before its FAIL comparison:
B2 rows 1-5 use `system_manager_unreachable`, `unit_property_unreadable` or
`unit_definition_unreadable`; B4 rows 8-9 use `unit_property_unreadable`. The binding
adjudication order captures stdout/stderr/rc/elapsed, resolves access and parse errors
first, and compares output only afterward. A valid `inactive` state remains an
evaluable B2 FAIL even if `systemctl is-active` uses a nonzero result rc; an absent or
error result STOPs. The general STOP list now names `systemctl` and the system bus.
Feasibility changed: B2 and B4 are `partial`, with manager-backed predicates
INCLUDE-READ-ONLY only after P0 readiness and DEFER-ROOT-SIDE if that precondition
cannot be established as `gatea`; B2's direct fragment read/grep/hash half remains
unprivileged. The TSV and RPD-VERIFY list record the split and reason.

**F4 - B3 partial `find` output (HIGH), closed.** Each filesystem walk is now atomic
for adjudication: stdout, stderr, rc and elapsed time are captured without streaming
stdout to a result parser. The binding order is timeout/budget first, then exit status
and the complete diagnostic stream, then stdout. Any LSM, ACL, mount, permission or
traversal error, or any nonzero rc, produces STOP. Rows were reordered so budget and
walk completeness (rows 12-13) precede writable-path interpretation (row 14), and
row 14 explicitly admits FAIL only from a complete rc-0 diagnostic-free sweep. Thus
a writable pathname emitted before a later EACCES remains partial output and cannot
accuse a correct host. The rule is generalized to metadata enumeration and every
other command whose stdout the draft interprets. Stage-1 frozen-block acceptance now
requires an adversarial transcript demonstrating partial pathname output followed by
an access/traversal error yields `B3_STOP`, never `B3_FAIL`.

**Earlier-round protections preserved.** No concrete RUNID, unit id or record root
was minted; all `<ALLOCATE-AT-DISPATCH>` and `<PIN-BEFORE-DISPATCH>` placeholders
remain. No mutating check was added. The round-1.2 requirement for explicit written
host-contact/transport authority and the budget lift remains necessary before any
successor is dispatchable.

**What round 1.3 read and wrote.** Read only `KICKOFF_ROUND13_F3F4.md`,
`../WPI_DRAFT_CODEX_AUDIT_2026-08-09.md` and the three deliverables. Wrote only the
three deliverables in place. No host contact, command against a host, Git action,
RUNID allocation, unit-id allocation, record-root creation or file outside the three
deliverables was performed.
