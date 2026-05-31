# Web UI Phase 3 Plan (Production-Grade Readability and UX)

Version: 3.0
Date: 2026-02-15
Owner: UI/UX + Streamlit

## 1) Problem Statement (from current screenshots)

Current UI quality is below production standard. Main issues:

1. Text encoding corruption (mojibake): icons and some labels render as broken characters.
2. Typography imbalance: some labels are too small to read, some values/headings are too large.
3. Contrast problems: blue info panels and muted text reduce readability.
4. Sidebar density and width: navigation + stats area feels crowded and visually heavy.
5. Weak visual hierarchy: sections, controls, and outputs compete equally for attention.
6. Form ergonomics: long pages with too many controls visible at once.
7. Inconsistent component styling: metrics, alerts, table headers, and expanders do not feel unified.

## 2) Goals

Primary goal: make the app readable, consistent, and operationally efficient on desktop and laptop screens.

Success criteria:
- No mojibake text in nav/buttons/headings/messages.
- Body text is readable at normal zoom (100%) without strain.
- All key pages (Home, Data, Backtest, Optimize, Reports) pass visual consistency checks.
- Sidebar and content spacing are balanced (no cramped blocks).
- Important actions are visually obvious (Run Backtest, Run Optimization, Load Case, etc.).

## 3) Constraints and Scope

In scope:
- UI/UX only (layout, typography, colors, spacing, labels, component polish).
- Refactor for maintainability only when needed for UI quality.

Out of scope:
- Engine behavior changes.
- Scoring changes.
- Backtest fill logic changes.

## 4) Design System (single source of truth)

Implement and enforce tokens in `mtc_backtest/utils/styles.py`:

### 4.1 Typography Scale
- page-title: 40 px / 700
- section-title: 28 px / 650
- block-title: 22 px / 600
- body: 15-16 px / 400-500
- label: 13-14 px / 500
- helper: 12 px / 400

Rules:
- No text below 12 px.
- Do not use mixed random font sizes.
- Metric values capped to avoid oversized numbers in sidebar.

### 4.2 Color and Contrast
- Keep dark theme, but increase text contrast for status/info panels.
- Ensure readable foreground/background pair for:
  - info panels
  - warning/error/success alerts
  - table headers/cells
- Replace low-contrast blue-on-blue text combinations.

### 4.3 Spacing and Rhythm
- Use 8 px base spacing grid.
- Standard vertical spacing between sections: 16-24 px.
- Inputs in same group share equal vertical gap.
- Page max content width and line-length limits for readability.

## 5) Architecture Strategy

Use incremental hardening first, then optional multipage split.

Step A (mandatory): stabilize current UI in place
- Keep existing page logic and improve styles + components first.
- Remove encoding issues and standardize labels.

Step B (optional): split to multipage only after visual parity
- `Home.py` + `pages/*` if maintainability benefit is clear.
- No functional regressions allowed.

## 6) Page-by-Page UX Targets

### 6.1 Sidebar
- Reduce visual noise and width pressure.
- Replace oversized quick stats numbers with compact metric cards.
- Ensure nav labels are clean UTF-8 text only.
- Add clearer active-page highlight.

### 6.2 Home
- Keep concise: title, short intro, quick actions, compact architecture/status cards.
- Remove long dense paragraphs from first fold.

### 6.3 Data Download
- Two-column layout remains, but:
  - left: form controls grouped and spaced
  - right: dataset table with readable row height and sticky header behavior (if possible)
- Improve upload area readability and button contrast.

### 6.4 Backtest
- Collapse non-critical controls by default.
- Keep key run controls visible above fold.
- Replace stale "Not implemented" list with accurate status text sourced from current feature state.

### 6.5 Optimize
- Parameter selection grid should be visually aligned.
- Sliders and numeric inputs should have consistent sizing.
- Emphasize primary action row (objective + trials + run).

### 6.6 Reports
- Better empty-state design (no DB/no runs).
- Improve artifact viewer readability (path, preview header, code block contrast).

## 7) Encoding and Copy Cleanup (critical)

Fix all text strings to UTF-8-safe content:
- Remove broken emoji sequences from titles/nav/buttons.
- Use plain text labels where emoji causes rendering issues.
- Keep wording short, operational, and consistent across pages.

Checklist:
- Sidebar page names
- Section headers
- Button labels
- Status/alert messages
- Tooltips/help text

## 8) Implementation Plan (ordered)

### Phase 3.1 - Emergency readability fixes (same day)
Files:
- `mtc_backtest/utils/styles.py`
- `mtc_backtest/utils/components.py`
- `mtc_backtest/app.py`

Tasks:
1. Normalize typography tokens and enforce minimum readable sizes.
2. Fix contrast for info/metric/alert blocks.
3. Reduce sidebar metric emphasis and spacing clutter.
4. Remove mojibake labels and replace with clean text.

Acceptance:
- No broken characters.
- Main pages readable at 100% zoom.

### Phase 3.2 - Layout and hierarchy pass
Files:
- `mtc_backtest/app.py`
- `mtc_backtest/src/ui/*.py` (as needed)

Tasks:
1. Re-group controls by task order (Setup -> Run -> Results).
2. Make critical actions visible above fold.
3. Standardize section headers and collapsible blocks.

Acceptance:
- Users can complete each page flow without scrolling through unrelated controls.

### Phase 3.3 - Components and consistency hardening
Files:
- `mtc_backtest/utils/components.py`
- `mtc_backtest/utils/styles.py`

Tasks:
1. Introduce shared wrappers for metric card, section header, empty state, panel.
2. Remove ad-hoc inline styling from page code.
3. Make all pages consume same component patterns.

Acceptance:
- Visual consistency across Home/Data/Backtest/Optimize/Reports.

### Phase 3.4 - Optional multipage extraction (if needed)
Files:
- `mtc_backtest/Home.py`
- `mtc_backtest/pages/*.py`
- keep `mtc_backtest/_legacy_app.py`

Acceptance:
- Zero functional regression.
- Same behavior as single-file flow.

## 9) QA and Verification

### Manual visual QA checklist
- No broken text/icon encoding.
- Sidebar readable and not visually dominant.
- Buttons and controls have clear hierarchy.
- Alerts and info boxes are readable.
- Data tables are legible.

### Functional QA
- Data download still works.
- Backtest run still works.
- Optimize run still works.
- Reports/history/artifact preview still works.

### Regression command
- `python -m pytest mtc_backtest/tests -v`

## 10) Definition of Done

UI Phase 3 is done when:
1. Readability issues are resolved on all five pages.
2. Encoding corruption is completely removed.
3. Typography and spacing are token-driven and consistent.
4. No workflow regressions are introduced.
5. Visual QA checklist is signed off with current screenshots replaced by clean versions.

## 11) Deliverables

1. Updated `styles.py` with strict tokens and readable defaults.
2. Updated `components.py` with reusable UI primitives.
3. Updated `app.py` (or pages) with cleaned labels and improved layout hierarchy.
4. Before/after screenshots for each major page.
5. This plan as execution baseline.
