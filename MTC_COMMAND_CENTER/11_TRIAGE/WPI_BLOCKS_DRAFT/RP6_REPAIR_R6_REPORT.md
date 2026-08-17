# RP6-P0 round-6 repair report — three Claude flagship re-audit findings (F1–F3)

Date: 2026-08-10
Implementer: GLM-5.2 (fresh session)
Auditor of this block: Claude `claude-opus-5`, `xhigh` (re-audit
`RP6_CLAUDE_REAUDIT_R5_2026-08-10.md`). Claude is this block's auditor for these
findings, so implementer/auditor separation holds; GLM-5.2 also implemented
round 5, which the kickoff permits.
Tier: **T0** — defensive staging preflight / host execution-domain surface.
Authority: owner grant #7 (2026-08-10) lifts the T0 round cap for this block set
— rounds continue until both flagships accept; the acceptance standard is
unchanged. DRAFT. Not frozen, not hashed into any kit, not dispatchable, carrying
NO host-contact authority. No host, SSH, network, deployment, broker, backtest,
Pine, parity, MTC, or trading action was performed. No commit was made.

## Inputs

- `RP6_CLAUDE_REAUDIT_R5_2026-08-10.md` — findings F1–F3 with executed
  falsifications and "Required repair" text. That text BINDS.
- `RP6_CLAUDE_FINAL_AUDIT_2026-08-10.md` — the original statement of Finding 1.
- `RP6-P0.sh` — target. Baseline (verified BEFORE the first edit):
  SHA-256 `490e3e4edfec811dee3dc90c6693e8ebeb865eb946a431ff017de58e66f0ce5f`,
  89029 B, commit `ae2c79ed`.
- `KICKOFF_RP6_REPAIR_R6.md` — the bounded round-6 contract.
- `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding pre-read (Patterns 4, 5, 9, 10).

## Artefact (real, computed in-session by read-only tools)

- Repaired `RP6-P0.sh` SHA-256:
  `75db028e76438bc88caba19b9c3b6411e5f573f7b6c2bd13c3883d24e4389570`
- Repaired `RP6-P0.sh` byte count: `93421` (was `89029`; +4392 B = the F2 grammar
  gate + `set -f`, the F3 glob gate, `p0_lookup`'s `set -f`, and the corrected
  comments). LF-only, no BOM; `tr -cd '\r'` = 0 — the edits introduced no CR.
- `bash -n RP6-P0.sh`: **PENDING** — the GLM-5.2 session gates `bash -n` and
  script execution (identical to the C13 and round-5 GLM rounds' recorded
  blocker). The Lead must execute it in an unhindered Git Bash, as it did for
  round 5.
- The five edits are grep-confirmed at their sites; the launch line is still
  `-I -S -c`; CR bytes = 0; no arm outside the three named sites changed.
  `shellcheck` is not installed and was not run.

## The three fixes

### F1 (MEDIUM, carried from round 4) — the "` -S` cannot be silently deleted" claim was false

**Root cause.** The block's interpreter-section comment (and three evidence
sentences that vouched for it) claimed that because the child verifies its own
`sys.flags.isolated`/`sys.flags.no_site`, deleting ` -S` from the launch line
"cannot silently restore the hole — it produces a named STOP." That self-check
runs INSIDE the `-c` body. A hostile `.pth` in the venv's `site-packages` runs at
`site` startup when ` -S` is removed, BEFORE the `-c` body is compiled, so it can
write the forged `P0PY` line and `os._exit(0)` and the self-check never runs.
Against such a `.pth` the no-`-S` mutant returns rc 0 with no STOP and the forged
accepted line (the auditor's `MUTANT_MINUS_S` reproduction: rc 0, marker CREATED,
`reported_version=9.9`). The round-4/round-5 `F1_MUTANT_*` assertions passed only
because the fixture `.pth` COOPERATED — it wrote a marker but did not `os._exit`,
so the `-c` body still ran and the self-check fired (Pattern 10 — evidence that
cannot fail).

**Repair.** Retract the false claim and state the truth at every in-scope site:
the child's `sys.flags` self-check guards only ACCIDENTAL flag-word loss (the
case where the flag words are dropped but the interpreter still reaches the `-c`
body, which a cooperating venv permits); it is NOT a substitute for ` -S`; ` -S`
itself is the control that closes the channel (with it present, `site` startup
never runs and the hostile `.pth` is never processed). Replace the
cooperating-fixture evidence with an ADVERSARIAL `.pth` (writes marker + forged
`P0PY 9.9` + `os._exit(0)`): under it the no-`-S` mutant is NOT caught (rc 0,
marker created, forged line, no STOP), which the claim now states plainly.

In `RP6-P0.sh` the change is COMMENT-ONLY at the interpreter section (~lines
1493-1525); the launch line `"$py" -I -S -c …` (~line 1561) and every executable
arm are byte-identical. In `SELF_QA_RP6.md` the R4 prose and the "what each arm
establishes" note are corrected in place and a round-6 disclosure is added at the
`F1_MUTANT_*` assertions; the cooperating fixture is superseded by the R6-F1
adversarial-`.pth` harness. In `STATUS_RP6_P0.md` the round-4 F1 bullet is
narrowed.

**Out-of-scope site, disclosed.** The audit named a fourth site,
`RP6_REPAIR_R4_REPORT.md:88`. That file is NOT in this round's four-file allowlist
(`RP6-P0.sh`, `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, this file), so it was NOT
touched and still carries the stale sentence. The residual is flagged for the
Lead/owner; its bytes are unchanged.

