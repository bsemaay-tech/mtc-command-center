All seven verification tracks executed. Report below.

---

# CLAUDE FLAGSHIP T0 FINAL AUDIT — `RP6-P0.sh` round-4 bytes

**Verdict: REQUEST_CHANGES — 1 required finding, 6 nits.**

Auditor: `claude-opus-5`, `xhigh`, fresh session, Claude slot.
Tier: **T0** (host execution-domain preflight). Read-only: no repository file was created or modified; every fixture ran under `mktemp -d` and was removed. No host, SSH, network, deployment, broker, backtest, Pine, parity, MTC or trading action was performed.

**The four round-4 findings F1–F4 are all genuinely CLOSED on the delivered bytes.** I re-drove each one with my own fixtures, not theirs, and each repair is load-bearing under mutation. The single required finding is a *false claim about defensive depth* that the round-4 repair introduced alongside the correct F1 fix: the block's own source, `STATUS_RP6_P0.md`, and `RP6_REPAIR_R4_REPORT.md` all state that deleting ` -S` "cannot silently restore the hole". I deleted ` -S` and silently restored the hole — with a forged version number on top. That is a Pattern 9 + Pattern 10 defect in a T0 block's own evidence, and this workstream has ruled the identical class required in three prior rounds.

**Round cap:** round 4 already exceeded the recorded T0 cap under explicit owner authorisation. A non-accepting verdict therefore stops the cycle. The Lead must report to Barış rather than open round 5 silently.

---

## Verification rows

