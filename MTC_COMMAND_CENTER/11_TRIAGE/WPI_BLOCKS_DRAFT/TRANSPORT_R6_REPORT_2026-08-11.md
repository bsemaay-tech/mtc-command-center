# WP-I transport round 6 — repair report (2026-08-11)

Implementer: Claude Opus 5 xhigh, Max account, under `KICKOFF_TRANSPORT_REPAIR_R6.md`.
Codex remains the auditor of record; this session implemented and did not audit its own
work. Input: `TRANSPORT_CODEX_R5_AUDIT_2026-08-11.md` (**REQUEST_CHANGES**, frozen commit
`37a87046`), read in full; its text binds.

## 0. Scope, method, and what was not done

- Working directory `C:\LAB\Tradingview_LAB_CLEAN`. **No commit** — the Lead commits.
- **No host contact and no network connection.** No socket of any kind was created and no
  `ssh.exe`, `scp.exe` or `sshd` process was started. The fixture re-run is on the same
  local WSL2 Ubuntu kernel rounds 4 and 5 used (`6.18.33.2-microsoft-standard-WSL2`, GNU
  Bash 5.3.9); every path it touches is under `/root/wpi_r5` on that local filesystem.
- No `git checkout`, `reset`, `stash`, `restore` or `clean` was run on any tracked file.
  The only Git commands used were `git cat-file blob`, `git rev-parse`, `git log` and
  `git status` — all read-only. Files in this tree carry uncommitted concurrent-lane work
  and none of it was disturbed.
- **`WPI_PREREG_DRAFT_ROUND1/` was not written to.** The Lead owns those drafts and had
  already applied R5-F1 there. Round 6 read them and ran `grep` over them; nothing else.
- **No byte of the transport target set changed.** All seven executable/plan targets hash
  exactly as `TRANSPORT_R5_REPORT_2026-08-11.md` §4 recorded them — re-verified, 7/7
  (§3, §4). The only executable change in round 6 is to `_r5_wsl_fixtures.sh`, the harness
  that ships beside them and is the object R5-F2 is about.
- All shell files remain LF-only (0 CR bytes, counted as bytes, per file).
  `transport_runner.ps1` parses under Windows PowerShell 5.1.26100.8875 with
  `PARSE_ERRORS=0`; it was not edited.
- Evidence is in `SELF_QA_TRANSPORT.md` §R6-1 … §R6-5, including the full verbatim
  transcript of the repaired harness.

## 1. Finding → disposition → evidence

### R5-F1 (HIGH) — the main draft still closed the open outer boundary → **APPLIED BY THE LEAD; verified read-only, not re-done**

The kickoff records this finding as already fixed by the Lead, and it is. The fix is in
commit **`008d2dde`**, which is the commit whose message records it. Round 6 did not
touch the drafts; it verified the result read-only on the committed bytes.

| site the finding named | disposition now recorded there |
|---|---|
| `WPI_PREREGISTRATION_DRAFT.md:343-344` — derivation class 5 | "**Disposition: inner child closed; outer SSH account-shell boundary OPEN.**" |
| `WPI_PREREGISTRATION_DRAFT.md:585-586` — remote-launch-domain narrative | "**This closes the inner child only; the outer SSH account-shell boundary is OPEN.**" |
| `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:408` and `:697` — the inherited "cleared launch domain" clauses | both now end "…closes the inner child only; the outer SSH account-shell boundary (a server-supplied `BASH_ENV`/`ENV` acting before `env -i`) remains OPEN, and no successor text may present the cleared inner-child domain as an end-to-end F1 closure" |

The earlier "closed by the operator side" sentence is gone: `grep -n -i "closed by the
operator side\|closed on the composition\|cannot select or influence"` over both drafts
returns nothing. The scoped sweep for `unreachable` returns seven hits, none of them
F1-related — five are the RP6-P0 `system_manager_unreachable` reason token (`:813`,
`:1063-1066`, `:1089`) and two are unrelated sentences (`:91`, `:1206`). Detail:
`SELF_QA_TRANSPORT.md` §R6-4.

