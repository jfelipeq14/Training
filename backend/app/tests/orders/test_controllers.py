# tests/test_orders/test_controllers.py - Pruebas de controladores de pedidos según contrato
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime

from app.orders.model import Order
from app.orders.schema import OrderCreate, OrderResponse

@pytest.mark.unit
@pytest.mark.order
class TestOrderController:
    def test_create_order_success(self, client, sample_order_data):
        """Prueba crear pedido exitosamente - Contrato: 201 CREATED"""
        # Arrange
        mock_order = {
            "id": 1,
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "order_date": "2024-01-15T10:30:00Z",
            "document": sample_order_data["document"],
            "meal_uuid": sample_order_data["meal_uuid"],
            "quantity": sample_order_data["quantity"],
            "additional_info": sample_order_data["additional_info"],
            "subtotal_without_iva": "30000.00",
            "iva_amount": "5700.00",
            "total_with_iva": "35700.00",
            "is_delivered": False,
            "delivery_date": None,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": None
        }
        
        with patch('app.orders.controller.OrderService') as mock_service_class:
            mock_service = Mock()
            mock_service.create_order.return_value = mock_order
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/orders/", json=sample_order_data)
            
            # Assert
            assert response.status_code == 201
            data = response.json()
            assert "uuid" in data
            assert "order_date" in data  # Fecha de creación del servidor
            assert data["is_delivered"] == False  # Por defecto no entregado
            assert data["delivery_date"] is None  # Por defecto NULL
            assert "subtotal_without_iva" in data  # Campo calculado
            assert "iva_amount" in data  # Campo calculado
            assert "total_with_iva" in data  # Campo calculado
            mock_service.create_order.assert_called_once()

    def test_create_order_customer_not_found(self, client, sample_order_data):
        """Prueba crear pedido con cliente no existente - Contrato: 404 NOT FOUND"""
        # Arrange
        with patch('app.orders.controller.OrderService') as mock_service_class:
            mock_service = Mock()
            mock_service.create_order.side_effect = ValueError("Cliente con documento 'CC-99999999' no encontrado")
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/orders/", json=sample_order_data)
            
            # Assert
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert "Cliente con documento" in data["detail"]

    def test_create_order_meal_not_found(self, client, sample_order_data):
        """Prueba crear pedido con combo no existente - Contrato: 404 NOT FOUND"""
        # Arrange
        with patch('app.orders.controller.OrderService') as mock_service_class:
            mock_service = Mock()
            mock_service.create_order.side_effect = ValueError("Combo con UUID '99999999-9999-9999-9999-999999999999' no encontrado")
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/orders/", json=sample_order_data)
            
            # Assert
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert "Combo con UUID" in data["detail"]

    def test_create_order_invalid_data(self, client):
        """Prueba crear pedido con datos inválidos - Contrato: 422 UNPROCESSABLE ENTITY"""
        # Arrange
        invalid_data = {
            "document": "",  # Vacío
            "meal_uuid": "invalid-uuid",  # Formato inválido
            "quantity": 0,  # Inválido (debe ser >= 1)
            "additional_info": "X" * 512  # Demasiado largo
        }
        
        # Act
        response = client.post("/orders/", json=invalid_data)
        
        # Assert
        assert response.status_code == 422

    def test_update_order_success(self, client):
        """Prueba actualizar pedido existente - Contrato: 200 OK"""
        # Arrange
        mock_updated_order = {
            "id": 1,
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "order_date": "2024-01-15T10:30:00Z",
            "document": "CC-12345678",
            "meal_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "quantity": 2,
            "additional_info": "Test",
            "subtotal_without_iva": "30000.00",
            "iva_amount": "5700.00",
            "total_with_iva": "35700.00",
            "is_delivered": True,
            "delivery_date": "2024-01-15T11:30:00Z",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T11:30:00Z"
        }
        
        update_data = {
            "timestamp": "2024-01-15T11:30:00Z"
        }
        
        with patch('app.orders.controller.OrderService') as mock_service_class:
            mock_service = Mock()
            mock_service.update_order.return_value = mock_updated_order
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.put("/orders/123e4567-e89b-12d3-a456-426614174000", json=update_data)
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["is_delivered"] == True
            assert data["delivery_date"] == "2024-01-15T11:30:00Z"

    def test_update_order_not_found(self, client):
        """Prueba actualizar pedido no existente - Contrato: 404 NOT FOUND"""
        # Arrange
        update_data = {
            "timestamp": "2024-01-15T11:30:00Z"
        }
        
        with patch('app.orders.controller.OrderService') as mock_service_class:
            mock_service = Mock()
            mock_service.update_order.return_value = None
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.put("/orders/99999999-9999-9999-9999-999999999999", json=update_data)
            
            # Assert
            assert response.status_code == 404

    def test_update_order_invalid_uuid(self, client):
        """Prueba actualizar pedido con UUID inválido - Contrato: 404 NOT FOUND"""
        # Arrange
        with patch('app.orders.controller.OrderService') as mock_service_class:
            mock_service = Mock()
            mock_service.update_order.return_value = None  # Simular que no se encontró
            mock_service_class.return_value = mock_service
            
            update_data = {
                "timestamp": "2024-01-15T11:30:00Z"
            }
            
            # Act
            response = client.put("/orders/invalid-uuid", json=update_data)
            
            # Assert
            assert response.status_code == 404  # El servicio retorna None -> 404

    def test_update_order_invalid_timestamp(self, client):
        """Prueba actualizar pedido con timestamp inválido - Contrato: 422 UNPROCESSABLE ENTITY"""
        # Arrange
        update_data = {
            "timestamp": "invalid-timestamp"
        }
        
        # Act
        response = client.put("/orders/123e4567-e89b-12d3-a456-426614174000", json=update_data)
        
        # Assert
        assert response.status_code == 422