| V | Contract item | Verdict | Independent evidence |
|---|---|---|---|
| **V1** | F1 — probe runs `-I -S`; an executable `.pth` cannot execute or forge the accepted line | **PASS** (defect closed) — see Finding 1 for the claim about the mutant | Real `python -m venv`, real `site-packages/zz_claude_forge.pth` containing `import os,sys; open(MARKER,'w').write('PTH_EXECUTED'); sys.stdout.write('P0PY 9.9'); sys.stdout.flush(); os._exit(0)`, driving the delivered `p0_assert_interpreter_executable` (`RP6-P0.sh:1403-1495`). Delivered bytes: `rc=0 marker_created=no`, `reported_version=3.14` — genuine, unforged, `.pth` never ran. Sanity control proving the `.pth` is live startup code under plain `-I`: `CLAUDE_F1_SANITY_I_ONLY marker=yes output=[P0PY 9.9]`. |
| **V2** | F2 — row-9 `systemctl` query genuinely bounded; stall fixture yields the block's own STOP, not an external kill | **PASS** | Delivered `p0_assert_system_manager_ready` (`RP6-P0.sh:1243-1283`) + real `/usr/bin/env`, real `/usr/bin/timeout`, four shims, external watchdog set to **40 s** (4× the budget) so it can only fire if the block is unbounded. Results: `GREEN_FAST rc=0` accepted line with `bound=pinned_timeout_inside_cleared_env budget_s=10 kill_after_s=5`; `GREEN_STALL external_watchdog_rc=3 elapsed_s=10 p0_stop_lines=1` → `P0_STOP reason=system_manager_unreachable rc=124 detail=manager_query_deadline_exceeded budget_s=10 elapsed_s=10 text=[]` — the block ended itself, the watchdog never fired; `GREEN_STALL_IGNORES_TERM elapsed_s=15` → `rc=137 detail=manager_query_killed_after_deadline`, proving `--kill-after` escalates against a SIGTERM-trapping child (an arm the delivered QA does not cover); `GREEN_NOISYFAIL` → `rc=1 detail=manager_query_nonzero_status` with the diagnostic captured. RED twins: bound removed → `external_watchdog_rc=137 elapsed_s=40 p0_stop_lines=0`; budget raised to 300 → `external_watchdog_rc=137 elapsed_s=40 p0_stop_lines=0`. Both the wrapper and the frozen literal are load-bearing. Launch order verified in source: `env -i` execs first, `timeout` is its argument (`RP6-P0.sh:1246-1249`). |
| **V3** | F3 — RO inventory equals the FROZEN RP7 tool set plus `id`/`getent`; a complete RP7 pin set is accepted; the drift test is real | **PASS** | Frozen basis re-hashed by me: `RP7-WPI-RO.sh` = `23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad`, 70941 B, byte-identical to `git show d6a976aa:…`. Independent re-derivation from RP7's own bytes at two sites — validator arm `RP7-WPI-RO.sh:594` and binding loop `:611` — both yield `stat readlink env find sha256sum systemctl ss curl timeout python3`; count gate `:610` = 10. Compared against `P0_RP7_RO_TOOLS` (`RP6-P0.sh:317`): `validator_vs_rp6=IDENTICAL`, `bindloop_vs_rp6=IDENTICAL`. Delivered pin validator (`RP6-P0.sh:438-480`): complete RP7 pin set → `rc=0 PIN_OK count=10 trusted_python_bound=yes`; with `id`/`getent` → `count=12`. Attacks all STOP with the preregistered tokens: `input_pin_not_frozen_trusted_python`, `input_pin_freeze_unfilled`, `input_pin_unknown_tool … tool=grep inventory=[…12 tools…]`, `prereg_input_malformed … duplicate=stat`. RED twin reproduces the auditor's original line verbatim on the round-3 inventory: `P0_STOP reason=input_pin_unknown_tool name=P0_TOOL_PINS tool=timeout inventory=[stat readlink id env find grep sha256sum awk systemctl ss curl getent]`. End-to-end `p0_resolve_tool` with a 12-tool pin set → `python3_resolution=pinned_absolute_via_canonicalized_path_symlink`; a shadowed `python3` canonicalising elsewhere → `P0_STOP reason=tool_pin_mismatch … canonical=[…/evil-python]`. Drift test falsified by me: `drop_timeout` → UNMET, `add_grep` → UNMET, unmutated → MET (see Nit 4 for its order-insensitivity). |
| **V4** | F4 — `identity_unresolvable` carries honest `rc=<n\|na>` on both callers; row-3 grammar matches the emitted token | **PASS** | Delivered `p0_resolve_passwd` + `p0_resolve_accounts` (`RP6-P0.sh:927-1075`) against 15 resolver-shim modes. Every `identity_unresolvable` line carries the shim's real status: `rc=5` (backend error, both accounts), `rc=2` (valid no-match, newline-only, diagnostic-carrying), `rc=0` (malformed record, duplicate record, NUL-corrupted capture). Row-3 no-match emits `P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match` — character-for-character the preregistered string. Row-2 route-login no-match emits `rc=2 detail=getent_valid_no_match_for_route_login`, also exact. RED twin: stripping `rc=$P0_PW_RC` reproduces the original F4 defect line `identity_unresolvable account=gatea detail=[…]`. Prereg amendments confirmed **committed** at `78173bfd` (rows 1, 2, 3, 9), working tree identical. |
| **V5** | Whole-block sweep independent of the finding lists | **PASS with nits** | See the sweep table below. |
| **V6** | QA integrity — the five mandated harnesses, and the disposition of the two deliberately-red fences | **PASS; disposition is honest** | All five re-run by me from the document: backstop `rc 0, cases=4 PASS`; full-block `rc 0, 39 ASSERT_MET / 0 UNMET`, `RED_SOURCE rev=0bbc3591 sha256=bff3c86e… bytes=57441`; freeze gate `rc 0, placeholder_rc=3 filled_fixture_rc=0`; R4 D026 `rc 0, 102 ASSERT_MET / 0 UNMET`, `pth_forge=real_venv manager_bound=real_timeout inventory_basis=23e55667@d6a976aa`; R4b C13 `rc 0, cases=27, 25 CASE_OK + 2 PROBE_OK, 0 CASE_BAD`. Superseded fences: 664-787 → `rc 1, 13 OK / 3 BAD`; 1181-1346 → `rc 1, 19 OK / 6 BAD`. **Honest**: I read the failing cases and every one breaks on an assertion string that omits the now-mandatory `rc=` field (e.g. expected `identity_unresolvable account=gatea detail=[…SERVBUSY…]`, emitted `identity_unresolvable account=gatea rc=2 detail=[…SERVBUSY…]`). The real failing output is pasted at `SELF_QA_RP6.md:2500-2515`, the supersession is stated at `:2518-2521` and `STATUS_RP6_P0.md:170-176`, and the fences are explicitly excluded from the mandated set at `SELF_QA_RP6.md:3757-3758`. This is a documented round record, not an undisclosed failure. |
| **V7** | Re-derived identity, `bash -n`, LF-only | **PASS** | `sha256=e93d07adcc9ae03ad15e0b0f10c76be54517251ab461c8fe789d160072d253c6`, `bytes=85540`, `CR=0`, `LF=1523`, final byte `0x0A`, no BOM. `bash -n` rc 0 under GNU bash 5.2.37. Byte-identical at `945e20f5` and at the branch head `78173bfd` (HEAD advanced during this audit; the target did not). `git status --porcelain` for the target is empty. |

