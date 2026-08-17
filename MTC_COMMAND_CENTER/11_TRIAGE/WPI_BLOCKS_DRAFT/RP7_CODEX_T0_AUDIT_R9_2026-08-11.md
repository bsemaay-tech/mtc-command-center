# PASS: 0 required findings

**VERDICT: PASS**

**FINDINGS: none.** The five round-8 findings are closed on the round-9
bytes. Neither carried stated limitation creates a reachable accepting result.

Auditor: Codex `gpt-5.6-sol`, xhigh, fresh independent T0 flagship slot.
This file records the Codex slot only; full T0 acceptance still requires the
separate accepting `claude-opus-5` xhigh slot under the repository policy.

## Applied contract and scope

- **TIER:** T0.
- **APPLIED AUDITOR CONTRACT:** Codex `gpt-5.6-sol` at xhigh; local,
  read-only inspection and execution; no host, network, credential, service,
  deployment, trading, Git-mutation, or commit action.
- **Audited tree:** commit `9f597117`. The four audit inputs are unchanged from
  that commit through the audit HEAD. The round-9 implementation itself entered
  at `437593c5` and changed only `RP7-WPI-RO.sh`, `SELF_QA_RP7.md`,
  `STATUS_RP7.md`, and `RP7_REPAIR_R9_REPORT.md`.
- **Executable identity:** 108301 bytes, SHA-256
  `0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62`,
  zero CR bytes, `bash -n` rc 0.
- No Pine, parity, MTC, strategy, broker, credential, staging-host, or
  deployment surface was changed or exercised.

## Executed evidence

I ran the published `RP7_EXACT_COMMAND` block verbatim from
`SELF_QA_RP7.md`, with stdout and stderr redirected to temporary audit files.
It completed in 238.1 seconds at rc 0. All six extracted fences emitted
`QA_PASS all_assertions=yes`; the final summary was
`PUBLISHED_COMMAND_RESULT=pass fences=6` with the stated per-fence bounds and
an unbounded prelude disclosed. Each of the six wrapper-stream markers reported
zero bytes.

The load-bearing round-9 marker outcomes were:

- `BYTE_IDENTITY` bound RED to the exact round-8 blob: 99903 bytes,
  SHA-256 `11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4`,
  and GREEN to the exact round-9 bytes above.
- `BODY_BINDING mode=outside`: RED rc 0 with
  `outside_is_original=no`; GREEN rc 3 with
  `outside_is_original=yes`.
- `BODY_BINDING mode=reader`: RED rc 0; GREEN rc 1 with the flag-mismatch
  disposition. The clean and deviant no-substitution controls were identical
  across RED and GREEN at rc 0 and rc 1 respectively.
- `BIND_RC mode=divert_rc7`: RED reported the false child rc 0; GREEN reported
  the measured child rc 7. Every diversion arm recorded `child_ran=yes` and
  zero escaped stderr bytes; undeclared and clean controls retained their
  previous dispositions.
- `RC137_PROVENANCE`: the rc-spoof RED was attributed to the wrapper and exited
  137; GREEN classified it as not originating from this wrapper and exited 1.
  The bare-137 and genuine kill-after controls retained their dispositions.
- `MAPPING_ASSERTION_POWER`: the round-8 count assertion accepted both the real
  command and the omit/duplicate mutant; the round-9 mapping accepted the real
  six-fence command and rejected that same mutant. `PUBLISHED_MAP_RESULT`
  reported zero mismatches for the real mapping and two for the mutant.
- `NETNS_DETAIL`: both RED failure paths had
  `detail_field_present=0`; both GREEN paths had
  `detail_field_present=1` and a diagnostic file. The equal-namespace control
  remained rc 0 on both subjects.

This satisfies D026 for every claimed closure. The RED subject is executed
prior code, not a reimplementation: findings 1, 2, and 5 drive the real
round-8 production callers; finding 3 drives the round-8 published command
text; finding 4 runs the old and new assertions over the same executed mutant.
A later supplemental attempt to run the round-9 fence alone was invalidated
while materialising the predecessor blob and is excluded from evidence; it does
not displace the completed end-to-end exact-command run above.

## Finding dispositions

### F1 — closed

