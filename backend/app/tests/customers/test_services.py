# tests/test_customers/test_services.py - Pruebas unitarias de CustomerService según contrato
import pytest
from unittest.mock import Mock, patch

from app.customers.service import CustomerService
from app.customers.repository import CustomerRepository
from app.customers.model import Customer
from app.customers.schema import CustomerCreate, CustomerUpdate
from app.tests.factories import CustomerFactory

@pytest.mark.unit
@pytest.mark.customer
class TestCustomerService:
    def test_create_customer_success(self):
        """Prueba crear cliente exitosamente"""
        # Arrange
        mock_customer = Mock()
        mock_customer.id = 1
        mock_customer.document_number = "CC-12345678"
        mock_customer.full_name = "Juan Pérez González"
        mock_customer.email = "juan.perez@email.com"
        mock_customer.phone_number = "3001234567"
        mock_customer.address = "Calle 123 #45-67, Bogotá"
        mock_customer.created_at = "2024-01-15T10:30:00Z"
        mock_customer.updated_at = "2024-01-15T10:30:00Z"
        
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=None)
        mock_repository.get_by_email = Mock(return_value=None)
        mock_repository.get_by_phone = Mock(return_value=None)
        mock_repository.create = Mock(return_value=mock_customer)
        
        service = CustomerService(mock_repository)
        
        customer_data = CustomerCreate(
            document_number="CC-12345678",
            full_name="Juan Pérez González",
            email="juan.perez@email.com",
            phone_number="3001234567",
            address="Calle 123 #45-67, Bogotá"
        )
        
        # Act
        result = service.create(customer_data.model_dump())
        
        # Assert
        assert result is not None
        mock_repository.get_by_document.assert_called_once_with("CC-12345678")
        mock_repository.get_by_email.assert_called_once_with("juan.perez@email.com")
        mock_repository.get_by_phone.assert_called_once_with("3001234567")
        mock_repository.create.assert_called_once()

    def test_create_customer_already_exists(self):
        """Prueba crear cliente cuando ya existe"""
        # Arrange
        mock_repository = Mock(spec=CustomerRepository)
        mock_repository.get_by_document = Mock(return_value=Mock())
        mock_repository.get_by_email = Mock(return_value=None)
        mock_repository.get_by_phone = Mock(return_value=None)
        mock_repository.create = Mock()
        
        service = CustomerService(mock_repository)
        
        customer_data = CustomerCreate(
            document_number="CC-12345678",
            full_name="Juan Pérez González",
            email="juan.perez@email.com",
            phone_number="3001234567",
            address="Calle 123 #45-67, Bogotá"
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Ya existe un cliente con documento 'CC-12345678'"):
            service.create(customer_data.model_dump())
        
        mock_repository.get_by_document.assert_called_once_with("CC-12345678")
        mock_repository.create.assert_not_called()

    def test_create_customer_email_already_exists(self):
        """Prueba crear cliente cuando email ya existe"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=None)
        mock_repository.get_by_email = Mock(return_value=Mock())
        mock_repository.get_by_phone = Mock(return_value=None)
        mock_repository.create = Mock()
        
        service = CustomerService(mock_repository)
        
        customer_data = CustomerCreate(
            document_number="CC-12345678",
            full_name="Juan Pérez González",
            email="juan.perez@email.com",
            phone_number="3001234567",
            address="Calle 123 #45-67, Bogotá"
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Ya existe un cliente con email 'juan.perez@email.com'"):
            service.create(customer_data.model_dump())
        
        mock_repository.get_by_document.assert_called_once_with("CC-12345678")
        mock_repository.get_by_email.assert_called_once_with("juan.perez@email.com")
        mock_repository.create.assert_not_called()

    def test_create_customer_phone_already_exists(self):
        """Prueba crear cliente cuando teléfono ya existe"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=None)
        mock_repository.get_by_email = Mock(return_value=None)
        mock_repository.get_by_phone = Mock(return_value=Mock())
        mock_repository.create = Mock()
        
        service = CustomerService(mock_repository)
        
        customer_data = CustomerCreate(
            document_number="CC-12345678",
            full_name="Juan Pérez González",
            email="juan.perez@email.com",
            phone_number="3001234567",
            address="Calle 123 #45-67, Bogotá"
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Ya existe un cliente con teléfono '3001234567'"):
            service.create(customer_data.model_dump())
        
        mock_repository.get_by_document.assert_called_once_with("CC-12345678")
        mock_repository.get_by_phone.assert_called_once_with("3001234567")
        mock_repository.create.assert_not_called()

    def test_create_customer_invalid_data(self):
        """Prueba crear cliente con datos válidos (Pydantic maneja la validación)"""
        # Arrange
        mock_customer = Mock()
        mock_customer.id = 1
        
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=None)
        mock_repository.get_by_email = Mock(return_value=None)
        mock_repository.get_by_phone = Mock(return_value=None)
        mock_repository.create = Mock(return_value=mock_customer)
        
        service = CustomerService(mock_repository)
        
        # Datos válidos que pasan la validación de Pydantic
        customer_data = CustomerCreate(
            document_number="CC-12345678",
            full_name="Juan Pérez González",
            email="juan.perez@email.com",
            phone_number="3001234567",
            address="Calle 123 #45-67, Bogotá"
        )
        
        # Act
        result = service.create(customer_data.model_dump())
        
        # Assert
        assert result is not None
        mock_repository.create.assert_called_once()

    def test_get_customer_success(self):
        """Prueba obtener cliente existente"""
        # Arrange
        mock_customer = Mock()
        mock_customer.document_number = "CC-12345678"
        mock_customer.full_name = "Juan Pérez González"
        mock_customer.email = "juan.perez@email.com"
        mock_customer.phone_number = "3001234567"
        mock_customer.address = "Calle 123 #45-67, Bogotá"
        
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=mock_customer)
        
        service = CustomerService(mock_repository)
        
        # Act
        result = service.get_customer("CC-12345678")
        
        # Assert
        assert result == mock_customer
        mock_repository.get_by_document.assert_called_once_with("CC-12345678")

    def test_get_customer_not_found(self):
        """Prueba obtener cliente no existente"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=None)
        
        service = CustomerService(mock_repository)
        
        # Act
        result = service.get_customer("CC-99999999")
        
        # Assert
        assert result is None
        mock_repository.get_by_document.assert_called_once_with("CC-99999999")

    def test_get_customer_invalid_document(self):
        """Prueba obtener cliente con documento inválido"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=None)
        
        service = CustomerService(mock_repository)
        
        # Act & Assert - El servicio no valida formato, solo busca
        # La validación de formato está en el controller
        result = service.get_customer("INVALID")
        
        # Assert
        assert result is None
        mock_repository.get_by_document.assert_called_once_with("INVALID")

    def test_update_customer_success(self):
        """Prueba actualizar cliente existente"""
        # Arrange
        mock_customer = Mock()
        mock_customer.document_number = "CC-12345678"
        mock_customer.full_name = "Juan Pérez González"
        mock_customer.email = "juan.perez@email.com"
        mock_customer.phone_number = "3001234567"
        mock_customer.address = "Calle 123 #45-67, Bogotá"
        
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=mock_customer)
        mock_repository.get_by_email = Mock(return_value=None)  # Email nuevo no existe
        mock_repository.get_by_phone = Mock(return_value=None)  # Teléfono nuevo no existe
        mock_repository.db = Mock()
        mock_repository.db.commit = Mock()
        mock_repository.db.refresh = Mock()
        
        service = CustomerService(mock_repository)
        
        update_data = CustomerUpdate(
            full_name="Juan Pérez Actualizado",
            email="juan.actualizado@email.com",
            phone_number="3007654321",
            address="Calle 456 #78-90, Bogotá"
        )
        
        # Act
        result = service.update_customer("CC-12345678", update_data)
        
        # Assert
        assert result == mock_customer
        mock_repository.db.commit.assert_called_once()
        mock_repository.db.refresh.assert_called_once_with(mock_customer)

    def test_update_customer_not_found(self):
        """Prueba actualizar cliente no existente"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=None)
        
        service = CustomerService(mock_repository)
        
        update_data = CustomerUpdate(
            full_name="Juan Pérez Actualizado"
        )
        
        # Act
        result = service.update_customer("CC-99999999", update_data)
        
        # Assert
        assert result is None
        mock_repository.get_by_document.assert_called_once_with("CC-99999999")

    def test_update_customer_email_conflict(self):
        """Prueba actualizar cliente con email existente"""
        # Arrange
        mock_customer = Mock()
        mock_customer.document_number = "CC-12345678"
        mock_customer.email = "juan.perez@email.com"
        
        existing_customer = Mock()
        existing_customer.document_number = "CC-87654321"
        
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=mock_customer)
        mock_repository.get_by_email = Mock(return_value=existing_customer)
        
        service = CustomerService(mock_repository)
        
        update_data = CustomerUpdate(
            email="maria.lopez@email.com"  # Email diferente pero ya existe
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Ya existe un cliente con email 'maria.lopez@email.com'"):
            service.update_customer("CC-12345678", update_data)

    def test_update_customer_phone_conflict(self):
        """Prueba actualizar cliente con teléfono existente"""
        # Arrange
        mock_customer = Mock()
        mock_customer.document_number = "CC-12345678"
        mock_customer.phone_number = "3001234567"
        
        existing_customer = Mock()
        existing_customer.document_number = "CC-87654321"
        
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=mock_customer)
        mock_repository.get_by_phone = Mock(return_value=existing_customer)
        
        service = CustomerService(mock_repository)
        
        update_data = CustomerUpdate(
            phone_number="3009876543"  # Teléfono diferente pero ya existe
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Ya existe un cliente con teléfono '3009876543'"):
            service.update_customer("CC-12345678", update_data)

    def test_delete_customer_success(self):
        """Prueba eliminar cliente existente"""
        # Arrange
        mock_customer = Mock()
        
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=mock_customer)
        mock_repository.delete = Mock(return_value=True)
        
        service = CustomerService(mock_repository)
        
        # Act
        result = service.delete("CC-12345678")
        
        # Assert
        assert result is True
        mock_repository.get_by_document.assert_called_once_with("CC-12345678")
        mock_repository.delete.assert_called_once_with("CC-12345678")

    def test_delete_customer_not_found(self):
        """Prueba eliminar cliente no existente"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=None)
        
        service = CustomerService(mock_repository)
        
        # Act
        result = service.delete("CC-99999999")
        
        # Assert
        assert result is False
        mock_repository.get_by_document.assert_called_once_with("CC-99999999")

    def test_delete_customer_invalid_document(self):
        """Prueba eliminar cliente con documento inválido"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_document = Mock(return_value=None)
        
        service = CustomerService(mock_repository)
        
        # Act & Assert - El servicio no valida formato, solo busca
        # La validación de formato está en el controller
        result = service.delete("INVALID")
        
        # Assert
        assert result is False
        mock_repository.get_by_document.assert_called_once_with("INVALID")