### V5 sweep detail

| Item | Verdict | Evidence |
|---|---|---|
| Rows 1–9 exact grammar | PASS (one superset nit) | Row 1 `tool_not_evaluable tool=ss path=… rc=na detail=access_builtin_x_denied mechanism=access_builtin_x` — exact match to the amended row 1, `rc=na` correct because nothing was invoked. Rows 2/3 verified in V4. Rows 4–7 `missing_tool` — see Nit 2. Row 8 `execution_domain_mismatch field=network_namespace observed=… attested=…` — exact. Row 9 rc 124/137/125 tokens — exact. |
| STOP-vs-FAIL truthfulness on every branch | PASS | Exactly 8 `p0_fail` sites (`RP6-P0.sh:1385,1387,1388,1397,1412,1414,1416,1418`), all in the venv-root and interpreter object arms, matching the audit-1 F5 ruling. Executed with real GNU `stat` and real ENOENT: `P0_FAIL reason=venv_root_absent … rc 1`, `P0_FAIL reason=interpreter_absent … detail=preregistered_path_observed_missing_parent_search_succeeded rc 1`, `P0_FAIL reason=venv_root_kind_unexpected kind=regular rc 1`. The stated uutils residual is real and fail-closed: a basename-prefixed `(os error 2)` diagnostic yields `P0_STOP reason=path_probe_unclassified … rc 3`, never a FAIL. 54 distinct STOP reason tokens, all could-not-evaluate classes. |
| Numeric identity | PASS | No `%U`, `%G`, `id -un` or `-nG` anywhere outside comments. `stat` format strings are `%F\|%a\|%u:%g`, `%d:%i`, `%d`, `%F` only. `getent` names captured as `name_diag=` and never compared. |
| Capability ledger | PASS | Whole-word membership on the space-padded list survives substring traps: gids `10 1988 9880` against forbidden `0 988` → admitted; `10 988` → `capability_wider_than_ledger gid=988`; `0 10` → `gid=0`; `988` against forbidden `0` → admitted. Correct polarity in all five. |
| Execution-domain gate still gates row 9 | PASS, and load-bearing under both mutations | GREEN: domain line then manager. Mismatched net ns → `rc 3`, `manager_ran=no`. Crafted procfs on the root filesystem → `execution_domain_unattested field=user_namespace detail=namespace_link_on_root_filesystem device=2049 root_device=2049`, `manager_ran=no`. **MUT1** (comparison removed) → mismatched ns **admitted**, `manager_ran=yes`. **MUT2** (top-level call removed) → `manager_ran=yes` with no domain evidence at all. **MUT3** (the four nsfs discriminations removed) → crafted fixture **admitted**, evidence line degrades to `ns_link_devices=,,,` exactly as the block's comment at `:1149-1153` predicts. All three gates are real. |
| getent sentinel incl. NUL | PASS | `mapfile -d ''` with the out-of-band `\0P0_GETENT_RC=<n>\0` record. Empty rc-2 → `nomatch`; newline-only rc-2 → `error / newline_only_capture_at_rc2`; NUL at rc 2 → `error / nul_byte_in_merged_capture` carrying the real `rc=2`; NUL at rc 0 → `error` carrying `rc=0`. Positive absence is never asserted from a capture that carried bytes. See Nit 1 for the label on the unreachable count<2 shape. |
| Evidence-leaf binding | PASS | dev:inode identity via fd 8. GREEN → `P0_evidence_bound … mechanism=dev_inode_identity`. Stdout bound elsewhere → `evidence_leaf_not_bound` with both ids printed. `EV_LOG` missing → `evidence_binding_unprobeable`. Stdout a pipe → `evidence_leaf_not_bound … stdout_path=[pipe:[…]]`. fd 8 is closed on every error arm. |
| Read-only scope | PASS | The only descriptor operation in the shell source is `exec 8>&1` / `exec 8>&-` (`:738,742,749,754`), which is disclosed. No `mktemp`, no `>` to a file, no `mkdir`/`touch`/`rm`/`mv`/`cp`/`chmod`/`chown`/`tee`. The `mutation=no_filesystem_write_primitive_in_this_shell_source` wording is accurate, and `child_side_effects=not_attested_except_venv_startup_which_is_disabled` is now the honest form. |
| Freeze-gate items | Not findings, per kickoff | Six `<PIN-AT-FREEZE>` literals confirmed present: four namespace pins, root-mount identity, and `P0_FIXED_TRUSTED_PYTHON`. No end-to-end `P0 PASS` can exist before freeze; the freeze fence proves the placeholder path STOPs at rc 3 and a filled fixture reaches rc 0. |

