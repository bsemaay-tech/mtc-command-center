# SELF-QA — SEC102 composite path proof, round 11

Implementer: `claude-opus-5` xhigh (Max). Input commit `a0ebac7b`, whose Codex T1 audit
(`SEC102_CODEX_T1_AUDIT_R10_2026-08-12.md`) returned **REQUEST_CHANGES** on two findings, **CLOSED**
direct same-object modification and replacement under the round-10 pin after independently
reproducing every number in it, and conserved every earlier SEC102 verdict. **The round-11 finding
is in the EVIDENCE HARNESS, not in the module** — for the fourth round running. Round 11 repairs
both findings and changes no code. **No audit or acceptance is claimed here.**

Every command below is literal, was run from `C:\LAB\Tradingview_LAB_CLEAN`, and its real output
follows it. Section 13 re-extracts every block from this file **as bytes**, pins the object it is
about to prove, reads the bytes back **through that pin**, and then hands *those bytes* — the same
buffer, on a pipe — to the interpreter, which is given **no pathname at all**. The document cannot
quietly drift from the tool, the tool cannot quietly drift from the document, and there is no name
left between them for anything to re-point.

**Sections 1-12 are the round-7/8/9/10 record, carried forward.** Every one of their `powershell`
blocks is byte-identical to `SELF_QA_SEC102_R10.md` — including round-8, round-9 and round-10
wording inside the section-9 comments, because a re-typed carried block is not a carried block, and
because not re-typing an instrument is the discipline round 8 introduced and rounds 9, 10 and 11
extend. Every carried block was re-executed for round 11 by section 13, and its real byte identity,
process status and stderr are published there.

## 0. What round 11 changes

### The two round-10 findings — one class, and the fourth instance of it

`SEC102_CODEX_T1_AUDIT_R10_2026-08-12.md`, two MEDIUM findings, Design Defect Pattern 11 with
Patterns 3, 6 and 9 overlays.

1. **The transient rebind.** Round 10 sampled the pathname's object identity before
   `subprocess.run` and again after the child exited, and called the pair a detection of the one
   thing its share modes could not prevent — a re-pointing of the DOS-device/volume mapping. A
   same-session actor can re-point that mapping *after* the first sample, let the child resolve the
   same pathname to different bytes, and restore it *before* the second. Both samples then agree,
   and the alternate child's output reaches the published comparison and is accepted. **A two-sample
   detector detects a persistent rebind. It does not detect a transient one.**
2. **The counted chain.** `for component in [WORK] + list(WORK.parents)` stored seven handles and a
   count. It never recorded a component's object identity, never proved parent/child adjacency, and
   never re-resolved the completed set as one coherent current chain. `PATH_PIN_HELD=7` proves seven
   opens happened; it does not prove that those seven objects are the chain PowerShell later walks.

Both are the same shape as rounds 7, 8 and 9, rotated once more:

| Round | What the harness never established |
|---|---|
| 7 | that the child **completed** — output was interpreted before status was known |
| 8 | that the child was handed **this document's bytes** — text I/O rewrote LF to CRLF |
| 9 | that those bytes were **still there when the interpreter opened them** |
| 10 | that nothing **re-pointed the name between the two samples that were supposed to notice** |

Four rounds, four repairs, four subtler successors. Each repair moved the proof one step closer to
the child without ever removing the thing the class lives in. **Round 11 does not add a third
temporal sample.** It removes the layer: *mutable name resolution*. Every finding since round 9 has
been an exploit of the fact that `powershell.exe -File <pathname>` re-resolves a name — through a
drive letter, a DOS device, a volume mapping, a junction, a directory entry — after the parent has
finished deciding. So round 11 stops handing the interpreter a name.

### The repair — there is no name

```
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass
               -Command "& ([scriptblock]::Create([Console]::In.ReadToEnd()))"
```

The child compiles and runs whatever arrives on standard input. The wrapper writes it the byte
string it read **through the pinned handle** and compared with the fence — the *identical* Python
object, `payload is on_disk`, not a re-read and not a copy of a file. Between the compared bytes
and the executed bytes there is now **no directory entry, no pathname, no drive letter, no DOS
device, no mount point, no junction and no volume**. The child's entire argument vector contains
**not one path separator** (`ARGV_PATH_SEPARATORS=0`, printed per block).

That is what makes this round different in kind from the previous three. Rounds 8, 9 and 10 each
*narrowed* the interval between the proof and the consumption and then *measured* that the
narrowing held. Round 11 has no interval to measure, because the proof and the consumption are the
same object in the same process. **Executed-byte binding is now a property of the construction, not
the output of a detector** — and therefore not something a same-session actor can race, restore, or
sit between. It is the same move that ended RP6's line-granularity regress (exact byte spans
replaced a granularity that could always be sliced finer) and SEC102's own command-word regress
(a closed whitelist replaced a blacklist that could always be extended by one character).

Every round-10 gate is **conserved behind** the new channel rather than replaced. The script is
still written to disk, still pinned before it is verified, still read back through the pin, the
exclusion is still *measured* (`ERROR_SHARING_VIOLATION`, twice per block) rather than asserted, the
pathname is still bound to the pinned object, and both are still re-measured after the child exits.
What changed is their standing: **none of them can now produce a false accept**, because the
pathname they are about is not the channel the bytes travelled. They can only reject conservatively,
and they are kept for exactly that reason.

### The chain is now a construction, not a count

Finding 2 is answered by building the thing that was previously only counted:

1. **The work directory is pinned first.** On NTFS an open handle anywhere in a subtree makes the
   operating system refuse to rename *any* ancestor of it. That refusal is the reason the chain
   above cannot move — so the wrapper **measures it, in both directions**, on a throwaway subtree of
   its own: permitted while nothing is held (`PERMITTED`), refused once a descendant is pinned
   (`DENIED/5`). A second measurement shows the pinned directory also refuses renames of its own
   entries (`DENIED/32`).
2. **The stable identity is derived from the held handle, not from the name we were given.**
   `GetFinalPathNameByHandleW` with `VOLUME_NAME_GUID` returns `\\?\Volume{…}\…` for the object the
   handle *already holds*. A drive letter, a `subst`, a junction or a DOS-device remap cannot change
   it, because it is read out of the object rather than resolved into one.
3. **Every component below the volume root is opened RELATIVE to its already-pinned parent** with
   `NtOpenFile` and `FILE_OPEN_REPARSE_POINT`, so no intermediate name is resolved through a mutable
   mapping and no reparse point is followed. Each link's object identity is recorded, each is proved
   distinct from its parent, and **the descent must terminate at the object the pin holds**.
   Adjacency is then a property of how the handles were obtained. One coherent current chain by
   construction — `CHAIN_LINKS=7 CHAIN_RELATIVE_OPENS=6 CHAIN_TERMINATES_AT_PINNED_DIR=1`, with a
   per-link disposition, instead of `PATH_PIN_HELD=7`.

### It is measured, not asserted — and both findings are reproduced first

Section 13b makes **both** round-10 findings deterministic against the **published round-10
wrapper**, extracted from its own document as bytes, and then shows round 11 unaffected.

* **Finding 1, reproduced.** The work tree is addressed through a free DOS device this block
  defines (no privilege: it is what `subst` does). Two declared substitutions route the child launch
  through a helper that re-points that device *after* round 10's pre-launch sample, holds it
  re-pointed across the child's whole lifetime, and restores it *before* round 10's post-run sample.
  Nothing is raced — the remap and the restore are ordinary statements either side of the child.
  `transient_certified` publishes the marker only the rebound tree can produce: **round 10 ACCEPTS
  it**, and prints `POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1` while doing so. That line is the
  finding in the detector's own words. Round 11 REJECTS it. `transient_honest` is the same defect
  inverted: round 10 can no longer reproduce an honest document once the window is occupied; round
  11 accepts it.
* **`M4` is the mutant that makes the channel load-bearing.** Same transient remap, same round-11
  wrapper, same pin, same measured exclusion, same chain, same post-run samples — **one constant
  flipped back** to round 10's `-File <pathname>`. The divergence returns and the block is accepted.
  If the nameless channel were decoration, `M4` would behave like round 11. It behaves like round 10.
* **Finding 2, reproduced.** One ordinary junction (`mklink /J`, no privilege) is re-pointed at the
  exact moment round 10's leaf-to-root loop has taken the leaf and has not yet reached the ancestor.
  Round 10's construction reports a complete pin set whose links come from **two different chains**,
  and the live leaf of the new chain is unpinned. Round 11's construction is anchored on the pinned
  object's volume-GUID identity, so the junction is not on its chain at all and the swap changes
  nothing. Both constructions are asserted to appear **verbatim** in the published wrapper bytes, so
  this arm measures the published constructions and not a paraphrase.
* **The channel contract is proved, not assumed.** The kickoff permits a nameless channel only if
  every published block's rc, stderr and stdout contract is conserved under it. Every block of this
  document is run **both ways** and all three must agree exactly.
* **Round 10's own arms are carried.** The rewriter at the launch boundary is still refused on both
  vectors (`INPLACE_WRITE=DENIED WINERROR=32`, `ENTRY_REPLACE=DENIED`); six carried children conserve
  every round-9 and round-10 verdict; `M1`, `M2` and `M3` still fire the byte gate, the measured
  exclusion and the post-run gate; and the pin's precondition still refuses to take a pin on an
  object another process already holds writable.

### What round 11 does NOT change

`composite_pathproof.py` is **untouched** — same bytes, same SHA-256 as rounds 7, 8, 9 and 10
(section 10), and section 9 asserts it has no worktree modification. No fixture was added, so
`.gitattributes` is unchanged. Every classification, reason token, rc and transcript in sections
2-12 is the round-7 record re-run, not a new claim. The interpreter-vocabulary production-gate
limitation stays disclosed exactly as the owner ratified it. And the interpreter **image** is still
located by name from `PATH`, exactly as in rounds 7-10: section 11, round-11 statement 2 states that
as an out-of-model disclosure rather than dressing it as a control, and the report says plainly what
it means for the Lead's stop rule.

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
| **Round 11: the interpreter is handed the compared buffer itself, on a pipe, with no pathname — so executed-byte binding is a property of the construction** | 0, 13a |
| **Round 11: both round-10 findings reproduced against the published round-10 wrapper and then closed — a transient DOS-device remap, a junction swap mid-acquisition, the channel contract, 6 carried children, 4 mutants, the pin precondition** | 13b |
| **Round 11: real byte identity, coherent component chain, nameless channel, process status and stderr for all eleven blocks, plus the outer wrapper** | 13c, 13d, 13e |
| The defect existed at `90868b86` and does not now, at the scanner boundary | 2 |
| Nothing carried regressed — 58 cases | 3 |
| Each new RED was `PASS` on the audited code and is `STOP` now | 4 |
| Restoring the blacklist returns the new REDs to `PASS` — 7 mutations x 16 REDs | 5 |
| The policy's shape — 77 declared forms + 7 word-boundary forms | 6 |
| **The fixpoint property over EVERY printable character, not a chosen list** | 7 |
| Round-5 prefix battery and the five round-3/round-4 discriminators | 8 |
| Hygiene, determinism, carried byte identity | 9 |
| Artifact identity | 10 |
| What rounds 7, 8, 9, 10 and 11 do NOT close | 11 |
| Thirteen-pattern self-adjudication | 12 |
| Paste-and-run verification of this document | 13 |

### What changed in the code in round 7 — and nothing in rounds 8, 9, 10 or 11

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

Command rc: `0`. **`CARRIED_CLEAN=composite_pathproof.py WORKTREE_CHANGES=0` is the central claim
of rounds 8, 9, 10 and 11, measured:** the module this document adjudicates has no worktree modification, so every
classification transcript above is the round-7 code re-executed rather than a new build.
`.gitattributes` is clean for the same reason — round 11 adds no fixture, so there is nothing to
pin. Round 11 ran under **Python 3.14.2**; nothing here establishes behaviour under any other
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

The three evidence documents (`SELF_QA_SEC102_R11.md`, `STATUS_SEC102.md` and
`SEC102_R11_REPORT_2026-08-12.md`) are re-derived by appending them to the `NAMES` list in the
command above. Their SHA-256 values are deliberately **not** transcribed here: a document cannot
contain its own digest, and a partially self-referential table is exactly what Pattern 10 warns
about. The Lead derives all three at commit time.

**Every byte above is the round-7 table, unchanged.** `composite_pathproof.py` is still
`129658` B / `adbf27fd…c05a` and `.gitattributes` is still `1630` B / `40e356f8…5077`, because
rounds 8, 9, 10 and 11 changed no code and added no fixture. Section 9 measures the same fact from the
other direction, as a worktree-clean assertion.

