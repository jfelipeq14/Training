"""
API Principal de Grandma's Food
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError

from config.config import settings
from config.database import engine
from app.customers.model import Base

# Importar handlers globales
from app.handler.base import (
    integrity_error_handler,
    operational_error_handler,
    validation_error_handler,
    request_validation_error_handler,
    generic_exception_handler
)

# Importar controllers
from app.customers.controller import router as customers_router
from app.meals.controller import router as meals_router
from app.orders.controller import router as orders_router

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Grandma's Food API",
    description="API para gestión de pedidos a domicilio de Grandma's Food",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Registrar manejadores globales de excepciones
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(OperationalError, operational_error_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Incluir controllers (arquitectura Controller + Service + Repository)
app.include_router(customers_router)
app.include_router(meals_router)
app.include_router(orders_router)


@app.get("/")
def read_root():
    return {
        "message": "Grandma's Food API corriendo en Docker",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Grandma's Food API"}
