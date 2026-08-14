# PATHSCOPE — cap-override repair report (round 4, C-2)

Date: 2026-08-13
Role: counterpart flagship **IMPLEMENTER**, fresh session. Model `claude-opus-5`, effort
**high** (T1).
Authorization: the single owner-authorized Pathscope T1 cap override recorded in
`WPI_OWNER_DECISIONS_2026-08-13.md` §4 ("I authorize both additional audit-cap overrides").
Working directory: `C:\LAB\Tradingview_LAB_CLEAN`, current committed bytes. No Git stash was
applied or inspected. No sub-delegation. No git mutation. No host, network, credential,
deployment, broker, Pine, parity, MTC or trading surface was touched.

**This report claims no acceptance.** It is the implementer's Gate 3–4 record for a fresh
T1 execution re-audit by a flagship that is neither `claude-opus-5` nor GLM-5.2.

## 0. Files owned and changed

| file | state |
|---|---|
| `pathscope_prover.py` | modified |
| `SELF_QA_PATHSCOPE.md` | modified |
| `STATUS_PATHSCOPE.md` | modified |
| `PATHSCOPE_CAP_OVERRIDE_REPAIR_REPORT_2026-08-13.md` | new (this file) |

All four under `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/`. Nothing else was
written inside the repository. All scratch artefacts live under `%TEMP%` and `C:\tmp\ps_c2`.

| artefact | bytes | SHA-256 |
|---|---:|---|
| `pathscope_prover.py` round 3 — the pre-repair subject, git blob `e600a107f2e2a790653cc544a94cd7436b7b070a` | 124251 | `0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7` |
| `pathscope_prover.py` round 4 — this repair | 131599 | `553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB` |
| harness extracted verbatim from `SELF_QA_PATHSCOPE.md` | 20110 | `27008BB5AAB4950935A235445C64EC0E1F91F3146CC5146D3A11063E4959BB63` (346 lines, 0 non-ASCII bytes) |

## 1. What C-2 actually was

`PATHSCOPE_CODEX_T1_EXEC_AUDIT_R3_2026-08-13.md` §3 located the cause at
`pathscope_prover.py:1265-1267` of the round-3 bytes:

```python
rendered = value.text or ""
if rendered.startswith(("/", "./", "../")):
    self.record_path_text(...)
```

Two distinct defects live in those three lines:

1. **No `else`.** A statically known value whose first character is not `/`, `.` is treated
   as non-path data with no PATH row and no coverage row. Bare-first loader lists, ordinary
   relative pathnames, command text and URI values all vanished.
2. **No member parsing even on the taken branch.** A value that *did* start with `/` was
   recorded only as one whole blob, so `/safe/lib:/etc/escape` matched `/safe/**` and
   returned `PASS rc=0` with `/etc/escape` never tested. This is why the kickoff states
   "member parsing must therefore run even when the rendered value starts with `/`".

A third defect belongs to the *incomplete first repair attempt* that the Lead rejected: it
applied Python `str.split()` to the already-rendered value, which turns the single quoted
pathname `/safe dir/escape` into `/safe` + `/safe/dir/escape`, both allowlisted — a false
PASS created by the repair itself.

## 2. The repair

`record_assignment_value` now resolves the value and hands it to a new
`record_assignment_members`, which gives every component a terminal disposition. The
decision procedure is stated in `SELF_QA_PATHSCOPE.md` §"The rule, stated so it can be
attacked"; in short:

1. **URI first.** `^[A-Za-z][A-Za-z0-9+.-]*://` routes to the **endpoint** domain via
   `record_network_text` and is never colon-split. This answers the kickoff's
   "URI/endpoint-shaped assignment values must not be misclassified as one filesystem path".
2. **Whitespace is never a shell separator here.** The lexer already guarantees an
   assignment word contains no *unquoted* whitespace, and the shell does not word-split
   assignment values. So `X="$ROOT dir/escape"` stays exactly one pathname — the repair does
   **not** split on quoted or escaped whitespace, as required. A *consumer* may still read
   the same bytes as a word list, so that reading is treated as live — one specific coverage
   record plus a row for every path-carrying word — when some word contains `/` **and**
   (some word is option-shaped, or a word after the first is absolute, or the first word is
   not path-shaped). A value in which no word contains `/` carries no pathname under any
   reading and stays benign.