`pathscope_prover.py` was not touched and its pin (`122446` B /
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`) is unchanged; the FREEZE
GREEN transcripts in section 3 are the running proof of it.

## 11. Honest residual scope — what rounds 7, 8, 9, 10 and 11 do NOT close

The full carried list is `STATUS_SEC102.md` items 1-52, of which 50-52 are the round-11 additions,
45-49 are round 10's (45, 46 and 48 retired by this round's construction, and said so there rather
than quietly dropped), and 41-44 are round 9's, carried. Item 43 now names the class round 11
closed — mutable name resolution in the execution channel — which is the naming Codex r9 asked for
and r10 found still incomplete.

### Round-11 statements — the executed channel

1. **The binding is a property of the construction; the remaining statements are about everything
   else.** The bytes the interpreter parses are the bytes the wrapper read through the pinned handle
   and compared with the fence: the same object in the same process, delivered on an anonymous pipe.
   There is no pathname in the child's argument vector (`ARGV_PATH_SEPARATORS=0`), so there is no
   name resolution to race and no post-run sample that anything depends on. This is the one claim
   in this document that is *not* the output of a detector, and it is the only reason the round-10
   findings do not have a round-11 successor.
2. **The interpreter IMAGE is still located by name, and round 11 makes no claim about it.**
   `powershell.exe` is resolved from `PATH` by `subprocess.run`, exactly as in rounds 7-10. A
   same-session actor who can change what that name resolves to can arrange for a program other
   than PowerShell to receive the bytes, and such a program could print anything, including a
   published transcript. **This is not prevented and it is not detected, and it is deliberately not
   dressed up as either.** It is out of the model every round of this document has worked in — the
   model is *"were the compared bytes the bytes that were executed"*, and image identity is
   *"which program executed them"* — but it is the same accepted-divergence *shape*, so the report
   states it plainly for the Lead's stop rule instead of leaving it to be discovered. Round-10
   residual 2 said the same thing in one sentence; round 11 says it in the same breath as the claim
   because round 11 is the round where it is the largest remaining thing.
3. **The nameless channel changes one contract, and the change is measured rather than hidden.**
   `$PSCommandPath` does not exist when there is no script file. No published block uses it; the two
   line-ending sentinels of section 13b did, and they now carry their own text in a here-string
   instead, which measures the same property — *the transport did not translate a newline* — in both
   channels and in both directions (`script_cr_bytes=0` for LF bytes, `=2` for CRLF). Every other
   contract is *proved* conserved rather than argued: `D026_CHANNEL_CONTRACT` runs each published
   block through both channels and requires identical rc, identical stderr length and byte-identical
   stdout. The block that contains the contract arm is excluded from it, because running it inside
   itself does not terminate; its own conservation is measured by the section-13c run, which
   executes it through the nameless channel like every other block.
4. **The conserved round-10 gates are now one-directional, and that is a weakening of their role,
   not of the result.** The pin, the measured exclusion, the name-to-object binding and the two
   post-run re-measurements are all still there and still terminal, but under round 11 they can only
   *reject*. `M3` shows this explicitly: the rewrite succeeds, the child still executes the compared
   buffer, and gate 4 refuses the block anyway. A conservative refusal is the correct failure
   direction, and it is published as that rather than as a control that closes anything.
5. **The component chain is proved coherent; it is also no longer load-bearing.** Round 11 builds it
   properly because round 10 claimed it without building it, not because the execution depends on
   it. Nothing the child does resolves a component, so a chain defect under round 11 is a refusal to
   launch, never an admission.
6. **The NTFS ancestor-freeze the chain rests on is measured on this wrapper's own subtree, and
   generalised by the rule rather than by a sweep.** `ANCESTOR_RENAME_NOTHING_HELD=PERMITTED/0` and
   `ANCESTOR_RENAME_DESCENDANT_PINNED=DENIED/5` are measurements of Windows on objects this run
   created. That the same I/O-manager rule governs `C:\Users` is an inference from the rule, not a
   measurement of those directories, and it is stated as an inference.
7. **`HOLD`, `TRANSIENT`, `M1`-`M4` are mutations of the published harness, not independent
   implementations.** They show that the transient window existed, that the round-10 construction
   false-accepts through it, that flipping one constant brings the false acceptance back, that the
   counted chain admits a mixed set, and that every conserved gate still fires — but a mutation
   cannot show that no other window exists anywhere in the wrapper. (These are *harness* mutants;
   the module mutants `M1`-`M7` of section 5 are a separate, unchanged set.)
8. **The two D026 environment primitives are ordinary, harmless and reverted.** A free drive letter
   is defined with `DefineDosDevice` (what `subst` does, no privilege) and released at the end of the
   block, with the release measured; one junction is created with `mklink /J` inside the block's own
   temporary tree and removed. No attack fixture was authored, no sensitive body exists, and nothing
   outside the temporary tree is written.
9. **Round 11 measures no new property of `composite_pathproof.py`.** Every classification claim in
   this document is the round-7 claim re-executed. Round 11 guarantees only that the block being
   re-executed is the block on this page, that the interpreter received exactly those bytes, and that
   a block which fails cannot be reported as reproduced.
10. **Round 9's checkout residual is carried unchanged** (`STATUS_SEC102.md` item 41): byte identity
    is asserted against this document as it exists on disk, not against a pinned checkout. That
    failure remains loud — a CRLF-materialised checkout changes the published counts and digests —
    and it remains the Lead's decision, not this round's.
11. **The run holds read handles on every directory from the volume root down to its temporary
    directory** for the duration of the run, which denies *other* processes a write-open, a rename or
    a delete of those directories, and denies renames of entries inside its own work directory. This
    is round 10's behaviour, carried and now measured. It is an availability side effect on a shared
    machine for the length of one run, and it is named rather than left to be noticed.

### Round-10 statements — the executed object, carried

1. **The pin binds every FILE and DIRECTORY on the path; it does not bind the VOLUME.** Windows
   share modes are enforced on file and directory objects. A rebinding one level below that — a
   per-session DOS-device or mount redefinition — is *not* prevented by any share mode. Round 10
   claimed to **detect** it and Codex r10 showed that claim was false for the transient case.
   **Round 11 neither prevents nor detects it, and no longer needs to:** the child resolves no name,
   so a volume rebinding cannot change what it executes. Section 13b measures exactly this — the
   remap is applied and restored around the child, and round 11's verdict does not move.
2. **The pinned object is the SCRIPT. The interpreter binary is not pinned.** Carried verbatim, and
   promoted to round-11 statement 2 above because under round 11 it is the largest remaining item.
3. **A concurrent writer cannot get past the pin, but it can stop the run.** If another process
   already holds a writable handle on the temporary name, the pin cannot be taken at all and the
   block is refused before the child exists. Integrity is closed; availability is not, and that is a
   different property.
4. **The binding is a Windows property**, measured on this host, on this volume, under
   **Python 3.14.2**. Nothing here establishes equivalent behaviour on another operating system or
   on a temporary directory that is not a local NTFS volume.
5. **The exclusion is measured for the two access classes that can rewrite the object** — a
   write-open and a delete-open — not for every access mask Windows defines.
6. **The rewriter and the transient helper are synthetic and harmless.** They write one benign
   marker line and print what Windows told them.
7. **Round 10's mutation caveat is carried** and restated as round-11 statement 7.
8. **Round 10 measured no new property of `composite_pathproof.py`**, and neither does round 11.

### Round-9 statements — the executed instrument, carried

1. **Byte identity is asserted against this document as it exists on disk, not against a pinned
   checkout.** The repository root sets `* text=auto` and this clone has `core.autocrlf=true`, so a
   *fresh* Windows clone would materialise this file with CRLF line endings. Every block's `LF`
   count, `CRLF` count and SHA-256 are published in section 13d, and section 13b's `D026_WRITEPATH`
   lines read this file's own first fence, so such a checkout makes block 11 report `MISMATCH`
   instead of reproduced. The failure is loud, not silent. Pinning the self-QA documents in
   `.gitattributes` would close it; the round-11 scope fence limits `.gitattributes` to fixture pins,
   so it is named for the Lead to decide, not deferred quietly.
2. **The proof is byte identity, not interpretation identity.** All eleven blocks are pure ASCII
   (`NONASCII=0` on every block in section 13d), so nothing published here turns on how
   `powershell.exe` decodes a UTF-8 file with no BOM — and, under round 11, on how it decodes a UTF-8
   *stream* with no BOM, which is the same disclosed Pattern-4 boundary one channel over.
3. **The sentinel measures the bytes the interpreter was handed, not what the interpreter did with
   them.** Under round 11 it counts CR bytes in text it carries itself. It proves the transport; it
   is deliberately not a claim about how PowerShell parses line endings.
4. **`M1` is a mutation of the published instrument, not an independent implementation.**
5. **Round 9 measured no new property of `composite_pathproof.py`.**
6. **The D026 children are synthetic and harmless.** They print a line, exit non-zero, write one
   diagnostic, or count CR bytes in text they carry. No attack fixture and no sensitive body was
   authored for them.
7. **Round 8's statements below are carried unchanged** — including the subset comparison, the empty
   `STDERR_CONTRACT`, and the fact that the outer wrapper's own status is adjudicated by whoever runs
   it rather than by itself.
8. **One carried round-8 statement was itself untrue when it was written.** Round-8 statement 1 below
   ends *"beyond byte-identity with the fence"* — and round 8's wrapper did not have byte-identity
   with the fence. It is carried verbatim rather than silently corrected, because an evidence
   document that quietly rewrites a claim an audit falsified is worse than one that shows the
   correction.

### Round-8 statements, carried

1. **The harness now proves that each child ran to completion; it does not prove the child ran the
   right thing.** Status 0 with empty stderr plus a stdout subset match is a much stronger acceptance
   than round 7's, and it is still an acceptance of *observed output from a process this document
   itself wrote*. Nothing here establishes that the extracted block is the block the Lead would have
   typed, beyond byte-identity with the fence.
2. **The comparison is still a SUBSET check.** A block may emit more than it publishes, and a
   declared excerpt (section 6) passes on the lines it publishes.
3. **The empty `STDERR_CONTRACT` is a property of this document, not a general rule.** An entry never
   waives test (1): an adjudicated diagnostic is not an adjudicated failure.
4. **The outer wrapper's own status is adjudicated by whoever runs it, not by itself.** Section 13e
   publishes the outer process status and stderr byte count as measured by the shell that launched
   it. A wrapper cannot be the sole witness to its own completion, and this one does not claim to be.
5. **Round 8 measured no new property of `composite_pathproof.py`.**
6. **The four D026 children are synthetic and harmless.**

### Round-7 statements, carried

The round-7-specific statements:

1. **The recognised-interpreter VOCABULARY is still a list, and this is the production-gate
   blocker.** Round 7 changed *how a command word is admitted*; it did not change *which names are
   recognised*. A proven-static literal made only of safe characters that names an executable-capable
   program absent from `GRAPH_INTERPRETER_WORDS` is still a benign leaf. The round-6 audit accepted
   this as a scoped limitation; nothing since has weakened or narrowed that acceptance.
2. **The safe set is a claim about Bash, and it is exactly as strong as one reading of the Bash
   grammar.** The inversion means an unknown character is refused rather than admitted, so an error
   in that reading now produces a false STOP instead of a false PASS. That is a strictly better
   failure direction, not a proof of correctness.
3. **The conservative false stops are larger than round 6's, and they are refusals, not
   detections.** New in round 7: any command word containing `+`, `@`, `%`, `=`, `,`, `^`, `#`, a
   quote character, or any non-ASCII character now STOPs — so `g++`, `tool@1.0`, `--opt=value`,
   `"bash"` and `café` all STOP although Bash would run them harmlessly. Carried from round 6:
   `[ -f x ]`, `\cat`, `~/bin/mytool`, `SEEN[0] "$ROOT/in.txt"`.
4. **A non-NAME function definition is a new false stop.** `bin/foo() { ...; }` STOPs because the
   scanner cannot tell it from an `extglob` pattern without deciding which shell options are set.
5. **The word-boundary conservation covers `(` only.** A `)` abutting a word is still treated as a
   separator, because subshell and `case` syntax depend on that and no `extglob` construct begins at
   a `)`. This is an argument from the Bash grammar, not a sweep.
6. **Quoted occurrences are still not excused,** for the round-6 reason: deciding that quoting
   suppressed a specific expansion is the class of reasoning that produced R5-F1.
7. **Nothing outside the command word moved.** Operand grammar, prefix grammar, the analysis unit,
   FREEZE, the prover adapter and every host/network non-claim are unchanged from round 6.
8. **`M3` shows the word-boundary conservation kills nothing on its own.** It is published as a
   correctness fix to what the classifier is shown, not as an independent guard.

## 12. Thirteen-pattern self-adjudication

| Pattern | Round-11 self-assessment |
|---|---|
| 1 — STOP/PASS/FAIL ordering | Unchanged; 58-case matrix asserts every rc. |
| 2 — Host and namespace identity | Unchanged non-claim; no host contacted. |
| 3 — Host-object, symlink, mount identity | **THE ROUND-10 FINDING 2.** Unchanged explicit non-claim *in the module*. In the harness, round 10 counted seven directory handles and called it a chain; round 11 builds one coherent current chain by construction — pin the leaf first, derive the volume-GUID identity from the held handle, open every component relative to its pinned parent with `FILE_OPEN_REPARSE_POINT`, record an identity per link, and require the descent to terminate at the pinned object. Section 13b re-points a junction mid-acquisition and shows round 10's set spanning two chains while round 11's anchor does not move. Mount-level rebinding is no longer a residual of the execution path at all, because the execution path resolves nothing. |
| 4 — External interpreter/environment boundary | Unchanged disclosed production blocker (round-7 residual 1). Round 11 proves the interpreter is handed this page's bytes by construction; it claims nothing about how the interpreter decodes them, and nothing about the identity of the interpreter binary (round-11 statement 2, stated as an out-of-model disclosure). |
| 5 — Grammar incompleteness | The round-6 finding, closed in round 7 by inverting the test so incompleteness produces a STOP rather than an admission; swept over every printable character in section 7. Codex r7 judged the whitelist a fixpoint for the class. Unchanged by rounds 8-11. |
| 6 — Probe status before adjudication | The round-7 finding, closed in round 8 and confirmed closed by Codex r8. Rounds 9, 10 and 11 conserve that ordering verbatim; section 13b measures the conservation with six carried children under both published wrappers. |
| 7 — Incomplete-reader path | Unchanged in the module. In the harness a run is refused before its output is believed if the chain is not coherent, the object is not pinned, the bytes differ, the exclusion is not measured, the channel is not nameless, the child did not complete, or the object changed underneath it. |
| 8 — Deployed identity | Unchanged lexical scope. |
| 9 — Claim wording vs predicate | **THE ROUND-10 FINDING 1.** Round 10's "detected, terminal, stdout never interpreted" was a two-sample claim written as a class claim. Round 11 does not re-word it and does not add a third sample: it removes the resolution the claim was about, so the sentence in section 13a is now the predicate the mechanism supports without qualification — and the one thing that remains (the interpreter image's own name) is stated as an out-of-model non-claim in the same breath, not after an audit. |
| 10 — Declared vs executed evidence | The round-8 finding, closed in round 9 and confirmed closed by Codex r9. Conserved: extraction and writing are still byte-mode, section 13b still reproduces the round-8 write path on this document's own first fence, `M1` still fires, and every instrument and mutant is still extracted **as bytes** with its SHA-256 printed. Section 13d's transcript prints no per-run temporary name or raw file index, so it re-derives byte-for-byte. |
| 11 — Instrument defects | **BOTH ROUND-10 FINDINGS, and the round-11 repair.** The verified object was still reached by the production caller through a mutable name. Round 11 removes the name: the compared buffer *is* the executed buffer, in one process, on a pipe. `M4` flips that one constant back and the false acceptance returns, which is what makes the channel the repair rather than a description of one. |
| 12 — Unmodeled behavior disappearing | The classifier's default is refusal; `SWEEP_LEAK_ADMITTED=0` and `SILENT_LEAK=0` are the measurements. The harness's default is refusal too. No new gate is an unexercised branch: `M1` fires the byte gate, `M2` the measured exclusion before the child exists, `M3` the post-run gate with a real rewrite behind it, `M4` the channel, and the chain arm exercises both acquisition constructions against a real junction swap. |
| 13 — Terminal-disposition conservation | Unchanged; every RED reaches a terminal STOP with a reason token, verified in sections 3-5. The harness's own rejections are terminal too — `CHAIN_NOT_COHERENT`, `SCRIPT_NOT_PINNED`, `SCRIPT_BYTES_MISMATCH`, `SCRIPT_NOT_BOUND_TO_PINNED_OBJECT`, `EXEC_NOT_NAMELESS`, `SCRIPT_REBOUND_UNDER_PIN`, `SCRIPT_BYTES_CHANGED_UNDER_PIN`, `STATUS_REJECT_NONZERO_EXIT`, `STATUS_REJECT_UNADJUDICATED_STDERR`, `NO_PUBLISHED_TRANSCRIPT` and `MISMATCH` each carry a named reason token and force a non-zero wrapper exit. Every chain link carries its own disposition, which is what finding 2 asked for. |

## 13. Paste-and-run verification of this document

Every fenced `powershell` block above is extracted byte-for-byte from this file, written to a
`.ps1` inside a directory tree this process pins open, proved byte-identical to its fence **through
the pin**, and then executed **from those bytes** — handed to the interpreter on a pipe, with no
pathname anywhere in the child's argument vector, from a working directory outside the repository.
**Round 11 makes the last clause of that sentence true.** Rounds 9 and 10 handed the interpreter a
name and then worked to make the name trustworthy; round 11 stops handing it one.

### 13a. What the round-11 wrapper adjudicates, in order

| # | Test | If it fails |
|---|---|---|
| 0a | The work directory is pinned; its stable volume-GUID path is derived **from that handle**; the volume root is opened and every component below it is opened **relative to its already-pinned parent**, each with a recorded object identity; the descent terminates at the pinned object; and the NTFS ancestor freeze the chain rests on is measured in both directions. | `CHAIN_NOT_COHERENT` — **no child is launched at all**, for any block. |
| 0b | The object is pinned (`FILE_SHARE_READ` only) **before** it is verified, the bytes read back **through that handle** equal the fence's bytes, and Windows refuses both a write-open and a delete-open of the name with `ERROR_SHARING_VIOLATION`. | `SCRIPT_NOT_PINNED` / `SCRIPT_BYTES_MISMATCH` — **the child is never launched.** |
| 0c | The script is reached **relative to the pinned directory handle** and is the same object, and the pathname resolves to the pinned object too. | `SCRIPT_NOT_BOUND_TO_PINNED_OBJECT` — **the child is never launched.** |
| 0d | The buffer handed to the interpreter **is** the buffer that was compared — object identity inside this process — and the child's argument vector contains **no path separator**. | `EXEC_NOT_NAMELESS` — **the child is never launched.** |
| 1 | The child's process status is `0`. | `STATUS_REJECT_NONZERO_EXIT` — **stdout is never read.** |
| 2 | The child's stderr is empty, or the block is named in `STDERR_CONTRACT` with a written reason. | `STATUS_REJECT_UNADJUDICATED_STDERR` — **stdout is never read**; the first three stderr lines are printed so the diagnostic is visible rather than swallowed. |
| 4 | After the child exits — with the pin still held — the pathname still resolves to the pinned object and the pinned object's bytes are still the fence's bytes. Conserved from round 10; under round 11 this can only reject. | `SCRIPT_REBOUND_UNDER_PIN` / `SCRIPT_BYTES_CHANGED_UNDER_PIN` — **stdout is never read.** |
| 3 | Every published line appears in the real stdout (subset check). | `MISMATCH`, with the first five missing lines printed. |

Tests 1-3 are round 8's and round 9's, conserved verbatim; 0b, 0c and 4 are round 10's, conserved;
0a is round 10's component pin, rebuilt as a construction; 0d is round 11's. The numbering keeps
round 9's names so the carried gates keep theirs; the table is in execution order.

**What that order supports, stated as the predicate the mechanism actually proves.** The byte string
this wrapper hands each interpreter is the byte string it read through a handle that Windows refused
to let any process open for writing or deletion, and that it compared with the fence on this page —
the identical object in this process's memory, delivered on an anonymous pipe. **There is no
pathname, no directory entry, no drive letter, no DOS device, no mount point and no volume between
the comparison and the execution, so there is no resolution to re-point and no interval to occupy.**
That is not a detection and it does not depend on one: every gate above can refuse a block, and
none of them is what makes the executed bytes the compared bytes. What this does **not** cover is
which *program* receives them — `powershell.exe` is still found by name on `PATH`, exactly as in
every previous round, and round-11 statement 2 says so as an out-of-model non-claim rather than as
a control.

A block failing 0a-0d reaches `continue` before `subprocess.run` exists. A block failing 1, 2 or 4
reaches `continue` before the comparison exists. The wrapper exits `0` only if no block was rejected
for any of these reasons, and it prints each block's byte count, `LF`/`CRLF`/non-ASCII composition,
SHA-256, pin state, chain membership, channel state and `RC=`/`STDERR_BYTES=` for **every** block
whether or not that block passed.

`STDERR_CONTRACT` is **empty**, and an empty contract is the strongest form of it: no block published
in this document may write anything to stderr. Adding an entry means naming the block and writing
down why its diagnostic is legitimate — and a block with an entry must *still* return process status
`0`, because an adjudicated diagnostic is not an adjudicated failure.

