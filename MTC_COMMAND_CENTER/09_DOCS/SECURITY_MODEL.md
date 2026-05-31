# Security Model

MTC Command Center starts with strict safety boundaries.

## Read-only

The default behavior is to read source systems and write only MCC reports, status files, registries, and handoffs.

## Dry-run

All future operational behavior begins in dry-run mode. Dry-run means no real trade, no external order, and no live webhook.

## No Live Trade

MCC must not send live trades, broker orders, WunderTrading alerts, TradersPost alerts, or any other execution signal in foundation work.

## No Secrets In Files

API keys, tokens, passwords, account IDs, and private credentials must not be stored in MCC files.

## No Direct Core Patch

AI workers must not patch MTC_v2 core files, `MTC_V2.pine`, PineTS/parity engine files, or TradingView exports unless a future task explicitly authorizes that exact scope.

## Report-first

AI workers should produce reports and status evidence before proposing implementation.