---

## Findings

### Finding 1 — MEDIUM, REQUIRED — the "` -S` cannot be silently deleted" claim is false; an adversarial `.pth` defeats the child self-check and forges the accepted line

**Where the claim is made**

- `RP6-P0.sh:1442-1445`:
  > `# The child also verifies its OWN startup rather than trusting that the flag`
  > `# words survived: if `sys.flags.isolated` and `sys.flags.no_site` are not both`
  > `# set it refuses to report a version and says so. Deleting ` -S` from this`
  > `# line therefore cannot silently restore the hole - it produces a named STOP.`
- `STATUS_RP6_P0.md:36-37`: "so deleting ` -S` yields a named `interpreter_startup_not_isolated` STOP instead of a silent hole."
- `RP6_REPAIR_R4_REPORT.md:87-88`: "The third row is why the fix cannot be silently undone."
- `SELF_QA_RP6.md:2676-2678` — the D026 assertions `F1_MUTANT_RC=3`, `F1_MUTANT_STOP`, `F1_MUTANT_FLAGS` are offered as proof of that property.

**Executed falsification.** Same shape as their fixture — a real `python -m venv`, a real executable `.pth` in the real `site-packages`, driving the delivered `p0_assert_interpreter_executable` bytes — with one change: my `.pth` terminates the process before the `-c` body can run, which is what any hostile `.pth` would do.

```text
CLAUDE_F1_PTH_LINE import os,sys; open(r'…/pth_marker.txt','w').write('PTH_EXECUTED'); sys.stdout.write('P0PY 9.9'); sys.stdout.flush(); os._exit(0)

CLAUDE_F1_SANITY_I_ONLY marker=yes output=[P0PY 9.9]          # the .pth is live startup code under -I

CLAUDE_F1_GREEN     rc=0 marker_created=no                     # DELIVERED BYTES — correct
  P0_interpreter … exec=ok env=cleared isolated=yes site_startup=disabled
    startup_flags=self_verified_isolated_and_no_site
    venv_pth_and_sitecustomize=not_executed reported_version=3.14 …

CLAUDE_F1_RED_NO_S  rc=0 marker_created=yes                    # ONLY ` -S` DELETED, self-check RETAINED
  P0_interpreter … exec=ok env=cleared isolated=yes site_startup=disabled
    startup_flags=self_verified_isolated_and_no_site
    venv_pth_and_sitecustomize=not_executed reported_version=9.9 …
```

The mutant produced **rc 0**, **no STOP line**, the full accepted evidence line, a written marker file, *and* a forged `reported_version=9.9`. The self-check never executed because `os._exit(0)` ran first, inside `site` startup, before the `-c` body was compiled. A third arm deleting both ` -S` and the self-check produced byte-identical output, which is the point: the self-check contributes nothing against the adversary.

