# RP7 cap-override - Claude T0 flagship audit

**Verdict: REQUEST_CHANGES** (1 REQUIRED, 3 optional nits)

Auditor: Claude, fresh independent non-implementer session, no `--resume` /
`--continue`, no sub-delegation. Exact model `claude-opus-5`; effort `xhigh` per
the dispatch contract of
`KICKOFF_CLAUDE_RP7_CAP_OVERRIDE_T0_AUDIT_2026-08-13.md` (the effort setting is
supplied by the launcher and is not introspectable from inside the session; I
state it as contracted, not as measured). Tier T0. Date 2026-08-15.

Worktree: `C:\R7AC`, detached at prompt commit
`d4e90cb05bfbe227d17ce6264f0d3c19d3b5337f`. Frozen subject commit
`2d0f24d0965c4ba7e7942dddac4fcac3bbb3240b`.

I did not read `RP7_CAP_OVERRIDE_CODEX_T0_AUDIT_2026-08-13.md` (it does not exist
in this tree) or any same-round Codex verdict. This verdict alone cannot accept
T0; both mandatory flagship verdicts are required.

The published fence reproduces exactly, both cap-override REQUIRED findings are
genuinely closed, and the row-9 work is sound. Acceptance is withheld for one
reason: the row-6 line grammar still models only `\n` as a line terminator, while
systemd 259 also terminates a unit-file line at a bare `CR`. I executed two
fragments that systemd 259 parses as having a **real `[Install]` section** and
that the frozen block reports as `install_section=absent` at rc 0 - a **false
PASS on the row-6 safety predicate**, driven through the production caller. One
of those two cases was handled correctly by the round-4 bytes `90cbeac4` and is
therefore a surviving regression of exactly the class this cap-override round was
authorized to close.

---

## 1. Identity - re-derived from Git object bytes, all four match the kickoff

`C:\R7AC` is a Windows checkout with `core.autocrlf=true` and `.gitattributes`
`* text=auto`, so its working-tree copies carry CRLF. Those transport-converted
bytes are **not** the frozen subject and are not reported as drift. Every
identity below was re-derived from the Git object database by walking
`commit -> tree -> path -> blob`, and materialized into a run-owned WSL scratch
tree preserving the repository-relative layout.

```text
$ git cat-file -t 2d0f24d0965c4ba7e7942dddac4fcac3bbb3240b        -> commit
$ git rev-parse 2d0f24d0...:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/<file>
RP7-WPI-RO.sh                     -> 6ac7c7a2d0dea7db16c4c2c3679a52c8deb926fb
SELF_QA_RP7.md                    -> 17583824d17aa12e46c868dd445c0a61c2bd4961
STATUS_RP7.md                     -> b67e6e4d080fa4747919ec92d9fe65350baf5a67
RP7_ROWS_1_9_REPORT_2026-08-13.md -> d829474c998073f2305cbbf0e38c07ebed59ab36

$ git cat-file blob <blob> > <scratch>/repo/.../<file>   (4x)
RP7-WPI-RO.sh                     bytes=132886 sha256=a4af307c34cbc6092676b0838e17090dcadeb1116703773f1dbd42749670b243 cr_bytes=0
SELF_QA_RP7.md                    bytes=504144 sha256=72aab351fc9f0d5881bbac995985338dc983777978b1787b4b5abe3bf0fda58f cr_bytes=0
STATUS_RP7.md                     bytes=12213  sha256=df44704c4099459d2860fd6ddbfc0b659b981eb4ecbe06a7f1ef89b99499ad65 cr_bytes=0
RP7_ROWS_1_9_REPORT_2026-08-13.md bytes=41843  sha256=4e5d38d422ab836aca3e2421f0430b4cdb72680c5d34de86e33d14b2c0fd7cde cr_bytes=0
```

All four equal the kickoff table exactly. The same four blobs are identical at
prompt commit `d4e90cb0`. For contrast, the CRLF working-tree copies in `C:\R7AC`
are 135095 / 510015 / 12408 / 42675 bytes with 2209 / 5871 / 195 / 832 CR bytes -
transport only.

