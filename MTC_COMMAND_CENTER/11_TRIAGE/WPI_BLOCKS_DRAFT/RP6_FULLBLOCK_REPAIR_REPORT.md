# RP6-P0 full-block repair report

Date: 2026-08-10  
Implementer: Codex under owner amendment A2/A2a (self-implementation; no
sub-delegation)  
Audit tier: T0 — host/execution-domain preflight  
Cycle: Claude flagship full-block audit round 1 → bounded repair  
Current state: repaired, locally verified, pending the two fresh T0 re-audits

## Scope contract

The repair closes the seven required findings in
`RP6_CLAUDE_T0_AUDIT_2026-08-10.md` and applies the kickoff's binding Lead
adjudication to implement §8.1 row 8. The only permitted repository writes are:

1. `WPI_BLOCKS_DRAFT/RP6-P0.sh`
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`
3. `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md`
4. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — row-3 grammar only
5. `WPI_BLOCKS_DRAFT/RP6_FULLBLOCK_REPAIR_REPORT.md`

`RP7-WPI-RO.sh` and `SELF_QA_RP7.md` were reference-only and were not written.
Concurrent work outside this whitelist was preserved. No commit was made.

## Finding disposition and evidence

| Finding | Disposition | Executed closure evidence |
|---|---|---|
| F1 — absolute argv[0] made filesystem FAIL arms unreachable | Repaired. `p0_classify_stat_shape` is parameterized by the exact `$P0_STAT` prefix and accepts only the controlled `stat`/`statx` forms, including GNU's observed `os error 2` suffix. Basename-prefixed diagnostics remain unclassified, preserving the RP7 R3 narrowing. | Two real GNU-lstat pairs: pre-repair missing venv root and interpreter both `path_probe_unclassified`, rc 3; repaired bytes emit `venv_root_absent` and `interpreter_absent`, rc 1. |
| F2 — row-8 execution domain absent; row 9 ungated | Implemented, not reduced. Five runtime prereg inputs are validated against five embedded freeze literals: user/mount/PID/network namespace tokens and root dev:inode. Missing/unfilled/unreadable → `execution_domain_unattested`; unequal live identity → `execution_domain_mismatch`; all rc 3. `p0_assert_execution_domain` is the top-level predecessor of `p0_assert_system_manager_ready`. | Matching fixture rc 0; network mismatch rc 3; unreadable user namespace rc 3 with real diagnostic; comparison-removed mutant falsely passes rc 0; missing-input precheck rc 3; precheck-removed mutation reaches the `:?` backstop; domain-call-removed mutation reaches `MANAGER_RAN`, whereas production stops first. |
| F3 — noncanonical prereg input accused host | Repaired in input validation. A doubled separator in `P0_VENV_ROOT` emits `input_not_canonical_spelling … detail=repeated_separator`, rc 3 before any filesystem probe. | Audited pre-repair bytes accept the doubled spelling, rc 0 in the isolated validator; repaired bytes STOP rc 3 with the exact input-error token. |
| F4 — conflicting tool pins were first-wins | Repaired. `P0_PIN_SEEN` rejects a repeated name as `prereg_input_malformed name=P0_TOOL_PINS duplicate=<tool>`. `P0_PIN_COUNT` advances only after uniqueness holds, so it is a distinct-tool count. | The same `stat=/usr/bin/stat stat=/decoy/stat` table: pre-repair validator rc 0; repaired validator rc 3 with `duplicate=stat`. |
| F5 — readlink failures had empty diagnostics | Repaired at every producer. Each invocation uses `readlink -v`; `p0_prepare_readlink_detail` requires a nonempty printable single-record shape for the normal diagnostic and emits explicit absent/multiline/nonprintable shape tokens otherwise. | Parameter-sensitive shim emits diagnostics only when `-v` is present. All three audited pre-repair arms emit empty `detail=`; all three repaired arms carry `Permission denied` and `diagnostic_shape=single_printable_record`, rc 3. The new root-canonicalization readlink uses the same repair path. |
| F6 — NUL-only rc-2 became valid no-match | Repaired. `mapfile -d ''` receives the producer stream followed by a NUL-delimited textual rc record. Exactly two fields are required; any producer NUL creates an extra field and becomes `error / nul_byte_in_merged_capture`. | NUL-only rc-2 shim: audited bytes print Bash's ignored-NUL warning and `OUTCOME=nomatch`; repaired bytes produce `OUTCOME=error DIAG=[nul_byte_in_merged_capture]`. Existing newline/text/valid-record behavior and the 27-case C13 harness remain GREEN. |
| F7 — missing tokens and incompatible identity grammar | Repaired in block and draft. Non-executable resolved tools use `tool_not_evaluable`; failed/unparseable `id -G` uses `group_query_not_evaluable`. Both account mismatches use `identity_unexpected observed_numeric=<u:g> expected_numeric=<u:g> account=<a>`. §8.1 row 3 now records that same order; row 9 is unchanged. | Tool fixture flips old `tool_not_executable` → required token; group fixture flips `identity_probe_failed` → required token; gatea and mtc fixtures show one exact grammar. Draft HEAD has the old row-3 order and the working draft has the unified order. |

## D026 evidence result

The literal executable fence in `SELF_QA_RP6.md` ran under Git Bash 5.2.37 and
ended:

```text
RP6_FULLBLOCK_D026_SUMMARY findings=7 real_lstat_arms=2 execution_domain_cases=7 readlink_stop_arms=3 result=PASS
```

Process rc was 0. A second literal run was normalized only for the randomized
`/tmp/tmp.*` directory and matched the recorded transcript exactly:
`NORMALIZED_TRANSCRIPT_MATCH=True`.

Regression evidence:

- Freeze-literal gate: placeholder rc 3 / filled fixture rc 0, result PASS.
- C13 R4 arm harness: `cases=27 result=PASS`, rc 0.
- C13 backstop harness: `inputs=2 mutations=2 cases=4 result=PASS`, rc 0.
- `bash -n RP6-P0.sh`: PASS, rc 0.
- `git diff --check` over the repair package: PASS.

## Executable identity

```text
audited_pre_repair_sha256=bff3c86e6e9b565c55da34580284f22c80253d9e931d879fd749459bac85b7cf
audited_pre_repair_bytes=57441
repaired_sha256=041c9da9769e36638c9785b54afc638fa8e7b475a6d24238fc10388916c048db
repaired_bytes=66381
cr_bytes=0
lf_bytes=1248
bom=false
```

## Freeze gate and remaining authority

The following literals intentionally remain `<PIN-AT-FREEZE>`:

- `P0_FIXED_ATTESTED_USER_NS`
- `P0_FIXED_ATTESTED_MNT_NS`
- `P0_FIXED_ATTESTED_PID_NS`
- `P0_FIXED_ATTESTED_NET_NS`
- `P0_FIXED_ATTESTED_ROOT_MOUNT_ID`

Therefore draft bytes cannot GREEN end-to-end. Before freeze, a root-authorised
deploy channel outside the tested ssh-login domain must mint and record the four
namespace tokens plus `stat -c '%d:%i' /`, embed those literals, provide identical
prelude values, and re-run the complete block on the intended guest. This report
grants no host-contact, transport, deployment, budget, or trading authority.

## Acceptance gate

Because this is T0, acceptance requires fresh independent `claude-opus-5` xhigh
and `gpt-5.6-sol` xhigh re-audits that execute the mandated suite. Any reproduced
required finding enters the bounded repair loop; the package is not accepted or
dispatchable until both flagship verdicts accept it. No commit is authorized by
the kickoff and none was made.
