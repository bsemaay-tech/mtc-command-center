"""WP-P0-12 capture-tool NIT slice after the exact-Opus PASS-WITH-NITS on af921d75 (NITs 1-7)."""
from __future__ import annotations

import pathlib
import shutil
import sys

W = pathlib.Path("C:/tmp/P1CAP_20260914/IBKR_PAPER_BRIDGE")
TOOL = W / "tools" / "capture_own_account_evidence.py"
TESTS = W / "tests" / "test_capture_own_account_evidence.py"
FIX = W / "tests" / "fixtures" / "p012_path1_r2_capture"
R2 = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/P012_PATH1_REAL_CAPTURE_20260917/r2")


def load(p):
    raw = p.read_bytes().decode("utf-8")
    return raw.replace("\r\n", "\n"), ("\r\n" if "\r\n" in raw else "\n")


def save(p, text, nl):
    p.write_bytes(text.replace("\n", nl).encode("utf-8"))


def rep(text, old, new, tag):
    n = text.count(old)
    if n != 1:
        print(f"PATCH ABORT [{tag}]: {n} occurrences")
        sys.exit(2)
    return text.replace(old, new)


t, nl = load(TOOL)

# imports for NIT-6
t = rep(t, "from eth_account import Account\nfrom eth_account.messages import encode_defunct\n",
        "from eth_account import Account\nfrom eth_account.messages import encode_defunct\nfrom eth_utils.exceptions import ValidationError\n", "imports")

# NIT-5: a fill without tid is refused (hash+oid+time can merge two identical partial fills)
t = rep(
    t,
    "    oid = row.get(\"oid\")\n"
    "    h = row.get(\"hash\")\n"
    "    t = row.get(\"time\")\n"
    "    if (\n"
    "        not isinstance(h, str)\n"
    "        or isinstance(oid, bool)\n"
    "        or not isinstance(oid, int)\n"
    "        or isinstance(t, bool)\n"
    "        or not isinstance(t, int)\n"
    "    ):\n"
    "        raise CaptureRefused(REFUSED_MALFORMED, \"fill identity is malformed\")\n"
    "    return f\"hash-oid-time:{h}:{oid}:{t}\"\n",
    "    # NIT-5 (exact-Opus read of af921d75): the former hash+oid+time fallback could merge two\n"
    "    # identical partial fills of one order in one block (an undercount). Every venue fill carries\n"
    "    # a tid (r1/r2 captures: all rows); a fill without one cannot be counted without ambiguity, so\n"
    "    # the shape is refused rather than guessed\n"
    "    raise CaptureRefused(REFUSED_MALFORMED, \"fill without tid (identity would be ambiguous)\")\n",
    "NIT-5",
)

# NIT-2: a page must be in non-decreasing time order (a descending page would be silently truncated)
t = rep(
    t,
    "        page_max = cursor\n"
    "        for index, row in enumerate(parsed):\n"
    "            ident = identity(row)\n"
    "            t = row_time(row)\n",
    "        page_max = cursor\n"
    "        previous_time: int | None = None\n"
    "        for index, row in enumerate(parsed):\n"
    "            ident = identity(row)\n"
    "            t = row_time(row)\n"
    "            if previous_time is not None and t < previous_time:\n"
    "                # NIT-2: the cursor arithmetic below assumes ascending pages (the SDK's order);\n"
    "                # a descending page would set the next cursor past unread rows - refuse instead\n"
    "                raise CaptureRefused(\n"
    "                    REFUSED_MALFORMED, f\"{kind} page not in ascending time order ({ident})\"\n"
    "                )\n"
    "            previous_time = t\n",
    "NIT-2",
)

# NIT-3: account state bytes are recorded before the shape check (a failed query is never evidence-free)
t = rep(
    t,
    "    ended = datetime.now(UTC)\n"
    "    if not isinstance(parsed, dict):\n"
    "        raise CaptureRefused(REFUSED_MALFORMED, \"account state is not an object\")\n"
    "    record_response(\n"
    "        out_dir,\n"
    "        manifest,\n"
    "        name=\"account_state\",\n"
    "        capture=raw,\n"
    "        base_url=base_url,\n"
    "        started=started,\n"
    "        ended=ended,\n"
    "    )\n",
    "    ended = datetime.now(UTC)\n"
    "    # NIT-3: the bytes are kept before the shape is judged, as paged_query does\n"
    "    record_response(\n"
    "        out_dir,\n"
    "        manifest,\n"
    "        name=\"account_state\",\n"
    "        capture=raw,\n"
    "        base_url=base_url,\n"
    "        started=started,\n"
    "        ended=ended,\n"
    "    )\n"
    "    if not isinstance(parsed, dict):\n"
    "        raise CaptureRefused(\n"
    "            REFUSED_MALFORMED, \"account state is not an object (bytes kept as account_state.json)\"\n"
    "        )\n",
    "NIT-3",
)