Pre-fix subject identities used by the fence were re-derived the same way and
match its assertions: `90cbeac4` = 127491 B /
`5b00207aff17a9a9f29e056b9f93fb46b2cf640376659bf75b9f33b9b9b3dbe3`; `8ec89675` =
127655 B / `beacf85b628e419d911416dc1ee51a382f742d90cbabe29602e60c4f52d809a8`.

## 2. Mandatory execution - the published rows-1-9 fence

Environment: WSL Ubuntu, kernel `6.18.33.2-microsoft-standard-WSL2`,
`systemd 259 (259.5-0ubuntu3)`, `GNU bash 5.3.9(1)`, `Python 3.14.4`, root.
Strictly sequential; one fence run; no parallel agent.

**Transport accommodation, disclosed exactly.** The fence body hard-codes
`REPO=/mnt/c/LAB/Tradingview_LAB_CLEAN`, i.e. a different working tree at a
different HEAD, which is not the frozen subject. I therefore retargeted `REPO` to
my run-owned materialization of the frozen blobs and changed nothing else. The
full diff between the verbatim extraction and what I executed:

```text
FENCE_VERBATIM   lines=690 bytes=72101 sha256=180a5122a4b501aa2970772856fd5cdd3ac94347fe1a93129b8ac75a5ca01632
FENCE_RETARGETED lines=690 bytes=72106 sha256=46a35fb277efc4e55a7c645aff83cc6792bddd81de521dd8b87f28e040faa5d3

@@ -2,7 +2,7 @@
 set -Eeuo pipefail
 set -f
 export LC_ALL=C
-REPO=/mnt/c/LAB/Tradingview_LAB_CLEAN
+REPO=/var/tmp/r7ac-claude-t0-2hMuKFPj/repo
 BLOCK="$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh"
 EXPECTED_BYTES=132886
```

The fence also runs `git -C "$REPO" cat-file blob 90cbeac4:...` and `8ec89675:...`
for its pre-fix subjects, so the scratch tree was made a run-owned Git repository
(`git init` inside the scratch only) whose `objects/info/alternates` points
read-only at the audited object store. No object was written and nothing in the
audited repository was mutated. Both blobs resolved to the exact declared
identities.

Result:

```text
NO_PREEXISTING_RP7_ROOT
FENCE_RC=0
FENCE_ELAPSED_S=124.226681992
FENCE_STDOUT_LINES=156
FENCE_STDERR_BYTES=0
HARNESS_CASE_FAIL=0  HARNESS_ABORT=0  HARNESS_BLOCK_ID_MISMATCH=0  HARNESS_CASE_STDERR=0
HARNESS_SUBJECT_FAIL=0  HARNESS_ORACLE_FAIL=0  HARNESS_COUNT_MISMATCH=0
HARNESS_EXTRACT_MISMATCH=0  HARNESS_EXTRACT_MISSING=0
D026 row lines=81   D026_SUBJECT=48   ORACLE=9   D026_CONTROL=2

HARNESS_BLOCK_ID stage=before bytes=132886 sha256=a4af307c...70b243 cr_bytes=0 bash_n=0
HARNESS_BLOCK_ID stage=after  bytes=132886 sha256=a4af307c...70b243 cr_bytes=0 bash_n=0
D026_SUMMARY rows=1-9 red_green_pairs=36 controls=9 multi_subject_red=11 multi_subject_green=10 multi_subject_controls=27 subjects=5 systemd_oracle_fixtures=9 result=PASS instrument=RP7-WPI-RO.sh extracted_block_functions=yes block_logic_reimplemented=no
```

Identity unchanged before and after; no harness abort, no capture collision, no
ERR-trap contamination, zero stderr. The run-owned `mktemp -d` root was
`/tmp/rp7_rows_1_9_rebuild_evidence.n3h3YsOh`; no `/tmp/rp7*` existed before the
run and none remained after it.

**Transcript comparison.** Against the transcript embedded at
`SELF_QA_RP7.md:793-948`, after substituting each run's own
`HARNESS_SCRATCH_ROOT` path as the document prescribes:

```text
published root /tmp/rp7_rows_1_9_rebuild_evidence.ZaS9b08X
my run root    /tmp/rp7_rows_1_9_rebuild_evidence.n3h3YsOh
differing lines after normalisation: 1 of 156
-HARNESS_ATTESTED_MOUNTINFO sha256=3a9486e6fc655a918097250412fa994c4e87233e21662e03b7e46533c1798444 ...
+HARNESS_ATTESTED_MOUNTINFO sha256=f19689b9e479cc06fee2cbb7d0cc3f48f9e128dc04dbff2124c9b73d4ddc4205 ...
```

Exactly the shape the package predicts at `SELF_QA_RP7.md:1002-1006`: identical on
155 of 156 lines, the single exception being the mount-projection digest, whose
per-run variation the document explains mechanically (the projection hashes a
`kind=point path=$WPI_UNIT_FRAGMENT` record that now lives under a run-owned
root). That explanation is correct and the field carries no row predicate.

All nine `ORACLE` arms executed live against `systemd-analyze verify`
(`systemd 259 (259.5-0ubuntu3)`) and reproduced their recorded sections and
terminator censuses exactly, controls first.

## 3. REQUIRED (new) - row 6 models only `\n` as a line terminator; two executed false PASSes

### 3.1 The systemd fact, executed

`systemd 259` terminates a unit-file line at a bare `CR`, not only at `LF`/`CRLF`.
Executed discriminator - a key unknown in every section (`ZZZBogus`) placed
immediately after `[Install]`, so systemd names the section it landed in:

```text
fixture: [Unit] LF Description=x CR ZZZBogus=1 LF [Service] LF ExecStart=/bin/true LF
systemd: probe.service:3: Unknown key 'ZZZBogus' in section [Unit], ignoring.
```

If `CR` were line content, `ZZZBogus=1` would be part of the `Description` value
and no diagnostic could fire. It fired, and at line 3 of a file with two `LF`
lines before it - systemd counted the `CR` as a line break.

### 3.2 The block's model

`RP7-WPI-RO.sh:719-720` (frozen 132886 bytes):

```python
for physical in text.split("\n"):
 line=physical.rstrip("\r").lstrip(WS)
```

`split("\n")` recognises only `LF`. `rstrip("\r")` then removes an arbitrary
**run** of trailing CRs, which is also broader than the block's own rule of
record at `RP7-WPI-RO.sh:660-666` - "systemd normalises the LINE TERMINATOR - and
only the terminator".

### 3.3 Two false PASSes, driven through the production caller

Both were driven through the real
`wpi_assert_fragment_has_no_install_section`, extracted from the frozen bytes with
the fence's own `sed '$d'` method and executed by the fence's own unmodified
`subject_child.sh` body (sha256
`0cdd5f69140db564a83ceb1c2b67578e64b257ca8507318caa365e77fa96b9ea`), one process
and one scratch namespace per (subject, arm). Child stderr was empty on every
arm, so no harness error is being read as a parser disposition.

`systemd-analyze verify` was run on the **same fixture bytes**; here `WantedBy` is
the discriminator, because it is valid in `[Install]` and unknown in `[Unit]`:

| arm | fixture (value line) | systemd 259 | truth |
|---|---|---|---|
| `bare_cr_install` | `Description=x` + **CR** + `[Install]` | *(silence: `WantedBy` accepted)* | `[Install]` is a **real section** |
| `double_cr` | `Description=continued \` + **CR CR** + LF, then `[Install]` | *(silence)* | `[Install]` is a **real section** |
| `single_cr` (control) | `Description=continued \` + **CR** + LF, then `[Install]` | `:4: Unknown key 'WantedBy' in section [Unit], ignoring.` | swallowed as continuation text |

Block dispositions on those exact fixtures:

```text
DRIVE subject=round4   arm=bare_cr_install  rc=1 disp=present      child_stderr=0
DRIVE subject=current  arm=bare_cr_install  rc=0 disp=absent       child_stderr=0
DRIVE subject=frozen   arm=bare_cr_install  rc=0 disp=absent       child_stderr=0   <- FALSE PASS

