"""Structural tests for the inert KVM2 Linux deployment package.

No test starts a service/server, touches a firewall, accesses a VPS, reads a
secret, or contacts a network endpoint.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from bridge.app import STATE_DB_ENV_VAR, create_app, resolve_state_db_path

BRIDGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BRIDGE_ROOT.parent
LINUX = BRIDGE_ROOT / "deploy" / "linux"
PROGRAM = REPO_ROOT / "MTC_COMMAND_CENTER" / "11_TRIAGE" / "KVM2_PROGRAM"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def noncomment_shell(path: Path) -> str:
    return "\n".join(
        line for line in read(path).splitlines() if line.strip() and not line.lstrip().startswith("#")
    )


def direct_requirements(path: Path) -> list[str]:
    return [
        line.strip()
        for line in read(path).splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def bash_executable() -> str:
    candidates = []
    if os.name == "nt":
        candidates.append(Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Git" / "bin" / "bash.exe")
    found = shutil.which("bash")
    if found:
        candidates.append(Path(found))
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    pytest.skip("bash is required for deterministic deployment-shell checks")


def run_bash(script: str, *args: Path | str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            bash_executable(),
            "-c",
            'export PATH="/usr/bin:/bin:$PATH"\n' + script,
            "pytest-bash",
            *(str(arg).replace("\\", "/") for arg in args),
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def test_requirements_in_mirrors_untouched_requirements_txt():
    assert direct_requirements(BRIDGE_ROOT / "requirements.in") == direct_requirements(
        BRIDGE_ROOT / "requirements.txt"
    )


def test_lock_is_exact_fully_hashed_and_contains_every_direct_dependency():
    verifier = load_module("deploy_verify_lock", LINUX / "verify_lock.py")
    locked = verifier.parse_lock(BRIDGE_ROOT / "requirements.lock")
    direct = {
        verifier.canonical_name(re.split(r"[<>=!~\[]", item, maxsplit=1)[0])
        for item in direct_requirements(BRIDGE_ROOT / "requirements.in")
    }
    assert direct <= set(locked)
    assert len(locked) >= len(direct)


def test_lock_generation_contract_targets_python_312_linux_with_hashes():
    header = "\n".join(read(BRIDGE_ROOT / "requirements.lock").splitlines()[:3])
    assert "uv pip compile" in header
    assert "--generate-hashes" in header
    assert "--python-version 3.12" in header
    assert "--python-platform linux" in header


def test_installer_requires_release_and_payload_manifest_hashes():
    script = read(LINUX / "install.sh")
    assert "--release-sha is required" in script
    assert "--manifest-sha256 is required" in script
    assert "payload manifest hash does not match --manifest-sha256" in script
    assert "assert_exact_payload_tree" in script
    assert "worktree" not in script.lower() or "dirty" in read(LINUX / "package.sh").lower()


def test_installer_uses_per_sha_venv_hashes_and_binary_wheels_only():
    script = read(LINUX / "install.sh")
    assert 'VENV="$(venv_dir "${RELEASE_SHA}")"' in script
    assert "--require-hashes --no-deps" in script
    assert "--only-binary=:all:" in script
    assert "--check-installed" in script
    assert "pip install --upgrade pip" in script  # present only in the explicit prohibition comment
    assert re.search(r'run "\$\{MTC_PYTHON\}" -m venv "\$\{VENV\}"', script)
    assert not re.search(r"(?m)^\s*(?:sudo\s+)?pip(?:3)?\s+install\b", script)


def test_installer_never_starts_enables_or_unmasks_a_service():
    commands = noncomment_shell(LINUX / "install.sh")
    assert not re.search(r"\bsystemctl\s+(?:start|enable|unmask)\b", commands)
    assert "run systemctl mask" in commands
    assert "run systemctl daemon-reload" in commands


def test_installer_never_installs_the_steady_profile():
    script = read(LINUX / "install.sh")
    assert "${MTC_STEADY_UNIT}.template" not in script
    assert "restart-enabled steady unit is present" in script
    assert '"steady_unit_installed": false' in script


def test_no_deployment_script_mutates_ufw():
    mutation = re.compile(r"\bufw\s+(?:allow|deny|reject|limit|delete|insert|enable|disable|reset)\b")
    for path in LINUX.rglob("*.sh"):
        assert not mutation.search(noncomment_shell(path)), path
    assert "ufw status verbose" in read(LINUX / "lib" / "common.sh")


def test_first_start_unit_is_separate_masked_design_and_restart_no():
    unit = read(LINUX / "systemd" / "mtc-bridge-first-start.service.template")
    assert "\nRestart=no\n" in unit
    assert "\n[Install]\n" not in unit
    assert "venvs/@RELEASE_SHA@/bin/python -m bridge.app" in unit
    assert "MTC_BRIDGE_STATE_DB=/var/lib/mtc-bridge/bridge.db" in unit
    assert "PrivateTmp=yes" in unit
    assert "KillSignal=SIGTERM" in unit
    assert "TimeoutStopSec=45" in unit
    assert "StartLimitBurst=3" in unit
    assert "NoNewPrivileges=yes" in unit
    assert "ProtectSystem=strict" in unit


def test_steady_unit_is_separate_restart_enabled_and_not_enableable():
    unit = read(LINUX / "systemd" / "mtc-bridge-steady.service.template")
    assert "\nRestart=on-failure\n" in unit
    assert "\n[Install]\n" not in unit
    assert "venvs/@RELEASE_SHA@/bin/python -m bridge.app" in unit
    assert "PrivateTmp=yes" in unit
    assert "StartLimitIntervalSec=600" in unit
    assert "StartLimitBurst=3" in unit


def test_canonical_paths_ownership_modes_and_no_symlink_contract_are_structural():
    common = read(LINUX / "lib" / "common.sh")
    installer = read(LINUX / "install.sh")
    for value in (
        'MTC_OPT_ROOT="/opt/mtc-bridge"',
        'MTC_RELEASES_ROOT="${MTC_OPT_ROOT}/releases"',
        'MTC_VENVS_ROOT="${MTC_OPT_ROOT}/venvs"',
        'MTC_STATE_DIR="/var/lib/mtc-bridge"',
        'MTC_LOG_DIR="/var/log/mtc-bridge"',
        'MTC_ENV_FILE="${MTC_CONF_DIR}/mtc-bridge.env"',
    ):
        assert value in common
    for mode in ("-m 0750", "-m 0755", "-m 0600", "-m 0644"):
        assert mode in installer
    assert "assert_not_symlink" in installer
    assert "assert_no_writable_paths" in installer


def test_payload_tree_rejects_symlinks_and_special_entries(tmp_path):
    common = LINUX / "lib" / "common.sh"
    payload = tmp_path / "payload"
    payload.mkdir()
    regular = payload / "regular"
    regular.write_text("accepted", encoding="utf-8")
    link = payload / "injected-link"
    try:
        link.symlink_to(regular)
    except OSError:
        common_text = read(common)
        assert "! -type d ! -type f -print -quit" in common_text
        assert "non-regular filesystem entry inside payload tree" in common_text
        return

    result = run_bash(
        '. "$1"; MTC_FAILURES=0; assert_regular_directory_tree "$2"',
        common,
        payload,
    )
    assert result.returncode != 0
    assert "non-regular filesystem entry" in result.stderr

    if hasattr(os, "mkfifo") and os.name != "nt":
        link.unlink()
        os.mkfifo(payload / "injected-fifo")
        result = run_bash(
            '. "$1"; MTC_FAILURES=0; assert_regular_directory_tree "$2"',
            common,
            payload,
        )
        assert result.returncode != 0
        assert "non-regular filesystem entry" in result.stderr


def test_package_and_install_enforce_complete_regular_file_inventory():
    package = read(LINUX / "package.sh")
    common = read(LINUX / "lib" / "common.sh")
    installer = read(LINUX / "install.sh")
    assert 'assert_regular_directory_tree "${OUT}"' in package
    assert "-mindepth 1 ! -type d ! -type f -print -quit" in common
    assert "assert_regular_directory_tree" in common
    assert "payload contains a symlink or special filesystem entry" in installer
    assert "payload file inventory differs from RELEASE_SHA256SUMS" in installer


def test_detached_installer_is_rejected_before_payload_helpers_or_mutation(tmp_path):
    payload = tmp_path / "detached-payload"
    payload.mkdir()
    result = run_bash(
        'bash "$1" --release-sha "$2" --manifest-sha256 "$3" --source "$4"',
        LINUX / "install.sh",
        "0" * 40,
        "0" * 64,
        payload,
    )
    assert result.returncode != 0
    assert "executing installer is not the installer inside the accepted payload" in result.stderr


def test_installer_sources_and_copies_only_hash_bound_payload_assets():
    script = read(LINUX / "install.sh")
    assert '. "${PAYLOAD_COMMON}"' in script
    assert 'ENV_TEMPLATE="${PAYLOAD_DEPLOY_DIR}/env/mtc-bridge.env.template"' in script
    assert 'FIRST_START_TEMPLATE="${PAYLOAD_DEPLOY_DIR}/systemd/${MTC_FIRST_START_UNIT}.template"' in script
    assert 'LOGROTATE_TEMPLATE="${PAYLOAD_DEPLOY_DIR}/logrotate/mtc-bridge"' in script
    for detached in (
        '"${SCRIPT_DIR}/lib/common.sh"',
        '"${SCRIPT_DIR}/env/mtc-bridge.env.template"',
        '"${SCRIPT_DIR}/systemd/${MTC_FIRST_START_UNIT}.template"',
        '"${SCRIPT_DIR}/logrotate/mtc-bridge"',
    ):
        assert detached not in script


def test_env_template_contains_names_and_comments_but_no_definitions():
    template = read(LINUX / "env" / "mtc-bridge.env.template")
    assert "HL_API_WALLET_KEY" in template
    assert "HL_LIVE_ACK" in template
    assignments = [
        line
        for line in template.splitlines()
        if line.strip() and not line.lstrip().startswith("#") and "=" in line
    ]
    assert assignments == []


def test_logrotate_contract_is_persistent_bounded_and_nonrestarting():
    policy = read(LINUX / "logrotate" / "mtc-bridge")
    for token in ("daily", "rotate 30", "size 64M", "compress", "delaycompress", "copytruncate"):
        assert token in policy
    assert "create 0640 mtc-bridge mtc-bridge" in policy
    assert "postrotate" not in policy


def test_state_path_default_is_preserved_and_posix_env_override_resolves():
    assert resolve_state_db_path(env={}) is None
    resolved = resolve_state_db_path(env={STATE_DB_ENV_VAR: "/var/lib/mtc-bridge/bridge.db"})
    assert resolved is not None
    assert resolved.as_posix() == "/var/lib/mtc-bridge/bridge.db"
    source = read(BRIDGE_ROOT / "bridge" / "app.py")
    assert 'root / "data" / "bridge.db"' in source
    assert 'host="127.0.0.1", port=8790' in source


def test_create_app_uses_explicit_state_path_without_starting_runtime(tmp_path):
    database = tmp_path / "state" / "bridge.db"
    app = create_app(store_path=database)
    try:
        assert database.is_file()
        assert app.state.bridge_store.db_path == database
        assert app.state.bridge_engine is None
    finally:
        app.state.bridge_store.close()


def test_state_path_cli_wins_and_bad_values_fail_closed():
    result = resolve_state_db_path(
        "/srv/bridge/state.db",
        {STATE_DB_ENV_VAR: "/var/lib/mtc-bridge/bridge.db"},
    )
    assert result is not None and result.as_posix() == "/srv/bridge/state.db"
    for value in ("", "   ", "relative/bridge.db", "/var/lib/../tmp/bridge.db"):
        with pytest.raises(ValueError):
            resolve_state_db_path(value, {})


def test_package_builder_requires_clean_exact_head_and_external_output():
    script = read(LINUX / "package.sh")
    assert "repo HEAD is not the requested release sha" in script
    assert "worktree is dirty" in script
    assert "archive --format=tar" in script
    assert "--out must be outside the repository worktree" in script
    assert "RELEASE_SHA256SUMS" in script


def test_closed_port_assertion_rejects_an_orphan_loopback_listener():
    result = run_bash(
        """