### 13b. D026 — both round-10 findings reproduced against the published round-10 wrapper, then closed

Synthetic documents are written outside the repository, each publishing one harmless child block and
the transcript that child is supposed to produce. **No wrapper is re-typed:** each is extracted from
the `python` fence of the document that publishes it — rounds 8, 9 and 10 from their frozen files,
round 11 from this one — and extracted **as bytes**. The SHA-256 of the exact bytes executed is
printed for every instrument and every mutant.

**Finding 1 is made deterministic, not raced.** The work tree of the wrapper under test is addressed
through a free drive letter this block defines with `DefineDosDevice` — no privilege; it is what
`subst` does — by scoping `TMP`/`TEMP` for that child process only. Two declared substitutions route
the wrapper's child launch through a helper that mirrors the current tree into a shadow root with
every `.ps1` replaced by one harmless marker line, re-points the drive letter at the shadow, runs
the child, and restores the letter before returning. The remap therefore begins **after** the
wrapper's pre-launch sample and ends **before** its post-run sample, as ordinary statements either
side of the child. If the window round 10 was accused of leaving does not exist, the helper can
achieve nothing.

| Case | The child | Round 10 + TRANSIENT | Round 11 + TRANSIENT |
|---|---|---|---|
| `transient_certified` | prints `compared-bytes-executed`; the document publishes the `rebound-bytes-executed` transcript only the shadow tree can produce | **ACCEPTED — the finding** | **REJECTED** |
| `transient_honest` | the same child; the document publishes the transcript its own bytes really produce | **REJECTED — the finding, inverted** | **ACCEPTED** |

`R10_TWO_SAMPLE_DETECTOR=CLEAN/1` alongside `transient_certified` accepted is the finding in one
line: in the same run round 10 printed `POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1` — its detector
reporting that nothing had been rebound — while certifying a transcript its compared bytes cannot
produce, because it did not run them. `M4` then flips **one constant** of the round-11 wrapper back
to `-File <pathname>` under the same remap and the acceptance returns, which is what makes the
channel the repair rather than a description of one.

**Finding 2 is made deterministic too.** One ordinary junction is created with `mklink /J` and
re-pointed at the exact moment round 10's leaf-to-root loop has taken the leaf and has not yet
reached the ancestor — a swap the operating system permits, because the junction itself has no open
handle. Round 10's construction then holds a complete-looking set whose links come from two
different chains, with the live leaf of the new chain unpinned. Round 11's construction reads the
stable identity out of the pinned handle, so the junction is not on its chain at all. Both
constructions are asserted to appear **verbatim** in the published wrapper bytes.

**The channel contract is proved.** Every published block of this document is run through both
channels and must return the same rc, the same stderr length and byte-identical stdout. The block
containing that arm is excluded from it — running it inside itself does not terminate — and its own
conservation is measured by the section-13c run.

Round 10's own arms are carried behind the new channel: the rewriter at the launch boundary is still
refused on both vectors; six carried children conserve every round-9 and round-10 verdict; `M2` is
caught before the child exists because the exclusion is measured rather than trusted; `M3` reaches
the post-run gate and is refused there even though, under round 11, the rewrite it achieved could
not have changed what ran; `M1` restores the round-8 translating write path and the pre-launch byte
gate fires; and `D026_PIN_PRECONDITION` shows a pin that cannot be taken is a child that is not
launched.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$base='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1'
$d026=@'
import ctypes, hashlib, os, pathlib, re, shutil, subprocess, sys, tempfile

BASE = pathlib.Path(sys.argv[1]).resolve()
TICKS = (chr(96) * 3).encode()
FENCE = re.compile(TICKS + rb"([a-z]*)\r?\n(.*?)" + TICKS, re.S)
LF = chr(10).encode()
CRLF = (chr(13) + chr(10)).encode()
off = 0

# The instrument under test is the PUBLISHED wrapper, extracted from the document that publishes
# it - never a re-typed copy - and extracted AS BYTES, because byte identity is the subject and
# reading the instrument through translating I/O would be the round-8 defect one level up.  Each
# document must publish exactly ONE python fence; anything else is AMBIGUOUS and fails this block.
def published_wrapper(name):
    global off
    bodies = [m.group(2) for m in FENCE.finditer((BASE / name).read_bytes())
              if m.group(1) == b"python"]
    one = len(bodies) == 1
    digest = hashlib.sha256(bodies[0]).hexdigest() if one else "AMBIGUOUS"
    print(f"D026_INSTRUMENT={name:23s} PYTHON_FENCES={len(bodies)} SHA256={digest}")
    off += not one
    return bodies[0] if one else None


R8_WRAPPER = published_wrapper("SELF_QA_SEC102_R8.md")
R9_WRAPPER = published_wrapper("SELF_QA_SEC102_R9.md")
R10_WRAPPER = published_wrapper("SELF_QA_SEC102_R10.md")
R11_WRAPPER = published_wrapper("SELF_QA_SEC102_R11.md")
if None in (R8_WRAPPER, R9_WRAPPER, R10_WRAPPER, R11_WRAPPER):
    print("D026_ABORT=instrument_not_uniquely_published")
    sys.exit(1)

# HOLD is round 10's substitution, CARRIED verbatim: one textual change, applied to the PUBLISHED
# bytes of both wrappers under test, inserting a genuinely separate same-principal process at the
# exact launch boundary.  It changes no gate and no comparison; it only occupies the window.
ANCHOR = b"    done = subprocess.run("
INJECT = (b'    subprocess.run([sys.executable, "-B", os.environ["D026_REBINDER"], str(script)])\n'
          b"    done = subprocess.run(")
R10_HOLD = R10_WRAPPER.replace(ANCHOR, INJECT)
R11_HOLD = R11_WRAPPER.replace(ANCHOR, INJECT)

# TRANSIENT is the round-10 FINDING 1 made deterministic.  THREE substitutions, all declared and
# counted, applied identically to both published wrappers: the first loads a helper, the second
# routes the child launch through it, the third removes `.resolve()` from the temporary-directory
# path.  The helper re-points the DOS device the work tree is addressed through AFTER the
# wrapper's pre-launch sample, holds it re-pointed across the child's whole lifetime, and restores
# it BEFORE the wrapper's post-run sample.  Nothing is raced: the remap and the restore are
# ordinary statements either side of the child.
#
# Why the third substitution is honest and necessary.  Under a real run the pathname the child is
# given is rooted at `C:`, which IS a per-session DOS device that a same-session actor can
# redefine with no privilege - that is the whole of finding 1.  Re-pointing `C:` on a live working
# machine, even for one child's lifetime, is not a safe thing to do, so the arm re-points a FREE
# letter instead and scopes TMP/TEMP to it for the wrapper under test.  `.resolve()` would
# canonicalise that stand-in letter straight back to `C:` and the stand-in would stop standing in
# for anything; it would NOT have protected the real `C:`-rooted pathname, because it is what
# PRODUCES that pathname rather than something that makes it immune.  Removing it makes the
# stand-in behave the way the real path behaves toward the mutable device layer, and it changes no
# gate, no comparison and no output.
IMPORT = b"import tempfile\n"
LOADER = b'import tempfile\nexec(open(os.environ["D026_TRANSIENT"]).read())\n'
CALL = b"    done = subprocess.run("
ROUTED = b"    done = __d026_transient("
RESOLVED = b')).resolve()'
PLAIN = b'))'
R10_TRANSIENT = R10_WRAPPER.replace(IMPORT, LOADER).replace(CALL, ROUTED).replace(RESOLVED, PLAIN)
R11_TRANSIENT = R11_WRAPPER.replace(IMPORT, LOADER).replace(CALL, ROUTED).replace(RESOLVED, PLAIN)
for tag, source, mutant, want in (("R10_HOLD", R10_WRAPPER, R10_HOLD, "1"),
                                  ("R11_HOLD", R11_WRAPPER, R11_HOLD, "1"),
                                  ("R10_TRANSIENT", R10_WRAPPER, R10_TRANSIENT, "1+1+1"),
                                  ("R11_TRANSIENT", R11_WRAPPER, R11_TRANSIENT, "1+1+2")):
    got = (f"{source.count(ANCHOR)}" if want == "1" else
           f"{source.count(IMPORT)}+{source.count(ANCHOR)}+{source.count(RESOLVED)}")
    print(f"D026_MUTANT={tag:18s} SUBSTITUTIONS={got} "
          f"SHA256={hashlib.sha256(mutant).hexdigest()}")
    off += got != want

# M4 is the round-11 CHANNEL mutant and the load-bearing one: on top of the same transient remap
# it flips ONE constant - the execution channel - back to round 10's `-File <pathname>`.  Nothing
# else changes: same pin, same measured exclusion, same chain, same post-run samples.  If the
# nameless channel were decoration, M4 would behave like round 11.  It behaves like round 10.
CHANNEL = b'EXEC_CHANNEL = "NAMELESS_STDIN"'
NAMED = b'EXEC_CHANNEL = "R10_NAMED_FILE"'
M4 = R11_TRANSIENT.replace(CHANNEL, NAMED)
print(f"D026_MUTANT={'M4_named_channel':18s} SUBSTITUTIONS={R11_TRANSIENT.count(CHANNEL)} "
      f"SHA256={hashlib.sha256(M4).hexdigest()}")
off += R11_TRANSIENT.count(CHANNEL) != 1

# M2, M3 and M1 are round 10's harness mutants, carried onto round 11's instrument so that every
# gate round 10 exercised is still shown firing behind the new channel rather than published as a
# branch nothing ever takes.
PIN = b"PIN_SHARE = FILE_SHARE_READ"
UNPINNED = b"PIN_SHARE = FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE"
M2 = R11_HOLD.replace(PIN, UNPINNED)
print(f"D026_MUTANT={'M2_pin_share_open':18s} SUBSTITUTIONS={R11_HOLD.count(PIN)} "
      f"SHA256={hashlib.sha256(M2).hexdigest()}")
off += R11_HOLD.count(PIN) != 1

GATE = b"    if not (excluded and name_bound and leaf_in_chain):"
GATE_OFF = b"    if not (name_bound and leaf_in_chain):"
M3 = M2.replace(GATE, GATE_OFF)
print(f"D026_MUTANT={'M3_post_run_reach':18s} SUBSTITUTIONS={R11_HOLD.count(PIN)}+"
      f"{M2.count(GATE)} SHA256={hashlib.sha256(M3).hexdigest()}")
off += M2.count(GATE) != 1

REPAIR = b"    path.write_bytes(command)"
ROUND8 = b'    path.write_text(command.decode("utf-8"), encoding="utf-8")'
M1 = R11_WRAPPER.replace(REPAIR, ROUND8)
print(f"D026_MUTANT={'M1_round8_write':18s} SUBSTITUTIONS={R11_WRAPPER.count(REPAIR)} "
      f"SHA256={hashlib.sha256(M1).hexdigest()}")
off += R11_WRAPPER.count(REPAIR) != 1

# The rewriter, carried verbatim from round 10.  A separate process, same principal, no
# privilege, no attack fixture: it opens the temporary script by name and tries to put different
# HARMLESS bytes there - first in place, then by replacing the directory entry.
REBINDER = b'''import ctypes, os, pathlib, sys
from ctypes import wintypes
K32 = ctypes.WinDLL("kernel32", use_last_error=True)
K32.CreateFileW.restype = wintypes.HANDLE
K32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
                            wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
K32.WriteFile.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
                          ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID]
INVALID = wintypes.HANDLE(-1).value
TARGET = pathlib.Path(sys.argv[1])
REBOUND = (chr(36) + 'ErrorActionPreference = "Stop"\\n"D026_SUMMARY=rebound-bytes-executed"\\n').encode()
ctypes.set_last_error(0)
h = K32.CreateFileW(str(TARGET), 0x40000000, 0x00000001 | 0x00000002 | 0x00000004, None, 3,
                    0x00000080, None)
inplace = "SUCCEEDED"
inplace_err = 0
if h == INVALID:
    inplace_err = ctypes.get_last_error()
    inplace = "DENIED"
else:
    written = wintypes.DWORD(0)
    K32.WriteFile(h, REBOUND, len(REBOUND), ctypes.byref(written), None)
    K32.SetEndOfFile(h)
    K32.CloseHandle(h)
replace = "NOT_ATTEMPTED"
replace_err = 0
if inplace == "DENIED":
    spare = TARGET.parent / (TARGET.name + ".rebind")
    spare.write_bytes(REBOUND)
    try:
        os.replace(spare, TARGET)
        replace = "SUCCEEDED"
    except OSError as exc:
        replace = "DENIED"
        replace_err = exc.winerror or 0
        spare.unlink(missing_ok=True)
effected = int(inplace == "SUCCEEDED" or replace == "SUCCEEDED")
print(f"D026_REBINDER INPLACE_WRITE={inplace} WINERROR={inplace_err} "
      f"ENTRY_REPLACE={replace} WINERROR={replace_err} REBIND_EFFECTED={effected}")
sys.exit(0)
'''

# The transient re-binder.  It does not touch a single byte of any file the wrapper pinned - it
# cannot, and round 10 already proved that.  It re-points the MAPPING the work tree is addressed
# through, which no share mode reaches, and it restores it before the wrapper looks again.  The
# rebound tree is a mirror of the real one with every .ps1 replaced by one harmless marker line.
TRANSIENT = b'''import os as _os, pathlib as _pl, subprocess as _sp, ctypes as _ct
from ctypes import wintypes as _wt
_K32 = _ct.WinDLL("kernel32", use_last_error=True)
_K32.DefineDosDeviceW.argtypes = [_wt.DWORD, _wt.LPCWSTR, _wt.LPCWSTR]
_LETTER = _os.environ["D026_LETTER"]
_REAL = _os.environ["D026_REAL_ROOT"]
_SHADOW = _os.environ["D026_SHADOW_ROOT"]
_REBOUND = (chr(36) + 'ErrorActionPreference = "Stop"\\n"D026_SUMMARY=rebound-bytes-executed"\\n').encode()


def _point_at(target):
    return bool(_K32.DefineDosDeviceW(0x1, _LETTER, "\\\\??\\\\" + str(target)))


def __d026_transient(*args, **kwargs):
    root = _pl.Path(_LETTER + "\\\\")
    for source in sorted(root.rglob("*")):
        dest = _pl.Path(_SHADOW) / source.relative_to(root)
        if source.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(_REBOUND)
    applied = _point_at(_SHADOW)
    try:
        done = _sp.run(*args, **kwargs)
    finally:
        restored = _point_at(_REAL)
    print(f"D026_TRANSIENT APPLIED={int(applied)} RESTORED={int(restored)} "
          f"WINDOW=BETWEEN_PRE_SAMPLE_AND_POST_SAMPLE")
    return done
'''

# Round 9's six children, carried.  The two line-ending sentinels carry their own text in a
# here-string instead of reading $PSCommandPath: a nameless channel has no script path, and the
# property the sentinel exists to measure - that the transport did not translate a newline - is
# measured by the here-string in BOTH channels, which the CHANNEL CONTRACT arm below verifies.
SUMMARY = "D026_SUMMARY=child-summary-line"
GOOD = ('$ErrorActionPreference = "Stop"\n"' + SUMMARY + '"\n').encode()
FAIL = GOOD + b"exit 7\n"
NOISE = GOOD + b"[Console]::Error.WriteLine('D026_DIAGNOSTIC=unadjudicated')\n"
WRONG = b'$ErrorActionPreference = "Stop"\n"D026_SUMMARY=a-different-line"\n'
SENTINEL = (b'$ErrorActionPreference = "Stop"\n'
            b"$self = @'\n"
            b"sentinel-line-1\n"
            b"sentinel-line-2\n"
            b"sentinel-line-3\n"
            b"'@\n"
            b"$raw = [System.Text.Encoding]::UTF8.GetBytes($self)\n"
            b'"D026_SUMMARY=script_cr_bytes=" + @($raw -eq 13).Count\n')
INNER = SENTINEL.split(b"@'" + LF)[1].split(LF + b"'@")[0].count(LF)
EXACT = "D026_SUMMARY=script_cr_bytes=0"
REWRITTEN = f"D026_SUMMARY=script_cr_bytes={INNER}"

# (case, child body, published transcript, want r10 verdict, want r11 verdict, want r11 reason)
CARRIED = [
    ("well_behaved_child",        GOOD,     SUMMARY,   "ACCEPTED", "ACCEPTED", "OK"),
    ("fails_after_summary",       FAIL,     SUMMARY,   "REJECTED", "REJECTED", "STATUS_REJECT_NONZERO_EXIT"),
    ("stderr_after_summary",      NOISE,    SUMMARY,   "REJECTED", "REJECTED", "STATUS_REJECT_UNADJUDICATED_STDERR"),
    ("published_line_absent",     WRONG,    SUMMARY,   "REJECTED", "REJECTED", "MISMATCH"),
    ("crlf_transcript_certified", SENTINEL, REWRITTEN, "REJECTED", "REJECTED", "MISMATCH"),
    ("lf_exact_bytes",            SENTINEL, EXACT,     "ACCEPTED", "ACCEPTED", "OK"),
]

