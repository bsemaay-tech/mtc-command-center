# RP7 rows 1-9 extension — GLM advance read-audit

Verdict label: **ADVANCE-SUPPLEMENTAL**
Auditor: GLM (unattended, `-PermissionMode acceptEdits`)
Date: 2026-08-13
Mode: source-level only. **No execution, no git mutation.** This read closes no
flagship slot; it reduces risk for the later flagship audits.

Subject of record: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`
Design of record: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROWS_1_9_OPTIONS_CODEX_2026-08-10.md` §D
Adjacent artifacts read: `WPI_BLOCKS_DRAFT/SELF_QA_RP7.md` (rebuild-fence section),
`WPI_BLOCKS_DRAFT/STATUS_RP7.md`.

---

## Identities re-derived before reading

Target block, re-derived with `wc -c` and `sha256sum`:

| field | kickoff-stated | re-derived | match |
|---|---|---|---|
| bytes | 126182 | 126182 | yes |
| sha256 | `8355cb00fda8af2140d99ff9e97fe458376215dbd39267b2f2958d29fb9aba85` | `8355cb00fda8af2140d99ff9e97fe458376215dbd39267b2f2958d29fb9aba85` | yes |

`STATUS_RP7.md:46-50` records the same final identity and a prior identity
(`previous_sha256=0e93f90d…`, `previous_bytes=108301`), consistent with a
scoped extension over the previously-accepted bytes.

---

## Coverage boundary (read honestly, not exhaustively)

Read in full:
- Design of record **§D** in full (`ROWS_1_9_OPTIONS_CODEX_2026-08-10.md:185-365`),
  i.e. §D.1 smallest-correct-shape, §D.2 plan deltas, §D.3 cost, §D.4 failure
  modes, §D.5 fixtures, §D.6 scope limit.
- Block new/changed code: the show-capture helpers and row-5/6/8/9 assertion
  functions (`RP7-WPI-RO.sh:528-835`); the reused row-7 digest predicate
  (`RP7-WPI-RO.sh:1328-1340`); the dispatch (`RP7-WPI-RO.sh:2023-2090`); the
  leaf/capture discipline the new code inherits (`RP7-WPI-RO.sh:272-360`).
- The rebuild fence in `SELF_QA_RP7.md` in full (`SELF_QA_RP7.md:1-256`, the
  whole `RP7_ROWS_1_9_REBUILD_FENCE_BEGIN…END` block).
- `STATUS_RP7.md` in full (55 lines).

NOT read (out of scope / deferred to flagship): the remainder of
`SELF_QA_RP7.md` (`:257-4831`), the block's pre-existing B3/B1/B5_B6 sections,
the design doc's §A-§C and §E-§G, the preregistration section-8.2 row text, and
the wider `WPI_BLOCKS_DRAFT` directory. Stopping here keeps the read inside the
bounded SMALL/MEDIUM budget the kickoff set.

---

## Findings

### REQUIRED

#### R1 — Row-8 rendered sandbox literals are committed, but confirmed only against author-supplied fixtures; §D.4 #2's #1 derivation risk is not closed by this fence
`wpi_expected_sandbox_value` (`RP7-WPI-RO.sh:671-685`) commits ten concrete
literals, including the four properties §D.4 #2 (`:296-304`) names as "where the
derivation risk sits": `ProtectSystem=strict` (`:674`),
`RestrictAddressFamilies='AF_INET AF_INET6 AF_UNIX'` (`:676`),
`CapabilityBoundingSet=''` (`:677`), `ReadWritePaths='/var/lib/mtc-bridge
/var/log/mtc-bridge'` (`:678`), plus the scalars `KillSignal=15` (`:679`),
`KillMode=mixed` (`:680`), `TimeoutStopSec→45s` (`:681`, queried as
`TimeoutStopUSec` via `:687-692`).

The rebuild fence GREENs these (`SELF_QA_RP7.md:149`) against a fixture the
implementer authored. A self-supplied fixture cannot validate the rendering
assumption — it can only prove the comparator is self-consistent. Two concrete
rendering questions the fence leaves open:
- `KillSignal=15` — modern `systemctl show -p KillSignal` renders the **symbolic**
  `SIGTERM`, not `15`. If the host renders symbolic, both the fixture and the
  literal are wrong together and the fence still passes.
