REQUEST_CHANGES

## Emit-site table

**TIER: T0. APPLIED AUDITOR CONTRACT: Codex `gpt-5.6-sol`, effort xhigh, fresh
report-only audit.** Subject identity was re-derived before review:

```text
RP6-P0.sh sha256 = 08e0a93562bb04f4f78bac77d973a26da5b609aa305491d3bfa51743adbcf10c
bytes             = 104683
CR bytes          = 0
bash -n rc        = 0  (GNU bash 5.3.9)
subject blob      = 3b9c78bbaffa3b296de3009ceb3779141909a724
```

The current subject, `SELF_QA_RP6.md`, `RP6_REPAIR_R9_REPORT.md`, and the
preregistration draft are byte-identical to their blobs at commit `9bc25721`.
The predecessors were materialised with `git cat-file blob`, not checkout, and
then removed:

```text
ab53a012 / blob a55defb4fa07ca856d0d5c77525cfc205898a842
sha256=e7ca9ff1e6d44b838b6d8bfddbb24bb68e2642b9f65abfc941f9482e465a0839 bytes=103808 CR=0 bash_n=0

d9d7420f / blob d663445bed0ddd22855ed0b73cee7a41b4555bf0
sha256=fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd bytes=103071 CR=0 bash_n=0
```

Independent enumeration command:

```bash
grep -Pc 'p0_(?:stop|fail)\x20\x22' MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh
```

Observed output `158`, rc `0`: 150 literal `p0_stop` calls and 8 literal
`p0_fail` calls. Line 159 is a further direct `P0_STOP` emitter in the ERR trap,
so the machine-result inventory is **159**, not the repair report's claimed 174.

Legend: **C** = the P0 prefix, reason, fields and constrained values match a form
declared in preregistration section 8.1; **D** = the reason is declared for P0,
but the site can emit an undeclared field/value shape; **U** = no matching
P0-prefixed reason form is declared. All line numbers in a grouped row are
individually enumerated sites; no row is a sample.

