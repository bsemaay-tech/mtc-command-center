# Pathscope — round-3 source repair of CRITICAL C-1 (GLM implementer report)

Date: 2026-08-13
Role: GLM-5.2, source-level implementer (Tier T1 repair). **Lead executes the harness.**
Work order: `PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md`, finding **C-1 (CRITICAL)**,
§5 + §12. The flagship execution audit returned **REQUEST_CHANGES** on exactly this one
blocking item.
Git mutation: **none.** No commit, no stage, no branch change.
Host contact / network / shell execution: **none.**

> **Every execution step in this report is `PENDING-LEAD-EXECUTION`.** GLM cannot run the
> PowerShell harness on this host (and `python`/`py_compile` need interactive approval in
> this unattended session). No transcript, byte-count or digest below was produced by
> running code; predictions are reasoned from the source. The Lead re-runs the harness in
> `SELF_QA_PATHSCOPE.md` to generate the real round-3 evidence.

---

## 1. The defect (C-1)

An assignment prefix / declaration-builtin assignment / `env` assignment whose value names
a path the dynamic loader or an interpreter opens (`LD_PRELOAD=/etc/evil.so cat "$ROOT/f"`,
`export LD_PRELOAD=/etc/evil.so`, `env LD_PRELOAD=/etc/evil.so cat "$ROOT/f"`) was **silently
dropped**: the out-of-allowlist path appeared nowhere in the output and the verdict was
`PASS rc=0`. Per the audit's contract item 2 ("any surviving silent sink is CRITICAL"),
this is the one blocking item. It fails **open** — the one direction the round-2 fail-closed
design promised never to fail in — because an assignment is neither an option nor a command,
so it fell through every registered grammar.

**Root cause, one defect class, three holes** (all in `pathscope_prover.py`):

| hole | site (pre-repair line) | what it did |
|---|---|---|
| assignment prefix loop | `analyze_command`, ~L2293 | `while … self.assignment(tokens[index]): index += 1` advanced past `NAME=value` tokens; the value was never inspected for path content |
| declaration builtins | `analyze_command`, ~L2299 | `local/declare/typeset/export/readonly` registered only bare names; an arg like `LD_PRELOAD=/etc/evil.so` matched `assignment()` and was skipped |
| `env` wrapper | `analyze_wrapped`, ~L1519 | `if ASSIGN_RE.fullmatch(rendered): index += 1; continue` skipped `NAME=value` args with no inspection |

## 2. The repair

A single new helper, called at all three holes. **Fail-closed on the construct, not on a
variable-name allowlist** (the auditor's explicit direction; avoids repeating the round-1
`NO_PATH_COMMANDS` mistake).

`pathscope_prover.py`, new method `record_assignment_value(token, primitive)` (after
`assignment()`):

- re-parses the token with `ASSIGN_RE`, expands the rhs via `expand_word`;
- **resolved path-shaped value** (starts with `/`, `./`, `../` — the codebase's existing
  path-shape convention at L2244/L2420) → a `PATH` row via `record_path_text`, bound to the
  assignment site (line + primitive);
- **value not statically resolvable** → a `kind=coverage` record;
- **known non-path value** (`IFS=:`, `count=1`) → carries no path, left alone.

Three call sites:

1. **Prefix loop** — `self.record_assignment_value(tokens[index], "assignment prefix")`
   inside the `while`. The bare-assignment early `return` (b08 `X=/etc/passwd`) is now
   covered because the record is emitted *during* the loop iteration, before the return.
2. **Declaration builtins** — the loop was restructured from
   `if not self.assignment(token) and NAME_RE.fullmatch(…)` to
   `if self.assignment(token): record…; continue` else register bare name. The primitive is
   `f"{first.text} assignment"` (e.g. `export assignment`). Side effects are unchanged.
3. **`env` wrapper** — `self.record_assignment_value(args[index], "env assignment")` before
   the `index += 1; continue`.

Array (`A=(…)`), compound (`X+=`) and arithmetic (`((…))`) assignments are pre-classified
earlier (`run()` ~L2608, `normalize_control_tokens` ~L2555/2533) and are unaffected: an
array token's rhs is empty (`A=`) or non-path-shaped, compound `+=` does not match
`ASSIGN_RE`, and arithmetic is rewritten to a separator before `analyze_command`.

## 3. Self-verification (source-level; no execution)

- **Manual trace of all seven P9 fixtures** through the repaired control flow (see §5). The
  five FORBID rows and two control rows behave as asserted.
- **Call-site completeness:** grep confirms `self.assignment(` has exactly two call sites
  (prefix loop, declaration loop) and `ASSIGN_RE.fullmatch` has exactly one skip site
  (`analyze_wrapped`); all three are patched. `parse_constants` (L647) uses `ASSIGN_RE` but
  is the constants-file parser, not a code path.
- **Syntax:** the four edits are a method definition plus three single-line insertions into
  existing blocks; structure and indentation verified by re-reading each site. `python -m
  py_compile` + `ast.parse(feature_version=(3,12))` were **attempted but require interactive
  approval** in this unattended session — `PENDING-LEAD-EXECUTION` (the Lead's re-run
  re-derives `ast.parse` over the new bytes anyway).
- **Determinism:** the helper adds no non-deterministic input; `expand_word`/`canonical_path`
  are pure. The new `assign_prefix` determinism pair in the harness will confirm this.

## 4. Files changed

