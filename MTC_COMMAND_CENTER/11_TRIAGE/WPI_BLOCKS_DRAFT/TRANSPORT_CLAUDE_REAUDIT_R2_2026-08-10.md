All scratch removed; the eight transport files are byte-identical to the pre-audit state. Report follows.

---

# TRANSPORT SET — CLAUDE FLAGSHIP T0 RE-AUDIT, ROUND 2 (`claude-opus-5`, xhigh, fresh session)

## VERDICT: **REQUEST_CHANGES — 1 required finding**

Fifteen of the sixteen required findings across both round-1 lists are closed, and closed *well*: every load-bearing round-1 falsification I re-ran against the repaired bytes now fails in the safe direction, and every RED arm I built reproduced the round-1 defect from the audited round-1 bytes, so the repairs are causal rather than incidental. The residual is narrow but real and sits inside a finding both reports called CRITICAL/REQUIRED:

**An operation rc outside the preregistered `{0,1,3}` outcome grammar is still classified as "a completed operation observed deviant state".** `ssh` returning **255** — its own code for a connection or authentication failure, in which nothing was observed at all — produces `TR_OP_DEVIANT`, `TR_RUN FAIL`, exit 1. Round-1 Claude F2 named that exact case in its list of reachable instances; the repair implemented the prescribed rc-3 fix and stopped there, while `STATUS_TRANSPORT.md` now asserts "A not-evaluable operation is no longer a FAIL."

Scope note: the set is independently authority- and budget-blocked by the prereg's own dispatch gates (§0 F6 amendment, §12). That is pre-existing state, not part of this verdict.

---

## 1. Method and integrity

Read-only. No SSH, SCP, host IP, credential, service, unit, broker, exchange or trading contact; no RUNID allocated; `C:\WPI_ARTIFACTS` untouched. The only sockets attempted were the runner's own bounded probe with an out-of-range port, which returns before a socket is constructed. Fixtures ran in WSL `/tmp/wpi_r3_*` and `C:\Users\Public\wpi_r3_*` (an ASCII-only path — this host's profile path is non-ASCII, the same constraint round 1 recorded), all removed.

Environment: Windows PowerShell **5.1.26100.8875**; WSL (bash 5.x, **uutils** coreutils); Git Bash 5.2.37.

Targets confirmed stable at `9ef4437d` before and after: `git diff --stat 9ef4437d` over all eight files is empty. Re-hashed after every fixture:

```
e4ddf87b0869ba0fadcb9750e65f4f276c90667e788e489c5921923b0d3e1f80   5215  run_p0.sh
cd659ee9e1edceb496a5ed08707abd283e3cf5f70a3872ab6f1fdc616ac3f4e8   5933  run_ro.sh
2f076ed9a928656fddf22969ea4bf70de895f2c84c73f13b4c64b8040e72aa9a  45066  transport_runner.ps1
3ff967294ec0f5d592701bc63940b24f2162b38f8734e38c5343930594da7149   4631  TRANSPORT_PLAN.tsv
e91bae0827f16cbefe2091980c0a049583bd8ce4173f99e802b2d54a224c29a8  12340  remote_setup_wpi.sh
8eb9c499a306c11595638d8db38b1611cdd38470ba12d2c0e019116e2139d412  16614  remote_extract_verify_wpi.sh
586804f852b6c8f31ad55414f5d6335f06ed8f4e1fe8148c624aea7ad05e5ee7 127570  SELF_QA_TRANSPORT.md
4c671840f972addad3c057fc7a8d50a3339c2eaccb5e3081da2cbcc66b5c61ab   3562  STATUS_TRANSPORT.md
```