3. **Colon members always.** Applied to every candidate, including one starting with `/`.
   The whole candidate is kept alongside its members, so neither the single-pathname reading
   nor any member can disappear. This is a union of readings, deliberately, so that no
   interpretation's sink is silent.
4. **Empty member fails closed only in a path list.** An empty member gets a coverage record
   only when the same value also carries a path member. `IFS=:` therefore stays benign
   because of its grammar — it has no path member — not because of its name. This answers
   "fail closed on any ambiguous empty member without making benign scalar `IFS=:` a
   name-based special case".
5. **Terminal disposition for every member:** endpoint, path, empty, or `bare`.

Two smaller closures ride with it:

* A **quoted** assignment word at the `env` site (`env "LD_PRELOAD=/etc/evil.so" cat …`)
  used to `return` silently because `ASSIGN_RE` was matched against the raw token. It is now
  recovered from the expanded word, or gets a specific coverage record. Fixture
  `c2_env_quoted`: rc 0 → rc 1.
* **NIT-1** from §5 of the r3 verdict: network allows printed bare `ALLOW` while filesystem
  allows printed `ALLOW-LEXICAL`, implying a stronger guarantee for endpoints. Both now read
  `ALLOW-LEXICAL`.

**No variable-name allowlist was introduced.** There is no set of names anywhere in the new
code; every branch keys on the grammar of the value. Measured:
`grep -n "LD_PRELOAD\|LD_LIBRARY_PATH\|BASH_ENV\|PYTHONPATH\|PERL5LIB\|GIT_SSH_COMMAND"
pathscope_prover.py` returns exactly four hits — lines 1250, 1251, 1253 and 1283 — all of
them comment prose inside `record_assignment_value`.

### All three sites

Prefix (`pathscope_prover.py:2452`), declaration builtins including `export` (`:2462`), and
the `env` wrapper (`:1676`) all call the same `record_assignment_value` (defined at `:1248`,
delegating to `record_assignment_members`), so the member grammar reaches all
three by construction. It is also demonstrated by measurement — `c2_list_prefix`,
`c2_list_env`, `c2_list_export` are the same value shape at the three different sites and
all three move rc 0 → rc 1.

## 3. D026 evidence — the RED column is executed pre-repair bytes

The harness now reconstructs **three** provers from pinned blobs and runs the eighteen new
C-2 fixtures against the round-3 committed blob as well, writing `RED_R3.txt`. No prediction
appears in the round-4 evidence: `SELF_QA_PATHSCOPE.md` §"Round 4" carries measured rc values
in every cell, and §"Complete pre-repair transcript for family P10" carries `RED_R3.txt` in
full.

Summary of the eighteen fixtures (full table and transcripts in the self-QA):

* **12 closures** — `PASS rc=0` on round-3 bytes with the sink lexeme absent → rc 1 or rc 3
  on round-4 bytes with the sink printed: `c2_list_prefix`, `c2_list_env`, `c2_list_export`,
  `c2_list_bare_first`, `c2_list_space`, `c2_relative`, `c2_empty_member`,
  `c2_escaped_space`, `c2_command_text`, `c2_uri_forbid`, `c2_env_quoted`,
  `c2_words_with_path`.
* **5 controls** that must not move and do not: `c2_uri_allow`, `c2_bare_soname`,
  `c2_allow_list`, `c2_benign_scalars`, `c2_benign_words`. Two of them now additionally
  print the ALLOW-LEXICAL rows round 3 dropped, which is the same defect seen from the
  allowed side.
* **1 regression guard**, `c2_quoted_space` — `X="$ROOT dir/escape" cat "$ROOT/f"` — rc 1
  before and rc 1 after, one FORBID row for `/safe dir/escape`. It is the Lead's reproduced
  case, and its RED side cannot be the round-3 blob (round 3 got it right); it is falsified
  by mutation instead.

### Mutations (D026 falsification of the round-4 source itself)

Copies outside the repository at `C:\tmp\ps_c2\MUT_*.py`, one line changed each:

| mutation | change | measured |
|---|---|---|
| **MUT-A** naive word split | `candidates = [rendered]` → `candidates = words if words else [rendered]` | `c2_quoted_space` **rc 1 → rc 0**, two ALLOW-LEXICAL rows (`/safe`, `/safe/dir/escape`), no FORBID — the exact false PASS the Lead reproduced |
| **MUT-B** no colon members | member-loop guard → `if False:` | `c2_list_prefix` **rc 1 → rc 0**, `c2_escaped_space` **rc 1 → rc 0**, `c2_empty_member` **rc 3 → rc 0** |
| **MUT-C** no word-list reading | `if word_list_reading:` → `if False:` | `c2_command_text` / `c2_list_space` keep rc 3 but `/etc/key` and `/etc/escape.so` **disappear from the report**, replaced by a bogus allowlisted relative path. Sink visibility, not rc, is what this falsifies — stated plainly rather than dressed up as an rc flip. |

## 4. Executed commands and real output

### 4.1 Syntax / AST

```
$ python -c "import ast,pathlib;p='MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py';s=pathlib.Path(p).read_text(encoding='utf-8');ast.parse(s);ast.parse(s,feature_version=(3,12));print('AST OK')"
AST OK
```

CPython 3.14.2. `py -3.12 -V` reports no installed 3.12 runtime, so the 3.12 claim is a
`feature_version` parse claim only — that limit is now cited in the self-QA rather than
asserted bare (U-3 nit).

### 4.2 Harness extracted verbatim from the document

```
$ python - <<'PY'   # reads the fenced body under "### The harness, verbatim", no retyping
...
harness bytes 20110 lines 346 nonascii 0
harness sha256 27008BB5AAB4950935A235445C64EC0E1F91F3146CC5146D3A11063E4959BB63
```

### 4.3 The published command, run from the repository root

```
PS> Remove-Item -Recurse -Force "$env:TEMP\pathscope-repair-r2"
PS> powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\pathscope_r4_verify.ps1" > "$env:TEMP\ps_verify_stdout.txt" 2> "$env:TEMP\ps_verify_stderr.txt"
outer_rc=0
stderr_bytes=0
R1_BASELINE bytes=49820 sha256=3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6
R3_PREREPAIR bytes=124251 sha256=0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7
R2_REPAIRED bytes=131599 sha256=553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB
BLOCK RP6-P0.sh bytes=107252 sha256=A090AE736CBECD9973E8AE948B052504B21CBE8B61602F4B5AC592394FAD0617 git_blob=3c7b7d26a763f3904ea4fa4c0be3d39dc598c64c
BLOCK RP7-WPI-RO.sh bytes=99903 sha256=11621044D0ADC21AF93E1CFC7B88EF88DE8ACA4683A69AB16CBC542A124141A4 git_blob=5c9a2f597cceaef80d1cbd0fc100732f4b216cf5
WROTE C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-repair-r2\RED_R1.txt lines=660
WROTE C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-repair-r2\GREEN_R2.txt lines=1363
WROTE C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-repair-r2\RED_R3.txt lines=150
DETERMINISM find_exec rc1=1 rc2=1 equal=True sha1=11c5cb8e39a2e9061e8c1d159817794b75b3ec2479649b146176f699d28067dd sha2=11c5cb8e39a2e9061e8c1d159817794b75b3ec2479649b146176f699d28067dd
DETERMINISM assign_prefix rc1=1 rc2=1 equal=True sha1=32da284224350fdb4a236c4d2238aad2f718b8b48cd89f04cf3fd1b57c30317a sha2=32da284224350fdb4a236c4d2238aad2f718b8b48cd89f04cf3fd1b57c30317a
DETERMINISM c2_list_prefix rc1=1 rc2=1 equal=True sha1=40e458dc11a9040bb4208e93097f19a3b5a9fd46c0d2043515ceb6ce3188bf62 sha2=40e458dc11a9040bb4208e93097f19a3b5a9fd46c0d2043515ceb6ce3188bf62
DETERMINISM RP6-P0 rc1=3 rc2=3 equal=True sha1=2e9d6f4465fcd4a6ee0cee9edfe6fc883725ef3b6dd8f6fa9eb97dec1fa605db sha2=2e9d6f4465fcd4a6ee0cee9edfe6fc883725ef3b6dd8f6fa9eb97dec1fa605db
DETERMINISM RP7-WPI-RO rc1=3 rc2=3 equal=True sha1=224cda7292d5e1b60f77b558e4b986d1ed39defdaa843f3a09e60a0625bb2ad2 sha2=224cda7292d5e1b60f77b558e4b986d1ed39defdaa843f3a09e60a0625bb2ad2
```

