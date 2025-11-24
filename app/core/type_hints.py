"""
Type hints для типизации
"""
from typing import TypedDict, Optional, List, Tuple, Dict, Any
from datetime import datetime


class StudentDict(TypedDict, total=False):
    """Тип для данных студента"""
    id: int
    surname: str
    name: str
    patronymic: Optional[str]
    gender: str
    phone: str
    email: Optional[str]
    group_number: str


class CommandantDict(TypedDict, total=False):
    """Тип для данных коменданта"""
    id: int
    surname: str
    name: str
    patronymic: Optional[str]
    phone: str


class BuildingDict(TypedDict, total=False):
    """Тип для данных корпуса"""
    id: int
    building_number: str
    address: str
    floors_count: int


class RoomDict(TypedDict, total=False):
    """Тип для данных комнаты"""
    id: int
    building_id: int
    floor: int
    room_number: str
    capacity: int
    area: Optional[float]


class CheckinDict(TypedDict, total=False):
    """Тип для данных заселения"""
    id: int
    student_id: int
    commandant_id: int
    room_id: int
    checkin_date: str


class CheckoutDict(TypedDict, total=False):
    """Тип для данных выселения"""
    id: int
    checkin_id: int
    commandant_id: int
    checkout_date: str

