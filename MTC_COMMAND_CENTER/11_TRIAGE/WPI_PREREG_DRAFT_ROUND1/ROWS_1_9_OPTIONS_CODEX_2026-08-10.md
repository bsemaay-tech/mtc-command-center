# Section 8.2 rows 1-9 - build them, or defer them and narrow every claim

Analysis only, authored 2026-08-10 under the Codex-led T2 documentation kickoff
`KICKOFF_CODEX_ROWS_1_9_OPTIONS.md`. No host contact, no network, no git action, no source
edit. This file is the only path this session created or changed. Every "AFTER" sentence in
section E is a **proposal for the Lead**, not an applied edit: the preregistration draft, both
blocks, the Audit-2 package, the gap matrix and the roadmap are untouched.

---

## A. Decision frame, and exactly what is covered today

### A.1 The decision

Freeze is blocked on one question the owner alone can answer: **do the nine section-8.2 rows
that describe the running service get built before the WP-I run, or do they get formally
deferred and every downstream sentence narrowed to match?** There is no third option in which
they are quietly left unimplemented: the run kit is frozen by hash, the closure record feeds
Audit 2, and the auditors are instructed in writing not to infer an unevidenced state.

### A.2 Current coverage, verified in the bytes

I did not take the skeleton review's word for this.

**`RP6-P0.sh` disclaims all twenty-four rows.** Its out-of-scope section is introduced by the
comment "Silence about an excluded check is how a scope reduction becomes an unnoticed
coverage loss. Everything P0 does not implement is named here." (`RP6-P0.sh:1618-1619`). Its
last out-of-scope line, `RP6-P0.sh:1626`, is verbatim:

```
printf 'P0_out_of_scope class=RO_STAGE item=every_prereg_8.2_row stage=ro implemented=no\n'
```

**`RP7-WPI-RO.sh` claims only rows 10 onward.** Header line 3 reads
`# WP-I read-only rows 10-24 (PROPOSED DESIGN, DRAFT).`, and the terminal claim at
`RP7-WPI-RO.sh:1262-1263` is:

```
printf 'RP7_claim establishes=rows_10_23_read_only_predicates_with_attested_preexec_objects_and_service_network_domain;executed_objects_use_separate_bounded_exec_after_preexec_mount_window\n'
printf 'RP7_claim does_not_establish=row_24_operator_side_result,ACL_or_capability_immutability,whole_tree_byte_identity,root_deferred_checks,group_C,host_authority\n'
```

The section headers inside `wpi_main` confirm the coverage boundary directly:
`B3_rows_10_15` (`:1232`), `B1a_row_17` (`:1239`), `B1_rows_18_19` (`:1244`),
`B5_B6_rows_20_24` (`:1249`). There is no `B2` or `B4` section, and no function in the
block's inventory reads unit state, a unit property, the fragment's grammar or the effective
environment. **Confirmed: RP7 still claims only rows 10 onward and implements nothing for
rows 1-9.**

The one manager call RP7 does make is a premise, not a row. `wpi_assert_manager_ready`
(`:667-674`) runs `systemctl --system --no-pager show --property=Version`, requires an empty
diagnostic and a single `Version=` record, and emits
`RP7_preflight system_manager=ready query=Manager.Version output=complete`. That is exactly
what gap 8's proposed clause says it is:

> P0's Manager.Version readiness query is a premise only; it is not evidence for any B2/B4
> row.

### A.3 The gap-8 clause this analysis serves

`SKELETON_REVIEW_CODEX_2026-08-10.md:152-157`:

> **Rows 1-9 coverage gate.** Operations 04 and 05 currently do not execute section-8.2
> rows 1-9. Freeze is blocked until an accepted frozen block and plan operation implement
> those nine rows in the preregistered first-divergence order, or the successor explicitly
> removes/defers them under an owner-approved scope change and narrows every claim and
> closure criterion accordingly. P0's Manager.Version readiness query is a premise only;
> it is not evidence for any B2/B4 row.

### A.4 What RP7 already carries for these rows, and does not use

Three inputs whose only possible consumers are rows 6 and 7 are already validated by the
block, and the fragment path is already attested:

- `wpi_expect_literal WPI_UNIT_FRAGMENT ... /usr/local/lib/systemd/system/mtc-bridge-first-start.service` (`:594`)
- `wpi_expect_literal WPI_UNIT_FRAGMENT_BYTES ... 3736` (`:595`)
- `wpi_require_sha256 WPI_UNIT_FRAGMENT_SHA256 ...` (`:596`)
- `"$WPI_UNIT_FRAGMENT"` is a point in `normalised_path_projection_v2` (`:463`)

And `WPI_MAINPID` is validated and pinned to `189813` (`:634-635`), is a projection point via
`/proc/$WPI_MAINPID/ns/net` (`:467`), and is consumed in production by
`wpi_assert_netns_binding`, which emits
`B6_netns caller=%s service=%s mainpid=%s binding=equal` (`:1073`). The draft's row-22 text
says that binding uses "`readlink /proc/<MainPID>/ns/net` (the service's netns identity,
MainPID from row 4)". **Row 4 does not exist**, so the token `service=` currently rests on a
frozen operator input that no probe re-confirms. That is an independent reason row 4 is worth
more than its mechanical difficulty suggests, and it is why section E carries a disclosure
for that line.

Named risk R1 is closed: `LEAD_PIN_RESOLUTION_2026-08-10.md` resolves
`WPI_UNIT_FRAGMENT_SHA256` to
`538c1c6038b475e87fb0e9b9c35fd4ebd8451b40ff93538f8fea5aa0b49279bd`, matching the matrix's
elided `538c1c60...279bd`. Row 7's expected value therefore exists today.

---

## B. The nine rows, quoted verbatim

From `WPI_PREREGISTRATION_DRAFT.md` section 8.2, original order, table header and result
grammar preserved exactly.

