# WP-P0-24 append-only dependency ledger

**Created:** 2026-08-24

**Package audit tier:** T1

**Scope:** every component that §13.2 of `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` marks **ADOPT** or **KEEP**. Combined rows are split into individual components.

**Authority:** this ledger can reject or hold a component. It does not authorize adoption, update, retirement or removal.

## Append-only contract

1. An entry is immutable after its first commit. Corrections, version bumps, decisions and status changes are new entries.
2. A successor says `SUPERSEDES entry N`; the old entry remains. A status marker may be appended, never substituted for old text.
3. Evidence is identified by immutable tag/commit, artifact hash, git blob or dated URL result. A moving `main` URL alone is not provenance.
4. `UNKNOWN`, `NOT PUBLICLY MEASURABLE`, `NOT VERSION-SELECTED` and `SOURCE UNREACHABLE` are evidence outcomes. They are never converted to a guess.
5. `HOLD AT EXISTING PIN` preserves existing state but authorizes no install, update or expansion. `REJECTED FOR IMPLEMENTATION` blocks a planned use. Neither status removes files.
6. Retirement/removal is always a separate, explicitly owner-authorized cleanup act after evidence preservation. No entry schedules deletion.
7. The dependency steward is the Lead Orchestrator. The named update owner in each entry prepares evidence; Barış retains retirement/removal authority and any adoption authority not separately delegated.

## Research method and shared evidence

Research was read-only and limited to repository manifests, PyPI JSON/release artifacts, upstream Git refs/release metadata, GitHub community-profile metadata and OSV. Checks occurred on 2026-08-24, approximately 16:55–17:01 UTC.

