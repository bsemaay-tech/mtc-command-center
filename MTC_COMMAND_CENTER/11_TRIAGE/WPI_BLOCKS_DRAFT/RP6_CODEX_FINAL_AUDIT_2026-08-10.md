BLOCK: 3 findings

# Codex final T0 flagship audit — `RP6-P0.sh` round-4 bytes

Date: 2026-08-10  
Auditor: Codex `gpt-5.6-sol`, `xhigh`, fresh flagship slot  
Tier: **T0** — defensive staging preflight / host execution-domain surface  
Applied auditor contract: two independent flagships (`claude-opus-5` and
`gpt-5.6-sol`) at xhigh; this Codex slot was performed directly under owner
amendment A2/A2a, with no sub-delegation.

The executable audit basis is `RP6-P0.sh` at commit
`945e20f5833abf422cc98c0970b5867aaabae317`. Concurrent work advanced repository
`HEAD` during the audit, but `git diff 945e20f5 --` over all five RP6 target files
remained empty. The kickoff calls the preregistration draft “current” while the
owner explicitly warns that it is under concurrent edit; I therefore snapshotted
the current draft for the row-grammar comparison only:

```text
RP6-P0.sh sha256=e93d07adcc9ae03ad15e0b0f10c76be54517251ab461c8fe789d160072d253c6
RP6-P0.sh bytes=85540 cr=0 lf=1523 bom=false bash_n_rc=0
current prereg sha256=96a91673e709f3697b5fe69f5cb5199b8845f8fe072503ecaee12821c26fb789
current prereg git_blob=d5d4a24e86b1079d7bf43f1b2dd251bea6401d00 bytes=104294
```

No host, SSH, network, deployment, broker, backtest, Pine, parity, MTC, or
trading action was performed. All adversarial fixtures were local and temporary.
The only repository write by this audit is this report.

## Verification rows

| V | Verdict | Independent evidence |
|---|---|---|
| **V1 — F1 interpreter startup** | **PASS** | A fresh real venv carried an executable `.pth` that writes a marker. Exact repaired function: rc 0, marker absent, `site_startup=disabled`. Comparison-only mutation deleting `-S`: marker present and rc 3 with `interpreter_startup_not_isolated ... P0PY_STARTUP_UNPROVEN isolated=1 no_site=0`. The flag guard is load-bearing. |
| **V2 — F2 bounded row 9** | **PASS** | Exact pre-fix function plus a 60-second stall needed an external 2-second kill: external rc 124, zero `P0_STOP` lines. Exact repaired function returned by itself after 10 seconds: rc 3, exactly one `P0_STOP reason=system_manager_unreachable rc=124 detail=manager_query_deadline_exceeded budget_s=10 ...`; the 20-second outer watchdog did not fire. Responsive control returned rc 0 with `bound=pinned_timeout_inside_cleared_env`. |
| **V3 — F3 frozen RO inventory** | **PASS for the specified closure; whole-block finding F1 remains** | I re-derived frozen `RP7-WPI-RO.sh@d6a976aa`: SHA-256 `23e55667...a0aad`, 70941 B, validator set = binding set = `stat readlink env find sha256sum systemctl ss curl timeout python3`, count 10. P0's RO half is identical; complete ten-pin input was accepted at rc 0 with `trusted_python_bound=yes`; removing `timeout` made the independent set comparison fail. |
| **V4 — F4 resolver status and grammar** | **PASS** | My rc-5 shims produced exact `identity_unresolvable account=gatea rc=5 ...` and `account=mtc-bridge rc=5 ...`, both rc 3. The current prereg snapshot carries `rc=<n|na>` on both resolver rows and preregisters the exact `state_account_resolution_unexpected ... detail=getent_valid_no_match` row-3 token. |
| **V5 — independent rows 1–9 / whole-block sweep** | **FAIL** | Row-8 comparison and call-removal mutations remain discriminating: the former reaches the false `binding=deploy_attested_exact` arm; the latter reaches `MANAGER_RAN`, while shipped bytes stop first. Numeric uid/gid comparisons, whole-word capability intersection, NUL-sentinel handling, status-before-output ordering, venv parent-before-leaf ordering, and the stated shell-source read-only boundary hold. Three independent gaps remain: findings F1–F3 below. |
| **V6 — QA integrity** | **PASS** | Mandatory fences, literally extracted: backstop rc 0 / 4 cases PASS; full-block rc 0 / 39 `ASSERT_MET`, 0 unmet; freeze rc 0; R4 D026 rc 0 (its fail gate can return 0 only with all 102 assertions met); C13 R4b rc 0 / 27 cases PASS. The older C13 R3 and R4 fences independently returned rc 1 with exactly 3 and 6 `CASE_BAD`, respectively, matching their explicit superseded-RED disposition. This is honest history, not an undisclosed failure. |
| **V7 — frozen mechanics** | **PASS** | SHA-256, byte count, LF-only form, no BOM, and `bash -n` all independently re-derived as shown above. RP6 targets remained byte-identical to `945e20f5`. |

## Required findings

### F1 — HIGH — the sixth freeze gate is optional when the `python3` pin is omitted

`RP6-P0.sh:437-480` describes `P0_TOOL_PINS` as optional. The only check of
`P0_FIXED_TRUSTED_PYTHON` is inside `if [ "$p0_pin_name" = python3 ]` at
lines 471-476. There is no post-loop requirement that `python3` was present;
`P0_TRUSTED_PYTHON_BOUND=no` is merely printed at lines 722-724. Thus the exact
freeze-gate item added to bind RP7's accepting adjudicators can be bypassed by
omission, contradicting the kickoff/status statement that all six
`<PIN-AT-FREEZE>` literals independently prevent end-to-end GREEN.