# ONE child body, published byte-for-byte in both documents of each pair; only the published
# TRANSCRIPT differs.  The `_certified` document publishes the line only the REBOUND tree can
# produce, so a wrapper that accepts it has certified bytes it never executed.  The `_honest`
# document publishes the line the COMPARED bytes really produce, so a wrapper that rejects it
# cannot reproduce an honest document once the window is occupied.
COMPARED_BODY = b'$ErrorActionPreference = "Stop"\n"D026_SUMMARY=compared-bytes-executed"\n'
REBOUND_LINE = "D026_SUMMARY=rebound-bytes-executed"
COMPARED_LINE = "D026_SUMMARY=compared-bytes-executed"
REBIND = [
    ("rebind_certified", COMPARED_BODY, REBOUND_LINE,  "REJECTED", "REJECTED", "MISMATCH"),
    ("rebind_honest",    COMPARED_BODY, COMPARED_LINE, "ACCEPTED", "ACCEPTED", "OK"),
]
TRANSIENT_CASES = [
    ("transient_certified", COMPARED_BODY, REBOUND_LINE,  "ACCEPTED", "REJECTED", "MISMATCH"),
    ("transient_honest",    COMPARED_BODY, COMPARED_LINE, "REJECTED", "ACCEPTED", "OK"),
]
REASONS = ("SCRIPT_BYTES_MISMATCH", "SCRIPT_NOT_BOUND_TO_PINNED_OBJECT", "EXEC_NOT_NAMELESS",
           "CHAIN_NOT_COHERENT", "SCRIPT_REBOUND_UNDER_PIN", "SCRIPT_BYTES_CHANGED_UNDER_PIN",
           "STATUS_REJECT_NONZERO_EXIT", "STATUS_REJECT_UNADJUDICATED_STDERR",
           "NO_PUBLISHED_TRANSCRIPT", "MISMATCH")


def reason_of(out):
    return next((token for token in REASONS if re.search(r"\b" + token + r"\b", out)), "OK")


def document(path, body, want_line):
    path.write_bytes(b"# synthetic D026 document, written outside the repository\n\n"
                     + TICKS + b"powershell\n" + body + TICKS + b"\n\nReal output:\n\n"
                     + TICKS + b"text\n" + want_line.encode() + b"\n" + TICKS + b"\n")
    return path


# ---------------------------------------------------------------------------------------------
# Win32, for the free drive letter the transient arm re-points and for the pin precondition.
# ---------------------------------------------------------------------------------------------
K32 = ctypes.WinDLL("kernel32", use_last_error=True)
K32.CreateFileW.restype = ctypes.c_void_p
K32.CreateFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p,
                            ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
K32.DefineDosDeviceW.argtypes = [ctypes.c_uint32, ctypes.c_wchar_p, ctypes.c_wchar_p]
K32.QueryDosDeviceW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32]
K32.GetFinalPathNameByHandleW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_uint32,
                                          ctypes.c_uint32]
INVALID = ctypes.c_void_p(-1).value


def dos_target(letter):
    buffer = ctypes.create_unicode_buffer(4096)
    return buffer.value if K32.QueryDosDeviceW(letter, buffer, 4096) else ""


def point_at(letter, target):
    return bool(K32.DefineDosDeviceW(0x1, letter, "\\??\\" + str(target)))


def release(letter):
    for _ in range(16):
        if not dos_target(letter):
            return True
        K32.DefineDosDeviceW(0x2, letter, None)
    return not dos_target(letter)


def free_letter():
    for code in range(ord("Z"), ord("P") - 1, -1):
        letter = chr(code) + ":"
        if not dos_target(letter) and not pathlib.Path(letter + "\\").exists():
            return letter
    return ""


def identity_of(path):
    class BHFI(ctypes.Structure):
        _fields_ = [("a", ctypes.c_uint32), ("b", ctypes.c_uint64), ("c", ctypes.c_uint64),
                    ("d", ctypes.c_uint64), ("vsn", ctypes.c_uint32), ("e", ctypes.c_uint32),
                    ("f", ctypes.c_uint32), ("g", ctypes.c_uint32), ("hi", ctypes.c_uint32),
                    ("lo", ctypes.c_uint32)]
    handle = K32.CreateFileW(str(path), 0x80000000, 0x1 | 0x2 | 0x4, None, 3, 0x02000000, None)
    if handle == INVALID:
        return None
    info = BHFI()
    K32.GetFileInformationByHandle.argtypes = [ctypes.c_void_p, ctypes.POINTER(BHFI)]
    ok = K32.GetFileInformationByHandle(ctypes.c_void_p(handle), ctypes.byref(info))
    K32.CloseHandle(ctypes.c_void_p(handle))
    return (info.vsn, info.hi, info.lo) if ok else None


conserved = false_accept = false_reject = denied = transient_denied = 0
letter = free_letter()
with tempfile.TemporaryDirectory() as name:
    tmp = pathlib.Path(name)
    real_root, shadow_root = tmp / "real", tmp / "shadow"
    real_root.mkdir()
    shadow_root.mkdir()
    rebinder = tmp / "d026_rebinder.py"
    rebinder.write_bytes(REBINDER)
    transient = tmp / "d026_transient.py"
    transient.write_bytes(TRANSIENT)
    env = dict(os.environ, D026_REBINDER=str(rebinder), D026_TRANSIENT=str(transient),
               D026_LETTER=letter, D026_REAL_ROOT=str(real_root),
               D026_SHADOW_ROOT=str(shadow_root))
    tools = {}
    for tag, source in (("r10", R10_WRAPPER), ("r11", R11_WRAPPER), ("r10_hold", R10_HOLD),
                        ("r11_hold", R11_HOLD), ("r10_transient", R10_TRANSIENT),
                        ("r11_transient", R11_TRANSIENT), ("m1", M1), ("m2", M2), ("m3", M3),
                        ("m4", M4)):
        tools[tag] = tmp / (tag + "_wrapper.py")
        tools[tag].write_bytes(source)

    def run(tag, doc, extra=None):
        done = subprocess.run([sys.executable, "-B", str(tools[tag]), str(doc), str(tmp)],
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", env=dict(env, **(extra or {})))
        return done.returncode, done.stdout

    for case, body, want_line, want10, want11, want_reason in CARRIED:
        doc = document(tmp / (case + ".md"), body, want_line)
        rc10, out10 = run("r10", doc)
        rc11, out11 = run("r11", doc)
        v10 = "ACCEPTED" if rc10 == 0 else "REJECTED"
        v11 = "ACCEPTED" if rc11 == 0 else "REJECTED"
        reason = reason_of(out11)
        unread = int("STDOUT_NOT_INTERPRETED" in out11)
        asserted = int("SCRIPT_BYTES_IDENTICAL=1" in out11)
        chained = int("LEAF_ON_PINNED_CHAIN=1" in out11)
        nameless = int("ARGV_PATH_SEPARATORS=0" in out11)
        want_unread = int(want_reason.startswith("STATUS_REJECT"))
        ok = ((v10, v11, reason, unread, asserted, chained, nameless)
              == (want10, want11, want_reason, want_unread, 1, 1, 1))
        off += not ok
        conserved += (want10 == want11) and ok
        print(f"D026 CARRIED={case:25s} R10={v10}/rc{rc10} R11={v11}/rc{rc11} "
              f"R11_REASON={reason} UNREAD_STDOUT={unread} BYTES_ASSERTED={asserted} "
              f"LEAF_ON_CHAIN={chained} NAMELESS={nameless} "
              f"WANT={want10}/{want11}/{want_reason}/{want_unread} "
              f"{'OK' if ok else 'OFF_EXPECTATION'}")

    # Round 10's rebinding arms, CARRIED: the same rewriter at the same launch boundary must
    # still be refused by the operating system on both vectors, behind the new channel.
    for case, body, want_line, want10, want11, want_reason in REBIND:
        doc = document(tmp / (case + ".md"), body, want_line)
        rc10, out10 = run("r10_hold", doc)
        rc11, out11 = run("r11_hold", doc)
        v10 = "ACCEPTED" if rc10 == 0 else "REJECTED"
        v11 = "ACCEPTED" if rc11 == 0 else "REJECTED"
        reason = reason_of(out11)
        effected = int("REBIND_EFFECTED=1" in out11)
        sharing = int("INPLACE_WRITE=DENIED WINERROR=32" in out11
                      and "ENTRY_REPLACE=DENIED" in out11)
        ok = ((v10, v11, reason) == (want10, want11, want_reason)
              and effected == 0 and sharing == 1)
        off += not ok
        denied += effected == 0 and sharing == 1
        print(f"D026 REBIND={case:25s} R10_HOLD={v10}/rc{rc10} R11_HOLD={v11}/rc{rc11} "
              f"R11_REASON={reason} REBOUND_UNDER_R11={effected} "
              f"R11_DENIAL=SHARING_VIOLATION_32/{sharing} WANT={want10}/{want11}/{want_reason} "
              f"{'OK' if ok else 'OFF_EXPECTATION'}")

    # M2, carried: the same hold, the same rewriter, ONE constant changed - write and delete
    # sharing are granted again.  Round 11 does not believe its own share mode either: it asks
    # Windows for the write handle the pin is supposed to forbid, gets it, and refuses the block
    # BEFORE the child exists.
    rc_m2, out_m2 = run("m2", tmp / "rebind_certified.md")
    m2_reason = reason_of(out_m2)
    m2_effected = int("REBIND_EFFECTED=1" in out_m2)
    m2_unlaunched = int("CHILD_NOT_LAUNCHED" in out_m2)
    m2_denied = int("WRITE_OPEN_DENIED=0" in out_m2)
    m2_ok = (rc_m2 != 0 and m2_reason == "SCRIPT_NOT_BOUND_TO_PINNED_OBJECT"
             and m2_effected == 0 and m2_unlaunched == 1 and m2_denied == 1)
    off += not m2_ok
    print(f"D026 MUTANT=M2_pin_share_open rc{rc_m2} REASON={m2_reason} "
          f"WRITE_OPEN_DENIED_0={m2_denied} CHILD_NOT_LAUNCHED={m2_unlaunched} "
          f"REBOUND={m2_effected} {'OK' if m2_ok else 'OFF_EXPECTATION'}")

    # M3, carried: share mode open AND the pre-launch exclusion requirement dropped, the only
    # path that reaches the post-run re-measurement.  The rewrite now succeeds - and under round
    # 11 it changes nothing about what ran, because the child was handed the compared buffer, not
    # the file.  Gate 4 refuses the block anyway, with its stdout unread: the conserved round-10
    # gate is exercised, and its round-11 role is visible - it can only reject conservatively.
    rc_m3, out_m3 = run("m3", tmp / "rebind_certified.md")
    m3_reason = reason_of(out_m3)
    m3_effected = int("REBIND_EFFECTED=1" in out_m3)
    m3_unread = int("STDOUT_NOT_INTERPRETED" in out_m3)
    m3_post = int("POST_BYTES_UNCHANGED=0" in out_m3)
    m3_ok = (rc_m3 != 0 and m3_reason == "SCRIPT_BYTES_CHANGED_UNDER_PIN"
             and m3_effected == 1 and m3_unread == 1 and m3_post == 1)
    off += not m3_ok
    print(f"D026 MUTANT=M3_post_run_reach rc{rc_m3} REASON={m3_reason} "
          f"REBOUND={m3_effected} POST_BYTES_UNCHANGED_0={m3_post} "
          f"STDOUT_NOT_INTERPRETED={m3_unread} {'OK' if m3_ok else 'OFF_EXPECTATION'}")

    # M1, carried from round 9 through round 10: restore the round-8 translating write path and
    # the pre-launch byte gate must refuse BEFORE the child exists.  Under round 11 this gate is
    # the one that protects the buffer, because the buffer IS what the interpreter receives.
    rc_m1, out_m1 = run("m1", tmp / "lf_exact_bytes.md")
    m1_reason = reason_of(out_m1)
    m1_unlaunched = int("CHILD_NOT_LAUNCHED" in out_m1)
    m1_zero = int("SCRIPT_BYTES_IDENTICAL=0" in out_m1)
    m1_ok = (rc_m1 != 0 and m1_reason == "SCRIPT_BYTES_MISMATCH"
             and m1_unlaunched == 1 and m1_zero == 1)
    off += not m1_ok
    print(f"D026 MUTANT=M1_round8_write_path rc{rc_m1} REASON={m1_reason} "
          f"CHILD_NOT_LAUNCHED={m1_unlaunched} SCRIPT_BYTES_IDENTICAL_0={m1_zero} "
          f"{'OK' if m1_ok else 'OFF_EXPECTATION'}")

    # ------------------------------------------------------------------------------------
    # FINDING 1, deterministic.  The work tree is addressed through a free DOS device this
    # block defines; the transient helper re-points it across the child open only.  Round 10
    # samples the pathname before the launch and after the exit, both samples agree, and the
    # bytes the child actually executed came from somewhere else entirely.
    # ------------------------------------------------------------------------------------
    letter_ok = bool(letter) and point_at(letter, real_root)
    print(f"D026_DEVICE LETTER={letter or 'NONE'} DEFINED={int(letter_ok)} "
          f"TARGET_IS_REAL={int(dos_target(letter) == chr(92) + '??' + chr(92) + str(real_root))}")
    off += not letter_ok
    if letter_ok:
        for case, body, want_line, want10, want11, want_reason in TRANSIENT_CASES:
            doc = document(tmp / (case + ".md"), body, want_line)
            scoped = {"TMP": letter + "\\", "TEMP": letter + "\\"}
            rc10, out10 = run("r10_transient", doc, scoped)
            rc11, out11 = run("r11_transient", doc, scoped)
            v10 = "ACCEPTED" if rc10 == 0 else "REJECTED"
            v11 = "ACCEPTED" if rc11 == 0 else "REJECTED"
            reason = reason_of(out11)
            applied10 = int("D026_TRANSIENT APPLIED=1 RESTORED=1" in out10)
            applied11 = int("D026_TRANSIENT APPLIED=1 RESTORED=1" in out11)
            # round 10's two-sample detector, reporting clean while the child ran other bytes
            r10_clean = int("POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1" in out10)
            r11_nameless = int("ARGV_PATH_SEPARATORS=0" in out11)
            ok = ((v10, v11, reason) == (want10, want11, want_reason)
                  and applied10 == 1 and applied11 == 1 and r10_clean == 1
                  and r11_nameless == 1)
            off += not ok
            false_accept += want10 == "ACCEPTED" and want11 == "REJECTED" and ok
            false_reject += want10 == "REJECTED" and want11 == "ACCEPTED" and ok
            transient_denied += v11 == want11 and ok
            print(f"D026 TRANSIENT={case:23s} R10={v10}/rc{rc10} R11={v11}/rc{rc11} "
                  f"R11_REASON={reason} REMAP_APPLIED_AND_RESTORED={applied10}/{applied11} "
                  f"R10_TWO_SAMPLE_DETECTOR=CLEAN/{r10_clean} R11_NAMELESS={r11_nameless} "
                  f"WANT={want10}/{want11}/{want_reason} {'OK' if ok else 'OFF_EXPECTATION'}")

        # M4: the SAME transient remap, the SAME round-11 wrapper, ONE constant flipped back to
        # round 10's pathname channel.  The divergence returns, which is what makes the channel
        # the repair rather than the decoration.
        rc_m4, out_m4 = run("m4", tmp / "transient_certified.md",
                            {"TMP": letter + "\\", "TEMP": letter + "\\"})
        m4_reason = reason_of(out_m4)
        m4_named = int("EXEC_CHANNEL=R10_NAMED_FILE" in out_m4)
        m4_clean = int("POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1" in out_m4)
        m4_ok = rc_m4 == 0 and m4_reason == "OK" and m4_named == 1 and m4_clean == 1
        off += not m4_ok
        print(f"D026 MUTANT=M4_named_channel rc{rc_m4} REASON={m4_reason} "
              f"CHANNEL_NAMED={m4_named} TWO_SAMPLE_DETECTOR=CLEAN/{m4_clean} "
              f"FALSE_ACCEPT_UNDER_NAMED_CHANNEL={int(m4_ok)} "
              f"{'OK' if m4_ok else 'OFF_EXPECTATION'}")
    release(letter)
    print(f"D026_DEVICE RELEASED={int(not dos_target(letter))}")

    # ------------------------------------------------------------------------------------
    # FINDING 2, deterministic.  Two ACQUISITION CONSTRUCTIONS on one tree, with one ordinary
    # junction re-pointed at the exact moment round 10's loop has taken the leaf and has not yet
    # reached the ancestor.  Both constructions are asserted to appear VERBATIM in the published
    # wrapper bytes, so this arm is measuring the published constructions and not a paraphrase.
    # ------------------------------------------------------------------------------------
    R10_LOOP = b"for component in [WORK] + list(WORK.parents):"
    R11_REL = b"child, status = relative_open(parent, component, True)"
    R11_ANCHOR = b"guid_path = final_path(work_pin, VOLUME_NAME_GUID)"
    verbatim = int(R10_LOOP in R10_WRAPPER and R11_REL in R11_WRAPPER
                   and R11_ANCHOR in R11_WRAPPER)
    off += not verbatim
    chain_base = tmp / "chain"
    for arm in ("realA", "realB"):
        (chain_base / arm / "w").mkdir(parents=True)
        (chain_base / arm / "w" / "leaf.ps1").write_bytes(f'"{arm}"\n'.encode())
    link = chain_base / "link"

    def relink(target):
        return subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                              capture_output=True).returncode == 0

    made = relink(chain_base / "realA")
    work = link / "w"
    pinned_leaf = identity_of(work)
    # round 10's construction: leaf-to-root, by NAME, counting handles.
    held = [(str(work), pinned_leaf)]
    swapped = False
    for component in list(work.parents):
        if not swapped:
            swapped = (os.rmdir(link) is None) and relink(chain_base / "realB")
        held.append((str(component), identity_of(component)))
    r10_complete = int(all(identity is not None for _, identity in held))
    live_leaf = identity_of(work)
    r10_mixed = int(live_leaf is not None and live_leaf != pinned_leaf)
    # round 11's construction: the STABLE identity of the pinned object, then relative descent.
    handle = K32.CreateFileW(str(chain_base / "realA" / "w"), 0x80000000, 0x1, None, 3,
                             0x02000000, None)
    buffer = ctypes.create_unicode_buffer(32768)
    K32.GetFinalPathNameByHandleW(ctypes.c_void_p(handle), buffer, 32768, 0x1)
    anchored = buffer.value
    K32.CloseHandle(ctypes.c_void_p(handle))
    r11_anchor_ok = int("realA" in anchored and "link" not in anchored)
    r11_unaffected = int(identity_of(chain_base / "realA" / "w") == pinned_leaf)
    chain_ok = (made and swapped and r10_complete == 1 and r10_mixed == 1
                and verbatim == 1 and r11_anchor_ok == 1 and r11_unaffected == 1)
    off += not chain_ok
    print(f"D026 CHAIN CONSTRUCTIONS_VERBATIM={verbatim} SWAP_APPLIED={int(bool(swapped))} "
          f"R10_HANDLES={len(held)} R10_PATH_PIN_COMPLETE={r10_complete} "
          f"R10_CHAIN_MIXED={r10_mixed} R10_LIVE_LEAF_UNPINNED={r10_mixed} "
          f"R11_ANCHOR=OBJECT_VOLUME_GUID/{r11_anchor_ok} "
          f"R11_UNAFFECTED_BY_SWAP={r11_unaffected} {'OK' if chain_ok else 'OFF_EXPECTATION'}")
    if link.is_dir():
        os.rmdir(link)

    # ------------------------------------------------------------------------------------
    # THE CHANNEL CONTRACT.  The kickoff permits a nameless channel only if every published
    # block's rc, stderr and stdout contract is conserved under it.  Each block of this document
    # is run BOTH ways and the three must agree exactly.  This block itself is excluded, because
    # running it inside itself does not terminate; its own conservation is measured by the
    # section 13c/13d run, which executes it through the nameless channel.
    # ------------------------------------------------------------------------------------
    published = [m.group(2) for m in
                 FENCE.finditer((BASE / "SELF_QA_SEC102_R11.md").read_bytes())
                 if m.group(1) == b"powershell"]
    common = ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass"]
    nameless_command = "& ([scriptblock]::Create([Console]::In.ReadToEnd()))"
    contract = excluded = 0
    for index, body in enumerate(published, 1):
        if b"D026_INSTRUMENT=" in body:
            excluded += 1
            continue
        script = tmp / f"contract_{index:02d}.ps1"
        script.write_bytes(body)
        named = subprocess.run(common + ["-File", str(script)], cwd=str(tmp),
                               capture_output=True)
        free = subprocess.run(common + ["-Command", nameless_command], input=body, cwd=str(tmp),
                              capture_output=True)
        script.unlink()
        same = (named.returncode == free.returncode and named.stdout == free.stdout
                and len(named.stderr) == len(free.stderr))
        contract += same
        off += not same
        print(f"D026_CHANNEL_CONTRACT BLOCK={index:02d} NAMED_RC={named.returncode} "
              f"NAMELESS_RC={free.returncode} STDOUT_IDENTICAL={int(named.stdout == free.stdout)} "
              f"STDERR_BYTES={len(named.stderr)}/{len(free.stderr)} CONSERVED={int(same)}")

    # The pin's PRECONDITION, carried verbatim from round 10.
    probe = tmp / "pin_precondition.ps1"
    probe.write_bytes(b'"D026_PRECONDITION=probe"' + LF)
    holder = K32.CreateFileW(str(probe), 0x40000000, 0x1 | 0x2 | 0x4, None, 3, 0x80, None)
    ctypes.set_last_error(0)
    attempt = K32.CreateFileW(str(probe), 0x80000000, 0x1, None, 3, 0x80, None)
    pin_taken = int(attempt != INVALID)
    pin_err = 0 if pin_taken else ctypes.get_last_error()
    if pin_taken:
        K32.CloseHandle(ctypes.c_void_p(attempt))
    if holder != INVALID:
        K32.CloseHandle(ctypes.c_void_p(holder))
    precondition_ok = pin_taken == 0 and pin_err == 32
    off += not precondition_ok
    print(f"D026_PIN_PRECONDITION EXISTING_WRITER=1 PIN_TAKEN={pin_taken} WINERROR={pin_err} "
          f"{'OK' if precondition_ok else 'OFF_EXPECTATION'}")

    # Round 9's write-path measurement on the real artifact, carried.
    first = [m.group(2) for m in
             FENCE.finditer((BASE / "SELF_QA_SEC102_R11.md").read_bytes())
             if m.group(1) == b"powershell"][0]
    for tag in ("R8_TEXTMODE", "R11_BYTEMODE"):
        path = tmp / (tag + ".ps1")
        if tag == "R8_TEXTMODE":
            path.write_text(first.decode("utf-8"), encoding="utf-8")
        else:
            path.write_bytes(first)
        got = path.read_bytes()
        same = int(got == first)
        off += same != int(tag == "R11_BYTEMODE")
        print(f"D026_WRITEPATH={tag:12s} SOURCE_LF={first.count(LF)} "
              f"SOURCE_CRLF={first.count(CRLF)} WRITTEN_LF={got.count(LF)} "
              f"WRITTEN_CRLF={got.count(CRLF)} BYTE_IDENTICAL={same}")
    shutil.rmtree(chain_base, ignore_errors=True)

