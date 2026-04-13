# customers/repository.py
from typing import Optional
from sqlalchemy.orm import Session
from app.customers.model import Customer

class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: dict) -> Customer:
        obj = Customer(**obj_in)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, id: int) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.id == id).first()

    def update(self, id: int, obj_in: dict) -> Optional[Customer]:
        obj = self.db.query(Customer).filter(Customer.id == id).first()
        if obj:
            for key, value in obj_in.items():
                setattr(obj, key, value)
            self.db.commit()
            self.db.refresh(obj)
        return obj

    def delete(self, document_number: str) -> bool:
        """Eliminar cliente por documento"""
        customer = self.get_by_document(document_number)
        if not customer:
            return False
        self.db.delete(customer)
        self.db.commit()
        return True

    def get_by_document(self, document_number: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.document_number == document_number).first()
    
    def get_by_email(self, email: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.email == email).first()
    
    def get_by_phone(self, phone_number: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.phone_number == phone_number).first()