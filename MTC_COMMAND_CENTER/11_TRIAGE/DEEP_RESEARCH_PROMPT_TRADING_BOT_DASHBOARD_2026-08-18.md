# Deep-Research Prompt — Dashboard & Observability for a Bar-Close Retail Trading Bot

**Purpose:** paste the prompt below (between the `=== PROMPT ===` markers) into a
deep-research tool. It is scoped so results match OUR system — not
high-frequency trading, not institutional OMS/EMS, not market making.

**Usage notes (for the operator, not part of the prompt):**
- Results are research input only; they authorize nothing. Anything adopted
  goes through the normal owner-approval + audit-tier flow.
- If the tool supports it, request citations for every claim.

=== PROMPT ===

## Role

You are researching dashboard, observability, and operational-safety features
for a specific class of automated trading system. Your job is to find what
mature systems OF THIS EXACT CLASS provide, what solo operators of such
systems say they actually needed (especially after incidents), and which
commonly recommended features do NOT apply to this class.

## The system you are researching for — read carefully, this defines relevance

**Decision cadence (the single most important scoping fact):**
- The bot evaluates ONLY on bar close, on 5-minute to 1-hour candles.
- It makes at most a handful of trade decisions per day per strategy —
  typically 0–5. Holding periods are minutes to days (intraday + swing).
- Decision latency budget is SECONDS, not microseconds. An order that
  arrives 500 ms later is operationally fine.

**Architecture and scale:**
- One strategy per worker process; a small number of workers (1–5), each
  trading ONE instrument with a frozen, pre-approved parameter set.
  Strategy logic originates in TradingView Pine Script and is ported to
  Python with verified parity; the live engine does not re-optimize itself.
- Runs 24/7 on a single self-hosted Linux VPS (systemd), Python, SQLite in
  WAL mode as the local source of truth, WebSocket market data.
- Venues: crypto perpetual futures on Hyperliquid (planned live venue);
  Interactive Brokers paper account for equities research. Retail-scale
  capital (five figures USD). No co-location, no direct market access.
- Single owner-operator (one person), not a team, not a SaaS product,
  not multi-tenant. The operator is often away from the desk and relies
  on notifications.
- Web dashboard served loopback-only today (SSH-tunnel access); any remote
  exposure would require login + 2FA first.
- Strict governance: strategies must pass a research/backtest promotion
  pipeline before live; the execution dashboard is read-only-plus-brakes
  (ARM/DISARM/KILL and emergency flatten are the ONLY controls; there is no
  manual order entry). An LLM assistant, if any, is advisory and
  architecturally isolated from order flow.

**Risk framework already in place (research how to VISUALIZE/operate it,
not whether to have it):** per-trade risk %, daily/weekly loss limits,
max drawdown kill switch, consecutive-loss pause, API/data-feed failure
protection, exposure caps.

## Explicitly OUT of scope — exclude these even if sources recommend them

Discard findings that only make sense for: high-frequency or low-latency
trading (co-location, kernel bypass, FPGA, microsecond latency dashboards,
tick-level microstructure analytics); market making and order-book-depth
strategies; institutional OMS/EMS/FIX connectivity; multi-desk or
multi-tenant platforms; options/greeks; portfolio-margin optimization;
ML feature-store/alpha-research tooling; anything whose value depends on
sub-second reaction. If a source is about such a system, extract only the
parts that transfer to bar-close cadence, and say explicitly that you did so.

## Research questions (answer all, in this order)

1. **Feature inventory of comparable systems.** What do the dashboards/UIs of
   mature open-source bots in this class actually ship? Examine at minimum:
   Freqtrade + FreqUI, Jesse, OctoBot, Hummingbot (strategy-runner side, not
   market-making analytics), NautilusTrader, Gekko successors, and any
   actively maintained equivalents. For each: what is on the main screen,
   what is one click away, what is deliberately absent, and what do their
   docs/issues say users demanded most?
2. **Reconciliation.** For bots keeping a local DB as truth while an exchange
   holds real positions: what reconciliation patterns, cadences, and
   drift-alarm designs are used or recommended? What do post-mortems say
   happens when reconciliation is missing (phantom/orphan positions, double
   fills, ghost orders after restart)?
3. **Staleness & transport health.** Best practices for surfacing data
   freshness, WebSocket reconnect state, and "feed frozen vs market quiet"
   disambiguation in bar-close bots. Include heartbeat design and dead-man
   patterns (client-side and exchange-side, e.g. scheduled cancel-all).
4. **Alerting for a solo operator.** Alert taxonomies that avoid fatigue:
   what should page immediately vs digest vs log-only for this class?
   Rate-limiting/dedup patterns; dead-man ("bot went silent") alerts;
   evidence on notification-channel reliability (Telegram/email/push).
5. **Incident-response UX.** When something is wrong, what must the first
   screen answer in the first 60 seconds? Research incident write-ups of
   retail algo operators (exchange outage, partial fill storms, stuck
   orders, restart with open positions) and derive the on-screen checklist
   they needed.
6. **Trade journal & post-trade review.** Journal schemas and review UIs
   that measurably speed up "why did the bot do that?" — decision-chain
   logging, per-trade context capture (gate states, indicator values at
   entry), and chart-linked replay. What granularity is worth storing?
7. **Performance analytics minimal set.** For 0–5 trades/day, which live
   metrics are statistically meaningful vs noise? Live slippage tracking
   vs backtest expectation; expectancy/PF confidence at small N; drawdown
   presentation; what mature bots compute live vs delegate to research
   tooling.
8. **Risk-guard visualization.** Good UI patterns for loss budgets, kill
   switches, exposure caps: armed/triggered states, pre-trigger warnings,
   audit trail of state changes (who/when/why).
9. **Security baseline.** For self-hosted, money-adjacent web dashboards:
   concrete hardening beyond loopback+SSH-tunnel; auth patterns proportionate
   to a solo operator (2FA options, session handling, CSRF on the few
   control endpoints); documented compromises/lessons from bot platforms
   (e.g. exposed FreqUI/Grafana instances found by scanners).
10. **Perp-specific surfaces.** For perpetual futures specifically: margin
    health, liquidation distance, funding-rate impact on P&L — how do
    comparable dashboards present these, and which presentations mislead?
11. **Anti-features.** Features commonly present in "trading dashboard"
    templates/products that practitioners of THIS class report as useless or
    harmful (screen candy, fake precision, always-on AI sentiment, etc.),
    with sources.

## Output requirements

- Structure the answer by the 11 questions above.
- End with a consolidated table: `feature | problem it solves | evidence
  (source) | fits bar-close solo-operator cadence? (yes/no/partial + why) |
  suggested surface (execution dashboard / research dashboard / backend
  gate / not at all)`.
- Cite a source for every non-obvious claim. Prefer, in order: official
  project documentation; maintainer statements / release notes / issue
  threads; practitioner post-mortems; opinion blogs (label as opinion).
  Flag every claim that rests only on a single low-quality source.
- Where sources conflict, present both sides and say which fits our cadence.
- Do NOT recommend adding trading-control features (manual orders, parameter
  editing from the UI): our governance forbids them; treat that as a fixed
  constraint, and evaluate everything else against it.
- Explicitly list, at the end, the findings you DISCARDED as
  out-of-scope-for-cadence and in one line each say why — so we can audit
  the filtering.

=== END PROMPT ===
