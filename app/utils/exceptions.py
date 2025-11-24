"""
Кастомные исключения
"""


class DormitoryException(Exception):
    """Базовое исключение для системы"""
    pass


class ValidationException(DormitoryException):
    """Ошибка валидации данных"""
    pass


class DatabaseException(DormitoryException):
    """Ошибка работы с БД"""
    pass


class BusinessRuleException(DormitoryException):
    """Нарушение бизнес-правил"""
    pass