> ### 8.2 RO stage - one row per admitted check
>
> | # | check | predicted outcome if it holds | exact predicted first divergence if it does not |
> |---|---|---|---|
> | 1 | B2 active | `systemctl is-active` returns a parseable unit state and that state is `active` | `B2_STOP reason=system_manager_unreachable operation=is-active rc=<n> detail=<d>` for invocation, bus, namespace, authorization or parse failure; after manager reachability is proven, a valid state such as `inactive` is evaluable and becomes `B2_FAIL reason=unit_not_active state=<s> expected=active` even when `is-active` uses a nonzero result rc |
> | 2 | B2 restart count | `NRestarts` is `0` | `B2_STOP reason=unit_property_unreadable prop=NRestarts rc=<n> detail=<d>` before comparison on any manager/query/parse error; only a successfully read value may become `B2_FAIL reason=nrestarts_nonzero value=<n> expected=0` |
> | 3 | B2 restart policy | `Restart` is `no` | `B2_STOP reason=unit_property_unreadable prop=Restart rc=<n> detail=<d>` before comparison on any manager/query/parse error; only a successfully read value may become `B2_FAIL reason=restart_policy value=<v> expected=no` |
> | 4 | B2 process identity | `MainPID` is `189813` | `B2_STOP reason=unit_property_unreadable prop=MainPID rc=<n> detail=<d>` before comparison on any manager/query/parse error; only a successfully read value may become `B2_FAIL reason=mainpid_changed value=<p> expected=189813` - **named risk R3**: with `Restart=no` a live unit cannot have self-restarted, so a changed MainPID means a manual restart between the transition inventory and dispatch. That is a FAIL requiring Lead adjudication, never a silent re-pin |
> | 5 | B2 candidate binding | after P0 domain binding, complete manager properties are structurally parsed: the effective `ExecStart` argv (not comments, inactive directives, environment text or arbitrary substrings) binds its executable and release argument to the exact venv and release roots for `2ce41e34...321b`, and the effective fragment/drop-in set contains no unpreregistered override | a valid complete manager result `LoadState=not-found` is observed deviant state and becomes `B2_FAIL reason=unit_not_loaded`; `B2_STOP reason=unit_definition_unreadable operation=show rc=<n> detail=<d>` applies only to invocation, bus, namespace, authorization, timeout, incomplete-output or grammar error; any other complete structural mismatch becomes `B2_FAIL reason=unit_not_bound_to_candidate field=<field> observed=<v>` |
> | 6 | B2 no `[Install]` | after path-object binding, a complete byte read of the fragment is parsed under the systemd unit-file line grammar and contains no section header whose exact parsed name is `Install`; comments, continuations and arbitrary substrings do not count | `B2_FAIL reason=unit_fragment_absent path=<p>` on positively established ENOENT; `B2_STOP reason=fragment_unreadable_or_unparseable rc=<n> path=<p> detail=<d>` on invocation/access/read/encoding/NUL/grammar or ambiguous-ENOENT error; only a complete successful parse may become `B2_FAIL reason=install_section_present path=<p>` - grep or substring matching is not admissible |
> | 7 | B2 fragment identity | after the section-wide path-object binding holds, `sha256sum` equals `WPI_UNIT_FRAGMENT_SHA256`, size 3736 | `B2_FAIL reason=unit_fragment_absent path=<p>` when a searchable, bound parent chain positively establishes ENOENT; `B2_FAIL reason=unit_fragment_digest_mismatch observed=<h> expected=<h>` only after `sha256sum` exited 0 and emitted a syntactically valid 64-hex digest plus the 3736-byte count; `B2_STOP reason=fragment_unreadable rc=<n> path=<p>` for invocation, permission, LSM, ambiguous-ENOENT or parent-traversal error |
> | 8 | B4 sandboxing | each named property is successfully read and equals the template-declared value (`PrivateTmp`, `ProtectSystem`, `NoNewPrivileges`, `RestrictAddressFamilies`, `CapabilityBoundingSet`, `ReadWritePaths`, `KillSignal`, `KillMode`, `TimeoutStopSec`, `FinalKillSignal`) | `B4_STOP reason=unit_property_unreadable prop=<P> rc=<n> detail=<d>` before comparison on any invocation, bus, namespace, authorization, incomplete-output or parse error; only a successfully read property may become `B4_FAIL reason=property_mismatch prop=<P> observed=<v> expected=<v>` |
> | 9 | B4 start mode | the complete effective `Environment` value is parsed as systemd's tokenized environment grammar and contains exactly one effective `MTC_BRIDGE_START_MODE` assignment whose value is `credential_free_disarmed`; a duplicate, shadowed or substring-only occurrence does not satisfy the row | `B4_STOP reason=unit_property_unreadable prop=Environment rc=<n> detail=<d>` before interpretation on any manager/query/grammar error; only a complete successful parse may become `B4_FAIL reason=start_mode_missing_or_altered observed=<v>` |

Two facts about that text govern everything below.

**The rows are already authored.** Neither option starts from a blank page. The grammar, the
STOP-before-FAIL ordering, the structural-parse prohibitions and named risk R3 exist and have
survived the draft's review rounds. Option A implements text that exists; option B suspends
text that exists.

**Their position is load-bearing.** Rows 1-9 precede rows 10-24 in the preregistered
first-divergence order. A wrong or unbound service is meant to be seen *before* the run spends
its remaining evidence describing files that may belong to a different process.

---

## C. Per-row feasibility

"Needs root" means: does the observation require privilege *by construction*. "Pinned tools"
is the ten-tool set RP7 binds inside its mount window (`RP7-WPI-RO.sh:1220`):
`stat readlink env find sha256sum systemctl ss curl timeout python3`.

| # | Assertion | Establishing host observation | Read-only | Needs root | Pinned tools sufficient | Difficulty | Reason |
|---|---|---|---|---|---|---|---|
| 1 | The unit is `active` | One bounded manager query returning a parseable unit state, adjudicated so a valid `inactive` (a result) is separable from "could not ask" (a STOP) | Yes | No | Yes (`systemctl`, `timeout`, `env`) | **MEDIUM** | Mechanically trivial, but `is-active` returns nonzero both for a genuine `inactive` and for a failed invocation, so the rc must be decoded through an exhaustively preregistered table or the row collapses STOP and FAIL into one branch. |
| 2 | `NRestarts` is `0` | One `show` record for `NRestarts`, proven present, then integer-parsed | Yes | No | Yes | **LOW** | A single scalar with an unambiguous grammar; the only discipline needed is that an unknown property must not render as an empty value. |
| 3 | `Restart` is `no` | One `show` record for `Restart`, proven present, then token-compared | Yes | No | Yes | **LOW** | Same shape as row 2 over a small closed token set. |
| 4 | `MainPID` is `189813` | One `show` record for `MainPID`, proven present, integer-parsed, compared to the preregistered value | Yes | No | Yes | **MEDIUM** | The read is trivial, but a mismatch is named risk R3 and routes to Lead adjudication, and this is the only row that would justify RP7's existing production use of PID 189813 in the netns binding. |
| 5 | The loaded unit is bound to candidate `2ce41e34...321b` with no unpreregistered override | One complete `show` result, structurally parsed: effective `ExecStart` (compound `path=` / `argv[]=` / flags record), `FragmentPath`, `DropInPaths`, `LoadState` | Yes | No | Yes for capture; the parser must be the pinned trusted `python3` under `-I -S` | **HIGH** | Binding "the executable and the release argument" is real argv parsing of a compound multi-valued record, plus enumeration of the drop-in set against an expected-empty set - not field extraction, and explicitly not substring matching. |
| 6 | The fragment contains no `[Install]` section | A complete byte read of the fragment, parsed under the systemd unit-file line grammar (sections, comments, continuations, encoding) | Yes | **No - and no manager either** | Yes (`stat`/`sha256sum` for binding, trusted `python3` for the grammar) | **MEDIUM** | The read is unprivileged over a `0644` world-readable object already in the section-10.1 allowlist, but the row forbids substring matching, so a real line-grammar parser must be authored and falsified. |
| 7 | The fragment is byte-identical to the accepted unit (3736 B, `538c1c60...279bd`) | Component-and-mount-bound `lstat` plus `sha256sum` of the literal fragment path | Yes | **No - and no manager either** | Yes | **LOW** | `wpi_assert_regular_digest` already does exactly this for rows 17 and 19a; path, byte count and digest are already validated block inputs and the path is already a projection-v2 point. |
| 8 | Ten sandbox properties equal their template-declared values | One bounded `show` with explicit per-property selection, each record proven present before comparison | Yes | No | Yes | **HIGH** | The query is easy; the expected values are not. The gap matrix's B4 entry records only that "the template declares them (A4)" - no effective-property capture has ever been taken - and systemd's rendered forms for the enum, list and capability-set properties are not the template's text, so ten new expected literals must be derived and pinned before freeze. |
| 9 | Exactly one effective `MTC_BRIDGE_START_MODE=credential_free_disarmed` | One complete `show` record for `Environment`, tokenized under systemd's environment grammar | Yes | No | Yes for capture; parser must be the trusted `python3` | **HIGH** | The row rejects duplicate, shadowed and substring-only occurrences, which is a tokenizer requirement including quoting and escaping - one assignment appearing twice must be distinguishable from one appearing once. |

