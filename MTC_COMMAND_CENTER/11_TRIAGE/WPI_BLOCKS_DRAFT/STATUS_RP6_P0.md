# RP6-P0 — status: ROUND-8-REPAIRED-PENDING-T0-REAUDIT (evidence-only round)

Updated 2026-08-11 by the round-8 implementer (Claude, fresh session). Round 8 is
an **evidence-only** round: it repairs the two legacy fences that failed the Lead's
round-7 QA execution (`RP6_R7_LEAD_QA_EXECUTION_2026-08-10.md`) and writes no
block byte. Audit tier unchanged: **T0** (host/execution-domain preflight). The
block remains a draft: not frozen, accepted, dispatchable, or authorised for host
execution. Full disposition: `RP6_REPAIR_R8_REPORT.md`; harnesses + R8 section in
`SELF_QA_RP6.md`.

**`RP6-P0.sh` is UNCHANGED this round** — SHA-256
`fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd`, 103071 B, 0 CR
bytes (re-derived this session by read-only tools; byte-identical to the round-7
commit `d9d7420f`). `bash -n` was not re-run (this session gates `bash`), but no
block byte was touched, so the round-7 `bash -n` rc 0 stands. If the block itself
were believed to need a change, this round would stop and report rather than
change it; it does not.

**Round-7 Lead QA result (the input to this round).** The Lead ran every fence by
anchored marker after round 7: the three R7 harnesses (4/4, 4/4, 8/8) and three
legacy fences (`C13_R3_BACKSTOP`, `F2_FREEZE_GATE`, `C13_R4B`) PASS. Two legacy
fences FAIL (rc 1) — `RP6_FULLBLOCK_D026` (7 s, no summary) and `RP6_R4_D026`
(41 s, `findings=4`) — both from `P0_FIXED_STAT: unbound variable` in their
landmark-sliced test arms: correction 7's frozen `P0_FIXED_*` literals
(`RP6-P0.sh:266-299`) fall outside the slices, and the extracted pin loop
references them under `set -u`.

**Round-8 repairs (`SELF_QA_RP6.md` only).**

- **Repair 1 — arm construction that survives block growth.** `build_f4_arm`
  (FULLBLOCK) and `build_pin_arm` (R4) now define every `P0_FIXED_*` literal their
  slices reference (the pin arm also mirrors the block's `P0_TOOL_COUNT_EXPECTED`
  derivation, another correction-7 value the slice reads), and each carries a
  build-time assertion that every `P0_FIXED_*` the slice references is defined —
  so a future round that adds a new frozen literal fails the build LOUDLY instead
  of emitting a silently-broken arm. Not a hand-widened slice.
- **F7_TOOL_POST — classified: block correct, fence fixture stale (fixed).**
  Correction 7 deleted the unpinned `command -v` fallback, so the F7 tool arm's
  empty `P0_TOOL_PINS` now STOPs at `tool_pin_unpinned` before the `[ -x ]` check
  that emits the R2-F1 `tool_not_evaluable … rc=na` token. Prereg §8.1 row 1 still
  carries `tool_not_evaluable tool=getent path=<p> rc=<n|na> detail=<d>
  mechanism=<m>` and its round-7 amendment defines `tool_pin_unpinned` for the
  unpinned case — so the block is right and the fixture is stale. The arm now pins
  `getent` to the fixture path; the PRE arm is unaffected (the pre-repair resolver
  kept the fallback).
- **R4 GREEN count — stale under correction 7 (fixed).** `$RP7PINS` supplied ten
  pins and asserted `count=10`; correction 7 requires twelve (row 1: `input_pin_omitted`,
  `input_pin_count_unexpected … expected=12`). `$RP7PINS` now carries all twelve
  (`id`/`getent` appended) and the GREEN assertion reads `count=12`. Block correct,
  fence stale.

**QA execution is PENDING-LEAD-EXECUTION.** This session gates the `bash`
interpreter (every `bash <script>`, `bash -n`, `bash -c`, `sed … | bash` returned
*requires approval* — same blocker the round-7 Claude and GLM sessions recorded),
so the round-8 re-run of the two repaired fences is recorded PENDING, not
fabricated (per the kickoff clause and AGENTS.md D026). Expected: both rc 0 / PASS.
Until the Lead re-runs them, the round-8 evidence is supplemental.

The freeze gate still has seventeen `<PIN-AT-FREEZE>` literals, so no end-to-end
`P0 PASS` is possible and nothing here is dispatchable regardless of this round's
verdict.

---

## Round-7 block change (the current bytes — round 8 changed no block byte)

Updated 2026-08-10 by the round-7 implementer (Claude, fresh session) for the
five Codex round-6 audit required corrections (`RP6_CODEX_AUDIT_R6_2026-08-10.md`,
REQUEST_CHANGES, rows A4/A8/A9/A10/A11). Audit tier: **T0** (host/execution-domain
preflight). Codex is this block's auditor of record for these corrections, so
implementer/auditor separation holds. Round 7 is authorised by owner grant #7
(2026-08-10), which lifts the T0 round cap for this block set — rounds continue
until both flagships accept; the acceptance standard is unchanged. The block
remains a draft: not frozen, accepted, dispatchable, or authorised for host
execution.

**QA execution is PENDING-LEAD-EXECUTION.** This Claude session's Bash tool gates
`bash -n`, script execution, `sha256sum` and `wc` (every `bash -n`/`bash -c`/
heredoc and the artefact hash/byte tools returned *requires approval*). Per the
kickoff's PENDING-LEAD-EXECUTION clause and AGENTS.md D026, the evidence is
recorded as PENDING rather than fabricated. The Lead must, in an unhindered Git
Bash against the round-7 bytes:

```text
tr -cd '\r' < RP6-P0.sh | wc -c                                       -> 0 (DONE in-session)
sha256sum < RP6-P0.sh                                                 -> fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd (DONE)
wc -c < RP6-P0.sh                                                     -> 103071 (DONE)
bash -n RP6-P0.sh                                                     -> PENDING (session gates bash)
sed -n '/^# R7_F2_HARNESS_BEGIN$/,/^# R7_F2_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc
sed -n '/^# R7_F3_HARNESS_BEGIN$/,/^# R7_F3_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc
sed -n '/^# R7_C3_HARNESS_BEGIN$/,/^# R7_C3_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc
the five marker-migrated legacy fences (C13_R3_BACKSTOP / RP6_FULLBLOCK_D026 /
  F2_FREEZE_GATE / RP6_R4_D026 / C13_R4B) by anchored marker, all rc 0
```

