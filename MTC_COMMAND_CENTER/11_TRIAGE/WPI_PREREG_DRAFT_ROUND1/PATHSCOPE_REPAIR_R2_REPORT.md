# Path-scope prover — repair round 2 report

Date: 2026-08-11
Implementer: `claude-opus-5`, effort xhigh, Max account. Codex is the auditor of record and
did not write these bytes.
Working directory: `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.
Neither block, the preregistration draft, nor `verify_lock.py` was modified.

Binding input: `PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md`, `REQUEST_CHANGES: 9`.
Executed evidence: `SELF_QA_PATHSCOPE.md` — one harness command produces the complete RED
transcript against the round-1 bytes and the complete GREEN transcript against these bytes.

| artefact | bytes | SHA-256 |
|---|---|---|
| round 1 (`3f0820a9…`) | 49820 | `3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6` |
| round 2 (this repair) | 122446 | `890016F0B9A8CDE4EED33F8733F69055471B07C6096F6BC07450457E6C52AF1D` |

Source locations below are given as **content anchors** — a literal string to search for —
not line ranges, because line ranges do not survive the next edit.

## The governing change

Round 1 had two open classes of command word: a registry of known sinks, and a
`NO_PATH_COMMANDS`/`CONTROL` shortcut that returned before looking at operands. Anything
that fell into the shortcut, and any option form the registry did not pattern-match, was
discarded in silence.

Round 2 replaces both with one explicit grammar registry. Anchor: `class Spec:` with the
docstring *"Every accepted option is listed with the role of its value. An option that is
not listed is a coverage STOP, never a silent skip"*. Each registered command declares its
flags and, for every option that takes a value, that value's role — `path`, `net`, `shell`,
`fd`, `form`, `data` (proved path-independent), `odata`, or `unmodeled`. Positional
operands get roles the same way. The scanner (`def scan_args`) classifies **every** token:
there is no branch that drops one. Anything not in the registry is an opaque sink and
STOPs (`opaque command {command} has no registered argv grammar`).

One command may stay silent about an operand it cannot expand: one whose every accepted
form is path-free. That is a declared property, not an assumption — anchor:
`def path_free`, *"True when no accepted form of this command can carry a path"*. It is
false the moment a command declares any path, net, shell, fd, form or unmodeled option, or
any non-`data` operand role.

## Finding-by-finding disposition

### 1. CRITICAL — `NO_PATH_COMMANDS`/control shortcut discards real sinks — REPAIRED

`NO_PATH_COMMANDS` no longer exists. `pushd` takes a path operand (anchor:
`spec("pushd", flags="-n", option_re=r"[+-][0-9]+", rest="path")`) with `+N`/`-N` handled
as stack indices, not paths. A trap action is shell source and is recursively analysed
(anchor: `def analyze_trap`, which ends in `self.analyze_shell_source(text, ...)`).

Evidence — `SELF_QA_PATHSCOPE.md` fixtures `pushd`, `pushd_forbidden`, `popd_stack`, `trap`:

```text
pushd            R1 rc 0, no row          → R2 rc 0, PATH /safe ALLOW-LEXICAL uses=line=2:pushd
pushd_forbidden  R1 rc 0, no row          → R2 rc 1, PATH /etc FORBID
trap             R1 rc 0, no row          → R2 rc 1, PATH /etc/passwd FORBID uses=line=2:cat
popd_stack       R1 rc 0                  → R2 rc 0 (`+1` is a stack index, correctly not a path)
```

**Extension — same class, found while repairing, not in the audit's nine.** Five more
complete fragments returned `PASS rc=0` with no path and no marker on the round-1 bytes.
They are fixed by the same registry and each has its own RED/GREEN pair:

| fixture | fragment | R1 | R2 |
|---|---|---|---|
| `python_c` | `python3 -c 'open("/etc/passwd")'` | rc 0, no row | rc 3, `python3 -c program text is opaque…` |
| `alias` | `alias ll='cat /etc/passwd'` | rc 0, no row | rc 1, `/etc/passwd` FORBID |
| `hash_p` | `hash -p /etc/passwd ff` | rc 0, no row | rc 1, `/etc/passwd` FORBID |
| `mapfile_cb` | `mapfile -C 'cat /etc/passwd' -c 1 arr` | rc 0, no row | rc 1, `/etc/passwd` FORBID |
| `systemctl_link` | `systemctl link /etc/systemd/system/evil.service` | rc 0, no row | rc 3, verb not in the modeled read-only set |
| `jobs_x` | `jobs -x cat /etc/passwd` | rc 0, no row | rc 3, `jobs option -x changes the operand grammar…` |

`jobs_x` was found by re-reading the `path_free` set against bash's manual rather than by a
fixture: `jobs -x` substitutes job specs into a command **and runs it**, so `jobs` is not a
path-free builtin. It is listed here as a finding of this round, with the RED/GREEN pair
that any other member of the class gets.

`python3 -c` mattered most: round 1 registered interpreters as sinks and captured
*post-code* argv while treating the inline program itself as invisible. Inline interpreter
text can open anything, so it is now a coverage STOP (anchor: `def analyze_interpreter`).

### 2. CRITICAL — ordinary SSH and NSS host grammar disappears — REPAIRED

`ssh` has a complete destination grammar with the implicit port 22, `-p`, and `-o Port=`
(anchor: `def analyze_ssh`). Options that carry a path (`-i`, `-F`, `-S`, `-E`) are
recorded as paths. Forwarding and bind options (`-L -R -D -W -J -b -B -e -w -I`) are an
explicit rc-3 endpoint STOP rather than a guess. `-o` is adjudicated against a named inert
set (anchor: `SSH_INERT_OPTIONS`); anything else STOPs, because `ProxyCommand`,
`IdentityFile`, `ControlPath` and `UserKnownHostsFile` all reach a path or a program. A
remote command vector STOPs with *"ssh remote command text executes on the remote host and
is outside the local static path domain"* — the same class the transport audit recorded as
pattern 11.

`getent` is adjudicated explicitly and **no form is asserted path/network-free** (anchor:
`def analyze_getent`). Every database resolves through NSS, whose backing service set
(files, DNS, LDAP, NIS, systemd-resolved) is host configuration a static reader cannot see,
so every invocation is an rc-3 unresolved endpoint naming the database.

`scp`/`sftp` now record the peer endpoint and every local path operand, and STOP on the
remote path because §10.1 describes the staging host, not the peer. `nc`/`ncat`/`netcat`
have a two-operand client grammar; the listener grammar is a declared coverage STOP.

Evidence — fixtures `ssh`, `ssh_command`, `getent`, `scp_remote`, `nc_client`:

```text
ssh          R1 rc 0, no row → R2 rc 1, ENDPOINT 198.51.100.10:22 FORBID sources=HOST
ssh_command  R1 rc 0, no row → R2 rc 3, ENDPOINT 198.51.100.10:2222 FORBID + remote-text STOP
getent       R1 rc 0, no row → R2 rc 3, kind=unresolved_endpoint naming the `hosts` database
scp_remote   R1 rc 3         → R2 rc 3 with the endpoint and the local path now reported
nc_client    R1 rc 0, no row → R2 rc 1, ENDPOINT 198.51.100.10:8790 FORBID
```

### 3. CRITICAL — `find -exec` hides a nested forbidden primitive — REPAIRED

The whole `find` expression is parsed (anchor: `def analyze_find`). Global options, search
roots, and then every predicate: data predicates, path-valued predicates (`-newer`,
`-anewer`, `-cnewer`, `-samefile`, `-fprint`, `-fprint0`, `-fls`, `-fprintf`,
`-files0-from`, `-newerXY`), and the four command-vector actions (anchor:
`FIND_EXEC = {"-exec", "-execdir", "-ok", "-okdir"}`) whose vector is collected to its `;`
or `+` terminator and recursively analysed as a command. An operand containing `{}` is an
explicit unresolved-path record, because it stands for each found pathname. **A predicate
the tool does not model is rc 3**, not a scan that stops quietly.

Evidence — fixtures `find_exec`, `find_unknown`:

```text
find_exec    R1 rc 0, only /safe ALLOW → R2 rc 1, /etc/passwd FORBID uses=line=2:cat plus /safe
find_unknown R1 rc 0                   → R2 rc 3, `find has no modeled grammar for the predicate …`
```

### 4. CRITICAL — `--option=PATH` discarded by registered sink adapters — REPAIRED

`nonoption_operands()` is gone. `scan_args` handles `--name value`, `--name=value` and
short clusters (`-ofile`, `-o file`, `-czf archive`) uniformly, and dispatches the value by
its declared role. An option a registered sink does not declare is an rc-3 coverage record
naming the option.

Evidence — fixtures `curl_upload`, `tar_option`, `cp_option`, `cp_unknown`:

```text
curl_upload R1 rc 0, endpoint only → R2 rc 1, /etc/passwd FORBID + endpoint ALLOW
tar_option  R1 rc 0, /safe only    → R2 rc 1, /etc/pathscope-evil.tar FORBID + /safe
cp_option   R1 rc 0, /safe/input   → R2 rc 1, /etc FORBID + /safe/input
cp_unknown  R1 rc 0                → R2 rc 3, `cp has no modeled grammar for option --pathscope-unmodeled`
```

`curl`'s `-d`/`--data*`/`-F` values are adjudicated for the `@file` and `=@file` forms
(anchor: `def record_form_value`), and `-O`/`-J` are declared `unmodeled` because they
derive the output name from the URL.

### 5. HIGH — tilde reported as resolved-and-allowed — REPAIRED

Bash tilde rules are implemented from pinned inputs, and the invented `PWD/~/...` path is
gone. Anchor: `"tilde expansion depends on HOME, which is not a pinned "`.
`~/…` expands from a pinned absolute `HOME` and carries `HOME` as provenance; with no such
constant it is an unresolved path, never an `ALLOW` row. `~user`, `~+`, `~-` and `~N` are
unresolved by name. A tilde after `:` in a word is also unresolved rather than literal.

Evidence — fixtures `tilde`, `tilde_user`, `tilde_home`:

```text
tilde       R1 rc 3 WITH the false row `PATH value=/safe/~/secret verdict=ALLOW`
            → R2 rc 3, no path row, `tilde expansion depends on HOME…`
