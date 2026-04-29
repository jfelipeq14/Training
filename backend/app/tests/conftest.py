# tests/conftest.py - Configuración global de pytest
import pytest
import asyncio
from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from httpx import AsyncClient
import uuid

from config.database import get_db
from app.tests.test_models import TestCustomer, TestMeal, TestOrder
from main import app

# Base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def event_loop():
    """Crear event loop para pruebas asíncronas"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_db_session():
    """Mock de sesión de base de datos para pruebas"""
    return Mock()

@pytest.fixture(scope="function")
def db_session():
    """Crear sesión de base de datos para pruebas con modelos compatibles"""
    # Crear tablas con modelos de prueba
    TestCustomer.metadata.create_all(bind=engine)
    TestMeal.metadata.create_all(bind=engine)
    TestOrder.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Limpiar tablas después de cada prueba
        TestCustomer.metadata.drop_all(bind=engine)
        TestMeal.metadata.drop_all(bind=engine)
        TestOrder.metadata.drop_all(bind=engine)

@pytest.fixture
def client(mock_db_session):
    """Crear cliente de prueba FastAPI con mock DB"""
    def override_get_db():
        try:
            yield mock_db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def async_client(mock_db_session):
    """Crear cliente asíncrono de prueba con mock DB"""
    def override_get_db():
        try:
            yield mock_db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_customer_data():
    """Datos de cliente válidos según contrato"""
    return {
        "document_number": "CC-12345678",
        "full_name": "Juan Pérez García",
        "email": "juan.perez@example.com",
        "phone_number": "3001234567",
        "address": "Calle 123 #45-67, Bogotá, Colombia"
    }

@pytest.fixture
def sample_meal_data():
    """Datos de combo válidos según contrato"""
    return {
        "name": "COMBO HAMBURGUESA CLÁSICA",
        "category": "HAMBURGERS_AND_HOTDOGS",
        "description": "Hamburguesa pan de ajonjolí, carne de 200gr, queso cheddar, papas fritas y gaseosa de 350ml",
        "price_without_iva": 15000.00,
        "is_available": True
    }

@pytest.fixture
def sample_order_data():
    """Datos de pedido válidos según contrato"""
    return {
        "document": "CC-12345678",
        "meal_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "quantity": 2,
        "additional_info": "Hamburguesa sin salsa de tomate"
    }