Expected: `R7_F2_QA_SUMMARY cases=4 … PASS`, `R7_F3_QA_SUMMARY cases=4 … PASS`,
`R7_C3_QA_SUMMARY cases=4 … PASS`, and the five legacy fences at their recorded
PASS summaries. Until these run, the round-7 evidence is supplemental (A11).

Round-7 disposition (Codex round-6 audit A4/A8/A9/A10/A11 + correction 7) — full
record in `RP6_REPAIR_R7_REPORT.md`; harnesses + marker migration in
`SELF_QA_RP6.md` §R7:

- **C1 / A4 (R5-F2) — REPAIRED.** `type -t` → `builtin type -t` (matches
  RP7-WPI-RO.sh:646-647), defeating a caller-defined `type(){…}`. Comment and
  `P0_prereq` narrowed to "required functions present and exercised", not RP0-LIB
  provenance. D026 harness `R7_F2` (PENDING).
- **C2 / A8 (R6-F3) — REPAIRED.** Outer pin parse wrapped in a caller-noglob
  save/restore, so a crafted cwd holding `stat=/usr/bin/stat` can no longer
  rewrite `stat=/usr/bin/sta*` before the charset gate. D026 harness `R7_F3`
  (PENDING) adds the exact whole-token crafted-cwd case.
- **C3 / A9 — REPAIRED.** `p0_probe_kind` and `p0_assert_venv_root` adjudicate
  rc-0 producer SHAPE (empty/multiline/non-printable/non-absolute) as rc 3 STOP
  before any rc-1 object verdict. D026 harness `R7_C3` (PENDING), both arms.
- **C4 / A10 — REPAIRED.** rc 124 relabelled
  `manager_query_rc124_timeout_reached_or_child_exit_124` (wrapper can't
  distinguish a child's own 124); interpreter isolation expressed as requested
  flags + child-reported state (binary provenance unbound); `pinned_timeout`
  honest via correction 7's mandatory timeout pin; python3 mandatory documented.
  Prereg §8.1 row 9 amended.
- **C5 / A11 — REPAIRED (re-run PENDING).** All eight fences carry unique
  anchored marker pairs; recorded commands are marker-based; R4 D026 POST
  assertions updated for the renamed tokens. The R4-fence open handle and the
  full re-run are pending Lead execution.
- **C6 — REPAIRED.** `RP6_REPAIR_R4_REPORT.md` stale `-S` "cannot be silently
  undone" claim replaced with the round-6 truth.
- **C7 — REPAIRED.** Exactly one frozen pin required per tool (twelve total),
  each equal to its frozen literal; omissions/extras/mismatches rejected;
  unpinned `command -v` fallback DELETED. Freeze-gate literals: **6 → 17**. Prereg
  §8.1 row 1 amended.

Current executable identity (round-7 bytes; hash/bytes/bash-n PENDING Lead
execution; CR bytes verified 0 by construction):

```text
sha256=fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd
bytes=103071
bash_n=PENDING-LEAD-EXECUTION
cr_bytes=0 (verified: tr -cd '\r' < RP6-P0.sh | wc -c)
line_endings=LF_only
bom=none
superseded_round6_sha256=75db028e76438bc88caba19b9c3b6411e5f573f7b6c2bd13c3883d24e4389570
superseded_round6_bytes=93421
freeze_gate_literal_count=17 (was 6; +11 per-tool path literals, correction 7)
frozen_ro_basis=RP7-WPI-RO.sh@d6a976aa sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad bytes=70941
```

The freeze gate now has seventeen `<PIN-AT-FREEZE>` literals, so no end-to-end
`P0 PASS` is possible and nothing here is dispatchable regardless of this round's
verdict.

---

# Prior status history — round 6 (REPAIRED-PENDING-T0-REAUDIT, superseded by round 7)

Updated 2026-08-10 by the round-6 implementer (GLM-5.2, fresh session) for the
three Claude flagship re-audit findings (`RP6_CLAUDE_REAUDIT_R5_2026-08-10.md`
F1–F3). Audit tier: **T0** (host/execution-domain preflight). GLM-5.2 implemented
only; Claude is this block's auditor for these findings, so implementer/auditor
separation holds (GLM-5.2 also implemented round 5, which is permitted). Round 6
is authorised by owner grant #7 (2026-08-10), which lifts the T0 round cap for
this block set — rounds continue until both flagships accept; the acceptance
standard is unchanged. The block remains a draft: not frozen, accepted,
dispatchable, or authorised for host execution.

**QA execution was PENDING at implementer hand-off; the Lead has now EXECUTED it.**
The GLM-5.2 session gates `bash -n` and script execution (same blocker the C13
and round-5 GLM rounds recorded), so it recorded the R6 evidence as PENDING
rather than fabricate output — the correct behaviour under D026. The Lead ran all
of it in an unhindered Git Bash on 2026-08-10 against the round-6 bytes
`75db028e…` / 93421 B:

```text
bash -n RP6-P0.sh                  -> rc 0, BASH_N=PASS
CR bytes (tr -cd '\r' | wc -c)     -> 0
R6-F1 adversarial .pth             -> R6_F1_QA_SUMMARY cases=3  pass=3  fail=0 result=PASS
R6-F2 gids grammar + noglob        -> R6_F2_QA_SUMMARY cases=10 pass=10 fail=0 result=PASS
R6-F3 pin-glob + p0_lookup         -> R6_F3_QA_SUMMARY cases=7  pass=7  fail=0 result=PASS
five prior mandated fences, all rc 0 against the NEW bytes:
  backstop        C13_R3_BACKSTOP_QA_SUMMARY inputs=2 mutations=2 cases=4 result=PASS
  full-block D026 RP6_FULLBLOCK_D026_SUMMARY … result=PASS
  freeze gate     F2_FREEZE_GATE_QA_SUMMARY placeholder_rc=3 filled_fixture_rc=0 result=PASS
  R4 D026         RP6_R4_D026_SUMMARY findings=4 pth_forge=real_venv
                  manager_bound=real_timeout inventory_basis=23e55667@d6a976aa result=PASS
  C13 R4b         C13_R4B_ARM_QA_SUMMARY cases=27 result=PASS
```

**Lead finding — fence addressing is fragile and MUST be fixed before freeze.**
The five prior fences are addressed by absolute LINE RANGES. Round 6 grew this
file, so the recorded ranges `2545,2989` and `3353,3518` now cut into prose: they
returned `rc 2` / no summary on first run and looked like regressions. They are
not — re-run at their true boundaries (R4 D026 `2553,3007`; C13 R4b `3379,3544`)
both return `result=PASS` at rc 0. Every future round shifts them again. The R5
and R6 harnesses already use `BEGIN`/`END` markers and are immune. **Action for
the next round: give all five prior fences marker pairs and record marker-based
invocations instead of line numbers.** A freeze whose evidence cannot be re-run
by a third party is not freeze-grade evidence.

Round-6 disposition (Claude re-audit findings F1–F3) — full record in
`RP6_REPAIR_R6_REPORT.md`; harnesses + expected polarity in `SELF_QA_RP6.md` §R6.
The disposition of EVERY finding is stated explicitly, including non-repairs:

- **F1 (MEDIUM, carried from round 4 — round 5 left it unaddressed) — REPAIRED
  in scope; one site out of scope, disclosed.** The false "` -S` cannot be
  silently deleted / it produces a named STOP" claim is retracted at every
  in-scope site (the block's interpreter-section comment, `SELF_QA_RP6.md`'s R4
  prose and arm note, and the round-4 F1 bullet below) and restated truthfully:
  the child's `sys.flags` self-check guards only ACCIDENTAL flag-word loss (it
  runs inside the `-c` body); a HOSTILE `.pth` that `os._exit(0)`s at `site`
  startup defeats it, so ` -S` — not the self-check — is the load-bearing control
  that contains a hostile venv. The cooperating fixture is superseded by an
  ADVERSARIAL `.pth` (writes marker + forged `P0PY` line + `os._exit(0)`); under
  it the no-`-S` mutant is NOT caught (rc 0, marker created, forged accepted
  line, no STOP), which the claim now states plainly. The fourth site the audit
  named, `RP6_REPAIR_R4_REPORT.md:88`, is NOT in this round's four-file allowlist
  and was left untouched/stale, flagged for the Lead.
