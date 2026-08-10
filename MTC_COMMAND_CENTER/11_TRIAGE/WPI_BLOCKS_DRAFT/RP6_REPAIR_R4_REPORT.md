# RP6-P0 repair round 4 — report

Implementer: `claude-opus-5`, xhigh, fresh session, 2026-08-10. Contract:
`KICKOFF_RP6_REPAIR_R4.md` and the four required findings of
`RP6_CODEX_T0_AUDIT_2026-08-10.md` (BLOCK: 4), whose "Required repair" text binds.

Owner authorised exceeding the recorded T0 cap for the identical venv
site-startup security class already resolved on RP7 (2026-08-10 ~17:15); the Lead
extended that authorisation to RP6-P0. No host contact, no network command, no
SSH/SCP, no RUNID, no deployment, no broker/backtest/Pine/parity/MTC action, and
no commit. Local Git Bash 5.2.37 `--noprofile --norc` execution only.

## Byte identity

| | bytes | SHA-256 |
|---|---:|---|
| baseline (round 3, the audited object) | 71743 | `2d9b166eacfc39ebe0d8d89edb5860876ccc4d9f0ff97f9e10a228dbcf96289e` |
| repaired (round 4) | 85540 | `e93d07adcc9ae03ad15e0b0f10c76be54517251ab461c8fe789d160072d253c6` |

The baseline was verified against the kickoff hash and byte count **before the
first edit**, and again inside the D026 fence from `git show bbb40ab6:<path>`,
which is the immutable revision the audit froze. `bash -n` returns 0 at the
repaired bytes. Every file written this round is UNIX LF; no CR byte exists in any
of them. `git diff --numstat`: block 253 insertions / 58 deletions. This round's
prereg-draft change is **four modified table rows** (§8.1 rows 1, 2, 3 and 9) —
`git diff -U0` hunks `@@ -514,3 +623,3 @@` and `@@ -522 +631 @@`. The draft's raw
numstat is larger (141/34 at the time of writing) because a CONCURRENT session
extended §4, §5 and §6 while this round was in progress; none of that is mine, and
nothing outside the four §8.1 rows was written here.

The frozen RP7 basis F3 targets was verified the same way, inside the fence,
before any comparison: `RP7-WPI-RO.sh` at commit `d6a976aa`, SHA-256
`23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad`, 70941 bytes —
exactly the gated values the kickoff records.

## Files touched

`RP6-P0.sh`, `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`,
`RP6_FULLBLOCK_REPAIR_REPORT.md`, this report, and four §8.1 rows of
`WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`. Nothing else.
`RP7-WPI-RO.sh`, `SELF_QA_RP7.md`, `STATUS_RP7.md` and the transport tree were
**read** — the frozen RO basis above — and never written.

## The four findings

### F1 (HIGH) — the "read-only" interpreter probe executed unverified venv startup code

**Closed.** `-I` implies `-E`, `-P` and `-s`; it does not imply `-S`. The probe
therefore imported `site`, processed the judged venv's `site-packages`, and
executed every `import` line in its `*.pth` files — and any
`sitecustomize`/`usercustomize` module in that tree — with this login's authority,
before the `-c` body was compiled. Three things changed:

- the launch is now `"$P0_ENV" -i LC_ALL=C "$py" -I -S -c …`, cleared environment
  retained;
- the `-c` body refuses to report a version unless `sys.flags.isolated` and
  `sys.flags.no_site` are both set, emitting `P0PY_STARTUP_UNPROVEN isolated=<i>
  no_site=<n>` instead, which the shell adjudicates BEFORE parsing any result as
  `P0_STOP reason=interpreter_startup_not_isolated … expected=isolated_and_no_site`
  (a STOP, never a host FAIL: the interpreter ran, but read-only scope was not
  established);