- Brief source: [`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`](../MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md), §§13.1, 13.1a, 13.2 and Appendix B.
- Bridge direct input: [`IBKR_PAPER_BRIDGE/requirements.in`](../../../IBKR_PAPER_BRIDGE/requirements.in), SHA-256 `709523df0106ac11546ca35e23e0eaad96b75f56010aacdbdc29fe9ab28c938d`, git blob `1852ff3b5a6591ddff029b984ff25dc689a3cac1`.
- Bridge lock: [`IBKR_PAPER_BRIDGE/requirements.lock`](../../../IBKR_PAPER_BRIDGE/requirements.lock), SHA-256 `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3`, git blob `47f53fa227bf0f18b9bf9bd77e060d8856961728`. It contains 56 exact packages and 1,345 permitted artifact hashes; the four direct components below each have two artifact hashes.
- Backtest lock: [`02_MTC_BACKTEST/requirements-lock.txt`](../../02_MTC_BACKTEST/requirements-lock.txt), SHA-256 `6469b053dcc97e9356d2d71619ffddf995a6b5f14e40e604d0c606e534f70d2a`, git blob `d24cf4b3c0cd3ecc4eb98fa914f8df442636df17`. It pins versions but contains no artifact hashes.
- Advisory source: [OSV API](https://api.osv.dev/v1/query) queried by PyPI package plus exact version. The 56-package Bridge batch returned zero affected packages at `2026-08-24T17:00:34Z`. A zero result is a dated source result, not a warranty.
- Maintainer proxy: distinct human GitHub release publishers during 2025-08-24 through 2026-08-24. This is a conservative, reproducible proxy, not a governance roster. Release counts include prereleases. The median time to close private security reports was not publicly measurable for any component; entries state that gap.
- Security path probe: the official GitHub community-profile API exposed no repository security-policy file for FastAPI, Uvicorn, Pydantic, hyperliquid-python-sdk, Arrow, Perspective, DuckDB or QuantStats. The same API returned HTTP 403 after the unauthenticated limit for vectorbt and Tailscale; those two are recorded as attempted/source unreachable tonight, not as “no policy.”

### Observed upstream activity (context, not version selection)

| Component | Latest stable release observed | Releases in prior 12 months | Human release publishers observed | Repository pushed | Source |
|---|---:|---:|---:|---:|---|
| FastAPI | `0.141.1`, 2026-07-29 | 93 | 1 | 2026-08-19 | [upstream](https://github.com/fastapi/fastapi) |
| Uvicorn | `0.52.4`, 2026-08-19 | 24 | 1 | 2026-08-24 | [upstream](https://github.com/encode/uvicorn) |
| Pydantic | `v2.13.4`, 2026-05-06 | 22 | 1 | 2026-08-24 | [upstream](https://github.com/pydantic/pydantic) |
| hyperliquid-python-sdk | `0.24.0`, 2026-06-04 | 7 | 1 | 2026-06-04 | [upstream](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) |
| Apache Arrow / PyArrow | `apache-arrow-25.0.1`, 2026-08-10 | 14 | 0 observable (automation published releases) | 2026-08-24 | [upstream](https://github.com/apache/arrow) |
| Perspective | `v5.2.0`, 2026-08-10 | 15 | 0 observable (automation published releases) | 2026-08-10 | [upstream](https://github.com/finos/perspective) |
| DuckDB | `v1.5.5`, 2026-07-22 | 12 | 3 | 2026-08-24 | [upstream](https://github.com/duckdb/duckdb) |
| QuantStats | `v0.0.81`, 2026-01-13 | 3 | 1 | 2026-07-20 | [upstream](https://github.com/ranaroussi/quantstats) |
| vectorbt | `v1.1.0`, 2026-07-05 | 4 | 1 | 2026-08-02 | [upstream](https://github.com/polakowo/vectorbt) |
| Tailscale client | `v1.102.3`, 2026-08-20 | 28 | 6 | 2026-08-24 | [upstream](https://github.com/tailscale/tailscale) |

## Shared lifecycle controls referenced by every entry

- **A — Abandonment floor:** abandoned if upstream archives/read-only-locks the repository; no stable release and no human merge/release activity occur for 365 consecutive days; a HIGH/CRITICAL report is not publicly acknowledged or privately confirmed within 7 calendar days, or no fix/operational mitigation is available within 30 calendar days; verified artifacts disappear or cease matching published hashes; or the licence changes outside the accepted integration mode. A stricter entry condition wins.
- **U — Update:** named update owner checks at the stated cadence and within one business day of an advisory. A bump regenerates the complete hash lock, runs repository-artifact compatibility tests and receives the tier required by the highest affected surface. No automatic update.
- **I — Incident:** record and notify the Lead the same business day; stop new installs/updates; preserve the current lock/artifacts; disable the dependent feature or pin to a known-safe prior state first. A compromised release additionally blocks the artifact hash. A breaking release stays out until tests and review accept it. No host/account contact is implied.
- **E — Evidence:** preserve source/tag/commit, artifacts and hashes, full licence/notice, advisory results, maintainer/activity measurements, benchmarks, decision, compatibility results and rollback evidence before retirement/removal.
- **R — Retirement:** after E, the Lead proposes an exact cleanup scope. Only a separate explicit Barış authorization may retire or remove it. Stop-maintaining is not delete authority; no automatic deletion.

---

## Entry 0001 — Perspective (FINOS)

**Brief status:** ADOPT — research only.

**Ledger disposition:** **REJECTED FOR IMPLEMENTATION until a separate adoption package selects a version and closes controls 1–5 and 10.** No Perspective package or asset is present in the inspected manifests.

**Integration mode:** `LINK_AS_DEPENDENCY`, research UI only; never execution truth.

| # | Criterion | Evidence and rule |
|---:|---|---|
| 1 | Provenance | Canonical upstream [finos/perspective](https://github.com/finos/perspective) redirects to the official repository. PyPI `perspective-python` latest observed was `5.2.0`, uploaded 2026-08-10, sdist SHA-256 `625a3dad9c398b703cf4f36ea116924ad6a3be7430480b1e2571ca934314199f`. This is research context only: **no exact tag/commit/artifact is adopted and no acquisition path exists**. |
| 2 | Licence | Upstream/PyPI declare Apache-2.0. No adopted-version licence/NOTICE text is captured because no version is selected. Linking must retain the licence, notices, change notices and applicable attribution. Until exact texts are captured, it **requires a documented licensing review before adoption in this integration mode**. |
| 3 | Dependency/supply chain | No repository lock and therefore no complete hash-pinned transitive set. PyPI 5.2.0 exposes optional `aiohttp`, `anywidget`, `starlette` and `tornado` integrations; exact chosen extras are not declared. Cost is unknown. Gate fails. |
| 4 | Vulnerabilities | 2026-08-24: exact-version review impossible because no version is selected. Before adoption query OSV and the upstream security tab for the selected Python and browser packages and record exposure in a browser-rendered research grid. |
| 5 | Maintainer/activity | 15 GitHub releases in 12 months; releases were automation-published, so active human-maintainer count is not established. Median security closure time is not public. No repository security-policy file was exposed by GitHub community profile. These unknowns are acceptance gaps. |
| 6 | Abandonment | Shared A, plus abandoned if two consecutive quarterly reviews show no human merge/release activity even when automation still publishes artifacts. |
| 7 | Update | Owner: Lead for WP-P0-14/Minimum Explorer. Quarterly per U. Test the selected build against a real `TrialRecord`, filter/sort/group behaviour, browser export and accessibility; no execution-dashboard import. |
| 8 | Incident | Shared I. First disable the Perspective renderer and fall back to the repository's plain read-only table; never disable or alter the underlying TrialRecord ledger. |
| 9 | Portability/export | Perspective may render but never own canonical data. Input remains TrialRecord/Parquet; view configuration must export as documented JSON. Acceptance test: the same rows remain readable without Perspective. |
| 10 | Replacement/rollback | Replacement: bounded vanilla HTML/JS table over the existing read-only query output. Estimated switch: medium (filters/grid state and accessibility). Required rollback: remove the pinned package/assets and render the preserved fixture in the plain table; not yet walked, so adoption is rejected. |
| 11 | Evidence preservation | Shared E, including screenshots, browser/accessibility results, bundle-size measurements, view-state JSON and the plain-table comparison. |
| 12 | Retirement/removal | Shared R. Rejection does not authorize deletion of a future POC or its findings. |

## Entry 0002 — DuckDB

**Brief status:** ADOPT.

**Ledger disposition:** **REJECTED FOR IMPLEMENTATION until an exact version, hash lock and real Parquet benchmark/rollback are accepted.** No DuckDB dependency was found in inspected manifests.

**Integration mode:** `LINK_AS_DEPENDENCY`, embedded research query layer only.

| # | Criterion | Evidence and rule |
|---:|---|---|
| 1 | Provenance | Canonical [duckdb/duckdb](https://github.com/duckdb/duckdb). PyPI latest observed `1.5.5`, uploaded 2026-07-22, sdist SHA-256 `72f33ee57ca7595b23957671a2cc7f7fe2be0ecc2d68f63abedcfcaa3a5c1238`. No exact version/tag/commit/artifact or acquisition path is adopted. |
| 2 | Licence | Upstream reports MIT. Exact adopted-version text is absent because no version is selected. Linking obligation is to preserve copyright and licence notice in copies/substantial portions. Exact capture remains mandatory. |
| 3 | Dependency/supply chain | No lock. Base Python wheel declares no mandatory Python dependency; `all` adds IPython, fsspec, NumPy, pandas, PyArrow and ADBC manager. Exact extras and native-binary hashes are not selected. Gate fails. |
| 4 | Vulnerabilities | 2026-08-24: no exact version to query; review not claimable. Selected native wheel and bundled engine must be checked in OSV/GitHub advisories before adoption. |
| 5 | Maintainer/activity | 12 releases/12 months; 3 human release publishers observed; pushed 2026-08-24. Median security closure time not public; no repository security-policy file exposed through GitHub community profile. |
| 6 | Abandonment | Shared A, plus abandoned if the selected platform wheel is missing or unverifiable for two consecutive stable releases. |
| 7 | Update | Owner: Lead for trial-catalog query layer. Quarterly per U. Benchmark real repository Parquet, schema/null semantics, deterministic queries, export and memory limits before every bump. |
| 8 | Incident | Shared I. Disable DuckDB query acceleration and use the named PyArrow/pandas bounded reader; canonical Parquet remains untouched. |
| 9 | Portability/export | DuckDB files are caches, never truth. Export every durable table to Parquet/CSV plus schema; acceptance proves a fresh process without DuckDB reads the export. |
| 10 | Replacement/rollback | Replacement: PyArrow/pandas bounded scans for small research sets. Switching cost medium. Rollback: uninstall exact DuckDB wheel, delete no data, rebuild query cache from preserved Parquet using fallback; not walked. |
| 11 | Evidence preservation | Shared E, including query SQL, explain plans, benchmark fixtures/results and exported datasets. |
| 12 | Retirement/removal | Shared R; removal of cache files also requires exact owner-authorized scope. |

## Entry 0003 — Apache Parquet format

**Brief status:** ADOPT — already declared.

**Ledger disposition:** **HOLD AT EXISTING FORMAT USE; no new writer/reader adoption authorized until a format-version/subset contract exists.**

**Integration mode:** `FILE_OR_API_INTEROP` (open file format; not a linked executable dependency).

| # | Criterion | Evidence and rule |
|---:|---|---|
| 1 | Provenance | Canonical format upstream is [apache/parquet-format](https://github.com/apache/parquet-format). Repository plans and manifests use `.parquet`, but no exact format-spec tag/commit or acquisition path is recorded. Each file's writer metadata is not a substitute for a repository format policy. |
| 2 | Licence | Apache-2.0 is declared upstream. The canonical Apache-2.0 full text was reviewed from `https://www.apache.org/licenses/LICENSE-2.0.txt` on 2026-08-24 (UTF-8 SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`). FILE interop adds no library-linking conclusion; copied specs/code/notices retain Apache obligations. |
| 3 | Dependency/supply chain | The format has zero executable/transitive dependencies. Every concrete reader/writer is separately ledgered and hash-locked; current PyArrow fails that hash floor (entry 0004). |
| 4 | Vulnerabilities | Formats have parser exposure rather than a package version. Review is delegated to each concrete reader/writer exact version; entry 0004 records an affected PyArrow parser path. Untrusted Parquet/IPC input is never assumed safe. |
| 5 | Maintainer/activity | Apache Arrow had 14 releases/12 months and current activity, but release automation does not establish a human maintainer count. Median security closure time is not public. Apache maintains a project security process outside this ledger; exact format governance roster still must be captured. |
| 6 | Abandonment | Shared A applied to `apache/parquet-format`, plus abandoned for new writes if two independent maintained readers cannot read the repository's declared subset. Existing files remain preserved. |
| 7 | Update | Owner: research-data steward/Lead. Quarterly. A format/subset bump must round-trip real bundles through two independent implementations and preserve schema/metadata/hashes. |
| 8 | Incident | Stop ingest of untrusted files, pin/disable the affected reader, preserve original bytes and use a non-affected independent reader in isolation. Never rewrite canonical data as an incident reflex. |
| 9 | Portability/export | This is the portability format. Every dataset also carries an external schema/manifest and can export bounded samples to CSV/JSON for independent recovery. |
| 10 | Replacement/rollback | Replacement: Arrow IPC or CSV+schema for bounded exchange. Switching cost high for bulk history. Rollback: previous writer and format subset read the preserved pre-change fixture; not yet walked as a format-version change. |
| 11 | Evidence preservation | Shared E plus byte hashes, schema, writer metadata, round-trip fixtures and independent-reader results. |
| 12 | Retirement/removal | Shared R. Old Parquet artifacts are evidence/data and cannot be deleted automatically. |

## Entry 0004 — PyArrow

**Brief status:** ADOPT — already declared.

**Ledger disposition:** **REJECTED at existing `23.0.0` for new/continued adoption evidence because of an affected advisory and unhashed lock. Existing protected code remains untouched; upgrade/removal needs separate authority.**

**Integration mode:** `LINK_AS_DEPENDENCY`, research data reader/writer.

| # | Criterion | Evidence and rule |
|---:|---|---|
| 1 | Provenance | Declared pin `pyarrow==23.0.0` in the backtest lock. Upstream tag `apache-arrow-23.0.0` resolves to annotated object `b503a105d1d61445280bdbdb1a643ca8b31d0674`, commit `eafe3a9e620cf94683dee2347f370c35156dc965`. PyPI sdist SHA-256 `180e3150e7edfcd182d3d9afba72f7cf19839a497cc76555a8dce998a8f67615`; upload 2026-01-18. Historical acquisition path is not recorded. |
| 2 | Licence | Apache-2.0; full canonical text/hash recorded in entry 0003. Linking/distribution must include the licence, preserve applicable notices and changed-file notices, and inspect the exact distribution NOTICE. The package-specific NOTICE capture is missing, so the criterion is incomplete. |
| 3 | Dependency/supply chain | `requirements-lock.txt` pins 14 environment packages but has **zero hashes** and does not encode a dependency graph. PyPI reports no mandatory Python dependency for 23.0.0, but the native wheel remains an artifact requiring a hash. Bridge supply-chain floor fails. |
| 4 | Vulnerabilities | **2026-08-24 OSV: affected.** `GHSA-rgxp-2hwp-jwgg` / `CVE-2026-25087` / `PYSEC-2026-113`: potential use-after-free reading IPC with pre-buffering; CVSS v3 vector `AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H`. OSV range is introduced 15.0.0, fixed 23.0.1; 23.0.0 is listed affected. Exposure is direct when this research dependency reads attacker-controlled/malformed Arrow IPC with pre-buffering; Parquet-only trusted local use narrows but does not erase parser/native-code risk. |
| 5 | Maintainer/activity | Arrow: 14 releases/12 months; current repo activity. Human maintainer count not established from automated release publishing. Median security closure time not public. GitHub community profile exposed no repository policy file; Apache's project security channel must be captured separately before acceptance. |
| 6 | Abandonment | Shared A, plus abandoned at a pin if a published HIGH advisory affecting the used parser path remains without an available fixed pin for 30 days. This pin is rejected now because a fixed release exists but is not adopted. |
| 7 | Update | Owner: protected backtest package Lead. Monthly until the advisory is resolved, then quarterly per U. A change is at least T0/T1 according to protected-surface classification and must round-trip real Parquet/IPC fixtures, run parity gates and prove RED/GREEN for this advisory path if used as closure evidence. |
| 8 | Incident | Shared I. Immediate policy action: block new installs and untrusted IPC ingestion at 23.0.0; notify Lead/owner. Do not self-upgrade this protected dependency. A separately authorized change may pin a fixed version after full validation. |
| 9 | Portability/export | Durable outputs remain Parquet plus schema/manifest; bounded recovery export is CSV/JSON. No Arrow in-memory object is the only copy. |
| 10 | Replacement/rollback | Replacement: DuckDB native Parquet reader for bounded queries, or the previous accepted PyArrow lock if safe. Switching cost medium/high. A PyArrow rollback has not been walked; current pin cannot count as a safe target while affected. |
| 11 | Evidence preservation | Shared E plus vulnerable fixtures (if lawfully available), advisory snapshot, exact bytes/hashes and format round trips. |
| 12 | Retirement/removal | Shared R. This rejection is not authority to edit protected requirements, uninstall anything or delete data. |

## Entry 0005 — QuantStats

**Brief status:** ADOPT with independent validation.

**Ledger disposition:** **REJECTED FOR IMPLEMENTATION until exact version/lock, financial RED/GREEN validation and rollback exist.**

**Integration mode:** `LINK_AS_DEPENDENCY`, research reporting only.

| # | Criterion | Evidence and rule |
|---:|---|---|
| 1 | Provenance | Canonical [ranaroussi/quantstats](https://github.com/ranaroussi/quantstats). Latest observed PyPI `0.0.81`, uploaded 2026-01-13, sdist SHA-256 `91f44895e4481167255384c2297193233255b427e3a09a3fa111a5ce77e9b44a`. No version/tag/commit/artifact or acquisition path is adopted. |
| 2 | Licence | PyPI/upstream declare Apache-2.0. No exact adopted-version licence/NOTICE capture. Linking obligations follow entry 0003. Until exact distribution texts are captured it **requires a documented licensing review before adoption in this integration mode**. |
| 3 | Dependency/supply chain | No lock. PyPI 0.0.81 declares 8 runtime dependencies (`matplotlib`, `numpy`, `pandas`, `python-dateutil`, `scipy`, `seaborn`, `tabulate`, `yfinance`) plus optional Plotly; complete closure/hashes unknown. This is a substantial supply-chain cost and gate failure. |
| 4 | Vulnerabilities | 2026-08-24: no exact selected version, so no acceptable version review. Selected package and full transitive lock must be batch-queried in OSV. Network-fetch features such as yfinance must be excluded or separately authorized. |
| 5 | Maintainer/activity | 3 releases/12 months; one human release publisher (single-maintainer proxy, named money-adjacent calculation risk); repo pushed 2026-07-20. Median security closure time not public; no repository security-policy file exposed. |
| 6 | Abandonment | Shared A with stricter 180-day no human merge/release activity because financial calculations are involved, or any two independently verified material metric defects open for 90 days. |
| 7 | Update | Owner: WP-V3-11/reporting Lead. Quarterly per U. Sharpe, Sortino and Calmar must be independently compared on identical real artifacts; each new regression test must show RED against a deliberate metric mutation and GREEN with accepted behaviour. |
| 8 | Incident | Disable QuantStats rendering/calculation and use the repository's independently verified calculations. Preserve reports; never wait for upstream or allow a metric to influence promotion while disputed. |
| 9 | Portability/export | Inputs/outputs are preserved as returns/trades in CSV/Parquet/JSON and static HTML. No yfinance cache or QuantStats object is canonical. |
| 10 | Replacement/rollback | Replacement: existing NumPy/pandas metric implementation plus static templates. Switching cost medium. Rollback removes the pinned reporting layer and regenerates the same report from preserved inputs; not walked. |
| 11 | Evidence preservation | Shared E plus identical input series, parameter conventions, independent outputs, mismatch decisions and rendered reports. |
| 12 | Retirement/removal | Shared R; failed metrics and rejected reports remain evidence. |

## Entry 0006 — vectorbt open edition

**Brief status:** KEEP as enrichment only, not primary engine.

**Ledger disposition:** **HOLD EXISTING OPTIONAL IMPORT; REJECT NEW/EXPANDED USE until version, licence and hash lock are resolved.** Existing `03_QUANTLENS/tools/vbt_enrichment.py` remains untouched.

**Integration mode:** `LINK_AS_DEPENDENCY`, optional research enrichment only.

| # | Criterion | Evidence and rule |
|---:|---|---|
| 1 | Provenance | Canonical candidate [polakowo/vectorbt](https://github.com/polakowo/vectorbt); repo contains an optional import but no dependency manifest pin. PyPI latest observed `1.1.0`, uploaded 2026-07-05, sdist SHA-256 `67a3b41466234485af70c18d201da105f1ebb2c1d1fac079db20059e45ddc73b`. No adopted version/tag/commit/artifact/acquisition path is recorded. |
| 2 | Licence | The brief says Apache-2.0, but GitHub API returned `NOASSERTION` and PyPI did not expose a licence expression in the checked metadata. Therefore it **requires a documented licensing review before adoption in this integration mode**. No legal conclusion is made. |
| 3 | Dependency/supply chain | No lock. PyPI 1.1.0 declares 17 base runtime dependencies and many extras, including an exact optional Rust component. Complete closure/hashes unknown. Gate fails. |
| 4 | Vulnerabilities | 2026-08-24: no exact selected version; review cannot be claimed. Query exact package plus all selected extras in OSV and review native/Rust artifacts when applicable. |
| 5 | Maintainer/activity | 4 releases/12 months; one human release publisher (single-maintainer proxy); pushed 2026-08-02. Median security closure time unknown. Security-policy query was attempted but source became unreachable tonight due GitHub API 403/rate limit. |
| 6 | Abandonment | Shared A with stricter 180-day no human activity, or loss of a compatible release for the repository's Python/NumPy/pandas line for two consecutive quarterly reviews. |
| 7 | Update | Owner: QuantLens enrichment Lead. Quarterly per U. It remains optional; compare enrichment results to pure NumPy/pandas functions on real artifacts, with no fill/parity/primary-engine claim. |
| 8 | Incident | Disable the optional import (`_VBT_AVAILABLE` false path) and keep pure NumPy/pandas enrichment. No strategy/parity logic changes are implied. |
| 9 | Portability/export | Inputs/outputs are arrays/data frames serialized to JSON/CSV/Parquet; no portfolio object is canonical. Pure fallback must reproduce accepted fields. |
| 10 | Replacement/rollback | Replacement already exists: pure NumPy/pandas helpers in `vbt_enrichment.py`. Switching cost low. A pinned install/uninstall rollback has not been walked because no pin exists. |
| 11 | Evidence preservation | Shared E plus comparison fixtures, warnings that vectorbt is approximation, metric outputs and dependency-extras selection. |
| 12 | Retirement/removal | Shared R. Optional-import code or POC evidence may not be removed by this rejection. |

## Entry 0007 — hyperliquid-python-sdk 0.24.0

**Brief status:** KEEP — existing adapter dependency.

**Ledger disposition:** **HOLD AT EXISTING PIN.** This entry records, but does not authorize, the already pinned state. No update/expansion is authorized.

**Integration mode:** `LINK_AS_DEPENDENCY` behind the existing project adapter; money-adjacent/broker surface.

| # | Criterion | Evidence and rule |
|---:|---|---|
| 1 | Provenance | Canonical [hyperliquid-dex/hyperliquid-python-sdk](https://github.com/hyperliquid-dex/hyperliquid-python-sdk); lightweight tag `0.24.0` resolves to commit `2fdb18f9517675ea03695a0962bd19eece9c83f0`. Obtained through PyPI via Bridge input/lock; PyPI sdist SHA-256 `b3fba7c53f4faee41578df4ee19471393866a4a188e38d1fd05a0217b7a74868`; locked wheel/sdist hashes are at lock line 601. |
| 2 | Licence | MIT. Exact 0.24.0 wheel `hyperliquid_python_sdk-0.24.0-py3-none-any.whl` hash `f472dd4f6d8ef0e66182c7627276400462c86fbc0929eb5b63feda3ae45605f6`; embedded `LICENSE.md` full-text bytes were reviewed, SHA-256 `ea5593116c0da7de3e5845941c8ce7f2c0692ee4671f7b3e3aa98a88726b913c`, copyright Hyperliquid Labs Pte. Ltd. Preserve notice/text in copies/substantial portions. |
| 3 | Dependency/supply chain | Bridge lock Annex A: 56 exact packages/1,345 hashes, including five declared SDK dependencies (`eth-utils`, `eth-account`, `websocket-client`, `requests`, `msgpack`) and their closure. No package in the lock was flagged by the 2026-08-24 OSV batch. Cost: 55 other packages in the unified environment; any unmaintained member requires a new status entry. |
| 4 | Vulnerabilities | 2026-08-24 OSV exact `hyperliquid-python-sdk==0.24.0`: zero advisories; full Bridge lock batch: zero affected packages. Named source/date recorded; this is not proof of safety. Exposure is highest because SDK messages cross the broker/exchange adapter. |
| 5 | Maintainer/activity | 7 releases/12 months; one human release publisher (`traderben`) — explicit single-maintainer proxy risk on a money-adjacent surface; last push/release 2026-06-04. Median security closure time not public; no repository security-policy file exposed. |
| 6 | Abandonment | Shared A with stricter 90 days without human commit/release **and** no response to a reproducible adapter defect for 30 days; or official API incompatibility with the pinned SDK across two consecutive venue-version notices. |
| 7 | Update | Owner: Bridge dependency steward/Lead. Monthly plus events per U. Any bump is protected/T0 unless Gate 1 proves otherwise; replay real signed/unsigned fixtures without credentials, run adapter/reconciliation tests and D026 RED/GREEN for defect claims. |
| 8 | Incident | Shared I. First keep the Bridge disarmed/disable the affected adapter or pin the known-safe prior lock under operator authorization. Never “test” on an account, testnet or live venue from this policy. |
| 9 | Portability/export | SDK holds no canonical state. Requests/responses needed for evidence are redacted and stored in open JSON; position truth remains venue plus project ledger, not SDK objects. |
| 10 | Replacement/rollback | Replacement: a separately audited direct REST/WebSocket client behind the same adapter contract, or a prior safe SDK lock. Switching cost high. Rollback path is restore prior git lock and reinstall with hashes in an isolated environment; package-specific rollback not walked in this lane. |
| 11 | Evidence preservation | Shared E plus redacted protocol fixtures, adapter results, venue API version, lock and reconciliation evidence. Never preserve credentials. |
| 12 | Retirement/removal | Shared R. Adapter or SDK removal is protected work and separately owner-authorized. |

## Entry 0008 — FastAPI 0.140.0

**Brief status:** KEEP.

**Ledger disposition:** **HOLD AT EXISTING PIN.** No update/expansion authorized.

**Integration mode:** `LINK_AS_DEPENDENCY`, Bridge HTTP/WebSocket application framework.

| # | Criterion | Evidence and rule |
|---:|---|---|
| 1 | Provenance | Canonical [fastapi/fastapi](https://github.com/fastapi/fastapi); tag `0.140.0` resolves to commit `255b912928904e3ba5980425a54d6837c8bd1a1c`. PyPI sdist SHA-256 `f338951b82fd74ca8f843163aec43ea1a1ce84d515415a50fa98fa25572a5544`; obtained through Bridge input/lock; two artifact hashes at line 523. |
| 2 | Licence | MIT. Exact wheel hash `e951c0a0d9540bf5d9a2a9e078fd415da2ab7e312d435139e7d9e2e7fe9f0b23`; embedded full `LICENSE` reviewed, SHA-256 `4ec89ffc81485b97fec584b2d4a961032eeffe834453894fd9c1274906cc744e`, copyright Sebastián Ramírez. Preserve notice/text. |
| 3 | Dependency/supply chain | Annex A's complete Bridge environment: 56 packages/1,345 hashes. Direct base path uses Starlette, Pydantic, typing extensions/inspection and annotated-doc; unified lock is the actual closure and cost. No affected package in 2026-08-24 OSV batch. |
| 4 | Vulnerabilities | 2026-08-24 OSV exact 0.140.0: zero advisories; full lock batch zero. Exposure: HTTP/WebSocket parsing and routing on the Bridge surface. |
| 5 | Maintainer/activity | 93 releases/12 months; one human release publisher plus automation (single-maintainer proxy risk); pushed 2026-08-19. Median security closure time not public; no repository security-policy file exposed. |
| 6 | Abandonment | Shared A, plus abandoned if no release compatible with the locked Starlette/Pydantic line exists for 180 days after either supported dependency publishes a security fix required by this surface. |
| 7 | Update | Owner: Bridge dependency steward/Lead. Monthly plus events per U. Protected/T0 unless proven otherwise; run complete Bridge API/WebSocket/auth/safe-state tests and a real hash-locked install. |
| 8 | Incident | Shared I. First stop external access/new launches or pin a known-safe prior application lock under the existing safe operational procedure; do not improvise runtime edits. |
| 9 | Portability/export | FastAPI owns no data. OpenAPI/JSON/WebSocket schemas and project state remain readable without it; preserve schema snapshots before changes. |
| 10 | Replacement/rollback | Replacement: Starlette behind the same versioned API contract. Switching cost high. The remove/reinstall rollback to the same prior pinned state is walked in `ROLLBACK_WALK_EVIDENCE.md`. |
| 11 | Evidence preservation | Shared E plus OpenAPI snapshot, request/response fixtures, route inventory and rollback output. |
| 12 | Retirement/removal | Shared R; framework removal is protected runtime work requiring separate authority. |

## Entry 0009 — Uvicorn 0.51.0

**Brief status:** KEEP.

**Ledger disposition:** **HOLD AT EXISTING PIN.** No update/expansion authorized.

**Integration mode:** `LINK_AS_DEPENDENCY`, ASGI server process library in the Bridge environment.

| # | Criterion | Evidence and rule |
|---:|---|---|
| 1 | Provenance | Canonical [encode/uvicorn](https://github.com/encode/uvicorn), now redirected to Kludex organization; tag `0.51.0` resolves to commit `e4d0b05eb8c6459b7ba27ad13a2c2f4f8d4ece50`. PyPI sdist SHA-256 `f6f4b69b657c312f516dd2d268ab9ae6f254b11e4bac504f37b2ab58b24dd0b0`; obtained via Bridge `uvicorn[standard]`; two hashes at lock line 1234. |
| 2 | Licence | BSD-3-Clause. Exact wheel hash `5d38af6cd620f2ae3849fb44fd4879e0890aa1febe8d47eb355fb45d93fe6a5b`; embedded full `LICENSE.md` reviewed, SHA-256 `efe1acf3e62fb99c288b0ec73e5a773b7268ef4320fe757ea994214e4b63c371`. Retain copyright/conditions/disclaimer in source and binary docs; no endorsement. |
| 3 | Dependency/supply chain | Annex A: 56 exact packages/1,345 hashes. Standard extra adds `httptools`, `python-dotenv`, `pyyaml`, `uvloop`, `watchfiles`, `websockets`; base adds `click`, `h11`. Unified lock is the full closure/cost. |
| 4 | Vulnerabilities | 2026-08-24 OSV exact 0.51.0 and full Bridge lock: zero affected packages. Exposure includes network protocol parsing and process lifecycle. |
| 5 | Maintainer/activity | 24 releases/12 months; one human release publisher (`Kludex`) — single-maintainer proxy risk; pushed 2026-08-24. Median security closure time not public; no repository security-policy file exposed. |
| 6 | Abandonment | Shared A, plus abandoned if no compatible server release/mitigation exists within 30 days of an affected HIGH protocol-parsing advisory. |
| 7 | Update | Owner: Bridge dependency steward/Lead. Monthly per U. Protected/T0 unless proven otherwise; run bind-address, proxy-header, WebSocket, shutdown/restart, worker and safe-state tests in isolation. |
| 8 | Incident | Shared I. Stop exposure/new launches or pin prior safe server lock; preserve logs and config. No host contact from this entry. |
| 9 | Portability/export | Server owns no canonical data. ASGI application contract, logs and configuration remain open text/JSON. |
| 10 | Replacement/rollback | Replacement: Hypercorn under the same ASGI contract. Switching cost medium/high. Rollback restores prior full hash lock and server configuration in an isolated environment; not walked for Uvicorn specifically. |
| 11 | Evidence preservation | Shared E plus startup/shutdown logs, bind/proxy config, protocol fixtures and ASGI compatibility results. |
| 12 | Retirement/removal | Shared R; process/runtime removal requires separate protected authorization. |

## Entry 0010 — Pydantic 2.13.4

**Brief status:** KEEP.

**Ledger disposition:** **HOLD AT EXISTING PIN.** No update/expansion authorized.

**Integration mode:** `LINK_AS_DEPENDENCY`, Bridge validation/serialization library.

| # | Criterion | Evidence and rule |
|---:|---|---|
| 1 | Provenance | Canonical [pydantic/pydantic](https://github.com/pydantic/pydantic); annotated tag object `07b73712023f052c7c008c4a9c5121b4894e44ec`, commit `cf67d4b3193c3fe43ede18612ed62785eee11382`. PyPI sdist SHA-256 `c40756b57adaa8b1efeeced5c196f3f3b7c435f90e84ea7f443901bec8099ef6`; obtained through Bridge input `pydantic>=2`, resolved exact with two hashes at line 846. |
| 2 | Licence | MIT. Exact wheel hash `45a282cde31d808236fd7ea9d919b128653c8b38b393d1c4ab335c62924d9aba`; embedded full `LICENSE` reviewed, SHA-256 `a9e186f3ca16b5eef84318e7a701721351a00cb7b8ae3a4394b67b49e3529ef3`, Pydantic Services Inc./contributors. Preserve notice/text. |
| 3 | Dependency/supply chain | Annex A: 56 exact packages/1,345 hashes. Direct closure includes exact `pydantic-core==2.46.4`, annotated-types, typing-extensions and typing-inspection; native core artifacts are hash-pinned. |
| 4 | Vulnerabilities | 2026-08-24 OSV exact 2.13.4 and full Bridge lock: zero affected packages. Exposure includes validation at every external/config boundary; unsafe coercion or parser defects can affect runtime decisions. |
| 5 | Maintainer/activity | 22 releases/12 months; one human release publisher observed (single-publisher proxy, although upstream organization is broader); pushed 2026-08-24. Median security closure time not public; no repository security-policy file exposed. |
| 6 | Abandonment | Shared A, plus abandoned at a major line if it lacks fixes for the repository's supported Python version for 180 days after upstream ends that line. |
| 7 | Update | Owner: Bridge dependency steward/Lead. Monthly per U. Protected/T0 unless proven otherwise; run schema snapshots, strict/coercion boundaries, persisted-state compatibility and complete Bridge tests; D026 for claimed validation defects. |
| 8 | Incident | Shared I. Pin prior safe validation lock or disable the affected input path while keeping the Bridge safe/disarmed; never loosen validation as a workaround. |
| 9 | Portability/export | Models serialize to versioned JSON/open schemas; no pickle or Pydantic-only object is canonical. Preserve schema and raw input. |
| 10 | Replacement/rollback | Replacement: stdlib dataclasses plus explicit validators/JSON Schema. Switching cost high. Rollback restores prior model/schema and hash lock in isolation; not walked specifically. |
| 11 | Evidence preservation | Shared E plus JSON Schema snapshots, boundary fixtures, persisted samples and migration/rollback results. |
| 12 | Retirement/removal | Shared R; validation-library removal is protected runtime/migration work. |

## Entry 0011 — Tailscale client and hosted control service

**Brief status:** ADOPT for private access.

**Ledger disposition:** **REJECTED FOR IMPLEMENTATION in this package until exact client version/hash, hosted-service terms, account/export, outage behaviour and T0 network package are separately accepted.** No install/account/contact occurred.

**Integration mode:** `SEPARATE_LOCAL_PROCESS` for the client plus `FILE_OR_API_INTEROP` with the hosted control service; network/host surface.

| # | Criterion | Evidence and rule |
|---:|---|---|
| 1 | Provenance | Canonical client [tailscale/tailscale](https://github.com/tailscale/tailscale). Latest observed release `v1.102.3`, 2026-08-20, but no version/tag/commit/binary hash or acquisition path is adopted. Hosted service is separately sourced and no account was created. |
| 2 | Licence | GitHub reports BSD-3-Clause for the client; the hosted control service has separate terms. Exact client text/binary notices and service terms were not captured for an adopted version. It **requires a documented licensing review before adoption in this integration mode**. No categorical legal conclusion is made. |
| 3 | Dependency/supply chain | No client binary/container/package lock or signature/hash policy exists in this repo; hosted service dependencies are opaque. Gate fails. Any accepted client must use vendor-published integrity/signing evidence and an exact platform package. |
| 4 | Vulnerabilities | 2026-08-24: exact-version review impossible. Check Tailscale advisories/security bulletins and OS/package advisories for the selected client; include exposure as a privileged network daemon and control-plane dependency. Review attempted; exact source version not selected. |
| 5 | Maintainer/activity | 28 releases/12 months; 6 human release publishers observed; pushed 2026-08-24. Median security closure time not public. GitHub security-policy query attempted but source was unreachable tonight after HTTP 403/rate limit. Hosted-service operational ownership/SLA remains separately unknown. |
| 6 | Abandonment | Shared A with stricter conditions: no supported client security release for 90 days; control service unavailable for 24 consecutive hours without documented recovery; export/API for required ACL/device state removed; or hosted terms materially change without owner acceptance. |
| 7 | Update | Owner: separately authorized network/host Lead. Monthly plus events per U. Every client change is T0 and must be tested offline/on an authorized non-production fixture; this ledger authorizes no host or account action. |
| 8 | Incident | First revoke/disable the affected private-access path through an explicitly authorized operator procedure and fall back to the named access path; preserve device/ACL evidence. Do not expose a public listener as a workaround. |
| 9 | Portability/export | ACL/policy must live as reviewable text; device inventory/audit events export to JSON/CSV where service permits. Repository operation cannot depend on non-exportable hosted-only state. |
| 10 | Replacement/rollback | Replacement: existing SSH tunnel first, self-managed WireGuard only under separate T0 design. Switching cost medium/high. Rollback must remove/disable the client and prove private access through the previous authorized path without widening exposure; not walked and not permitted in this lane. |
| 11 | Evidence preservation | Shared E plus client package/signature, policy, device inventory, outage test and redacted access logs; never credentials or auth keys. |
| 12 | Retirement/removal | Shared R. Account/device/client cleanup requires exact, separately owner-authorized host/account actions; nothing is auto-removed. |

---

## Annex A — Bridge hash-locked transitive set

This is the full resolved environment referenced by entries 0007–0010. Every name/version below has one or more `--hash=sha256:` lines in the immutable lock identified above. This unified set overstates a single root's private closure but never understates the installed supply-chain cost.

`annotated-doc==0.0.4`, `annotated-types==0.8.0`, `anthropic==0.120.0`, `anyio==4.14.2`, `bitarray==3.9.2`, `certifi==2026.7.22`, `charset-normalizer==3.4.9`, `ckzg==2.1.8`, `click==8.4.2`, `cytoolz==1.1.0`, `distro==1.9.0`, `docstring-parser==0.18.0`, `eth-abi==5.2.0`, `eth-account==0.13.7`, `eth-hash==0.8.0`, `eth-keyfile==0.8.1`, `eth-keys==0.7.0`, `eth-rlp==2.2.0`, `eth-typing==6.0.0`, `eth-utils==5.3.1`, `fastapi==0.140.0`, `h11==0.16.0`, `hexbytes==1.3.1`, `httpcore==1.0.9`, `httptools==0.8.0`, `httpx==0.28.1`, `hyperliquid-python-sdk==0.24.0`, `idna==3.18`, `iniconfig==2.3.0`, `jiter==0.16.0`, `msgpack==1.2.1`, `packaging==26.2`, `parsimonious==0.10.0`, `pluggy==1.6.0`, `pycryptodome==3.23.0`, `pydantic==2.13.4`, `pydantic-core==2.46.4`, `pydantic-settings==2.14.2`, `pygments==2.20.0`, `pytest==9.1.1`, `python-dotenv==1.2.2`, `pyyaml==6.0.3`, `regex==2026.7.19`, `requests==2.34.2`, `rlp==4.1.0`, `sniffio==1.3.1`, `starlette==1.3.1`, `toolz==1.1.0`, `typing-extensions==4.16.0`, `typing-inspection==0.4.2`, `urllib3==2.7.0`, `uvicorn==0.51.0`, `uvloop==0.22.1`, `watchfiles==1.2.0`, `websocket-client==1.9.0`, `websockets==16.1.1`.

## Annex B — Licence-text capture index

The full text was read from the exact adopted wheel for existing Bridge packages; the immutable artifact hash and internal path make the captured text reproducible. Apache-2.0's full canonical text was read from the Apache Software Foundation URL and hashed. This index is evidence location, not legal advice.

| Component/version | Licence | Full-text carrier | Full-text SHA-256 |
|---|---|---|---|
| FastAPI 0.140.0 | MIT | wheel `e951…f0b23`, `fastapi-0.140.0.dist-info/licenses/LICENSE` | `4ec89ffc81485b97fec584b2d4a961032eeffe834453894fd9c1274906cc744e` |
| Uvicorn 0.51.0 | BSD-3-Clause | wheel `5d38…6a5b`, `uvicorn-0.51.0.dist-info/licenses/LICENSE.md` | `efe1acf3e62fb99c288b0ec73e5a773b7268ef4320fe757ea994214e4b63c371` |
| Pydantic 2.13.4 | MIT | wheel `45a2…9aba`, `pydantic-2.13.4.dist-info/licenses/LICENSE` | `a9e186f3ca16b5eef84318e7a701721351a00cb7b8ae3a4394b67b49e3529ef3` |
| hyperliquid-python-sdk 0.24.0 | MIT | wheel `f472…05f6`, `hyperliquid_python_sdk-0.24.0.dist-info/LICENSE.md` | `ea5593116c0da7de3e5845941c8ce7f2c0692ee4671f7b3e3aa98a88726b913c` |
| Apache-2.0 canonical | Apache-2.0 | `https://www.apache.org/licenses/LICENSE-2.0.txt`, read 2026-08-24 | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |

## Demonstration of supersession (non-component test data)

### Entry DEMO-0001 — fictional `example-grid` 1.0

**Status:** **SUPERSEDED by entry DEMO-0002 — retained, never edited away**.

This deliberately fictional record proves that an old trusted statement remains visible. It is not a dependency, adoption, licence conclusion or recommendation.

### Entry DEMO-0002 — fictional `example-grid` 1.1 status marker

**SUPERSEDES:** entry DEMO-0001.

Reason: demonstration-only version change. In a real entry this successor would repeat all twelve criteria with new evidence; the old bytes would remain.