tilde_user  R1 rc 3 with the false row `/safe/~gatea/secret`
            → R2 rc 3, `tilde expansion ~gatea names a home directory that is not statically known`
tilde_home  (HOME=/home/gatea pinned) R1 rc 3 with the false row `/safe/~/secret`
            → R2 rc 1, PATH /home/gatea/secret FORBID sources=HOME
```

The third fixture is the one that proves the rule is *implemented* rather than merely
refused: with a pinned `HOME` the tool produces the path bash would produce, and forbids it.

### 6. HIGH — lexical membership presented as unconditional host-path ALLOW — REPAIRED AS DISCLOSURE (see residual R1)

The claim sentence was narrowed to what the predicate establishes, and the narrowing is
machine-readable. Every run prints (anchor: `SEMANTICS_LINE`):

```text
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
```

The allow token for a filesystem path is now `ALLOW-LEXICAL`, and a clean run reports
`reason=closed_and_allowlisted_lexical_argv_scope`. The module docstring states the same
limit in prose and says the symlink/mount-chain proof is neither attempted nor claimed.
`STATUS_PATHSCOPE.md` repeats it.

Evidence — fixture `symlink_lexical` (`cat "$ROOT/link/passwd"`):

```text
R1: PATH value=/safe/link/passwd verdict=ALLOW ... PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
R2: PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
    PATH value=/safe/link/passwd verdict=ALLOW-LEXICAL ...
    PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
