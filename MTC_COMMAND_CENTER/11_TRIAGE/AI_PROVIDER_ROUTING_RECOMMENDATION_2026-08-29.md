# AI provider routing recommendation — 2026-08-29

## Scope and operational boundary

This is a current, source-backed routing recommendation for the already working
Gemini, OpenCode Go, and OpenRouter routes. It is **not** a benchmark result, a
claim of live quota, or authority to relax any repository safety rule. No model
completion, credential inspection, purchase, or account change was performed
for this research.

Operational premises supplied for this decision (not re-verified here):

- Gemini 3.7 Flash High is working through the existing read-only helper.
- OpenCode Go is connected and working.
- OpenRouter has approximately USD 10 in prepaid credit.

Existing Gate policy remains controlling: Gemini is a mandatory, concurrent,
read-only audit lane for every T0/T1/T2 Gate 5/Gate 6 audit; its output is
supplemental and cannot replace final acceptance or an executable mandated test
suite. The same final-acceptance boundary applies to all routes below.

## Facts from first-party sources

| Route | Verified current fact | Source |
|---|---|---|
| Gemini 3.7 Flash | GA production model for complex coding and agentic workflows; 1M context, 64K output, and `low`/`medium`/`high` thinking. | [Google: latest model](https://ai.google.dev/gemini-api/docs/latest-model), [model specification](https://ai.google.dev/gemini-api/docs/models/gemini-3.7-flash) |
| OpenCode Go | USD 10/month; allowance is USD 12 per 5 hours, USD 30/week, and USD 60/month. OpenCode says the listed model/provider combinations were curated and tested for coding agents, but it publishes no universal quality ranking. | [OpenCode Go](https://dev.opencode.ai/docs/go/) |
| Go: GLM-5.3-Flash | Available as `opencode-go/glm-5.3-flash`; OpenCode estimates 1,580 / 3,950 / 7,900 typical requests per 5h/week/month. Its published Go rate is USD 0.15/M input and USD 0.50/M output. | [OpenCode Go](https://dev.opencode.ai/docs/go/) |
| Go: Kimi K3 | Available as `opencode-go/kimi-k3`; OpenCode estimates 110 / 250 / 490 typical requests per 5h/week/month. Its published Go rate is USD 3/M input and USD 15/M output. Moonshot describes K3 as its most capable model, with native vision and 1M context, designed for long-horizon coding and reasoning. This is a vendor capability claim, not an independent benchmark. | [OpenCode Go](https://dev.opencode.ai/docs/go/), [Moonshot K3 announcement](https://forum.moonshot.ai/t/kimi-k3-is-here-our-most-capable-model/480) |
| Go: DeepSeek V4 Pro | `opencode-go/deepseek-v4-pro` is currently listed. OpenCode's published allowance makes it materially more expensive than Flash, so use it for deep adversarial review rather than high-volume work. | [OpenCode Go](https://dev.opencode.ai/docs/go/) |
| Go: other material options | `opencode-go/kimi-k2.7-code`, `opencode-go/deepseek-v4-flash`, and `opencode-go/hy3` are currently present. They are fallbacks, not a reason to fragment routine routing before task-specific evidence exists. | [OpenCode Go](https://dev.opencode.ai/docs/go/) |
| OpenRouter: DeepSeek V4 Flash | The public current model catalogue exposes `deepseek/deepseek-v4-flash`, with 1,048,576 context and published per-token prices of USD 0.08344/M input and USD 0.16688/M output. It supports reasoning, structured outputs, and tool calling. This price is a dated snapshot, not a permanent policy input. | [OpenRouter public model catalogue](https://openrouter.ai/api/v1/models), [model page](https://openrouter.ai/deepseek/deepseek-v4-flash-20260423) |
| OpenRouter: DeepSeek V4 Pro | `deepseek/deepseek-v4-pro` is currently present in the same public catalogue. It is a paid alternative only when Go V4 Pro quota is exhausted or provider diversity is intentionally required. Its price and revision are dated snapshots, not routing policy. | [OpenRouter public model catalogue](https://openrouter.ai/api/v1/models) |
| OpenRouter: Hy3 | Paid `tencent/hy3` is currently available through OpenRouter; it is not merely a Go model. It has 262,144 context, tool calling and reasoning controls. The public catalogue prices it at USD 0.132/M input and USD 0.528/M output; the active price may vary by UTC window/provider. `tencent/hy3:free` is marked deprecated, so it must not be an automated production route. | [OpenRouter public model catalogue](https://openrouter.ai/api/v1/models), [Hy3 model page](https://openrouter.ai/tencent/hy3) |
| GLM-5.3-Flash capability | Z.ai positions it as an efficient multimodal coding/agentic model and reports internal comparisons against other models. Those comparisons are supplier evidence only; they justify a trial/default low-cost lane, not unqualified acceptance authority. | [Z.ai GLM-5.3-Flash announcement](https://z.ai/blog/glm-5.3-flash) |

## Recommendation

### 1. Mandatory audit lane: Gemini 3.7 Flash High

Keep the owner decision exactly as ratified: dispatch the same scoped,
read-only audit prompt to Gemini concurrently with every T0/T1/T2 model audit,
then compare common findings, Gemini-only findings, and contradictions before
the lead decides. Gemini is the **required independent auditor**, not a cheap
background helper and not an acceptance substitute.

### 2. Default OpenCode Go worker: GLM-5.3-Flash

Use `opencode-go/glm-5.3-flash` for routine bounded coding, implementation
drafts, low-risk review, and first-pass diagnosis. It preserves Go allowance
far better than Kimi K3 (OpenCode's published 5-hour estimate is roughly 14x
higher), while its supplier reports strong coding/agentic capability. Require
explicit allowed paths and an independent diff/test review before any protected
scope result is accepted.

### 3. OpenCode Go escalation: Kimi K3

Use `opencode-go/kimi-k3` selectively for difficult architecture, long-context
codebase understanding, a second independent design/review, or a stalled GLM
attempt. Do **not** make it the default worker: it consumes Go allowance at a
much higher published rate. Prefer a tightly specified, read-only prompt for
review/design; use a bounded implementation task only where write authority
already exists.

`kimi-k2.7-code` remains an optional code-specialist fallback, but should not
receive a permanent role until it has passed the same task-specific comparison
against GLM and K3.

### 4. Distinct DeepSeek lanes: Flash for volume, Pro for depth

Use paid `deepseek/deepseek-v4-flash` as the default OpenRouter route for
high-volume, non-protected coding drafts, mechanical analysis, and cheap
independent checks. On the current public catalogue it is cheaper than paid
Hy3 on both input and output and offers a four-times-larger context window.
That makes the prepaid credit go farther.

Use `opencode-go/deepseek-v4-pro` for evidence-backed deep audit, adversarial review,
architecture review, difficult bug analysis, requirements-versus-implementation verification, and
failure-mode discovery. It is a supplemental reviewer, never a replacement for a required
flagship acceptance slot. Prefer the included OpenCode Go allowance before paid
`deepseek/deepseek-v4-pro`; choose the latter only when Go quota is exhausted or deliberately
using a different provider matters to the review.

Use paid `tencent/hy3` only when a second model family is materially useful:
an independent counter-review of a DeepSeek/GLM conclusion, structured/tool
calling work needing a fresh perspective, or a specific short task that has
not been resolved by the default lane. Never route automatically to the
deprecated free alias. `Hy3` is available through **both** OpenRouter and
OpenCode Go, but those are different billing/allowance paths:

- OpenRouter: `tencent/hy3`, consuming prepaid API credit.
- OpenCode Go: `opencode-go/hy3`, consuming Go's dollar-denominated allowance.

## Routing matrix

| Work type | First route | Second route / escalation | Non-negotiable boundary |
|---|---|---|---|
| T0/T1/T2 audit | Gemini 3.7 Flash High, concurrent and read-only | DeepSeek V4 Pro for supplemental deep-adversarial review; Kimi K3 for difficult design/long-context review; Hy3 for high-volume model-family diversity | Lead compares findings; only authorized flagship acceptance and executable evidence can accept. |
| Routine coding, bounded unprotected paths | OpenCode Go GLM-5.3-Flash | Kimi K3 when task complexity or prior failure warrants it | Explicit path/scope contract; independent real-diff and test review. |
| Cheap/high-volume analysis or mechanical draft | OpenRouter DeepSeek V4 Flash | Go GLM-5.3-Flash if an agent-style coding loop is more useful | No secret handling, no global profile change, no protected-scope acceptance. |
| Deep audit / adversarial review / difficult diagnosis | OpenCode Go DeepSeek V4 Pro | OpenRouter DeepSeek V4 Pro only after Go quota exhaustion or for intentional provider diversity; Kimi K3 for unresolved macro disagreement | Supplemental evidence only; it cannot replace an exact acceptance auditor or executable test. |
| Difficult coding / architecture | Go Kimi K3 | Gemini High for parallel critique; GLM for an implementation alternative | K3's cost makes it an escalation lane, not an unattended worker. |
| High-volume diversity review | OpenRouter Hy3 (paid) | Kimi K3 for long-context/difficult disagreement | Record that it is a distinct family/provider route; do not use `:free`. |

## Practical routing order

1. For every covered audit, send Gemini High the identical read-only audit
   packet at the same time as the other auditor(s).
2. For normal implementation, start with Go GLM-5.3-Flash.
3. If the work is cheap/mechanical and no coding-agent loop is needed, spend
   OpenRouter credit on DeepSeek V4 Flash.
4. For deep adversarial review or difficult diagnosis, use Go DeepSeek V4 Pro;
   spend OpenRouter V4 Pro only after Go quota exhaustion or for intentional provider diversity.
5. Escalate to Kimi K3 only for genuinely difficult/long-horizon work or an
   independent high-effort review.
6. Use paid Hy3 for high-volume different-family review, not because it is
   cheaper than DeepSeek on the present OpenRouter catalogue.
7. Treat all published capacities, prices, model revisions, and provider claims as changeable;
   refresh the public catalogues before changing this routing policy.
