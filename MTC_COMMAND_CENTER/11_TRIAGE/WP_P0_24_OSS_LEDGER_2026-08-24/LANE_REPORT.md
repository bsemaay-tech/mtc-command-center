# Lane D report — WP-P0-24 OSS lifecycle policy and ledger

**Status:** **LANE D DONE — implementer package complete; T1 Lead acceptance remains Lead-owned.**

**Branch:** `feature/wp-p0-24-oss-ledger-20260824`

**Specified base verified at start:** `fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7` equalled `origin/master` when the lane began. Other worktrees advanced the remote-tracking ref by four commits during this lane; this branch was not rebased, merged or pushed.

**Audit tier:** T1, as fixed by the lane contract.

## Gate-1 package and explicit ADOPT/KEEP inventory

Before ledger authoring, §§13.1, 13.1a, 13.2 and Appendix B were read. The §13.2 rows marked ADOPT or KEEP were enumerated as:

1. Perspective — ADOPT, research only.
2. DuckDB — ADOPT.
3. Parquet — ADOPT, already declared.
4. PyArrow — ADOPT, already declared.
5. QuantStats — ADOPT with independent validation.
6. vectorbt open edition — KEEP, enrichment only.
7. hyperliquid-python-sdk — KEEP.
8. FastAPI — KEEP.
9. Uvicorn — KEEP.
10. Pydantic — KEEP.
11. Tailscale — ADOPT for private access.

The combined matrix rows `Parquet / PyArrow` and `FastAPI / Uvicorn / Pydantic` were split so every component has a distinct entry. No CANDIDATE, OPTIONAL/POC, REJECT, DEFER or reference-only row was silently promoted into this adopted/kept set.

## Delivered

- `PROPOSED_AGENTS_MD_POLICY.md`: clearly proposal-only; assigns dependency-steward/update/retirement roles; carries the twelve controls, integration modes, supply-chain floor, service cost, incident, abandonment, append-only and owner-authorized exit rules. Root `AGENTS.md` was not edited.
- `DEPENDENCY_LEDGER.md`: append-only contract; 11 real entries; every entry names an integration mode and has criteria 1–12; shared source/method evidence; complete Bridge 56-package hash-locked environment inventory; licence-text capture index; a deliberately superseded demo record retained with the required marker.
- `ROLLBACK_WALK_EVIDENCE.md`: real FastAPI 0.140.0 hash-enforced install → remove → absence check → reinstall prior exact pin; exit 0; commands and output captured; venv and temporary pin removed.
- `LANE_REPORT.md`: this status, QA, commit/staging evidence and open issues.

## Dispositions without unauthorized actions

- Existing Bridge pins FastAPI 0.140.0, Uvicorn 0.51.0, Pydantic 2.13.4 and hyperliquid-python-sdk 0.24.0 are `HOLD AT EXISTING PIN`; the ledger records them without authorizing update/expansion.
- Plan-level Perspective, DuckDB, QuantStats and Tailscale implementations are rejected until exact version/hash/licence/security/rollback gates close.
- Existing vectorbt optional import is held; new/expanded use is rejected pending exact version, licence and lock.
- Existing Parquet use is held pending an exact format/subset contract.
- PyArrow 23.0.0 is rejected as current adoption evidence because it is unhashed in the repository lock and affected by a named advisory. No protected file was edited and no upgrade/removal was attempted.

## Acceptance-gate self-QA

| Gate | Evidence | Result |
|---|---|---|
| Every currently adopted component has an entry | 11 explicit components above; ledger parser found 11 real entries | PASS |
| All twelve criteria per entry | structural parser found criteria 1–12 exactly 11 times each and zero missing rows | PASS |
| Integration mode named | structural parser checked every entry | PASS |
| Objective abandonment conditions | shared measurable windows/events plus component-specific conditions; no judgement-only wording | PASS |
| Dated vulnerability review with named source | OSV exact/version batch dated 2026-08-24; source failures/unknown versions recorded honestly | PASS |
| Supply-chain evidence | Bridge lock identified by SHA-256/git blob, 56 packages/1,345 hashes; missing locks explicitly fail/reject rather than being assumed | PASS |
| One rollback walked | FastAPI exact hash install/remove/absence/restore, exit 0, real output | PASS |
| Superseded entry retained | `DEMO-0001` says `SUPERSEDED by entry DEMO-0002 — retained, never edited away` | PASS |
| Authority boundaries | no adoption/update/removal authorized; no `AGENTS.md`, protected logic, schema, host or account change | PASS |
| Temporary cleanup | venv `Test-Path=False`; temporary pin deleted; only four deliverables remain | PASS |
| Markdown/diff hygiene | structural QA clean; trailing whitespace found after content commit was normalized; working-tree and cached `git diff --check` both passed before finalization commit | PASS |

