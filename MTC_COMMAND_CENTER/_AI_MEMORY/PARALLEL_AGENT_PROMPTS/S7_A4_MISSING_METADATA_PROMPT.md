# S7 — A4: Missing Metadata Tab in Strategy Research Lab

## PREREQUISITE CHECK — do this FIRST

Run this to see current metadata coverage (S1 may still be running — proceed regardless):

```bash
cd C:\LAB\Tradingview_LAB_CLEAN
python -c "
import json
from pathlib import Path
reg = json.loads(Path('MTC_COMMAND_CENTER/05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json').read_text(encoding='utf-8'))
entries = reg.get('strategies', reg) if isinstance(reg, dict) else reg
if isinstance(entries, dict):
    entries = list(entries.values())
review = [e for e in entries if e.get('trailing_logic') == 'review_needed']
filled = [e for e in entries if e.get('trailing_logic') not in (None, 'review_needed', '')]
print(f'Total entries: {len(entries)}')
print(f'trailing_logic = review_needed: {len(review)}')
print(f'trailing_logic filled: {len(filled)}')
"
```

**Proceed regardless of the count.** If 0 are filled, the UI will honestly show "0/N filled" —
that is the correct current state. The UI reads live from the API so it auto-updates when S1 finishes.

---

## Project context

Repo: `C:\LAB\Tradingview_LAB_CLEAN`  
Dashboard frontend: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js` (3000+ lines — read it fully)  
Dashboard CSS: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/styles.css`  
Strategy registry: `MTC_COMMAND_CENTER/05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json`  
Backend API endpoint: `GET /api/snapshot` → key `registry` (from `registry_reader.py`)

**Previous agents (S2, S5, S6) have already edited app.js.** READ IT FULLY before touching it.

---

## Task A4 — "Missing Metadata" tab in Strategy Research Lab

### Problem

The Strategy Research section of the dashboard has no tab showing which strategies still
have `"review_needed"` in `trailing_logic`, `filters_used`, `known_strengths`,
or `known_weaknesses`. After S1's A1 extractor runs, many of these fields are filled —
but some will remain as `"review_needed"`. The dashboard should show this coverage.

### What to build

Find the **Strategy Registry** or **Research Lab** section in app.js (search for
`renderStrategyRegistry`, `renderResearchLab`, or similar). Add a **"Missing Metadata"**
sub-tab/section inside it.

**What to display:**

1. **Coverage summary bar:**
   ```
   Metadata Coverage: 48/63 strategies fully filled (76%)
   trailing_logic:  ████████░░  55/63
   filters_used:    ██████████  63/63
   known_strengths: ████████░░  51/63
   known_weaknesses:████████░░  51/63
   ```

2. **Table of strategies still missing metadata** (where any of the 4 fields = "review_needed"):
   | Strategy ID | trailing_logic | filters_used | known_strengths | known_weaknesses |
   |---|---|---|---|---|
   | STG042_... | ⚠ missing | ✓ | ✓ | ⚠ missing |

3. **"All filled" message** if 0 strategies have any `review_needed` field.

### Data source

Read from `snapshot.registry` (check what key `registry_reader.py` puts in the snapshot)
OR directly fetch `/api/snapshot` and navigate to registry entries.

Each registry entry has: `strategy_id`, `trailing_logic`, `filters_used`, `known_strengths`, `known_weaknesses`.

```javascript
function buildMetadataCoverage(registryEntries) {
    const REVIEW = 'review_needed';
    const fields = ['trailing_logic', 'filters_used', 'known_strengths', 'known_weaknesses'];
    const total = registryEntries.length;

    const coverage = {};
    fields.forEach(f => {
        coverage[f] = registryEntries.filter(e => e[f] && e[f] !== REVIEW).length;
    });

    const missing = registryEntries.filter(e =>
        fields.some(f => !e[f] || e[f] === REVIEW)
    );

    return { total, coverage, missing, fields };
}
```

### Where to add it

Search app.js for the Strategy Registry rendering function. Add the Missing Metadata
section as a collapsible `<details>` block or a sub-tab within that section.

If no Strategy Registry section exists in app.js, add it to the Pipeline tab as a
"Metadata Coverage" panel below the strategy list.

---

## Validation

```bash
node --check MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js
# Expected: PASS

cd C:\LAB\Tradingview_LAB_CLEAN
$env:PYTHONPATH = "MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api"
python -m pytest MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests -q
# Expected: 35 passed — must not regress

# Visual check:
cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api && python -m mcc_readonly serve
# Open http://127.0.0.1:8765/dashboard
# Find the Missing Metadata section — verify coverage counts match registry state
```

---

## HARD SAFETY RULES

- NEVER edit `*.pine` files, `02_MTC_BACKTEST/src/engine/`, `mega_walk_forward.py`
- NEVER edit `apps/api/mcc_readonly/*.py` (backend off-limits)
- NEVER edit `05_REGISTRY/*.json` (generated)
- app.js single-writer — one coherent edit pass only
- Only write to:
  - `08_DASHBOARD_APP/apps/web/app.js`
  - `08_DASHBOARD_APP/apps/web/styles.css` (minimal additions only)

---

## Report output

Write to EXACTLY this path:
`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\_AI_MEMORY\PARALLEL_AGENT_REPORTS\S7_A4_MISSING_METADATA_REPORT.md`

Report must contain:
- S1 prerequisite check result: how many `trailing_logic` filled vs review_needed
- Which function added and at what line in app.js
- Coverage numbers shown in UI (total / per field)
- `node --check` result
- API test result (N passed)
- Browser verification result
