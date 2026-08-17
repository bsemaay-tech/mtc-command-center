# RP7 rows 1-9 post-round-4 - Claude T0 flagship audit

**Verdict: REQUEST_CHANGES** (2 REQUIRED, 1 NIT)

Auditor: Claude, fresh independent non-implementer session, sequential run.
Session model `claude-opus-5`, effort `xhigh`. Tier T0, final available round.
Date: 2026-08-13. Subject commit `8ec8967542a3d6f733cc235b724c6797b7f256cf`.

The three REQUIRED findings from `RP7_CODEX_T0_EXT_AUDIT_2026-08-13.md` are all
closed, and I falsified each one against its true pre-fix bytes rather than
accepting the closure claim. The published fence runs clean and its transcript
reproduces on all 85 lines. Acceptance is withheld for two reasons: the
post-round-4 row-6 repair introduced a new carriage-return regression that makes
the block contradict real systemd in the same predicate it was repairing, and
the six new row-6 RED/GREEN pairs are labelled but never falsified inside the
package, which is the exact D026 shortfall the kickoff named.

## Identities - all four match the kickoff exactly

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `RP7-WPI-RO.sh` | 127655 | `beacf85b628e419d911416dc1ee51a382f742d90cbabe29602e60c4f52d809a8` |
| `SELF_QA_RP7.md` | 445965 | `54b115d0bfe25b45b52fba50dc8c2893eb99007d4021f07b310f50e83a3419fa` |
| `RP7_ROWS_1_9_REPORT_2026-08-13.md` | 31982 | `2a6cff5cdec28df1174aa8e62eec491c001cb10227f5fff5bbd5be69a20a0284` |
| `STATUS_RP7.md` | 7725 | `4cf27ca778bb7d056648cc9880733285589b2e3814efbeb50add138e7357a054` |

History identities independently re-derived from Git objects, all matching the
values `STATUS_RP7.md:113-123` declares:

- round 3 `30f638f1`: 127038 B / `ac73485ff75ab6e731bf1bc137ae77f7074cab04700603ab71cba1c591141fe3`, 0 CR.
- round 4 `90cbeac4`: 127491 B / `5b00207aff17a9a9f29e056b9f93fb46b2cf640376659bf75b9f33b9b9b3dbe3`, 0 CR.

Block CR bytes 0 and `bash --noprofile --norc -n` rc 0 at both fence stages
(`HARNESS_BLOCK_ID stage=before` and `stage=after`).

## Mandatory execution - published fence, verbatim

Run in the foreground under WSL (`systemd 259 (259.5-0ubuntu3)`, kernel
`6.18.33.2-microsoft-standard-WSL2`), as published at `SELF_QA_RP7.md:78-79`:

```text
cd /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
sed -n '/^# RP7_ROWS_1_9_REBUILD_FENCE_BEGIN$/,/^# RP7_ROWS_1_9_REBUILD_FENCE_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

Result: **rc 0, 0 stderr bytes, 85 stdout lines**, RED=35, GREEN=35, CONTROL=7,
`D026_CONTROL`=2, zero `HARNESS_CASE_FAIL` / `HARNESS_ABORT` /
`HARNESS_BLOCK_ID_MISMATCH` / `HARNESS_CASE_STDERR` markers. Terminal line:

```text
D026_SUMMARY rows=1-9 red_green_pairs=35 controls=7 result=PASS instrument=RP7-WPI-RO.sh extracted_block_functions=yes block_logic_reimplemented=no
```

`diff` against the transcript embedded at `SELF_QA_RP7.md:364-448` is **clean on
all 85 lines with no normalization at all** - the disclosed host-derived
`HARNESS_ATTESTED_MOUNTINFO sha256=be94739e...82dbb2` happened to match my
namespace too, so even that field is identical. Counts agree across
`STATUS_RP7.md:80-81`, `:110-111`, the report at `:84-85`, and my run.

`ROOT` is the fixed `/tmp/rp7_rows_1_9_rebuild_evidence`. I confirmed no
`/tmp/rp7*` existed before starting and ran strictly sequentially; the aborted
parallel attempt referenced in the kickoff contributed nothing here.

## REQUIRED-1 - Row 6 mis-classifies a CRLF fragment; regression against `90cbeac4`

The post-round-4 parser replaced round-3/round-4's `text.splitlines()` with
`line=physical.rstrip("\r")` by `text.split("\n")` with `line=physical.lstrip(WS)`
(`RP7-WPI-RO.sh:681-682`). `lstrip` strips leading bytes only, and `continues()`
(`:674-680`) counts the trailing backslash run of the raw logical line. On a CRLF
fragment the final character is `\r`, never `\`, so **a continuation is never
opened** and every following `[Install]` is classified as a real section header.
`classify()` strips `WS` (`:690`), so the header still matches and FAILs.

Real systemd disagrees. Fixture `Description=continued \` + CRLF + `[Install]`:

```text
crlf.service:4: Unknown key 'WantedBy' in section [Unit], ignoring.
```

That diagnostic is the same proof the Codex audit used: systemd concatenated
`[Install]` into the `Description` value and never opened an Install section. The
LF counterpart of the identical fixture produces the identical diagnostic, so the
correct block disposition for both is `install_section=absent`.

Driven through the block's own extracted `wpi_assert_fragment_has_no_install_section`,
same fence prelude, only `BLOCK`/`EXPECTED_BYTES`/`EXPECTED_SHA` substituted:

```text
SUBJECT=round4  bytes=127491  (git object 90cbeac4)
PROBE crlf_install   rc=0 B2_fragment_install_section ... install_section=absent   <- agrees with systemd

