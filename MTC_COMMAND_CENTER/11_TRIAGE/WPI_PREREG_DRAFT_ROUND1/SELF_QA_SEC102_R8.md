# SELF-QA — SEC102 composite path proof, round 8

Implementer: `claude-opus-5` xhigh (Max). Input commit `df983737`, whose Codex T1 audit
(`SEC102_CODEX_T1_AUDIT_R7_2026-08-12.md`) returned **REQUEST_CHANGES** on one finding,
CONFIRMED the round-7 command-word whitelist is a **fixpoint** for its class, and ACCEPTED the
interpreter-vocabulary residual as a disclosed production-gate decision. **The round-8 finding is
in the EVIDENCE HARNESS, not in the module.** Round 8 repairs that one finding and changes no
code. **No audit or acceptance is claimed here.**

Every command below is literal, was run from `C:\LAB\Tradingview_LAB_CLEAN`, and its real
output follows it. Section 13 re-extracts every block from this file and re-runs it from a
working directory OUTSIDE the repository, so the document cannot quietly drift from the tool.

**Sections 1-12 are the round-7 record, carried forward.** Every one of their `powershell` blocks
is byte-identical to `SELF_QA_SEC102_R7.md` except the hygiene block in section 9, which gains
`composite_pathproof.py`, `.gitattributes` and `sec102_r7_fixtures` in its carried-clean list so
that round 8's central claim — *no code changed* — is measured rather than asserted. Every carried
block was re-executed for round 8 by section 13 and its real process status and stderr are
published there.

## 0. What round 8 changes

### The round-7 finding — the harness read output before it proved execution

`SEC102_CODEX_T1_AUDIT_R7_2026-08-12.md`, HIGH, Design Defect Pattern 6 overlaid by Pattern 10:
the section-13 paste-and-run wrapper invoked each extracted `powershell` block with captured
output, tested only whether the published stdout subset was present, and based its own exit
solely on the mismatch counter. **It never read the child's process status and never read the
child's stderr.** So a child could emit exactly the published subset and *then* fail, or emit an
unadjudicated diagnostic, and the wrapper would report the block reproduced. Output was
interpreted before execution completeness was proved.

This is the same shape as the defects rounds 4-7 closed in `composite_pathproof.py` — a verdict
issued over something that was never established — except that this time the instrument, not the
subject, carried it. An evidence harness that can false-accept is worse than no harness, because
every carried GREEN in this document is quoted on its authority.

### The repair — three tests in a fixed order, and the order is the repair

1. The child's **process status must be 0**.
2. The child's **stderr must be empty**, or the block must be named in an explicit
   `STDERR_CONTRACT` with a written reason. The contract is currently **empty**, which is its
   strongest form: no block published here may write anything to stderr.
3. **Only then** is stdout read and compared with the published transcript.

A block failing (1) or (2) is REJECTED and **its stdout is never interpreted at all** — the
wrapper prints `STDOUT_NOT_INTERPRETED` and moves on. That is what makes the repair an ordering
property rather than an extra counter: there is no path through the wrapper on which an
incomplete run's output reaches the comparison.

### It is measured, not asserted

Section 13b runs the **published round-7 wrapper** (extracted byte-for-byte from
`SELF_QA_SEC102_R7.md`) and the **published round-8 wrapper** (extracted byte-for-byte from this
file) over four synthetic documents outside the repository. Two of them are the finding: a child
that prints the expected summary and then exits non-zero, and a child that prints the expected
summary and writes a diagnostic to stderr. Both are **ACCEPTED by round 7 and REJECTED by round
8** — RED before GREEN at the rc level. The other two are controls: a well-behaved child both
wrappers accept, so round 8 is not a blanket reject, and a child whose published line is absent,
which both wrappers reject, so the round-7 subset comparison is conserved.

### What round 8 does NOT change

`composite_pathproof.py` is **untouched** — same bytes, same SHA-256 as round 7
(section 10), and section 9 asserts it has no worktree modification. No fixture was added, so
`.gitattributes` is unchanged. Every classification, reason token, rc and transcript in sections
2-12 is the round-7 record re-run, not a new claim.

## 1. The round-7 finding, the repair, and where the evidence lives

### The finding

