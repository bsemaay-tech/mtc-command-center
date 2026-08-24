# Tier-B machine-grouping rules

Generated: 2026-08-24T19:56:34+03:00

Tier B is restricted to mechanically generated or product-irrelevant local tooling paths. Rules are applied in the listed order; Tier-A membership is the complement over the fixed-point tracked set plus the freshly enumerated untracked set. Evidence-marker paths are not grouped here.

## TB001

- Regex: `^\.agents/skills/`
- Matched count: **98**
- Rule: Locally installed agent-skill package files; tooling support, not product runtime or repository evidence.
- Spot-check method: deterministic spread across the sorted match list; 20 sample(s) inspected (at least 20 for this big rule).
- Tier-A exclusion result: PASS — every sample satisfies the stated generated/irrelevant rule; none carries a Tier-A evidence, migration, or canonical product path marker.

| Sample path | Spot-check result |
|---|---|
| .agents/skills/ask-matt/agents/openai.yaml | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/code-review/agents/openai.yaml | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/codebase-design/SKILL.md | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/domain-modeling/agents/openai.yaml | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/git-guardrails-claude-code/SKILL.md | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/grilling/SKILL.md | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/implement/agents/openai.yaml | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/loop-me/agents/openai.yaml | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/prototype/LOGIC.md | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/resolving-merge-conflicts/agents/openai.yaml | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/setup-matt-pocock-skills/domain.md | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/setup-matt-pocock-skills/triage-labels.md | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/setup-ts-deep-modules/SKILL.md | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/teach/agents/openai.yaml | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/teach/SKILL.md | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/to-tickets/SKILL.md | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/wait-what/agents/openai.yaml | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/wizard/SKILL.md | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/writing-for-agents/SKILL-MECHANICS.md | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |
| .agents/skills/writing-shape/SKILL.md | Path is confined to the local .agents/skills package tree and has no product/evidence path marker. |

## TB002

- Regex: `^skills-lock\.json$`
- Matched count: **1**
- Rule: Local skill-install lock metadata; generated tooling state rather than a product or evidence artefact.
- Spot-check method: deterministic spread across the sorted match list; 1 sample(s) inspected (all matches for this small rule).
- Tier-A exclusion result: PASS — every sample satisfies the stated generated/irrelevant rule; none carries a Tier-A evidence, migration, or canonical product path marker.

| Sample path | Spot-check result |
|---|---|
| skills-lock.json | Singleton lockfile is local agent-tool dependency state. |

## TB003

- Regex: `(^|/)(?:__pycache__|\.pytest_cache|\.mypy_cache|\.ruff_cache|\.coverage_cache)(/|$)|\.(?:pyc|pyo)$`
- Matched count: **0**
- Rule: Interpreter/test/lint cache or bytecode files.
- Spot-check method: deterministic spread across the sorted match list; 0 sample(s) inspected (all matches for this small rule).
- Tier-A exclusion result: PASS — every sample satisfies the stated generated/irrelevant rule; none carries a Tier-A evidence, migration, or canonical product path marker.

| Sample path | Spot-check result |
|---|---|
| (no matches) | Rule retained to make future grouping explicit; no path excluded in this run. |

## TB004

- Regex: `(^|/)(?:Thumbs\.db|\.DS_Store)$|(?:^|/)(?:~\$|\.~lock\.)|\.(?:swp|swo|tmp)$`
- Matched count: **0**
- Rule: Operating-system, editor, and transient temporary files.
- Spot-check method: deterministic spread across the sorted match list; 0 sample(s) inspected (all matches for this small rule).
- Tier-A exclusion result: PASS — every sample satisfies the stated generated/irrelevant rule; none carries a Tier-A evidence, migration, or canonical product path marker.

| Sample path | Spot-check result |
|---|---|
| (no matches) | Rule retained to make future grouping explicit; no path excluded in this run. |
<!-- end of Tier-B rules -->
