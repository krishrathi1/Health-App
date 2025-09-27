from app.utils.security_utils import AuthService


def test_register_and_login():
    auth = AuthService()
    assert auth.register_user(name="A", phone="123", password="pw")
    token = auth.login(phone="123", password="pw")
    assert token is not None

