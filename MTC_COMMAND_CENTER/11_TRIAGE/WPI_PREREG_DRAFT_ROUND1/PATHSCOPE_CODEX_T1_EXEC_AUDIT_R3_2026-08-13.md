# PATHSCOPE — Codex T1 EXECUTION re-audit, round 3

Date: 2026-08-13
Auditor: `gpt-5.6-sol`, effort **high** (T1), fresh independent session; neither the
round-2 `claude-opus-5` implementer nor the round-3 GLM-5.2 implementer.
Working directory: `C:\LAB\Tradingview_LAB_CLEAN`
Mode: repository read-only except this single verdict file. No git mutation, no host
contact, no network, and no sub-delegation. Shell fixtures were input data to the static
reader only; none was executed as shell.

## VERDICT: REQUEST_CHANGES

The seven published P9 RED/GREEN fixtures are real and the nominated round-3 harness
reproduces exactly. However, the construct-level repair is incomplete. A known assignment
value is recorded only when the complete rendered value starts with `/`, `./`, or `../`.
Path-bearing values with a different first member — including loader lists with a later
absolute member and ordinary relative pathnames containing `/` — disappear with no PATH or
coverage record. I reproduced this at all three repaired call sites. Each case returned
`PASS rc=0` while the out-of-allowlist sink lexeme was absent.

Under the kickoff's standing contract, **any new surviving silent sink is CRITICAL**.
Finding C-2 below therefore blocks flagship EXECUTION acceptance. I do not state the
acceptance sentence.

## 1. Identity — re-derived before execution

| artefact | expected | re-derived | match |
|---|---:|---:|---|
| `pathscope_prover.py` bytes | 124251 | 124251 | yes |
| SHA-256 | `0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7` | `0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7` | yes, case-insensitive comparison |

The identity was unchanged after all execution and inspection.

## 2. Published harness — extracted and run verbatim

I extracted the fenced body under `### The harness, verbatim` from
`SELF_QA_PATHSCOPE.md` without retyping it and wrote it outside the repository as
`%TEMP%\pathscope_r2_harness.ps1`:

- 15,781 bytes
- 276 lines
- zero non-ASCII bytes
- SHA-256 `EAB8ED25EB5EA974F7F7B4689332A49C5844067FEF44FC1A545D86C8F6ACB2A2`

From the repository root I invoked the published command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\pathscope_r2_harness.ps1"
```

Stdout and stderr were redirected to scratch outside the repository as required. Measured
result:

```text
outer_rc=0 stdout_lines=10 stderr_bytes=0 recorded_stdout_exact_match=True
RED_R1_lines=552 GREEN_R2_lines=1189 determinism_pairs=4 all_equal=True
```

All ten stdout lines match the UTF-8 round-3 fence at `SELF_QA_PATHSCOPE.md:61-71`
character for character. This includes both prover identities, both pinned block identities,
both transcript counts, and all four determinism digests.

### Seven P9 fixtures — independently read from the generated transcripts

The generated `RED_R1.txt` and `GREEN_R2.txt` confirm the round-3 table:

| symbolic fixture | R1 rc | round-3 rc | round-3 terminal accounting |
|---|---:|---:|---|
| `assign_prefix` | 0 | 1 | 1 FORBID + 1 ALLOW-LEXICAL |
| `assign_prefix_allow` | 0 | 0 | 2 ALLOW-LEXICAL |
| `assign_bare` | 0 | 1 | 1 FORBID |
| `assign_benign` | 0 | 0 | 1 ALLOW-LEXICAL |
| `assign_export` | 0 | 1 | 1 FORBID + 1 ALLOW-LEXICAL |
| `assign_env` | 0 | 1 | 1 FORBID + 1 ALLOW-LEXICAL |
| `assign_multi` | 0 | 1 | 2 FORBID + 1 ALLOW-LEXICAL |

The five named sinks therefore have executed RED-before-GREEN evidence, and both controls
hold. The repair genuinely closes the exact published fixtures.

The round-3 source also parses successfully with
`ast.parse(..., feature_version=(3, 12))` under CPython 3.14.2.

## 3. CRITICAL C-2 — internal and relative assignment path grammar still disappears

**Severity: CRITICAL. Required repair.**

The source-level cause is `pathscope_prover.py:1265-1267`:

```python
rendered = value.text or ""
if rendered.startswith(("/", "./", "../")):
    self.record_path_text(...)
