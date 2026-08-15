#!/usr/bin/env python3
"""Adversarial Option-C accounting mutations for the published self-QA harness."""

from __future__ import annotations

import argparse
import base64
import contextlib
import dataclasses
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import types
from typing import Any


def load_module(name: str, path: Path, source: str | None = None) -> Any:
    if source is None:
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {name}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(source, str(path), "exec"), module.__dict__)
    return module


def invoke(prover: Path, fixture_dir: Path, name: str) -> tuple[int, str, str]:
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(prover),
            f"{name}.sh",
            "constants.env",
            "allowlist.txt",
        ],
        cwd=fixture_dir,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="strict",
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("frozen_r5", type=Path)
    parser.add_argument("composite", type=Path)
    parser.add_argument("fixture_dir", type=Path)
    args = parser.parse_args()

    args.candidate = args.candidate.resolve()
    args.frozen_r5 = args.frozen_r5.resolve()
    args.composite = args.composite.resolve()
    args.fixture_dir = args.fixture_dir.resolve()

    prover = load_module("pathscope_option_c_candidate", args.candidate)
    composite = load_module("pathscope_option_c_composite", args.composite)
    environment = prover.parse_constants(args.fixture_dir / "constants.env")
    rules = prover.parse_allowlist(args.fixture_dir / "allowlist.txt", environment)

    def analyzer(name: str) -> Any:
        text = (args.fixture_dir / f"{name}.sh").read_text(encoding="utf-8")
        result = prover.Analyzer(text, environment, rules)
        result.run()
        return result

    mutation_count = 0

    def execute_mutation(label: str, result: Any) -> None:
        nonlocal mutation_count
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            rc = prover.output_report(Path(f"{label}.sh"), rules, result)
        lines = stream.getvalue().splitlines()
        terminal = next(
            (line for line in lines if line.startswith("PATHSCOPE verdict=")),
            "MISSING",
        )
        summary = next(
            (line for line in lines if line.startswith("PATHSCOPE accounting_summary=")),
            "MISSING",
        )
        faults = sum(line.startswith("ACCOUNTING_FAULT ") for line in lines)
        passed = any("verdict=PASS" in line for line in lines)
        if not (
            rc == 3
            and terminal
            == "PATHSCOPE verdict=REJECT rc=3 reason=accounting_invariant_failed"
            and "accounting_summary=FAIL" in summary
            and faults > 0
            and not passed
        ):
            raise RuntimeError(f"{label} did not fail closed")
        mutation_count += 1
        print(
            f"MUTATION {label} rc={rc} summary=FAIL faults={faults} "
            f"pass_present={str(passed).lower()} terminal=accounting_invariant_failed"
        )

    # 1. A split member with no disposition.
    item = analyzer("f3_duplicate")
    item.dispositions.pop()
    execute_mutation("M01_delete_disposition", item)

    # 2. A split member with two dispositions.
    item = analyzer("f3_duplicate")
    item.dispositions.append(item.dispositions[0])
    execute_mutation("M02_duplicate_disposition", item)

    # 3. A disposition for a member that was never split.
    item = analyzer("f3_duplicate")
    item.dispositions[0] = dataclasses.replace(
        item.dispositions[0], member_id="A0000.V0000.colon.M9999"
    )
    execute_mutation("M03_unknown_member", item)

    # 4. A disposition outside the closed enum.
    item = analyzer("f3_duplicate")
    item.dispositions[0] = dataclasses.replace(
        item.dispositions[0], disposition="UNKNOWN_ENUM"
    )
    execute_mutation("M04_unknown_enum", item)

    # 5. Restore text dedupe while retaining the independent separator count.
    item = analyzer("f3_duplicate")
    victim = next(member for member in item.members if member.member_id.endswith("colon.M0001"))
    item.members.remove(victim)
    item.dispositions = [
        disposition
        for disposition in item.dispositions
        if disposition.member_id != victim.member_id
    ]
    item.admitted_values[0] = dataclasses.replace(
        item.admitted_values[0],
        member_ids=tuple(member.member_id for member in item.members),
    )
    execute_mutation("M05_member_dedupe", item)

    # 6. Launder ROOT provenance onto the literal /safe/literal member.
    item = analyzer("f2_provenance")
    member = next(member for member in item.members if member.member_id.endswith("colon.M0001"))
    member_index = item.members.index(member)
    item.members[member_index] = dataclasses.replace(
        member, sources=frozenset({"ROOT"})
    )
    disposition = next(
        disposition
        for disposition in item.dispositions
        if disposition.member_id == member.member_id
    )
    disposition_index = item.dispositions.index(disposition)
    item.dispositions[disposition_index] = dataclasses.replace(
        disposition,
        disposition=prover.DispositionKind.ALLOWED_WITH_REASON,
        reason="member_allowlisted",
        rule="/safe/**",
        sources=frozenset({"ROOT"}),
    )
    execute_mutation("M06_provenance_launder", item)

    # 7. Suppress one printed MEMBER after in-memory conservation succeeds.
    item = analyzer("f3_duplicate")
    records = prover._accounting_records(item)
    records.remove(next(row for row in records if row.startswith("MEMBER ")))
    prover.reconcile_accounting_records(item, records)
    execute_mutation("M07_suppress_member_record", item)

    # 8. Give a bare colon member a whole-scalar ALLOW reason.
    item = analyzer("f1_uri_bare")
    disposition = next(
        disposition
        for disposition in item.dispositions
        if disposition.member_id.endswith("colon.M0001")
    )
    index = item.dispositions.index(disposition)
    item.dispositions[index] = dataclasses.replace(
        disposition,
        disposition=prover.DispositionKind.ALLOWED_WITH_REASON,
        reason="whole_scalar_no_lexical_sink",
    )
    execute_mutation("M08_bare_colon_scalar_allow", item)

    # 9. Give a words member a whole-scalar ALLOW reason.
    item = analyzer("f1_command_words")
    disposition = next(
        disposition for disposition in item.dispositions if ".words." in disposition.member_id
    )
    index = item.dispositions.index(disposition)
    item.dispositions[index] = dataclasses.replace(
        disposition,
        disposition=prover.DispositionKind.ALLOWED_WITH_REASON,
        reason="whole_scalar_no_lexical_sink",
    )
    execute_mutation("M09_words_scalar_allow", item)

    # 10. Use a scalar reason while colon children are active.
    item = analyzer("f3_empty")
    disposition = next(
        disposition for disposition in item.dispositions if ".whole." in disposition.member_id
    )
    index = item.dispositions.index(disposition)
    item.dispositions[index] = dataclasses.replace(
        disposition, reason="whole_scalar_no_lexical_sink"
    )
    execute_mutation("M10_scalar_with_children", item)

    # 11. Allow a colon candidate without its exact rule/provenance proof.
    item = analyzer("f2_provenance")
    disposition = next(
        disposition
        for disposition in item.dispositions
        if disposition.member_id.endswith("colon.M0001")
    )
    index = item.dispositions.index(disposition)
    item.dispositions[index] = dataclasses.replace(
        disposition,
        disposition=prover.DispositionKind.ALLOWED_WITH_REASON,
        reason="member_allowlisted",
        rule=None,
    )
    execute_mutation("M11_allow_without_rule_provenance", item)

    # 12. Force two values to reuse one member ID.
    item = analyzer("adjacent_duplicate_values")
    first, second = item.members[:2]
    item.members[1] = dataclasses.replace(second, member_id=first.member_id)
    item.dispositions[1] = dataclasses.replace(
        item.dispositions[1], member_id=first.member_id
    )
    item.admitted_values[1] = dataclasses.replace(
        item.admitted_values[1], member_ids=(first.member_id,)
    )
    execute_mutation("M12_cross_value_member_collision", item)

    # 13. Collapse two analyzer-instance prefixes.
    item = analyzer("adjacent_cross_analyzer")
    old, new = "A0002.V0000", "A0001.V0000"
    value_index = next(
        index for index, value in enumerate(item.admitted_values) if value.value_id == old
    )
    value = item.admitted_values[value_index]
    item.admitted_values[value_index] = dataclasses.replace(
        value,
        value_id=new,
        member_ids=tuple(member_id.replace(old, new, 1) for member_id in value.member_ids),
    )
    item.members = [
        dataclasses.replace(
            member,
            value_id=new,
            member_id=member.member_id.replace(old, new, 1),
        )
        if member.value_id == old
        else member
        for member in item.members
    ]
    item.dispositions = [
        dataclasses.replace(
            disposition,
            value_id=new,
            member_id=disposition.member_id.replace(old, new, 1),
        )
        if disposition.value_id == old
        else disposition
        for disposition in item.dispositions
    ]
    execute_mutation("M13_analyzer_prefix_collision", item)

    # 14. Keep the container reason after deleting one required child.
    item = analyzer("f3_empty")
    victim = next(member for member in item.members if member.member_id.endswith("colon.M0002"))
    item.members.remove(victim)
    item.dispositions = [
        disposition
        for disposition in item.dispositions
        if disposition.member_id != victim.member_id
    ]
    item.admitted_values[0] = dataclasses.replace(
        item.admitted_values[0],
        member_ids=tuple(member.member_id for member in item.members),
    )
    execute_mutation("M14_incomplete_container", item)

    # 15. Suppress the summary while retaining VALUE_ACCOUNT/MEMBER rows.
    item = analyzer("f3_duplicate")
    records = prover._accounting_records(item)
    records.remove(
        next(row for row in records if row.startswith("PATHSCOPE accounting_summary="))
    )
    prover.reconcile_accounting_records(item, records)
    execute_mutation("M15_suppress_summary", item)

    attack_names = (
        "guard_colon", "guard_true", "guard_echo", "guard_printf", "guard_equal",
        "control_single_quote", "control_fallback", "f1_command_words", "f1_uri_bare",
        "f2_provenance", "f3_duplicate", "f3_empty", "adjacent_endpoint",
        "adjacent_interleaved_empty", "adjacent_newline", "adjacent_duplicate_values",
        "adjacent_mixed_whole", "adjacent_cross_analyzer",
    )
    candidate_reports = {
        name: invoke(args.candidate, args.fixture_dir, name)
        for name in attack_names + ("find_exec", "literal")
    }
    frozen_reports = {
        name: invoke(args.frozen_r5, args.fixture_dir, name) for name in attack_names
    }
    if any(stderr for _rc, _stdout, stderr in candidate_reports.values()):
        raise RuntimeError("candidate stderr is not empty")
    if any(stderr for _rc, _stdout, stderr in frozen_reports.values()):
        raise RuntimeError("frozen-R5 stderr is not empty")

    expected_frozen_rc = {
        name: 0 for name in attack_names
    }
    expected_frozen_rc.update({
        "f3_duplicate": 1,
        "adjacent_duplicate_values": 1,
        "adjacent_mixed_whole": 3,
        "adjacent_cross_analyzer": 3,
    })
    expected_candidate_rc = {
        "guard_colon": 3, "guard_true": 3, "guard_echo": 3, "guard_printf": 3,
        "guard_equal": 3, "control_single_quote": 0, "control_fallback": 0,
        "f1_command_words": 3, "f1_uri_bare": 3, "f2_provenance": 3,
        "f3_duplicate": 1, "f3_empty": 0, "adjacent_endpoint": 3,
        "adjacent_interleaved_empty": 0, "adjacent_newline": 3,
        "adjacent_duplicate_values": 1, "adjacent_mixed_whole": 3,
        "adjacent_cross_analyzer": 3,
    }
    for name in attack_names:
        frozen_rc = frozen_reports[name][0]
        candidate_rc = candidate_reports[name][0]
        if frozen_rc != expected_frozen_rc[name] or candidate_rc != expected_candidate_rc[name]:
            raise RuntimeError(
                f"{name} RED/GREEN rc mismatch: "
                f"R5={frozen_rc} candidate={candidate_rc}"
            )

    def member_fields(name: str) -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        for line in candidate_reports[name][1].splitlines():
            if not line.startswith("MEMBER "):
                continue
            fields = dict(part.split("=", 1) for part in line.split()[1:])
            rows.append(fields)
        return rows

    def require(name: str, condition: bool, closure: str) -> None:
        if not condition:
            raise RuntimeError(f"{name} attack closure failed: {closure}")
        print(
            f"ATTACK {name} r5_rc={frozen_reports[name][0]} "
            f"candidate_rc={candidate_reports[name][0]} closure={closure}"
        )

    for name in attack_names[:5]:
        output = candidate_reports[name][1]
        require(
            name,
            "kind=coverage reason=assignment_parameter_expansion_not_modeled" in output
            and "accounting_summary=" not in output,
            "assignment_effect_guard",
        )
    for name in ("control_single_quote", "control_fallback"):
        require(
            name,
            candidate_reports[name][1] == frozen_reports[name][1],
            "byte_identical_control",
        )

    rows = member_fields("f1_command_words")
    require(
        "f1_command_words",
        len(rows) == 3
        and len({row["member_id"] for row in rows}) == 3
        and sum(row["reading"] == "words" for row in rows) == 2
        and all(
            row["reason"] == "consumer_word_semantics_unmodeled"
            for row in rows if row["reading"] == "words"
        ),
        "two_unresolved_words",
    )
    rows = member_fields("f1_uri_bare")
    require(
        "f1_uri_bare",
        len(rows) == 3
        and any(
            row["reading"] == "colon" and row["sources"] == "-"
            and row["reason"] == "member_consumer_search_unmodeled"
            for row in rows
        ),
        "bare_colon_unresolved",
    )
    rows = member_fields("f2_provenance")
    literal_row = next(
        (row for row in rows if row["member_id"].endswith("colon.M0001")),
        None,
    )
    literal_slices = None
    if literal_row is not None and literal_row["raw_slices"].startswith("b64u:"):
        payload = literal_row["raw_slices"][5:]
        payload += "=" * (-len(payload) % 4)
        literal_slices = json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))
    require(
        "f2_provenance",
        len(rows) == 3
        and literal_row is not None
        and literal_row["sources"] == "-"
        and literal_row["reason"] == "member_exact_provenance_missing"
        and literal_slices == [{
            "origin": "literal",
            "raw_end": 39,
            "raw_start": 26,
            "raw_text": "/safe/literal",
        }],
        "literal_member_sources_none",
    )
    rows = member_fields("f3_duplicate")
    duplicate_children = [row for row in rows if row["reading"] == "colon"]
    require(
        "f3_duplicate",
        len(duplicate_children) == 2
        and len({row["member_id"] for row in duplicate_children}) == 2
        and len({row["candidate_value"] for row in duplicate_children}) == 1,
        "two_distinct_duplicate_members",
    )
    rows = member_fields("f3_empty")
    empty_children = [row for row in rows if row["reading"] == "colon"]
    require(
        "f3_empty",
        len(rows) == 4 and len(empty_children) == 3
        and len({row["member_id"] for row in empty_children}) == 3
        and all(row["text"] == "b64u:" and row["sources"] == "PWD" for row in empty_children),
        "three_distinct_empty_members",
    )
    rows = member_fields("adjacent_endpoint")
    require(
        "adjacent_endpoint",
        len(rows) == 3
        and sum(row["candidate_domain"] == "net" for row in rows) == 3
        and any(row["sources"] == "-" and row["reading"] == "colon" for row in rows),
        "endpoint_occurrences_and_local_provenance",
    )
    rows = member_fields("adjacent_interleaved_empty")
    colon_rows = [row for row in rows if row["reading"] == "colon"]
    require(
        "adjacent_interleaved_empty",
        len(colon_rows) == 5 and sum(row["text"] == "b64u:" for row in colon_rows) == 4,
        "five_colon_members_four_empty",
    )
    rows = member_fields("adjacent_newline")
    require(
        "adjacent_newline",
        len(rows) == 3 and sum(row["reading"] == "words" for row in rows) == 2,
        "quoted_newline_two_words",
    )
    rows = member_fields("adjacent_duplicate_values")
    require(
        "adjacent_duplicate_values",
        len(rows) == 2 and len({row["value_id"] for row in rows}) == 2,
        "same_line_value_ids_distinct",
    )
    rows = member_fields("adjacent_mixed_whole")
    require(
        "adjacent_mixed_whole",
        len(rows) == 3
        and any(row["reading"] == "whole" and row["candidate_domain"] == "fs" for row in rows)
        and sum(row["reading"] == "colon" for row in rows) == 2,
        "path_shaped_whole_and_colon_children",
    )
    rows = member_fields("adjacent_cross_analyzer")
    analyzer_prefixes = {row["value_id"].split(".", 1)[0] for row in rows}
    require(
        "adjacent_cross_analyzer",
        len(rows) == 4 and analyzer_prefixes == {"A0000", "A0001", "A0002"},
        "global_analyzer_ordinals_distinct",
    )

    unresolved_rc, unresolved_output, _ = candidate_reports["f1_command_words"]
    pass_rc, pass_output, _ = candidate_reports["f3_empty"]

    def composite_stop(
        label: str,
        adapter: Any,
        rc: int,
        output: str,
        expected_reason: str | None = None,
    ) -> None:
        result = adapter._interpret_output(label, rc, output, "")
        if result.verdict.value != "STOP" or (
            expected_reason is not None and result.reason != expected_reason
        ):
            raise RuntimeError(f"{label} composite parser accepted a mutation")
        print(f"COMPOSITE_MUTATION {label} verdict=STOP reason={result.reason}")

    # 16. Remove the member-unresolved semantic arm in an in-memory parser mutant.
    composite_source = args.composite.read_text(encoding="utf-8")
    anchor = 'elif accounting_state == "OK" and has_member_unresolved:'
    if composite_source.count(anchor) != 1:
        raise RuntimeError("M16 source anchor count is not one")
    composite_mutant = load_module(
        "pathscope_option_c_composite_mut16",
        args.composite,
        composite_source.replace(anchor, "elif False:", 1),
    )
    composite_stop(
        "M16_removed_member_arm",
        composite_mutant.SubprocessPathProver(),
        unresolved_rc,
        unresolved_output,
    )

    # Build a real FAIL-summary output for the remaining contract mutations.
    item = analyzer("f3_duplicate")
    item.dispositions.pop()
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        fault_rc = prover.output_report(Path("fault.sh"), rules, item)
    fault_output = stream.getvalue()

    # 17. Pair summary FAIL with the wrong terminal reason.
    composite_stop(
        "M17_fault_wrong_terminal",
        composite.SubprocessPathProver(),
        fault_rc,
        fault_output.replace(
            "reason=accounting_invariant_failed",
            "reason=static_resolution_incomplete",
            1,
        ),
        "prover_accounting_terminal_mismatch",
    )

    # 18. Omit and duplicate a mandatory standard header.
    pass_lines = pass_output.splitlines()
    omitted = "\n".join(
        line for line in pass_lines if not line.startswith("PATHSCOPE semantics=")
    ) + "\n"
    composite_stop(
        "M18a_omitted_header",
        composite.SubprocessPathProver(),
        pass_rc,
        omitted,
        "prover_output_grammar_incomplete",
    )
    semantics = next(line for line in pass_lines if line.startswith("PATHSCOPE semantics="))
    duplicated = pass_output.replace(semantics, semantics + "\n" + semantics, 1)
    composite_stop(
        "M18b_duplicate_header",
        composite.SubprocessPathProver(),
        pass_rc,
        duplicated,
        "prover_output_grammar_incomplete",
    )

    # 19. Duplicate a global member ID and falsify VALUE_ACCOUNT cardinality.
    serialized_members = [line for line in pass_lines if line.startswith("MEMBER ")]
    first_id = serialized_members[0].split(" member_id=", 1)[1].split(" ", 1)[0]
    second_id = serialized_members[1].split(" member_id=", 1)[1].split(" ", 1)[0]
    composite_stop(
        "M19a_duplicate_member_id",
        composite.SubprocessPathProver(),
        pass_rc,
        pass_output.replace(second_id, first_id),
    )
    composite_stop(
        "M19b_value_count",
        composite.SubprocessPathProver(),
        pass_rc,
        pass_output.replace(
            "member_count=4 disposition_count=4 conserved=true",
            "member_count=99 disposition_count=4 conserved=true",
            1,
        ),
        "prover_value_account_count_mismatch",
    )

    # 20. Remove a member identity from the mandatory projection.
    composite_stop(
        "M20_projection_omission",
        composite.SubprocessPathProver(),
        pass_rc,
        pass_output.replace(",member_id=A0000.V0000.colon.M0001", "", 1),
        "prover_member_projection_mismatch",
    )

    # 21. Add an unknown accounting prefix.
    composite_stop(
        "M21_unknown_prefix",
        composite.SubprocessPathProver(),
        pass_rc,
        pass_output.replace(
            "PATHSCOPE accounting_summary=", "PATHSCOPE accounting_extra=", 1
        ),
        "prover_output_unknown_record",
    )

    # 22. Assignment-free output must remain byte-identical; an added summary fails.
    old_literal_rc, old_literal, old_literal_err = invoke(
        args.frozen_r5, args.fixture_dir, "literal"
    )
    new_literal_rc, new_literal, new_literal_err = candidate_reports["literal"]
    if old_literal_err or new_literal_err or old_literal_rc != new_literal_rc or old_literal != new_literal:
        raise RuntimeError("assignment-free literal compatibility baseline changed")
    injected_summary = new_literal.replace(
        "PATHSCOPE verdict=",
        "PATHSCOPE accounting_summary=OK admitted_value_count=0 member_count=0 "
        "disposition_count=0 accounting_fault_count=0\nPATHSCOPE verdict=",
        1,
    )
    result = composite.SubprocessPathProver()._interpret_output(
        "M22_summary_on_assignment_free", new_literal_rc, injected_summary, ""
    )
    if injected_summary == old_literal or result.verdict.value != "STOP":
        raise RuntimeError("M22 did not fail compatibility/composite checks")
    print(
        "COMPAT_MUTATION M22_summary_on_assignment_free byte_equal=false "
        f"composite=STOP reason={result.reason}"
    )

    # 23. An argv-only projection remains byte-identical; formatting drift fails compare.
    old_argv_rc, old_argv, old_argv_err = invoke(args.frozen_r5, args.fixture_dir, "find_exec")
    new_argv_rc, new_argv, new_argv_err = candidate_reports["find_exec"]
    if old_argv_err or new_argv_err or old_argv_rc != new_argv_rc or old_argv != new_argv:
        raise RuntimeError("argv-only compatibility baseline changed")
    changed_argv = new_argv.replace("sources=ROOT", "sources=ROOT,ROOT", 1)
    if changed_argv == old_argv:
        raise RuntimeError("M23 did not change bytes")
    print("COMPAT_MUTATION M23_argv_projection_format byte_equal=false")

    if mutation_count != 15:
        raise RuntimeError(f"expected 15 in-prover mutations, got {mutation_count}")
    print("OPTION_C_MUTATIONS PASS arms=23 checks=25")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