| file | change |
|---|---|
| `pathscope_prover.py` | +`record_assignment_value`; 3 call-site edits (prefix loop, declaration builtins, `env` wrapper). Identity bytes/SHA **change** — Lead re-derives. |
| `SELF_QA_PATHSCOPE.md` | +round-3 stale banner; +7 P9 fixtures + 7 CASES + `assign_prefix` determinism pair; +§"Round 3 — C-1 repair" assertion table; F-3 wording corrected per the auditor's supplied text; D026 heading marked STALE. No transcript was rewritten or fabricated. |
| `PATHSCOPE_GLM_T1_R3_REPAIR_REPORT_2026-08-13.md` | this report (new) |

## 5. P9 fixtures added and asserted behaviour (`PENDING-LEAD-EXECUTION`)

Per D026, the five FORBID rows are the falsification: **R1 RED = silent `PASS rc=0` →
R2 GREEN = `rc=1` with the path visible.** The two control rows guard against false
positives.

| fixture | fragment | hole | R1 RED (predicted) | R2 GREEN (predicted) |
|---|---|---|---|---|
| `assign_prefix` | `LD_PRELOAD=/etc/evil.so cat "$ROOT/f"` | prefix | rc 0 (sink) | rc 1 — `/etc/evil.so` FORBID; `/safe/f` ALLOW-LEXICAL |
| `assign_prefix_allow` | `LD_PRELOAD="$ROOT/ok.so" cat "$ROOT/f"` | prefix | rc 0 (path invisible) | rc 0 — `/safe/ok.so` + `/safe/f` ALLOW-LEXICAL |
| `assign_bare` | `X=/etc/passwd` | prefix (bare) | rc 0 (no row) | rc 1 — `/etc/passwd` FORBID |
| `assign_benign` | `IFS=: cat "$ROOT/f"` | prefix (control) | rc 0 | rc 0 — `/safe/f` ALLOW-LEXICAL |
| `assign_export` | `export LD_PRELOAD=/etc/evil.so`; `cat "$ROOT/f"` | declaration | rc 0 (sink) | rc 1 — `/etc/evil.so` FORBID |
| `assign_env` | `env LD_PRELOAD=/etc/evil.so cat "$ROOT/f"` | env wrapper | rc 0 (sink) | rc 1 — `/etc/evil.so` FORBID |
| `assign_multi` | `LD_PRELOAD=/etc/a.so BASH_ENV=/etc/b.sh cat "$ROOT/f"` | prefix ×2 | rc 0 (both dropped) | rc 1 — `/etc/a.so` + `/etc/b.sh` FORBID |

R1 behaviour (especially `assign_env`/`assign_export`) is a **prediction** and must be
measured; R2 GREEN is reasoned from the patched source.

## 6. Impact on the real blocks (`RP6-P0.sh`, `RP7-WPI-RO.sh`)

Predicted **nil-to-negligible**. The blocks' assignment prefixes are `<PIN-AT-FREEZE>`
placeholders, `$VAR`/parameter references, or arithmetic — none a hardcoded
out-of-allowlist absolute path (grep of the two scripts confirms no `NAME=/abs/path`
prefix). Allowlisted resolved values add only `ALLOW-LEXICAL` rows (no rc change); both
blocks already `REJECT rc=3`. The pinned-blob runs remain **historical regressions** per
audit §3. **Lead confirms on re-run.**

## 7. Known residual (disclosed for the auditor's call)

This fix closes every demonstrated silent sink — the audit's reproducer and **all** the
`/etc/…`-valued b-probes (b01–b03, b07–b12, b14). It does **not** flag a **bare soname**
with no slash, e.g. `LD_PRELOAD=libc.so`: the loader resolves that via runtime search paths
(`ld.so.cache`, `/lib`, …) which a lexical prover cannot statically resolve, and `libc.so`
is not path-shaped by the codebase's own convention (`cat libc.so` is not flagged either).
This matches the auditor's stated "minimally" (path-shaped → PATH row; unresolvable →
coverage) and the prover's lexical contract. If the auditor wants bare-soname loader
variables covered too, that is a **supplementary** loader-variable-name check layered on top
of (not replacing) this construct-level path check — flag for a possible round 4, not done
here.

## 8. Follow-ups left for the Lead / re-audit (rode-along items, not blocking)

- **NIT-1 (asymmetry):** `ENDPOINT` rows still print bare `verdict=ALLOW` where `PATH` rows
  print `ALLOW-LEXICAL`. One-token render change for symmetry; out of C-1's scope, left
  untouched.
- **U-3:** the three Python-3.14.2 / `ast.parse(3,12)` / no-3.12 claims at
  `SELF_QA_PATHSCOPE.md:8-10` were measured TRUE by the audit; remedy is a citation or
  three added harness probes — documentary only.
- **NIT-2 / NIT-3:** one-sentence doc notes (benign zero-record rows; effort field). Doc
  only.
- **Identities / transcripts / digests:** regenerate after re-run; update the Identities
  table with the round-3 `pathscope_prover.py` bytes + SHA-256, and the 511/644 line counts
  and the (now four) DETERMINISM lines.

## 9. What the Lead must do

1. Run the harness in `SELF_QA_PATHSCOPE.md` (it now includes the P9 fixtures + CASES +
   the `assign_prefix` determinism pair). Confirm the seven P9 rows match §5 (five RED→GREEN
   FORBID transitions; two controls unchanged).
2. Re-derive the round-3 `pathscope_prover.py` identity (bytes + SHA-256) and update the
   Identities table; confirm `ast.parse(feature_version=(3,12))` still succeeds.
3. Re-confirm the existing 62-fixture D026 rc values are unchanged (P9 fixtures are the only
   additions) and that the real-block verdicts are not newly perturbed (§6).
4. Dispatch the round-3 re-audit (T1, alternate flagship) over the new bytes.

— end of report —