print(f"D026_CARRIED={len(CARRIED)} CONSERVED_R10_VERDICTS={conserved} "
      f"D026_REBIND={len(REBIND)} REBIND_DENIED_UNDER_R11={denied} "
      f"D026_TRANSIENT={len(TRANSIENT_CASES)} FALSE_ACCEPT_UNDER_R10={false_accept} "
      f"FALSE_REJECT_UNDER_R10={false_reject} TRANSIENT_CLOSED_UNDER_R11={transient_denied} "
      f"CHANNEL_CONTRACT_CONSERVED={contract} CHANNEL_CONTRACT_SELF_EXCLUDED={excluded} "
      f"M1_GATE_FIRED={int(m1_ok)} M2_EXCLUSION_MEASURED={int(m2_ok)} "
      f"M3_POST_RUN_GATE_FIRED={int(m3_ok)} M4_CHANNEL_LOAD_BEARING={int(m4_ok)} "
      f"D026_OFF_EXPECTATION={off}")
sys.exit(0 if off == 0 else 1)
'@
$d026 | python -B - $base
"D026_HARNESS_BLOCK_RC=$LASTEXITCODE"
```

Real output:

```text
D026_INSTRUMENT=SELF_QA_SEC102_R8.md    PYTHON_FENCES=1 SHA256=391a8e208f16c2c53c434d5800af0fd0c24b49df4ddba39aef28cc96ed11473c
D026_INSTRUMENT=SELF_QA_SEC102_R9.md    PYTHON_FENCES=1 SHA256=54ddb9e6510928e9a1e461826a920c9667dc2c2b2a865d15b96e260d06d21ca9
D026_INSTRUMENT=SELF_QA_SEC102_R10.md   PYTHON_FENCES=1 SHA256=fa17160a92612c93280ca451b06ad7bf8c1bca008b2d8345c1996bf7c303f1bb
D026_INSTRUMENT=SELF_QA_SEC102_R11.md   PYTHON_FENCES=1 SHA256=c04cdab51359a76e41b2a91d6514e2cb3faaa068c9bc90187845463b90ae2ae1
D026_MUTANT=R10_HOLD           SUBSTITUTIONS=1 SHA256=ab1e25db446c926c77a18ce31b087eafa020ab33d0edab32694481b9e029a592
D026_MUTANT=R11_HOLD           SUBSTITUTIONS=1 SHA256=df919527f4d1462e67ab172f2008b695b240a815c63386759f6388a981209693
D026_MUTANT=R10_TRANSIENT      SUBSTITUTIONS=1+1+1 SHA256=789807812176c887f77c2643c848ff01c2a3d23947efc98affc03d4c744d78b9
D026_MUTANT=R11_TRANSIENT      SUBSTITUTIONS=1+1+2 SHA256=4fd04f5c5a03188225ad3c170478d65813278d550ac74256493bd4b7ee67ce89
D026_MUTANT=M4_named_channel   SUBSTITUTIONS=1 SHA256=6056637a3f56201a0bccacfc1000a12f4638b7915e7fd6e55ff9163485c03c99
D026_MUTANT=M2_pin_share_open  SUBSTITUTIONS=1 SHA256=ed715fd3706e4266e0ff79331c54099afc5368b7aa833f32a00b545b72d4e343
D026_MUTANT=M3_post_run_reach  SUBSTITUTIONS=1+1 SHA256=070759729897a689d520cb0f9f0041a35fd23ad726cd84d27ba58586e711b82d
D026_MUTANT=M1_round8_write    SUBSTITUTIONS=1 SHA256=3a6ed2aa8a9cf11f738796fe9fe04aacafb42e3c9f4cc6d69cf548f1078cab2b
D026 CARRIED=well_behaved_child        R10=ACCEPTED/rc0 R11=ACCEPTED/rc0 R11_REASON=OK UNREAD_STDOUT=0 BYTES_ASSERTED=1 LEAF_ON_CHAIN=1 NAMELESS=1 WANT=ACCEPTED/ACCEPTED/OK/0 OK
D026 CARRIED=fails_after_summary       R10=REJECTED/rc1 R11=REJECTED/rc1 R11_REASON=STATUS_REJECT_NONZERO_EXIT UNREAD_STDOUT=1 BYTES_ASSERTED=1 LEAF_ON_CHAIN=1 NAMELESS=1 WANT=REJECTED/REJECTED/STATUS_REJECT_NONZERO_EXIT/1 OK
D026 CARRIED=stderr_after_summary      R10=REJECTED/rc1 R11=REJECTED/rc1 R11_REASON=STATUS_REJECT_UNADJUDICATED_STDERR UNREAD_STDOUT=1 BYTES_ASSERTED=1 LEAF_ON_CHAIN=1 NAMELESS=1 WANT=REJECTED/REJECTED/STATUS_REJECT_UNADJUDICATED_STDERR/1 OK
D026 CARRIED=published_line_absent     R10=REJECTED/rc1 R11=REJECTED/rc1 R11_REASON=MISMATCH UNREAD_STDOUT=0 BYTES_ASSERTED=1 LEAF_ON_CHAIN=1 NAMELESS=1 WANT=REJECTED/REJECTED/MISMATCH/0 OK
D026 CARRIED=crlf_transcript_certified R10=REJECTED/rc1 R11=REJECTED/rc1 R11_REASON=MISMATCH UNREAD_STDOUT=0 BYTES_ASSERTED=1 LEAF_ON_CHAIN=1 NAMELESS=1 WANT=REJECTED/REJECTED/MISMATCH/0 OK
D026 CARRIED=lf_exact_bytes            R10=ACCEPTED/rc0 R11=ACCEPTED/rc0 R11_REASON=OK UNREAD_STDOUT=0 BYTES_ASSERTED=1 LEAF_ON_CHAIN=1 NAMELESS=1 WANT=ACCEPTED/ACCEPTED/OK/0 OK
D026 REBIND=rebind_certified          R10_HOLD=REJECTED/rc1 R11_HOLD=REJECTED/rc1 R11_REASON=MISMATCH REBOUND_UNDER_R11=0 R11_DENIAL=SHARING_VIOLATION_32/1 WANT=REJECTED/REJECTED/MISMATCH OK
D026 REBIND=rebind_honest             R10_HOLD=ACCEPTED/rc0 R11_HOLD=ACCEPTED/rc0 R11_REASON=OK REBOUND_UNDER_R11=0 R11_DENIAL=SHARING_VIOLATION_32/1 WANT=ACCEPTED/ACCEPTED/OK OK
D026 MUTANT=M2_pin_share_open rc1 REASON=SCRIPT_NOT_BOUND_TO_PINNED_OBJECT WRITE_OPEN_DENIED_0=1 CHILD_NOT_LAUNCHED=1 REBOUND=0 OK
D026 MUTANT=M3_post_run_reach rc1 REASON=SCRIPT_BYTES_CHANGED_UNDER_PIN REBOUND=1 POST_BYTES_UNCHANGED_0=1 STDOUT_NOT_INTERPRETED=1 OK
D026 MUTANT=M1_round8_write_path rc1 REASON=SCRIPT_BYTES_MISMATCH CHILD_NOT_LAUNCHED=1 SCRIPT_BYTES_IDENTICAL_0=1 OK
D026_DEVICE LETTER=Z: DEFINED=1 TARGET_IS_REAL=1
D026 TRANSIENT=transient_certified     R10=ACCEPTED/rc0 R11=REJECTED/rc1 R11_REASON=MISMATCH REMAP_APPLIED_AND_RESTORED=1/1 R10_TWO_SAMPLE_DETECTOR=CLEAN/1 R11_NAMELESS=1 WANT=ACCEPTED/REJECTED/MISMATCH OK
D026 TRANSIENT=transient_honest        R10=REJECTED/rc1 R11=ACCEPTED/rc0 R11_REASON=OK REMAP_APPLIED_AND_RESTORED=1/1 R10_TWO_SAMPLE_DETECTOR=CLEAN/1 R11_NAMELESS=1 WANT=REJECTED/ACCEPTED/OK OK
D026 MUTANT=M4_named_channel rc0 REASON=OK CHANNEL_NAMED=1 TWO_SAMPLE_DETECTOR=CLEAN/1 FALSE_ACCEPT_UNDER_NAMED_CHANNEL=1 OK
D026_DEVICE RELEASED=1
D026 CHAIN CONSTRUCTIONS_VERBATIM=1 SWAP_APPLIED=1 R10_HANDLES=10 R10_PATH_PIN_COMPLETE=1 R10_CHAIN_MIXED=1 R10_LIVE_LEAF_UNPINNED=1 R11_ANCHOR=OBJECT_VOLUME_GUID/1 R11_UNAFFECTED_BY_SWAP=1 OK
D026_CHANNEL_CONTRACT BLOCK=01 NAMED_RC=0 NAMELESS_RC=0 STDOUT_IDENTICAL=1 STDERR_BYTES=0/0 CONSERVED=1
D026_CHANNEL_CONTRACT BLOCK=02 NAMED_RC=0 NAMELESS_RC=0 STDOUT_IDENTICAL=1 STDERR_BYTES=0/0 CONSERVED=1
D026_CHANNEL_CONTRACT BLOCK=03 NAMED_RC=0 NAMELESS_RC=0 STDOUT_IDENTICAL=1 STDERR_BYTES=0/0 CONSERVED=1
D026_CHANNEL_CONTRACT BLOCK=04 NAMED_RC=0 NAMELESS_RC=0 STDOUT_IDENTICAL=1 STDERR_BYTES=0/0 CONSERVED=1
D026_CHANNEL_CONTRACT BLOCK=05 NAMED_RC=0 NAMELESS_RC=0 STDOUT_IDENTICAL=1 STDERR_BYTES=0/0 CONSERVED=1
D026_CHANNEL_CONTRACT BLOCK=06 NAMED_RC=0 NAMELESS_RC=0 STDOUT_IDENTICAL=1 STDERR_BYTES=0/0 CONSERVED=1
D026_CHANNEL_CONTRACT BLOCK=07 NAMED_RC=0 NAMELESS_RC=0 STDOUT_IDENTICAL=1 STDERR_BYTES=0/0 CONSERVED=1
D026_CHANNEL_CONTRACT BLOCK=08 NAMED_RC=0 NAMELESS_RC=0 STDOUT_IDENTICAL=1 STDERR_BYTES=0/0 CONSERVED=1
D026_CHANNEL_CONTRACT BLOCK=09 NAMED_RC=0 NAMELESS_RC=0 STDOUT_IDENTICAL=1 STDERR_BYTES=0/0 CONSERVED=1
D026_CHANNEL_CONTRACT BLOCK=10 NAMED_RC=0 NAMELESS_RC=0 STDOUT_IDENTICAL=1 STDERR_BYTES=0/0 CONSERVED=1
D026_PIN_PRECONDITION EXISTING_WRITER=1 PIN_TAKEN=0 WINERROR=32 OK
D026_WRITEPATH=R8_TEXTMODE  SOURCE_LF=110 SOURCE_CRLF=0 WRITTEN_LF=110 WRITTEN_CRLF=110 BYTE_IDENTICAL=0
D026_WRITEPATH=R11_BYTEMODE SOURCE_LF=110 SOURCE_CRLF=0 WRITTEN_LF=110 WRITTEN_CRLF=0 BYTE_IDENTICAL=1
D026_CARRIED=6 CONSERVED_R10_VERDICTS=6 D026_REBIND=2 REBIND_DENIED_UNDER_R11=2 D026_TRANSIENT=2 FALSE_ACCEPT_UNDER_R10=1 FALSE_REJECT_UNDER_R10=1 TRANSIENT_CLOSED_UNDER_R11=2 CHANNEL_CONTRACT_CONSERVED=10 CHANNEL_CONTRACT_SELF_EXCLUDED=1 M1_GATE_FIRED=1 M2_EXCLUSION_MEASURED=1 M3_POST_RUN_GATE_FIRED=1 M4_CHANNEL_LOAD_BEARING=1 D026_OFF_EXPECTATION=0
D026_HARNESS_BLOCK_RC=0
```

Command rc: `0`. `FALSE_ACCEPT_UNDER_R10=1` is Codex's finding 1 at rc level and
`R10_TWO_SAMPLE_DETECTOR=CLEAN/1` is the detector that was supposed to catch it saying it had not
happened. `TRANSIENT_CLOSED_UNDER_R11=2` is the repair, and it is not a better detector: under round
11 the remap is applied and restored around the child exactly as before and the child executes the
compared buffer regardless, because it never opened a name. `M4_CHANNEL_LOAD_BEARING=1` is the
control experiment — one constant back to `-File` and the acceptance returns.
`R10_CHAIN_MIXED=1` with `R11_UNAFFECTED_BY_SWAP=1` is finding 2 and its repair on one tree with one
junction. `CHANNEL_CONTRACT_CONSERVED=10` with `CHANNEL_CONTRACT_SELF_EXCLUDED=1` is the kickoff's
precondition for a nameless channel, measured block by block rather than argued.
`CONSERVED_R10_VERDICTS=6`, `REBIND_DENIED_UNDER_R11=2`, `M1_GATE_FIRED=1`,
`M2_EXCLUSION_MEASURED=1`, `M3_POST_RUN_GATE_FIRED=1` and
`D026_PIN_PRECONDITION ... PIN_TAKEN=0 WINERROR=32` are round 10's evidence surviving intact behind
the new channel.

`D026_WRITEPATH` is round 9's measurement carried, reproduced on the real artifact: this document's
own first `powershell` fence through both write paths.

### 13c. The published round-11 wrapper

Written outside the repository and reproduced here in full so the Lead can re-run it without
trusting this document. The fence marker is built with `chr(96)`, so this source contains no literal
triple backtick and is safe to publish inside the document it parses.

```python
#!/usr/bin/env python3
"""Extract every fenced powershell block from SELF_QA_SEC102_R11.md AS BYTES and execute it
through a channel that performs NO NAME RESOLUTION AT ALL: the bytes read back through a held
handle are the bytes handed to the interpreter, on a pipe, in the same process memory.  Nothing
the child opens can be re-pointed, because the child opens nothing.

Round 11 repairs the two defects `SEC102_CODEX_T1_AUDIT_R10_2026-08-12.md` found in the round-10
wrapper.  Both are the same shape: round 10 bound its proof to a PATHNAME and let the child
resolve that pathname again.

  * finding 1 - a same-session actor can re-point the DOS-device/volume mapping AFTER the
    pre-launch sample, let the child resolve the same pathname to different bytes, and restore
    the mapping BEFORE the post-run sample.  Two samples that agree do not exclude a transient
    rebind between them.
  * finding 2 - `[WORK] + list(WORK.parents)` counted seven directory handles.  A count is not a
    proof that the seven handles form ONE coherent current root-to-leaf chain.

Rounds 7, 8, 9 and 10 each closed one temporal instance of this class and each left a subtler
one.  Round 11 does not add a third temporal sample.  It removes the layer the whole class lives
in - MUTABLE NAME RESOLUTION - and it removes it from the only place that decides anything: the
channel the interpreter consumes.

THE CONSTRUCTION.  `powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command
"& ([scriptblock]::Create([Console]::In.ReadToEnd()))"` compiles and runs whatever arrives on
standard input.  The wrapper hands it the byte string it read THROUGH THE PINNED HANDLE and
compared with the fence - the identical Python object, not a re-read, not a re-resolution, not a
copy of a file.  The child's whole argument vector contains not one path separator; the pipe has
no name; there is no directory entry, no drive letter, no DOS device, no mount point and no
volume anywhere between the compared bytes and the executed bytes.  Executed-byte binding is
therefore a property of the CONSTRUCTION and not of any measurement: there is nothing left to
race, and no post-run sample is load-bearing.

Every round-10 gate is CONSERVED behind that channel rather than replaced - the script is still
written, still pinned before it is verified, still read back through the pin, the exclusion is
still MEASURED (`ERROR_SHARING_VIOLATION`) rather than asserted, the pathname is still bound to
the pinned object, and both are still re-measured after the child exits.  Under round 11 those
gates can no longer produce a false ACCEPT, because the pathname they are about is not the
channel the bytes travelled; they are kept because a gate that can only reject conservatively is
worth keeping, and because retiring a gate an auditor accepted is not this project's habit.

The component chain is rebuilt as a CONSTRUCTION rather than a count (finding 2).  The directory
that holds the scripts is pinned FIRST - which is what makes the operating system refuse every
ancestor rename from that instant, a refusal this wrapper MEASURES on its own subtree in both
directions rather than assuming.  Its stable volume-GUID path is then derived FROM THE HELD
HANDLE (`GetFinalPathNameByHandleW`, `VOLUME_NAME_GUID`), the volume root is opened, and every
component below it is opened RELATIVE TO THE ALREADY-PINNED PARENT with `NtOpenFile`
(`FILE_OPEN_REPARSE_POINT`, so no reparse point is followed), each link's object identity is
recorded, and the descent must terminate at the object the pin holds.  One coherent current
chain by construction, with an identity per link - not `PATH_PIN_HELD=7`.

Tests, in execution order.  1-3 are round 8's and round 9's, conserved verbatim; 0a-0c and 4 are
round 10's, conserved; 0d and the channel are round 11's:

  0a. the work directory is pinned, its volume-GUID path is derived from that handle, and every
      component from the volume root down is opened RELATIVE to its pinned parent and terminates
      at the pinned object                            -> otherwise NO CHILD IS EVER LAUNCHED
  0b. the bytes read back THROUGH THE PINNED HANDLE equal the fence bytes, and Windows itself
      refuses a write-open and a delete-open of the name
                                                      -> otherwise THE CHILD IS NEVER LAUNCHED
  0c. the script is the object its own directory handle reaches by name, and the pathname
      resolves to the pinned object                   -> otherwise THE CHILD IS NEVER LAUNCHED
  0d. the buffer handed to the interpreter IS the buffer that was compared (object identity in
      this process), and the child's argument vector contains no path separator
                                                      -> otherwise THE CHILD IS NEVER LAUNCHED
  1.  process status must be 0                        -> otherwise STDOUT IS NEVER READ
  2.  stderr must be empty, or the block must be       -> otherwise STDOUT IS NEVER READ
      named in STDERR_CONTRACT with a written reason
  4.  after the child exits, the pathname must still resolve to the pinned object and the pinned
      object's bytes must be unchanged (CONSERVED from round 10; under round 11 this can only
      reject conservatively, never admit) -> otherwise STDOUT IS NEVER READ
  3.  only then: every published line must appear in the real stdout (subset check)

What is NOT claimed.  The interpreter IMAGE is still located by name (`powershell.exe` from
`PATH`), exactly as in rounds 7-10, and round 11 makes no claim about which executable receives
the bytes - see section 11, round-11 statement 2, where it is stated as an out-of-model
disclosure rather than dressed as a detected control.

A fence in any language other than `text` ends the current block's transcript association, so
this file's own listing inside the document cannot be mistaken for a published transcript.  The
fence marker is built with chr(96) so this source contains no literal triple backtick and is
therefore safe to publish inside the very document it parses.

The comparison is a SUBSET check: every published line must appear in the real output.
"""

