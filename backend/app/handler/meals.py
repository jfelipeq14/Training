"""
Manejador de excepciones específico para el módulo de meals (combos).
"""
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)


class MealExceptionHandler:
    """Handler específico para errores del módulo de meals"""
    
    @staticmethod
    def handle_create_error(exc: Exception) -> HTTPException:
        """Maneja errores durante la creación de meals"""
        if isinstance(exc, ValueError):
            logger.warning(f"Error de validación al crear combo: {str(exc)}")
            return HTTPException(status_code=409, detail=str(exc))
        
        if isinstance(exc, RequestValidationError):
            logger.warning(f"Error de validación de request: {str(exc)}")
            return HTTPException(status_code=422, detail="Datos de entrada inválidos")
        
        logger.error(f"Error inesperado al crear combo: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500, 
            detail="Error al crear el combo. Por favor, intente nuevamente."
        )
    
    @staticmethod
    def handle_get_error(exc: Exception) -> HTTPException:
        """Maneja errores durante la consulta de meals"""
        if isinstance(exc, ValueError):
            logger.warning(f"UUID inválido: {str(exc)}")
            return HTTPException(status_code=400, detail="Formato de UUID inválido")
        
        logger.error(f"Error al consultar combo: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500, 
            detail="Error al consultar el combo. Por favor, intente nuevamente."
        )
    
    @staticmethod
    def handle_update_error(exc: Exception) -> HTTPException:
        """Maneja errores durante la actualización de meals"""
        if isinstance(exc, ValueError):
            logger.warning(f"Error de validación al actualizar combo: {str(exc)}")
            return HTTPException(status_code=409, detail=str(exc))
        
        if isinstance(exc, RequestValidationError):
            logger.warning(f"Error de validación de request: {str(exc)}")
            return HTTPException(status_code=422, detail="Datos de entrada inválidos")
        
        logger.error(f"Error al actualizar combo: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500, 
            detail="Error al actualizar el combo. Por favor, intente nuevamente."
        )
    
    @staticmethod
    def handle_delete_error(exc: Exception) -> HTTPException:
        """Maneja errores durante la eliminación de meals"""
        if isinstance(exc, ValueError):
            logger.warning(f"UUID inválido al eliminar: {str(exc)}")
            return HTTPException(status_code=400, detail="Formato de UUID inválido")
        
        if isinstance(exc, IntegrityError):
            error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
            
            if "ForeignKeyViolation" in error_msg or "violates foreign key" in error_msg:
                logger.warning("Intento de eliminar combo con pedidos asociados")
                return HTTPException(
                    status_code=409,
                    detail="No se puede eliminar el combo porque tiene pedidos asociados."
                )
            elif "UniqueViolation" in error_msg or "violates unique constraint" in error_msg:
                logger.warning("Violación de constraint único")
                return HTTPException(
                    status_code=409,
                    detail="Ya existe un registro con esta información."
                )
        
        if isinstance(exc, RequestValidationError):
            logger.warning(f"Error de validación de request: {str(exc)}")
            return HTTPException(status_code=422, detail="Datos de entrada inválidos")
        
        logger.error(f"Error al eliminar combo: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500, 
            detail="Error al eliminar el combo. Por favor, intente nuevamente."
        )


def handle_meal_exception(exc: Exception, operation: str) -> HTTPException:
    """
    Función auxiliar para manejar excepciones según la operación
    """
    handler = MealExceptionHandler()
    
    if operation == "create":
        return handler.handle_create_error(exc)
    elif operation == "get":
        return handler.handle_get_error(exc)
    elif operation == "update":
        return handler.handle_update_error(exc)
    elif operation == "delete":
        return handler.handle_delete_error(exc)
    else:
        logger.error(f"Error en operación {operation}: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500,
            detail="Error inesperado. Por favor, contacte al administrador."
        )


# Funciones exportables para uso directo en controllers
def handle_create_error(exc: Exception):
    """Maneja errores de creación de meals - lanza HTTPException"""
    raise MealExceptionHandler.handle_create_error(exc)


def handle_get_error(exc: Exception):
    """Maneja errores de consulta de meals - lanza HTTPException"""
    raise MealExceptionHandler.handle_get_error(exc)


def handle_update_error(exc: Exception):
    """Maneja errores de actualización de meals - lanza HTTPException"""
    raise MealExceptionHandler.handle_update_error(exc)


def handle_delete_error(exc: Exception):
    """Maneja errores de eliminación de meals - lanza HTTPException"""
    raise MealExceptionHandler.handle_delete_error(exc)
