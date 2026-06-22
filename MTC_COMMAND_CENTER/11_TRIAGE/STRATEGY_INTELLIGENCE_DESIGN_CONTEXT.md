---
name: MTC Strategy Intelligence Command Center
description: A quiet, evidence-first dark command center for trading-strategy research.
colors:
  bg: "#07090E"
  panel: "#0E131C"
  panel-2: "#121924"
  panel-3: "#0A0D15"
  panel-hover: "#1A2333"
  border: "#1e2733"
  border-strong: "#2b3645"
  teal: "#2dd4bf"
  teal-dim: "#14b8a6"
  emerald: "#34d399"
  amber: "#f59e0b"
  red: "#f87171"
  blue: "#60a5fa"
  purple: "#8b5cf6"
  text: "#e2e8f0"
  text-strong: "#f1f5f9"
  muted: "#94a3b8"
  faint: "#64748b"
  faintest: "#475569"
typography:
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  heading:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 800
    lineHeight: 1.3
    letterSpacing: "-0.01em"
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "12.5px"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  label:
    fontFamily: "ui-monospace, JetBrains Mono, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "10px"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "0.12em"
  data:
    fontFamily: "ui-monospace, JetBrains Mono, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "normal"
rounded:
  sm: "7px"
  md: "10px"
  pill: "999px"
spacing:
  xs: "6px"
  sm: "8px"
  md: "14px"
  lg: "20px"
  xl: "26px"
components:
  button-default:
    backgroundColor: "{colors.panel-2}"
    textColor: "{colors.text}"
    rounded: "{rounded.sm}"
    padding: "8px 13px"
  button-default-hover:
    backgroundColor: "{colors.panel-hover}"
    textColor: "{colors.text}"
  button-primary:
    backgroundColor: "{colors.teal}"
    textColor: "#04201c"
    rounded: "{rounded.sm}"
    padding: "8px 13px"
  chip:
    backgroundColor: "{colors.panel-3}"
    textColor: "{colors.muted}"
    rounded: "{rounded.pill}"
    padding: "6px 11px"
  chip-active:
    backgroundColor: "rgba(6,40,38,0.4)"
    textColor: "{colors.teal}"
  panel:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "18px 20px"
  status-pill:
    backgroundColor: "{colors.panel-2}"
    textColor: "{colors.muted}"
    rounded: "6px"
    padding: "5px 10px"
---

# Design System: MTC Strategy Intelligence Command Center

## 1. Overview

**Creative North Star: "The Quiet Terminal"**

A trading terminal stripped of its noise. The reference point is the data desk of a
serious research operation — Bloomberg-grade density of information, but with the
wall-of-numbers clutter removed and replaced by hierarchy. Near-black surfaces let
sourced numbers and earned verdicts carry the screen; a single teal accent marks
what the operator should act on, and nothing else. The interface is calm at rest:
no motion competes for attention, no decoration asks to be admired. Confidence comes
from accuracy and legibility, not flash.

This system explicitly rejects the **cluttered legacy terminal** (MT4 / old-Bloomberg
density without a visual spine — every dense block here earns its density with a clear
heading and rhythm). It also rejects the **generic SaaS dashboard** (no hero-metric
cards, no gradient accents, no identical icon+heading+text grids), the **crypto/retail
trading app** (no neon glow, no gamified green/red, no casino energy), and **consumer
fintech** playfulness (no rounded confetti, no emotion-driven oversimplification).

The voice is exact and unhedged: state what is known, label what is estimated, surface
what is stale. Skepticism is a designed feature — the system makes it easy to distrust
a weak result.

**Key Characteristics:**
- Near-black layered surfaces (five tones from `#07090E` to `#1A2333`), depth by tone not shadow.
- One teal accent (`#2dd4bf`) reserved for action, selection, and live state.
- Monospace for every number, label, and code token; sans for prose and headings.
- Semantic state vocabulary (ok / bad / warn / neutral) shared across pills, badges, banners, dots.
- Dense by intent, legible by hierarchy.

## 2. Colors

A cool, near-black slate palette with a single teal-emerald accent family and a tight set of semantic status hues.