**F1 remains OPEN.** Nothing in round 6 narrows it, and no client-side control was
invented.

### R5-F2 (HIGH) — the published BA-1 D026 arms did not use the claimed same argv → **REPAIRED; harness re-run; the claim now matches the harness**

**The finding is accepted in full.** Round 5 published two statements the harness it
shipped contradicted: that the RED and GREEN arms used "the same instrument, launch, and
argv", and that the GREEN refusal was byte-identical to the RED one. In fact `arm` took a
per-arm subject path and a per-arm base directory, so RED ran `$FIX/red_diag.sh` against
`$FIX/red_diag` and GREEN ran `$FIX/green_diag.sh` against `$FIX/green_diag`; the two
`CLOSE_STOP` lines therefore differed in their `path=` field. Codex's own supplemental
control — both blobs through one common subject and one common argv — returned the same
RED/GREEN answer, and Codex says so; that confirms the **code** repair and does not
repair the **evidence**. D026 makes the implementer's recorded RED/GREEN and its literal
reproducibility part of the closure evidence, so a provenance claim the harness
contradicts is a false evidence claim whatever the bytes do. Pattern 10, as recorded.

**Repair, in `_r5_wsl_fixtures.sh`:**

| round 5 | round 6 |
|---|---|
| `arm <label> <script> <base>` — each arm supplied its own subject path and its own tree | `arm <label> <built-bytes>` — every arm resets the one tree `$BA1_BASE`, installs the bytes at the one pathname `$BA1_SUBJECT`, and launches **that** with the one vector `<$BA1_EV> <$RUNID> <$BA1_WORK>` |
| instrumented variants were built at the path they were then launched from | variants are built under `$FIX/build/` and never launched from there; the arm copies the chosen build to `$BA1_SUBJECT` |
| the late-refusal control built `mkdir_wide_red` and `mkdir_wide_green` — two instrument pathnames holding identical bytes | one `mkdir_wide` instrument at one pathname serves both arms |
| the two refusals were quoted and compared by eye | `REFUSAL_BYTE_IDENTICAL` is computed on the two whole lines |
| nothing asserted that the arms shared a launch | each arm appends `<subject>\|<ev>\|<runid>\|<work>` to `$BA1_IDENT`, and a **BA-1 LAUNCH IDENTITY** banner asserts the distinct count |
| the arms printed rc and residue only | each arm also prints `SUBJECT_BUILT_FROM`, `SUBJECT_PATH`, `SUBJECT_SHA256` and `ARGV` |

`<label>` and `SUBJECT_BUILT_FROM` name only the harness's own capture files and
provenance; neither is passed to the subject or forms part of its argv.

**Re-run, verbatim** (`SELF_QA_TRANSPORT.md` §R6-2; the harness's own process rc is 0 and
it wrote **0 bytes** to its own stderr):

