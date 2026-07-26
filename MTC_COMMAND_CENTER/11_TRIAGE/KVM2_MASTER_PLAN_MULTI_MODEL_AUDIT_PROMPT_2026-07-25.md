# KVM2 Master Plan — Independent Read-Only Audit Contract

## Role

This is the frozen joint-input contract for KVM2 documentation Cycle 4/R1.
D024 and the current canonical `AGENTS.md` roster authorize five sequential
fresh read-only reviews in this frozen post-repair order: (1) an additional
independent GLM-5.2 advisory audit, (2) an independent Grok advisory audit,
(3) an independent DeepSeek advisory audit, (4) a fresh independent exact
`claude-opus-5` audit at effort `xhigh`, and (5) a fresh final exact
`gpt-5.6-sol` audit at effort `xhigh` as final acceptance authority. Every
review is sequential, fresh, and read-only. Each auditor must compute both
hashes and perform the content audit itself without nested delegation,
resume/continue, implicit alias, or fallback. If its exact contract cannot be
established, return `BLOCK`.

GLM-5.2, Grok, and DeepSeek are advisory auditors only. They never replace any
mandatory Gate 5 or Gate 6 auditor, and their reports are not acceptance; the
canonical Gate 5/Gate 6 auditors remain exact `claude-opus-5` at `xhigh` and
exact `gpt-5.6-sol` at `xhigh`. Codex must independently classify every
external finding as `ACCEPTED`, `REJECTED`, or `NEEDS_VERIFICATION` against
the actual frozen files and decide by evidence, not by majority, before its
own fresh audit. Cycle 3 closed non-accepting at capped R3 `REQUEST_CHANGES`.

Review the master plan and execution companion together as one joint program
document. Do not edit, repair, install, deploy, execute, connect to the VPS,
access runtime systems, or perform broker/exchange/network actions.

## Immutable audit input

Auditors must read and evaluate **both** the master plan and the execution companion
together. Neither is complete without the other. Compute the SHA-256 of each file
before reading any content. If either hash differs from the expected value, return
`BLOCK: INPUT_DRIFT` with the filename and hash mismatch, and stop.

- Master plan:
  `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md`
- Master expected SHA-256 (Cycle-4/R1 post-roster-repair 2026-07-26):
  `B4C9E2FF370D023B57141EB3DFB77D796B7C1FF666312278CD655D88E55CD48E`
- Master superseded SHA-256 (Cycle-4/R1 pre-roster-repair input; never audited):
  `9A287D425573C73F9EDE4E5DF30FBB994CBB78CA965E8731D5DDBE58D6ADF178`
- Master superseded SHA-256 (Cycle-3/R3 `REQUEST_CHANGES`):
  `2F2CB58785A06ACC7BDEFC790C1466B8072E8355504438F1C79BBDF4426EC7E2`
- Master superseded SHA-256 (Cycle-3/R2 transport-blocked input; hashes
  verified, no content audit or findings):
  `E031867C89B7E7D4766B5D3C7127958F564C4CDF2C8BF0B0BC0DDBA7B590959C`
- Master superseded SHA-256 (Cycle-3/R1 audit input; `REQUEST_CHANGES`):
  `A595A85A36CCA6BEB2C9D9568CD4BE368BC0F4A3A930622F62B91E13D2FAC68A`
- Master superseded SHA-256 (Cycle-3/R1 pre-repair input; Cycle-2 final-repair-sync):
  `CA0A8943916F653A11656A3A415B516100252D436DFA928C7BCCB96569BA9F38`
- Master superseded SHA-256 (round-7 repair 2026-07-26, before final-repair-sync):
  `BAA3EDE4B2E22674AD1EBFF210AEE012CA7EF0DFAEFCBC738D534E4325693747`
- Master superseded SHA-256 (round-6 repair 2026-07-26, before round-7 repair):
  `C88C12E6B3EB8AC3BC87D706472240F391ED0B221E241C62B849EA238B34BF44`
- Master superseded SHA-256 (round-5 repair 2026-07-26, before round-6 repair):
  `10468C8A12F72F467CD0105CC4C3049862498E45E0E816A2C43827895DE77C5C`
- Master superseded SHA-256 (round-4 repair 2026-07-26, before round-5 repair):
  `3C61B08B17867C2EEB602FD407CF327C95FF7446DB492304DDB6A926A3E8EF3C`
- Master superseded SHA-256 (round-4 pre-edit input, from consolidated audit report):
  `10C79396D63DE330BD4F920146B8CDB0C39C10C342233AEAE4E1C8B9CCD12F02`
- Master superseded SHA-256 (split-intermediate, before P5-06 ref fix):
  `3B275B846B2D09804428C44A70B7155AF987DE0D941BBB5B1E99A7A0234E3FBA`
- Master superseded SHA-256 (pre-split, round-3 post-repair):
  `3C7764DD006026274F9677FF2B8E81F4240B39BF638BB42427AE256860286475`
- Master superseded SHA-256 (repair-round 2 input, before round-3 repair):
  `C8D4CFBEA2BF7C3F5E831D4A5748E25F875429A8B3445CDAD900B98C198140CE`
- Master superseded SHA-256 (repair-round 1 input, before round-2 repair):
  `FFF86A50AD8CF0AB993BAE6CAA141AB6549FE94F07A66FDDFDF557E1D6368B43`
- Master superseded SHA-256 (original pre-repair, first-round audit):
  `2EA390E1C4A6C5DEF60F556BA9C041AB3189299E97DACD3036D1706049BF8CF8`

- Execution companion:
  `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`
- Companion expected SHA-256 (Cycle-4/R1 post-roster-repair 2026-07-26):
  `6996C9309459932C3BBCEE1C3AFCD7E56D542FEDCC47748E11782A854EEEEA9C`
- Companion superseded SHA-256 (Cycle-4/R1 pre-roster-repair input; never audited):
  `9F2894246926A6C6FE2ABF924F666FD7453EA2BBD76C0A588B13D99FE9815FB4`
- Companion superseded SHA-256 (Cycle-3/R3 `REQUEST_CHANGES`):
  `C98AADA35C2D8175A45945ADF583F72A4853CF9F23E825ECDE45E3339E92659C`
- Companion superseded SHA-256 (Cycle-3/R2 transport-blocked input; hashes
  verified, no content audit or findings):
  `4AC648CE7CC789D068E005A7FC6716596384E1ED9A2160DACB9601ADE88CEB4D`
- Companion superseded SHA-256 (Cycle-3/R1 audit input; `REQUEST_CHANGES`):
  `45FA823C6F88152FC61239A805AECCCD99F29975ECC61A4D65E60F213D376396`
- Companion superseded SHA-256 (Cycle-3/R1 pre-compression intermediate):
  `DFA077FBDE479FD2C1B71CA0EDE664B0262BD3559242B171298AC647F210FD6A`
- Companion superseded SHA-256 (Cycle-3/R1 pre-repair input; Cycle-2 final-repair-sync):
  `5CAED6D80CA9D0799BDA038696C31D57FC5DC1932E5A4DBDE5BE9670CF2A2610`
- Companion superseded SHA-256 (round-7 repair 2026-07-26, before final-repair edits):
  `68388E503A410E82A207D2C914595CEC3B99E637618B99395B0C8C5E7E3D3B43`
- Companion superseded SHA-256 (round-6 repair 2026-07-26, before round-7):
  `0A669E640F96F2E84C81101195E86CC5A37060EC10645938B4044562DC533528`
- Companion superseded SHA-256 (round-5 repair 2026-07-26, before round-6 repair):
  `97A3844EB741820A0AB2534B0B240525F9564A51B4F181F9F68F7EE380049FBC`
- Companion superseded SHA-256 (round-4 repair 2026-07-26, before round-5 repair):
  `CB4C686A161CA8D40DC6C1C235B6371A4ADE1DCDDA23D2535259F39E0177C885`
- Companion superseded SHA-256 (initial frozen input, pre-round-4 repair):
  `8706621CE52010465B408B265267F7320078E2A79F01533E85513335619615D9`

- Lower-level authority:
  `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`
- Source scenario report:
  auditor-supplied `HOSTINGER_KVM2_KULLANIM_SENARYOLARI.md` (inject its
  current external path only at runtime; never persist that private path)
- Governing rules:
  `AGENTS.md`,
  `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`,
  `MTC_COMMAND_CENTER/_AI_MEMORY/DO_NOT_TOUCH.md`,
  `MTC_COMMAND_CENTER/_AI_MEMORY/DECISIONS.md` (D024 through D020)

First compute the SHA-256 of both the master plan and the execution companion. If
either differs from its expected value above, return `BLOCK: INPUT_DRIFT` (state
which file and the expected vs actual hash) and stop without proceeding.

## User outcome to test

The Windows PC cannot stay on. KVM2 must become a safe 24/7 TESTNET bridge first.
Only after accepted bridge-only stability may the same KVM2 temporarily host
strictly isolated, individually admitted AI-lab workloads. Before mainnet, either
KVM2 is destructively reprovisioned from a trusted clean image into trading-only,
or a separate clean trading VPS is used. The plan must prepare that clean rebuild
now without authorizing execution.

## Required adversarial checks

These checks apply to both the master plan and the execution companion, evaluated
as a single joint program document.

1. **Authority integrity:** find wording that accidentally authorizes or
   conflates document writes, account/credential provisioning, billing,
   purchase, network, install, deploy, cutover, ARM, lab admission,
   reprovision, or mainnet. D024 is this repair only; audit acceptance grants no
   write or execution authority.
2. **Dependency order:** identify tasks that can be executed before their true
   prerequisites or owner/audit gates.
3. **Canonical consistency:** compare the master and companion with the
   lower-level bridge task, D024, and the closed Cycle-3 history. The master
   must not weaken or duplicate canonical bridge gates.
4. **Single-writer/state safety:** prove the old writer is quiesced before final
   WAL-consistent risk-state capture; exact accepted transfer/reset,
   SQLite/application semantics, and source/destination hashes close before
   one DISARMED start; that start must load the exact accepted artifact.
5. **AI-lab isolation:** attack Unix-user, cgroup, service-control, raw-log,
   credential, repo, Docker/socket, browser, Kodee, MCP, scheduler, and supply-chain
   boundaries. Treat same-kernel co-tenancy as compromised by design.
6. **Resource admission:** verify the implementation-only gate precedes actual
   identity/final controls; the complete denial/kill-switch suite runs from that
   identity and representative children and receives fresh exact-evidence
   Gate 6 acceptance; each workload then binds an immutable manifest, named
   executor, pre/post hashes, and one install/start attempt with no retry.
7. **Network exposure:** attack SSH tunnel, UFW, Tailscale/private access, reverse
   proxy, dashboard, alerts, webhooks, DNS, certificates, and port 8790.
8. **Monitoring/recovery:** require separate owner authority for external
   provider/account, cost/billing, credential roles, bounded provisioning/tests,
   purchase/network scope, off-host liveness, encryption, retention, restore,
   RPO/RTO, corruption detection, and credential recovery.
9. **Clean rebuild/mainnet:** attack trusted source, bootstrap, allowlists,
   rotation, contamination, wipe proof, and Option A/B. Require an independent
   post-build clean-host Gate 5/Gate 6 audit over resulting-host evidence before
   the separate mainnet gate.
10. **Operational executability:** test full-lab, partial-lab, and no-lab paths;
    optional skips need dated absence records, while any admitted lab workload
    contaminates the host and forces Option A/B. Flag ambiguous owners,
    unverifiable evidence, cycles, duplicates, or impossible validation.
11. **Scope/value:** identify useful low-risk VPS functions omitted from the user's
    goal, but reject feature accumulation that weakens bridge reliability.
12. **Secret/privacy hygiene and selection order:** detect secrets, identifiers,
    public IPs, private-key paths, wallet addresses, connection commands, or
    leak-prone instructions; verify Hermes/OpenClaw selection and unselected-agent
    absence precede manifest acceptance, credentials, install, or start.

## Finding standard

Report only findings that are concrete and actionable.

For every finding include:

- `ID`
- `Severity`: BLOCKER / HIGH / MEDIUM / LOW
- `Disposition`: REQUIRED_REPAIR / OPTIONAL
- exact plan section and line(s)
- failure scenario
- why current text is insufficient
- minimal replacement/addition
- acceptance evidence that would close it

Do not call an optional idea a required repair. Do not return generic advice such
as "use best practices," "add monitoring," or "consider containers."

## Required output

1. Auditor identity, CLI/tool, model if visible, and fresh-session statement.
2. Verified input SHA-256 for both master plan and execution companion.
3. One verdict:
   - `PASS`
   - `PASS-WITH-NITS` — optional items only
   - `REQUEST_CHANGES` — at least one required repair
   - `BLOCK` — cannot safely continue
4. Required findings, highest severity first.
5. Optional improvements.
6. Coverage matrix for all 12 adversarial checks.
7. Three strongest parts of the plan.
8. Residual risk after all proposed repairs.
9. Explicit statement that no files or systems were changed.

The plan is preparation-only. An accepting audit does not authorize execution.