- every sentence the old launch could not support is corrected — the
  `MUTATION SURFACE` header paragraph, the section comment that claimed "nothing
  is written and nothing is installed", the evidence line (now
  `site_startup=disabled startup_flags=self_verified_isolated_and_no_site
  venv_pth_and_sitecustomize=not_executed …
  interpreter_binary_behaviour=not_attested`), and the terminal claim, where
  `mutation=none_in_this_block` becomes
  `mutation=no_filesystem_write_primitive_in_this_shell_source
  child_side_effects=not_attested_except_venv_startup_which_is_disabled
  interpreter_launch=isolated_and_no_site`, with
  `behaviour_inside_any_executed_tool_binary` added to `does_not_establish`.

**Falsified, executed, on real bytes.** A real `python -m venv` environment whose
`site-packages` carries a real one-line executable `zzforge.pth`; the block's real
`p0_assert_interpreter_executable`; the real `env -i`; the real interpreter. The
`.pth` is the only fixture.

| arm | result |
|---|---|
| pre-fix bytes (`-I`), forged `.pth` | rc 0, `P0_interpreter … exec=ok`, **`MARKER_CREATED=yes MARKER_CONTENT=[PTH_EXECUTED]`** |
| repaired bytes (`-I -S`), same `.pth` | rc 0, accepted line with `site_startup=disabled`, `MARKER_CREATED=no` |
| repaired bytes with ` -S` deleted (mutant) | `MARKER_CREATED=yes` **and** rc 3, `interpreter_startup_not_isolated … [P0PY_STARTUP_UNPROVEN isolated=1 no_site=0]` |
| pre-fix bytes, `.pth` removed (control) | rc 0, `MARKER_CREATED=no` |

The first row is the finding, reproduced: arbitrary code from the object under
test wrote a file while the block reported success. The third row is why the fix
cannot be silently undone. The fourth proves the marker comes from the forged line
and nothing else.

### F2 (MEDIUM) — row 9 had no timeout and could hang without any reasoned STOP

**Closed.** `p0_assert_system_manager_ready` now launches

```text
env -i LC_ALL=C <pinned timeout> --signal=TERM --kill-after=5s 10s \
    <pinned systemctl> --system --no-pager show --property=Version
```

with the cleared-environment exec FIRST and the pinned `timeout` as its argument,
exactly as the preregistered probe-execution-environment rule requires — the
process that decides whether the query was bounded runs under the same cleared
environment as the query it bounds. `P0_MANAGER_QUERY_BUDGET_S=10` and
`P0_MANAGER_QUERY_KILL_AFTER_S=5` are frozen block literals, deliberately not
operator inputs. Status mapping, all under `system_manager_unreachable` at exit 3:
124 → `manager_query_deadline_exceeded`, 137 →
`manager_query_killed_after_deadline`, 125 → `bounding_wrapper_failed`, 126/127
unchanged, anything else `manager_query_nonzero_status`. `budget_s` and an
`elapsed_s` from the `SECONDS` builtin are recorded; `elapsed_s` is diagnostic
only, at whole-second resolution, and no branch reads it — `timeout`'s status
decides.

**Falsified, executed**, with the real GNU `timeout` 8.32 and a stalling shim, the
external watchdog placed OUTSIDE the delivered function exactly as the audit did:

```text
pre-fix,  stalled : output=[]  EXTERNAL_WATCHDOG_RC=124 P0_STOP_LINES=0
repaired, stalled : P0_STOP reason=system_manager_unreachable rc=124
                    detail=manager_query_deadline_exceeded budget_s=10
                    elapsed_s=10 text=[]   rc 3, watchdog 40 s never fired
budget literal raised to 600 s (mutant): EXTERNAL_WATCHDOG_RC=124 P0_STOP_LINES=0
pre-fix,  responsive : rc 0, response_value=[252]
repaired, responsive : rc 0, response_value=[252] … bound=… budget_s=10 kill_after_s=5
```

The mutant matters: it shows the recorded literal — not the shim, not the harness
— is what bounds the query. The two responsive arms show the bound did not turn a
healthy manager into a STOP.

