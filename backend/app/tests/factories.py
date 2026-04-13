# tests/factories.py - Factorías para crear datos de prueba
import pytest
from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
from factory import Sequence, LazyAttribute
from decimal import Decimal
import uuid
from datetime import datetime

# Importar modelos reales
from app.customers.model import Customer
from app.meals.model import Meal
from app.orders.model import Order

fake = Faker()

class CustomerFactory(SQLAlchemyModelFactory):
    """Factory para crear clientes de prueba"""
    class Meta:
        model = Customer
        sqlalchemy_session_persistence = "flush"
    
    document_number = Sequence(lambda n: f"CC-{n:08d}")
    full_name = LazyAttribute(lambda _: fake.name())
    email = LazyAttribute(lambda _: fake.email())
    phone_number = LazyAttribute(lambda _: fake.numerify('3########'))
    address = LazyAttribute(lambda _: fake.address())

class MealFactory(SQLAlchemyModelFactory):
    """Factory para crear combos de prueba"""
    class Meta:
        model = Meal
        sqlalchemy_session_persistence = "flush"
    
    uuid = LazyAttribute(lambda _: str(uuid.uuid4()))
    name = LazyAttribute(lambda _: fake.sentence())
    category = LazyAttribute(lambda _: fake.word())
    description = LazyAttribute(lambda _: fake.sentence())
    price_without_iva = LazyAttribute(lambda _: Decimal('25000.00'))
    is_available = LazyAttribute(lambda _: True)

class OrderFactory(SQLAlchemyModelFactory):
    """Factory para crear pedidos de prueba"""
    class Meta:
        model = Order
        sqlalchemy_session_persistence = "flush"
    
    uuid = LazyAttribute(lambda _: str(uuid.uuid4()))
    customer_document = LazyAttribute(lambda _: fake.unique.numerify('CC-########'))
    meal_id = LazyAttribute(lambda _: fake.random_int(min=1, max=100))
    combo_uuid = LazyAttribute(lambda _: str(uuid.uuid4()))
    quantity = LazyAttribute(lambda _: fake.random_int(min=1, max=10))
    additional_info = LazyAttribute(lambda _: fake.sentence())
    subtotal_without_iva = LazyAttribute(lambda _: Decimal('15000.00'))
    iva_amount = LazyAttribute(lambda _: Decimal('2850.00'))
    total_with_iva = LazyAttribute(lambda _: Decimal('17850.00'))
    is_delivered = LazyAttribute(lambda _: fake.boolean())
    order_date = LazyAttribute(lambda _: datetime.now())
    delivery_date = LazyAttribute(lambda _: None)
    document = LazyAttribute(lambda _: fake.unique.numerify('CC-########'))
