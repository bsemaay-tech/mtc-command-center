# RP7 compact continuation packet — claude-opus-5 xhigh — 2026-08-14

This is the owner-approved compact-context launch packet for the next fresh
`claude-opus-5` xhigh session that continues the still-authorized single RP7 T0
cap-override repair. It replaces the full-read startup of the 446 KB
`SELF_QA_RP7.md` and 131 KB `RP7-WPI-RO.sh` with a staged, targeted read order.
It changes **no acceptance standard and no safety/audit requirement**; it only
optimizes quota. It is not an audit verdict and claims no acceptance.

The canonical binding documents remain `KICKOFF_CLAUDE_RP7_CAP_OVERRIDE_REPAIR_2026-08-13.md`
(work order, now with the compact read order) and
`RP7_CAP_OVERRIDE_LEAD_CONTINUATION_2026-08-14.md` (binding Lead findings). This
packet is the read-order/evidence map you execute; where it and the kickoff
conflict on scope or findings, the kickoff + continuation win.

---

## 1. Role, model, authority, gates

- **Role:** counterpart flagship **IMPLEMENTER** in a fresh, independent session.
  You are not the Lead and not an auditor. Do not claim acceptance.
- **Model/effort:** exactly `claude-opus-5`, effort `xhigh`. No alias, no
  `--resume`, no `--continue`, no silent fallback. If the exact model/effort is
  unavailable, stop and report BLOCK unless Barış explicitly waives it.
- **Owner authority:** the single additional RP7 T0 repair cycle was authorized
  verbatim by Barış ("I authorize both additional audit-cap overrides"),
  recorded in `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-13.md`
  §4. It authorizes one repair + the two fresh mandatory T0 flagship audits. It
  waives **nothing**: not findings, acceptance standard, model identity, effort,
  fresh-session, D026, or Lead reproduction duty. It grants no host, deployment,
  credential, service, broker/exchange, ARM, order, TESTNET, mainnet, or other
  economic authority. Hostinger Stage 1 stays behind its own later owner decision.
- **Tier:** T0 (protected WP-I remote read-only verification block touching
  systemd/host-verification predicates). T0 round cap = 3; this is the final
  authorized round. After this round the two fresh flagship audits decide.
- **Hard safety gates (never relax):** no host contact/network probe/SSH/SCP/RUNID
  minting; no deployment, service action, credential handling, trading/ARM/order
  surface; no Pine/parity/MTC/schema/broker/trading edits; no destructive Git
  (`checkout`, `reset`, `stash`, `commit`, `push`, `branch`, stage are all
  forbidden — read-only `git diff`, `git show`, `git cat-file`, `git status` are
  allowed); no sub-delegation; no persistent repository writing outside the
  four owned files below. Ephemeral run-owned scratch outside the repository is
  allowed and required for the evidence runs.
- **Uncommitted work warning:** the four owned files contain prior agents'
  uncommitted work. Never discard, stash, reset, checkout, or overwrite the
  partial diff. Save a pre-repair snapshot of `RP7-WPI-RO.sh` before editing
  (see §4/§8) so the RED arms have their true pre-fix subject.

## 2. Current identities (record of record, 2026-08-14)