Executed falsification used the shipped input loop:

```text
PIN_NONE      rc=0 PIN_INPUT_ACCEPTED count=0 trusted_python_bound=no fixed=[<PIN-AT-FREEZE>]
PIN_NO_PYTHON rc=0 PIN_INPUT_ACCEPTED count=1 trusted_python_bound=no fixed=[<PIN-AT-FREEZE>]
PIN_WITH_PYTHON rc=3 P0_STOP reason=input_pin_freeze_unfilled tool=python3 name=P0_FIXED_TRUSTED_PYTHON ...
```

The polarity is backwards: supplying the security-relevant pin engages the gate;
omitting it disables the gate. The other five placeholders still stop the draft
today, but after they are filled this sixth placeholder is not load-bearing.

Required repair: after parsing pins, require an explicit `python3` entry bound to
`P0_FIXED_TRUSTED_PYTHON` (or require the complete frozen RP7 pin set) before any
host observation. Add D026 omission evidence: current bytes admit the missing-pin
fixture, repaired bytes must emit a named rc-3 STOP, and the complete pin set must
remain GREEN.

### F2 — MEDIUM — PATH executables are accepted and reported as sourced RP0 functions

`RP6-P0.sh:331-346` uses `command -v` to assert that
`rp0_require_safe_component` and `rp0_allocate_evidence_dir` were sourced. That
does not establish command type: `command -v` also accepts executable files from
PATH. The block then executes the first object and prints
`P0_prereq lib=sourced bootstrap=ran`, even when neither function exists. This
contradicts lines 119-121 and 323-347, which say the accepted library predicate
is genuinely sourced and functional.

Executed falsification put two executable files of those names first in PATH;
the first wrote a marker and returned 0:

```text
P0_prereq lib=sourced bootstrap=ran run_id=RUN1 stage=STAGE1 dir=/fixture/dir leaf=/fixture/log
PREREQ_FUNCTION_TYPES safe=file alloc=file marker=yes
PREREQ_EXTERNAL_RC=0
```

This is also a pre-inventory child-execution channel: a PATH file can approve
unsafe identifiers and run arbitrary child behavior before P0 has established
any tool premise.

Required repair: use a builtin type assertion (`declare -F` or an exact
`type -t ... == function` check) for both RP0 symbols before calling either.
Add a PATH-shadow RED fixture proving files/aliases cannot satisfy the source
precondition, while actual sourced functions still pass.

### F3 — MEDIUM — malformed forbidden-GID input is pathname-expanded and can be admitted

The raw `P0_FORBIDDEN_GIDS` value is never grammar-checked before the unquoted
loop at `RP6-P0.sh:395`; Bash therefore performs pathname expansion before
`p0_require_uint` sees each item. The later capability loop at lines 842-845
repeats the same expansion. A malformed operator value can consequently be
rewritten by the inherited working directory into a numeric ledger, despite the
block's rule that malformed preregistered input must STOP and its terminal
disclosure that cwd is caller-inherited.

Executed falsification used the exact validator with `P0_FORBIDDEN_GIDS='*'`:

```text
empty cwd:   rc=3 P0_STOP reason=input_charset name=P0_FORBIDDEN_GIDS_ENTRY expected=decimal_digits
cwd with entries named 0 and 988:
             rc=0 FORBIDDEN_INPUT_ACCEPTED raw=[*] count=2
```

The same raw input changes verdict solely with cwd contents. A cwd containing a
different set of numeric names can silently weaken which groups are checked.

Required repair: validate the complete raw value against an exact digits-plus-
separator grammar before expansion, and parse with pathname expansion disabled
or an array mechanism that cannot glob. D026 must drive the wildcard fixture in
both empty and numeric-name directories; repaired bytes must STOP identically.

## Ten-pattern attack summary

| Pattern | Result |
|---|---|
| 1 — STOP is not a result | Completed host probes retain truthful polarity; F1 and F3 instead expose missing input STOPs. |
| 2 — whose kernel answered | Five external-attestation comparisons and row-9 ordering are load-bearing; the procfs/nsfs residual remains explicitly disclosed. |
| 3 — leaf is not path | Venv root precedes leaf; canonical/symlink limitations are stated. No new finding. |
| 4 — privileged child environment | `-I -S` and cleared manager launch pass; F2 exposes a separate pre-inventory PATH child accepted as a sourced function. |
| 5 — parser matches grammar | Getent/NUL parser passes; F3 is a concrete shell-expansion-before-validation parser defect. |
| 6 — status before stdout | Manager, getent, stat, readlink, and id captures adjudicate status first. |
| 7 — nonzero read is not EOF | No line-reader EOF loop exists; NUL-delimited resolver capture rejects extra records. |
| 8 — name is not identity | Admission comparisons remain numeric; returned names remain diagnostic by the preregistered contract. |
| 9 — sentence outruns probe | F1 and F2 directly contradict the freeze-gate and `lib=sourced` sentences. |
| 10 — evidence that cannot fail | Five mandatory fences executed; mutation polarities are active; the two historical RED fences fail exactly as disclosed. |

## Terminal disposition

The four round-4 Codex findings are closed, but the independent whole-block sweep
found three required repairs. This is a non-accepting T0 flagship verdict. Because
round 4 already exceeded the ordinary T0 cap under a bounded owner amendment, this
report authorizes no additional repair/audit round. `RP6-P0.sh` remains draft,
not accepted, not frozen, not dispatchable, and carries no host-contact authority.