### F3 (MEDIUM) — the RO tool inventory was stale, omitted `timeout`, and rejected its pin

**Closed.** The inventory is no longer written from prose. It is now

```text
P0_RP7_RO_TOOLS="stat readlink env find sha256sum systemctl ss curl timeout python3"
P0_P0_ONLY_TOOLS="id getent"
P0_RO_TOOLS="$P0_RP7_RO_TOOLS $P0_P0_ONLY_TOOLS"
```

— the RO half a mirror of what the FROZEN `RP7-WPI-RO.sh@d6a976aa` validates and
binds, the second half the P0-only remainder. `grep` and `awk` are removed:
neither stage invokes either (this block counts literal substrings with builtins,
and the budgeted-sweep clock `awk` was listed for is not reachable from any tool
the frozen RO block pins). `timeout` becomes a resolved first-class tool
(`P0_TIMEOUT`), which F2 then uses. The count is 12, the terminal claim says what
the twelve are and where the ten came from, and `P0_tool_inventory` now carries
`ro_half=[…] p0_only_half=[…] ro_basis=RP7-WPI-RO.sh@d6a976aa:23e55667:70941
trusted_python_pin=<yes|no>`.

`python3` is inventoried but **never executed by P0**. Two consequences were
handled rather than glossed:

- its pin value is bound to a new freeze-gate literal
  `P0_FIXED_TRUSTED_PYTHON` (the RP7 `WPI_FIXED_TRUSTED_PYTHON` value), so P0
  cannot admit an interpreter different from the one the RO stage's two accepting
  adjudicators will run under;
- because that pin is the resolved non-symlink leaf while PATH still spells
  `/usr/bin/python3`, exact pin/PATH equality would have made a complete RP7 pin
  set **fail** in P0. `p0_resolve_tool` therefore admits, for `python3` ALONE, a
  pin that the PATH-resolved object canonicalises to; the resolution token records
  it as `pinned_absolute_via_canonicalized_path_symlink`, the pin (the object the
  RO stage invokes) becomes the recorded path, and a shadowing `python3` — which
  canonicalises somewhere else — still STOPs. Every other tool keeps exact
  equality.

**Falsified, executed.** A drift test re-derives the RO half from the frozen bytes
in three independent places inside them (the `WPI_TOOL_PINS` validator alternation
at `:594`, the binding loop at `:611`, the declared count at `:610`) after
verifying their SHA-256 and byte count; all three read the same ten names, and
P0's RO half is identical. The executable half drives P0's **real** pin validator:

```text
pre-fix  + complete RP7 pin set : P0_STOP reason=input_pin_unknown_tool name=P0_TOOL_PINS
                                  tool=timeout inventory=[stat readlink id env find grep
                                  sha256sum awk systemctl ss curl getent]      <- the audit's own line
repaired + complete RP7 pin set : P0_PINS_ACCEPTED count=10 trusted_python_pin=yes
repaired + python3 pin, freeze literal unfilled : input_pin_freeze_unfilled tool=python3
repaired + python3 pin != frozen value          : input_pin_not_frozen_trusted_python
repaired + a `grep` pin                          : input_pin_unknown_tool tool=grep
pre-fix  + grep/awk pins                         : accepted, rc 0            <- the stale contract
```

plus the canonicalisation arms: the `python3` link is admitted, a decoy `python3`
earlier in PATH STOPs with `tool_pin_mismatch … canonical=[…]`, and the same
divergence on `stat` still STOPs with no `canonical=` field, proving the allowance
did not leak.

### F4 (LOW/MED) — getent error/no-match divergences did not match the §8.1 grammar

**Closed, both halves.**

1. `p0_resolve_passwd` exports `P0_PW_RC`. The status sentinel is read from the
   **last** capture field, so even a NUL-corrupted capture — where getent's own
   NUL adds fields at the front — still records the resolver's real status
   instead of losing it. `na` survives only for the two shapes that fail before
   any status can be read (lost sentinel, unparseable status record) and is never
   a stand-in for an available status. Both `identity_unresolvable` callers, for
   both accounts, now emit `rc=<n|na>`.
