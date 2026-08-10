BLOCK: 4 findings

# Codex flagship T0 audit — `RP6-P0.sh` full block

Date: 2026-08-10
Auditor: Codex `gpt-5.6-sol`, `xhigh`, fresh second-flagship slot
Tier: **T0** — defensive staging-admission / host execution-domain preflight
Applied auditor contract: `claude-opus-5` xhigh + `gpt-5.6-sol` xhigh acceptance floor; maximum three rounds. This is the terminal audit after repair round 3, so a non-accepting verdict stops the cycle and must be reported to Barış.
Owner amendment: A2/A2a followed; this audit was performed directly with no sub-delegation.

The frozen audit basis is exactly commit `bbb40ab61dafc46c2c708e2aa447a87c5c7a4f79`. The target was clean and byte-identical to that commit before this report was written:

```text
sha256=2d9b166eacfc39ebe0d8d89edb5860876ccc4d9f0ff97f9e10a228dbcf96289e
bytes=71743
lf_bytes=1328
cr_bytes=0
bom=false
bash_n_rc=0
```

No host, SSH, network, deployment, broker, backtest, Pine, parity, MTC, or trading action was performed. All adversarial fixtures were local and temporary. The concurrent RP7 and transport changes were not edited. The only repository write by this audit is this report.

## Required findings

### Finding 1 — HIGH — the supposedly read-only interpreter probe executes unverified venv startup code

`RP6-P0.sh:1267-1269` says `-I` means only `sys` is imported and nothing is written, then runs:

```bash
"$P0_ENV" -i LC_ALL=C "$py" -I -c 'import sys; print(...)'
```

That is false. `-I` implies `-E`, `-P`, and `-s`; it does **not** imply `-S`. Python imports `site` during startup, processes the venv's `site-packages`, and executes `import` lines in `.pth` files before the `-c` body. Python 3.12 documents both facts: [`-I` does not include `-S`](https://docs.python.org/3.12/using/cmdline.html#cmdoption-I), while [`-S` suppresses `site`](https://docs.python.org/3.12/using/cmdline.html#cmdoption-S), and [executable `.pth` lines run at startup](https://docs.python.org/3.12/library/site.html).

Independent falsification used a fresh local venv containing a one-line `.pth` file that writes a marker. The production command shape both created the marker and emitted the accepted output; the `-S` control did not:

```text
PYTHON_PTH_PROBE I_ONLY_RC=0 MARKER_CREATED=yes MARKER_CONTENT=[PTH_EXECUTED] OUTPUT=[P0PY 3.14]
PYTHON_PTH_CONTROL I_PLUS_S_RC=0 MARKER_CREATED=no OUTPUT=[P0PY 3.14]
```

The exact local Python was 3.14, while the cited 3.12 documentation confirms the same startup contract for the preregistered runtime. This is not merely an overbroad sentence: a deviant or compromised candidate venv can perform arbitrary file or network actions under `gatea` authority and still return the exact `P0PY` success line. The later `P0_claim ... mutation=none_in_this_block` at `RP6-P0.sh:1327` is therefore false, and V11 read-only scope fails.

Required repair: execute the probe with `-I -S` (and retain the cleared environment), then add D026 evidence using an executable `.pth` fixture: current/pre-fix bytes must create the marker, repaired bytes must not, and both result shapes must be recorded. Update the explanatory and terminal claims to state only what the repaired launch establishes.

### Finding 2 — MEDIUM — row 9 has no timeout and can hang without any reasoned STOP

Preregistration row 9 at `WPI_PREREGISTRATION_DRAFT.md:503` explicitly assigns timeout to:

```text
P0_STOP reason=system_manager_unreachable rc=<n> detail=<d>
```

The implementation at `RP6-P0.sh:1091-1119` invokes `systemctl` directly. It has no bounding process, deadline, elapsed-time capture, or timeout branch. A stalled D-Bus/system-manager query therefore never reaches the rc/diagnostic adjudicator and emits no `P0_STOP`.

