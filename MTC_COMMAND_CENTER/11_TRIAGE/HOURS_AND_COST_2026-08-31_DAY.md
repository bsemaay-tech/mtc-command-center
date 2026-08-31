# Hours and cost — 2026-08-31 day session

Verdict: **MEASURED WITH LIMITS**. All durations are filesystem-mtime proxy spans; overlapping lane spans are never summed (`C:\tmp\LANE_PROMPTS_20260828\LANE_W151_HOURS_FINAL.md:6-20`).

## Session span

| Start | Close proxy | Wall-clock envelope | Basis |
|---|---|---:|---|
| 2026-08-31 09:00:00.000 +03:00 | 2026-08-31 17:42:38.123 +03:00 | 522.635 min (8:42:38.123) | Start is the ledger's declared session start (`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:374`); close is the newest cited landing artifact, `C:\tmp\LANE_PROMPTS_20260828\W151_REPORT.md [metadata]`. |

This is a session envelope, not labor hours, model-active hours, or billable time. The ledger itself retracts minute-level prose timing and makes mtimes govern (`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:400`).

## Per-package wall-clock envelopes

Each row is `earliest cited start proxy → latest cited end proxy` inside the group. These envelopes overlap each other and must not be summed (`C:\tmp\LANE_PROMPTS_20260828\LANE_W151_HOURS_FINAL.md:10-12`; `C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:207`). Cancelled routes without an end proxy do not extend an envelope.

| Package/group | Earliest start | Latest end | Envelope min | Evidence |
|---|---:|---:|---:|---|
| P0-12 core / design / build | 09:12:06.411 | 17:29:26.292 | 497.331 | Morning start `W120`; latest completion `W150b` (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:13`; `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:419`; metadata below). |
| P0-13 | 09:12:38.273 | 13:28:34.674 | 255.940 | `G42` through DEAD `A10` (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:28`; `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:410,412`). |
| P0-14 | 09:12:41.754 | 13:28:33.872 | 255.869 | `G43` through DEAD `A11` (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:37`; `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:410,412`). |
| P0-21 | 09:12:32.675 | 14:35:58.372 | 323.428 | `W123` through `DS25` (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:45`; `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:416-417`). |
| P0-22 | 09:12:27.686 | 14:46:13.221 | 333.759 | `W122` through `G58` (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:52`; `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:416-417`). |
| P0-30 | 11:05:03.580 | 14:46:51.128 | 221.792 | `DS20` through `G59` (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:59`; `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:416-417`). |
| P0-31 M2 | 11:03:58.255 | 12:42:01.363 | 98.052 | `GM22` through `G54` (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:67`; `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:405-407`). |
| V2A-01 | 09:31:21.703 | 14:46:07.447 | 314.762 | `DS17` through `G57` (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:73`; `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:413-417`). |
| V2A-02 | 09:41:17.929 | 14:12:21.205 | 271.055 | `DS19` through `GM25`; A12 was cancelled with no end proxy (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:81`; `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:411-414`). |
| V2A-03 | 11:49:27.677 | 14:12:21.284 | 142.893 | `DS22` through `GM26`; A13 was cancelled with no end proxy (`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:402-405,411-414`). |
| OPEN-01 | 10:02:31.052 | 12:16:22.385 | 133.856 | `W133` through `W142` (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:89-90`; `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:404-405`). |
| OPEN-03 | 10:02:40.287 | 11:30:46.289 | 88.100 | `W134` through shared `W136` artifact (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:90,96`). |
| OPEN-05 | 10:02:48.898 | 10:27:35.021 | 24.769 | `W135` (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:102`). |
| OPEN-06 | 09:27:36.124 | 10:27:01.253 | 59.419 | `W126` through `A8` (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:108-111`). |
| OPEN-07 | 10:00:24.245 | 11:35:35.114 | 95.181 | `W132` through shared repaired object (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:117-119`). |
| Venue evidence bundle | 11:49:10.612 | 11:56:48.797 | 7.636 | `A9` (`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:402-404`; metadata below). |
| Session records / hours basis | 11:32:55.632 | 17:42:38.123 | 369.708 | `W139` through `W151` (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:131-132`; `C:\tmp\LANE_PROMPTS_20260828\W151_REPORT.md [metadata]`). |

## Full per-lane table

The final population is 80 rows: the carried 45-row morning population (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:203`) plus 35 distinct appended route rows from the requested afternoon inventory; A9 and W127 were already in the morning population and are refreshed rather than duplicated (`C:\tmp\LANE_PROMPTS_20260828\LANE_W151_HOURS_FINAL.md:7-12`). Times are local `+03:00` `LastWriteTime` values; every named start/end file is a metadata source (`path [metadata]`).

