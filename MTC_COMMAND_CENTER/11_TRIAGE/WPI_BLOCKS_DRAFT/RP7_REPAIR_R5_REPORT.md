# RP7-WPI-RO repair round 5 - report

Implementer: Claude Opus 5, effort xhigh, under owner grant #7 (T0 round cap lifted for
this block set until both flagships accept). Codex is the auditor of record for findings
1-3 and re-audits these bytes, so implementer/auditor separation holds. No host contact,
no network, no SSH/SCP, no RUNID, no commit, no deployment.

## Subject identity

| | bytes | SHA-256 | CR bytes | `bash -n` |
|---|---:|---|---:|---|
| round-4 input (commit `d6a976aa`) | 70941 | `23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad` | 0 | 0 |
| round-5 output | 77179 | `393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee` | 0 | 0 |

Byte count re-derived with `wc -c`; CR count with `tr -cd '\r' < file | wc -c` (never
`grep -c $'\r'`). Both values are also re-derived from inside both published fences.

The whole executable delta is `+93/-7` lines, of which the non-comment part is exactly the
five repairs below and nothing else. No other production line changed.

## Finding disposition

Every finding is listed with its disposition. Nothing is deferred and nothing is silently
dropped.

| # | Source | Severity | Disposition | Evidence |
|---|---|---|---|---|
| F1 | Codex R4 finding 1 | BLOCK | **REPAIRED** | round-5 fence, F1 arm: RED `rp7_pass=1` / GREEN `rp7_pass=0` |
| F2 | Codex R4 finding 2 | HIGH | **REPAIRED** | round-5 fence, four F2 arms incl. a clean no-regression PASS |
| F3 | Codex R4 finding 3 | MEDIUM | **REPAIRED** | published anchored command, executed; extracted-body digests recorded |
| F4 | §10.1 reconciliation, Lead-verified | LOW | **REPAIRED** | static 3→0 plus an executed PATH-shadow RED/GREEN |
| F5 | §10.1 reconciliation, Lead-verified | MEDIUM | **REPAIRED, with a named freeze-gate input Stage 1 must close** | round-5 fence, five F5 arms |

### F1 - `python3` was never bound in the production main path (BLOCK)

**What was wrong.** The tenth pin was accepted at `:594-614`, included in projection v2 at
`:443-456`, and its required binding was defined at `:546-562` - but the only production
binding loop in `wpi_main` listed nine tools. The unbound executable then ran at both
adjudicators while the block printed `adjudicator=pinned_system_interpreter` and
`parser=pinned_system_interpreter isolation=isolated_no_site`.

**Repair.** `python3` was added to the single production binding loop in `wpi_main`, which
sits between `wpi_mount_guard_begin` and `wpi_mount_guard_end`, so the binding happens
inside the initial mount window and before it closes. `-I -S` and the startup guards are
untouched, per the kickoff: they only became load-bearing once the program interpreting
them is the bound one. No new binding path was invented - the tenth pin now goes through
the same `wpi_map_get` + `wpi_bind_tool` pair as the other nine, and therefore inherits the
non-symlink, `0:0`, not-group/other-writable, component-and-mount discipline and emits its
own `RP7_tool name=python3 ... attestation=bound_instrument` line.

**Evidence (D026, real caller).** One harness, two byte sets. `wpi_bind_tool` is replaced
by a recorder that STOPs if and only if production asks it to bind `python3`, and the mount
guard is replaced by markers so the *order* is read out of the production body rather than
asserted. Nothing redeclares the tool list - the arm fails if `wpi_main` stops calling the
binding.

```text
RED   MAIN_BIND rc=0 bound=[stat,readlink,env,find,sha256sum,systemctl,ss,curl,timeout,] python3_bound=no  malicious_marker=present accepted_status=1 rp7_pass=1 window_open=1 window_closed=1 binding_stop=0
GREEN MAIN_BIND rc=3 bound=[stat,readlink,env,find,sha256sum,systemctl,ss,curl,timeout,python3,] python3_bound=yes malicious_marker=absent  accepted_status=0 rp7_pass=0 window_open=1 window_closed=0 binding_stop=1
```

