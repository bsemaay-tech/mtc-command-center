# Pathscope final additional T1 repair — implementer report (round 5)

Date: 2026-08-14
Implementer: fresh `claude-opus-5` session, effort **high**, no session persistence, no
sub-delegation, no Git mutation.
Authority: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISION_PATHSCOPE_FINAL_OVERRIDE_2026-08-14.md`
Gate-1 tier: **T1** — local non-economic static prover and its evidence harness.
Subject rejected: `PATHSCOPE_CAP_OVERRIDE_CODEX_T1_AUDIT_2026-08-13.md`, verdict
REQUEST_CHANGES, frozen candidate `2fb3eac05f8da716609549179a7961aa692eae6b`.

This is the one repair the owner authorized. It is followed, if the Lead freezes an
eligible candidate, by exactly one fresh `gpt-5.6-sol` high execution audit. Nothing here
claims acceptance.

## 0. Identity

| artefact | bytes | SHA-256 |
|---|---:|---|
| `pathscope_prover.py` before (committed at `2fb3eac0`, blob `55ea3a852f7781d03d57483f554c1b8ac62007c6`) | 131599 | `553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB` |
| `pathscope_prover.py` after | 137520 | `28848D60F74A7C668DB3019BBAC58550F4A55C1C02038C013153316C711EDF9C` |

`git diff --stat` on the prover: **164 insertions, 60 deletions, 1 file.**
`git diff --check` over all owned files: clean, rc 0.
`ast.parse(source, feature_version=(3, 12))`: OK on the round-5 bytes.
Runtime used: CPython 3.14.2 with `-B`. `py -3.12 -V` reports no such runtime on this
workstation, so 3.12 compatibility is established by feature-version parsing, as in prior
rounds.

### Owned files, with checkout bytes *and* blob bytes stated separately

The previous audit asked for exactly this: "future freeze records should say whether they
pin blob bytes or checkout bytes." Both are given. `checkout` is the working-tree file as
this session left it; `blob` is the LF-normalised content `git hash-object` computes over
it, which is what a commit would store. The prospective blob id is included so the Lead can
confirm the frozen object without re-deriving it.

| owned file | checkout bytes | checkout SHA-256 | blob bytes | prospective blob id |
|---|---:|---|---:|---|
| `pathscope_prover.py` | 137520 | `28848D60F74A7C668DB3019BBAC58550F4A55C1C02038C013153316C711EDF9C` | 137520 | `695ca9c951e31f53da9580d41326583d71086bb3` |
| `SELF_QA_PATHSCOPE.md` | 311577 | `F99D972F46C12AB1EEA3FB426B9F9F39D98B6A3724CFCD229140D1433DA0703D` | 311577 | `96af8b035e243a6f39486e4e674dfde7448ae917` |
| `STATUS_PATHSCOPE.md` | 12359 | `6C2C409A338A9084C40A660150B803C916C3383940E5BE6CB531E66C0D58A804` | 12197 | `06e963d6915e9627a3e0538631f4b81eaf023ca5` |
| `PATHSCOPE_FINAL_OVERRIDE_REPAIR_REPORT_2026-08-14.md` (new) | see note | — | — | — |

Line endings, stated because they are the one place where the two columns diverge:
`pathscope_prover.py` is LF in both columns, because this directory's `.gitattributes`
pins it with `text eol=lf`; `SELF_QA_PATHSCOPE.md` is LF in both columns and was LF at
`HEAD` as well (blob size 240907 equalled its checkout size), so this round did not change
its kind; `STATUS_PATHSCOPE.md` is CRLF in the working tree and LF in the blob, a
**pre-existing** condition of that file which this round did not introduce and could not
fix without editing `.gitattributes`, which is not an owned file. This report's own bytes
are omitted from the table for the obvious reason that stating them inside itself is
circular; the Lead should hash it after freeze.

No other tracked file was touched. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` still carries its
pre-existing uncommitted partial and was not read for modification, not staged and not
reverted. No `git checkout`, `git reset` or `git stash` was run on any tracked file. No
commit, push, host contact, credential, deployment, service, broker, ARM, order, TESTNET,
mainnet, Pine, parity, MTC or trading action occurred. All scratch lives under
`%TEMP%\pathscope-repair-r5` and `C:\tmp\ps_final_r5`. No shell fixture body was executed
as shell; every fixture was read only by the static Python analyzer.

## 1. Every required finding reproduced first, against the committed pre-repair bytes

