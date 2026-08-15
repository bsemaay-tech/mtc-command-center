SOUND-WITH-GAPS

# Adversarial design review — Pathscope Option C occurrence-accounting redesign

Subject: `C:\PSC\MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\PATHSCOPE_OPTION_C_DESIGN_2026-08-15.md`
(design lines cited as `design:<line>`; that worktree is not shared and was read only).
Baseline sources: `pathscope_prover.py`, `composite_pathproof.py`, `SELF_QA_PATHSCOPE.md`
in `C:\RO\MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\`, plus the T1 audit and
owner-boundary records. Read-only review; nothing was executed; nothing in `C:\RO` was
touched. All rc derivations below are static traces against the R5 source, cross-checked
against the audit's measured outputs wherever the two overlap.

## Attack 1 — can an input reach `PASS rc=0` with something dangerous unaccounted?

**What I tried.** I enumerated every construct that binds a shell variable or carries an
assignment-shaped value, and for each asked: does it reach one of §3.1's three admission
sites (design:108-118), or does it STOP? The three sites check out against the source:
assignment prefix (`pathscope_prover.py:2564-2566`), `env` post-expansion
(`pathscope_prover.py:1788-1791`), and declaration builtins both raw and expanded
(`pathscope_prover.py:1290-1307`).

**Attacks that failed (evidence the boundary is tight where the design owns it):**

- Quoted declaration operands (`export "X=/etc/x"`) are admitted via the expanded
  `ASSIGN_RE` arm (`pathscope_prover.py:1303-1308`) — the C-4 closure survives.
- A pinned-constant override is still admitted and separately STOPs
  (`pathscope_prover.py:1243-1248`).
- An un-expandable raw RHS is admitted per §3.1 and keeps the current coverage STOP
  (`pathscope_prover.py:1346-1351`) — `dynamic`, `nested`, `backtick` stay rc 3.
- Array assignments STOP (`pathscope_prover.py:2873-2881`), `X+=…` STOPs
  (`pathscope_prover.py:2820-2825`), `env -S` STOPs (`pathscope_prover.py:1768-1773`),
  `eval` is forbidden (`pathscope_prover.py:2587-2590`), a dynamic `env` operand STOPs
  (`pathscope_prover.py:1744-1749`), and subshells, brace groups, pipelines, case-arm
  bodies, and function bodies all route through `analyze_command`
  (`pathscope_prover.py:2690-2704`, `2831-2864`).
- `"$X"=1` as a command word becomes an opaque-command STOP (`pathscope_prover.py:2671-2677`);
  `let X=…` only ever binds arithmetic values; `read`/`for` variables are dynamic and
  fail closed at use.

**The attack that succeeded.** `: ${LD_PRELOAD:=/etc/evil.so}` — and the same shape on
`true`, `echo`, `printf` — reaches `PASS rc=0` under R5 **and under Option C**, with the
loader-path string bound into the environment and zero rows. Trace: the operand token
reaches `scan_args` (`pathscope_prover.py:1555-1562`); `expand_word` rejects the `:=`
mode ("unsupported parameter expansion", `pathscope_prover.py:615-617`); `scan_args` then
suppresses the issue because the command is path-free (`pathscope_prover.py:1564-1570`,
`path_free` at `pathscope_prover.py:813-826`; `:`, `true`, `echo`, `printf` all qualify —
`pathscope_prover.py:1023,1048-1049`). In bash, `${X:=v}` performs an assignment; the
prover neither admits it (it is none of §3.1's three sites) nor STOPs it. The prover's own
C-1 rationale names `LD_PRELOAD` as the threat this lane exists to close
(`pathscope_prover.py:1320-1330`). Conservation over admitted values is silent here by
construction. This contradicts the design's own stated principle that an assignment shape
which cannot be established "remains the existing coverage STOP; it is not silently
promoted into this universe" (design:119-124). Residual 1 (design:535-539) frames
leftover sinks as parser/grammar defects, but this is an *assignment* construct escaping
the assignment universe — the exact seam the redesign owns — so the residual does not
cleanly cover it. See finding 1.

## Attack 2 — is the closed disposition set actually closed?

**What I tried.** I hunted for a member that fits no bucket cleanly, or where a
convenient bucket is reachable.

**Failed attacks (the set holds as prose):** the bare colon member (`evil.so`) falls to
the default arm `member_classifier_no_terminal_rule` (design:252,270); a quoted newline
activates the words reading unconditionally (design:173-175); a glob member dies at
normalization (`pathscope_prover.py:686-687`); a URI without a static port dies at
`normalize_network` (`pathscope_prover.py:708-710`); empty whole and empty colon members
are distinguished (§5 steps 3 vs 6, design:262,267); `mailto:root` (colon outside any
`scheme://authority`) splits into two bare colon members → unresolved, not silently
scalar.

