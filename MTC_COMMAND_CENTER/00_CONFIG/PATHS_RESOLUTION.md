# Paths Resolution

`paths.example.json` defines safe defaults. `paths.local.json` may override local machine paths and must not be committed.

Resolution order:

1. Load `00_CONFIG/paths.example.json`.
2. If `00_CONFIG/paths.local.json` exists, merge it over the example.
3. Canonicalize paths before use.
4. Warn when a path exceeds 200 characters.
5. On Windows, apply the long-path prefix only after canonicalization and only when needed.

Required MVP-1 keys:

- `mcc_root`
- `mtc_v2_root`
- `reports_root`

Optional MVP-1 keys:

- `mtc_v2_python_exe`
- `pinets_root`
- `tradingview_exports_dir`
