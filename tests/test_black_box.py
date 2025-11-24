"""
Тестирование методом черного ящика
Тестирование функциональности без знания внутренней реализации
"""
import unittest
import os
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import StudentModel, CommandantModel, BuildingModel, RoomModel, CheckinModel, CheckoutModel
from app.database import Database


class BlackBoxTestStudent(unittest.TestCase):
    """Тесты для студентов (черный ящик)"""
    
    def setUp(self):
        """Создание тестовой БД"""
        self.test_db = 'test_dormitory.db'
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        # Монkey-patch для использования тестовой БД
        import app.database
        original_init = Database.__init__
        def test_init(self, db_name='test_dormitory.db'):
            from pathlib import Path
            project_root = Path(__file__).parent.parent
            self.db_path = project_root / db_name
            self.db_name = str(self.db_path)
            self.init_database()
        Database.__init__ = test_init
        
        self.model = StudentModel()
    
    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_create_student_valid(self):
        """Тест создания студента с валидными данными"""
        student_id = self.model.create(
            'Иванов', 'Иван', 'Иванович', 'М', 
            '+79001234567', 'ivan@mail.ru', 'ИВТ-21'
        )
        self.assertIsNotNone(student_id)
        self.assertGreater(student_id, 0)
    
    def test_create_student_without_patronymic(self):
        """Тест создания студента без отчества"""
        student_id = self.model.create(
            'Петров', 'Петр', None, 'М',
            '+79001234568', None, 'ИВТ-21'
        )
        self.assertIsNotNone(student_id)
    
    def test_create_student_invalid_gender(self):
        """Тест создания студента с невалидным полом"""
        with self.assertRaises(Exception):
            self.model.create(
                'Сидоров', 'Сидор', None, 'X',
                '+79001234569', None, 'ИВТ-21'
            )
    
    def test_get_student_by_id(self):
        """Тест получения студента по ID"""
        student_id = self.model.create(
            'Иванов', 'Иван', 'Иванович', 'М',
            '+79001234567', 'ivan@mail.ru', 'ИВТ-21'
        )
        student = self.model.get_by_id(student_id)
        self.assertIsNotNone(student)
        self.assertEqual(student[1], 'Иванов')
    
    def test_update_student(self):
        """Тест обновления данных студента"""
        student_id = self.model.create(
            'Иванов', 'Иван', 'Иванович', 'М',
            '+79001234567', 'ivan@mail.ru', 'ИВТ-21'
        )
        self.model.update(
            student_id, 'Иванов', 'Иван', 'Петрович', 'М',
            '+79001234567', 'ivan@mail.ru', 'ИВТ-21'
        )
        student = self.model.get_by_id(student_id)
        self.assertEqual(student[3], 'Петрович')
    
    def test_delete_student_without_checkin(self):
        """Тест удаления студента без заселений"""
        student_id = self.model.create(
            'Иванов', 'Иван', 'Иванович', 'М',
            '+79001234567', 'ivan@mail.ru', 'ИВТ-21'
        )
        self.model.delete(student_id)
        student = self.model.get_by_id(student_id)
        self.assertIsNone(student)


class BlackBoxTestCheckin(unittest.TestCase):
    """Тесты для заселения (черный ящик)"""
    
    def setUp(self):
        """Создание тестовых данных"""
        self.test_db = 'test_dormitory.db'
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        
        self.student_model = StudentModel()
        self.commandant_model = CommandantModel()
        self.building_model = BuildingModel()
        self.room_model = RoomModel()
        self.checkin_model = CheckinModel()
        
        # Создаем тестовые данные
        self.student_id = self.student_model.create(
            'Иванов', 'Иван', 'Иванович', 'М',
            '+79001234567', 'ivan@mail.ru', 'ИВТ-21'
        )
        self.commandant_id = self.commandant_model.create(
            'Петров', 'Петр', 'Петрович', '+79001234568'
        )
        self.building_id = self.building_model.create(
            '1', 'ул. Ленина, 1', 5
        )
        self.room_id = self.room_model.create(
            self.building_id, 1, '101', 2, 20.5
        )
    
    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_checkin_valid(self):
        """Тест валидного заселения"""
        checkin_id = self.checkin_model.create(
            self.student_id, self.commandant_id, self.room_id, '2024-01-01'
        )
        self.assertIsNotNone(checkin_id)
    
    def test_checkin_room_full(self):
        """Тест заселения в заполненную комнату"""
        # Заселяем первого студента
        self.checkin_model.create(
            self.student_id, self.commandant_id, self.room_id, '2024-01-01'
        )
        
        # Создаем второго студента
        student2_id = self.student_model.create(
            'Петров', 'Петр', 'Петрович', 'М',
            '+79001234569', 'petr@mail.ru', 'ИВТ-21'
        )
        
        # Заселяем второго (комната вмещает 2)
        self.checkin_model.create(
            student2_id, self.commandant_id, self.room_id, '2024-01-02'
        )
        
        # Пытаемся заселить третьего (комната заполнена)
        student3_id = self.student_model.create(
            'Сидоров', 'Сидор', 'Сидорович', 'М',
            '+79001234570', 'sidor@mail.ru', 'ИВТ-21'
        )
        
        with self.assertRaises(ValueError):
            self.checkin_model.create(
                student3_id, self.commandant_id, self.room_id, '2024-01-03'
            )
    
    def test_checkin_gender_mismatch(self):
        """Тест заселения с несоответствием пола"""
        # Заселяем студента-мужчину
        self.checkin_model.create(
            self.student_id, self.commandant_id, self.room_id, '2024-01-01'
        )
        
        # Пытаемся заселить студентку-женщину
        student_female_id = self.student_model.create(
            'Иванова', 'Мария', 'Ивановна', 'Ж',
            '+79001234571', 'maria@mail.ru', 'ИВТ-21'
        )
        
        with self.assertRaises(ValueError):
            self.checkin_model.create(
                student_female_id, self.commandant_id, self.room_id, '2024-01-02'
            )


if __name__ == '__main__':
    unittest.main()