Working directory: `C:\LAB\Tradingview_LAB_CLEAN`.
All four owned files live in
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/`.

| File | Bytes | SHA-256 |
|---|---|---|
| `RP7-WPI-RO.sh` | 130788 | `7126AD78737C481C56149D87B41A089D23279C7E1EDFEDF403311702CF883A50` |
| `SELF_QA_RP7.md` | 445965 | `54B115D0BFE25B45B52FBA50DC8C2893EB99007D4021F07B310F50E83A3419FA` |
| `STATUS_RP7.md` | 7725 | `4CF27CA778BB7D056648CC9880733285589B2E3814EFBEB50ADD138E7357A054` |
| `RP7_ROWS_1_9_REPORT_2026-08-13.md` | 31982 | `2A6CFF5CDEC28DF1174AA8E62EEC491C001CB10227F5FFF5BBD5BE69A20A0284` |

SHA-256 hex is case-insensitive; these exact strings are the identity to
re-derive. Only `RP7-WPI-RO.sh` differs from Git: **53 insertions / 5
deletions** (Lead-recorded). Repo HEAD when the Lead recorded state:
`4070ef3623b65b87a10584144944d1310405bd9c`. The committed (HEAD) script blob is
the audited `127655` / `beacf85b628e419d911416dc1ee51a382f742d90cbabe29602e60c4f52d809a8`
bytes; the working-tree partial is the `130788` bytes above. `SELF_QA_RP7.md`,
`STATUS_RP7.md`, and the report are still at committed bytes.

Other identity facts you must not re-derive from scratch (they are pinned):

- round-4 pre-fix blob (REQUIRED-2 subject): commit `90cbeac4`, script
  `127491` B / `5b00207aff17a9a9f29e056b9f93fb46b2cf640376659bf75b9f33b9b9b3dbe3`,
  0 CR.
- current committed bytes (row-9 pre-fix subject): `127655` /
  `beacf85b628e419d911416dc1ee51a382f742d90cbabe29602e60c4f52d809a8`, 0 CR.
- Both are reachable via `git cat-file blob <commit>:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`.

## 3. REQUIRED-1 — CRLF continuation repair (exact)

**Still open.** The partial added a **false** comment (script lines ~659–673)
claiming a trailing CR *blocks* continuation and "do not add any rstrip", but
left the rejected parser logic unchanged. The Lead reproduced the real behavior
on systemd 259:

```text
/tmp/.../crlf.service:4: Unknown key 'WantedBy' in section [Unit], ignoring.
CURRENT_CONTINUES=False
REPAIRED_CONTINUES=True
```

Meaning: a value line ending in **backslash + CRLF** *continues* in systemd; the
following `[Install]` is absorbed into the continued value and no Install section
opens. The correct block disposition is therefore
`install_section=absent` (rc 0). The current bytes report
`install_section=present` (rc 1) — a **false FAIL** inside the exact row-6
safety predicate this repair is about.

**Required code change (surgical, in the embedded Python parser of
`wpi_assert_fragment_has_no_install_section`, script lines ~657–706):**

- Change the physical-line normalization from
  `line=physical.lstrip(WS)` to **`line=physical.rstrip("\r").lstrip(WS)`**.
  Strip the trailing CR **before** the continuation test; never before/after
  other whitespace.
- **Never** use broad `rstrip()` or `rstrip(WS)`: the trailing-space-after-
  backslash control must keep systemd's disposition (see below).
- **Remove or correct the false comment** at script lines ~659–673. Replace it
  with the observed rule: systemd normalizes the CRLF line terminator before it
  evaluates the trailing-backslash continuation; surgical `rstrip("\r")`
  mirrors that behavior, while broad whitespace stripping would fabricate
  continuations systemd does not perform.

**Literal D026 evidence to add and execute in the published fence:**

- `crlf_install` **RED/GREEN pair** — fixture is a CRLF fragment whose value
  line ends in a single backslash followed by CRLF, then `[Install]`.
  - RED (pre-repair bytes): rc **1**, line `B2_FAIL reason=install_section_present path=<fragment>`.
  - GREEN (repaired bytes): rc **0**, line `B2_fragment_install_section path=<fragment> install_section=absent parser=systemd_unit_line_grammar binding=component_and_mount_window_closed`.
- `trailing_space_after_backslash` **CONTROL** — fixture is a value line ending
  in backslash + trailing spaces (no CR), then `[Install]`. systemd does **not**
  continue this, so `[Install]` is a real section:
  - On **repaired** bytes this must remain rc **1**
    `B2_FAIL reason=install_section_present` — the no-weakening assertion that
    the surgical CR-only strip did not turn broad whitespace swallowing into a
    false PASS.
  - Also assert it on the pre-repair subject (expect the same rc 1) if the
    fence structure makes that cheap.

Do not disturb the existing six row-6 pairs and three controls (§4) while making
this change; the row-6 rule of record (comment bridges, blank terminates, odd
backslash count continues) is already correct and must be preserved.

## 4. REQUIRED-2 — six row-6 pairs against two subjects, separate processes

**Still open.** The post-round-4 audit proved the six new row-6 pairs do
discriminate, but the *package* never executed the RED arms against pre-fix
bytes — the fence pins `EXPECTED_BYTES=127655`/`EXPECTED_SHA=beacf85b…` and runs
only one (already-fixed) subject. That is exactly the D026 shortfall.

**Fold a two-subject run into the published rows-1-9 rebuild fence**, mirroring
the existing round-9 discipline (`SELF_QA_RP7.md` ~lines 703–710 materializes the
frozen round-8 blob with `git cat-file blob` and runs every arm twice).

Subjects:

1. **round-4 pre-fix blob** — `git cat-file blob 90cbeac4:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`
   → assert `127491` B / `5b00207aff17a9a9f29e056b9f93fb46b2cf640376659bf75b9f33b9b9b3dbe3`,
   0 CR, `bash -n` rc 0.
2. **repaired worktree file** — assert its re-derived current identity (will
   change after §3/§5 edits), 0 CR, `bash -n` rc 0.

**Hard constraints (from the Lead, binding):**

- Run the two subjects in **separate processes**. Both define the same function
  names; sourcing both into one shell silently overwrites the first parser and
  fabricates D026 evidence.
- Each subject × case gets a **unique run-owned scratch namespace** (root
  outside the repository, freshly created per run, strictly sequential; never
  the fixed `/tmp` collision the earlier harness had).
- Assert **exact per-case rc and terminal line** for each subject. The six pairs
  are heterogeneous — there is no valid uniform "GREEN means rc 0" template.
- **Normal capture closure:** before treating a parser rc 3 as a predicate STOP,
  assert the capture opened/closed normally (empty parser stderr, record
  consumed, mount guard closed). Do not let a harness error masquerade as a
  parser STOP.

**Expected matrix (already executed by the post-round-4 auditor; the published
fence must reproduce these exact outcomes):**

```text
                             round4 (127491)                     repaired