DRIVE subject=round4   arm=double_cr        rc=0 disp=absent       child_stderr=0
DRIVE subject=current  arm=double_cr        rc=1 disp=present      child_stderr=0
DRIVE subject=frozen   arm=double_cr        rc=0 disp=absent       child_stderr=0   <- FALSE PASS

DRIVE subject=frozen   arm=single_cr        rc=0 disp=absent       child_stderr=0   (correct)
DRIVE subject=frozen   arm=clean            rc=0 disp=absent       child_stderr=0   (correct)
```

The accepting line emitted by the frozen bytes for `bare_cr_install` is:

```text
B2_fragment_install_section path=<ns>/unit/mtc-bridge-first-start.service install_section=absent parser=systemd_unit_line_grammar binding=component_and_mount_window_closed
```

Row 6 exists to prove the deployed fragment has no `[Install]` section. Both
arms above are fragments systemd loads **with** an `[Install]` section while the
block reports `absent` at rc 0. That is the false-PASS direction the package
itself names as "the more dangerous of the two errors"
(`SELF_QA_RP7.md:1086-1090`).

### 3.4 Why this is a surviving regression, not a new scope

The mechanism is visible across the three committed byte sets:

```text
round4  90cbeac4 (127491): for physical in text.splitlines():           line=physical.rstrip("\r")
current 8ec89675 (127655): for physical in text.split("\n"):            line=physical.lstrip(WS)
frozen           (132886): for physical in text.split("\n"):            line=physical.rstrip("\r").lstrip(WS)
```

Round 4's `splitlines()` splits on a bare `CR`, which is why `round4` answers
`bare_cr_install` correctly. The post-round-4 repair replaced it with
`split("\n")` and dropped `rstrip("\r")`. This cap-override round restored only
the `rstrip("\r")` half. The terminator half was never restored, so the
`bare_cr_install` regression against `90cbeac4` survives untouched - the same
defect class, in the same predicate, as the REQUIRED-1 this round was authorized
to close.

### 3.5 Required repair, with an executed non-weakening demonstration

Make the line grammar model systemd's terminator set. One executed candidate -
two lines in the embedded parser, `re` is already imported:

```text
- for physical in text.split("\n"):
-  line=physical.rstrip("\r").lstrip(WS)
+ for physical in re.split("\r\n|\r|\n",text):
+  line=physical.lstrip(WS)
```

(With a correct terminator split no trailing `CR` survives, so the `rstrip("\r")`
- and its CR-run over-reach - becomes unnecessary rather than merely narrowed.
A plain revert to `str.splitlines()` is **not** equivalent: it also splits on
`\v`, `\f`, `\x1c`-`\x1e`, `\x85`, `\u2028`, `\u2029`, which systemd treats as
content.)

Comparative sweep, frozen parser vs candidate repair vs systemd 259 on identical
fixture bytes:

```text
bare_cr_install       systemd=present  frozen=absent   DIVERGE | fixterm=present  OK
double_cr             systemd=present  frozen=absent   DIVERGE | fixterm=present  OK
single_cr             systemd=absent   frozen=absent   OK      | fixterm=absent   OK
crlf_file_bs          systemd=absent   frozen=absent   OK      | fixterm=absent   OK
trailing_space        systemd=present  frozen=present  OK      | fixterm=present  OK
trailing_space_crlf   systemd=present  frozen=present  OK      | fixterm=present  OK
even_backslash        systemd=present  frozen=present  OK      | fixterm=present  OK
odd_three             systemd=absent   frozen=absent   OK      | fixterm=absent   OK
comment_bridge        systemd=absent   frozen=absent   OK      | fixterm=absent   OK
blank_terminates      systemd=present  frozen=present  OK      | fixterm=present  OK
comment_then_blank    systemd=present  frozen=present  OK      | fixterm=present  OK
bare_backslash        systemd=present  frozen=present  OK      | fixterm=present  OK
real_install          systemd=present  frozen=present  OK      | fixterm=present  OK
crlf_real_install     systemd=present  frozen=present  OK      | fixterm=present  OK
```

The trailing-space-after-backslash boundary - the control REQUIRED-1 was
explicitly told not to regress - is preserved in both LF and CRLF form. Two
sweep rows are discriminator artefacts, not divergences: `lower_install`
(systemd says `Unknown section 'install'`, so `absent` is correct) and
`crlf_no_install` (the fixture contains no `[Install]` and no `ZZZBogus`).

D026 for this finding is satisfied in both directions: RED against the frozen
bytes, GREEN against the candidate repair, with the commands and real outputs
above, plus the `single_cr` / `trailing_space` / `real_install` no-weakening
controls.

**Pattern classification:** 5 (grammar completeness - the terminator set is not
modelled) and 12 (an unmodelled member disappears instead of stopping), producing
1 (an accepting disposition where the truthful one is FAIL), with 9 as the overlay
(`RP7-WPI-RO.sh:660-666` says "the terminator, and only the terminator"; the code
strips a CR run and splits on `\n` only).

**Why the package's own evidence did not catch it:** the fence's nine ORACLE arms
vary what precedes the terminator (backslash, spaces, even count) and whether the
file is CRLF, but every arm uses `LF` or `CRLF` as the terminator itself. No arm
varies the terminator identity, and no arm has more than one CR. The fence
therefore PASSes over the gap - the `fixture_terms` census measures the same
unmodelled dimension it is blind to.

## 4. The two cap-override REQUIRED findings - both genuinely closed

**REQUIRED-1 (CR handling) - closed for the case it names.** `crlf_install`
(`\` + CRLF) is now `absent` at rc 0 on the frozen bytes and `present` at rc 1 on
`current` and on `mut_nocr`, executed in-fence against the real pre-fix blob. The
rule is executed against systemd rather than asserted, and my own independent
oracle reproduced all six rule arms and all three controls. The finding in §3 is a
*different* half of the same normalisation, not a re-opening of this one.

**REQUIRED-2 (two-subject D026) - closed properly.** The fence materialises the
actual round-4 blob with `git cat-file blob 90cbeac4:...` and the current blob
with `8ec89675:...`, asserts each subject's bytes/sha256/`bash -n` before use,
and runs every multi-subject arm in a **separate process**
(`bash --noprofile --norc "$ROOT/subject_child.sh"`) with a scratch namespace
unique to (subject, arm). Sourcing both subjects into one shell does not occur.
Per-pair assertions are heterogeneous and exact - `absent` rc 0, `present` rc 1,
`grammar` rc 3, `b4_ok` rc 0, `b4_name` rc 3, `b4_dup` rc 1 - and the terminal
line is compared by **string equality**, not substring. Before an rc 3 is read as
a predicate STOP the fence requires empty child stderr, no non-empty captured
`ro.*.stderr` leaf, exactly one single-line parser record, and no `RP7_STOP`.
All 48 arms executed in my run with zero `HARNESS_SUBJECT_FAIL`.

**NIT-1 (trailing space) - adopted.** `trailing_space_after_backslash` exists as a
single-subject pair and as five multi-subject arms, with `mut_broad` supplying the
executed false-PASS RED.

## 5. Row 9 - mid-name quoting, quoted controls, duplicate policy

The kickoff's attack is refused, and I searched the adjacent grammar for a way
around it. Driving the frozen tokenizer (`RP7-WPI-RO.sh:773-843`, sha256 of the
extracted program `e658776f0eddc7e787852649487623bd96ac1c1ed9f1b2abfa1ae1df3ec95208`):

```text
midname_dq          MTC_BRIDGE"_START_MODE=credential_free_disarmed"    rc=3 PARSE environment_token_name_not_literal
midname_sq          MTC_BRIDGE'_START_MODE=credential_free_disarmed'    rc=3 PARSE environment_token_name_not_literal
midname_outer_pair  "MTC_BRIDGE""_START_MODE=credential_free_disarmed"  rc=3 PARSE environment_token_lexing_disagreement
midname_4quotes     "MTC_BRIDGE"_START"_MODE=credential_free_disarmed"  rc=3 PARSE environment_token_lexing_disagreement
name_esc_backslash  MTC_BRIDGE\_START_MODE=credential_free_disarmed     rc=3 PARSE environment_token_name_not_literal
empty_quotes_prefix ""MTC_BRIDGE_START_MODE=credential_free_disarmed    rc=3 PARSE environment_token_lexing_disagreement
name_quoted_only    "MTC_BRIDGE_START_MODE"=credential_free_disarmed    rc=3 PARSE environment_token_lexing_disagreement
unbalanced_quote    MTC_BRIDGE_START_MODE=credential_free_disarmed"     rc=3 PARSE ValueError
```

No quoting form I could construct normalises into the protected target name. The
guard is sound in mechanism: the name is taken from the posix lex, and the raw
(quote-preserving) token must literally start with `name=` after at most one
outer quote pair is removed, so any quote inside the name survives into the
comparison and fails it.

Fully quoted valid assignments remain accepted, as required:

```text
clean_single         MTC_BRIDGE_START_MODE=credential_free_disarmed     rc=0 OK ... tokens=1
whole_quoted         "MTC_BRIDGE_START_MODE=credential_free_disarmed"   rc=0 OK ... tokens=1
value_quoted         MTC_BRIDGE_START_MODE="credential_free_disarmed"   rc=0 OK ... tokens=1
single_quoted_whole  'MTC_BRIDGE_START_MODE=credential_free_disarmed'   rc=0 OK ... tokens=1
```

Duplicate-key policy is explicit and tested. The invariant is declared in the
code itself (`RP7-WPI-RO.sh:827-838`), in `STATUS_RP7.md:99-100` and in the report
at `:766-767`, each stating plainly that it is **stronger than systemd**, that
systemd applies last-assignment-wins and accepts a same-value duplicate, and that
this row refuses it as a FAIL rather than a STOP because the rendering was fully
evaluable. I confirmed the systemd half independently: `systemd-analyze verify`
emits no diagnostic for a same-value duplicate, and none for the mid-name quote
form either - so the block's strictness is a declared narrowing, correctly
labelled, not a systemd-fidelity claim. Executed:

```text
dup_same_value   rc=1 BAD count=2 observed_sha256=e9cc545dfb074abf6ff63c26a42b6139c12f714e3b20bb87ba31283ceba1b7de
dup_diff_value   rc=1 BAD count=2 observed_sha256=cc90d731cfd30bb1e7fff90f61e655bc644eb221e155c7151e627d6a99ed57b8
other_var_substring / absent / empty_string   rc=1 BAD count=0
token_no_assignment / bad_name_digit          rc=3 PARSE (fail-closed; systemd only warns and continues)
value_extra_word / empty_value / value_with_equals / dollar_expansion  rc=1 BAD count=1
```

No false PASS found in row 9. `MTC_BRIDGE_START_MODE=cred"ential"_free_disarmed`
is accepted with `value=credential_free_disarmed`, which is exactly the value
systemd resolves, so it is faithful rather than a splice.

## 6. D026 verification of every new test claimed in this round

| new test | RED subject | GREEN subject | I verified |
|---|---|---|---|
| row 6 `blank_no_bridge` | `round4` 127491, rc 0 `absent` | `repaired`, rc 1 `present` | yes - executed in my fence run |
| row 6 `comment_then_blank` | `round4`, rc 0 `absent` | `repaired`, rc 1 `present` | yes |
| row 6 `even_backslash_no_bridge` | `round4`, rc 0 `absent` | `repaired`, rc 1 `present` | yes |
| row 6 `bare_backslash_line` | `round4`, rc 0 `absent` | `repaired`, rc 1 `present` | yes |
| row 6 `eof_dangling_install` | `round4`, rc 3 `section_header_grammar` | `repaired`, rc 1 `present` | yes (heterogeneous polarity honoured) |
| row 6 `header_trailing_comment` | `round4`, rc 1 `present` | `repaired`, rc 3 `grammar` | yes (inverted polarity honoured) |
| row 6 `crlf_install` | `current` 127655 **and** `mut_nocr`, rc 1 `present` | `repaired`, rc 0 `absent` | yes - true pre-fix bytes |
| row 6 `trailing_space_after_backslash` | `mut_broad`, rc 0 `absent` | `repaired`, rc 1 `present` | yes - executed mutant, false-PASS direction |
| row 6 `crlf_no_install` / `crlf_real_install` | - | - | controls on all five subjects, executed |
| row 6 nine `ORACLE` arms | - | - | yes - live `systemd-analyze verify`, censuses matched, reproduced independently |
| row 9 `midname_quote` | `current`, rc 0 accepted | `repaired`, rc 3 `environment_token_name_not_literal` | yes - true pre-fix bytes |
| row 9 `whole_quoted` / `value_quoted` | - | - | controls on both subjects, executed |
| row 9 `same_value_duplicate` / `clean_single` | *(declared discrimination pair, not pre-fix)* | both subjects rc 1 / rc 0 | yes; the package labels it honestly (see NIT-3) |

Every arm the package labels RED against a named other byte set is executed
against that byte set, in its own process, in this run. The one place D026 is not
literally satisfied - the duplicate pair - the package itself says so in band.

## 7. Thirteen-pattern adjudication

| Pattern | Adjudication |
|---|---|
| 1 STOP is not a result | **Finding (§3):** two fragments with a real `[Install]` are emitted as an accepting `install_section=absent`. Elsewhere clean: row 1/2/3/4/8 unreadable and grammar cases STOP, evaluable deviations FAIL. |
| 2 Whose kernel answered? | Clean. The oracle names its own domain (`systemd 259 (259.5-0ubuntu3)`, printed with the tool path); the terminal claim stays inside the attested execution domain. |
| 3 Leaf is not path | Clean. Component/mount binding retained; the C1 mount-projection residual stays disclosed at `STATUS_RP7.md:154-156`, not silently dropped. |
| 4 Child environment | Clean. Pinned absolute tools, `python3 -I -S`, isolation re-asserted inside both embedded parsers before any work. |
| 5 Parser completeness | **Finding (§3):** the row-6 line grammar models `\n` only; systemd also terminates at `CR`. |
| 6/7 Status before stdout | Clean. rc, stderr emptiness, record count and single-line shape are all adjudicated before semantics, in both `run_case` and `subject_case`. |
| 8 Name is not identity | Clean; no new rendered-name comparison. Row 9 strengthens the opposite way, requiring a literal name in the raw rendering. |
| 9 Sentence outruns probe | **Overlay on §3:** "the LINE TERMINATOR - and only the terminator" is not what `split("\n")` + `rstrip("\r")` implements. Otherwise the prose is unusually disciplined: the transcript exception is stated, the duplicate invariant is labelled stronger-than-systemd, and "what is not established" is written down. |
| 10 Evidence that can fail | Clean and materially improved. Counters are measured and compared to declared expectations, identity is asserted before and after, mutants are applied by exact single-line match, and the transcript reproduced 155/156 lines for me with the sole exception the document predicted. |
| 11 Declared instrument not executed | Clean. The fence extracts and drives the delivered functions; `HARNESS_EXTRACT` refuses a residual `wpi_main "$@"` and requires the named functions to exist in every subject. I drove the same production function for my own finding. |
| 12 Unmodelled input disappears | **Finding (§3):** a bare `CR` terminator is outside the model and produces an accepting line instead of a coverage STOP. Row 9 is closed for this pattern - unconsumed and malformed tokens STOP. |
| 13 Terminal disposition | Clean. Row-9 tokens each receive one disposition; property-table members are conserved and duplicate-checked; the fence's count gates fail closed on a dropped arm. |

## 8. Optional nits (no repair required)

- **NIT-1 - oracle coverage.** The nine ORACLE arms establish what may precede the
  terminator, but never vary the terminator itself, and the comment-bridge /
  blank-terminate half of the row-6 rule of record is equally a claim about
  systemd yet is not in the oracle. I executed that half independently against
  systemd 259 and the block agrees on all of it (`# comment`, `; comment` and
  indented comment bridge an open continuation; blank and whitespace-only lines
  terminate it; comment-then-blank terminates). So this is an evidence-coverage
  gap, not a second defect.