**Two real weaknesses:**

1. The runtime invariant set never binds a disposition/reason to a reading or shape.
   §4 (design:207-216) verifies counts, IDs, enum closure, and provenance; §10.5's seven
   mutations (design:518-529) never falsify "mark a words member or a bare colon member
   `ALLOWED_WITH_REASON reason=whole_scalar_no_lexical_sink`". §5's ordering forbids it
   in prose (design:273-275), but prose-only rules are what failed four consecutive
   cycles — the design's own premise is that accepting conditions must be
   runtime-checkable (design:29-31). A lazy or buggy classifier can PASS every invariant
   while re-admitting F1 through the front door. See finding 2.
2. "Non-path whole container" (§5 step 5, design:265-266) is undefined against a whole
   like `bare.so:/etc/escape.so`, which contains `/` and is classified `fs` by the
   current kind test (`pathscope_prover.py:1394-1397`). Step 4 (path occurrence, allowlist
   + provenance) and step 5 (container) both end non-PASS for this shape, so there is no
   soundness hole — but the design should pin the path-shape test, because the bucket
   choice changes c2_list_bare_first's row set. See finding 8.

## Attack 3 — is the conservation check itself falsifiable?

**What I tried.** Look for a trivial satisfaction of the counters.

- "Emit `UNRESOLVED_FAIL_CLOSED` for everything": conserves trivially but cannot PASS
  (§4 condition 4, design:236) — not exploitable; the trivial implementation is boxed
  into rc 3. Failed attack.
- Each §10.5 arm maps to a named invariant: deleted/duplicated append → Counter equality;
  unknown member_id → the outside-M(v) clause; unknown enum → closed-set check;
  dedupe-before-identity → per-reading cardinality (§3.3, design:187-191); non-overlapping
  constant source → §6 equality; suppressed MEMBER line → printed-record reconciliation
  (§12.3, design:580). Failed attack — the plan is genuinely discriminating on these axes.

**Two falsifiability gaps:**

1. Reason/reading consistency is un-falsifiable today (attack 2, finding 2).
2. `member_id` uniqueness is asserted only *per value* (design:212). A cross-value ID
   collision satisfies every §4 equation — both Counters carry the collision twice — and
   would be caught only by the composite's duplicate-ID rejection (design:370-372), which
   exists only after the §2.3 integration and is downstream of PASS selection. See
   finding 5.

## Attack 4 — provenance binding and occurrence-ID collisions

**What I tried.** Construct two distinct source positions with colliding IDs.

- Same-line duplicate assignments: distinct value ordinals; §10.4 row 4 (design:514)
  already covers it. Failed attack.
- Two command substitutions on one line: `lexer.substitutions` is ordered and each nested
  analyzer is merged once (`pathscope_prover.py:268`, `2925-2932`); with per-instance
  analyzer ordinals the prefixes differ. Failed attack — *provided* the scope prefix is an
  instance ordinal. Design:182-185 says the prefix "distinguishes root, nested shell, and
  substitution analyzers" — if an implementer reads that as a *kind* label rather than a
  per-instance ordinal, two substitution analyzers collide and finding 5's gap becomes
  live.
- `merge` rebasing: design:77 never rewrites IDs — correct. But the ID example embeds a
  line field (`A0.V0007.colon.M0002@15:15`, design:184); for merged nested occurrences
  the ID's line will disagree with the rebased display line. Cosmetic, but an auditor
  recomputing from records will trip on it. See finding 9.
