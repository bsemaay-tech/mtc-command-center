# TRANSPORT SET — ROUND 2 REPAIR REPORT

**Implementer:** `claude-opus-5`, xhigh, fresh session, 2026-08-10. Owner
amendment A2/A2a observed: implemented directly, no sub-delegation.
**Round:** 2 of the T0 cap 3. **Inputs:** `TRANSPORT_CODEX_AUDIT_2026-08-10.md`
(REQUEST_CHANGES, 10 required), `TRANSPORT_CLAUDE_T0_AUDIT_2026-08-10.md`
(REQUEST_CHANGES, 6 required + 5 nits), `DESIGN_DEFECT_PATTERNS_2026-08-10.md`
(binding pre-read).

**Claim of this report:** all 16 required findings across both lists are closed
with executed RED/GREEN, and all five Claude nits are closed as well. **One
disposition is a deviation request, not a closure** — see §3. No host was
contacted, no RUNID allocated, no archive built, no freeze performed, nothing
committed.

---

## 1. Codex findings

| # | Severity | Disposition | Evidence (`SELF_QA_TRANSPORT.md`) |
|---|---|---|---|
| **F1** | CRITICAL | **CLOSED.** The op loop now classifies the *mismatch*: an actual rc 3 sets `$anyNotEvaluable`, anything else sets `$anyDeviant`. Run level emits `TR_RUN STOP` + exit 3, `TR_RUN FAIL` + exit 1, or `TR_RUN PASS` + 0. Precedence is explicit and logged in `TR_RUN_CLASS`: a completed deviant observation outranks a later inability to evaluate, and every not-evaluable op is still enumerated by `TR_OP_NOT_EVALUABLE`. First-FAIL skipping and `always` retention are untouched. | §4 arms `C1` (rc 3, `TR_RUN STOP`) vs `C2` (repair reverted → `TR_RUN FAIL` rc 1); `C3` (deviant + later STOP → FAIL, `deviant=1 not_evaluable=1`); `C4`/`C5` (ordering unchanged); `A6` and all seven `B*` arms show the whole runner returning 3 for a binding STOP |
| **F2** | CRITICAL | **CLOSED.** Every regex capture in `Read-RemoteCloseRecord` is latched into a local on the line after its own match, before any further `-match`/`-notmatch`. Both the `CLOSE_DIGEST` branch (which was broken) and the `CLOSE_SIZE` branch (which was accidentally safe) are repaired. `CLOSE_SIZE` is no longer decoration: sizes are now compared per file as well as counted. | §4 `A1`: byte-equal pair → `TR_BIND_SET remote=…c208 reconstructed=…c208`, `TR_BIND_PASS files=3`, rc 0. `A2` (latch reverted) → `digest_differs` ×3 on identical bytes, rc 1. `A3`/`A4`/`A5`: differing pairs FAIL with distinct reasons |
| **F3** | CRITICAL | **CLOSED.** Operator side: `$PROGRAM_PINS` gives `ssh`/`scp` frozen absolute paths under `%SystemRoot%`, admitted only after a non-reparse check on every chain component, a write/delete/take-ownership ACL sweep compared by **numeric SID**, and a `<PIN-AT-FREEZE>` digest match. `Get-Command` is gone. Children start via `ProcessStartInfo` with `EnvironmentVariables.Clear()`, a frozen `PATH`, a run-owned `TEMP`/`TMP` under the record root, and a preregistered cwd checked against an allowlist. Wrappers and both remote scripts pin their own tools (`stat`, `sha256sum`, `tar`, `mkdir`, `readlink`, `find`, `chmod`) by absolute path with numeric `0:0` ownership and a not-group/other-writable mode; `mktemp` and `tr` are removed entirely. | §4 `D1` (reverted to PATH resolution → `FAKE_SSH_EXECUTED`, `TR_RUN PASS` rc 0) vs `D2` (`resolution=pinned_absolute chain=trusted`, `PINNED_PROGRAM_RAN`); `D3` (child env contains neither the planted `PYTHONPATH` nor the poisoned `PATH`); §3 `P0/RO_HIJACK_RED` (`P0W_HIJACKED_BLOCK_EXECUTED` rc 0) vs `_GREEN` (`block_sha256_mismatch` rc 3); `P0_TOOL_IS_SYMLINK`, `P0_TOOL_OTHER_WRITABLE` |
| **F4** | HIGH | **CLOSED, and by a stronger predicate than prose matching.** The ENOENT sentence is no longer guessed at authoring time: the script measures the exact sentence its own pinned `stat` emits for an absent name under an already-bound parent, turns it into a template, and later classifies `absent` only when three statements agree — the probe failed, the kernel reports neither object nor link, and the diagnostic equals the template **as a whole string**. Multiline or unrecognised → STOP, before any mutation. Applied to both copies. | §3 `A2_RED` (round-1 bytes: mixed diagnostic → absent, `SETUP PASS`, `DIRS_CREATED=4`) vs `A2_GREEN` (`path_probe_multiline`, rc 3, `DIRS_CREATED=0`); `A3_GREEN` (one line carrying both classes → `path_probe_unclassified`, 0 dirs). The calibration line in every green transcript shows it binding to the uutils wording `… (os error 2)`, which no hardcoded GNU sentence would have matched |
| **F5** | HIGH | **CLOSED.** `bind_parent_chain` walks `/` down to the preregistered parent before the first `mkdir`, requiring each component to be a non-symlink directory, canonical, searchable, numerically owned, and not group/other writable. Identity is `%u:%g` against `<PIN-AT-FREEZE>` `EXPECT_UID`/`EXPECT_GID`, cross-checked against `$EUID`; `%U:%G` is printed as `owner_name=` diagnostic only. Allocation and assertion are interleaved so no object is created through an unverified parent. `mktemp` is gone, so the "creates exactly four directories and nothing else" claim is now true. | §3 `A4_RED` (4 dirs created through the symlink, then `path_not_canonical`) vs `A4_GREEN` (`parent_not_canonical`, 0 created); `A5_RED` (`%U:%G` = `root:root` → `SETUP PASS` rc 0) vs `A5_GREEN` (`owner_numeric=1000:1000 expected=0:0 … owner_name=root:root` rc 1); `A7` (world-writable ancestor refused); `A6` (unfilled identity pin → STOP) |
| **F6** | HIGH | **CLOSED.** `run_capture` runs each listing twice — once merged, once stdout-only — and STOPs unless the two rc values agree, rc is 0, the two payloads are byte-identical (i.e. the diagnostic stream was empty), and the stream ends on a record boundary. The termination evidence survives because an `S<rc>` sentinel is appended *inside* the same command substitution. CR is refused. The archive is re-hashed after the listings, so a listing cannot describe different bytes from the ones hashed. `find`, `chmod` and `sha256sum` diagnostics are adjudicated the same way; `wc` is gone. | §3 `B2_RED` (`FAKE_TAR_WARNING` ×2 then `EXTRACT PASS` rc 0 — Codex's own reproduction) vs `B2_GREEN` (`tar_type_listing_diagnostics`, rc 3, before any member is parsed); `B3_RED`/`B3_GREEN` (unterminated final record: PASS vs `tar_name_listing_unterminated_final_record`); `B6_GREEN` (`tar_type_listing_failed rc=2`) |
| **F7** | HIGH | **PARTLY CLOSED, PARTLY A DEVIATION REQUEST — see §3.** The count literals are *restored inside* the permitted constants block: `MEMBER_COUNT` is derived from `MEMBERS` by `count_records`, and the result text prints the derived value, so no count literal exists anywhere to drift. The member set is still the six-file WP-I kit with `RP1-B3.sh` excluded. The rest of the derivation cannot be brought inside a constants block, so §4 has been amended to enumerate exactly four permitted classes and the amendment is raised for Lead adjudication rather than treated as settled. | §3 `B4_RED` (five-member archive vs literal six → `tar_member_count=5 expected=6`) vs `B4_GREEN` (derived → `EXTRACT PASS … members=5 verified=5`). Boundary table: §5 of the self-QA |
| **F8** | HIGH | **CLOSED.** `$RUNKIT_DIR` is a distinct frozen directory (`…\WPI_BLOCKS_DRAFT\01_RUNKIT`), matching §5's op-02 cwd, and the plan's op-02 `cwd` now points there. `$PINNED_FILES` resolves `runkit.tar` under that directory only. | §4 `F1` (`TR_PINNED path=…\01_RUNKIT\runkit.tar`) and `F2` (a same-named decoy beside the runner is never selected: pinning the decoy's digest yields `pinned_file_sha256_mismatch` against the kit copy's digest) |
| **F9** | HIGH | **CLOSED by the second option Codex offered** — the plan and runner are pinned to the file's real immutable location, rather than a copy being assembled in the draft directory. The `stdin_file` column now carries a frozen root token (`PREREG:` / `ACCEPTED:`) plus a basename; `ACCEPTED` resolves to the Stage-2 `02_PREREG` directory. **Why the copy was not made:** the kickoff binds this round to ten named files, and creating `remote_close_tree.sh` in the draft would be an eleventh. This is flagged in §3 as a Lead choice. | §4 `F3` (ops 07/08 → `root=ACCEPTED path=…\02_PREREG\remote_close_tree.sh sha256=87157f0e…`), `F4` (absent → `stdin_file_missing`), `F5` (right file, wrong root token → STOP) |
| **F10** | HIGH | **CLOSED.** `SELF_QA_TRANSPORT.md` is now produced by two standalone scripts reproduced verbatim in it, taking no arguments and declaring no shell state. Every shell RED arm executes the audited round-1 bytes read from commit `1c1c9ed1` (digests printed by the script); every runner RED arm executes the current file with the repair reverted at an anchor asserted present first. `Get-Sha256OfText`, `Test-Ascii`, `Invoke-ExternalProcess`, `Read-RemoteCloseRecord`, `Invoke-LocalBind` and both support-script `stop` functions all have executed arms — except `Test-Ascii`, which had zero call sites and has been **deleted**. Row 24's five arms are one command. Coverage accounting states arms run, arms not driven, and the direction each undriven arm fails in. | Self-QA §0 (re-execution contract), §6 (coverage), §4 arm `H` (row 24), §4 arm `I` (the delivered file, as it ships) |

---

## 2. Claude findings and nits

| # | Disposition | Evidence |
|---|---|---|
| **F1** | CLOSED — same repair as Codex F2. `CLOSE_SIZE` latched too, and sizes are now compared rather than merely counted. | §4 `A1`/`A2` |
| **F2** | CLOSED — same repair as Codex F1, including the precedence rule Claude asked to see defined. | §4 `C1`/`C2`/`C3` |
| **F3** | CLOSED in both halves: `remote_close_tree.sh` is bound by root token to its accepted location (Codex F9), and `runkit.tar` moves to a distinct `01_RUNKIT` matching binding §5 (Codex F8). §5 is amended to say the kit directory is distinct from the preregistration directory. | §4 `F1`–`F5` |
| **F4** | CLOSED — see Codex F10. The §7 binding, previously with no demonstration at all, now has a PASS arm, three discriminating FAIL arms, a set-SHA STOP arm and seven grammar STOP arms, all over a real `remote_close_tree.sh` transcript. | Self-QA §4, §6 |
| **F5** | CLOSED by derivation, not by amendment: the counts come from `MEMBERS`. The wider §4 amendment is §3 below. | §3 `B4` |
| **F6** | CLOSED. A marker gate runs before any constant is consumed, and a top-level `trap` converts any unhandled terminating error into `TR_STOP reason=runner_unhandled_error` at exit 3. `Write-TextFile` failures mid-run take that path too. | §4 `E1` (`unfilled_marker field=RECORD_ROOT`, rc 3) vs `E2` (gate and trap removed → the audit's exact localized `Test-Path` crash, exit 1); arm `I` |
| **N1** | CLOSED. `WPI_LOG_DIR='/var/log/mtc-bridge'` per §2. | Self-QA §8 |
| **N2** | **Not repaired — deliberately.** `require_block` still returns rc 3 for `block_sha256_mismatch`. Claude classified this as inherited from the accepted Stage-2 `run_r45.sh` precedent, and changing it would put the WP-I wrappers out of step with an accepted artefact on a point neither audit made required. Recorded here so the decision is visible rather than silent. | — |
| **N3** | CLOSED. The plan grammar now requires `ssh_stdin` to carry a stdin file, forbids one on every other kind, requires argv[0] to match the kind's program element-for-element, and constrains `cwd` to a preregistered allowlist. | §4 `F6`–`F9` |
| **N4** | CLOSED. In execute mode the record root is created before the remaining preflight, so `plan_sha256_mismatch`, `stdin_sha256_mismatch`, `program_*` and the new marker/grammar STOPs all persist a `TRANSPORT_RECORD.txt`. | Every execute-mode transcript shows `TR_RECORD_ROOT` before `TR_PLAN_READ`; `F2`'s `pinned_file_sha256_mismatch` is a recorded preflight STOP |
| **N5** | Half closed. §5's rows 01/03 now name the `_wpi` derivations. §1's stale collision list is **not** edited — it is prereg-side text outside §4/§5/§7 and outside this round's edit permission. For the record, `C:\WPI_ARTIFACTS` currently also holds `WPLP2B_TRANSPORT_WPLP2B-20260809T210610Z-834380c5`, exactly as Claude reported; no `WPI_TRANSPORT_*` entry exists. | §5 rows; `C:\WPI_ARTIFACTS` listing taken this session |

---

## 3. Deviation requests — Lead decision needed

**D-1 — §4 was widened, and the kickoff asked me to say so rather than do it
quietly.** The kickoff's instruction was to bring every changed executable
predicate back inside the §4 permitted constants block, "or (if genuinely
impossible) record a Lead-visible deviation request."

- What *was* brought back: the member-count predicates, now derived from
  `MEMBERS` (Codex F7 / Claude F5 closed by construction, `B4` proves it).
- What could not be: Codex F4 and F5 require `remote_setup_wpi.sh` to bind a
  parent chain and classify a diagnostic before mutating; Codex F6 requires
  `remote_extract_verify_wpi.sh` to adjudicate status, diagnostics and record
  completion before parsing; Codex F3 requires both to pin their programs. None
  of these is expressible as a constant. Leaving them out would leave three
  CRITICAL/HIGH findings open, and the kickoff's own non-negotiable list names
  the setup-script repair explicitly.
- What I did: implemented the repairs, and amended §4 to enumerate **exactly four
  permitted classes** with the boundary stated mechanically, so a future audit
  can check membership rather than argue about "minimal". Self-QA §5 maps every
  changed region of both files to one of the four; the derivation is now
  178/+51 and 246/+69 lines against the accepted originals.
- **The request:** ratify the amended §4, or direct that the two scripts be
  re-derived under a narrower contract — in which case the corresponding Codex
  findings must be re-opened rather than considered closed. I have not treated
  this as settled.

**D-2 — `remote_close_tree.sh` was pinned in place, not copied.** Codex F9
allowed either; Claude F3 preferred co-location, noting that `02_PREREG`,
`04_PREREG_R45B` and `08_PREREG_B3B` each hold their own copy. The kickoff binds
this round to ten named files and a copy would be an eleventh, so I took the
pinned-location option. If the Lead prefers co-location, it is a one-file
addition at Stage 1 plus a one-token plan edit (`ACCEPTED:` → `PREREG:`); the
runner needs no change, and `F5` already proves the wrong root token STOPs.

**D-3 — the remote tool pins are strict about symlinks.** Both remote scripts
refuse a pinned tool that is a symlink, as Codex F3's "non-following kind"
required. On a host that ships coreutils as symlinks into a multicall binary —
the QA host does — they STOP with `tool_is_symlink` rather than proceed. That is
the safe direction, but it is a real dispatch precondition: Stage 1 must confirm
each `/usr/bin/<tool>` on `GATEA-STAGING` is a regular root-owned file before
freeze. Recorded in self-QA §7.

---

## 4. Preregistration draft edits (complete list)

Four edits, all in §4 and §5, each named by a required finding.

| # | Section | Edit | Named by |
|---|---|---|---|
| 1 | §4 table, `remote_setup_wpi.sh` row | "the ONLY semantic change is the base-prefix constant" → the four enumerated classes of the round-2 derivation contract | Codex F3/F4/F5, F7 |
| 2 | §4 table, `remote_extract_verify_wpi.sh` row | same, plus "no member-count literal may exist: every count is derived from `MEMBERS`" | Codex F6, F7 / Claude F5 |
| 3 | §4 table, `remote_close_tree.sh` row, and the reused-script disposition paragraph | records that the file is not copied into the draft but named by the `ACCEPTED` root token and resolved to the frozen Stage-2 directory; adds the **round-2 derivation contract** (four classes), the operator-side program-identity rule, and the statement that the kit archive and the plan/runner live in distinct pinned directories | Codex F3, F8, F9 / Claude F3 |
| 4 | §5 op table, rows 01/02/03 | rows 01/03 now name `remote_setup_wpi.sh` / `remote_extract_verify_wpi.sh`; row 02 notes that `01_RUNKIT` is a pinned directory distinct from the preregistration directory | Codex F8 / Claude F3, N5 |

Nothing else in the draft was touched. §7 needed no edit: the repair implements
what §7 already required. §1's stale collision list (Claude N5) was left alone as
outside the permitted edit scope, and is reported in §2 above instead.

---

## 5. Files touched, and integrity

Ten files, exactly as the kickoff bounded. `RP6-P0.sh`, `SELF_QA_RP6.md` and
`STATUS_RP6_P0.md` were never written by this session.

| File | Bytes | SHA-256 |
|---|---:|---|
| `run_p0.sh` | 5215 | `e4ddf87b0869ba0fadcb9750e65f4f276c90667e788e489c5921923b0d3e1f80` |
| `run_ro.sh` | 5933 | `cd659ee9e1edceb496a5ed08707abd283e3cf5f70a3872ab6f1fdc616ac3f4e8` |
| `transport_runner.ps1` | 45066 | `2f076ed9a928656fddf22969ea4bf70de895f2c84c73f13b4c64b8040e72aa9a` |
| `TRANSPORT_PLAN.tsv` | 4631 | `3ff967294ec0f5d592701bc63940b24f2162b38f8734e38c5343930594da7149` |
| `remote_setup_wpi.sh` | 12340 | `e91bae0827f16cbefe2091980c0a049583bd8ce4173f99e802b2d54a224c29a8` |
| `remote_extract_verify_wpi.sh` | 16614 | `8eb9c499a306c11595638d8db38b1611cdd38470ba12d2c0e019116e2139d412` |
| `SELF_QA_TRANSPORT.md` | — | rewritten this round |
| `STATUS_TRANSPORT.md` | — | rewritten this round |
| `WPI_PREREGISTRATION_DRAFT.md` | — | four edits, §4 and §5 (list above) |
| `TRANSPORT_REPAIR_R2_REPORT.md` | — | this file |

`bash -n` PASS on all four shell files. Windows PowerShell **5.1.26100.8875**
`[Parser]::ParseFile` → 0 errors. 0 CR bytes in all six executable/plan files;
`transport_runner.ps1` and `TRANSPORT_PLAN.tsv` are pure ASCII. 36
`<ALLOCATE-AT-DISPATCH>` and 40 `<PIN-AT-FREEZE>` markers remain literal; no
RUNID-shaped literal exists anywhere in the set.

Scratch used and removed: `/wpi_r2_qa` (WSL) and `C:\Users\Public\wpi_r2_qa`
(ASCII-only path, required because the runner's own reader refuses a non-ASCII
plan byte and this host's profile path is non-ASCII — the same constraint the
round-1 Claude audit hit and recorded).

---

## 6. Ten-pattern self-check

| # | Pattern | Where it bit this round |
|---|---|---|
| 1 | STOP is not a result | Codex F1/Claude F2 (run-level rollup), Codex F4 (ambiguity read as absence), Claude F1 (a null parse became a host accusation). All three now have a red state |
| 2 | Whose kernel answered? | Unchanged and out of scope for the transport set; the deploy-channel attestation stays in §4/RP6 |
| 3 | The leaf is not the path | Codex F5. Parent chain bound before mutation on the setup script; container bound before contents on the extractor; the program chain bound up to `%SystemRoot%` on the operator side |
| 4 | The privileged child brought its own environment | Codex F3. Cleared environment, frozen `PATH`, run-owned `TEMP`, pinned absolute programs, no `mktemp` anywhere |
| 5 | grep is not a parser | Codex F4. Substring matching on an errno diagnostic is replaced by whole-string equality against a template calibrated from the pinned binary in the same run |
| 6 | Read the status before the stdout | Codex F6. `run_capture` adjudicates rc, diagnostics and termination before a byte is parsed |
| 7 | Nonzero read is not end of file | The plan reader's seven completion classes are all executed (`G1`–`G7`); the extractor's listing termination is now provable through command substitution |
| 8 | The name is not the identity | Codex F5. `%u:%g` on the remote side, numeric SIDs in the Windows ACL sweep; rendered names are printed as `owner_name=` only |
| 9 | The sentence outruns the probe | Claude F5/F6. §4's "ONLY semantic change" is replaced by an enumerated contract; STATUS's placeholder claim is now demonstrated by arm `I`; `TR_ENV_POLICY` states exactly what was carried and what was cleared |
| 10 | Evidence that cannot fail | Codex F10/Claude F4. Two standalone scripts, RED from the audited commit or from an asserted anchor revert, and a coverage table that names what was **not** driven |

---

## 7. Required next action

Two fresh T0 flagship auditors (`claude-opus-5` xhigh and `gpt-5.6-sol` xhigh)
must audit these exact bytes. This is round 2 of 3; if it does not produce two
accepting verdicts, one repair round remains before the cap is exhausted and the
matter goes to Barış.

This report supplies no host, freeze, execution, allocation, or Git authority,
and the set remains authority- and budget-blocked by the preregistration's own
dispatch gates.
