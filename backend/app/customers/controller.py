# customers/controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from config.database import get_db
from app.customers.service import CustomerService
from app.customers.repository import CustomerRepository
from app.customers.schema import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerListResponse
from app.handler.customers import handle_create_error, handle_get_error, handle_update_error, handle_delete_error

router = APIRouter(prefix="/customers", tags=["customers"])

def get_customer_service(db: Session = Depends(get_db)) -> CustomerService:
    repository = CustomerRepository(db)
    return CustomerService(repository)

@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    customer: CustomerCreate,
    service: CustomerService = Depends(get_customer_service)
):
    try:
        return service.create(customer)
    except Exception as exc:
        handle_create_error(exc)

@router.get("/{document}", response_model=CustomerResponse)
def get_customer_by_document(
    document: str,
    service: CustomerService = Depends(get_customer_service)
):
    try:
        customer = service.get_customer(document)
        if not customer:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return customer
    except HTTPException:
        raise
    except Exception as exc:
        handle_get_error(exc)

@router.put("/{document}", status_code=204)
def update_customer(
    document: str,
    customer_update: CustomerUpdate,
    service: CustomerService = Depends(get_customer_service)
):
    try:
        updated_customer = service.update_customer(document, customer_update)
        if not updated_customer:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    except HTTPException:
        raise
    except Exception as exc:
        handle_update_error(exc)

@router.delete("/{document}", status_code=204)
def delete_customer(
    document: str,
    service: CustomerService = Depends(get_customer_service)
):
    try:
        success = service.delete(document)
        if not success:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    except HTTPException:
        raise
    except Exception as exc:
        handle_delete_error(exc)