Independent fixture: the exact delivered `p0_assert_system_manager_ready` was extracted, first driven by a fast `Version=252` shim, then by a shim sleeping five seconds. A one-second watchdog had to be placed **outside** the delivered function to keep the audit bounded:

```text
MANAGER_FAST rc=0 output=[P0_system_manager_ready ... response_value=[252] ...]
MANAGER_STALL external_watchdog_rc=124 elapsed_s=1 output_bytes=0 p0_stop_lines=0 output=[]
```

The external rc 124 is not a block verdict and carries no reason line. This violates row 9, Pattern 1, and Pattern 6 even though all completed manager branches otherwise classify as STOP correctly.

Required repair: add a preregistered bounded launcher for the manager query. Per the preregistered execution-environment rule, the cleared-environment exec must come first and the pinned timeout must be its argument, for example `env -i ... <pinned-timeout> ... <pinned-systemctl> ...`; timeout must map to `system_manager_unreachable` rc 3 with an honest recorded status/detail. D026 must show the current arm requiring an external kill and the repaired arm returning its own bounded STOP.

### Finding 3 — MEDIUM — the RO tool inventory is stale, omits `timeout`, and rejects its pin

`RP6-P0.sh:267` declares:

```text
stat readlink id env find grep sha256sum awk systemctl ss curl getent
```

At the frozen basis `bbb40ab6`, `RP7-WPI-RO.sh:573,952` uses the nine-tool RO set `stat readlink env find sha256sum systemctl ss curl timeout`; prereg row 12 at `WPI_PREREGISTRATION_DRAFT.md:534` likewise calls `/usr/bin/timeout` the ninth bound tool. RP6 omits that real dependency and carries stale `grep` and `awk` dependencies that the frozen RP7 executable does not invoke.

The omission is executable, not documentary. Driving RP6's exact pin validator with the required pin produced:

```text
P0_TIMEOUT_PIN rc=3 output=[P0_STOP reason=input_pin_unknown_tool name=P0_TOOL_PINS tool=timeout inventory=[stat readlink id env find grep sha256sum awk systemctl ss curl getent]]
```

Thus RP6 cannot accept a complete RP7 pin set, can pass without checking a tool the RO block executes, and can falsely STOP on missing unused `grep`/`awk`. Its terminal claim at `RP6-P0.sh:1325` that it established the 12 listed RO tools is not the actual frozen RO dependency contract.

Required repair: regenerate the P0 inventory from the frozen RP7 executable plus P0-only dependencies, include/pin `timeout`, remove dependencies not executed by either stage, update the count and claim, and add a drift test comparing the two frozen inventories. Coordinate this repair against a frozen RP7 basis rather than the concurrently moving worktree.

### Finding 4 — LOW/MEDIUM — getent error/no-match divergences do not match the exact section 8.1 grammar

Rows 2 and 3 at `WPI_PREREGISTRATION_DRAFT.md:496-497` require resolver/invocation/parse failures to emit:

```text
P0_STOP reason=identity_unresolvable account=<a> rc=<n> detail=<d>
```

The two error callers at `RP6-P0.sh:916,937` drop `rc=` entirely because `p0_resolve_passwd` keeps its status local and exports no status to the caller. Independent rc-5 resolver fixtures reproduced both violations:

```text
GETENT_ERROR_GATEA rc=3 reason=[P0_STOP reason=identity_unresolvable account=gatea detail=[gatea backend unavailable]] contains_rc_field=0
GETENT_ERROR_MTC rc=3 reason=[P0_STOP reason=identity_unresolvable account=mtc-bridge detail=[mtc backend unavailable]] contains_rc_field=0
```

There is a second exact-contract mismatch at `RP6-P0.sh:934`: a valid `mtc-bridge` no-match emits `state_account_resolution_unexpected`, a reason token not present in current row 3. The 16-case harness reproduced that current line while still passing because it asserts the implementation's substring rather than the current row's divergence table.

The polarity remains fail-closed at rc 3, so this is not a false host FAIL. It is nevertheless a required repair under the kickoff's exact-grammar contract: the recorded status is lost on real resolver errors and one reachable reason token has no preregistered grammar.

