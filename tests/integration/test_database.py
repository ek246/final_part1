from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import pytest
from unittest.mock import MagicMock
from app import database

from app.models.users import Users

def test_create_user_model():
    user = Users(id=1, username="JDoe", email="jdoe@example.com", password_hash="hashed_password")
    assert user.id == 1
    assert user.username == "JDoe"
    assert user.email == "jdoe@example.com"
    assert user.password_hash == "hashed_password"

def test_save_user_to_db(db_session):
    user = Users(username="JDoe", email="jdoe@example.com", password_hash="hashed_password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    assert user.id is not None
    assert user.created_at is not None
    assert user.username == "JDoe"
    assert user.email == "jdoe@example.com"
    assert user.password_hash == "hashed_password"

def test_retrieve_user_from_db(db_session):
    user = Users(username="JDoe", email="jdoe@example.com", password_hash="hashed_password")
    db_session.add(user)
    db_session.commit()
    retrieved_user = db_session.query(Users).filter_by(username="JDoe").first()
    assert retrieved_user is not None
    assert retrieved_user.username == "JDoe"
    assert retrieved_user.email == "jdoe@example.com"
    assert retrieved_user.password_hash == "hashed_password"
    assert retrieved_user.id == user.id

def test_deny_duplicate_emails(db_session):
    user1 = Users(username="JDoe", email="jdoe@example.com", password_hash="hashed_password")
    user2 = Users(username="LDoe", email="jdoe@example.com", password_hash="hashed_password")
    db_session.add(user1)
    db_session.commit()
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()  # Rollback the session to clean up after the failed commit
    
    

def test_deny_duplicate_usernames(db_session):
    user1 = Users(username="JDoe", email="jdoe@example.com", password_hash="hashed_password")
    user2 = Users(username="JDoe", email="ldoe@example.com", password_hash="hashed_password")
    db_session.add(user1)
    db_session.commit()
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()  # Rollback the session to clean up after the failed commit

def test_get_engine_error(monkeypatch, capsys):
    mock_create_engine = MagicMock(side_effect=SQLAlchemyError("Engine creation failed"))
    monkeypatch.setattr(database, "create_engine", mock_create_engine)

    with pytest.raises(SQLAlchemyError, match="Engine creation failed"):
        database.get_engine("postgresql://unused:")
    
    assert "Error creating engine" in capsys.readouterr().out

def test_get_db_closes_session(monkeypatch):
    session = MagicMock()
    monkeypatch.setattr(
        database, "SessionLocal", MagicMock(return_value=session)
    )

    dependency = database.get_db()

    assert next(dependency) is session
    session.close.assert_not_called()

    with pytest.raises(StopIteration):
        next(dependency)

    session.close.assert_called_once()

def test_get_db_closes_on_error(monkeypatch):
    session = MagicMock()
    monkeypatch.setattr(
        database, "SessionLocal", MagicMock(return_value=session)
    )

    dependency = database.get_db()
    next(dependency)

    with pytest.raises(RuntimeError, match="Request failed"):
        dependency.throw(RuntimeError("Request failed"))

    session.close.assert_called_once()
