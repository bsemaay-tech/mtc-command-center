# KICKOFF — Claude Pro T0 audit: RP6-P0 + round-18 assigning-effect repair

You are the fresh independent Claude auditor: exact model `claude-opus-5`,
effort xhigh, default Claude Pro account. This is a **T0** audit of a host-
targeting run-kit evidence surface. Working directory:
`C:\LAB\Tradingview_LAB_CLEAN`.

Read-only repository contract: edit exactly one new verdict file named below.
No Git mutation, remote host, network, deployment, credential, broker, exchange,
ARM, order, backtest, or trading action. Local execution of the published QA
harness is required. If you cannot execute it, return **BLOCK**.

## Exact bytes under audit

- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh`:
  **110817 bytes**, SHA-256
  `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`.
  The block is byte-identical from **round 11 through round 18**. Round 10/10a
  is not the boundary: commit `71a62cc8` carried 107252 bytes / SHA-256
  `a090ae736cbecd9973e8ae948b052504b21cbe8b61602f4b5ac592394fad0617`;
  round 11 changed the block to the current identity.
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`:
  **1065504 bytes**, SHA-256
  `0bbf41dd2985a587c97a992589c7576b31e92217d11ecb888b4c8b2c84b84481`.
  This is the current round-18 evidence identity. No earlier r16/r17 acceptance
  carries to these bytes.

Re-derive both identities before execution. Stop as BLOCK on mismatch.

## Reading order

1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md`
2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_R18_REPORT_2026-08-12.md`
3. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R17_2026-08-12.md`
4. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`, ROUND 18,
   then the carried R17/R16 sections needed to audit it
5. Required repo rules and
   `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md`

The r17 Codex verdict is **REQUEST_CHANGES**, not an accepting slot. It found:

1. `wait -p` survived the claimed closed effect model;
2. the pass-format assertion was self-certifying;
3. eleven local transcript slots contradicted resolved/captured-output claims;
4. the opening no-temp scope, whole-session negatives, and r10a stability
   boundary outran the evidence.

Round 18 claims all four are settled. Verify; do not inherit the implementer's
conclusion.

## Published command — execute verbatim

Run from `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT`:

```bash
sed -n '/^# R18_ASSIGNING_EFFECT_HARNESS_BEGIN$/,/^# R18_ASSIGNING_EFFECT_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc
```

The implementer recorded outer rc 0, zero stderr bytes, and:

```text
R18_ASSERT_MET D026_RED_DELIVERED_R17 mutant=wait_p rc=0 summary=[R17_DYNAMIC_TARGETS_SUMMARY cases=15 pass=15 fail=0 result=PASS] target=[R17_ASSERT_MET r17_dynamic_targets_measured variable_targets=113 inventory_targets=0 dynamic_targets=0 dynamic_variable_targets=0 opaque_mutators=0 effect_unmodeled=0 nonfunction_bare=11]
R18_ASSERT_MET wait_p_bash_semantics target=P0_R18_WAIT_TARGET changed=yes numeric=yes rc=0
R18_ASSERT_MET GREEN_CLEAN_R18_POLICY rc=0 summary=[R17_DYNAMIC_TARGETS_SUMMARY cases=16 pass=16 fail=0 result=PASS] pass_format=measured_and_falsified
R18_ASSERT_MET D026_GREEN_R18 mutant=wait_p rc=1 record=[UNMODELED kind=dynamic_variable_target:wait_p line=1567 raw=["$P0_R18_WAIT_NAME"]] summary=[R17_DYNAMIC_TARGETS_SUMMARY cases=15 pass=11 fail=4 result=FAIL]
R18_ASSERT_MET assigning_option_matrix_executed rc=1 printf_v=dynamic_target_refused read_a=option_refused wait_p_literal=target_recorded wait_unknown=option_refused wait_p_missing=target_refused
R18_ASSERT_MET effect_partition_conserved admitted=37 target_grammar=13 prefix_recursive=3 action_grammar=1 no_named_target=20
R18_ASSERT_MET assigning_option_matrix entries=3 printf_v=target_grammar wait_p=target_grammar read_a=fail_closed_unmodeled_option
R18_ASSIGNING_EFFECT_SUMMARY cases=14 pass=14 fail=0 result=PASS
```