The prompt forbids inferring old behaviour from source text, so the pre-repair blob was
extracted and driven before a line was edited:

```
git rev-parse 2fb3eac05f8da716609549179a7961aa692eae6b:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py
  -> 55ea3a852f7781d03d57483f554c1b8ac62007c6
git cat-file blob 55ea3a85... > C:\tmp\ps_final_r5\R4.py     (131599 B, sha256 553A97E9…E2EB)
```

Result of running the eight audit fixtures through `R4.py`, verbatim rc values:

| audit item | fixture | pre-repair result | matches the audit? |
|---|---|---|---|
| C-3.1 whitespace list, later relative member | `c3_ws_relative` | rc 0; the only assignment row is the allowed whole value `/safe/lib relative/escape.so` | yes |
| C-3.2 URI-shaped list, later absolute member | `c3_uri_list` | rc 0; allowed endpoint `127.0.0.1:8790` and `/safe/f` only, no row for `/etc/escape` | yes |
| C-3.3 colon-bearing whole pathname | `c3_colon_whole` | rc 0; `/safe/dir/file` allowed, no row for the admitted `/safe/relative:dir/file` reading | yes |
| C-3.4 empty-only loader list | `c3_empty_only` | rc 0; **no assignment row at all** | yes |
| C-3.5 command text without `/` | `c3_cmdtext_noslash` | rc 0; only the `cat` path | yes |
| C-4 `export "LD_PRELOAD=/etc/escape.so"` | `c4_export_quoted` | rc 0; `/etc/escape.so` absent | yes |
| C-4 `export 'X=/safe dir/escape'` | `c4_export_quoted_space` | rc 0; no assignment row | yes |
| C-4 `env` control | `c4_env_quoted_ctl` | rc 1; `/etc/escape.so` FORBID via `env assignment` | yes |

All eight reproduce exactly what the audit recorded, including the asymmetry that made C-4
diagnosable: the identical value reaches the repaired parser through `env` and does not
through `export`.

The published harness was likewise reproduced before it was changed. Its body was
extracted from `SELF_QA_PATHSCOPE.md` under `### The harness, verbatim` without retyping —
**20110 bytes, 346 lines, SHA-256 `27008BB5AAB4950935A235445C64EC0E1F91F3146CC5146D3A11063E4959BB63`**,
the same three numbers the audit recorded — saved to `%TEMP%\pathscope_r2_harness.ps1` and
run under its literal published command from the repository root.

## 2. The harness portability defect: cause measured, not inferred

Under **this session's ambient environment** the round-4 harness reproduced its recorded
digests exactly (`11c5cb8e…67dd`, `32da2842…317a`, `40e458dc…8bf62`, `2e9d6f44…05db`,
`224cda72…2ad2`). That is itself the finding: the run is clean only because of something
the harness never set. Probing the environment showed why:

```
python -c "import sys;print(sys.stdout.encoding)"   -> utf-8
$env:PYTHONIOENCODING                                -> utf-8:surrogateescape   (ambient, not set by the harness)
chcp                                                 -> Active code page: 65001
locale.getpreferredencoding(False)                   -> cp1254
```

Removing only the ambient `PYTHONIOENCODING` and re-running the same invocation reproduces
the auditor's numbers, all five of them, character for character:

```
child_stdout_enc=cp1254
first=PATHSCOPE shell=C:\Users\Bar<U+FFFD><U+FFFD>Semaay\AppData\Local\Temp\pathscope-repair-r2\find_exec.sh

R4_UNDER_STRIPPED_ENV find_exec      rc=1 sha=b3119f99152c865da799f5ac638327d32458fc9f02e6c73e07e7c496320d5620
R4_UNDER_STRIPPED_ENV assign_prefix  rc=1 sha=f77f67147f87fdcdc2f5b8891e7e3c4a062c0da7c0197c568ab4264e1cb04d81
R4_UNDER_STRIPPED_ENV c2_list_prefix rc=1 sha=b2f153c2c0ade040cc39c8d0df1c7a7956be5a076c1842c325bd132d57e4f611
R4_UNDER_STRIPPED_ENV RP6-P0         rc=3 sha=8ce5571bd2e4f8f24135c860324e6c67bd84358fc77a095a1b53d768abe61ecf
R4_UNDER_STRIPPED_ENV RP7-WPI-RO     rc=3 sha=c0e4b8073e7c387bf17e80435ddcfbd3d5ddf7d1b1db956cdbb1812c468bf452
```

