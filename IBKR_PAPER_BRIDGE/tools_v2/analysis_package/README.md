# Owner Analysis-Package Generator (Bridge V2 Package 4, T1)

Bounded, redacted, read-only export of an **explicit allowlist** of local files
and directories into **one self-describing Markdown bundle**, for the documented
manual Codex-subscription workflow.

The generator is
`IBKR_PAPER_BRIDGE/tools_v2/analysis_package/generate_analysis_package.py`
(stdlib-only, no network imports, no clock reads).

## Usage

From this directory (`IBKR_PAPER_BRIDGE/tools_v2/analysis_package`):

```text
python generate_analysis_package.py --config fixtures/sample_config.json
```

The sample config (`fixtures/sample_config.json`) is a working example against
the committed synthetic fixtures:

```json
{
  "timestamp": "2026-08-18T00:00:00Z",
  "output": "sample_output/analysis_package_bundle.md",
  "inputs": [
    "src/sample_settings.txt",
    "src/app_config.txt",
    "src/notes_with_creds.md",
    "src/hex_addresses.log"
  ]
}
```

Rules for any config:

- `timestamp` is **caller-supplied** and non-empty. The generator never reads the
  clock, so identical config + inputs produce a byte-identical bundle.
- `output` is the bundle path. Relative paths resolve against the config file's
  directory.
- `inputs` is a **non-empty explicit allowlist** of files and/or directories.
  Relative paths resolve against the config file's directory. There are no
  defaults that touch live paths.
- Unknown config keys are refused loudly (exit code 2), never silently ignored.

Exit codes: `0` = bundle written; `2` = configuration/allowlist/bounds error.

## Format decision

The first Gate-1 deliverable chose a **single self-describing Markdown bundle**:
a header (caller-supplied generation time, input inventory, bounds applied,
per-kind redaction summary) followed by one fenced section per included file.
This fits the manual Codex-subscription workflow because exactly one readable
file is pasted/uploaded, the header makes the file self-explanatory, and every
disposition (included / truncated / excluded / omitted) is recorded explicitly.

## Bounds (enforced and recorded in the output header)

| Bound | Value |
|---|---|
| Per-file byte cap | 200 KB (`MAX_FILE_BYTES = 204800`) |
| Per-file line cap | 4000 lines |
| Total bundle cap | 2 MB (`MAX_TOTAL_BYTES = 2097152`) |
| Header reservation | 32768 bytes inside the total cap |
| Binary exclusion | extension denylist + null-byte sniff of the first 8192 bytes |

A file over the byte cap is truncated to the first 200 KB. A file over the line
cap is truncated to the first 4000 lines. Binary files are never embedded; they
appear in the inventory with an exclusion reason. If adding the next file would
exceed the content budget, that file is **omitted** and listed as such — nothing
is skipped silently.

## Redaction (enforced, per-kind counts in the header)

| Kind | What is replaced by `[REDACTED:<kind>]` |
|---|---|
| `assignment` | values of `key=` / `token=` / `password=` / `secret=` assignments (incl. prefixed forms like `api_key`) |
| `aws_key_id` | AWS-style access key ids (`AKIA`/`ASIA` + 16 upper alnum) |
| `hex_address` | `0x`-prefixed 40- or 64-hex addresses/keys |
| `bearer` | HTTP `Bearer` credentials |
| `long_token` | long hex tokens (>=32 hex chars) or base64-like tokens (>=40 chars, digit+upper+lower) |

The committed fixtures under `fixtures/src/` contain only obviously synthetic,
clearly fake planted secrets used to demonstrate the redaction.

## Boundaries

- New `analysis_package` directory only; no modifications to existing files.
- No network capability in the generator (no `urllib`/`http`/`socket`/
  `requests`/`ssl` imports).
- No provider/API integration; the bundle is a file handed over manually.
- No reading of real credential stores: credential-store filenames (`.env`,
  `.netrc`, `auth.json`, `credentials.json`, `id_rsa`, `id_ed25519`, ...) and
  dotfiles are refused or excluded during directory walks, and naming one
  directly in the allowlist is a loud error.
- Tests run on fixtures only.

## Non-authority statement

This package and its fixtures are generated tooling/test artifacts for the
Gate-1 Package 4 increment. This `README.md` documents the generator's actual
implemented behavior; it does **not** amend the frozen Gate-1 scope record and
does **not** grant authority to change bounds, redaction kinds, or boundaries.
The authoritative scope is
`MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE4_ANALYSIS_PACKAGE_GENERATOR_2026-08-18.md`.

## Redaction precision notes (implemented behavior, exactly)

The Gate-1 record names the redaction kinds in prose; the implemented patterns
are narrower in five documented ways. These are recorded here so nobody assumes
broader coverage than the code delivers:

1. **AWS-style ids** — only access-key ids matching `AKIA`/`ASIA` + 16
   uppercase alphanumerics are redacted; other AWS identifier shapes are not.
2. **Long base64 tokens** — only `[A-Za-z0-9+/]{40,}` with up to two `=` of
   padding AND containing at least one digit, one uppercase, and one lowercase
   character. URL-safe base64 (`-`/`_`) and single-case runs are not matched
   (single-case hex-alphabet runs are caught by the hex-token pattern instead).
3. **Per-file 200 KB cap** — enforced on decoded characters (reading at most
   204,801 raw bytes); for non-ASCII or undecodable input the recorded
   included-bytes figure can differ slightly from 204,800.
4. **Loud failure vs. inventory exclusion** — missing paths, directly-named
   credential-store files, directly-named dotfiles, and symlink escapes fail
   loudly (exit 2); binary files, duplicates, and the output file itself are
   recorded as inventory exclusions in a successful run.
5. **Assignment values** — `key=`/`token=`/`password=`/`secret=` redaction
   requires a value of at least 4 non-space characters; shorter values are left
   as-is.
6. **Known non-matches (next increment):** camelCase assignment keys
   (`apiKey=`, `dbPassword=`, `clientSecret=`) and quoted assignment values
   containing spaces (`password = "pass phrase here"`) are NOT redacted by the
   current patterns. Review bundles by eye before sharing when inputs may
   contain such shapes.
