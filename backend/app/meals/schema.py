# meals/schemas.py
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional
from decimal import Decimal
from datetime import datetime
from uuid import UUID

class CategoryEnum(str, Enum):
    HAMBURGERS_AND_HOTDOGS = "HAMBURGERS_AND_HOTDOGS"
    CHICKEN = "CHICKEN"
    FISH = "FISH"
    MEATS = "MEATS"
    DESSERTS = "DESSERTS"
    VEGAN_FOOD = "VEGAN_FOOD"
    KIDS_MEALS = "KIDS_MEALS"

class MealBase(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    
    name: str = Field(..., min_length=1, max_length=255, description="Nombre del combo (máximo 255 caracteres)")
    category: CategoryEnum
    description: str = Field(..., min_length=1, description="Descripción del combo")
    price_without_iva: Decimal = Field(..., gt=0)
    is_available: bool = True

class MealCreate(MealBase):
    @field_validator('name')
    def name_to_uppercase(cls, v):
        if v is not None:
            return v.upper()
        return v

class MealUpdate(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[CategoryEnum] = None
    description: Optional[str] = Field(None, min_length=1)
    price_without_iva: Optional[Decimal] = Field(None, gt=0)
    is_available: Optional[bool] = None

class MealResponse(MealBase):
    id: int
    uuid: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}

class MealListResponse(BaseModel):
    meals: list[MealResponse]
    total: int