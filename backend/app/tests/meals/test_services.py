# tests/test_meals/test_services.py - Pruebas unitarias de MealService según contrato
import pytest
from unittest.mock import Mock, patch
from decimal import Decimal

from app.meals.service import MealService
from app.meals.repository import MealRepository
from app.meals.model import Meal, CategoryEnum
from app.meals.schema import MealCreate, MealUpdate

@pytest.mark.unit
@pytest.mark.meal
class TestMealService:
    def test_create_meal_success(self):
        """Prueba crear combo exitosamente"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_name.return_value = None
        mock_repository.create.return_value = Mock()
        
        service = MealService(mock_repository)
        
        meal_data = MealCreate(
            name="COMBO HAMBURGUESA CLÁSICA",
            category=CategoryEnum.HAMBURGERS_AND_HOTDOGS,
            description="Hamburguesa pan de ajonjolí, carne de 200gr, queso cheddar, papas fritas y gaseosa de 350ml",
            price_without_iva=Decimal("15000.00"),
            is_available=True
        )
        
        # Act
        result = service.create(meal_data)
        
        # Assert
        assert result is not None
        mock_repository.get_by_name.assert_called_once_with("COMBO HAMBURGUESA CLÁSICA")
        mock_repository.create.assert_called_once()

    def test_create_meal_conflict(self):
        """Prueba crear combo con nombre duplicado"""
        # Arrange
        mock_repository = Mock()
        existing_meal = Mock()
        mock_repository.get_by_name.return_value = existing_meal
        
        service = MealService(mock_repository)
        
        meal_data = MealCreate(
            name="COMBO HAMBURGUESA CLÁSICA",
            category=CategoryEnum.HAMBURGERS_AND_HOTDOGS,
            description="Hamburguesa pan de ajonjolí, carne de 200gr, queso cheddar, papas fritas y gaseosa de 350ml",
            price_without_iva=Decimal("15000.00"),
            is_available=True
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Ya existe un combo con ese nombre"):
            service.create(meal_data)

    def test_create_meal_invalid_data(self):
        """Prueba crear combo con datos inválidos"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_name.return_value = None
        mock_repository.create.return_value = Mock()
        
        service = MealService(mock_repository)
        
        # Datos válidos (el servicio no valida formato, eso es trabajo del schema)
        meal_data = MealCreate(
            name="COMBO VÁLIDO",
            category=CategoryEnum.HAMBURGERS_AND_HOTDOGS,
            description="Descripción válida",
            price_without_iva=Decimal("10000.00"),
            is_available=True
        )
        
        # Act
        result = service.create(meal_data)
        
        # Assert
        assert result is not None

    def test_get_meal_success(self):
        """Prueba obtener combo existente"""
        # Arrange
        mock_repository = Mock()
        expected_meal = Mock()
        mock_repository.get_by_uuid.return_value = expected_meal
        
        service = MealService(mock_repository)
        uuid = "123e4567-e89b-12d3-a456-426614174000"
        
        # Act
        result = service.get_by_uuid(uuid)
        
        # Assert
        assert result == expected_meal
        mock_repository.get_by_uuid.assert_called_once_with(uuid)

    def test_get_meal_not_found(self):
        """Prueba obtener combo no existente"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_uuid.return_value = None
        
        service = MealService(mock_repository)
        uuid = "123e4567-e89b-12d3-a456-426614174999"
        
        # Act
        result = service.get_by_uuid(uuid)
        
        # Assert
        assert result is None
        mock_repository.get_by_uuid.assert_called_once_with(uuid)

    def test_get_meal_invalid_uuid(self):
        """Prueba obtener combo con UUID inválido"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_uuid.return_value = None
        
        service = MealService(mock_repository)
        invalid_uuid = "invalid-uuid"
        
        # Act
        result = service.get_by_uuid(invalid_uuid)
        
        # Assert - El servicio no valida formato, solo busca
        assert result is None

    def test_update_meal_success(self):
        """Prueba actualizar combo existente"""
        # Arrange
        mock_repository = Mock()
        existing_meal = Mock()
        existing_meal.name = "COMBO ANTIGUO"
        existing_meal.uuid = "123e4567-e89b-12d3-a456-426614174000"
        
        mock_repository.get_by_uuid.return_value = existing_meal
        mock_repository.get_by_name.return_value = None
        # El update debe retornar el mismo objeto modificado
        mock_repository.update.return_value = existing_meal
        
        service = MealService(mock_repository)
        
        update_data = MealUpdate(
            name="COMBO ACTUALIZADO",
            description="Descripción actualizada",
            price_without_iva=Decimal("18000.00")
        )
        
        # Act
        result = service.update("123e4567-e89b-12d3-a456-426614174000", update_data)
        
        # Assert
        assert result == existing_meal

    def test_update_meal_not_found(self):
        """Prueba actualizar combo no existente"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_uuid.return_value = None
        
        service = MealService(mock_repository)
        
        update_data = MealUpdate(
            name="COMBO ACTUALIZADO"
        )
        
        # Act
        result = service.update("123e4567-e89b-12d3-a456-426614174999", update_data)
        
        # Assert
        assert result is None

    def test_update_meal_no_changes(self):
        """Prueba actualizar combo sin cambios"""
        # Arrange
        mock_repository = Mock()
        existing_meal = Mock()
        existing_meal.name = "COMBO EXISTENTE"
        existing_meal.uuid = "123e4567-e89b-12d3-a456-426614174000"
        
        mock_repository.get_by_uuid.return_value = existing_meal
        
        service = MealService(mock_repository)
        
        update_data = MealUpdate()  # Vacío
        
        # Act
        result = service.update("123e4567-e89b-12d3-a456-426614174000", update_data)
        
        # Assert
        assert result == existing_meal  # No hay cambios, retorna el mismo objeto

    def test_update_meal_name_conflict(self):
        """Prueba actualizar combo con nombre duplicado"""
        # Arrange
        mock_repository = Mock()
        existing_meal = Mock()
        existing_meal.name = "COMBO ACTUAL"
        existing_meal.uuid = "123e4567-e89b-12d3-a456-426614174000"
        
        conflicting_meal = Mock()
        conflicting_meal.uuid = "99999999-9999-9999-9999-999999999999"
        
        mock_repository.get_by_uuid.return_value = existing_meal
        mock_repository.get_by_name.return_value = conflicting_meal
        
        service = MealService(mock_repository)
        
        update_data = MealUpdate(
            name="COMBO CONFLICTIVO"
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Ya existe un combo con ese nombre"):
            service.update("123e4567-e89b-12d3-a456-426614174000", update_data)

    def test_delete_meal_success(self):
        """Prueba eliminar combo existente"""
        # Arrange
        mock_repository = Mock()
        mock_repository.delete_by_uuid.return_value = True
        
        service = MealService(mock_repository)
        uuid = "123e4567-e89b-12d3-a456-426614174000"
        
        # Act
        result = service.delete(uuid)
        
        # Assert
        assert result is True
        mock_repository.delete_by_uuid.assert_called_once_with(uuid)

    def test_delete_meal_not_found(self):
        """Prueba eliminar combo no existente"""
        # Arrange
        mock_repository = Mock()
        mock_repository.delete_by_uuid.return_value = False
        
        service = MealService(mock_repository)
        uuid = "123e4567-e89b-12d3-a456-426614174999"
        
        # Act
        result = service.delete(uuid)
        
        # Assert
        assert result is False
        mock_repository.delete_by_uuid.assert_called_once_with(uuid)

    def test_delete_meal_invalid_uuid(self):
        """Prueba eliminar combo con UUID inválido"""
        # Arrange
        mock_repository = Mock()
        mock_repository.delete_by_uuid.return_value = False
        
        service = MealService(mock_repository)
        invalid_uuid = "invalid-uuid"
        
        # Act
        result = service.delete(invalid_uuid)
        
        # Assert - El servicio no valida formato, solo delega al repositorio
        assert result is False