- Provenance semantics: segment-intersection is right for a split inside one expansion
  (both members legitimately name the variable, design:293-296); the `{PWD}`-only rule
  for empties removes the current union laundering at `pathscope_prover.py:1509`; the
  zero-width empty anchor makes the expected==actual equality vacuous for empties, which
  is acceptable because their sources are pinned by rule, not by intersection.

F2 stays closed; I could not construct an ID collision under the design as written.

## Attack 5 — the eight residuals

- **Residual 2 (bare whole scalar) — plainly: it leaves a usable hole.** Single-token
  consumer-search values still PASS: `LD_PRELOAD=evil.so`, `LD_LIBRARY_PATH=.` or
  `=evilsubdir` (no colon → single member), `PYTHONPATH=dir`, `GIT_SSH_COMMAND=toolname`
  all take §5 step 7 (design:268-269) and return rc 0. It is not a regression — R5 is
  identical via `kind == "bare"` (`pathscope_prover.py:1491-1497`) — and it is disclosed
  (design:539-546). One caveat: the retained PASS reason string
  `closed_and_allowlisted_lexical_argv_scope` (which the composite hard-requires,
  `composite_pathproof.py:2375-2376`) now asserts more than §11.2 admits; the honest
  claim lives in the MEMBER reason tokens. Finding 6.
- **Residual 6 (generic Issue dedupe) — no usable hole.** The dedupe
  (`pathscope_prover.py:1131-1134`, `2961-2964`) collapses multiplicity, never
  existence: identical keys merge N→1 ≥ 1, so any real issue still forces rc 3. The
  240-char expression truncation (`pathscope_prover.py:1132`) can merge two distinct
  long expressions — a count-only effect, and the composite counts printed rows
  consistently (`composite_pathproof.py:2322-2336`). Members never touch that container
  (design:83-85, 328-330), so F3 stays closed for members. Finding 7.
- **Residual 1:** honest as far as it goes, but it must not be read to absorb the
  Attack-1 `${X:=v}` gap — that is an assignment construct, not foreign grammar.
- **Residuals 3, 4, 5, 7:** honestly scoped and correctly bounded (over-rejection is
  disclosed via c2_benign_words; option paths are terminal-unresolved; token-local
  offsets are stated as a limitation, not hidden; no host proof is added).
- **Residual 8:** see Attack 6 — "mandatory and mechanical" is the one false word in the
  section.

## Attack 6 — residual 8 / the composite parser integration

I read `composite_pathproof.py:2129-2391`. The design's factual claims are accurate:
unknown-record rejection via the prefix tuple (`composite_pathproof.py:2287-2293`), header
cardinalities (`2294-2305`), count reconciliation (`2306-2336`), disposition-enum checks
(`2337-2348`), terminal rc/reason adjudication (`2350-2376`).

It is **not** merely additive, and calling it "mechanical" (design:97, 563-564) hides
four concrete conflicts:

1. **Branch selection keys off the five issue counts and three hard-coded terminal
   reasons** (`composite_pathproof.py:2354-2376`). Option C deliberately moves member
   dispositions out of the `Issue` container (design:83-85, 328-330), which creates
   rc-3-with-zero-issue-count outputs (e.g. c2_benign_words after §9.3.1). Those fall
   into the composite's PASS/FAIL arms and STOP on reason mismatch. The composite needs a
   fourth arm and a specified reason-token table.
2. **The prover's terminal reason for member-unresolved rc 3 is nowhere specified.**
   §8 gives only `accounting_invariant_failed` (design:361); the composite requires an
   exact reason per branch (`composite_pathproof.py:2361-2362,2368-2369,2375-2376`).
3. **§8's fault block omits the standard headers.** The block at design:357-362 prints
   no `PATHSCOPE shell=`/`semantics=`/`resolved_`/`unresolved_` lines, yet the composite
   requires exactly one of each (`composite_pathproof.py:2275-2283,2294-2305`). An
   implementer guessing wrong gets a guaranteed `prover_output_grammar_incomplete`.
4. **"Exactly one accounting summary" (design:370) contradicts §9.1 byte-identity**
   (design:386-388). An unconditional summary line changes every report including
   assignment-free fixtures like `literal.sh`. Per-value records alone would satisfy
   both, but then "exactly one summary" needs a definition for zero-value runs.