The chain is: Python falls back to the locale encoding for a piped stdout; PowerShell
decodes that stream with `[Console]::OutputEncoding` (UTF-8 under code page 65001); the
`ı` byte is invalid UTF-8 and becomes U+FFFD; `$QA` is a .NET string that still holds the
real character, so `.Replace($QA, '<QA>')` matches nothing; the absolute user path then
survives into every transcript line and into the harness's own `WROTE …` lines, and the
recorded digests cannot reproduce.

**The repair does not make two broken runs agree.** Three independent defences remove the
dependency, and none of them is a manual substitution:

1. the harness pins `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8` and
   `[Console]::OutputEncoding` to UTF-8;
2. it runs every prover invocation from the fixture directory with **relative** arguments,
   so no user-specific absolute path can enter a transcript at all — the transcripts are
   pure ASCII and there is no `<QA>` normalisation left to fail;
3. it fails closed: any transcript line containing the scratch directory, the temporary
   root or the repository root aborts the run with `TRANSCRIPT_LEAK` rather than writing
   an unreproducible transcript.

Blob extraction no longer routes a non-ASCII destination path through `cmd /c "… > path"`
(the same class of defect); the blob is streamed to disk through .NET and the git blob id
is computed in process instead of by passing a non-ASCII file name to `git hash-object`.

**Verification at the document level, which is the only level that counts.** The new fence
was extracted back out of `SELF_QA_PATHSCOPE.md` programmatically and compared to the
source file: identical, 27699 bytes, SHA-256 `0C6E0B28A6F2057DCE2EC9CB802B77D2864148A7C1382ED424EDBDEDA723C93D`.
It was then saved as `%TEMP%\pathscope_r5_harness.ps1` and run under its literal published
command in two deliberately different environments:

* **A** — this session's environment (`PYTHONIOENCODING=utf-8:surrogateescape`, code page
  65001): `RUN_A_MATCHES_RECORDED=True`;
* **B** — `PYTHONIOENCODING` and `PYTHONUTF8` removed, `chcp 1254`, and
  `[Console]::OutputEncoding` forced to `windows-1254`: `RUN_B_MATCHES_RECORDED=True`.

Both runs reproduce the recorded stdout byte for byte, including all four transcript
digests (`667BF364…E89D`, `A534BDCF…328C`, `599B4482…CBCC`, `BC142778…C01B`) and all seven
determinism digests. Environment B is the environment in which the round-4 harness
demonstrably diverges, which is what makes the comparison a test rather than a repetition.

## 3. C-3 — terminal conservation across the admitted member grammar

`record_assignment_members` and its two helpers were rewritten so that conservation is a
property of the rule, not of the example list.

**What changed, and why each change is the general rule rather than a patch for a fixture:**

1. **The whole value is always a candidate; members are added, never substituted.** Round 4
   replaced the candidate list with the words whenever the word-list reading was live, so
   the single-pathname reading disappeared in exactly the case the C-2 regression guard
   exists to protect. Both readings are now always present.
2. **One predicate for the word-list reading.** Round 4 required that some word carry `/`
   **and** (an option word exist, or a *later* word be *absolute*, or the first word not be
   path-shaped). That conjunction is what let a later *relative* word behind a path-shaped
   first word (C-3.1) and command text with no `/` at all (C-3.5) fall through. The rule is
   now: a multi-word value is a live word list when **any word is option-shaped or any word
   carries `/`**. A value where neither holds (`MSG="Permission denied"`) carries neither a
   pathname nor an argv under either reading and stays in the disclosed `bare` residual.
3. **`split_list_members` replaces the "starts with a scheme" shortcut.** Round 4 disabled
   colon splitting for the complete value whenever `URI_SCHEME_RE` matched it, so a mixed
   list lost every member after the URI (C-3.2). Splitting now protects only the
   `scheme://authority` span (`URI_PREFIX_RE`), a colon after the authority is a separator,
   and a member that itself begins a new URI re-arms the protection — so `$URL:/etc/escape`
   splits and `http://h:8443/x` does not.
4. **A relative value carrying `:` is still a pathname.** `assignment_member_kind` dropped
   the `":" not in text` condition, so the admitted single-pathname reading
   `<PWD>/relative:dir/file` gets a row (C-3.3) exactly as an absolute list value always
   did.
