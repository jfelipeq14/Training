# orders/schemas.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal
from uuid import UUID

class OrderBase(BaseModel):
    document: str = Field(..., description="Documento del cliente")
    meal_uuid: UUID = Field(..., description="UUID del combo")
    quantity: int = Field(..., ge=1, lt=100, description="Cantidad (1-99)")
    additional_info: str = Field("", max_length=511, description="Información adicional")

class OrderCreate(OrderBase):
    @field_validator('quantity')
    def validate_quantity(cls, v):
        if v < 1 or v >= 100:
            raise ValueError('La cantidad debe ser entre 1 y 99')
        return v

class OrderUpdate(BaseModel):
    timestamp: datetime = Field(..., description="Hora de entrega del producto")
    
class OrderResponse(BaseModel):
    id: int
    uuid: UUID
    order_date: datetime
    document: str
    meal_uuid: UUID
    quantity: int
    additional_info: str
    subtotal_without_iva: Decimal
    iva_amount: Decimal
    total_with_iva: Decimal
    is_delivered: bool
    delivery_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}

class OrderResponseWithDetails(OrderResponse):
    customer_name: Optional[str] = None
    meal_name: Optional[str] = None
    meal_category: Optional[str] = None

class OrderListResponse(BaseModel):
    orders: list[OrderResponse]
    total: int
