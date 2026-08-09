# WP-L P2 Claude repair prompt — GLM-5.2 audit (2026-08-09)

## Verdict

**PASS-WITH-NITS. Zero required repairs.** The durable prompt is safe to dispatch as fresh Claude
counterpart proposal-repair round 1/3. This verdict covers the prompt contract only; it does not accept a
future repaired proposal or authorize host/script/trading/deployment action.

## Independent execution

GLM-5.2 via the Z.AI Coding Plan read the exact prompt, accepted repair specification, specification
audit, reproduced-findings audit, and governing `AGENTS.md`. It checked the exact pinned commits, RP0-RP6,
F1-F9, one-file scope, blocked C1/C2/C5 boundaries, four prior optional nits, self-QA, and round accounting.
Final `git status --short` was empty.

The auditor returned four optional prompt-hardening nits, all Lead-reproduced and folded into the prompt:

1. explicitly bind external remote/local hashes of the closed evidence tree;
2. name restored-connection `quick_check` and `foreign_key_check`;
3. require a newly created rollback manifest at exact `0640 root:root` with every field validated;
4. clarify that "executable proposals" means API-consistent design blocks, not host-runnable blocks.

These additions tighten the accepted specification and do not expand writable scope or authority.

## Lead result

- exact writable target remains only
  `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md`;
- C1 and C5 remain explicitly non-executable/BLOCKED;
- C2 blocked prerequisites cannot become commands;
- Git, host, SSH, script transfer, credentials, broker/TESTNET, ARM/orders, WP-V/KVM2/master, old payload,
  economic action, and `C:\PGRK` reopening remain forbidden;
- no repair round was consumed because no proposal implementation ran.

## Routing record

```text
Classification          : Tier 4 protected Bridge safety/evidence prompt audit
Protected               : yes — persistence, stop/reboot, rollback and broker boundaries
Model/provider          : GLM-5.2 via Z.AI Coding Plan
Cheaper-model rationale : owner exact-model request plus protected cross-cutting contract
Exact paths             : prompt, repair spec, spec audit, proposal audit, AGENTS.md
Context/tool budget     : compact five-file read-only audit; completed in 202 seconds
Fallback                : Lead reproduction; secondary model cannot implement protected scope
External API credits    : no
```

## Next steps

1. Freeze the hardened prompt and this audit in Git and continuity memory.
2. Dispatch it to a fresh exact Claude flagship route when account capacity returns.
3. Lead independently inspects the actual one-file proposal diff and reproduces F1-F9.
4. Only then freeze a candidate and start fresh protected-scope proposal audit.