```

This is the disclosure half of the audit's required repair. The other half — binding the
lexical result to a symlink/mount-chain proof — is **not** in this tool and is recorded as
residual R1 below. A static reader of frozen bytes cannot perform it, and inventing a host
probe here would be exactly the defect the §10.2 contract forbids.

### 7. HIGH — `<>` not tokenised, real target disappears — REPAIRED

`<>` is in the operator table ahead of `<` and `>`, and in the redirection set with its own
primitive label (anchor: the operator tuple line `"<<", ">>", "<>", ">|", "&&", "||",`).
`>|` was found to have the same defect and is fixed with it. The full redirection set now
modelled: `< > >> <> >| &> &>> >& <& <<< << <<-`, plus numeric and `{name}` descriptor
prefixes and `>&-`/`<&-` closes.

Evidence — fixtures `redir_rw`, `redir_clobber`, `redir_amp`, `fddup`, `exec_redir`:

```text
redir_rw      R1 rc 3 with the invented row `PATH value=/safe/> verdict=ALLOW`
              → R2 rc 1, `PATH value=/etc/x verdict=FORBID uses=line=2:redirection <>`
redir_clobber R1 rc 3 with `redirection has no target expression=>` and the real target
              read as a command (`opaque command y`); `/etc/y` never appears as a path
              → R2 rc 1, `PATH value=/etc/y verdict=FORBID uses=line=2:redirection >|`