Required repair: preserve/export the getent status and include honest `rc=<n>` on every `identity_unresolvable` arm. Align the valid-no-match reason with one explicit row-3 grammar (either amend the authoritative row to preregister the absence token or change the block to the chosen registered token). Add exact-line assertions, not substring-only assertions, for rc 0 parse errors, rc 2 no-match/diagnostic cases, and other nonzero resolver statuses.

## Verification rows

| V | Contract item | Verdict | Independent evidence |
|---|---|---|---|
| V1 | Frozen identity, bytes, syntax | **PASS** | HEAD is `bbb40ab6`; target diff vs that commit is empty; SHA-256 `2d9b...89e`, 71743 B, LF-only, no BOM; Git Bash `bash -n` rc 0. |
| V2 | Section 8.1 rows 1-9, exact divergence grammar | **FAIL** | Rows 1 and 4-8 conform on their exercised reason families. Row 9 has no timeout outcome (finding 2). Rows 2-3 lose mandatory getent `rc=` and row 3 has an unregistered no-match token (finding 4). |
| V3 | STOP-vs-FAIL truthfulness on every branch | **FAIL** | Every completed branch inspected exits only 0/1/3 with defensible polarity; however, a stalled row-9 observation never terminates and never becomes the mandatory STOP (finding 2). GNU ENOENT object arms correctly produce rc-1 FAIL. |
| V4 | Numeric identity | **PASS** | No `%U`/`%G`, `id -un`, or name-based admission. Live uid/gid/groups and passwd uid/gid are numeric; returned names remain diagnostic-only. |
| V5 | Capability ledger | **PASS** | Exact whole-word fixture: groups `10 1988` with forbidden `0 988` admitted rc 0; groups `10 988` STOPped rc 3 with `capability_wider_than_ledger gid=988`. No substring collision. |
| V6 | Getent parser, R4 sentinel, NUL handling | **PASS for capture semantics; FAIL for output grammar under V2** | Full-block fence reproduced pre-fix NUL-only rc2 as false `nomatch`, current bytes as `error / nul_byte_in_merged_capture`. R3 16-case and R4 27-case harnesses pass. Finding 4 concerns the caller's exact reason fields/tokens, not the NUL repair. |
| V7 | `:?` backstops | **PASS** | Four-case harness rc 0, 4 `CASE_OK`, 0 `CASE_BAD`; both double mutations were killed. Row-8 pre-check removal reaches the named `P0_ATTESTED_USER_NS:` backstop. |
| V8 | Tool inventory | **FAIL** | Finding 3: required `timeout` pin rejected; frozen RP7 dependency absent; unused `grep`/`awk` carried. |
| V9 | Row-8 domain gate and row-9 ordering | **FAIL overall** | Row 8 itself passes: exact five comparisons, two named STOP families, no visible-PID-1 comparison. Removing the live comparison admitted a mismatched net namespace; removing the top-level domain call made `MANAGER_RAN` reachable. Row 9 fails only the independent timeout requirement in finding 2. |
| V10 | Evidence-leaf binding | **PASS** | fd 8 and `EV_LOG` are compared by numeric dev:inode; readlink/stat failures are reasoned STOPs; fd 8 closes on each explicit error arm inspected. |
| V11 | Read-only scope | **FAIL** | Shell source contains no filesystem-writing primitive beyond the disclosed fd duplication, but the invoked `python -I` executes venv `.pth` startup code and performed a real temporary write while returning the accepted output (finding 1). |
| V12 | Mandated QA and evidence reproducibility | **PASS** | 16-case rc 0 (16 `CASE_OK`); four-case rc 0 (4 `CASE_OK`); 27-case rc 0 (25 `CASE_OK` + 2 probe successes, no bad cases); full-block fence rc 0 with 39 `ASSERT_MET`, 0 `ASSERT_UNMET`; freeze fence rc 0. All three C13 transcripts and freeze transcript were byte-identical; full-block transcript matched after normalizing only its random `/tmp/tmp.*` root. |

## Ten-pattern attack summary

