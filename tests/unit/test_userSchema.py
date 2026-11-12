from app.schemas.userSchema import UserCreate, UserRead
import pytest
from datetime import datetime
from pydantic import ValidationError
def test_user_create_schema():
    user_create = UserCreate(username="JDoe", email="jdoe@example.com", password="my_password")
    assert user_create.username == "JDoe"
    assert user_create.email == "jdoe@example.com"
    assert user_create.password == "my_password"
def test_user_read_schema():
    user_read = UserRead(id=1, username="JDoe", email="jdoe@example.com", created_at="2024-06-06T12:00:00")
    assert user_read.id == 1
    assert user_read.username == "JDoe"
    assert user_read.email == "jdoe@example.com"
    assert user_read.created_at == datetime(2024, 6, 6, 12, 0, 0)

def test_user_create_invalid_username():
    with pytest.raises(ValidationError):
        UserCreate(username="jj", email="jdoe@example.com", password="my_password")
    with pytest.raises(ValidationError):
        UserCreate(username="a" * 51, email="jdoe@example.com", password="my_password") 
def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="JDoe", email="invalid_email", password="my_password")
def test_user_create_invalid_password():
    with pytest.raises(ValidationError):
        UserCreate(username="JDoe", email="jdoe@example.com", password="short")
def test_user_create_missing_fields():
    with pytest.raises(ValidationError):
        UserCreate(username="JDoe", email="jdoe@example.com")
    with pytest.raises(ValidationError):
        UserCreate(email="jdoe@example.com", password="my_password")
    with pytest.raises(ValidationError):
        UserCreate(username="JDoe", password="my_password")
    with pytest.raises(ValidationError):
        UserCreate()
def test_user_read_excludes_sensitive_fields():
    fake_user = data = {
        "id": 1,
        "username": "JDoe",
        "email": "jdoe@example.com",
        "created_at": "2024-06-06T12:00:00",
        "password": "my_password"
    }
    profile = UserRead.model_validate(fake_user).model_dump()
    assert profile["username"] == "JDoe"
    assert "password" not in profile
    assert "password_hash" not in profile