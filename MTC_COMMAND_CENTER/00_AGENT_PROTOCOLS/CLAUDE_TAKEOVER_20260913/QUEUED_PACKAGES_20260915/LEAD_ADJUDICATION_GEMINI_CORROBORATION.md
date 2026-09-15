# LEAD_ADJUDICATION — QUEUED_PKGS_GEMINI (gemini-3.8-flash-high T2 corroboration of the P0-27 / P0-28 / P0-26 documentary packets) — 2026-09-15 08:50Z

**Formal outcome: attempt 1 VOIDED by the wrapper (`launch.exit` exit=1; CLI envelope `status: ERROR`, `error: "API error (attempt 1): UNAVAILABLE (code 503): No capacity available for model gemini-3.8-flash-high on the server"`, 858.5 s), chain outcome FAIL. The complete report WAS produced (recovered from `%TEMP%\gemini_wrapper_failures\20260915T084311Z_2564.stdout.jsonl`: 33 453 chars, JSON verdict + `GEMINI_READ_ONLY_OK` sentinel; sha256 `25a353a9…`; `RECOVERED_ENVELOPE.json`, `RECOVERED_RESPONSE_UTF8.md`; usage input 654 631 / output 37 580 / thinking 22 436). Kept as SUPPLEMENTAL; a counted re-run is queued for the next quiet window (the packets are owner decision inputs, not acceptance objects — the supplemental read is used today with that label).**

## Recovered verdict: PASS-WITH-NITS (4 NITs) — all accepted and applied
| # | Gemini finding | Lead disposition |
|---|---|---|
| F-01 | the reconciliation credited `CI_POLICY.md` with two required contexts; on 2026-08-25 it recorded one and said `pine-alert-guard` was not yet required | CORRECT — reworded: the ruleset query today shows two; the second was added after WP-P0-23 delivered (progressive policy as written) |
| F-02 | R1-R18 omitted the 4th acceptance-gate clause (P0-10/P0-23 must not claim continuous protection before acceptance) and the P0-26 paging channel from plan lines 593/599 | CORRECT — rows R19 (holds today; re-grep at the acceptance step) and R20 (dependent on P0-26) added |
| F-03 | phrasing suggested a T2 corroboration suffices for a T1 acceptance | CORRECT — reworded: acceptance is a T1 call on the flagship verdict already recorded for the workflow files (2026-08-25) plus the evidence; no acceptance claimed |
| F-04 | option B2 (GitHub Actions `schedule:`) conflicts with P0-27's non-goal | CORRECT — B2 marked NOT available without a plan amendment |
`p027_gate_satisfied_except`: the e-mail confirmation (since received from the owner, "yes"), the formal owner acceptance of the day-one scope (the Lead's recommendation, still the owner's act), and the R19 re-check — all recorded in the reconciliation.

Additional Lead correction found on re-read (not raised by Gemini): the P0-26 packet §0 said the watchdog still carried the 900-second default and the single-shot dedupe — wrong; `53d33dbc` already fixed the watchdog half with its three tests. Corrected in the packet.

Recorded by Claude Opus 5 Lead (743291).

---
# Counted re-run — 2026-09-15 10:25Z

