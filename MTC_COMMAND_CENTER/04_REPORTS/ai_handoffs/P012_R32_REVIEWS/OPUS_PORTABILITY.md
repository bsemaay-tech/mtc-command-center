# T0 EXECUTION REFRESH — claude-opus-5 xhigh, first-party Pro, R32 portability repair

## Identity personally measured
- `git -C C:/tmp/P0S32A rev-parse HEAD` → **7f22a4f17a458e843a45c162cbbc843a33d822ba** before **and** after all commands; `status --porcelain --untracked-files=no` empty both times. Parent (`HEAD^`) → **3e9f8038f2765ad8e89977fd60470974d88f65ed** ✓.
- `P0R32T/TASK.md` sha256 **3657cf24…1d72** ✓; `P0R32T/PACKET_MANIFEST.sha256` sha256 **627e3e56…43a4** ✓ — original packet bytes unchanged.
- All 24 manifest-listed `QA/` entries (incl. `run_d026.py` + sidecar fixtures) rehashed: **24 ok / 0 mismatch / 0 missing**.

## Delta actually verified (3e9f8038 → 7f22a4f1)
`git diff --stat` = **1 file, 1 insertion, 1 deletion**. Only hunk: `test_verify_bceg.py:2055`, removing `, dir=r"C:\tmp"` = **exactly 15 bytes**. `TEST_BEFORE.py` 152047 B → `TEST_AFTER.py` 152032 B (sha256 `1bd7b8d0…c7ef`), which is **byte-identical to the live source file**. Line-by-line compare of BEFORE/AFTER: 4074 lines both, **sole differing line 2055**. `REPAIR.patch` reproduces the actual git diff verbatim. No assertion, fixture, skip, or other file touched. Grep across all `mtc_v2/**/*.py` for `TemporaryDirectory|mkdtemp|NamedTemporaryFile(... dir=...)`: **no matches** — no hardcoded temp root remains.

## Commands 1–4 — personally executed here, raw
1. **exit 0** — `3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)]`; `C:\Python314\python.exe`; `mtc_v2.__path__ = ['C:\\tmp\\P0S32A\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2']` — frozen worktree, not canonical root.
2. **GREEN exit 0** — stdout `{"outcome":"PASS","output":"C:\\tmp\\P0R32O2\\d026_green.json"}`; summary `semantic_failures:9, control_passes:2, unexpected_blocks:0`; `fixture_bytes_unchanged:true`; `test_source_and_import_state_unchanged:true`.
3. **RED exit 1** (intentional) — stdout `{"outcome":"RED","output":"C:\\tmp\\P0R32O2\\d026_red.json"}`; identical 9/2/0. No fixture or source mutation.
4. **Full gate exit 0** — `contract_selftest_suite: ran=true, returncode=0, passed_count=495, failed_count=0, failing_test_ids=[]`; `claim_label=BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_ACCEPTED`; `acceptance_blockers=[]`; `expected_source_provenance: status=MATCH, method=INDEPENDENT_DERIVATION, implementation_base_sha=3eebdf54…, observed_build_sha=7f22a4f1…, expected_path_change_count=0`; `legacy_reproduction 17 scenarios / 34 surfaces / MATCH`; 10/10 probes `DETECTED`; 20 pre-existing `BLOCKED-DESIGN-UNENUMERATED` skips; `declared_field_validation` 4 refusals (report-only). Three outputs all initially absent. No timeout, no hang — the pre-repair 600 s failure mode is gone.

## Platform skip — honest statement
`verify_bceg.py:4867-4877` parses only `N passed` / `N failed`; the receipt has **no skipped/error field**. So the one conditional platform skip, `test_verify_bceg.py:1986` `pytest.skip("symlink creation unavailable")`, cannot be read out of `full_gate.json`, and I did not run pytest outside the four authorized commands. Whether it fired in my elevated run is **NOT VERIFIED**. Pre-existing, unchanged by this delta, and `returncode != 0` is still enforced (`verify_bceg.py:5037`), so this hides no failure. Not a new finding; no skip/filter/monkeypatch added.

## Preserved, not re-audited
All three prior NITs (aggregate pinned only by test literal `test_economic_records.py:59-70`; reseal-31 wording `implementation_anchor.json:225`; non-self-discriminating RED/GREEN asserts) stand unchanged. Prior NOT VERIFIED set retained in full: Section 16 semantics and eight identities, 19+40 re-derivations, Gemini 3.8 A5 report contents (bytes only) and Item-1 nit/ratification, C31 capture truthfulness, per-member manifest re-measurement, end-to-end mutant acceptance (D026 in-memory `verified.digest` neutralization — production digest fence exercised only unattributed inside the 495), plus Sol/Lead/Gemini boundaries, CI and production facts. Retained: 27 production risks, 5 integration obligations, 10 accepted Section 19 closure-evidence items (distinct from those obligations), receipt-29 semantic redo before FINAL production only, HIST0037 deferral, Sol R5 BLOCK dissent.

Several Bash calls were **denied** (`ls` with pipe, chained `git …; …`, `git log/rev-list`). Denials preserved; same read-only facts obtained via authorized `rev-parse`/`status`/`diff` and Read/Grep/Python. No bypass, no writes to source or packet, no permission/model/account change, no network, no delegation.

## Verdict — **PASS**
Scoped to the 15-byte portability repair 3e9f8038 → 7f22a4f1, executed on this identity today. Not P012 acceptance, not integration or production authorization, waives no auditor, no new seal, validates no historical overrule.