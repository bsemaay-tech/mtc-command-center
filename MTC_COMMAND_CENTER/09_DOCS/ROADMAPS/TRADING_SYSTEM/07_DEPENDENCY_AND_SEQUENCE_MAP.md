# 07 — Dependency and Sequence Map

## Critical path

```mermaid
flowchart LR
    A["P0-001 Drift checker"] --> B["P0-002 Release/rollback manifest"]
    B --> C["P1-001 Order state"]
    C --> D["P1-002 Durable identity"]
    D --> E["P1-003 Unknown submission"]
    E --> F["P1-004 Partial-fill protection"]
    C --> G["P1-005 Full reconciliation"]
    G --> H["P1-006 Risk snapshot"]
    H --> I["P1-007/008 Loss and exposure controls"]
    F --> J["P4-001 Restart recovery"]
    G --> J
    I --> J
    B --> K["P2-006 Storage/recovery decision"]
    K --> J
    J --> L["P4-004 Failure suite"]
    L --> M["P4-005 Paper evidence"]
    M --> N["P5 Read-only operations"]
    N --> O["P6-001 Signed live-gate package"]
    O --> P["P6-002 Limited release candidate"]
```

Phase 6 nodes are blocked, not scheduled delivery commitments.

## ADR dependency graph

```mermaid
flowchart TD
    G["Standing governance\n0003, 0004, 0008, 0010, 0015"] --> MODE["0019 Mode separation"]
    G --> SEC["0026 LLM boundary\n0027 Supply chain"]
    CONT["0018 Continue system\nProposed"] --> BUILD["0025 Own core\nProposed"]
    MODE --> EX["0021 Hyperliquid policy"]
    SEC --> EX
    EX --> OMS["0023 Orders/reconciliation"]
    RISK["0022 Risk veto"] --> OMS
    STORE["0024 Storage split\nProposed"] --> OMS
    MODE --> VALID["0020 Hybrid validation\nProposed"]
    OMS --> DASH["0028 Read-only dashboard"]
    VALID --> LIVE["0029 Promotion gates\nProposed"]
    OMS --> LIVE
    SEC --> LIVE
    DASH --> LIVE
```

## Task waves and parallel work

| Wave | Serial work | Safe parallel work | Blocker/approval |
| --- | --- | --- | --- |
| W0 | P0-001 → P0-002 | P0-003 after P0-001 | Documentation only; Barış chooses P0-004 ADR status |
| W1 | P1-001 → P1-002 → P1-003 → P1-004 | P1-011 → P1-012; P1-005 begins after P1-001 | Safety design/adversarial review |
| W2 | P1-005 → P1-006 → P1-007/008 → P1-009 | P1-010 after P1-001/005 | Testnet drills separately approved |
| W3 | P2-001, P2-004, P2-006 feed later tasks | P2-002, P2-003, P2-005 | ADR-0018/0025 and schema/migration approvals |
| W4 | P3-001 → P3-002/003/004/005 → P3-006 | Tools can run in separate research-only branches | ADR-0020 acceptance; no backtest/download without approval |
| W5 | P4-001/002/003 → P4-004 → P4-005 | Mock/recorded drills parallel by subsystem | P4-005 requires explicit testnet/paper approval |
| W6 | P5-001 → P5-002/003 | UI and alert work can be separate after read model | Dashboard remains read-only |
| W7 | P6-001 → P6-002 | None | Signed live gate and separate written approval; currently blocked |
| W8 | P7 tasks one dimension at a time | No bundled exchange/symbol/platform expansion | Gate F and per-expansion approval |

## Approval and environment map

| Task class | Mock/fixture allowed | Recorded exchange fixture | Testnet required | Paper duration required | Real capital required | Manual approval |
| --- | --- | --- | --- | --- | --- | --- |
| Phase 0 identity/docs | Yes | No | No | No | No | ADR status only |
| Order/risk/reconcile code | Yes, mandatory first | Yes | Final adapter/drill tier only | No | No | Safety policy and external run |
| Validation integration | Yes | Yes | No by default | No | No | Backtest/download execution and ADR-0020 |
| Paper hardening | Yes first | Yes | P4-001/002 final tier and P4-005 | P4-005 | No | Explicit per run/window |
| Dashboard | Yes | Snapshot fixtures | Read-only observation optional | No | No | UI review; mutations forbidden |
| Limited live | Yes | Yes | Yes | Yes | P6-002 only | Barış explicit written approval; currently absent |

## Tasks blocked by current monitoring state

- TS-P4-005 cannot claim continuation of Day 0 v5. The current bridge API is unavailable; a future approved monitoring window must follow the reset policy.
- TS-P6-001 cannot cite an interrupted/unobservable window as complete paper evidence.
- No task may restart or ARM the bridge merely to collect roadmap evidence.

## Tasks blocked by missing evidence

- TS-P0-004: owner decision on ADR-0018/0025.
- TS-P2-006: representative writer/load/restore benchmark and recovery requirements.
- TS-P3-001: Barış decision on ADR-0020 after current-engine map.
- TS-P3-004: verified hftbacktest Hyperliquid field/sequence coverage.
- TS-P6-001/002: signed ADR-0029/live gate and all preceding evidence.

## Real-capital boundary

Only TS-P6-002 could ever require real capital, and only after TS-P6-001 passes and Barış issues a separate explicit authorization defining account, amount, limits, start/stop, retry and rollback. The roadmap itself provides no such authorization.