blank_no_bridge           rc=0 install_section=absent   ->   rc=1 install_section_present
comment_then_blank        rc=0 install_section=absent   ->   rc=1 install_section_present
even_backslash_no_bridge  rc=0 install_section=absent   ->   rc=1 install_section_present
bare_backslash_line       rc=0 install_section=absent   ->   rc=1 install_section_present
eof_dangling_install      rc=3 section_header_grammar   ->   rc=1 install_section_present
header_trailing_comment   rc=1 install_section_present  ->   rc=3 section_header_grammar
multi_comment_bridge      rc=0 absent (CONTROL)         ->   rc=0 absent
odd_backslash_three       rc=0 absent (CONTROL)         ->   rc=0 absent
continued_comment_install rc=0 absent (CONTROL)         ->   rc=0 absent
```

Terminal-line grammars to assert exactly:

- FAIL: `B2_FAIL reason=install_section_present path=<fragment>`
- STOP: `B2_STOP reason=fragment_unreadable_or_unparseable rc=0 path=<fragment> detail=section_header_grammar`
- PASS: `B2_fragment_install_section path=<fragment> install_section=absent parser=systemd_unit_line_grammar binding=component_and_mount_window_closed`

The six pair names and their current fence definitions are reachable with:

```text
rg -n "blank_no_bridge|comment_then_blank|even_backslash_no_bridge|bare_backslash_line|eof_dangling_install|header_trailing_comment" SELF_QA_RP7.md
```

Narration alone is forbidden: the published fence and transcript must contain
the real two-subject commands, outputs, identities, and polarity assertions.

## 5. Row-9 constraints (script lines ~746–824, core ~750–813)

The partial's row-9 tokenizer changes are **directionally correct** but the
literal D026 fixtures are still missing. Ensure all three:

1. **Mid-name quote rejection (new, required):** raw token
   `MTC_BRIDGE"_START_MODE=credential_free_disarmed` must be refused **before**
   it normalizes into the protected target name. The partial already emits
   `detail=environment_token_name_not_literal` for this shape; add the literal
   D026 pair:
   - RED (pre-fix = HEAD committed `127655` bytes, which accepted it): rc **0**
     `B4_environment ... occurrences=1` (the false PASS being fixed).
   - GREEN (repaired bytes): rc **3**
     `B4_STOP reason=unit_property_unreadable prop=Environment rc=0 detail=environment_token_name_not_literal`.
