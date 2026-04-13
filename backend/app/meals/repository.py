# meals/repository.py
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.meals.model import Meal, CategoryEnum

class MealRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: dict) -> Meal:
        obj = Meal(**obj_in)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, id: int) -> Optional[Meal]:
        return self.db.query(Meal).filter(Meal.id == id).first()

    def get_by_uuid(self, uuid: str) -> Optional[Meal]:
        """Obtener combo por UUID"""
        return self.db.query(Meal).filter(Meal.uuid == uuid).first()
    
    def get_by_name(self, name: str) -> Optional[Meal]:
        """Obtener combo por nombre"""
        return self.db.query(Meal).filter(Meal.name == name).first()
    
    def update(self, uuid: str, obj_in: dict) -> Optional[Meal]:
        """Actualizar combo por UUID"""
        obj = self.db.query(Meal).filter(Meal.uuid == uuid).first()
        if obj:
            for key, value in obj_in.items():
                setattr(obj, key, value)
            self.db.commit()
            self.db.refresh(obj)
        return obj
    
    def delete_by_uuid(self, uuid: str) -> bool:
        """Eliminar combo por UUID"""
        meal = self.get_by_uuid(uuid)
        if not meal:
            return False
        self.db.delete(meal)
        self.db.commit()
        return True