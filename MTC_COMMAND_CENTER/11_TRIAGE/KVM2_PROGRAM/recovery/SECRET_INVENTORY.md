# Secret inventory — names only

No value, private key, account identifier, host identifier, connection command,
or private path belongs in this artifact.

| Name | Purpose | Allowed consumer | Storage | Backup | Rotation/revocation trigger |
|---|---|---|---|---|---|
| `HL_ACCOUNT_ADDRESS` | TESTNET account identifier | Bridge service | Root-owned 0600 env file | Excluded | Host/cutover/account change |
| `HL_API_WALLET_KEY` | VPS-specific TESTNET agent authority | Bridge service only | Root-owned 0600 env file | Excluded | Incident, host change, suspected exposure, cutover |
| `TELEGRAM_BOT_TOKEN` | Optional outbound alerts | Bridge notifier only | Root-owned 0600 env file | Excluded | Exposure/provider reset |
| `TELEGRAM_CHAT_ID` | Optional alert destination | Bridge notifier only | Root-owned 0600 env file | Excluded | Destination change |
| `ANTHROPIC_API_KEY` | Optional risk-reducing veto layer | Bridge service only | Root-owned 0600 env file | Excluded | Exposure/provider reset |
| `XAI_API_KEY` | Optional risk-reducing regime layer | Bridge service only | Root-owned 0600 env file | Excluded | Exposure/provider reset |

`HL_LIVE_ACK` is forbidden and must be absent from the env file, unit, process
environment, manifests, and evidence. Monitoring/backup credentials are not
inventoried until P5-01 separately names their provider, issuer, consumer,
least-privilege scope, storage class, revocation owner, cost, and attempt bound.

Secret provisioning remains owner-only P4-03 work. The installer creates only a
comment-only contract and stops if definitions already exist.
