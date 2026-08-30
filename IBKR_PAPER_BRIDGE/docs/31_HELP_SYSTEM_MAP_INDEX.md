# 31 — Help / System Map: AI-facing index

**Date:** 2026-08-16
**Status:** Index only — documentation, no implementation authority
**Audience:** A future AI agent (or developer) that needs a truthful map of this system

---

## 0. What this document is, and is not

This is a **pointer**, not a knowledge base. The knowledge lives in exactly one
machine-readable file:

```
IBKR_PAPER_BRIDGE/bridge/static/help_map.json
```

That file is the canonical Help/System-Map source. The browser Help page and any
future AI consumer read the **same** file, which is the whole point: a human
explanation and a machine explanation that cannot drift apart.

**Do not** copy component facts into this document, into a second JSON, or into a
memory file. If a fact is wrong, fix `help_map.json`. If a fact is missing, add it
to `help_map.json`.

This document authorizes nothing: no deployment, no TESTNET or mainnet activity,
no ARM, no order, no credential handling.

---

## 1. How to consume it

Read the file directly (it is plain JSON, UTF-8, no build step, no external
dependency):

```python
import json, pathlib
data = json.loads(
    pathlib.Path("IBKR_PAPER_BRIDGE/bridge/static/help_map.json").read_text(encoding="utf-8")
)
```

At runtime the same file is served by the existing static mount at
`/static/help_map.json`. Nothing else serves it, and it is never generated.

### Top-level keys

| Key | What it holds |
|---|---|
| `schema_version` | Integer. Bump it on any breaking shape change. |
| `truth_rules` | The rules every statement in the file obeys. Read these first. |
| `statuses` | The four allowed status labels and what each one means. |
| `connection_kinds` | The allowed `connections[].kind` values, including `blocked`. |
| `planes` | The four planes: `research`, `execution`, `exchange`, `control`. |
| `identities` | Owner / Bridge runtime / AI assistant, and what each may do. |
| `components` | The map itself. One object per component. |
| `flows` | Ordered step chains, including the deliberately blocked AI→controls flow. |
| `readiness` | The "built now / still required" view, per area. |
| `glossary` | Plain-language terms for a non-technical reader. |

### Component object

Every entry in `components` carries: `id`, `plane`, `name`, `status`,
`status_detail`, `one_liner`, `purpose`, `does`, `does_not`, `boundaries`,
`safety`, `connections`, `sources`, `technical`.

Two fields matter more than the rest and are routinely skipped by readers:

- **`does_not`** — the boundary that stops a reader assuming a component does
  more than it does. Most misreadings of this system come from ignoring it.
