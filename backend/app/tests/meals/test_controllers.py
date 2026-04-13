# tests/test_meals/test_controllers.py - Pruebas de controladores de combos según contrato
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app.meals.model import Meal, CategoryEnum
from app.meals.schema import MealCreate, MealResponse

@pytest.mark.unit
@pytest.mark.meal
class TestMealController:
    def test_create_meal_success(self, client, sample_meal_data):
        """Prueba crear combo exitosamente - Contrato: 201 CREATED"""
        # Arrange
        mock_meal = {
            "id": 1,
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "name": "COMBO HAMBURGUESA CLÁSICA",
            "description": "Combo de hamburguesa con papas",
            "price_without_iva": "15000.00",
            "category": "HAMBURGERS_AND_HOTDOGS",
            "is_available": True,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
        
        with patch('app.meals.controller.MealService') as mock_service_class:
            mock_service = Mock()
            mock_service.create.return_value = mock_meal
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/meals/", json=sample_meal_data)
            
            # Assert
            assert response.status_code == 201
            data = response.json()
            assert "uuid" in data
            assert data["name"] == sample_meal_data["name"].upper()  # Guardado en mayúsculas
            assert data["price_without_iva"] == "15000.00"  # Formato que retorna el servicio

    def test_create_meal_conflict(self, client, sample_meal_data):
        """Prueba crear combo con nombre duplicado - Contrato: 409 CONFLICT"""
        # Arrange
        with patch('app.meals.controller.MealService') as mock_service_class:
            mock_service = Mock()
            mock_service.create.side_effect = ValueError("Ya existe un combo con ese nombre")
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.post("/meals/", json=sample_meal_data)
            
            # Assert
            assert response.status_code == 409
            data = response.json()
            assert "detail" in data
            assert "Ya existe un combo con ese nombre" in data["detail"]

    def test_create_meal_invalid_data(self, client):
        """Prueba crear combo con datos inválidos - Contrato: 422 UNPROCESSABLE ENTITY"""
        # Arrange
        invalid_data = {
            "name": "",  # Vacío
            "description": "Combo inválido",
            "price_without_iva": -10,  # Negativo
            "category": "INVALID_CATEGORY"
        }
        
        # Act
        response = client.post("/meals/", json=invalid_data)
        
        # Assert
        assert response.status_code == 422

    def test_get_meal_success(self, client):
        """Prueba obtener combo existente - Contrato: 200 OK"""
        # Arrange
        mock_meal = {
            "id": 1,
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "name": "COMBO HAMBURGUESA CLÁSICA",
            "description": "Combo de hamburguesa con papas",
            "price_without_iva": "15000.00",
            "category": "HAMBURGERS_AND_HOTDOGS",
            "is_available": True,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
        
        with patch('app.meals.controller.MealService') as mock_service_class:
            mock_service = Mock()
            mock_service.get_by_uuid.return_value = mock_meal
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.get("/meals/123e4567-e89b-12d3-a456-426614174000")
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["uuid"] == "123e4567-e89b-12d3-a456-426614174000"
            assert data["name"] == "COMBO HAMBURGUESA CLÁSICA"

    def test_get_meal_not_found(self, client):
        """Prueba obtener combo no existente - Contrato: 404 NOT FOUND"""
        # Arrange
        with patch('app.meals.controller.MealService') as mock_service_class:
            mock_service = Mock()
            mock_service.get_by_uuid.return_value = None
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.get("/meals/123e4567-e89b-12d3-a456-426614174999")
            
            # Assert
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert "no encontrado" in data["detail"].lower()

    def test_get_meal_invalid_uuid(self, client):
        """Prueba obtener combo con UUID inválido - Contrato: 404 NOT FOUND"""
        # Arrange
        with patch('app.meals.controller.MealService') as mock_service_class:
            mock_service = Mock()
            mock_service.get_by_uuid.return_value = None  # Simular que no se encontró
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.get("/meals/invalid-uuid")
            
            # Assert
            assert response.status_code == 404  # El servicio retorna None -> 404

    def test_update_meal_success(self, client, sample_meal_data):
        """Prueba actualizar combo existente - Contrato: 200 OK"""
        # Arrange
        mock_updated_meal = {
            "id": 1,
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "name": "COMBO ACTUALIZADO",
            "description": "Combo actualizado",
            "price_without_iva": "18000.00",
            "category": "HAMBURGERS_AND_HOTDOGS",
            "is_available": True,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T11:30:00Z"
        }
        
        with patch('app.meals.controller.MealService') as mock_service_class:
            mock_service = Mock()
            mock_service.update.return_value = mock_updated_meal
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.put("/meals/123e4567-e89b-12d3-a456-426614174000", json=sample_meal_data)
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["uuid"] == "123e4567-e89b-12d3-a456-426614174000"
            assert data["name"] == "COMBO ACTUALIZADO"

    def test_update_meal_not_found(self, client, sample_meal_data):
        """Prueba actualizar combo no existente - Contrato: 404 NOT FOUND"""
        # Arrange
        with patch('app.meals.controller.MealService') as mock_service_class:
            mock_service = Mock()
            mock_service.update.return_value = None
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.put("/meals/123e4567-e89b-12d3-a456-426614174999", json=sample_meal_data)
            
            # Assert
            assert response.status_code == 404

    def test_update_meal_no_changes(self, client):
        """Prueba actualizar combo sin cambios - Contrato: 404 NOT FOUND"""
        # Arrange
        with patch('app.meals.controller.MealService') as mock_service_class:
            mock_service = Mock()
            mock_service.update.return_value = None  # Simular que no se encontró
            mock_service_class.return_value = mock_service
            
            no_changes_data = {}
            
            # Act
            response = client.put("/meals/123e4567-e89b-12d3-a456-426614174000", json=no_changes_data)
            
            # Assert
            assert response.status_code == 404  # El servicio retorna None -> 404

    def test_update_meal_name_conflict(self, client, sample_meal_data):
        """Prueba actualizar combo con nombre duplicado - Contrato: 409 CONFLICT"""
        # Arrange
        with patch('app.meals.controller.MealService') as mock_service_class:
            mock_service = Mock()
            mock_service.update.side_effect = ValueError("Ya existe un combo con ese nombre")
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.put("/meals/123e4567-e89b-12d3-a456-426614174000", json=sample_meal_data)
            
            # Assert
            assert response.status_code == 409

    def test_delete_meal_success(self, client):
        """Prueba eliminar combo existente - Contrato: 204 NO CONTENT"""
        # Arrange
        with patch('app.meals.controller.MealService') as mock_service_class:
            mock_service = Mock()
            mock_service.delete.return_value = True
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.delete("/meals/123e4567-e89b-12d3-a456-426614174000")
            
            # Assert
            assert response.status_code == 204

    def test_delete_meal_not_found(self, client):
        """Prueba eliminar combo no existente - Contrato: 404 NOT FOUND"""
        # Arrange
        with patch('app.meals.controller.MealService') as mock_service_class:
            mock_service = Mock()
            mock_service.delete.return_value = False
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.delete("/meals/123e4567-e89b-12d3-a456-426614174999")
            
            # Assert
            assert response.status_code == 404

    def test_delete_meal_invalid_uuid(self, client):
        """Prueba eliminar combo con UUID inválido - Contrato: 404 NOT FOUND"""
        # Arrange
        with patch('app.meals.controller.MealService') as mock_service_class:
            mock_service = Mock()
            mock_service.delete.return_value = False  # Simular que no se eliminó
            mock_service_class.return_value = mock_service
            
            # Act
            response = client.delete("/meals/invalid-uuid")
            
            # Assert
            assert response.status_code == 404  # El servicio retorna False -> 404
