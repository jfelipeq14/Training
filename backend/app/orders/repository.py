# orders/repository.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.orders.model import Order
from typing import Optional

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: dict) -> Order:
        obj = Order(**obj_in)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, id: int) -> Optional[Order]:
        return self.db.query(Order).filter(Order.id == id).first()
    
    def get_by_uuid(self, uuid: str) -> Optional[Order]:
        """Obtener pedido por UUID"""
        return self.db.query(Order).filter(Order.uuid == uuid).first()
    
    def update(self, uuid: str, update_data: dict) -> Optional[Order]:
        """Actualizar pedido por UUID"""
        order = self.get_by_uuid(uuid)
        if not order:
            return None
        for key, value in update_data.items():
            setattr(order, key, value)
        self.db.commit()
        self.db.refresh(order)
        return order