2. The valid-no-match token was aligned by the **first** of the two options the
   finding offers: `state_account_resolution_unexpected` is preregistered verbatim
   in §8.1 row 3 rather than replaced in the block. Reason, stated as the kickoff
   requires: positive absence of a *dynamically allocated* account is a host
   observation about the allocation, not an inability to evaluate, and folding it
   into `identity_unresolvable` would erase exactly the distinction rows 2-3 exist
   to make. The row now records the token, its full field list, and why it carries
   no `rc=` field.

**Falsified, executed**, with eight **exact whole-line** assertions — not
substrings, because a substring assertion is precisely what let the old 27-case
harness pass while the field was missing — each with its RED twin on the audited
pre-fix bytes:

```text
rc 0 parse error   P0_STOP reason=identity_unresolvable account=mtc-bridge rc=0 detail=[mtc-bridge:x:999:988:svc]
rc 2 no-match      P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
rc 2 no-match      P0_STOP reason=identity_unresolvable account=gatea rc=2 detail=getent_valid_no_match_for_route_login
rc 2 diagnostic    P0_STOP reason=identity_unresolvable account=mtc-bridge rc=2 detail=[getent: sss_nss: connection to the name service timed out]
rc 2 diagnostic    P0_STOP reason=identity_unresolvable account=gatea rc=2 detail=[getent: nss module returned SERVBUSY for gatea]
other nonzero      P0_STOP reason=identity_unresolvable account=mtc-bridge rc=5 detail=[mtc backend unavailable]
other nonzero      P0_STOP reason=identity_unresolvable account=gatea rc=5 detail=[gatea backend unavailable]
NUL capture        P0_STOP reason=identity_unresolvable account=mtc-bridge rc=2 detail=[nul_byte_in_merged_capture]
```

The audit's own rc-5 fixtures and marker are reproduced in both directions:
`contains_rc_field=0` on the pre-fix bytes for both accounts, `1` on the repaired
bytes. The healthy path still admits at rc 0.

## Draft edits (four §8.1 rows, nothing else)

The kickoff scopes draft edits to "§8.1 rows a fix names".

- **Row 1** — the preregistered inventory is named for the first time (the ten
  frozen RO tools plus `id`/`getent`, `grep`/`awk` removed, with the frozen basis
  identity), together with the pin-table divergence grammar: `input_pin_unknown_tool`,
  `tool_pin_mismatch` (+ `canonical=` for the python3 allowance),
  `input_pin_freeze_unfilled` and `input_pin_not_frozen_trusted_python`.
- **Rows 2 and 3** — `rc=<n>` becomes `rc=<n|na>` with the mandatory-field rule and
  the exact meaning of `na`, and the gatea valid-no-match line is recorded.
- **Row 3** — additionally preregisters `state_account_resolution_unexpected …`
  verbatim, states that it is deliberately distinct from `identity_unresolvable`,
  and states why it carries no `rc=`.
- **Row 9** — records the executable deadline: the exact launch shape, both frozen
  literals, the 124/137/125 detail tokens, and the plain statement that without the
  bound a stalled manager produces no reason line, no rc and no verdict.

Nothing outside those four rows was touched. Row 8 and rows 4-7 are unchanged; the
existing "Probe execution-environment rule" paragraph already required `-I -S`
generically, so F1 needed no new prose there. The two anchors the full-block fence
greps (row 1's `rc=<n|na>` form, row 3's unified `identity_unexpected` form) were
preserved verbatim and re-verified at `grep -c` = 1 each.

## Self-QA

`SELF_QA_RP6.md` carries the round-4 D026 fence (102 assertions, all four
findings) and the superseding C13 arm harness (27 cases), each with its complete
real transcript. Both were re-extracted from the markdown and re-run: extraction
byte-identical to the file that ran, both green.

