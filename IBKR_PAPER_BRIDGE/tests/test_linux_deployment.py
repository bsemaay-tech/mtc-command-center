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


def logical_shell_statements(script: str) -> list[str]:
    """Return normalized shell statements while excluding here-document data."""
    statements: list[str] = []
    current = ""
    heredoc_end: str | None = None
    array_depth = 0
    for raw_line in script.splitlines():
        stripped = raw_line.strip()
        if heredoc_end is not None:
            if stripped == heredoc_end:
                heredoc_end = None
            continue
        if not stripped or stripped.startswith("#"):
            continue
        if array_depth:
            array_depth += stripped.count("(") - stripped.count(")")
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=\($", stripped):
            statements.append(stripped)
            array_depth = 1
            continue
        continued = stripped.endswith("\\")
        piece = stripped[:-1].rstrip() if continued else stripped
        current = f"{current} {piece}".strip()
        if continued:
            continue
        statement = re.sub(r"\s+", " ", current)
        statements.append(statement)
        heredoc = re.search(r"<<-?['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?$", statement)
        if heredoc:
            heredoc_end = heredoc.group(1)
        current = ""
    assert not current, "unterminated shell continuation"
    assert heredoc_end is None, "unterminated here-document"
    assert array_depth == 0, "unterminated shell array"
    return statements


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


def run_bash(
    script: str,
    *args: Path | str,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    process_env = os.environ.copy()
    if env:
        process_env.update(env)
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
        env=process_env,
    )


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return result


def make_package_fixture(repo: Path, files: dict[str, bytes]) -> str:
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "core.autocrlf", "false")
    for relative, content in files.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    git(repo, "add", "--all")
    git(
        repo,
        "-c",
        "user.name=Deployment Test",
        "-c",
        "user.email=deployment-test@example.invalid",
        "commit",
        "-q",
        "-m",
        "fixture",
    )
    release_sha = git(repo, "rev-parse", "HEAD").stdout.strip()
    assert re.fullmatch(r"[0-9a-f]{40}", release_sha)
    return release_sha