```text
########## BA-1 RED - PRE-REPAIR bytes + INSTRUMENT 1 (mkdir creates, warns, rc 0)
SUBJECT_BUILT_FROM=/root/wpi_r5/build/red_diag.sh
SUBJECT_PATH=/root/wpi_r5/close_subject.sh
SUBJECT_SHA256=a61ac611fd8da95338ff9467f81a27f1097d1bd28b7a0da806f7bc79c048b2cf
ARGV=[/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] [/root/wpi_r5/ba1/work]
SCRIPT_RC=3
CLOSE_STOP reason=work_dir_mkdir_diagnostics path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 detail=injected_success_diagnostic
RESIDUE_PRESENT=yes path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0

########## BA-1 GREEN - REPAIRED bytes + THE SAME INSTRUMENT 1
SUBJECT_BUILT_FROM=/root/wpi_r5/build/green_diag.sh
SUBJECT_PATH=/root/wpi_r5/close_subject.sh
SUBJECT_SHA256=e48e1a07e3ef4e2a4a6f48c830cf0389bb883f42f4a33922008f3fd5957758b4
ARGV=[/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] [/root/wpi_r5/ba1/work]
SCRIPT_RC=3
CLOSE_STOP reason=work_dir_mkdir_diagnostics path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 detail=injected_success_diagnostic
RESIDUE_PRESENT=no

########## BA-1 FENCE DISCRIMINATING POWER - old and new assertion, same deviant output
OLD_ASSERTION_LINE : 402:[ -z "$MKDIR_OUT" ] || stop "work_dir_mkdir_diagnostics path=$WORK detail=$MKDIR_OUT"
NEW_ASSERTION_LINE : 483:[ -z "$MKDIR_OUT" ] || stop "work_dir_mkdir_diagnostics path=$WORK detail=$MKDIR_OUT"
OLD_REFUSAL        : CLOSE_STOP reason=work_dir_mkdir_diagnostics path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 detail=injected_success_diagnostic
NEW_REFUSAL        : CLOSE_STOP reason=work_dir_mkdir_diagnostics path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 detail=injected_success_diagnostic
REFUSAL_BYTE_IDENTICAL=yes

########## BA-1 LAUNCH IDENTITY - every arm above used ONE pathname and ONE argv
BA1_ARMS_RECORDED=10
DISTINCT_SUBJECT_ARGV_LINES=1
THE_LINE=/root/wpi_r5/close_subject.sh|/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0|WPIR5-FIXTURE-P0|/root/wpi_r5/ba1/work
```

The excerpt above is contiguous within each banner; the elided lines are the
`RESIDUE_LISTING` / `EVIDENCE_TREE_AFTER` listings, which are in §R6-2 in full along with
the other six arms.

**One pathname, one argv, ten arms.** `DISTINCT_SUBJECT_ARGV_LINES=1` is the whole
finding answered: if any arm had differed in its subject pathname or in any of its three
arguments, that count would exceed 1 and the same-argv claim would be false again. Ten
distinct `SUBJECT_SHA256` values across those ten arms is the complement — the pathname
and the argv are constant and the **bytes** are the variable, which is what D026 asks of
a RED/GREEN pair.

`SUBJECT_SHA256` hashes what is installed at the common pathname — the fixture-retargeted
and, where declared, instrumented form of the delivered bytes — **not** a delivered file.
The two delivered identities under test are printed once by the `FIXTURE ENVIRONMENT`
banner: `29b6412a466c10854ddf09effc8d5216317738a012235ce563c9764a9e0c40ef` for RED (the
pre-repair blob, read with `git cat-file blob 61696132a5f2fce97aad4054d41a780297ff21a1`,
the object the round-5 kickoff named) and
`8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf` for GREEN (the
working-tree file, unchanged since round 5). `SUBJECT_BUILT_FROM` names which of the two
each arm's bytes derive from.

**The carried assertion is unchanged, as the kickoff requires.** The fence is
`[ -z "$MKDIR_OUT" ] || stop "work_dir_mkdir_diagnostics …"` — line 402 in the pre-repair
bytes, 483 in the repaired bytes, predicate and reason token identical — and both arms
refuse the same injected diagnostic. It kept its discriminating power in round 5 and
keeps it now; nothing about it was touched.

**Nothing else moved.** Every one of the ten arms reached the same disposition it reached
in round 5: same `SCRIPT_RC`, same residue answer, same reason tokens, including the
deliberately uncovered nonzero-create arm (`object_after_failed_create=present`, residue
present by design and named in the record) and the `rm_noop` arm
(`CLOSE_STOP reason=work_dir_removal_failed`). The two clean-run regression arms now
differ in exactly one field, and because they share the tree and the argv that field can
be read off the two lines directly:
`removal=adjudicated_on_every_exit_path` → `removal=adjudicated_on_every_exit_path_after_a_zero_status_create`.

**The round-5 transcript is withdrawn, not archived beside the new one.** D026 makes the
published transcript the reproducibility target; two transcripts for one harness would
give a re-auditor two targets, one of them wrong. `SELF_QA_TRANSPORT.md` §R5-6 now carries
the withdrawal and the reason, §R5-1 carries the struck claim with its correction, and
§R6-2 carries the single verbatim transcript the delivered harness produces.

