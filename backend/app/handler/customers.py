"""
Manejador de excepciones específico para el módulo de clientes.
"""
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


class CustomerExceptionHandler:
    """Handler específico para errores del módulo de clientes"""
    
    @staticmethod
    def handle_create_error(exc: Exception) -> HTTPException:
        """Maneja errores durante la creación de clientes"""
        if isinstance(exc, ValueError):
            logger.warning(f"Error de validación al crear cliente: {str(exc)}")
            return HTTPException(status_code=409, detail=str(exc))
        
        logger.error(f"Error inesperado al crear cliente: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500, 
            detail="Error al crear el cliente. Por favor, intente nuevamente."
        )
    
    @staticmethod
    def handle_get_error(exc: Exception) -> HTTPException:
        """Maneja errores durante la consulta de clientes"""
        if isinstance(exc, ValueError):
            logger.warning(f"Documento inválido: {str(exc)}")
            return HTTPException(status_code=400, detail="Formato de documento inválido")
        
        logger.error(f"Error al consultar cliente: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500, 
            detail="Error al consultar el cliente. Por favor, intente nuevamente."
        )
    
    @staticmethod
    def handle_update_error(exc: Exception) -> HTTPException:
        """Maneja errores durante la actualización de clientes"""
        if isinstance(exc, ValueError):
            logger.warning(f"Error de validación al actualizar cliente: {str(exc)}")
            return HTTPException(status_code=409, detail=str(exc))
        
        logger.error(f"Error al actualizar cliente: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500, 
            detail="Error al actualizar el cliente. Por favor, intente nuevamente."
        )
    
    @staticmethod
    def handle_delete_error(exc: Exception) -> HTTPException:
        """Maneja errores durante la eliminación de clientes"""
        if isinstance(exc, ValueError):
            logger.warning(f"Documento inválido al eliminar: {str(exc)}")
            return HTTPException(status_code=400, detail="Formato de documento inválido")
        
        if isinstance(exc, IntegrityError):
            error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
            
            if "ForeignKeyViolation" in error_msg or "violates foreign key" in error_msg:
                logger.warning("Intento de eliminar cliente con pedidos asociados")
                return HTTPException(
                    status_code=409,
                    detail="No se puede eliminar el cliente porque tiene pedidos asociados. Complete o cancele los pedidos pendientes antes de eliminar."
                )
            elif "UniqueViolation" in error_msg or "violates unique constraint" in error_msg:
                logger.warning("Violación de constraint único")
                return HTTPException(
                    status_code=409,
                    detail="Ya existe un registro con esta información."
                )
        
        logger.error(f"Error al eliminar cliente: {str(exc)}", exc_info=True)
        return HTTPException(
            status_code=500, 
            detail="Error al eliminar el cliente. Por favor, intente nuevamente."
        )


def handle_customer_exception(exc: Exception, operation: str) -> HTTPException:
    """
    Función auxiliar para manejar excepciones según la operación
    """
    handler = CustomerExceptionHandler()
    
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
    """Maneja errores de creación de clientes - lanza HTTPException"""
    raise CustomerExceptionHandler.handle_create_error(exc)


def handle_get_error(exc: Exception):
    """Maneja errores de consulta de clientes - lanza HTTPException"""
    raise CustomerExceptionHandler.handle_get_error(exc)


def handle_update_error(exc: Exception):
    """Maneja errores de actualización de clientes - lanza HTTPException"""
    raise CustomerExceptionHandler.handle_update_error(exc)


def handle_delete_error(exc: Exception):
    """Maneja errores de eliminación de clientes - lanza HTTPException"""
    raise CustomerExceptionHandler.handle_delete_error(exc)
