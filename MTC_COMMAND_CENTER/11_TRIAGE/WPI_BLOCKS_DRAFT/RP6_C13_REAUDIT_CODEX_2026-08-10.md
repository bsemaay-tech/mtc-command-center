BLOCK: 2

Audit tier: **T0** (host-touching run-kit block). This is the owner-directed Codex
re-audit slot under amendment A2/A2a; it was performed directly, with no
sub-delegation. No host was contacted and no production/preregistration artefact was
modified.

# Verification matrix

| Item | Result | Independently reproduced evidence |
|---|---|---|
| **V1 — F1 closure** | **FAIL** | The documented harness-1 fence re-ran at process rc 0 and showed the intended text-bearing rc-2 cases GREEN on repaired bytes, RED on pre-R3 bytes, and a genuine empty rc-2 no-match still reaching `state_account_resolution_unexpected ... observed_numeric=absent` rc 3. However, an additional rc-2 fixture emitting one newline byte on merged stderr reproduced a false no-match: `FALSE_NOMATCH_REPRODUCED=yes`, `REQUIRED_ERROR_OUTCOME_PRESENT=no`. Finding 1. |
| **V2 — F2 closure** | **PASS** | Harness 1 was executed verbatim from `SELF_QA_RP6.md`: `DRIVER_LINES repaired=1 prerepair=1 nocall=0`; all three no-call assertions were `ASSERT_UNMET ... polarity=RED`; the pre-R3 F1 assertions were RED; summary `C13_R3_ARM_QA_SUMMARY cases=16 result=PASS`, process rc 0. Harness 2 was also re-run: both `precheck_only` cases were `ASSERT_MET ... polarity=GREEN`, both `precheck_and_backstop` cases were `ASSERT_UNMET ... polarity=RED`, summary `C13_R3_BACKSTOP_QA_SUMMARY ... cases=4 result=PASS`, process rc 0. The earlier C13 fences are labelled SUPPLEMENTAL. This verifies the requested integration and backstop mutations, but it does not cure V1's untested newline-only semantic gap. |
| **V3 — F3 closure** | **PASS** | `RP6-P0.sh:31-43` now says admission is numeric only, explicitly says `gatea` and `mtc-bridge` names are queried through pinned `getent passwd`, limits returned name/gecos/home/shell fields to diagnostics, and disclaims establishment of the answering NSS source. The executable diff shows no name-based verdict was introduced. |
| **V4 — isolation vs `8d2f25a5^`** | **FAIL** | Source isolation passes: after comments/blank lines are excluded, the only executable diff is the rc-2 arm at `RP6-P0.sh:676-681`; all other executable arms are byte-identical. Package isolation fails: `git diff-tree --no-commit-id --name-status -r 8d2f25a5` lists the four whitelisted deliverables **plus** added `C13_R3_CLAUDEPRO_RUN_2026-08-10.log`. Finding 2. |
| **V5 — hash, bytes, syntax** | **PASS** | Git Bash independently derived pre-R3 `cfdb23b8834a783638723c54cf632973c1cc20c5fb676cb6d310a9d43b9acf1c`, 54109 B, and repaired `ef205e2064caa0cb1493abf037ce9d435f2bf8f6259c5bb3fc4964d1abb2b4b9`, 55467 B. `bash -n RP6-P0.sh` returned rc 0. `cbaf3ec8` and `8d2f25a5^` have byte-identical `RP6-P0.sh` baselines. |

# Findings

## 1. HIGH — newline-only rc-2 output is still falsely admitted as a valid no-match

`RP6-P0.sh:673` captures merged output with Bash command substitution:

```bash
raw="$(LC_ALL=C "$P0_GETENT" passwd "$acct" 2>&1)" || rc=$?
```

Bash removes trailing newline bytes from command-substitution output. Therefore the
`[ -n "$raw" ]` test at lines 677-681 cannot distinguish a truly empty rc-2 capture
from a capture containing only one or more newline bytes. The latter falls through to
`P0_PW_OUTCOME="nomatch"`, contrary to the closure contract that **any byte** at rc 2
must be `error` / `identity_unresolvable` rc 3.

Executed against the real repaired parser and caller with `gatea` valid and the
`mtc-bridge` fixture writing one newline byte to stderr before returning 2:

```text
FIXTURE=mtc-bridge_rc2_stderr_single_newline_byte
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
FALSE_NOMATCH_REPRODUCED=yes
REQUIRED_ERROR_OUTCOME_PRESENT=no
```

Required repair: preserve whether the complete merged stream contained bytes without
letting command substitution erase a newline-only capture, and add D026 RED/GREEN for
that exact fixture. The existing text-bearing fixtures remain useful but are not full
closure evidence for the stated any-byte rule.

## 2. MEDIUM — the R3 package exceeds the exact four-file repair whitelist

The repair kickoff says `Touch ONLY those four files`, and the implementer report at
line 22 says those are exactly the four touched deliverables. The actual diff from
`8d2f25a5^` contains a fifth added file:

```text
A  MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/C13_R3_CLAUDEPRO_RUN_2026-08-10.log
M  MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh
A  MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_C13_REPAIR_R3_REPORT.md
M  MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md
M  MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md
```

Required repair: reconcile the committed package to the four-file whitelist (or obtain
an explicit scope amendment covering the provenance log) and make the touched-file
claim match the actual accepted diff.

# Commands executed

```text
sed -n '664,787p' SELF_QA_RP6.md | bash --noprofile --norc
sed -n '942,1025p' SELF_QA_RP6.md | bash --noprofile --norc
<real-function newline-only rc-2 falsification, Git Bash>
git diff --no-ext-diff --unified=0 8d2f25a5^ -- RP6-P0.sh
git diff-tree --no-commit-id --name-status -r 8d2f25a5
git show 8d2f25a5^:.../RP6-P0.sh | sha256sum / wc -c
sha256sum RP6-P0.sh
wc -c < RP6-P0.sh
bash -n RP6-P0.sh
```

This report is the only repository file touched by the re-audit.