### R5-F3 (MEDIUM) — status and evidence still called committed draft edits pending → **CORRECTED; the terminal disposition is bound to its commits**

**The finding is accepted in full.** The four cross-directory draft edits — three BA-3
sentences and the BA-1 draft mirror — were applied by the Lead **before** the freeze and
are present in commit `37a87046`, the very commit Codex audited. The round-5 evidence
chain nevertheless recorded them as outstanding. Those statements described the
implementer session's boundary accurately and were false as the final status of the
commit; Pattern 13, as recorded.

Verified read-only on the committed bytes:

| edit | site | check |
|---|---|---|
| 1 — BA-3 | `WPI_PREREGISTRATION_DRAFT.md` §6 | `grep -c 'The reason recorded is the'` = **1** |
| 2, 3 — BA-3 | `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md` §6 and Gap 10 | `grep -c 'first applicable reason recorded'` = **2** — both copies present, as Band A requires |
| 4 — BA-1 | `WPI_PREREGISTRATION_DRAFT.md` §4, derivation class 6 | `grep -c 'object_after_failed_create=present\|absent'` = **1** |

Bound identities — the two draft blobs and the commits that carry them:

| file | blob at `37a87046` (BA-3 ×3 + BA-1 mirror) | blob at `008d2dde` = current `HEAD` (R5-F1) |
|---|---|---|
| `WPI_PREREGISTRATION_DRAFT.md` | `f2bc8f682f054d9283922d17501ea0dfa94d0bfc` | `35936fe464c8b1d7faf892bcc809aac38da48b1e` |
| `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md` | `0c6e8030eaf0b5858f1af34fb6fd29fc65cff2a2` | `1aad4f61a76085605cf3a2664f012d4e3d7407ba` |

Neither draft is modified in the working tree relative to `HEAD`, so the bytes checked
above are the committed bytes.

**Corrected in every place the finding named, plus one it did not:**

| file | what changed |
|---|---|
| `STATUS_TRANSPORT.md` | the BA-3 bullet's "until those three edits land, BA-3 is not fully closed" replaced with **applied in `37a87046`, BA-3 FULLY CLOSED**; new "What changed in round 6" section; header block now records the three round-5 findings as closed |
| `TRANSPORT_R5_REPORT_2026-08-11.md` | new "ROUND-6 CORRECTIONS — READ FIRST" block; §0's not-applied bullet, §BA-1's site table, §BA-3's heading and three site rows, §BA-3's closing sentence, §5 in full, §6's last item and §7 all struck and corrected in place, with the commit cited |
| `SELF_QA_TRANSPORT.md` | §R5-0's BA-3 row and §R5-4 updated to APPLIED with a round-6 status box; new §R6-3 with the per-edit checks and the bound blob identities |
| `TRANSPORT_R5_DRAFT_EDITS_PENDING.md` | **not deleted.** Marked **SUPERSEDED — HISTORICAL RECORD ONLY** in a box at the top, with the verification and both commits; the file's own "BA-3 is NOT fully closed" status line struck in place. It is kept because it is the specification a re-auditor needs in order to check that what landed is what was handed over |
| `_r5_wsl_fixtures.sh` | not affected by R5-F3 |

**Consequence:** **BA-3 is fully closed** and **F1's draft mirror is aligned**. F1 itself
stays OPEN — that is a finding about the boundary, not about the drafts.

## 2. What was NOT changed, and why

- **The seven transport targets** — byte-unchanged, 7/7 verified against round-5 §4. No
  round-5 finding and no round-6 finding calls for a code change; R5-F2 is about the
  harness's provenance and R5-F3 about status text.
- **The carried BA-1 fence** — untouched. The kickoff explicitly requires it to stay as
  it is, and the re-run confirms it still refuses in both arms.
- **`WPI_PREREG_DRAFT_ROUND1/`** — read only. The Lead owns it and had already applied
  R5-F1.