2. **Fully quoted valid control:** keep the existing `arm=quoted
   mutation=quoted_assignment CONTROL` (whole-assignment quoted form, e.g.
   `"MTC_BRIDGE_START_MODE=credential_free_disarmed"`) accepted at rc 0
   `B4_environment ... occurrences=1`. Verify the new mid-name rejection did not
   break this; re-run it against the repaired bytes.
3. **Same-value duplicate stronger-invariant fixture (new, required):** systemd
   applies last-assignment-wins, so two *identical* assignments have the correct
   effective value and systemd accepts them. This block intentionally refuses
   them (documented stronger invariant). Add a literal RED/GREEN pair:
   - RED (repaired bytes): two identical
     `MTC_BRIDGE_START_MODE=credential_free_disarmed` assignments → rc **1**
     `B4_FAIL reason=start_mode_missing_or_altered observed=count=2 observed_sha256=e9cc545dfb074abf6ff63c26a42b6139c12f714e3b20bb87ba31283ceba1b7de`.
   - GREEN: the single clean assignment → rc 0
     `B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed parser=systemd_environment_tokenizer occurrences=1`.
   - Keep the existing different-values duplicate (`arm=duplicate`) intact.
   - The `observed_sha256` above is `sha256("credential_free_disarmed\ncredential_free_disarmed")`.

Existing row-9 arms to preserve: `duplicate` (different values),
`substring`, `unmodeled_token`, `malformed_name`, `quoted` (control).

## 6. Current partial state — inspect these ranges, not the whole script

- **Row-9 changes are directionally correct** around script lines **750–800**
  (tokenizer name-literal guard ~782–794, stronger-invariant comment ~798–809).
  Do not rewrite them; only add the missing literal fixtures/evidence in §5.
- **CRLF logic is still wrong** around script lines **657–706** (false comment
  ~659–673, wrong `line=physical.lstrip(WS)` at ~696). This is the §3 repair.
- Read those two targeted ranges and the **current git diff hunks** at startup —
  **not** the whole 131 KB script. Get the diff read-only:

```text
git --no-pager diff --stat -- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
git --no-pager diff -- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
```

Expect exactly **53 insertions / 5 deletions** versus HEAD; verify the hunks are
confined to the row-6 parser (~657–721) and row-9 tokenizer (~746–824) regions.
If a hunk touches any other function, stop and report before continuing.

## 7. Staged read budget (quota-efficient; follow in order)

Do not full-read the 446 KB `SELF_QA_RP7.md` or the 131 KB script at startup.
Read only what each step concretely needs.

1. Root `AGENTS.md` and `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md` (small,
   mandatory onboarding).