# NIT-6 + NIT-7: named refusals for a malformed signature file / signature; the exact signed text and
# the signature are stored in the manifest
t = rep(
    t,
    "def read_signature(path: Path) -> str:\n"
    "    raw = path.read_text(encoding=\"utf-8\").strip()\n"
    "    if raw.startswith(\"{\"):\n"
    "        value = json.loads(raw).get(\"signature\")\n"
    "        if not isinstance(value, str):\n"
    "            raise CaptureRefused(REFUSED_BAD_SIGNATURE, \"JSON missing signature\")\n"
    "        return value.strip()\n"
    "    return raw\n",
    "def read_signature(path: Path) -> str:\n"
    "    # NIT-6: an unreadable or malformed signature file is a named refusal (exit 2), not a\n"
    "    # raw exception (exit 1)\n"
    "    try:\n"
    "        raw = path.read_text(encoding=\"utf-8\").strip()\n"
    "    except (OSError, UnicodeDecodeError) as exc:\n"
    "        raise CaptureRefused(\n"
    "            REFUSED_BAD_SIGNATURE, f\"signature file unreadable: {path.name}\"\n"
    "        ) from exc\n"
    "    if raw.startswith(\"{\"):\n"
    "        try:\n"
    "            value = json.loads(raw).get(\"signature\")\n"
    "        except (json.JSONDecodeError, AttributeError) as exc:\n"
    "            raise CaptureRefused(\n"
    "                REFUSED_BAD_SIGNATURE, \"signature file is not a JSON object\"\n"
    "            ) from exc\n"
    "        if not isinstance(value, str):\n"
    "            raise CaptureRefused(REFUSED_BAD_SIGNATURE, \"JSON missing signature\")\n"
    "        return value.strip()\n"
    "    return raw\n",
    "NIT-6 read_signature",
)
t = rep(
    t,
    "    signature = read_signature(signature_path)\n"
    "    recovered = Account.recover_message(\n"
    "        encode_defunct(text=ownership_message(address, run_id)),\n"
    "        signature=signature,\n"
    "    )\n"
    "    ok = recovered.lower() == address.lower()\n"
    "    if not ok:\n"
    "        raise CaptureRefused(REFUSED_BAD_SIGNATURE, \"recovered address mismatch\")\n"
    "    return {\"status\": \"OWNERSHIP_EVIDENCE: VERIFIED\", \"recovered_address\": recovered}\n",
    "    signature = read_signature(signature_path)\n"
    "    message = ownership_message(address, run_id)\n"
    "    try:\n"
    "        recovered = Account.recover_message(\n"
    "            encode_defunct(text=message), signature=signature\n"
    "        )\n"
    "    except (ValueError, TypeError, ValidationError) as exc:\n"
    "        # NIT-6: a signature that cannot be parsed or recovered is a named refusal\n"
    "        raise CaptureRefused(\n"
    "            REFUSED_BAD_SIGNATURE, f\"signature not recoverable: {type(exc).__name__}\"\n"
    "        ) from exc\n"
    "    ok = recovered.lower() == address.lower()\n"
    "    if not ok:\n"
    "        raise CaptureRefused(REFUSED_BAD_SIGNATURE, \"recovered address mismatch\")\n"
    "    # NIT-7: the exact signed text and the signature travel with the manifest, so the record is\n"
    "    # complete without a file kept beside the tool. The message binds address + run_id only\n"
    "    # (start / end / network are NOT signed) - a design change to the signed text would\n"
    "    # invalidate the owner's earlier signatures and is the owner's call, not this slice's.\n"
    "    return {\n"
    "        \"status\": \"OWNERSHIP_EVIDENCE: VERIFIED\",\n"
    "        \"recovered_address\": recovered,\n"
    "        \"message\": message,\n"
    "        \"signature\": signature,\n"
    "        \"binds\": \"address+run_id\",\n"
    "    }\n",
    "NIT-6/7 ownership_result",
)