| Lane/route | Status | Start proxy | Selected end proxy | Span min | Family/account | Package/object | Ledger evidence |
|---|---|---|---|---:|---|---|---|
| W120 | LANDED | `LANE_W120_P012_FOLD_R4.md` 09:12:06.411 | `W120_FOLD_REPORT.md` 09:34:02.737 | 21.939 | Codex/free/xhigh | P0-12 design fold r4 | `N_TIMES.txt:376,383` |
| W121 | LANDED; shared artifact | `LANE_W121_P012_GATE2_PLAN.md` 09:12:22.745 | `P012_GATE2_PLAN_AND_PATHLIST_V1.md` 10:18:39.934 | 66.286 | Codex/secondary/high | P0-12 Gate-2 plan/path list | `N_TIMES.txt:376,379,386` |
| A4 | LANDED | `LANE_A4_ONEPAGER_AUDIT.md` 09:14:39.998 | `AUDIT_A4_ONEPAGER.md` 09:20:56.164 | 6.269 | Claude/account NOT VERIFIED | P0-12 owner one-pager | `N_TIMES.txt:377-378` |
| G46 | LANDED | `LANE_G46_P012_V13_DETECT.md` 09:28:32.868 | `DETECT_G46_P012_V13.md` 09:48:53.834 | 20.349 | Grok/N/A | P0-12 v1.3 re-verify | `N_TIMES.txt:384,390` |
| GM21 | LANDED after DEAD first attempt | `GM21_BRIEF_TEMPLATE.md` 09:29:00.955 | `DETECT_GM21_P012_V13.md` 10:03:16.518 | 34.259 | Gemini/account NOT VERIFIED | P0-12 v1.3 corroboration | `N_TIMES.txt:381,391` |
| DS18 | LANDED | `OC_P012_V13_REVIEW\TASK.md` 09:31:49.705 | `REVIEW_DS18_P012_V13.md` 09:39:28.060 | 7.639 | OpenCode/DeepSeek | P0-12 v1.3 review | `N_TIMES.txt:381-385` |
| W127 | DEAD initial Claude route | `LANE_W127_CONTRACT_TABLES.md` 12:36:36.931 | `W127_RUN.log` 13:15:15.280 (last log) | 38.639 | Claude/Pro | P0-12 contract tables | `N_TIMES.txt:408-412,417` |
| W129 | LANDED after relaunch | `LANE_W129_GATE2_REPAIR.md` 09:40:14.174 | `W129B_RUN.log` 10:20:14.635 | 40.008 | Codex/secondary→free | P0-12 Gate-2 repair v2 | `N_TIMES.txt:387,392-395` |
| A5 | LANDED | `LANE_A5_GATE2_AUDIT.md` 09:27:01.579 | `AUDIT_A5_GATE2_PLAN.md` 09:33:34.517 | 6.549 | Claude/account NOT VERIFIED | P0-12 Gate-2 audit | `N_TIMES.txt:380,386` |
| A7 | LANDED | `LANE_A7_GATE2_V2_RECHECK.md` 10:20:40.206 | `AUDIT_A7_GATE2_V2.md` 10:28:41.576 | 8.023 | Claude/account NOT VERIFIED | P0-12 Gate-2 v2 recheck | `N_TIMES.txt:394-395` |
| G42 | LANDED | `LANE_G42_P013_V13_CENSUS.md` 09:12:38.273 | `DETECT_G42_P013_V13.md` 09:24:34.734 | 11.941 | Grok/N/A | P0-13 v1.3 census | `N_TIMES.txt:376,379` |
| W124 | LANDED | `LANE_W124_P013_FOLD_V14.md` 09:27:17.760 | `W124_FOLD_REPORT.md` 09:37:08.257 | 9.842 | Codex/secondary | P0-13 v1.4 fold | `N_TIMES.txt:380,386` |
| G47 | LANDED | `LANE_G47_P013_V14_VERIFY.md` 09:40:19.917 | `DETECT_G47_P013_V14.md` 09:47:08.912 | 6.817 | Grok/N/A | P0-13 v1.4 verify | `N_TIMES.txt:387,393` |
| GM23 | LANDED | `launch_GM22_GM23.ps1` 11:03:58.255 | `DETECT_GM23_P013_V14.md` 11:06:38.871 | 2.677 | Gemini/account NOT VERIFIED | P0-13 v1.4 corroboration | `N_TIMES.txt:396-397` |
| G43 | LANDED | `LANE_G43_P014_V12_CENSUS.md` 09:12:41.754 | `DETECT_G43_P014_V12.md` 09:25:04.935 | 12.386 | Grok/N/A | P0-14 v1.2 census | `N_TIMES.txt:376,379` |
| W125 | LANDED after DEAD initial attempt | `LANE_W125_P014_FOLD_V13.md` 09:27:23.404 | `W125B_RUN.log` 09:47:24.236 | 20.014 | Codex/third→fourth | P0-14 v1.3 fold | `N_TIMES.txt:380,387,389` |
| G48 | LANDED | `LANE_G48_P014_V13_VERIFY.md` 09:48:12.937 | `DETECT_G48_P014_V13.md` 09:53:45.246 | 5.538 | Grok/N/A | P0-14 v1.3 verify | `N_TIMES.txt:393` |
| W123 | LANDED | `LANE_W123_P021_FOLD_V14.md` 09:12:32.675 | `W123_FOLD_REPORT.md` 09:17:12.414 | 4.662 | Codex/fourth/medium | P0-21 v1.4 fold | `N_TIMES.txt:376,379` |
| G45 | LANDED | `LANE_G45_P021_V14_VERIFY.md` 09:27:12.132 | `DETECT_G45_P021_V14.md` 09:33:51.247 | 6.652 | Grok/N/A | P0-21 v1.4 verify | `N_TIMES.txt:380,386` |
| W122 | LANDED | `LANE_W122_P022_FOLD_V15.md` 09:12:27.686 | `W122_FOLD_REPORT.md` 09:17:47.410 | 5.329 | Codex/third/medium | P0-22 v1.5 fold | `N_TIMES.txt:376,379` |
| G44 | LANDED | `LANE_G44_P022_V15_VERIFY.md` 09:27:06.487 | `DETECT_G44_P022_V15.md` 09:34:27.168 | 7.345 | Grok/N/A | P0-22 v1.5 verify | `N_TIMES.txt:380,386` |
| DS20 | LANDED | `OC_P030_CENSUS\TASK.md` 11:05:03.580 | `REVIEW_DS20_P030_V12.md` 11:16:10.500 | 11.115 | OpenCode/DeepSeek | P0-30 v1.2 census | `N_TIMES.txt:396,398-400` |
| W137 | LANDED | `LANE_W137_P030_FOLD_V13.md` 11:16:34.513 | `W137_FOLD_REPORT.md` 11:22:46.445 | 6.199 | Codex/secondary | P0-30 v1.3 fold | `N_TIMES.txt:398-399` |
| G52 | LANDED | `LANE_G52_P030_V13_VERIFY.md` 11:32:43.868 | `DETECT_G52_P030_V13.md` 11:39:07.379 | 6.392 | Grok/N/A | P0-30 v1.3 verify | `N_TIMES.txt:399-401` |
| GM22 | LANDED | `launch_GM22_GM23.ps1` 11:03:58.255 | `DETECT_GM22_P031M2_V12.md` 11:06:38.808 | 2.676 | Gemini/account NOT VERIFIED | P0-31 M2 v1.2 corroboration | `N_TIMES.txt:396-397` |
| DS17 | LANDED after two DEAD launch variants | `OC_V2A01_CENSUS\TASK.md` 09:31:21.703 | `REVIEW_DS17_V2A01_V12.md` 09:35:36.355 | 4.244 | OpenCode/DeepSeek | V2A-01 v1.2 census | `N_TIMES.txt:376,379-385` |
| W128 | LANDED | `LANE_W128_V2A01_FOLD_V13.md` 09:35:43.973 | `W128_FOLD_REPORT.md` 09:41:06.051 | 5.368 | Codex/free/medium | V2A-01 v1.3 fold | `N_TIMES.txt:385-386` |
| G49 | LANDED | `LANE_G49_V2A01_V13_VERIFY.md` 10:00:11.188 | `DETECT_G49_V2A01_V13.md` 10:06:58.112 | 6.782 | Grok/N/A | V2A-01 v1.3 verify | `N_TIMES.txt:392-393` |
| DS19 | LANDED | `OC_V2A02_CENSUS\TASK.md` 09:41:17.929 | `REVIEW_DS19_V2A02_V13.md` 10:00:05.654 | 18.795 | OpenCode/DeepSeek | V2A-02 v1.3 census | `N_TIMES.txt:388,392` |
| W131 | LANDED | `LANE_W131_V2A02_FOLD_V14.md` 10:02:18.376 | `W131_FOLD_REPORT.md` 10:11:15.359 | 8.950 | Codex/third | V2A-02 v1.4 fold | `N_TIMES.txt:392-393` |
| G50 | LANDED | `LANE_G50_V2A02_V14_VERIFY.md` 10:20:32.440 | `DETECT_G50_V2A02_V14.md` 10:26:52.287 | 6.331 | Grok/N/A | V2A-02 v1.4 verify | `N_TIMES.txt:394-395` |
| W133 | LANDED after variants; shared artifact | `LANE_W133_OPEN01_RECORD_DRAFT.md` 10:02:31.052 | `P012_OPEN01_INSTRUMENT_RECORD_V1.md` 11:27:50.441 | 85.323 | Codex/fourth→Claude | OPEN-01 instrument record | `N_TIMES.txt:392-396` |
| W136 | LANDED; two-object package | `LANE_W136_OPEN01_03_COMPLETE.md` 11:04:52.180 | `P012_OPEN03_FEE_TABLE_V1.md` 11:30:46.289 | 25.902 | Codex/free | OPEN-01 + OPEN-03 | `N_TIMES.txt:396-399` |
| W134 | LANDED after DEAD initial attempt; shared artifact | `LANE_W134_OPEN03_FEE_TABLE.md` 10:02:40.287 | `P012_OPEN03_FEE_TABLE_V1.md` 11:30:46.289 | 88.100 | Codex/free→third | OPEN-03 fee table | `N_TIMES.txt:394-396` |
| W135 | LANDED | `LANE_W135_OPEN05_FUNDING_RULES.md` 10:02:48.898 | `P012_OPEN05_FUNDING_RULES_V1.md` 10:27:35.021 | 24.769 | Codex/secondary | OPEN-05 funding | `N_TIMES.txt:394-395` |
| W126 | LANDED; shared artifact | `LANE_W126_OPEN06_DRAFT.md` 09:27:36.124 | `P012_OPEN06_RETAINED_RETIRED_PROPOSAL_V1.md` 10:10:23.800 | 42.795 | Codex/fourth | OPEN-06 proposal | `N_TIMES.txt:380,392-393` |
| A6 | LANDED | `LANE_A6_OPEN06_AUDIT.md` 09:41:06.606 | `AUDIT_A6_OPEN06.md` 09:46:53.918 | 5.789 | Claude/account NOT VERIFIED | OPEN-06 audit | `N_TIMES.txt:388,392` |
| W130 | LANDED | `LANE_W130_OPEN06_REPAIR.md` 10:02:10.536 | `W130_REPAIR_REPORT.md` 10:13:11.127 | 11.010 | Codex/secondary | OPEN-06 repair v2 | `N_TIMES.txt:392-393` |
| A8 | LANDED | `LANE_A8_OPEN06_V2_RECHECK.md` 10:20:47.007 | `AUDIT_A8_OPEN06_V2.md` 10:27:01.253 | 6.237 | Claude/account NOT VERIFIED | OPEN-06 v2 recheck | `N_TIMES.txt:394-395` |
| W132 | LANDED; shared artifact | `LANE_W132_OPEN07_BRIDGE_MAPPING.md` 10:00:24.245 | `P012_OPEN07_BRIDGE_MAPPING_V1.md` 11:35:35.114 | 95.181 | NOT VERIFIED | OPEN-07 bridge mapping | `N_TIMES.txt:393,396-401` |
| G51 | LANDED | `LANE_G51_OPEN07_VERIFY.md` 11:16:42.657 | `DETECT_G51_OPEN07.md` 11:25:09.093 | 8.441 | Grok/N/A | OPEN-07 verify | `N_TIMES.txt:398-399` |
| W138 | LANDED | `LANE_W138_OPEN07_REPAIR.md` 11:32:38.231 | `P012_OPEN07_BRIDGE_MAPPING_V1.md` 11:35:35.114 | 2.948 | Claude/account NOT VERIFIED | OPEN-07 repair | `N_TIMES.txt:399-401` |
| A9 | LANDED | `LANE_A9_VENUE_BUNDLE_AUDIT.md` 11:49:10.612 | `AUDIT_A9_VENUE_BUNDLE.md` 11:56:48.797 | 7.636 | Claude/account NOT VERIFIED | Venue evidence bundle | `N_TIMES.txt:402-404` |
| W139 | LANDED | `LANE_W139_LEAD_SELF_AUDIT.md` 11:32:55.632 | `AUDIT_W139_LEAD_MIDDAY.md` 11:46:50.830 | 13.920 | Codex/third/high | Midday self-audit | `N_TIMES.txt:399-401` |
| W140 | LANDED | `LANE_W140_MTIME_HOURS.md` 11:49:37.748 | `W140_MTIME_HOURS_TABLE.md` 12:03:40.291 | 14.042 | Codex/fourth/medium | Morning mtime table | `N_TIMES.txt:402-404` |
| W141 | LANDED | `LANE_W141_V2A03_FOLD_V13.md` 12:04:52.680 | `W141_FOLD_REPORT.md` 12:16:56.414 | 12.062 | Codex/free | V2A-03 v1.3 fold | `N_TIMES.txt:403-405` |
| W142 | LANDED; two-object package | `LANE_W142_OPEN01_MINNOTIONAL.md` 12:05:59.607 | `P012_OPEN01_INSTRUMENT_RECORD_V1.md` 12:16:22.385 | 10.380 | Claude/account NOT VERIFIED | OPEN-01 minimum notional | `N_TIMES.txt:404-405` |
| W143 | LANDED | `LANE_W143_P031M2_FOLD_V13.md` 12:17:53.540 | `P031M2_DESIGN_DRAFT_V1.md` 12:34:40.968 | 16.790 | Codex/secondary | P0-31 M2 v1.3 fold | `N_TIMES.txt:405-407` |
| W144 | LANDED | `LANE_W144_P012_MICROFOLD.md` 12:34:55.234 | `W144_FOLD_REPORT.md` 12:56:55.904 | 22.011 | Codex/free/xhigh | P0-12 v1.4 micro-fold | `N_TIMES.txt:406-408` |
| W145 | LANDED | `LANE_W145_BASELINE_DRIVER.md` 13:05:12.160 | `W145_DRIVER_REPORT.md` 13:36:53.895 | 31.696 | Codex/free | P0-12 baseline driver | `N_TIMES.txt:409-413` |
| W146 | LANDED | `LANE_W146.md` 14:12:21.351 | `W146_FOLD_REPORT.md` 14:33:19.379 | 20.967 | Codex/free | V2A-01 v1.4 fold | `N_TIMES.txt:413-416` |
| W147 | LANDED | `LANE_W147.md` 14:12:21.368 | `W147_FOLD_REPORT.md` 14:28:58.238 | 16.614 | Codex/secondary | P0-22 v1.6 fold | `N_TIMES.txt:413-416` |
| W148 | LANDED | `LANE_W148.md` 14:12:21.393 | `W148_FOLD_REPORT.md` 14:25:38.820 | 13.290 | Codex/third | P0-30 v1.4 fold | `N_TIMES.txt:413-416` |
| W149 | LANDED | `LANE_W149.md` 14:12:21.413 | `W149_FOLD_REPORT.md` 14:21:32.042 | 9.177 | Codex/fourth | P0-21 v1.5 fold | `N_TIMES.txt:413-416` |
| W150 | BLOCKED; fail-closed before run | `LANE_W150_BASELINE_RUN.md` 15:17:27.272 | `W150_BASELINE_REPORT.md` 15:23:13.089 | 5.764 | Codex/free | P0-12 baseline attempt | `N_TIMES.txt:418-419` |
| W151 | LANDED | `LANE_W151_HOURS_FINAL.md` 17:29:05.478 | `W151_REPORT.md` 17:42:38.123 | 13.544 | Codex/account NOT VERIFIED | Final hours/cost ledger | `LANE_W151_HOURS_FINAL.md:6-22`; metadata |
| G53 | LANDED | `LANE_G53_V2A03_V13_VERIFY.md` 12:17:59.417 | `DETECT_G53_V2A03_V13.md` 12:23:56.450 | 5.951 | Grok/N/A | V2A-03 v1.3 verify | `N_TIMES.txt:405-406` |
| G54 | LANDED | `LANE_G54_P031M2_V13_VERIFY.md` 12:35:24.476 | `DETECT_G54_P031M2_V13.md` 12:42:01.363 | 6.615 | Grok/N/A | P0-31 M2 v1.3 verify | `N_TIMES.txt:406-407` |
| G55 | LANDED | `LANE_G55_P012_V14_TERMINAL.md` 12:56:47.020 | `DETECT_G55_P012_V14.md` 13:04:00.929 | 7.232 | Grok/N/A | P0-12 terminal pass | `N_TIMES.txt:407-408` |
| G56 | LANDED | `LANE_G56_APPLICABILITY.md` 13:27:53.276 | `DETECT_G56_APPLICABILITY.md` 13:37:57.559 | 10.071 | Grok/N/A | P0-12 applicability | `N_TIMES.txt:410,413` |
| G57 | LANDED | `LANE_G57.md` 14:33:08.033 | `DETECT_G57_V2A01_V14.md` 14:46:07.447 | 12.990 | Grok/N/A | V2A-01 v1.4 verify | `N_TIMES.txt:416-417` |
| G58 | LANDED | `LANE_G58.md` 14:33:08.067 | `DETECT_G58_P022_V16.md` 14:46:13.221 | 13.086 | Grok/N/A | P0-22 v1.6 verify | `N_TIMES.txt:416-417` |
| G59 | LANDED | `LANE_G59.md` 14:33:08.087 | `DETECT_G59_P030_V14.md` 14:46:51.128 | 13.717 | Grok/N/A | P0-30 v1.4 verify | `N_TIMES.txt:416-417` |
| GM24 | LANDED | `launch_GM24.ps1` 12:56:55.036 | `DETECT_GM24_P012_V14.md` 13:04:38.020 | 7.716 | Gemini/account NOT VERIFIED | P0-12 terminal corroboration | `N_TIMES.txt:407-408` |
| GM25 | LANDED | `launch_GM25_GM26.ps1` 13:46:23.584 | `DETECT_GM25_V2A02_V14.md` 14:12:21.205 | 25.960 | Gemini/account NOT VERIFIED | V2A-02 corroboration | `N_TIMES.txt:411,413-414` |
| GM26 | LANDED | `launch_GM25_GM26.ps1` 13:46:23.584 | `DETECT_GM26_V2A03_V13.md` 14:12:21.284 | 25.962 | Gemini/account NOT VERIFIED | V2A-03 corroboration | `N_TIMES.txt:411,413-414` |
| DS21 | DEAD; silent no-output route | `OC_P031M2_CENSUS\TASK.md` 11:49:22.709 | `DS21_ERR.log` 11:50:18.168 (last log) | 0.924 | OpenCode/DeepSeek V4 Flash | P0-31 M2 census | `N_TIMES.txt:402-404` |
| DS21b | LANDED relaunch | `launch_DS21b.ps1` 12:04:45.042 | `REVIEW_DS21_P031M2_V12.md` 12:17:45.209 | 13.003 | OpenCode/GLM-5.3-Flash | P0-31 M2 census | `N_TIMES.txt:403-405` |
| DS22 | LANDED | `OC_V2A03_CENSUS\TASK.md` 11:49:27.677 | `REVIEW_DS22_V2A03_V12.md` 12:04:44.978 | 15.288 | OpenCode/DeepSeek V4 Flash | V2A-03 census | `N_TIMES.txt:402-404` |
| DS23 | LANDED; delayed transcription upper proxy | `OC_P021_CENSUS\TASK.md` 13:28:12.846 | `REVIEW_DS23_P021_V14.md` 14:12:21.330 | 44.141 | OpenCode/DeepSeek V4 Flash | P0-21 census | `N_TIMES.txt:410,413-414` |
| DS24 | DEAD; exit 1 | `OC_P022_CENSUS\TASK.md` 13:28:12.867 | `DS24_ERR.log` 13:28:30.736 (last log) | 0.298 | OpenCode/GLM-5.3-Flash | P0-22 census | `N_TIMES.txt:410,413` |
| DS25 | LANDED in run-log output | `OC_P021_V15_VERIFY\TASK.md` 14:33:08.161 | `DS25_RUN.log` 14:35:58.372 | 2.837 | OpenCode/DeepSeek V4 Flash | P0-21 v1.5 verify | `N_TIMES.txt:416-417` |
| A10 | DEAD; Claude Pro cap at launch | `LANE_A10_P013_V14.md` 13:27:53.246 | `A10_RUN.log` 13:28:34.674 (last log) | 0.690 | Claude/Pro | P0-13 census | `N_TIMES.txt:410,412` |
| A11 | DEAD; Claude Pro cap at launch | `LANE_A11_P014_V13.md` 13:27:53.257 | `A11_RUN.log` 13:28:33.872 (last log) | 0.677 | Claude/Pro | P0-14 census | `N_TIMES.txt:410,412` |
| A12 | CANCELLED before launch | `LANE_A12_V2A02_V14.md` 13:46:00.384 | — | — | Claude/Pro | V2A-02 census | `N_TIMES.txt:411-412` |
| A13 | CANCELLED before launch | `LANE_A13_V2A03_V13.md` 13:46:00.411 | — | — | Claude/Pro | V2A-03 census | `N_TIMES.txt:411-412` |
| W127b | DEAD launcher; no process | `LANE_W127B_TABLES_COMPLETE.md` 14:07:23.817 | `W127B_RUN.log` 14:07:32.082 (last log) | 0.138 | Claude/Max Opus | P0-12 contract tables | `N_TIMES.txt:412,417` |
| W127c | DEAD launcher; shared-spec upper proxy | `LANE_W127B_TABLES_COMPLETE.md` 14:07:23.817 | `W127C_RUN.log` 14:47:37.475 (last log) | 40.228 | Claude/Max Opus | P0-12 contract tables | `N_TIMES.txt:417` |
| W127d | LANDED relaunch | `launch_W127B.ps1` 14:48:43.703 | `W127_TABLES_REPORT.md` 15:16:31.963 | 27.804 | Claude/Max Opus | P0-12 contract tables | `N_TIMES.txt:417-418` |
| W150b | LANDED relaunch | `launch_W150B.ps1` 17:21:24.541 | `W150B_BASELINE_REPORT.md` 17:29:26.292 | 8.029 | Codex/secondary/high | P0-12 baseline run | `N_TIMES.txt:419`; filesystem metadata |

