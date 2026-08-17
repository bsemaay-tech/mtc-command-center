# RP7 rows 1-9 extension — Claude Pro T0 flagship audit

**Verdict: REQUEST_CHANGES** (2 REQUIRED, 4 NIT)

Auditor: Claude Pro, first flagship on these bytes, non-implementer.
Session model header: `claude-opus-5`. Tier T0, dispatched xhigh per kickoff. Fresh session.
Date: 2026-08-13.
Kickoff: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP7_EXT_AUDIT_2026-08-13.md`.
Design of record: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROWS_1_9_OPTIONS_CODEX_2026-08-10.md` §D.

**An accepting verdict was available on the execution evidence and is withheld on two
predicate-vs-preregistration divergences, one of which rests on a factually false
justification.** Both are documentary-plus-small-code fixes. Nothing in the rebuild fence,
the capture discipline or the RED/GREEN arithmetic is wrong; the transcript reproduces
byte-for-byte. The block nonetheless implements two row predicates that the preregistration
of record does not describe.

---

## Contract item 1 — identities, `bash -n`, CR bytes

Re-derived under WSL Ubuntu (`Linux 6.18.33.2-microsoft-standard-WSL2`, GNU bash 5.3.9)
before reading anything:

| artifact | field | kickoff-stated | re-derived | match |
|---|---|---|---|---|
| `RP7-WPI-RO.sh` | bytes | 127046 | 127046 | yes |
| `RP7-WPI-RO.sh` | sha256 | `a2ec1d0c47db53a756b7abe0803e7c6e62d42dd4c6b69934332c2eb501c714ad` | `a2ec1d0c47db53a756b7abe0803e7c6e62d42dd4c6b69934332c2eb501c714ad` | yes |

**SELF_QA identity I audited** (kickoff requires this be stated):
`SELF_QA_RP7.md` = **414797 bytes**, sha256
`741a9e1908560b9402f807ad9b0bf4ba272138d94b52c61dbffff10322d71a07`.

- `bash -n RP7-WPI-RO.sh` → **rc 0**, no output.
- **CR (0x0D) bytes: 0** in both files, counted byte-exactly (`tr -dc '\r' | wc -c`), not by a
  line-oriented grep. LF count 2109 (block) / 4858 (SELF_QA); block's final byte is `0a`.
- Block carries **0** high-bit (0x80-0xFF) bytes and **0** tab bytes; `file(1)` reports
  `Bourne-Again shell script, ASCII text executable` with no CRLF terminator note.

---

## Contract item 2 — rebuild fence executed verbatim

Ran the published extraction command unmodified, foreground, from `WPI_BLOCKS_DRAFT` under
WSL, exactly as `SELF_QA_RP7.md:36-37` publishes it:

```bash
cd /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
sed -n '/^# RP7_ROWS_1_9_REBUILD_FENCE_BEGIN$/,/^# RP7_ROWS_1_9_REBUILD_FENCE_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

**Result: rc 0, empty stderr, 57 transcript lines.**

**My transcript is byte-identical to the pasted one.** Both the 57 lines I produced and
`SELF_QA_RP7.md:283-339` hash to
`1843c3f459956f5f83a18eeb28b022c8164279edbc0bbed358d05ac8b376c078`; `diff -u` is empty.

Structural counts, independently derived from my own run:

| quantity | claimed | mine |
|---|---|---|
| `D026 row=` lines | 49 | **49** |
| RED | 23 | **23** |
| GREEN | 23 | **23** |
| CONTROL | 3 | **3** |
| `D026_CONTROL` (row-8 ten-property proof) | 2 | **2** |
| `HARNESS_CASE_FAIL` / `HARNESS_ABORT` / `HARNESS_CASE_STDERR` | 0 | **0** |

`red_green_pairs=23 controls=3 result=PASS` is arithmetically honest: 23×2 + 3 = 49.
Identity is asserted **before and after** the run inside the fence itself
(`SELF_QA_RP7.md:57-61`, `:271-275`) and both stages re-print 127046 / `a2ec1d0c…` / `cr=0`.

**Instrument check (Pattern 11).** The fence is not a re-implementation. It drops only the
terminal `wpi_main "$@"` line (`:63`), **proves that call is absent** from the extract
(`:65`), proves both new entry points are present (`:66-67`), sources the extract (`:69`) and
drives the block's own functions. `python3 -I -S` appears only where the block itself invokes
it. This satisfies the standard that rejected the first D026 delivery.

**Disclosed limitation of my reproduction:** `HARNESS_ATTESTED_MOUNTINFO
sha256=78388f0d…` matched the pasted value exactly. That digest derives from
`/proc/self/mountinfo`, so the match confirms I ran in the **same WSL instance** the Lead did.
My run is an independent *execution*, not an independent *host*. Anyone re-running elsewhere
should expect that one line to differ; nothing else in the transcript is host-derived.

---

## Contract item 3 — adversarial audit of `B2_rows_1_7` and `B4_rows_8_9`

### Verified correct

**Presence-before-value is centrally enforced and cannot be bypassed.** `wpi_show_get`
(`RP7-WPI-RO.sh:566-570`) tests `WPI_SHOW_SEEN[$query]` and STOPs with
`property_record_absent` **before** touching the value. `WPI_SHOW_VALUES` is read at exactly
one site in the whole block (`:569`, inside `wpi_show_get`); every one of the eleven property
accesses in B2 (`:768,773,778,783,788,793,797,801,805`) and B4 (`:832,844`) goes through it.
There is no path by which an absent record becomes an empty value.

**I confirmed against a real manager that this is the correct shape.** systemd 259 answering
`systemctl show --property=NoSuchPropertyXYZ` prints **nothing at all** at **rc 0** — it omits
the record rather than rendering `X=`. That is precisely §D.4 #4's masquerade, and it is
precisely what the fixture's `__DELETE__` arm (`SELF_QA_RP7.md:143`) reproduces. The
absent-record fixtures are faithful to real systemd behaviour, which the fence alone could not
establish.

**`wpi_capture` is unchanged.** I extracted the dual-accepted r9 blob from git
(`git show 437593c5:…/RP7-WPI-RO.sh` → 108301 B / `0e93f90d…`, matching the kickoff) and
diffed the function body: **byte-identical**, both hashing to `927ecca34598d62f…`. The
extension adds 10 functions and removes none. Bounded captures are reused, not re-authored.

**Descriptor discipline / C1 carried finding — does not widen, and row 6 narrows.**
`wpi_alloc_leaf` is **absent** from the block (grep: no matches), as the kickoff requires. All
leaves are addressed by the monotonic `WPI_PROBE_SEQ` under `$EV_DIR` (`:204-206`, `:288-290`,
`:348-352`), never by a re-resolved name. Row 6 reads the fragment through a **bound file
descriptor** opened once (`:631`) and passed as the child's stdin (`:636`), so no name is
re-resolved between binding and read — strictly narrower than the C1 class. Row 7 adds one
further caller of the pre-existing `wpi_assert_regular_digest`, which still digests by path
(`:1351`); that is the existing C1 predicate reused unchanged, not a new instance of the
defect. **No name-readdressed leaf is added.**

**Row 6 capture-ordering defect is genuinely fixed.** `parser_rc` is preserved (`:674`), the
stderr and stdout captures are consumed (`:676-678`), and only then is
`wpi_mount_guard_end` called (`:679`). The ordering the rebuild exposed is correct in the
delivered bytes.

**Row 7 adjudicates size before digest** (`:1354` precedes `:1355`), as §D.5 requires.

**ExecStart parser (GLM R2) is properly repaired.** `wpi_assert_unit_execstart:585-595` is a
**depth-aware** scanner that splits on `;` only at bracket depth 0, so the real rendering
`start_time=[Thu … UTC; 17s ago]` cannot break mid-timestamp. Unknown keyed runtime fields are
tolerated (`:611`) while `path`, `argv[]` and `ignore_errors` remain mandatory and
duplicate-checked (`:608-616`). The `r5_exec_realistic` RED/GREEN pair exercises it. GLM R2 is
closed.

**Parsers, not matchers (Pattern 5).** Row 6 is a real line-grammar parser handling comments,
continuations, NUL and encoding (`:652-672`); row 9 is a `shlex` tokenizer counting effective
assignments (`:714-742`); row 5 parses the compound `ExecStart` struct. No `grep`/substring
adjudication anywhere in the new sections. The 5-decoy, 6-comment and 9-substring
demonstrations §D.5:351-353 names as non-optional are all present and all behave correctly.

**Evidence that can fail (Pattern 10).** Every GREEN has a paired RED except the 3 declared
controls; each `B4_property … value=matches` line is printed only after the comparison passed
(`:835-841`), and the fence independently asserts all ten such lines were emitted in both
row-8 GREEN runs (`:266-270`). No expected value is a timing or derived measurement.

**Thirteen-pattern adjudication** (`DESIGN_DEFECT_PATTERNS_2026-08-10.md`): P1 clean (STOP/FAIL
separated and both arms demonstrated — `r1_inactive` FAIL rc 1 vs `r1_manager_stop` STOP rc 3);
P2 clean (terminal claim keeps the attested-execution-domain qualifier, `:2087-2088`);
P3 clean (`wpi_alloc_leaf` absent; row 6 fd-bound); P4 clean (`python3 -I -S` with isolation
self-check at `:640-644` and `:716-720`, invoked via the bound `$WPI_PYTHON3`); P5 clean;
P6 clean (rc → stderr → stdout precedence at `:764-766` and `:826-828`); P7 clean
(`wpi_parse_show_capture` separates clean EOF, unterminated final record and hard read error);
P8 — see NIT-4; P9 clean; P10 clean; P11 clean (fence proves declared == executed instrument);
P12 clean; P13 clean. **P1 is the pattern row 6 now violates in the reverse direction — see
REQUIRED-1: a condition systemd ignores is rendered as a FAIL.**

---

### REQUIRED-1 — Row 6 now flags `[install]`, contradicting the design of record and the unamended preregistration, on a justification that is factually false

`RP7-WPI-RO.sh:667` matches the parsed section name case-**insensitively**:

```python
if m.group(1).lower()=="install":
 print("INSTALL section=%s"%m.group(1)); sys.exit(1)
