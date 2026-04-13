# tests/test_customers/test_controllers.py - Pruebas de controladores de clientes según contrato
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app.customers.model import Customer
from app.customers.schema import CustomerCreate, CustomerResponse
from app.tests.factories import CustomerFactory

@pytest.mark.unit
@pytest.mark.customer
class TestCustomerController:
    def test_create_customer_success(self, client):
        """Prueba crear cliente exitosamente - Contrato: 201 CREATED"""
        # Arrange
        customer_data = {
            "document_number": "CC-12345678",
            "full_name": "Juan Pérez",
            "email": "juan.perez@example.com",
            "phone_number": "3001234567",
            "address": "Calle 123 #45-67, Bogotá"
        }
        
        # Mock simple del customer con todos los atributos necesarios
        mock_customer = Mock()
        mock_customer.id = 1
        mock_customer.document_number = customer_data["document_number"]
        mock_customer.full_name = customer_data["full_name"]
        mock_customer.email = customer_data["email"]
        mock_customer.phone_number = customer_data["phone_number"]
        mock_customer.address = customer_data["address"]
        mock_customer.created_at = "2024-01-15T10:30:00Z"
        mock_customer.updated_at = "2024-01-15T10:30:00Z"
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.create.return_value = mock_customer
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/customers/", json=customer_data)
            
            # Assert
            assert response.status_code == 201
            data = response.json()
            assert data["document_number"] == customer_data["document_number"]
            mock_service.create.assert_called_once()
    
    def test_create_customer_already_exists(self, client):
        """Prueba crear cliente con documento existente - Contrato: 409 CONFLICT"""
        # Arrange
        customer_data = {
            "document_number": "CC-12345678",
            "full_name": "Juan Pérez",
            "email": "juan.perez@example.com",
            "phone_number": "3001234567",
            "address": "Calle 123 #45-67, Bogotá"
        }
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.create.side_effect = ValueError("Ya existe un cliente con documento 'CC-12345678'")
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/customers/", json=customer_data)
            
            # Assert
            assert response.status_code == 409
            assert "Ya existe un cliente con documento" in response.json()["detail"]
            assert "Ya existe un cliente" in response.json()["detail"]

    def test_create_customer_email_already_exists(self, client):
        """Prueba crear cliente con email existente - Contrato: 409 CONFLICT"""
        # Arrange
        customer_data = {
            "document_number": "CC-87654321",
            "full_name": "María López",
            "email": "juan.perez@example.com",  # Email existente
            "phone_number": "3009876543",
            "address": "Calle 456 #78-90, Bogotá"
        }
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.create.side_effect = ValueError("Ya existe un cliente con email 'juan.perez@example.com'")
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/customers/", json=customer_data)
            
            # Assert
            assert response.status_code == 409
            assert "Ya existe un cliente con email" in response.json()["detail"]
    
    def test_create_customer_phone_already_exists(self, client):
        """Prueba crear cliente con teléfono existente - Contrato: 409 CONFLICT"""
        # Arrange
        customer_data = {
            "document_number": "CC-11223344",
            "full_name": "Carlos Martínez",
            "email": "carlos.martinez@example.com",
            "phone_number": "3001234567",  # Teléfono existente
            "address": "Carrera 15 #32-10, Bogotá"
        }
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.create.side_effect = ValueError("Ya existe un cliente con teléfono '3001234567'")
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/customers/", json=customer_data)
            
            # Assert
            assert response.status_code == 409
            assert "Ya existe un cliente con teléfono" in response.json()["detail"]
            assert "Ya existe un cliente" in response.json()["detail"]

    def test_create_customer_invalid_data(self, client):
        """Prueba crear cliente con datos inválidos - Contrato: 422 UNPROCESSABLE ENTITY"""
        # Arrange
        invalid_data = {
            "document_number": "INVALID",  # Formato inválido según validador
            "full_name": "",  # Nombre vacío (violación de min_length=1)
            "email": "invalid-email",  # Email inválido según validador
            "phone_number": "123",  # Teléfono muy corto (violación de min_length=7)
            "address": ""
        }
        
        # Act
        response = client.post("/customers/", json=invalid_data)
        
        # Assert
        assert response.status_code == 422
    
    def test_get_customer_success(self, client):
        """Prueba consultar cliente existente - Contrato: 200 OK"""
        # Arrange
        document = "CC-12345678"
        
        # Mock simple del customer con todos los atributos necesarios
        mock_customer = Mock()
        mock_customer.id = 1
        mock_customer.document_number = document
        mock_customer.full_name = "Juan Pérez"
        mock_customer.email = "juan.perez@example.com"
        mock_customer.phone_number = "3001234567"
        mock_customer.address = "Calle 123 #45-67, Bogotá"
        mock_customer.created_at = "2024-01-15T10:30:00Z"
        mock_customer.updated_at = "2024-01-15T10:30:00Z"
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.get_customer.return_value = mock_customer
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.get(f"/customers/{document}")
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["document_number"] == document
            mock_service.get_customer.assert_called_once_with(document)
    
    def test_get_customer_not_found(self, client):
        """Prueba consultar cliente no existente - Contrato: 404 NOT FOUND"""
        # Arrange
        document = "CC-12345678"
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.get_customer.return_value = None
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.get(f"/customers/{document}")
            
            # Assert
            assert response.status_code == 404
            assert "Cliente no encontrado" in response.json()["detail"]
    
    def test_get_customer_invalid_document(self, client):
        """Prueba consultar cliente con documento inválido - Contrato: 400 BAD REQUEST"""
        # Arrange
        invalid_document = "123"  # Formato inválido
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.get_customer.side_effect = ValueError("Formato de documento inválido")
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.get(f"/customers/{invalid_document}")
            
            # Assert
            assert response.status_code == 400
            assert "Formato de documento inválido" in response.json()["detail"]
    
    def test_update_customer_success(self, client):
        """Prueba actualizar cliente existente - Contrato: 204 NO CONTENT"""
        # Arrange
        document = "CC-12345678"
        update_data = {
            "full_name": "Juan Pérez Actualizado",
            "email": "juan.actualizado@example.com",
            "phone_number": "3007654321",
            "address": "Calle 456 #78-90, Bogotá"
        }
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.update_customer.return_value = Mock()  # Mock simple
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.put(f"/customers/{document}", json=update_data)
            
            # Assert
            assert response.status_code == 204
            assert response.content == b""  # Sin cuerpo de respuesta
            mock_service.update_customer.assert_called_once()
    
    def test_update_customer_not_found(self, client):
        """Prueba actualizar cliente no existente - Contrato: 404 NOT FOUND"""
        # Arrange
        document = "CC-12345678"
        update_data = {
            "name": "Juan Pérez Actualizado",
            "email": "juan.actualizado@example.com",
            "phone": "3007654321",
            "address": "Calle 456 #78-90, Bogotá"
        }
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.update_customer.return_value = None
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.put(f"/customers/{document}", json=update_data)
            
            # Assert
            assert response.status_code == 404
            assert "Cliente no encontrado" in response.json()["detail"]
    
    def test_update_customer_email_conflict(self, client):
        """Prueba actualizar cliente con datos en conflicto - Contrato: 409 CONFLICT"""
        # Arrange
        document = "CC-12345678"
        update_data = {
            "name": "Juan Pérez Actualizado",
            "email": "juan.actualizado@example.com",
            "phone": "3007654321",
            "address": "Calle 456 #78-90, Bogotá"
        }
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.update_customer.side_effect = ValueError("Ya existe un cliente con email 'juan.actualizado@example.com'")
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.put(f"/customers/{document}", json=update_data)
            
            # Assert
            assert response.status_code == 409
            assert "Ya existe un cliente" in response.json()["detail"]
    
    def test_update_customer_phone_conflict(self, client):
        """Prueba actualizar cliente con teléfono en conflicto - Contrato: 409 CONFLICT"""
        # Arrange
        document = "CC-12345678"
        update_data = {
            "phone": "3009999999"  # Teléfono de otro cliente
        }
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.update_customer.side_effect = ValueError("Ya existe un cliente con teléfono '3009999999'")
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.put(f"/customers/{document}", json=update_data)
            
            # Assert
            assert response.status_code == 409
            assert "Ya existe un cliente" in response.json()["detail"]

    def test_delete_customer_success(self, client):
        """Prueba eliminar cliente existente - Contrato: 204 NO CONTENT"""
        # Arrange
        document = "CC-12345678"
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.delete.return_value = True
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.delete(f"/customers/{document}")
            
            # Assert
            assert response.status_code == 204
            assert response.content == b""  # Sin cuerpo de respuesta
            mock_service.delete.assert_called_once_with(document)
    
    def test_delete_customer_not_found(self, client):
        """Prueba eliminar cliente no existente - Contrato: 404 NOT FOUND"""
        # Arrange
        document = "CC-12345678"
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.delete.return_value = False
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.delete(f"/customers/{document}")
            
            # Assert
            assert response.status_code == 404
            assert "Cliente no encontrado" in response.json()["detail"]
    
    def test_delete_customer_invalid_document(self, client):
        """Prueba eliminar cliente con documento inválido - Contrato: 400 BAD REQUEST"""
        # Arrange
        invalid_document = "123"  # Formato inválido
        
        with patch('app.customers.controller.CustomerService') as mock_service_class:
            mock_service = Mock()
            mock_service.delete.side_effect = ValueError("Formato de documento inválido")
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.delete(f"/customers/{invalid_document}")
            
            # Assert
            assert response.status_code == 400
            assert "Formato de documento inválido" in response.json()["detail"]