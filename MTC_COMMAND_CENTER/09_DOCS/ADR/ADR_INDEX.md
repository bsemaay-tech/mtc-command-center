# ADR Index

Canonical directory: `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\09_DOCS\ADR`  
Last updated: 2026-07-18

> **2026-07-18 correction + ratification:** ADR-0019/0021/0022/0023/0026/0027/0028 were created 2026-07-17 as `Accepted` without owner ratification and were corrected to `Proposed`. Later the same day Barış formally ratified **all twelve records, ADR-0018 through ADR-0029** — recorded in `_AI_MEMORY/DECISIONS.md` entry **D016** plus its same-day addendum (0026/0028/0029 after explicit discussion). Qualifications: 0020/0024 = direction only, evidence-gated; 0029 = gate framework only — the live gate remains unsigned and live/mainnet remains blocked.

| ADR | Title | Status | Date | Main decision | Implementation phase | Related files |
| --- | --- | --- | --- | --- | --- | --- |
| [ADR-0001](./ADR-0001-command-dash-as-reference.md) | command-dash as reference | Accepted | 2026-05-30 | UI/API reference, not base engine | Historical MVP | ADR-0003 |
| [ADR-0002](./ADR-0002-file-status-first-sqlite-later.md) | File status first | Accepted | 2026-05-30 | JSON/Markdown before database | MVP-0/1 | ADR-0006, ADR-0024 |
| [ADR-0003](./ADR-0003-read-only-first.md) | Read-only first | Accepted | 2026-05-30 | Early dashboard reads only | MVP-1 and standing | ADR-0028 |
| [ADR-0004](./ADR-0004-no-live-trading-in-mvp.md) | No live trading in MVP | Accepted | 2026-05-30 | Live execution remains separately gated | Standing | ADR-0019, ADR-0029 |
| [ADR-0005](./ADR-0005-pine-builder-standalone-drafts.md) | Pine Builder drafts | Accepted | 2026-05-30 | Generated Pine is review-only | MVP | ADR-0010 |
| [ADR-0006](./ADR-0006-single-writer-lockfile-before-database.md) | Single writer before database | Accepted | 2026-05-30 | Locks/backups/atomic replace before DB | MVP-2 | ADR-0017, ADR-0024 |
| [ADR-0007](./ADR-0007-utf8-and-windows-path-policy.md) | UTF-8 and Windows paths | Accepted | 2026-05-30 | Explicit encoding and canonical paths | Standing | ADR-0017 |
| [ADR-0008](./ADR-0008-lineage-required-for-executed-results.md) | Result lineage | Accepted | 2026-05-30 | Executed evidence needs code/config/data/runtime lineage | Standing | ADR-0020, ADR-0029 |
| [ADR-0009](./ADR-0009-manual-tradingview-export-manifest.md) | TradingView export manifest | Accepted | 2026-05-30 | Hash and manifest manual exports | Parity evidence | ADR-0008 |
| [ADR-0010](./ADR-0010-protected-core-path-policy.md) | Protected core paths | Accepted | 2026-05-30 | Approval and verification for core edits | Standing | ADR-0012, ADR-0018 |
| [ADR-0011](./ADR-0011-subprocess-environment-isolation.md) | Subprocess isolation | Accepted | 2026-05-30 | Clean configured execution environments | Standing | ADR-0019, ADR-0020 |
| [ADR-0012](./ADR-0012-mechanical-protected-path-hook.md) | Protected-path hook | Accepted | 2026-05-30 | Mechanically block unauthorized staged paths | Standing | ADR-0010 |
| [ADR-0013](./ADR-0013-manual-input-drop-folder.md) | Manual input drop folder | Accepted | 2026-05-30 | Manifested user input root | Intake | ADR-0008 |
| [ADR-0014](./ADR-0014-minimal-status-event-ledger.md) | Status event ledger | Accepted | 2026-05-30 | Append accepted/rejected writes | MVP-2 | ADR-0023, ADR-0024 |
| [ADR-0015](./ADR-0015-command-allowlist-and-network-gate.md) | Command/network gate | Accepted | 2026-05-30 | Named operations; explicit outbound permission | Standing | ADR-0026, ADR-0028 |
| [ADR-0016](./ADR-0016-mvp1-read-model-and-path-config.md) | Read model/path contract | Accepted | 2026-05-30 | Shared validated read contract | MVP-1 | ADR-0028 |
| [ADR-0017](./ADR-0017-windows-safe-lock-and-atomic-write-recovery.md) | Windows atomic recovery | Accepted | 2026-05-30 | Bounded retries and recoverable atomic writes | MVP-2 | ADR-0023, ADR-0024 |
| [ADR-0018](./ADR-0018-continue-existing-python-system.md) | Continue existing Python system | Accepted (D016) | 2026-07-17 | Continue and borrow selectively after gap audit | Architecture route | ADR-0025 |
| [ADR-0019](./ADR-0019-separate-research-validation-paper-live.md) | Separate operational modes | Accepted (D016) | 2026-07-17 | Isolate environment/config/state/credentials/runtime | Foundation | ADR-0029 |
| [ADR-0020](./ADR-0020-hybrid-backtesting-validation-stack.md) | Hybrid validation stack | Accepted (D016; direction only, evidence-gated) | 2026-07-17 | Fast, event-driven, and microstructure tiers | Research/validation | ADR-0008, ADR-0029 |
| [ADR-0021](./ADR-0021-hyperliquid-integration-policy.md) | Hyperliquid integration policy | Accepted (D016) | 2026-07-17 | Official SDK plus selective CCXT behind owned adapter | Exchange foundation | ADR-0023, ADR-0027 |
| [ADR-0022](./ADR-0022-independent-risk-engine-veto.md) | Independent risk veto | Accepted (D016) | 2026-07-17 | Strategies propose; risk authorizes or vetoes | Core safety | ADR-0023, ADR-0029 |
| [ADR-0023](./ADR-0023-idempotent-order-management-reconciliation.md) | Idempotent orders and reconciliation | Accepted (D016) | 2026-07-17 | Deterministic identity, unknown recovery, exchange truth | Core execution | ADR-0021, ADR-0024 |
| [ADR-0024](./ADR-0024-data-storage-separation.md) | Data storage separation | Accepted (D016; direction only, no migration before TS-P2-006) | 2026-07-17 | Historical, operational, audit, and metrics stores differ | Data foundation | ADR-0002, ADR-0006, ADR-0014 |
| [ADR-0025](./ADR-0025-build-core-risk-reconciliation-internally.md) | Build core internally | Accepted (D016) | 2026-07-17 | Own core; import bounded tools; study frameworks | Build-versus-borrow | ADR-0018, ADR-0021-0023 |
| [ADR-0026](./ADR-0026-llm-trading-safety-boundary.md) | LLM safety boundary | Accepted (D016) | 2026-07-17 | Advisory analysis only; no order authority | Standing security | ADR-0022, ADR-0027 |
| [ADR-0027](./ADR-0027-supply-chain-secret-security.md) | Supply-chain and secrets | Accepted (D016) | 2026-07-17 | Least privilege, locked/reviewed dependencies, scans | Standing security | ADR-0021, ADR-0026 |
| [ADR-0028](./ADR-0028-dashboard-read-only-first.md) | Dashboard read-only first | Accepted (D016) | 2026-07-17 | Observability first; remote actions deferred | Dashboard | ADR-0003, ADR-0015 |
| [ADR-0029](./ADR-0029-paper-to-live-promotion-gates.md) | Paper-to-live gates | Accepted (D016; framework only — live gate unsigned, live blocked) | 2026-07-17 | Multi-layer evidence and explicit approval; live blocked | Future governance | ADR-0004, ADR-0019-0023, ADR-0027 |