## Ambiguous proxies and all variant candidates

Morning ambiguity is carried from the measured basis (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:134-148`):

- W121: `W121_RUN.log` 09:22:03.463; shared object `P012_GATE2_PLAN_AND_PATHLIST_V1.md` 10:18:39.934 selected. Later W129 edits make this an upper proxy.
- W125: `W125_RUN.log` 09:28:21.160; `W125_FOLD_REPORT.md` 09:46:35.926; `W125B_RUN.log` 09:47:24.236 selected.
- W126: `W126_RUN.log` 09:38:15.199; shared object `P012_OPEN06_RETAINED_RETIRED_PROPOSAL_V1.md` 10:10:23.800 selected; later W130 edits make it an upper proxy.
- W129: `W129_RUN.log` 09:43:10.217; `W129_REPAIR_REPORT.md` 10:19:27.751; `W129B_RUN.log` 10:20:14.635 selected.
- W132: `W132_RUN.log` 10:05:41.027; shared object `P012_OPEN07_BRIDGE_MAPPING_V1.md` 11:35:35.114 selected; later W138 edits make it an upper proxy.
- W133: `W133_RUN.log` 10:17:45.805; `W133B_RUN.log` 10:21:16.608; `W133C_RUN.log` 10:57:42.796; shared object `P012_OPEN01_INSTRUMENT_RECORD_V1.md` 11:27:50.441 selected; later W136 edits make it an upper proxy.
- W134: `W134_RUN.log` 10:25:02.380; `W134B_RUN.log` 11:03:43.994; shared object `P012_OPEN03_FEE_TABLE_V1.md` 11:30:46.289 selected; later W136 edits make it an upper proxy.
- W136: object candidates `P012_OPEN01_INSTRUMENT_RECORD_V1.md` 11:27:50.441 and `P012_OPEN03_FEE_TABLE_V1.md` 11:30:46.289 selected; `W136_RUN.log` 11:32:07.440 is later but is not a landing artifact.
- DS17: initial `DS17_RUN/ERR/DONE` 09:13:12.240/09:13:12.615/09:13:13.269; B `DS17B_RUN/ERR/DONE` 09:28:12.483/09:28:12.418/09:28:13.629; C `TASK.md` 09:31:21.703, `DS17C_ERR/RUN/DONE` 09:31:47.331/09:34:21.942/09:34:22.479; `REVIEW_DS17_V2A01_V12.md` 09:35:36.355 selected.
- GM21: `GM21_BRIEF_TEMPLATE.md` 09:29:00.955; initial `RUN/ERR/DONE` 09:59:44.846/09:59:45.111/09:59:45.871; `launch_GM21.ps1` 10:01:40.182; B `ERR/RUN/DONE` 10:01:45.747/10:02:41.852/10:02:42.290; `DETECT_GM21_P012_V13.md` 10:03:16.518 selected.

Afternoon candidates, all from file metadata:

- A9: `AUDIT_A9_VENUE_BUNDLE.md` 11:56:48.797 selected; `A9_RUN.log` 11:56:57.707 excluded as a run log.
- W140: `W140_MTIME_HOURS_TABLE.md` 12:03:40.291 selected; `W140_RUN.log` 12:04:25.187 excluded as a run log.
- DS21: `DS21_RUN.log` 11:49:52.715, `DS21_ERR.log` 11:50:18.168 selected as last log, `DS21_DONE.txt` 11:57:13.088 excluded because the death rule says last **log**, not marker (`C:\tmp\LANE_PROMPTS_20260828\LANE_W151_HOURS_FINAL.md:10-12`). DS21b candidates: `DS21B_ERR.log` 12:06:02.688, `DS21B_RUN.log` 12:15:55.011, `DS21B_DONE.txt` 12:15:55.569, landing `REVIEW_DS21_P031M2_V12.md` 12:17:45.209 selected.
- W142: candidate JSON 12:11:31.805; primary record 12:16:22.385 selected; `W142_RUN.log` 12:16:47.989 excluded as a run log.
- W143: report 12:34:16.592; primary edited object 12:34:40.968 selected; `W143_RUN.log` 12:35:24.952 excluded.
- GM24: `GM24_RUN/DONE` 12:58:07.427/12:58:08.280; transcribed landing `DETECT_GM24_P012_V14.md` 13:04:38.020 selected. GM25/GM26 similarly select their later transcribed `DETECT_*` files at 14:12:21.205/14:12:21.284 over run/done markers at 14:10:23.769/14:10:24.448 and 14:11:31.559/14:11:31.982.
- DS23: `DS23_RUN.log` 13:39:31.672 and `DS23_DONE.txt` 13:39:32.598; transcribed `REVIEW_DS23_P021_V14.md` 14:12:21.330 selected, so 44.141 min is an upper proxy. DS24 selects last log `DS24_ERR.log` 13:28:30.736 over `DS24_RUN.log` 13:28:29.395; DS25 selects console landing `DS25_RUN.log` 14:35:58.372 over marker `DS25_DONE.txt` 14:35:59.343.
- W127: morning-captured spec candidate 09:35:17.937 (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:19`) and current rewritten spec 12:36:36.931; current mtime selected for the afternoon initial route. W127b uses `LANE_W127B_TABLES_COMPLETE.md` 14:07:23.817 → `W127B_RUN.log` 14:07:32.082. W127c has no distinct spec; shared 14:07:23.817 spec → `W127C_RUN.log` 14:47:37.475 is retained as an explicit upper proxy. W127d uses dedicated launcher 14:48:43.703 → landing report 15:16:31.963; later `W127D_RUN/DONE` 15:16:59.063/15:16:59.631 are excluded. The contract manifest's 15:24:59.870 mtime is excluded because the Lead later performed the anchor act (`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:419`).
- W150: landing report 15:23:13.089 selected over run log 15:23:32.632. W150b: launcher 17:21:24.541 → landing report 17:29:26.292 selected over run/done 17:30:06.528/17:30:06.829. `N_TIMES.txt` still says running, so filesystem metadata governs (`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:419`).
- W151: zero-byte progress log 17:29:11.854; completed `W151_REPORT.md` 17:42:38.123 selected. A12 and A13 have specs at 13:46:00.384/13:46:00.411 but no logs or landing artifacts because they were cancelled (`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:411-412`).

