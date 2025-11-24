"""
Кастомные исключения
"""
from typing import Optional


class DormitoryException(Exception):
    """Базовое исключение для системы"""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
    
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class ValidationException(DormitoryException):
    """Ошибка валидации данных"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field


class DatabaseException(DormitoryException):
    """Ошибка работы с БД"""
    
    def __init__(self, message: str, sql_error: Optional[str] = None):
        super().__init__(message, "DATABASE_ERROR")
        self.sql_error = sql_error


class BusinessRuleException(DormitoryException):
    """Нарушение бизнес-правил"""
    
    def __init__(self, message: str, rule_name: Optional[str] = None):
        super().__init__(message, "BUSINESS_RULE_VIOLATION")
        self.rule_name = rule_name


class NotFoundException(DormitoryException):
    """Запись не найдена"""
    
    def __init__(self, message: str, entity_type: Optional[str] = None):
        super().__init__(message, "NOT_FOUND")
        self.entity_type = entity_type