redir_amp     R1 rc 3, `/etc/z` FORBID plus `opaque command ls`
              → R2 rc 1, `/etc/z FORBID uses=line=2:redirection &>` with `ls` registered
fddup         rc 0 both — `>&2`, `>&-` correctly carry no filesystem path
exec_redir    rc 0 both — `exec 3> "$ROOT/out"` records `/safe/out`
```

`/dev/tcp/HOST/PORT` and `/dev/udp/HOST/PORT` redirection targets are now network
endpoints rather than filesystem paths (anchor: `DEV_NET_RE`), which the round-1 audit
listed as *"treated as forbidden filesystem path, rc 1; no network verdict"*. Fixtures
`devtcp` and `devtcp_allow`.

### 8. MEDIUM — `unresolved_count` is an issue count, not a path count — REPAIRED

Every `Issue` now carries a `kind` (anchor: `KIND_ORDER`), and the report prints the
cardinalities as separate fields with separate names:

```text
PATHSCOPE resolved_fs_path_count=… resolved_net_endpoint_count=…
PATHSCOPE unresolved_path_count=… unresolved_endpoint_count=… coverage_issue_count=… provenance_issue_count=… parse_issue_count=…
```

Each `UNRESOLVED` line carries `kind=` so the reader can attribute it. `resolved_count` and
`unresolved_count` no longer exist; a consumer that parsed them must be updated. This is
the one repair that changes a published output field name.

The audit's two examples now separate cleanly:

```text
heredoc R1: unresolved_count=3, rc 3     → R2: every count 0, rc 0 (the body is stdin data)
array   R1: unresolved_count=2, rc 3     → R2: coverage_issue_count=1 (the array assignment)
                                                unresolved_path_count=1 (the `${A[0]}` use), rc 3
