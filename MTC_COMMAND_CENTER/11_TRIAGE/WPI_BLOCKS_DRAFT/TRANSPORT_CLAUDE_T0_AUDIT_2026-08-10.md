Cleanup is complete, WSL and `C:\Users\Public` scratch removed, and the repo is untouched — all eight transport files carry the same digests I recorded at the start (the two modified tracked files, `RP7-WPI-RO.sh` and the prereg draft, are the concurrent RP7 round‑3 session's work, not mine; I re-verified §1/§4/§5/§7 and §8 row 24 against the current bytes after that edit landed).

---

# TRANSPORT SET — CLAUDE FLAGSHIP T0 AUDIT (`claude-opus-5`, xhigh, fresh session)

## VERDICT: **REQUEST_CHANGES** — 6 required repairs, 5 optional nits

The blocking one: **ops 11 and 12 — the entire local half of the §7 evidence binding — cannot return 0 under any host state.** A `$Matches` clobber makes every remote digest parse as null, so a byte-perfect run reports `digest_differs` for every evidence file, `TR_RUN FAIL`, exit 1 — after two one-use RUNIDs have already been spent. I proved it RED against the delivered bytes and GREEN against a one-line repair, using a real `remote_close_tree.sh` transcript. The self-QA never executed either op, which is exactly how it shipped.

Scope note: the set is independently authority- and budget-blocked by the prereg's own dispatch gates (§0 F6 amendment, §12). That is pre-existing state, not part of this verdict.

---

## 1. Audit method and integrity

Read-only. No SSH, SCP, host IP, credential, service, broker or trading contact. The only sockets opened were `127.0.0.1` listener/connect fixtures for the op-06 classification arms. No RUNID allocated. All fixtures ran in scratch (`%TEMP%\claude\…\scratchpad`, an ASCII-only path `C:\Users\Public\wpiqa` required because the runner's own `Test-SafeArg` forbids `~` and non-ASCII, and WSL `/tmp`), all removed afterwards.

```
git status --porcelain  → no entry authored by this session
the eight transport files, re-hashed after all fixtures:
8b2c520aa342f3f49fc9f0ad543b6c8a918c995b66e1cae8a1dd1c543b9dbfe9  run_p0.sh
88f9f736e68c4978cc15d29621082d0395dc49de97a4c8efc79893fc536ad3e0  run_ro.sh
84942683a6c25973f1785e48dc8ed76aea99be27c9ee50bf1ed5f7726b518cdc  transport_runner.ps1
bcc10a6a71456580a93eb0da6c1f9bc03da154ae59cf14a0821e6b8bd6edd3b5  TRANSPORT_PLAN.tsv
5b2598184b228eef5d93c7f4ef7a5aa8a627ffbdea8c71e6cc093b416ebb0a34  remote_setup_wpi.sh
17ed8f3f8d80a79fc1b132ff1ef55cf0677da13c551da30e0db7531935c1f6f2  remote_extract_verify_wpi.sh
13b8204a835922824b1af817752f879be5b7b54c14d5095073a64877c7ba6cb4  SELF_QA_TRANSPORT.md
89d4b99fb382b22777e94700cc63f794cbd10b711a8286b86e71d3096aede7c9  STATUS_TRANSPORT.md
```

Environment: Windows PowerShell **5.1.26100.8875**; WSL Ubuntu (bash 5.x) and Git Bash 5.2.37 for the shell fixtures.

---

## 2. V-rows

| V | Item | Verdict | Evidence |
|---|---|---|---|
| **V1** | Wrapper contract: symlink refusal, `/dev/null` on every child, STOP-first, rc conveyance | **PASS** | Independent WSL fixtures, both wrappers. `-f` alone proven not a refusal: `test -f symlink→regular` = TRUE while `test -L` = TRUE. RED (delete `[ ! -L ]`) admits the symlink, block runs, `RC=0`, `TAIL_EXECUTED`; GREEN → `P0W_STOP reason=block_is_symlink`, `RC=3`. RED (drop `</dev/null` on the target source only) → `BLOCK stdin=STOLEN got=[]`, `RC=1`, tail lost; GREEN → `BLOCK stdin=eof`, `P0W/ROW done`, `TAIL_EXECUTED`, `RC=0`. All three source lines carry `</dev/null` in both wrappers (grep count = 3 each). rc conveyance: block exit 3→3, 1→1, 0→0, no re-classification. |
| **V2** | Runner: §5 op fidelity, first-FAIL with `always` retained, per-op capture, remote-vs-local binding local-only, PS 5.1 semantics | **REQUEST_CHANGES** | Op list matches §5 exactly, 12 ops, 13 records, kinds/run_when/argv/cwd all as tabled (one deviation: op 02 cwd — F3). First-FAIL RED/GREEN executed: RED (`if ($false)`) runs op 02; GREEN emits `TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch`, `02.rc=skipped`, `02.elapsed_ms=0`, and both `always` ops still run. Per-op `.argv/.stdout/.stderr/.rc/.elapsed_ms` present for all four ops incl. the skipped one; `TRANSPORT_SHA256SUMS.txt` contains `TRANSPORT_RECORD.txt`. `Invoke-LocalBind` verified to open no socket. PS 5.1 parse PASS; no `&&`/`\|\|`/ternary; the `SocketException` unwrap is by type, no localized text. **But F1 and F2.** |
| **V3** | TSV reader: clean EOF / unterminated populated final record / hard read error | **PASS** | Re-run independently: `TR_PLAN_READ completion=clean_eof records=2` / `TR_STOP reason=plan_unterminated_final_record` rc 3 / `TR_STOP reason=plan_read_error detail=…MethodInvocationException` rc 3. Three distinct classifications; no partial row reaches the parser. Reproduces SELF_QA §6. |
| **V4** | Row-24 probe: classified outcomes, bounded, no false-FAIL route | **PASS** | Five arms driven on loopback: `connection_refused` rc 0 (2027 ms, well inside 20000); `connected` → `B6_FAIL reason=host_reachable_8790 outcome=connected` rc 1; `port_invalid`, `timeout_invalid`, `argv_malformed` → `B6_STOP reason=external_probe_not_evaluable outcome=<o> rc=3 detail=<d>` — byte-exact against §8 row 24's grammar. Only rc-1 route is a completed handshake. `payload_bytes=0` earned (BeginConnect/EndConnect only). Bound validated 1..60000. **`timeout` arm undriven** — it needs a non-loopback destination, outside the read-only envelope; SELF_QA §8 discloses this honestly. |
| **V5** | Derivation minimality vs accepted originals | **PASS-WITH-CHANGES (F5)** | Both originals byte-verified: `remote_setup.sh` 4976 B `faee3725…`, `remote_extract_verify.sh` 8270 B `ba0bef0e…`. Setup diff = **one line**, the prefix constant — exactly what §4 permits. Extractor diff = the archive-constants block **plus five executable count predicates 9→6** (F5). Member list = `RP0-LIB.sh, RP0-BOOTSTRAP.sh, RP6-P0.sh, RP7-WPI-RO.sh, run_p0.sh, run_ro.sh`; `RP1-B3.sh` excluded ✓. `<PIN-AT-FREEZE>` block clearly marked and inert (7 markers). |
| **V6** | Placeholders intact, nothing minted, no concrete RUNID | **PASS-WITH-CHANGES (F6, F7)** | 37 `<ALLOCATE-AT-DISPATCH>` + 32 `<PIN-AT-FREEZE>` across the set, all literal; no RUNID-shaped literal anywhere. Every concrete constant traced to a binding source: `RP0_LIB_SHA`/`RP0_BOOTSTRAP_SHA` re-derived from accepted `01_RUNKIT` bytes (18968 B `4a404d7b…`, 1937 B `e7d748f6…`) ✓; `87157f0e…` = accepted `remote_close_tree.sh` ✓; `WPI_MAINPID=189813` is preregistered at §8 row 4, not minted ✓. **But** the runner has no fail-closed guard for `<ALLOCATE-AT-DISPATCH>` (F6) and `WPI_LOG_DIR` is left unfilled though §2 resolves it (F7). |
| **V7** | Re-run key fixtures; RED cases actually falsify; coverage | **REQUEST_CHANGES (F4)** | Every SELF_QA fixture I re-ran reproduced its recorded output without edits (§3, §6, §7, §8, §9, §10). But three functions and two of twelve ops have **no executed arm in the self-QA**, and one function is dead code. Ledger in §4 below. |
| **V8** | Hashes, `bash -n`, PS 5.1 parse | **PASS** | All eight digests + byte counts match SELF_QA §10 and STATUS exactly; plan sha `bcc10a6a…` matches the runner's own `TR_PLAN` line. `bash -n` PASS on all four shell files and on the accepted `remote_close_tree.sh`. `[Parser]::ParseFile` → `POWERSHELL_5_1_PARSE PASS`. TSV: 4575 B, **0 CR bytes**, 0 bytes >127, LF-terminated ✓. `transport_runner.ps1` is pure ASCII, matching its "ASCII-only by construction" header. (The 6/9 high bytes in the two derived shell scripts are em-dashes inherited verbatim from the accepted originals — not introduced.) |

---

## 3. Findings — most severe first

### F1 — REQUIRED, SEVERE. `$Matches` clobbering nulls every remote digest: ops 11 and 12 can never PASS
`transport_runner.ps1:376–381`

```powershell
if ($line -match '^CLOSE_DIGEST ([0-9a-f]{64})  (.+)$') {
    if ($state -ne 'digests') { … }
    $rel=$matches[2]
    if ($rel -notmatch '^[A-Za-z0-9._/-]+$' -or $rel.StartsWith('/') -or $rel -match '(^|/)\.\.?(?:/|$)') { … }
    if ($digests.ContainsKey($rel)) { … }
    $digests.Add($rel,$matches[1]); continue      # <-- $matches is no longer the CLOSE_DIGEST match
}
```

The path-safety guard's `-notmatch` **succeeds** against `'^[A-Za-z0-9._/-]+$'` for every well-formed relative path, and a successful `-notmatch` repopulates `$Matches` with a single-group match. `$matches[1]` at the `Add()` call is therefore `$null`, not the sha256. Isolated mechanism (PS 5.1):

```
after CLOSE_DIGEST match : matches[1]=[d3580109246af482d69508e1254eefc0996888473aaf229b7c04964b94fd90d7]
rel=[aaa.txt]
guard_bad=False
after guard             : matches.Count=1 matches[0]=[aaa.txt] matches[1]=[]
value that Add() stores : []  <-- should be the sha256
```

**Executed falsification.** I generated a genuine `CLOSE` transcript by running the accepted `remote_close_tree.sh` (7470 B `87157f0e…`, only `EXPECT_OWNER` substituted for the sandbox) over a 3-file fixture tree, then drove the delivered runner through ops 07 → 09 → 11 with that transcript and the identical tree:

```
=== GREEN_binding_matches ===   (nothing mutated; local bytes == remote bytes)
TR_OP_END id=11 rc=1 expect_rc=0 …
TR_FIRST_FAIL id=11 rc=1 expected=0 later_sequence_ops=skip always_ops=run
TR_RUN FAIL base_run=QA first_fail=11
  | TR_BIND_COUNTS remote=3 local=3
  | TR_BIND_DIFF digest_differs=aaa.txt
  | TR_BIND_DIFF digest_differs=p0.log
  | TR_BIND_DIFF digest_differs=sub/nested.txt
```

Independently computed, the three local digests are **identical** to the three `CLOSE_DIGEST` values, name-for-name, size-for-size. Causation, one-line latch of the capture before the guard:

```
=== RED_as_delivered ===                 rc=1  TR_RUN FAIL   digest_differs ×3
=== GREEN_one_line_repair ===            rc=0  TR_RUN PASS
  | TR_BIND_SET remote_set_sha256=561dbcea…c208 reconstructed=561dbcea…c208
  | TR_BIND_PASS files=3
```

Consequences:
1. **Ops 11 and 12 return 1 whenever the close record parses, 3 when it does not — never 0, under any host state.** §7's "local half of the binding" never executes.
2. `TR_BIND_SET` is unreachable in the delivered bytes (`$ok=$false` returns before the set comparison), so `CLOSE_DIGEST_SET_SHA256` is **never** compared. §7's stated requirement — "the reconstructed digest-set rendering must reproduce `CLOSE_DIGEST_SET_SHA256`" — is not met by any code path.
3. A correct run produces `TR_RUN FAIL first_fail=11` plus `TR_ADDITIONAL_MISMATCH id=12`, i.e. a **false deviant-state verdict against the host** — after both one-use RUNIDs are spent and unrecoverable (§1: "if allocation fails for any reason it is burned").
4. Every RED mutation of the binding is non-discriminating while this stands: my `RED_local_byte_changed`, `RED_local_file_missing`, `RED_extra_local_file` and `RED_close_set_sha_tampered` cases all produced the same rc 1 as the unmutated GREEN. Any future QA that "passes" these RED cases proves nothing (Pattern 10).

The same idiom appears at `:391–395` for `CLOSE_SIZE` and is **accidentally safe** there only because that guard's regex does *not* match a well-formed path, leaving `$Matches` intact. Repair both, and prefer latching every capture immediately after the match.

*Patterns:* 1 (STOP/FAIL truthfulness — a null parse becomes a host accusation), 5 (a captured group used after the matcher has been reused), 10 (the arm was never executed).

---

### F2 — REQUIRED. A not-evaluable operation is rolled up as FAIL; the runner's documented exit 3 is unreachable
`transport_runner.ps1:504–508` and `:531–532`, against its own header `:8–10` and the prereg's binding cross-cutting rule.

The header states: `3 = could not evaluate the plan, operation, or evidence binding`. The op loop classifies not-evaluable correctly at the op level (`$rc=3`), then:

```powershell
if ($rc -ne $op.ExpectRc) { $anyMismatch=$true; … }
…
if ($anyMismatch) { exit 1 }
```

No path converts an op-level rc 3 into a run-level exit 3. Every op preregisters `expect_rc = 0` (§5), so **every** STOP becomes FAIL. Executed:

```
TR_OP_END id=11 rc=3 …            (TR_BIND_STOP reason=remote_close_binding_mismatch)
TR_FIRST_FAIL id=11 rc=3 expected=0 …
TR_RUN FAIL base_run=QA first_fail=11
RUNNER_RC=1
```

Reachable for: every `B6_STOP` from op 06 (three arms driven, all rc 3); every wrapper STOP (driven: `P0_STOP reason=missing_tool tool=systemctl` → rc 3); `cwd_absent`; `operation_exception`; every `TR_BIND_STOP`; and ssh's own rc 255 on connection/auth failure — a pure transport failure in which no probe observed anything, reported as `TR_RUN FAIL`.

This is the defect the whole preregistration exists to prevent. Round 1.3's binding rule (draft lines 21–22): *"an inability to evaluate must STOP (rc 3), never FAIL (rc 1)."* `[B3-ADJ Classification]` records the Lead having to hand-adjudicate exactly this — an operator-side rc 3 as could-not-evaluate rather than FAIL. As delivered, the runner reintroduces that manual adjudication for every STOP.

Minimal fix: track a separate `$anyNotEvaluable`, emit `TR_RUN STOP`, and exit 3 when any executed op returned 3 with no genuine deviant-state mismatch; or narrow the header to say the runner never distinguishes them, and record the disposition rule in §6. The first is right — §5's `always` ops exist precisely so a STOPped stage still gets its evidence closed and bound, which is a different operator action from a FAIL.

*Patterns:* 1 (primary), 9 (the header sentence outruns the code).

---

### F3 — REQUIRED. The transport set is incomplete, and op 02's cwd deviates from binding §5
`TRANSPORT_PLAN.tsv` ops 02, 07, 08; `transport_runner.ps1:26, 33–35`

`TRANSPORT_PLAN.tsv` pins ops 07/08 to `stdin_file=remote_close_tree.sh`, `stdin_sha256=87157f0e…` — a **concrete, already-frozen** digest. That file is not in `WPI_BLOCKS_DRAFT/`. The runner resolves every stdin file against `$PREREG_DIR`, which is that directory.

The gap is masked in the draft because `plan_pin_unfilled` (`:156`) trips before the stdin-existence loop (`:201`), so SELF_QA §9's recorded STOP does not reach it. I simulated a Stage-1 freeze in scratch (allocation placeholders filled, each stdin pinned to its real digest, nothing else changed):

```
=== RUN 1: transport set exactly as delivered ===
TR_PLAN_ROWS count=12
TR_STDIN op=01 file=remote_setup_wpi.sh          sha256=5b259818…
TR_STDIN op=03 file=remote_extract_verify_wpi.sh sha256=17ed8f3f…
TR_STDIN op=04 file=run_p0.sh                    sha256=8b2c520a…
TR_STDIN op=05 file=run_ro.sh                    sha256=88f9f736…
TR_STOP reason=stdin_file_missing op=07 path=…\remote_close_tree.sh

=== RUN 2: after adding the accepted remote_close_tree.sh ===
TR_STDIN op=07 file=remote_close_tree.sh sha256=87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e
TR_STDIN op=08 file=remote_close_tree.sh sha256=87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e
TR_STOP reason=pinned_file_pin_unfilled path=…\runkit.tar
```

The set is a nine-file set delivered as eight. Every accepted precedent co-locates it: `02_PREREG/`, `04_PREREG_R45B/` and `08_PREREG_B3B/` each hold their `remote_close_tree*.sh` beside their plan and runner.

Second half of the same finding: the runner collapses `$RUNKIT_DIR = $PREREG_DIR` (`:26`) and pins `runkit.tar` there, and TSV op 02 sets `cwd` to the draft directory. Binding §5 records op 02 as `runkit.tar gatea@…:<REMOTE_BASE>/kit/runkit.tar` **(cwd `01_RUNKIT`)**, and the accepted Stage-2 runner keeps `$RUNKIT_DIR` (`…\01_RUNKIT`) separate from `$PREREG_DIR` (`…\02_PREREG`), with the plan's `scp_up` row using the `01_RUNKIT` cwd. As delivered, a ~100 KB binary archive must be dropped into a git-tracked triage directory, and the accepted kit structure (`ARCHIVE_MEMBERS.txt`, `BLOCK_IDENTITIES.tsv`, `SOURCE_IDENTITY.txt`, `STAGE1_RECORD.md`, `runkit.tar.sha256`, `stage1_build.py`) has nowhere to live. Either restore a separate kit directory or amend §5 — §5 is binding, so silence is not an option.

*Pattern:* one-off 1 ("the hidden fifth deliverable" — enumerate the deliverable set mechanically; here a pinned member is absent rather than extra).

---

### F4 — REQUIRED. Self-QA coverage: §7's binding and the process-launch path used by 8 of 12 ops have no executed arm
`SELF_QA_TRANSPORT.md`

Every fixture in the self-QA uses `tcp_probe` ops only (§6 "a one-row local `tcp_probe` plan"; §7 "four loopback probes"). Consequently:

| function | driven by SELF_QA | driven by me | note |
|---|---|---|---|
| `Read-RemoteCloseRecord` | **no** | yes | ships broken — **F1** |
| `Invoke-LocalBind` | **no** | yes | ships broken — **F1** |
| `Get-Sha256OfText` | **no** | only after repair | reachable only from `Invoke-LocalBind` |
| `Invoke-ExternalProcess` | **no** | yes (8 processes) | executes ops 01–05, 07–10 — 8 of 12 |
| `Test-ReparsePoint` | not recorded | yes | |
| `Test-Ascii` (`:85`) | **impossible** | impossible | **defined, zero call sites — dead code** |

§5 demands, for first-FAIL, *"exact paste-and-run commands and real output … RED … then GREEN"* and that *"a narrated plan or reconciled op count cannot satisfy this gate."* §7's binding is subject to the same standard and has no demonstration at all. Under D026 the §7 binding claim in `STATUS_TRANSPORT.md` ("11/12 local-only remote/local digest-set binding in `transport_runner.ps1`") is **supplemental, not closure evidence** — and F1 shows why the distinction is not academic. I have supplied a working harness shape: run the accepted `remote_close_tree.sh` over a fixture tree, feed its real transcript as `ops/07.stdout`, stage the tree as the retrieved copy, and drive op 11 — with RED cases for a changed byte, a missing file, an extra file, a tampered set-SHA, a RUNID mismatch, and a dropped digest line.

Also newly established (positives that were previously unverified): on this PS 5.1 build `Start-Process -Wait -PassThru` with `RedirectStandardInput/Output/Error` conveys the child exit code faithfully (`cmd /c exit 1` → rc 1), and the `TR_BIND_SET` reconstruction is byte-correct once F1 is repaired (ordinal sort of relative paths reproduces `LC_ALL=C` sort of absolute paths; two-space separator, trailing LF, UTF-8 no BOM all match `sha256sum`).

Residual undriven arms after my pass, for the record: `Invoke-TcpProbe` `timeout` / `connect_incomplete` / `local_exception`; `Read-StrictAsciiLines` `empty_input` / `non_ascii_byte` / `carriage_return_not_allowed` / `control_byte_*`; most `Read-RemoteCloseRecord` out-of-order and path-safety arms; `Invoke-LocalBind` `local_dir_absent` / `local_reparse_point` / `local_path_outside_dir` / `local_duplicate_name` / `local_hash_error`; `digest_set_rendering_differs` (unreachable while F1 stands).

*Pattern:* 10 (evidence that cannot fail), plus 1 as the realised consequence.

---

### F5 — REQUIRED (narrow). The extractor derivation exceeds what binding §4 permits
`remote_extract_verify_wpi.sh` vs §4 row for that file

§4: *"the ONLY semantic change is the pinned archive-constants block (bytes, member list, per-member digests = the WP-I kit of section 3, `RP1-B3.sh` excluded; concrete values enter at Stage 1 freeze)."*

The delivered file also changes five **executable** predicates outside that block:

```
-[ "$TYPE_COUNT" -eq 9 ] || fail "tar_member_count=$TYPE_COUNT expected=9"
+[ "$TYPE_COUNT" -eq 6 ] || fail "tar_member_count=$TYPE_COUNT expected=6"
-[ "$NAME_COUNT" -eq 9 ] || fail "tar_name_count=$NAME_COUNT expected=9"
+[ "$NAME_COUNT" -eq 6 ] …
-[ "$FILE_COUNT" -eq 9 ] || fail "extracted_file_count=$FILE_COUNT expected=9"
+[ "$FILE_COUNT" -eq 6 ] …
-note "members_exact count=9 order=stage1"          → count=6
-printf 'EXTRACT PASS … members=9 verified=9 …'      → members=6 verified=6
```

The changes are correct and necessary — the old constants would reject every valid WP-I archive, which is why round 1.5 exists. The defect is the mismatch: the kickoff's rule is *"any other semantic delta is a finding,"* and SELF_QA §2 already describes the change more broadly than §4 authorises ("the WP-I archive constants, **their six-member count literals**, and their truthful result text"). Resolve by either amending §4 to name the count literals, or deriving the count from `MEMBERS` so no literal exists to drift. Do not revert.

*Pattern:* 9 (the recorded sentence and the code have diverged).

---

### F6 — REQUIRED (low). `<ALLOCATE-AT-DISPATCH>` has no fail-closed guard, and STATUS's claim about it is not established
`transport_runner.ps1:251`; `STATUS_TRANSPORT.md:5–7`

The runner validates `<PIN-AT-FREEZE>` twice (`Test-HexSha256` on `$PLAN_SHA256` and on each stdin/pinned digest) but never validates `<ALLOCATE-AT-DISPATCH>` in `$BASE_RUN`, `$CONFIRM_TOKEN` or `$RECORD_ROOT`. With the hash pins filled and `$RECORD_ROOT` still literal — a realistic partial freeze, since §-gates put hashing and identifier allocation in different steps — the run dies at `:251`:

```
TR_OP_ARGV id=01 argv=[tcp_probe] [127.0.0.1] [9] [20000]
<stderr> Test-Path : Yolda geçersiz karakterler var.
         At …\transport_runner.ps1:251 char:5
         + if (Test-Path -LiteralPath $RECORD_ROOT) { Stop-Run ('record_root_alr …
         + CategoryInfo : InvalidArgument … [Test-Path], ArgumentException
MEASURED_EXIT_CODE=1        TR_STOP lines: 0        record root created: (none)
```

No `TR_STOP`, no reason token, no `TRANSPORT_RECORD.txt`, exit **1 (FAIL)** rather than the documented 3, and the only diagnostic is a **localized** .NET message — in a file that elsewhere takes care to unwrap `SocketException` by type precisely so it never depends on localized text.

`STATUS_TRANSPORT.md` claims `<ALLOCATE-AT-DISPATCH>` and `<PIN-AT-FREEZE>` *"remain literal and intentionally make the draft runner STOP before starting a process."* Only the second half is demonstrated: the observed `TR_STOP reason=plan_pin_unfilled` is a `<PIN-AT-FREEZE>` effect, and the allocation placeholders are protected only by check ordering — an accident, not an interlock.

Same class, reachable **after** freeze: `Write-TextFile` at `:475`, `:478`, `:498`, `:499` sits outside any try/catch, so a mid-run record-write failure (full disk, ACL change, locked file) takes the identical unhandled path. Add an explicit "no unfilled allocation marker" preflight gate, and wrap the whole script so any unhandled terminating error becomes a reasoned `TR_STOP` at exit 3.

*Patterns:* 1, 6 (unadjudicated helper status escaping as a raw exit), 10 (a STATUS claim with no red state).

---

### Nits (optional — no required repair)

- **N1 — `run_ro.sh:38` leaves `WPI_LOG_DIR='<PIN-AT-FREEZE>'` although §2 resolves it** to `/var/log/mtc-bridge` (source: `LEAD_PIN_RESOLUTION_2026-08-10.md`, unit-template `ReadWritePaths` at the candidate SHA). Every other §2 value is concrete in the wrapper; only `WPI_UNIT_FRAGMENT_SHA256` is legitimately deferred (§2 marks it `<PIN-BEFORE-DISPATCH>`). Fail-closed, but an artifact↔prereg disagreement to close before freeze.
- **N2 — the set classifies the same observation two ways (inherited).** `require_block` → `stop`/rc 3 for `block_sha256_mismatch`, `block_missing_or_not_regular`; `remote_extract_verify_wpi.sh` → `fail`/rc 1 for `archive_sha256_mismatch` and `block_hash_verification_failed`. By the wrappers' own header (`1 = FAIL (completed probe found deviant state)`), a successfully computed digest that differs is rc 1. Driven: mismatch → rc 3, absent → rc 3, directory-in-place → rc 3 under one undifferentiated token. **The wrappers faithfully match the accepted Stage-2 `run_r45.sh` precedent** (`r45w_stop … file_sha256_mismatch`), so this is inherited, not introduced — hence a nit. If it is ever repaired, split `block_missing_or_not_regular` into absent / not-regular / not-evaluable, as the accepted `probe_path()` does.
- **N3 — plan-grammar gaps.** `$ALLOWED_PROGRAMS` is checked as a set, so a row may declare `kind=ssh_stdin` with `argv[0]=scp`; nothing requires `ssh_stdin` to carry a stdin file or `scp_up`/`scp_down` to omit one. `$sizes` is parsed from `CLOSE_SIZE` and then used only for count and name-set agreement — the byte counts are never compared against the retrieved files, so §7's size listing carries no independent weight.
- **N4 — a preflight STOP in execute mode persists no record.** `$script:RecordReady` stays false until after the dry-run gate, so `Flush-Log` writes nothing for `plan_sha256_mismatch`, `stdin_sha256_mismatch`, `record_root_already_exists`, `program_not_found`. §6 says these pre-leaf failures "are precisely the failures that decide whether a RUNID is burned" and names `TRANSPORT_RECORD.txt` as the record that captures them. Console-only is thin for that role.
- **N5 — §1's create-once collision list is stale, and §5's kind column lags §4.** §1 names two recorded operator roots; `C:\WPI_ARTIFACTS` also holds `WPLP2B_TRANSPORT_WPLP2B-20260809T210610Z-834380c5`. No collision with `WPI_TRANSPORT_*`, and the runner's own create-once check enforces it regardless. Separately, §5's rows 01/03 still name `remote_setup.sh` / `remote_extract_verify.sh`, which round 1.5 replaced with the `_wpi` derivations in §4; and the document's title still reads "round 1.4" while its body carries round 1.5 and the round-1.6 edits land with no round-1.6 note. Prereg-side (T2), listed for completeness.

---

## 4. Ten-pattern sweep

| # | Pattern | Result |
|---|---|---|
| 1 | STOP is not a result | **F2** (run-level rollup), **F1** (null parse → host accusation), **F6**, N2 |
| 2 | Whose kernel answered? | Clean for the transport set. Op 06 is explicitly operator-side and §5/§12 call it out rather than burying it; the wrappers make no domain claim, and the deploy-channel attestation obligation sits in §4/RP6 where it belongs. |
| 3 | The leaf is not the path | Clean. `Test-ReparsePoint` on the plan, every stdin file, every pinned file and every retrieved item; the accepted close script requires a canonical, non-symlink, owner/mode-checked `EV_DIR` and rejects non-regular entries in the tree. |
| 4 | The privileged child brought its own environment | Not applicable — no privileged child; `$ALLOWED_PROGRAMS` restricts to `ssh`/`scp` and `Get-Command` resolution is recorded (`TR_PROGRAM … resolved=`). |
| 5 | grep is not a parser | Clean at the grammar level — the `CLOSE` record is parsed by a full state machine (I verified the grammar line-for-line against the accepted script's real output, including the two-space `CLOSE_DIGEST` separator). **F1** is the same family one level down: a captured group consumed after the matcher was reused. |
| 6 | Read the status before the stdout | Mostly clean: `Read-StrictAsciiLines` gates completeness before any consumer sees content; `Invoke-TcpProbe` classifies before writing. **F6** is the exception — an unadjudicated helper status escaping as a raw exit. |
| 7 | Nonzero read is not end of file | **Clean, executed.** Three distinct completion classes; the reader refuses CR, NUL, other control bytes and non-ASCII before any partial content is exposed. |
| 8 | The name is not the identity | Clean for the transport set — the runner compares digests, never names. The wrappers pass numeric `WPI_STATE_UID=999` / `WPI_STATE_GID=988` through as separate values per §2's "uid and gid are deliberately not assumed equal". (The accepted close script's `%U:%G` owner check is inherited accepted bytes.) |
| 9 | The sentence outruns the probe | **F2** (header claims an exit 3 the code cannot produce), **F5** (§4's "ONLY semantic change"), **F6** (STATUS's placeholder claim). Conversely `payload_bytes=0` and `wrote_into_evidence_tree=0` are both earned. |
| 10 | Evidence that cannot fail | **F4** — the §7 binding claim has no red state, and F1 is what was hiding behind it. Everything the self-QA *did* record re-executed verbatim for me, which is genuine credit; the gap is what it never ran. |

---

## 5. What I did not verify

- The `timeout` arm of `Invoke-TcpProbe` — deterministically driving it needs a black-holed non-loopback destination, outside this audit's read-only/no-network envelope. `timeout → rc 0` is authorised by §8 row 24 (`connection_refused` **or** `timeout`), so it is the prereg's classification decision, not the runner's, and I raise no finding; the residual is that a dropped SYN is admitted as evidence of a closed port.
- Real `ssh`/`scp` behaviour, host state, and the actual `remote_close_tree.sh` execution on `GATEA-STAGING`. I substituted `cmd` for `ssh`/`scp` to drive `Invoke-ExternalProcess`, and generated the `CLOSE` transcript by running the accepted script under WSL with `EXPECT_OWNER` substituted for the sandbox (the only substitution, recorded by diff).
- `RP6-P0.sh` and `RP7-WPI-RO.sh` block internals — separate T0 slots. `run_ro.sh`'s `WPI_MAINPID=189813` is faithful to §8 row 4; whether pinning a volatile PID is the right predicate is an RP7 question, and §8 row 4 already records it as named risk R3 requiring Lead adjudication rather than a silent re-pin.
- The prereg draft and `RP7-WPI-RO.sh` were being edited by the concurrent RP7 round-3 session during this audit. I re-verified §1, §4's derivation rows, §5's op table and §8 row 24 against the post-edit bytes; none of my citations moved.

---

## 6. Repair scope for the next round

1. **F1** — latch `$matches[1]`/`$matches[2]` immediately after each `-match` in `Read-RemoteCloseRecord` (both the `CLOSE_DIGEST` and `CLOSE_SIZE` branches), then prove ops 11/12 with an executed RED/GREEN set over a real `remote_close_tree.sh` transcript.
2. **F2** — give the runner a run-level STOP: `TR_RUN STOP` + exit 3 when any executed op returned 3 and no genuine deviant-state mismatch occurred.
3. **F3** — add `remote_close_tree.sh` to the set at `87157f0e…`, and resolve `runkit.tar`'s home against §5's `01_RUNKIT` (amend one or the other, not neither).
4. **F4** — drive `Read-RemoteCloseRecord`, `Invoke-LocalBind`, `Get-Sha256OfText` and `Invoke-ExternalProcess`; delete `Test-Ascii` or call it; state exact counts for arms run, stubbed, and inherited-not-re-run.
5. **F5** — amend §4 to authorise the count literals, or derive the count from `MEMBERS`.
6. **F6** — add an unfilled-allocation-marker preflight gate and a top-level trap that turns any unhandled error into a reasoned `TR_STOP` at exit 3.

Nits N1–N5 are optional and do not gate acceptance.