- **F2 (MEDIUM, NEW) — REPAIRED.** The raw `id -G` `gids` capture is now
  grammar-gated against `*[!0-9[:space:]]*` BEFORE any expansion, and the
  per-item split runs under `set -f` — the F3 pattern applied to `gids`. `*`,
  `0*`, `?` now STOP as `group_query_not_evaluable … response_not_decimal_gid_list`
  identically in an empty and a numeric-named cwd; the false `form=numeric_only`
  and the laundered whole-word intersection are gone; `HONEST_ROOT_GROUP`
  (`1001 0`) still STOPs with `capability_wider_than_ledger gid=0`.
- **F3 (LOW/MEDIUM, NEW) — REPAIRED.** The pin-path charset gate refuses `*`,
  `?`, `[` (`expected=printable_without_glob_metacharacters`); `p0_lookup`'s
  unquoted map split runs under `set -f`; the "deliberate and safe" comment now
  certifies safety against pathname expansion, not only word splitting.
- **Codex round-5 F1/F2/F3 — unchanged, still CLOSED** (no round-6 edit touches
  the pin post-loop gate, the `type -t` prerequisite, or the `P0_FORBIDDEN_GIDS`
  gate). **Round-4 nits 1-6 and round-5 nit 3 — still open (optional)**,
  untouched as permitted. Nit 1 (`set +f` restores to block-default ON, not
  caller-saved state) now spans three pairs; a full save/restore remains a future
  optional hardening.

Current executable identity (round-6 bytes; QA PENDING Lead execution):

```text
sha256=75db028e76438bc88caba19b9c3b6411e5f573f7b6c2bd13c3883d24e4389570
bytes=93421
bash_n=PASS (Lead-executed 2026-08-10, rc 0)
line_endings=LF_only
bom=none
superseded_round5_sha256=490e3e4edfec811dee3dc90c6693e8ebeb865eb946a431ff017de58e66f0ce5f
superseded_round5_bytes=89029
frozen_ro_basis=RP7-WPI-RO.sh@d6a976aa sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad bytes=70941
```

The freeze gate is unchanged in COUNT (still six `<PIN-AT-FREEZE>` literals), so
no end-to-end `P0 PASS` is possible and nothing here is dispatchable regardless
of this round's verdict.

---

# Prior status history — round 5 (REPAIRED-PENDING-T0-REAUDIT, superseded by round 6)

Updated 2026-08-10 by the round-5 implementer (GLM-5.2, fresh session) for the
three Codex final-audit findings (`RP6_CODEX_FINAL_AUDIT_2026-08-10.md` F1–F3).
Audit tier: **T0** (host/execution-domain preflight). GLM-5.2 implemented only;
it did not audit this block, so implementer/auditor separation holds. The
round-4 Codex audit closed the four round-4 findings, but its independent
whole-block sweep returned a non-accepting T0 verdict with three NEW required
repairs (F1 HIGH freeze-gate polarity; F2/F3 MEDIUM). Round 5 closes those three.
**Cap note:** the final-audit report itself states it "authorizes no additional
repair/audit round," and T0 is capped at 3; this round is therefore presented
for Lead adjudication of whether the owner amendment covering round 4 extends to
this round. Acceptance still requires fresh independent `claude-opus-5` xhigh
and `gpt-5.6-sol` xhigh verdicts. The block remains a draft: not frozen,
accepted, dispatchable, or authorised for host execution.

**QA execution was PENDING at implementer hand-off; the Lead has now EXECUTED it.**
The GLM-5.2 session gates `bash -n` and script execution (same blocker the C13
GLM-5.2 round recorded), so it recorded the evidence as PENDING rather than
fabricate output — the correct behaviour under D026. The Lead ran all of it in an
unhindered Git Bash on 2026-08-10 against the round-5 bytes `490e3e4e…` / 89029 B:

```text
bash -n RP6-P0.sh                      -> rc 0, BASH_N=PASS
CR bytes (tr -cd '\r' | wc -c)         -> 0
R5-F1 python3 freeze-gate polarity     -> R5_F1_QA_SUMMARY cases=6 pass=6 fail=0 result=PASS
R5-F2 RP0 symbol type assertion        -> R5_F2_QA_SUMMARY cases=4 pass=4 fail=0 result=PASS
R5-F3 forbidden-GID grammar + set -f   -> R5_F3_QA_SUMMARY cases=5 pass=5 fail=0 result=PASS
five prior mandated fences, all rc 0:
  952,1035    backstop            cases=4  PASS
  1678,2068   full-block D026     RP6_FULLBLOCK_D026_SUMMARY … result=PASS
  2286,2319   freeze-literal gate PASS
  2545,2989   R4 D026             PASS
  3353,3518   C13 R4b             C13_R4B_ARM_QA_SUMMARY cases=27 result=PASS
```

No regression: every `ASSERT_UNMET`/`FAIL` token in those transcripts sits on a
pre-fix or mutant variant (the intended RED polarity) — none on a repaired or
current variant, verified by filtering the transcripts. QA is therefore real
executed evidence, not design intent, and the block is ready for T0 re-audit
dispatch.

Round-5 disposition (Codex final-audit findings F1–F3) — full record in
`RP6_REPAIR_R5_REPORT.md`; harnesses + expected polarity in `SELF_QA_RP6.md` §R5:

- **F1 (HIGH) — REPAIRED IN THE BLOCK.** After the pin-parse loop, REQUIRE
  `P0_TRUSTED_PYTHON_BOUND=yes`, so omitting the `python3` pin is a named rc-3
  STOP (`input_pin_freeze_unfilled tool=python3 …
  detail=trusted_python_pin_omitted_freeze_gate_load_bearing`) rather than a
  bypass. Freeze-gate polarity is now correct: omission STOPs, presence (with the
  deploy-channel value filled) passes. The in-loop placeholder gate
  (`detail=deploy_channel_value_never_derived_here`) is preserved unchanged.
- **F2 (MEDIUM) — REPAIRED IN THE BLOCK.** The two RP0-symbol prerequisite
  checks now use an exact builtin `type -t … = function` assertion instead of
  `command -v`, so a PATH executable (or alias) of the same name is rejected at
  rc 3 (`… detail=not_a_shell_function`) and — critically — is never called,
  closing the pre-inventory child-execution channel. Genuine sourced functions
  still pass. (`command -v` remains correct inside `p0_resolve_tool`, where the
  intent is to resolve a PATH tool to an absolute path.)
- **F3 (MEDIUM) — REPAIRED IN THE BLOCK.** `P0_FORBIDDEN_GIDS` is now
  grammar-gated against `*[!0-9[:space:]]*` BEFORE any expansion, and both split
  loops (the input gate and the capability intersection loop) run with pathname
  expansion disabled (`set -f`). A wildcard or any non-digit/non-space byte is a
  STOP (`input_charset … expected=decimal_digits_and_separators_only`)
  regardless of cwd; valid lists are still admitted.

Current executable identity (round-5 bytes; QA EXECUTED by the Lead, see above):

```text
sha256=490e3e4edfec811dee3dc90c6693e8ebeb865eb946a431ff017de58e66f0ce5f
bytes=89029
bash_n=PASS (Lead-executed 2026-08-10, rc 0)
line_endings=LF_only
bom=none
superseded_round4_sha256=e93d07adcc9ae03ad15e0b0f10c76be54517251ab461c8fe789d160072d253c6
superseded_round4_bytes=85540
frozen_ro_basis=RP7-WPI-RO.sh@d6a976aa sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad bytes=70941
```

The freeze gate is unchanged in COUNT (still six `<PIN-AT-FREEZE>` literals); F1
makes the sixth one (`P0_FIXED_TRUSTED_PYTHON`) load-bearing by construction
instead of by operator choice.

---

# Prior status history — round 4 and earlier (REPAIRED-PENDING-AUDIT, do not treat as accepted)

Updated 2026-08-10 by the round-4 implementer (`claude-opus-5` xhigh, fresh
session). Audit tier: **T0** (host/execution-domain preflight). The second-flagship
Codex T0 audit of the round-3 bytes (`RP6_CODEX_T0_AUDIT_2026-08-10.md`) returned
**BLOCK on 4** — one executed security failure (the "read-only" interpreter probe
ran unverified venv startup code), one executed availability failure (row 9 could
hang with no reasoned STOP), and two exact frozen-contract mismatches. **Round 4
exceeds the recorded T0 cap under explicit owner authorisation**, granted for the
identical venv site-startup security class already resolved on RP7 (2026-08-10
~17:15) and extended to RP6-P0 by the Lead. Acceptance still requires fresh
independent `claude-opus-5` xhigh and `gpt-5.6-sol` xhigh verdicts. The block
remains a draft: not frozen, accepted, dispatchable, or authorised for host
execution.

Round-4 executable identity (superseded by the round-5 bytes above):

```text
sha256=e93d07adcc9ae03ad15e0b0f10c76be54517251ab461c8fe789d160072d253c6
bytes=85540
bash_n=PASS
line_endings=LF_only
bom=none
superseded_round3_sha256=2d9b166eacfc39ebe0d8d89edb5860876ccc4d9f0ff97f9e10a228dbcf96289e
superseded_round3_bytes=71743
frozen_ro_basis=RP7-WPI-RO.sh@d6a976aa sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad bytes=70941
```

Round-4 disposition (Codex T0 findings 1-4) — full record in
`RP6_REPAIR_R4_REPORT.md`, evidence in `SELF_QA_RP6.md`:

- **F1 (HIGH) — CLOSED (interpreter isolation); the `-S` sub-claim was NARROWED
  in round 6.** The interpreter probe runs `-I -S`, not `-I`. `-I` implies
  `-E`/`-P`/`-s` but not `-S`, so the previous bytes imported `site` and
  executed the judged venv's `*.pth` `import` lines before the `-c` body. The
  child also refuses to report a version unless `sys.flags.isolated` and
  `sys.flags.no_site` are both set. Round 6 retracts this bullet's earlier
  sentence that this means deleting ` -S` "yields a named
  `interpreter_startup_not_isolated` STOP instead of a silent hole": that holds
  only against a COOPERATING `.pth` (no `os._exit`); a HOSTILE `.pth` that
  `os._exit(0)`s before the `-c` body defeats the self-check, so ` -S` (not the
  self-check) is the load-bearing control (see round 6 / R6-F1). Every other
  false sentence was corrected here in round 4: the `MUTATION SURFACE` header,
  the "nothing is written" comment, and `P0_claim … mutation=none_in_this_block`,
  which becomes `mutation=no_filesystem_write_primitive_in_this_shell_source`,
  with `behaviour_inside_any_executed_tool_binary` added to `does_not_establish`.
  Falsified on a REAL venv with a REAL executable `.pth`: pre-fix bytes create the
  marker and still print the accepted line; repaired bytes do not.
- **F2 (MEDIUM) — CLOSED.** Row 9 is bounded by the pinned `timeout` placed INSIDE
  the cleared environment (`env -i LC_ALL=C <timeout> --signal=TERM
  --kill-after=5s 10s <systemctl> …`). rc 124/137/125 map to
  `manager_query_deadline_exceeded` / `manager_query_killed_after_deadline` /
  `bounding_wrapper_failed`, all under `system_manager_unreachable` at exit 3, with
  `budget_s` and a diagnostic-only `elapsed_s` recorded. Falsified with a real
  stalling shim: the pre-fix arm needed an external kill and emitted zero
  `P0_STOP` lines; the repaired arm returns its own bounded STOP with no external
  kill.
- **F3 (MEDIUM) — CLOSED.** The RO inventory is regenerated from the FROZEN RP7
  executable: the ten tools it pins (`stat readlink env find sha256sum systemctl
  ss curl timeout python3`) plus the P0-only `id` and `getent`. `grep` and `awk`
  are dropped — neither stage invokes them. `timeout` is now a resolved
  first-class tool; `python3` is inventoried, never executed by P0, and its pin is
  bound to the new `P0_FIXED_TRUSTED_PYTHON` freeze-gate literal with a
  python3-only canonicalisation allowance for the `/usr/bin/python3` symlink. A
  drift test re-derives the RO half from the frozen bytes; the auditor's own
  `input_pin_unknown_tool … tool=timeout` line is reproduced on the pre-fix bytes
  and a complete RP7 pin set is now accepted (`count=10 trusted_python_pin=yes`).
- **F4 (LOW/MED) — CLOSED.** `p0_resolve_passwd` exports `P0_PW_RC`, read from the
  last capture field so even a NUL-corrupted capture keeps the resolver's real
  status; both `identity_unresolvable` callers emit `rc=<n|na>`. The
  valid-no-match token was aligned by preregistering
  `state_account_resolution_unexpected` verbatim in §8.1 row 3 rather than
  changing the block, because positive absence of a dynamically allocated account
  is a host observation, not an inability to evaluate. Eight exact-WHOLE-LINE
  assertions (not substrings) cover rc-0 parse error, rc-2 no-match, rc-2
  diagnostic and other-nonzero for both accounts, each with its RED twin.

Round-3 disposition (re-audit R2 findings 1-3, nits 1-2) — full record in
`RP6_REPAIR_R3_REPORT.md`:

- **R2-F1 (MEDIUM):** the non-executable-tool STOP no longer asserts an
  invocation status it never observed. It now emits
  `tool_not_evaluable tool=<t> path=<resolved> rc=na
  detail=access_builtin_x_denied mechanism=access_builtin_x` — required token
  kept, resolved path restored, fabricated `rc=126` gone. Prereg §8.1 row 1 was
  amended to `rc=<n|na>` because P0 decides executability with shell builtins
  only and never invokes an inventory tool, so no arm of this block can carry an
  honest invocation status.
- **R2-F2 (MEDIUM):** the repair's own D026 evidence reproduces again. The
  full-block fence's RED side is pinned to the immutable `0bbc3591`
  (`= 90d8d447^`) instead of the moving `HEAD`, for both the block and the prereg
  draft, and all four recorded transcripts were re-executed and replaced. Three
  reproduce byte-identically; the fence matches after normalizing only its random
  `mktemp` root.
- **R2-F3 (LOW/MED):** row 8 now discriminates a crafted `/proc`. Each namespace
  link's followed device is compared against the root object's device — a
  namespace inode lives on the anonymous `nsfs` superblock, so a fabrication
  allocated on the root filesystem is refused as
  `namespace_link_on_root_filesystem`. Because a fabrication on any *other*
  filesystem would still pass, the evidence line states
  `procfs_identity=not_established` and the terminal claim carries
  `procfs_mount_identity_of_the_namespace_links` in `does_not_establish`.
- **Nit 1:** the `(os error 2)` classifier alternative was **dropped**, not kept,
  and its provenance corrected (see F1 below).
- **Nit 2:** the block header now names the GNU-producer assumption explicitly.

Full-block repair disposition:

- F1: the filesystem diagnostic classifier now accepts only the exact absolute
  `$P0_STAT` argv[0] prefix and the controlled C-locale GNU coreutils
  `stat`/`statx` forms. Both real-lstat missing-object arms flip from unclassified
  STOP rc 3 to the required host FAIL rc 1. **Corrected in round 3 (R2 nit 1):**
  the `(os error 2)` alternative this bullet used to call "the observed ENOENT
  form" was never observed here. `(os error N)` is a Rust `std::io::Error`
  rendering from uutils coreutils, and uutils prefixes its messages with the
  *basename* of `argv[0]`, so an absolute prefix combined with that suffix is
  unreachable. Round 3 deleted the alternative. The residual is stated in the
  block header: on a uutils host the whole class returns fail-closed at rc 3
  `path_probe_unclassified` rather than FAIL, and the shape must be re-pinned
  before such a host is preregistered.
- F2: P0 now requires frozen deploy-channel pins for user/mount/PID/network
  namespaces plus `stat -c '%d:%i' /`, validates the prelude values with reasoned
  rc-3 pre-checks and `:?` backstops, compares every live identity, and gates the
  manager query behind the comparison. Missing/unreadable input is
  `execution_domain_unattested`; mismatch is `execution_domain_mismatch`.