Also: §2.2/§7 leave the PATH/ENDPOINT compatibility projection as optional ("may",
design:81,332-334) while §9.1's byte-identity promise de facto requires it. All solvable,
none designed. Finding 3.

## Attack 7 — regression preservation vs `SELF_QA_PATHSCOPE.md`

I traced **every** assignment-admitting fixture in `$CASES`/`$C2CASES`/`$C3CASES`
(`SELF_QA_PATHSCOPE.md:310-313,314,367,389-453,493-609`) through the Option C
classifier:

- §9.3's "exactly two rc changes" **holds**: `c2_benign_words` 0→3 (`SELF_QA_PATHSCOPE.md:422`)
  and `c3_colon_whole` 1→3 (`SELF_QA_PATHSCOPE.md:440`) are the only changes I can
  derive. Spot checks: `assign_benign` rc 0 via two PWD members; `c2_list_bare_first`
  stays rc 3 (bare first member unresolved); `c2_relative` rc 1; `c3_uri_pair` rc 1;
  `c3_uri_list` rc 1; `c3_empty_only`/`_out` rc 0/1; `c2_command_text`,
  `c3_cmdtext_noslash`, `c3_ws_*`, `c2_quoted_space`, `c2_escaped_space`,
  `c4_*` families all keep their rc. The audit's measured rc values agree wherever they
  overlap (`PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:126-176`).
- The five assignment-admitting exceptions in the 310-384 range are exactly
  `green` (310), `assembled` (312), `dynamic` (313), `nested` (314), `backtick` (367).
  Everything else in that range admits nothing (`array` STOPs; `read x` binds nothing
  static). Failed attack — §9.1's inventory claim is correct.

Two wrinkles the design under-states:

1. §7 bullet 4 replaces set-deduplicated evidence and aggregate source names citing
   `pathscope_prover.py:2993-2997` (design:330-332) — but those lines format the
   PATH/ENDPOINT rows of **all** uses, including argv-only fixtures. Applied literally,
   every non-assignment fixture changes bytes and §9.1 is falsified by the design's own
   instructions. The replacement must be scoped to member-derived evidence. Finding 4.
2. `GREEN_R5.txt` and the seven determinism digests are produced from the working-tree
   prover (`SELF_QA_PATHSCOPE.md:284-286,650-653,655-672`), so they necessarily retire
   when the prover changes. The design says the R5 blob becomes the RED subject and a new
   GREEN column appears (design:395-397), but `SELF_QA_PATHSCOPE.md`'s published stdout
   block (`127-145`) is then a one-time re-fence that §12.6 must itemize, and "the full
   harness must still run verbatim" (design:393-395) is true only of the *edited*
   round-6 harness. Finding 10.

## Findings

1. **MUST-FIX-BEFORE-IMPLEMENTATION — admission boundary hole (F1's class, outside the
   admitted universe).** `${X:=v}`-style assignment-bearing parameter expansions on
   path-free carriers (`:`, `true`, `echo`, `printf`) are silently swallowed by
   `scan_args`'s `path_free` exemption (`pathscope_prover.py:1564-1570`): never admitted
   under §3.1, never STOPped. `: ${LD_PRELOAD:=/etc/evil.so}` returns `PASS rc=0` under
   R5 and under Option C with zero accounting. Either widen admission or add a STOP for
   assignment-shaped expansion forms (note: the fix touches kept machinery at
   `pathscope_prover.py:1512-2933`, outside §2's declared seam — so this needs a design
   amendment, and given D1's one-layer authorization, an explicit owner decision if the
   fix is deferred). At minimum, residual 1 must be rewritten to name this construct
   instead of absorbing it under "parser/grammar".
