# WP-P0-20 · dependent-tool disposition — per tool, per class

**Status: PROPOSED, not PERFORMED.** The acceptance gate wants a record of what each
dependent tool *was* — re-based, retired, patched, updated as reporting, or left on the
legacy path — and that is a migration output. The migration has not happened. What this
record does supply is the half that does not need it: every tool located, its class
verified against its source rather than against the plan's prose, and a disposition
proposed with the evidence that decides it. A migration executes this table; it does not
have to rediscover it.

Verified in this container against `master` `fe35b7c`. Line numbers are current.

## Class 1 — direct callers of the canonical function

Each imports `mega_walk_forward` and calls its `simulate_slice`, so each inherits the
canonical economics automatically once the function is migrated. The work is not code but
lineage: their existing artifacts were produced under the old economics.

| Tool | Evidence | Proposed disposition |
|---|---|---|
| `tools/multiwindow_oos.py` | `import mega_walk_forward as M` (:28, comment: "reuse data loaders, signals, simul…"), 3 `simulate_slice` sites | **RE-BASED.** No code change needed to inherit; every prior artifact must be re-stamped with the new cost lineage or retained as pre-migration history |
| `tools/cpcv_validator.py` | `import mega_walk_forward as mw` (:18), 1 site | **RE-BASED, then RETIRED at the port harvest.** Known-divergence #8 (`exit_mode` not passed to the simulator) is a LEGACY-DEFECT of the offline stage, and the map-#75 CPCV/PBO inline unification supersedes the stage — "the offline validation stage does not survive the harvest" |
| `tools/finalize_bootstrap_bh.py` | `import mega_walk_forward as M` (:22), 1 site | **RE-BASED.** Feeds the battery's BH-FDR element, so its outputs become verdict-bearing and bind to `evaluation_run_hash` + battery version |
| `tools/reference_producer.py` | `import mega_walk_forward as M` (:32), 3 sites | **RE-BASED, outputs regenerated.** It produces reference artifacts other work cites as ground truth; regenerate under the new lineage and retain the old set frozen and tagged, never deleted (WP-P0-02 namespaces) |

## Class 2 — independent simulators that do NOT inherit the canonical economics

The plan's earlier text claimed all eight "reference" the canonical function and that the
whole battery "inherits" its economics, and explicitly forbids repeating that. These two
are why: each **defines its own** `simulate_slice` and never imports `mega_walk_forward`.

| Tool | Evidence | Proposed disposition |
|---|---|---|
| `tools/rigorous_walk_forward.py` | `def simulate_slice(...)` at **:266**; no `mega_walk_forward` import | **LEFT ON THE LEGACY PATH, results stamped `SIGNAL_SCREEN_ONLY`.** Migrating a second simulator is a second migration and is outside this package. Under the ratified two-tier funnel cheap screening stays fully legal and its numbers are never acceptance-bearing |
| `tools/rigorous_walk_forward_parallel.py` | `def simulate_slice(...)` at **:254**; no `mega_walk_forward` import | **Same.** Its parallelism changes throughput, not economics; it is the same legacy path twice |

Leaving these unmigrated is only safe while the stamp is enforced. That enforcement is the
manifest and the promotion block, not this record.

## Class 3 — a patcher of the mega engine

| Tool | Evidence | Proposed disposition |
|---|---|---|
| `tools/variant_missing_knobs.py` | `def apply()` at **:233**, invoked as `import variant_missing_knobs as v; v.apply()  # patch mega_walk_…` (:29) | **PATCHED — re-pointed, with a behaviour freeze.** A monkey-patch aimed at the pre-migration function will silently patch a stale path, or worse, still apply and re-introduce the old behaviour inside the migrated one. Its own docstring (:15–18) records that the engine "fixes the stop at entry" and that changing this "would alter EVERY strategy's behavior -> that is Faz 3b": the re-point must therefore carry a proof that it changes nothing but its target |

## Class 4 — a reporting consumer that only describes the semantics

| Tool | Evidence | Proposed disposition |
|---|---|---|
| `tools/enrich_gate3_evidence.py` | `simulate_slice` appears only inside description strings, at **:17** and **:48** ("entry/exit resolved on the close bar (simulate_slice); holding_bar_limit caps duration") | **UPDATED AS REPORTING.** No code path changes. Those two sentences become false at migration and must be rewritten to describe the migrated economics — a stale description that outlives the behaviour it describes is how evidence quietly starts lying |

## What still makes this record incomplete

- Every disposition above is **proposed**. None has been performed, because none can be
  until the canonical path is migrated, and that waits on `WP-P0-12` reaching this
  repository.
- Class 1's re-basing needs the before/after comparison to name the economic differences;
  that comparison is its own outstanding acceptance criterion.
- The `SIGNAL_SCREEN_ONLY` stamp for Class 2 must be mechanically enforced at the point
  those tools write results. No such enforcement exists in this repository today.