### Primary
- **Command Teal** (`#2dd4bf`): The one voice. Primary actions, active nav route, current selection, live/"ok-teal" state, section eyebrows. Its dimmed sibling **Teal Dim** (`#14b8a6`) anchors the brand mark and primary-button base.

### Secondary
- **Verdict Emerald** (`#34d399`): Pass / healthy / promotable state only — on badges, pills, and status dots.
- **Caution Amber** (`#f59e0b`): Pending / evaluation-in-progress / warning. The pulsing sidebar status dot uses it.
- **Alert Red** (`#f87171`): Fail / blocker / danger banners and notices.

### Tertiary
- **Signal Blue** (`#60a5fa`) and **Taxonomy Purple** (`#8b5cf6`): categorical accents for non-state classification (run types, taxonomy tags). Never used for primary action.

### Neutral
- **Void** (`#07090E`): app background, the deepest layer.
- **Panel** (`#0E131C`) / **Panel-2** (`#121924`) / **Panel-3** (`#0A0D15`) / **Panel Hover** (`#1A2333`): the surface ladder — sidebar/topbar/cards, raised controls, inset wells, and hover.
- **Border** (`#1e2733`) and **Border Strong** (`#2b3645`): hairlines and emphasized dividers; most dividers use a 12%-opacity slate (`rgba(148,163,184,0.12)`).
- **Ink ramp**: **Text** (`#e2e8f0`) body, **Text Strong** (`#f1f5f9`) headings, **Muted** (`#94a3b8`) secondary, **Faint** (`#64748b`) captions, **Faintest** (`#475569`) disabled.

### Named Rules
**The One Voice Rule.** Teal marks what the operator can act on or what is currently live — primary buttons, the active route, the current selection. It is never decoration. If teal appears on a surface the user can't act on, it's wrong.

**The Status-Hue Rule.** Emerald/amber/red mean exactly pass/pending/fail and nothing else. Never reach for red because a number is large, or green because it's positive — only because the gate verdict says so.

## 3. Typography

**Display / Body Font:** System sans (`-apple-system, Segoe UI, Roboto, …`)
**Label / Data Font:** JetBrains Mono (`ui-monospace, JetBrains Mono, Consolas, …`)

**Character:** One workhorse sans for prose and headings, paired with a monospace that does all the numeric and label work. The contrast axis is humanist-sans vs. mechanical-mono — not two similar sans families. The mono signals "this is a measured value," which is the whole job of the tool.

### Hierarchy
- **Title** (800, 17px, -0.01em): topbar page title; the single largest text on a screen.
- **Heading** (800, 14px, -0.01em): panel and section headings (`.panel-heading h3`, `.section-title`).
- **Body** (400, 12.5px, 1.6 line-height): summaries and prose; cap prose blocks at 65–75ch.
- **Data** (600–700, 12px, mono): every metric, price, ratio, and code token.
- **Label** (700, 10px, 0.12em, UPPERCASE mono): eyebrows, nav captions, pill/badge text, panel meta.

### Named Rules
**The Mono-for-Measures Rule.** Every number the user might compare, copy, or trust is monospace. Sans numbers are forbidden in data contexts — alignment and "this is a value" legibility depend on it.

**The Terminal-Label Rule.** Uppercase tracked mono labels are a deliberate system convention here (the data-desk dialect), not a decorative eyebrow. They are allowed to repeat across sections because they're structural wayfinding, not ornament — but keep them at 9–10px and `--faint`/`--teal`, never larger.

## 4. Elevation

Depth is conveyed by **tonal layering, not shadows**. Surfaces step through five near-black tones (`#07090E` → `#1A2333`); a 1px hairline (usually 12%-opacity slate) separates planes. The only shadows in the system are functional micro-accents: a faint teal glow under the brand mark and primary affordances. There are no ambient drop shadows on panels or cards.

### Shadow Vocabulary
- **Accent glow** (`box-shadow: 0 2px 10px rgba(20,184,166,0.25)`): brand mark and teal primary affordances only — signals "this is live/actionable," not elevation.

### Named Rules
**The Flat-Plane Rule.** Panels are flat. If a surface needs to read as "above" another, it moves up the tonal ladder (`panel` → `panel-2` → `panel-hover`); it does not cast a shadow. A drop shadow on a card is a 2014 tell and is forbidden here.