SUBJECT=current bytes=127655
PROBE crlf_install   rc=1 B2_FAIL reason=install_section_present ...               <- contradicts systemd
```

The audited commit therefore **un-fixed a case the superseded bytes handled
correctly**, inside the very predicate the repair was aimed at. This is a
Pattern-5 grammar-completeness defect producing a Pattern-1 false FAIL - the same
defect class as the Codex REQUIRED-2 this repair answered, only reached through
`\r` instead of a comment line.

Reachability is not hypothetical for this repo: `.gitattributes` is `* text=auto`,
`core.autocrlf=true` on this workstation, and the tracked unit source
`IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template`
carries 0 CR in the blob but **91 CR in the working tree**. That template happens
to contain no line-continuation backslash today, so today's exact fragment is not
mis-classified - but row 6 exists to classify a *modified* fragment, and the
fixture set contains no CR arm of any kind.

Repair: restore trailing-`\r` handling on the physical line before the
continuation test (the pre-repair `rstrip("\r")` is exactly right, and it
preserves the correct `Description=foo\` + trailing-space behaviour - see NIT-1).
Add a CRLF RED/GREEN pair, RED on these bytes and GREEN on the repair.

## REQUIRED-2 - The six new row-6 pairs are labelled, never falsified (D026)

The published fence pins `EXPECTED_BYTES=127655` / `EXPECTED_SHA=beacf85b...` and
aborts on anything else (`SELF_QA_RP7.md:89-101`). It executes **one subject**.
Every arm labelled RED is a fixture the *current, already-fixed* code rejects;
no pre-fix subject and no deliberate mutation is ever run. That is precisely what
D026 forbids as closure evidence.

The package nonetheless states the falsification outcome as fact, twice, with no
command and no output:

- `SELF_QA_RP7.md:625-629` - "against round-4 bytes this fragment returned rc 0
  `install_section=absent`; against the current bytes it returns rc 1".
- `RP7_ROWS_1_9_REPORT_2026-08-13.md:581-584` - the same sentence.

D026 is explicit that asserting a test covers a defect is not the same as showing
it fails without the fix, and the kickoff states that current-only fixture labels
do not satisfy it. This is not a missing capability: **the same file already does
it correctly one section down** - the round-9 fence materialises the frozen
round-8 blob with `git cat-file blob` and runs every arm twice
(`SELF_QA_RP7.md:703-710`). That discipline was simply not applied to the
rows-1-9 rebuild fence.

I executed the missing demonstration. The claim is **true** - all six new pairs
discriminate, and both new controls hold on both subjects:

```text
                            round4 (127491)                    current (127655)