- F3: repeated separators in `P0_VENV_ROOT` STOP as
  `input_not_canonical_spelling` before any host object verdict.
- F4: duplicate/conflicting tool pins STOP as
  `prereg_input_malformed name=P0_TOOL_PINS duplicate=<tool>`; the count is now
  the count of distinct accepted tools.
- F5: every readlink producer uses `-v`; failed captures have nonempty bracketed
  `detail=` plus an explicit diagnostic-shape token.
- F6: getent capture uses NUL-delimited `mapfile` records with an out-of-band rc
  record; NUL emitted by the producer creates an extra record and becomes
  `identity_unresolvable` via `nul_byte_in_merged_capture`, never no-match.
- F7: `tool_not_evaluable` and `group_query_not_evaluable` are executable reason
  tokens. Every `identity_unexpected` line now uses
  `observed_numeric=<u:g> expected_numeric=<u:g> account=<a>`; §8.1 row 3 was
  aligned without changing row 9.

**Freeze gate — mandatory, same class as RP7. SIX literals after round 4.** The
following embedded literals remain `<PIN-AT-FREEZE>` and deliberately prevent an
end-to-end `P0 PASS`:

- `P0_FIXED_ATTESTED_USER_NS`
- `P0_FIXED_ATTESTED_MNT_NS`
- `P0_FIXED_ATTESTED_PID_NS`
- `P0_FIXED_ATTESTED_NET_NS`
- `P0_FIXED_ATTESTED_ROOT_MOUNT_ID`
- `P0_FIXED_TRUSTED_PYTHON` — **new in round 4**, the same deploy-channel value
  RP7 carries as `WPI_FIXED_TRUSTED_PYTHON`: the resolved non-symlink leaf behind
  `/usr/bin/python3`, because no symlinked object is admissible as a bound RO tool
  and both RO accepting adjudicators execute that exact object.

Before freeze/dispatch, the root-authorised deploy channel must mint the four exact
`readlink /proc/<attested-host-pid>/ns/<kind>` tokens, the exact
`stat -c '%d:%i' /` identity and the resolved trusted-python leaf, embed each
literal, supply identical prelude values, and re-run the whole block on the
intended guest. No value may be learned or re-pinned from the login session being
tested. `P0_MANAGER_QUERY_BUDGET_S=10` and `P0_MANAGER_QUERY_KILL_AFTER_S=5` are
NOT freeze-gate inputs — they are frozen design literals with real values, held in
the block precisely so the environment under test cannot raise its own deadline.

Local evidence, all executed in round 4 against `e93d07ad…` / 85540 B. The five
mandated fences and their results:

```text
sed -n '952,1035p'   SELF_QA_RP6.md  -> rc 0, backstop cases=4 PASS
sed -n '1678,2068p'  SELF_QA_RP6.md  -> rc 0, 39 ASSERT_MET, full-block PASS
sed -n '2286,2319p'  SELF_QA_RP6.md  -> rc 0, freeze-literal gate PASS
sed -n '2545,2989p'  SELF_QA_RP6.md  -> rc 0, 102 ASSERT_MET / 0 UNMET, R4 D026 PASS
sed -n '3353,3518p'  SELF_QA_RP6.md  -> rc 0, C13_R4B cases=27 PASS
```

The two older C13 fences (lines 664-787 and 1181-1346) assert the pre-round-4
`identity_unresolvable` grammar and are therefore RED against these bytes ON
PURPOSE — the exact assertions that break are the lines that lacked the mandatory
`rc=` field. They are retained as round records, their failing output is recorded
in `SELF_QA_RP6.md`, and they are superseded by the R4b harness, which carries all
27 of their cases with the corrected grammar. Both new fences were re-extracted
from the document and re-run: extraction byte-identical, both green, transcripts
reproduce after normalising the random `mktemp` root, with the single documented
exception of the F2 deadline arm's diagnostic-only `elapsed_s` (10 vs 11 s), which
no assertion reads. No host, SSH, network, deployment, backtest, broker, or trading
action occurred, and no commit was made.

---

# Prior status history — REPAIRED-PENDING-AUDIT, do not treat as accepted

Updated by the Codex implementer on 2026-08-10 under owner amendment A2/A2a. The
repair and its local falsification evidence are ready for independent Lead review;
the block is not frozen, accepted, dispatchable, or authorised for host execution.

- **F1 — REPAIRED BY HONEST DISCLOSURE.** The false fixed child count was removed.
  The header and terminal evidence now state the mixed environment, PATH-resolution,
  inherited-cwd and inherited-or-unset-TMPDIR surface, and explicitly do not claim
  round-1.4 probe-execution-environment binding. Full binding needs new preregistered
  inputs and is outside this bounded repair.
- **F2 — CLOSED BY LEAD ADJUDICATION; NO BLOCK CHANGE.** The existing STOP polarity
  remains correct under draft round 1.4's numeric-identity rows.
- **F3 — REPAIRED BY EXPLICIT RESIDUAL DISCLOSURE.** The terminal evidence now says
  P0 does not establish interpreter intermediate-component or symlink-target binding.
  Learning a target at runtime would violate row 18; accepting one requires a future
  preregistered target chain.
- **F4 — REPAIRED.** `:?` fail-closed backstops now follow the rc-3 pre-checks for
  `P0_EXPECT_UID`, `P0_FORBIDDEN_GIDS`, and `P0_VENV_ROOT`.

`SELF_QA_RP6.md` records literal local commands and real RED/GREEN output. No host
was contacted; no ssh, network, backtest, deployment, or trading action was run.

## C13 round — getent resolution arm (GLM-5.2 implementer, 2026-08-10)

Added by GLM-5.2 as IMPLEMENTER under the bounded C13 kickoff (round-1.4
section 8.1 rows 1–3, repair C13; Lead-adjudicated real conformance gap). Status
stays **REPAIRED-PENDING-AUDIT** — the Codex (G5) audit is outstanding, so the
block remains not frozen, not accepted, not dispatchable, and not authorised for
host execution.