| Pattern | Result |
|---|---|
| 1 — STOP is not a result | **Finding 2:** timeout cannot become STOP because no timeout exists. Completed outcome polarities otherwise hold. |
| 2 — Whose kernel answered? | Row-8 comparison and call-removal mutants prove the gate load-bearing. `<PIN-AT-FREEZE>` constants and the accepting host arm remain freeze-gate items, not findings. The `procfs_identity=not_established` residual is stated honestly. |
| 3 — The leaf is not the path | Venv root is checked before the interpreter, literal canonicalization is enforced, and intermediate/target/mount limitations are disclosed. No new finding. |
| 4 — The privileged child brought its own environment | **Finding 1:** cleared environment and `-I` do not suppress venv `.pth` startup execution. The separately disclosed inherited cwd/TMPDIR/tool-provenance limits were not re-labelled as closure. |
| 5 — grep is not a parser | Getent is parsed as a complete seven-field, single-record response with NUL/multiline rejection. No substring parser decides admission. Finding 4 is output-contract loss, not a false parser admission. |
| 6 — Read status before stdout | Status-first ordering holds on completed captures; **finding 2** is the missing pre-status timeout gate. |
| 7 — Nonzero read is not EOF | No line-reader EOF loop is present. The NUL-delimited `mapfile` capture requires exactly two records and fail-closes extra delimiters. |
| 8 — The name is not the identity | Numeric-only admission and exact forbidden-gid membership pass. |
| 9 — The sentence outruns the probe | **Findings 1 and 3:** `mutation=none` and the stated RO tool inventory are broader than the executed predicates establish. |
| 10 — Evidence that cannot fail | Mandated fences are mutation-killing and reproduce. The four new audit fixtures each have a discriminating control or external kill and real output recorded above. |

## Mandated harness record

Executed from repository root with `C:\Program Files\Git\bin\bash.exe`:

```text
sed -n '664,787p'  SELF_QA_RP6.md | bash --noprofile --norc  -> rc 0, cases=16 PASS
sed -n '952,1035p' SELF_QA_RP6.md | bash --noprofile --norc  -> rc 0, cases=4 PASS
sed -n '1181,1346p' SELF_QA_RP6.md | bash --noprofile --norc -> rc 0, cases=27 PASS
sed -n '1678,2068p' SELF_QA_RP6.md | bash --noprofile --norc -> rc 0, full-block PASS
sed -n '2286,2319p' SELF_QA_RP6.md | bash --noprofile --norc -> rc 0, freeze gate PASS
```

Transcript comparisons:

```text
C13_R3_16            cmp rc 0
C13_R3_BACKSTOP_4    cmp rc 0
C13_R4_27            cmp rc 0
FREEZE_LITERAL       cmp rc 0
FULLBLOCK_NORMALIZED cmp rc 0
```

The full-block fence independently re-derived its immutable RED basis as:

```text
RED_SOURCE rev=0bbc3591 sha256=bff3c86e6e9b565c55da34580284f22c80253d9e931d879fd749459bac85b7cf bytes=57441
RP6_FULLBLOCK_D026_SUMMARY findings=7 round3_residuals=3 real_lstat_arms=2 execution_domain_cases=9 readlink_stop_arms=3 result=PASS
```

The GNU argv[0]-prefix repair is load-bearing: real GNU absolute-path `stat` produced the pre-repair `path_probe_unclassified` STOP and current `venv_root_absent` / `interpreter_absent` rc-1 FAIL arms. The stated uutils residual is correct and fail-closed: uutils uses a basename prefix, so the exact GNU absolute-prefix classifier will STOP as unclassified rather than falsely FAIL/PASS until a uutils shape is separately preregistered.

## Terminal disposition

The four findings are required repairs. Findings 1 and 2 are executed security/availability failures; findings 3 and 4 are exact frozen-contract mismatches. Because repair round 3 exhausted the T0 cap, this report does not authorize another silent repair/audit round. The Lead must stop and report the blocker to Barış. `RP6-P0.sh` remains draft, not accepted, not frozen, not dispatchable, and carries no host-contact authority.