### F2 (MEDIUM, NEW) — `gids` was pathname-expanded before validation (the F3 class, at the host-response parser)

**Root cause.** `p0_record_identity` did `for g in $gids` (unquoted) and only
then grammar-checked each item, so pathname expansion ran on the raw `id -G`
value BEFORE the per-item check — the identical defect class the round-5 F3
repair closed for `P0_FORBIDDEN_GIDS`, unrepaired at the more load-bearing site
where the host's own answer is parsed. Three wrongs followed: (1) the verdict was
cwd-dependent (`*` STOPped in an empty cwd but was admitted in a cwd holding a
numeric-named entry); (2) the printed evidence asserted `form=numeric_only` about
a non-numeric raw string (`gids=[0*]`); (3) the whole-word intersection matched
the RAW `" $gids "` string, so `" 0* "` never contained `" 0 "` and
`capability_wider_than_ledger` did not fire for a response that literally began
with the forbidden gid (the auditor's `GLOB_HIDES_ROOT`).

**Repair.** Apply the F3 pattern to `gids` at `RP6-P0.sh` ~lines 903-924:
grammar-check the COMPLETE raw capture against `*[!0-9[:space:]]*` BEFORE any
expansion, and run the per-item split inside `set -f`. The per-item check is
retained as the second layer. Result: `*`, `0*`, `?` STOP as
`group_query_not_evaluable rc=0 detail=[response_not_decimal_gid_list]`
identically in an empty and a numeric-named cwd; `HONEST_ROOT_GROUP` (`1001 0`)
still STOPs with `capability_wider_than_ledger gid=0`; `HONEST_CLEAN` (`1001 100`)
is still admitted. All three wrongs are gone (a laundered value now STOPs before
it reaches the intersection, so the whole-word match always sees a clean numeric
list).

### F3 (LOW/MEDIUM, NEW) — pin paths could carry glob metacharacters; `p0_lookup` split was not noglob

**Root cause.** The pin-path charset gate at `RP6-P0.sh:492-495` refused only
non-printable/whitespace bytes, so `*`, `?`, `[` were admitted into a pin (the
auditor's `stat=/usr/bin/sta*` was accepted at rc 0). `p0_lookup` then split its
map UNQUOTED at ~line 230, under a comment at ~lines 223-226 that certified the
expansion "deliberate and safe" against word splitting but was silent about
pathname expansion, which the same unquoted expansion also performs.

**Repair.** Two defenses plus the comment, at `RP6-P0.sh` ~lines 222-247 and
~513-524: (1) refuse `*`, `?`, `[` at the pin charset gate
(`expected=printable_without_glob_metacharacters`); (2) run `p0_lookup`'s split
under `set -f` (defense in depth over every map, restoring glob to the block
default ON on both exits, matching the two existing `set -f`/`set +f` pairs); (3)
correct the comment so it certifies safety against pathname expansion, not only
word splitting. The auditor's `stat=/usr/bin/sta*` pin flips from admitted (rc 0)
to a glob-metacharacter STOP (rc 3); a clean pin is still admitted.

## Preservation (every arm not named above is byte-identical)

- **rc 0/1/3 contract, STOP-vs-FAIL truthfulness, numeric identity, read-only
  scope:** unchanged. F1 is comment-only; F2 adds a grammar STOP and a `set -f`
  bracket (more STOPs for malformed input, identical behavior for valid input);
  F3 adds a charset STOP and a `set -f` bracket (identical behavior for clean
  maps/pins). No accepting arm changed its output.
- **Interpreter arm, row-8 execution-domain gate, row-9 manager bound, resolver,
  evidence binding, numeric-identity discipline:** byte-identical to the round-5
  bytes (the seven round-4→5 change hunks are untouched; the five round-6 hunks
  are confined to the three named sites).
- **Codex round-5 F1/F2/F3 closures:** stand (no round-6 edit touches them).
- **Freeze gate:** unchanged in COUNT — still six `<PIN-AT-FREEZE>` literals, so
  no end-to-end `P0 PASS` is possible and nothing here is dispatchable.

## Evidence (D026 — REAL RED/GREEN, PENDING Lead execution)

The session gates `bash -n` and script execution, so the R6 evidence is recorded
as **PENDING** rather than fabricated (D026 / Pattern 10; the GLM known-failure-
mode of AGENTS.md four-auditor rule 4). `SELF_QA_RP6.md` §R6 carries three
self-contained, marker-delimited harnesses that the Lead runs by
`sed -n '/R6_FX_HARNESS_BEGIN/,/R6_FX_HARNESS_END/p' SELF_QA_RP6.md | bash --noprofile --norc`:

- **R6-F1** — REAL `python -m venv`, REAL interpreter, ADVERSARIAL `.pth`
  (`os._exit(0)`). Drives the block's verbatim `p0_assert_interpreter_executable`
  for delivered (`-I -S`) vs mutant (`-I -c`, `-S` deleted). GREEN: rc 0, marker
  no, real version (`-S` neutralises the `.pth`); RED mutant: rc 0, marker yes,
  forged `9.9`, no STOP (self-check defeated). The contrast proves ` -S` is
  load-bearing and the self-check is not a substitute for it.
- **R6-F2** — REAL shim `id` and REAL cwd-driven pathname expansion, driving the
  block's verbatim `p0_record_identity` (repaired) vs a round-5-defect replica.
  `*`/`0*`/`?` in a numeric cwd admit on the defect (RED) and STOP identically in
  both cwds on the repair (GREEN); `HONEST_ROOT_GROUP` still STOPs with
  `capability_wider_than_ledger gid=0`.
- **R6-F3** — the pin validator (round-5 replica vs repaired) and `p0_lookup`
  (verbatim repaired vs round-5 replica). `stat=/usr/bin/sta*` flips from admitted
  to a glob STOP; `p0_lookup`'s `a=b*` split stops being rewritten by the cwd.

Each harness has its expected-polarity table in `SELF_QA_RP6.md` §R6. The Lead
must also re-run the five prior mandated fences (backstop, full-block D026,
freeze-literal gate, R4 D026, C13 R4b) against the new bytes to confirm no
regression in the unchanged arms.

## Scope

Four files touched only (`RP6-P0.sh`, `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, this
file); nothing committed; no host contacted and no network command run. Read-only
scope, the rc 0/1/3 contract, STOP-vs-FAIL truthfulness, numeric identity, and
every pre-existing arm are preserved.

## Required to close

Independent Claude (`claude-opus-5`, `xhigh`) re-audit — and, for dispatch
blockade, Codex (`gpt-5.6-sol`, `xhigh`) — of the round-6 bytes
`75db028e…` (93421 B) against `RP6_CLAUDE_REAUDIT_R5_2026-08-10.md`, after the
Lead executes the PENDING `bash -n` and the three R6 harnesses.