The RED line reproduces Codex's transcript exactly. The GREEN line satisfies the kickoff's
requirement that the repaired run STOP *before either adjudicator runs*: no marker was
written, no `B5_status ... parser=pinned_system_interpreter` line exists, no `RP7 PASS`
exists, and `window_closed=0` proves the STOP happened with the initial window still open.

### F2 - a malformed admitted `*.dist-info` object was silently dropped (HIGH)

**What was wrong.** `:797-859` proved object kind, ownership and byte readability; the
trusted driver built a `PathDistribution` for every admitted directory without requiring a
valid `Name`/`Version` or a unique canonical name; and
`IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:68-74` skips every object whose `METADATA`
lacks `Name` and overwrites duplicate canonical names in a dict. Row 19 could therefore
print the accepting parity line for a universe it never adjudicated.

**Repair.** The byte-frozen `verify_lock.py` was **not** modified. The adjudication is in
the block's own trusted driver, placed after the universe scan and **before** any
`PathDistribution` is constructed or the verifier source is compiled. For every admitted
object the driver requires exactly one grammar-valid `Name`, exactly one `Version`, and a
canonical name (`re.sub("[-_.]+","-",name).lower()`, the verifier's own canonicalisation)
unique across the admitted set. Any failure is `die(6, ...)`, which the block classifies -
under the same field-by-field grammar already used for the rc-5 universe token - as

```text
B1_STOP reason=metadata_identity_unestablished stage=verifier detail=<t> name_sha256=<h>
```

with `<t>` from the fixed set `metadata_unreadable`, `name_absent`, `name_ambiguous`,
`name_grammar`, `version_absent`, `version_ambiguous`, `version_grammar`,
`canonical_name_duplicate`, and the entry name content-suppressed to a digest exactly as
the existing universe token does. This is a STOP - an inability to evaluate - never a
silent omission and never a `lock_installed_parity` FAIL, per the kickoff.

**Evidence (D026, real caller).** Four cases, each run against both byte sets through the
production row-19 preflight, the production trusted driver and the real digest-bound
`verify_lock.py`:

```text
RED   META_IDENTITY case=clean          rc_preflight=0 rc_parity=0 dist_info_dirs=1 accepted_parity=1 parity_fail=0 identity_stop=0
GREEN META_IDENTITY case=clean          rc_preflight=0 rc_parity=0 dist_info_dirs=1 accepted_parity=1 parity_fail=0 identity_stop=0
RED   META_IDENTITY case=name_absent    rc_preflight=0 rc_parity=0 dist_info_dirs=2 accepted_parity=1 parity_fail=0 identity_stop=0
GREEN META_IDENTITY case=name_absent    rc_preflight=0 rc_parity=3 dist_info_dirs=2 accepted_parity=0 parity_fail=0 identity_stop=1
RED   META_IDENTITY case=version_absent rc_preflight=0 rc_parity=1 dist_info_dirs=2 accepted_parity=0 parity_fail=1 identity_stop=0
GREEN META_IDENTITY case=version_absent rc_preflight=0 rc_parity=3 dist_info_dirs=2 accepted_parity=0 parity_fail=0 identity_stop=1
RED   META_IDENTITY case=duplicate      rc_preflight=0 rc_parity=0 dist_info_dirs=2 accepted_parity=1 parity_fail=0 identity_stop=0
GREEN META_IDENTITY case=duplicate      rc_preflight=0 rc_parity=3 dist_info_dirs=2 accepted_parity=0 parity_fail=0 identity_stop=1
```

Three points worth naming:

- `case=name_absent` RED reproduces Codex's fixture: two admitted directories, one with no
  `Name`, accepting parity line printed.
- `case=duplicate` is a second, independent false PASS Codex named but did not execute: two
  directories whose `Name` values (`demo-pkg` and `Demo_Pkg`) canonicalise to one key, so
  the verifier's dict collapses them and reports `packages=1` for two distributions.
- `case=version_absent` RED is the *other* dishonesty in the same defect: a distribution
  whose version cannot be established surfaced as
  `B1_FAIL reason=lock_installed_parity` - a host-state finding about an object that was
  never evaluable, which is catalogue pattern 1. The repaired bytes STOP.

The `clean` case PASSes on both byte sets, which is the required no-regression arm. Each
GREEN `name_sha256` is asserted equal to a digest the fixture re-derives from the offending
directory's own name.

**Disclosed limits of this repair.**

1. The adjudication is driver-side only. The bash preflight still proves kind, ownership
   and readability, not identity: RFC-822 header parsing in shell would be a worse
   instrument than the one already running under `-I -S`. Both sides still share one
   discovery universe; only the semantic layer is single-sided, and it runs before any
   verifier result can exist.
2. `Version` is validated as `[0-9][0-9A-Za-z.!+_-]*` (full match). That admits every
   normalised PEP 440 version, including epochs and local labels, and rejects empty,
   whitespace-bearing and control-bearing values. It would reject a non-normalised
   `v`-prefixed version. The choice is deliberate: a stricter PEP 440 grammar buys nothing
   here - the verifier only string-compares the value - while adding false-STOP risk on a
   healthy 56-package venv, and a STOP on a healthy host is itself a defect.
3. `email` parse defects are not inspected. A malformed header block simply yields no
   `Name` or no `Version` and reaches the same STOP, so the check does not depend on defect
   classification.

### F3 - the published "Exact command" was a literal placeholder (MEDIUM)

**What was wrong.** `SELF_QA_RP7.md:26-37` published `bash <fence-file>`, which is a shell
syntax error at rc 2 - reproduced this round.

**Repair.** Both fences are delimited by unique content markers that are bash comments, so
the extracted body is executable as-is with no post-processing:

```bash
cd /c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
sed -n '/^# RP7_QA_FENCE_BEGIN$/,/^# RP7_QA_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r5-fence-body.sh
sed -n '/^# RP7_R4_FENCE_BEGIN$/,/^# RP7_R4_FENCE_END$/p' SELF_QA_RP7.md > /tmp/rp7-r4-fence-body.sh
sha256sum /tmp/rp7-r5-fence-body.sh /tmp/rp7-r4-fence-body.sh
wc -c /tmp/rp7-r5-fence-body.sh /tmp/rp7-r4-fence-body.sh
bash --noprofile --norc /tmp/rp7-r5-fence-body.sh; printf 'R5_FENCE_RC=%s\n' "$?"
bash --noprofile --norc /tmp/rp7-r4-fence-body.sh; printf 'R4_FENCE_RC=%s\n' "$?"
```

The command block is itself anchored (`# RP7_EXACT_COMMAND_BEGIN`/`END`) and was executed
by extracting it from the committed document and piping it to a fresh
`bash --noprofile --norc`. The standing rule holds by construction: a marker only matches
at the start of a line, and every line of the command starts with something else, so the
command's own text cannot re-open either range. No line numbers anywhere.

**Recorded results.**

```text
0263067e4bb41d8c4c6bbfd96bd35b8a83cc48d1eedc14c1acdc886ee7a5b62f */tmp/rp7-r5-fence-body.sh
94101ef7fdf70d0f4628685811160389227cbba3c10e999e1942e8eb82bb56e0 */tmp/rp7-r4-fence-body.sh
20050 /tmp/rp7-r5-fence-body.sh
76710 /tmp/rp7-r4-fence-body.sh
R5_FENCE_RC=0
R4_FENCE_RC=0
```

Both fences ended `QA_PASS all_assertions=yes`, stderr empty. The command was then re-run
verbatim against the document as committed: identical digests, identical rc, and a diff
confined to the `mktemp` scratch names plus the three measured wall-clock fields of the
budget arm (`elapsed_ms=8070`/`8060`, `2040`/`2200`, `production_wall_s=2`/`3`).

### F4 - the `/dev/null` write opens (LOW)

**What was wrong.** Three write opens outside the §10.1 allowlist: `:183`
(`2>/dev/null` on the `noclobber` probe) and `:624-625` (`command -v ... >/dev/null 2>&1`).

**Repair.** Exactly as the kickoff directed:

- both prerequisite probes became
  `[ "$(builtin type -t <name>)" = function ] || wpi_stop ...`. With `-t`, an undefined
  name prints nothing on either stream and returns 1, so no redirection is needed at all;
  `builtin` bypasses any function named `type`; and the check is strictly narrower than
  `command -v`, which an executable of the predicate's name on `PATH` would have satisfied.
- the `noclobber` probe closes fd 2 (`2>&-`) instead of redirecting it. The `noclobber`
  semantics of `:183` are unchanged - it is still a subshell `set -o noclobber; : > "$leaf"`
  whose failure is the create-once verdict.

**Evidence.** Static and executed.

```text
DEVNULL_STATIC red_non_comment=3 green_non_comment=0
RED   PREREQ_PATH_SHADOW rc=0 stdout=[] stderr_bytes=0
GREEN PREREQ_PATH_SHADOW rc=3 stdout=[RP7_STOP reason=rp0_lib_not_sourced predicate=rp0_require_safe_component] stderr_bytes=0
GREEN ALLOC_LEAF rc_first=0 rc_second=3 rc_outside=3 err1=0 err2=0 err3=0
        second_stdout=[RP7_STOP reason=capture_leaf_not_create_once leaf=...]
        outside_stdout=[RP7_STOP reason=capture_path_outside_evidence leaf=... ev_dir=...]
```

The three remaining `/dev/null` strings in the block are all inside comments. The PATH-shadow
arm is a genuine RED/GREEN: an executable named `rp0_require_safe_component` on `PATH`
satisfied the round-4 check and is refused by the round-5 one. Every `stderr_bytes=0` /
`err*=0` field is the proof that closing fd 2 discards the `noclobber` diagnostic without
opening anything.

### F5 - evidence-root provenance (MEDIUM)

**What was wrong.** `:631` proved `EV_LOG` below `EV_DIR` and `:182` proved every leaf
below `EV_DIR`, but nothing proved `EV_DIR` itself. Both containments are relative, so the
entire create-once chain hung from a root supplied by the same channel it was meant to
bound.

**Repair.** A new frozen constant `WPI_FIXED_EVIDENCE_ROOT` (value `<REMOTE_BASE>/evidence`)
and, in `wpi_assert_prerequisites` - the first predicate `wpi_main` runs, before any leaf
can be allocated - a STOP unless `EV_DIR` is absolute, canonical and a **strict descendant**
of that constant:

```text
RP7_STOP reason=evidence_root_unattested detail=freeze_gate_pin_unfilled name=WPI_FIXED_EVIDENCE_ROOT
RP7_STOP reason=evidence_root_unattested ev_dir=<d> expected_root=<r>
```

No new environment input was introduced, so no wrapper edit is required and no value the
run learns about itself can satisfy the check. `EV_PARENT`/`EV_RUNKIT` were deliberately
**not** used for this: they arrive on the same channel as `EV_DIR` and would have been
circular. The claim was narrowed to what is established: the file header now says mutation
is confined to create-once leaves inside `EV_DIR`, that `EV_DIR` is proven a strict
descendant of the frozen evidence root before any leaf is allocated, and that no path
outside that tree is opened for writing. `RP7_evidence_bound` gained
`evidence_root=<r> root_binding=frozen_prefix_descent`.

**Evidence.**

```text
EV_ROOT_CONSTANT red=0 green=1
RED   EV_ROOT pin=[keep]      ev_dir=[<Q>/other/x]                    rc=0 stdout=[]
GREEN EV_ROOT pin=[keep]      ev_dir=[<Q>/other/x]                    rc=3 stdout=[RP7_STOP reason=evidence_root_unattested detail=freeze_gate_pin_unfilled name=WPI_FIXED_EVIDENCE_ROOT]
GREEN EV_ROOT pin=[<Q>/base]  ev_dir=[<Q>/base/evidence/runkit/RUN-RO] rc=0 stdout=[]
GREEN EV_ROOT pin=[<Q>/base]  ev_dir=[<Q>/other/x]                    rc=3 stdout=[RP7_STOP reason=evidence_root_unattested ev_dir=<Q>/other/x expected_root=<Q>/base]
GREEN EV_ROOT pin=[<Q>/base]  ev_dir=[<Q>/base-evil/x]                rc=3 stdout=[RP7_STOP reason=evidence_root_unattested ev_dir=<Q>/base-evil/x expected_root=<Q>/base]
```

The last arm is the prefix-boundary falsification: `<Q>/base-evil` is not admitted by a
`<Q>/base` root. The filled-pin arms simulate freeze by assigning the constant in the
sourced scope; that substitution is disclosed in the QA and is the only way to exercise the
accepting arm before the pin exists.

## Freeze-gate inputs

Three, and item 3 is new this round and carries an ordering constraint.

1. `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` - the `normalised_path_projection_v2`
   digest over 21 point paths and 6 roots, from the deploy channel. Unchanged.
2. `WPI_FIXED_TRUSTED_PYTHON` - the resolved non-symlink `/usr/bin/python3.<minor>`.
   Unchanged in nature; as of this round the refusal of an unresolved (symlinked) pin is
   reachable from the production path rather than only from a helper.
3. **`WPI_FIXED_EVIDENCE_ROOT` (new)** - `<REMOTE_BASE>/evidence`. `REMOTE_BASE` is
   `<ALLOCATE-AT-DISPATCH>` in `run_ro.sh:9` and section 1 of the preregistration, so
   **Stage 1 must allocate `REMOTE_BASE` before it freezes and hashes the RO block**; a
   block frozen first cannot carry a base allocated later. If that ordering cannot be met,
   the honest resolution is to record that the RO block does not claim evidence-root
   provenance for this run - not to fill the pin from anything the run learns about itself.
   This is the "record the missing binding as a named freeze-gate input" branch the kickoff
   required, taken deliberately and in addition to the implemented check, not instead of it.

## Preregistration draft edits (complete list)

All five are in `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`. That file already
carried uncommitted Lead edits from the §10.1 reconciliation when this round started
(`+24/-17` against `HEAD`); those were not touched, and the five edits below sit on top of
them, taking the working-tree diff to `+57/-18`.

1. **§1, allocation rules** - new bullet: the RO block binds its own evidence root against
   a frozen `WPI_FIXED_EVIDENCE_ROOT`, the two STOP forms, and the freeze-before-allocation
   ordering constraint Stage 1 must close. (F5)
2. **§8.2 row 19, check column** - the trusted driver semantically establishes each
   admitted object's package identity before parity: exactly one grammar-valid `Name` and
   `Version`, unique canonical names. (F2)
3. **§8.2 row 19, divergence column** - adds
   `B1_STOP reason=metadata_identity_unestablished stage=verifier detail=<t> name_sha256=<h>`
   with its fixed eight-token `<t>` set, and states why an unadjudicated identity is neither
   a silent omission nor a parity FAIL. (F2)
4. **§8.2 instrument-attestation paragraph** - `attestation=bound_instrument` is truthful
   only if the tool was bound; all ten pins pass through the production loop inside the
   initial mount window, and no accepting `pinned_system_interpreter` token in rows 19 or 21
   is admissible without this tool's own `RP7_tool` line. (F1)
5. **§10.1, after the allowlist table** - the list is exhaustive for write opens too;
   `/dev/null` is deliberately absent, and the three RO-block write opens of it were
   removed. (F4)

No other section was touched. Section 4 needed no edit: it already required the trusted
interpreter - the block, not the draft, was non-conformant.

## What this round does not close

- No accepting `wpi_validate_inputs` arm exists and none can before freeze; three
  freeze-gate constants are still `<PIN-AT-FREEZE>` and deliberately refuse it.
- The identity adjudication is driver-side; the preflight remains a kind/ownership/
  readability proof (disclosed above with its reasoning).
- `shellcheck` is not installed on this workstation; no ShellCheck result is claimed.
- Row 24 remains correctly operator-side and is not evaluated by RP7.

## Deliverables

| File | State |
|---|---|
| `RP7-WPI-RO.sh` | repaired, 77179 B, `393a16ce...b0ee`, 0 CR, `bash -n` 0 |
| `SELF_QA_RP7.md` | rewritten; two anchored fences, both executed to `QA_PASS`, real RED/GREEN transcripts |
| `STATUS_RP7.md` | updated to `REPAIRED-R5-PENDING-INDEPENDENT-REAUDIT`, three freeze-gate items |
| `WPI_PREREGISTRATION_DRAFT.md` | five narrow edits, listed above |
| `RP7_REPAIR_R5_REPORT.md` | this file |

Not committed. The Lead commits after verifying the hash.
