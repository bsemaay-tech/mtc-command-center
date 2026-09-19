# OPS-A dry-run measurement over the packet section 1 evidence roots - 2026-09-15 19:36:12-19:37:06Z
Command: `backup.py --config opsa_dryrun_config_20260915.json --dry-run` (candidate bytes `e114ed31`, pinned 3.12.12; write-free by design - `PLAN` lines only; backup root stayed empty; stderr empty; exit 0).
Per-file lines: 11469; other lines: {'{"mode":': 1, 'SKIP': 2, '{"run_id":': 1}

| store | class | files | bytes | MiB |
|---|---|---|---|---|
| `p020_derived` | bulk | 94 | 259,983,472 | 247.9 |
| `p0_run_root` | protected | 7,345 | 52,108,275 | 49.7 |
| `gemini_packets` | reproducible | 1,401 | 24,303,139 | 23.2 |
| `p020_benchmark` | protected | 2,012 | 13,151,264 | 12.5 |
| `gemini_review_roots` | protected | 567 | 3,900,977 | 3.7 |
| `p020_preselect` | protected | 32 | 1,811,590 | 1.7 |
| `opus_queue` | process | 18 | 67,257 | 0.1 |
| **total** | | **11,469** | **355,325,974** | **338.9** |

Reading: one full daily all-store run today = the total above (the tool copies every file each run; there is no incremental mode - a 'daily delta' is therefore the whole set, ~339 MiB, until OPS-A gains a changed-only mode); the two protected roots that exist ONLY on the owner PC (`p0_run_root`, `gemini_review_roots`) are 53.4 MiB together.

SKIPs reported by the tool (2, both pytest scratch directories under the run root whose names carry a non-ASCII character and are sandbox-locked: `laneP1CAP_build/tmp/pytest-of-<user>/`, `laneP20DERIVFIX_build/tmp/pytest-of-<user>/` - `WinError 5` access denied). Not evidence; a real run would record them as `skipped` records, and the P0-30 adapter's restore gate refuses a run that carries `skipped` records - so those two directories must be excluded (or deleted as scratch) before OPS-A runs over `p0_run_root` for real.

Owner-PC drives (Get-PSDrive / Win32_DiskDrive, 19:34Z): ONE physical drive (Crucial CT1000P3PSSD8 NVMe, 932 GB); volume C: 930.3 GB, 54.9 GB free (94 % used). There is no second physical drive in the machine today, so option A1 ("backup root on a second physical drive") needs either an external drive or has to fall back to KVM2 / a cloud store as the ONLY off-disk copy; 54.9 GB free comfortably holds the 339 MiB set for many days, but on the same failure domain.
Full PLAN listing (11,473 lines, 1,753,620 bytes) kept in the run root only: opsa_dryrun_stdout_20260915.txt sha256 6a258bb9c5a187f8c7eede7aa0d9df4bfc057390be7132e20516726d23238f8f (not copied to CT13 - size; nothing in it beyond paths, sizes and hash prefixes).