ss() { printf '%s\n' 'LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*'; }
. "$1"
MTC_FAILURES=0
assert_control_port_closed
""",
        LINUX / "lib" / "common.sh",
    )
    assert result.returncode != 0
    assert "control port 8790 still has a listener" in result.stderr


def test_masked_unstarted_verifier_requires_zero_writers_and_closed_port():
    script = read(LINUX / "verify.sh")
    assert "pgrep -f '[b]ridge\\.app'" in script
    assert "orphan bridge.app writer exists while service must be unstarted" in script
    assert "assert_control_port_closed || true" in script
    assert "assert_no_public_control_listener || true" in script


def test_verifier_is_read_only_and_binds_release_unit_venv_and_manifest():
    script = noncomment_shell(LINUX / "verify.sh")
    assert not re.search(r"\bsystemctl\s+(?:start|stop|restart|enable|disable|unmask|mask)\b", script)
    for token in (
        "--manifest-sha256 is required",
        "assert_exact_payload_tree",
        "--check-installed",
        "installed unit exactly matches",
        "first-start unit is masked",
        "restart-enabled steady unit absent",
    ):
        assert token in read(LINUX / "verify.sh")


def test_rollback_is_exact_preserves_state_and_never_starts():
    script = read(LINUX / "rollback.sh")
    commands = noncomment_shell(LINUX / "rollback.sh")
    assert "--state-manifest-file is required" in script
    assert "--state-manifest-sha256 is required" in script
    assert "--to-manifest-sha256" in script
    assert "assert_exact_payload_tree" in script
    assert "--check-installed" in script
    assert "assert_control_port_closed" in script
    assert "pgrep -f '[b]ridge\\.app'" in script
    assert "run systemctl stop" in commands
    assert "run systemctl mask" in commands
    assert not re.search(r"\bsystemctl\s+(?:start|enable|unmask)\b", commands)
    assert "state preserved" in script


def test_kvm2_program_required_artifacts_exist():
    required = (
        "INDEX.md",
        "SOURCE_SCENARIO_RECONCILIATION.md",
        "evidence/EVIDENCE_LEDGER.jsonl",
        "evidence/ledger_schema.json",
        "evidence/validate_ledger.py",
        "rebuild/profiles/temporary-testnet-lab.md",
        "rebuild/profiles/future-trading-only.md",
        "rebuild/profiles/PROFILE_DIFF.md",
        "rebuild/manifests/TRUSTED_INPUTS.md",
        "rebuild/manifests/release_candidate_manifest.template.json",
        "boundaries/IDENTITY_AND_FILESYSTEM.md",
        "boundaries/NETWORK_AND_SERVICE.md",
        "boundaries/loopback_isolation_design.md",
        "recovery/SECRET_INVENTORY.md",
        "recovery/STATE_CONTINUITY.md",
        "recovery/ACCESS_RECOVERY.md",
        "recovery/TEARDOWN_AND_REPROVISION.md",
        "recovery/MAINTENANCE.md",
        "recovery/INCIDENT_RESPONSE.md",
        "rehearsals/STAGING_MATRIX.md",
        "rehearsals/summaries/P2_09_REPRODUCIBILITY.md",
        "rehearsals/summaries/P3_03_UBUNTU_STAGING.md",
        "audits/READINESS_STATUS.md",
    )
    assert all((PROGRAM / item).is_file() for item in required)


def test_canonical_ledger_and_all_three_row_fixtures_validate():
    validator = load_module("kvm2_ledger_validator", PROGRAM / "evidence" / "validate_ledger.py")
    assert validator.validate_file(
        PROGRAM / "evidence" / "EVIDENCE_LEDGER.jsonl",
        repo_root=REPO_ROOT,
        verify_artifacts=True,
    ) == 1
    fixtures = PROGRAM / "evidence" / "fixtures"
    for name in ("valid_publishable_only.jsonl", "valid_restricted_only.jsonl", "valid_mixed.jsonl"):
        assert validator.validate_file(fixtures / name) == 1


def test_canonical_ledger_artifact_fresh_autocrlf_checkout_matches_recorded_identity(tmp_path):
    ledger_path = PROGRAM / "evidence" / "EVIDENCE_LEDGER.jsonl"
    rows = [json.loads(line) for line in read(ledger_path).splitlines() if line.strip()]
    assert len(rows) == 1
    row = rows[0]
    artifact_path = Path(row["publishable_artifact_path"])
    assert artifact_path.as_posix() == (
        "MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json"
    )

    blob = subprocess.run(
        ["git", "show", f"HEAD:{artifact_path.as_posix()}"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=True,
    ).stdout
    assert hashlib.sha256(blob).hexdigest() == row["artifact_sha256"]

    checkout_root = tmp_path / "fresh-autocrlf-checkout"
    checkout_root.mkdir()
    subprocess.run(
        ["git", "-c", "init.defaultBranch=main", "init", "--quiet"],
        cwd=checkout_root,
        capture_output=True,
        check=True,
    )
    (checkout_root / ".gitattributes").write_bytes((REPO_ROOT / ".gitattributes").read_bytes())
    checkout_artifact = checkout_root / artifact_path
    checkout_artifact.parent.mkdir(parents=True)
    checkout_artifact.write_bytes(blob)
    subprocess.run(
        [
            "git",
            "-c",
            "core.autocrlf=false",
            "add",
            "--",
            ".gitattributes",
            artifact_path.as_posix(),
        ],
        cwd=checkout_root,
        capture_output=True,
        check=True,
    )
    checkout_artifact.unlink()
    subprocess.run(
        [
            "git",
            "-c",
            "core.autocrlf=true",
            "checkout-index",
            "--force",
            "--",
            artifact_path.as_posix(),
        ],
        cwd=checkout_root,
        capture_output=True,
        check=True,
    )

    assert hashlib.sha256(checkout_artifact.read_bytes()).hexdigest() == row["artifact_sha256"]
    attributes = subprocess.run(
        ["git", "check-attr", "text", "eol", "--", artifact_path.as_posix()],
        cwd=checkout_root,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    assert attributes == [
        f"{artifact_path.as_posix()}: text: set",
        f"{artifact_path.as_posix()}: eol: lf",
    ]


def test_ledger_rejects_all_declared_synthetic_invalid_cases():
    validator = load_module("kvm2_ledger_validator_invalid", PROGRAM / "evidence" / "validate_ledger.py")
    fixture = json.loads(
        read(PROGRAM / "evidence" / "fixtures" / "valid_publishable_only.jsonl")
    )

    cases = {}
    row = copy.deepcopy(fixture)
    row["publishable_artifact_path"] = chr(67) + chr(58) + chr(92) + "private" + chr(92) + "file"
    cases["private_path"] = row
    row = copy.deepcopy(fixture)
    row["description"] += " " + ".".join(("192", "0", "2", "1"))
    cases["public_ip"] = row
    row = copy.deepcopy(fixture)
    row["description"] = "synthetic-host" + "." + "example"
    cases["hostname"] = row
    row = copy.deepcopy(fixture)
    row["description"] = "private_key=" + "synthetic-value"
    cases["credential"] = row
    row = copy.deepcopy(fixture)
    row["publishable_artifact_path"] = (
        "MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/" + ".." + "/outside"
    )
    cases["path_escape"] = row
    row = copy.deepcopy(fixture)
    del row["authorizer"]
    cases["malformed_row"] = row

    definitions = json.loads(
        read(PROGRAM / "evidence" / "fixtures" / "invalid_case_definitions.json")
    )
    assert {item["case"] for item in definitions} == set(cases)
    for row in cases.values():
        with pytest.raises(validator.LedgerValidationError):
            validator.validate_row(row)


def test_program_tree_has_no_private_host_ip_user_or_key_path():
    windows_path = re.compile(r"(?i)\b[a-z]:[\\/]")
    ipv4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    home_path = re.compile(r"(?i)(?:^|\s)/(?:home|users|root)/")
    for path in PROGRAM.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".json", ".jsonl", ".py"}:
            continue
        text = read(path)
        assert not windows_path.search(text), path
        assert all(match.group(0) == "127.0.0.1" for match in ipv4.finditer(text)), path
        assert not home_path.search(text), path
        assert "user@" not in text


def test_readiness_docs_keep_open_blocked_gates_honest():
    index = read(PROGRAM / "INDEX.md")
    audit = read(PROGRAM / "audits" / "READINESS_STATUS.md")
    for token in (
        "P1 host baseline | OPEN / BLOCKED",
        "P2-09 reproducibility rehearsal | BLOCKED / UNVERIFIED",
        "P3-01 owner risk-state choice | OPEN",
        "P3-03 Ubuntu staging matrix | BLOCKED / UNVERIFIED",
        "Final acceptance: **OPEN",
    ):
        assert token in index or token in audit
    assert "Codex Lead" in audit
    assert "Independent audit verdict: **NONE / OPEN**" in audit


def test_bridge_task_tracks_merged_pr25_and_uncommitted_candidate():
    task = read(
        REPO_ROOT
        / "MTC_COMMAND_CENTER"
        / "11_TRIAGE"
        / "BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md"
    )
    assert "PR #25 is merged" in task
    assert "423897b76b32f68cdabcae16b39c078fdd1f67cb" in task
    assert "local candidate uncommitted" in task
    assert "Independent audit status: **OPEN**" in task
    assert "P3-01 owner" in task and "OPEN" in task


def test_legacy_linux_recipe_is_explicitly_retired():
    deployment = read(BRIDGE_ROOT / "docs" / "17_DEPLOYMENT.md")
    assert "old global-pip" in deployment
    assert "Do not use it" in deployment
    assert "deploy/linux/install.sh" in deployment
    assert "Restart=no" in deployment
    assert "P2-09 and P3-03" in deployment


def test_documented_install_uses_the_installer_inside_the_accepted_payload():
    commands = read(LINUX / "COMMANDS.md")
    readme = read(LINUX / "README.md")
    exact = "<PAYLOAD>/IBKR_PAPER_BRIDGE/deploy/linux/install.sh"
    assert commands.count(f"sudo bash {exact}") >= 2
    assert "sudo bash ./deploy/linux/install.sh" not in commands
    assert exact in readme


def test_stage_e_requires_external_manifest_bundle_and_invariant_hashes():
    commands = read(LINUX / "COMMANDS.md")
    stage_e = commands.split("## Stage E", 1)[1].split("## Stage F", 1)[0]
    for token in (
        "EXPECTED_BUNDLE_SHA256",
        "EXPECTED_INVARIANTS_SHA256",
        "EXPECTED_MANIFEST_FILE_SHA256",
        "--expect-bundle-sha256",
        "--expect-invariants-sha256",
        "sha256sum --strict --check",
    ):
        assert token in stage_e
    assert stage_e.index("sha256sum --strict --check") < stage_e.index(
        "wal_state_bundle.py verify"
    )
