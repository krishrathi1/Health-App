from app.services.consult_service import get_consult_service


def test_consult_creation():
    svc = get_consult_service()
    c = svc.create_consult(user_id="u_1", symptoms_text="fever", triage_level="urgent")
    assert c["id"] in [x["id"] for x in svc.list_consults(user_id="u_1")]