from __future__ import annotations

import ctypes
import hashlib
import os
import pathlib
import re
import subprocess
import sys
import tempfile
from ctypes import wintypes

DOC = pathlib.Path(sys.argv[1])
OUTSIDE = pathlib.Path(sys.argv[2])
raw = DOC.read_bytes()
TICKS = (chr(96) * 3).encode()
FENCE = re.compile(TICKS + rb"([a-z]*)\r?\n(.*?)" + TICKS, re.S)
LF = chr(10).encode()
CRLF = (chr(13) + chr(10)).encode()

# The documented non-empty-stderr contract: block index -> the written reason that block's
# stderr is legitimate.  It is EMPTY, which is the strongest form of the contract.
STDERR_CONTRACT: dict[int, str] = {}

# THE CHANNEL.  One constant, and it is load-bearing: section 13b flips exactly this line and
# shows the transient rebind come back through the round-10 pathname channel.
EXEC_CHANNEL = "NAMELESS_STDIN"
INTERPRETER = "powershell.exe"
COMMON = ["-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass"]
NAMELESS_COMMAND = "& ([scriptblock]::Create([Console]::In.ReadToEnd()))"

# ---------------------------------------------------------------------------------------------
# Win32 / NT.  One share mode, one relative-open primitive, and the errors Windows returns.
# ---------------------------------------------------------------------------------------------
K32 = ctypes.WinDLL("kernel32", use_last_error=True)
NTDLL = ctypes.WinDLL("ntdll", use_last_error=True)
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
DELETE = 0x00010000
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
FILE_SHARE_DELETE = 0x00000004
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x00000080
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FILE_BEGIN = 0
ERROR_SHARING_VIOLATION = 32
ERROR_ACCESS_DENIED = 5
INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value
VOLUME_NAME_GUID = 0x00000001
VOLUME_NAME_NT = 0x00000002
FILE_READ_ATTRIBUTES = 0x00000080
SYNCHRONIZE = 0x00100000
FILE_LIST_DIRECTORY = 0x00000001
FILE_TRAVERSE = 0x00000020
FILE_DIRECTORY_FILE = 0x00000001
FILE_NON_DIRECTORY_FILE = 0x00000040
FILE_SYNCHRONOUS_IO_NONALERT = 0x00000020
FILE_OPEN_REPARSE_POINT = 0x00200000
OBJ_CASE_INSENSITIVE = 0x00000040

# THE PIN.  Read sharing is granted so nothing legitimate is broken; write and delete sharing are
# withheld, which is what makes a concurrent modify, replace, rename or delete impossible for as
# long as the handle is held.  Section 13b flips exactly this constant too.
PIN_SHARE = FILE_SHARE_READ


class UNICODE_STRING(ctypes.Structure):
    _fields_ = [("Length", wintypes.USHORT), ("MaximumLength", wintypes.USHORT),
                ("Buffer", wintypes.LPWSTR)]


class OBJECT_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("Length", wintypes.ULONG), ("RootDirectory", wintypes.HANDLE),
                ("ObjectName", ctypes.POINTER(UNICODE_STRING)), ("Attributes", wintypes.ULONG),
                ("SecurityDescriptor", wintypes.LPVOID),
                ("SecurityQualityOfService", wintypes.LPVOID)]


class IO_STATUS_BLOCK(ctypes.Structure):
    _fields_ = [("Status", ctypes.c_void_p), ("Information", ctypes.c_void_p)]


class BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
    _fields_ = [("dwFileAttributes", wintypes.DWORD), ("ftCreationTime", wintypes.FILETIME),
                ("ftLastAccessTime", wintypes.FILETIME), ("ftLastWriteTime", wintypes.FILETIME),
                ("dwVolumeSerialNumber", wintypes.DWORD), ("nFileSizeHigh", wintypes.DWORD),
                ("nFileSizeLow", wintypes.DWORD), ("nNumberOfLinks", wintypes.DWORD),
                ("nFileIndexHigh", wintypes.DWORD), ("nFileIndexLow", wintypes.DWORD)]


K32.CreateFileW.restype = wintypes.HANDLE
K32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
                            wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
K32.ReadFile.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
                         ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID]
K32.SetFilePointerEx.argtypes = [wintypes.HANDLE, ctypes.c_longlong,
                                 ctypes.POINTER(ctypes.c_longlong), wintypes.DWORD]
K32.CloseHandle.argtypes = [wintypes.HANDLE]
K32.GetFileInformationByHandle.argtypes = [wintypes.HANDLE,
                                           ctypes.POINTER(BY_HANDLE_FILE_INFORMATION)]
K32.GetFinalPathNameByHandleW.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD,
                                          wintypes.DWORD]
NTDLL.NtOpenFile.argtypes = [ctypes.POINTER(wintypes.HANDLE), wintypes.DWORD,
                             ctypes.POINTER(OBJECT_ATTRIBUTES),
                             ctypes.POINTER(IO_STATUS_BLOCK), wintypes.ULONG, wintypes.ULONG]


def win_open(path, access, share, flags=FILE_ATTRIBUTE_NORMAL):
    """Open an existing object BY NAME.  Returns (handle, 0) or (None, win32 error code)."""
    ctypes.set_last_error(0)
    handle = K32.CreateFileW(str(path), access, share, None, OPEN_EXISTING, flags, None)
    if handle == INVALID_HANDLE_VALUE:
        return None, ctypes.get_last_error()
    return handle, 0


def relative_open(parent, component, directory):
    """Open `component` RELATIVE TO the already-pinned `parent` handle.  No part of the name
    above `component` is resolved, so nothing above it can be re-pointed between links; and
    FILE_OPEN_REPARSE_POINT means a reparse point put in the way is opened, not followed."""
    buffer = ctypes.create_unicode_buffer(component)
    name = UNICODE_STRING(len(component) * 2, len(component) * 2,
                          ctypes.cast(buffer, wintypes.LPWSTR))
    attributes = OBJECT_ATTRIBUTES(ctypes.sizeof(OBJECT_ATTRIBUTES), parent,
                                   ctypes.pointer(name), OBJ_CASE_INSENSITIVE, None, None)
    iosb = IO_STATUS_BLOCK()
    handle = wintypes.HANDLE()
    access = (FILE_READ_ATTRIBUTES | SYNCHRONIZE
              | (FILE_LIST_DIRECTORY | FILE_TRAVERSE if directory else GENERIC_READ))
    options = (FILE_SYNCHRONOUS_IO_NONALERT | FILE_OPEN_REPARSE_POINT
               | (FILE_DIRECTORY_FILE if directory else FILE_NON_DIRECTORY_FILE))
    status = NTDLL.NtOpenFile(ctypes.byref(handle), access, ctypes.byref(attributes),
                              ctypes.byref(iosb), PIN_SHARE, options)
    return (handle.value, 0) if status == 0 else (None, status & 0xFFFFFFFF)


def object_identity(handle):
    """The object's true identity: volume serial number + NTFS file index."""
    info = BY_HANDLE_FILE_INFORMATION()
    if not K32.GetFileInformationByHandle(handle, ctypes.byref(info)):
        return None
    return (info.dwVolumeSerialNumber, info.nFileIndexHigh, info.nFileIndexLow)


def final_path(handle, flags):
    """The canonical path of the object THE HANDLE ALREADY HOLDS - derived from the object, not
    from any name we were given."""
    buffer = ctypes.create_unicode_buffer(32768)
    return buffer.value if K32.GetFinalPathNameByHandleW(handle, buffer, 32768, flags) else ""


def read_through_handle(handle):
    """Read the whole object THROUGH THE HELD HANDLE.  Re-opening the name to read it back is
    precisely the round-9 defect, so the name is never used here."""
    K32.SetFilePointerEx(handle, 0, None, FILE_BEGIN)
    buffer = ctypes.create_string_buffer(65536)
    got = wintypes.DWORD(0)
    chunks = []
    while True:
        if not K32.ReadFile(handle, buffer, 65536, ctypes.byref(got), None):
            raise OSError(ctypes.get_last_error(), "ReadFile through pinned handle")
        if got.value == 0:
            return b"".join(chunks)
        chunks.append(buffer.raw[:got.value])


def name_identity(path):
    """Resolve the pathname and report which object it reaches.  CONSERVED from round 10 - under
    round 11 nothing is executed through this pathname, so this can only reject, never admit."""
    handle, err = win_open(path, GENERIC_READ, FILE_SHARE_READ)
    if handle is None:
        return None, err
    identity = object_identity(handle)
    K32.CloseHandle(handle)
    return identity, 0