### C.1 Testing the required conclusion: read-only, and root

**Confirmed, with one correction of emphasis.** All nine are read-only observations - each is
a query or a file read, none mutates the host - and **none needs root by construction**. The
installed fragment is recorded at `0644`, 3736 B, "world-readable regular file" in the
section-10.1 unprivileged allowlist (`WPI_PREREGISTRATION_DRAFT.md:1027`), and its parent
chain is world-searchable, so rows 6 and 7 are ordinary unprivileged reads. Nothing in my
reading disproves any part of that conclusion. **No row changes the authorisation question.**

The correction is that "no root needed" is the less important half of the answer.
**Seven of the nine (1-5, 8, 9) depend on an authorization that has never been demonstrated
on this host**: that `gatea` can reach the intended system manager over the system bus from
its PID/mount namespace, pass D-Bus/polkit policy, and get a complete parseable answer inside
a deadline. The draft already routes them conditionally on exactly that
(`WPI_PREREGISTRATION_DRAFT.md:999-1002`):

> - B2 rows 1-5 and B4 rows 8-9 if `gatea` cannot establish P0 system-manager query
>   readiness because `systemctl`, the system bus, the intended PID/mount namespace or
>   D-Bus/polkit authorization is unavailable. Direct fragment reads in B2 rows 6-7
>   remain unprivileged; manager-backed state/property claims require RPD-VERIFY.

So the real risk is not privilege, it is that seven rows can STOP on the day and route to
RPD-VERIFY no matter how much code was written for them. **Rows 6 and 7 carry none of that
risk.** They need no manager, no bus, no polkit and no root.

### C.2 Testing the required conclusion: tools

**Confirmed.** The pinned `systemctl`, `env`, `timeout`, `python3`, `stat`, `readlink` and
`sha256sum`, plus the existing capture and path/mount-binding machinery, are sufficient for
all nine. `wpi_capture` already records stdout, stderr, rc and elapsed time per child;
`wpi_single_record` already distinguishes clean EOF, an unterminated populated final record
and a hard read error; `wpi_walk_components` and `wpi_build_mount_projection` already bind
paths component-wise inside a mount window; `wpi_assert_regular_digest` already implements
row 7's exact shape. No new tool pin, no eleventh binary, no new authority class. What is
missing is not capability - it is three parsers and ten expected values.

---

## D. Option A - build them

### D.1 The smallest correct shape

**Extend `RP7-WPI-RO.sh` with two sections placed between the manager preflight and
`RP7_SECTION B3_rows_10_15`, in the preregistered first-divergence order. Do not author a new
transport stage or a new block.**

| Surface | Extending RP7 | A new rows-1-9 block/stage |
|---|---|---|
| Manager readiness | `wpi_assert_manager_ready` already runs STOP-first before any comparison | Must duplicate it, or inherit an unproven premise across a process boundary |
| Tool binding | `systemctl`, `python3`, `stat`, `readlink`, `sha256sum`, `timeout`, `env` already bound inside the mount window | Must rebuild the whole bind loop and its attestation disclosure |
| Path/mount binding | Projection v2 already carries `$WPI_UNIT_FRAGMENT` and `/proc/$WPI_MAINPID/ns/net` | Needs its own projection, its own attested digest, another freeze-gate pin |
| Trusted Python | `-I -S` isolated adjudicator discipline already established and audited | Must restate it, and restate its startup self-check |
| Evidence tree | `EV_DIR` create-once leaves, `wpi_capture`, `wpi_alloc_leaf` reusable as-is | New stage id, new leaf namespace, new binding proof, new close/hash op |
| RUNID and archive | Unchanged | New RUNID accounting, new archive member, new digest set |
| Transport | Op 05 already carries the RO stage; no new op | New op between 04 and 05, new `expect_rc`, new stdin pin, cascade renumbering |
| Divergence order | Rows 1-9 precede rows 10-24 naturally in one process | Cross-process ordering enforced only by the coarse transport sequence |
| Review surface | One artifact under review | A third artifact must earn the two-flagship acceptance floor |

The honest counter-argument: RP7 is already large, and its round-4 finding was a pin defined
in three places and omitted from the one loop that executed - a defect whose root cause is
size. Splitting keeps each artifact reviewable. It loses on every other axis, and decisively
on the acceptance floor, because a new block is a third artifact needing two flagship
acceptances before the freeze gate's first item can be satisfied.

Decomposition inside that shape:

1. `RP7_SECTION B2_rows_1_7` - one bounded `show` capture with explicit per-property
   selection covering rows 1-5, adjudicated record-by-record with presence proven before
   value; then rows 6-7 over the fragment path, reusing `wpi_assert_regular_digest` for row 7
   and adding one trusted-`python3` unit-file line-grammar parser for row 6.
2. `RP7_SECTION B4_rows_8_9` - one bounded `show` capture covering the ten sandbox properties
   plus `Environment`, then the environment tokenizer.

Two captures, not eleven. Each is adjudicated under the existing precedence rule (timeout,
then rc and complete diagnostics, then stdout), so the number of new bounded children stays
small and `wpi_capture` is reused unchanged.

