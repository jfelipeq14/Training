# orders/model.py
from sqlalchemy import Column, Integer, String, Boolean, Text, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from datetime import datetime

from config.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)
    order_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    customer_document = Column(String(20), ForeignKey('customers.document_number'), nullable=False, index=True)
    meal_id = Column(Integer, ForeignKey('meals.id'), nullable=False, index=True)
    combo_uuid = Column(UUID(as_uuid=True), ForeignKey('meals.uuid'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    additional_info = Column(Text, nullable=True)
    subtotal_without_iva = Column(Numeric(10, 2), nullable=False)
    iva_amount = Column(Numeric(10, 2), nullable=False)
    total_with_iva = Column(Numeric(10, 2), nullable=False)
    is_delivered = Column(Boolean, default=False, nullable=False, index=True)
    delivery_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Order(id={self.id}, uuid={self.uuid}, customer='{self.customer_document}', meal_id={self.meal_id})>"
