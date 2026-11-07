import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError


def get_engine(database_url: str = None):
    if database_url is None:
        database_url = os.environ["DATABASE_URL"]
    try:
        return create_engine(database_url, echo=True)
    except SQLAlchemyError as e:
        print(f"Error creating engine: {e}")
        raise

def get_sessionmaker(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
engine = get_engine()
SessionLocal = get_sessionmaker(engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