```

so a lowercase `[install]` header becomes `B2_FAIL reason=install_section_present`
(`:682`), confirmed executing in my own run:

```text
D026 row=6 arm=case_variant mutation=lower_case_install RED rc=1 line=B2_FAIL reason=install_section_present path=…
```

Three sources say that is the wrong verdict:

1. **The design of record.** §D.5 (`ROWS_1_9_OPTIONS_CODEX_2026-08-10.md:341`) lists the
   case-variant beside the comment and continuation decoys: "`[Install]` inside a comment;
   after a line continuation; **case-variant `[install]`** | **Must NOT trigger
   `install_section_present`**."
2. **The preregistration of record, which is unamended.**
   `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md:1094` still reads: "contains no
   section header whose **exact parsed name** is `Install`". `[install]` is not exactly
   `Install`.
3. **systemd itself.** `STATUS_RP7.md:36-37` justifies the change as "treats `[Install]`
   section names case-insensitively, **matching systemd section parsing**". That claim is
   false. I tested it on systemd 259 (`259.5-0ubuntu3`) with a parse-only
   `systemd-analyze verify`, installing nothing:

   ```text
   /tmp/rp7_case_probe/rp7probe-lower.service:6: Unknown section 'install'. Ignoring.
   ```

   The canonical `[Install]` unit produced no such diagnostic. **systemd section names are
   case-sensitive; a lowercase `[install]` is inert and enables nothing.**

**Provenance.** This came in as GLM advance-read **NIT** N2
(`RP7_ROWS_1_9_GLM_ADVANCE_READ_2026-08-13.md:144-155`), whose own text conceded the existing
behaviour "matches the §D.5 fixture's stated intent … so it is consistent with the design as
written" and merely invited the flagship to revisit it. The round-2 repair
(`RP7_ROWS_1_9_REPORT_2026-08-13.md:205-207`) escalated that NIT into a **silent predicate
change**: it inverted a §D.5-mandated control into a RED, dropped the control count from 4 to
3, and recorded the reversal as a fix rather than as an amendment. Contrast row 1, which the
same round *did* label an explicit preregistration amendment (`SELF_QA_RP7.md:25-28`,
`STATUS_RP7.md:54-59`). Row 6 got no such label anywhere.

**Consequence.** A fragment carrying a systemd-inert `[install]` header FAILs the run for a
condition the host would ignore. The direction is fail-closed, and row 7's digest pin means an
accepted fragment cannot contain one without row 7 failing first — so live risk is low. That
is not the objection. The objection is that the bytes under acceptance implement a predicate
neither the design nor the preregistration describes, defended by a false statement about the
system under test, in a project whose own history already contains a round titled *"false
justification corrected"* (`bb8546e6`).

**Required:** either revert `:667` to the exact-name match and restore `r6_case` to a CONTROL
(matching §D.5:341 and prereg:1094), **or** amend §8.2 row 6 and §D.5 first, label it a
preregistration amendment as row 1 was, and correct the false systemd claim at
`STATUS_RP7.md:36-37` in either case. **My recommendation is the revert:** the preregistered
"exact parsed name" text is the technically correct reading of systemd.

### REQUIRED-2 — The row-1 amendment was never carried into the preregistration; the block emits a STOP token the preregistration does not declare

The kickoff asks me to adjudicate whether the `ActiveState` amendment is acceptable or must be
built as written.

**On the engineering, I accept it.** Reading `ActiveState` from the same bounded property
table (`:768`) is §D.4 #3's own option (b) (`:305-309`), and it defeats Pattern 1 — `is-active`
uses exit status as a result channel, which is exactly how the catalogue's Pattern-1 defect
reproduces. The block separates the two arms correctly and demonstrates both: `inactive` →
`B2_FAIL reason=unit_not_active` (rc 1), manager rc 7 → `B2_STOP
reason=system_manager_unreachable` (rc 3). Building it as literally written would be worse.

**On the record, it is not yet a valid amendment.** The preregistration still describes the
other predicate. `WPI_PREREGISTRATION_DRAFT.md:1089` reads "`systemctl is-active` returns a
parseable unit state", and preregisters the STOP token **`operation=is-active`**. The block
emits **`operation=show`** (`:764`), which my run reproduces:

```text
D026 row=1 arm=manager_stop … line=B2_STOP reason=system_manager_unreachable operation=show rc=7 …
```

The string `systemctl is-active` still occurs twice in the preregistration. The amendment is
recorded only inside the block's own SELF_QA and STATUS — the artifacts under audit — never in
the document of record. GLM R3 asked the flagship to confirm the §8.2 text had been amended;
**it has not been.** As it stands the block implements, and this audit would be accepting, a
predicate and an emitted token that the preregistration does not contain.

**Required:** amend §8.2 row 1 and its declared first-divergence grammar (`operation=is-active`
→ `operation=show`) in `WPI_PREREGISTRATION_DRAFT.md`, so the accepted predicate and the
preregistered predicate are the same sentence. This is documentary; no block change is needed.

---

### NITs

**NIT-1 — §D.5's absent-record fixture is built for 2 of the 4 rows it names.** §D.5:333
requires it for rows "2,3,4,8"; the fence supplies `r2_missing` (NRestarts) and `r8_missing`
(ProtectSystem). Rows 3 and 4 have no such arm. Low severity because all four go through the
identical `wpi_show_get` STOP path (`:566-570`), which the two existing fixtures exercise in
both B2 and B4 — the mechanism is demonstrated even though the named fixtures are not.

**NIT-2 — the row-9 duplicate fixture is weaker than §D.5 specifies.** §D.5:347 asks for
`MTC_BRIDGE_START_MODE` "assigned twice with **different values**"; the fixture
(`SELF_QA_RP7.md:261`) assigns the same value twice. The tokenizer fails on `count != 1`
(`:739-742`) so the verdict is identical either way, and shadowing is therefore covered by
construction — but the built fixture does not demonstrate the shadowing case the design named.

**NIT-3 — the row-7 STOP fixture exercises the file, not a parent component.** §D.5:345 asks
for "unreadable **parent component** / ambiguous ENOENT". `r7_unreadable` chmod-000s the
fragment itself and runs as `nobody`. It correctly proves STOP `fragment_unreadable` rather
than `unit_fragment_absent`, which is the property that matters; the parent-traversal arm of
`wpi_walk_components` is not exercised.

**NIT-4 — `CapabilityBoundingSet=''` is the row-8 pin most likely to be wrong.** Judging the
disclosure as the kickoff directs: `HARNESS_DISCLOSURE row=8
sandbox_pins=asserted_rendered_systemctl_show_literals host_derivation=freeze_time_act
fixture_fidelity_not_established` is **honest and adequate** — it states plainly that the fence
proves only comparator behaviour and that fidelity is not established. It is not, however,
specific about which pins carry risk, so I measured what I could read-only against systemd 259:

| pin | block expects | real rendering observed | assessment |
|---|---|---|---|
| `KillSignal` | `15` | `15` (numeric, across 4 units) | **GLM R1's symbolic-`SIGTERM` prediction is wrong; pin is consistent** |
| `FinalKillSignal` | `9` | `9` | consistent |
| `TimeoutStopSec`→`TimeoutStopUSec` | `45s` | human form (`1min 30s` for 90s) | `45s` plausible |
| `CapabilityBoundingSet` | `` (empty) | full 40-capability list unless the unit explicitly drops all | **only correct if the fragment sets `CapabilityBoundingSet=`; unverified** |

GLM R1's first concrete worry is refuted; its second stands. The `ProtectSystem`,
`RestrictAddressFamilies` and `ReadWritePaths` renderings remain underived, as disclosed.
Recommend the freeze-time derivation start with `CapabilityBoundingSet`.

---

## Contract item 4 — delta-gate proof

**Path-scoped gate (governing).** This session wrote exactly one file:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_EXT_AUDIT_2026-08-13.md
```

