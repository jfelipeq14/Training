"""
Manejador global de excepciones para la API de Grandma's Food.
Este módulo define handlers para errores generales que afectan a toda la aplicación.
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
import logging

# Configurar logger
logger = logging.getLogger(__name__)


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    Maneja errores de integridad de la base de datos (ForeignKey, Unique, etc.)
    Captura violaciones de constraints sin exponer detalles SQL al cliente.
    """
    error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    
    # Log interno del error completo (para debugging)
    logger.error(f"IntegrityError: {error_msg}", exc_info=True)
    
    # Detectar tipo de violación sin exponer detalles SQL
    if "ForeignKeyViolation" in error_msg or "violates foreign key" in error_msg:
        return JSONResponse(
            status_code=409,
            content={
                "detail": "No se puede eliminar este registro porque tiene pedidos asociados. Complete o cancele los pedidos pendientes antes de continuar.",
                "error_code": "FOREIGN_KEY_VIOLATION"
            }
        )
    elif "UniqueViolation" in error_msg or "violates unique constraint" in error_msg:
        return JSONResponse(
            status_code=409,
            content={
                "detail": "Ya existe un registro con esta información. Verifique los datos e intente nuevamente.",
                "error_code": "UNIQUE_VIOLATION"
            }
        )
    else:
        return JSONResponse(
            status_code=409,
            content={
                "detail": "Error de integridad en la base de datos. Por favor, contacte al administrador.",
                "error_code": "INTEGRITY_ERROR"
            }
        )


async def operational_error_handler(request: Request, exc: OperationalError):
    """
    Maneja errores operacionales de la base de datos (conexión perdida, timeout, etc.)
    """
    logger.error(f"OperationalError: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Servicio temporalmente no disponible. Intente nuevamente en unos momentos.",
            "error_code": "DATABASE_UNAVAILABLE"
        }
    )


async def validation_error_handler(request: Request, exc: ValidationError):
    """
    Maneja errores de validación de Pydantic
    """
    logger.warning(f"ValidationError: {str(exc)}", exc_info=False)
    
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error.get("loc", []))
        msg = error.get("msg", "Error de validación")
        errors.append({"field": field, "message": msg})
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Error de validación en los datos proporcionados.",
            "errors": errors,
            "error_code": "VALIDATION_ERROR"
        }
    )


async def request_validation_error_handler(request: Request, exc: RequestValidationError):
    """
    Maneja errores de validación de requests de FastAPI
    """
    logger.warning(f"RequestValidationError: {str(exc)}", exc_info=False)
    
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error.get("loc", []))
        msg = error.get("msg", "Error de validación")
        errors.append({"field": field, "message": msg})
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Error de validación en la solicitud.",
            "errors": errors,
            "error_code": "REQUEST_VALIDATION_ERROR"
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """
    Manejador genérico para cualquier excepción no capturada
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor. Por favor, contacte al administrador.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )
