# Dashboard stage rules

The active Strategy Intelligence Command Center shell is vanilla HTML/JS/CSS with a left sidebar
and read-only feeds. It must not imply backtest, broker, paper, ARM, order, or live capability.

- Preserve read-only-first authority. UI controls never create business logic or authority; programmatic
  writes belong behind the owned CLI/API contracts and require separate scope.
- `/dashboard` serves `apps/web/index.html`; current feeds are `/healthz`, `/api/snapshot`, and
  `/api/read-model`.
- Keep missing/stale artifacts explicit. Never render absence, inability to evaluate, or stale data
  as PASS/healthy/ready.
- Follow the accepted dark command-center visual contract: dark canvas, compact navigation, dense
  cards/tables, status accents, workflow cards, and read-only missing-artifact states. Do not regress
  to a light admin skeleton.
- UI/chart changes require visual verification at desktop and phone widths. Security/network/write
  surfaces escalate the audit tier; cosmetic/read-only UI is normally T1.
- OPEN-01 (vanilla JS versus bounded build step) remains unresolved until WP-V2B-05 measures it;
  do not choose a framework preemptively.
