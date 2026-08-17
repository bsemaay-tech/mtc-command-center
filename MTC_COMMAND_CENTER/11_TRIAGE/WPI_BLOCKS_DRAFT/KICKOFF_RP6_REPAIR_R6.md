# KICKOFF — RP6-P0 round 6: three required repairs from the Claude flagship

You are GLM-5.2, IMPLEMENTER (Claude is this block's auditor for these findings, so
separation holds; you also implemented round 5, which is fine). Working directory:
C:\LAB\Tradingview_LAB_CLEAN. No host contact, no network. Do not commit.

Round 6 is authorised: owner grant #7 (2026-08-10) lifts the T0 round cap for this
block set — rounds continue until both flagships accept. The acceptance STANDARD is
unchanged.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/`)

1. `RP6_CLAUDE_REAUDIT_R5_2026-08-10.md` — Findings 1, 2, 3 with executed
   falsifications and "Required repair" text. That text BINDS.
2. `RP6_CLAUDE_FINAL_AUDIT_2026-08-10.md` — the original statement of Finding 1.
3. `RP6-P0.sh` — target. Current: SHA-256
   `490e3e4edfec811dee3dc90c6693e8ebeb865eb946a431ff017de58e66f0ce5f`, 89029 B,
   commit `ae2c79ed`. Verify before editing.
4. `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, `RP6_REPAIR_R5_REPORT.md`.
5. `../DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding pre-read.

## The three repairs

- **Finding 1 (MEDIUM, carried from round 4 — round 5 neither addressed nor disclosed
  it).** The block claims `-S` cannot be silently deleted; an adversarial `.pth` can
  defeat the child self-check and forge the accepted line, and the `F1_MUTANT_*`
  assertions pass only because the fixture `.pth` cooperates (Pattern 10 — evidence
  that cannot fail). Repair BOTH halves: (a) correct the false claim in the block's
  source comments and in the two evidence documents that vouch for it, stating only
  what the delivered launch actually establishes; (b) replace the cooperating fixture
  with an ADVERSARIAL `.pth` that actively tries to forge the accepted output and
  defeat the self-check — the mutant (no `-S`) must be caught, and if the self-check
  genuinely cannot detect a hostile `.pth`, say so plainly in the claim rather than
  asserting protection the code does not provide.
- **Finding 2 (MEDIUM, NEW).** Apply the round-5 F3 pattern to `gids`: grammar-check
  the COMPLETE raw `id -G` capture against digits-plus-separators BEFORE the split,
  and run the split inside `set -f`. D026 arm must drive `*`, `0*` and `?` in BOTH an
  empty cwd and a numeric-named cwd; repaired bytes must STOP identically in both
  (`group_query_not_evaluable`), and `HONEST_ROOT_GROUP` (`id -G` = `1001 0`) must
  still STOP with `capability_wider_than_ledger gid=0`. Note the three separate wrongs
  the auditor identified — cwd-dependent verdict, false `form=numeric_only`, and the
  whole-word intersection matching the RAW string so `" 0* "` never matches `" 0 "`.
  All three must be gone.
- **Finding 3 (LOW/MEDIUM).** The pin-path charset gate at `:492-495` admits `*`, `?`
  and `[`; `p0_lookup` then splits its map unquoted at `:230`. Refuse glob
  metacharacters in pin paths and/or disable pathname expansion around that split, and
  correct the "deliberate and safe" comment so it covers globbing, not only splitting.

Preserve: rc 0/1/3 contract, STOP-vs-FAIL truthfulness, numeric identity, read-only
scope, every arm not named above byte-identical.

## Deliverables

Repaired `RP6-P0.sh` + `SELF_QA_RP6.md` (REAL RED/GREEN per fix; the auditor's own
fixtures must flip) + `STATUS_RP6_P0.md` + `RP6_REPAIR_R6_REPORT.md`. **Write UNIX LF
only.** Report new SHA-256 + byte count. Touch ONLY those four files.

If your session gates `bash -n` or script execution, mark that evidence PENDING and say
so — do NOT fabricate output. The Lead will execute it, as it did for round 5. Also:
round 5 silently left Finding 1 unaddressed; this round must state the disposition of
EVERY finding explicitly, including any you decide not to repair and why.