### D.2 What changes in the plan

| Artifact | Change |
|---|---|
| `TRANSPORT_PLAN.tsv` op 05 | **argv unchanged.** Op 05 is `ssh ... bash -s --` with `stdin_file=PREREG:run_ro.sh`; a bigger RP7 does not change the operation, the twelve-op sequence, the first-FAIL cascade or RUNID accounting. |
| `run_ro.sh` | Content unchanged in shape; its `stdin_sha256` `<PIN-AT-FREEZE>` refills at freeze - already a freeze-time fill. |
| Runkit | `RP7-WPI-RO.sh` bytes/SHA-256 (draft section 3, currently `<PIN-AT-STAGE-1>`) and `runkit.tar` bytes/SHA-256 refill; member list unchanged (RP0-LIB, RP0-BOOTSTRAP, RP6-P0, RP7-WPI-RO, run_p0.sh, run_ro.sh). |
| Preregistered pins (draft section 2) | **One new class:** ten *rendered* expected sandbox values for row 8, plus the expected `FragmentPath` and an expected-empty drop-in set for row 5. Rows 6, 7 and 9 need no new pin - the fragment path, byte count and digest are already validated inputs and R1 is resolved. |
| Draft section 8.2 | No re-authoring. The nine rows stand as written. |
| Draft section 9 | The conditional DEFER-ROOT-SIDE bullet for B2 rows 1-5 / B4 rows 8-9 stays exactly as written - it is the correct fallback if readiness fails on the day. |
| RP7 terminal claim | `establishes=rows_10_23...` becomes `rows_1_23...`; the `does_not_establish` list keeps `identity_of_the_manager_that_answered` in substance, i.e. the claim sentence must stay about *the manager that answered in the attested execution domain*, never about "the host". |
| RP6-P0 | Unchanged. Its out-of-scope line stays true: P0 still implements no 8.2 row. |
| Successor skeleton | Freeze-gate item 1 waits on RP7's acceptance *including* the new sections; item 2's accepting-input QA arms grow by the row-8 expected values. |
| Audit-2 package | Nothing to narrow. Handoff item I3 becomes satisfiable as written. |

### D.3 Cost: 3 to 6 additional repair-plus-two-flagship-review rounds

Anchors, stated honestly because they are worse than they first look. `RP7-WPI-RO.sh` has been
through four repair rounds and `RP6-P0.sh` through six - but `KICKOFF_RP7_REPAIR_R5.md` and
`KICKOFF_RP6_REPAIR_R7.md` both exist in `WPI_BLOCKS_DRAFT`, so **neither block has yet
reached a two-flagship acceptance and both anchors are lower bounds, not settled costs.**

**Estimate for all nine rows: 3 to 6 additional rounds, most likely 4.**

| Slice | Rounds | Basis |
|---|---|---|
| Rows 6-7 | 1-2 | Row 7 reuses an already-audited function over an already-validated path, digest and projection point; row 6 adds one small-grammar parser. |
| Rows 2, 3, 4 | 1-2 | Three scalars from one capture; the only new discipline is presence-before-value. |
| Row 1 | 1-2 | Entirely inside the STOP-versus-FAIL trap; likely needs a preregistration amendment if `is-active` is kept. |
| Rows 5, 8, 9 | 3-5 | Three new grammars plus ten expected values that do not exist yet. |
| All nine | **3-6** | Review rounds are shared across sections, so the total is well under the sum; the slowest slice sets the floor. |

**What drives the spread, in order of weight.**

1. **Parsing the effective `ExecStart` and the drop-in set (row 5).** systemd renders
   `ExecStart` as a compound record - executable path, an `argv[]` vector, and flags - and the
   effective definition is fragment plus drop-ins. The row demands that the *executable and
   the release argument* bind to the exact venv and release roots, and that the effective
   fragment/drop-in set contain no unpreregistered override. That is argv-level parsing plus
   set enumeration, with a FAIL/STOP split (`LoadState=not-found` is a FAIL, a grammar error
   is a STOP) that must be right on the first divergence. It is the single largest source of
   review surface.
2. **The unit-file line grammar (row 6).** Section headers, comments, continuations and
   encoding all have to be modelled, because the row states outright that "comments,
   continuations and arbitrary substrings do not count" and that "grep or substring matching
   is not admissible". A parser is a new repair path, and on this cycle new parsers have
   reliably produced their own findings.
3. **Ten sandbox properties (row 8).** Not one predicate but ten, and the expected values are
   the problem, not the query: only template-declared text exists today. Enum, list-valued and
   capability-set properties render differently from how the template writes them, so ten new
   literals must be derived and defended before freeze. If they cannot be derived without
   observing the host, the row can be written but not frozen - see failure mode 2.
4. **`Environment` tokenization (row 9).** Rejecting duplicate, shadowed and substring-only
   occurrences means implementing systemd's quoting and escaping rules, then proving the
   parser distinguishes one assignment from two.
5. **The base rate that repairs generate the next finding.** The pattern catalogue documents
   this as a property of this cycle: replacing `grep` with a Python parser created the
   unisolated-interpreter and non-JSON-constant defects; the mount-boundary predicate added
   for one finding created the mount-reader defect, whose round-3 repair still left the
   empty-nonzero-read defect closed only in round 4; a namespace comparison added to close a
   finding was itself an overclaim. **Three new grammars is three new repair paths.** This is
   most of the distance between 3 and 6.
6. **Compression from batching.** Rows 2, 3, 4 and 7 are near-mechanical and ride free on the
   review rounds the hard rows need. This is the only force pulling the estimate down, and it
   is why the floor is 3 rather than 5.

### D.4 Failure modes

1. **Editing RP7 while its current round is open.** Adding scope to bytes that are under
   audit produces an acceptance of superseded bytes - the defect the skeleton review names
   when it says an acceptance of pre-repair bytes does not count. **Rows 1-9 must be a
   separate, later, scoped round on accepted bytes.** Sequencing constraint, not preference.
2. **Row 8 is unpinnable at freeze.** If the ten rendered values cannot be derived from
   committed records, the block ships with ten more `<PIN-AT-FREEZE>` literals and the row can
   only STOP. Paying several rounds for a row that can only STOP is the worst outcome
   available. The scalar properties (`PrivateTmp`, `NoNewPrivileges`, `KillSignal`, `KillMode`,
   `TimeoutStopSec`, `FinalKillSignal`) render predictably; the enum, list and capability-set
   properties (`ProtectSystem`, `RestrictAddressFamilies`, `CapabilityBoundingSet`,
   `ReadWritePaths`) are where the derivation risk sits. Deriving and defending those four
   renderings from committed records is the first task of the rows-1-9 round, not the last, so
   that the risk is known before the rounds are spent.