| Lines | Sites | Output | Reason | Contract comparison |
|---|---:|---|---|---|
| 159 | 1 | `P0_STOP` | `unadjudicated_command_status` | **U** — direct ERR-trap emitter; absent from the draft |
| 399, 401 | 2 | `P0_STOP` | `rp0_lib_not_sourced` | **U** |
| 403, 404, 405, 406 | 4 | `P0_STOP` | `rp0_bootstrap_not_run` | **U** |
| 411, 413 | 2 | `P0_STOP` | `evidence_identifier_refused` | **U** |
| 426, 459, 493 | 3 | `P0_STOP` | `input_missing` | **U** |
| 428, 476, 497 | 3 | `P0_STOP` | `input_charset` | **U** |
| 431, 486 | 2 | `P0_STOP` | `input_range` | **U** |
| 501 | 1 | `P0_STOP` | `input_not_absolute` | **U** |
| 505 | 1 | `P0_STOP` | `input_path_traversal` | **U** |
| 508 | 1 | `P0_STOP` | `input_not_canonical_spelling` | **U** |
| 514 | 1 | `P0_STOP` | `input_not_candidate_bound` | **U** |
| 570 | 1 | `P0_STOP` | `input_pin_malformed` | **U** |
| 579, 614 | 2 | `P0_STOP` | `input_pin_unknown_tool` | **C** |
| 582 | 1 | `P0_STOP` | `prereg_input_malformed` | **U** |
| 586 | 1 | `P0_STOP` | `input_pin_not_absolute` | **U** |
| 590, 604 | 2 | `P0_STOP` | `input_pin_charset` | **U** |
| 616 | 1 | `P0_STOP` | `input_pin_freeze_unfilled` | **D** — the draft declares only `tool=python3 name=P0_FIXED_TRUSTED_PYTHON`; this generic site can emit all twelve tool/constant pairs |
| 619 | 1 | `P0_STOP` | `input_pin_not_frozen_trusted_python` | **C** |
| 623 | 1 | `P0_STOP` | `input_pin_not_frozen_path` | **C** |
| 635, 668 | 2 | `P0_STOP` | `input_pin_omitted` | **C** syntactically; line 668's predicate does not establish omission (finding 4) |
| 639 | 1 | `P0_STOP` | `input_pin_count_unexpected` | **D** — undeclared `detail=exactly_one_frozen_pin_per_preregistered_tool` |
| 676, 678, 680, 682, 684, 694, 697, 700, 709, 712, 714, 718, 720, 722, 724, 726, 728, 730, 732, 734, 736, 1315, 1317, 1320, 1324, 1327, 1343, 1347, 1363, 1381, 1384, 1389, 1393, 1395 | 34 | `P0_STOP` | `execution_domain_unattested` | **D** — draft form is only `field=<f>`; every site adds `detail`, and some add `rc`, `diagnostic_shape`, `subject`, `device`, or `root_device` |
| 776, 887, 889, 891, 893, 895, 897, 899, 904 | 9 | `P0_STOP` | `missing_tool` | **D** — declared absence form has `tool` only; sites add `rc/detail` or `detail`, and the draft names only a subset of dynamic tool values |
| 781, 786, 906 | 3 | `P0_STOP` | `tool_resolution_unparsable` | **U** |
| 804, 810 | 2 | `P0_STOP` | `tool_pin_uncanonicalizable` | **U** |
| 814, 822 | 2 | `P0_STOP` | `tool_pin_mismatch` | **C** |
| 828 | 1 | `P0_STOP` | `tool_pin_unpinned` | **D** — undeclared `detail=every_tool_requires_a_frozen_pin` |
| 838 | 1 | `P0_STOP` | `tool_not_evaluable` | **C** |
| 852 | 1 | `P0_STOP` | `metadata_unreadable` | **U** — the same token appears only under the draft's `B1_STOP` grammar, not P0 |
| 857 | 1 | `P0_STOP` | `metadata_multiline` | **U** |
| 862, 869, 872, 876, 878 | 5 | `P0_STOP` | `metadata_unparsable` | **U** |
| 934, 941, 948 | 3 | `P0_STOP` | `evidence_binding_unprobeable` | **U** |
| 951, 953, 956, 958 | 4 | `P0_STOP` | `evidence_binding_unparsable` | **U** |
| 962 | 1 | `P0_STOP` | `evidence_leaf_not_bound` | **U** |
| 989, 997, 1003, 1038, 1043, 1048 | 6 | `P0_STOP` | `group_query_not_evaluable` | **C** |
| 991 | 1 | `P0_STOP` | `identity_probe_failed` | **U** |
| 999 | 1 | `P0_STOP` | `identity_probe_multiline` | **U** |
| 1005 | 1 | `P0_STOP` | `identity_probe_empty` | **U** |
| 1014, 1018 | 2 | `P0_STOP` | `identity_probe_unparsable` | **U** |
| 1062 | 1 | `P0_STOP` | `capability_wider_than_ledger` | **D** — undeclared `caller_gids` field |
| 1258, 1261 | 2 | `P0_STOP` | `identity_unexpected` | **C** |
| 1282 | 1 | `P0_STOP` | `identity_unexpected` | **D** — the draft fixes the service identity at `999:988`, but the site prints operator-supplied `P0_STATE_UID:P0_STATE_GID`, which the block constrains only to positive decimals |
| 1267, 1270, 1291 | 3 | `P0_STOP` | `identity_unresolvable` | **C** |
| 1288 | 1 | `P0_STOP` | `state_account_resolution_unexpected` | **D** — same unfrozen dynamic expected identity instead of the declared `999:988` |
| 1330, 1398 | 2 | `P0_STOP` | `execution_domain_mismatch` | **C** |
| 1489 | 1 | `P0_STOP` | `system_manager_unreachable` | **D/mixed** — the extended fields are declared for rc 124 only, but this site emits them for every nonzero status |
| 1494, 1499 | 2 | `P0_STOP` | `system_manager_unreachable` | **D** — undeclared `text` field on rc-0 shape errors |
| 1503 | 1 | `P0_STOP` | `system_manager_unreachable` | **C** |
| 1563, 1598 | 2 | `P0_STOP` | `path_probe_empty` | **U** |
| 1568, 1605 | 2 | `P0_STOP` | `path_probe_multiline` | **U** |
| 1573 | 1 | `P0_STOP` | `path_probe_nonprintable` | **U** |
| 1584 | 1 | `P0_STOP` | `link_target_probe_empty` | **U** |
| 1595 | 1 | `P0_STOP` | `link_target_probe_error` | **U** |
| 1612 | 1 | `P0_STOP` | `path_probe_ambiguous` | **U** |
| 1618 | 1 | `P0_STOP` | `path_probe_denied` | **U** |
| 1620 | 1 | `P0_STOP` | `path_probe_unclassified` | **U** |
| 1631 | 1 | `P0_FAIL` | `venv_root_absent` | **U** — draft has no P0 FAIL form |
| 1633 | 1 | `P0_FAIL` | `venv_root_is_symlink` | **U** |
| 1634 | 1 | `P0_FAIL` | `venv_root_kind_unexpected` | **U** |
| 1639 | 1 | `P0_STOP` | `venv_root_canonicalization_failed` | **U** |
| 1647, 1652, 1657, 1662 | 4 | `P0_STOP` | `venv_root_canonicalization_unparsable` | **U** |
| 1666 | 1 | `P0_FAIL` | `venv_root_not_literal_canonical` | **U** |
| 1681 | 1 | `P0_FAIL` | `interpreter_target_kind_unexpected` | **U** |
| 1683 | 1 | `P0_FAIL` | `interpreter_absent` | **U** — draft uses this reason only as `B1_FAIL`, not `P0_FAIL` |
| 1685 | 1 | `P0_FAIL` | `interpreter_symlink_dangling` | **U** |
| 1687 | 1 | `P0_FAIL` | `interpreter_kind_unexpected` | **U** |
| 1695 | 1 | `P0_STOP` | `interpreter_not_executable` | **U** — draft uses this reason only as `B1_STOP`, not `P0_STOP` |
| 1737 | 1 | `P0_STOP` | `interpreter_exec_denied` | **U** |
| 1738, 1739 | 2 | `P0_STOP` | `interpreter_exec_failed` | **U** |
| 1745 | 1 | `P0_STOP` | `interpreter_probe_multiline` | **U** |
| 1754 | 1 | `P0_STOP` | `interpreter_startup_not_isolated` | **U** |
| 1759, 1763, 1765, 1766 | 4 | `P0_STOP` | `interpreter_probe_unparsable` | **U** |

