from sqlalchemy import Integer
from datetime import datetime
from passlib.context import CryptContext
from app.database import Base

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(51), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    password_hash = Column(String(255), nullable=False)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    
    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password_hash)

