Status: AMENDED DESIGN — SUPERSEDES V1 — NO CODE CHANGE, NOT ACCEPTED

# Pathscope Option C — occurrence-accounting redesign, amended design V2

Date: 2026-08-15
Design-worktree baseline: `87a4edb7f7cb0ab9263f9f28419d30355159fccb`
Frozen R5 prover blob: `695ca9c951e31f53da9580d41326583d71086bb3`
Frozen R5 prover SHA-256: `28848D60F74A7C668DB3019BBAC58550F4A55C1C02038C013153316C711EDF9C`

## 0. Review-closure map

This document is complete and supersedes V1; the implementer must not treat V1 as a second
source of requirements. The `SOUND-WITH-GAPS` review's four required findings and six notes
are all adopted, with one logical clarification called out below.

Citation shorthand below: `V1:<lines>` means
`PATHSCOPE_OPTION_C_DESIGN_2026-08-15.md:<lines>`; `review:<lines>` means
`PATHSCOPE_OPTION_C_DESIGN_REVIEW_2026-08-15.md:<lines>`.

| Review item | Disposition | Closed here |
|---|---|---|
| Finding 1 — assignment-bearing parameter expansion bypasses admission | Adopted: a narrow fail-closed admission-boundary guard; no grammar widening | §§2.1, 2.2, 3.1, 9.3, 10.1, 11.1, 12.1 |
| Finding 2 — reason/reading consistency exists only in prose | Adopted as runtime invariants plus mutations | §§4, 5, 10.5 |
| Finding 3 — composite contract is underspecified | Adopted: exact prefixes, headers, summary rule, reconciliation, precedence, and terminal table | §§2.3, 7.1–7.3, 8, 10.5, 12.7 |
| Finding 4 — §7 accidentally changes argv-only projection rows | Adopted: occurrence formatting is scoped to member-derived evidence only | §§7, 9.1, 10.5 |
| Note 5 — globally unique member IDs and per-instance analyzer prefix | Adopted | §§3.3, 4, 7, 10.5 |
| Note 6 — a one-member bare scalar remains a usable disclosed hole | Adopted; the compatibility PASS token is not the claim authority | §§5, 9.2, 11.2 |
| Note 7 — generic `Issue` dedupe is count-only, not a usable hole | Adopted | §§2.2, 7, 11.6 |
| Note 8 — whole-value path-shape test is ambiguous | Adopted with an exact ordered predicate | §§3.3, 5 |
| Note 9 — member-ID line field conflicts with rebased display lines | Adopted by removing line numbers from IDs | §§3.3, 7 |
| Note 10 — retired fences must be itemized | Adopted; `GREEN_R5.txt` and all seven named digests are explicit | §§9.4, 12.6 |

The review's reason-consistency sentence groups `whole_container_decomposed` with scalar
reasons and then says those reasons require no active colon/words reading
(`PATHSCOPE_OPTION_C_DESIGN_REVIEW_2026-08-15.md:241-250`). Taken literally, that makes the
container reason impossible: V1 defines it specifically for a whole which owns active child
readings (`PATHSCOPE_OPTION_C_DESIGN_2026-08-15.md:264-266`). This V2 follows the review's
enforceable intent: all three reasons are legal only on `reading=whole`; the two *scalar*
reasons require no active child reading, while `whole_container_decomposed` requires one.
That clarification preserves the closed classifier and the two-verdict-change regression
contract instead of silently deleting the container disposition.

## 1. Authority, scope, and gate contract

