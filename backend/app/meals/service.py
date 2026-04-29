# meals/service.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.meals.repository import MealRepository
from app.meals.model import Meal, CategoryEnum
from app.meals.schema import MealCreate, MealUpdate

class MealService:
    def __init__(self, repository: MealRepository):
        self.repository = repository

    def create(self, meal_data: MealCreate) -> Meal:
        """Crear combo con validaciones"""
        # Verificar que no exista un combo con el mismo nombre
        existing_meal = self.repository.get_by_name(meal_data.name)
        if existing_meal:
            raise ValueError(f"Ya existe un combo con ese nombre")
        
        return self.repository.create(meal_data.model_dump())

    def get_by_uuid(self, uuid: str) -> Optional[Meal]:
        """Obtener combo por UUID"""
        return self.repository.get_by_uuid(uuid)
    
    def update(self, uuid: str, meal_data: MealUpdate) -> Optional[Meal]:
        """Actualizar combo por UUID"""
        # Obtener combo existente
        meal = self.get_by_uuid(uuid)
        if not meal:
            return None
        
        # Si se actualiza el nombre, verificar que no exista otro combo con ese nombre
        if meal_data.name and meal_data.name != meal.name:
            existing_meal = self.repository.get_by_name(meal_data.name)
            if existing_meal and existing_meal.uuid != uuid:
                raise ValueError(f"Ya existe un combo con ese nombre")
        
        # Aplicar actualizaciones
        update_dict = meal_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            if value is not None:
                setattr(meal, key, value)
        
        self.repository.db.commit()
        self.repository.db.refresh(meal)
        return meal
    
    def delete(self, uuid: str) -> bool:
        """Eliminar combo por UUID"""
        return self.repository.delete_by_uuid(uuid)
