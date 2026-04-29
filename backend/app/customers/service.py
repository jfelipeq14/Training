# customers/service.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.customers.repository import CustomerRepository
from app.customers.model import Customer
from app.customers.schema import CustomerCreate, CustomerUpdate

import re

class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository
    
    def create(self, customer_data):
        """Crear cliente con validaciones"""
        # Manejar tanto CustomerCreate como diccionario
        if hasattr(customer_data, 'document_number'):
            # Es un objeto CustomerCreate
            document_number = customer_data.document_number
            email = customer_data.email
            phone_number = customer_data.phone_number
            data_dict = customer_data.model_dump()
        else:
            # Es un diccionario
            document_number = customer_data['document_number']
            email = customer_data['email']
            phone_number = customer_data['phone_number']
            data_dict = customer_data
        
        # Verificar que el documento no exista
        existing_customer = self.get_customer(document_number)
        if existing_customer:
            raise ValueError(f"Ya existe un cliente con documento '{document_number}'")
        
        # Verificar que el email no exista
        existing_email = self.repository.get_by_email(email)
        if existing_email:
            raise ValueError(f"Ya existe un cliente con email '{email}'")
        
        # Verificar que el teléfono no exista
        existing_phone = self.repository.get_by_phone(phone_number)
        if existing_phone:
            raise ValueError(f"Ya existe un cliente con teléfono '{phone_number}'")
        
        return self.repository.create(data_dict)

    def get_customer(self, document: str) -> Optional[Customer]:
        """Obtener cliente por documento con validación de formato"""
        # Validar formato: TIPO-NUMERO (CC-12345678, CE-123456, P-1234567)
        if not re.match(r'^[A-Z]{1,3}-\d+$', document.upper()):
            raise ValueError("Formato de documento inválido. Debe tener formato TIPO-NUMERO (ej: CC-12345678)")
        return self.repository.get_by_document(document)
    
    def update_customer(self, document: str, customer_data: CustomerUpdate) -> Optional[Customer]:
        """Actualizar cliente por documento"""
        customer = self.get_customer(document)
        if not customer:
            return None
        
        # Si se actualiza el email, verificar que no exista
        if customer_data.email and customer_data.email != customer.email:
            existing_email = self.repository.get_by_email(customer_data.email)
            if existing_email:
                raise ValueError(f"Ya existe un cliente con email '{customer_data.email}'")
        
        # Si se actualiza el teléfono, verificar que no exista
        if customer_data.phone_number and customer_data.phone_number != customer.phone_number:
            existing_phone = self.repository.get_by_phone(customer_data.phone_number)
            if existing_phone:
                raise ValueError(f"Ya existe un cliente con teléfono '{customer_data.phone_number}'")
        
        update_data = customer_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)
        
        self.repository.db.commit()
        self.repository.db.refresh(customer)
        return customer
    
    def delete(self, document: str) -> bool:
        """Eliminar cliente por documento"""
        customer = self.get_customer(document)
        if not customer:
            return False
        return self.repository.delete(document)