blank_no_bridge           rc=0 install_section=absent   ->    rc=1 install_section_present
comment_then_blank        rc=0 install_section=absent   ->    rc=1 install_section_present
even_backslash_no_bridge  rc=0 install_section=absent   ->    rc=1 install_section_present
bare_backslash_line       rc=0 install_section=absent   ->    rc=1 install_section_present
eof_dangling_install      rc=3 section_header_grammar   ->    rc=1 install_section_present
header_trailing_comment   rc=1 install_section_present  ->    rc=3 section_header_grammar
multi_comment_bridge      rc=0 absent                   ->    rc=0 absent      (CONTROL holds)
odd_backslash_three       rc=0 absent                   ->    rc=0 absent      (CONTROL holds)
continued_comment_install rc=0 absent                   ->    rc=0 absent      (CONTROL holds)
```

I also checked each of those six against real systemd 259 rather than against the
document's rule of record. `systemd-analyze verify` confirms `[Install]` is a
**real section** in the blank-line, comment-then-blank, even-backslash,
bare-backslash and EOF-dangling forms (no `Unknown key` diagnostic in any of
them), and reports `Invalid section header '[Install] # tail'` with
`failed to load properly ... Bad message` for the trailing-comment header. The
current bytes match systemd on all six; the round-4 bytes matched on none. The
repair is materially correct - but on my evidence, not the package's.

Repair: fold a two-subject run into the published fence so the RED arms are
executed against `90cbeac4` bytes materialised in-fence, exactly as the round-9
fence does for round 8.

## Round-4 closure adjudication - all three Codex REQUIRED findings verified closed

Falsified against round-3 `30f638f1` (127038 B), the true pre-fix bytes for these
three findings, through the block's own extracted B2/B4 drivers:

**Codex REQUIRED-1 (row-1 amended STOP domain) - CLOSED.**

```text
                   round3 (127038)                                              current (127655)
active_absent    B2_STOP system_manager_unreachable prop=ActiveState    ->  B2_STOP ... operation=show ... query=ActiveState
active_empty     B2_FAIL unit_not_active state= expected=active         ->  B2_STOP ... operation=show ... detail=active_state_value_grammar
active_unknown   B2_FAIL unit_not_active state=maybe expected=active    ->  B2_STOP ... operation=show ... detail=active_state_value_grammar
table_parse      B2_STOP unit_definition_unreadable operation=show      ->  B2_STOP system_manager_unreachable operation=show
```

All four reproduce the exact defects Codex named at `:766`, `:768` and `:572-575`,
including the undeclared `prop=ActiveState` grammar and the Pattern-1 false FAIL
on an empty token. `wpi_require_active_state_grammar` (`:577-582`) now admits only
the eight systemd `ActiveState` values and STOPs otherwise, before the first
comparison at `:793`.

**Codex REQUIRED-2 (row-6 continuation) - closed for the comment form, with the
new regression at REQUIRED-1 above.** `continued_comment_install` and
`multi_comment_bridge` both report `install_section=absent` at rc 0, matching
systemd; the round-4 blank-line over-reach is genuinely repaired.

**Codex REQUIRED-3 (row-9 tokenizer) - CLOSED.**

```text
                 round3 (127038)                                       current (127655)
