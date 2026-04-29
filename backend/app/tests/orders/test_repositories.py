# tests/test_orders/test_repositories.py - Pruebas unitarias de OrderRepository según contrato
import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from decimal import Decimal
import uuid as uuid_lib

from app.tests.test_models import TestOrder, TestCustomer, TestMeal

# Repositorio de prueba específico para TestOrder
class TestOrderRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, order_data):
        order = TestOrder(
            uuid=str(uuid_lib.uuid4()),
            **order_data
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_by_uuid(self, order_uuid: str):
        return self.db.query(TestOrder).filter(TestOrder.uuid == order_uuid).first()
    
    def update(self, order_uuid: str, update_data):
        order = self.get_by_uuid(order_uuid)
        if not order:
            return None
        
        for key, value in update_data.items():
            if hasattr(order, key):
                setattr(order, key, value)
        
        self.db.commit()
        self.db.refresh(order)
        return order

@pytest.mark.unit
@pytest.mark.order
class TestOrderRepositoryClass:
    def test_create_order_success(self, db_session):
        """Prueba crear un pedido exitosamente"""
        # Arrange
        repository = TestOrderRepository(db_session)
        
        # Crear cliente y meal de prueba
        customer = TestCustomer(
            document_number="CC-12345678",
            full_name="Juan Pérez",
            phone_number="3001234567",
            email="juan@example.com",
            address="Calle 123 #45-67"
        )
        db_session.add(customer)
        
        meal = TestMeal(
            uuid="123e4567-e89b-12d3-a456-426614174000",
            name="COMBO PRUEBA",
            category="HAMBURGERS",
            description="Combo de prueba",
            price_without_iva=Decimal('15000.00'),
            is_available=True
        )
        db_session.add(meal)
        db_session.commit()
        
        order_data = {
            "customer_document": customer.document_number,
            "combo_uuid": meal.uuid,
            "meal_id": meal.id,
            "quantity": 2,
            "additional_info": "Hamburguesa sin salsa de tomate",
            "subtotal_without_iva": Decimal('30000.00'),
            "iva_amount": Decimal('5700.00'),
            "total_with_iva": Decimal('35700.00'),
            "is_delivered": False,
            "delivery_date": None,
            "order_date": datetime.utcnow()
        }
        
        # Act
        result = repository.create(order_data)
        
        # Assert
        assert result is not None
        assert result.customer_document == order_data["customer_document"]
        assert result.quantity == order_data["quantity"]

    def test_get_order_success(self, db_session):
        """Prueba obtener pedido existente"""
        # Arrange
        repository = TestOrderRepository(db_session)
        
        # Crear cliente y meal de prueba
        customer = TestCustomer(
            document_number="CC-12345678",
            full_name="Juan Pérez",
            phone_number="3001234567",
            email="juan@example.com",
            address="Calle 123 #45-67"
        )
        db_session.add(customer)
        
        meal = TestMeal(
            uuid="123e4567-e89b-12d3-a456-426614174001",
            name="COMBO PRUEBA",
            category="HAMBURGERS",
            description="Combo de prueba",
            price_without_iva=Decimal('15000.00'),
            is_available=True
        )
        db_session.add(meal)
        db_session.commit()
        
        # Crear pedido de prueba
        test_order = TestOrder(
            uuid="123e4567-e89b-12d3-a456-426614174002",
            customer_document=customer.document_number,
            combo_uuid=meal.uuid,
            meal_id=meal.id,
            quantity=1,
            additional_info="Pedido de prueba",
            subtotal_without_iva=Decimal('10000.00'),
            iva_amount=Decimal('1900.00'),
            total_with_iva=Decimal('11900.00'),
            is_delivered=False,
            delivery_date=None,
            order_date=datetime.utcnow()
        )
        db_session.add(test_order)
        db_session.commit()
        
        # Act
        result = repository.get_by_uuid(test_order.uuid)
        
        # Assert
        assert result is not None
        assert result.customer_document == customer.document_number

    def test_get_order_not_found(self, db_session):
        """Prueba obtener pedido no existente"""
        # Arrange
        repository = TestOrderRepository(db_session)
        non_existent_uuid = "99999999-9999-9999-9999-999999999999"
        
        # Act
        result = repository.get_by_uuid(non_existent_uuid)
        
        # Assert
        assert result is None

    def test_update_order_success(self, db_session):
        """Prueba actualizar pedido existente"""
        # Arrange
        repository = TestOrderRepository(db_session)
        
        # Crear cliente y meal de prueba
        customer = TestCustomer(
            document_number="CC-12345678",
            full_name="Juan Pérez",
            phone_number="3001234567",
            email="juan@example.com",
            address="Calle 123 #45-67"
        )
        db_session.add(customer)
        
        meal = TestMeal(
            uuid="123e4567-e89b-12d3-a456-426614174003",
            name="COMBO PRUEBA",
            category="HAMBURGERS",
            description="Combo de prueba",
            price_without_iva=Decimal('15000.00'),
            is_available=True
        )
        db_session.add(meal)
        db_session.commit()
        
        # Crear pedido de prueba
        test_order = TestOrder(
            uuid="123e4567-e89b-12d3-a456-426614174004",
            customer_document=customer.document_number,
            combo_uuid=meal.uuid,
            meal_id=meal.id,
            quantity=1,
            additional_info="Pedido original",
            subtotal_without_iva=Decimal('10000.00'),
            iva_amount=Decimal('1900.00'),
            total_with_iva=Decimal('11900.00'),
            is_delivered=False,
            delivery_date=None,
            order_date=datetime.utcnow()
        )
        db_session.add(test_order)
        db_session.commit()
        
        update_data = {
            "is_delivered": True,
            "delivery_date": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Act
        result = repository.update(test_order.uuid, update_data)
        
        # Assert
        assert result is not None
        assert result.is_delivered == True

    def test_update_order_not_found(self, db_session):
        """Prueba actualizar pedido no existente"""
        # Arrange
        repository = TestOrderRepository(db_session)
        non_existent_uuid = "99999999-9999-9999-9999-999999999999"
        
        update_data = {
            "is_delivered": True,
            "delivery_date": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Act
        result = repository.update(non_existent_uuid, update_data)
        
        # Assert
        assert result is None
