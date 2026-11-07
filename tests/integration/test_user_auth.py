from app.models.users import Users
import pytest

from app.schemas.userSchema import UserCreate, UserRead

def save_password_hash(db_session):
    origin_password = "my_password"
    hashed_password = Users.hash_password(origin_password)
    user = Users(id=1, username="JDoe", email="jdoe@example.com", password_hash=hashed_password)

    db_session.add(user)
    db_session.commit()
    db_session.expunge_all(user)  # Detach the user instance from the session

    saved_user = db_session.query(Users).filter_by(username="JDoe").first()
    assert saved_user is not None
    assert saved_user.verify_password(origin_password) is True
    assert saved_user.password_hash != origin_password  # Ensure the password is hashed
    assert saved_user.password_hash == hashed_password  # Ensure the saved hash matches the original hash
    assert saved_user.verify_password("wrong_password") is False  # Ensure wrong password fails verification

def test_correct_password_after_saving_db(db_session):
    user_data = UserCreate(username="JDoe", email="jdoe@example.com", password="my_password")
    user = Users(username=user_data.username, email=user_data.email, password_hash=Users.hash_password(user_data.password))
    db_session.add(user)
    db_session.commit()
    db_session.expunge(user)  # Detach the user instance from the session

    saved_user = db_session.query(Users).filter_by(username="JDoe").first()
    assert saved_user is not None
    assert saved_user.verify_password(user_data.password) is True  # Ensure the correct password verifies
    assert saved_user.verify_password("wrong_password") is False  # Ensure wrong password fails verification

    profile = UserRead.model_validate(saved_user)
    assert profile.username == user_data.username
    assert profile.email == user_data.email