# PyArrow 23.0.1 bump — fix evidence

Date: 2026-08-25

Lane: X, Codex implementer under Claude Lead

Branch: `fix/pyarrow-cve-bump-20260825`

Base: `46f5bafbf82f3366c8bc7ee08f6f0eee08d46138`

## Authority and scope

Owner authorization supplied in the lane contract: “I authorize the pyarrow 23.0.1 pin bump in the backtest lock with validation”.

The implementation changes only `pyarrow==23.0.0` to `pyarrow==23.0.1` in the protected backtest lock. No other pin, engine/source file, Pine/parity file, strategy behavior, schema, host, credential, or deployment surface was changed. The remaining repository changes are this evidence package and an append-only dependency-ledger successor entry.

The Lead should treat review as **T0** because the changed lock is under the protected `02_MTC_BACKTEST` surface and the change closes a security advisory.

## Lockfile change and pin count

Command:

```powershell
git diff --unified=0 -- MTC_COMMAND_CENTER/02_MTC_BACKTEST/requirements-lock.txt
$pinLines = Select-String -LiteralPath 'MTC_COMMAND_CENTER\02_MTC_BACKTEST\requirements-lock.txt' -Pattern '^[A-Za-z0-9_.-]+=='
$pinLines | ForEach-Object { $_.Line }
"COUNT=$($pinLines.Count)"
```

Real output:

```text
@@ -6 +6 @@ plotly==6.5.2
-pyarrow==23.0.0
+pyarrow==23.0.1
ccxt==4.5.36
numpy==2.4.2
optuna==4.7.0
pandas==2.3.3
plotly==6.5.2
pyarrow==23.0.1
pydantic==2.12.5
pytest==9.0.2
pytest-cov==7.0.0
python-dateutil==2.9.0.post0
pytz==2025.2
streamlit==1.54.0
tqdm==4.67.3
COUNT=13
```

## Fresh locked environment

The validation root was newly created and did not exist before the run:

`C:\Users\BarışSemaay\AppData\Local\Temp\pyarrow_bump_20260825_lane_x_46f5baf`

Commands:

```powershell
py -3.13 -m venv "$validationRoot\.venv"
& "$validationRoot\.venv\Scripts\python.exe" --version
& "$validationRoot\.venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r MTC_COMMAND_CENTER\02_MTC_BACKTEST\requirements-lock.txt
& "$validationRoot\.venv\Scripts\python.exe" -m pip check
& "$validationRoot\.venv\Scripts\python.exe" -c "import pyarrow; print('PYARROW_VERSION=' + pyarrow.__version__)"
```

Relevant real output (the resolver/download body is omitted here only for length):

```text
VALIDATION_ROOT=C:\Users\BarışSemaay\AppData\Local\Temp\pyarrow_bump_20260825_lane_x_46f5baf
Python 3.13.14
Successfully installed ... numpy-2.4.2 ... pandas-2.3.3 ... pyarrow-23.0.1 ...
No broken requirements found.
PYARROW_VERSION=23.0.1
```

This was a complete install of the bumped 13-line lock, not a standalone pyarrow install.

## Selected artifact and licence capture

Commands used the same fresh environment:

```powershell
python -m pip download --disable-pip-version-check --no-deps --only-binary=:all: --dest "$validationRoot\downloaded_wheel" pyarrow==23.0.1
Get-FileHash <downloaded-wheel> -Algorithm SHA256
```

Installed distribution metadata and licence files were inspected with `importlib.metadata` and SHA-256.

Real output:

```text
Successfully downloaded pyarrow
WHEEL_FILE=pyarrow-23.0.1-cp313-cp313-win_amd64.whl
WHEEL_BYTES=27540749
WHEEL_SHA256=cecfb12ef629cf6be0b1887f9f86463b0dd3dc3195ae6224e74006be4736035a
METADATA_NAME=pyarrow
METADATA_VERSION=23.0.1
METADATA_LICENSE_EXPRESSION=Apache-2.0
LICENSE_FILE=pyarrow-23.0.1.dist-info/licenses/LICENSE.txt BYTES=115832 SHA256=1149fe68558c3e9841aa055e3bdeb42f0c5693cc9ba4ff370b82d6bbac04ae9e
LICENSE_FILE=pyarrow-23.0.1.dist-info/licenses/NOTICE.txt BYTES=2997 SHA256=2ccca1e730e671f55b8028facf2261a6f74b561a4d96a2ccd743be19c5619236
```