Record your real rc, stderr byte count, and summary lines. Do not accept copied
implementer output as execution evidence.

## First-class audit questions

### 1. Structural assigning-effect closure

Audit the full 37-member effect partition, not only the spelling `wait -p`.
Confirm every member reaches exactly one terminal class and that the target class
includes `printf`, `wait`, and all eleven generic variable-mutating builtins.
Check every caller-selected assigning option reachable from that universe:
`printf -v`, `wait -p`, and `read -a`. Try option bundling, missing operands,
expanded/escaped targets, an unknown option, prefix recursion, and a second
assignment-capable form you derive independently. An unmodeled form must refuse;
zero facts plus PASS is red.

Judge whether temporary injection of `waittarget` into the extracted R16 policy
is a real executable acceptance layer or merely a demonstration disconnected
from the round-18 verdict. Trace the actual published top-level command.

### 2. D026 RED/GREEN honesty

Verify commit `671d9b40` yields the exact delivered r17 `SELF_QA_RP6.md`
identity: 1038848 bytes / SHA-256
`07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac`.
Confirm the RED rebind changes only the two fixture identity fields, the delivered
r17 fence accepts the wait mutant, Bash really assigns the symbolic target, and
the repaired policy refuses the same mutant for
`dynamic_variable_target:wait_p`. State explicitly whether you verified each new
test RED and GREEN as required by D026.

### 3. Measured pass-format scan

Confirm the former constants at the old r17 pass-format site are gone. Audit the
producer scan's grammar and scope. Verify it derives the clean count rather than
choosing it, and that inserting a one-time numeric constant plus
`unsupported_count=$P0_R17_FORMAT_MUTANT_COUNT` makes the measured count change
from zero to one. Try a differently shaped unsupported numeric result field to
test for a matcher-shaped blind spot.

### 4. Eleven transcript contradictions

Verify the exact eleven local positions now carry truthful
`LOCAL_TRANSCRIPT_ABSENT` markers:

- eight in `SELF_QA_RP6.md`;
- one in `STATUS_RP6_P0.md`;
- one in `RP6_R15_REPORT_2026-08-11.md`;
- one in `RP6_R16_REPORT_2026-08-11.md`.

Check each cited external record directly:
`RP6_CODEX_T0_AUDIT_R15_2026-08-12.md:146-148` or
`RP6_CODEX_T0_AUDIT_R16_2026-08-12.md:23-25`. The historical round reports keep
their original prose; their marker explicitly labels the contrary historical
claim as not local evidence. Judge whether that is honest and sufficient under
the no-unfilled-slot rule.

### 5. Claim and provenance scope

Confirm the opening sentence distinguishes original no-temp fences from later
local scratch use. Treat historical whole-session no-host/network/Git/write-set
negatives as author attestations unless a separate transcript proves the narrow
claim. Re-derive the block history and confirm **r11→r18**, not r10a→r18.

### 6. Adversarial closure and verdict

Apply all thirteen defect patterns. Seek another class, not another spelling.
If the claimed property still needs unbounded enumeration or an assignment-
capable class survives without a terminal disposition, return REQUEST_CHANGES
and say whether Rule 8's accept-with-disclosure boundary has been reached.

Verdict vocabulary: **PASS**, **PASS-WITH-NITS**, **REQUEST_CHANGES**, or
**BLOCK**. PASS-WITH-NITS may contain no required repair.

An accepting Claude verdict fills only the fresh Claude T0 auditor slot on the
round-18 bytes. The r18 Codex session was the implementer and its self-QA is not
an independent Codex audit. Do **not** claim dual flagship acceptance; a fresh
independent `gpt-5.6-sol` xhigh audit of the same round-18 identity is still
required.

## Sole output and delta gate

Write exactly one new file in this directory:
`RP6_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`.

The worktree has many pre-existing entries, so global cleanliness is not the
gate:

1. Capture `git status --porcelain=v1 --untracked-files=all` before execution.
2. Run the audit and write the sole verdict file.
3. Capture the same status after execution.
4. Prove the set delta contains only
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`.
5. Record the path-scoped status for that exact file.

Any other changed path in this audit lane's delta fails the gate.
