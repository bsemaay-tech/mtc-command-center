# DRAFT — Monthly AI Budget Proposal

**Status: DECIDED 2026-08-16 (late evening) — owner picked Option 2 (STANDARD, ~$800–1200/mo) as a MAXIMUM CEILING, not a spending target; cheapest-suitable-model-first routing continues regardless of headroom. Binding record: `OWNER_DECISIONS_2026-08-16_HOUSEKEEPING.md`. Body below kept unchanged as the analysis the decision was made on.**
**Prepared:** 2026-08-16 · **Prepared by:** Claude (Sonnet 5) · **Scope:** read-only research, one output file. No git changes, no account/subscription changes made.

---

## 0. The one thing to read even if you skip everything else

The `codeburn` tool tracks token counts and prices every token at **API-metered rates**, whether or not the tokens were actually paid for that way. Right now `codeburn plan` reports **"Plan: none. API-pricing view is active"** — meaning **none of your flat-fee subscriptions (Claude Pro, Claude Max, ChatGPT Plus/Pro ×4, Z.AI GLM Coding Plan) are marked as subscription-covered.**

Practical effect: the **$2,650 month-to-date number is a "value of compute consumed" figure, not your actual bill.** Almost all of it (99%) comes from four routes that you already pay a **flat monthly fee** for, regardless of how many tokens you burn on them. Your real monthly AI cash outflow is dominated by a shorter list of fixed subscription charges (see §2), not by this number ticking up.

That does **not** mean the number is meaningless — it's the best available proxy for "which route is getting hammered," which matters because burning a subscription's quota fast is what forces you to buy a bigger plan, a second seat, or hit rate-limit walls mid-task. But treat it as a **usage-intensity signal**, not a bill.

---

## 1. What was run to produce this draft

```
codeburn status            → Today $488.06 / 1935 calls · Month $2647.91 / 16050 calls
codeburn models -p month   → per-model breakdown, calendar month-to-date, total $2650.71
codeburn plan               → "Plan: none. API-pricing view is active."
codeburn proxy-path          → "No proxy paths configured."
```

The CLI worked and returned live data. Note the small drift between `status` ($2647.91) and `models -p month` ($2650.71) and between these and the two numbers you were quoted this morning ($469.90/1894 calls today, $2629.75/16009 calls month) — the figures move in real time as sessions (including the one that wrote this file) keep running. Treat every dollar figure here as accurate to within a few dollars at the moment it was pulled, not to the cent, and re-pull before acting on a threshold.

---

## 2. Where the money went — facts vs. estimates, clearly separated

### 2a. FACTS — from `codeburn models -p month` (calendar month-to-date, live pull)

| Provider | Model | Notional cost (month) | % of month total |
|---|---|---:|---:|
| Codex | gpt-5.6-sol | $968.74 | 36.5% |
| Claude | Opus 5 | $746.84 | 28.2% |
| Claude | Fable 5 | $673.24 | 25.4% |
| Claude | Opus 4.8 | $236.75 | 8.9% |
| Claude | Sonnet 5 | $15.00 | 0.6% |
| Codex | gpt-5.6-terra | $8.38 | 0.3% |
| Cursor | Cursor (auto) + low-tier models | $0.87 | <0.1% |
| Codex | gpt-5.6-luna | $0.43 | <0.1% |
| Claude | Sonnet 4.5, Haiku 4.5 | $0.33 | <0.1% |
| OpenCode | **DeepSeek v4 Pro** (the designated cheap route) | **$0.086** | <0.01% |
| Claude | glm-5.2 (via Claude-side route) | $0.028 | <0.01% |
| **Total** | | **$2,650.71** | 100% |

**Fact, not estimate:** the top 4 rows — all four flagship/premium models — are **99.0%** of this month's notional total. The designated cheap-delegation route (DeepSeek) is **$0.09 for the entire month**, essentially unused. This is the exact "agents forget to delegate to cheap models" pattern the `codeburn` pilot flagged when it was first installed on 2026-06-21 (then: Opus 4.8 + Codex flagship = ~$940 of ~$1,186 all-time; DeepSeek = $2.44) — it has gotten more pronounced, not less.

