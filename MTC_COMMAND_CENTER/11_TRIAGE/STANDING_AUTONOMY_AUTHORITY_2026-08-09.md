# STANDING AUTONOMY AUTHORITY — owner grant (2026-08-09 night)

Barış granted this in-session, explicitly, to stop the Lead from idling on
owner-gated decision points: "work continuously and autonomously until morning, finish
the project, use the Claude Max credits, you have no luxury to stop or sit idle."
This document is the binding standing authorization that flows from that instruction.
It is READ by every autonomous/overnight Lead session together with the active handoff
and the `overnight-autonomy-rules` memory.

## What is now STANDING-AUTHORIZED (proceed WITHOUT asking)

All of the following are reversible, in-repo, or delegate-orchestration work. The Lead
proceeds and reports after — it does NOT stop to ask, and does NOT use AskUserQuestion
for any of these:

1. **Repair/audit cycles past the 3-round soft limit.** The ≤3-round rule is a quality
   cadence, not a stop sign. When a cycle hits round 3 with only NARROW survivors
   (mechanical code fixes, documentation/QA gaps, subcount labels — the kind an auditor
   calls MEDIUM/LOW and describes with a one-line minimal fix), the Lead opens a
   bounded fix round automatically, scoped to exactly those survivors, and re-audits.
   Repeat until PASS or until a survivor is genuinely architectural (needs a design the
   accepted contract forbids) or needs a hard-gated action (below) — only THEN
   escalate.
2. **Delegate dispatch to Max / Codex / GLM / DeepSeek** for implementation, audit,
   review, mechanical work — as many rounds as convergence needs. Claude Max credits
   are meant to be spent on this; spending them to finish is the goal, not a cost to
   minimize. Fable Lead stays orchestration-only.
3. **Stage 1B / runkit re-freeze**, evidence indexing, preregistration DRAFTS,
   checklist/record authoring, proposal status notes, gap adjudications that do not
   change accepted design text.
4. **Commit, push, PR** on the feature branch (per standing git delegation).
5. **Choosing the recommended default** on any reversible fork and proceeding, logging
   the choice in the commit/record.

## What STILL requires a fresh explicit Barış authorization (HARD GATES — unchanged)

These are irreversible or outward-facing; the standing grant does NOT cover them and
the Lead still stops for them (recording the ask, then continuing OTHER backlog while
waiting — never idling):

- Host mutation of any kind on `GATEA-STAGING` or any host (service stop/start/enable/
  mask, reboot, chmod/chown outside a run's own create-once tree, reprovisioning,
  group/ACL changes). **Running any repaired block against a real host** is host
  contact and stays gated.
- Credential load, ARM, orders, broker/exchange contact, TESTNET/mainnet, any economic
  action.
- Master merge; WP-V / KVM2; deleting the old payload archive.
- Anything the Instruction-source / safety rules classify as prohibited or
  permission-required outside the repo (sending messages, publishing, purchases, etc.).

## The anti-idle rule (operational)

The Lead must always be either (a) doing non-gated work, or (b) waiting on a delegate
notification WHILE the loop heartbeat is armed AND at least one other backlog item is
in progress or queued. "Blocked on owner" is NEVER a stop: it is a note in the morning
record plus immediate pivot to the next non-gated item. The loop terminates only at the
morning summary (~06:30) or on an explicit "stop" from Barış. If the entire non-gated
backlog is genuinely exhausted, the Lead GENERATES more prep work (next-WP drafts,
deeper evidence indexing, audit-readiness packaging) rather than going idle.

## Precedence

This document is subordinate to the safety rules and the hard gates above; it overrides
only the *instinct to stop and ask on reversible decisions*. When unsure whether an
action is reversible/in-repo (proceed) or host/irreversible (gate), treat it as gated
and pivot — do not guess toward action on the dangerous side.
