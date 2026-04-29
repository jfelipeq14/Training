# tests/test_models.py - Modelos compatibles con SQLite para pruebas
from sqlalchemy import Column, Integer, String, Boolean, Text, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base
import uuid
from decimal import Decimal
from datetime import datetime

# Base para modelos de prueba
TestBase = declarative_base()

# Modelo Customer compatible con SQLite
class TestCustomer(TestBase):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    document_number = Column(String(20), nullable=False, unique=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone_number = Column(String(10), nullable=False)
    address = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<TestCustomer(id={self.id}, document_number='{self.document_number}', full_name='{self.full_name}')>"

# Modelo Meal compatible con SQLite (UUID como String)
class TestMeal(TestBase):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, nullable=False, index=True)  # UUID como String
    name = Column(String(255), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    price_without_iva = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<TestMeal(id={self.id}, uuid='{self.uuid}', name='{self.name}', category='{self.category}')>"

# Modelo Order compatible con SQLite (UUID como String)
class TestOrder(TestBase):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, nullable=False, index=True)  # UUID como String
    order_date = Column(DateTime(timezone=True), nullable=False)
    customer_document = Column(String(20), ForeignKey("customers.document_number"), nullable=False)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    combo_uuid = Column(String(36), ForeignKey("meals.uuid"), nullable=False)  # UUID como String
    quantity = Column(Integer, nullable=False)
    additional_info = Column(Text, nullable=True)
    subtotal_without_iva = Column(Numeric(10, 2), nullable=False)
    iva_amount = Column(Numeric(10, 2), nullable=False)
    total_with_iva = Column(Numeric(10, 2), nullable=False)
    is_delivered = Column(Boolean, default=False, nullable=False)
    delivery_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones
    customer = relationship("TestCustomer", backref="orders")
    meal = relationship("TestMeal", backref="orders", foreign_keys=[meal_id])
    
    def __repr__(self):
        return f"<TestOrder(id={self.id}, uuid='{self.uuid}', customer_document='{self.customer_document}', meal_id={self.meal_id})>"
