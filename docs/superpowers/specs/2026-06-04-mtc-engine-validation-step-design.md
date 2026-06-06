# MTC-Engine Validation Step — Design Spec

> **Status:** Implemented additively in `MTC_COMMAND_CENTER/02_MTC_BACKTEST` on 2026-06-04.
> **Date:** 2026-06-04
> **Owner discipline:** parity-first, deterministic, additive-only, do-not-break-existing.
> **Author:** Claude Opus 4.8

## 1. Problem

Today the QuantLens → MTC funnel tests each YouTube-derived **signal producer in isolation** (raw
signal only, separated from exits/filters/risk — Signal Integrity Gate). A producer is never run
through the real **MTC risk engine** (SL / TP / trailing / position sizing) until the final MTC_v2
integration stage. Result: we never learn how a strategy actually behaves under MTC money management
before committing to integration.

**Goal:** Insert one new workflow stage — **MTC-Engine Validation** — between naked-producer
screening and the parity-candidate stage. A shortlisted producer is run through the existing MTC
Python engine (`MTCRunner`) with **risk ON, filters/guards OFF**, benchmarked against buy-and-hold,
and verified for **producer-level parity** against a standalone Pine adapter — all **without touching
`MTC_V2.pine`**.

## 2. Approved Decisions (from brainstorming)

| Decision | Choice | Rationale |
|---|---|---|
| Engine | Reuse existing `MTCRunner` with a **light config profile** (filters/guards OFF, risk ON) | One engine, no fork, parity preserved |
| Producer binding | **Manual `SignalPlugin` adapter** per promoted producer | Explicit, no hidden abstraction, decouples research tools from production engine; parity test catches mismatch |
| Funnel position | **Shortlist only** — run MTC engine only for producers that already passed cheap naked screening | Keeps cheap mass screening; heavy engine runs for few candidates |
| Pine scope | **Python plugin + standalone Pine producer adapter + producer-level parity** | Intermediate parity check, but `MTC_V2.pine` stays untouched until final stage (Production Safety preserved) |
| Packaging | **Approach A** — new bridge module + CLI inside `02_MTC_BACKTEST` that orchestrates existing engine + WF/stats/parity tools | Least coupling, reuses everything |

## 3. Production-Safety Reconciliation

The user wants an intermediate parity check; the existing rule says `MTC_V2.pine` changes only at the
final stage (default-OFF, feature-gated). These do **not** conflict:

- Parity is verified on a **standalone Pine producer adapter** (raw signal only), reusing the existing
  `01_MTC_PROJECT/parity_oracles/feature_adapters/pinets/` infrastructure.
- `MTC_V2.pine` is **not edited** at this stage. Full integration into `MTC_V2.pine` (feature-gated,
  default-OFF) remains the final stage, unchanged.
- "Pine" at this step = isolated producer adapter for parity, **not** an `MTC_V2.pine` edit.

## 4. Architecture — New Components (all additive)

| # | Component | Location | Responsibility |
|---|---|---|---|
| 1 | Light config profile | `02_MTC_BACKTEST/src/config/profiles/light_risk.py` | Factory returning an `MTCConfig`: all filters OFF, all guards OFF, SL/TP/trailing/sizing ON. Not a new engine — a preset. Supports per-producer overrides. |
| 2 | Producer adapters | `02_MTC_BACKTEST/src/modules/signals/producers/<name>.py` | One `SignalPlugin` subclass per promoted producer. `generate(df) -> (long_raw, short_raw)`. Mirrors existing `supertrend.py` / `range_filter.py`. |
| 3 | Standalone Pine producer adapter | `01_MTC_PROJECT/parity_oracles/feature_adapters/pinets/producer_<name>_v1.pine` | Emits raw long/short signal only, for parity. Not `MTC_V2.pine`. |
| 4 | Bridge CLI / orchestrator | `02_MTC_BACKTEST/src/cli/mtc_engine_validate.py` | Loads producer + light profile, runs `MTCRunner` over WF/OOS windows, computes metrics + buy&hold + alpha + bootstrap/DSR/FDR (existing tools), runs producer parity, emits summary-first report + CSV/JSON + Artifact Index. Orchestrates; does not reimplement. |
| 5 | Promotion level + gate | `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` | Add `MTC_ENGINE_VALIDATED` to the ladder (between SANDBOX/FORWARD and PARITY_CANDIDATE). Add **MTC-Engine Gate**: edge survives MTC risk engine AND producer parity passes. |
| 6 | Workflow doc | `04_SHARED/prompts/05_ai_workflow/` + pointers in `START_HERE.md` / runbook | Runbook entry describing the step. |