`git status` carries nothing authored by this session (the RP6/RP7 entries are the concurrent sessions').

**Accepted Stage-2 originals, byte-verified independently:** `remote_setup.sh` 4976 `faee3725…21b5`; `remote_extract_verify.sh` 8270 `ba0bef0e…3db3`; `remote_close_tree.sh` 7470 `87157f0e…f3f0e`. All three match. `04_PREREG_R45B/remote_close_tree.sh` is byte-identical to the `02_PREREG` copy.

**RED baseline provenance:** the round-1 bytes I ran out of commit `1c1c9ed1` re-derive to 4973/`5b259818…`, 7689/`17ed8f3f…`, 3693/`8b2c520a…` — exactly the identities both round-1 reports audited. The RED arms are the audited bytes, not a reconstruction.

**Declared substitutions in my own fixtures** (each printed by the harness, each asserted-present-then-replaced so a missed anchor throws): Stage-1 freeze fills (`BASE_RUN`, `RECORD_ROOT`, `PREREG_DIR`, `RUNKIT_DIR`, `ACCEPTED_DIR`, plan/stdin/program digests, `EXPECT_UID/GID`, `EXPECT_ARCHIVE_BYTES`, `HASHES`); `ssh`/`scp` pin targets → `C:\Windows\System32\cmd.exe` at its real digest; remote `TOOL_*` pins → regular root-owned 0755 copies (this kernel ships `/usr/bin/{stat,mkdir,readlink,sha256sum,chmod}` as **symlinks**, which the delivered scripts refuse by design); `remote_close_tree.sh` `EXPECT_OWNER` → `root:root` (diffed). Nothing else.

---

## 2. V-rows — one row per original required finding

### Codex list (V1–V10)

| V | Finding | Disposition | Evidence I executed |
|---|---|---|---|
| **V1** | **F1** CRITICAL — op STOP converted into transport FAIL | **PARTIAL** | `B1_GREEN`: probe rc 3 → `TR_OP_NOT_EVALUABLE`, `TR_RUN_CLASS deviant=0 not_evaluable=1`, `TR_RUN STOP`, **rc 3**. `B1_RED` (anchor `if ($rc -eq 3) {` asserted, then neutralised): identical fixture → `TR_OP_DEVIANT`, `TR_RUN FAIL`, **rc 1** — the round-1 behaviour, so the repair is causal. Precedence tested: `B2` (deviant op 01 + later `always` STOP op 11) → `deviant=1 not_evaluable=1`, `TR_RUN FAIL … first_fail=01 first_not_evaluable=11`, rc 1, with `TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch` and the `always` op still run. **But** `B3` (`rc 255`) and `B4` (`rc 2`) → `TR_OP_DEVIANT`, `TR_RUN FAIL`, rc 1. See finding 1. |
| **V2** | **F2** CRITICAL — equal digest sets cannot bind | **CLOSED** | Fixture: the **accepted** `remote_close_tree.sh` run over a 3-file tree under WSL (only `EXPECT_OWNER` substituted, diff printed), its real transcript delivered as `ops/07.stdout` by a real child process, the identical tree fetched by a real child into `evidence/<RUNID>`. `A1_GREEN`: `TR_BIND_COUNTS remote=3 local=3` → `TR_BIND_SET remote_set_sha256=5113f55b…2bfb reconstructed=5113f55b…2bfb` → `TR_BIND_PASS files=3` → `TR_RUN PASS`, **rc 0**. `A2_RED` (latch `$digests.Add($capRel,$capDigest)` reverted to `$matches[1]`): `digest_differs` ×3 on byte-identical files, rc 1. Round-1 consequence 2 also closed — `TR_BIND_SET` is reached and `CLOSE_DIGEST_SET_SHA256` is genuinely compared (`A6`). |
| **V3** | **F3** CRITICAL — inherited PATH/env selects the trusted chain | **CLOSED** | Operator: with `C:\Users\Public\wpi_r3_fakebin` first on PATH and `PYTHONPATH`/`TMPDIR` planted, `C0` confirms the round-1 mechanism would still select the plant (`Get-Command ssh → …fakebin\ssh.exe`), while `C1` on the delivered bytes runs `resolution=pinned_absolute chain=trusted` and the child receives **11 variables**: `PATH=C:\Windows\System32;C:\Windows`, `TEMP`/`TMP` run-owned under the record root; planted dir, `PYTHONPATH` and `TMPDIR` all absent from the child. `C2` (pin outside `%SystemRoot%`, byte-identical to `cmd.exe`, correct digest) → `program_chain_untrusted detail=not_under_pinned_system_root`. `C3` → `program_sha256_mismatch`. `C4` (`C:\Windows\Temp`) → `chain_owner_sid_untrusted=S-1-12-1-…` — the numeric-SID sweep fires. Wrappers: `F1_RED` round-1 `run_p0.sh` with a hostile PATH `sha256sum` that answers with the expected digests → `HIJACKED_LIB_SOURCED`, `HIJACKED_BOOTSTRAP_SOURCED`, `HIJACKED_P0_BLOCK_EXECUTED`, `P0W done`, **rc 0**; `F1_GREEN` same plant → pinned tool runs, `block_sha256_mismatch`, **rc 3, zero hijacked blocks executed**. Remote: `D7` — hostile `stat` first on PATH is simply never consulted, `SETUP PASS`. |
| **V4** | **F4** HIGH — ambiguous diagnostic read as absence | **CLOSED** | `D2_RED` round-1 bytes, mixed ENOENT+EACCES: `base_absent` → **DIRS_CREATED=4**. `D2_GREEN` (multiline) → `path_probe_multiline`, rc 3, **0 dirs**. `D2b_GREEN` (one line carrying both classes) → `path_probe_unclassified … detail=…No such file or directory / Permission denied`, rc 3, **0 dirs**. The calibration line reads `template=stat: cannot stat '@PATH@': No such file or directory (os error 2)` — it bound to this kernel's **uutils** wording, which no hardcoded GNU sentence would have matched. The predicate is measured, not guessed. |
| **V5** | **F5** HIGH — mutation before binding; resolver names as identity | **CLOSED** | `D3_RED` round-1 through a parent symlink: 4 directories created, *then* `path_not_canonical`. `D3_GREEN`: `parent_not_canonical path=/home/gatea canonical=/home/real` — **0 created**. `D3b`: world-writable ancestor → `parent_other_writable mode=757`, 0 created. Pattern 8, the fixture Codex asked for: a process at uid **4242** whose rendered name is `gatea` (second `/etc/passwd` entry), preregistration expecting uid 1000 — `D5_RED` round-1 returns **`SETUP PASS` rc 0** with 4 directories; `D5_GREEN` returns `login_euid=4242 expected=1000`, rc 1, 0 directories, with `owner_name=` kept diagnostic. `mktemp`/`tr`/`TMPDIR` appear nowhere but in comments, so "creates exactly four directories and nothing else" is now true (`D1` tree listing). |
| **V6** | **F6** HIGH — listing stdout consumed before status/completion | **CLOSED** | `E2_RED` round-1 bytes with a `tar` that warns on stderr and returns the correct list at rc 0: `FAKE_TAR_WARNING` ×2 then `EXTRACT PASS … members=6 verified=6`, **rc 0, 6 files extracted** — Codex's own reproduction. `E2_GREEN` same stub re-pinned: `EXTRACT_STOP reason=tar_type_listing_diagnostics`, **rc 3, 0 extracted**, before a member is parsed. Also `E4` `tar_type_listing_unterminated_final_record`; `E5` `tar_type_listing_failed rc=2 detail=tar: unreadable`; `E6` `archive_changed_during_listing first=e67e8923… second=b141f079…` — the post-listing re-hash is load-bearing. The `S<rc>` sentinel inside the substitution is what keeps the termination evidence alive; I confirmed the `${both##*S}` split is unambiguous because the sentinel is always the last `S`. |
| **V7** | **F7** HIGH — extractor not the §4 minimal derivation | **CLOSED BY DERIVATION + DEVIATION (D-1)** | No count literal exists: `MEMBER_COUNT="$(count_records "$MEMBERS")"` and every comparison and the result text use it. `E3` (five-member archive vs the derived six) → `tar_member_count=5 expected=6`. The wider §4 question is V17. |
| **V8** | **F8** HIGH — op 02 violates the binding cwd | **CLOSED** | `TRANSPORT_PLAN.tsv:3` cwd is `…\WPI_BLOCKS_DRAFT\01_RUNKIT`; `$RUNKIT_DIR` is a distinct frozen constant and `$PINNED_FILES` resolves under it only. `G4a` (kit digest pinned) → `TR_PINNED path=…\01_RUNKIT\runkit.tar`, `TR_RUN PASS`. `G4b` (decoy's digest pinned, decoy sitting beside the runner) → `pinned_file_sha256_mismatch … actual=eedc8ffb… expected=1fd0fd87…` — the decoy is never reachable. |
| **V9** | **F9** HIGH — ops 07/08 name an absent artifact | **CLOSED** (second option) | `G1`: `TR_STDIN op=07 root=ACCEPTED path=…\WPL_P2_STAGING_…\02_PREREG\remote_close_tree.sh sha256=87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e`. `G2` right file, wrong token → `stdin_file_missing`. `G3` unknown token → `stdin_root_unknown=ELSEWHERE`. |
| **V10** | **F10** HIGH — self-QA not literal D026 evidence | **CLOSED** | §0 names two standalone scripts, reproduced verbatim, taking no arguments and declaring no shell state; §3/§4 carry their full bodies. Shell RED arms read commit `1c1c9ed1` and print digests — I confirmed those digests are the audited round-1 identities. Runner RED arms assert the anchor first (`SELF_QA_TRANSPORT.md:966`, `throw ('MUTATION_ANCHOR_NOT_FOUND: …')`), so a missed anchor cannot manufacture a false RED. §6 states arms executed, arms not driven, and the direction each undriven arm fails in. `Test-Ascii` is deleted. One census nit — see N-a. |

### Claude list (V11–V16)

| V | Finding | Disposition | Evidence |
|---|---|---|---|
| **V11** | **F1** `$Matches` clobber | **CLOSED** | As V2. Every capture in `Read-RemoteCloseRecord` is latched on the line after its own match, in all nine grammar branches; `CLOSE_SIZE` is latched too and sizes are now compared per file (`TR_BIND_DIFF size_differs=` exists), not merely counted. My four RED cases (`A3` changed byte, `A4` missing file, `A5` extra file, `A6` tampered set-SHA) each produce a **distinct** reason — the non-discrimination that made round-1 RED arms worthless is gone. |
| **V12** | **F2** not-evaluable rolled up as FAIL | **PARTIAL** | As V1. Exit 3 is reachable through the whole runner and precedence is defined, logged and tested. The rc-255 case F2 enumerated is not repaired. |
| **V13** | **F3** set incomplete; op-02 cwd | **CLOSED** | `G1` + `G4a/G4b`. §4 and §5 record the `ACCEPTED` root token and the distinct `01_RUNKIT`. D-2 remains a live Lead choice (co-locate vs pin-in-place); `G2` already proves the wrong-token direction, so the co-location option costs one file plus one token. |
| **V14** | **F4** §7 binding and the launch path have no executed arm | **CLOSED** | The §7 binding now has a PASS arm, four discriminating FAIL/STOP arms, and a full grammar. `Invoke-ExternalProcess` was driven by **real child processes** in my A/B/C/G arms (ops 07, 09, 01, 02 across ~14 runs), with `.argv/.stdout/.stderr/.rc/.elapsed_ms` present for every op including skipped ones. `Get-Sha256OfText` is reached and its output compared. |
| **V15** | **F5** derivation exceeds §4 | **CLOSED BY DERIVATION** | As V7. Counts derive from `MEMBERS`; no literal remains to drift. |
| **V16** | **F6** no fail-closed guard for `<ALLOCATE-AT-DISPATCH>` | **CLOSED** | Delivered file run exactly as it ships: `TR_STOP reason=unfilled_marker field=BASE_RUN`, **exit 3**, before any path is evaluated. `G9` partial freeze (hash pins filled, `RECORD_ROOT` literal — Claude F6's realistic case) → `TR_STOP reason=unfilled_marker field=RECORD_ROOT`, exit 3. `G10_GREEN` (invalid `RECORD_ROOT`) → `TR_STOP reason=runner_unhandled_error detail=System.ArgumentException`, exit 3; `G10_RED` with the top-level `trap` neutralised → the audit's exact localized crash `Test-Path : Yolda geçersiz karakterler var.`, **exit 1**. |

### Nits N1–N5

`N1` **closed** (`run_ro.sh:38 WPI_LOG_DIR='/var/log/mtc-bridge'`). `N2` **not repaired, deliberately** — I confirmed `block_sha256_mismatch` → rc 3 (`F1_GREEN`); the disposition (inherited from the accepted `run_r45.sh` precedent) is recorded rather than silent, which is the right handling. `N3` **closed**: `G5` `plan_row_ssh_stdin_without_file`, `G6` `plan_row_stdin_file_on_non_ssh_kind op=02 kind=scp_up`, `G7` `plan_row_kind_program_mismatch op=01 kind=ssh_stdin program=scp`, `G8` `plan_row_cwd_not_preregistered op=01 cwd=C:\Windows`. `N4` **closed**: `TR_RECORD_ROOT` precedes `TR_PLAN_READ` in every execute-mode arm, so `stdin_file_missing`, `pinned_file_sha256_mismatch`, `program_*` and the marker/grammar STOPs all persist a record (`record_root_already_exists` inherently cannot, and should not). `N5` half-closed as declared.

---

## V17 — D-1 ratification check

**The four-class contract is coherent and mechanically checkable, and the shipped bytes honour it.** §4's classes are (1) pinned constants, (2) program identity, (3) STOP-before-mutation path classification, (4) status-before-stdout adjudication — each stated as a predicate a future audit can test membership against, not as a judgement about "minimal".

I re-derived the diff with the command §5 quotes: `remote_setup_wpi.sh` **178 insertions / 51 deletions, 22 hunks**; `remote_extract_verify_wpi.sh` **246 / 69, 31 hunks** — both figures exactly as claimed. I read the complete deletion side of both diffs (every line of accepted logic removed) and classified each region:

- **Setup** — `EXPECT_PREFIX`/`EXPECT_OWNER`→`EXPECT_UID`+`EXPECT_GID`+`EXPECT_OWNER_NAME` (class 1); bare `stat`/`mkdir`/`readlink` → pinned `TOOL_*` + `require_tool`, `mktemp` and `tr` deleted (class 2); `probe_path`→`calibrate_absence`+`probe_leaf`, new `bind_component`/`bind_parent_chain`, numeric `assert_dir`, allocate/assert interleaved (class 3); `allocate` refusing any `mkdir` diagnostic (class 4).
- **Extractor** — archive-constants block and `MEMBER_COUNT` derivation (class 1); seven `TOOL_*` pins, `wc` removed (class 2); `bind_dir`/`calibrate_absence`/`probe_path` (class 3); `run_capture`, post-listing re-hash, `chmod`/`sha256sum` diagnostic adjudication (class 4).

Nothing falls outside. The member set is still the six-file WP-I kit with `RP1-B3.sh` excluded, and every archive value is still `<PIN-AT-FREEZE>`. The one boundary judgement I had to make: the setup's `SETUP PASS` result text changed from `owner=%s` to `owner_numeric=%s:%s owner_name=%s`. That is non-executable output consequent to class 3's numeric-identity rule, and §4's extractor row already authorises the analogous derived result text — I read it as in-bounds, and flag it so the Lead's ratification covers it explicitly.

**`remote_close_tree.sh` co-located-by-token resolves to the accepted bytes** — proven in `G1`, at `87157f0e…` at the frozen `02_PREREG` path, with both refusal directions driven.

**Remote tool pins refuse symlinks** — `D6a tool_is_symlink`, `D6b tool_other_writable mode=757`, `D6c tool_owner_numeric=4242:4242 expected=0:0`. **Deviation D-3 is independently confirmed and is not hypothetical**: this kernel ships `/usr/bin/{stat,mkdir,readlink,sha256sum,chmod}` as symlinks into a multicall binary, and the delivered scripts STOP at `tool_is_symlink` before doing anything. That is the safe direction, and it is a hard Stage-1 precondition: `GATEA-STAGING` must be confirmed to carry each `/usr/bin/<tool>` as a regular root-owned, not-group/other-writable file, or op 01 and op 03 will STOP at dispatch.

**Recommendation on D-1: ratify.** The alternative — re-deriving under the round-1 constants-only contract — would re-open Codex F3, F4, F5 and F6, three of which I have just watched the round-1 bytes fail live. D-2: either option is sound; the pinned-in-place choice is proven working, and co-location remains a one-file change if the Lead prefers precedent consistency.

## V18 — placeholders

All `<ALLOCATE-AT-DISPATCH>` and `<PIN-AT-FREEZE>` markers are literal. Census over the six executable/plan files: **36 `<ALLOCATE-AT-DISPATCH>`, 27 `<PIN-AT-FREEZE>`** (`run_p0` 6/3, `run_ro` 6/5, runner 4/5, plan 20/5, setup 0/2, extractor 0/7). No RUNID-shaped literal anywhere; the only concrete `WPLP2-…` text is `$ACCEPTED_DIR`, which is accepted-source provenance, not a WP-I allocation. `remote_setup_wpi.sh` STOPs at `identity_pin_unfilled field=EXPECT_UID` on the remote side (`D4`), so the placeholders are fail-closed on both sides. See N-a on the self-QA's census figure.

## V19 — identity and syntax

Per-file SHA-256 and byte counts re-derived twice (start and after all fixtures) — all eight match §8 of the self-QA and the repair report's table. `bash -n` PASS on all four in-scope shell files and on the accepted `remote_close_tree.sh`. `[Parser]::ParseFile` on `transport_runner.ps1` → 0 errors under Windows PowerShell 5.1.26100.8875; no `&&`, `||` or ternary. **0 CR bytes** in all six executable/plan files; runner and plan are pure ASCII; the two derived shell scripts carry 6 and 9 high bytes on 2 and 3 comment lines respectively — em-dashes, matching the accepted originals' 2 and 3 high-byte lines.

---

## 3. Finding

### F1 — REQUIRED, HIGH. An observed rc outside the preregistered `{0,1,3}` grammar is recorded as a completed deviant observation
`transport_runner.ps1:769–776`, against its own header `:10` and `STATUS_TRANSPORT.md:32–33`

The classifier branches only on `$rc -eq 3`; everything else that mismatches `expect_rc` becomes `$anyDeviant` and drives `TR_RUN FAIL` at exit 1. Executed, delivered bytes, Stage-1 freeze simulated:

```text
B3_ssh_rc255_transport_failure
  TR_OP_END id=01 rc=255 expect_rc=0 elapsed_ms=67 …
  TR_FIRST_FAIL id=01 rc=255 expected=0 later_sequence_ops=skip always_ops=run
  TR_OP_DEVIANT id=01 rc=255 expected=0
  TR_RUN_CLASS deviant=1 not_evaluable=1 precedence=deviant_outranks_not_evaluable
  TR_RUN FAIL base_run=WPIQA first_fail=01 first_not_evaluable=11 …
  RUNNER_RC=1

B4_rc2_out_of_grammar
  TR_OP_DEVIANT id=01 rc=2 expected=0
  TR_RUN FAIL …                                        RUNNER_RC=1
```

Why this is not a theoretical rc. Every artifact the plan delivers on stdin — both wrappers, both derived remote scripts, the accepted close script — exits only 0, 1 or 3. `ssh` conveys the remote status faithfully *except* 255, which is ssh's own code for "could not connect / could not authenticate / connection closed". So on ops 01, 03, 04, 05, 07 and 08, **rc 255 means the operation never ran and nothing was observed** — the definition of not-evaluable. The runner already enforces this grammar on the *plan* side (`:342` rejects any `expect_rc` outside `{0,1,3}`); it does not enforce it on the *observed* side.

Consequence at dispatch: a staging host that is down, a rejected key, a DNS failure or a dropped route produces `TR_RUN FAIL` — which the runner's own header defines as "at least one completed operation observed deviant state" — after the one-use RUNIDs are spent and unrecoverable (§1: "if allocation fails for any reason it is burned"). That is a false deviant-state verdict against the host, Pattern 1, and precisely the `[B3-ADJ Classification]` hand-adjudication the preregistration exists to eliminate.

Round-1 Claude F2 listed this case by name: *"and ssh's own rc 255 on connection/auth failure — a pure transport failure in which no probe observed anything, reported as `TR_RUN FAIL`."* The implementer built exactly the fix F2's "minimal fix" paragraph prescribed, so part of this is a defect in my own round-1 prescription — but the closure claim now outruns the code. `TRANSPORT_REPAIR_R2_REPORT.md` §1 records F1 as unqualified **CLOSED**, and `STATUS_TRANSPORT.md:32` leads with "**A not-evaluable operation is no longer a FAIL.**" before narrowing to rc 3 in the next sentence.

**Repair.** Classify any executed op whose observed rc is outside the preregistered outcome grammar as not-evaluable: emit `TR_OP_NOT_EVALUABLE … rc=<n> reason=rc_outside_outcome_grammar`, set `$anyNotEvaluable`, and let the existing precedence stand. Preregister the grammar per kind in §5/§6 while doing it — `scp`'s failure rc is **1**, which collides with the FAIL class and cannot be separated by rc alone, so the §5 row for ops 02/09/10 should say so explicitly rather than leave it implicit. RED/GREEN is cheap: `B3`/`B4` above are the RED; the same fixtures under the repair are the GREEN.

**Alternative disposition, if the Lead judges this a preregistration matter rather than a runner defect:** preregister the observed-rc grammar in §6 and narrow both the runner header `:10` and `STATUS_TRANSPORT.md:32` to say the runner distinguishes rc 3 only, and that any other non-zero rc requires operator adjudication before the record is read as a host-state finding. Silence is not an option — the present sentence is not true of the present code.

---

## 4. Nits (optional — none gate acceptance)

- **N-a — the §8 placeholder census mixes scopes, and one half of it depends on files outside the set.** `SELF_QA_TRANSPORT.md:1806–1807` states "36 `<ALLOCATE-AT-DISPATCH>`, 40 `<PIN-AT-FREEZE>`" immediately after a table of the six transport files. 36 is the six-file figure; the six-file `<PIN-AT-FREEZE>` figure is **27**. 40 is only reachable by including `RP6-P0.sh` and `RP7-WPI-RO.sh` — which are not in this set, are being repaired by concurrent sessions, and today total **41**. A census in the closure document for "placeholders intact" should be over the set it closes. The substance passes; the number does not re-derive.
- **N-b — the pinned `ssh` option set does not neutralise the operator's own `ssh_config`.** §5 pins `-i / BatchMode / StrictHostKeyChecking / IdentitiesOnly / ConnectTimeout` and no `-F`, while the child environment deliberately carries `USERPROFILE`. A `ProxyCommand` in `%USERPROFILE%\.ssh\config` would therefore select the program that contacts the host — the one inherited-state channel Codex F3's *principle* covers that its falsification did not reach. Self-QA §7 discloses the profile is carried, validated and recorded, and that bound claim is honest; the hardening (`-F NUL`, `-o ProxyCommand=none`, a frozen `UserKnownHostsFile`) is a §5 option-set change and therefore a prereg/Lead call, not a round-2 edit.
- **N-c — `run_capture` mislabels one condition.** `remote_extract_verify_wpi.sh:132` reports `${label}_diagnostics` whenever the merged and stdout-only passes differ. That is correct for a non-empty stderr, but the same branch catches *stdout that changed between the two passes*, which is a different (and more alarming) fact. Two reasons would read truer.
- **N-d — the setup script's own rc contract is applied inconsistently.** `bind_component` STOPs (rc 3) on `parent_component_is_symlink` / `not_a_directory` / `not_searchable` — completed observations of deviant state, which line 23's contract calls FAIL (rc 1) — while `parent_owner_numeric` and `parent_*_writable` correctly FAIL. Safe direction, and F1's repair should not make it worse; worth one pass for consistency.
- **N-e — `tar` and `find` inside `run_capture` are the only children in the two remote scripts without `</dev/null`.** Every other invocation in both files carries it. Neither `tar -t` nor `find` reads stdin, and the shape is inherited verbatim from the accepted original, so this is inert — but the scripts arrive on ssh stdin and the discipline is otherwise universal.

**Credit where the accounting is conservative:** self-QA §6 lists `program_sha256_mismatch`, the `Test-TrustedProgramChain` untrusted-owner branch, and `Invoke-ExternalProcess stdin_state=incomplete` as *not driven*. I drove all three (`C3`, `C4`, and incidentally `G1`, where a child that exited before consuming a 7 KB stdin was correctly classified rc 3 rather than ignored). The coverage table understates itself, which is the right direction for it to err.

---

## 5. What I did not verify

- Real `ssh`/`scp` behaviour, host state, and `remote_close_tree.sh` on `GATEA-STAGING`. `cmd.exe` stood in for the pinned programs at its real digest, so the pin, digest, chain and environment logic under test is the delivered logic; the transport itself is not.
- `Invoke-TcpProbe`'s `timeout`, `connect_incomplete`, `local_exception` and `socket_error` arms, and `connection_refused` — all need socket states loopback will not produce here or a destination outside this envelope. All fail toward rc 3.
- The `Test-TrustedProgramChain` reparse-point branch (needs a reparse point under `%SystemRoot%`, i.e. elevation) — though I did confirm the predicate **accepts** the real pinned `C:\Windows\System32\OpenSSH\ssh.exe` (`8607ff93…`) and `scp.exe` (`7758d689…`) on this host, so the check is not vacuously fail-closed.
- The six-member happy path against the real WP-I `runkit.tar` — the kit does not exist before Stage 1; `01_RUNKIT` is absent from the draft directory, and the runner STOPs at `pinned_file_pin_unfilled` until it is built.
- `RP6-P0.sh` and `RP7-WPI-RO.sh` internals — separate T0 slots, and both under concurrent repair during this audit. Neither is a transport target; the eight targets did not move.

---

## 6. Repair scope

One item: **F1**, plus the one-sentence corrections to `transport_runner.ps1:10` and `STATUS_TRANSPORT.md:32` and the §5/§6 rc-grammar preregistration that go with whichever disposition the Lead chooses. Nits N-a…N-e are optional. Everything else in this round stands: fifteen required findings closed, each with a RED arm I reproduced from the audited round-1 bytes and a GREEN arm I executed against the delivered bytes.

This is round 2 of the T0 cap 3; one repair round remains. This report supplies no host, freeze, execution, allocation, or Git authority, and modified nothing.