- **C13 — IMPLEMENTED; QA EXECUTION PENDING.** Added one arm to `RP6-P0.sh`: a
  pinned-absolute `getent` (added to the inventory as the 12th RO tool) resolves
  `gatea` and `mtc-bridge`, each record parsed whole under the passwd grammar
  (Pattern 5; duplicate/multiline/malformed → ambiguous → STOP), admitting on
  NUMERIC uid/gid only (Pattern 8) with names as diagnostics. rc contract per
  the kickoff and the F2 polarity: getent missing/error/unparsable/duplicate →
  `identity_unresolvable` rc 3; `gatea` numeric mismatch → `identity_unexpected`
  rc 3; `mtc-bridge` valid no-match (rc 2) or numeric mismatch →
  `state_account_resolution_unexpected` rc 3. Two new preregistered inputs
  `P0_STATE_UID` (999) / `P0_STATE_GID` (988) use the same `p0_require_uint`
  rc-3 pre-check + `:?` backstop as `P0_EXPECT_UID` (F4 pattern). Claim lines
  updated honestly (11→12 tools; adds
  `name_to_numeric_resolution_of_gatea_and_mtc_bridge_via_getent`; discloses
  `nss_source_identity_of_getent_resolution`; `getent` joins the inherited-env
  set). Read-only scope, the 0/1/3 contract, STOP-vs-FAIL truthfulness, and all
  existing arms are preserved.
- **QA NOT YET EXECUTED — concrete harness blocker.** The GLM-5.2 implementer
  session's Bash tool gates interpreter/script execution (every `bash -n`,
  `bash -c`, path-script run, process substitution, brace heredoc, and
  off-tree write returned *requires approval* and was not approved this turn).
  `SELF_QA_RP6.md` therefore contains the paste-and-run RED/GREEN + backstop
  commands and the real final SHA-256/byte count, but the RED/GREEN real output
  and `bash -n` are marked **PENDING**, not fabricated. Per AGENTS.md the
  implementer reports this blocker rather than silently substituting fake
  evidence (D026 / Pattern 10; the GLM known-failure-mode of AGENTS.md rule 4).
- **Artefact (real, computed in-session).** Repaired `RP6-P0.sh` SHA-256
  `cfdb23b8834a783638723c54cf632973c1cc20c5fb676cb6d310a9d43b9acf1c`, 54109
  bytes (baseline `6c5b8945…766f7`, 44979 bytes). Three files touched only
  (`RP6-P0.sh`, `SELF_QA_RP6.md`, this file); nothing committed.

**Required to close C13:** run the C13 commands in `SELF_QA_RP6.md` in an
unhindered Git Bash process (or have Codex run them at G5), paste the real
RED/GREEN output, and confirm `bash -n` PASS — then the Codex G5 audit.

**Lead QA execution, 2026-08-10 — the blocker above is CLEARED.** The Lead ran
the full C13 QA in an unhindered Git Bash: arm RED/GREEN 5/5 CASE_OK (GREEN
rc 0; four REDs rc 3 with the exact preregistered reason tokens); backstop
2/2 GREEN after a Lead harness correction (the drafted C13 backstop caller fed
`sed` no input and its summary was ungated — both defects recorded with the
as-drafted failing run in `SELF_QA_RP6.md`, then fixed); `bash -n` PASS; hash
and byte count re-verified identical to the implementer's record
(`cfdb23b8…`, 54109 B). Real outputs pasted into `SELF_QA_RP6.md`. Remaining
to close: the independent Codex G5 audit of the C13 arm.

## C13 round 3 — Codex audit repair (Claude Opus 5 implementer, 2026-08-10)

The Codex G5 audit of the C13 arm returned **BLOCK, 3 findings**
(`RP6_C13_CODEX_AUDIT_2026-08-10.md`: V2/V3/V5 FAIL, V1/V4/V6 PASS). GLM-5.2, the
C13 implementer, is quota-blocked, so Claude Opus 5 executed this bounded repair
round as implementer; it neither authored nor audited the C13 arm. Status stays
**REPAIRED-PENDING-AUDIT** — the block is not frozen, not accepted, not
dispatchable, and not authorised for host execution, and the Codex re-audit is
outstanding.

- **F1 (HIGH) — REPAIRED IN THE BLOCK.** `p0_resolve_passwd` accepts getent
  `rc 2` as `nomatch` only when the complete merged capture is empty, this
  interface's exact valid-no-match shape. `rc 2` carrying any byte (NSS
  diagnostic, partial record, module warning) is now `error`, so the caller emits
  `identity_unresolvable … rc 3` instead of asserting a positive absence it never
  observed. `P0_PW_DIAG` on the surviving no-match path records
  `empty_capture_at_rc2`. All other parser arms and both caller `case` statements
  are byte-identical, and the genuine `mtc-bridge` valid no-match still yields
  `state_account_resolution_unexpected observed_numeric=absent` (regression-tested).
- **F2 (MEDIUM) — REPAIRED IN THE QA.** The two earlier C13 fences are re-labelled
  SUPPLEMENTAL in place, and two D026 harnesses were added and executed locally.
  Harness 1 (16 cases) no longer calls the arm: it appends the block's own
  top-level driver lines, matched as exact whole lines out of the source bytes, so
  the block decides whether the arm runs; it then runs one assertion set across
  three variants — R3-repaired bytes, pre-R3 bytes (`cbaf3ec8`, `cfdb23b8…`), and
  bytes with the production integration call deleted. Deleting that call takes all
  three arm assertions to `ASSERT_UNMET`; the pre-repair bytes fail every F1
  assertion and are separately recorded emitting the defective
  `observed_numeric=absent` verdict. Harness 2 (4 cases) adds the mutation that
  removes each new `:?` backstop itself. Both harnesses check assertion POLARITY,
  so a surviving mutant fails the run.
- **F3 (MEDIUM) — REPAIRED IN THE BLOCK.** The "NUMERIC IDENTITY ONLY" header no
  longer claims that no name is looked up or captured and that the block asks the
  resolver database nothing. It states the truth: admission is numeric only and no
  name is ever compared or asserted; two names ARE queried via the pinned
  `getent passwd`; the returned name/gecos/home/shell fields are diagnostics no
  verdict depends on; NSS source identity is not established.