**Why this is required, not a nit.** F1's stated threat model is "a deviant or compromised candidate venv". Within that model the mutation-detection property is not merely weaker than claimed — it is absent, and the delivered evidence line will assert `venv_pth_and_sitecustomize=not_executed` while the `.pth` has just executed. Three separate documents tell a future maintainer that removing ` -S` is safe-by-detection. That is Pattern 9 (the sentence outruns the probe) and Pattern 10 (evidence that cannot fail: the D026 mutant assertion passes only because the fixture `.pth` cooperates by letting the `-c` body run). This block's own history has ruled the identical class required three times — audit-1 F6, audit-3 F1, and Codex round-4 F1's `mutation=none_in_this_block`.

**Scope of the damage.** The security repair itself is sound: on the delivered bytes `-S` is present, the `.pth` does not execute, and V1 passes. Nothing about the rc contract, the verdict polarity, or any host claim is wrong. What must be repaired is the false claim and the evidence record that vouches for it.

**Required repair.**
1. Correct `RP6-P0.sh:1442-1445`, `STATUS_RP6_P0.md:36-37` and `RP6_REPAIR_R4_REPORT.md:87-88` to state the truth: the child's `sys.flags` self-check detects flag-word loss only when the venv's startup code permits the `-c` body to run, so it is a guard against accidental flag loss, not against the hostile venv this arm exists to contain. ` -S` alone closes that channel.
2. Add the adversarial `.pth` arm above to the R4 D026 fence as the honest bound on what `F1_MUTANT_*` proves — a `.pth` that pre-empts the `-c` body, recorded RED against the ` -S`-deleted mutant.
3. If a real mutation kill is wanted, it must come from something the child cannot pre-empt — e.g. a source-level assertion that the launch line literally contains ` -S`, checked at the same freeze gate that checks the six `<PIN-AT-FREEZE>` literals. Optional; item 1 alone discharges the finding.

---

## Nits (optional; none blocks acceptance on its own)

1. **`nul_byte_in_merged_capture` names an observation it may not have made.** `RP6-P0.sh:959-963` assigns that diagnostic for *any* `mapfile` field count ≠ 2, including counts 0 and 1, where the cause is a lost status sentinel and no NUL was seen. Unreachable in the delivered bytes — the producer's `printf` always runs unless the process-substitution subshell is SIGKILLed — so this is cosmetic, but it is the same class the block is otherwise rigorous about. Suggest splitting the label by count.
2. **Rows 4–7 grammar superset.** The preregistered divergence is the bare `P0_STOP reason=missing_tool tool=<t>`; the block emits `P0_STOP reason=missing_tool tool=ss rc=1 detail=[]` (verified by execution). The extra `rc=` is `command -v`'s builtin status, not an invocation. Fields are added, none removed, and the prior flagship round recorded rows 4–7 as conforming — worth aligning the rows to the emitted shape at freeze rather than changing the block.
3. **`timeout` rc 124 is ambiguous by construction.** GNU `timeout` returns 124 both when it kills the child and when the child itself exits 124, so `detail=manager_query_deadline_exceeded` could in principle misattribute a systemctl status of 124. `systemctl` does not use 124, so this is a note, not a defect.
4. **The drift test is set-sensitive but order-insensitive** (`SELF_QA_RP6.md:2777` normalises with `sort`). Order carries no privilege for `stat`, but `readlink` must precede `python3` (`RP6-P0.sh:613-616`); reordering is fail-closed (`tool_pin_uncanonicalizable … readlink_not_resolved_before_python3`) yet would be a false STOP on a healthy host, and drift would not catch it.
5. **Commit bookkeeping.** The §8.1 rows 1/2/3/9 amendments — which carry half of F4's closure and the entire row-9 deadline grammar — landed in `78173bfd` ("transport round 3 — all five both-flagship findings closed"), not in `945e20f5` ("RP6-P0 round 4 — all four Codex flagship findings closed"). Both are on the branch and the working tree matches the committed text, so the contract is complete; only the commit titles misplace it.
6. **`ns_link_devices_distinct_from_root=yes` is an unconditional printf literal**, not derived from the comparison it reports. Under the documented D026 mutation it still prints `yes` while the device fields go empty (`ns_link_devices=,,,`). The empty fields are the intended tell, and the block says so — but the token itself asserts a result it does not read.

---

## Ten-pattern attack record