## Route and cost notes

Primary-family counts classify each final table row once; morning rows that combine variants remain combined, while the requested afternoon deaths/relaunches are separate route rows (`C:\tmp\LANE_PROMPTS_20260828\LANE_W151_HOURS_FINAL.md:9-12,17-20`).

| Primary route family | Final table rows | LANDED | DEAD | CANCELLED | BLOCKED | Cost treatment |
|---|---:|---:|---:|---:|---:|---|
| Codex | 29 | 28 | 0 | 0 | 1 | Fixed-price subscription usage fact; marginal lane cost not allocated. CodeBurn: see "Lead cost readings" section. |
| Claude | 16 | 9 | 5 | 2 | 0 | Fixed-price subscription usage fact; marginal lane cost not allocated. Banner: see "Lead cost readings" section. |
| Grok | 18 | 18 | 0 | 0 | 0 | Subscription usage fact; monetary allocation: see "Lead cost readings" section. |
| Gemini | 6 | 6 | 0 | 0 | 0 | Subscription usage fact; monetary allocation: see "Lead cost readings" section. |
| OpenCode Go | 10 | 8 | 2 | 0 | 0 | Subscription usage fact; monetary allocation: see "Lead cost readings" section. |
| Route NOT VERIFIED | 1 | 1 | 0 | 0 | 0 | Cost `LEAD-FILLS`. |
| **Total** | **80** | **70** | **7** | **2** | **1** | **CodeBurn banner total: `LEAD-FILLS`** |