3. **Row 1's designed STOP/FAIL collision.** `is-active` uses exit status as a result channel.
   An implementer who writes a bare rc test reproduces the catalogue's Pattern-1 defect
   exactly. Either preregister the exit-code table exhaustively, or read `ActiveState` as a
   property instead - which is cleaner but amends a preregistered row and is its own review
   step.
4. **A missing property rendering as an empty value.** `show -p <Prop> --value` prints an
   empty line at rc 0 for a property the manager does not know. Under rows 2, 3, 4 and 8 that
   is an unread property masquerading as a read one. The block must use the `Prop=value`
   record form and prove the record present before interpreting it.
5. **Implementing from the gap matrix instead of from section 8.2.** The matrix's own proposed
   B2 commands are `systemctl cat ... | grep -E 'releases/2ce41e34|venvs/2ce41e34'` and
   `grep -q '^\[Install\]' ...`. **Neither is admissible** under rows 5 and 6 as written.
   Anyone working from the matrix ships an inadmissible check that passes its happy path.
6. **Multi-record readers.** Rows 5 and 8 need a multi-record reader, which must again
   distinguish clean EOF, a populated unterminated final record and a hard read error, and
   must reach a semantic verdict only after the whole table has parsed.
7. **The seven can STOP on the day anyway** if manager readiness fails on the real host. The
   one-use RUNID is still spent.

### D.5 D026 fixtures the build must produce

Every new predicate needs a recorded RED against a deliberately built state, then GREEN with
the accepted bytes. Minimum fixture set, one line per required demonstration:

| Row | Fixture (RED) | Required result |
|---|---|---|
| 1 | Unit in a valid `inactive` state | `B2_FAIL reason=unit_not_active`, never STOP |
| 1 | Manager unreachable / bus or polkit denial / invocation failure | `B2_STOP reason=system_manager_unreachable`, never FAIL |
| 2,3,4,8 | A property the manager does not know, queried so it renders empty at rc 0 | STOP `unit_property_unreadable`, never a comparison against an empty value |
| 2 | `NRestarts` non-zero | `B2_FAIL reason=nrestarts_nonzero` |
| 3 | `Restart` set to a non-`no` token | `B2_FAIL reason=restart_policy` |
| 4 | `MainPID` differing from 189813 | `B2_FAIL reason=mainpid_changed` routed to Lead adjudication, never a silent re-pin |
| 5 | Drop-in `.conf` overriding `ExecStart` | `B2_FAIL reason=unit_not_bound_to_candidate` |
| 5 | Release/venv path present only in a comment, an inactive directive, or environment text | Must NOT satisfy the binding |
| 5 | `LoadState=not-found` | `B2_FAIL reason=unit_not_loaded`, not STOP |
| 5 | Truncated or ungrammatical `show` output | STOP `unit_definition_unreadable`, not FAIL |
| 6 | `[Install]` inside a comment; after a line continuation; case-variant `[install]` | Must NOT trigger `install_section_present` |
| 6 | A genuine `[Install]` section header | `B2_FAIL reason=install_section_present` |
| 6 | Fragment containing a NUL byte or invalid encoding | STOP `fragment_unreadable_or_unparseable` |
| 7 | Fragment one byte short, and fragment with correct size but altered bytes | `unit_fragment_digest_mismatch` in both, size adjudicated before digest |
| 7 | Unreadable parent component / ambiguous ENOENT | STOP `fragment_unreadable`, never `unit_fragment_absent` |
| 8 | One property mismatched; one property absent | FAIL `property_mismatch` for the first, STOP for the second |
| 9 | `MTC_BRIDGE_START_MODE` assigned twice with different values | Must NOT pass on the first occurrence |
| 9 | A different variable whose name contains the token as a substring | Must NOT satisfy the row |
| 9 | Quoted/escaped forms of the assignment | Tokenized correctly, not substring-matched |

Fixtures 5-decoy, 6-comment and 9-substring are the ones that would have caught the historical
`grep` defects in this project. They are not optional extras; they are the demonstrations that
distinguish a parser from a matcher.

### D.6 What Option A does not buy

Even fully built and accepted, rows 1-5 and 8-9 claim only that *the system manager that
answered a bounded query, over the system bus, from a login whose execution domain was
externally attested, reported these values.* RP6 already disclaims
`identity_of_the_manager_that_answered`. Option A buys narrower honest claims and an unbroken
chain from the running unit to the frozen candidate; it does not buy an unqualified statement
about "the host's systemd".

---

## E. Option B - defer them, and narrow every claim

Deferral is legitimate. It is not legitimate silently: gap 8's clause permits it only "under
an owner-approved scope change" that "narrows every claim and closure criterion accordingly".
This section is that narrowing, written out as replaceable sentences so the deferral has a
falsifiable form - either these exact strings appear downstream, or the deferral was not
applied.

**No owner decision exists as of this writing.** Every AFTER sentence below is a conditional
template for a deferral that has not been chosen. Where a template needs to name the authority
for the deferral, it says so as an instruction to the drafter - *cite the resulting owner
decision record and date* - and never asserts a decision, a record or a date of its own. A
drafter who applies these sentences with that placeholder left unfilled has not applied the
narrowing.

Throughout: the sequence `WP-L Phase 2 closed -> WP-I closed -> freeze SHA and ledger
ratified -> Audit 2 accepted -> WP-A begins` is **preserved unchanged**. Only the meaning of
the second step is renamed, from closure to **limited-scope closure**.

### E.1 Preregistration - the scope-of-claim paragraph (lines 930-943)

**BEFORE:**

> **Scope of the WP-I claim, preregistered.** A clean RO stage admits exactly this:
> the running unit is the accepted first-start unit bound to the frozen candidate,
> the complete release and venv walks found no DAC write bits, the installed lock bytes
> match the preregistered lock digest and the completely readable installed-distribution
> set matches that lock, its sandboxing and start-mode pins are effective, its status
> endpoint in the service network namespace reports credential-free DISARMED, and the
> same service namespace has only the preregistered loopback control listener while the
> operator-side probe cannot connect.

**AFTER:**

> **Scope of the WP-I claim, preregistered (limited scope: section-8.2 rows 1-9 deferred;
> cite the resulting owner decision record and date).** A clean RO stage admits exactly this: the complete
> release and venv walks found no DAC write bits, the installed lock bytes match the
> preregistered lock digest and the completely readable installed-distribution set matches
> that lock, an endpoint answering on the preregistered loopback control port - in a network
> namespace equal to that of the preregistered MainPID, which this run does not bind to the
> unit - reports credential-free DISARMED, and that same namespace has only the preregistered
> loopback control listener while the operator-side probe cannot connect. **It does NOT admit
> that the running unit is the accepted first-start unit, that it is bound to the frozen
> candidate, that it is active, that it has not been restarted, that its fragment is
> unmodified or free of an `[Install]` section, or that its sandboxing and start-mode pins are
> effective. Those are rows 1-9: deferred, implemented by no block, and observed by no
> executable in this run.
> A credential-free DISARMED report from the application's own status endpoint is the
> application describing itself; it is not evidence of how the system manager started the
> process, from which unit definition, or under which sandbox.**