- **`RP6-P0.sh`, `RP7-WPI-RO.sh`** — not read, not touched; other lanes own them.
- **BA-2's disposition** — unchanged. Codex re-executed all seven arms in round 5 and
  found them matching the withdrawn-claim disposition; the round-6 re-run reproduces the
  same seven results.
- **The F1 local-model arm** — unchanged, and still labelled in the transcript as **not**
  closure evidence and **not** the real transport path.
- **No fence anywhere was weakened**, and no predicate in any delivered file was changed
  in round 6.

## 3. Static gates

| gate | result |
|---|---|
| the seven executable/plan targets vs round-5 §4 SHA-256 | **7/7 identical — no target byte changed** |
| `bash -n` on all five delivered shell files | rc 0 for each |
| `bash -n _r5_wsl_fixtures.sh` | rc 0 |
| CR bytes per file (`tr -cd '\r' \| wc -c`) | 0 for all seven targets, the harness, and every document edited this round |
| Windows PowerShell 5.1.26100.8875 parse of `transport_runner.ps1` | `PARSE_ERRORS=0` |
| placeholder census over the seven executable/plan targets | `alloc=37 pin=38` — unchanged from rounds 4 and 5 |
| `_r5_wsl_fixtures.sh` process rc / its own stderr | 0 / **0 bytes**, 280 stdout lines |
| BA-1 arms recorded / distinct subject+argv lines | 10 / **1** |
| RED vs GREEN refusal | `REFUSAL_BYTE_IDENTICAL=yes` |
| RED / GREEN delivered identities printed by the fixture | `29b6412a…` / `8892574f…` — both as declared |

## 4. Delivered identities (round 6)

The frozen set — **unchanged from round 5**:

| Target | Bytes | SHA-256 | `<ALLOCATE-AT-DISPATCH>` | `<PIN-AT-FREEZE>` | CR | changed in r6 |
|---|---:|---|---:|---:|---:|:--:|
| `run_p0.sh` | 13,608 | `4f608ad546402ad9587eeac237c16c7c3c3e707ebf4e6cb589e9459f08413c0c` | 6 | 8 | 0 | **no** |
| `run_ro.sh` | 13,470 | `3dea6e64b087488fda2ab9bac8b66fceac1c13e70719b3ce9d81797a50443e3c` | 6 | 4 | 0 | **no** |
| `transport_runner.ps1` | 71,137 | `4db0fbd17f9b32da13564a9ce2d0786283151737d81bcee031ed2bcb7b347fd2` | 3 | 7 | 0 | **no** |
| `TRANSPORT_PLAN.tsv` | 7,970 | `e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c` | 22 | 7 | 0 | **no** |
| `remote_setup_wpi.sh` | 26,483 | `4428a60da02415ef1b7c84561b1bba458ee7f1affcfe9d33c4b1c3f07bcb5aa5` | 0 | 3 | 0 | **no** |
| `remote_extract_verify_wpi.sh` | 23,592 | `5b3c0b225fdca18fd0a074a7bcce3c7124930e62eacc9e41da236db28585a55b` | 0 | 7 | 0 | **no** |
| `remote_close_tree_wpi.sh` | 32,630 | `8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf` | 0 | 2 | 0 | **no** |

The evidence and status documents, and the harness beside the set:

| File | Bytes | SHA-256 | CR | changed in r6 |
|---|---:|---|---:|:--:|
| `SELF_QA_TRANSPORT.md` | 193,981 | `c025bacd9514cf423a2cdfcdd7049486177ac4d9c9f8edb9c0a3062b5b7d98a3` | 0 | yes |
| `STATUS_TRANSPORT.md` | 22,096 | `7e48246e77fb42bd965070c0fd6cdf0d7d3d7722fb3e018e0b21d8bfbc9a5dee` | 0 | yes |
| `_r5_wsl_fixtures.sh` | 21,221 | `a2bb6f6e3c0022aa001db7adb58189649acab9b23b522dc0544b018f9ce7971b` | 0 | yes |
| `TRANSPORT_R5_REPORT_2026-08-11.md` | 30,263 | `b45ecd82d9fcc8bcb76d0a814cee3e194a3cfe36524f45c54fc0bb1cff950469` | 0 | yes |
| `TRANSPORT_R5_DRAFT_EDITS_PENDING.md` | 8,834 | `89e85b72191ef2d663f3119cd93697796a477654daf4f8ad39839f2617779a46` | 0 | yes (superseded box) |
| `TRANSPORT_R4_REPORT_2026-08-11.md` | 38,356 | `33bdeced4f70d4e8e0d22b252b79afb1dabd0f13c5c4a8a05447e8f4f08b9b62` | 0 | **no** |

This report is not in either table; its own identity is whatever the Lead commits.

## 5. Not applied — stated plainly

**Nothing.** Every item the kickoff assigned to round 6 is applied in this working tree:
the harness repair and its re-run (R5-F2), the status/evidence corrections and the
superseded marking (R5-F3), and the read-only verification and reporting of the Lead's
R5-F1 fix. There is no `PENDING-LEAD-EXECUTION` item and no cross-directory hold this
round — the one directory this session could not write to, `WPI_PREREG_DRAFT_ROUND1/`,
needed no round-6 edit because the Lead had already made it.

The Lead still commits, and the kickoff records the Lead's own intention to re-run the
BA-1 fixture verbatim. The command is in `SELF_QA_TRANSPORT.md` §R6-2; the pre-repair arm
needs `git cat-file blob 61696132a5f2fce97aad4054d41a780297ff21a1` written to a scratch
`remote_close_tree_wpi.sh` and that directory passed as the harness's second argument.

## 6. What I did not verify

- Any real connection behaviour against `GATEA-STAGING`. No socket was opened.
- The **real** SSH account-shell boundary. The F1 arm is a local model of the composition
  step, executed and labelled as such in the transcript; it demonstrates that the boundary
  is open and is explicitly **not** closure evidence for anything.
- The remote scripts' behaviour on the real host, including whether `/proc/self/environ`
  and the `/usr/bin` pin set have the shapes these rounds assume there.
- Whether the target host's `sshd`/account shell honours a startup file. F1 is OPEN
  because the transport **cannot establish** that it does not.
- The **content** of the four applied draft edits against Band A's intent. Round 6
  verified that the specified anchors are present in the committed bytes and that the two
  successor copies both exist; it did not re-derive whether the replacement wording is the
  right wording. That was round 5's judgement and Codex's round-5 audit examined the
  applied text at `37a87046`, finding the classifier order matched the narrowed prose.
- Any part of `RP6-P0.sh` or `RP7-WPI-RO.sh`; neither was read or modified this round.
- Anything about the concurrent lanes' uncommitted work in this tree. It was left alone.

## 7. Required next action

Codex re-audit under T0 policy against the identities in §4. The two questions this round
most needs adversarial attention on:

1. **Does the repaired harness now support the sentences that cite it?** The claim is
   narrow and machine-checked — one subject pathname, one argument vector, ten arms,
   `DISTINCT_SUBJECT_ARGV_LINES=1`, `REFUSAL_BYTE_IDENTICAL=yes` — but the assertion is
   computed *by the harness under audit*. Is there an arm, or a field in an arm's record,
   that still varies with something other than the delivered bytes?
2. **Is withdrawing the round-5 transcript the right call, or does it lose evidence?** The
   alternative was to keep it beside the corrected one and label it. Round 6 judged that
   two transcripts for one harness give a re-auditor two reproducibility targets, one of
   which is known-wrong, and that the historical account survives in §R5-1's struck text
   and in this report.

One item needs the Lead rather than the auditor: re-confirming the round-4 open items that
F1's status change touches — derivation classes 5 and 6 are still new permissions, and
class 5 buys an inner-child guarantee rather than the end-to-end one round 4 implied.

This report grants no host, freeze, allocation, execution, dispatch, or Git authority.