## 5. Components

### Buttons
- **Shape:** gently rounded (7px, `--radius-sm`); compact padding (8px 13px), `.mini` at 6px 11px.
- **Default:** `panel-2` fill, `border` hairline, `text` ink → hover lifts to `panel-hover`.
- **Primary (teal):** solid `#2dd4bf` on near-black ink (`#04201c`), weight 700 → hover brightens to `#5fe6d5`. Also `teal-outline`, `purple`, `blue` semantic variants.
- **Disabled:** opacity .45, `not-allowed` cursor.
- **Transitions:** 150ms on background/border only.

### Chips
- **Style:** pill (999px), `panel-3` fill, muted text, hairline border. Used for filters and toggles.
- **State:** active = teal text on `rgba(6,40,38,0.4)` tint with teal-tinted border. `.static` removes the pointer affordance for read-only tags.

### Cards / Containers (`.panel`)
- **Corner Style:** 10px (`--radius-md`).
- **Background:** `panel` on `bg`; nested wells drop to `panel-3`.
- **Shadow Strategy:** none — see Elevation (Flat-Plane Rule).
- **Border:** 1px soft slate (12% opacity).
- **Internal Padding:** 18px 20px; 20px bottom margin between panels.

### Pills & Badges (signature)
- **Status-pill** (5px 10px, 6px radius, uppercase mono) and **badge** (3px 8px, 5px radius): the core state-display vocabulary. Variants `.ok` (emerald), `.bad` (red), `.warn` (amber), `.teal`, `.purple`, `.neutral` — each pairs a tinted background, tinted border, and the hue, so state never relies on color alone (text label always present).

### Banners (signature)
- Three intents: `.info` (teal-tinted), `.warn` (amber), `.danger` (red), plus the top-level `.notice` (red). Each leads with a 34px round icon chip, an uppercase heading, and a one-line body. Used for stale-data, missing-evidence, and blocker messaging — honest states are first-class.

### Navigation
- **Style:** 256px fixed left sidebar, `panel` surface. Routes are 12px semibold sans with a 16px icon, default `muted` → hover tints background + `text`, **active** = teal text on `#15202E` with a teal-tinted border. Uppercase mono nav captions group routes. A pulsing status pill sits in the sidebar foot.

### Dots
- 8px round state indicators (`amber` pulses at 2s for pending; `teal`/`green`/`red` static) — the most compact state token, always paired with adjacent text.

## 6. Do's and Don'ts

### Do:
- **Do** keep teal (`#2dd4bf`) on actionable or live elements only — primary buttons, active route, current selection (The One Voice Rule).
- **Do** set every number, ratio, and code token in JetBrains Mono (The Mono-for-Measures Rule).
- **Do** convey depth by stepping the tonal ladder (`panel` → `panel-2` → `panel-hover`), never with drop shadows (The Flat-Plane Rule).
- **Do** pair every status color with a text label or icon, so pass/fail/stale survive colorblindness and grayscale.
- **Do** give stale, missing, and estimated data first-class banner/badge treatment — make it easy to see what NOT to trust.
- **Do** earn density with hierarchy: every dense block gets a heading and rhythm.

### Don't:
- **Don't** build the **cluttered legacy terminal** — no wall of undifferentiated numbers with no visual spine (MT4 / old-Bloomberg overload).
- **Don't** drift toward the **generic SaaS dashboard**: no hero-metric template, no gradient accents, no identical icon+heading+text card grids.
- **Don't** import **crypto/retail trading app** energy: no neon glow, no gamified hype green/red, no casino flash.
- **Don't** add **consumer-fintech** playfulness: no confetti, no oversized rounded P&L, no emotion-driven oversimplification.
- **Don't** use `background-clip: text` gradients, side-stripe `border-left` accents, or decorative glassmorphism — all forbidden.
- **Don't** color a number red because it's big or green because it's positive — status hues mean only the gate verdict (The Status-Hue Rule).
- **Don't** animate for decoration; motion conveys state only, 150ms, and respects `prefers-reduced-motion`.