## Dependency order

1. Standing governance: ADR-0003, ADR-0004, ADR-0008, ADR-0010, ADR-0015.
2. Product and mode boundary: ADR-0018 and ADR-0019.
3. Build-versus-borrow and security boundary: ADR-0025, ADR-0026, ADR-0027.
4. Research/data foundations: ADR-0020 and ADR-0024.
5. Exchange and safety core: ADR-0021, ADR-0022, ADR-0023.
6. Observability and promotion governance: ADR-0028 and ADR-0029.

## Roadmap prerequisites and blockers

All ADR-0018 through ADR-0029 are Accepted by Barış as of 2026-07-18 (D016 + addendum). Qualifications that remain binding: 0020 and 0024 accept direction only and stay evidence-gated per their ratification lines; 0029 accepts the promotion-gate framework only — `_AI_MEMORY/LIVE_TRADING_GATE.md` is unsigned and live/mainnet stays blocked. TS-P0-004 (build-versus-borrow route) is resolved by D016.

ADR-0022, ADR-0023, ADR-0026, and ADR-0027 block any execution-authority implementation that does not satisfy their boundaries; these safety boundaries remain enforced by standing project rules regardless of ADR status (unsigned live gate, advisory-only LLM policy, protected scopes). ADR-0029 blocks any live consideration and remains subordinate to the unsigned `_AI_MEMORY/LIVE_TRADING_GATE.md` and explicit Barış approval.

## Future review

- ADR-0018 after the current-system gap audit.
- ADR-0020 after engine and Hyperliquid collector inspection.
- ADR-0024 after storage workload/recovery benchmarks.
- ADR-0025 after build-versus-borrow cost mapping.
- ADR-0029 only after the live gate is signed; live remains blocked.

Additional topics from the research—strategy plugins, event bus, configuration versioning, database migration, deployment topology, funding accounting, and historical-data versioning—are implementation choices within these ADRs or unresolved gap-audit inputs. No additional ADR was created without a durable decision.
