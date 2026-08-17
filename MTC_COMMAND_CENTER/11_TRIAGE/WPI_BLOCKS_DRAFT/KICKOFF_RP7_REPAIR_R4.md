# KICKOFF — RP7-WPI-RO round 4 (owner-authorized past the T0 cap): five Codex findings

Owner authorized this 4th round in-session 2026-08-10 (~17:15) after the second-flagship
Codex xhigh audit (`RP7_CODEX_T0_AUDIT_2026-08-10.md`) returned BLOCK 5 — F1 is a
security-relevant false-PASS hole that must be closed regardless of the cap. Recorded as
a standing-authority §1 escalation resolved to CONTINUE by explicit owner grant.

You are Claude Opus 5 xhigh, implementer. Working dir: C:\LAB\Tradingview_LAB_CLEAN.
No host/network. No commit.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

`WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_2026-08-10.md` (findings 1–5 with executed
falsifications + required repairs = the contract), `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`
(current `1d118d15…`, 58012 B), `SELF_QA_RP7.md`, `STATUS_RP7.md`,
`WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` (edit only §8.2 rows the fixes
name), `DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

## The five, exact repairs (Codex's "Required repair" text binds)

- **F1 (BLOCK)** — the subject venv must NOT arbitrate its own status or package state.
  (a) STATUS JSON parser: run under the PINNED system interpreter (add `/usr/bin/python3`
  as a bound tool with the same kind/mode/owner discipline as the other tools) with
  `-I -S` — it needs no venv context. (b) `verify_lock.py` parity: run under a trusted
  interpreter with `site` disabled (`-I -S`), supplying the venv's `site-packages` as an
  EXPLICIT, bounded, complete metadata path the trusted process inspects — do NOT import
  venv startup configuration. This composes with F3: define ONE explicit discovery
  universe. Add D026 fixtures where a `.pth` and a `sitecustomize.py` forge the accepted
  output and attempt a write: RED on the current `-I` bytes, GREEN only when neither
  executes (marker absent, forged line rejected).
- **F2 (HIGH)** — row 22: parse and validate ALL `ss` rows to clean EOF first, recording
  only sanitised counters/flags in-loop; apply wildcard / unexpected-address / count
  FAILs only AFTER reader diagnostics + termination + grammar all hold. Both order
  permutations (wildcard-first, malformed-first) must be D026 RED/GREEN and both must
  reach STOP rc 3 when any record is malformed.
- **F3 (HIGH)** — row 19 preflight: enumerate every metadata format/location the
  verifier's `importlib.metadata` discovery accepts (dist-info, egg-info, and any
  zip/extension route the trusted verifier permits), OR make the trusted verifier reject
  every non-preregistered format/location before comparing versions. Add readable /
  unreadable / malformed / unexpected-egg-info D026 cases. Keep it consistent with the
  F1 explicit-discovery-universe design.
- **F4 (MEDIUM)** — restore the preregistered order: `netns binding → status rows 20-21
  → listener rows 22-23`. Only the row-22 netns preflight inversion is authorized; the
  whole-listener move is not. Add a two-deviation fixture proving which result is first.
- **F5 (LOW)** — carry caller-specific unreadable reasons through lstat/component walks
  (`installed_lock_unreadable` row 17, `verifier_unreadable` row 19a,
  `metadata_unreadable` row 19 — not generic `path_not_evaluable`); reconcile the
  regular-digest metadata-deviation forms with rows 17/19a; drop the extra `path=` from
  `installed_lock_object_unexpected`; route the two remaining raw `%F` sites
  (`:762`, `:768`) through `wpi_kind_token`. Falsify each against an erroring stat + a
  multi-word object kind.

## Deliverables

Repaired `RP7-WPI-RO.sh` + `SELF_QA_RP7.md` (every fix REAL RED/GREEN; the .pth/
sitecustomize forge fixtures are the load-bearing ones — run them; the QA fence must
re-extract and re-run green) + `STATUS_RP7.md` + narrow draft edits +
`RP7_REPAIR_R4_REPORT.md`. `bash -n` PASS; new SHA-256 + bytes. If a new pinned tool
(`python3`) needs a `<PIN-AT-FREEZE>` path/hash, mark it so and note it as a freeze-gate
input. Touch ONLY those five files (+draft). Do not commit.