5. **An empty member is resolved, not declared unevaluable.** An empty member exists only
   because a separator does; it names the consumer's current directory, which is the pinned
   `PWD`, so it is recorded as that path (C-3.4). Round 4 emitted a coverage record only
   when some *other* member was already a path, so `LD_LIBRARY_PATH=:` — the case that most
   needs consumer semantics — had zero accounting. Resolving rather than STOPping is
   deliberate: an inability to evaluate must not be manufactured where the fact is
   available. If `PWD` is unpinned the row fails closed as an unresolved path, which is what
   happens on `RP7-WPI-RO` under `real.constants`. A whole value that is simply empty
   (`X=`) is an empty scalar, not a one-element list, and is left alone.

Measured closure for all five audit items plus three generalisations
(`c3_ws_later_word`, `c3_uri_pair`, `c3_empty_only_out`) is in
`SELF_QA_PATHSCOPE.md` §"Round 5", with the complete pre-repair transcript in
`RED_R4.txt` and the complete repaired transcript in `GREEN_R5.txt`, both embedded.

The strongest of the new fixtures is `c3_empty_only_out`: an empty loader-list member with
`PWD=/elsewhere` pinned outside the allowlist returns **rc 0 with nothing at all** on the
committed bytes and **rc 1 with `/elsewhere` FORBID** after the repair. That is the real
risk the empty member carries, and it was completely invisible.

## 4. C-4 — the three assignment sites re-audited as one grammar

The audit's diagnosis was exact: `record_assignment_value` already contained a correct
quote-recovery fallback, and the declaration site simply could not reach it, because the
loop gated every operand on `assignment(token)` — an `ASSIGN_RE` match against the **raw**
token text. A quoted operand matched nothing, fell past the `NAME_RE` arm, and vanished
with no row and no coverage record.

`analyze_declaration` now classifies each operand on its **expanded** form:

| site | gate | why |
|---|---|---|
| assignment prefix | raw `ASSIGN_RE` on the token | correct as-is: Bash does not treat a word with a quoted *name* as an assignment prefix either, so the raw match is the shell's own rule. `LD_PRELOAD="/etc/x"` still matches, because only the value is quoted. |
| `env` wrapper | `ASSIGN_RE` on the **expanded** word | already correct at round 4; unchanged. |
| `local` `declare` `typeset` `export` `readonly` | raw `ASSIGN_RE` first (byte-identical to round 4, so the C-1 closure is preserved rather than re-derived), otherwise expand and re-test | the repair. A quoted `NAME=VALUE` now binds through `bind_assignment` — which repeats the pinned-constant override check, so a quoted declaration cannot silently redefine a preregistered constant — and then records through the same `record_assignment_value`. |

Two arms that previously produced silence now fail closed: an operand whose expansion is
not statically known emits a coverage record, and an operand that is neither an option, a
NAME, nor `NAME=VALUE` after expansion emits a specific coverage record
(`c4_export_opaque`, rc 0 → rc 3).

All five declaration keywords are driven by the P11 family and all five move from rc 0 to
a non-zero verdict with the sink printed. The `env` control that already worked stays at
rc 1, and `export LD_PRELOAD="$ROOT/ok.so"` stays at rc 0 — the repair fails closed on the
construct, not on a variable name.

## 5. D026 — RED against the committed bytes, GREEN against the repaired bytes

The primary RED column for every claimed closure is the committed pre-repair blob
`55ea3a852f7781d03d57483f554c1b8ac62007c6`, extracted and executed **by the published
harness itself** (`RED_R4.txt`, 324 lines, SHA-256 `BC142778035AE9B759A47869CCEA86D8C23D9406735BBDB189009188C36CC01B`).
Nothing in family P11 is a prediction, and the RED column cannot rot when the repair is
committed because it is reconstructed from a pinned blob.

Seven single-line mutations were then applied to copies of the round-5 source outside the
repository and executed. Each mutation restores exactly one round-4 behaviour or deletes
exactly one round-5 property; the mutation driver asserts that each anchor occurs exactly
once before applying it, so a mutation cannot silently miss.

| mutation | destroys | measured effect |
|---|---|---|
| MUT-A whole value dropped | the quoted-space regression guard | `c2_quoted_space` loses its `/safe dir/escape` FORBID row and prints only the two fabricated ALLOW rows |
| MUT-B no colon members | C-2 and C-3.2/C-3.4 | `c2_list_prefix`, `c3_uri_list`, `c3_empty_only_out` all fall back to `PASS rc=0` |
| MUT-C no word-list reading | C-3.1 and C-3.5 | `c3_ws_relative` and `c3_cmdtext_noslash` fall back to `PASS rc=0` |
| MUT-D round-4 URI shortcut | C-3.2 | `c3_uri_list` and `c3_uri_pair` fall back to `PASS rc=0` |
| MUT-E empty member ignored | C-3.4 | `c3_empty_only` loses its only row; `c3_empty_only_out` falls back to `PASS rc=0` |
| MUT-F round-4 member kind | C-3.3 | `c3_colon_whole` falls back to `PASS rc=0` |
| MUT-G round-4 declaration gate | C-4 entirely | every quoted declaration falls back to `PASS rc=0` |