The fixture directory was deleted before this run, so nothing was inherited from an earlier
one. Determinism: five pairs, all `equal=True` with identical digests.

### 4.4 Every embedded identity, count, transcript and digest reproduces exactly

```
harness stdout         exact_match=True doc_lines=13   file_lines=13
RED_R1 transcript      exact_match=True doc_lines=660  file_lines=660
GREEN transcript       exact_match=True doc_lines=1363 file_lines=1363
RED_R3 transcript      exact_match=True doc_lines=150  file_lines=150
prover bytes=131599 sha256=553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB
identity row present in doc: True
ALL EXACT: True
```

This is a string comparison of the fenced document bodies against the files the fresh run
produced, not a summary. It closes the evidence mismatch the Lead recorded against the
abandoned first attempt (`PATHSCOPE_CAP_OVERRIDE_LEAD_FINDING_2026-08-13.md`
§"Evidence mismatch to correct"): the digest recorded in the self-QA is the digest the
harness generates.

### 4.5 Regression sweep — round-3 blob versus round-4 source, byte for byte

Each of the 87 fixture cases plus the two real blocks was run under both provers and the
complete stdout compared:

```
fixture cases 87 changed r3->r4: 17
  curl_upload            r3_rc=1 r4_rc=1      (NIT-1 label only)
  curl_net               r3_rc=0 r4_rc=0      (NIT-1 label only)
  devtcp_allow           r3_rc=3 r4_rc=3      (NIT-1 label only)
  c2_list_prefix         r3_rc=0 r4_rc=1
  c2_list_env            r3_rc=0 r4_rc=1
  c2_list_export         r3_rc=0 r4_rc=1
  c2_list_bare_first     r3_rc=0 r4_rc=1
  c2_list_space          r3_rc=0 r4_rc=3
  c2_relative            r3_rc=0 r4_rc=1
  c2_empty_member        r3_rc=0 r4_rc=3
  c2_escaped_space       r3_rc=0 r4_rc=1
  c2_command_text        r3_rc=0 r4_rc=3
  c2_uri_forbid          r3_rc=0 r4_rc=1
  c2_uri_allow           r3_rc=0 r4_rc=0      (control; rows added, rc held)
  c2_env_quoted          r3_rc=0 r4_rc=1
  c2_allow_list          r3_rc=0 r4_rc=0      (control; rows added, rc held)
  c2_words_with_path     r3_rc=0 r4_rc=3
  RP6-P0                 r3_rc=3 r4_rc=3 identical=True
  RP7-WPI-RO             r3_rc=3 r4_rc=3 identical=False
```

The other 70 cases are byte-identical. In particular **all seven round-3 P9 assignment
fixtures are byte-identical**, so the C-1 closure is preserved rather than re-derived.

`RP7-WPI-RO`'s single difference, isolated by sorted `comm` of the UNRESOLVED lines:

```
new in round 4: UNRESOLVED line=681 kind=coverage reason=assignment value is a
                whitespace-separated word list ... expression=seen_roots="$seen_roots$r "
gone in round 4: (none)
coverage_issue_count 336 -> 337; every other count unchanged; rc 3 unchanged
```

`RP6-P0` is byte-identical to round 3. That is the measured form of the premise behind owner
decision §1 — the audited RP6 block contains none of the surviving assignment forms.

### 4.6 Adversarial probes beyond the harness

Run against the repaired bytes with the same `/safe/**` allowlist; all fail closed:

| probe | rc | terminal disposition |
|---|---:|---|
| `X=/safe/* cat "$ROOT/f"` | 3 | `unresolved_path`: glob makes the path set dynamic |
| `declare -x LD_PRELOAD=/etc/evil.so` | 1 | `/etc/evil.so` FORBID |
| `f() { local LD_PRELOAD=/etc/evil.so; …; }` | 1 | `/etc/evil.so` FORBID |
| `env env LD_PRELOAD=/etc/evil.so cat "$ROOT/f"` | 1 | `/etc/evil.so` FORBID |
| `X=~/secret cat "$ROOT/f"` | 3 | coverage: HOME is not a pinned absolute constant |
| `X=$UNPINNED:/etc/escape cat "$ROOT/f"` | 3 | coverage: unpinned variable |
| `LD_PRELOAD=./rel.so cat "$ROOT/f"` | 3 | provenance: allowlisted path has no constant provenance |
| `LD_PRELOAD=../../etc/escape.so cat "$ROOT/f"` | 1 | `/etc/escape.so` FORBID |
| `LD_LIBRARY_PATH=/etc/escape: cat "$ROOT/f"` | 3 | `/etc/escape` FORBID + `/etc/escape:` FORBID + empty-member coverage |
| `IFS=:: cat "$ROOT/f"` | 0 | no assignment row (all members empty, no path member) |
| `WEBHOOK=ftp://h/x cat "$ROOT/f"` | 3 | `unresolved_endpoint`: no static port |
| `X= cat "$ROOT/f"` | 0 | no assignment row |

### 4.7 Whitespace / hygiene

```
$ git diff --check -- <the three tracked owned files>
(no output; rc 0)
$ git status --porcelain -- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/
 M .../SELF_QA_PATHSCOPE.md
 M .../STATUS_PATHSCOPE.md
 M .../pathscope_prover.py
(plus pre-existing untracked *.log files not written by this session)
```

`git diff --check` emits only the standing advisory that `SELF_QA_PATHSCOPE.md` is `text=auto`
and would be checked out CRLF on Windows; the working copy and the index are both LF, as
before this session. No trailing-whitespace or conflict-marker finding.

## 5. Disclosed residuals — stated narrowly this time

The round-3 disclosure ("bare sonames such as `LD_PRELOAD=libc.so`") was judged *materially
incomplete* by the r3 verdict §4 because it hid mixed lists and relative pathnames. Those are
now caught. What remains:

1. **A member containing no `/`** — a bare soname, a scalar, a tool name, an option word — is
   resolved by the consumer's own search rules, is not an argv pathname, and carries no row.
   `c2_bare_soname` pins this behaviour.
2. **The union of readings is conservative, not exact.** `MSG="denied /etc/secret"` is
   rejected although no consumer opens that path there. A fail-closed prover may over-reject;
   it may not under-report. `c2_words_with_path` pins this deliberately, and
   `c2_benign_words` pins the boundary that keeps ordinary prose values benign.
3. **A whole-value row such as `/safe/lib:/etc/escape` ALLOW-LEXICAL never stands alone** —
   the same run prints `/etc/escape` FORBID and rejects. It is the single-pathname reading of
   an ambiguous value, recorded so that reading cannot silently disappear.
4. **Unchanged from earlier rounds:** the claim is lexical argv scope. `symlink_resolution`
   and `mount_boundary` remain `not_established`; no host probe is performed.

## 6. Scope and safety statement

* Only the four listed files were written. No other repository path was created or modified.
* No git command mutated repository state; nothing was staged, committed, stashed, or
  checked out. No Git stash was applied or inspected at any point.
* No sub-agent, CLI implementer, or second model was invoked.
* No shell fixture was executed as shell; the static Python reader consumed fixture text
  only. Harness, mutation copies, and probe scratch stayed under `%TEMP%` and `C:\tmp\ps_c2`.
* No host contact, no network call, no credential, no deployment, no ARM, no broker or
  exchange action.

## 7. What the re-auditor should attack first

1. **The union-of-readings model.** Is recording both the whole value and its members
   genuinely fail-closed for every shape, or is there a value where the whole-value row is
   allowlisted and the true sink is neither a colon member nor a whitespace word?
2. **The `any("/" in word)` gate on the word-list reading.** It exists to keep prose values
   benign. Construct a value where a consumer opens a path that no word spells with `/`.
3. **`assignment_member_kind`'s relative-path rule** (`"/" in text and ":" not in text and
   not text.startswith("-")`). The `":" not in text` clause exists so `:/etc/escape` is
   handled by its members rather than as a bogus relative path; check it does not also skip
   a genuine relative pathname that legitimately contains a colon.
4. **The empty-member rule's `path_member` precondition.** Confirm it cannot be defeated by a
   value whose only path member is itself dropped for another reason.
5. **The three sites.** Confirm by execution, not by reading, that prefix, `env` and
   declaration-builtin assignments all reach the member grammar, including quoted forms.

Session model/effort: `claude-opus-5` / **high** (T1). Verdict authority is the Lead's; this
document asserts none.
