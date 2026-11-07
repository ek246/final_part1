from app.models.users import Users
import pytest

def test_password_hashing():
    origin_password = "my_password"
    hashed_password = Users.hash_password(origin_password)
    fake_user = Users(id=1, username="JDoe", email="jdoe@example.com", password_hash=hashed_password)
    assert hashed_password != origin_password
    assert fake_user.verify_password(origin_password) is True
    assert fake_user.verify_password("wrong_password") is False