`SEC102_CODEX_T1_AUDIT_R6_2026-08-12.md`: the round-6 admission test asked whether a command
word **contained** one of a listed set of expansion metacharacters (`*`, `?`, `[`, `]`, `{`,
`}`, `~`, `\`). That is a BLACKLIST, and it missed the `extglob` operator family. One-or-more
`+(...)`, exactly-one `@(...)` and negated `!(...)` carry none of the listed characters, so with
`extglob` enabled `/usr/bin/ba+(s)h library.sh` pathname-resolves to `bash`, runs the operand,
and round 6 classified it as a benign leaf and returned `PASS rc 0` over an unanalysed program.

### Why the fix is not "add three more characters"

Round 4 closed the numeric file descriptor. Round 5 closed the named descriptor and the indexed
assignment. Round 6 closed the pathname/brace/tilde/backslash forms. Round 7 was handed a
seventh class. The regress is structural: **as long as the test enumerates what is forbidden,
completeness depends on the enumeration, and no static tool can prove an enumeration of shell
operators complete.** Adding `+`, `@` and `!` would buy one round.

### The repair — invert the direction of proof

A command word is admissible as a PROVEN-STATIC benign leaf **only when every character of the
raw, pre-expansion word token is in an explicit safe set**. Any other character — a known
operator, an unknown operator, or a character with no shell meaning at all — makes the word not
proven-static, so it is `unmodeled` and the stage STOPs. The default for an unrecognised
character is refusal, so a form nobody anticipated cannot be admitted by not having been listed.

**The safe set is `[A-Za-z0-9._/:-]`**, and each member is admitted with a reason, not by
convenience (`composite_pathproof.py:207-268` states all of this in the module):

| Member | Why it cannot introduce dynamic resolution |
|---|---|
| `A-Z a-z 0-9` | Ordinary characters: not metacharacters, not expansion operators, not quoting. They can only spell a name. |
| `.` | Ordinary pathname character. The one-character word `.` is the source builtin and is classified by `GRAPH_SOURCE_WORDS` before any word can be admitted as a leaf. |
| `_` | Ordinary pathname and NAME character. Special only as the variable `_`, which requires a `$` the set does not admit. |
| `-` | Ordinary. A leading `-` makes an option word, not an expansion. Special only inside `${var-alt}`, which requires `$` and `{`. |
| `/` | The pathname separator. It suppresses PATH, function and builtin lookup rather than introducing expansion, and the classifier already takes the last pathname component of any word containing one. |
| `:` | Ordinary; the one-character word `:` is the null builtin. Special only inside `${var:-alt}`, which requires `$` and `{`. |

Excluded, each exclusion load-bearing rather than cautious:

* `?`, `*`, `+`, `@`, `!` — the five `extglob` operator characters. Excluding all five refuses
  the whole family in one rule instead of by enumeration. This is the round-6 finding.
* `%` — introduces job-specification resolution when job control is enabled, an option state the
  composite does not model.
* `=` — selects `equals` expansion in shells that implement it, and every assignment word Bash
  does recognise is classified *before* this test, so admitting `=` would buy nothing.
* `'` and `"` — build a name out of quote removal rather than spelling it.
* `,`, `^`, `#`, and every other printable or non-printable character — refused because no proof
  was offered that they cannot resolve. That is the entire point of the inversion.

### The kickoff's illustrative safe set does not close the finding — measured, not argued

`KICKOFF_SEC102_BUILD_R7.md:26` suggests `[A-Za-z0-9._/+=:@%-]`. **`+` and `@` in that set are
two of the five `extglob` operators**, so under it `ba+(s)h` and `ba@(s)h` remain benign leaves.
This is not asserted; it is mutation `M2` in section 5, which puts that exact set into the module
and shows two round-7 REDs returning to `PASS`. The implemented set is strictly smaller and the
difference is the repair.

### One scanner change, and it decides nothing

The safe set has to be applied to the word Bash would look up. The scanner split at `(`, so
`ba+(s)h` reached the classifier as three fragments — `ba+`, `s`, `h` — and the classifier was
adjudicating something that is not a word. Round 7 conserves an abutting `(` INTO the raw token
(`composite_pathproof.py:1429-1451`), so the safe set adjudicates `ba+(` instead of `ba+`.

The one benign construct with that shape is a function definition, and Bash requires a NAME for
it; an `extglob` pattern requires `?`, `*`, `+`, `@` or `!` immediately before the `(`, and no
NAME ends in one of those. So `fixture_main()` keeps its round-6 treatment and nothing else does.
**This conservation is not a second fence and is not load-bearing on its own** — mutation `M3`
turns it off and kills nothing, because the safe set already refuses `ba+`. It is measured that
way and published that way rather than claimed as defence in depth.

### Evidence map

| Claim | Section |
|---|---|
| **Round 8: the evidence harness now proves execution before it reads output** | 0, 13a |
| **Round 8: the harness's own RED before GREEN — 4 synthetic children x 2 published wrappers** | 13b |
| **Round 8: real process status and stderr for all eleven blocks, plus the outer wrapper** | 13c |
| The defect existed at `90868b86` and does not now, at the scanner boundary | 2 |
| Nothing carried regressed — 58 cases | 3 |
| Each new RED was `PASS` on the audited code and is `STOP` now | 4 |
| Restoring the blacklist returns the new REDs to `PASS` — 7 mutations x 16 REDs | 5 |
| The policy's shape — 77 declared forms + 7 word-boundary forms | 6 |
| **The fixpoint property over EVERY printable character, not a chosen list** | 7 |
| Round-5 prefix battery and the five round-3/round-4 discriminators | 8 |
| Hygiene, determinism, carried byte identity | 9 |
| Artifact identity | 10 |
| What rounds 7 and 8 do NOT close | 11 |
| Thirteen-pattern self-adjudication | 12 |
| Paste-and-run verification of this document | 13 |

### What changed in the code in round 7 — and nothing in round 8

* `COMMAND_WORD_EXPANSION_RE` (blacklist) is **replaced** by `COMMAND_WORD_STATIC_RE`
  (whitelist, `^[A-Za-z0-9._/:-]+$`) and a `COMMAND_WORD_SAFE_SET` label.
* `_command_word_class` now returns `unmodeled` when the raw word is not a full match.
* `_shell_words` conserves an abutting `(` into the raw token unless the token is a NAME
  (`SHELL_FUNCTION_NAME_RE`).
* No reason token was added or renamed. Every refusal still reports
  `source_graph_unmodeled_command_word`, so no carried expectation moved.
* `COMMAND_WORD_SUBSTITUTION_RE` (`$`, backtick) is kept ahead of the whitelist even though the
  whitelist would also refuse those words, so the `dynamic` class and its distinct reason token
  survive and no single fence carries that class alone.

## 2. The defect measured at the scanner boundary, both sides, one command

The module is loaded twice — once from the worktree, once streamed from `90868b86` — and asked
what it sees. `SILENT_NO_EDGE` is true when the module reports **no edge, no uncovered command
word and no opaque reason** over bytes that reach another program: the exact shape of a false
RENDER `PASS`. Four expectation classes are declared, so the block fails if the repair became a
blanket STOP as easily as if it missed a form.

* `REACHES` — Bash can reach another program here and the composite models no edge; must not be silent.
* `DERIVES` — the modelled interpreter/source form; must still derive its edge after the repair.
* `BENIGN` — Bash reaches nothing; must stay silent, i.e. no over-STOP.
* `DISCLOSED` — benign in Bash but refused by the closed policy; asserted so the conservative
  stop stays visible instead of drifting.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$old='90868b86:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$probe=@'
import pathlib, subprocess, sys, types
TOOL = pathlib.Path(sys.argv[1]); OLD = sys.argv[2]
def load(name, source):
    module = types.ModuleType(name)
    module.__file__ = str(TOOL)
    sys.modules[name] = module
    exec(compile(source, str(TOOL), "exec"), module.__dict__)
    return module
new = load("cpp_new", TOOL.read_text(encoding="utf-8"))
old = load("cpp_old", subprocess.run(["git", "show", OLD], capture_output=True, text=True,
                                     check=True, encoding="utf-8").stdout)
# (label, rendered bytes, expectation)
#   REACHES  - Bash can reach another program at this command word and the composite
#              models no edge for it; the module must NOT be silent
#   DERIVES  - the modelled interpreter/source form; must still derive its edge
#   BENIGN   - Bash reaches nothing; the module must stay silent, i.e. no over-STOP
#   DISCLOSED- benign in Bash but refused by the closed policy; asserted so the
#              conservative stop stays visible instead of drifting
CASES = [
    # --- the round-6 audit finding: the extglob operator family -----------------
    ("xg_plus_interpreter",      "/usr/bin/ba+(s)h /safe/fixture/library.sh\n",                "REACHES"),
    ("xg_at_interpreter",        "/usr/bin/ba@(s)h /safe/fixture/library.sh\n",                "REACHES"),
    ("xg_bang_interpreter",      "/usr/bin/ba!(x)h /safe/fixture/library.sh\n",                "REACHES"),
    ("xg_qmark_interpreter",     "/usr/bin/ba?(s)h /safe/fixture/library.sh\n",                "REACHES"),
    ("xg_star_interpreter",      "/usr/bin/ba*(s)h /safe/fixture/library.sh\n",                "REACHES"),
    ("xg_bare_at",               "@(bash) /safe/fixture/library.sh\n",                         "REACHES"),
    ("xg_bare_plus",             "+(bash) /safe/fixture/library.sh\n",                         "REACHES"),
    ("xg_in_directory",          "/usr/+(bin)/bash /safe/fixture/library.sh\n",                "REACHES"),
    ("xg_relative",              "ba+(s)h /safe/fixture/library.sh\n",                         "REACHES"),
    ("xg_after_assign_prefix",   "A=1 /usr/bin/ba+(s)h /safe/fixture/library.sh\n",            "REACHES"),
    ("xg_after_named_fd",        "{fd}>/dev/null /usr/bin/ba+(s)h /safe/fixture/library.sh\n", "REACHES"),
    ("xg_in_function_body",      "function reload { /usr/bin/ba+(s)h /safe/fixture/library.sh; }\n", "REACHES"),
    # --- the unenumerated-character case ---------------------------------------
    ("novel_percent",            "%bash /safe/fixture/library.sh\n",                           "REACHES"),
    ("novel_caret",              "^bash /safe/fixture/library.sh\n",                           "REACHES"),
    ("novel_comma",              "/usr/bin/ba,sh /safe/fixture/library.sh\n",                  "REACHES"),
    # --- carried round-6 REACHES forms -----------------------------------------
    ("glob_star_interpreter",    "/usr/bin/ba*h /safe/fixture/library.sh\n",                   "REACHES"),
    ("glob_bracket_interpreter", "/usr/bin/[b]ash /safe/fixture/library.sh\n",                 "REACHES"),
    ("brace_interpreter",        "/usr/bin/{ba,z}sh /safe/fixture/library.sh\n",               "REACHES"),
    ("tilde_interpreter",        "~/bin/bash /safe/fixture/library.sh\n",                      "REACHES"),
    ("relative_interpreter",     "bin/bash /safe/fixture/library.sh\n",                        "REACHES"),
    ("escaped_interpreter",      "\\bash /safe/fixture/library.sh\n",                          "REACHES"),
    ("quoted_interpreter",       "\"bash\" /safe/fixture/library.sh\n",                        "REACHES"),
    ("param_interpreter",        "A=1 ${SHELL_BIN} /safe/fixture/library.sh\n",                "REACHES"),
    ("substitution_interpreter", "$(printf bash) /safe/fixture/library.sh\n",                  "REACHES"),
    # --- the repair must not become a blanket STOP ------------------------------
    ("modelled_interpreter_edge","/usr/bin/bash /safe/fixture/library.sh\n",                   "DERIVES"),
    ("modelled_bare_interpreter","bash /safe/fixture/library.sh\n",                            "DERIVES"),
    ("modelled_source_builtin",  "source /safe/fixture/library.sh\n",                          "DERIVES"),
    ("static_leaf",              "cat \"$ROOT/in.txt\"\n",                                     "BENIGN"),
    ("absolute_static_leaf",     "/bin/cat /safe/fixture/in.txt\n",                            "BENIGN"),
    ("relative_static_leaf",     "bin/verify_marker /safe/fixture/in.txt\n",                   "BENIGN"),
    ("hyphen_dot_digit_leaf",    "bin/verify_marker-2.0 /safe/fixture/in.txt\n",               "BENIGN"),
    ("colon_leaf",               "/opt/tools:probe_1/run.check /safe/fixture/in.txt\n",        "BENIGN"),
    ("null_builtin",             ": /safe/fixture/in.txt\n",                                   "BENIGN"),
    ("function_definition",      "fixture_main() { /bin/cat /safe/fixture/in.txt; }\n",        "BENIGN"),
    ("function_definition_ws",   "fixture_main () { /bin/cat /safe/fixture/in.txt; }\n",       "BENIGN"),
    ("subshell_group",           "( /bin/cat /safe/fixture/in.txt )\n",                        "BENIGN"),
    ("group_command",            "{ /bin/cat /safe/fixture/in.txt; }\n",                       "BENIGN"),
    ("double_bracket_test",      "[[ -f /safe/fixture/in.txt ]]\n",                            "BENIGN"),
    ("assign_prefix_leaf",       "A=1 /bin/cat /safe/fixture/in.txt\n",                        "BENIGN"),
    ("named_fd_leaf",            "{fd}>/dev/null /bin/cat /safe/fixture/in.txt\n",             "BENIGN"),
    # --- conservative stops, published so they cannot drift unnoticed -----------
    ("plus_name_leaf",           "/usr/bin/g++ /safe/fixture/in.cpp\n",                        "DISCLOSED"),
    ("at_name_leaf",             "/usr/bin/tool@1.0 /safe/fixture/in.txt\n",                   "DISCLOSED"),
    ("comma_name_leaf",          "/usr/bin/a,b /safe/fixture/in.txt\n",                        "DISCLOSED"),
    ("equals_name_leaf",         "--opt=value /safe/fixture/in.txt\n",                         "DISCLOSED"),
    ("non_name_function_def",    "bin/foo() { /bin/cat /safe/fixture/in.txt; }\n",             "DISCLOSED"),
    ("test_builtin_bracket",     "[ -f /safe/fixture/in.txt ]\n",                              "DISCLOSED"),
    ("escaped_leaf",             "\\cat /safe/fixture/in.txt\n",                               "DISCLOSED"),
    ("tilde_leaf",               "~/bin/verify_marker /safe/fixture/in.txt\n",                 "DISCLOSED"),
    ("glob_leaf",                "/safe/fixture/*.tool /safe/fixture/in.txt\n",                "DISCLOSED"),
]
def matchers(module, text):
    return (list(module.SOURCE_COMMAND_RE.finditer(text)),
            list(module.EXEC_COMMAND_RE.finditer(text)))
def silent(module, text):
    """True when the module sees no edge, no uncovered command word and no opaque reason."""
    if module._graph_opaque_reason(text) is not None:
        return False
    src, exe = matchers(module, text)
    return not src and not exe and not module._graph_word_conservation(text, src, exe)
def derives(module, text):
    src, exe = matchers(module, text)
    return bool(src or exe) and not module._graph_word_conservation(text, src, exe)
bad = 0
newly = 0
for label, text, expectation in CASES:
    before, after = silent(old, text), silent(new, text)
    if expectation == "BENIGN":
        ok = after
    elif expectation == "DERIVES":
        ok = (not after) and derives(old, text) and derives(new, text)
    else:
        ok = not after
    if expectation == "REACHES" and before and not after:
        newly += 1
    bad += not ok
    print(f"PROBE={label:27s} EXPECT={expectation:9s} 90868b86_SILENT_NO_EDGE={str(before):5s} "
          f"R7_SILENT_NO_EDGE={str(after):5s} {'OK' if ok else 'OFF_EXPECTATION'}")
print(f"PROBES={len(CASES)} OFF_EXPECTATION={bad} NEWLY_CLOSED_BY_R7={newly}")
sys.exit(0 if bad == 0 else 1)
'@
$probe | python -B - $tool $old
"PROBE_BLOCK_RC=$LASTEXITCODE"
```

Real output:

```text
PROBE=xg_plus_interpreter         EXPECT=REACHES   90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=xg_at_interpreter           EXPECT=REACHES   90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=xg_bang_interpreter         EXPECT=REACHES   90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=xg_qmark_interpreter        EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=xg_star_interpreter         EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=xg_bare_at                  EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=xg_bare_plus                EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=xg_in_directory             EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=xg_relative                 EXPECT=REACHES   90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=xg_after_assign_prefix      EXPECT=REACHES   90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=xg_after_named_fd           EXPECT=REACHES   90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=xg_in_function_body         EXPECT=REACHES   90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=novel_percent               EXPECT=REACHES   90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=novel_caret                 EXPECT=REACHES   90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=novel_comma                 EXPECT=REACHES   90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=glob_star_interpreter       EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=glob_bracket_interpreter    EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=brace_interpreter           EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=tilde_interpreter           EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=relative_interpreter        EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=escaped_interpreter         EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=quoted_interpreter          EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=param_interpreter           EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=substitution_interpreter    EXPECT=REACHES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=modelled_interpreter_edge   EXPECT=DERIVES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=modelled_bare_interpreter   EXPECT=DERIVES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=modelled_source_builtin     EXPECT=DERIVES   90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=static_leaf                 EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=absolute_static_leaf        EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=relative_static_leaf        EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=hyphen_dot_digit_leaf       EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=colon_leaf                  EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=null_builtin                EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=function_definition         EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=function_definition_ws      EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=subshell_group              EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=group_command               EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=double_bracket_test         EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=assign_prefix_leaf          EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=named_fd_leaf               EXPECT=BENIGN    90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=True  OK
PROBE=plus_name_leaf              EXPECT=DISCLOSED 90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=at_name_leaf                EXPECT=DISCLOSED 90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=comma_name_leaf             EXPECT=DISCLOSED 90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=equals_name_leaf            EXPECT=DISCLOSED 90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=non_name_function_def       EXPECT=DISCLOSED 90868b86_SILENT_NO_EDGE=True  R7_SILENT_NO_EDGE=False OK
PROBE=test_builtin_bracket        EXPECT=DISCLOSED 90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=escaped_leaf                EXPECT=DISCLOSED 90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=tilde_leaf                  EXPECT=DISCLOSED 90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBE=glob_leaf                   EXPECT=DISCLOSED 90868b86_SILENT_NO_EDGE=False R7_SILENT_NO_EDGE=False OK
PROBES=49 OFF_EXPECTATION=0 NEWLY_CLOSED_BY_R7=10
PROBE_BLOCK_RC=0
```

Command rc: `0`. **Ten forms that reach another program were silent on the audited code and are
not silent now** — the three extglob classes in six spellings and the three unenumerated
characters. Thirteen benign forms stay silent and three modelled forms still derive their edge,
which is what distinguishes a repair from a blanket STOP.

Two honest asymmetries, published rather than smoothed:

* `xg_qmark_`, `xg_star_`, `xg_bare_at`, `xg_bare_plus` and `xg_in_directory` were **already**
  not silent at `90868b86` — the first two because `?` and `*` were on the round-6 blacklist, the
  last three because the fragment after the `(` was itself a recognised interpreter. They are
  carried controls, not counted in `NEWLY_CLOSED_BY_R7`.
* Five `DISCLOSED` forms are new conservative stops that round 6 admitted (`g++`, `tool@1.0`,
  `a,b`, `--opt=value`, and a non-NAME function definition). They are refusals, not detections,
  and they are section 11 residuals.

## 3. Literal all-case assertion command — 58 cases

All 52 round-6 cases are carried with their rc and reason token unchanged; six are round-7
additions. No carried fixture file was edited (section 9).

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$r1='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r1_fixtures'
$r2='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures'
$r3='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures'
$r4='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r4_fixtures'
$r5='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r5_fixtures'
$r6='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r6_fixtures'
$r7='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r7_fixtures'
$cases=@(
  @('allocate',$r1,'red_plan_contract.json',3,'plan_schema_unknown_key'),
  @('allocate',$r1,'red_entrypoint.json',1,'entrypoint_not_declared'),
  @('allocate',$r1,'red_allocation_conservation.json',1,'allocation_not_one_to_one'),
  @('allocate',$r1,'red_allocation_value.json',3,'allocation_value_unresolved'),
  @('allocate',$r1,'red_graph_conservation.json',1,'declared_member_unreachable'),
  @('allocate',$r1,'red_component_identity.json',3,'member_file_missing'),
  @('allocate',$r1,'green.json',0,'allocate_stage_closed'),
  @('render',$r2,'red_render_contract.json',3,'plan_schema_unknown_key'),
  @('render',$r2,'red_render_template_conservation.json',1,'render_template_member_not_one_to_one'),
  @('render',$r2,'red_render_materialisation.json',1,'rendered_bytes_mismatch'),
  @('render',$r2,'red_render_graph_dynamic.json',3,'source_operand_dynamic'),
  @('render',$r2,'red_render_identity.json',3,'member_file_missing'),
  @('render',$r2,'red_render_member_disposition.json',1,'render_member_rejected'),
  @('render',$r2,'red_render_heredoc_false_edge.json',3,'source_graph_heredoc_not_modeled'),
  @('render',$r3,'red_render_non_shell_member.json',3,'member_kind_graph_derivation_not_modeled'),
  @('render',$r2,'green_render.json',0,'render_stage_closed'),
  @('freeze',$r2,'red_freeze_contract.json',3,'plan_schema_unknown_key'),
  @('freeze',$r2,'red_freeze_member_pin.json',3,'frozen_identity_mismatch'),
  @('freeze',$r2,'red_freeze_graph.json',3,'derived_declared_graph_mismatch'),
  @('freeze',$r2,'red_freeze_prover_pin.json',3,'approved_prover_identity_not_declared'),
  @('freeze',$r2,'red_freeze_prover_grammar.json',3,'prover_output_grammar_incomplete'),
  @('freeze',$r2,'red_freeze_coverage.json',3,'coverage_issue_count=2'),
  @('freeze',$r2,'red_freeze_forbidden.json',1,'prover_forbidden_operand'),
  @('freeze',$r2,'red_freeze_residual.json',3,'prover_residual_disclosure_missing'),
  @('freeze',$r2,'red_freeze_member_disposition.json',3,'non_shell_member_analyzer_not_integrated'),
  @('freeze',$r3,'red_freeze_deploy_identity.json',3,'source_operand_deploy_identity_unbound'),
  @('freeze',$r3,'red_freeze_deploy_path_invalid.json',3,'member_deploy_path_not_canonical_absolute'),
  @('freeze',$r3,'red_freeze_deploy_path_alias.json',3,'member_deploy_path_alias'),
  @('freeze',$r3,'red_freeze_allocation_constants.json',3,'allocation_constants_value_divergence'),
  @('freeze',$r3,'red_freeze_constants_grammar.json',3,'constants_line_not_key_value'),
  @('freeze',$r3,'red_freeze_constants_operand_unbound.json',3,'analysis_unit_source_operand_constants_unbound'),
  @('freeze',$r3,'red_freeze_execute_source_edge.json',3,'analysis_unit_non_source_edge_not_integrated'),
  @('freeze',$r3,'red_freeze_source_site_not_standalone.json',3,'analysis_unit_source_site_not_standalone'),
  @('freeze',$r3,'red_freeze_zero_facts.json',3,'prover_zero_facts_pass'),
  @('freeze',$r3,'red_freeze_divergent_control.json',1,'prover_forbidden_operand'),
  @('freeze',$r2,'green_freeze.json',0,'freeze_stage_closed'),
  @('freeze',$r2,'green_freeze_network.json',0,'resolved_net_endpoint_count=1'),
  @('render',$r4,'red_render_wrapped_source.json',3,'source_graph_command_wrapper_not_modeled'),
  @('freeze',$r4,'red_freeze_wrapped_source.json',3,'source_graph_command_word_not_modeled'),
  @('freeze',$r4,'red_freeze_allocation_absent.json',3,'allocation_absent_from_pinned_constants'),
  @('render',$r5,'red_render_named_fd_source.json',3,'source_graph_command_word_not_modeled'),
  @('render',$r5,'red_render_indexed_assign_source.json',3,'source_graph_command_word_not_modeled'),
  @('render',$r5,'red_render_unmodeled_prefix.json',3,'source_graph_unmodeled_assignment_prefix'),
  @('render',$r5,'red_render_function_body_source.json',3,'source_graph_command_word_not_modeled'),
  @('render',$r6,'red_render_glob_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r6,'red_render_bracket_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r6,'red_render_brace_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r6,'red_render_tilde_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r6,'red_render_relative_interpreter.json',3,'source_graph_command_word_not_modeled'),
  @('render',$r6,'red_render_param_command_word.json',3,'source_graph_dynamic_command_not_modeled'),
  @('render',$r6,'red_render_substitution_command_word.json',3,'source_graph_nested_execution_not_modeled'),
  @('render',$r6,'green_render_static_leaf.json',0,'render_stage_closed'),
  @('render',$r7,'red_render_extglob_plus_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r7,'red_render_extglob_at_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r7,'red_render_extglob_bang_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r7,'red_render_extglob_qmark_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r7,'red_render_novel_operator_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r7,'green_render_safe_set_leaf.json',0,'render_stage_closed')
)
$failed=0
foreach($case in $cases){
  $stage=$case[0]; $dir=$case[1]; $name=$case[2]
  $want=[int]$case[3]; $token=$case[4]
  $out=(& python -B $tool $stage (Join-Path $dir $name)) -join "`n"
  $got=$LASTEXITCODE
  $ok=($got -eq $want -and $out.Contains($token))
  if(-not $ok){$failed++}
  "CASE=$name STAGE=$stage RC=$got EXPECTED=$want TOKEN=$token ASSERT=$(if($ok){'PASS'}else{'FAIL'})"
}
"CASES=$($cases.Count) FAILED_COUNT=$failed"
if($failed){exit 1}else{exit 0}
```

Real output:

```text
CASE=red_plan_contract.json STAGE=allocate RC=3 EXPECTED=3 TOKEN=plan_schema_unknown_key ASSERT=PASS
CASE=red_entrypoint.json STAGE=allocate RC=1 EXPECTED=1 TOKEN=entrypoint_not_declared ASSERT=PASS
CASE=red_allocation_conservation.json STAGE=allocate RC=1 EXPECTED=1 TOKEN=allocation_not_one_to_one ASSERT=PASS
CASE=red_allocation_value.json STAGE=allocate RC=3 EXPECTED=3 TOKEN=allocation_value_unresolved ASSERT=PASS
CASE=red_graph_conservation.json STAGE=allocate RC=1 EXPECTED=1 TOKEN=declared_member_unreachable ASSERT=PASS
CASE=red_component_identity.json STAGE=allocate RC=3 EXPECTED=3 TOKEN=member_file_missing ASSERT=PASS
CASE=green.json STAGE=allocate RC=0 EXPECTED=0 TOKEN=allocate_stage_closed ASSERT=PASS
CASE=red_render_contract.json STAGE=render RC=3 EXPECTED=3 TOKEN=plan_schema_unknown_key ASSERT=PASS
CASE=red_render_template_conservation.json STAGE=render RC=1 EXPECTED=1 TOKEN=render_template_member_not_one_to_one ASSERT=PASS
CASE=red_render_materialisation.json STAGE=render RC=1 EXPECTED=1 TOKEN=rendered_bytes_mismatch ASSERT=PASS
CASE=red_render_graph_dynamic.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_operand_dynamic ASSERT=PASS
CASE=red_render_identity.json STAGE=render RC=3 EXPECTED=3 TOKEN=member_file_missing ASSERT=PASS
CASE=red_render_member_disposition.json STAGE=render RC=1 EXPECTED=1 TOKEN=render_member_rejected ASSERT=PASS
CASE=red_render_heredoc_false_edge.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_heredoc_not_modeled ASSERT=PASS
CASE=red_render_non_shell_member.json STAGE=render RC=3 EXPECTED=3 TOKEN=member_kind_graph_derivation_not_modeled ASSERT=PASS
CASE=green_render.json STAGE=render RC=0 EXPECTED=0 TOKEN=render_stage_closed ASSERT=PASS
CASE=red_freeze_contract.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=plan_schema_unknown_key ASSERT=PASS
CASE=red_freeze_member_pin.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=frozen_identity_mismatch ASSERT=PASS
CASE=red_freeze_graph.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=derived_declared_graph_mismatch ASSERT=PASS
CASE=red_freeze_prover_pin.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=approved_prover_identity_not_declared ASSERT=PASS
CASE=red_freeze_prover_grammar.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=prover_output_grammar_incomplete ASSERT=PASS
CASE=red_freeze_coverage.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=coverage_issue_count=2 ASSERT=PASS
CASE=red_freeze_forbidden.json STAGE=freeze RC=1 EXPECTED=1 TOKEN=prover_forbidden_operand ASSERT=PASS
CASE=red_freeze_residual.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=prover_residual_disclosure_missing ASSERT=PASS
CASE=red_freeze_member_disposition.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=non_shell_member_analyzer_not_integrated ASSERT=PASS
CASE=red_freeze_deploy_identity.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=source_operand_deploy_identity_unbound ASSERT=PASS
CASE=red_freeze_deploy_path_invalid.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=member_deploy_path_not_canonical_absolute ASSERT=PASS
CASE=red_freeze_deploy_path_alias.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=member_deploy_path_alias ASSERT=PASS
CASE=red_freeze_allocation_constants.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=allocation_constants_value_divergence ASSERT=PASS
CASE=red_freeze_constants_grammar.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=constants_line_not_key_value ASSERT=PASS
CASE=red_freeze_constants_operand_unbound.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=analysis_unit_source_operand_constants_unbound ASSERT=PASS
CASE=red_freeze_execute_source_edge.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=analysis_unit_non_source_edge_not_integrated ASSERT=PASS
CASE=red_freeze_source_site_not_standalone.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=analysis_unit_source_site_not_standalone ASSERT=PASS
CASE=red_freeze_zero_facts.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=prover_zero_facts_pass ASSERT=PASS
CASE=red_freeze_divergent_control.json STAGE=freeze RC=1 EXPECTED=1 TOKEN=prover_forbidden_operand ASSERT=PASS
CASE=green_freeze.json STAGE=freeze RC=0 EXPECTED=0 TOKEN=freeze_stage_closed ASSERT=PASS
CASE=green_freeze_network.json STAGE=freeze RC=0 EXPECTED=0 TOKEN=resolved_net_endpoint_count=1 ASSERT=PASS
CASE=red_render_wrapped_source.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_command_wrapper_not_modeled ASSERT=PASS
CASE=red_freeze_wrapped_source.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=source_graph_command_word_not_modeled ASSERT=PASS
CASE=red_freeze_allocation_absent.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=allocation_absent_from_pinned_constants ASSERT=PASS
CASE=red_render_named_fd_source.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_command_word_not_modeled ASSERT=PASS
CASE=red_render_indexed_assign_source.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_command_word_not_modeled ASSERT=PASS
CASE=red_render_unmodeled_prefix.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_assignment_prefix ASSERT=PASS
CASE=red_render_function_body_source.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_command_word_not_modeled ASSERT=PASS
CASE=red_render_glob_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=red_render_bracket_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=red_render_brace_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=red_render_tilde_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=red_render_relative_interpreter.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_command_word_not_modeled ASSERT=PASS
CASE=red_render_param_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_dynamic_command_not_modeled ASSERT=PASS
CASE=red_render_substitution_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_nested_execution_not_modeled ASSERT=PASS
CASE=green_render_static_leaf.json STAGE=render RC=0 EXPECTED=0 TOKEN=render_stage_closed ASSERT=PASS
CASE=red_render_extglob_plus_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=red_render_extglob_at_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=red_render_extglob_bang_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=red_render_extglob_qmark_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=red_render_novel_operator_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=green_render_safe_set_leaf.json STAGE=render RC=0 EXPECTED=0 TOKEN=render_stage_closed ASSERT=PASS
CASES=58 FAILED_COUNT=0
```

Command rc: `0`.

## 4. D026 RED before GREEN — behavioural pre-feature falsification

Every round-7 plan runs over byte-identical inputs against the audited code streamed from
`90868b86` and against the worktree code. The declared roles are asserted, so a case that is not
the kind of case it claims to be fails the block.

**Four of the five new REDs are rc-level REDs.** The `?(` class is not: `?` was already on the
round-6 blacklist, so `red_render_extglob_qmark_command_word.json` was `STOP rc 3` at `90868b86`
and is carried as a `CARRIED_STOP` control. The kickoff groups `?(`/`@(` as one class; the
measured before-state is published instead of the grouping.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$r7=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r7_fixtures').Path
$old='90868b86:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$prefeature=@'
import contextlib, io, pathlib, re, subprocess, sys
TOOL = pathlib.Path(sys.argv[1]); FX = pathlib.Path(sys.argv[2]); OLD = sys.argv[3]
NEW_SOURCE = TOOL.read_text(encoding="utf-8")
OLD_SOURCE = subprocess.run(["git", "show", OLD], capture_output=True, text=True,
                            check=True, encoding="utf-8").stdout
# (plan, declared role, expected rc on 90868b86, expected rc under round 7)
CASES = [
    ("red_render_extglob_plus_command_word.json",  "NEW_RED",       0, 3),
    ("red_render_extglob_at_command_word.json",    "NEW_RED",       0, 3),
    ("red_render_extglob_bang_command_word.json",  "NEW_RED",       0, 3),
    ("red_render_novel_operator_command_word.json","NEW_RED",       0, 3),
    ("red_render_extglob_qmark_command_word.json", "CARRIED_STOP",  3, 3),
    ("green_render_safe_set_leaf.json",            "GREEN_CONTROL", 0, 0),
]
R4 = re.compile(r'^CLAIM id="R4".*reason="([^"]*)"', re.MULTILINE)
def run(source, plan):
    buffer = io.StringIO(); argv = sys.argv[:]
    sys.argv = [str(TOOL), "render", str(plan)]
    try:
        with contextlib.redirect_stdout(buffer):
            exec(compile(source, str(TOOL), "exec"), {"__name__": "__main__", "__file__": str(TOOL)})
        code = 0
    except SystemExit as exc:
        code = int(exc.code or 0)
    finally:
        sys.argv = argv
    found = R4.search(buffer.getvalue())
    return code, (found.group(1) if found else "-")
off = 0
new_reds = 0
for name, role, want_old, want_new in CASES:
    old_rc, old_reason = run(OLD_SOURCE, FX / name)
    new_rc, new_reason = run(NEW_SOURCE, FX / name)
    ok = old_rc == want_old and new_rc == want_new
    off += not ok
    new_reds += role == "NEW_RED" and old_rc == 0 and new_rc == 3
    print(f"CASE={name}")
    print(f"  ROLE={role} EXPECT_90868b86_RC={want_old} GOT={old_rc}  EXPECT_R7_RC={want_new} GOT={new_rc} "
          f"{'OK' if ok else 'OFF_EXPECTATION'}")
    print(f"  90868b86_R4={old_reason}")
    print(f"  R7_R4={new_reason}")
print(f"CASES={len(CASES)} RC_LEVEL_NEW_REDS={new_reds} OFF_EXPECTATION={off}")
sys.exit(0 if off == 0 else 1)
'@
$prefeature | python -B - $tool $r7 $old
"PREFEATURE_BLOCK_RC=$LASTEXITCODE"
```

Real output:

```text
CASE=red_render_extglob_plus_command_word.json
  ROLE=NEW_RED EXPECT_90868b86_RC=0 GOT=0  EXPECT_R7_RC=3 GOT=3 OK
  90868b86_R4=rendered_bytes_derive_the_declared_reachable_graph
  R7_R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
CASE=red_render_extglob_at_command_word.json
  ROLE=NEW_RED EXPECT_90868b86_RC=0 GOT=0  EXPECT_R7_RC=3 GOT=3 OK
  90868b86_R4=rendered_bytes_derive_the_declared_reachable_graph
  R7_R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
CASE=red_render_extglob_bang_command_word.json
  ROLE=NEW_RED EXPECT_90868b86_RC=0 GOT=0  EXPECT_R7_RC=3 GOT=3 OK
  90868b86_R4=rendered_bytes_derive_the_declared_reachable_graph
  R7_R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
CASE=red_render_novel_operator_command_word.json
  ROLE=NEW_RED EXPECT_90868b86_RC=0 GOT=0  EXPECT_R7_RC=3 GOT=3 OK
  90868b86_R4=rendered_bytes_derive_the_declared_reachable_graph
  R7_R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
CASE=red_render_extglob_qmark_command_word.json
  ROLE=CARRIED_STOP EXPECT_90868b86_RC=3 GOT=3  EXPECT_R7_RC=3 GOT=3 OK
  90868b86_R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  R7_R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
CASE=green_render_safe_set_leaf.json
  ROLE=GREEN_CONTROL EXPECT_90868b86_RC=0 GOT=0  EXPECT_R7_RC=0 GOT=0 OK
  90868b86_R4=rendered_bytes_derive_the_declared_reachable_graph
  R7_R4=rendered_bytes_derive_the_declared_reachable_graph
CASES=6 RC_LEVEL_NEW_REDS=4 OFF_EXPECTATION=0
PREFEATURE_BLOCK_RC=0
```

Command rc: `0`. Four rc-level REDs, each `PASS rc 0` on the audited code and `STOP rc 3` now.
The GREEN control proves the same policy still admits a proven-static non-interpreter leaf,
including the function-definition form `fixture_main() { ... }` that the word-boundary change
could plausibly have broken.

## 5. D026 mutation discriminators — 7 mutations x 16 REDs

Each mutation edits exactly one production expression; the file on disk is never changed, the
mutated source is compiled and executed in memory. Every mutation is run against **all sixteen**
REDs — five round-7, seven round-6, four round-5 — and `EXPECTED_KILLS` is declared in the script
and asserted, so a mutation that kills more or less than declared fails the block.

`M1` is the discriminator the kickoff requires: put the round-6 blacklist back, character for
character, change nothing else, and watch the three extglob REDs and the unenumerated-character
RED return to `PASS`. `M2` does the same with the kickoff's own illustrative safe set. `M3`
measures the word-boundary conservation alone and finds it kills nothing. `M5` widens the safe
set to every printable character and shows the NARROWNESS is what carries the property, not the
mere presence of a whitelist.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$r5=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r5_fixtures').Path
$r6=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r6_fixtures').Path
$r7=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r7_fixtures').Path
$mutants=@'
import contextlib, io, pathlib, re, sys
TOOL = pathlib.Path(sys.argv[1])
FX5 = pathlib.Path(sys.argv[2]); FX6 = pathlib.Path(sys.argv[3]); FX7 = pathlib.Path(sys.argv[4])
SOURCE = TOOL.read_text(encoding="utf-8")

# --- production anchors, each asserted unique before it is edited ---------------
SAFE_SET_R7      = 'COMMAND_WORD_STATIC_RE = re.compile(r"^[A-Za-z0-9._/:-]+$")'
SAFE_SET_R6_BLACKLIST = 'COMMAND_WORD_STATIC_RE = re.compile(r"^[^*?\\[\\]{}~\\\\]+$")'
SAFE_SET_KICKOFF = 'COMMAND_WORD_STATIC_RE = re.compile(r"^[A-Za-z0-9._/+=:@%-]+$")'
SAFE_SET_PRINTABLE = 'COMMAND_WORD_STATIC_RE = re.compile(r"^[ -~]+$")'
BOUNDARY_R7      = '            raw += "("\n            index += 1\n'
BOUNDARY_OFF     = '            pass\n'
SUBSTITUTION_FENCE = ('    if COMMAND_WORD_SUBSTITUTION_RE.search(raw):\n'
                      '        return "dynamic"\n')
BASENAME_R6 = ('    if "/" in literal:\n'
               '        name = posixpath.basename(literal)\n'
               '        if name == "":\n'
               '            return "unmodeled"\n'
               '    else:\n'
               '        name = literal\n')
BASENAME_R5 = '    name = posixpath.basename(literal) if literal.startswith("/") else literal\n'
UNMODELED_REPORT = (
    '        elif word_class == "unmodeled":\n'
    '            # A command word that was not PROVEN static: some character of it is\n'
    '            # outside the safe set, so this module cannot show that the spelling is\n'
    '            # already the name Bash looks up.  It is refused here rather than leafed,\n'
    '            # so whatever it might resolve to - including a recognised interpreter\n'
    '            # with a script operand behind it - cannot pass through unanalysed.  Note\n'
    '            # the direction: the word is refused for lacking a proof, not for\n'
    '            # carrying an operator this round happened to recognise.\n'
    '            reasons.append("source_graph_unmodeled_command_word")\n')

MUTATIONS = {
  # THE REQUIRED DISCRIMINATOR: put the round-6 blacklist back, character for
  # character, and leave everything else round-7.
  "M1_round6_blacklist_restored":   [(SAFE_SET_R7, SAFE_SET_R6_BLACKLIST)],
  # The kickoff's own illustrative safe set, applied at round-6 word boundaries.
  "M2_kickoff_safe_set_at_r6_bounds": [(SAFE_SET_R7, SAFE_SET_KICKOFF), (BOUNDARY_R7, BOUNDARY_OFF)],
  # Word-boundary conservation alone, safe set untouched.
  "M3_word_boundary_conservation_off": [(BOUNDARY_R7, BOUNDARY_OFF)],
  # The complete round-6 command-word classifier: blacklist + round-6 boundaries +
  # the round-5 basename rule round 6 replaced.
  "M4_full_round6_classifier":      [(SAFE_SET_R7, SAFE_SET_R6_BLACKLIST), (BOUNDARY_R7, BOUNDARY_OFF),
                                     (BASENAME_R6, BASENAME_R5)],
  # The safe set exists but admits every printable character: proves the NARROWNESS
  # is load-bearing, not merely the presence of a whitelist.
  "M5_safe_set_all_printable":      [(SAFE_SET_R7, SAFE_SET_PRINTABLE)],
  # The refusal is classified but never reported.
  "M6_unmodeled_reason_deleted":    [(UNMODELED_REPORT, "")],
  # Carried round-6 guard.
  "M7_substitution_fence_deleted":  [(SUBSTITUTION_FENCE, "")],
}
EXPECTED_KILLS = {
  "M1_round6_blacklist_restored":      {"xg_plus", "xg_at", "xg_bang", "novel"},
  "M2_kickoff_safe_set_at_r6_bounds":  {"xg_plus", "xg_at", "novel"},
  "M3_word_boundary_conservation_off": set(),
  "M4_full_round6_classifier":         {"xg_plus", "xg_at", "xg_bang", "novel", "relative"},
  "M5_safe_set_all_printable":         {"xg_plus", "xg_at", "xg_bang", "xg_qmark", "novel",
                                        "glob", "bracket", "brace"},
  "M6_unmodeled_reason_deleted":       {"xg_plus", "xg_at", "xg_bang", "xg_qmark", "novel",
                                        "glob", "bracket", "brace", "tilde"},
  "M7_substitution_fence_deleted":     set(),
}
CASES = [("xg_plus",          FX7, "red_render_extglob_plus_command_word.json"),
         ("xg_at",            FX7, "red_render_extglob_at_command_word.json"),
         ("xg_bang",          FX7, "red_render_extglob_bang_command_word.json"),
         ("xg_qmark",         FX7, "red_render_extglob_qmark_command_word.json"),
         ("novel",            FX7, "red_render_novel_operator_command_word.json"),
         ("glob",             FX6, "red_render_glob_command_word.json"),
         ("bracket",          FX6, "red_render_bracket_command_word.json"),
         ("brace",            FX6, "red_render_brace_command_word.json"),
         ("tilde",            FX6, "red_render_tilde_command_word.json"),
         ("relative",         FX6, "red_render_relative_interpreter.json"),
         ("param",            FX6, "red_render_param_command_word.json"),
         ("substitution",     FX6, "red_render_substitution_command_word.json"),
         ("named_fd",         FX5, "red_render_named_fd_source.json"),
         ("indexed_assign",   FX5, "red_render_indexed_assign_source.json"),
         ("unmodeled_prefix", FX5, "red_render_unmodeled_prefix.json"),
         ("function_body",    FX5, "red_render_function_body_source.json")]
GREENS = [("green_safe_set_leaf", FX7, "green_render_safe_set_leaf.json"),
          ("green_static_leaf",   FX6, "green_render_static_leaf.json")]
R4 = re.compile(r'^CLAIM id="R4".*reason="([^"]*)"', re.MULTILINE)
def run(source, plan):
    buffer = io.StringIO(); argv = sys.argv[:]
    sys.argv = [str(TOOL), "render", str(plan)]
    try:
        with contextlib.redirect_stdout(buffer):
            exec(compile(source, str(TOOL), "exec"), {"__name__": "__main__", "__file__": str(TOOL)})
        code = 0
    except SystemExit as exc:
        code = int(exc.code or 0)
    finally:
        sys.argv = argv
    found = R4.search(buffer.getvalue())
    return code, (found.group(1) if found else "-")
off = 0
print("BASELINE unmutated round-7 code on disk")
for label, root, name in CASES:
    code, reason = run(SOURCE, root / name)
    if code != 3:
        off += 1
    print(f"  BASELINE RED={label:16s} rc={code} {'STOP' if code==3 else 'NOT_STOP'} R4={reason}")
for label, root, name in GREENS:
    code, reason = run(SOURCE, root / name)
    if code != 0:
        off += 1
    print(f"  BASELINE {label:22s} rc={code} {'PASS' if code==0 else 'NOT_PASS'}")
for mutation, edits in MUTATIONS.items():
    mutated = SOURCE
    applied = 0
    for old, new in edits:
        if mutated.count(old) != 1:
            print(f"MUTATION={mutation} ANCHOR_NOT_UNIQUE count={mutated.count(old)}")
            off += 1
            continue
        mutated = mutated.replace(old, new, 1)
        applied += 1
    if applied != len(edits) or mutated == SOURCE:
        print(f"MUTATION={mutation} NOT_APPLIED")
        off += 1
        continue
    killed = set()
    rows = []
    for label, root, name in CASES:
        code, reason = run(mutated, root / name)
        if code == 0:
            killed.add(label)
            rows.append(f"{label}=KILLED")
        elif code == 3:
            rows.append(f"{label}=SURVIVES")
        else:
            rows.append(f"{label}=ANOMALY_rc{code}")
            off += 1
    ok = killed == EXPECTED_KILLS[mutation]
    if not ok:
        off += 1
    print(f"MUTATION={mutation}")
    print(f"  EXPECTED_KILLS={sorted(EXPECTED_KILLS[mutation])} OBSERVED_KILLS={sorted(killed)} "
          f"{'OK' if ok else 'OFF_EXPECTATION'}")
    print("  " + " ".join(rows))
print(f"MUTATIONS={len(MUTATIONS)} REDS={len(CASES)} CELLS={len(MUTATIONS)*len(CASES)} OFF_EXPECTATION={off}")
sys.exit(0 if off == 0 else 1)
'@
$mutants | python -B - $tool $r5 $r6 $r7
"MUTATION_BLOCK_RC=$LASTEXITCODE"
```

Real output:

```text
BASELINE unmutated round-7 code on disk
  BASELINE RED=xg_plus          rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=xg_at            rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=xg_bang          rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=xg_qmark         rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=novel            rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=glob             rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=bracket          rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=brace            rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=tilde            rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=relative         rc=3 STOP R4=derived_graph_not_traversable,source_graph_command_word_not_modeled
  BASELINE RED=param            rc=3 STOP R4=derived_graph_not_traversable,source_graph_dynamic_command_not_modeled
  BASELINE RED=substitution     rc=3 STOP R4=derived_graph_not_traversable,source_graph_nested_execution_not_modeled
  BASELINE RED=named_fd         rc=3 STOP R4=derived_graph_not_traversable,source_graph_command_word_not_modeled
  BASELINE RED=indexed_assign   rc=3 STOP R4=derived_graph_not_traversable,source_graph_command_word_not_modeled
  BASELINE RED=unmodeled_prefix rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_assignment_prefix
  BASELINE RED=function_body    rc=3 STOP R4=derived_graph_not_traversable,source_graph_command_word_not_modeled
  BASELINE green_safe_set_leaf    rc=0 PASS
  BASELINE green_static_leaf      rc=0 PASS
MUTATION=M1_round6_blacklist_restored
  EXPECTED_KILLS=['novel', 'xg_at', 'xg_bang', 'xg_plus'] OBSERVED_KILLS=['novel', 'xg_at', 'xg_bang', 'xg_plus'] OK
  xg_plus=KILLED xg_at=KILLED xg_bang=KILLED xg_qmark=SURVIVES novel=KILLED glob=SURVIVES bracket=SURVIVES brace=SURVIVES tilde=SURVIVES relative=SURVIVES param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
MUTATION=M2_kickoff_safe_set_at_r6_bounds
  EXPECTED_KILLS=['novel', 'xg_at', 'xg_plus'] OBSERVED_KILLS=['novel', 'xg_at', 'xg_plus'] OK
  xg_plus=KILLED xg_at=KILLED xg_bang=SURVIVES xg_qmark=SURVIVES novel=KILLED glob=SURVIVES bracket=SURVIVES brace=SURVIVES tilde=SURVIVES relative=SURVIVES param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
MUTATION=M3_word_boundary_conservation_off
  EXPECTED_KILLS=[] OBSERVED_KILLS=[] OK
  xg_plus=SURVIVES xg_at=SURVIVES xg_bang=SURVIVES xg_qmark=SURVIVES novel=SURVIVES glob=SURVIVES bracket=SURVIVES brace=SURVIVES tilde=SURVIVES relative=SURVIVES param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
MUTATION=M4_full_round6_classifier
  EXPECTED_KILLS=['novel', 'relative', 'xg_at', 'xg_bang', 'xg_plus'] OBSERVED_KILLS=['novel', 'relative', 'xg_at', 'xg_bang', 'xg_plus'] OK
  xg_plus=KILLED xg_at=KILLED xg_bang=KILLED xg_qmark=SURVIVES novel=KILLED glob=SURVIVES bracket=SURVIVES brace=SURVIVES tilde=SURVIVES relative=KILLED param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
MUTATION=M5_safe_set_all_printable
  EXPECTED_KILLS=['brace', 'bracket', 'glob', 'novel', 'xg_at', 'xg_bang', 'xg_plus', 'xg_qmark'] OBSERVED_KILLS=['brace', 'bracket', 'glob', 'novel', 'xg_at', 'xg_bang', 'xg_plus', 'xg_qmark'] OK
  xg_plus=KILLED xg_at=KILLED xg_bang=KILLED xg_qmark=KILLED novel=KILLED glob=KILLED bracket=KILLED brace=KILLED tilde=SURVIVES relative=SURVIVES param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
MUTATION=M6_unmodeled_reason_deleted
  EXPECTED_KILLS=['brace', 'bracket', 'glob', 'novel', 'tilde', 'xg_at', 'xg_bang', 'xg_plus', 'xg_qmark'] OBSERVED_KILLS=['brace', 'bracket', 'glob', 'novel', 'tilde', 'xg_at', 'xg_bang', 'xg_plus', 'xg_qmark'] OK
  xg_plus=KILLED xg_at=KILLED xg_bang=KILLED xg_qmark=KILLED novel=KILLED glob=KILLED bracket=KILLED brace=KILLED tilde=KILLED relative=SURVIVES param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
MUTATION=M7_substitution_fence_deleted
  EXPECTED_KILLS=[] OBSERVED_KILLS=[] OK
  xg_plus=SURVIVES xg_at=SURVIVES xg_bang=SURVIVES xg_qmark=SURVIVES novel=SURVIVES glob=SURVIVES bracket=SURVIVES brace=SURVIVES tilde=SURVIVES relative=SURVIVES param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
MUTATIONS=7 REDS=16 CELLS=112 OFF_EXPECTATION=0
MUTATION_BLOCK_RC=0
```

Command rc: `0`. **Every mutation that removes a round-7 fence leaves all four round-5 REDs and
the round-6 `param`/`substitution`/`relative` REDs intact**, so the round-7 evidence does not
rest on a fence some other round already carried.

## 6. Command-word grammar battery — 77 declared forms and 7 word-boundary forms

All 59 round-6 forms are carried verbatim. **Six of them MOVE under the whitelist and the move is
declared in the script's CARRY column in advance**, so a silent reclassification fails the block
instead of passing it: `"bash"`, `'source'` and `"if"` move because quote characters are not in
the safe set, and `2a=b`, `--opt=val` and `a-b=c` move because `=` is not. Eighteen round-7 forms
are added. The `BOUNDARY` table measures the one place round 7 changed how a word is DELIMITED
rather than classified.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$battery=@'
import pathlib, sys, types
TOOL = pathlib.Path(sys.argv[1])
module = types.ModuleType("cpp_battery")
module.__file__ = str(TOOL)
sys.modules["cpp_battery"] = module
exec(compile(TOOL.read_text(encoding="utf-8"), str(TOOL), "exec"), module.__dict__)
classify = module._command_word_class
# ALL 59 round-6 forms are carried verbatim.  Six of them MOVE under the round-7
# whitelist and the move is declared here in advance, in the CARRY column, so a
# silent reclassification fails the block instead of passing it.
#   (raw command word, expected class under round 7, CARRY, why)
TABLE = [
    ("source",             "graph",      "SAME",  "modelled source builtin"),
    (".",                  "graph",      "SAME",  "modelled source builtin"),
    ("bash",               "graph",      "SAME",  "recognised interpreter"),
    ("/usr/bin/bash",      "graph",      "SAME",  "absolute interpreter path"),
    ("bin/bash",           "graph",      "SAME",  "relative interpreter path"),
    ("./bash",             "graph",      "SAME",  "dot-relative interpreter path"),
    ("python3.11",         "graph",      "SAME",  "versioned interpreter"),
    ("/opt/py/python3",    "graph",      "SAME",  "absolute versioned interpreter"),
    ("zsh",                "graph",      "SAME",  "recognised, deliberately outside the edge grammar"),
    ("\"bash\"",           "unmodeled",  "MOVED", "quote characters are not in the safe set"),
    ("'source'",           "unmodeled",  "MOVED", "quote characters are not in the safe set"),
    ("env",                "wrapper",    "SAME",  "runs a command from its own operands"),
    ("bin/env",            "wrapper",    "SAME",  "relative wrapper path"),
    ("xargs",              "wrapper",    "SAME",  "runs a command from its own operands"),
    ("eval",               "wrapper",    "SAME",  "runs a command from its own operands"),
    ("cat",                "leaf",       "SAME",  "proven-static non-interpreter"),
    ("/bin/cat",           "leaf",       "SAME",  "proven-static absolute non-interpreter"),
    ("bin/verify_marker",  "leaf",       "SAME",  "proven-static relative non-interpreter"),
    ("_helper",            "leaf",       "SAME",  "proven-static non-interpreter"),
    ("-f",                 "leaf",       "SAME",  "leading hyphen is an option, not an expansion"),
    ("\"if\"",             "unmodeled",  "MOVED", "quote characters are not in the safe set"),
    ("2a=b",               "unmodeled",  "MOVED", "`=` is not in the safe set"),
    ("--opt=val",          "unmodeled",  "MOVED", "`=` is not in the safe set"),
    ("a-b=c",              "unmodeled",  "MOVED", "`=` is not in the safe set"),
    ("if",                 "control",    "SAME",  "reserved word"),
    ("then",               "control",    "SAME",  "reserved word"),
    ("fi",                 "control",    "SAME",  "reserved word"),
    ("while",              "control",    "SAME",  "reserved word"),
    ("{",                  "control",    "SAME",  "group open, matched before the safe set"),
    ("}",                  "control",    "SAME",  "group close, matched before the safe set"),
    ("[[",                 "control",    "SAME",  "conditional open, matched before the safe set"),
    ("]]",                 "control",    "SAME",  "conditional close, matched before the safe set"),
    ("!",                  "control",    "SAME",  "reserved word, matched before the safe set"),
    ("function",           "control",    "SAME",  "reserved word that binds a name"),
    ("coproc",             "control",    "SAME",  "reserved word that binds a name"),
    ("A=1",                "assignment", "SAME",  "scalar assignment prefix, matched before the safe set"),
    ("A+=1",               "assignment", "SAME",  "append assignment prefix"),
    ("SEEN[0]=1",          "assignment", "SAME",  "indexed assignment prefix"),
    ("SEEN[0]+=1",         "assignment", "SAME",  "indexed append assignment prefix"),
    ("$FOO",               "dynamic",    "SAME",  "parameter expansion"),
    ("${FOO}",             "dynamic",    "SAME",  "braced parameter expansion"),
    ("x$FOO",              "dynamic",    "SAME",  "embedded parameter expansion"),
    ("$(",                 "dynamic",    "SAME",  "command substitution"),
    ("`cmd`",              "dynamic",    "SAME",  "backtick command substitution"),
    ("$((1+1))",           "dynamic",    "SAME",  "arithmetic expansion"),
    ("ba*h",               "unmodeled",  "SAME",  "pathname expansion"),
    ("/usr/bin/ba*h",      "unmodeled",  "SAME",  "pathname expansion over an absolute path"),
    ("pytho?",             "unmodeled",  "SAME",  "single-character pathname expansion"),
    ("[b]ash",             "unmodeled",  "SAME",  "bracket-expression pathname expansion"),
    ("{ba,z}sh",           "unmodeled",  "SAME",  "brace expansion"),
    ("~/bin/bash",         "unmodeled",  "SAME",  "tilde expansion"),
    ("~",                  "unmodeled",  "SAME",  "tilde expansion"),
    ("\\bash",             "unmodeled",  "SAME",  "backslash-constructed name"),
    ("\\cat",              "unmodeled",  "SAME",  "backslash-constructed name, DISCLOSED conservative stop"),
    ("[",                  "unmodeled",  "SAME",  "test builtin, DISCLOSED conservative stop"),
    ("]",                  "unmodeled",  "SAME",  "test terminator, DISCLOSED conservative stop"),
    ("~/bin/verify_marker","unmodeled",  "SAME",  "benign tilde tool, DISCLOSED conservative stop"),
    ("''",                 "unmodeled",  "SAME",  "degenerate quoting: names nothing adjudicable"),
    ("dir/",               "unmodeled",  "SAME",  "empty basename: names nothing adjudicable"),
    # --- round-7 additions: the operator family the round-6 audit found ----------
    ("ba+(",               "unmodeled",  "NEW",   "extglob one-or-more, boundary-conserved token"),
    ("ba@(",               "unmodeled",  "NEW",   "extglob exactly-one"),
    ("ba!(",               "unmodeled",  "NEW",   "extglob negated"),
    ("ba?(",               "unmodeled",  "NEW",   "extglob zero-or-one"),
    ("ba*(",               "unmodeled",  "NEW",   "extglob zero-or-more"),
    ("/usr/bin/ba+(",      "unmodeled",  "NEW",   "extglob over an absolute interpreter path"),
    ("@(",                 "unmodeled",  "NEW",   "extglob at the whole word"),
    ("+(",                 "unmodeled",  "NEW",   "extglob at the whole word"),
    # --- round-7 additions: characters NO round enumerated -----------------------
    ("%bash",              "unmodeled",  "NEW",   "job-specification character; refused for lacking a proof"),
    ("^bash",              "unmodeled",  "NEW",   "unenumerated character"),
    ("ba,sh",              "unmodeled",  "NEW",   "unenumerated character"),
    ("ba#sh",              "unmodeled",  "NEW",   "unenumerated character"),
    ("caf\u00e9",          "unmodeled",  "NEW",   "non-ASCII: outside the safe set by default"),
    ("g++",                "unmodeled",  "NEW",   "real program name, DISCLOSED conservative stop"),
    ("tool@1.0",           "unmodeled",  "NEW",   "real program name, DISCLOSED conservative stop"),
    # --- round-7 additions: the safe set must still admit a static literal -------
    (":",                  "leaf",       "NEW",   "null builtin; `:` is in the safe set"),
    ("bin/verify_marker-2.0", "leaf",    "NEW",   "hyphen, dot and digits are in the safe set"),
    ("/opt/tools:probe_1/run.check", "leaf", "NEW", "every safe-set character class in one word"),
]
off = 0
moved = 0
for raw, expected, carry, why in TABLE:
    actual = classify(raw)
    ok = actual == expected
    off += not ok
    moved += carry == "MOVED"
    print(f"WORD={raw!r:24s} EXPECT={expected:11s} ACTUAL={actual:11s} CARRY={carry:5s} "
          f"{'OK' if ok else 'OFF_EXPECTATION'}  # {why}")

# --- word-boundary conservation, measured at the scanner --------------------------
# The one place round 7 changed how a word is DELIMITED rather than classified.
# (rendered bytes, expected first raw token, expected class of that token, why)
BOUNDARY = [
    ("fixture_main() { :; }",  "fixture_main", "leaf",
     "NAME-shaped: the `(` stays a separator and the function definition is benign"),
    ("_x9() { :; }",           "_x9",          "leaf",  "NAME-shaped"),
    ("bin/foo() { :; }",       "bin/foo(",     "unmodeled",
     "not a NAME: the `(` is conserved into the token, DISCLOSED conservative stop"),
    ("ba+(s)h /lib.sh",        "ba+(",         "unmodeled", "extglob one-or-more"),
    ("ba@(s)h /lib.sh",        "ba@(",         "unmodeled", "extglob exactly-one"),
    ("ba!(x)h /lib.sh",        "ba!(",         "unmodeled", "extglob negated"),
    ("/usr/bin/ba+(s)h /lib.sh", "/usr/bin/ba+(", "unmodeled", "extglob over an absolute path"),
]
for text, want_raw, want_class, why in BOUNDARY:
    words, reason = module._shell_words(text)
    got_raw = words[0].text if words else f"SCAN_STOP:{reason}"
    got_class = classify(got_raw) if words else "-"
    ok = got_raw == want_raw and got_class == want_class
    off += not ok
    print(f"BOUNDARY TEXT={text!r:28s} EXPECT_TOKEN={want_raw!r:16s} GOT={got_raw!r:16s} "
          f"CLASS={got_class:10s} {'OK' if ok else 'OFF_EXPECTATION'}  # {why}")
print(f"TABLE_FORMS={len(TABLE)} CARRIED_MOVED={moved} BOUNDARY_FORMS={len(BOUNDARY)} "
      f"OFF_EXPECTATION={off}")
sys.exit(0 if off == 0 else 1)
'@
$battery | python -B - $tool
"BATTERY_BLOCK_RC=$LASTEXITCODE"
```

Real output (the `BOUNDARY` rows and the summary; all 77 per-form lines end `OK` and are reproduced by the command):

```text
BOUNDARY TEXT='fixture_main() { :; }'      EXPECT_TOKEN='fixture_main'   GOT='fixture_main'   CLASS=leaf       OK  # NAME-shaped: the `(` stays a separator and the function definition is benign
BOUNDARY TEXT='_x9() { :; }'               EXPECT_TOKEN='_x9'            GOT='_x9'            CLASS=leaf       OK  # NAME-shaped
BOUNDARY TEXT='bin/foo() { :; }'           EXPECT_TOKEN='bin/foo('       GOT='bin/foo('       CLASS=unmodeled  OK  # not a NAME: the `(` is conserved into the token, DISCLOSED conservative stop
BOUNDARY TEXT='ba+(s)h /lib.sh'            EXPECT_TOKEN='ba+('           GOT='ba+('           CLASS=unmodeled  OK  # extglob one-or-more
BOUNDARY TEXT='ba@(s)h /lib.sh'            EXPECT_TOKEN='ba@('           GOT='ba@('           CLASS=unmodeled  OK  # extglob exactly-one
BOUNDARY TEXT='ba!(x)h /lib.sh'            EXPECT_TOKEN='ba!('           GOT='ba!('           CLASS=unmodeled  OK  # extglob negated
BOUNDARY TEXT='/usr/bin/ba+(s)h /lib.sh'   EXPECT_TOKEN='/usr/bin/ba+('  GOT='/usr/bin/ba+('  CLASS=unmodeled  OK  # extglob over an absolute path
TABLE_FORMS=77 CARRIED_MOVED=6 BOUNDARY_FORMS=7 OFF_EXPECTATION=0
BATTERY_BLOCK_RC=0
```

Command rc: `0`.

## 7. The fixpoint property, swept over EVERY character rather than a chosen list

This is the block that distinguishes round 7 from round 6. Round 6's sweep enumerated ten
characters it already knew were dangerous and confirmed they were caught — which is exactly the
reasoning that missed `extglob`. Round 7 sweeps **all 95 printable ASCII characters plus a
non-ASCII sample**, in four positions over six bases, and asserts the property in BOTH
directions:

* a word containing any character outside the safe set is never `leaf`, `graph` or `wrapper`
  (never admitted, never promoted); and
* a word containing only safe characters is never `dynamic` or `unmodeled` (no over-refusal).

`assignment` and `control` are exempt with a stated reason: both are matched before the fence and
both LEAVE the command position open, so the real command word behind them is still classified —
neither can hide a command, which is the property under test. The block also asserts that the
safe set it sweeps against IS the safe set the module implements, so the sweep cannot drift from
the thing it measures.

A second pass runs each unsafe character as a whole rendered program and requires the refusal to
reach a terminal STOP rather than merely a class. Its third bucket is enumerated in full rather
than dropped: `' '` and `'\t'` are silent because they genuinely split the constructed token into
two words (`/usr/b` and `in/bash`), so Bash reaches `/usr/b` and nothing was hidden.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$sweep=@'
import pathlib, sys, types
TOOL = pathlib.Path(sys.argv[1])
def load(name, source):
    module = types.ModuleType(name)
    module.__file__ = str(TOOL)
    sys.modules[name] = module
    exec(compile(source, str(TOOL), "exec"), module.__dict__)
    return module
m = load("cpp", TOOL.read_text(encoding="utf-8"))
SAFE = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._/:-")
# Assert the declared safe set IS the implemented one, so this sweep cannot drift
# from the module it is measuring.
IMPLEMENTED = {chr(c) for c in range(0x20, 0x7F) if m.COMMAND_WORD_STATIC_RE.fullmatch(chr(c))}
print(f"SAFE_SET_DECLARED={''.join(sorted(SAFE))}")
print(f"SAFE_SET_IMPLEMENTED={''.join(sorted(IMPLEMENTED))}")
print(f"SAFE_SET_AGREES={SAFE == IMPLEMENTED}")
if SAFE != IMPLEMENTED:
    sys.exit(1)

# The universe is EVERY printable ASCII character plus a non-ASCII sample - not a
# list of operators this round happens to know about.  That is the point: the claim
# under test is "a character outside the safe set is never admitted", and it is only
# meaningful if the sweep does not get to choose which characters to try.
CHARS = [chr(c) for c in range(0x20, 0x7F)] + ["\u00e9", "\u0661", "\u00a0", "\u2044", "\uff42", "\t"]
BASES = ["bash", "cat", "/usr/bin/bash", "/bin/cat", "bin/verify_marker", "python3"]
POSITIONS = ("prefix", "infix", "suffix", "alone")

# Two classes are exempt and each exemption is justified, not convenient:
#   assignment - matched before the fence; an assignment prefix LEAVES the command
#                position open, so the real command word is still classified.
#   control    - a reserved word; also leaves the command position open.
# Neither can hide a command, which is the property under test.
OPEN_POSITION = {"assignment", "control"}
ADMITTED = {"leaf", "graph", "wrapper"}
REFUSED = {"dynamic", "unmodeled"}

def variant(base, char, position):
    if position == "prefix":
        return char + base
    if position == "infix":
        return base[: len(base) // 2] + char + base[len(base) // 2 :]
    if position == "suffix":
        return base + char
    return char

leak_admitted = []
leak_overrefused = []
total = 0
for char in CHARS:
    for base in BASES:
        for position in POSITIONS:
            word = variant(base, char, position)
            if position == "alone" and base != BASES[0]:
                continue  # the bare character does not depend on the base
            total += 1
            cls = m._command_word_class(word)
            unsafe = any(c not in SAFE for c in word)
            if unsafe:
                if cls in ADMITTED:
                    leak_admitted.append((word, cls))
            else:
                # A proven-static word must not be refused.  The one exception is a
                # word whose last pathname component is empty (`bin/`), which names
                # a directory rather than a program and is refused by the basename
                # rule, not by the safe set.
                if cls in REFUSED and not word.endswith("/"):
                    leak_overrefused.append((word, cls))

print(f"SWEEP_CHARS={len(CHARS)} BASES={len(BASES)} POSITIONS={len(POSITIONS)} VARIANTS={total}")
print(f"SWEEP_LEAK_ADMITTED={len(leak_admitted)}")
for word, cls in leak_admitted[:20]:
    print(f"  LEAK word={word!r} class={cls}")
print(f"SWEEP_LEAK_OVERREFUSED={len(leak_overrefused)}")
for word, cls in leak_overrefused[:20]:
    print(f"  OVERREFUSED word={word!r} class={cls}")

# --- whole-text sweep: the refusal must reach a terminal STOP, not just a class ---
# Every character is tried again as a rendered program.  Three outcomes are counted
# and the third is enumerated in full rather than dropped, because "the module was
# silent" is only acceptable when the constructed word never became a command word
# at all (a `#` prefix makes the line a comment, a `;` splits it, and so on).
def silent(text):
    if m._graph_opaque_reason(text) is not None:
        return False
    src = list(m.SOURCE_COMMAND_RE.finditer(text))
    exe = list(m.EXEC_COMMAND_RE.finditer(text))
    return not src and not exe and not m._graph_word_conservation(text, src, exe)

not_silent = 0
never_a_command_word = []
silent_leak = []
for char in CHARS:
    word = variant("/usr/bin/bash", char, "infix")
    if not any(c not in SAFE for c in word):
        continue
    text = f"{word} /safe/fixture/library.sh\n"
    if not silent(text):
        not_silent += 1
        continue
    words, reason = m._shell_words(text)
    if words is not None and any(w.command_position and w.text == word for w in words):
        silent_leak.append((char, word))
    else:
        never_a_command_word.append(char)
print(f"WHOLE_TEXT_UNSAFE_CHARS={not_silent + len(never_a_command_word) + len(silent_leak)} "
      f"NOT_SILENT={not_silent} NEVER_A_COMMAND_WORD={len(never_a_command_word)} "
      f"SILENT_LEAK={len(silent_leak)}")
print(f"  NEVER_A_COMMAND_WORD_CHARS={[repr(c) for c in never_a_command_word]}")
for char, word in silent_leak:
    print(f"  SILENT_LEAK char={char!r} word={word!r}")
bad = len(leak_admitted) + len(leak_overrefused) + len(silent_leak)
print(f"SWEEP_TOTAL_LEAKS={bad}")
sys.exit(0 if bad == 0 else 1)
'@
$sweep | python -B - $tool
"SWEEP_BLOCK_RC=$LASTEXITCODE"
```

Real output:

```text
SAFE_SET_DECLARED=-./0123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz
SAFE_SET_IMPLEMENTED=-./0123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz
SAFE_SET_AGREES=True
SWEEP_CHARS=101 BASES=6 POSITIONS=4 VARIANTS=1919
SWEEP_LEAK_ADMITTED=0
SWEEP_LEAK_OVERREFUSED=0
WHOLE_TEXT_UNSAFE_CHARS=34 NOT_SILENT=32 NEVER_A_COMMAND_WORD=2 SILENT_LEAK=0
  NEVER_A_COMMAND_WORD_CHARS=["' '", "'\\t'"]
SWEEP_TOTAL_LEAKS=0
SWEEP_BLOCK_RC=0
```

Command rc: `0`. `SWEEP_TOTAL_LEAKS=0` over 1919 variants.

## 8. Carried batteries and discriminators

### 8a. The round-5 prefix battery, re-run under round-7 code

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$carried=@'
import json, pathlib, subprocess, sys, tempfile
TOOL = pathlib.Path(sys.argv[1]).resolve()
# The round-5 battery, re-run under round-7 code.  Every form keeps the round-5
# expectation except the one declared MOVED below.
BLIND = [
    ("named_fd_out",            '{fd}>/dev/null source "$LIBRARY_PATH"', 3),
    ("named_fd_in",             '{fd}</dev/null source "$LIBRARY_PATH"', 3),
    ("named_fd_append",         '{fd}>>/safe/fixture/out.log source "$LIBRARY_PATH"', 3),
    ("named_fd_dup",            '{fd}>&2 source "$LIBRARY_PATH"', 3),
    ("named_fd_bash",           '{fd}>/dev/null bash /safe/fixture/library.sh', 3),
    ("named_fd_after_scalar",   'LC_ALL=C {fd}>/dev/null source "$LIBRARY_PATH"', 3),
    ("indexed_assign",          'SEEN[0]=1 source "$LIBRARY_PATH"', 3),
    ("indexed_append",          'SEEN[0]+=1 source "$LIBRARY_PATH"', 3),
    ("indexed_quoted_sub",      'SEEN["a b"]=1 source "$LIBRARY_PATH"', 3),
    ("indexed_assign_bash",     'SEEN[0]=1 bash /safe/fixture/library.sh', 3),
    ("indexed_then_scalar",     'SEEN[0]=1 LC_ALL=C source "$LIBRARY_PATH"', 3),
    ("nested_subscript",        'SEEN[IDX[0]]=1 source "$LIBRARY_PATH"', 3),
    ("function_body_source",    'function reload { source "$LIBRARY_PATH"; }', 3),
    ("function_body_bash",      'function run { bash /safe/fixture/library.sh; }', 3),
    ("coproc_named_body",       'coproc logger { source "$LIBRARY_PATH"; }', 3),
    ("every_prefix_at_once",    'LC_ALL=C {fd}>/dev/null SEEN[0]=1 source "$LIBRARY_PATH"', 3),
]
CONTROLS = [
    ("operand_named_bash",      'echo bash', 0),
    ("word_containing_bash",    'cat "$ROOT/notes.bash"', 0),
    ("numeric_fd_redirection",  'cat "$ROOT/in.txt" 2> /safe/fixture/err.log', 0),
    ("leaf_with_dot_in_path",   'cat /safe/fixture/a.sh.b', 0),
    ("comment_mentions_source", '# source /safe/fixture/library.sh', 0),
    ("indexed_assign_leaf",     'SEEN[0]=1 cat "$ROOT/in.txt"', 0),
    ("named_fd_leaf",           '{fd}>/dev/null cat "$ROOT/in.txt"', 0),
    ("word_abutting_redirect",  'cat>/safe/fixture/out.log', 0),
]
# Declared in advance: forms whose round-5 disposition CHANGES under the closed
# command-word policy, and the round-5 false stop that is carried unchanged.
DISCLOSED_STOPS = [
    ("subscript_word_no_equal", 'SEEN[0] "$ROOT/in.txt"', 3,
     "MOVED: round-5 control rc 0 -> round-7 disclosed conservative stop; SEEN[0] is a "
     "bracket-expression pathname-expansion token in command position"),
    ("brace_non_name_fd",       '{1}>/dev/null cat "$ROOT/in.txt"', 3,
     "CARRIED: round-5 disclosed false stop, unchanged"),
]
def build(root, name, body):
    template = ("#!/usr/bin/env bash\nROOT='{{REMOTE_BASE}}'\nRUNID='{{RUNID}}'\n"
                f"{body}\n" 'cat "$ROOT/$RUNID/input.txt"\n').encode()
    rendered = (template.replace(b"{{REMOTE_BASE}}", b"/safe/fixture")
                        .replace(b"{{RUNID}}", b"WPI-FIXTURE-FREEZE"))
    (root / f"{name}.sh.in").write_bytes(template)
    (root / f"{name}.sh").write_bytes(rendered)
    plan = {"schema": "sec102-composite-plan-v1", "stage": "render", "composites": [{
        "id": "grammar", "entrypoint": "entry",
        "members": [{"id": "entry", "kind": "shell", "path": f"{name}.sh",
                     "deploy_path": "/safe/fixture/entry.sh"}],
        "edges": [],
        "allocation_requirements": [
            {"name": "REMOTE_BASE", "kind": "absolute_path", "consumers": ["entry"]},
            {"name": "RUNID", "kind": "safe_component", "consumers": ["entry"]}],
        "allocations": [{"name": "REMOTE_BASE", "value": "/safe/fixture"},
                        {"name": "RUNID", "value": "WPI-FIXTURE-FREEZE"}],
        "proof": {"render_templates": [{"member": "entry", "template": f"{name}.sh.in"}]}}]}
    path = root / f"{name}.json"
    path.write_text(json.dumps(plan), encoding="utf-8")
    return path
def run_new(plan):
    done = subprocess.run([sys.executable, "-B", str(TOOL), "render", str(plan)],
                          capture_output=True, text=True)
    reason = "-"
    for line in done.stdout.splitlines():
        if line.startswith('CLAIM id="R4"'):
            reason = line.split("reason=", 1)[1].strip('"')
    return done.returncode, reason
off = 0
with tempfile.TemporaryDirectory(prefix="sec102-r7-carried-") as tmp:
    root = pathlib.Path(tmp)
    for group, rows in (("BLIND", BLIND), ("CONTROL", CONTROLS)):
        for name, body, want in rows:
            rc, reason = run_new(build(root, name, body))
            ok = rc == want
            off += not ok
            print(f"{group}={name:26s} EXPECT_RC={want} R7_RC={rc} "
                  f"{'OK' if ok else 'OFF_EXPECTATION'} R7_REASON={reason}")
    for name, body, want, note in DISCLOSED_STOPS:
        rc, reason = run_new(build(root, name, body))
        ok = rc == want
        off += not ok
        print(f"DISCLOSED={name:24s} EXPECT_RC={want} R7_RC={rc} "
              f"{'OK' if ok else 'OFF_EXPECTATION'} R7_REASON={reason}")
        print(f"    NOTE {note}")
print(f"BLIND={len(BLIND)} CONTROLS={len(CONTROLS)} DISCLOSED={len(DISCLOSED_STOPS)} OFF_EXPECTATION={off}")
sys.exit(0 if off == 0 else 1)
'@
$carried | python -B - $tool
"CARRIED_BATTERY_RC=$LASTEXITCODE"
```

Real output:

```text
BLIND=named_fd_out               EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=named_fd_in                EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=named_fd_append            EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=named_fd_dup               EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=named_fd_bash              EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=named_fd_after_scalar      EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=indexed_assign             EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=indexed_append             EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=indexed_quoted_sub         EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=indexed_assign_bash        EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=indexed_then_scalar        EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=nested_subscript           EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_unmodeled_assignment_prefix
BLIND=function_body_source       EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=function_body_bash         EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=coproc_named_body          EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND=every_prefix_at_once       EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
CONTROL=operand_named_bash         EXPECT_RC=0 R7_RC=0 OK R7_REASON=rendered_bytes_derive_the_declared_reachable_graph
CONTROL=word_containing_bash       EXPECT_RC=0 R7_RC=0 OK R7_REASON=rendered_bytes_derive_the_declared_reachable_graph
CONTROL=numeric_fd_redirection     EXPECT_RC=0 R7_RC=0 OK R7_REASON=rendered_bytes_derive_the_declared_reachable_graph
CONTROL=leaf_with_dot_in_path      EXPECT_RC=0 R7_RC=0 OK R7_REASON=rendered_bytes_derive_the_declared_reachable_graph
CONTROL=comment_mentions_source    EXPECT_RC=0 R7_RC=0 OK R7_REASON=rendered_bytes_derive_the_declared_reachable_graph
CONTROL=indexed_assign_leaf        EXPECT_RC=0 R7_RC=0 OK R7_REASON=rendered_bytes_derive_the_declared_reachable_graph
CONTROL=named_fd_leaf              EXPECT_RC=0 R7_RC=0 OK R7_REASON=rendered_bytes_derive_the_declared_reachable_graph
CONTROL=word_abutting_redirect     EXPECT_RC=0 R7_RC=0 OK R7_REASON=rendered_bytes_derive_the_declared_reachable_graph
DISCLOSED=subscript_word_no_equal  EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_unmodeled_command_word
    NOTE MOVED: round-5 control rc 0 -> round-7 disclosed conservative stop; SEEN[0] is a bracket-expression pathname-expansion token in command position
DISCLOSED=brace_non_name_fd        EXPECT_RC=3 R7_RC=3 OK R7_REASON=derived_graph_not_traversable,source_graph_unmodeled_redirection_prefix
    NOTE CARRIED: round-5 disclosed false stop, unchanged
BLIND=16 CONTROLS=8 DISCLOSED=2 OFF_EXPECTATION=0
CARRIED_BATTERY_RC=0
```

Command rc: `0`. All 16 blind forms still STOP, all 8 controls still pass, and both round-6
disclosed stops are unchanged. **No form moved between round 6 and round 7 in this battery.**

### 8b. The five carried round-3 and round-4 discriminators

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$r3=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures').Path
$r4=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r4_fixtures').Path
$carried=@'
import contextlib, io, pathlib, sys
TOOL = pathlib.Path(sys.argv[1]); R3 = pathlib.Path(sys.argv[2]); R4 = pathlib.Path(sys.argv[3])
SOURCE = TOOL.read_text(encoding="utf-8")
DISCRIMINATORS = [
  ("R3F1_basename_fallback_restored", "freeze", R3 / "red_freeze_deploy_identity.json", {
    "    return deploy_to_id.get(identity)":
      "    if identity in deploy_to_id:\n        return deploy_to_id[identity]\n"
      "    fallback = [value for key, value in deploy_to_id.items()\n"
      "                if posixpath.basename(key) == posixpath.basename(operand)]\n"
      "    return fallback[0] if len(fallback) == 1 else None",
    "                target = deploy_to_id.get(_canonical_deployed_path(operand) or \"\")":
      "                target = _member_for_operand(operand, deploy_to_id)"}),
  ("R3F2_allocation_constants_comparisons_disabled", "freeze", R3 / "red_freeze_allocation_constants.json", {
    "        elif binding.value != allocation_values[binding.name]:":
      "        elif False and binding.value != allocation_values[binding.name]:",
    "        elif binding.value != allocation.value:":
      "        elif False and binding.value != allocation.value:",
    "                if constants_operand != operand:":
      "                if False and constants_operand != operand:"}),
  ("R3F3_non_shell_graph_stop_reverted", "render", R3 / "red_render_non_shell_member.json", {
    "            recorder.record(claim_id, Verdict.STOP, \"member_kind_graph_derivation_not_modeled\")\n"
    "            derivation_blocked = True\n            continue": "            continue"}),
  ("R4F1_command_word_conservation_deleted", "render", R4 / "red_render_wrapped_source.json", {
    "            for reason in _graph_word_conservation(text, source_matches, exec_matches):":
      "            for reason in ():"}),
  ("R4F2_absent_allocation_disposition_reverted", "freeze", R4 / "red_freeze_allocation_absent.json", {
    "        elif binding is None:\n            disposition, reason = \"STOP\", \"allocation_absent_from_pinned_constants\"":
      "        elif binding is None:\n            disposition, reason = \"RECONCILED\", \"allocation_and_constants_byte_equal\""}),
]
restored = 0
for name, stage, plan, mutations in DISCRIMINATORS:
    mutated = SOURCE
    for old, new in mutations.items():
        assert mutated.count(old) == 1, (name, old[:50])
        mutated = mutated.replace(old, new)
    buffer = io.StringIO(); argv = sys.argv[:]
    sys.argv = [str(TOOL), stage, str(plan)]
    try:
        with contextlib.redirect_stdout(buffer):
            exec(compile(mutated, str(TOOL), "exec"), {"__name__": "__main__", "__file__": str(TOOL)})
        code = 0
    except SystemExit as exc:
        code = int(exc.code or 0)
    finally:
        sys.argv = argv
    restored += code == 0
    print(f"MUTATION={name} CASE={plan.name} MUTANT_RC={code} REQUIRED_RED_RC=3 "
          f"{'RED_RESTORED_TO_PASS' if code == 0 else 'DISCRIMINATOR_BROKEN'}")
print(f"CARRIED_DISCRIMINATORS={len(DISCRIMINATORS)} RESTORED_DEFECTIVE_PASS={restored}")
sys.exit(0 if restored == len(DISCRIMINATORS) else 1)
'@
$carried | python -B - $tool $r3 $r4
"CARRIED_DISCRIMINATOR_RC=$LASTEXITCODE"
```

Real output:

```text
MUTATION=R3F1_basename_fallback_restored CASE=red_freeze_deploy_identity.json MUTANT_RC=0 REQUIRED_RED_RC=3 RED_RESTORED_TO_PASS
MUTATION=R3F2_allocation_constants_comparisons_disabled CASE=red_freeze_allocation_constants.json MUTANT_RC=0 REQUIRED_RED_RC=3 RED_RESTORED_TO_PASS
MUTATION=R3F3_non_shell_graph_stop_reverted CASE=red_render_non_shell_member.json MUTANT_RC=0 REQUIRED_RED_RC=3 RED_RESTORED_TO_PASS
MUTATION=R4F1_command_word_conservation_deleted CASE=red_render_wrapped_source.json MUTANT_RC=0 REQUIRED_RED_RC=3 RED_RESTORED_TO_PASS
MUTATION=R4F2_absent_allocation_disposition_reverted CASE=red_freeze_allocation_absent.json MUTANT_RC=0 REQUIRED_RED_RC=3 RED_RESTORED_TO_PASS
CARRIED_DISCRIMINATORS=5 RESTORED_DEFECTIVE_PASS=5
CARRIED_DISCRIMINATOR_RC=0
```

Command rc: `0`. All five still restore their defective `PASS`, so no earlier round's guard was
weakened while the command-word policy was rewritten.

## 9. Hygiene, determinism and carried byte identity

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$base='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1'
$hygiene=@'
import ast, hashlib, json, pathlib, subprocess, sys
BASE = pathlib.Path(sys.argv[1])
TOOL = BASE / "composite_pathproof.py"
R7 = BASE / "sec102_r7_fixtures"
ALLOC = {"REMOTE_BASE": "/safe/fixture", "RUNID": "WPI-FIXTURE-FREEZE",
         "LIBRARY_PATH": "/safe/fixture/library.sh"}
off = 0

# 1. The repaired module still parses as Python.
try:
    ast.parse(TOOL.read_text(encoding="utf-8"))
    print(f"AST_PARSE={TOOL.name} OK python={sys.version.split()[0]}")
except SyntaxError as exc:
    print(f"AST_PARSE={TOOL.name} FAILED {exc}")
    off += 1

# 2. Every round-7 plan is well-formed JSON.
plans = sorted(R7.glob("*.json"))
for plan in plans:
    try:
        json.loads(plan.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"JSON_PARSE={plan.name} FAILED {exc}")
        off += 1
print(f"JSON_PLANS={len(plans)} PARSED_OK={len(plans) - off}")

# 3. Every round-7 fixture byte is LF-only, so the .gitattributes pin has something
#    stable to protect and a CRLF checkout cannot silently change a SHA-256.
crlf = [p.name for p in sorted(R7.iterdir()) if b"\r" in p.read_bytes()]
print(f"R7_FIXTURE_FILES={len(list(R7.iterdir()))} FILES_CONTAINING_CR={len(crlf)} {crlf}")
off += len(crlf)

# 4. Every rendered .sh equals its .in with the fixture allocations substituted, so a
#    hand-edited fixture cannot silently disagree with what RENDER proves.
mismatched = []
templates = sorted(R7.glob("*.sh.in"))
for template in templates:
    rendered = R7 / template.name[:-3]
    expected = template.read_bytes()
    for name, value in ALLOC.items():
        expected = expected.replace(("{{" + name + "}}").encode(), value.encode())
    if rendered.read_bytes() != expected:
        mismatched.append(rendered.name)
print(f"TEMPLATE_PAIRS={len(templates)} RENDER_IDENTITY_MISMATCHES={len(mismatched)} {mismatched}")
off += len(mismatched)

# 5. Determinism: repeated runs of two new REDs and the new GREEN must be
#    byte-identical on stdout.
for name in ("red_render_extglob_plus_command_word.json",
             "red_render_novel_operator_command_word.json",
             "green_render_safe_set_leaf.json"):
    outs = set()
    codes = set()
    for _ in range(3):
        done = subprocess.run([sys.executable, "-B", str(TOOL), "render", str(R7 / name)],
                              capture_output=True, text=True)
        outs.add(done.stdout)
        codes.add(done.returncode)
    ok = len(outs) == 1 and len(codes) == 1
    off += not ok
    print(f"DETERMINISM={name} RUNS=3 DISTINCT_STDOUT={len(outs)} DISTINCT_RC={len(codes)} "
          f"{'OK' if ok else 'NON_DETERMINISTIC'}")

# 6. No carried tracked artifact was edited by this round.  Round 8 is an evidence-
#    harness repair, so composite_pathproof.py and .gitattributes are in this list
#    too: round 8's central claim is that NO CODE CHANGED, and this measures it
#    rather than asserting it.  sec102_r7_fixtures is now a carried tree as well.
carried = ["composite_pathproof.py", ".gitattributes", "pathscope_prover.py",
           "sec102_r1_fixtures", "sec102_r2_fixtures", "sec102_r3_fixtures",
           "sec102_r4_fixtures", "sec102_r5_fixtures", "sec102_r6_fixtures",
           "sec102_r7_fixtures"]
for name in carried:
    done = subprocess.run(["git", "status", "--porcelain", "--",
                           f"MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/{name}"],
                          capture_output=True, text=True)
    dirty = [line for line in done.stdout.splitlines() if line.strip()]
    off += len(dirty)
    print(f"CARRIED_CLEAN={name:22s} WORKTREE_CHANGES={len(dirty)} {dirty}")

print(f"HYGIENE_OFF_EXPECTATION={off}")
sys.exit(0 if off == 0 else 1)
'@
$hygiene | python -B - $base
"HYGIENE_BLOCK_RC=$LASTEXITCODE"
```

Real output:

```text
AST_PARSE=composite_pathproof.py OK python=3.14.2
JSON_PLANS=6 PARSED_OK=6
R7_FIXTURE_FILES=18 FILES_CONTAINING_CR=0 []
TEMPLATE_PAIRS=6 RENDER_IDENTITY_MISMATCHES=0 []
DETERMINISM=red_render_extglob_plus_command_word.json RUNS=3 DISTINCT_STDOUT=1 DISTINCT_RC=1 OK
DETERMINISM=red_render_novel_operator_command_word.json RUNS=3 DISTINCT_STDOUT=1 DISTINCT_RC=1 OK
DETERMINISM=green_render_safe_set_leaf.json RUNS=3 DISTINCT_STDOUT=1 DISTINCT_RC=1 OK
CARRIED_CLEAN=composite_pathproof.py WORKTREE_CHANGES=0 []
CARRIED_CLEAN=.gitattributes         WORKTREE_CHANGES=0 []
CARRIED_CLEAN=pathscope_prover.py    WORKTREE_CHANGES=0 []
CARRIED_CLEAN=sec102_r1_fixtures     WORKTREE_CHANGES=0 []
CARRIED_CLEAN=sec102_r2_fixtures     WORKTREE_CHANGES=0 []
CARRIED_CLEAN=sec102_r3_fixtures     WORKTREE_CHANGES=0 []
CARRIED_CLEAN=sec102_r4_fixtures     WORKTREE_CHANGES=0 []
CARRIED_CLEAN=sec102_r5_fixtures     WORKTREE_CHANGES=0 []
CARRIED_CLEAN=sec102_r6_fixtures     WORKTREE_CHANGES=0 []
CARRIED_CLEAN=sec102_r7_fixtures     WORKTREE_CHANGES=0 []
HYGIENE_OFF_EXPECTATION=0
HYGIENE_BLOCK_RC=0
```

Command rc: `0`. **`CARRIED_CLEAN=composite_pathproof.py WORKTREE_CHANGES=0` is round 8's central
claim, measured:** the module this document adjudicates has no worktree modification, so every
classification transcript above is the round-7 code re-executed rather than a new build.
`.gitattributes` is clean for the same reason — round 8 adds no fixture, so there is nothing to
pin. Round 8 ran under **Python 3.14.2**; nothing here establishes behaviour under any other
interpreter version (`STATUS_SEC102.md` item 15).

## 10. Artifact identity

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$base='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1'
$identity=@'
import hashlib, pathlib, sys
BASE = pathlib.Path(sys.argv[1]).resolve()
# The three evidence documents are re-derived by appending them to this list.  Their
# digests are deliberately NOT transcribed in the self-QA: a document cannot contain
# its own digest, and a partially self-referential table is exactly what Pattern 10
# warns about.  The Lead derives all three at commit time.
NAMES = ["composite_pathproof.py", ".gitattributes"]
paths = [BASE / n for n in NAMES] + sorted((BASE / "sec102_r7_fixtures").iterdir())
for path in paths:
    data = path.read_bytes()
    print(f"{path.relative_to(BASE).as_posix():<52} bytes={len(data):<7} "
          f"sha256={hashlib.sha256(data).hexdigest()}")
'@
$identity | python -B - $base
"IDENTITY_BLOCK_RC=$LASTEXITCODE"
```

Real output:

```text
composite_pathproof.py                               bytes=129658  sha256=adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a
.gitattributes                                       bytes=1630    sha256=40e356f814c61d1435d60391b53f60c7fdde9924dddc305fda0c8344d9805077
sec102_r7_fixtures/entry_extglob_at_command_word.sh  bytes=187     sha256=f830ea03a7fccc0cae177e57146e541f39569092a353eaaf091091df2fb4f99d
sec102_r7_fixtures/entry_extglob_at_command_word.sh.in bytes=164     sha256=59eed55fc31f0922ee1bfda2c3d6060c6679c79033ed19d00851dd9d5421c566
sec102_r7_fixtures/entry_extglob_bang_command_word.sh bytes=187     sha256=f6c6cfad2a911d951cb725cf013af7c780f46f17c1e7cf33e47e6475c82d6658
sec102_r7_fixtures/entry_extglob_bang_command_word.sh.in bytes=164     sha256=276a3f62752423d9191a177b4e33f25a9e00232631693257c199311493cdaf50
sec102_r7_fixtures/entry_extglob_plus_command_word.sh bytes=187     sha256=ed4b1acd7dbddea3ca7191d7f22be5d27265e11d2ac28392f3a29f31e0427c34
sec102_r7_fixtures/entry_extglob_plus_command_word.sh.in bytes=164     sha256=246522997fb2248a7bc5e9b5d3d124d740de1cd6388dfd77af9a533548ce3e6a
sec102_r7_fixtures/entry_extglob_qmark_command_word.sh bytes=187     sha256=43bcde04b1ce48cfaf425dc877733c2a2e995df6972e9d77f671814b523b7b71
sec102_r7_fixtures/entry_extglob_qmark_command_word.sh.in bytes=164     sha256=93136b8b0e17fd723369851bdff12a0f9a6fd092cbc230b6e7d38ad8e7d8d159
sec102_r7_fixtures/entry_novel_operator_command_word.sh bytes=176     sha256=8cf2998e2c68408b54e437d83034015fced10d4f8c2a627172cb9226924f81b9
sec102_r7_fixtures/entry_novel_operator_command_word.sh.in bytes=153     sha256=7240b95d74a613b9ca3d355b31d63299d34e7ae0cba4709f7c3cf49c4d1e3d74
sec102_r7_fixtures/entry_safe_set_leaf.sh            bytes=239     sha256=1b5d98008e54c66ec40fdd50ceb80705934bc0106d53922703a82002451070bf
sec102_r7_fixtures/entry_safe_set_leaf.sh.in         bytes=224     sha256=652c340d9489561402934a3dadd9d4e01bc55e40458186bdd5ed8bfbaecb18ad
sec102_r7_fixtures/green_render_safe_set_leaf.json   bytes=1336    sha256=e4bcc5b81360bef2c6b3bda20b622807fb7ac620e822c7461a1e4d338852ed1f
sec102_r7_fixtures/red_render_extglob_at_command_word.json bytes=1366    sha256=71db2bfe01ad99fab1f24aaafb85c2a579219f0e30cbecd7b32fe615687ef1f3
sec102_r7_fixtures/red_render_extglob_bang_command_word.json bytes=1372    sha256=ebfe1ae713bae6d87785d9ed5d144f1656c6ad88e67cb74f9fc405e43ca77b88
sec102_r7_fixtures/red_render_extglob_plus_command_word.json bytes=1372    sha256=baa7f1b00a818fd05b901936811d206cc9ea544b2ea9efa2b6b9e0dd39a75fbd
sec102_r7_fixtures/red_render_extglob_qmark_command_word.json bytes=1375    sha256=d3bea1e63766d3314ed79c1e47904a5874e8b022fee189e1d8e3e2f15276b10c
sec102_r7_fixtures/red_render_novel_operator_command_word.json bytes=1378    sha256=317840951dc37141b989f6a7b23bca1769316ff4d5e4367b8a8bc33713f1fc14
IDENTITY_BLOCK_RC=0
```

The three evidence documents (`SELF_QA_SEC102_R8.md`, `STATUS_SEC102.md` and
`SEC102_R8_REPORT_2026-08-11.md`) are re-derived by appending them to the `NAMES` list in the
command above. Their SHA-256 values are deliberately **not** transcribed here: a document cannot
contain its own digest, and a partially self-referential table is exactly what Pattern 10 warns
about. The Lead derives all three at commit time.

**Every byte above is the round-7 table, unchanged.** `composite_pathproof.py` is still
`129658` B / `adbf27fd…c05a` and `.gitattributes` is still `1630` B / `40e356f8…5077`, because
round 8 changed no code and added no fixture. Section 9 measures the same fact from the other
direction, as a worktree-clean assertion.

`pathscope_prover.py` was not touched and its pin (`122446` B /
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`) is unchanged; the FREEZE
GREEN transcripts in section 3 are the running proof of it.

## 11. Honest residual scope — what rounds 7 and 8 do NOT close

The full carried list is `STATUS_SEC102.md` items 1-40, updated for round 8.

### Round-8 statements — the harness

1. **The harness now proves that each child ran to completion; it does not prove the child ran
   the right thing.** Status 0 with empty stderr plus a stdout subset match is a much stronger
   acceptance than round 7's, and it is still an acceptance of *observed output from a process
   this document itself wrote*. Nothing here establishes that the extracted block is the block
   the Lead would have typed, beyond byte-identity with the fence.
2. **The comparison is still a SUBSET check.** A block may emit more than it publishes, and a
   declared excerpt (section 6) passes on the lines it publishes. Round 8 does not make the
   published transcript exhaustive, and claiming it did would be the same overreach the round-7
   finding punished.
3. **The empty `STDERR_CONTRACT` is a property of this document, not a general rule.** A future
   round whose block legitimately writes to stderr must add a named entry with a written reason;
   the mechanism exists so that such a block is *adjudicated* rather than silently tolerated.
   An entry never waives test (1): an adjudicated diagnostic is not an adjudicated failure.
4. **The outer wrapper's own status is adjudicated by whoever runs it, not by itself.** Section
   13c publishes the outer process status and stderr byte count as measured by the shell that
   launched it. A wrapper cannot be the sole witness to its own completion, and this one does not
   claim to be.
5. **Round 8 measures no new property of `composite_pathproof.py`.** Every classification claim
   in this document is the round-7 claim re-executed. If the round-7 evidence was wrong about the
   module, round 8 does not detect that; it only guarantees that a block which *fails* can no
   longer be reported as reproduced.
6. **The four D026 children are synthetic and harmless.** They print a line, exit non-zero, or
   write one diagnostic. They are a test of the instrument, not of shell grammar, and no attack
   fixture and no sensitive body was authored for them.

### Round-7 statements, carried

The round-7-specific statements:

1. **The recognised-interpreter VOCABULARY is still a list, and this is the production-gate
   blocker.** Round 7 changed *how a command word is admitted*; it did not change *which names
   are recognised*. A proven-static literal made only of safe characters that names an
   executable-capable program absent from `GRAPH_INTERPRETER_WORDS` is still a benign leaf. The
   round-6 audit accepted this as a scoped limitation; round 7 does not weaken that acceptance
   and does not claim to have narrowed it further.
2. **The safe set is a claim about Bash, and it is exactly as strong as one reading of the Bash
   grammar.** The inversion means an unknown character is refused rather than admitted, so an
   error in that reading now produces a false STOP instead of a false PASS. That is a strictly
   better failure direction, not a proof of correctness.
3. **The conservative false stops are larger than round 6's, and they are refusals, not
   detections.** New in round 7: any command word containing `+`, `@`, `%`, `=`, `,`, `^`, `#`,
   a quote character, or any non-ASCII character now STOPs — so `g++`, `tool@1.0`,
   `--opt=value`, `"bash"` and `café` all STOP although Bash would run them harmlessly. Carried
   from round 6: `[ -f x ]`, `\cat`, `~/bin/mytool`, `SEEN[0] "$ROOT/in.txt"`.
4. **A non-NAME function definition is a new false stop.** `bin/foo() { ...; }` STOPs because
   the scanner cannot tell it from an `extglob` pattern without deciding which shell options are
   set. Bash does accept some non-NAME function names; this refuses them.
5. **The word-boundary conservation covers `(` only.** A `)` abutting a word is still treated as
   a separator, because subshell and `case` syntax depend on that and no `extglob` construct
   begins at a `)`. This is an argument from the Bash grammar, not a sweep.
6. **Quoted occurrences are still not excused,** for the round-6 reason: deciding that quoting
   suppressed a specific expansion is the class of reasoning that produced R5-F1.
7. **Nothing outside the command word moved.** Operand grammar, prefix grammar, the analysis
   unit, FREEZE, the prover adapter and every host/network non-claim are unchanged from round 6.
8. **`M3` shows the word-boundary conservation kills nothing on its own.** It is published as a
   correctness fix to what the classifier is shown, not as an independent guard.

## 12. Thirteen-pattern self-adjudication

| Pattern | Round-8 self-assessment |
|---|---|
| 1 — STOP/PASS/FAIL ordering | Unchanged; 58-case matrix asserts every rc. |
| 2 — Host and namespace identity | Unchanged non-claim; no host contacted. |
| 3 — Host-object, symlink, mount identity | Unchanged explicit non-claim. |
| 4 — External interpreter/environment boundary | Unchanged disclosed production blocker (residual 1 of the round-7 list). |
| 5 — Grammar incompleteness | The round-6 finding, closed in round 7 by inverting the test so incompleteness produces a STOP rather than an admission; swept over every printable character in section 7. Codex r7 judged the whitelist a fixpoint for the class. Unchanged by round 8. |
| 6 — Probe status before adjudication | **THE ROUND-7 FINDING, and the round-8 repair.** The harness read stdout without ever reading the child's process status or stderr. Section 13a now proves status 0 and adjudicated stderr *before* stdout is read at all; a child failing either test has its stdout left uninterpreted. Section 13b measures this as RED-before-GREEN against the published round-7 wrapper. Every block's real rc and stderr byte count is published in section 13c. |
| 7 — Incomplete-reader path | Unchanged in the module. In the harness, an incomplete child run is now a terminal REJECT with its output discarded, rather than a silent read of a partial stream. |
| 8 — Deployed identity | Unchanged lexical scope. |
| 9 — Claim wording vs predicate | Carried from round 7. Round 8 adds one claim and narrows it in advance: the harness proves *execution completeness plus published-subset presence*, not that the transcript is exhaustive (residual 2 of the round-8 list). |
| 10 — Declared vs executed evidence | **Also the round-7 finding**, as the overlay on Pattern 6: the outer verifier could false-accept an incomplete child. Repaired with Pattern 6. Additionally, the round-8 discriminator does not re-type either wrapper — it extracts both from the published documents and prints the SHA-256 of the exact bytes it executed, so the instrument under test is the instrument on the page. |
| 11 — Instrument defects | The round-7 sweep asserts that the safe set it measures against equals the one the module implements. Round 8 extends that discipline to the harness itself: section 13b asserts each document publishes exactly one `python` fence and pins the digest of the program it ran, so a re-typed or drifted wrapper fails the block instead of passing it. |
| 12 — Unmodeled behavior disappearing | The classifier's default is refusal; `SWEEP_LEAK_ADMITTED=0` and `SILENT_LEAK=0` are the measurements. The harness's default is now also refusal: a block is reproduced only by passing all three tests. |
| 13 — Terminal-disposition conservation | Unchanged; every RED reaches a terminal STOP with a reason token, verified in sections 3-5. The harness's own rejections are terminal too — each carries a named reason token and forces a non-zero wrapper exit. |

## 13. Paste-and-run verification of this document

Every fenced `powershell` block above is extracted byte-for-byte, written to a `.ps1` outside the
repository, and executed from a working directory outside the repository. **Round 8 changes what
happens next.** The round-7 wrapper compared the child's stdout with the published transcript and
never looked at anything else; the round-8 wrapper first proves the child ran to completion, and
only a child that did so has its output read at all.

### 13a. What the round-8 wrapper adjudicates, in order

| # | Test | If it fails |
|---|---|---|
| 1 | The child's process status is `0`. | `STATUS_REJECT_NONZERO_EXIT` — **stdout is never read.** |
| 2 | The child's stderr is empty, or the block is named in `STDERR_CONTRACT` with a written reason. | `STATUS_REJECT_UNADJUDICATED_STDERR` — **stdout is never read**; the first three stderr lines are printed so the diagnostic is visible rather than swallowed. |
| 3 | Every published line appears in the real stdout (subset check). | `MISMATCH`, with the first five missing lines printed. |

The order is the repair, not the counters. A block failing (1) or (2) reaches `continue` before
the comparison exists, so there is no path through the wrapper on which an incomplete run's
output is interpreted. The wrapper exits `0` only if no block was rejected for any of the three
reasons, and it prints `RC=` and `STDERR_BYTES=` for **every** block whether or not that block
passed, so the real status of all eleven children is on the page.

`STDERR_CONTRACT` is **empty**, and an empty contract is the strongest form of it: no block
published in this document may write anything to stderr. Adding an entry means naming the block
and writing down why its diagnostic is legitimate — and a block with an entry must *still* return
process status `0`, because an adjudicated diagnostic is not an adjudicated failure.

### 13b. D026 — RED under the published round-7 wrapper, GREEN under the round-8 wrapper

Four synthetic documents are written outside the repository, each publishing one harmless child
block and the transcript that child is supposed to produce. Both wrappers are then run over all
four. **Neither wrapper is re-typed:** each is extracted from the `python` fence of the document
that publishes it — round 7 from the frozen `SELF_QA_SEC102_R7.md`, round 8 from this file — and
the SHA-256 of the exact bytes executed is printed, so the instrument under test is the
instrument on the page (Pattern 11).

| Case | The child | Round 7 | Round 8 |
|---|---|---|---|
| `well_behaved_child` | prints the published summary, exits `0` | ACCEPTED | ACCEPTED |
| `fails_after_summary` | prints the published summary, **then `exit 7`** | **ACCEPTED — the finding** | **REJECTED** |
| `stderr_after_summary` | prints the published summary, **then writes one diagnostic to stderr** | **ACCEPTED — the finding** | **REJECTED** |
| `published_line_absent` | prints a different line | REJECTED | REJECTED |

Rows 2 and 3 are the round-7 finding reproduced at the rc level: the published round-7 wrapper
reports the block reproduced and exits `0` over a child that failed. Rows 1 and 4 are controls in
both directions — round 8 is not a blanket reject, and the round-7 subset comparison survives the
repair unchanged.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$base='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1'
$d026=@'
import hashlib, pathlib, re, subprocess, sys, tempfile

BASE = pathlib.Path(sys.argv[1]).resolve()
TICKS = chr(96) * 3
FENCE = re.compile(TICKS + r"([a-z]*)\n(.*?)" + TICKS, re.S)
off = 0

# The instrument under test is the PUBLISHED wrapper, extracted from the document that
# publishes it - never a re-typed copy.  Each document must publish exactly ONE python
# fence; anything else is AMBIGUOUS and fails this block, so the discriminator cannot
# silently run a different program from the one an auditor reads.  The digest pins the
# exact bytes that were executed.
def published_wrapper(name):
    global off
    bodies = [m.group(2) for m in FENCE.finditer((BASE / name).read_text(encoding="utf-8"))
              if m.group(1) == "python"]
    one = len(bodies) == 1
    digest = hashlib.sha256(bodies[0].encode("utf-8")).hexdigest() if one else "AMBIGUOUS"
    print(f"D026_INSTRUMENT={name:22s} PYTHON_FENCES={len(bodies)} SHA256={digest}")
    off += not one
    return bodies[0] if one else None

R7_WRAPPER = published_wrapper("SELF_QA_SEC102_R7.md")
R8_WRAPPER = published_wrapper("SELF_QA_SEC102_R8.md")
if R7_WRAPPER is None or R8_WRAPPER is None:
    print("D026_ABORT=instrument_not_uniquely_published")
    sys.exit(1)

# Four harmless synthetic children.  Nothing here is an attack fixture: they print one
# line, exit non-zero, or write one diagnostic.  The subject is the harness.
SUMMARY = "D026_SUMMARY=child-summary-line"
GOOD = f'$ErrorActionPreference = "Stop"\n"{SUMMARY}"\n'
FAIL = GOOD + "exit 7\n"
NOISE = GOOD + "[Console]::Error.WriteLine('D026_DIAGNOSTIC=unadjudicated')\n"
WRONG = '$ErrorActionPreference = "Stop"\n"D026_SUMMARY=a-different-line"\n'

# (case, child body, published transcript, want r7 verdict, want r8 verdict, want r8 reason)
# Cases 2 and 3 ARE the round-7 finding: the expected summary is emitted and the run then
# fails.  Cases 1 and 4 are controls - not a blanket reject, and the subset check survives.
CASES = [
    ("well_behaved_child",    GOOD,  SUMMARY, "ACCEPTED", "ACCEPTED", "OK"),
    ("fails_after_summary",   FAIL,  SUMMARY, "ACCEPTED", "REJECTED", "STATUS_REJECT_NONZERO_EXIT"),
    ("stderr_after_summary",  NOISE, SUMMARY, "ACCEPTED", "REJECTED", "STATUS_REJECT_UNADJUDICATED_STDERR"),
    ("published_line_absent", WRONG, SUMMARY, "REJECTED", "REJECTED", "MISMATCH"),
]
REASONS = ("STATUS_REJECT_NONZERO_EXIT", "STATUS_REJECT_UNADJUDICATED_STDERR",
           "NO_PUBLISHED_TRANSCRIPT", "MISMATCH")

red_then_green = 0
with tempfile.TemporaryDirectory() as name:
    tmp = pathlib.Path(name)
    tools = {}
    for tag, source in (("r7", R7_WRAPPER), ("r8", R8_WRAPPER)):
        tools[tag] = tmp / (tag + "_wrapper.py")
        tools[tag].write_text(source, encoding="utf-8")
    for case, body, want_line, want7, want8, want_reason in CASES:
        doc = tmp / (case + ".md")
        doc.write_text("# synthetic D026 document, written outside the repository\n\n"
                       + TICKS + "powershell\n" + body + TICKS + "\n\nReal output:\n\n"
                       + TICKS + "text\n" + want_line + "\n" + TICKS + "\n",
                       encoding="utf-8")
        seen = {}
        for tag in ("r7", "r8"):
            done = subprocess.run([sys.executable, "-B", str(tools[tag]), str(doc), str(tmp)],
                                  capture_output=True, text=True, encoding="utf-8",
                                  errors="replace")
            seen[tag] = (done.returncode, done.stdout)
        rc7, out7 = seen["r7"]
        rc8, out8 = seen["r8"]
        v7 = "ACCEPTED" if rc7 == 0 else "REJECTED"
        v8 = "ACCEPTED" if rc8 == 0 else "REJECTED"
        # Word-bounded, so the summary counter MISMATCHED=0 cannot be read as the
        # per-block reason token MISMATCH.  A substring test scored a clean control as
        # a mismatch on the first run of this block.
        reason = next((token for token in REASONS
                       if re.search(r"\b" + token + r"\b", out8)), "OK")
        # UNREAD_STDOUT is the ORDERING measurement: it is 1 only when the round-8 wrapper
        # refused to interpret the child's stdout at all.  A wrapper that merely counted the
        # failure and still compared the output would score 0 here and fail the case.
        unread = int("STDOUT_NOT_INTERPRETED" in out8)
        want_unread = int(want_reason.startswith("STATUS_REJECT"))
        ok = (v7, v8, reason, unread) == (want7, want8, want_reason, want_unread)
        off += not ok
        red_then_green += want7 == "ACCEPTED" and want8 == "REJECTED" and ok
        print(f"D026 CASE={case:21s} R7={v7}/rc{rc7} R8={v8}/rc{rc8} R8_REASON={reason} "
              f"UNREAD_STDOUT={unread} WANT={want7}/{want8}/{want_reason}/{want_unread} "
              f"{'OK' if ok else 'OFF_EXPECTATION'}")

print(f"D026_CASES={len(CASES)} RED_UNDER_R7_GREEN_UNDER_R8={red_then_green} "
      f"D026_OFF_EXPECTATION={off}")
sys.exit(0 if off == 0 else 1)
'@
$d026 | python -B - $base
"D026_HARNESS_BLOCK_RC=$LASTEXITCODE"
```

Real output:

```text
D026_INSTRUMENT=SELF_QA_SEC102_R7.md   PYTHON_FENCES=1 SHA256=4ba21f81088d73cc17f5162377c42a53792f2668401be9323a3732f98b507bca
D026_INSTRUMENT=SELF_QA_SEC102_R8.md   PYTHON_FENCES=1 SHA256=391a8e208f16c2c53c434d5800af0fd0c24b49df4ddba39aef28cc96ed11473c
D026 CASE=well_behaved_child    R7=ACCEPTED/rc0 R8=ACCEPTED/rc0 R8_REASON=OK UNREAD_STDOUT=0 WANT=ACCEPTED/ACCEPTED/OK/0 OK
D026 CASE=fails_after_summary   R7=ACCEPTED/rc0 R8=REJECTED/rc1 R8_REASON=STATUS_REJECT_NONZERO_EXIT UNREAD_STDOUT=1 WANT=ACCEPTED/REJECTED/STATUS_REJECT_NONZERO_EXIT/1 OK
D026 CASE=stderr_after_summary  R7=ACCEPTED/rc0 R8=REJECTED/rc1 R8_REASON=STATUS_REJECT_UNADJUDICATED_STDERR UNREAD_STDOUT=1 WANT=ACCEPTED/REJECTED/STATUS_REJECT_UNADJUDICATED_STDERR/1 OK
D026 CASE=published_line_absent R7=REJECTED/rc1 R8=REJECTED/rc1 R8_REASON=MISMATCH UNREAD_STDOUT=0 WANT=REJECTED/REJECTED/MISMATCH/0 OK
D026_CASES=4 RED_UNDER_R7_GREEN_UNDER_R8=2 D026_OFF_EXPECTATION=0
D026_HARNESS_BLOCK_RC=0
```

Command rc: `0`. `RED_UNDER_R7_GREEN_UNDER_R8=2` is the finding: exactly the two children Codex
described are accepted by the wrapper this document used to publish and rejected by the one it
publishes now, and `UNREAD_STDOUT=1` on both proves the rejection happens *before* the output is
interpreted rather than after.

### 13c. The published round-8 wrapper

Written outside the repository and reproduced here in full so the Lead can re-run it without
trusting this document. The fence marker is built with `chr(96)`, so this source contains no
literal triple backtick and is safe to publish inside the document it parses.

```python
#!/usr/bin/env python3
"""Extract every fenced powershell block from SELF_QA_SEC102_R8.md, run it from a working
directory OUTSIDE the repository, PROVE THE CHILD RUN COMPLETED, and only then compare its
output with the published transcript.

Round 8 repairs the defect `SEC102_CODEX_T1_AUDIT_R7_2026-08-12.md` found in the round-7
wrapper: it read each child's stdout and never its process status or its stderr, so a child
could emit exactly the published subset and THEN fail - or emit an unadjudicated diagnostic -
and still be reported as reproduced.  Three tests now run in a fixed order:

  1. process status must be 0                       -> otherwise STDOUT IS NEVER READ
  2. stderr must be empty, or the block must be      -> otherwise STDOUT IS NEVER READ
     named in STDERR_CONTRACT with a written reason
  3. only then: every published line must appear in the real stdout (subset check)

The ORDER is the repair.  A block failing 1 or 2 reaches `continue` before the comparison
exists, so this file cannot report "reproduced" over an incomplete run.  RC and STDERR_BYTES
are printed for every block whether it passed or not, so the real status of each child is
published rather than merely tested.

A fence in any language other than `text` ends the current block's transcript association, so
this file's own listing inside the document cannot be mistaken for a published transcript.  The
fence marker is built with chr(96) so this source contains no literal triple backtick and is
therefore safe to publish inside the very document it parses.

The comparison is a SUBSET check: every published line must appear in the real output.  A block
whose transcript is a declared excerpt therefore passes on exactly the lines it publishes, and a
block that publishes a line the tool did not emit fails.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys
import tempfile

DOC = pathlib.Path(sys.argv[1])
OUTSIDE = pathlib.Path(sys.argv[2])
text = DOC.read_text(encoding="utf-8")
TICKS = chr(96) * 3
FENCE = re.compile(TICKS + r"([a-z]*)\n(.*?)" + TICKS, re.S)

# The documented non-empty-stderr contract: block index -> the written reason that block's
# stderr is legitimate.  It is EMPTY, which is the strongest form of the contract: no block
# published in this document may write anything to stderr.  An entry must name the block and
# state why - and a block with an entry must STILL return process status 0, because an
# adjudicated diagnostic is not an adjudicated failure.
STDERR_CONTRACT: dict[int, str] = {}

blocks: list[tuple[str, list[str]]] = []
current: list[str] | None = None
for match in FENCE.finditer(text):
    kind, body = match.group(1), match.group(2)
    if kind == "powershell":
        current = []
        blocks.append((body, current))
    elif kind == "text" and current is not None:
        current.append(body)
    elif kind != "text":
        current = None

rejected = status_rejects = stderr_rejects = mismatched = compared = complete = 0
print(f"BLOCKS_FOUND={len(blocks)} STDERR_CONTRACT_ENTRIES={len(STDERR_CONTRACT)}")
for index, (command, published) in enumerate(blocks, 1):
    lines = command.strip().splitlines()
    label = lines[1][:70] if len(lines) > 1 else "?"
    with tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False, encoding="utf-8") as handle:
        handle.write(command)
        script = handle.name
    done = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
         "-File", script],
        cwd=str(OUTSIDE), capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    pathlib.Path(script).unlink()
    err = done.stderr or ""
    head = f"BLOCK={index:02d} RC={done.returncode} STDERR_BYTES={len(err.encode('utf-8'))}"

    # (1) process status, adjudicated BEFORE any output is interpreted.
    if done.returncode != 0:
        rejected += 1
        status_rejects += 1
        print(f"{head} STATUS_REJECT_NONZERO_EXIT STDOUT_NOT_INTERPRETED {label}")
        continue
    # (2) stderr, adjudicated BEFORE any output is interpreted.
    if err and index not in STDERR_CONTRACT:
        rejected += 1
        stderr_rejects += 1
        print(f"{head} STATUS_REJECT_UNADJUDICATED_STDERR STDOUT_NOT_INTERPRETED {label}")
        for line in err.splitlines()[:3]:
            print(f"    STDERR {line.rstrip()}")
        continue
    complete += 1
    note = "STATUS_OK" if not err else f"STATUS_OK_STDERR_ADJUDICATED[{STDERR_CONTRACT[index]}]"

    # (3) execution completeness is proved; only now may the transcript be interpreted.
    if not published:
        rejected += 1
        print(f"{head} {note} NO_PUBLISHED_TRANSCRIPT {label}")
        continue
    actual = [line.rstrip() for line in done.stdout.splitlines()]
    want = [line.rstrip() for chunk in published for line in chunk.splitlines()]
    missing = [line for line in want if line not in actual]
    compared += 1
    mismatched += bool(missing)
    rejected += bool(missing)
    print(f"{head} {note} PUBLISHED_LINES={len(want)} MISSING_FROM_REAL_OUTPUT={len(missing)} "
          f"{'OK' if not missing else 'MISMATCH'} {label}")
    for line in missing[:5]:
        print(f"    MISSING {line}")
print(f"BLOCKS={len(blocks)} STATUS_PROVED_COMPLETE={complete} REJECTED_ON_STATUS={status_rejects} "
      f"REJECTED_ON_STDERR={stderr_rejects} COMPARED={compared} MISMATCHED={mismatched} "
      f"REJECTED={rejected} CWD={OUTSIDE}")
sys.exit(0 if rejected == 0 else 1)
```

### 13d. Real per-block status for all eleven blocks

Write the section-13c fence to `verify_selfqa_r8.py` in a directory outside the repository and
run it as `python -B verify_selfqa_r8.py <path-to-this-file> <that-directory>`. Real output:

```text
BLOCKS_FOUND=11 STDERR_CONTRACT_ENTRIES=0
BLOCK=01 RC=0 STDERR_BYTES=0 STATUS_OK PUBLISHED_LINES=51 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=02 RC=0 STDERR_BYTES=0 STATUS_OK PUBLISHED_LINES=59 MISSING_FROM_REAL_OUTPUT=0 OK $tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_
BLOCK=03 RC=0 STDERR_BYTES=0 STATUS_OK PUBLISHED_LINES=26 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=04 RC=0 STDERR_BYTES=0 STATUS_OK PUBLISHED_LINES=42 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=05 RC=0 STDERR_BYTES=0 STATUS_OK PUBLISHED_LINES=9 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=06 RC=0 STDERR_BYTES=0 STATUS_OK PUBLISHED_LINES=10 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=07 RC=0 STDERR_BYTES=0 STATUS_OK PUBLISHED_LINES=30 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=08 RC=0 STDERR_BYTES=0 STATUS_OK PUBLISHED_LINES=7 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=09 RC=0 STDERR_BYTES=0 STATUS_OK PUBLISHED_LINES=19 MISSING_FROM_REAL_OUTPUT=0 OK $base='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1'
BLOCK=10 RC=0 STDERR_BYTES=0 STATUS_OK PUBLISHED_LINES=21 MISSING_FROM_REAL_OUTPUT=0 OK $base='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1'
BLOCK=11 RC=0 STDERR_BYTES=0 STATUS_OK PUBLISHED_LINES=8 MISSING_FROM_REAL_OUTPUT=0 OK $base='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1'
BLOCKS=11 STATUS_PROVED_COMPLETE=11 REJECTED_ON_STATUS=0 REJECTED_ON_STDERR=0 COMPARED=11 MISMATCHED=0 REJECTED=0 CWD=C:\Users\BARSEM~1\AppData\Local\Temp\claude\C--LAB-Tradingview-LAB-CLEAN\8c951c80-4d84-4125-8475-4f0d0231134a\scratchpad\outside
```

Every one of the eleven children returned process status `0` with **zero** stderr bytes, so no
block relied on the empty `STDERR_CONTRACT` and every stdout comparison was made over a run
already proved complete.

### 13e. The outer wrapper's own status

A wrapper cannot be the sole witness to its own completion. The outer process status and stderr
byte count below were measured by the shell that launched it, not by the wrapper itself:

```text
OUTER_WRAPPER_RC=0
OUTER_WRAPPER_STDERR_BYTES=0
```

The section-13d transcript above was re-derived on the **final** bytes of this file, after the
last prose edit, and is byte-identical to the run published there. What is *not* claimed: that
the eleven children could not have done something this document failed to ask about. Round 8
proves each of them ran to completion before its output was believed — nothing more, and the
round-7 finding is that "nothing more" was previously "nothing at all".
