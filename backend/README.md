# 🍔 Grandma's Food Backend

API RESTful para gestión de pedidos a domicilio de Grandma's Food construida con FastAPI, SQLAlchemy y PostgreSQL.

## 📋 **Tabla de Contenido**

- [🏗️ Arquitectura](#️-arquitectura)
- [🚀 Instalación](#-instalación)
- [🧪 Pruebas](#-pruebas)
- [📦 Dependencias](#-dependencias)
- [🎯 Características Clave](#-características-clave)
- [🚀 Despliegue](#-despliegue)
- [🤝 Contribución](#-contribución)
- [� Licencia](#-licencia)

---

## 🏗️ **Arquitectura**

### **Controller + Service + Repository Pattern**

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuración de variables de entorno
│   │   └── database.py         # Conexión a base de datos
│   ├── models/
│   │   └── base.py            # Modelo base SQLAlchemy
│   ├── repositories/
│   │   └── base.py            # Repositorio base genérico
│   └── services/
│       └── base.py            # Servicio base genérico
├── customers/
│   ├── controllers.py         # 🆕 Controladores de clientes
│   ├── models.py              # Modelo SQLAlchemy Customer
│   ├── schemas.py             # Schemas Pydantic
│   ├── repository.py          # Repositorio CustomerRepository
│   ├── service.py             # Servicio CustomerService
│   └── __init__.py
├── meals/
│   ├── controllers.py         # 🆕 Controladores de combos
│   ├── models.py              # Modelo SQLAlchemy Meal
│   ├── schemas.py             # Schemas Pydantic
│   ├── repository.py          # Repositorio MealRepository
│   ├── service.py             # Servicio MealService
│   └── __init__.py
├── orders/
│   ├── controllers.py         # 🆕 Controladores de pedidos
│   ├── models.py              # Modelo SQLAlchemy Order
│   ├── schemas.py             # Schemas Pydantic
│   ├── repository.py          # Repositorio OrderRepository
│   ├── service.py             # Servicio OrderService
│   └── __init__.py
├── tests/
│   ├── conftest.py            # Configuración global de pytest
│   ├── factories.py           # Data factories para pruebas
│   ├── test_customers/
│   │   ├── test_repositories.py    # Pruebas de repositorios
│   │   ├── test_services.py         # Pruebas de servicios
│   │   └── test_controllers.py      # Pruebas de controladores
│   ├── test_meals/
│   │   ├── test_repositories.py    # Pruebas de repositorios
│   │   ├── test_services.py         # Pruebas de servicios
│   │   └── test_controllers.py      # Pruebas de controladores
│   ├── test_orders/
│   │   ├── test_repositories.py    # Pruebas de repositorios
│   │   ├── test_services.py         # Pruebas de servicios
│   │   └── test_controllers.py      # Pruebas de controladores
│   └── test_integration/
│       └── test_integration.py        # Pruebas de integración
├── scripts/
│   └── seed_data.py          # Script para datos de prueba
├── main.py                   # Punto de entrada
├── requirements.txt           # Dependencias Python
└── .env                     # Variables de entorno
```

### **🔄 Flujo de Datos**

```
HTTP Request → Controller → Service → Repository → Database
     ↑                ↑           ↑           ↑
Response ← Controller ← Service ← Repository ← Database
```

### **🎯 Responsabilidades por Capa**

- **Controllers**: Manejo de peticiones HTTP y validación
- **Services**: Lógica de negocio, cálculos y coordinación
- **Repositories**: Acceso a datos y operaciones CRUD

---

## 🚀 **Instalación**

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd backend

# 2. Construir y levantar servicios
docker compose up --build

# 3. Esperar a que los servicios inicien
sleep 10

# 4. Inicializar datos
docker exec -it fast_api python scripts/seed_data.py

# 5. Acceder a la API
http://localhost:8000/docs
```

### **📋 Servicios Docker**
- **fast_api**: API FastAPI en puerto 8000
- **fast_db**: Base de datos PostgreSQL en puerto 5432

---

## 🧪 **Pruebas**

### **📊 Estructura de Pruebas**

- **Repository Tests**: Pruebas de acceso a datos con BD real
- **Service Tests**: Pruebas de lógica de negocio con mocks
- **Controller Tests**: Pruebas de endpoints HTTP
- **Integration Tests**: Pruebas de flujo completo

### **🎮 Ejecución de Pruebas**

```bash
# Todas las pruebas
pytest

# Pruebas por capa
pytest tests/test_customers/test_repositories.py
pytest tests/test_meals/test_services.py
pytest tests/test_orders/test_controllers.py

# Pruebas por módulo
pytest tests/test_customers/
pytest tests/test_meals/
pytest tests/test_orders/

# Pruebas de integración
pytest tests/test_integration/

# Con coverage
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### **📈 Estadísticas de Pruebas**

- **Total**: 129 pruebas
- **Repository**: 40 pruebas (31.0%)
- **Service**: 37 pruebas (28.7%)
- **Controller**: 42 pruebas (32.6%)
- **Integration**: 10 pruebas (7.7%)

---

## 📦 **Dependencias**

### **🔧 Core Dependencies**
- `fastapi==0.104.1` - Framework web
- `uvicorn[standard]==0.24.0` - Servidor ASGI
- `sqlalchemy==2.0.23` - ORM
- `psycopg2-binary==2.9.9` - Driver PostgreSQL
- `pydantic==2.5.0` - Validación de datos
- `pydantic-settings==2.1.0` - Configuración
- `email-validator==2.1.0` - Validación de emails
- `python-multipart==0.0.6` - Form data

### **🧪 Testing Dependencies**
- `pytest==7.4.3` - Framework de pruebas
- `pytest-asyncio==0.21.1` - Soporte asíncrono
- `httpx==0.25.2` - Cliente HTTP para pruebas
- `factory-boy==3.3.0` - Data factories
- `faker==20.1.0` - Datos falsos realistas
- `coverage==7.3.2` - Medición de coverage
- `pytest-cov==4.1.0` - Plugin coverage para pytest
- `sqlalchemy-utils==0.41.1` - Utilidades SQLAlchemy


---

## 🎯 **Características Clave**

- ✅ **API RESTful** con FastAPI
- ✅ **Validación de datos** con Pydantic
- ✅ **Base de datos PostgreSQL** con UUIDs
- ✅ **Arquitectura limpia** Controller+Service+Repository
- ✅ **Pruebas completas** (129 tests)
- ✅ **Docker ready** para producción
- ✅ **Type hints** en todo el código
- ✅ **Manejo de errores** consistente
- ✅ **Logging estructurado**
- ✅ **CORS configurado**

---

## 🚀 **Despliegue**

### **🐳 Docker Production**
```bash
# Build imagen optimizada
docker build -t grandma-food-backend .

# Run en producción
docker run -d \
  --name grandma-food-api \
  -p 8000:8000 \
  -e DATABASE_URL=$DATABASE_URL \
  grandma-food-backend
```

### **☁️ Cloud Deployment**
La API está lista para desplegar en:
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**
- **Heroku**
- **DigitalOcean App Platform**

---

## 🤝 **Contribución**

1. Fork del repositorio
2. Crear feature branch: `git checkout -b feature/amazing-feature`
3. Commit cambios: `git commit -m 'Add amazing feature'`
4. Push al branch: `git push origin feature/amazing-feature`
5. Abrir Pull Request

---

## 📄 **Licencia**

Este proyecto está bajo licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🎉 **Resumen**

Backend profesional para Grandma's Food con:

- **🏗️ Arquitectura limpia** y escalable
- **🧪 Pruebas completas** y bien organizadas
- **📚 Documentación automática** y completa
- **🐳 Docker ready** para producción
- **🔧 Configuración flexible** y segura

**¡Listo para producción y desarrollo!** 🚀
