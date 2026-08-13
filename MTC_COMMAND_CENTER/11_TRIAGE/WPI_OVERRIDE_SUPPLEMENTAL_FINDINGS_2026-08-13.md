# WP-I override supplemental findings - 2026-08-13

Status: `PRE-REPAIR-INPUTS`; no acceptance claim.

Two parallel GLM-5.2 read-only lanes were run during the Claude Pro reset
window. DeepSeek was also tried: ClinePass was not subscribed, one broad direct
API run exhausted its iteration budget, and a narrowed RP7 run produced no
verified new finding. DeepSeek output is therefore not acceptance evidence.

## Tier application

- Pathscope is T1. The required accepting slot remains one fresh flagship at
  high effort. GLM-5.2 is used only as the policy's conditional second opinion
  because prior findings exist and the evidence delta is large.
- RP7 is T0. Acceptance still requires fresh independent
  `claude-opus-5` xhigh and `gpt-5.6-sol` xhigh verdicts. GLM-5.2 and DeepSeek
  are supplemental discovery only.

## Lead-reproduced Pathscope inputs

Against committed round-3 bytes:

| fixture | result |
|---|---|
| `$ROOT/lib:/etc/escape` | rc 0; complete blob incorrectly ALLOW-LEXICAL |
| `:/etc/escape` | rc 0; escape absent |
| `ssh -i /etc/key` assignment value | rc 0; key path absent |
| quoted `$ROOT dir/escape` | rc 1 FORBID; required non-regression |

The upcoming repair must preserve quote/escape membership, split relevant
members even when the first starts inside the allowlist, and fail closed on
unmodeled ambiguity. Every closure needs real committed-pre-fix/repaired D026
execution.

## Lead-reproduced RP7 inputs

The current environment tokenizer returns rc 0 for
`MTC_BRIDGE"_START_MODE=credential_free_disarmed`. Local WSL
`systemd-analyze verify` reports `Invalid syntax, ignoring` for the matching
unit directive. This is a false PASS and is added to the repair work order.

Two identical protected assignments are accepted by systemd but rejected by
the checker. This is a conservative false FAIL; the implementer must either
document and test strict single occurrence as an intentional stronger invariant
or align to systemd's effective value.

GLM also identified harness-integrity requirements independently confirmed by
source inspection: run the two subjects in separate processes, use run-owned
scratch roots, assert per-pair heterogeneous polarities, and prevent block ERR
traps or capture-leaf collisions from masquerading as predicate STOPs.

No remote host, deployment, service mutation, credential, ARM, order, TESTNET,
mainnet, Pine, parity, or trading action occurred.