The paragraph's existing negative list ("not a full `verify.sh` run", "not a permissions proof
of the root-owned metadata surface", "not a SIGTERM/reboot/rollback/backup proof", "not WP-L,
WP-A or Audit-2 completion") is retained unchanged and extended by the sentence above.

### E.2 Preregistration section 9 - the DEFER-ROOT-SIDE bullet

**BEFORE:**

> - B2 rows 1-5 and B4 rows 8-9 if `gatea` cannot establish P0 system-manager query
>   readiness because `systemctl`, the system bus, the intended PID/mount namespace or
>   D-Bus/polkit authorization is unavailable. Direct fragment reads in B2 rows 6-7
>   remain unprivileged; manager-backed state/property claims require RPD-VERIFY.

**AFTER:**

> - B2 rows 1-7 and B4 rows 8-9, **unconditionally**. No block implements them and none will
>   be authored for this run. The conditional readiness argument is superseded: these rows are
>   not deferred *because* readiness might fail, they are deferred by owner scope decision
>   (cite the resulting owner decision record and date), and readiness is therefore never
>   tested for them. None of the nine is executed by this run, and this deferral schedules no
>   later execution of them: any future evidence for them requires its own authorization and
>   its own record. Rows 6-7 remain unprivileged file reads and may be re-admitted without any
>   new authority if the scope decision is revisited.

### E.3 Section 8.2 heading, and the RP7/RP6 evidence lines

**BEFORE:** `### 8.2 RO stage - one row per admitted check`

**AFTER:** `### 8.2 RO stage - one row per admitted check (rows 1-9 are DEFERRED by owner scope change <cite the resulting owner decision record and date>: they are retained for the record and are NOT admitted checks - see section 9)`

**BEFORE** (`RP7-WPI-RO.sh:1263`):
`printf 'RP7_claim does_not_establish=row_24_operator_side_result,ACL_or_capability_immutability,whole_tree_byte_identity,root_deferred_checks,group_C,host_authority\n'`

**AFTER:**
`printf 'RP7_claim does_not_establish=rows_1_9_unit_runtime_identity_fragment_integrity_and_sandbox_effectiveness_deferred_by_scope,row_24_operator_side_result,ACL_or_capability_immutability,whole_tree_byte_identity,root_deferred_checks,group_C,host_authority\n'`

**BEFORE** (`RP7-WPI-RO.sh:1073`, forced by section A.4 - under deferral the MainPID is never
re-bound to the unit):
`printf 'B6_netns caller=%s service=%s mainpid=%s binding=equal\n' "$caller" "$service" "$WPI_MAINPID"`

**AFTER:**
`printf 'B6_netns caller=%s peer_at_preregistered_pid=%s mainpid=%s mainpid_source=preregistered_input_unverified binding=equal service_binding=not_established\n' "$caller" "$service" "$WPI_MAINPID"`

**BEFORE** (`RP6-P0.sh:1626`): the existing out-of-scope line, which is true for P0 but leaves
no single line anywhere in the evidence saying rows 1-9 are covered by nobody.

**AFTER:** keep it, and add immediately after it - the `decision=` token is filled from the
resulting owner decision record and date, and the line may not be emitted while it is unfilled:
`printf 'P0_out_of_scope class=RO_STAGE item=prereg_8.2_rows_1_9 stage=ro implemented=no implemented_by_any_block=no disposition=deferred_owner_scope_change decision=<OWNER-DECISION-RECORD-AND-DATE>\n'`

### E.4 Closure criterion - gap 8's coverage gate

**BEFORE:** "Freeze is blocked until an accepted frozen block and plan operation implement
those nine rows in the preregistered first-divergence order, or the successor explicitly
removes/defers them under an owner-approved scope change and narrows every claim and closure
criterion accordingly."

**AFTER:** "Freeze is blocked until either condition is met. **If the owner chooses deferral,
cite the resulting owner decision record and date here:** rows 1-9 are deferred by that owner
scope change, and the freeze gate is then satisfied
only when every narrowing in `ROWS_1_9_OPTIONS_CODEX_2026-08-10.md` section E is applied
verbatim to the successor preregistration, both blocks, the Audit-2 handoff package, the
Audit-2 evidence checklist, the auditor session inputs, the freeze prerequisites and the
Gate-B checklist. **WP-I then closes as a limited-scope closure, and the phrase 'WP-I closed'
is replaced by 'WP-I closed (limited scope: 8.2 rows 1-9 deferred)' everywhere the sequence is
stated.** The sequence itself is unchanged."

### E.5 Audit-2 freeze prerequisites - gate 2

**BEFORE (required close action):** "Obtain both authorities, execute only the authorized WP-I
scope, close it with evidence, and preserve all exclusions. Audit 2 cannot start before this
happens."

**AFTER:** "Obtain both authorities, execute only the authorized WP-I scope, close it with
evidence, and preserve all exclusions - **including, if the owner chooses deferral, the
section-8.2 rows 1-9 deferral, which must appear in the WP-I closure record's open-item
registry with the owner's own words and the date of that decision, and be carried unsoftened
into the Audit-2 handoff. This gate is then satisfied by a limited-scope closure, not a full
one.** Audit 2 cannot start before this happens."

**BEFORE (sequencing stop rule):**
`WP-L Phase 2 closed -> WP-I closed -> freeze SHA and ledger ratified -> Audit 2 accepted -> WP-A begins`

**AFTER:**
`WP-L Phase 2 closed -> WP-I closed (limited scope: 8.2 rows 1-9 deferred) -> freeze SHA and ledger ratified -> Audit 2 accepted -> WP-A begins`

### E.6 Audit-2 handoff package - items I2 and I3

**BEFORE (I2):** "Executed read-only WP-I host-check logs with no-clobber path, SHA-256, and
byte count" / "After authority and execution, verify each no-clobber log path, byte count,
SHA-256, command, output, rc, and RUNID against the WP-I close record."

**AFTER (I2):** "Executed read-only WP-I host-check logs with no-clobber path, SHA-256, and
byte count, **for the limited scope only (section-8.2 rows 10-24; rows 1-9 deferred - cite the
resulting owner decision record and date)**" / "After authority and execution, verify each no-clobber log path, byte count,
SHA-256, command, output, rc, and RUNID against the WP-I close record. **Then verify the
converse: no log, line or claim in the package asserts unit active state, restart count,
restart policy, MainPID continuity, unit-to-candidate binding, `[Install]` absence, fragment
digest, sandbox properties or start mode. Any such assertion is a finding, because no
executable produced it.**"

