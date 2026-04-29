# meals/controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from config.database import get_db
from app.meals.service import MealService
from app.meals.repository import MealRepository
from app.meals.schema import MealCreate, MealUpdate, MealResponse, MealListResponse
from app.handler.meals import handle_create_error, handle_get_error, handle_update_error, handle_delete_error

router = APIRouter(prefix="/meals", tags=["meals"])

def get_meal_service(db: Session = Depends(get_db)) -> MealService:
    repository = MealRepository(db)
    return MealService(repository)

@router.post("/", response_model=MealResponse, status_code=201)
def create_meal(
    meal: MealCreate,
    service: MealService = Depends(get_meal_service)
):
    try:
        return service.create(meal)
    except Exception as exc:
        handle_create_error(exc)

@router.get("/{uuid}", response_model=MealResponse)
def get_meal(
    uuid: str,
    service: MealService = Depends(get_meal_service)
):
    try:
        meal = service.get_by_uuid(uuid)
        if not meal:
            raise HTTPException(status_code=404, detail="Combo no encontrado")
        return meal
    except HTTPException:
        raise
    except Exception as exc:
        handle_get_error(exc)

@router.put("/{uuid}")
def update_meal(
    uuid: str,
    meal_update: MealUpdate,
    service: MealService = Depends(get_meal_service)
):
    try:
        updated_meal = service.update(uuid, meal_update)
        if not updated_meal:
            raise HTTPException(status_code=404, detail="Combo no encontrado")
        return updated_meal
    except HTTPException:
        raise
    except Exception as exc:
        handle_update_error(exc)

@router.delete("/{uuid}", status_code=204)
def delete_meal(
    uuid: str,
    service: MealService = Depends(get_meal_service)
):
    try:
        success = service.delete(uuid)
        if not success:
            raise HTTPException(status_code=404, detail="Combo no encontrado")
        return success
    except HTTPException:
        raise
    except Exception as exc:
        handle_delete_error(exc)