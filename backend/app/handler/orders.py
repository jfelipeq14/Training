"""
Manejador de excepciones específico para el módulo de orders (pedidos).
"""
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)


class OrderExceptionHandler:
    """Handler específico para errores del módulo de orders"""
    
    @staticmethod
    def handle_create_error(exc: Exception) -> HTTPException:
        """Maneja errores durante la creación de orders"""
        if isinstance(exc, ValueError):
            error_msg = str(exc)
            logger.warning(f"Error de validación al crear pedido: {error_msg}")
            
            # Determinar si es un error 404 o 409 basado en el mensaje
            if "no encontrado" in error_msg.lower():
                return HTTPException(status_code=404, detail=error_msg)
            return HTTPException(status_code=409, detail=error_msg)
        
        if isinstance(exc, RequestValidationError):
            logger.warning(f"Error de validación de request: {str(exc)}")
            return HTTPException(status_code=422, detail="Datos de entrada inválidos")
        
        logger.error(f"Error inesperado al crear pedido: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500, 
            detail="Error al crear el pedido. Por favor, intente nuevamente."
        )
    
    @staticmethod
    def handle_get_error(exc: Exception) -> HTTPException:
        """Maneja errores durante la consulta de orders"""
        if isinstance(exc, ValueError):
            logger.warning(f"UUID inválido: {str(exc)}")
            return HTTPException(status_code=400, detail="Formato de UUID inválido")
        
        logger.error(f"Error al consultar pedido: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500, 
            detail="Error al consultar el pedido. Por favor, intente nuevamente."
        )
    
    @staticmethod
    def handle_update_error(exc: Exception) -> HTTPException:
        """Maneja errores durante la actualización de orders"""
        if isinstance(exc, ValueError):
            logger.warning(f"Error de validación al actualizar pedido: {str(exc)}")
            return HTTPException(status_code=400, detail="Formato de UUID inválido")
        
        if isinstance(exc, RequestValidationError):
            logger.warning(f"Error de validación de request: {str(exc)}")
            return HTTPException(status_code=422, detail="Datos de entrada inválidos")
        
        logger.error(f"Error al actualizar pedido: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500, 
            detail="Error al actualizar el pedido. Por favor, intente nuevamente."
        )
    
    @staticmethod
    def handle_delete_error(exc: Exception) -> HTTPException:
        """Maneja errores durante la eliminación de orders"""
        if isinstance(exc, ValueError):
            logger.warning(f"UUID inválido al eliminar: {str(exc)}")
            return HTTPException(status_code=400, detail="Formato de UUID inválido")
        
        if isinstance(exc, IntegrityError):
            error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
            
            if "ForeignKeyViolation" in error_msg or "violates foreign key" in error_msg:
                logger.warning("Violación de foreign key al eliminar pedido")
                return HTTPException(
                    status_code=409,
                    detail="No se puede eliminar el pedido porque tiene dependencias asociadas."
                )
            elif "UniqueViolation" in error_msg or "violates unique constraint" in error_msg:
                logger.warning("Violación de constraint único")
                return HTTPException(
                    status_code=409,
                    detail="Ya existe un registro con esta información."
                )
        
        logger.error(f"Error al eliminar pedido: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500, 
            detail="Error al eliminar el pedido. Por favor, intente nuevamente."
        )


def handle_order_exception(exc: Exception, operation: str) -> HTTPException:
    """
    Función auxiliar para manejar excepciones según la operación
    """
    handler = OrderExceptionHandler()
    
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
    """Maneja errores de creación de orders - lanza HTTPException"""
    raise OrderExceptionHandler.handle_create_error(exc)


def handle_get_error(exc: Exception):
    """Maneja errores de consulta de orders - lanza HTTPException"""
    raise OrderExceptionHandler.handle_get_error(exc)


def handle_update_error(exc: Exception):
    """Maneja errores de actualización de orders - lanza HTTPException"""
    raise OrderExceptionHandler.handle_update_error(exc)


def handle_delete_error(exc: Exception):
    """Maneja errores de eliminación de orders - lanza HTTPException"""
    raise OrderExceptionHandler.handle_delete_error(exc)
