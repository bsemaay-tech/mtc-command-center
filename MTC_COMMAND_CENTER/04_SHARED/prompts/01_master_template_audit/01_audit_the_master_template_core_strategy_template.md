# 01 Audit The Master Template Core Strategy Template

**Short description**
This prompt asks you to audit a reusable Pine Script v5 strategy template called **MASTER TEMPLATE CORE** for architecture, correctness, and safety, and to output a strictly structured report that multiple LLMs can run identically.

---

### MASTER TEMPLATE CORE AUDIT PROMPT

**ROLE**
You are an expert Pine Script v5 **STRATEGY AUDITOR** and **TEMPLATE ARCHITECT**.

---

**CONTEXT**
I am building a reusable strategy template called **MASTER TEMPLATE CORE**.

* This is **not** a finished trading system; it is a **framework** with:

  * One example strategy block (currently **Supertrend-based**)
  * A central **engine** for:

    * trade direction toggles (enable long/short, allow flips)
    * global filters (MA, ADX, HTF trend, ATR volatility, etc.)
    * risk & position sizing
    * SL / TP / break-even / multi-TP / trailing stop
    * daily loss limits, max trades per day
    * JSON alert generation for automation (WunderTrading / webhooks)

Goal: later I will remove the Supertrend example and plug in other modules (MA crossover, RSI, candle pattern modules, etc.) **without touching** the core engine (risk, money management, alerts, filters).

Several different LLMs will run the **same prompt** on the **same code**, and I will merge the results. Your output must be **highly structured and deterministic**.

---

### GLOBAL RULES

* First line of your answer **must** be:
  `Model: <your model name here>`
* Do **not** rewrite, refactor, or extend the code. You only audit and propose an improvement plan.
* In the **Issues** section, list **only problems** (no fixes, no new features, no performance talk).
* Keep terminology precise so outputs from different LLMs are easy to compare and merge.

---

### WHAT TO CHECK

#### A) Template Architecture & Modularity

Check whether **MASTER TEMPLATE CORE** works as a clean reusable template:

* Is the **signal module** (entry/exit logic) clearly separated from:

  * risk engine
  * SL / TP / break-even / trailing / multi-TP
  * global filters
  * JSON alerts?
* Can another LLM/developer:

  * Delete the Supertrend logic,
  * Insert a different signal module,
  * Only edit a dedicated **Signal Plugin** section,
  * While preserving:

    * `longSignal_raw`, `shortSignal_raw`, `longSignal`, `shortSignal` (or equivalent public API),
    * all risk/SL/TP/trailing/daily-limit logic?

#### B) Public API & Engine Inputs

* Identify the **public API** from strategy logic â†’ engine:

  * Signals like `longSignal_raw`, `shortSignal_raw`, `longSignal`, `shortSignal`
  * Any helper series actually used by the engine (trend direction, filters, etc.)
* Confirm:

  * The engine uses these API signals,
  * No indicator-specific internals (e.g. raw Supertrend vars) are used outside the signal block.
* Flag any place where risk engine, filters, or alerts bypass the public API and depend on internal logic.

#### C) Correctness & Safety (STRICT PROBLEM SCAN)

Scan for problems in these areas:

1. **LOGICAL / MATH ERRORS**
   Wrong conditions, dead branches, bad comparisons, incorrect `ta.*` usage, `na`/indexing errors, etc.

2. **RISK & POSITION SIZING PROBLEMS**
   Risk larger than expected, misuse of `default_qty_type` / `default_qty_value`, leverage assumptions, incorrect risk-% logic, inconsistent use of `initial_capital` / equity / per-trade risk.

3. **REPAINT / DATA / EXECUTION RISKS**
   Misuse of `request.security`, lookahead, future data access, and order timing issues related to `process_orders_on_close`, `calc_on_every_tick`, etc.

4. **BUGS THAT CAN BREAK THE STRATEGY**
   Potential runtime errors, variables used before initialization, invalid function arguments, division by zero, etc.

#### D) Design Smells & Coupling

* Duplicated logic between:

  * signal module and filters, or
  * risk engine and signal module.
* Direct calls to `strategy.entry/exit/close` **inside** the signal module (usually should live in engine).
* Risk sizing or SL/TP calculations leaking into the signal section.
* Tight coupling to Supertrend:

  * Supertrend variable names used outside signal block,
  * Comments or structure that lock the template to that indicator.

#### E) Robustness & Clarity for Future Strategy Swaps

* Are input groups (`group=`) logically organized (Trade, Signal, Risk, SL/TP, Filters, Alerts, etc.)?
* Are comments/section headers clear enough so another LLM can:

  * remove Supertrend,
  * plug in a new strategy module safely?
* Any ambiguous naming or structure likely to mislead a future developer/LLM?

---

### OUTPUT FORMAT (STRICT)

Your answer **must** use this structure:

---

**Model line (single line)**
`Model: <your model name here>`

---

**1) TEMPLATE SUMMARY**

* Brief explanation of how the template is structured.
* One line with readiness:
  `Template readiness: Yes / Almost / No â€“ <short reason>`

---

**2) PUBLIC API DEFINITION**

List all public API items from strategy module â†’ engine.

For each item:

* Name (exact variable)
* Type (bool, float, int, series<bool>, etc.)
* Meaning / role
* Where it is **produced** (section)
* Where it is **consumed** (engine, filters, alerts, etc.)

---

**3) MODULARITY & COUPLING REVIEW**

Describe the **example strategy block**:

* Where it lives (section name and/or rough line range)
* How it connects to the engine (which variables it sets)
* Any unwanted dependencies between:

  * example block and
  * risk engine, filters, alerts, or other sections

Only describe problems here; do **not** modify code.

---

**4) ISSUES (STRICT PROBLEM LIST)**

List **only problems**, no fixes or suggestions.

Each bullet must follow this format:

* `[Category: LOGIC/RISK/REPAINT/RUNTIME/ARCHITECTURE] [Severity: HIGH/MEDIUM/LOW] â€“ Short title`

  * **Location:** section name and/or key variables
  * **What:** clear description of the problem
  * **Why itâ€™s a problem:** short explanation of impact

Rules:

* Bullet points only.
* No improvements, no new features, no refactors, no performance comments.

---

**5) OPTIONAL WARNINGS**

Non-fatal but suspicious or fragile patterns.

Format (same bullet style):

* `[Category: WARNING] [Severity: LOW/MEDIUM] â€“ Short title`

  * **Location:** â€¦
  * **What / Why:** short explanation

Examples: fragile naming, overly complex inputs, subtle timeframe quirks, etc.

---

**6) RISKS & PITFALLS FOR FUTURE STRATEGIES**

Explain what can break when a new strategy module is plugged in:

* E.g. â€œIf `longSignal_raw` is misused, engine misinterprets Xâ€,
* â€œIf a new module calls `strategy.entry` directly, daily-loss and risk controls breakâ€, etc.

Focus on **misuse scenarios** based on the issues found.

---

**7) ACTIONABLE IMPROVEMENT LIST**

Now describe conceptual fixes and improvements (no code).

For each item:

* `[Priority: HIGH/MEDIUM/LOW] â€“ Short title`

  * **Goal:** what this change achieves
  * **Linked issues:** which items from sections (4) / (5) it addresses
  * **Brief description:** what should be changed conceptually

Rules:

* Focus on safety, clarity, template reusability, and API cleanliness.
* Do **not** add new trading features/indicators; keep to robustness and maintainability.

---

**Final reminder**
Do **not** paste or rewrite the original code, and do **not** add new features.
Your job is to provide a precise, structured audit that multiple LLMs can run in a comparable way.