- **NIT-2 - unqualified terminal token.** `D026_SUMMARY ... red_green_pairs=36
  controls=9` carries no "single-subject" qualifier, although the fence body
  (`SELF_QA_RP7.md:522-524`), `STATUS_RP7.md:126-128` and the report all state
  plainly that a single-subject RED "is only a fixture the already-fixed code
  rejects". A reader of the terminal line alone would over-read it.
- **NIT-3 - counter mixing.** `same_value_duplicate` / `clean_single` increment the
  RED/GREEN counters although the fence itself declares them a discrimination
  pair rather than a pre-fix falsification. Honest in band; a separate counter
  would keep the summary line exact.

## 9. Scope, safety and repository state

`git diff 8ec89675..2d0f24d0 --name-status` is the four owned files only, all
inside `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/`. No Pine, parity,
`MTC_V2`, schema, broker, deploy, credential or trading surface is touched.

This session performed no Git mutation of the audited repository: no stage,
commit, checkout, reset, stash, branch, push or worktree change. HEAD remained
`d4e90cb05bfbe227d17ce6264f0d3c19d3b5337f` throughout, `git status --porcelain`
was empty (0 paths) immediately before this write, and the two pre-existing
stashes (`pathscope-...-2026-08-13`, `-2026-08-14`) are untouched and predate this
session. The only path this session wrote inside the repository is:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CAP_OVERRIDE_CLAUDE_T0_AUDIT_2026-08-13.md
```

All dynamic evidence is outside the repository, under the run-owned WSL scratch
root `/var/tmp/r7ac-claude-t0-2hMuKFPj` plus the fence's own `mktemp -d` root,
which the fence removed at exit. The `git init` in §2 created a repository inside
that scratch root only; it reads the audited object store through
`objects/info/alternates` and wrote nothing to it. The four materialized frozen
artifacts were re-hashed after all execution and are byte-identical to §1.

No host contact, network probe, SSH/SCP, deployment, service action, credential
handling, ARM, order, TESTNET, mainnet, Pine, parity, MTC or trading action
occurred. `systemd-analyze verify` was used read-only on local fixture files and
contacted no service manager. No sub-delegation; no other model was invoked.

**Auditor self-disclosure.** My first boundary-sweep harness was itself invalid:
the tooling layer between this session and WSL collapsed doubled backslashes, so
the fixtures carried the letter `r` where a `CR` was intended. I detected it
because the four reference arms failed to reproduce the fence's already-recorded
oracle answers, discarded that sweep entirely, rebuilt every fixture with octal
byte escapes (`\134`, `\015`, `\012`), and made reproduction of the fence's five
known oracle answers a hard gate before any new arm was read. Every result in §3
and §5 comes from the rebuilt harness. This is the same failure the package
documents at `SELF_QA_RP7.md:1119-1142`, and it is the reason its `fixture_terms`
census is the right design.

## 10. Verdict

**REQUEST_CHANGES**

One required repair: §3 - restore a line grammar that models systemd's terminator
set, so a bare `CR` before a section header and a trailing `CR` run can no longer
produce an accepting `install_section=absent`. A candidate two-line repair, its
RED/GREEN evidence and its non-weakening controls are recorded above; the
implementer must also update the fence's `MUT_TARGET` literal
(`SELF_QA_RP7.md:562`), add `bare_cr_install` and a multi-CR arm as multi-subject
D026 pairs with `round4` and the delivered bytes as the named other subjects, and
extend the ORACLE to vary the terminator itself.

Everything else in the cap-override round is accepted on my evidence: identities
re-derive exactly, the fence runs clean and reproduces its transcript, REQUIRED-1
and REQUIRED-2 are closed as specified, and the row-9 work withstood an
independent quoting attack.

The T0 round cap is exhausted and this round was the single owner-authorized
cap-override cycle (`WPI_OWNER_DECISIONS_2026-08-13.md` §4), so under `AGENTS.md`
this finding is reported to Barış rather than dispatched as a further round. This
verdict does not fill an acceptance slot; both mandatory flagship verdicts are
required and neither is an acceptance here.