def exclusion_is_real(path):
    """MEASURE the exclusion instead of asserting it: ask Windows for a write handle and for a
    delete handle on the name, and require ERROR_SHARING_VIOLATION on both."""
    write_handle, write_err = win_open(path, GENERIC_WRITE,
                                       FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE)
    if write_handle is not None:
        K32.CloseHandle(write_handle)
    delete_handle, delete_err = win_open(path, DELETE,
                                         FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE)
    if delete_handle is not None:
        K32.CloseHandle(delete_handle)
    return (write_handle is None and write_err == ERROR_SHARING_VIOLATION
            and delete_handle is None and delete_err == ERROR_SHARING_VIOLATION,
            write_err, delete_err)


def write_script(command: bytes, path: pathlib.Path) -> None:
    """Write the fence bytes with no newline translation in either direction.  Round 9's repair,
    carried; section 13b still restores the round-8 write path and shows the byte gate fire."""
    path.write_bytes(command)


# ---------------------------------------------------------------------------------------------
# (0a) ONE COHERENT CURRENT CHAIN, BY CONSTRUCTION - the round-10 finding 2 repair.
#
# Round 10 opened `[WORK] + list(WORK.parents)` and printed how many handles it got.  Seven
# handles are not a chain.  Round 11:
#   1. pins WORK FIRST.  On NTFS an open handle anywhere in a subtree makes the operating system
#      refuse to rename ANY ancestor of it, so from this instant the chain above WORK is frozen -
#      and that refusal is MEASURED below, in both directions, on this wrapper's own subtree.
#   2. derives WORK's STABLE volume-GUID path FROM THE HELD HANDLE, not from the pathname it was
#      given, so a drive-letter or DOS-device remap cannot change which volume is walked.
#   3. opens the volume root, then every component RELATIVE TO ITS ALREADY-PINNED PARENT, records
#      each link's object identity, and requires the descent to terminate at the object the WORK
#      pin holds.  Adjacency is then a property of how the handles were obtained.
# ---------------------------------------------------------------------------------------------
WORK = pathlib.Path(tempfile.mkdtemp(prefix="sec102_r11_")).resolve()

# The platform property the chain rests on, MEASURED in BOTH directions on a throwaway subtree of
# this wrapper's own, BEFORE anything is pinned - permitted while nothing is held, refused by the
# operating system once a descendant is pinned - so step 1 is a measurement of Windows rather
# than a sentence about Windows.  The probe tree is created and removed before the chain exists,
# because a pinned directory also refuses renames of its own entries (measured separately below).
PROBE = pathlib.Path(tempfile.mkdtemp(prefix="sec102_r11_probe_")).resolve()


def rename_round_trip(target: pathlib.Path):
    try:
        os.rename(target, target.with_name(target.name + "_swapped"))
        os.rename(target.with_name(target.name + "_swapped"), target)
        return "PERMITTED", 0
    except OSError as exc:
        return "DENIED", exc.winerror or 0


probe_ancestor = PROBE / "ancestor"
(probe_ancestor / "descendant").mkdir(parents=True)
free_verdict, free_err = rename_round_trip(probe_ancestor)
# Deliberately the LITERAL exclusive share mode, not PIN_SHARE: these three lines measure a
# property of Windows, so they must not move when section 13b flips this wrapper's pin constant.
probe_pin, _ = win_open(probe_ancestor / "descendant", GENERIC_READ, FILE_SHARE_READ,
                        FILE_FLAG_BACKUP_SEMANTICS)
held_verdict, held_err = rename_round_trip(probe_ancestor)
if probe_pin is not None:
    K32.CloseHandle(probe_pin)
# and the same measurement for a directory holding an entry: while the DIRECTORY is held with
# write and delete sharing withheld, Windows refuses to rename or replace any entry inside it,
# which is what protects each script's own directory entry for as long as the run lasts.
probe_parent = PROBE / "parent"
(probe_parent / "entry").mkdir(parents=True)
parent_pin, _ = win_open(probe_parent, GENERIC_READ, FILE_SHARE_READ, FILE_FLAG_BACKUP_SEMANTICS)
entry_verdict, entry_err = rename_round_trip(probe_parent / "entry")
if parent_pin is not None:
    K32.CloseHandle(parent_pin)
(probe_parent / "entry").rmdir()
probe_parent.rmdir()
(probe_ancestor / "descendant").rmdir()
probe_ancestor.rmdir()
PROBE.rmdir()
ancestor_frozen = (free_verdict == "PERMITTED" and held_verdict == "DENIED"
                   and held_err == ERROR_ACCESS_DENIED)
entry_frozen = entry_verdict == "DENIED" and entry_err == ERROR_SHARING_VIOLATION

work_pin, work_err = win_open(WORK, GENERIC_READ, PIN_SHARE, FILE_FLAG_BACKUP_SEMANTICS)
chain_handles: list[int] = []
chain_links: list[tuple[str, tuple | None]] = []
chain_coherent = False
guid_path = nt_path = ""
if work_pin is not None:
    guid_path = final_path(work_pin, VOLUME_NAME_GUID)
    nt_path = final_path(work_pin, VOLUME_NAME_NT)
    head = guid_path[4:] if guid_path.startswith("\\\\?\\") else ""
    parts = [p for p in head.split("\\") if p]
    if parts:
        volume_root = "\\\\?\\" + parts[0] + "\\"
        root_handle, root_err = win_open(volume_root, GENERIC_READ, PIN_SHARE,
                                         FILE_FLAG_BACKUP_SEMANTICS)
        if root_handle is not None:
            chain_handles.append(root_handle)
            chain_links.append((parts[0], object_identity(root_handle)))
            parent = root_handle
            for component in parts[1:]:
                child, status = relative_open(parent, component, True)
                if child is None:
                    chain_links.append((component + f"=NTSTATUS_0x{status:08X}", None))
                    break
                chain_handles.append(child)
                chain_links.append((component, object_identity(child)))
                parent = child
            else:
                chain_coherent = object_identity(parent) == object_identity(work_pin)
work_dir_handle = chain_handles[-1] if chain_coherent else work_pin
frozen = ancestor_frozen and entry_frozen

# The per-link disposition finding 2 asked for: an identity per component and an adjacency
# disposition per component, not one count.  Component NAMES and raw file indices are deliberately
# not printed - they carry this host's user name and a per-run temporary directory, and a
# transcript that cannot be re-derived byte-for-byte is the Pattern-10 defect.  What is printed is
# the property: how each link was obtained, that its identity was read, and that it is a distinct
# object from its parent.  A link that fails prints its component and NTSTATUS instead.
recorded = sum(identity is not None for _, identity in chain_links)
distinct = sum(chain_links[k][1] is not None and chain_links[k][1] != chain_links[k - 1][1]
               for k in range(1, len(chain_links)))
print(f"CHAIN_LINKS={len(chain_links)} CHAIN_RELATIVE_OPENS={max(len(chain_handles) - 1, 0)} "
      f"CHAIN_IDENTITIES_RECORDED={recorded} CHAIN_ADJACENT_PAIRS_DISTINCT={distinct} "
      f"CHAIN_TERMINATES_AT_PINNED_DIR={int(chain_coherent)} "
      f"CHAIN_COHERENT={int(chain_coherent)} CHAIN_ANCHOR=VOLUME_GUID "
      f"PIN_SHARE_DENIES=WRITE|DELETE")
for depth, (component, identity) in enumerate(chain_links):
    if identity is None:
        print(f"    CHAIN[{depth}] OPEN_FAILED {component}")
    elif depth == 0:
        print(f"    CHAIN[{depth}] OPENED=ABSOLUTE_VOLUME_GUID_ROOT IDENTITY_RECORDED=1")
    else:
        terminal = depth == len(chain_links) - 1 and chain_coherent
        print(f"    CHAIN[{depth}] OPENED=RELATIVE_TO_CHAIN[{depth - 1}] IDENTITY_RECORDED=1 "
              f"DISTINCT_FROM_PARENT={int(identity != chain_links[depth - 1][1])}"
              + (" TERMINATES_AT_WORK_PIN=1" if terminal else ""))
print(f"ANCESTOR_RENAME_NOTHING_HELD={free_verdict}/{free_err} "
      f"ANCESTOR_RENAME_DESCENDANT_HELD={held_verdict}/{held_err} "
      f"HELD_DIR_ENTRY_RENAME={entry_verdict}/{entry_err} "
      f"ANCESTOR_CHAIN_FROZEN={int(ancestor_frozen)} DIR_ENTRIES_FROZEN={int(entry_frozen)}")
if not (chain_coherent and frozen):
    print("CHAIN_NOT_COHERENT CHILD_NOT_LAUNCHED")

blocks: list[tuple[bytes, list[bytes]]] = []
current: list[bytes] | None = None
for match in FENCE.finditer(raw):
    kind, body = match.group(1), match.group(2)
    if kind == b"powershell":
        current = []
        blocks.append((body, current))
    elif kind == b"text" and current is not None:
        current.append(body)
    elif kind != b"text":
        current = None

rejected = byte_rejects = binding_rejects = status_rejects = stderr_rejects = mismatched = 0
compared = complete = identical = pinned = bound = post_bound = post_same = 0
in_chain = nameless = 0
print(f"BLOCKS_FOUND={len(blocks)} STDERR_CONTRACT_ENTRIES={len(STDERR_CONTRACT)} "
      f"EXEC_CHANNEL={EXEC_CHANNEL}")
for index, (command, published) in enumerate(blocks, 1):
    lines = command.strip().splitlines()
    label = lines[1][:70].decode("utf-8", "replace") if len(lines) > 1 else "?"
    name = f"block_{index:02d}.ps1"
    script = WORK / name
    write_script(command, script)

    # (0b) CONSERVED from round 10.  The object is pinned BEFORE it is verified, the bytes are
    # read back THROUGH the pin rather than by re-opening the name, and Windows is asked to break
    # the pin and refuses.
    pin, pin_err = win_open(script, GENERIC_READ, PIN_SHARE)
    if pin is None or not (chain_coherent and frozen):
        rejected += 1
        byte_rejects += 1
        print(f"BLOCK={index:02d} PIN_HELD=0 PIN_WINERROR={pin_err} "
              f"SCRIPT_NOT_PINNED CHILD_NOT_LAUNCHED {label}")
        if pin is not None:
            K32.CloseHandle(pin)
        script.unlink(missing_ok=True)
        continue
    pinned += 1
    on_disk = read_through_handle(pin)
    same = on_disk == command
    identical += same
    excluded, write_err, delete_err = exclusion_is_real(script)
    pinned_object = object_identity(pin)
    # (0c) the leaf is reached RELATIVE TO the pinned directory handle - one more link on the
    # same coherent chain - and, conserved from round 10, the pathname is bound too.
    leaf_handle, leaf_status = relative_open(work_dir_handle, name, False)
    leaf_in_chain = leaf_handle is not None and object_identity(leaf_handle) == pinned_object
    if leaf_handle is not None:
        K32.CloseHandle(leaf_handle)
    in_chain += leaf_in_chain
    resolved, resolve_err = name_identity(script)
    name_bound = resolved is not None and resolved == pinned_object
    bound += name_bound
    print(f"BLOCK={index:02d} FENCE_BYTES={len(command)} SCRIPT_BYTES={len(on_disk)} "
          f"LF={command.count(LF)} CRLF={command.count(CRLF)} "
          f"NONASCII={sum(byte > 127 for byte in command)} "
          f"SCRIPT_BYTES_IDENTICAL={int(same)} SHA256={hashlib.sha256(on_disk).hexdigest()}")
    print(f"BLOCK={index:02d} PIN_HELD=1 READ_THROUGH_PIN=1 "
          f"WRITE_OPEN_DENIED={int(write_err == ERROR_SHARING_VIOLATION)} "
          f"DELETE_OPEN_DENIED={int(delete_err == ERROR_SHARING_VIOLATION)} "
          f"WINERROR={write_err}/{delete_err} LEAF_ON_PINNED_CHAIN={int(leaf_in_chain)} "
          f"NAME_BOUND_TO_PINNED_OBJECT={int(name_bound)}")
    if not same:
        K32.CloseHandle(pin)
        script.unlink(missing_ok=True)
        rejected += 1
        byte_rejects += 1
        print(f"BLOCK={index:02d} SCRIPT_BYTES_MISMATCH CHILD_NOT_LAUNCHED {label}")
        continue
    if not (excluded and name_bound and leaf_in_chain):
        K32.CloseHandle(pin)
        script.unlink(missing_ok=True)
        rejected += 1
        binding_rejects += 1
        print(f"BLOCK={index:02d} SCRIPT_NOT_BOUND_TO_PINNED_OBJECT CHILD_NOT_LAUNCHED {label}")
        continue

    # (0d) THE ROUND-11 CONSTRUCTION.  `payload` IS `on_disk` - the identical object read through
    # the pin and compared above, not a re-read and not a pathname - and the argument vector the
    # child receives contains no path separator at all, so there is no name for anything to
    # re-point between this line and the interpreter's parser.
    if EXEC_CHANNEL == "NAMELESS_STDIN":
        argv = [INTERPRETER, *COMMON, "-Command", NAMELESS_COMMAND]
        payload = on_disk
    else:
        argv = [INTERPRETER, *COMMON, "-File", str(script)]
        payload = None
    separators = sum(argument.count("\\") + argument.count("/") for argument in argv)
    buffer_is_pinned_read = payload is on_disk
    print(f"BLOCK={index:02d} EXEC_CHANNEL={EXEC_CHANNEL} ARGV_PATH_SEPARATORS={separators} "
          f"EXEC_BUFFER_IS_PINNED_READ={int(buffer_is_pinned_read)} "
          f"EXEC_SHA256={hashlib.sha256(payload).hexdigest() if payload is not None else 'NONE'}")
    if EXEC_CHANNEL == "NAMELESS_STDIN" and not (buffer_is_pinned_read and separators == 0):
        K32.CloseHandle(pin)
        script.unlink(missing_ok=True)
        rejected += 1
        binding_rejects += 1
        print(f"BLOCK={index:02d} EXEC_NOT_NAMELESS CHILD_NOT_LAUNCHED {label}")
        continue
    nameless += EXEC_CHANNEL == "NAMELESS_STDIN" and separators == 0

    done = subprocess.run(
        argv, input=payload, cwd=str(OUTSIDE), capture_output=True,
    )
    # (4) CONSERVED from round 10, and deliberately no longer load-bearing: the pathname below is
    # not the channel the bytes travelled, so this re-measurement can reject conservatively but
    # can no longer be the thing that admits a block.
    after_resolved, after_err = name_identity(script)
    after_bound = after_resolved is not None and after_resolved == pinned_object
    after_bytes = read_through_handle(pin)
    after_identical = after_bytes == command
    post_bound += after_bound
    post_same += after_identical
    K32.CloseHandle(pin)
    script.unlink(missing_ok=True)
    err = done.stderr.decode("utf-8", "replace") if done.stderr else ""
    out = done.stdout.decode("utf-8", "replace") if done.stdout else ""
    head = (f"BLOCK={index:02d} RC={done.returncode} STDERR_BYTES={len(done.stderr or b'')} "
            f"POST_NAME_BOUND={int(after_bound)} POST_BYTES_UNCHANGED={int(after_identical)}")

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
    # (4) conserved round-10 gates, still terminal.
    if not after_bound:
        rejected += 1
        binding_rejects += 1
        print(f"{head} SCRIPT_REBOUND_UNDER_PIN STDOUT_NOT_INTERPRETED {label}")
        continue
    if not after_identical:
        rejected += 1
        binding_rejects += 1
        print(f"{head} SCRIPT_BYTES_CHANGED_UNDER_PIN STDOUT_NOT_INTERPRETED {label}")
        continue
    complete += 1
    note = "STATUS_OK" if not err else f"STATUS_OK_STDERR_ADJUDICATED[{STDERR_CONTRACT[index]}]"

    # (3) only now may the transcript be interpreted.
    if not published:
        rejected += 1
        print(f"{head} {note} NO_PUBLISHED_TRANSCRIPT {label}")
        continue
    actual = [line.rstrip() for line in out.splitlines()]
    want = [line.rstrip() for chunk in published
            for line in chunk.decode("utf-8", "replace").splitlines()]
    missing = [line for line in want if line not in actual]
    compared += 1
    mismatched += bool(missing)
    rejected += bool(missing)
    print(f"{head} {note} PUBLISHED_LINES={len(want)} MISSING_FROM_REAL_OUTPUT={len(missing)} "
          f"{'OK' if not missing else 'MISMATCH'} {label}")
    for line in missing[:5]:
        print(f"    MISSING {line}")
if work_pin is not None:
    K32.CloseHandle(work_pin)
for handle in chain_handles:
    K32.CloseHandle(wintypes.HANDLE(handle))
try:
    WORK.rmdir()
except OSError:
    pass