The owner ruled to maximize subscription usage (`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:375`). Therefore the counts above report utilization as fact, not a fabricated per-lane cost. Current subscription prices, entitlement allocation, external-credit spend, and CodeBurn readings are **NOT VERIFIED** in this lane; the task assigns CodeBurn completion to the Lead (`C:\tmp\LANE_PROMPTS_20260828\LANE_W151_HOURS_FINAL.md:17-20`).

Explicit afternoon recovery accounting: 7 DEAD route rows (DS21, DS24, A10, A11, W127, W127b, W127c), 2 CANCELLED rows (A12, A13), 1 fail-closed BLOCKED row (W150), and 3 successful named relaunch rows (DS21b, W127d, W150b). Morning combined rows additionally record prior variants for W125, W129, W133, W134, DS17, and GM21 without pretending those combined proxy spans are separate route durations (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:134-148`).

## Method and limits

1. Population follows the exact W151 inventory and the 45-row W140 basis (`C:\tmp\LANE_PROMPTS_20260828\LANE_W151_HOURS_FINAL.md:7-12`; `C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:201-203`). A9, W127, and W140 were refreshed in place; route variants DS21b, W127b/c/d, and W150b are distinct rows.
2. Arithmetic is `(selected_end.LastWriteTime - selected_start.LastWriteTime).TotalMinutes`, rounded to three decimals. A launch script is used as the start proxy only where the route has no distinct spec, matching W140's GM22/GM23 treatment (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:31,67,204`). DEAD routes select the last log as required (`C:\tmp\LANE_PROMPTS_20260828\LANE_W151_HOURS_FINAL.md:10-12`).
3. These are proxy spans, not labor, billed, or active-model time. Specs can be pre-staged or rewritten; transcription can lag; shared artifacts can be modified by later lanes; logs can buffer or outlive a report. W121, W126, W132, W133, W134, DS23, and W127c are explicit upper/contaminated proxies (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:203-206`; candidates above).
4. No package or lane total is computed. All groups overlap, so span addition would double-count wall time (`C:\tmp\LANE_PROMPTS_20260828\LANE_W151_HOURS_FINAL.md:10-12`). Counts are route-row counts only.
5. A12 and A13 have no end proxy. Their duration is **NOT VERIFIED**, not zero (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:20-23`; `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:411-412`).
6. W150b landed after the final `N_TIMES.txt` line; the measured artifact overrides the stale “running” prose under the repository/evidence rule (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:9-13`; `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:419`; `C:\tmp\LANE_PROMPTS_20260828\W150B_BASELINE_REPORT.md [metadata]`).

## Discrepancies

- The day-session ledger ends with W150b running, while later landing and done artifacts exist; the table uses those mtimes (`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:419`; metadata above).
- W127's spec mtime changed from the 09:35:17.937 morning capture to 12:36:36.931 before its afternoon launch; both candidates are disclosed and the current spec mtime is selected (`C:\tmp\LANE_PROMPTS_20260828\W140_MTIME_HOURS_TABLE.md:19,160`; metadata above).
- The mandated `C:\WLDOCS` worktree is on `docs/session-20260829-status`, while repository policy says `feature/<scope>` (`C:\LAB\Tradingview_LAB_CLEAN\.git\worktrees\WLDOCS\HEAD:1`; `C:\WFMERGE54\AGENTS.md:48-50`). No Git mutation or commit was performed; the Lead owns disposition (`C:\tmp\LANE_PROMPTS_20260828\LANE_W151_HOURS_FINAL.md:20-22`).


## Lead cost readings (source-attributed)

CodeBurn banner at session start 09:00 (harness-injected reading): **Today $140.59 / 338 calls; Month $6,210.13 / 36,024 calls**. No close-of-session banner reading was captured (the banner arrives only at session start), so the day-session marginal USD is NOT MEASURED - next session's start banner minus this one approximates it. Owner ruling (addendum 14 / memory budget-rule-maximize-subscriptions): subscription usage is reported as utilization FACT, never as an overspend flag; PAYG APIs stayed unused today (zero OpenRouter dispatches).