## Real and synthetic Parquet / Arrow IPC round-trips

The real source was opened read-only from the existing repository data tree:

`MTC_COMMAND_CENTER/02_MTC_BACKTEST/data/history_sweeps_e3002_mini/20250630_0000.parquet`

The QuantLens `03_QUANTLENS/data` tree contains no local Parquet files in this worktree, so the bounded source was selected from the repository's backtest data tree. Its SHA-256 was checked before and after validation.

For each of a 128-row real OHLCV slice and a synthetic table containing integer, float/null, string/null, Boolean/null, binary/null, and timezone-aware timestamp columns, the validator:

1. wrote the table to a first Parquet or Arrow IPC file;
2. read the first file;
3. compared schema including metadata and compared all table values;
4. wrote the read-back table to a second file; and
5. compared the two files byte-for-byte and by SHA-256.

Parquet used `compression="NONE"` and format version `2.6`; Arrow IPC used the file format through `pyarrow.ipc.new_file` / `open_file`.

Real output:

```text
PYTHON=3.13.14 PYARROW=23.0.1
REAL_SOURCE=C:\WPPPYAR_20260825\MTC_COMMAND_CENTER\02_MTC_BACKTEST\data\history_sweeps_e3002_mini\20250630_0000.parquet
REAL_SOURCE_BYTES=754207 REAL_SOURCE_SHA256_BEFORE=3aa0d38943e04ca907ba3c178fdd1fbfae1b7ce43f731ded6d3ccb9da9cecf01
REAL_SOURCE_ROWS=17856 REAL_SLICE_ROWS=128 REAL_COLUMNS=['timestamp', 'open', 'high', 'low', 'close', 'volume']
REAL_SCHEMA=timestamp: timestamp[ns, tz=UTC] | open: double | high: double | low: double | close: double | volume: double | -- schema metadata -- | pandas: ...
SYNTHETIC_SCHEMA=row_id: int64 | price: double | symbol: string | active: bool | payload: binary | event_time: timestamp[us, tz=UTC] | -- schema metadata -- | fixture: 'pyarrow-23.0.1-validation'
CASE=real_repo_slice FORMAT=PARQUET ROWS=128 COLS=6 SCHEMA_EQUAL=True TABLE_EQUAL=True BYTE_EQUAL=True BYTES=10787 SHA256=c30c574e7157c2b95a1132fb176c28badd9bbc83bf01be618edd24d295dc0a7a
CASE=real_repo_slice FORMAT=ARROW_IPC_FILE ROWS=128 COLS=6 SCHEMA_EQUAL=True TABLE_EQUAL=True BYTE_EQUAL=True BYTES=9162 SHA256=7331fc07fa4327e30c0f68659eb64b7c48d0fcbeffc8445ca8a4fcc883534aaa
CASE=synthetic FORMAT=PARQUET ROWS=4 COLS=6 SCHEMA_EQUAL=True TABLE_EQUAL=True BYTE_EQUAL=True BYTES=1984 SHA256=f801fa86804d90db6f06eab70eb7323265873ac6d3e07fc3edacdd0a8f5aafdd
CASE=synthetic FORMAT=ARROW_IPC_FILE ROWS=4 COLS=6 SCHEMA_EQUAL=True TABLE_EQUAL=True BYTE_EQUAL=True BYTES=1642 SHA256=893d63203cbc9393e6f5fe068657c3367210dfbbec7bd21e07f82f1e4e4715ff
REAL_SOURCE_SHA256_AFTER=3aa0d38943e04ca907ba3c178fdd1fbfae1b7ce43f731ded6d3ccb9da9cecf01 SOURCE_UNCHANGED=True
ROUNDTRIP_RESULT=PASS
```

The first harness invocation stopped before any round-trip because string values were supplied for a typed synthetic timestamp array. PyArrow raised `ArrowTypeError: object of type <class 'str'> cannot be converted to int`. The fixture was corrected to use timezone-aware Python `datetime` values and rerun in a new temp subdirectory. The failed attempt wrote no repository file and did not modify the real source.