# NIT-1: verify_sidecars covers every sidecar in the directory and the recorded derived digest
t = rep(
    t,
    "def verify_sidecars(out_dir: Path) -> None:\n"
    "    manifest = json.loads(\n"
    "        (out_dir / \"CAPTURE_MANIFEST.json\").read_text(encoding=\"utf-8\")\n"
    "    )\n"
    "    for entry in manifest[\"responses\"]:\n"
    "        path = out_dir / entry[\"file\"]\n"
    "        actual = sha256_bytes(path.read_bytes())\n"
    "        sidecar = (\n"
    "            path.with_name(path.name + \".sha256\").read_text(encoding=\"utf-8\").strip()\n"
    "        )\n"
    "        if actual != sidecar or actual != entry[\"response_sha256\"]:\n"
    "            raise CaptureRefused(REFUSED_BAD_SIDECAR, entry[\"file\"])\n",
    "def _sidecar_digest(path: Path) -> str:\n"
    "    sidecar = path.with_name(path.name + \".sha256\")\n"
    "    try:\n"
    "        return sidecar.read_text(encoding=\"utf-8\").strip()\n"
    "    except (OSError, UnicodeDecodeError) as exc:\n"
    "        raise CaptureRefused(\n"
    "            REFUSED_BAD_SIDECAR, f\"sidecar unreadable: {sidecar.name}\"\n"
    "        ) from exc\n"
    "\n"
    "\n"
    "def verify_sidecars(out_dir: Path) -> None:\n"
    "    \"\"\"``CAPTURE_VERIFY_OK`` means: every recorded response matches its sidecar AND the\n"
    "    manifest's digest; every ``*.sha256`` in the directory (the derived view and the manifest\n"
    "    included) names an existing file that hashes to it; and, when the manifest records\n"
    "    ``derived_extraction_sha256`` (written from this version on), the derived view matches it.\n"
    "    NIT-1 of the exact-Opus read of af921d75: the former check covered the responses only.\"\"\"\n"
    "    manifest_path = out_dir / \"CAPTURE_MANIFEST.json\"\n"
    "    try:\n"
    "        manifest = json.loads(manifest_path.read_text(encoding=\"utf-8\"))\n"
    "    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:\n"
    "        # NIT-6: a missing directory or manifest is a named refusal, not a raw exception\n"
    "        raise CaptureRefused(\n"
    "            REFUSED_BAD_SIDECAR, f\"manifest unreadable: {manifest_path}\"\n"
    "        ) from exc\n"
    "    if not isinstance(manifest, dict) or not isinstance(manifest.get(\"responses\"), list):\n"
    "        raise CaptureRefused(REFUSED_BAD_SIDECAR, \"manifest has no responses list\")\n"
    "    for entry in manifest[\"responses\"]:\n"
    "        path = out_dir / entry[\"file\"]\n"
    "        try:\n"
    "            actual = sha256_bytes(path.read_bytes())\n"
    "        except OSError as exc:\n"
    "            raise CaptureRefused(REFUSED_BAD_SIDECAR, entry[\"file\"]) from exc\n"
    "        if actual != _sidecar_digest(path) or actual != entry[\"response_sha256\"]:\n"
    "            raise CaptureRefused(REFUSED_BAD_SIDECAR, entry[\"file\"])\n"
    "    for sidecar in sorted(out_dir.glob(\"*.sha256\")):\n"
    "        target = sidecar.with_name(sidecar.name[: -len(\".sha256\")])\n"
    "        try:\n"
    "            actual = sha256_bytes(target.read_bytes())\n"
    "        except OSError as exc:\n"
    "            raise CaptureRefused(\n"
    "                REFUSED_BAD_SIDECAR, f\"{sidecar.name} names a missing file\"\n"
    "            ) from exc\n"
    "        if actual != _sidecar_digest(target):\n"
    "            raise CaptureRefused(REFUSED_BAD_SIDECAR, target.name)\n"
    "    recorded = manifest.get(\"derived_extraction_sha256\")\n"
    "    if recorded is not None:\n"
    "        derived = out_dir / \"DERIVED_EXTRACTION.json\"\n"
    "        try:\n"
    "            actual = sha256_bytes(derived.read_bytes())\n"
    "        except OSError as exc:\n"
    "            raise CaptureRefused(REFUSED_BAD_SIDECAR, derived.name) from exc\n"
    "        if actual != recorded:\n"
    "            raise CaptureRefused(\n"
    "                REFUSED_BAD_SIDECAR, \"DERIVED_EXTRACTION.json differs from the manifest digest\"\n"
    "            )\n",
    "NIT-1 verify_sidecars",
)
t = rep(
    t,
    "    write_once(out_dir / \"DERIVED_EXTRACTION.json\", json_bytes(extraction))\n"
    "    manifest = {\n"
    "        \"kind\": \"P012_PATH1_OWN_ACCOUNT_CAPTURE_MANIFEST_V1\",\n"
    "        \"run_id\": run_id,\n",
    "    derived_digest = write_once(out_dir / \"DERIVED_EXTRACTION.json\", json_bytes(extraction))\n"
    "    manifest = {\n"
    "        \"kind\": \"P012_PATH1_OWN_ACCOUNT_CAPTURE_MANIFEST_V1\",\n"
    "        \"run_id\": run_id,\n"
    "        # NIT-1: the derived view's digest is part of the manifest, so verify_sidecars binds it\n"
    "        \"derived_extraction_sha256\": derived_digest,\n",
    "NIT-1 manifest",
)
save(TOOL, t, nl)

