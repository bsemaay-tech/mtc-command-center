# Implementation Plan - Phase 3: Web UI 2.0 (Professional Ops Dashboard)

**Version**: 2.1 (UX/UI Enhanced - Professional) | **Date**: 2026-02-15

## 🎯 Goal
Transform monolithic `app.py` into a **professional, readable, and visually consistent Streamlit multipage dashboard** with enterprise-grade UI.

## 📸 Current Issues Identified

### Visual Problems (from screenshots)
1. **Text Size Inconsistency** - Some text too large, some unreadable
2. **Poor Color Contrast** - Low contrast between text and background
3. **Layout Clutter** - Too much information without proper grouping
4. **No Visual Hierarchy** - Everything competes for attention
5. **Expanders Too Dense** - Too many options without proper categorization

### UX Problems
1. **Navigation Unclear** - Radio buttons not visually distinct
2. **Metrics Display** - KPI boxes poorly organized
3. **No Consistent Spacing** - Elements feel cramped

---

## 🎨 Design System (Professional)

### Typography Scale
```
- Hero Title: 2.5rem (40px), weight 700
- Page Title: 1.75rem (28px), weight 600  
- Section Header: 1.25rem (20px), weight 600
- Body Text: 1rem (16px), weight 400
- Caption/Label: 0.875rem (14px), weight 400
- Small/Helper: 0.75rem (12px), weight 400
```

### Color Palette (Dark Theme - Professional)
```
--bg-primary: #0e1117 (Streamlit default dark)
--bg-secondary: #161b22 (Cards/panels)
--bg-tertiary: #21262d (Inputs/expanders)
--text-primary: #f0f6fc (Main text)
--text-secondary: #8b949e (Muted text)
--text-tertiary: #6e7681 (Helper text)
--accent-primary: #238636 (Success/green)
--accent-secondary: #1f6feb (Primary blue)
--accent-warning: #d29922 (Warning/yellow)
--accent-danger: #f85149 (Error/red)
--border-color: #30363d
```

### Spacing System
```
--space-xs: 4px
--space-sm: 8px  
--space-md: 16px
--space-lg: 24px
--space-xl: 32px
--space-2xl: 48px
```

---

## 📁 Final Structure
```
mtc_backtest/
├── Home.py                 # Landing + dashboard
├── pages/
│   ├── 1_Data.py          # Downloads + catalog
│   ├── 2_Backtest.py      # Config/Run/Results tabs
│   ├── 3_Optimize.py      # Optuna + presets
│   └── 4_Reports.py       # History/compare/artifacts
├── utils/
│   ├── __init__.py
│   ├── session.py         # Shared st.session_state
│   ├── components.py      # Reusable UI components
│   └── styles.py          # Custom CSS
└── _legacy_app.py         # Backup of original app.py
```

---

## 🔧 Implementation Details

### 1. Custom CSS Module (styles.py)
```python
def get_custom_css() -> str:
    return """
    <style>
    /* Typography Scale */
    h1 { font-size: 2rem !important; font-weight: 700 !important; }
    h2 { font-size: 1.5rem !important; font-weight: 600 !important; }
    h3 { font-size: 1.25rem !important; font-weight: 600 !important; }
    p, .stMarkdown { font-size: 1rem !important; line-height: 1.6 !important; }
    
    /* Card Styling */
    .metric-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 16px;
    }
    
    /* Sidebar Improvements */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
    }
    
    /* Expander Improvements */
    .streamlit-expanderHeader {
        background: var(--bg-tertiary);
        border-radius: 6px;
    }
    
    /* DataFrame Styling */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
    }
    </style>
    """
```

### 2. Reusable Components (components.py)
```python
def kpi_card(label: str, value: str, delta: str = None, 
             icon: str = None, color: str = "default"):
    """Professional KPI card with consistent styling"""
    
def section_header(title: str, icon: str = None):
    """Section header with consistent typography"""
    
def config_group(title: str, expand: bool = False):
    """Grouped configuration with visual hierarchy"""
    
def metric_row(*metrics):
    """Horizontal metric row"""
```

### 3. Page Layout Improvements
| Page | Layout | Improvements |
|------|--------|--------------|
| Home | 3-column KPI + quick actions | Visual hierarchy, consistent spacing |
| Data | Left: controls, Right: table | Split view, better contrast |
| Backtest | Tabs: Config/Run/Results | Tabbed interface, cleaner |
| Optimize | Param grid + results | Better parameter grouping |
| Reports | Filter + results | Clear visual separation |

---

## ✅ Verification Checklist

### Visual Checkpoints
- [ ] Text readable at all levels (check contrast ratio ≥ 4.5:1)
- [ ] Consistent spacing between elements
- [ ] Clear visual hierarchy (title > section > subsection)
- [ ] Professional color scheme applied
- [ ] Cards have proper borders and shadows

### Functional Checkpoints
- [ ] Navigation works across all pages
- [ ] All expanders expand/collapse properly
- [ ] Data loads and displays correctly
- [ ] Charts render with proper styling
- [ ] Mobile responsive (if applicable)

---

## 🚀 Implementation Steps (2-4 hours)

1. **Create CSS Module** (30 min)
   - Define design tokens
   - Create reusable components
   - Test in isolation

2. **Extract Pages** (1 hour)
   - Move page functions to separate files
   - Apply consistent styling

3. **Polish & Refine** (30 min)
   - Fix any visual issues
   - Ensure accessibility

4. **Test Full Flow** (30 min)
   - Download → Backtest → Optimize → Reports
   - Verify all features work

---

## 📦 Deliverables

1. **styles.py** - Custom CSS with design system
2. **components.py** - Reusable UI components  
3. **Home.py** - Landing page with KPIs
4. **pages/1_Data.py** - Data download page
5. **pages/2_Backtest.py** - Backtest page with tabs
6. **pages/3_Optimize.py** - Optimization page
7. **pages/4_Reports.py** - Reports page

---

**Status**: Ready for Implementation
**Priority**: High - UI affects user experience daily