## Offline engine smoke — no backtest execution

The repository offers `src.cli.run_backtest --dry-run`. Its control flow loads configuration and data, then returns before calling `run_backtest`, creating a runner, saving results, or starting research. The validated real-data-derived Parquet fixture was supplied to that path.

Command (from `MTC_COMMAND_CENTER/02_MTC_BACKTEST`):

```powershell
& $venvPython -m src.cli.run_backtest --data $fixture --dry-run --output $output
```

Real output:

```text
============================================================
MTC Python Backtest CLI
============================================================
Using default configuration
Loaded 128 bars from: C:\Users\BarışSemaay\AppData\Local\Temp\pyarrow_bump_20260825_lane_x_46f5baf\fixtures_final\real_repo_slice_first.parquet

✅ Dry run successful!
   Config valid: Yes
   Data loaded: 128 bars
DRY_RUN_EXIT_CODE=0
DRY_RUN_OUTPUT_PATH_EXISTS=False
```

No real backtest, optimization, parity execution, strategy research, server, broker, or host action was run.

## OSV verification for CVE-2026-25087

Queried OSV on 2026-08-25. Exact-version query:

```powershell
$body = @{ version = '23.0.1'; package = @{ name = 'pyarrow'; ecosystem = 'PyPI' } } | ConvertTo-Json -Compress
Invoke-WebRequest -Method Post -Uri 'https://api.osv.dev/v1/query' -ContentType 'application/json' -Body $body
```

Corrected real output from the final assertion (an absent `vulns` property is counted as zero):

```text
OSV_RECHECKED_AT_UTC=2026-08-25T03:42:01Z
OSV_VERSION_QUERY_HTTP=200
OSV_VERSION_QUERY_RAW={}
OSV_VERSION_QUERY_VULN_COUNT=0
```

Advisory query:

```powershell
Invoke-WebRequest -Method Get -Uri 'https://api.osv.dev/v1/vulns/GHSA-rgxp-2hwp-jwgg'
```

Real output extracted directly from the response:

```text
OSV_QUERIED_AT_UTC=2026-08-25T03:41:28Z
OSV_ADVISORY_HTTP=200
OSV_ADVISORY_ID=GHSA-rgxp-2hwp-jwgg
OSV_ADVISORY_ALIASES=CVE-2026-25087,PYSEC-2026-113
OSV_ADVISORY_PUBLISHED=2026-02-17T15:31:35Z
OSV_ADVISORY_MODIFIED=2026-06-12T10:29:15.451071539Z
OSV_AFFECTED_PACKAGE=PyPI:pyarrow
OSV_RANGE_TYPE=ECOSYSTEM
OSV_RANGE_EVENT_INTRODUCED=15.0.0
OSV_RANGE_EVENT_FIXED=23.0.1
OSV_EXPLICIT_AFFECTED_VERSIONS=15.0.0,15.0.1,15.0.2,16.0.0,16.1.0,17.0.0,18.0.0,18.1.0,19.0.0,19.0.1,20.0.0,21.0.0,22.0.0,23.0.0
```

Therefore OSV identifies `23.0.0` as affected and `23.0.1` as the fixed boundary, while the exact `23.0.1` package query returns no OSV vulnerability record.

## RED/GREEN feasibility and closure claim

No RED/GREEN test of the native use-after-free advisory path is feasible or claimed in this lane. The advisory concerns malformed Arrow IPC with pre-buffering in native code. No approved, lawfully preserved exploit fixture is available here, and intentionally inducing a native heap use-after-free would be unsafe and would not be an ordinary compatibility regression test.

Consistent with the owner-directed ledger update policy for this bump, closure evidence for **this named advisory** is the OSV fixed-range record, the zero-result exact-version query, the exact selected artifact/version, and successful real/synthetic Parquet and Arrow IPC compatibility round-trips. This does not claim exploit-path RED/GREEN, does not prove absence of unrelated vulnerabilities, and does not erase the existing unhashed/transitive-lock supply-chain debt.

## Result

**PASS for implementer validation.** Lead acceptance and the mandatory T0 review remain separate.
