# ROUTING POLICY — Claude Max conservation + parallel dispatch (owner, 2026-08-10 ~19:00)

**Binding from this point.** Supersedes the routing order in
`STANDING_AUTONOMY_AUTHORITY_2026-08-09.md` §A2 where they differ. Does NOT change the
audit-tier policy (`AGENTS.md` §AUDIT TIER POLICY) — tiers still decide auditor count,
effort and round caps; this document decides **which account fills each slot**.

## Why

Owner, in-session: Claude Max is at **~50% of its weekly credit with ~4.5 days until
reset** (2026-08-10). The weight of the work must move to Codex Pro, the other Codex
accounts, GLM-5.2, DeepSeek and the NVIDIA NIM routes. Claude Pro ($20) is to be used.
Max is reserved.

## The key fact that makes this cheap

**Claude Pro ($20, default account `bsemaay3@gmail.com`) runs `claude-opus-5` at
`--effort xhigh`** — verified 2026-08-10 (`CLAUDE_PRO_OK`). The T0 contract's Claude
flagship slot therefore does **not** require Max. Use:

```
claude --print '<PROMPT>' --model claude-opus-5 --effort xhigh --no-session-persistence --dangerously-skip-permissions
```

Constraint: Claude Pro enforces a rolling **5-hour session window**. Plan around it —
when it locks out, the slot waits or Codex takes the round; it does not silently escalate
to Max.

## Slot → account map

| Slot | Account / route | Invocation |
|---|---|---|
| **T0 Claude flagship** (audit, xhigh, fresh) | **Claude Pro** (default `.claude`) | `claude --print … --model claude-opus-5 --effort xhigh --no-session-persistence` |
| **T0 Codex flagship** (audit, xhigh, fresh) | **Codex Pro** | `Invoke-CodexForClaude.ps1 -Account fourth -CodexArgs @('exec','-m','gpt-5.6-sol','-c','model_reasoning_effort=xhigh','--dangerously-bypass-approvals-and-sandbox',$p)` |
| **Implementation, any tier** | **Codex first**, then GLM-5.2 | `-Account fourth` (`secondary` exhausted → resets 2026-08-16; `free` also in the wrapper's ValidateSet) / `Invoke-GlmTask.ps1 -PermissionMode acceptEdits` |
| **T1 audit** (1 flagship, high) | alternate Codex / Claude Pro | as above at `high` |
| **T2 review** (docs/evidence/prereg) | **GLM-5.2 preferred**, DeepSeek acceptable | `Invoke-GlmAudit.ps1 -TaskFile … -RepositoryPath … -OutputReport …` |
| **Mechanical / bulk** | DeepSeek `_deepseek_driver`, NVIDIA NIM | `Invoke-NvidiaNim.ps1 -Route deepseek|minimax` |
| **T3** | implementer self-verification | — |
| **Claude Max** | **EMERGENCY ONLY** | see below |

### Claude Max — the reserve rule

Max (`Invoke-ClaudeMax.ps1`) may be used ONLY when **all** hold:

1. The work is acceptance-critical (T0 slot or a blocking repair), **and**
2. Claude Pro's window is exhausted or its session errored, **and** Codex cannot fill the
   slot (wrong family for a cross-model check, or its account is exhausted), **and**
3. The Lead records the justification in the unit's status/record file at dispatch time.

Not for: authoring that Codex or GLM can do, re-runs, exploratory work, or anything a
cheaper route completed acceptably.

### Known account state (re-verify before relying on it)

- Codex `secondary` (`.codex-hesap2`): **exhausted until 2026-08-16 09:44**.
- Codex `fourth`: working (xhigh verified 2026-08-10).
- Claude Pro default: working at `claude-opus-5` xhigh; 5-hour rolling window.
- GLM-5.2: 5-hour credit windows; hit one 2026-08-10 ~15:40 (reset ~19:56).
- NVIDIA NIM (`-Route deepseek` / `minimax`): live, **but the claude-CLI wrapper narrates
  without engaging file-write tools** — use for read/analysis/second opinion, NOT for
  tool-driven authoring.
- Cline: ClinePass subscription paused/unpaid → no capacity.

## Parallel dispatch — mandatory, not optional

Speed comes from concurrency. Rules that make it safe:

1. **Never leave a capable agent idle** while independent work is queued. Dispatch every
   non-dependent item at once — 3–5 concurrent agents is normal and was sustained
   successfully on 2026-08-10.
2. **Scope by disjoint file sets.** Every kickoff states its exact writable file list AND
   names the files other live sessions are editing, with "never write them". This is how
   RP6 / RP7 / transport ran simultaneously without a single clobber.
3. **Gate only on real dependencies.** If round B needs round A's frozen output (e.g. a
   tool-set drift check), write the kickoff immediately with a `GATE:` block and fill the
   basis hash the moment A commits — do not hold the authoring.
4. **Commit each result as it lands**, exact file sets only, so a crashed agent never
   costs more than its own round.
5. **A crashed mid-write agent leaves partial bytes.** Restore with
   `git cat-file blob HEAD:<path> > <path>` — NEVER `git checkout` (Windows autocrlf
   rewrites LF→CRLF and breaks frozen hashes).
6. Batch independent Lead reads/greps in a single message too.

## Tier discipline — restated because it saves the most money

Classify **before** dispatching any audit and record the tier. The cost difference is
large and the temptation is always to over-audit:

- **T0** (touches a real host, credentials, economics): 2 flagships xhigh, cap 3 rounds.
- **T1** (non-economic code/scripts/tools): 1 flagship at `high`; GLM second opinion only
  if the flagship raised findings or the diff exceeds ~300 lines. Cap 2.
- **T2** (docs, prereg text, evidence write-ups): single reviewer, single round, GLM
  preferred.
- **T3** (kickoffs, checklists, status stamps, indexes): self-verification, no model
  audit. Most process artifacts are T3 — do not spend a flagship on them.

Overlap rule: highest applicable tier wins. Do NOT add GLM/DeepSeek rounds to a T0 cycle
unless the tier contract or the owner requires it — they cannot fill a flagship slot and
the extra round costs time without changing acceptance.

## Owner's standing offer, and the Lead's recommendation

Owner offered to buy **Cline ($10)** and/or **Grok (~$30 / 3 months)** if audits need
them. **Recommendation: not yet — do not spend.** Reasoning: the T0 acceptance floor is
defined as exactly two flagships (`claude-opus-5` + `gpt-5.6-sol`), and both slots are
covered by subscriptions already paid for (Claude Pro + Codex Pro). Cline and Grok could
only add *supplemental detection*, which GLM-5.2 already provides at no extra cost. The
bottleneck today was never auditor count — it was flagship account windows.

Revisit and buy if either becomes true:
- Codex accounts exhaust simultaneously (would break the Codex flagship slot), or
- a work package needs genuinely independent third-family detection that GLM cannot give.