2. This packet (already in hand).
3. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-13.md` §4 (3.3 KB
   file; read §4 for the cap-override authority).
4. Prior audit findings sections:
   - `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_POST_R4_AUDIT_2026-08-13.md`
     (16.7 KB) — read **REQUIRED-1**, **REQUIRED-2**, **NIT-1**, the six-pair
     matrix, and the identities table. This is the binding prior audit for the
     two still-open findings.
   - `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CODEX_T0_EXT_AUDIT_2026-08-13.md`
     (12.1 KB) — read only its three REQUIRED-findings sections (row-1 STOP
     domain, row-6 continuation, row-9 tokenizer) for context on what is already
     closed; do not re-litigate closed items.
   - `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CAP_OVERRIDE_LEAD_CONTINUATION_2026-08-14.md`
     (4.8 KB) — full; it contains the binding Lead REQUIRED-1 reproduction and
     the supplemental row-9 adjudication.
   - `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP7.md` (7.7 KB) —
     full; small and authoritative for identity/history.
5. Script targeted ranges (line-numbered reads, not full file): **630–825**
   covers both edit regions (`wpi_assert_fragment_has_no_install_section`
   633–721 and `wpi_assert_environment_start_mode` 746–824). Then read the exact
   git diff hunks from §6.
6. `SELF_QA_RP7.md` targeted anchors via `rg` (do not open the whole file):

```text
rg -n "^# RP7_ROWS_1_9_REBUILD_FENCE_BEGIN$|^# RP7_ROWS_1_9_REBUILD_FENCE_END$" SELF_QA_RP7.md
rg -n "blank_no_bridge|comment_then_blank|even_backslash_no_bridge|bare_backslash_line|eof_dangling_install|header_trailing_comment" SELF_QA_RP7.md
rg -n "quoted|duplicate|unmodeled_token|malformed_name|substring|environment_token_name_not_literal" SELF_QA_RP7.md
rg -n "git cat-file blob|red_green_pairs|D026_SUMMARY|HARNESS_ABORT|HARNESS_BLOCK_ID_MISMATCH" SELF_QA_RP7.md
```

   Then read only these windows: **lines 50–130** (disclosures + fence command +
   pins + prelude), **lines 360–449** (executed transcript), **lines 600–730**
   (D026 claim + count delta + round-9 two-subject discipline). Read further
   fence-body windows only where `rg` shows a fixture you must edit.
7. `RP7_ROWS_1_9_REPORT_2026-08-13.md` (32 KB): read the **Post-round-4
   regression repair** section and the SELF_QA/identity sections; skip the
   superseded round-2/3/4 history unless a concrete question requires it.
8. **Full-file reads only if a concrete unresolved dependency requires one.**
   Editing the fence body or transcript inside `SELF_QA_RP7.md` may require a
   full read of that file — that is a legitimate concrete dependency, but do it
   only after the targeted windows above and only once.

## 8. Execution discipline

- Send the **full harness output to a run-owned temp file** (e.g.
  `<scratch>/fence.stdout.txt`), never into model context. During reasoning
  inspect only: `wc -c`/`sha256sum` of subjects, `wc -l`/`grep -c` of
  `D026 row=`, the `D026_SUMMARY` line, and the specific required terminal
  snippets for `crlf_install`, `trailing_space_after_backslash`, the six row-6
  pairs, and the three row-9 arms. Then **paste/insert the full transcript into
  `SELF_QA_RP7.md` mechanically** without echoing it back into context.
- Use a **unique run-owned scratch root** outside the repository for every run;
  run strictly sequentially; clean up only your own scratch.
- **Run the complete published rows-1-9 fence once, verbatim, at the end** after
  all code/fixture edits, and record its real rc/stderr/stdout. Re-derive every
  byte/SHA identity and make the pasted transcript reproduce exactly (the single
  disclosed host-derived `HARNESS_ATTESTED_MOUNTINFO sha256=` field is allowed to
  differ across namespaces and is not evidence for/against any predicate).
- Run `bash -n` on `RP7-WPI-RO.sh` and the extracted fence body, and
  `git diff --check` on the owned files.
- Report every command/result honestly, including any failure or blocker.

## 9. Completion contract

- Change **exactly four owned files** (no others):
  - `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`
  - `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md`
  - `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP7.md`
  - `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_ROWS_1_9_REPORT_2026-08-13.md`
- Do **not** claim T0 acceptance. The Lead and two fresh flagship auditors
  (`claude-opus-5` xhigh and `gpt-5.6-sol` xhigh) decide acceptance.
- Do **not** run any Git mutation (no stage/commit/checkout/reset/stash/push/
  branch). Stop after the four owned files are internally complete, and report
  exact commands and real outputs.

## 10. Quick-reference anchors (verified against current bytes)

- Published fence command: `SELF_QA_RP7.md` lines 78–79.
- Fence identity pins + abort: `SELF_QA_RP7.md` lines 89–101.
- Executed transcript: `SELF_QA_RP7.md` lines 363–449.
- Un-executed D026 claim (the REQUIRED-2 defect): `SELF_QA_RP7.md` lines 623–633.
- Round-9 two-subject discipline to mirror: `SELF_QA_RP7.md` lines 703–710.
- Row-8 disclosure / `CapabilityBoundingSet=''`: `SELF_QA_RP7.md` lines 59–64.
- Same row-8 disclosure repeated in report:
  `RP7_ROWS_1_9_REPORT_2026-08-13.md` lines 628–633.
- Script CRLF region: `RP7-WPI-RO.sh` lines 657–706 (false comment ~659–673,
  wrong normalization ~696).
- Script row-9 region: `RP7-WPI-RO.sh` lines 746–824 (guard ~782–794, stronger
  invariant comment ~798–809).

---

*Quota optimization note: this packet changes the read order only. Every
finding, D026 requirement, fence requirement, identity assertion, safety gate,
and acceptance standard from the kickoff, the Lead continuation, and the binding
prior audits remains in force unchanged.*

## 11. Superseding live delta — 2026-08-14 19:35 Europe/Chisinau

Read this delta before the older identity/read-window sections above. The 18:54
fresh Opus continuation stopped on HTTP 429 after about 33 minutes. Preserve its
partial; no writer remains:

| File | Bytes | SHA-256 | State |
|---|---:|---|---|
| `RP7-WPI-RO.sh` | 131662 | `0B8EBF40A328225750B651D3511E71A9F7C550295492E75807A4497DA758484B` | modified, +64/-5 |
| `SELF_QA_RP7.md` | 476484 | `1CCFF50C23C0A15302E9DC4420F42131012282CDD1F896608D8AF7E95483B0C3` | modified, +316/-6 |
| `STATUS_RP7.md` | 7725 | `4CF27CA778BB7D056648CC9880733285589B2E3814EFBEB50ADD138E7357A054` | unchanged |
| `RP7_ROWS_1_9_REPORT_2026-08-13.md` | 31982 | `2A6CFF5CDEC28DF1174AA8E62EEC491C001CB10227F5FFF5BBD5BE69A20A0284` | unchanged |

The new fence genuinely executes the two-subject row-6 matrix and row-9
mid-name/quote/duplicate cases; preserve those additions. Its reproduced run
ended `D026_SUMMARY ... result=PASS`, but that is not acceptable because the
CRLF expected polarity contradicts direct systemd 259 evidence.

Focused completion only:

1. Read current script lines 650–715 and SELF_QA lines 360–610 plus the current
   diff hunks; do not initially reread either full file.
2. Apply the binding surgical repair
   `line=physical.rstrip("\r").lstrip(WS)` and correct the adjacent false
   systemd commentary.
3. In the multi-subject fence, make the pre-fix/current parser the CRLF RED
   (`install_section_present`, rc 1) and repaired CR-strip parser the GREEN
   (`install_section=absent`, rc 0). Keep broad `rstrip()` as the trailing-space
   RED and keep the trailing-space no-weakening controls.
4. Replace the fixed top-level `/tmp/rp7_rows_1_9_rebuild_evidence` root with a
   unique run-owned scratch root; preserve case isolation and cleanup guards.
5. Rerun the complete published fence, repaste real output, recompute all pins,
   then update STATUS and the report. Finish with `bash -n`, extracted-fence
   syntax, and `git diff --check`.

The next Pro reset reported by Claude is 23:50 Europe/Chisinau. This remains a
fresh continuation of the same owner-authorized repair, not another repair or
audit cycle.
