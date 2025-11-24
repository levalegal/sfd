"""
Модуль статистики
"""
from app.models import StudentModel, RoomModel, CheckinModel, BuildingModel
from app.utils.logger import setup_logger

logger = setup_logger('statistics')


class Statistics:
    """Класс для получения статистики"""
    
    def __init__(self):
        self.student_model = StudentModel()
        self.room_model = RoomModel()
        self.checkin_model = CheckinModel()
        self.building_model = BuildingModel()
    
    def get_total_students(self):
        """Общее количество студентов"""
        return len(self.student_model.get_all())
    
    def get_total_rooms(self):
        """Общее количество комнат"""
        return len(self.room_model.get_all())
    
    def get_total_buildings(self):
        """Общее количество корпусов"""
        return len(self.building_model.get_all())
    
    def get_occupied_rooms(self):
        """Количество занятых комнат"""
        rooms = self.room_model.get_all()
        occupied = 0
        for room in rooms:
            occupancy = self.room_model.get_current_occupancy(room[0])
            if occupancy > 0:
                occupied += 1
        return occupied
    
    def get_total_checkins(self):
        """Общее количество заселений"""
        return len(self.checkin_model.get_all())
    
    def get_active_checkins(self):
        """Количество активных заселений"""
        return len(self.checkin_model.get_active_checkins())
    
    def get_occupancy_rate(self):
        """Процент заселенности"""
        rooms = self.room_model.get_all()
        if not rooms:
            return 0.0
        
        total_capacity = sum(room[4] for room in rooms)  # capacity
        total_occupied = 0
        
        for room in rooms:
            total_occupied += self.room_model.get_current_occupancy(room[0])
        
        if total_capacity == 0:
            return 0.0
        
        return round((total_occupied / total_capacity) * 100, 2)
    
    def get_gender_distribution(self):
        """Распределение по полу"""
        students = self.student_model.get_all()
        male = sum(1 for s in students if s[4] == 'М')
        female = sum(1 for s in students if s[4] == 'Ж')
        return {'М': male, 'Ж': female, 'Всего': len(students)}
    
    def get_all_statistics(self):
        """Получить всю статистику"""
        try:
            return {
                'total_students': self.get_total_students(),
                'total_rooms': self.get_total_rooms(),
                'total_buildings': self.get_total_buildings(),
                'occupied_rooms': self.get_occupied_rooms(),
                'total_checkins': self.get_total_checkins(),
                'active_checkins': self.get_active_checkins(),
                'occupancy_rate': self.get_occupancy_rate(),
                'gender_distribution': self.get_gender_distribution()
            }
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {}

