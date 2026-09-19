"""Lead probe (J-03 real edge): REGISTRAR deployment-refresh event, accepted catalog CONFIGURED, catalog_backed=True,
no evaluation_run_hash (registrar events must not carry one). Pre-fix ledger vs P31FIX candidate."""
import sys, pathlib
from datetime import timedelta
root = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(root / "MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests"))
sys.path.insert(0, str(root / "MTC_COMMAND_CENTER/03_QUANTLENS/tools"))
sys.path.insert(0, str(root / "MTC_COMMAND_CENTER/contracts"))
import test_p031_lifecycle_ledger as T
tc = T.LifecycleLedgerTests("test_catalog_backed_argument_must_be_bool")
tc.setUp()
try:
    ledger = tc.new_ledger("lead-registrar-probe", accepted_evaluation_catalog=(T.EVALUATION_A,))
    cand = "QLC-20260913-lead-registrar-probe"
    tc.append_frozen_fixture(ledger, cand, "lead-registrar-probe")
    tc.append_authority_event(ledger, candidate_id=cand, event_id="lead-probe-shadow", event_type="SHADOW_ELIGIBLE",
        previous_state="FROZEN", next_state="SHADOW", writer_class="ENVIRONMENT_ADMISSION_AUTHORITY", writer_id="admission-1",
        check_set_version="shadow-eligibility.v1", evaluation_run_hash=T.EVALUATION_A, catalog_backed=True)
    print("state before probe:", T.observed_state(ledger.current_state(cand)))
    registrar = T.Registrar(ledger, "registrar-1")
    ev = T.event(event_id="lead-registrar-refresh-catalog-backed-no-hash", event_type="FROZEN", previous_state="SHADOW", next_state="FROZEN",
                 candidate_id=cand, package_hash=T.PACKAGE_A, deployment_identity_hash=T.DEPLOYMENT_B,
                 evidence_references=("fixture://lead-probe/registrar-refresh",), timestamp=T.BASE_TIME + timedelta(seconds=9))
    try:
        registrar.append(ev, catalog_backed=True)
        rec = ledger.current_state(cand)
        print("RESULT: APPENDED (fail-open) state=%s" % T.observed_state(rec))
    except ValueError as exc:
        print("RESULT: REFUSED", exc)
finally:
    tc.tearDown()
