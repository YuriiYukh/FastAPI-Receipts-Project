# app/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    receipts = relationship("Receipt", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