Reconciliation: **159 machine emitters = 23 C + 52 D + 84 U** (83 literal
wrapper sites plus the direct ERR-trap emitter). The repair report's family table
therefore does not constitute an exhaustive grammar sweep.

## Findings

### 1. HIGH — `R9_GRAMMAR` is not executable closure evidence

The documented RED command does not run the harness. With a filename after the
options, Bash treats that filename as the script to execute; piped stdin is not
the script. I materialised the exact round-8 blob (the relic-restored mutant) and
ran the documented command verbatim from `WPI_BLOCKS_DRAFT`:

```bash
mutant=$(mktemp)
git -C ../../.. cat-file blob a55defb4fa07ca856d0d5c77525cfc205898a842 > "$mutant"
sed -n '/R9_GRAMMAR_HARNESS_BEGIN/,/R9_GRAMMAR_HARNESS_END/p' SELF_QA_RP6.md | bash --noprofile --norc "$mutant"
rc=$?
```

Observed rc and output:

```text
P0_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP6-P0 stage=p0
P0_SECTION prerequisites
P0_STOP reason=rp0_lib_not_sourced predicate=rp0_require_safe_component detail=not_a_shell_function
DOCUMENTED_RED_RC=3
```

There is no `R9_GRAMMAR_SUMMARY`; the command ran the mutant RP6 block.

Adding the missing stdin-script selector makes the harness run, but exposes the
second defect: the harness prints FAIL and exits 0 because its last command is an
unconditional successful `printf`.

```bash
sed -n '/^# R9_GRAMMAR_HARNESS_BEGIN$/,/^# R9_GRAMMAR_HARNESS_END$/p' SELF_QA_RP6.md \
  | bash --noprofile --norc -s -- "$mutant"
rc=${PIPESTATUS[1]}
```

Observed:

