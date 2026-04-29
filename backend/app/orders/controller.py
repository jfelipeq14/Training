# orders/controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from config.database import get_db
from app.orders.service import OrderService
from app.orders.repository import OrderRepository
from app.meals.repository import MealRepository
from app.customers.repository import CustomerRepository
from app.orders.schema import OrderCreate, OrderUpdate, OrderResponse, OrderListResponse, OrderResponseWithDetails
from app.handler.orders import handle_create_error, handle_get_error, handle_update_error

router = APIRouter(prefix="/orders", tags=["orders"])

def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    order_repository = OrderRepository(db)
    meal_repository = MealRepository(db)
    customer_repository = CustomerRepository(db)
    return OrderService(order_repository, meal_repository, customer_repository)

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(
    order: OrderCreate,
    service: OrderService = Depends(get_order_service)
):
    try:
        return service.create_order(order)
    except Exception as exc:
        handle_create_error(exc)

@router.put("/{uuid}", response_model=OrderResponse)
def update_order(
    uuid: str,
    order_update: OrderUpdate,
    service: OrderService = Depends(get_order_service)
):
    try:
        updated_order = service.update_order(uuid, order_update.timestamp)
        if not updated_order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return updated_order
    except HTTPException:
        raise
    except Exception as exc:
        handle_update_error(exc)