- `CapabilityBoundingSet=''` requires the unit to **explicitly** drop all
  capabilities; if the fragment does not set it, systemd renders the full default
  set, not empty.

§D.4 #2 states deriving and defending these four renderings from committed
records is "the first task of the rows-1-9 round, not the last." This advance
read sees the literals committed but sees **no derivation provenance in scope**.
Flagship must demand the derivation (or a host observation) before freeze; per
§D.4 #2, if undefendable the row can only STOP and the worst-case cost is paid.

#### R2 — ExecStart parser splits the rendered struct on `;` and recognizes only three fields; real systemd ExecStart rendering is richer and is not exercised by the fence
`wpi_assert_unit_execstart` (`RP7-WPI-RO.sh:577-607`) parses the `ExecStart={…}`
value by `IFS=';' read -r -a` (`:583`) and recognizes only `path`, `argv[]`,
`ignore_errors` (`:591-595`); any other token without `=` trips
`execstart_field_grammar` STOP (`:589`).

`systemctl show -p ExecStart` for a *started* unit renders additional runtime
fields, and the bracketed timestamp form `start_time=[<datetime>; <duration>
ago]` contains a literal `;`. A flat `;` split would break mid-timestamp,
producing a token with no `=` and a **false STOP on a correctly-running unit**.
The fence's ExecStart fixture (`SELF_QA_RP7.md:138`) renders only the three
known fields with no timestamps, so it neither reproduces nor stresses the real
rendering. (I cannot execute to confirm the exact field set on the host's
systemd; flagging the parsing fragility and the fixture gap, both citable.)
This is the "single largest source of review surface" row per §D.3 #1
(`:258-265`).