```

There is no `else`. Every statically known value that does not start with one of those
three prefixes is treated as non-path data, even when the value contains a pathname that a
runtime primitive consumes. This contradicts the source contract at `:6-9`: unmodeled
constructs must emit a specific unresolved record; silence is never a result.

### Executed adversarial evidence

I drove the repaired prover directly with small symbolic fixtures and the same `/safe/**`
allowlist. All output stayed in scratch. The absolute-path control proves the helper itself
was reached; the next cases expose its boundary:

| symbolic fixture | repaired site / value shape | rc | PATH rows | coverage rows | sink visible | verdict |
|---|---|---:|---:|---:|---|---|
| `control_abs` | prefix; complete value begins `/` | 1 | 2 | 0 | yes | REJECT |
| `list_prefix` | prefix; bare loader member then absolute member | **0** | 1 | 0 | **no** | **PASS** |
| `list_env` | `env`; same loader-list shape | **0** | 1 | 0 | **no** | **PASS** |
| `list_export` | `export`; same loader-list shape | **0** | 1 | 0 | **no** | **PASS** |
| `list_space` | prefix; whitespace-separated loader list with later absolute member | **0** | 1 | 0 | **no** | **PASS** |
| `relative_path` | prefix; ordinary relative pathname containing `/`, pinned `PWD` outside allowlist | **0** | 1 | 0 | **no** | **PASS** |

In every failing row, the sole PATH row is the benign allowlisted operand of the visible
command. The assignment sink has no terminal disposition. Stderr was empty in every run.

This is not the disclosed bare-soname residual. A value shaped like
`bare-member:/etc/escape.so` contains an explicit absolute pathname, and `relative/path.so`
contains a slash and is a pathname relative to the preregistered `PWD`. Both are within the
repair's assignment-value lexical subject. The current first-character test neither models
their grammar nor fails closed on it.

### Required direction

Do not replace this with a variable-name allowlist. For assignment values that may carry
one path, a path list, or command text, either:

1. parse the complete value grammar and give every component a terminal disposition, or
2. emit a specific coverage record when the grammar is not modeled.

At minimum, the repair must handle ordinary relative pathnames and multi-member values
without allowing a later pathname to disappear. Add executed RED/GREEN falsification for
the repaired cases under D026.

## 4. C-1 closure and disclosed residual

- **Exact published C-1 fixtures:** CLOSED. The harness proves all seven predictions.
- **Construct-level C-1 property:** NOT CLOSED. C-2 is the same silent-disappearance class
  immediately adjacent to the repaired predicate.
- **Bare soname disclosure:** accurate for the narrow example `LD_PRELOAD=libc.so`, but
  materially incomplete as a boundary disclosure. It does not disclose mixed loader lists
  containing a later absolute path or ordinary relative pathnames containing `/`.

The disclosure therefore cannot convert C-2 into an accepted residual.

## 5. Cheap-item adjudication

| item | adjudication |
|---|---|
| `:325-327` wording from the prior audit | **FIXED.** Current `SELF_QA_PATHSCOPE.md:406-410` correctly says sixteen zero-row RED fragments, distinguishes CRITICAL 1/2 and F1-EXT from CRITICAL 3/4, and explains the three benign survivors. |
| U-3 facts and citation | **Facts re-verified true; citation still absent.** CPython is 3.14.2, the round-3 source parses with feature version 3.12, and `py -3.12 -V` reports no installed 3.12 runtime. Lines 26-28 still present these as local assertions without citing the prior execution audit or printing the probes in this document's harness output. Documentary nit, not a factual defect. |
| NIT-1 ENDPOINT label | **Still present.** `pathscope_prover.py:2748` renders filesystem allows as `ALLOW-LEXICAL` but network allows as bare `ALLOW`; the recorded allowed endpoint rows retain the asymmetry. Optional wording nit, not the blocking finding. |
| determinism prose | **New optional stale wording.** `SELF_QA_PATHSCOPE.md:1644-1646` says “last three lines” and names three pairs, but round 3 now emits four determinism lines including `assign_prefix`. |

## 6. Scope and safety

- No Pine, parity, MTC strategy, trading, broker, host, deployment, or network surface was
  touched.
- The nominated prover and documents were read only.
- Harness and adversarial artifacts were confined to the Windows temporary directory.
- No shell fixture was executed; only the static Python reader processed fixture text.
- No model, CLI implementer, or sub-agent was invoked.
- No git command mutated repository state.

## 7. Delta gate

Before execution, `git status --porcelain=v1 --untracked-files=all` contained 180 entries.
After all execution and this verdict write, it contained 181 entries.

The path-scoped result is exactly:

```text
?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CODEX_T1_EXEC_AUDIT_R3_2026-08-13.md
```

**Path-scoped gate: PASS.** The only status entry at the authorized output path is this new
verdict file.

Whole-status advisory: `after - before` contains exactly the same one entry above;
`before - after` is empty. No concurrent or pre-existing entry changed during this lane.
The whole-status delta is therefore fully attributable to this verdict file.

## 8. Recommendation

**REQUEST_CHANGES.** C-2 is a reproduced surviving silent sink, so these bytes do not hold
flagship EXECUTION acceptance. Repair the construct boundary and demonstrate D026 RED/GREEN
for mixed-member and relative-path assignment values. The three documentary nits may ride
with that repair but do not independently block.

If the prior Claude round-2 audit and this re-audit are the two T1 rounds counted for this
work package, the permanent T1 round cap is now exhausted; the Lead should surface the
boundary rather than silently opening another audit round unless the owner supplies an
explicit override.

Session model/effort: `gpt-5.6-sol` / **high** (T1).
