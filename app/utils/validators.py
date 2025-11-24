"""
Модуль валидации данных
"""
import re
from typing import Optional, Callable
from functools import wraps


class ValidationError(Exception):
    """Исключение для ошибок валидации"""
    pass


def validator(func: Callable) -> Callable:
    """Декоратор для создания валидаторов"""
    @wraps(func)
    def wrapper(value, *args, **kwargs):
        try:
            return func(value, *args, **kwargs)
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(str(e))
    return wrapper


def validate_phone(phone):
    """Валидация номера телефона"""
    if not phone:
        raise ValidationError("Номер телефона обязателен")
    # Удаляем все нецифровые символы
    digits = re.sub(r'\D', '', phone)
    if len(digits) < 10:
        raise ValidationError("Номер телефона должен содержать минимум 10 цифр")
    return True


def validate_email(email):
    """Валидация email (опциональное поле)"""
    if not email:
        return True  # Email необязателен
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Некорректный формат email")
    return True


def validate_name(name, field_name="Имя"):
    """Валидация имени, фамилии, отчества"""
    if not name or not name.strip():
        raise ValidationError(f"{field_name} обязательно к заполнению")
    if len(name.strip()) < 2:
        raise ValidationError(f"{field_name} должно содержать минимум 2 символа")
    if not re.match(r'^[а-яА-ЯёЁa-zA-Z\s-]+$', name):
        raise ValidationError(f"{field_name} должно содержать только буквы")
    return True


def validate_group_number(group_number):
    """Валидация номера группы"""
    if not group_number or not group_number.strip():
        raise ValidationError("Номер группы обязателен")
    return True


def validate_building_number(building_number):
    """Валидация номера корпуса"""
    if not building_number or not building_number.strip():
        raise ValidationError("Номер корпуса обязателен")
    return True


def validate_address(address):
    """Валидация адреса"""
    if not address or not address.strip():
        raise ValidationError("Адрес обязателен")
    if len(address.strip()) < 5:
        raise ValidationError("Адрес должен содержать минимум 5 символов")
    return True


def validate_floors_count(floors_count):
    """Валидация количества этажей"""
    if not isinstance(floors_count, int) or floors_count < 1:
        raise ValidationError("Количество этажей должно быть положительным числом")
    if floors_count > 100:
        raise ValidationError("Количество этажей не может превышать 100")
    return True


def validate_room_number(room_number):
    """Валидация номера комнаты"""
    if not room_number or not room_number.strip():
        raise ValidationError("Номер комнаты обязателен")
    return True


def validate_capacity(capacity):
    """Валидация вместимости комнаты"""
    if not isinstance(capacity, int) or capacity < 1:
        raise ValidationError("Вместимость должна быть положительным числом")
    if capacity > 20:
        raise ValidationError("Вместимость не может превышать 20 человек")
    return True


def validate_area(area):
    """Валидация площади комнаты (опциональное поле)"""
    if area is None:
        return True
    if isinstance(area, (int, float)) and area < 0:
        raise ValidationError("Площадь не может быть отрицательной")
    if isinstance(area, (int, float)) and area > 1000:
        raise ValidationError("Площадь не может превышать 1000 м²")
    return True


def validate_gender(gender):
    """Валидация пола"""
    if gender not in ['М', 'Ж']:
        raise ValidationError("Пол должен быть 'М' или 'Ж'")
    return True

