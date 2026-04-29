from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class CustomerBase(BaseModel):
    document_number: str = Field(..., min_length=1, max_length=20, description="Número de documento (tipo-guion-número)")
    full_name: str = Field(..., min_length=1, max_length=255, description="Nombre y apellido completo")
    email: str = Field(..., max_length=255, description="Email del cliente")
    phone_number: str = Field(..., min_length=1, max_length=10, description="Número de celular (máximo 10 dígitos)")
    address: str = Field(..., min_length=1, max_length=500, description="Dirección de envío")

class CustomerCreate(CustomerBase):
    @field_validator('document_number')
    def validate_document_format(cls, v):
        # Validar formato: TIPO-NUMERO (CC-12345678, CE-123456, P-1234567)
        if not re.match(r'^[A-Z]{1,3}-\d+$', v.upper()):
            raise ValueError('El documento debe tener formato TIPO-NUMERO (ej: CC-12345678)')
        return v.upper()
    
    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if not v.isdigit():
            raise ValueError('El número de celular debe contener solo dígitos')
        if len(v) < 7 or len(v) > 10:
            raise ValueError('El número de celular debe tener entre 7 y 10 dígitos')
        return v
    
    @field_validator('email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('Email inválido')
        return v.lower()

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, min_length=1, max_length=10)
    address: Optional[str] = Field(None, min_length=1, max_length=500)

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if v is not None:
            if not v.isdigit():
                raise ValueError('El número de celular debe contener solo dígitos')
            if len(v) < 7 or len(v) > 10:
                raise ValueError('El número de celular debe tener entre 7 y 10 dígitos')
        return v
    
    @field_validator('email')
    def validate_email(cls, v):
        if v is not None:
            if '@' not in v or '.' not in v.split('@')[-1]:
                raise ValueError('Email inválido')
            return v.lower()
        return v

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CustomerListResponse(BaseModel):
    customers: list[CustomerResponse]
    total: int