print(f"BLOCKS={len(blocks)} SCRIPT_BYTES_IDENTICAL_ALL={identical} PINNED_ALL={pinned} "
      f"LEAF_ON_CHAIN_ALL={in_chain} NAME_BOUND_ALL={bound} NAMELESS_EXEC_ALL={nameless} "
      f"POST_NAME_BOUND_ALL={post_bound} POST_BYTES_UNCHANGED_ALL={post_same} "
      f"REJECTED_ON_BYTES={byte_rejects} REJECTED_ON_BINDING={binding_rejects} "
      f"STATUS_PROVED_COMPLETE={complete} REJECTED_ON_STATUS={status_rejects} "
      f"REJECTED_ON_STDERR={stderr_rejects} COMPARED={compared} MISMATCHED={mismatched} "
      f"REJECTED={rejected} CWD={OUTSIDE}")
sys.exit(0 if rejected == 0 and chain_coherent and frozen else 1)
```

### 13d. Real byte identity, chain, channel and status for all eleven blocks

Write the section-13c fence to `verify_selfqa_r11.py` in a directory outside the repository and run
it as `python -B verify_selfqa_r11.py <path-to-this-file> <that-directory>`. Real output:

```text
CHAIN_LINKS=7 CHAIN_RELATIVE_OPENS=6 CHAIN_IDENTITIES_RECORDED=7 CHAIN_ADJACENT_PAIRS_DISTINCT=6 CHAIN_TERMINATES_AT_PINNED_DIR=1 CHAIN_COHERENT=1 CHAIN_ANCHOR=VOLUME_GUID PIN_SHARE_DENIES=WRITE|DELETE
    CHAIN[0] OPENED=ABSOLUTE_VOLUME_GUID_ROOT IDENTITY_RECORDED=1
    CHAIN[1] OPENED=RELATIVE_TO_CHAIN[0] IDENTITY_RECORDED=1 DISTINCT_FROM_PARENT=1
    CHAIN[2] OPENED=RELATIVE_TO_CHAIN[1] IDENTITY_RECORDED=1 DISTINCT_FROM_PARENT=1
    CHAIN[3] OPENED=RELATIVE_TO_CHAIN[2] IDENTITY_RECORDED=1 DISTINCT_FROM_PARENT=1
    CHAIN[4] OPENED=RELATIVE_TO_CHAIN[3] IDENTITY_RECORDED=1 DISTINCT_FROM_PARENT=1
    CHAIN[5] OPENED=RELATIVE_TO_CHAIN[4] IDENTITY_RECORDED=1 DISTINCT_FROM_PARENT=1
    CHAIN[6] OPENED=RELATIVE_TO_CHAIN[5] IDENTITY_RECORDED=1 DISTINCT_FROM_PARENT=1 TERMINATES_AT_WORK_PIN=1
ANCESTOR_RENAME_NOTHING_HELD=PERMITTED/0 ANCESTOR_RENAME_DESCENDANT_HELD=DENIED/5 HELD_DIR_ENTRY_RENAME=DENIED/32 ANCESTOR_CHAIN_FROZEN=1 DIR_ENTRIES_FROZEN=1
BLOCKS_FOUND=11 STDERR_CONTRACT_ENTRIES=0 EXEC_CHANNEL=NAMELESS_STDIN
BLOCK=01 FENCE_BYTES=8316 SCRIPT_BYTES=8316 LF=110 CRLF=0 NONASCII=0 SCRIPT_BYTES_IDENTICAL=1 SHA256=a02bd8235dee5d9f04dbf8235c883c6f2d5cdc91782840e24f19142a637f779b
BLOCK=01 PIN_HELD=1 READ_THROUGH_PIN=1 WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32 LEAF_ON_PINNED_CHAIN=1 NAME_BOUND_TO_PINNED_OBJECT=1
BLOCK=01 EXEC_CHANNEL=NAMELESS_STDIN ARGV_PATH_SEPARATORS=0 EXEC_BUFFER_IS_PINNED_READ=1 EXEC_SHA256=a02bd8235dee5d9f04dbf8235c883c6f2d5cdc91782840e24f19142a637f779b
BLOCK=01 RC=0 STDERR_BYTES=0 POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1 STATUS_OK PUBLISHED_LINES=51 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=02 FENCE_BYTES=6322 SCRIPT_BYTES=6322 LF=81 CRLF=0 NONASCII=0 SCRIPT_BYTES_IDENTICAL=1 SHA256=ca5f5ffe5fd27d91a294267d8b82256b8ac98f5b7ba3fcc27c1cd639eae2e908
BLOCK=02 PIN_HELD=1 READ_THROUGH_PIN=1 WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32 LEAF_ON_PINNED_CHAIN=1 NAME_BOUND_TO_PINNED_OBJECT=1
BLOCK=02 EXEC_CHANNEL=NAMELESS_STDIN ARGV_PATH_SEPARATORS=0 EXEC_BUFFER_IS_PINNED_READ=1 EXEC_SHA256=ca5f5ffe5fd27d91a294267d8b82256b8ac98f5b7ba3fcc27c1cd639eae2e908
BLOCK=02 RC=0 STDERR_BYTES=0 POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1 STATUS_OK PUBLISHED_LINES=59 MISSING_FROM_REAL_OUTPUT=0 OK $tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_
BLOCK=03 FENCE_BYTES=2533 SCRIPT_BYTES=2533 LF=51 CRLF=0 NONASCII=0 SCRIPT_BYTES_IDENTICAL=1 SHA256=1294b658374d717661b06222ffed7cfc95c64f54c2cda284ec08e4f5f2205294
BLOCK=03 PIN_HELD=1 READ_THROUGH_PIN=1 WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32 LEAF_ON_PINNED_CHAIN=1 NAME_BOUND_TO_PINNED_OBJECT=1
BLOCK=03 EXEC_CHANNEL=NAMELESS_STDIN ARGV_PATH_SEPARATORS=0 EXEC_BUFFER_IS_PINNED_READ=1 EXEC_SHA256=1294b658374d717661b06222ffed7cfc95c64f54c2cda284ec08e4f5f2205294
BLOCK=03 RC=0 STDERR_BYTES=0 POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1 STATUS_OK PUBLISHED_LINES=26 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=04 FENCE_BYTES=8139 SCRIPT_BYTES=8139 LF=151 CRLF=0 NONASCII=0 SCRIPT_BYTES_IDENTICAL=1 SHA256=4f1e84f48e26240bb1e119fa68621ed284275e0edc4900efef3c4dba5c10b0f9
BLOCK=04 PIN_HELD=1 READ_THROUGH_PIN=1 WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32 LEAF_ON_PINNED_CHAIN=1 NAME_BOUND_TO_PINNED_OBJECT=1
BLOCK=04 EXEC_CHANNEL=NAMELESS_STDIN ARGV_PATH_SEPARATORS=0 EXEC_BUFFER_IS_PINNED_READ=1 EXEC_SHA256=4f1e84f48e26240bb1e119fa68621ed284275e0edc4900efef3c4dba5c10b0f9
BLOCK=04 RC=0 STDERR_BYTES=0 POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1 STATUS_OK PUBLISHED_LINES=42 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=05 FENCE_BYTES=9601 SCRIPT_BYTES=9601 LF=134 CRLF=0 NONASCII=0 SCRIPT_BYTES_IDENTICAL=1 SHA256=467b348487e86eb637e00a81800927a040eea1fd3a74c92504c78ed27045bc64
BLOCK=05 PIN_HELD=1 READ_THROUGH_PIN=1 WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32 LEAF_ON_PINNED_CHAIN=1 NAME_BOUND_TO_PINNED_OBJECT=1
BLOCK=05 EXEC_CHANNEL=NAMELESS_STDIN ARGV_PATH_SEPARATORS=0 EXEC_BUFFER_IS_PINNED_READ=1 EXEC_SHA256=467b348487e86eb637e00a81800927a040eea1fd3a74c92504c78ed27045bc64
BLOCK=05 RC=0 STDERR_BYTES=0 POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1 STATUS_OK PUBLISHED_LINES=9 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=06 FENCE_BYTES=5440 SCRIPT_BYTES=5440 LF=119 CRLF=0 NONASCII=0 SCRIPT_BYTES_IDENTICAL=1 SHA256=79c828245b86cacf16b0547f3621330eacb7d2aca83756432b0fafc9579248dd
BLOCK=06 PIN_HELD=1 READ_THROUGH_PIN=1 WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32 LEAF_ON_PINNED_CHAIN=1 NAME_BOUND_TO_PINNED_OBJECT=1
BLOCK=06 EXEC_CHANNEL=NAMELESS_STDIN ARGV_PATH_SEPARATORS=0 EXEC_BUFFER_IS_PINNED_READ=1 EXEC_SHA256=79c828245b86cacf16b0547f3621330eacb7d2aca83756432b0fafc9579248dd
BLOCK=06 RC=0 STDERR_BYTES=0 POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1 STATUS_OK PUBLISHED_LINES=10 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=07 FENCE_BYTES=5396 SCRIPT_BYTES=5396 LF=95 CRLF=0 NONASCII=0 SCRIPT_BYTES_IDENTICAL=1 SHA256=7c66da5889124e919f983a527c0c6975e1fadfa5369aef90dd280d37c7154592
BLOCK=07 PIN_HELD=1 READ_THROUGH_PIN=1 WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32 LEAF_ON_PINNED_CHAIN=1 NAME_BOUND_TO_PINNED_OBJECT=1
BLOCK=07 EXEC_CHANNEL=NAMELESS_STDIN ARGV_PATH_SEPARATORS=0 EXEC_BUFFER_IS_PINNED_READ=1 EXEC_SHA256=7c66da5889124e919f983a527c0c6975e1fadfa5369aef90dd280d37c7154592
BLOCK=07 RC=0 STDERR_BYTES=0 POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1 STATUS_OK PUBLISHED_LINES=30 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=08 FENCE_BYTES=3567 SCRIPT_BYTES=3567 LF=58 CRLF=0 NONASCII=0 SCRIPT_BYTES_IDENTICAL=1 SHA256=709c6da5d8e44a08a6060a155d10620c8849a19ea16cdaf5df354a43a083ab20
BLOCK=08 PIN_HELD=1 READ_THROUGH_PIN=1 WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32 LEAF_ON_PINNED_CHAIN=1 NAME_BOUND_TO_PINNED_OBJECT=1
BLOCK=08 EXEC_CHANNEL=NAMELESS_STDIN ARGV_PATH_SEPARATORS=0 EXEC_BUFFER_IS_PINNED_READ=1 EXEC_SHA256=709c6da5d8e44a08a6060a155d10620c8849a19ea16cdaf5df354a43a083ab20
BLOCK=08 RC=0 STDERR_BYTES=0 POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1 STATUS_OK PUBLISHED_LINES=7 MISSING_FROM_REAL_OUTPUT=0 OK $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=09 FENCE_BYTES=3891 SCRIPT_BYTES=3891 LF=87 CRLF=0 NONASCII=0 SCRIPT_BYTES_IDENTICAL=1 SHA256=edd0e16393948dfc1fc7c483220c251197d277788bf305812ba58f629f36787f
BLOCK=09 PIN_HELD=1 READ_THROUGH_PIN=1 WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32 LEAF_ON_PINNED_CHAIN=1 NAME_BOUND_TO_PINNED_OBJECT=1
BLOCK=09 EXEC_CHANNEL=NAMELESS_STDIN ARGV_PATH_SEPARATORS=0 EXEC_BUFFER_IS_PINNED_READ=1 EXEC_SHA256=edd0e16393948dfc1fc7c483220c251197d277788bf305812ba58f629f36787f
BLOCK=09 RC=0 STDERR_BYTES=0 POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1 STATUS_OK PUBLISHED_LINES=19 MISSING_FROM_REAL_OUTPUT=0 OK $base='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1'
BLOCK=10 FENCE_BYTES=886 SCRIPT_BYTES=886 LF=18 CRLF=0 NONASCII=0 SCRIPT_BYTES_IDENTICAL=1 SHA256=c7882cd7892fd28d4fefef09b4ba19f7c3156283ce5a64f71828f00ac8e95272
BLOCK=10 PIN_HELD=1 READ_THROUGH_PIN=1 WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32 LEAF_ON_PINNED_CHAIN=1 NAME_BOUND_TO_PINNED_OBJECT=1
BLOCK=10 EXEC_CHANNEL=NAMELESS_STDIN ARGV_PATH_SEPARATORS=0 EXEC_BUFFER_IS_PINNED_READ=1 EXEC_SHA256=c7882cd7892fd28d4fefef09b4ba19f7c3156283ce5a64f71828f00ac8e95272
BLOCK=10 RC=0 STDERR_BYTES=0 POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1 STATUS_OK PUBLISHED_LINES=21 MISSING_FROM_REAL_OUTPUT=0 OK $base='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1'
BLOCK=11 FENCE_BYTES=34053 SCRIPT_BYTES=34053 LF=621 CRLF=0 NONASCII=0 SCRIPT_BYTES_IDENTICAL=1 SHA256=1b2ca5bc66aa0505c6b3e4951a80a1faf70f73ac8de93c99430b53abbe0db6b4
BLOCK=11 PIN_HELD=1 READ_THROUGH_PIN=1 WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32 LEAF_ON_PINNED_CHAIN=1 NAME_BOUND_TO_PINNED_OBJECT=1
BLOCK=11 EXEC_CHANNEL=NAMELESS_STDIN ARGV_PATH_SEPARATORS=0 EXEC_BUFFER_IS_PINNED_READ=1 EXEC_SHA256=1b2ca5bc66aa0505c6b3e4951a80a1faf70f73ac8de93c99430b53abbe0db6b4
BLOCK=11 RC=0 STDERR_BYTES=0 POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1 STATUS_OK PUBLISHED_LINES=44 MISSING_FROM_REAL_OUTPUT=0 OK $base='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1'
BLOCKS=11 SCRIPT_BYTES_IDENTICAL_ALL=11 PINNED_ALL=11 LEAF_ON_CHAIN_ALL=11 NAME_BOUND_ALL=11 NAMELESS_EXEC_ALL=11 POST_NAME_BOUND_ALL=11 POST_BYTES_UNCHANGED_ALL=11 REJECTED_ON_BYTES=0 REJECTED_ON_BINDING=0 STATUS_PROVED_COMPLETE=11 REJECTED_ON_STATUS=0 REJECTED_ON_STDERR=0 COMPARED=11 MISMATCHED=0 REJECTED=0 CWD=C:\Users\BARSEM~1\AppData\Local\Temp\claude\C--LAB-Tradingview-LAB-CLEAN\6e4c4dff-61c3-4a9a-b874-f1b6a251ff44\scratchpad\r11\outside
```

Every one of the eleven children was handed the bytes of an object that was **pinned before it was
verified** (`PINNED_ALL=11`), proved byte-identical to its fence through that pin
(`SCRIPT_BYTES_IDENTICAL_ALL=11`, `REJECTED_ON_BYTES=0`), reached relative to the pinned directory
handle on one coherent chain (`LEAF_ON_CHAIN_ALL=11`, `CHAIN_COHERENT=1`), and executed **from that
same buffer with no pathname anywhere in the child's argument vector**
(`NAMELESS_EXEC_ALL=11`, `ARGV_PATH_SEPARATORS=0` and `EXEC_BUFFER_IS_PINNED_READ=1` per block, with
`EXEC_SHA256` equal to the digest of the bytes read through the pin). Each returned process status
`0` with **zero** stderr bytes, and only then had its output compared. The conserved round-10 gates
all held (`NAME_BOUND_ALL=11`, `POST_NAME_BOUND_ALL=11`, `POST_BYTES_UNCHANGED_ALL=11`,
`REJECTED_ON_BINDING=0`) — under round 11 they could only have rejected. `WRITE_OPEN_DENIED=1
DELETE_OPEN_DENIED=1 WINERROR=32/32` on every block is Windows refusing, once per block, the two
opens that could have rewritten the script. `NONASCII=0` on every block, so nothing above turns on
how the interpreter decodes a non-ASCII byte. The `LF`/`CRLF` columns are the composition of this
file as it exists on the disk this transcript was produced on — a checkout that rewrote them would
print different numbers and different digests rather than passing silently.

### 13e. The outer wrapper's own status

A wrapper cannot be the sole witness to its own completion. The outer process status and stderr byte
count below were measured by the shell that launched it, not by the wrapper itself:

```text
OUTER_WRAPPER_RC=0
OUTER_WRAPPER_STDERR_BYTES=0
```

The section-13d transcript above was re-derived on the **final** bytes of this file, after the last
prose edit, and is byte-identical to the run published there. What is *not* claimed: that the eleven
children could not have done something this document failed to ask about, that the bytes proved here
are the bytes a fresh clone would materialise (section 11, round-9 statement 1, carried), or that
the *program* which received them is the PowerShell this host normally runs (section 11, round-11
statement 2 — an out-of-model disclosure, not a detected control). Round 11 proves each child was
handed this page's bytes and no name, and that it ran to completion before its output was believed —
nothing more, and the round-10 findings are that "was handed this page's bytes" had never previously
been established without a resolution step that a same-session actor could move.
