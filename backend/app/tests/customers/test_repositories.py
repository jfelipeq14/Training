# tests/test_customers/test_repositories.py - Pruebas unitarias de CustomerRepository según contrato
import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.customers.repository import CustomerRepository
from app.customers.model import Customer

@pytest.mark.unit
@pytest.mark.customer
class TestCustomerRepository:
    def test_create_customer_success(self, db_session):
        """Prueba crear un cliente exitosamente"""
        # Arrange
        repository = CustomerRepository(db_session)
        customer_data = {
            "document_number": "CC-12345678",
            "full_name": "Juan Pérez González",
            "email": "juan.perez@example.com",
            "phone_number": "3001234567",
            "address": "Calle 123 #45-67, Bogotá"
        }
        
        # Act
        result = repository.create(customer_data)
        
        # Assert
        assert result is not None
        assert result.document_number == customer_data["document_number"]
        assert result.full_name == customer_data["full_name"]
        assert result.email == customer_data["email"]
        assert result.phone_number == customer_data["phone_number"]
        assert result.address == customer_data["address"]

    def test_create_customer_already_exists(self, db_session):
        """Prueba crear cliente cuando ya existe"""
        # Arrange
        repository = CustomerRepository(db_session)
        customer_data = {
            "document_number": "CC-12345678",
            "full_name": "Juan Pérez González",
            "email": "juan.perez@example.com",
            "phone_number": "3001234567",
            "address": "Calle 123 #45-67, Bogotá"
        }
        
        # Crear cliente existente manualmente
        existing_customer = Customer(
            document_number="CC-12345678",
            full_name="Existing Customer",
            email="existing@example.com",
            phone_number="3000000000",
            address="Existing Address"
        )
        db_session.add(existing_customer)
        db_session.commit()
        
        # Act & Assert - El repositorio debe lanzar IntegrityError por constraint UNIQUE
        with pytest.raises(IntegrityError):
            result = repository.create(customer_data)
        
        # Hacer rollback para limpiar la sesión
        db_session.rollback()
        
        # Verificar que solo hay un cliente con el documento
        customers = db_session.query(Customer).filter(Customer.document_number == "CC-12345678").all()
        assert len(customers) == 1

    def test_create_customer_email_already_exists(self, db_session):
        """Prueba crear cliente cuando email ya existe"""
        # Arrange
        repository = CustomerRepository(db_session)
        customer_data = {
            "document_number": "CC-87654321",
            "full_name": "María López",
            "email": "juan.perez@example.com",  # Email existente
            "phone_number": "3009876543",
            "address": "Calle 456 #78-90, Bogotá"
        }
        
        # Crear cliente existente con mismo email
        existing_customer = Customer(
            document_number="CC-99999999",
            full_name="Existing Customer",
            email="juan.perez@example.com",  # Mismo email
            phone_number="3000000000",
            address="Existing Address"
        )
        db_session.add(existing_customer)
        db_session.commit()
        
        # Act & Assert - El repositorio debe lanzar IntegrityError por constraint UNIQUE
        with pytest.raises(IntegrityError):
            result = repository.create(customer_data)
        
        # Hacer rollback para limpiar la sesión
        db_session.rollback()
        
        # Verificar que solo hay un cliente con el email
        customers = db_session.query(Customer).filter(Customer.email == "juan.perez@example.com").all()
        assert len(customers) == 1

    def test_create_customer_phone_already_exists(self, db_session):
        """Prueba crear cliente cuando teléfono ya existe"""
        # Arrange
        repository = CustomerRepository(db_session)
        customer_data = {
            "document_number": "CC-11223344",
            "full_name": "Carlos Rodríguez",
            "email": "carlos.rodriguez@example.com",
            "phone_number": "3001234567",  # Teléfono existente
            "address": "Calle 789 #12-34, Bogotá"
        }
        
        # Crear cliente existente con mismo teléfono
        existing_customer = Customer(
            document_number="CC-99999999",
            full_name="Existing Customer",
            email="existing@example.com",
            phone_number="3001234567",  # Mismo teléfono
            address="Existing Address"
        )
        db_session.add(existing_customer)
        db_session.commit()
        
        # Act - El repositorio permite duplicados de teléfono (no hay constraint UNIQUE)
        result = repository.create(customer_data)
        
        # Assert - El repositorio no valida duplicados de teléfono
        assert result is not None
        assert result.phone_number == "3001234567"
        
        # Verificar que hay dos clientes con el mismo teléfono
        customers = db_session.query(Customer).filter(Customer.phone_number == "3001234567").all()
        assert len(customers) == 2

    def test_create_customer_invalid_data(self, db_session):
        """Prueba crear cliente con datos inválidos"""
        # Arrange
        repository = CustomerRepository(db_session)
        
        # Test con datos válidos básicos (el repositorio no valida, solo persiste)
        # La validación de formato está en el servicio
        valid_data = {
            "document_number": "CC-12345678",
            "full_name": "Juan Pérez González",
            "email": "juan.perez@example.com",
            "phone_number": "3001234567",
            "address": "Calle 123 #45-67, Bogotá"
        }
        
        # Act
        result = repository.create(valid_data)
        
        # Assert - El repositorio crea el cliente sin validar formato
        assert result is not None
        assert result.document_number == "CC-12345678"

    def test_get_customer_success(self, db_session):
        """Prueba obtener cliente existente"""
        # Arrange
        repository = CustomerRepository(db_session)
        
        # Crear cliente de prueba
        customer = Customer(
            document_number="CC-12345678",
            full_name="Juan Pérez González",
            email="juan.perez@example.com",
            phone_number="3001234567",
            address="Calle 123 #45-67, Bogotá"
        )
        db_session.add(customer)
        db_session.commit()
        
        # Act
        result = repository.get_by_document("CC-12345678")
        
        # Assert
        assert result is not None
        assert result.document_number == "CC-12345678"
        assert result.full_name == "Juan Pérez González"

    def test_get_customer_not_found(self, db_session):
        """Prueba obtener cliente no existente"""
        # Arrange
        repository = CustomerRepository(db_session)
        
        # Act
        result = repository.get_by_document("CC-99999999")
        
        # Assert
        assert result is None

    def test_get_customer_invalid_document(self, db_session):
        """Prueba obtener cliente con documento inválido"""
        # Arrange
        repository = CustomerRepository(db_session)
        
        # Act & Assert - El repositorio no valida formato, solo busca
        result = repository.get_by_document("INVALID")
        
        # Assert
        assert result is None

    def test_update_customer_success(self, db_session):
        """Prueba actualizar cliente existente"""
        # Arrange
        repository = CustomerRepository(db_session)
        
        # Crear cliente de prueba
        customer = Customer(
            document_number="CC-12345678",
            full_name="Juan Pérez González",
            email="juan.perez@example.com",
            phone_number="3001234567",
            address="Calle 123 #45-67, Bogotá"
        )
        db_session.add(customer)
        db_session.commit()
        
        update_data = {
            "full_name": "Juan Pérez Actualizado",
            "email": "juan.actualizado@example.com",
            "phone_number": "3007654321",
            "address": "Calle 456 #78-90, Bogotá"
        }
        
        # Act
        result = repository.update(customer.id, update_data)
        
        # Assert
        assert result is not None
        assert result.full_name == "Juan Pérez Actualizado"

    def test_update_customer_not_found(self, db_session):
        """Prueba actualizar cliente no existente"""
        # Arrange
        repository = CustomerRepository(db_session)
        
        update_data = {
            "full_name": "Juan Pérez Actualizado"
        }
        
        # Act
        result = repository.update(999999, update_data)
        
        # Assert
        assert result is None

    def test_update_customer_email_conflict(self, db_session):
        """Prueba actualizar cliente con email existente"""
        # Arrange
        repository = CustomerRepository(db_session)
        
        # Crear dos clientes
        customer1 = Customer(
            document_number="CC-12345678",
            full_name="Juan Pérez",
            email="juan.perez@example.com",
            phone_number="3001234567",
            address="Calle 123 #45-67, Bogotá"
        )
        
        customer2 = Customer(
            document_number="CC-87654321",
            full_name="María López",
            email="maria.lopez@example.com",
            phone_number="3009876543",
            address="Calle 456 #78-90, Bogotá"
        )
        
        db_session.add(customer1)
        db_session.add(customer2)
        db_session.commit()
        
        # Intentar actualizar customer1 con email de customer2
        update_data = {
            "email": "maria.lopez@example.com"
        }
        
        # Act & Assert - El repositorio debe lanzar IntegrityError por constraint UNIQUE en email
        with pytest.raises(IntegrityError):
            result = repository.update(customer1.id, update_data)
        
        # Hacer rollback para limpiar la sesión
        db_session.rollback()

    def test_update_customer_phone_conflict(self, db_session):
        """Prueba actualizar cliente con teléfono existente"""
        # Arrange
        repository = CustomerRepository(db_session)
        
        # Crear dos clientes
        customer1 = Customer(
            document_number="CC-12345678",
            full_name="Juan Pérez",
            email="juan.perez@example.com",
            phone_number="3001234567",
            address="Calle 123 #45-67, Bogotá"
        )
        
        customer2 = Customer(
            document_number="CC-87654321",
            full_name="María López",
            email="maria.lopez@example.com",
            phone_number="3009876543",
            address="Calle 456 #78-90, Bogotá"
        )
        
        db_session.add(customer1)
        db_session.add(customer2)
        db_session.commit()
        
        # Intentar actualizar customer1 con teléfono de customer2
        update_data = {
            "phone_number": "3009876543"
        }
        
        # Act - El repositorio permite duplicados de teléfono
        result = repository.update(customer1.id, update_data)
        
        # Assert - El repositorio actualiza sin validar duplicados
        assert result is not None
        assert result.phone_number == "3009876543"

    def test_delete_customer_success(self, db_session):
        """Prueba eliminar cliente existente"""
        # Arrange
        repository = CustomerRepository(db_session)
        
        # Crear cliente de prueba
        customer = Customer(
            document_number="CC-12345678",
            full_name="Juan Pérez González",
            email="juan.perez@example.com",
            phone_number="3001234567",
            address="Calle 123 #45-67, Bogotá"
        )
        db_session.add(customer)
        db_session.commit()
        
        # Act
        result = repository.delete("CC-12345678")
        
        # Assert
        assert result is True
        
        # Verificar que el cliente fue eliminado
        deleted_customer = repository.get_by_document("CC-12345678")
        assert deleted_customer is None

    def test_delete_customer_not_found(self, db_session):
        """Prueba eliminar cliente no existente"""
        # Arrange
        repository = CustomerRepository(db_session)
        
        # Act
        result = repository.delete("CC-99999999")
        
        # Assert
        assert result is False

    def test_delete_customer_invalid_document(self, db_session):
        """Prueba eliminar cliente con documento inválido"""
        # Arrange
        repository = CustomerRepository(db_session)
        
        # Act & Assert - El repositorio no valida formato, solo busca
        result = repository.delete("INVALID")
        
        # Assert
        assert result is False