| Pattern | Result |
|---|---|
| 1 — STOP is not a result | PASS. Row 9 now ends itself at 10 s (rc 124) and at 15 s against a TERM-trapping child (rc 137). All 54 STOP tokens are could-not-evaluate classes; the only 8 FAIL sites are positively-established ENOENT / wrong-kind on preregistered absolute paths. |
| 2 — Whose kernel answered? | PASS. Five exact deploy-attested comparisons; visible PID 1 never consulted; nsfs-vs-root device discrimination refuses a crafted `/proc` on the root filesystem; `procfs_identity=not_established` and `manager_identity=not_established` are stated, not implied. Both call-removal mutants admit the fixture, proving the gate load-bearing. |
| 3 — The leaf is not the path | PASS. Venv root adjudicated before the interpreter; literal canonicalisation enforced; symlink-target and intermediate-component binding disclosed as not established. |
| 4 — The privileged child brought its own environment | PASS on the delivered bytes — `env -i` + `-I -S`; `timeout` placed inside the cleared environment. **Finding 1** concerns the claim about the mutant, not the delivered launch. |
| 5 — grep is not a parser | PASS. Seven-field whole-record passwd parse with colon-count gate; duplicate, multiline, partial and NUL captures all refused; no substring decides an admission. Builtin-only substring counter, no `grep`/`awk` anywhere. |
| 6 — Read the status before the stdout | PASS. Every capture adjudicates rc, then shape, then value — verified on the manager, identity, getent, metadata, readlink and interpreter arms. |
| 7 — Nonzero read is not EOF | PASS. `mapfile -d ''` demands exactly two records; an extra NUL fails closed while still carrying the resolver's real status out of the last field. |
| 8 — The name is not the identity | PASS. Numeric-only admission; names diagnostic-only; whole-word forbidden-gid membership survives the `1988`/`9880` substring traps. |
| 9 — The sentence outruns the probe | **Finding 1.** Also Nits 1 and 6. Otherwise the claim lines are now honest: `mutation=no_filesystem_write_primitive_in_this_shell_source`, `interpreter_binary_behaviour=not_attested`, `provenance=not_established`, `nss_source_identity_of_getent_resolution` in `does_not_establish`. |
| 10 — Evidence that cannot fail | **Finding 1** — the `F1_MUTANT_*` assertions pass only because the fixture `.pth` cooperates. Everything else is mutation-killing: I independently killed the row-8 comparison, the row-8 call, the four nsfs discriminations, the row-9 bound, the row-9 budget literal, the F4 rc export, the F4 rc field, and the F3 inventory — every mutation changed the verdict. |

---

## Terminal disposition

`RP6-P0.sh` at `e93d07ad…` / 85540 B remains **draft**: not frozen, not accepted, not dispatchable, carrying no host-contact authority. F1–F4 are closed and I reproduced each closure with my own fixtures. One required repair remains — a false defensive claim in the block's source and in two of its evidence documents. Round 4 already consumed an over-cap round under explicit owner authorisation, so this verdict stops the cycle: the Lead must take Finding 1 to Barış rather than open round 5.

---

**Next steps**

1. **Default path — take Finding 1 to Barış as a bounded documentation-only round.** The repair touches three comment/prose blocks plus one added D026 fixture arm; zero executable logic changes, so the re-audit surface is tiny.
2. If Barış prefers, downgrade Finding 1 to a recorded nit and accept — but that puts a demonstrably false defensive claim into a block headed for freeze, and the freeze pass would inherit it.
3. Do **not** open round 5 without his word — the T0 cap is already spent.
4. Whichever path: the six `<PIN-AT-FREEZE>` literals still block any end-to-end `P0 PASS`, so nothing here is dispatchable regardless.

**Plain-language version for Barış:** the script's four known problems are genuinely fixed — I re-tested every one myself instead of trusting the report. But the script tells a small lie about itself: it says "if someone deletes this one safety flag, the script will notice and stop." I deleted the flag and it did not notice — it happily printed a fake success line. The safety flag is there and working right now, so nothing is unsafe today; the sentence describing it is wrong and should be corrected before this gets frozen. That's a five-minute text fix, but the rules say I can't wave it through, and the repair budget for this file is already used up — so it needs your call.
