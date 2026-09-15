# Additional engineering plan — G2

Use only when the scope brief leaves a consequential interface, architecture, data-flow or
failure decision unresolved. Do not make a second plan for already-clear small work.

Builder: read the accepted scope, selected INPUTS/TESTS, relevant module contracts and protected
rules. Describe inputs -> existing modules -> observable outcome. Name the exact affected
interfaces, failure cases, recovery/rollback and parity/Pine/MTC impact. Prefer one vertical slice
with a working path. Preserve architecture unless a reproduced problem requires the scoped change.

Add exact QA command/cwd/environment and independently expected behavior to the same brief.
The Lead checks the plan against original authority before implementation; ask the owner only
for a retained material gate. Further PRD polishing ends once scope and sufficient evidence are
clear. Write-back only changed facts to the selected stage's current HANDOFF.
