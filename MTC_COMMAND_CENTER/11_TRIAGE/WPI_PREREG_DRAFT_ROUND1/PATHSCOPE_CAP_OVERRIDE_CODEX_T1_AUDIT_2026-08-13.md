# PATHSCOPE cap-override Codex T1 execution audit

Date: 2026-08-14  
Auditor: fresh independent `gpt-5.6-sol`, effort **high**, T1  
Frozen subject: `2fb3eac05f8da716609549179a7961aa692eae6b`

## VERDICT: REQUEST_CHANGES

The published C-2 fixtures demonstrate real closures, and the quoted-space regression
guard is sound. Acceptance nevertheless fails. The assignment-member grammar still has
several adjacent silent sinks that return `PASS rc=0`, quoted declaration assignments do
not reach the repaired grammar, and the published harness does not reproduce its recorded
transcript/determinism hashes under its literal command. This is the authorized final T1
cycle, so the required findings below return the lane to the owner boundary.

## 1. Identity and frozen subject

All four materialized working-tree artifacts matched the kickoff before execution and
again afterward:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `pathscope_prover.py` | 131599 | `553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB` |
| `SELF_QA_PATHSCOPE.md` | 240907 | `3EFEA7F34521BC02D2FADAB102A7A59AE25D1C6A6BEC8E1D93A6AF47510A92FB` |
| `STATUS_PATHSCOPE.md` | 6981 | `85E6C03CEC42F306B6D001E90EC919AC77304EF5226AB6C1C6B7A25D6B783D4A` |
| `PATHSCOPE_CAP_OVERRIDE_REPAIR_REPORT_2026-08-13.md` | 19739 | `389D7688295BD3637292D660A908DE7B97B331173FADDF4C63585DAEFFD88D28` |

Identity nuance: `STATUS_PATHSCOPE.md` is `text: auto`. The Git blob at the frozen commit
is the LF-normalized 6886-byte blob (SHA-256
`A0BFAE7D8DDF283E207B223AD9D3A60F912639608674B927AAA9A965FFB152CE`), while the kickoff
pins its 6981-byte CRLF checkout projection. The content is the same under Git's clean
filter, but future freeze records should say whether they pin blob bytes or checkout bytes.

## 2. Published harness: clean completion but exact-reproduction failure

I extracted the body under `### The harness, verbatim` without retyping it:

- 20110 bytes, 346 lines
- SHA-256 `27008BB5AAB4950935A235445C64EC0E1F91F3146CC5146D3A11063E4959BB63`

I ran the published command literally from the repository root. Two runs completed at
outer rc 0; the captured run had zero stderr bytes. Artifact identities and transcript
line counts reproduced: RED_R1 660, GREEN 1363, RED_R3 150. Every determinism pair was
internally equal. The recorded digests did not reproduce:

| pair | recorded | observed (both copies) |
|---|---|---|
| `find_exec` | `11c5cb8e...67dd` | `b3119f99...5620` |
| `assign_prefix` | `32da2842...317a` | `f77f6714...4d81` |
| `c2_list_prefix` | `40e458dc...8bf62` | `b2f153c2...f611` |
| `RP6-P0` | `2e9d6f44...05db` | `8ce5571b...1ecf` |
| `RP7-WPI-RO` | `224cda72...2ad2` | `c0e4b807...f452` |

The cause is reproduced, not inferred. Windows PowerShell decoded the Python-emitted temp
path as `C:\Users\Bar��Semaay\...`; `$QA` retained `C:\Users\BarışSemaay\...`.
The harness's `.Replace($QA, '<QA>')` therefore replaced nothing. Raw embedded transcript
comparisons had 89 RED_R1, 89 GREEN, and 18 RED_R3 differing lines. If I manually replace
the actually rendered corrupt prefix, all three transcripts match their embedded fences
exactly. That manual repair is diagnostic only: the mandatory verbatim evidence contract
requires exact reproduction without editing. The harness is environment/encoding-dependent
despite claiming otherwise. This is required repair under the kickoff's item 1 and D026's
literal-reproducibility rule.

## 3. Intended C-2 cases independently reproduced

The intended repair cases behave as claimed when driven directly against the frozen R4
prover:

| case | observed result |
|---|---|
| later absolute member, assignment prefix | rc 1; `/etc/escape` FORBID |
| later absolute member, `env` | rc 1; `/etc/escape` FORBID |
| later absolute member, `export` | rc 1; `/etc/escape` FORBID |
| allowlisted-first colon list | rc 0; whole value and both members accounted |
| empty plus path member | rc 3; path row plus empty-member coverage |
| whitespace command text with `/etc/key` | rc 3; sink row plus coverage |
| ordinary relative pathname with `PWD=/elsewhere` | rc 1; `/elsewhere/relative/path.so` FORBID |
| `X="$ROOT dir/escape"` | rc 1; one `/safe dir/escape` FORBID row, not split |