**BEFORE (I3):** "WP-I current-state proofs: DISARMED, state version, loopback-only,
`Restart=no`, and no credentials loaded" / "Reproduce each named read-only proof from the
authorized host-check record and compare output, rc, hash, and byte count. An auditor unable
to access the recorded evidence must not infer the state."

**AFTER (I3):** "WP-I current-state proofs: DISARMED, state version, loopback-only, and no
credentials loaded. **`Restart=no` is REMOVED from this item.** Restart policy, restart count,
active state, MainPID continuity, unit-to-candidate binding, `[Install]` absence, fragment
identity, sandbox effectiveness and start mode are section-8.2 rows 1-9, deferred by owner
scope change (cite the resulting owner decision record and date), produced by no WP-I
evidence" / "Reproduce each remaining named
read-only proof from the authorized host-check record and compare output, rc, hash, and byte
count. An auditor unable to access the recorded evidence must not infer the state. **The
deferred properties must not be inferred from the DISARMED status reading, from the release
tree evidence, or from the unit template in the repository: the status endpoint is the
application describing itself, and the template is a declaration, not an observation.**"

### E.7 Audit-2 evidence checklist section 3

**BEFORE (third bullet):**

> - ☐ Current-state proofs: DISARMED, `state_version`, loopback-only listener, `Restart=no`,
>   no credentials loaded (Group B5/B6 style).

**AFTER:**

> - ☐ Current-state proofs: DISARMED, `state_version`, loopback-only listener, no credentials
>   loaded (Group B5/B6 style).
> - ☐ Recorded deferral of section-8.2 rows 1-9 (Group B2 in full, and Group B4 in full) with
>   the owner scope-change reference and date. The absence of unit runtime-identity and
>   sandbox-effectiveness evidence is **pre-disclosed and expected**, not a finding against the
>   run; an undisclosed absence is a finding.

The section's second bullet - "Executed read-only host-check logs (Group B items **actually
run**)" - already carries the right hedge and needs no change; the deferral bullet is what
makes "actually run" auditable.

### E.8 Auditor session inputs - scope contract and input bundle

**BEFORE (section 2 scope bullet):** "- WP-I staging-verification closure;"

**AFTER:** "- WP-I staging-verification closure **at its limited scope: the frozen release and
venv trees, installed lock byte identity, installed-distribution parity, the reported
credential-free DISARMED status, and the loopback listener set. Unit runtime identity,
restart policy and count, MainPID continuity, unit-to-candidate binding, fragment integrity,
sandbox effectiveness and start mode are OUT of this scope by owner scope change (cite the
resulting owner decision record and date) and must not be accepted, inferred, or treated as
missing evidence;**"

**BEFORE (section 3 input-bundle row):**
`| WP-I closure and evidence index | `BLOCKED-UPSTREAM: no exact paths recorded in the permitted inputs` |`

**AFTER:**
`| WP-I closure and evidence index (limited scope; 8.2 rows 1-9 deferred - cite the resulting owner decision record and date; that scope-change record is a required member of this bundle) | `PRODUCED-AT-WP-I-CLOSE` |`

The section-3 preamble sentence "Each session must receive only the frozen scope contract..."
gains: "**and the section-8.2 rows 1-9 scope-change record.** An auditor who does not receive
that record cannot distinguish a deliberate exclusion from a coverage failure, and must return
BLOCK rather than guess."

### E.9 WP-A's premise

**BEFORE (roadmap step 5, line 974):** "5. **WP-A 3 h Ubuntu invariant verification** on the
retained Gate-A-authorised staging host, including capture of all required staging evidence."

**AFTER:** "5. **WP-A 3 h Ubuntu invariant verification** on the retained Gate-A-authorised
staging host, including capture of all required staging evidence. **WP-A begins from an
unverified premise: WP-I did not observe the unit's active state, restart policy or count,
MainPID continuity, unit-to-candidate binding, fragment integrity, sandbox effectiveness or
start mode (8.2 rows 1-9 deferred; cite the resulting owner decision record and date). WP-A
may still test behaviour, and its results remain valid as behavioural evidence, but no WP-A
result may be read as establishing which unit definition started the process, whether the
process is the one the frozen candidate installs, or that its hardening is in force. If WP-A
needs that premise, it must come from separate evidence obtained BEFORE the first authorized
restart - rows 2 and 4 are perishable: after any restart, `NRestarts=0` and `MainPID=189813`
can never be observed on this host again, and after host discard nothing can.**"

Group E's preamble gains the same two sentences, since E1/E2 measure restart invariants
against a pre-restart state that would otherwise be a document rather than an observation.

### E.10 Gate B criteria

**BEFORE (line 1012):** "All items below must be satisfied, in this order, before owner
production-deploy approval is requested. Executed-Ubuntu staging/systemd/SQLite/rollback/WP-A
evidence (from the Gate-A-authorised staging action) is a prerequisite."

**AFTER:** "...is a prerequisite. **The systemd portion of that prerequisite cannot cite the
WP-I run for unit runtime identity, restart policy or count, unit-to-candidate binding,
`[Install]` absence, fragment integrity, sandbox effectiveness or start mode: those are 8.2
rows 1-9, deferred (cite the resulting owner decision record and date) and observed by no
executable. Each such property needs separate evidence captured before host discard, or the
corresponding criterion is narrowed in writing or BLOCKED.**"

**BEFORE (line 1017):** "- [ ] systemd start / reboot / SIGTERM verified on the expendable
staging host."

**AFTER:** "- [ ] systemd start / reboot / SIGTERM verified on the expendable staging host.
**WP-I contributes nothing to this item: start mode, unit identity, restart policy and sandbox
effectiveness were deferred (cite the resulting owner decision record and date). Evidence must
come from a separate source, captured before the host is discarded.**"

**BEFORE (line 1021):** "- [ ] Every COVERED/SMALL-GAP invariant required for DISARMED VPS
readiness has passing Ubuntu evidence from WP-A on the retained staging host (per WP-A
invariant map)."

**AFTER:** same, plus: "**The invariant map must record, for each invariant, whether its
premise about how the service was started and hardened rests on an observation or on the unit
template. Any invariant whose premise rests on the template alone is marked NARROWED, and the
Gate-6 security review is told so explicitly rather than being handed a declaration as if it
were a runtime observation.**"

### E.11 What the run still proves, and what it stops proving

**Still proved** - rows 10-23 through RP7, plus operator-side row 24 through transport operation 06:

- the release and venv roots are non-symlink directories at numeric `0555 0:0`, completely
  walkable inside a 120 s bound with clean diagnostics, containing no DAC-writable path
  (rows 10-14);