The repair binds both consumers to the object created once. `wpi_open_leaf`
keeps the descriptor returned by the exclusive create
(`RP7-WPI-RO.sh:270-282`). `wpi_assert_status` derives the parser's read
descriptor before the child exists, passes the creating descriptor into the
child, and gives the parser only the bound read stream
(`RP7-WPI-RO.sh:1581-1618`). The parser computes the digest over the same bytes
it parses (`RP7-WPI-RO.sh:1631-1646`). There is no second body hash read and no
body-name input to the parser.

The outside-overwrite and body-swap outcomes are therefore causal, not merely
textual: the former cannot change the outside object or accept; the latter
adjudicates the child-written object and produces the truthful deviation. The
no-substitution controls show that the repair did not obtain safety by refusing
all clean or deviant inputs.

### F2 — closed

The bind-stop declaration now specifies only the row reason and whether that
row carries an rc field (`RP7-WPI-RO.sh:308-318`). On a post-child stream-bind
failure, `wpi_capture` renders its local measured child status before any
caller-specific STOP (`RP7-WPI-RO.sh:382-395`). The executed rc-7 arm proves
the child ran, proves no raw diagnostic escaped, and distinguishes RED's false
0 from GREEN's measured 7.

### F3 — closed

The published wrapper captures its own diagnostic channel separately and
redirects the bounded body's stderr before the body begins
(`SELF_QA_RP7.md:142-173`). The rc-spoof RED/GREEN vector proves the separation
is load-bearing; the genuine kill-after control proves the repair did not erase
the wrapper's real signal evidence.

### F4 — closed

The replacement checks a one-to-one relation for every fence: extraction,
wrapper operand, body-error operand, rc variable, and classifier call
(`SELF_QA_RP7.md:2227-2247`). The auditor's omit-R8/duplicate-R7 mutant is the
executed RED, and the old count comparison is retained only as a measuring
instrument (`SELF_QA_RP7.md:2248-2265`). Equal totals can no longer substitute
for the required mapping.

### F5 — closed

Both nonzero namespace-reader paths now emit the mandatory detail and diagnostic
leaf, while the completed equal-namespace path is unchanged
(`RP7-WPI-RO.sh:1319-1342`). The RED/GREEN caller and service vectors directly
exercise both branches.

## Stated limitations

1. **Target descriptor semantics versus MSYS2:** honestly scoped. On this
   workstation the outside-overwrite GREEN arm stops fail-closed because the
   platform does not reproduce the target Linux descriptor-path behavior after
   the leaf name changes. Static inspection confirms that the target-side write
   handle is derived from the inherited creating descriptor, while the executed
   GREEN outcome proves the local platform neither changes the outside object
   nor accepts substituted bytes. The clean control still reaches rc 0. This is
   a platform coverage limitation, not a reachable false-PASS.
2. **Concurrent unrelated kill while the wrapper also kills:** honestly scoped.
   The wrapper proves only that its own protected stream records its kill; it
   does not prove that no other kill happened concurrently. That residual can
   affect causal attribution, but every affected path remains non-accepting and
   cannot turn a failed fence into the final pass summary.

The separately disclosed name-opened readers outside rows 20-24 remain outside
this round's inherited audit band and are not claimed as capture-identity proof
for these rows. The three `<PIN-AT-FREEZE>` inputs and the missing accepting
`wpi_validate_inputs` arm also remain explicit freeze gates. This PASS closes
the five round-8 findings; it is not a freeze, dispatch, host-contact, or
deployment-readiness verdict.

## Thirteen-pattern check

Patterns 1-13 were applied to the changed bytes and evidence contract. The
round-9 repair closes the relevant Pattern 11 identity break, Pattern 10
non-falsifiable evidence, and Pattern 6/9 claim-to-fact mismatches. No new
Pattern 1 STOP/FAIL inversion, Pattern 2 domain substitution, Pattern 3 path
overclaim, Pattern 4 environment injection, Pattern 5 grammar shortcut,
Pattern 6/7 incomplete-read admission, Pattern 8 name-for-identity comparison,
Pattern 9 overclaim, Pattern 10 evidence-only assertion, Pattern 11 unbound
instrument, Pattern 12 silent unsupported form, or Pattern 13 dropped member
was found in the round-9 change.