No regression test is offered as defect-closure evidence, so D026 RED/GREEN is not claimed. The rollback's observed absent/restored states are operational evidence, not a simulated test.

## Primary finding requiring Lead/owner attention

`pyarrow==23.0.0` is listed affected by OSV under `GHSA-rgxp-2hwp-jwgg`, `CVE-2026-25087` and `PYSEC-2026-113`: potential use-after-free when reading Arrow IPC with pre-buffering. OSV marks versions 15.0.0 through 23.0.0 affected and 23.0.1 fixed. The repository's backtest lock also lacks hashes. This lane had no authority to edit the protected dependency; a separately scoped package must classify and handle it.

## Commit and exact staged-file record

### Content commit

Commit: `26e3582acf924adc47ec8a13338076f118cf496c`

Message (exact lane requirement):

`docs(wp-p0-24): OSS lifecycle policy proposal + dependency ledger (T1, lane D 2026-08-24)`

Verified cached file list before commit:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_24_OSS_LEDGER_2026-08-24/DEPENDENCY_LEDGER.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_24_OSS_LEDGER_2026-08-24/PROPOSED_AGENTS_MD_POLICY.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_24_OSS_LEDGER_2026-08-24/ROLLBACK_WALK_EVIDENCE.md
```

### Finalization commit

The finalization commit stages exactly these four paths: the three content files for whitespace-only normalization plus this report.

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_24_OSS_LEDGER_2026-08-24/DEPENDENCY_LEDGER.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_24_OSS_LEDGER_2026-08-24/LANE_REPORT.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_24_OSS_LEDGER_2026-08-24/PROPOSED_AGENTS_MD_POLICY.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_24_OSS_LEDGER_2026-08-24/ROLLBACK_WALK_EVIDENCE.md
```

Its SHA cannot be embedded in the bytes that create that same SHA. The final CLI summary and `git log -2` are the authoritative record. No push or merge is performed.

## Open issues and limits

1. PyArrow 23.0.0 advisory/unhashed-lock finding above requires separately authorized classification and remediation; this is the only identified current-version advisory.
2. Perspective, DuckDB, QuantStats and Tailscale are plan-level decisions without adopted versions or complete locks; ledger entries therefore reject implementation instead of inventing provenance.
3. vectorbt's checked PyPI metadata had no licence expression and GitHub returned `NOASSERTION`, conflicting with the brief's Apache-2.0 statement; documented licensing review is required before linked adoption.
4. Median private security-issue closure time is not publicly measurable for the components. Human release-publisher counts are clearly labelled as a conservative proxy, not a maintainer roster.
5. GitHub community-profile security-policy checks for vectorbt and Tailscale ended with HTTP 403/rate-limit after the earlier successful checks; recorded as attempted/source unreachable tonight.
6. The FastAPI walk is component-distribution scope with `--no-deps`; a future bump still needs a full-lock A→B→A rollback and application compatibility suite.
7. Lead Gate 5 T1 review, acceptance, repair dispatch (if any), Gate 7 handoff updates and any further git sequencing remain outside implementer authority.

## Boundary confirmation

No Pine, parity, MTC_V2, Bridge runtime, schema, deployment, host, credential, Docker, WSL, testnet, live, trading, account, push or merge action occurred. The dirty `C:\LAB\Tradingview_LAB_CLEAN` checkout and all named sibling worktrees were not touched. No AI CLI or sub-agent was spawned.