Full measured output is embedded in `SELF_QA_PATHSCOPE.md`.

**The regression guard is stated honestly.** `c2_quoted_space` has no pre-repair RED column
— round 4 already handled it correctly — so its evidence is MUT-A. Its rc moved from 1 to 3
this round because the value is a multi-word value carrying `/`, which the single uniform
word-list rule now treats as live. The guard property is therefore stated at row level and
not at rc level: the whole quoted pathname must appear as its own FORBID row and must not
be replaced by two allowed paths. The repaired prover prints the FORBID row plus the two
member rows plus a coverage record; MUT-A prints only the two allowed member rows and no
FORBID row. An rc comparison would **not** discriminate here, and this report does not
offer one as if it did.

## 6. Carried fences, controls and regression surface

109 cases (105 fixtures + 4 real-block runs) were executed under the committed round-4 blob
and the round-5 source and compared byte for byte: **84 byte-identical, 25 differ.** The 25
are 15 P11 fixtures (whose purpose is to differ), 8 P10 fixtures, 1 base fixture
(`assign_benign`) and `RP7-WPI-RO`. Every one is itemised in `SELF_QA_PATHSCOPE.md`
§"Carried fences that changed, with discriminating power", with the cause and the mutation
that falsifies it. **No FORBID row is lost anywhere**; every change adds rows, adds a
coverage or provenance record, or replaces an unevaluable record with a resolved one.

Benign controls: `assign_benign` and `c2_benign_scalars` (`IFS=:`) stay at **rc 0**. They
gain one `/safe` row with `sources=PWD`, because C-3.4 is decided on grammar and `IFS=:`
and `LD_LIBRARY_PATH=:` are the same lexeme — there is no lexical discriminator between
them, and inventing one from the variable name is precisely the mistake round 1 made with
`NO_PATH_COMMANDS`. `c2_benign_words`, `c2_bare_soname`, `c2_uri_allow`, `c2_allow_list`,
`c4_export_plain_ctl` and `c3_scalar_ctl` are unchanged at rc 0.

Real blocks: `RP6-P0` is **byte-identical** under round 4 and round 5. `RP7-WPI-RO` gains
one unresolved-path record at line 681 (`seen_roots="$seen_roots$r "`, whose whole-value
reading is relative and fails closed because `real.constants` pins no `PWD`), moving
`unresolved_path_count` 34 → 35 with every other count unchanged. Both blocks stay at rc 3
under both the `<ALLOCATE-AT-DISPATCH>` placeholder and the disclosed static `REMOTE_BASE`.
The tool was not tuned to admit either.

## 7. Disclosed residual and known limits

* A member with **no `/` and no option shape** — a bare soname, a scalar, a tool name — is
  resolved by the consumer's own search rules, is not an argv pathname, and carries no row.
* **An option word carrying an attached pathname is not decomposed.** `-I/usr/include` or
  `ssh -i/etc/key` produces the word-list coverage record, not a row for the embedded path.
  The construct is visible and fail-closed at rc 3, but the pathname inside the option word
  is not extracted. This limit is written into the coverage reason text the tool emits, so
  it cannot be read off a transcript as a resolved fact. It is a candidate for a later
  round; it is **not** claimed closed here.
* **The union of readings is conservative, not exact.** The tool over-rejects
  (`MSG="denied /etc/secret"`; whole-value rows such as `/safe/ssh -i /etc/key`). A
  fail-closed prover may over-reject; it may not under-report.
* The membership claim remains **lexical argv scope**: no symlink resolution, no mount
  boundary, no host probe. Unchanged by this round.

## 8. What this report does not claim

It does not claim acceptance, PASS, or that the tool is fit for any host action. It records
one implementer round with its evidence. The Lead owns reproduction and acceptance; one
fresh independent `gpt-5.6-sol` high execution audit is the authorized next step, and no
further Pathscope repair or audit cycle is authorized without a new owner decision.
Hostinger Stage 1 remains a separate hard gate.