For D026, the harness literally ran all eighteen P10 cases against Git blob
`e600a107f2e2a790653cc544a94cd7436b7b070a` and the repaired bytes. After the path-rendering
normalization described above, the 150-line RED_R3 and 1363-line GREEN fences reproduce.
The twelve claimed closures have actual R3 RED/current GREEN execution; five controls
hold. `c2_quoted_space` is correctly described as a regression guard, not a pre-fix
closure. I independently recreated MUT-A by replacing the single candidate line in a temp
copy: R4 returned rc 1 with the whole pathname; the mutant returned rc 0 with fabricated
`/safe` and `/safe/dir/escape` ALLOW rows. The guard discriminates.

## 4. REQUIRED C-3: alternate member readings still disappear

`record_assignment_members` does not conserve all readings it says it conserves. These
fixtures were static-reader input only; none was executed as shell.

1. **Whitespace list with a later relative member.** With `ROOT=/safe`,
   `PWD=/elsewhere`, and allowlist `/safe/**`:

   ```bash
   LD_PRELOAD="$ROOT/lib relative/escape.so" cat "$ROOT/f"
   ```

   R3 and R4 both return rc 0. R4 records only the allowed whole value
   `/safe/lib relative/escape.so`; the consumer's later relative member
   `/elsewhere/relative/escape.so` has no terminal disposition. The predicate tests later
   words for absolute paths and options, but not later relative pathnames.

2. **URI-shaped loader list with a later absolute member.** With the pinned allowed
   `$URL` endpoint:

   ```bash
   LD_LIBRARY_PATH=$URL:/etc/escape cat "$ROOT/f"
   ```

   R4 returns rc 0, emits the allowed endpoint and `/safe/f`, and emits no filesystem row
   for `/etc/escape`. `URI_SCHEME_RE` disables colon splitting for the complete value, so
   endpoint provenance converts a mixed loader-list sink into PASS.

3. **A colon-bearing single pathname is not kept.** With `BASE=dir/file`, `PWD=/safe`,
   and exact allows for `<BASE>` and `<ROOT>/f`:

   ```bash
   X=relative:$BASE cat "$ROOT/f"
   ```

   R4 returns rc 0 after allowing `/safe/dir/file`; it emits no row for the admitted
   single-pathname reading `/safe/relative:dir/file`. The source comment says the whole
   candidate is retained, but `assignment_member_kind` classifies a relative value
   containing `:` as `bare`, so retention is non-terminal.

4. **An empty-only loader list has zero accounting.** `LD_LIBRARY_PATH=:` returns rc 0 and
   emits no assignment row. Empty loader-list members name the consumer's current
   directory. The implementation emits coverage only when some other member was already
   classified as a path, so the empty member that most needs consumer semantics silently
   disappears.

5. **Executable command text without `/` has zero accounting.** 
   `GIT_SSH_COMMAND="ssh -v" cat "$ROOT/f"` returns rc 0 with only the cat path. The
   repair's comments expressly name `GIT_SSH_COMMAND`, while the kickoff requires any
   executable command text with zero terminal accounting to be found. Requiring a slash
   before the word-list grammar becomes live leaves the entire command string silent.

These are the same Pattern 12/13 failure class as C-2: admitted syntax is reduced before
terminal accounting, and absence from the result is read as absence from the subject.

## 5. REQUIRED C-4: quoted declaration assignments bypass the repair

The quote-recovery fallback in `record_assignment_value` is reachable from the `env` site,
but declaration builtins call `assignment(token)` first and call the repaired function
only when that raw-token match succeeds. Valid quoted declaration arguments therefore
disappear before the fallback:

```bash
export "LD_PRELOAD=/etc/escape.so"
cat "$ROOT/f"
```

R3 and R4 both return rc 0 and emit only `/safe/f`; `/etc/escape.so` is absent. The Lead's
quoted-space shape at the same site also false-passes:

```bash
export 'X=/safe dir/escape'
cat "$ROOT/f"
```

Again R4 returns rc 0 with no assignment row. By contrast, the independently executed
`env "LD_PRELOAD=/etc/escape.so" cat "$ROOT/f"` control reaches the fallback and returns
rc 1. The repair must make declaration-prefix reachability quote-aware rather than leaving
the correct parser unreachable.

## 6. Scope, safety, and delta

- No host, network, deployment, credential, ARM, broker, exchange, order, TESTNET,
  mainnet, Pine, parity, MTC, or trading action occurred.
- Shell fixture bodies were read only by the static Python analyzer; none was executed as
  shell.
- No sub-agent, model, or counterpart CLI was invoked.
- No Git mutation occurred.
- Scratch files were confined to the user temp directory.
- All four subject identities were unchanged after execution.
- Immediately before this verdict write, whole-repository status had 184 pre-existing
  entries. The pre-existing `RP7-WPI-RO.sh` diff remained present and untouched; its patch
  was 4723 bytes with SHA-256
  `005381FAF6DF63139C895778E27A03092C562FC2D5162E307ED5BD6079926482`.
- The only repository delta attributable to this audit is this verdict file.

## 7. Required disposition

**REQUEST_CHANGES.** The exact published cases are not enough to establish complete member
grammar. Repair C-3 and C-4 with terminal conservation across alternate readings and all
three call sites, and make the published harness byte-reproducible under its literal
command. Because this was the owner-authorized final T1 cap-override audit, do not open
another repair/audit cycle without a new owner decision.