- `/etc/mtc-bridge`, the state directory and the log directory are non-symlink directories at
  their preregistered numeric modes and owners (row 15);
- the installed `requirements.lock` is byte-identical to the candidate's LF payload, through a
  component-and-mount-bound chain (row 17);
- the venv interpreter is a non-symlink regular file that demonstrably runs and reports 3.12
  (row 18);
- the installed distribution set matches the 56-entry lock, adjudicated by a pinned trusted
  interpreter under `-I -S` over one explicit discovery universe, with the verifier's own
  identity bound first (rows 19, 19a);
- an endpoint on `127.0.0.1:8790`, in a namespace equal to that of PID 189813, returns HTTP
  200 and a strict-JSON credential-free DISARMED body with the flags off (rows 20-21);
- the complete listener table parses and holds exactly one port-8790 loopback listener
  (rows 22-23);
- the operator-side probe cannot connect from outside (row 24).

That is a substantial, honest package. **It is a package about files and a port.**

**Not proved.** Deferral preserves rows 10-23 plus operator row 24 and nothing else. It does
**not** establish:

1. **that the service is active** - row 1;
2. **restart count and restart policy** - rows 2-3; named risk R3 stops being detectable and
   becomes an assumption, and the "first-start, one-shot, never restarted" premise enters and
   leaves the successor as transition-inventory history;
3. **MainPID continuity** - row 4;
4. **any binding from the running process to the frozen candidate** - row 5;
5. **fragment `[Install]` absence and fragment byte identity** - rows 6-7, so nothing shows
   the accepted unit cannot be enabled into a boot target and nothing shows the unit on disk
   is still the accepted one;
6. **effective sandbox properties** - row 8; the security posture reverts from an observation
   to a declaration in a template file;
7. **how systemd started the process** - row 9.

And the point that matters most for how the result will be read: **an API-reported
credential-free DISARMED status is not proof of how the process was started.** It is the
application's own self-report over loopback, corroborated only by a source-code argument at
the candidate. Row 9 was the only check on the pinned start-mode assignment that is supposed
to *cause* that report.

### E.12 The strongest bridge that is lost

**Running process to frozen candidate.** Rows 10-19 prove the *installed release* is intact.
Rows 20-23 prove *something* on loopback answers correctly. Row 5 was the only row that joins
them by binding the effective `ExecStart` to that release root and that venv. Without it, a
service started from a different unit file, a different `ExecStart`, an overridden drop-in, or
by hand produces byte-for-byte the same rows 10-24 output. The run then proves that the right
bits are on the disk and that a healthy-looking thing is listening - not that they are the
same thing.

Downstream, that single missing bridge is what each consumer inherits:

- **Audit 2** must accept a deliberately limited WP-I package, with the deferral disclosed in
  the closure record's open-item registry. A disclosed gap is an accepted scope; an
  undisclosed one is a required finding from an auditor who reads I3, finds no evidence, and
  follows the instruction it was given not to infer. The whole cost of Option B lands on
  whether E.1-E.10 are actually applied before dispatch.
- **WP-A** may still test behaviour, and should, but inherits an unproven identity, hardening
  and startup premise - and it is the *mutating* package, the most expensive place to discover
  that the premise was wrong.
- **Gate B's** broad staging/systemd evidence requirement cannot cite this run for the omitted
  properties. Each needs separate evidence, a narrowed criterion, or a BLOCK. The window is
  hard: after WP-A's first authorized restart, rows 2 and 4 are unobservable forever, and
  after host discard there is no channel for any of the nine.

---

## F. Recommendation

**Option A. Build all nine rows, in one scoped round opened after the current RP7 bytes have
finished their existing acceptance cycle.** The decision in A.1 is binary and this
recommendation takes one side of it: all nine, not a subset.

Grounds:

1. **Row 5 is the only running-process-to-frozen-candidate bridge** (E.12). It is the single
   row that joins "the right bits are on the disk" to "something healthy is listening". No
   cheaper row buys that bridge back, so it cannot be the row dropped for cost.
2. **Rows 8 and 9 are the runtime hardening and startup proof.** Row 8 is the only observation
   of effective sandbox properties; without it the posture reverts to a declaration in a
   template file. Row 9 is the only check on the pinned start-mode assignment that is supposed
   to *cause* the credential-free DISARMED report - and that report is the application
   describing itself. Dropping either leaves the hardening claim resting on text nobody ran.
3. **Deferral makes Audit 2, WP-A and Gate B inherit weaker premises** (E.12). All three
   inherit the same unproven premise, and the window closes: after WP-A's first authorized
   restart, rows 2 and 4 are unobservable forever, and after host discard so is everything else.
4. **The rows are authored, the tooling exists, and no new authority is needed.** Section C
   confirms all nine are read-only, none needs root by construction, and the ten pinned tools
   suffice. D.1 shows the smallest correct shape is two new sections inside RP7 - not a new
   block, not a new transport op, no RUNID or archive churn.
5. **Sequencing is a hard constraint, not a preference.** No rows may be added to RP7 until its
   current round's bytes hold two flagship acceptances; adding scope to bytes under audit
   produces an acceptance of superseded bytes.

**The honest price: 3 to 6 additional repair-plus-two-flagship-review rounds, most likely 4**
(D.3), on top of two blocks not yet accepted once. That cost is real and is not minimised here.
It buys a WP-I closure whose premises are observed rather than assumed. On this cycle, the
stronger premise is worth the rounds.

The two Option-A risks in D.4 stay named: row 8's ten rendered values may not be derivable
before freeze, and the seven manager-backed rows can STOP on the day if readiness fails.
Neither is a reason to build less; both are reasons to schedule the round deliberately rather
than fold it into an open one.

If the owner instead chooses deferral, that choice is legitimate, but only if every sentence in
section E is actually applied before Audit 2 is dispatched - Option B is not "skip nine checks",
it is "skip nine checks and narrow every downstream claim to match".

---

## For the owner, in plain language

There is one decision, and it is yours. It is all nine or none.

Today's checks look at the program files on the rented test machine, the one network door it
answers on, and what the program says about itself. Nine further checks would look at how the
machine's own start-up manager is running the program: whether it is running, whether it was
restarted, whether it was started from exactly the copy we approved, and whether its safety
settings are switched on. Nobody has built those nine.

My recommendation is to build all nine, starting once the work now under review is signed off.
The honest cost is three to six more rounds of building and checking. That cost is real.

Skipping them is quicker, but it costs two things. We lose the only check tying the running
program to the copy we approved, so we would know the right files are there and that something
is answering, but not that they are the same thing. And we lose any proof that its safety
settings and start-up mode actually work. The test machine is wiped after the next stage, and
some of these facts can never be checked later.
