# orders/service.py
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session
from app.orders.repository import OrderRepository
from app.orders.model import Order
from app.orders.schema import OrderCreate, OrderUpdate
from app.meals.repository import MealRepository
from app.customers.repository import CustomerRepository

class OrderService:
    IVA_RATE = Decimal('0.19')
    
    def __init__(self, repository: OrderRepository, meal_repository: MealRepository, customer_repository: CustomerRepository):
        self.repository = repository
        self.meal_repository = meal_repository
        self.customer_repository = customer_repository
    
    def create_order(self, order_data: OrderCreate) -> Order:
        # Verificar que el cliente exista
        customer = self.customer_repository.get_by_document(order_data.document)
        if not customer:
            raise ValueError(f"Cliente con documento '{order_data.document}' no encontrado")
        
        # Verificar que el combo exista
        meal = self.meal_repository.get_by_uuid(order_data.meal_uuid)
        if not meal:
            raise ValueError(f"Combo con UUID '{order_data.meal_uuid}' no encontrado")
        
        # Calcular valores
        subtotal = Decimal(str(meal.price_without_iva)) * Decimal(str(order_data.quantity))
        iva_amount = subtotal * self.IVA_RATE
        total = subtotal + iva_amount
        
        # Crear diccionario del pedido
        order_dict = {
            'document': order_data.document,
            'meal_uuid': order_data.meal_uuid,
            'meal_id': meal.id,  # Guardar referencia al meal_id
            'quantity': order_data.quantity,
            'additional_info': order_data.additional_info,
            'subtotal_without_iva': subtotal,
            'iva_amount': iva_amount,
            'total_with_iva': total,
            'is_delivered': False,
            'order_date': datetime.utcnow(),
            'delivery_date': None
        }
        
        return self.repository.create(order_dict)
    
    def update_order(self, uuid: str, timestamp: datetime) -> Optional[Order]:
        """Actualizar pedido con timestamp de entrega"""
        order = self.repository.get_by_uuid(uuid)
        if not order:
            return None
        
        update_data = {
            'is_delivered': True,
            'delivery_date': timestamp,
            'updated_at': datetime.utcnow()
        }
        
        return self.repository.update(uuid, update_data)
    
    def get_by_uuid(self, uuid: str) -> Optional[Order]:
        """Obtener pedido por UUID"""
        return self.repository.get_by_uuid(uuid)
    
    def update_order_delivery(self, uuid: str, timestamp: datetime) -> Optional[Order]:
        """Actualizar pedido con timestamp de entrega"""
        return self.update_order(uuid, timestamp)