which is the exact path the kickoff names, and which did not exist at session start
(`ls` → `No such file or directory`). No other repository path was created, modified or
deleted by me.

**No git mutation.** No commit, stage, checkout, branch, stash, reset or push was executed.
HEAD is unchanged at `d2fd0040b0b4d96e8a2344b9715fea5d788303df`, branch
`feature/donchian-crypto-ladder`.

**Read-only elsewhere.** Reads of the block, SELF_QA, STATUS, the design doc, the
preregistration and the git object store; one `git show` of an existing blob to a scratch path
outside the repo. Fence side effects are confined to `/tmp/rp7_rows_1_9_rebuild_evidence`
inside WSL, created and removed by the fence's own guarded `cleanup` trap (`SELF_QA_RP7.md:50`,
`:52-53`). My systemd probe wrote two unit files to `/tmp` inside WSL, ran parse-only
`systemd-analyze verify`, installed nothing, reloaded nothing, and deleted them. Working files
were kept in `C:\tmp\rp7_audit`, outside the repository.

**Whole-status delta (advisory, with attribution).** Baseline at session start: 133
`git status --porcelain` lines, including one tracked modification —
`M MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`. **That modification is not
mine**; it predates this session and belongs to a concurrent lane in this shared worktree. The
only delta attributable to this audit is the single untracked verdict file above, taking the
count to 134.

---

## Standing

This verdict **does not fill the Claude flagship slot**, because it is not an accepting
verdict. Dual acceptance additionally needs a fresh Codex `gpt-5.6-sol` audit, blocked on
account limits until 08-16/08-18.

The execution evidence is sound and reproduces byte-for-byte; I re-ran it rather than trusting
either prior party, as instructed. Both REQUIRED items are narrow and closeable in one round —
REQUIRED-2 is purely documentary, and REQUIRED-1 is a three-character code revert plus a fixture
reclassification plus the removal of a false sentence. On their repair I would expect to reach
PASS or PASS-WITH-NITS on the same bytes-plus-repair.