- **Artefact (real, computed in-session, Git Bash).** Repaired `RP6-P0.sh`
  SHA-256 `ef205e2064caa0cb1493abf037ce9d435f2bf8f6259c5bb3fc4964d1abb2b4b9`,
  55467 bytes (pre-R3 `cfdb23b8…`, 54109 bytes; diff 34 insertions / 12
  deletions, one file). `bash -n` rc 0, `BASH_N=PASS`. Harness 1 process rc 0,
  `C13_R3_ARM_QA_SUMMARY cases=16 result=PASS`; harness 2 process rc 0,
  `C13_R3_BACKSTOP_QA_SUMMARY … cases=4 result=PASS`. Both fenced commands in
  `SELF_QA_RP6.md` were re-run from the document itself and diffed byte-for-byte
  against the pasted output.
- **Scope.** Four files touched (`RP6-P0.sh`, `SELF_QA_RP6.md`, this file,
  `RP6_C13_REPAIR_R3_REPORT.md`); nothing committed; no host contacted and no
  network command run. Read-only scope, the rc 0/1/3 contract, and every
  pre-existing arm are preserved.

**Required to close C13:** the independent Codex re-audit of the R3 bytes
`ef205e20…` (55467 B) against `RP6_C13_CODEX_AUDIT_2026-08-10.md`. — DONE: that
re-audit ran and returned BLOCK with 2 findings; see the round-4 section below,
which supersedes this requirement.

## C13 round 4 — Codex re-audit repair (Claude Opus 5 implementer, 2026-08-10)

The Codex re-audit of the R3 bytes returned **BLOCK, 2 findings**
(`RP6_C13_REAUDIT_CODEX_2026-08-10.md`: V1 and V4 FAIL, V2/V3/V5 PASS). This is the
last bounded round under the T0 cap. Claude Opus 5 executed it as implementer; it
neither authored nor audited the C13 arm. Status stays **REPAIRED-PENDING-AUDIT** —
the block is not frozen, not accepted, not dispatchable, and not authorised for host
execution.

- **Finding 1 (HIGH) — REPAIRED IN THE BLOCK.** `p0_resolve_passwd` captured getent
  with a plain `$( … )`, which deletes trailing newlines, so the `[ -n "$raw" ]`
  emptiness test could not tell a truly empty rc-2 capture from a newline-only one
  and admitted the latter as a valid no-match. The capture now appends a sentinel
  byte INSIDE the substitution and strips it afterwards, so the complete merged
  stream survives; `had_bytes` is decided on those preserved bytes before any
  normalization. A newline-only rc-2 capture is now `error` with
  `P0_PW_DIAG=newline_only_capture_at_rc2`, and the caller emits
  `identity_unresolvable … rc 3` for both accounts. getent sits on the left of `||`
  inside the substitution so an inherited `set -e` cannot kill the subshell before
  the sentinel is written, and its own rc is carried out by re-exiting the subshell
  with it. If the sentinel is missing anyway, the capture was truncated by something
  other than getent and the outcome is `error` / `capture_sentinel_lost` — fail
  closed, never a no-match. After the emptiness question is answered `raw` is
  normalized back to the value plain command substitution used to produce, so the
  rc-0 record parse and every diagnostic string are byte-identical to the
  R3-audited behaviour.
- **Finding 2 (MEDIUM) — NO REPAIR, LEAD-ADJUDICATED.** The extra committed
  provenance log was added by the Lead at commit time, not by the round-3
  implementer; the Lead recorded it as an accepted Lead-side deviation. Out of this
  round's scope; the file was not touched.
- **Same-pattern sweep.** `p0_resolve_passwd` is the only site in the block that
  adjudicates rc 2 as its own outcome (one `2)` case arm in the file). Every other
  capture site treats any non-zero rc as an error, and every other emptiness test —
  e.g. `p0_capture_numeric`'s `[ -n "$raw" ] || p0_stop identity_probe_empty` —
  fails CLOSED, so newline stripping there can only cause a STOP, never a false
  admission. No other site was changed.
- **QA (real, local Git Bash, D026).** `SELF_QA_RP6.md` harness 1 was extended, not
  replaced: all sixteen R3 cases verbatim, plus a fourth source variant `prer4` (the
  committed R3 bytes `ef205e20…`), three newline-only rc-2 shim modes
  (`mtc_rc2_newline`, `mtc_rc2_newlines3`, `gatea_rc2_newline`), the `nocall`
  mutation applied to the new case as well, and a probe that prints the auditor's own
  markers. Result: `C13_R4_ARM_QA_SUMMARY cases=27 result=PASS`, process rc 0, 25
  `CASE_OK` + 2 `PROBE_OK`, zero `CASE_BAD`. The new fixture is GREEN on R4 bytes
  (`identity_unresolvable … detail=[newline_only_capture_at_rc2]` rc 3) and RED on
  the R3 bytes, which are separately recorded emitting the defect
  (`state_account_resolution_unexpected … observed_numeric=absent`). The probe
  reproduces `FALSE_NOMATCH_REPRODUCED=yes` / `REQUIRED_ERROR_OUTCOME_PRESENT=no` on
  R3 bytes and `no` / `yes` on R4 bytes. Harness 2 was re-run unchanged against the
  R4 bytes: process rc 0, `C13_R3_BACKSTOP_QA_SUMMARY … cases=4 result=PASS`.
- **Artefact (real, computed in-session, Git Bash).** Repaired `RP6-P0.sh` SHA-256
  `bff3c86e6e9b565c55da34580284f22c80253d9e931d879fd749459bac85b7cf`, 57441 bytes
  (pre-R4 `ef205e20…`, 55467 bytes; diff 36 insertions / 5 deletions, one file).
  `bash -n RP6-P0.sh` rc 0, `BASH_N=PASS`. The extended harness was re-run from the
  document itself (`sed -n '1159,1324p' SELF_QA_RP6.md | bash --noprofile --norc`)
  and its pasted output is that run.
- **Scope.** Four files touched (`RP6-P0.sh`, `SELF_QA_RP6.md`, this file,
  `RP6_C13_REPAIR_R3_REPORT.md`); nothing committed; no host contacted and no network
  command run. Read-only scope, the rc 0/1/3 contract, and every pre-existing arm are
  preserved.

**Required to close C13:** the independent Codex re-audit of the R4 bytes
`bff3c86e…` (57441 B) against `RP6_C13_REAUDIT_CODEX_2026-08-10.md`.