#### R3 — Row 1 is implemented via the `ActiveState` property, not `systemctl is-active` as row 1 is verbatim written; this is a §D.4 #3 preregistration amendment needing its own review
The implementation reads `ActiveState` from the `show` capture
(`RP7-WPI-RO.sh:751-753`), not `systemctl is-active`. This is design §D.4 #3
**option (b)** (`:305-309`): cleaner and it sidesteps the Pattern-1 rc trap —
and the STOP/FAIL split is done correctly (`inactive`→`B2_FAIL unit_not_active`
at `:753`; absent record→STOP via `wpi_show_get` at `:568`). But §D.4 #3 states
explicitly that this "amends a preregistered row and is its own review step."
The §B verbatim row-1 text (`:106`) still says "`systemctl is-active` returns …
active." Flagship must confirm the **section-8.2 preregistration text for row 1
was amended** to match the `ActiveState`-property implementation; otherwise the
block implements a different predicate than the one under acceptance. (The 8.2
text is outside this read's scope — flagged, not verified.)

#### R4 — The §D.5 row-5 "decoy" fixture is absent from the rebuild fence
§D.5 (`:338`) requires the row-5 demonstration: "Release/venv path present only
in a comment, an inactive directive, or environment text → Must NOT satisfy the
binding." §D.5 (`:351-353`) marks **5-decoy, 6-comment and 9-substring** as
"not optional extras … the demonstrations that distinguish a parser from a
matcher." The fence provides 6-comment (`SELF_QA_RP7.md:206`) and 9-substring
(`:242`) but **not** 5-decoy. Lower-risk than it sounds, because row 5 binds
`ExecStart` structurally from the rendered `show` value
(`RP7-WPI-RO.sh:577-607`) rather than substring-matching the fragment, so a
venv path hidden in a fragment comment cannot reach the comparator; but the
§D.5-named fixture is still missing and the flagship should either add it or
record the structural-parsing rationale for its absence.

### NIT

#### N1 — B2 capture-level parse errors are labeled `system_manager_unreachable`, diverging from §D.5 row 5's prescribed `unit_definition_unreadable`
The B2 show capture binds its STOP reason to `system_manager_unreachable
operation=show` (`RP7-WPI-RO.sh:742`), and the whole-table parse inherits that
reason (`:749`). So a truncated/ungrammatical show at rc 0 STOPs as
`system_manager_unreachable … detail=unterminated_final_record` — which is
exactly what the fence's `r5_truncated` RED asserts (`SELF_QA_RP7.md:203`).
§D.5 row 5 (`:340`) prescribes `unit_definition_unreadable` for "truncated or
ungrammatical show output." The **verdict is correct** (STOP, not FAIL), but the
top-level reason token conflates "manager unreachable" (the rc≠0 case at
`:747`) with "manager reached, output ungrammatical" (the rc=0 parse case), and
the r5_truncated RED consequently fails for the capture-level reason rather than
row 5's own prescribed reason. Note the internal inconsistency: B4's analogous
capture-level parse errors use `unit_property_unreadable` (`:803,:811`), so the
two sections label the same failure class differently.

#### N2 — Row-6 Install-section match is case-sensitive; systemd parses section names case-insensitively
The fragment grammar parser matches `[Install]` case-sensitively
(`m.group(1)=="Install"`, `RP7-WPI-RO.sh:650`, regex at `:635`). Thus `[install]`
is counted as a section but not flagged, and the fence treats it as a CONTROL
GREEN (`SELF_QA_RP7.md:208`). systemd honors section names **case-insensitively**,
so a `[install]` header would be a real Install section on the host and the unit
would install, yet the block would not flag it. This matches the §D.5 fixture's
stated intent (`:341`: "case-variant `[install]` → Must NOT trigger
`install_section_present`"), so it is consistent with the design as written —
but the flagship may want to revisit it against systemd semantics. (All other
§D.5 row-6 fixtures are covered and correct: comment `:206`, continuation
`:207`, real Install `:209`, NUL `:211`.)

---

## What this read verified as correct (positive confirmations)

Structural conformance to §D.1:
- The two new sections are placed between the manager preflight
  (`wpi_assert_manager_ready`, `RP7-WPI-RO.sh:2048`) and `B3_rows_10_15`
  (`:2057`), exactly as §D.1 (`:189-191`) prescribes.
- Two bounded `systemctl show` captures, reusing `wpi_capture` unchanged
  (`:743` B2, `:804` B4) — not eleven. Precedence rule rc→stderr→stdout is
  applied in both (`:747-749`, `:809-811`).

Presence-before-value and absent→STOP (the core §D.4 #4 discipline):
- `wpi_show_get` (`:566-570`) checks `WPI_SHOW_SEEN[$query]` and STOPs with
  `property_record_absent` **before** returning any value (`:568`). Every
  property access in B2 (`:751,756,761,766,771,776,780,784,788`) and B4
  (`:815,827`) goes through it; no value is used before presence is proven, and
  no absent record is defaulted to empty.
- `wpi_parse_show_capture` (`:530-564`) is a genuine multi-record reader
  satisfying §D.4 #6: hard-read-error (`:540`), NUL byte (`:541`), empty output
  (`:542`), charset (`:543`), unterminated final record (`:548`), blank/grammar/
  duplicate/unexpected property (`:551-559`), byte accounting (`:563`) — and it
  reaches a semantic verdict only after the whole table parses.

Leaf discipline (the `wpi_alloc_leaf` concern):
- There is no name-based leaf addressing. Leaf allocation is `wpi_open_leaf`
  (`:272`), which validates each path is under `$EV_DIR/*` (`:274`) and
  addresses leaves by the monotonic `WPI_PROBE_SEQ`
  (`:349-350`, e.g. `ro.0007.b2_unit_show.stdout`). The new sections inherit
  this by reusing `wpi_capture` / `wpi_alloc_read_diag`; they introduce no
  name-addressed leaf.

Trusted-Python discipline (§D.1 "restate startup self-check"):
- Row-6 parser is invoked `"$WPI_PYTHON3" -I -S -c` over a **stdin descriptor**
  bound to the fragment fd (`RP7-WPI-RO.sh:619-621`), not a re-resolved name,
  and performs the isolation self-check (`:623-627`).
- Row-9 tokenizer is invoked `"$WPI_PYTHON3" -I -S -c` with the Environment
  value as an argv element (`:697`), with the same self-check (`:699-703`) and
  `shlex` tokenization that rejects duplicates and substring-only matches
  (`:713-725`). Both use the **bound** `$WPI_PYTHON3` (the round-4 tenth pin),
  not bare `python3`.

Row 7 reuse and capture ordering:
- Row 7 reuses `wpi_assert_regular_digest` (`:795-797`), which manages its own
  mount window and captures size/digest into locals **before**
  `wpi_mount_guard_end` (`:1330-1338`).
- Row 6 consumes its parser capture (`parser_rc` `:657`, stderr `:659`, record
  `:660-661`) **before** `wpi_mount_guard_end` (`:662`) — the real defect
  `STATUS_RP7.md:27-30` says the rebuild exposed and fixed. Verified in the
  delivered bytes.

Terminal claim and pin class (§D.2):
- Terminal claim is `establishes=rows_1_23…` with the manager-identity
  disclaimer preserved (`does_not_establish=…host_authority_or_any_manager_
  identity_beyond_the_attested_execution_domain_that_answered`,
  `RP7-WPI-RO.sh:2087-2088`); matches §D.2 (`:234`) and `STATUS_RP7.md:24-26`.
- New pin class recorded as "ten rendered row-8 sandbox values, the expected
  FragmentPath, and the expected-empty DropInPaths set for row 5"
  (`STATUS_RP7.md:22-23`); `$WPI_EXPECTED_DROPIN_PATHS=''` (`RP7-WPI-RO.sh:98`),
  fragment bytes pinned to 3736 (`:1161`), MainPID pinned to 189813 (`:1201`).
  Matches §D.2 (`:231`).

Rebuild fence quality (scope item 2):
- The fence **does** extract and invoke the block's own functions: it strips
  only the terminal `wpi_main "$@"` call (`SELF_QA_RP7.md:52-55`, verified
  absent at `:55`), confirms `wpi_assert_b2_rows_1_7`/`wpi_assert_b4_rows_8_9`
  are present (`:56-57`), **sources** the extract (`:59`) and drives the real
  B2/B4/row-6/row-7 functions (`:182-244`). It is not a re-implementation.
- It asserts block identity (bytes/sha/CRLF=0) **before and after** the run
  (`:47-51`, `:250-254`) and syntax-checks both block and extract
  (`bash -n`, `:50,:54`).
- **No expected value is formatted as a timing/derived measurement**: expected
  lines are categorical tokens (`active`/`inactive`, `yes`/`no`, `loaded`),
  pinned integers (MainPID 189813, fragment bytes 3735/3736, counts), paths, and
  sha256 digests (`:182-244`).
- **Every row's RED fails for a row-specific reason**, with one exception
  documented as N1: the `r5_truncated` RED fails at the capture-level parse
  (`system_manager_unreachable`, `:203`) rather than row 5's prescribed
  `unit_definition_unreadable`. All other REDs (rows 1-4, 5-fragment/dropin/
  exec/not-found, 6-real/nul, 7-short/wrongsha/unreadable, 8-mismatch/missing,
  9-duplicate/substring) fail for their own row's predicate, because each
  fixture mutates only the field under test and the whole-table parse succeeds.
- Arithmetic is honest: 20 RED/GREEN pairs + 4 controls
  (`SELF_QA_RP7.md:255`), plus 2 B4-property-count controls (`:245-249`).

Inherent fence limitation (not a defect, recorded for the flagship): the
`systemctl` the block calls is a synthetic script (`SELF_QA_RP7.md:81-89`) and
every show output is an author-supplied fixture (`:128-154`). The fence proves
the block's B2/B4 **logic** is internally consistent and routes RED/GREEN
correctly; it does **not** validate fidelity to real `systemctl show` rendering.
Consequently R1 and R2 can only be closed by a host run or a derivation from
committed records, not by this fence.

---

## Closing statement

No execution occurred. No git mutation occurred. No file outside this single
report was written. This was a source-level read only. Verdict label
**ADVANCE-SUPPLEMENTAL**: it reduces risk for the later flagship audits and
closes no flagship acceptance slot. The four REQUIRED items (R1 row-8 rendered
literals' derivation provenance, R2 ExecStart `;`-split vs real systemd
rendering, R3 row-1 prereg amendment consistency, R4 missing §D.5 row-5 decoy
fixture) and two NITs (N1 B2 capture-level reason label, N2 case-sensitive
Install match) are offered for the flagship rounds to resolve; the positive
confirmations above stand as verified.