unmodeled_token  rc=0 B4_environment ... occurrences=1  (accepts!)  -> rc=3 B4_STOP ... detail=environment_token_without_assignment
malformed_name   rc=0 B4_environment ... occurrences=1  (accepts!)  -> rc=3 B4_STOP ... detail=environment_name_grammar
```

The round-3 bytes silently dropped `UNMODELED_TOKEN` and `1BAD=value` and still
printed an accepting line - Codex's Pattern-12 finding, reproduced exactly. The
current tokenizer requires every token to carry a valid `NAME=` assignment before
target semantics (`:753-758`), and the quoted / duplicate / substring controls are
retained.

**Codex NIT-1 (stale 23/3 count) - CLOSED.** The stale sentence is gone from the
owned files; `23 RED/GREEN pairs and 3 controls` now appears only inside the
report's own closure record at `:442` and `:501`.

**Carried C1 / descriptor discipline - no new implementation class.** `wpi_capture`
is byte-identical to r9 (3884 B, `927ecca34598d62f0ed3590d646f3ee8caa998cdf8568da771876c62d4cdaf1e`)
and so is `wpi_assert_regular_digest` (1001 B,
`3a6dd84879357821a1d59195b2d797dbf9ed187e71a4c0f820cbbd3d0849296f`) - both
independently re-derived here and both matching the Codex audit's values.
`wpi_alloc_leaf` has zero matches. The C1 mount-projection digest residual stays
disclosed and unrepaired at `STATUS_RP7.md:100-102`, as scoped.

**Row-8 pin disclosure - adequate, unchanged.** `HARNESS_DISCLOSURE row=8` is
emitted in the transcript, the pins are labelled asserted rendered `systemctl show`
literals, host derivation is kept as a freeze-time act, and
`CapabilityBoundingSet=''` is named as the highest-risk pin
(`SELF_QA_RP7.md:59-64`, `:654-658`). Absent host derivation is not treated as a
repair finding, per kickoff.

## Thirteen-pattern adjudication

| Pattern | Adjudication |
|---|---|
| 1 STOP is not a result | **Finding:** a CRLF fragment becomes a false `B2_FAIL install_section_present`. Row 1's empty/unknown `ActiveState` false FAILs are now correctly STOPs. |
| 2 Whose kernel answered? | Clean: the terminal claim stays inside the attested execution domain that answered. |
| 3 Leaf is not path | Component/mount binding retained; carried C1 remains disclosed, not silently dropped. |
| 4 Child environment | Clean: pinned absolute tools, cleared environment, trusted `python3 -I -S` with isolation re-asserted inside both parsers. |
| 5 Parser completeness | **Finding:** the row-6 line grammar does not model `\r`, and the fixture set has no CR arm. |
| 6 Status before stdout | Clean: rc, stderr emptiness and completeness precede semantics in both bounded captures. |
| 7 Nonzero read is not EOF | Clean: `wpi_parse_show_capture` STOPs on hard read error, NUL, empty output and unterminated final record. |
| 8 Name is not identity | No new rendered-name identity comparison in this delta. |
| 9 Sentence outruns probe | **Finding:** the package states the round-4 RED outcome as executed fact in two documents without a command or output. Row 1's emitted grammar now matches its amendment. |
| 10 Evidence can fail | Fence is literal and reproducible; arithmetic is honest for the cases it contains, and it fails closed on identity, extraction and per-case mismatch. |
| 11 Declared instrument not executed | Clean: the fence extracts and drives the delivered functions; no re-implementation. |
| 12 Unmodeled input disappears | Closed for row 9 and falsified above. |
| 13 Terminal disposition | Row-9 tokens now all receive a disposition; property-table members conserved and duplicate-checked. |

## NIT-1 - trailing whitespace after a backslash is unmodeled in the fixture set

systemd does **not** continue `Description=foo\` followed by trailing spaces
(verified: `[Install]` remains a real section, no `Unknown key` diagnostic). The
current parser agrees by construction, because `lstrip` leaves the trailing
spaces and `continues()` then sees a space. That agreement is accidental rather
than tested, and the REQUIRED-1 repair must not break it - `rstrip("\r")` keeps
it, a general `rstrip()` would not. Worth one arm alongside the CR pair. This
does not affect the executable verdict.

## Scope and delta gate

`git diff --name-status 90cbeac4..8ec89675` is four files, all inside
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/`:

```text
M  RP7-WPI-RO.sh                    (+43/-30 region, row-6 parser only)
M  RP7_ROWS_1_9_REPORT_2026-08-13.md
M  SELF_QA_RP7.md
M  STATUS_RP7.md
```

562 insertions, 57 deletions. No Pine, parity, `MTC_V2`, schema, broker, trading,
deploy or credential surface is touched. The block change is confined to
`wpi_assert_fragment_has_no_install_section`'s embedded parser; every other B2/B4
predicate is unchanged, which my round-3 and round-4 probes corroborate.

The governing verdict path was absent at session start and immediately before this
write. This session wrote exactly:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_POST_R4_AUDIT_2026-08-13.md
```

No Git mutation: no stage, commit, checkout, reset, stash, branch or push. HEAD
remained `8ec8967542a3d6f733cc235b724c6797b7f256cf` throughout, and all four
audited tracked files were clean against it immediately before this write.
Pre-write whole-repo status contained 138 pre-existing paths and is advisory only.
No host contact, network probe, SSH/SCP, deployment, service action, credential
handling or trading action occurred. All scratch was under `/tmp` prefixes checked
before removal, plus the fence's own guarded root; `systemd-analyze verify` was
used read-only on local fixture files and contacted no manager.

This verdict does **not** fill the Claude T0 acceptance slot. The T0 round cap is
reached with no accepting verdict, so under `AGENTS.md` the repair loop stops here
and the two REQUIRED findings are reported to Barış rather than dispatched as a
further round.