# ---------------------------------------------------------------- fixture (NIT-4): the real r2 capture bytes
if FIX.exists():
    shutil.rmtree(FIX)
FIX.mkdir(parents=True)
for f in sorted(R2.iterdir()):
    if f.is_file() and (f.suffix == ".json" or f.name.endswith(".sha256")):
        shutil.copyfile(f, FIX / f.name)
(FIX / "README.md").write_bytes(
    b"# Fixture: the real WP-P0-12 Path 1 capture r2 (mainnet, 2026-09-17, run p012-path1-20260917T0700Z-1100Z-r2)\n\n"
    b"Byte-identical copies of the tool's outputs for the owner's own account (public address; the ownership\n"
    b"signature was verified at capture time by the tool at af921d75, LF-form tool sha256 in the manifest).\n"
    b"Used by test_capture_own_account_evidence.py to replay the stored bytes (NIT-4): sidecars verify, and\n"
    b"the derived view is reproducible from the stored page bytes. No key, no private data.\n"
)

# ---------------------------------------------------------------- tests
s, nls = load(TESTS)
s = rep(
    s,
    "def test_tampered_stored_bytes_vs_sidecar_refuses(tmp_path, monkeypatch):\n",
    "FIXTURE_R2 = Path(__file__).parent / \"fixtures\" / \"p012_path1_r2_capture\"\n"
    "\n"
    "\n"
    "def test_verify_covers_derived_view_and_manifest_sidecars(tmp_path, monkeypatch):\n"
    "    # NIT-1: CAPTURE_VERIFY_OK used to cover the responses only; the derived view and the manifest\n"
    "    # have sidecars too, and the manifest records the derived digest\n"
    "    patch_info(monkeypatch, FakeInfo())\n"
    "    manifest = cae.run_capture(args(tmp_path))\n"
    "    derived = tmp_path / \"DERIVED_EXTRACTION.json\"\n"
    "    assert manifest[\"derived_extraction_sha256\"] == cae.sha256_bytes(derived.read_bytes())\n"
    "    cae.verify_sidecars(tmp_path)\n"
    "    good = derived.read_bytes()\n"
    "    derived.write_bytes(good.replace(b'\"0.01\"', b'\"0.02\"', 1))\n"
    "    with pytest.raises(cae.CaptureRefused) as exc:\n"
    "        cae.verify_sidecars(tmp_path)\n"
    "    assert exc.value.code == cae.REFUSED_BAD_SIDECAR\n"
    "    assert \"DERIVED_EXTRACTION.json\" in exc.value.detail\n"
    "    # a re-hashed sidecar does not help: the manifest carries the digest\n"
    "    (tmp_path / \"DERIVED_EXTRACTION.json.sha256\").write_text(\n"
    "        cae.sha256_bytes(derived.read_bytes()) + \"\\n\", encoding=\"utf-8\"\n"
    "    )\n"
    "    with pytest.raises(cae.CaptureRefused) as exc:\n"
    "        cae.verify_sidecars(tmp_path)\n"
    "    assert \"differs from the manifest digest\" in exc.value.detail\n"
    "    derived.write_bytes(good)\n"
    "    (tmp_path / \"DERIVED_EXTRACTION.json.sha256\").write_text(\n"
    "        cae.sha256_bytes(good) + \"\\n\", encoding=\"utf-8\"\n"
    "    )\n"
    "    cae.verify_sidecars(tmp_path)\n"
    "    manifest_path = tmp_path / \"CAPTURE_MANIFEST.json\"\n"
    "    manifest_path.write_bytes(manifest_path.read_bytes() + b\"\\n\")\n"
    "    with pytest.raises(cae.CaptureRefused) as exc:\n"
    "        cae.verify_sidecars(tmp_path)\n"
    "    assert exc.value.detail == \"CAPTURE_MANIFEST.json\"\n"
    "\n"
    "\n"
    "def test_stray_sidecar_without_its_file_refuses(tmp_path, monkeypatch):\n"
    "    patch_info(monkeypatch, FakeInfo())\n"
    "    cae.run_capture(args(tmp_path))\n"
    "    (tmp_path / \"ghost.json.sha256\").write_text(\"00\" * 32 + \"\\n\", encoding=\"utf-8\")\n"
    "    with pytest.raises(cae.CaptureRefused) as exc:\n"
    "        cae.verify_sidecars(tmp_path)\n"
    "    assert exc.value.code == cae.REFUSED_BAD_SIDECAR\n"
    "    assert \"ghost.json.sha256 names a missing file\" == exc.value.detail\n"
    "\n"
    "\n"
    "def test_descending_page_refuses_instead_of_truncating(tmp_path, monkeypatch):\n"
    "    # NIT-2: the cursor arithmetic assumes ascending pages; a descending page is refused\n"
    "    later = fill_row(tid=2, time=INSIDE_MS + 1000)\n"
    "    earlier = fill_row(tid=1, time=INSIDE_MS)\n"
    "    patch_info(monkeypatch, FakeInfo(fills=[[later, earlier], [later, earlier]]))\n"
    "    with pytest.raises(cae.CaptureRefused) as exc:\n"
    "        cae.run_capture(args(tmp_path))\n"
    "    assert exc.value.code == cae.REFUSED_MALFORMED\n"
    "    assert \"not in ascending time order\" in exc.value.detail\n"
    "\n"
    "\n"
    "def test_malformed_account_state_keeps_its_bytes_before_refusing(tmp_path, monkeypatch):\n"
    "    # NIT-3: account_state bytes are recorded before the shape check, like the paged queries\n"
    "    patch_info(monkeypatch, FakeInfo(state=[\"not\", \"an\", \"object\"]))\n"
    "    with pytest.raises(cae.CaptureRefused) as exc:\n"
    "        cae.run_capture(args(tmp_path))\n"
    "    assert exc.value.code == cae.REFUSED_MALFORMED\n"
    "    assert \"account state is not an object\" in exc.value.detail\n"
    "    assert (tmp_path / \"account_state.json\").exists()\n"
    "    assert (tmp_path / \"account_state.json.sha256\").exists()\n"
    "\n"
    "\n"
    "def test_fill_without_tid_is_refused_not_guessed():\n"
    "    # NIT-5: hash+oid+time could merge two identical partial fills; the shape is refused\n"
    "    with pytest.raises(cae.CaptureRefused) as exc:\n"
    "        cae.fill_identity(fill_row(tid=None))\n"
    "    assert exc.value.code == cae.REFUSED_MALFORMED\n"
    "    assert \"without tid\" in exc.value.detail\n"
    "    assert cae.fill_identity(fill_row(tid=7)) == \"tid:7\"\n"
    "\n"
    "\n"
    "@pytest.mark.parametrize(\n"
    "    (\"content\", \"fragment\"),\n"
    "    [\n"
    "        (\"{not json\", \"not a JSON object\"),\n"
    "        (\"0xzz\", \"not recoverable\"),\n"
    "        (\"0x\" + \"11\" * 65, \"not recoverable\"),\n"
    "    ],\n"
    ")\n"
    "def test_malformed_signature_is_a_named_refusal(tmp_path, monkeypatch, content, fragment):\n"
    "    # NIT-6: a malformed signature file or signature exits 2 with a named refusal, never a raw\n"
    "    # exception (exit 1)\n"
    "    patch_info(monkeypatch, FakeInfo())\n"
    "    path = tmp_path / \"sig.txt\"\n"
    "    path.write_text(content, encoding=\"utf-8\")\n"
    "    with pytest.raises(cae.CaptureRefused) as exc:\n"
    "        cae.run_capture(args(tmp_path, ownership_signature=path))\n"
    "    assert exc.value.code == cae.REFUSED_BAD_SIGNATURE\n"
    "    assert fragment in exc.value.detail\n"
    "    assert not (tmp_path / \"CAPTURE_MANIFEST.json\").exists()\n"
    "\n"
    "\n"
    "def test_missing_signature_file_and_bad_verify_dir_exit_two(tmp_path, monkeypatch, capsys):\n"
    "    patch_info(monkeypatch, FakeInfo())\n"
    "    rc = cae.main(\n"
    "        [\n"
    "            \"--network\", \"testnet\", \"--address\", ADDRESS, \"--start\", START, \"--end\", END,\n"
    "            \"--out\", str(tmp_path / \"out\"), \"--run-id\", \"run-1\",\n"
    "            \"--ownership-signature\", str(tmp_path / \"absent.txt\"),\n"
    "        ]\n"
    "    )\n"
    "    assert rc == 2\n"
    "    assert cae.REFUSED_BAD_SIGNATURE in capsys.readouterr().err\n"
    "    rc = cae.main([\"--verify-existing\", str(tmp_path / \"no-such-dir\")])\n"
    "    assert rc == 2\n"
    "    assert cae.REFUSED_BAD_SIDECAR in capsys.readouterr().err\n"
    "\n"
    "\n"
    "def test_manifest_carries_the_signed_text_and_signature(tmp_path, monkeypatch):\n"
    "    # NIT-7: the exact signed text and the signature are stored in the manifest (the message\n"
    "    # still binds address + run_id only - changing it is the owner's call)\n"
    "    account = Account.create()\n"
    "    patch_info(monkeypatch, FakeInfo())\n"
    "    path = signed(account, \"run-7\", tmp_path)\n"
    "    manifest = cae.run_capture(\n"
    "        args(tmp_path, address=account.address, ownership_signature=path, run_id=\"run-7\")\n"
    "    )\n"
    "    evidence = manifest[\"ownership_evidence\"]\n"
    "    assert evidence[\"status\"] == \"OWNERSHIP_EVIDENCE: VERIFIED\"\n"
    "    assert evidence[\"message\"] == cae.ownership_message(account.address, \"run-7\")\n"
    "    assert evidence[\"signature\"] == path.read_text(encoding=\"utf-8\").strip()\n"
    "    assert evidence[\"binds\"] == \"address+run_id\"\n"
    "    stored = read_json(tmp_path / \"CAPTURE_MANIFEST.json\")[\"ownership_evidence\"]\n"
    "    assert stored == evidence\n"
    "\n"
    "\n"
    "def test_real_r2_capture_bytes_replay(tmp_path):\n"
    "    # NIT-4: the stored bytes of the real r2 capture (mainnet, 2026-09-17) verify, and the derived\n"
    "    # view is reproducible from the stored page bytes with the current identity/derivation code\n"
    "    cae.verify_sidecars(FIXTURE_R2)\n"
    "    manifest = read_json(FIXTURE_R2 / \"CAPTURE_MANIFEST.json\")\n"
    "    assert manifest[\"run_id\"] == \"p012-path1-20260917T0700Z-1100Z-r2\"\n"
    "    assert manifest[\"network\"] == \"mainnet\"\n"
    "    assert len(manifest[\"responses\"]) == 5\n"
    "    derived = read_json(FIXTURE_R2 / \"DERIVED_EXTRACTION.json\")\n"
    "\n"
    "    def rows(kind: str, identity):\n"
    "        digest = next(\n"
    "            e[\"response_sha256\"] for e in manifest[\"responses\"] if e[\"file\"] == f\"{kind}_pass1_page001.json\"\n"
    "        )\n"
    "        page = read_json(FIXTURE_R2 / f\"{kind}_pass1_page001.json\")\n"
    "        return [\n"
    "            {\"identity\": identity(row), \"row\": row, \"capture_sha256\": digest, \"json_pointer\": f\"/{i}\"}\n"
    "            for i, row in enumerate(page)\n"
    "        ]\n"
    "\n"
    "    assert cae.fill_derived(rows(\"fills\", cae.fill_identity)) == derived[\"fills\"]\n"
    "    assert cae.funding_derived(rows(\"funding\", cae.funding_identity)) == derived[\"funding\"]\n"
    "    assert len(derived[\"fills\"]) == 2 and len(derived[\"funding\"]) == 3\n"
    "    # the old manifest (af921d75) has no derived digest; verification tolerates its absence\n"
    "    assert \"derived_extraction_sha256\" not in manifest\n"
    "\n"
    "\n"
    "def test_tampered_stored_bytes_vs_sidecar_refuses(tmp_path, monkeypatch):\n",
    "tests",
)
save(TESTS, s, nls)
print("P1CAP NIT slice patched: tool, tests, fixture", len(list(FIX.iterdir())), "files")