**Reused, NOT modified:** `MTCRunner`, `SignalPlugin` base, risk modules (SL/TP/trailing/sizer),
QuantLens WF/stats/alpha tools, `parity_oracles` infra, `MTC_V2.pine`.

## 5. Data Flow

```
[EXISTING] QL naked screening (overnight, hundreds of configs, cheap filter)
         -> shortlist (PROMOTE_TO_SANDBOX and above)
[NEW]    1. Write producer SignalPlugin adapter (manual)
         2. Build light config profile (filters/guards OFF, risk ON, per-producer overrides)
         3. mtc_engine_validate CLI:
               run MTCRunner (risk ON, filters OFF) over WF/OOS windows
               metrics + buy&hold + excess alpha + bootstrap/DSR/FDR  (existing tools)
               producer parity: Python plugin  <->  standalone Pine adapter
               summary-first report + CSV/JSON + Artifact Index
         -> if pass -> MTC_ENGINE_VALIDATED
[EXISTING] PROMOTE_TO_PARITY_CANDIDATE -> ... -> MTC_V2.pine final integration (final stage, default-OFF)
```

One new link inserted in the funnel; everything before and after is unchanged.

## 6. Parity Scope

- **Producer-level only** (raw signal, L0–L3). Full lifecycle parity (L4–L6) is **not** claimed here
  — consistent with Appendix A / PineTS limits.
- Parity asserts: Python plugin raw long/short signals match the standalone Pine adapter within
  tolerance on a shared dataset, on confirmed bars only (no repaint / no lookahead).

## 7. Light Config Profile Semantics

- **Base preset:** every filter OFF (volume, ATR vol, HTF trend, MA, MA slope, MACD hub, McGinley,
  range regime), every guard OFF (equity-curve guard, drawdown guard, consecutive-loss guard).
- **Risk ON:** stop loss (mode/params per producer), multi-TP, break-even, trailing, position sizing.
- **Per-producer overrides:** a producer that is TP-only or SL-only in its source video overrides the
  base preset accordingly. Base opens all risk features; the producer narrows to its native semantics.
- **Entry mode:** producer's native mode (Signal vs Edge), `max_entries` per the source video.

## 8. Compatibility Constraints (must-not-break)

- `MTCRunner`, risk-module, and `SignalPlugin` signatures unchanged.
- QuantLens overnight tools untouched.
- `MTC_V2.pine` untouched until the existing final integration stage.
- `parity_oracles` infra reused; only new adapters added.
- `07_BACKTEST_AND_OPTIMIZATION_RULES.md` gates/levels **extended, not rewritten** (new gate + level
  inserted).

## 9. Testing

| Type | Check |
|---|---|
| Unit — profile | Light profile factory yields filters OFF / guards OFF / risk ON (assert config flags). |
| Unit — adapter | Each producer `generate()` returns boolean Series aligned to df; signals only on confirmed bars (no lookahead). |
| Regression/golden | A known producer (e.g. Supertrend) through the bridge yields a deterministic metric snapshot. |
| Parity | Producer Python vs standalone Pine adapter raw-signal match within tolerance (existing parity harness). |
| Integration | Bridge CLI end-to-end on a small dataset produces report + artifacts + Artifact Index. |

## 10. Reporting

Follows the existing standard (07 RULES §5, §10, §11): summary-first Markdown, raw rows in CSV/JSON,
mandatory metrics (strategy return, buy&hold, excess alpha, max DD, PF, trades, etc.), Artifact Index.
Report explicitly states: filters/guards OFF, risk ON, producer-level parity status.

## 11. Open Risks / Notes

- Producer native entry/exit semantics may differ from MTC defaults → handled by per-producer overrides
  (Section 7).
- This step proves edge **with MTC risk management**, not a proven live edge — promotion ceiling rules
  in 07 RULES §9 still apply.
- The bridge is an orchestrator: if an existing tool (WF, alpha, parity) changes its interface, the
  bridge adapts — no engine logic is duplicated.

## 12. Out of Scope

- No changes to `MTC_V2.pine`.
- No new backtest engine.
- No modification of QuantLens overnight screening tools.
- No auto-generation of producers from a shared spec (explicitly rejected — manual adapters chosen).

## 13. Implementation Status

Implemented additively:
- `02_MTC_BACKTEST/src/config/profiles/light_risk.py`
- `02_MTC_BACKTEST/src/modules/signals/producers/`
- `02_MTC_BACKTEST/src/cli/mtc_engine_validate.py`
- `02_MTC_BACKTEST/tests/test_light_risk_profile.py`
- `02_MTC_BACKTEST/tests/test_mtc_engine_validate_cli.py`

`MTC_V2.pine`, `MTCRunner`, risk modules, and QuantLens overnight tools were not modified.