**Chain `gemini_retry_chain_v2.py QUEUED_PKGS_GEMINI` (packet re-staged 09:48:48Z, 23 files, prompt annotated for the re-run):**
| Attempt | Window | Outcome |
|---|---|---|
| 2 | 09:51:43Z – 10:03:43Z (725 s) | **VOIDED by the wrapper guard**: `Filesystem changes were observed during the Gemini invocation … Events: Changed:_gemini_packets_20260913\QUEUED_PKGS_20260915` — a single directory-level `Changed` event on the packet directory, no `Created`/`Deleted`/`Renamed`, and afterwards no file or directory under the packet carries an mtime later than the 09:48:48Z staging (dir mtime unchanged). Cause NOT identified (the Lead's shell cwd was outside every worktree; no Lead write touched `C:/LAB/…`). Kept as `FAILED_ATTEMPTS/attempt2/`; no report was produced. |
| 3 | 10:04:39Z – 10:17:18Z (758 s; `elapsed_seconds` 763.6) | **COUNTED**: `launch.exit` `exit=0 actual_exit=0`; envelope `status: SUCCESS`, conversation `b1d5d10f-7e54-4226-b870-56954b63a3db`; `GEMINI_READ_ONLY_OK` sentinel present; usage input 644 073 / output 46 785 / thinking 32 796; `REVIEW.log` sha256 `d64affd8…`; response 29 797 chars sha256 `0f7996a9…` (`RESPONSE_UTF8.md`); `agy_helpers_after` 0, candidate HEAD/dirty unchanged. |

**Native-read audit (`native_read_audit.py`, `NATIVE_READ_AUDIT.json`):** 25 native reads, 0 outside the packet, 0 failures; every one of the 22 REQUIRED files plus `PACKET_SHA256SUMS.txt` read COMPLETE (the 176-line `P027_CI_POLICY.md` in two ranges 1-150 / 151-177, as instructed); one extra in-packet read (`sources/P026_opsa_config.example.json`). `required_scope_unread: []` in the verdict matches the audit.

## Counted verdict: PASS-WITH-NITS (3 NITs, 0 REQUIRED) — `evidence_class SUPPLEMENTAL_UNEXECUTED`
R1-R20: AGREE on every row (R5 "AGREE with NIT"). Red-demo chain corroborated from the packet copies (failed log names step + probe; RED JSON BLOCKED/FAILURE; GREEN JSON CLEAN/SUCCESS; PR closed unmerged). `p027_gate_satisfied_except`: (1) documentary proof of the e-mail (owner-side), (2) the formal T1 acceptance of the day-one scope, (3) the R19 re-check at acceptance — same three residuals the reconciliation lists. P0-28 and P0-26 packets: faithful reuse, exact owner questions, no action started, options bounded, exclusions respected. Cross-cutting: seven acceptance/readiness sentences quoted, all judged fenced.

| # | Gemini finding (citation grepped by the Lead) | Lead disposition |
|---|---|---|
| F-01 NIT | `P027_REQUIREMENT_RECONCILIATION_20260915.md:18` — R5 labelled "IMPLEMENTED + VERIFIED" although master was never red, the probe ran on a draft PR, and e-mail delivery is owner-side (`:54` NOT VERIFIED) | CORRECT — R5 relabelled "IMPLEMENTED; RED path PROBE-VERIFIED (draft PR #192, never on master); e-mail delivery OWNER-CONFIRMED only"; `:54` expanded. Applied 10:25Z in CT13 and the run root. |
| F-02 NIT | `RED_DEMO_EVIDENCE_20260915.md:18` — "Notification half CLOSED" rests on the chat "yes"; recommends an immutable artifact (headers / screenshot) | CORRECT — sentence amended: closed on the owner's word, artifact NOT on record. Capturing one means reading the owner's mailbox (the Gmail connector is attached to this session but has not been used); **OPEN pending an owner one-liner**. |
| F-03 NIT | `P026_DEPLOYMENT_AND_DRILL_DECISION_PACKET_20260915.md:7` — draft 1 is a pre-build snapshot; candidate `6ac9cfb7` exists since | CORRECT — status note added under the title (snapshot; candidate built; not reviewed/accepted; master unchanged). |

NOT VERIFIED (Gemini, kept): live GitHub state (JSON/log copies only), e-mail arrival, KVM2 facts, Hyperliquid volume (the P028 READ has since been executed — `P028_ELIGIBILITY_CAPTURE_20260915/`, outside this packet), candidate `6ac9cfb7` (separate corroboration later), a failing run of `pine-alert-guard` (WP-P0-23 scope).

Comparison with the voided attempt 1 (supplemental): attempt 1's four NITs (CI_POLICY wording, rows R19/R20, T1 wording, option B2) do not recur — the amendments held; attempt 3 raises three new, smaller NITs on labelling and evidence custody. Nothing in either attempt is REQUIRED. The three packets remain owner decision inputs, not acceptance objects; this corroboration is recorded as T2 SUPPLEMENTAL_UNEXECUTED for the P0-27 acceptance file.

Recorded by Claude Opus 5 Lead (743291).
