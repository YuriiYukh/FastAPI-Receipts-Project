# app/models/receipt.py
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_type = Column(String, nullable=False)
    payment_amount = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    rest = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="receipts")
    products = relationship(
        "Product", back_populates="receipt", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Receipt(id={self.id}, user_id={self.user_id}, total={self.total})>"
