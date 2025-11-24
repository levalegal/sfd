"""
Декораторы для валидации и обработки ошибок
"""
from functools import wraps
from typing import Callable, Any
from app.utils.logger import setup_logger
from app.utils.exceptions import ValidationException, DatabaseException

logger = setup_logger('decorators')


def validate_input(**validators):
    """Декоратор для валидации входных параметров"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Валидация параметров
            for param_name, validator_func in validators.items():
                if param_name in kwargs:
                    try:
                        validator_func(kwargs[param_name])
                    except Exception as e:
                        raise ValidationException(f"Ошибка валидации {param_name}: {str(e)}")
            
            try:
                return func(*args, **kwargs)
            except ValidationException:
                raise
            except Exception as e:
                logger.error(f"Ошибка в {func.__name__}: {e}")
                raise DatabaseException(f"Ошибка выполнения {func.__name__}: {str(e)}")
        
        return wrapper
    return decorator


def log_operation(operation_name: str = None):
    """Декоратор для логирования операций"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__
            logger.info(f"Начало операции: {op_name}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Операция {op_name} успешно завершена")
                return result
            except Exception as e:
                logger.error(f"Ошибка в операции {op_name}: {e}")
                raise
        
        return wrapper
    return decorator


def handle_db_errors(func: Callable) -> Callable:
    """Декоратор для обработки ошибок БД"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseException:
            raise
        except Exception as e:
            logger.error(f"Ошибка БД в {func.__name__}: {e}")
            raise DatabaseException(f"Ошибка работы с БД: {str(e)}")
    
    return wrapper