```text
ASSERT_UNMET freeze_emit_site_count=1 observed=2
ASSERT_MET freeze_site_detail=declared observed=1
ASSERT_MET freeze_site_name=generic_P0_FROZEN_CONST_NAME
ASSERT_UNMET relic_detail_count=0 observed=1
ASSERT_UNMET post_loop_backstop=declared_input_pin_omitted MISSING
R9_GRAMMAR_SUMMARY cases=5 pass=2 fail=3 result=FAIL
CORRECTED_RED_HARNESS_RC=0
```

This violates the kickoff's own-status contract and D026. Required repair: use a
verbatim invocation that actually executes the harness (`-s --` or a separately
materialised harness), and explicitly exit nonzero when `R9_FAIL != 0`. Re-run
real GREEN and RED and record both commands, outputs and statuses.

The carried-fence check found no reduction in the eight older fences. Exact
marker lines are unique (one BEGIN and one END each). Six fences are identical
from round 7 through round 9. Only `RP6_FULLBLOCK_D026` and `RP6_R4_D026` changed
in round 8; their changes add missing frozen-literal fixtures, build-completeness
guards, the required getent pin, and the 12-pin expectation while retaining the
exact rc/line assertions. Both are byte-identical between rounds 8 and 9. The
carried-fence regression is confined to the new R9 evidence and its incomplete
grammar predicate.

### 2. HIGH — the declared grammar and the executable grammar are not closed

The table above is the independent sweep: only 23 of 159 emitters match a P0 form
declared by the draft. The largest gaps are not cosmetic:

- The draft declares zero `P0_FAIL` forms, while the block has eight.
- Fifty literal reason tokens are absent from the P0 grammar; reasons that
  appear only under `B1_*` or `B3_*` cannot be borrowed by changing the prefix.
- Declared reasons add fields the exact form does not permit, including all 34
  `execution_domain_unattested` sites, all 9 `missing_tool` sites, and the
  `caller_gids`, count-detail, unpinned-detail, and manager `text` variants.
- The direct ERR-trap `unadjudicated_command_status` reason was omitted by the
  report's `p0_stop`/`p0_fail` grep and is undeclared.
- The report states 174 call sites, but both round-7 and round-8 predecessors and
  the round-9 subject contain 158 literal wrapper sites.

The central round-9 claim is itself false. The draft's only occurrence is:

```text
P0_STOP reason=input_pin_freeze_unfilled tool=python3 name=P0_FIXED_TRUSTED_PYTHON detail=deploy_channel_value_never_derived_here
```

Line 616 is generic over all twelve tools. A bounded pre-input fixture, which
stops before any external tool or host observation, proves the non-python form is
live:

```bash
RUNID=R9GRAMMARFIXTURE EV_STAGE_ID=p0 EV_DIR=/fixture/evidence \
EV_LOG=/fixture/evidence/p0.log P0_EXPECT_UID=1000 P0_STATE_UID=999 \
P0_STATE_GID=988 P0_FORBIDDEN_GIDS='0 988' \
P0_VENV_ROOT=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b \
P0_TOOL_PINS='stat=/usr/bin/stat' bash --noprofile --norc -c '
  rp0_require_safe_component(){ return 0; }
  rp0_allocate_evidence_dir(){ return 0; }
  . MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh
'
```

Observed rc and terminal output:

```text
P0_STOP reason=input_pin_freeze_unfilled tool=stat name=P0_FIXED_STAT detail=deploy_channel_value_never_derived_here
OBSERVED_RC=3
```

The R9 harness passes this defect because it asserts the generic
`name=$P0_FROZEN_CONST_NAME` source text and calls the detail "declared" without
checking the draft's fixed `tool=python3/name=P0_FIXED_TRUSTED_PYTHON` form.

Required repair: define an exhaustive P0 result grammar in the preregistration
and make every emitter conform to it, including prefix, exact fields, constrained
values and every `detail` token. Derive the grammar fence from that declaration,
not from four hand-picked source substrings. The draft must either declare a
generic freeze-unfilled form for all twelve tool/constant pairs or the block must
emit only the currently declared python3 form; this cannot be closed by calling
the generic variable name a declaration.

### 3. HIGH — malformed followed-target output reaches rc 1