Barış authorized one accounting-layer redesign in which every admitted member reaches
exactly one terminal disposition, followed by one fresh flagship execution audit. He did
not authorize an open-ended repair sequence; the parser is kept and the reporting layer is
replaced (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:8-28`).

This amendment round changes one documentation file and no executable byte. Its artifact
tier is T2. No other AI is dispatched because the amendment kickoff explicitly forbids
sub-delegation. The later implementation is one local, non-economic T1 work package under
the explicit owner contract; the one fresh execution audit decides acceptance. A required
finding from that audit returns the lane to the owner boundary.

Allowed in this round: this V2 file only. Forbidden in this round: every line of
`pathscope_prover.py` and `composite_pathproof.py`; all Pine, parity, MTC, and trading
surfaces; and all host, network, deployment, service, credential, broker/exchange, ARM,
order, TESTNET/mainnet, merge, push, and economic action.

The design value remains the V1 architecture: declare the occurrence universe once, keep
stable identity through classification and reporting, and prove conservation before PASS.
This is not another list of dangerous variable names or three more recognizers.

## 2. Source diagnosis and exact implementation boundary

The current prover says coverage is fail-closed and zero facts plus PASS is a bug
(`pathscope_prover.py:2-17`), but the assignment path loses occurrence identity:

- `record_assignment_value` expands one whole RHS and reduces provenance to one source set
  before members exist (`pathscope_prover.py:1319-1370`).
- `record_assignment_members` constructs whole and optional word/list candidates, string-
  deduplicates through `pool`, reduces repeated empties to one Boolean, and emits nothing
  for `bare` members (`pathscope_prover.py:1430-1510`).
- `output_report` groups `Use` objects by normalized value, set-deduplicates issues and
  evidence, and only then selects the verdict (`pathscope_prover.py:2942-3016`).

“Accounting layer” therefore means admission of a script assignment value, expansion trace,
occurrence enumeration, member-local provenance, total terminal classification, immutable
ledgers, occurrence records, compatibility projection, and downstream reconciliation. It
does not mean only the final print loop.

### 2.1 Kept machinery, with one narrow fail-closed exception

The following behavior remains outside the redesign:

- `ShellLexer` tokenization, quote handling, heredoc collection, and substitution harvesting
  (`pathscope_prover.py:138-452`);
- the rendered text and known/unknown semantics of `expand_word`, apart from trace metadata
  (`pathscope_prover.py:514-647`);
- constants and allowlist parsing (`pathscope_prover.py:650-754`);
- registered argv roles and path/endpoint normalization (`pathscope_prover.py:757-1094,
  681-719`);
- command, wrapper, redirection, function, control-flow, and nested-source traversal, except
  for the guard below (`pathscope_prover.py:1512-2933`);
- CLI/input plumbing (`pathscope_prover.py:3019-3040`); and
- the lexical-only claim: no host probe, symlink resolution, or mount proof
  (`pathscope_prover.py:2-17,2936-2939`).

**Narrow exception required by the review.** V1 called all of
`pathscope_prover.py:1512-2933` kept (`PATHSCOPE_OPTION_C_DESIGN_2026-08-15.md:60-61`), but
the raw-argument branch at `scan_args` expands an operand and silently discards an unknown
value whenever `Spec.path_free` is true (`pathscope_prover.py:1555-1570`). `:`, `true`,
`printf`, and `echo` all have data-only grammars and therefore qualify as path-free
(`pathscope_prover.py:813-826,1021-1023,1048-1049`). The current expander rejects `:=` as
an unsupported parameter expansion (`pathscope_prover.py:607-623`), so
`: ${LD_PRELOAD:=/etc/evil.so}` reaches that silent branch.

V2 follows review finding 1, not V1's over-broad “kept” sentence (`review:230-240`). The implementation changes
the current `scan_args` branch at **`pathscope_prover.py:1555-1570`, specifically the
path-free exemption at lines 1564-1570**, so an execution-active assignment-bearing
parameter-expansion shape cannot use the exemption. A small quote-aware helper may be
placed adjacent to that branch, but no other traversal rule in `1512-2933` changes for this
fix.

The helper classifies active `${...}` forms before the exemption:

1. any top-level parameter operator `=` or `:=` is `ASSIGNMENT_EFFECT`;
2. a nested or malformed `${...}` whose effect cannot be proved non-assigning is
   `EFFECT_UNKNOWN`; and
3. quoted literal text and parameter forms proved non-assigning are `NO_ASSIGNMENT_EFFECT`.

Both `ASSIGNMENT_EFFECT` and `EFFECT_UNKNOWN` emit one ordinary coverage `Issue` with a
stable reason (`assignment_parameter_expansion_not_modeled` or
`parameter_expansion_effect_ambiguous`) even when `path_free` is true. The path therefore
terminates at rc 3 through the existing generic-issue branch. It creates no admitted value,
does not execute or emulate the assignment, and does not bind the resulting environment.
Single-quoted literal `${X:=v}` and supported non-assigning `${X:-v}` remain controls.

This is intentionally smaller and safer than widening admission. Widening would require the
accounting layer to model Bash's conditional assignment state, side effects, nesting, and
subsequent environment reachability. The guard proves only what is needed: an unmodeled
assignment side effect cannot disappear into a path-free carrier. The owner authorized a
class-closing accounting redesign, and the review says deferral—not closure—would require a
new decision (`PATHSCOPE_OPTION_C_DESIGN_REVIEW_2026-08-15.md:230-240,288-297`); this V2 does
not defer it.

### 2.2 Replaced and extended seam

| Current source | Required implementation disposition |
|---|---|
| `Value`, `Use` (`pathscope_prover.py:74-93`) | Add immutable expansion segments and optional member identity without changing legacy rendered-value semantics. |
| `expand_word` (`514-647`) | Produce an ordered source-to-rendered trace together with the same rendered text, known/unknown outcome, and transitive constant-source set. |
| `Analyzer.__init__` (`1119-1128`) | Receive a shared run context; add analyzer/value ordinals and admitted-value, member, disposition, and accounting-fault ledgers. |
| `merge` (`1218-1223`) | Merge ledgers without dedupe; rebase display lines only; never rewrite IDs. |
| Assignment functions (`1319-1510`) | Replace value/member accounting with admission, span-preserving splits, total classification, and one disposition per occurrence; remove `pool` and `empty_member`. |
| Three admission routes (`1267-1317,1741-1797,2564-2572`) | Keep reachability and environment binding; each assignment token occurrence creates exactly one admitted value. |
| `scan_args` (`1555-1570`) | Add only the fail-closed assignment-effect guard in §2.1; do not admit the side effect. |
| `Analyzer.run`/nested analyzers (`2866-2933`) | Allocate per-instance analyzer IDs from the shared context and carry immutable ledgers through merges. |
| `output_report`/`main` (`2942-3040`) | Replace value-first adjudication with occurrence-first adjudication, mandatory legacy projection, conditional accounting grammar, and strict precedence. |
| `SubprocessPathProver` (`composite_pathproof.py:2129-2391`) | Parse and reconcile the additive grammar, retain the mandatory projection, and implement the terminal contract in §7.3. |

Generic `Issue` dedupe may remain for non-member parser/coverage issues: it only collapses
identical issue multiplicity and cannot erase the existence of every issue
(`pathscope_prover.py:1131-1134,2961-2964`). No member or member disposition may use that
container.

### 2.3 Downstream machine-grammar seam

`SubprocessPathProver` currently admits only a fixed prefix tuple, rejects unknown records,
requires exactly one standard header of each type, reconciles projection and generic-issue
counts, validates projection dispositions, and then selects among generic-issue, forbidden,
and pass branches (`composite_pathproof.py:2272-2376`). The accounting grammar is therefore
a required part of the same T1 implementation work package, not an optional follow-up.

The mandatory implementation is the additive grammar in §§7.1–7.3. Hiding the ledger in a
`uses=` field, labeling a scalar as `PATH`, omitting occurrence rows from the downstream
records tuple, or relying on unknown-line rejection is forbidden. The generic
`ProverMemberResult.records` field can carry the added records without changing its data
type, and the later recorder already forwards each string as a `PROVER_RECORD`
(`composite_pathproof.py:511-525,2377-2390,2655-2680`).

## 3. Exact definitions

### 3.1 Admitted value and the admission guard

An **admitted value** is one occurrence of a script-side `NAME=VALUE` assignment reaching
the common accounting call through exactly one existing route:

1. assignment prefix or standalone assignment (`pathscope_prover.py:2564-2568`);
2. `env` assignment after expanded `ASSIGN_RE` recognition
   (`pathscope_prover.py:1741-1797`); or
3. `local`, `declare`, `typeset`, `export`, or `readonly` after raw or expanded
   `NAME=VALUE` recognition (`pathscope_prover.py:1267-1317,2569-2572`).

Admission occurs before successful RHS expansion. A raw assignment with an opaque RHS is
admitted and receives one opaque whole member with an unresolved disposition. An `env` or
declaration operand that cannot be established as an assignment retains its existing
coverage STOP. Constants-file entries are preregistered inputs, not admitted script values
(`pathscope_prover.py:650-668`). Every token occurrence is separate even when text, line,
normalized value, and primitive are identical.

The §2.1 guard is part of the **admission boundary**, but guarded `${X:=v}` is deliberately
not admitted. It stops because the analyzer cannot safely establish or model the side
effect. This keeps the accounting universe precise while closing the silent pre-admission
escape.

### 3.2 Expansion trace and exact source substring

Expansion of an admitted RHS produces:

`ExpansionTrace(raw_rhs, rendered_text, segments)`

Each immutable segment carries half-open rendered offsets, half-open token-local raw
offsets, the exact raw and rendered substrings, origin kind, and exact transitive
preregistered-constant sources. Origin kinds cover literal, escape, quote elision,
parameter expansion, fallback expansion, and semantic PWD substitution.

Rendered non-empty segments are ordered, non-overlapping, and cover every rendered
character exactly once. Zero-output syntax may have zero-width rendered segments. Segment
concatenation must reconstruct `rendered_text`; any gap, overlap, range error, or mismatch
is an accounting fault. Token-local offsets are honest because `Token` has text and line,
but no column or absolute byte position (`pathscope_prover.py:67-71`).

### 3.3 Member occurrence, reading, shape, and identity

A member is an occurrence, never a string key:

`MemberOccurrence(member_id, value_id, reading, ordinal, rendered_span, raw_slices, text)`

The deterministic splitter admits these readings without a danger predicate:

1. `whole`: exactly one member for every admitted value, including empty and opaque values;
2. `colon`: when a live `:` exists outside a URI `scheme://authority` span, every separator
   creates ordered `n + 1` slices, including every empty (`pathscope_prover.py:1400-1428`);
3. `words`: whitespace plus at least two non-empty `\S+` matches always creates every word
   occurrence; V1's option-or-slash activation is removed (`pathscope_prover.py:1459-1462`);
4. `word-colon`: each word containing a live colon also creates all nested colon members,
   while retaining the word occurrence.

Reading order is `whole`, `colon`, `words`, `word-colon`; source order is final within a
reading. Independent cardinality checks require colon count `separator_count + 1` and words
count equal to the `\S+` match count before disposition accounting.

Shape classification is ordered and exact:

```text
endpoint_shaped(x) = URI_SCHEME_RE matches x
path_shaped(x) = x starts with '/', './', or '../'
                 OR ('/' occurs in x AND x does not start with '-')
```

Endpoint shape is tested before path shape, matching the current ordered kind test
(`pathscope_prover.py:1390-1398`). Thus `bare.so:/etc/escape.so` is path-shaped as a whole;
it takes the path/endpoint classifier arm, not the container arm. Its colon children are
still independently present and classified.

An `AccountingRunContext` allocates a monotonically increasing **per-instance analyzer
creation ordinal**. Root is `A0000`; every nested shell or command-substitution analyzer
gets the next ordinal at construction, in deterministic traversal order. IDs are, for
example, `A0000.V0007.colon.M0002`. They contain no line number. Analyzer ordinal, value
ordinal, reading, and member ordinal distinguish all instances; rendered text, normalized
value, analyzer *kind*, and display line never participate. Merge rebases only display
lines (`pathscope_prover.py:1218-1223,2925-2932`).

### 3.4 Terminal disposition

A terminal disposition is one immutable record keyed by one `member_id`, chosen from:

- `ALLOWED_WITH_REASON`;
- `FORBIDDEN_WITH_REASON`; or
- `UNRESOLVED_FAIL_CLOSED`.

Candidate normalization, allowlist result, provenance, and rule token are fields on that
single disposition. They are not additional dispositions.

## 4. Conservation and reason/reading consistency — accepting invariants

For every admitted value `v`:

- `M(v)` is the multiset of IDs emitted by the immutable splitter;
- `D(v)` is the multiset of IDs on terminal dispositions; and
- `S(v,r)` is the independently counted separator/match set for reading `r`.

The runtime checks all of the following after splitting and again before reporting:

```text
|M(v)| >= 1
Counter(M(v)) == Counter(D(v))
for each member_id in M(v): Counter(D(v))[member_id] == 1
for each reading r: |M(v,r)| == grammar_cardinality(S(v,r))
no disposition references an ID outside M(v)
every disposition belongs to the closed enum
all value_ids are unique across the run
all member_ids in ⊎v M(v) are globally unique across the run
⊎v M(v) == ⊎v D(v)
```

The global member-ID assertion is independent of the Counter equality; a collision across
two values must fault even when both Counters contain it twice. This closes the gap identified
at review lines 102-109 and 266-270.

The following **reason/reading rules are runtime invariants**, not classifier prose:

1. every `words` and `word-colon` member is
   `UNRESOLVED_FAIL_CLOSED reason=consumer_word_semantics_unmodeled`, regardless of any
   candidate path, endpoint, or allowlist match;
2. `whole_scalar_no_lexical_sink`, `empty_scalar_no_lexical_sink`, and
   `whole_container_decomposed` are legal only for `reading=whole`;
3. `whole_scalar_no_lexical_sink` and `empty_scalar_no_lexical_sink` require no active
   colon, words, or word-colon reading for that value;
4. `whole_container_decomposed` requires at least one active colon/words child reading,
   successful independent cardinality checks, and the complete child occurrence set; it
   authenticates no child;
5. a bare colon member cannot use any scalar/container ALLOW reason and is
   `UNRESOLVED_FAIL_CLOSED reason=member_consumer_search_unmodeled`;
6. an allowed colon path/endpoint member requires a non-empty exact member-provenance set
   and an exact rendered allowlist rule token on the same disposition; an empty colon member
   requires exact `{PWD}` provenance and its matching PWD allowlist rule;
7. `ALLOWED_WITH_REASON reason=member_allowlisted` requires a resolved path/endpoint,
   successful member-local rule match, required exact provenance, and `rule != -`;
8. `FORBIDDEN_WITH_REASON reason=member_outside_allowlist` requires a resolved candidate
   and failed rule context; and
9. every disposition/reason/reading combination not enumerated above or in §5 is an
   accounting fault, not a convenient default bucket.

Any violation emits `accounting_invariant_failed`; it cannot be downgraded to an ordinary
member unresolved result. PASS additionally requires: no accounting fault; no existing
generic parse, coverage, path, endpoint, or provenance issue; every member disposition
allowed; and no forbidden or unresolved disposition. An admitted value therefore cannot
PASS with zero printed member facts.

## 5. Closed, ordered terminal classifier

| Disposition | Exact class | Run effect |
|---|---|---|
| `ALLOWED_WITH_REASON` | Member-local allowlisted path/endpoint with required exact provenance and rule token; empty colon member resolved through pinned PWD and allowlisted; `reading=whole` scalar reason under §4; or `reading=whole reason=whole_container_decomposed` with complete active child readings. | Eligible for rc 0 only if every other invariant and member also allows. |
| `FORBIDDEN_WITH_REASON` | Resolved path/endpoint candidate with at least one required use outside the allowlist; carries normalized candidate and failed rule context. | rc 1 only if no accounting fault, generic issue, or unresolved member exists. |
| `UNRESOLVED_FAIL_CLOSED` | Opaque expansion; words/word-colon consumer semantics; bare colon search semantics; unmodeled option member; unavailable PWD; missing exact provenance; ambiguous reading; failed normalization; or default arm. | rc 3. |

The total classifier order is:

1. opaque expansion or normalization failure → unresolved;
2. `words` or `word-colon` → unresolved, retaining candidate facts only as fields;
3. empty colon member → resolve through PWD, then allow, forbid, or unresolved;
4. any other endpoint-shaped or path-shaped member → member-local allow, forbid, or
   provenance unresolved;
5. non-endpoint, non-path `whole` with active child reading →
   `whole_container_decomposed` only after child/cardinality proof;
6. empty `whole` with no active child reading → `empty_scalar_no_lexical_sink`;
7. non-empty `whole` with no endpoint/path/list/whitespace shape and no active child reading
   → `whole_scalar_no_lexical_sink`;
8. bare member in colon/words/word-colon → unresolved; and
9. anything else → `UNRESOLVED_FAIL_CLOSED reason=member_classifier_no_terminal_rule`.

The whole-container eligibility test uses the exact shape predicates in §3.3. This pins the
row set for mixed values rather than letting the implementer choose step 4 or 5. Existing
unresolved precedence remains stricter than forbidden precedence
(`pathscope_prover.py:3009-3016`).

The one-member bare whole scalar class is deliberately retained for regression compatibility.
It is no longer silent, but it does not prove loader, PATH, module, or executable search
semantics; §11.2 states that usable limitation plainly.

## 6. Member-local provenance

For each non-empty member `m`:

```text
expected_sources(m) = union(segment.sources for segments intersecting m.rendered_span)
actual_sources(m) == expected_sources(m)
```

Members split from one parameter expansion may legitimately share that parameter's source.
Adjacent literal text does not inherit the RHS-wide union. An empty colon member has a
zero-width boundary anchor and semantic PWD value; its sources are exactly `{PWD}` when PWD
is pinned, never `RHS_sources ∪ {PWD}`. The current union in the empty-member arm is removed
(`pathscope_prover.py:1498-1510`).

Every member record prints escaped raw slices, rendered span/text, and member-local sources.
The runtime recomputes the equality before verdict selection. For
`$ROOT/lib:/safe/literal`, the first colon member names `ROOT`; the literal neighbor names no
constant and, even if allowlisted, terminates unresolved for missing exact provenance. An
RHS-wide source union is an accounting fault.

## 7. Identity, reporting, mandatory projection, and composite grammar

The value/member/disposition ledgers are ordered sequences. No dictionary keyed by text,
line, normalized path, endpoint, primitive, or evidence owns the accounting universe.
Duplicate values and repeated empty members remain separate records, sorted only by
analyzer/value/reading/member ordinals.

Required source changes:

- remove `pool` and membership-dedupe tests (`pathscope_prover.py:1473-1490`);
- replace `empty_member` with one occurrence per zero-width slice
  (`pathscope_prover.py:1476-1510`);
- keep member dispositions out of generic `Issue` and report set dedupe
  (`pathscope_prover.py:1131-1134,2961-2964`);
- replace set-deduplicated evidence and RHS-wide sources **only for member-derived uses**;
  and
- retain the grouped PATH/ENDPOINT table as a **mandatory compatibility projection**. It
  cannot decide conservation, provenance, or PASS.

The scope on bullet 4 is strict. A projection group containing only argv-derived `Use`
objects must run the current grouping, sorting, rule, evidence, and source code unchanged,
so its `PATH`/`ENDPOINT` row—including `uses=` and `sources=`—is byte-identical
(`pathscope_prover.py:2943-3003`). A group with member-derived evidence includes every
contributing `member_id` in stable member order; legacy evidence items remain in their
current format. The projection's `sources=` is only a compatibility aggregate; MEMBER rows
remain provenance authority.

V1 called this projection optional (`V1:81,332-334`), while its own byte-identity promise
requires the existing argv-only projection (`V1:386-391`). V2 follows the review and makes
the projection mandatory because removing it or changing all evidence rows would falsify
that promise (`review:190-192,260-265`).

### 7.1 Exact additive prover grammar

For every invocation that reaches `output_report` and the accounting-reporting boundary,
the standard output order is:

1. exactly one `PATHSCOPE shell=` header;
2. exactly one unchanged semantics header;
3. exactly one resolved-count header;
4. exactly one five-kind unresolved-count header;
5. mandatory PATH/ENDPOINT projection rows and generic UNRESOLVED rows;
6. the conditional accounting block below; and
7. exactly one terminal verdict row.

The existing standard headers are required on **every accounting-reporting path**, including
`accounting_invariant_failed`, because the composite currently requires exactly one of each
(`composite_pathproof.py:2275-2305`). Their counts continue to reconcile only the printed
projection and generic UNRESOLVED rows. Existing earlier CLI input-read/input-parse exits at
`pathscope_prover.py:3027-3038` are not redesigned by this statement.

The accounting block admits exactly these new record prefixes:

- `PATHSCOPE accounting_summary=`;
- `VALUE_ACCOUNT` followed by one ASCII space;
- `MEMBER` followed by one ASCII space; and
- `ACCOUNTING_FAULT` followed by one ASCII space.

The composite adds those exact prefixes to `known_lines`; all other unknown lines still
STOP as `prover_output_unknown_record` (`composite_pathproof.py:2287-2293`). Strict regular
expressions, fixed field order, single field occurrence, and deterministic ASCII escaping
are required. The normative shapes are:

```text
PATHSCOPE accounting_summary=<OK|FAIL> admitted_value_count=<n> member_count=<m> disposition_count=<d> accounting_fault_count=<k>
VALUE_ACCOUNT value_id=<id> line=<display-line> site=<escaped-site> member_count=<m> disposition_count=<d> conserved=<true|false>
MEMBER member_id=<id> value_id=<id> reading=<whole|colon|words|word-colon> ordinal=<n> rendered_span=<a:b> raw_slices=<escaped> text=<escaped> sources=<escaped-set> disposition=<enum> reason=<token> rule=<escaped-or-dash> candidate_domain=<fs|net|none> candidate_value=<escaped-or-dash>
ACCOUNTING_FAULT value_id=<id-or-NONE> member_id=<id-or-NONE> reason=<stable-token>
```

Every `<escaped...>` field is one whitespace-free token: `b64u:` followed by the unpadded
base64url encoding of the field's UTF-8 bytes; an empty string is `b64u:` and an absent
optional field is `-`. `raw_slices` encodes a canonical no-whitespace JSON array in source
order before base64url conversion. `sources` is `-` or a comma-separated lexical sort of
`NAME_RE` constant names. IDs, enum values, integers, booleans, spans, and stable reason
tokens have their own closed ASCII grammars and are never base64-wrapped. This makes exact
raw spelling reversible without allowing whitespace or `=` inside a field to forge another
record field.

One MEMBER line is the serialized join of one immutable member and its one terminal
disposition. On an `OK` path, the number of MEMBER rows must equal both summary counts;
duplicates reveal duplicate dispositions and omissions reveal a missing side of the join.

### 7.2 Accounting-summary emission and reconciliation

The emission rule is exact:

- if `admitted_value_count == 0` and `accounting_fault_count == 0`, emit **zero** accounting
  summaries and zero VALUE_ACCOUNT/MEMBER/ACCOUNTING_FAULT rows;
- otherwise emit **exactly one** accounting summary;
- `summary=OK` requires `fault_count=0`, one VALUE_ACCOUNT per admitted value, one MEMBER per
  member/disposition pair, globally unique value/member IDs, per-value and global count
  equality, `conserved=true`, and zero ACCOUNTING_FAULT rows; and
- `summary=FAIL` requires `fault_count > 0`, exactly that many ACCOUNTING_FAULT rows, stable
  diagnostic rows for every safely serializable ledger item, and terminal rc 3. A failed
  summary is never accepted even if partial counts happen to balance.

The zero-summary case is what preserves §9.1 byte identity for assignment-free fixtures.
The composite accepts zero summaries only when every other new-prefix count is also zero.
When any accounting row exists, missing or duplicate summary is grammar-incomplete.

This explicitly resolves V1's conflict between “exactly one accounting summary” (`V1:370`)
and assignment-free byte identity (`V1:386-391`). V2 follows the review's required
reconciliation (`review:181-188,251-259`): zero summaries is the only legal no-admission,
no-fault case; otherwise exactly one is mandatory.

For `summary=OK`, the composite independently recomputes per-value MEMBER counts, verifies
VALUE_ACCOUNT totals, checks every value reference, checks global ID uniqueness, validates
the closed disposition enum and reason/reading table, and reconciles all four summary
counts before terminal adjudication. For `summary=FAIL`, it verifies the summary/fault
grammar and fault cardinality, then returns STOP without pretending the broken ledger can
be accepted.

All accounting summary, VALUE_ACCOUNT, MEMBER, and ACCOUNTING_FAULT strings are included in
`ProverMemberResult.records` together with PATH, ENDPOINT, and UNRESOLVED strings, so the
later composite evidence stream does not discard the new proof
(`composite_pathproof.py:2377-2390,2655-2680`).

### 7.3 Composite precedence and exact terminal-reason table

The composite performs grammar/header/count reconciliation first. It then applies this
ordered table; no later branch may override an earlier one:

| Precedence | Condition | Prover terminal required | Composite result/reason |
|---|---|---|---|
| 1 | accounting summary is `FAIL` with positive reconciled fault count | `REJECT rc=3 reason=accounting_invariant_failed` | `STOP / prover_accounting_invariant_failed` |
| 2 | no accounting fault; sum of the five generic issue counts is positive | `REJECT rc=3 reason=static_resolution_incomplete` | `STOP / prover_static_resolution_incomplete` |
| 3 — new fourth semantic arm | zero generic issues; `summary=OK`; at least one MEMBER is `UNRESOLVED_FAIL_CLOSED` | `REJECT rc=3 reason=member_resolution_incomplete` | `STOP / prover_member_resolution_incomplete` |
| 4 | no unresolved condition; any MEMBER or projection row is forbidden | `REJECT rc=1 reason=path_outside_allowlist` | `FAIL / prover_forbidden_operand` |
| 5 | no fault, issue, unresolved, or forbidden record | `PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope` | `PASS / prover_closed_and_allowlisted_lexical_scope` |

Row 3 is the required rc-3-with-zero-generic-issue branch. It is selected from MEMBER
dispositions before `has_forbid`, so an unresolved bare list member cannot fall into the
current forbid or pass arms (`composite_pathproof.py:2354-2376`). Row 1 is an accounting-
fault pre-arm because a broken ledger cannot safely participate in the four normal semantic
branches. Process rc must equal terminal rc on every row, preserving the existing check
(`composite_pathproof.py:2350-2353`).

The retained PASS reason is a byte-compatibility token, not proof of variable-specific
consumer semantics. Auditor-facing claims are derived from MEMBER reason tokens and §11,
not from reading more into that legacy terminal string.

After `_invoke_member` accepts row 5, the existing outer `prove` zero-resolved-facts guard
may still conservatively turn a prover PASS into composite STOP; that guard and the later
member-result aggregation are outside terminal parsing and remain unchanged
(`composite_pathproof.py:2423-2435`).

## 8. Fail-closed accounting-fault output

Any trace, identity, split-cardinality, global-uniqueness, provenance, reason/reading,
closed-enum, Counter, serialization, or printed-record reconciliation failure emits the
four standard headers, any fully formed projection/generic issue rows, then an accounting
block of this form:

```text
PATHSCOPE accounting_summary=FAIL admitted_value_count=<n> member_count=<m> disposition_count=<d> accounting_fault_count=<positive-k>
ACCOUNTING_FAULT value_id=<id-or-NONE> member_id=<id-or-NONE> reason=<stable-token>
PATHSCOPE verdict=REJECT rc=3 reason=accounting_invariant_failed
```

There are exactly `k` fault records. Fully serializable VALUE_ACCOUNT/MEMBER rows appear in
stable identity order for diagnosis, but cannot make a failed summary acceptable. No PASS
terminal prints. The process returns `RC_PARSE` 3, the existing incomplete/static-stop code
(`pathscope_prover.py:30-31,3009-3011`). An exception at the accounting boundary is converted
to a stable fault; it does not escape as a traceback or become rc 1.

## 9. Regression-preservation contract

### 9.1 Bytes that remain identical

Fixture bytes, constants, allowlists, pinned R1/R3/R4 prover blobs, and pinned RP6/RP7 block
blobs remain unchanged (`SELF_QA_PATHSCOPE.md:275-307,309-491`). Existing `$CASES`,
`$C2CASES`, and `$C3CASES` remain intact (`SELF_QA_PATHSCOPE.md:493-609`). Existing
`RED_R1.txt`, `RED_R3.txt`, and `RED_R4.txt` bytes/hashes remain reproducible; the R5 source
blob is newly frozen as the literal Option-C RED subject.

Against the redesigned prover, every published fixture in `SELF_QA_PATHSCOPE.md:310-384`
that admits no script assignment remains byte-identical. The known assignment-admitting
exceptions are `green`, `assembled`, `dynamic`, `nested`, and `backtick`; they gain the
conditional accounting block. Assignment-free runs emit no accounting summary or new
prefix, and argv-only projection rows execute the unchanged formatting path in §7.

No parser, command role, path normalization, endpoint normalization, or allowlist result
outside the explicit seam may change. The admission guard changes only previously silent
assignment-effect shapes on registered path-free argv routes; its controls remain unchanged.

### 9.2 Same semantic result, added accounting records

- All seven P9 fixtures retain current rc and candidate facts
  (`SELF_QA_PATHSCOPE.md:677-703`).
- P10/P11 retain every observed dangerous candidate and rc except §9.3's two deliberate
  existing-fixture changes.
- `c3_empty_only` and `_out` remain rc 0 and rc 1, with two separate colon-empty member
  dispositions rather than one collapsed PWD row (`V1:406-407`; `review:200-207`).
- `assign_benign` and `c2_benign_scalars` remain rc 0; every `IFS=:` occurrence is reported
  (`V1:408-409`; `review:200-207`).
- `c2_bare_soname` and `c3_scalar_ctl` remain rc 0 through the explicit whole-scalar reason,
  not silence (`V1:410-411`; `review:200-207`).
- RP6-P0 and RP7-WPI-RO remain rc 3 under placeholder and real constants; no forbidden or
  unresolved fact disappears (`V1:412-414`; `review:196-211`).

For assignment-admitting fixtures, compare the complete new report to its new fence and a
named mandatory legacy-candidate projection to R5. Any projection delta needs a row-level
reason. The legacy PASS token cannot be cited to erase MEMBER-level residuals.

### 9.3 Authorized semantic tightening

Exactly two existing fixture verdicts may tighten:

1. `c2_benign_words`: rc 0 → rc 3 because all multiword values create words members and
   each words member is runtime-bound to unresolved consumer semantics; and
2. `c3_colon_whole`: rc 1 → rc 3 because the forbidden whole and allowed `$BASE` candidate
   remain, while bare colon member `relative` becomes unresolved.

The review independently traced the complete published assignment fixture inventory and
confirmed these as the only two predicted rc changes (`review:194-211`).

No other existing rc change is authorized. The new `${X:=v}` family is additive, not an
existing fixture verdict change. If any other old fixture changes rc, implementation stops
and explains reachability before any fence update.

### 9.4 One-time fences that explicitly retire

The current working-tree prover drives `GREEN_R5.txt` and the determinism loop
(`SELF_QA_PATHSCOPE.md:650-672`), so these R5-derived fences retire once code changes:

1. `GREEN_R5.txt` and its published hash;
2. determinism digest `find_exec`;
3. determinism digest `assign_prefix`;
4. determinism digest `c2_list_prefix`;
5. determinism digest `c3_ws_relative`;
6. determinism digest `c4_export_quoted`;
7. determinism digest `RP6-P0`; and
8. determinism digest `RP7-WPI-RO`.

Those seven names and current digest lines are published at
`SELF_QA_PATHSCOPE.md:138-144`; `GREEN_R5.txt` is published at lines 122 and 135. The
implementation edits the harness once to reconstruct blob
`695ca9c951e31f53da9580d41326583d71086bb3` as `pathscope_prover_R5.py`. It writes the
candidate's existing-suite fence as `GREEN_OPTION_C.txt`, keeps new attacks in a separate
`$OPTION_C_CASES` list, and writes that list as `RED_R5_OPTION_C.txt` under the frozen R5
blob and `GREEN_OPTION_C_ATTACKS.txt` under the candidate. It also reproduces the old full
suite under the frozen blob as `R5_BASELINE.txt`; that file must match the retired
`GREEN_R5.txt` bytes/hash, but is a baseline, never the new GREEN claim. This preserves the
existing RED transcript identities because no new case is appended to their lists. The
implementation updates the published stdout block at
`SELF_QA_PATHSCOPE.md:127-145` with literal output from the edited harness. The fixture
families and old RED identities do not retire.

“Run the full harness verbatim” henceforth means the committed, explicitly re-fenced
Option-C harness, not pretending the old working-tree GREEN identity can survive a prover
change. Old and new commands/output remain recorded for D026.

## 10. Falsification plan

Every new regression is closure evidence only after literal RED against frozen R5 (or an
equivalent deliberate mutation) and GREEN against the redesigned bytes, with exact commands
and real output. Static reasoning alone is supplemental.

### 10.1 Admission-boundary and F1 attacks

Run each carrier with an unset target:

```bash
: ${LD_PRELOAD:=/etc/evil.so}
true ${LD_PRELOAD:=/etc/evil.so}
echo ${LD_PRELOAD:=/etc/evil.so}
printf '%s\n' ${LD_PRELOAD:=/etc/evil.so}
: ${LD_PRELOAD=/etc/evil.so}
```

R5 is expected to PASS these through the path-free exemption identified at
`pathscope_prover.py:1555-1570`; Option C must emit a coverage UNRESOLVED row and terminal
`REJECT rc=3 reason=static_resolution_incomplete`, with no admitted-value claim. Execute R5
before calling that RED. Controls `: '${LD_PRELOAD:=/etc/evil.so}'` and supported
non-assigning `${ROOT:-/fallback}` must not be rejected by the assignment-effect guard.

Also run the original F1 attacks:

```bash
GIT_SSH_COMMAND="ssh evil.example" cat "$ROOT/f"
LD_LIBRARY_PATH=$URL:evil.so cat "$ROOT/f"
```

The first creates two unresolved words members. The second creates an allowed URL member
with exact provenance and an unresolved bare colon member. Conservation may pass; terminal
rc must be 3.

### 10.2 F2 — provenance laundering

```bash
LD_LIBRARY_PATH=$ROOT/lib:/safe/literal cat "$ROOT/f"
```

`$ROOT/lib` intersects ROOT; the literal member intersects no constant segment. The literal
member is unresolved for exact provenance. Mutating member-local intersection back to the
whole-trace union must produce an accounting fault before verdict.

### 10.3 F3 — duplicates and repeated empties

```bash
LD_LIBRARY_PATH=/etc/escape:/etc/escape cat "$ROOT/f"
LD_LIBRARY_PATH=:: cat "$ROOT/f"
```

The first produces two distinct forbidden colon members. The second has two separators and
therefore three colon-empty PWD members plus its distinct whole container member. Restoring
text dedupe must violate the Counter equation; restoring the one-empty Boolean must also
violate independent separator cardinality.

### 10.4 Adjacent attacks

| Attack | Exact input | Required closure |
|---|---|---|
| Endpoint normalization collision and provenance | `X=$URL:http://127.0.0.1:8790/other cat "$ROOT/f"` | Two endpoint occurrences survive; the literal neighbor cannot inherit URL provenance. |
| Interleaved empties | `LD_LIBRARY_PATH=::$ROOT/lib:: cat "$ROOT/f"` | Four separators require five colon members: four empties and one ROOT path. |
| Quoted newline words | `GIT_SSH_COMMAND="ssh\nevil.example" cat "$ROOT/f"`, with a literal newline | Words reading is unconditional and every word terminates unresolved. |
| Same-line duplicate values | `X=/etc/escape X=/etc/escape cat "$ROOT/f"` | Distinct value and member IDs survive reporting. |
| Mixed whole shape | `X=bare.so:/etc/escape.so cat "$ROOT/f"` | Whole takes the exact path-shaped arm; colon bare/path children remain separate. |
| Cross-analyzer identity | Two same-line command substitutions containing identical assignments | Per-instance analyzer ordinals keep every value/member ID distinct. |

These predictions must first be measured against frozen R5. No predicted RED is evidence
until executed.

### 10.5 Required mutations

The implementation harness deliberately applies each mutation and records literal output.
In-prover invariant mutations must produce rc 3 with
`reason=accounting_invariant_failed` and no PASS:

1. delete one disposition append;
2. duplicate one disposition append;
3. reference an unknown member ID;
4. return an unknown disposition enum;
5. dedupe members before assigning identity while leaving separator counts intact;
6. attach a non-intersecting constant source to a literal member;
7. suppress one printed MEMBER while keeping its in-memory disposition;
8. mark a bare colon member `ALLOWED_WITH_REASON reason=whole_scalar_no_lexical_sink`;
9. mark a words member allowed with any scalar/container reason;
10. apply a scalar reason to a whole with an active colon or words reading;
11. allow a colon member without an exact rule token or exact member provenance;
12. force two different values to reuse one member ID;
13. replace per-instance analyzer ordinals with kind labels so two nested analyzers collide;
14. emit `whole_container_decomposed` without complete/cardinality-checked children; and
15. suppress the accounting summary while retaining VALUE_ACCOUNT or MEMBER rows.

Composite-contract mutations must make `SubprocessPathProver` STOP before accepting the
terminal line:

16. remove the member-unresolved zero-generic-issue arm and feed a summary-OK unresolved
    member report;
17. pair `summary=FAIL` with any terminal reason other than
    `accounting_invariant_failed`;
18. omit or duplicate a standard header on the accounting-fault path;
19. duplicate a global member ID or falsify a VALUE_ACCOUNT count in an otherwise OK report;
20. omit a member-derived ID from the mandatory PATH/ENDPOINT projection; and
21. inject an unknown accounting prefix.

Compatibility mutations must fail byte comparison:

22. emit an accounting summary on an assignment-free fixture; and
23. change `uses=` or `sources=` formatting on a projection group containing only argv uses.

Arms 8–11 are the discriminating reason/reading tests required by review finding 2. Arms
12–13 close note 5. Arms 15–23 prove the composite and byte-identity promises rather than
merely restating them.

## 11. Honest residuals

This redesign does not prove:

1. **Semantic support for assignment-bearing parameter expansion `${X:=v}` or `${X=v}`.**
   The §2.1 guard closes the demonstrated silent PASS by STOPping assignment-effect or
   ambiguous forms on the registered `scan_args` path. It deliberately does not admit,
   evaluate, or bind those side effects. It also does not claim complete Bash coverage of
   every context in which an assignment-bearing expansion could occur. Any such construct
   outside the guarded argv route remains unproved parser/grammar coverage, not something
   conservation can see. The exact demonstrated form is named here rather than hidden under
   “parser/grammar.”
2. **Consumer-specific meaning of a one-member bare whole scalar.**
   `LD_PRELOAD=evil.so`, `LD_LIBRARY_PATH=.`, `PYTHONPATH=dir`, and
   `GIT_SSH_COMMAND=toolname` can still PASS through
   `whole_scalar_no_lexical_sink`. This is a usable, disclosed hole retained from R5, not a
   dynamic-loader or search-path proof. The authoritative narrow claim is the MEMBER reason;
   the legacy terminal PASS string overstates it.
3. **Which alternate reading a real consumer chooses.** The conservative union can
   over-reject prose, as `c2_benign_words` demonstrates.
4. **Attached option-path extraction.** An option member such as `-I/usr/include` is
   unresolved; the embedded candidate is not proven.
5. **Absolute source byte columns.** Current tokens have no column
   (`pathscope_prover.py:67-71`); exact token-local slices plus stable IDs are the available
   identity.
6. **Multiplicity of non-member generic issues.** Existing equality dedupe can collapse
   identical generic issues, including through 240-character expression truncation
   (`pathscope_prover.py:1131-1134,2961-2964`). It cannot remove the existence of every
   issue, so it has no usable PASS hole; member ledgers never use it.
7. **Host object identity.** Lexical allowlisting establishes no symlink target, mount
   boundary, file existence, namespace, or runtime open (`pathscope_prover.py:2-17,
   2936-2939`).
8. **Downstream acceptance before the composite integration is implemented and tested.**
   New prefixes are currently rejected and the three current adjudication branches do not
   understand member-unresolved or accounting-fault output
   (`composite_pathproof.py:2287-2305,2354-2376`). This integration is mandatory and
   non-trivial; it requires its own parser, reconciliation, mutation, and terminal tests.
9. **Independent downstream re-parsing of Bash admission.** Conditional summary emission
   preserves assignment-free bytes, but the composite does not independently parse the shell
   to prove that summary absence means no admitted value. Admission completeness remains a
   prover responsibility, fenced at all three admission routes plus the §2.1 guard.
10. **Correction of unrelated conservative composite behavior.** The current prover prints
    `ALLOW-LEXICAL` for both PATH and ENDPOINT projections
    (`pathscope_prover.py:2982-3003`), while the current composite accepts `ALLOW` (not
    `ALLOW-LEXICAL`) for an allowed ENDPOINT (`composite_pathproof.py:2343-2348`). That
    pre-existing mismatch can over-STOP an allowed endpoint but cannot produce a false PASS.
    It is not silently changed by this accounting design; if it blocks the mandated suite,
    it must be reported for owner adjudication rather than folded into an unrelated repair.

These residuals bound the printable claim: every admitted assignment-member occurrence has
one exact, reported terminal disposition under the stated lexical readings; unmodeled
assignment-effect argv cannot silently cross the admission boundary. They do not establish
complete shell semantics, consumer search semantics, or runtime filesystem safety.

## 12. Implementation-round acceptance checklist

The one implementation round is incomplete until all are true:

1. changes stay inside §2's accounting seam plus the exact `scan_args:1555-1570` guard;
   no other kept traversal behavior changes;
2. no `pool`, member-text dedupe, normalized-value identity, or single-empty Boolean owns
   the member universe;
3. trace reconstruction, independent reading cardinality, global ID uniqueness, Counter
   equality, provenance equality, reason/reading consistency, enum closure, serialization,
   and printed-record reconciliation all run before PASS;
4. every admission-boundary, F1/F2/F3, and §10.4 attack has literal frozen-R5 RED and current
   GREEN evidence;
5. every §10.5 mutation is demonstrably discriminating under D026;
6. the edited Option-C harness runs verbatim with outer rc 0, empty stderr, no transcript
   leak, old RED identities reproduced, exactly two existing fixture rc changes, and the
   retired `GREEN_R5.txt` plus all seven determinism digests explicitly re-fenced;
7. `SubprocessPathProver` admits only the exact new prefixes, keeps all four standard
   headers on fault, enforces conditional summary cardinality, independently reconciles OK
   ledgers, implements the accounting-fault and member-unresolved arms, requires the
   mandatory projection, and forwards every accounting record;
8. argv-only PATH/ENDPOINT rows are byte-identical, including `uses=` and `sources=`;
9. Python 3.12 parsing and installed-runtime execution both succeed; inability to run an
   actual 3.12 interpreter is reported honestly;
10. stderr is empty, output is deterministic, and no machine-specific path leaks into a
    transcript; and
11. the one fresh flagship execution auditor receives the frozen diff, complete literal
    harness output, exact RED/GREEN commands/output, every mutation result, and this V2—no
    implementer-session context.

Only that fresh execution audit may decide acceptance. A required finding returns the lane
to the owner boundary; it does not authorize a second implementation round.