```

The heredoc change is a second repair inside the same finding: round 1 emitted
*"here input is outside the accepted static path subset"* and then **lexed the body as
commands**, so data was read as program text. The lexer now collects here-document bodies
(anchor: `def _consume_heredocs`), honours `<<-` tab stripping and quoted delimiters, and
harvests command substitutions only when the delimiter is unquoted — which is when bash
actually expands them. Fixtures `heredoc`, `heredoc_subst`, `heredoc_quoted` prove all
three arms, including that `$(cat /etc/shadow)` inside an unquoted-delimiter body is caught
(rc 1) and inside a quoted-delimiter body is data (rc 0).

### 9. MEDIUM — real-input diagnostic not literally re-runnable — REPAIRED

`SELF_QA_PATHSCOPE.md` publishes one PowerShell harness, verbatim, that needs no editing
and no pre-existing shell state. It writes every fixture, both constants files and the
machine-form §10.1 allowlist; reconstructs the round-1 prover from its pinned blob
`3f0820a9…` and prints its size and SHA-256; extracts both blocks with `git cat-file blob`
from pinned blobs and prints size, SHA-256 and `git hash-object` of what it extracted; runs
the full case list against both provers; and runs the determinism check. The complete
stdout of every case, for both provers, is published — not summarised.

Both real-block arms are included: the draft's literal `<ALLOCATE-AT-DISPATCH>` placeholder
(rc 3 before analysis, unchanged) and the disclosed non-authoritative static substitution
used for diagnostic depth only.

## Coverage matrix — what is modeled, and what STOPs

Everything below has a fixture in `SELF_QA_PATHSCOPE.md`.

| construction | round-2 behaviour |
|---|---|
| tilde `~`, `~user`, `~+`, `~-` | expanded from pinned `HOME`; otherwise unresolved path. No invented row |
| brace expansion `{a,b}`, `{a..b}` | unresolved path; the lexer no longer splits the word at `{` |
| arithmetic `$(( ))` | unresolved with the correct reason (round 1 mislabeled it *command substitution*) |
| arrays `A=(…)`, `${A[0]}` | coverage STOP on the assignment, unresolved path on the use |
| `${var:-default}` | fallback expanded; forbidden fallback reported FORBID |
| `${var/x/y}` and every other unmodeled form | unresolved with the exact expansion quoted |
| `$'…'` | decoded; forbidden result reported FORBID |
| backslash-newline continuation | joined; path resolves normally |
| here-document `<< <<- <<'EOF'` | body collected as stdin data; substitutions harvested only for unquoted delimiters |
| here-string `<<<` | data, no filesystem path |
| `$( )`, backticks, nesting | analysed as nested shell; nested sinks reported at the outer line |
| `< > >> <> >| &> &>> >& <& {fd}> >&- ` | full grammar; each records its real target with a distinct primitive label |
| `exec` | wrapper; `exec >file` is a pure redirection, `exec cmd` recurses |
| `source`, `.` | operand recorded as a path **and** a coverage STOP for the unanalysed content |
| `cd`, `pushd`, `popd`, `dirs` | path operands recorded; `cd -`/`pushd -` STOP on OLDPWD; `+N`/`-N` are stack indices |
| command substitution into a path | unresolved path |
| `find` incl. `-exec/-execdir/-ok/-okdir` | full expression parser; unmodeled predicate STOPs |
| `xargs` | `-a` recorded; command vector recursed; stdin-derived operand set is a declared STOP |
| multi-path argv (`cp`, `tar`, `install`, `ln`, `mv`) | every operand recorded, both positional and option-borne |
| `/dev/tcp`, `/dev/udp` | network endpoint, not a filesystem path |
| `ssh`, `scp`, `sftp`, `nc`, `curl`, `wget` | per-command grammars with implicit ports and path-bearing options |
| `getent` | always an unresolved endpoint naming the database |
| interpreters (`python*`, `perl`, `ruby`, `node`, `bash`, `sh`, …) | inline `-c`/`-e`/`-m` text is a coverage STOP; a script operand is recorded as a path **and** STOPs |
| `sed`, `awk` | file operands recorded; program text is a coverage STOP |
| `grep`, `jq` | fully registered; file operands recorded, no STOP |
| `systemctl` | modeled read-only verb set; any other verb STOPs |
| unregistered command | opaque sink: STOP, plus a STOP for every path-shaped or unresolvable argument |
| unknown option on a registered command | coverage STOP naming the option |
| `case`/`for`/`while`, functions | arm bodies and function bodies analysed; positional uses fail closed |

## Residuals — stated, not repaired

**R1. Lexical-versus-host binding (finding 6, second half).** The tool discloses that
membership is lexical and that symlink and mount resolution are not established; it does
not bind that to a host-side proof. Nothing a static reader of frozen bytes can do closes
this. Until a separate symlink/mount-chain proof exists, an `ALLOW-LEXICAL` row is a
statement about argv text, not about the object a run would open. Design-defect patterns 2
and 3 remain live against the Stage-1 design, not against this file.

**R2. Function call-site positional dataflow.** A function body is analysed at its
definition; the call site records nothing. This is sound only because every positional
expansion is fail-closed — `cat "$1"` inside a body is an unresolved path, `"$@"` is a
dynamic shell parameter — so a path handed to a function cannot reach a sink without a STOP
somewhere. Fixtures `func_positional` (rc 3) and `func_body` (rc 0) show both arms. If a
future audit finds a body shape where a positional reaches a sink without a STOP, this
residual becomes a finding.

**R3. Alias definitions are analysed, alias expansion is not applied.** `alias x='…'`
analyses the body at the definition. It does not then substitute `x` at later call sites.
Non-interactive bash does not expand aliases unless `shopt -s expand_aliases` is set, and an
unexpanded `x` is an opaque command that STOPs, so the direction of error is conservative.

**R4. Deliberate over-reporting.** `dirname` and `basename` transform strings and open
nothing, but their operands are still reported as argv paths (round-1 behaviour, kept: it
can only produce a false FORBID, never a false ALLOW). A `-` operand is modeled as the
stdin/stdout convention and is not recorded as a path. `ss` is modeled as a netlink query
with no argv endpoint; its `-F` filter file is a path.

**R5. Provenance attribution for inline option values.** For `--opt=VALUE` the provenance
set of the whole token is attributed to the value. A token like `--file="$ROOT"x` therefore
counts as having `ROOT` provenance. This can suppress a provenance issue but cannot change
a path's value or its allowlist verdict.

**R6. A registry is finite.** Unregistered commands STOP rather than resolve, so the
*resolved* path set of any input containing a STOP is a lower bound. The change from round
1 is that this is now visible: a rc-0 PASS is only reachable when every construct in the
input was modeled and every count is zero.

**R7. Counts field names changed.** See finding 8. Any consumer parsing
`resolved_count`/`unresolved_count` must be updated; `PATHSCOPE_LEAD_RERUN_2026-08-10.md`
and the round-1 self-QA quote the old names and are historical records of the round-1 bytes.

## Against the audit's minimum acceptance repair set

| required | disposition |
|---|---|
| 1. remove every silent-pass sink class in findings 1–4; unmodeled grammar → specific rc-3 | done; four more of the same class found and fixed |
| 2. correct tilde and `<>`; add falsifications for brace, arithmetic, arrays, substitutions, heredoc, every redirection | done; 62 fixtures, one per class, all with RED/GREEN |
| 3. define and disclose lexical-versus-host semantics incl. symlink/mount limits | disclosed in output, docstring and status; binding proof recorded as residual R1 |
| 4. separate unresolved path cardinality from parser/coverage issues | done; seven distinct fields plus `kind=` per record |
| 5. D026 RED/GREEN for every silent-pass fixture, RED against the current implementation | done, from the pinned round-1 blob so the RED column stays reproducible |
| 6. publish literally rerunnable real-block commands and complete output | done; one harness, no edit needed, complete stdout published |

## What did not change, deliberately

The blocks were not made to pass and the tool was not relaxed. With the draft's
`<ALLOCATE-AT-DISPATCH>` placeholder both blocks still stop at rc 3 before analysis, with
the identical `reason=input_parse_error line=7 detail=path contains an unresolved
angle-bracket placeholder`. With the disclosed static substitution both still reach rc 3.
`/dev/null` is still FORBID in RP6 and RP7, and `/proc/uptime` and `/proc/self/mountinfo`
are still FORBID in RP7 — they are §10.1 EXTEND candidates, not tool defects.

Line numbers for those rows moved (RP6 `/dev/null` at 398/400, RP7 `/proc/uptime` at 232,
`/proc/self/mountinfo` at 633, venv python at 999) because the committed blocks changed
after the round-1 audit: RP6-P0.sh is now 107252 B / `a090ae73…`, RP7-WPI-RO.sh 99903 B /
`11621044…`. The audit's 93421 B / `75db028e…` and 70941 B / `23e55667…` are earlier bytes.
Both round-1 and round-2 provers were run against the same current blobs in
`SELF_QA_PATHSCOPE.md`, so the RED/GREEN comparison is like for like.

## What a re-audit should attack first

1. The registry entries themselves — every `spec(...)` line is a claim that the listed
   options are the complete grammar. Insert an option that a real GNU tool accepts and this
   file does not list; the tool must STOP, and if it silently accepts, that is a finding.
2. The `path_free` property. Any command marked path-free that has *some* accepted form
   carrying a path is a silent-loss defect of exactly the round-1 class.
3. Heredoc collection against `<<-` with mixed tabs, nested here-documents on one line, and
   a delimiter that also appears indented in the body.
4. `scan_args` short-cluster handling where a value-taking option is not last in the
   cluster.
5. Residual R2: find a function body shape where a positional reaches a sink with no STOP.