**Fact:** all four top-spend rows run through subscriptions that are billed as a **flat monthly fee**, per `MTC_COMMAND_CENTER\_AI_MEMORY\AI_ACCOUNT_AND_MODEL_ROUTING.md` (2026-08-08/2026-08-10 snapshot):

| Route (this doc's naming) | Subscription | Documented price | Real spend driver |
|---|---|---:|---|
| Claude Pro (`bsemaay3@gmail.com`) | Pro | ~$20/mo | flat fee |
| Claude Max (`bsemaay3@gmail.com`, isolated profile) | Max | ~$100/mo | flat fee; **policy says EMERGENCY-ONLY**, already 50% of weekly quota used as of 2026-08-10 |
| Codex `secondary` (default CLI route) | Plus | not priced in the doc | flat fee (est.) |
| Codex `fourth` | Plus | not priced in the doc | flat fee (est.) |
| Codex `free`/`.codex_OLD` | **ChatGPT Pro** | doc says ~$100/mo | flat fee — **verify against your card statement; OpenAI's public Pro price has historically been $200/mo, doc may be stale or discounted** |
| Codex `desktop` (owner's personal app) | Plus | not priced in the doc | pre-existing personal use, not incremental to project work, but heavy CLI spend on the `free` route competes with it per the routing doc's own warning |
| Z.AI GLM Coding Plan | Coding Plan | $16.20/mo, auto-renews Aug 26 | flat fee — **and per the table above, essentially unused this month ($0.03 notional)**, i.e. you may be paying for a seat that isn't doing its job |
| ClinePass | — | PAUSED, unpaid invoice, 0 credits | $0 currently — either reactivate or drop it, it's dead weight either way |
| Cursor | (subscription tier unknown) | **not found in any memory file** | flag for owner: what does Cursor actually cost you monthly? |

**Estimate, not fact:** the "not priced in the doc" rows above are marked so because the routing file records account tier names ("Plus") but not the dollar amount. Standard ChatGPT Plus list price is commonly ~$20/mo, so a rough estimate for 3 Codex Plus-tier accounts is **~$60/mo**, but this is an assumption, not a confirmed figure — recommend the owner check actual card statements once rather than trust an inferred number in a budget document.

**Rough fixed-subscription floor (mix of fact + flagged estimate):** $20 (Claude Pro) + $100 (Claude Max) + ~$60 (3× Codex Plus, estimated) + $100 (Codex Pro doc figure, needs verification) + $16.20 (GLM) ≈ **$296/mo committed regardless of token burn**, before any Cursor subscription cost (unknown) and before true metered spend below.

### 2b. FACTS — true metered (pay-per-token) spend

- **DeepSeek API:** real metered billing, `DEEPSEEK_API_KEY`. Balance was ~$2.90 as of the 2026-08-08 snapshot. This month's actual usage per the table above is ~$0.09 — genuinely tiny, and the balance is close to needing a top-up if usage ever increases, which is the opposite of today's problem.
- **NVIDIA NIM:** read-only route, $0 usage this month (didn't appear in the model breakdown at all).

### 2c. UNCERTAIN — flagged, not asserted

- Whether Claude Pro/Max or ChatGPT Plus/Pro ever convert to per-token overage billing beyond their quota (vs. simply rate-limiting/blocking until the next 5-hour or weekly reset) was **not verified against your actual account billing settings** in this pass. Anthropic and OpenAI consumer subscription plans are quota/rate-limited by design (this matches the "50% weekly used" language already in your own memory files for Claude Max and the "5-hour/weekly quota" language for GLM); an unexpected overage charge would only happen if a separate pay-as-you-go API key were linked to billing on top of the subscription. Worth a one-time check, not something this draft can confirm from local files.
- Cursor's actual subscription price is not recorded anywhere this pass searched. Low dollar impact this month ($0.87 notional) but worth naming for completeness.

---

## 3. Three budget options

| | **LEAN** | **STANDARD** | **HEAVY (current)** |
|---|---|---|---|
| **Monthly cap** (true out-of-pocket: subscriptions + metered API) | **$300–500/mo** | **$800–1,200/mo** | **$2,000+/mo** (current notional run-rate implies this if it stayed metered) |
| Subscriptions kept | Claude Pro, one Codex Plus seat, GLM Coding Plan, DeepSeek API top-up | Above + Codex Pro (`free` route) kept active, Claude Max kept as emergency-only | All current: Claude Pro + Max, 4 Codex accounts, GLM, DeepSeek, Cursor |
| Flagship (Opus 5 / gpt-5.6-sol xhigh) audits | **T0 gates only** — economic/live/host-touching surfaces. No T1 flagship audits; T1 uses one alternating flagship at `high` only when genuinely needed. | T0 always + **bounded** T1/T2 flagship use when GLM/DeepSeek genuinely can't cover it, with a soft per-week cap | Current behavior — flagship used routinely across T0/T1/T2 as convenient |
| Parallel lane fan-outs | **None** without explicit pre-approval per lane batch | Allowed **only with pre-approval**, capped lane count stated up front | Current behavior — fan-outs launched at agent discretion |
| Cheap-route delegation (DeepSeek/Cline/GLM tier-1-2) | **Mandatory first resort** for all mechanical/bounded work — this is already the AGENTS.md TOKEN DISCIPLINE rule, just actually enforced | Same rule, same enforcement, slightly more flagship headroom for judgment calls | Same rule exists on paper; this month's data (§2a) shows it is **not** being followed — DeepSeek is 0.003% of spend |
| Claude Max | Cancel or downgrade if emergency use has been ~zero; re-subscribe if a real emergency arises | Keep, emergency-only, re-verify weekly quota isn't being burned on non-emergencies | Keep as-is |
| Codex accounts | Drop to 1–2 seats (secondary + one backup); free/Pro seat only if genuinely needed for its higher quota | Keep 3 (secondary, fourth, free/Pro); desktop stays personal/untouched | Keep all 4 |
| What you lose vs. today | Slower T1/T2 turnaround on judgment-heavy tasks that currently get a "just use the flagship, it's easier" shortcut; more discipline required from every session (yours and the AI's) to actually route to cheap models first | Some flexibility on ad-hoc flagship use for convenience; fan-outs need a quick pre-approval message instead of happening silently | Nothing — this is what's happening now, at the current run-rate |

### In plain terms

- **LEAN** forces the token-discipline rule that's already written in `AGENTS.md` to actually be followed, cuts Claude Max and probably 2 Codex seats, and reserves flagship models for the small number of gates where a wrong call is genuinely expensive (deploy scripts, broker code, credentials, staging/production). Strategy research work (the next project phase) is naturally light on flagship-tier reasoning and heavy on long-running, low-stakes iteration — a good fit for LEAN's cheap-first posture.
- **STANDARD** keeps more convenience — flagship models are still available for T1 work when it's genuinely warranted, not just because it's the default habit — but adds a pre-approval gate on parallel fan-outs, which is where large single-night burns have happened before (per your own memory: "~60 lanes in a night... ten of ten contracts failed review").
- **HEAVY** is not a new option, it's a label for what's already happening. Documented here so you can see, in one place, that the current pattern is: 4 Codex seats, 2 Claude subscriptions, flagship models used as the default rather than the exception, and the designated cheap route essentially idle.

---

## 4. Enforcement mechanics — things that actually work in this setup

1. **Session-start `codeburn status` check is already mandated** (`AGENTS.md` line 282: "Cost / token check ... → `codeburn status` (and `codeburn models` for the breakdown). If premium spend (Opus/Codex) dwarfs delegated work, route more mechanical work through Cline CLI first, then `_deepseek_driver` fallback"). **The rule exists; §2a shows it is not being followed.** No new rule is needed here — what's needed is actually stopping to look at the number and act on it, not just printing it.
2. **Add a hard stop-and-ask threshold.** None currently exists. Proposed: *"When `codeburn status` month-to-date crosses 75% of whichever cap Barış picked below, the session must stop new discretionary (non-T0) flagship work and message Barış before continuing."* This is a new rule this draft proposes — it doesn't exist in AGENTS.md today.
3. **Weekly checkpoint line in the handoff file.** Add one line to the weekly handoff (`GLOBAL_HANDOFF.md` or equivalent): `AI SPEND WEEK OF <date>: $X notional / $Y est. real, vs monthly cap $Z.` Cheap to produce (one `codeburn status` call), makes drift visible before it's a surprise at month-end.
4. **Tier-routing discipline is already written (AGENTS.md TOKEN DISCIPLINE, lines 135–154, and the GLM routing tiers at 156–235) — the gap is enforcement, not policy.** Recommend: any session that reaches for a flagship model for T1/T2/T3-tier work must first name, in its own output, why the cheap route (DeepSeek/Cline/GLM tier 1–2) doesn't fit — a one-line justification, not a process. Cheap to enforce, expensive to skip honestly.
5. **Mark GLM as subscription-covered in codeburn** (`codeburn plan` / `codeburn proxy-path`) so future `codeburn status` pulls net out flat-fee subscription usage and show a more honest "true incremental $" number instead of the current all-API-rate view. This is a five-minute one-time config change, not a policy change, and would make every future budget check in this doc's spirit more accurate. (Not done in this pass — read-only scope — flagged as a cheap follow-up.)
6. **Cancel or fix the two dead-weight subscriptions regardless of which option is picked:** ClinePass (paused, unpaid, 0 credits, not usable capacity right now) and GLM Coding Plan (auto-renewing $16.20/mo, essentially unused this month). Either use them or stop paying for them — this isn't really a budget-tier decision, it's just waste either way.

---

## 5. Recommendation

**Recommend STANDARD (~$800–1,200/mo cap).**

Reasoning tied to project phase: the deployment/bridge work is nearly done — that phase has been genuinely T0-heavy (host-touching, credential, broker-adjacent work that correctly warranted flagship xhigh audits). The next phase, strategy research (combining existing strategies/indicators, per `START_HERE.md`), is described in your own project docs as long-running but comparatively compute-light on AI — lots of iteration, backtesting, and waiting on data, not lots of judgment calls that need a $746/month flagship model. That shift argues for pulling back from HEAVY, but going all the way to LEAN right now would likely cause friction while the habit of routing to cheap models first is still unbuilt (§2a shows it's currently not happening at all) — a mid-point cap with a real stop-and-ask trigger (§4.2) gives room to prove out the discipline before tightening further next month.

If the actual metered/fixed-fee accounting in §2 turns out to already be near the LEAN range once someone (not this draft) confirms the estimated Codex Plus prices and the Claude Pro/Max overage question, LEAN becomes the stronger pick — that verification is worth doing before committing either way.

---

## OWNER ASK — plain language

**The AI spend tracker shows about $2,650 in "value used" so far this month. Most of that isn't a real bill going up — it's tokens burned on subscriptions you already pay a flat monthly fee for (like Claude Pro/Max and your ChatGPT accounts). But some of it is real, and either way, the pattern shows the cheap/free option (DeepSeek) is basically never being used even though it's supposed to be the default for routine work.**

**Question: which monthly AI budget do you want to set?**

1. **LEAN (~$300–500/mo)** — cut Claude Max, drop to 1–2 Codex accounts, flagship AI only for the highest-stakes gates (deploy/broker/credentials), cheap models mandatory for everything else, no surprise multi-agent overnight runs without asking you first.
2. **STANDARD (~$800–1,200/mo)** — RECOMMENDED — keep the current subscriptions but hold the line: flagship AI only when actually needed (not just convenient), any big multi-agent run needs your yes first, session checks its own spend and stops to ask you if it's burning through the month too fast.
3. **HEAVY (~$2,000+/mo)** — keep doing exactly what's happening now, no new limits, this document just makes visible what that currently costs.

**Default if you don't want to think about it further: option 2, STANDARD.**

---

*This file is a draft for your decision — nothing here changes any subscription, account, or spending behavior on its own. No git changes were made. No accounts were touched.*