- **`status` + `status_detail`** — `status` is one of four coarse labels; the
  nuance ("implemented but switched off", "code exists but unverified on the
  server") lives in `status_detail`. Never quote the label without the detail.

`connections[]` entries are `{to, label, kind}`. `to` is another component `id`.
A `kind` of `blocked` means the connection **deliberately does not exist and must
never be built** — it is drawn so the absence is visible, not because a wire is
there.

---

## 2. How to verify it before trusting it

Automated integrity checks live in
`IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py` and run with the normal suite:

```
python -m pytest IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py -q
```

They assert that the JSON parses, that component ids are unique, that every
`plane`, `status` and `connections[].to` resolves, that every `flows[].steps[]`
target resolves and that no step claims `current` for a component whose `status`
is not `current_v1`, that no component links to itself, that no required field is
empty, that every path in `sources` exists in the repository, that a set of
contested `status` values stays pinned, and that a fixed list of load-bearing
phrases is still present. They also pin the two source-truth repairs of
2026-08-17: the LLM gate's dormant classification and its `planned` edges, and
the Dashboard V1 surface description (page count, next-bar UTC time, no
client-side reconnect).

### What the suite does **not** prove

These are **structural and selected-phrase tripwires**. They catch shape damage,
a dangling reference, a status quietly flipped, and the deletion of a phrase
someone previously decided was load-bearing. They do **not** prove that every
semantic claim in the file is still current: a sentence can keep its exact
wording and become false the moment the code, the configuration, the deployment
state or an owner decision changes.

A green run therefore means "the map did not erode in the ways we know how to
detect". It does not mean "the map is true". When the system changes, the
affected claims must be re-verified by a human against repository source,
configuration, deployment evidence and recorded owner decisions. Do not treat a
passing suite — or this document — as acceptance.

---

## 3. Rules for editing `help_map.json`

1. **Source before claim.** Every statement must be checkable against repository
   source, configuration, or a recorded owner decision. If you cannot point at
   one, do not write the sentence.
2. **Never promote a plan.** `PLANNED V2` and `SEPARATE FUTURE GATE` items are
   written as not existing. Existing code is not the same as deployed,
   configured, or verified — that distinction is why `NOT DEPLOYED` exists as a
   separate label.
3. **Keep `does_not` honest.** It is the field a careless edit erodes first.
4. **Add `sources` for anything new**, and keep them repository-relative so the
   existence check can resolve them.
5. **The AI boundary is not negotiable.** The AI assistant has no ARM, DISARM,
   KILL, config, order, wallet, shell, deployment or code-editing authority in
   any current or planned version. Any edit implying otherwise is wrong.
6. **No secrets, ever** — no keys, addresses, tokens or wallet material.
7. **Stay dependency-free.** The Help page renders with no external library, no
   CDN, and no markup injection; every value reaches the document as text.
8. **Separate owner-operated control from automatic fail-safe action.** Only the
   owner may arm, and only the owner operates ARM/DISARM/KILL. The runtime may
   still disarm *itself* for safety. Both facts are true; writing either one
   alone produces a false picture. `ARMED` gates new entries — reconciliation,
   protection, notification and safety work continue while `DISARMED` or
   `KILLED`, as applicable to each.
9. **Do not soften a recorded gap.** KILL is not production-hardened: the
   Dashboard requests `flatten=false` while the engine's KILL path calls
   `cancel_all()` regardless, which can leave an open position whose
   exchange-native protective orders were cancelled. State the mechanism, not a
   reassurance.
10. **Modelled is not realized.** Research costs are assumptions; actual fills,
    realized slippage, funding and partial-fill behaviour are execution and
    exchange evidence. Never let the two share a sentence without the
    distinction.
11. **Hashed is not signed.** Full-reconciliation checkpoints are canonically
    hashed and immutable. They are not cryptographically signed, and
    "read-only" there means zero *exchange-state* mutation — local evidence and
    checkpoints are written every cycle.
12. **Scaffolding is not a feature — check the constructor, not the class.**
    Rule 2 is about deployment and configuration; this one is about reach. A
    class can exist, pass its own unit tests, and own a block in
    `config/bridge.yaml` while no runtime path ever constructs it. The LLM gate
    is exactly that: `bridge/app.py` builds `BridgeEngine(...)` with no
    `llm_gate`, so `bridge/engine/engine.py` installs `NullLLMGate`. Before
    writing that a component works, find its constructor. If nothing but a test
    constructs it, it is dormant scaffolding: label it `PLANNED V2`, and make
    its store, logging and directive edges `planned`. Preserve the future
    boundary either way — an enabled gate could suppress or select trades and
    so change outcomes, but could never originate or enlarge an order.
13. **Configuration visibility is not activation, and dormant is not silent.**
    The two corollaries a careless edit of rule 12 gets wrong, both checkable
    against source. First, `bridge/config_contract.py` reads the candidate once,
    validates modeled active leaves, and binds them into
    `ValidatedRuntimeSettings`. `bridge/api/routes.py` serves only
    `ValidatedRuntimeSettings.effective_view()` from `/api/config` and places
    that same view in the dashboard snapshot. The view has no `llm` namespace,
    so `app.js` displays Veto Mode as `N/A`; this absence does not construct or
    activate a gate. Second, the dormant path still writes:
    `NullLLMGate.check()` returns `SKIPPED` with
    reason `llm disabled`, and the engine stores a generic `LLM_SKIPPED`
    decision row for it. What is genuinely absent is narrower — no `directives`
    row and no `llm_calls` row. And `llm_directive_id` is a column on the
    **`trades`** row, not on a decision row.
14. **Describe the interface as it is wired, and state each gap once.** Count
    the pages in `index.html` rather than repeating a remembered number: V1 has
    the six original pages plus Help. Read `app.js` before describing
    behaviour — the Next Bar card renders a UTC time, not a countdown, and
    `connectWs()` registers only a `message` listener, so the snapshot `ws.py`
    sends on connection is the client's only resynchronisation and a dropped
    socket is never reopened. In `readiness`, a gap belongs to exactly one
    area row: interface gaps live under Dashboard V2, not under Source
    implementation.

---

## 4. Related documents

- `01_ARCHITECTURE.md` — the binding V1 technical contract.
- `30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md` — V2 direction and open
  questions (documentation only; grants no implementation authority).
- `26_FULL_RECONCILIATION_CONTRACT.md`, `27_AUTHORITATIVE_RISK_SNAPSHOT_CONTRACT.md`
  — the read-only reconciliation and risk-evidence contracts the map summarises.
- `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_HELP_WIKI_GATE1_2026-08-16.md` — the Gate-1
  scope this feature was built against.