2. **MUST-FIX-BEFORE-IMPLEMENTATION — reason/reading consistency must be a runtime
   invariant, not prose.** Add to §4: a `words`/`word-colon` member must be
   `UNRESOLVED_FAIL_CLOSED` (§5 step 2); scalar/container ALLOW reasons
   (`whole_scalar_no_lexical_sink`, `empty_scalar_no_lexical_sink`,
   `whole_container_decomposed`) are legal only on `reading=whole` values with no active
   colon/words reading; colon-member ALLOW requires an allowlist rule token plus exact
   member provenance. Add the corresponding mutation arms to §10.5 ("mark a bare colon
   member `whole_scalar_no_lexical_sink`"; "mark a words member allowed"). Without this,
   the closed set is closed on paper only, and the convenient-bucket failure mode the
   redesign exists to eliminate remains available to the implementer.
3. **MUST-FIX-BEFORE-IMPLEMENTATION — design the composite contract; drop "mechanical".**
   Specify, in this design: the new record prefixes the composite's `known_lines` tuple
   must admit (`composite_pathproof.py:2290`); the terminal-reason table per branch
   including member-unresolved rc 3 (currently unspecified) and
   `accounting_invariant_failed`; the fourth composite arm for rc 3 with zero
   issue-counts; whether the standard headers print on the accounting-fault path
   (`composite_pathproof.py:2294-2305` requires exactly one of each); and the
   accounting-summary emission rule reconciling design:370 with §9.1 byte-identity.
   State that the PATH/ENDPOINT projection is mandatory, not optional.
4. **MUST-FIX-BEFORE-IMPLEMENTATION — scope §7 bullet 4 to member-derived evidence.**
   As written ("replace set-deduplicated `evidence` and aggregate source names
   (`2993-2997`)") it changes the rows of every fixture, falsifying §9.1's byte-identity
   promise for non-assignment fixtures and silently invalidating the published evidence
   base. The projection rows and their `uses=`/`sources=` formatting for argv-only uses
   must remain byte-identical.
5. **NOTE — global member-ID uniqueness and the analyzer-prefix scheme.** Add a
   prover-side run-level assertion that all member_ids across `⊎v M(v)` are distinct
   (§4 currently checks uniqueness only per value, so a cross-value collision passes
   every equation), and pin the analyzer scope prefix to a per-instance creation
   ordinal rather than a kind label (design:182-185 is ambiguous).
6. **NOTE — residual 2 leaves a usable, disclosed hole.** Single-token consumer-search
   values (`LD_PRELOAD=evil.so`, `LD_LIBRARY_PATH=.`, `PYTHONPATH=dir`) still PASS via
   step 7. Honest scoping, no regression vs R5; but the retained PASS reason string
   overstates the claim — keep the auditor-facing claim anchored to MEMBER reason
   tokens.
7. **NOTE — residual 6 has no usable hole.** Dedupe collapses multiplicity, never
   existence; the 240-char expression truncation is count-only.
8. **NOTE — define the path-shape test for wholes.** Step 5's "non-path whole" vs
   step 4's path occurrence is ambiguous for values like `bare.so:/etc/escape.so`
   (contains `/`); both arms fail closed, but the bucket choice changes rows.
9. **NOTE — ID line field vs rebased display lines.** For merged nested occurrences the
   member ID's line component (design:184) will disagree with rebased display lines;
   state that ID line fields are pre-rebase, or drop the line from the ID.
10. **NOTE — retired fences must be itemized.** `GREEN_R5.txt` and the seven determinism
    digests retire with the prover change; §12.6 should name them explicitly as the
    one-time re-fence rather than "every other changed fence is itemized" by implication.

## Where I am least sure

- **Scope of finding 1.** Whether closing the `${X:=v}` hole belongs inside D1's "one
  accounting layer" authorization or requires the owner boundary is a judgment call I
  cannot make from the design alone; the technical finding is solid either way.
- **Attack 7 is trace-based, not executed.** I derived rc values by reading R5 and the
  design's classifier; the review round forbids execution. My traces agree with every
  measured value the audit published, but the "exactly two rc changes" confirmation
  should be re-measured in the implementation round's first RED run, as §10.4 already
  requires.
- **Composite upstream behavior.** I reviewed `SubprocessPathProver` only
  (`composite_pathproof.py:2129-2391`); I did not audit how `ProverMemberResult` rows
  feed later composite stages, so finding 3's blast radius may be slightly larger than
  stated.

The conservation core survived every attack I could mount against it: F1, F2, and F3 are
closed by construction for admitted members, the falsification plan is discriminating on
the axes it covers, and the §9 regression contract checked out against the full fixture
inventory. The gaps are all at the edges the design explicitly left thin — the admission
boundary, the classification-vs-invariant distinction, and the downstream consumer — and
each has a cheap fix that belongs in this document before any code is written.