`p0_probe_kind` now validates the first rc-0 `%F` response before semantics, but
does not apply the same shape gate to the second `%F` response used after an
allowed interpreter symlink is followed. At lines 1577-1587 it sanitises a
multi-line or non-printable response and maps it to `P0_FKIND=other`; line 1681
then emits a host-state FAIL. This is an unparseable producer result and must be
STOP.

Executed bounded fixture from the repository root: a local stat shim returned `symbolic link` for the
leaf and `regular file\nwarning_from_follow_probe\n` at rc 0 for the followed
target. The real round-9 functions were extracted by their function anchors and
called through `p0_assert_interpreter_executable`.

```bash
block='MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh'
q=$(mktemp -d)
printf '%s\n' '#!/bin/sh' \
  'if [ "$1" = "-c" ] && [ "$2" = "%F" ]; then printf "symbolic link"; exit 0; fi' \
  'if [ "$1" = "-L" ] && [ "$2" = "-c" ] && [ "$3" = "%F" ]; then printf "regular file\nwarning_from_follow_probe\n"; exit 0; fi' \
  'printf "regular file|755|0:0"; exit 0' > "$q/stat"
chmod +x "$q/stat"
{
  sed -n '/^p0_stop() {/p' "$block"
  sed -n '/^p0_fail() {/p' "$block"
  sed -n '/^p0_sanitize()/,/^}/p' "$block"
  sed -n '/^p0_count_substr()/,/^}/p' "$block"
  sed -n '/^p0_classify_stat_shape()/,/^}/p' "$block"
  sed -n '/^p0_probe_kind()/,/^}/p' "$block"
  sed -n '/^p0_assert_interpreter_executable()/,/^}/p' "$block"
} > "$q/arm.sh"
P0_STAT="$q/stat" P0_EACCES_TEXT='Permission denied' \
P0_ENOENT_TEXT='No such file or directory' bash --noprofile --norc -c \
  '. "$1"; p0_assert_interpreter_executable /fixture/python' _ "$q/arm.sh"
```

Observed:

```text
FIXTURE_SHIM=/tmp/tmp.ECz2wzgKjF/stat
P0_FAIL reason=interpreter_target_kind_unexpected kind=other path=/fixture/python expected=regular
OBSERVED_RC=1
```

Required repair: adjudicate the followed-target rc-0 response as empty,
multiline, non-printable, or a recognised complete kind before assigning
`P0_FKIND`. Add RED/GREEN cases for at least multiline and non-printable target
responses; GREEN must emit a declared P0 STOP and return 3.

### 4. MEDIUM — round-9b's post-loop relabelling is convenient, not established

The draft does clearly distinguish the two input conditions:
`input_pin_omitted` means a pin entry is absent; `input_pin_freeze_unfilled`
means a supplied frozen literal is still the placeholder. That distinction is
sound.

Line 668, however, does not test omission. It tests only
`P0_TRUSTED_PYTHON_BOUND != yes`:

```powershell
rg -n -F -e 'P0_TRUSTED_PYTHON_BOUND' -e 'input_pin_omitted tool=python3' `
  MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh
```

Observed rc `0`:

```text
531:P0_TRUSTED_PYTHON_BOUND=no
620:        P0_TRUSTED_PYTHON_BOUND=yes
667:[ "$P0_TRUSTED_PYTHON_BOUND" = yes ] \
668:    || p0_stop "input_pin_omitted tool=python3 detail=every_preregistered_tool_requires_one_frozen_pin"
```

Under the current control flow every false case is already consumed by the
omission loop, the freeze-unfilled gate, or the disagreement gate, so line 668
is unreachable. Unreachability does not turn its broader invariant predicate
into an observation of omission, and a static grep cannot be D026 evidence for
an unreachable branch.

Required repair: remove the dead backstop, or declare it as an internal-binding
invariant reason whose predicate it actually establishes and provide an
executable falsification that reaches it. Do not retain an unreachable invariant
branch under an input-deficiency label and call the condition adjudicated.

## Out-of-scope bands

Namespace correctness, privilege-domain correctness, and filesystem-escape
behaviour were out of scope and no fixtures were constructed for them. The
`<PIN-AT-FREEZE>` values and section 8.2 rows 1-9 remain freeze-gate/owner items,
not findings here. No host was contacted, no network command was run, and no
commit or source edit was made. Only this audit report was written.
