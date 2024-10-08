# app/models/product.py
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    receipt = relationship("Receipt", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, quantity={self.quantity}, total={self.total})>"