Mandated set after this round, all executed against `e93d07ad…` / 85540 B:

```text
sed -n '952,1035p'   SELF_QA_RP6.md -> rc 0, backstop cases=4 PASS
sed -n '1678,2068p'  SELF_QA_RP6.md -> rc 0, 39 ASSERT_MET / 0 UNMET, full-block PASS
sed -n '2286,2319p'  SELF_QA_RP6.md -> rc 0, freeze-literal gate PASS
sed -n '2545,2989p'  SELF_QA_RP6.md -> rc 0, 102 ASSERT_MET / 0 UNMET, R4 D026 PASS
sed -n '3353,3518p'  SELF_QA_RP6.md -> rc 0, C13_R4B cases=27 PASS
```

**Two previously mandated fences are now RED, and that is the point.** The C13 R3
fence (lines 664-787, 3 `CASE_BAD`) and the C13 R4 fence (lines 1181-1346, 6
`CASE_BAD`) assert the pre-round-4 `identity_unresolvable` grammar by substring.
The F4 repair makes `rc=` mandatory on that line, so exactly the assertions that
lacked the required field now fail. Both sections are left byte-untouched as the
honest record of their own rounds, their failing output is recorded in
`SELF_QA_RP6.md`, and the R4b harness carries all 27 of their cases with the three
broken strings corrected — twelve `run_case` lines updated in total:
`repaired`/`prerepair` × {`mtc_rc2_diag`, `mtc_rc2_partial`, `gatea_rc2_diag`} and
`repaired`/`prer4` × {`mtc_rc2_newline`, `mtc_rc2_newlines3`, `gatea_rc2_newline`}.
The one `prer4 mtc_rc2_diag … GREEN` case deliberately keeps the old string,
because its whole purpose is to assert what the round-3 bytes emit.

Disclosed substitutions in the new fence, all narrow: `systemctl` and `getent` are
shims (this Windows-hosted session has neither, and neither is the subject of a
finding), and the `python3` pin/PATH canonicalisation arm renders its symlink
through a deterministic `readlink` shim because Git Bash cannot create a native
symlink here. Nothing about interpreter selection, flag words, startup behaviour,
`env -i`, the real deadline, or the frozen RP7 bytes is simulated.

## Freeze-gate inputs (six, one new)

`P0_FIXED_ATTESTED_USER_NS`, `…MNT_NS`, `…PID_NS`, `…NET_NS`, `…ROOT_MOUNT_ID`,
and new this round **`P0_FIXED_TRUSTED_PYTHON`** — the resolved non-symlink leaf
behind `/usr/bin/python3`, the same deploy-channel value RP7 pins as
`WPI_FIXED_TRUSTED_PYTHON`. All six must come from the deploy channel; until they
do, the block necessarily STOPs and no end-to-end `P0 PASS` can or should exist.
`P0_MANAGER_QUERY_BUDGET_S` / `P0_MANAGER_QUERY_KILL_AFTER_S` are NOT freeze-gate
inputs: they are frozen design literals with real values, held in the block so the
environment under test cannot raise its own deadline.

## What this round does not establish

No staging execution, no `/proc` namespace objects, no reachable system manager,
no real `getent`, no `shellcheck` (not installed), and no accepting end-to-end
arm. The `.pth` behaviour was observed on local CPython 3.14.2; the identical
startup contract is documented for the target Python 3.12 in the primary sources
the audit cites, and the block's own `sys.flags.isolated`/`sys.flags.no_site`
guard makes the requirement self-checking on the target rather than assumed. P0
still does not attest the provenance of any tool binary, and now says so
explicitly rather than implying mutation-freedom it cannot observe.

Acceptance belongs to fresh independent `claude-opus-5` xhigh and `gpt-5.6-sol`
xhigh re-audits that execute the mandated suite. The block remains a draft: not
frozen, not accepted, not dispatchable, and carrying no host-contact authority.