def run_package(
    repo: Path,
    output: Path,
    release_sha: str,
    *,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return run_bash(
        'bash "$1" --release-sha "$2" --repo "$3" --out "$4"',
        LINUX / "package.sh",
        release_sha,
        repo,
        output,
        env=env,
    )


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bash_mode(path: Path) -> str:
    result = run_bash("stat -c '%a' \"$1\"", path)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


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
    assert re.search(
        r'run_action "venv-create" "\$\{MTC_PYTHON\}" -m venv "\$\{VENV\}"',
        script,
    )
    assert not re.search(r"(?m)^\s*(?:sudo\s+)?pip(?:3)?\s+install\b", script)


def test_installer_preflights_venv_capability_before_any_mutation():
    common = LINUX / "lib" / "common.sh"
    result = run_bash(
        '. "$1"; MTC_PYTHON=false; preflight_venv_capability',
        common,
    )
    assert result.returncode != 0
    assert "python3.12-venv" in result.stderr

    installer = read(LINUX / "install.sh")
    assert installer.index("preflight_venv_capability") < installer.index(
        'run_action "identity-group" groupadd'
    )


def test_dry_run_manifest_matches_every_real_install_mutation():
    script = read(LINUX / "install.sh")
    planned_id_list = re.findall(r'^\s*dry_run_action "([^"]+)"', script, re.MULTILINE)
    guarded_calls = re.findall(
        r'^\s*run_action "([^"]+)"[ \t]+([^\n]+)',
        script,
        re.MULTILINE,
    )
    guarded_id_list = [action_id for action_id, command in guarded_calls if command.strip()]

    # Both inventories are parsed from executable install.sh text. No
    # hand-maintained action dictionary can hide a newly added mutation.
    assert len(planned_id_list) == len(set(planned_id_list))
    assert len(guarded_id_list) == len(set(guarded_id_list))
    assert set(planned_id_list) == set(guarded_id_list)

    # Every modeled mutation must name its dry-run ID through run_action. A raw
    # `run install ... /opt/hermes` addition is therefore visible and RED.
    raw_run_calls = re.findall(r'^\s*run\s+([^\n]+)', script, re.MULTILINE)
    assert raw_run_calls == ['"$@"']

    statements = logical_shell_statements(script)
    guarded_helper = script[
        script.index("write_install_manifest() {") : script.index(
            'run_action "manifest-write" write_install_manifest'
        )
    ]
    assert re.search(r'cat\s+>\s+"\$\{MTC_INSTALL_MANIFEST\}"\s+<<EOF', guarded_helper)
    assert script.count('run_action "manifest-write" write_install_manifest') == 1
    assert len(re.findall(r"(?m)^\s*write_install_manifest(?:\s|$)", script)) == 0

    # Structural fence for the installer's current shell grammar. Direct
    # mutators are unclassifiable and fail; the only output redirection outside
    # /dev/null is the exact manifest helper invoked only by run_action.
    direct_mutator = re.compile(
        r"(?:^|(?:&&|\|\||;)\s*)(?:if\s+|elif\s+|while\s+|until\s+|!\s+)*"
        r"(?:command\s+|sudo\s+)?"
        r"(?:install|mkdir|cp|mv|rm|chown|chmod|ln|tee|useradd|groupadd)\b"
    )
    assert not [statement for statement in statements if direct_mutator.search(statement)]

    direct_systemctl = re.compile(
        r"(?:^|(?:&&|\|\||;)\s*)(?:if\s+|elif\s+|while\s+|until\s+|!\s+)*"
        r"systemctl\s+([a-z-]+)"
    )
    direct_systemctl_verbs = {
        match.group(1)
        for statement in statements
        for match in direct_systemctl.finditer(statement)
    }
    assert direct_systemctl_verbs <= {"is-active", "is-enabled"}
    assert not re.search(
        r"(?m)^\s*(?:python(?:[0-9.]+)?|perl|bash)\s+-c\b",
        noncomment_shell(LINUX / "install.sh"),
    )

    output_redirection = re.compile(
        r'(?<![<>])(?P<fd>\d*)(?P<operator>>>?)(?![>&])\s*'
        r'(?P<target>"[^"]*"|\'[^\']*\'|[^\s;|&]+)'
    )
    redirection_targets = {
        match.group("target").strip('"\'')
        for statement in statements
        for match in output_redirection.finditer(statement)
    }
    assert redirection_targets == {"/dev/null", "${MTC_INSTALL_MANIFEST}"}

    # The direct-command grammar is closed: a newly introduced executable head
    # (including a direct `install`) must be reviewed and explicitly classified.
    allowed_heads = {
        ".",
        ":",
        "assert_control_port_closed",
        "assert_exact_payload_tree",
        "assert_loopback_only_source",
        "assert_no_writable_paths",
        "assert_not_symlink",
        "assert_ufw_bridge_safe",
        "bootstrap_die",
        "cd",
        "command",
        "cmp",
        "die",
        "dry_run_action",
        "exit",
        "fail",
        "find",
        "getent",
        "grep",
        "id",
        "local",
        "log",
        "pgrep",
        "preflight_venv_capability",
        "printf",
        "readlink",
        "require_cmd",
        "require_release_sha",
        "require_root",
        "require_sha256",
        "run",
        "run_action",
        "cat",
        "print_dry_run_manifest",
        "sed",
        "set",
        "sha256sum",
        "shift",
        "sort",
        "systemctl",
        "tr",
        "umask",
        "verify_service_identity",
        "write_install_manifest",
        "usage",
    }
    unclassified: list[str] = []
    for statement in statements:
        candidate = statement
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*\(\)\s*\{$", candidate):
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*(?:\+)?=", candidate):
            continue
        if candidate in {"do", "done", "then", "else", "fi", "esac", "}", ")"}:
            continue
        if re.match(r"^(?:for|case)\b", candidate):
            continue
        candidate = re.sub(r"^[^\s()]+\)\s*", "", candidate)
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*(?:\+)?=", candidate):
            continue
        if candidate.endswith("$(") or candidate == '); then' or candidate == ')"; then':
            continue
        candidate = re.sub(r"^(?:if|elif|while|until)\s+!?\s*", "", candidate)
        candidate = candidate.lstrip("(! ")
        if not candidate or candidate.startswith("["):
            continue
        head = re.match(r'^(?:"?\$\{[^}]+\}"?|[A-Za-z0-9_./:-]+)', candidate)
        if not head:
            unclassified.append(statement)
            continue
        token = head.group(0)
        if token.startswith('${') or token.startswith('"${'):
            continue
        if token not in allowed_heads:
            unclassified.append(statement)
    assert unclassified == []

    for exact_path in (
        "${MTC_STATE_DIR}",
        "${MTC_LOG_DIR}",
        "${MTC_CONF_DIR}",
        "${DEST}",
        "${VENV}",
        "${MTC_ENV_FILE}",
        "${MTC_UNIT_DIR}/${MTC_FIRST_START_UNIT}",
        "${MTC_LOGROTATE_FILE}",
        "${MTC_LOGROTATE_CRON}",
        "${MTC_INSTALL_MANIFEST}",
    ):
        assert re.search(rf'^\s*dry_run_action .*{re.escape(exact_path)}', script, re.MULTILINE)


def test_installer_never_starts_enables_or_unmasks_a_service():
    commands = noncomment_shell(LINUX / "install.sh")
    assert not re.search(r"\bsystemctl\s+(?:start|enable|unmask)\b", commands)
    assert 'run_action "unit-mask" systemctl mask' in commands
    assert 'run_action "systemd-reload" systemctl daemon-reload' in commands


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


# A commented row must fail for the reason the comment-stripped row implies, not
# merely "some FAIL": each entry pins that exact failure category. The stripped
# row also cannot carry the trailing comment marker any more, so its absence from
# the diagnostic proves the reported row is the stripped one.
COMMENTED_NEGATIVE_DIAGNOSTICS = {
    "commented_bridge_port_exposed": "ufw exposes Bridge port 8790",
    "commented_unknown_verb": "rule action/direction is not a modelled inbound UFW status verb",
    "commented_named_profile": "port field is not an explicit numeric port/range",
}
UFW_COMMENT_MARKER = " #"


@pytest.mark.parametrize(
    ("name", "rules", "should_pass"),
    (
        (
            "future_web_tenant",
            "22/tcp ALLOW IN Anywhere\n80/tcp ALLOW IN Anywhere\n443/tcp ALLOW IN Anywhere\n",
            True,
        ),
        (
            "bridge_port_exposed",
            "22/tcp ALLOW IN Anywhere\n8790/tcp ALLOW IN Anywhere\n",
            False,
        ),
        (
            "bridge_port_after_destination_address",
            "22/tcp ALLOW IN Anywhere\n152.239.123.231 8790/tcp ALLOW IN Anywhere\n",
            False,
        ),
        (
            "bridge_port_inside_wide_range",
            "22/tcp ALLOW IN Anywhere\n8000:9000/tcp ALLOW IN Anywhere\n",
            False,
        ),
        (
            "bridge_port_at_range_start",
            "22/tcp ALLOW IN Anywhere\n8790:8800/tcp ALLOW IN Anywhere\n",
            False,
        ),
        (
            "unmodelled_application_profile",
            "22/tcp ALLOW IN Anywhere\nNginx Full ALLOW IN Anywhere\n",
            False,
        ),
        (
            "safe_numeric_range",
            "22/tcp ALLOW IN Anywhere\n80:443/tcp ALLOW IN Anywhere\n",
            True,
        ),
        (
            "known_openssh_profile",
            "22/tcp ALLOW IN Anywhere\nOpenSSH ALLOW IN Anywhere\n80/tcp ALLOW IN Anywhere\n",
            False,
        ),
        (
            "bridge_port_limit_in",
            "22/tcp ALLOW IN Anywhere\n8790/tcp LIMIT IN Anywhere\n",
            False,
        ),
        (
            "bridge_port_allow_fwd",
            "22/tcp ALLOW IN Anywhere\n8790/tcp ALLOW FWD Anywhere\n",
            False,
        ),
        (
            "ssh_missing",
            "80/tcp ALLOW IN Anywhere\n443/tcp ALLOW IN Anywhere\n",
            False,
        ),
        # Live Ubuntu rows carry a trailing rule comment; the exact shipped shape.
        (
            "live_commented_ssh_pair",
            "22/tcp                     ALLOW IN    Anywhere                   # SSH\n"
            "22/tcp (v6)                ALLOW IN    Anywhere (v6)              # SSH\n",
            True,
        ),
        (
            "commented_bridge_port_exposed",
            "22/tcp                     ALLOW IN    Anywhere                   # SSH\n"
            "8790/tcp ALLOW IN Anywhere                # temporary\n",
            False,
        ),
        (
            "commented_unknown_verb",
            "22/tcp WEIRD IN Anywhere # x\n",
            False,
        ),
        (
            "commented_named_profile",
            "OpenSSH ALLOW IN Anywhere # SSH\n",
            False,
        ),
        # A comment may mention the Bridge port without any rule admitting it.
        # Only the substring backstop sees this row, so this case is the sole
        # discriminator for the backstop's own comment strip.
        (
            "comment_mentions_bridge_port",
            "22/tcp ALLOW IN Anywhere # was 8790 before\n",
            True,
        ),
    ),
)
def test_ufw_bridge_safe_invariant_is_multi_tenant_and_fail_closed(
    tmp_path, name, rules, should_pass
):
    fixture = tmp_path / f"{name}.txt"
    fixture.write_text(
        "Status: active\n"
        "Logging: on (low)\n"
        "Default: deny (incoming), allow (outgoing), disabled (routed)\n"
        "To Action From\n"
        "-- ------ ----\n"
        + rules,
        encoding="utf-8",
    )
    result = run_bash(
        """
UFW_FIXTURE="$2"
ufw() { cat "${UFW_FIXTURE}"; }
. "$1"
MTC_FAILURES=0
assert_ufw_bridge_safe
""",
        LINUX / "lib" / "common.sh",
        fixture,
    )
    if should_pass:
        assert result.returncode == 0, result.stderr
        assert "Bridge port 8790 not exposed" in result.stdout
    else:
        assert result.returncode != 0
        assert "FAIL" in result.stderr
        expected_diagnostic = COMMENTED_NEGATIVE_DIAGNOSTICS.get(name)
        if expected_diagnostic is not None:
            assert expected_diagnostic in result.stderr, result.stderr
            assert UFW_COMMENT_MARKER not in result.stderr, result.stderr


def test_first_start_unit_is_separate_masked_design_and_restart_no():
    unit = read(LINUX / "systemd" / "mtc-bridge-first-start.service.template")
    effective_settings: dict[str, list[str]] = {}
    for raw_line in unit.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("[") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        effective_settings.setdefault(key, []).append(value)
    assert "\nRestart=no\n" in unit
    assert "\n[Install]\n" not in unit
    assert "venvs/@RELEASE_SHA@/bin/python -m bridge.app" in unit
    assert "MTC_BRIDGE_STATE_DB=/var/lib/mtc-bridge/bridge.db" in unit
    assert "MTC_BRIDGE_START_MODE=credential_free_disarmed" in unit
    assert "MTC_BRIDGE_RELEASE_SHA=@RELEASE_SHA@" in unit
    assert effective_settings.get("MemoryHigh") == ["768M"]
    assert effective_settings.get("MemoryMax") == ["1G"]
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
    assert "MTC_BRIDGE_START_MODE=credential_free_disarmed" not in unit
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


def test_writable_path_assertion_ignores_symlink_but_rejects_regular_file(tmp_path):
    common = LINUX / "lib" / "common.sh"
    immutable = tmp_path / "immutable"
    immutable.mkdir()
    target = immutable / "target"
    target.write_text("read-only", encoding="utf-8")
    os.chmod(target, 0o444)
    link = immutable / "python"
    try:
        link.symlink_to(target)
    except OSError:
        assert '! -type l -perm /222' in read(common)
    else:
        os.chmod(immutable, 0o555)
        try:
            result = run_bash(
                '. "$1"; MTC_FAILURES=0; assert_no_writable_paths "$2"',
                common,
                immutable,
            )
        finally:
            os.chmod(immutable, 0o755)
        assert result.returncode == 0, result.stderr

    writable = tmp_path / "writable"
    writable.mkdir()
    regular = writable / "regular"
    regular.write_text("writable", encoding="utf-8")
    os.chmod(regular, 0o666)
    os.chmod(writable, 0o555)
    try:
        result = run_bash(
            '. "$1"; MTC_FAILURES=0; assert_no_writable_paths "$2"',
            common,
            writable,
        )
    finally:
        os.chmod(writable, 0o755)
        os.chmod(regular, 0o644)
    assert result.returncode != 0
    assert "writable path inside immutable release" in result.stderr


def test_writable_path_assertion_rejects_writable_fifo(tmp_path):
    common = LINUX / "lib" / "common.sh"
    immutable = tmp_path / "fifo-root"
    immutable.mkdir()
    fifo = immutable / "writable-fifo"
    find_override = ""
    if os.name == "nt":
        # MSYS reports every directory as mode 0755 even after chmod. Exclude
        # only the fixture root so the real FIFO remains the behavioral target.
        find_override = r'''
find() {
  root="$1"
  shift
  command find "${root}" -mindepth 1 "$@"
}
'''
    try:
        result = run_bash(
            find_override
            + r'''
umask 022
mkfifo "$2/writable-fifo"
chmod 0555 "$2"
. "$1"
MTC_FAILURES=0
assert_no_writable_paths "$2"
''',
            common,
            immutable,
        )
    finally:
        os.chmod(immutable, 0o755)
        fifo.unlink(missing_ok=True)
    assert result.returncode != 0
    assert "writable path inside immutable release" in result.stderr


def test_writable_path_assertion_fails_closed_for_missing_root(tmp_path):
    common = LINUX / "lib" / "common.sh"
    missing = tmp_path / "does-not-exist"
    result = run_bash(
        '. "$1"; MTC_FAILURES=0; assert_no_writable_paths "$2"',
        common,
        missing,
    )
    assert result.returncode != 0
    assert "cannot inventory writable paths" in result.stderr


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
    assert 'LOGROTATE_CRON_TEMPLATE="${PAYLOAD_DEPLOY_DIR}/cron/mtc-bridge-logrotate"' in script
    for detached in (
        '"${SCRIPT_DIR}/lib/common.sh"',
        '"${SCRIPT_DIR}/env/mtc-bridge.env.template"',
        '"${SCRIPT_DIR}/systemd/${MTC_FIRST_START_UNIT}.template"',
        '"${SCRIPT_DIR}/logrotate/mtc-bridge"',
        '"${SCRIPT_DIR}/cron/mtc-bridge-logrotate"',
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


def test_logrotate_contract_is_hourly_nominal_and_nonrestarting():
    policy = read(LINUX / "logrotate" / "mtc-bridge")
    cron = read(LINUX / "cron" / "mtc-bridge-logrotate")
    for token in ("hourly", "rotate 7", "maxsize 64M", "compress", "delaycompress", "copytruncate"):
        assert token in policy
    assert "daily" not in noncomment_shell(LINUX / "logrotate" / "mtc-bridge")
    assert "1 GiB" in policy
    assert "NOT a bound or quota" in policy
    assert "unbounded even after rotation" in policy
    assert "Compensating control" in policy
    assert "10 GiB Bridge disk budget" in policy
    assert "create 0640 mtc-bridge mtc-bridge" in policy
    assert "postrotate" not in policy
    assert "exec /usr/sbin/logrotate /etc/logrotate.d/mtc-bridge" in cron
    assert "not a disk quota" in cron


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


def test_package_builder_pins_export_inputs_and_has_fail_closed_cr_guard():
    script = read(LINUX / "package.sh")
    compact = " ".join(script.split())
    assert "-c core.autocrlf=false -c core.eol=lf -c tar.umask=0022" in compact
    assert 'git -C "${REPO}" ls-tree -rz --long "${RELEASE_SHA}"' in script
    assert "exported file inventory or sizes differ from release commit tree" in script
    assert 'cd "${OUT}"' in script
    assert "-path './IBKR_PAPER_BRIDGE/deploy/linux/*'" in script
    assert '> "${CR_INVENTORY}"' in script
    assert '"${LF_REQUIRED_COUNT}" -gt 0' in script
    assert "export LC_ALL=C" in script


def test_package_manifest_is_identical_across_c_and_en_us_utf8_locales(tmp_path):
    locale_probe = run_bash("locale charmap", env={"LC_ALL": "en_US.UTF-8"})
    if locale_probe.returncode != 0 or locale_probe.stdout.strip().upper() not in {
        "UTF-8",
        "UTF8",
    }:
        pytest.skip("en_US.UTF-8 locale is not generated on this builder")

    repo = tmp_path / "repo"
    release_sha = make_package_fixture(
        repo,
        {
            "IBKR_PAPER_BRIDGE/deploy/linux/README.md": b"deployment fixture\n",
            "a-b.sh": b"#!/bin/sh\n",
            "a_b.sh": b"#!/bin/sh\n",
        },
    )
    output_c = tmp_path / "payload-c"
    output_utf8 = tmp_path / "payload-en-us"
    result_c = run_package(repo, output_c, release_sha, env={"LC_ALL": "C"})
    result_utf8 = run_package(
        repo,
        output_utf8,
        release_sha,
        env={"LC_ALL": "en_US.UTF-8"},
    )
    assert result_c.returncode == 0, result_c.stderr
    assert result_utf8.returncode == 0, result_utf8.stderr
    assert file_sha256(output_c / "RELEASE_SHA256SUMS") == file_sha256(
        output_utf8 / "RELEASE_SHA256SUMS"
    )


def test_package_core_eol_pin_overrides_text_auto_and_repo_crlf(tmp_path):
    relative = "IBKR_PAPER_BRIDGE/deploy/linux/README.md"
    expected = b"line one\nline two\n"
    repo = tmp_path / "repo"
    release_sha = make_package_fixture(
        repo,
        {
            ".gitattributes": b"* text=auto\n",
            relative: expected,
        },
    )
    git(repo, "config", "core.eol", "crlf")

    output = tmp_path / "payload"
    result = run_package(repo, output, release_sha)

    assert result.returncode == 0, result.stderr
    assert (output / relative).read_bytes() == expected


def test_package_conflicting_tar_umask_cannot_change_manifest_or_modes(tmp_path):
    relative = "IBKR_PAPER_BRIDGE/deploy/linux/README.md"
    repo = tmp_path / "repo"
    release_sha = make_package_fixture(repo, {relative: b"deployment fixture\n"})

    git(repo, "config", "tar.umask", "0000")
    output_permissive = tmp_path / "payload-umask-0000"
    result_permissive = run_package(repo, output_permissive, release_sha)
    git(repo, "config", "tar.umask", "0077")
    output_restrictive = tmp_path / "payload-umask-0077"
    result_restrictive = run_bash(
        r'''
TAR_CAPTURE_ROOT="$5"
tar() {
  archive_file="${TAR_CAPTURE_ROOT}/captured.tar"
  cat > "${archive_file}"
  archive_mode="$(command tar --force-local -tvf "${archive_file}" \
    | awk '$NF == "IBKR_PAPER_BRIDGE/deploy/linux/README.md" { print $1; exit }')"
  [ "${archive_mode}" = '-rw-r--r--' ] || {
    printf 'unexpected archive mode: %s\n' "${archive_mode}" >&2
    return 73
  }
  command tar "$@" < "${archive_file}"
}
. "$1" --release-sha "$2" --repo "$3" --out "$4"
''',
        LINUX / "package.sh",
        release_sha,
        repo,
        output_restrictive,
        tmp_path,
    )

    assert result_permissive.returncode == 0, result_permissive.stderr
    assert result_restrictive.returncode == 0, result_restrictive.stderr
    assert file_sha256(output_permissive / "RELEASE_SHA256SUMS") == file_sha256(
        output_restrictive / "RELEASE_SHA256SUMS"
    )
    assert bash_mode(output_permissive / relative) == "644"
    assert bash_mode(output_restrictive / relative) == "644"


def test_package_rejects_export_ignore_inventory_divergence(tmp_path):
    repo = tmp_path / "repo"
    release_sha = make_package_fixture(
        repo,
        {
            ".gitattributes": b"omitted.txt export-ignore\n",
            "omitted.txt": b"must remain in the release inventory\n",
            "IBKR_PAPER_BRIDGE/deploy/linux/README.md": b"deployment fixture\n",
        },
    )
    result = run_package(repo, tmp_path / "payload", release_sha)
    assert result.returncode != 0
    assert "exported file inventory or sizes differ from release commit tree" in result.stderr


def test_package_cr_guard_rejects_cr_bytes(tmp_path):
    repo = tmp_path / "repo"
    release_sha = make_package_fixture(repo, {"bad.sh": b"#!/bin/sh\r\nexit 0\r\n"})
    result = run_package(repo, tmp_path / "payload", release_sha)
    assert result.returncode != 0
    assert "archive contains CR byte in LF-required file: bad.sh" in result.stderr


def test_package_cr_guard_propagates_find_failure(tmp_path):
    repo = tmp_path / "repo"
    release_sha = make_package_fixture(repo, {"good.sh": b"#!/bin/sh\nexit 0\n"})
    result = run_bash(
        r'''
find() {
  for find_arg in "$@"; do
    if [ "${find_arg}" = './IBKR_PAPER_BRIDGE/deploy/linux/*' ]; then
      printf '%s\n' 'simulated CR-inventory find failure' >&2
      return 73
    fi
  done
  command find "$@"
}
. "$1" --release-sha "$2" --repo "$3" --out "$4"
''',
        LINUX / "package.sh",
        release_sha,
        repo,
        tmp_path / "payload",
    )
    assert result.returncode != 0
    assert "simulated CR-inventory find failure" in result.stderr
    assert "cannot inventory LF-required payload files" in result.stderr


def test_package_cr_guard_rejects_missing_deployment_directory_inventory(tmp_path):
    repo = tmp_path / "repo"
    release_sha = make_package_fixture(repo, {"outside.sh": b"#!/bin/sh\n"})
    result = run_package(repo, tmp_path / "payload", release_sha)
    assert result.returncode != 0
    assert "no deployment LF-required payload files were found to inspect" in result.stderr


def test_package_cr_guard_handles_metacharacter_output_path(tmp_path):
    repo = tmp_path / "repo"
    relative = "IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template"
    release_sha = make_package_fixture(repo, {relative: b"# env with CR\r\nKEY=1\r\n"})
    output = tmp_path / "payload[meta]"
    result = run_package(repo, output, release_sha)
    assert result.returncode != 0
    assert "archive contains CR byte in LF-required file" in result.stderr


def test_package_cleans_partial_temp_allocations_when_mktemp_fails(tmp_path):
    repo = tmp_path / "repo"
    release_sha = make_package_fixture(
        repo,
        {"IBKR_PAPER_BRIDGE/deploy/linux/README.md": b"deployment fixture\n"},
    )
    package_temps = tmp_path / "package-temps"
    package_temps.mkdir()
    result = run_bash(
        r'''
PACKAGE_TEMP_ROOT="$5"
mktemp() {
  printf 'call\n' >> "${PACKAGE_TEMP_ROOT}/calls"
  call_number="$(wc -l < "${PACKAGE_TEMP_ROOT}/calls")"
  if [ "${call_number}" -eq 3 ]; then
    return 73
  fi
  temp_path="${PACKAGE_TEMP_ROOT}/temp-${call_number}"
  : > "${temp_path}"
  printf '%s\n' "${temp_path}"
}
. "$1" --release-sha "$2" --repo "$3" --out "$4"
''',
        LINUX / "package.sh",
        release_sha,
        repo,
        tmp_path / "payload",
        package_temps,
    )
    assert result.returncode != 0
    assert list(package_temps.glob("temp-*")) == []


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
    output_redirection = re.compile(
        r'(?<![<>])(?P<fd>\d*)(?P<operator>>>?)(?![>&])\s*'
        r'(?P<target>"[^"]*"|\'[^\']*\'|[^\s;|&]+)'
    )
    redirections = [match.group("target").strip('"\'') for match in output_redirection.finditer(script)]
    assert redirections
    assert set(redirections) == {"/dev/null"}

    write_commands = re.compile(
        r"(?m)(?:^|[;|&()]\s*)(?:command\s+|sudo\s+)?"
        r"(?:mktemp|rm|mv|cp|install|touch|tee|dd|truncate|ln|mkdir|rmdir|chmod|chown)\b"
    )
    assert not write_commands.search(script)
    assert not re.search(r"\bsed\s+(?:[^\n;]*\s)?-i(?:[.A-Za-z]*)?(?:\s|$)", script)
    executable_script = "\n".join(
        line for line in script.splitlines() if not line.lstrip().startswith("require_cmd ")
    )
    systemctl_verbs = set(re.findall(r"\bsystemctl\s+([a-z-]+)", executable_script))
    assert systemctl_verbs <= {"is-active", "is-enabled"}
    assert not re.search(r"\b(?:printf|echo)\b[^\n]*(?:>>?|\btee\b)\s*/", script)

    # Every lower-case interpreter token is inventoried, including read-only
    # path tests and unit-text checks. This is intentionally stricter than a
    # command-position denylist: any added python/perl/bash-c spelling must be
    # reviewed, and the two executable venv probes remain the only calls.
    normalized = "\n".join(logical_shell_statements(read(LINUX / "verify.sh")))
    interpreter_token_lines = [
        line
        for line in normalized.splitlines()
        if re.search(r"(?<![A-Za-z0-9_.-])(?:python(?:[0-9.]+)?|perl|bash\s+-c)(?![A-Za-z0-9_.-])", line)
    ]
    assert interpreter_token_lines == [
        'if [ -x "${VENV}/bin/python" ]; then',
        'pyver="$("${VENV}/bin/python" -c \'import sys; print("%d.%d" % sys.version_info[:2])\')"',
        'if "${VENV}/bin/python" "${DEST}/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py" --lock "${DEST}/IBKR_PAPER_BRIDGE/requirements.lock" --check-installed; then',
        'if grep -q "venvs/${RELEASE_SHA}/bin/python" "${unit}"; then',
    ]
    interpreter_command = re.compile(
        r'(?:^|="?\$\(|\bif\s+)(?:"\$\{VENV\}/bin/python"|python(?:[0-9.]+)?|perl|bash\s+-c)'
    )
    interpreter_lines = [
        line
        for line in normalized.splitlines()
        if interpreter_command.search(line)
    ]
    assert interpreter_lines == [
        'pyver="$("${VENV}/bin/python" -c \'import sys; print("%d.%d" % sys.version_info[:2])\')"',
        'if "${VENV}/bin/python" "${DEST}/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py" --lock "${DEST}/IBKR_PAPER_BRIDGE/requirements.lock" --check-installed; then',
    ]
    awk_with_output = re.compile(r"\bawk\b[^\n]*(?<![<>])(?:>>?)(?![>&])")
    assert not awk_with_output.search(normalized)
    assert "expected_unit" not in script
    common = read(LINUX / "lib" / "common.sh")
    inventory_helper = common[
        common.index("assert_exact_payload_tree()") : common.index("# Read-only UFW assertion")
    ]
    assert "mktemp" not in inventory_helper
    assert "cmp -s <(" in inventory_helper
    for token in (
        "--manifest-sha256 is required",
        "assert_exact_payload_tree",
        "--check-installed",
        "installed unit exactly matches",
        "first-start unit is masked",
        "restart-enabled steady unit absent",
        "hourly Bridge logrotate runner exactly matches",
    ):
        assert token in read(LINUX / "verify.sh")


def test_verifier_rejects_unsafe_logrotate_asset_metadata(tmp_path):
    verify = read(LINUX / "verify.sh")
    block = verify[
        verify.index("# --- 8. logs, rotation, control plane") : verify.index(
            'assert_loopback_only_source "${DEST}/IBKR_PAPER_BRIDGE/bridge/app.py"'
        )
    ]
    assert 'assert_mode_owner "${MTC_LOGROTATE_FILE}" 0644 root:root 0:0 file' in block
    assert 'assert_mode_owner "${MTC_LOGROTATE_CRON}" 0755 root:root 0:0 file' in block

    release = tmp_path / "release"
    installed = tmp_path / "installed"
    policy_source = release / "IBKR_PAPER_BRIDGE" / "deploy" / "linux" / "logrotate" / "mtc-bridge"
    cron_source = release / "IBKR_PAPER_BRIDGE" / "deploy" / "linux" / "cron" / "mtc-bridge-logrotate"
    policy_target = installed / "mtc-bridge"
    cron_target = installed / "mtc-bridge-logrotate"
    for path in (policy_source, cron_source, policy_target, cron_target):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("accepted bytes\n", encoding="utf-8")

    result = run_bash(
        r'''
. "$1"
DEST="$2"
MTC_LOGROTATE_FILE="$3"
MTC_LOGROTATE_CRON="$4"
stat() {
  case "$2" in
    '%a') printf '%s\n' '777' ;;
    '%U:%G') printf '%s\n' 'root:root' ;;
    '%u:%g') printf '%s\n' '1000:1000' ;;
    *) return 73 ;;
  esac
}
MTC_FAILURES=0
''' + block + r'''
[ "${MTC_FAILURES}" -gt 0 ]
''',
        LINUX / "lib" / "common.sh",
        release,
        policy_target,
        cron_target,
    )
    assert result.returncode == 0, result.stderr
    assert "mode 777, expected 644" in result.stderr
    assert "mode 777, expected 755" in result.stderr

    owner_result = run_bash(
        r'''
. "$1"
DEST="$2"
MTC_LOGROTATE_FILE="$3"
MTC_LOGROTATE_CRON="$4"
stat() {
  case "$2" in
    '%a')
      case "$3" in
        *mtc-bridge-logrotate) printf '%s\n' '755' ;;
        *) printf '%s\n' '644' ;;
      esac
      ;;
    '%U:%G') printf '%s\n' 'root:root' ;;
    '%u:%g') printf '%s\n' '1000:1000' ;;
    *) return 73 ;;
  esac
}
MTC_FAILURES=0
''' + block + r'''
[ "${MTC_FAILURES}" -gt 0 ]
''',
        LINUX / "lib" / "common.sh",
        release,
        policy_target,
        cron_target,
    )
    assert owner_result.returncode == 0, owner_result.stderr
    assert "numeric owner 1000:1000, expected 0:0" in owner_result.stderr


def test_verifier_rejects_start_mode_defined_in_env_file(tmp_path):
    # Behavioral regression: extract the real MTC_BRIDGE_START_MODE env-file
    # guard block from verify.sh and execute it with stub fail/pass functions
    # and a temporary env file. This is not a source-string assertion — the
    # extracted block is the code under test. It must reject a bare or exported
    # definition and accept commented/clean content, matching leading whitespace
    # and the optional `export` form, while never reading the assigned value.
    lines = read(LINUX / "verify.sh").splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^\s*if\b", line) and "MTC_BRIDGE_START_MODE=" in line and "MTC_ENV_FILE" in line:
            start = i
            break
    assert start is not None, "MTC_BRIDGE_START_MODE env-file guard not found in verify.sh"
    guard = None
    for j in range(start + 1, len(lines)):
        if lines[j].strip() == "fi":
            guard = "\n".join(lines[start : j + 1])
            break
    assert guard, "MTC_BRIDGE_START_MODE env-file guard has no closing fi"

    harness = (
        'fail() { printf "FAIL_BRANCH\\n"; }\n'
        'pass() { printf "PASS_BRANCH\\n"; }\n'
        'MTC_ENV_FILE="$1"\n'
        + guard
        + "\n"
    )

    cases = [
        ("bare_assignment", "MTC_BRIDGE_START_MODE=credentialed\n", "FAIL_BRANCH"),
        ("export_assignment", "export MTC_BRIDGE_START_MODE=credentialed\n", "FAIL_BRANCH"),
        ("indented_assignment", "\tMTC_BRIDGE_START_MODE=credentialed\n", "FAIL_BRANCH"),
        ("commented_assignment", "# MTC_BRIDGE_START_MODE=credentialed\n", "PASS_BRANCH"),
        ("clean_content", "# only an unrelated name here\nHL_API_WALLET_KEY\n", "PASS_BRANCH"),
    ]
    for name, content, expected in cases:
        env_file = tmp_path / f"{name}.env"
        env_file.write_text(content, encoding="utf-8")
        result = run_bash(harness, env_file)
        assert result.returncode == 0, (name, result.returncode, result.stderr)
        assert result.stdout.strip() == expected, (name, result.stdout)


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
