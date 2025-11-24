"""
Тестирование методом белого ящика
Тестирование с знанием внутренней реализации
"""
import unittest
import os
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import StudentModel, RoomModel, CheckinModel
from app.database import Database
from app.utils.validators import (
    validate_name, validate_phone, validate_email, validate_gender,
    ValidationError
)


class WhiteBoxTestValidators(unittest.TestCase):
    """Тесты валидаторов (белый ящик)"""
    
    def test_validate_name_valid(self):
        """Тест валидации имени - валидные данные"""
        self.assertTrue(validate_name('Иван', 'Имя'))
        self.assertTrue(validate_name('Иванов', 'Фамилия'))
    
    def test_validate_name_empty(self):
        """Тест валидации имени - пустое значение"""
        with self.assertRaises(ValidationError):
            validate_name('', 'Имя')
        with self.assertRaises(ValidationError):
            validate_name(None, 'Имя')
    
    def test_validate_name_short(self):
        """Тест валидации имени - слишком короткое"""
        with self.assertRaises(ValidationError):
            validate_name('А', 'Имя')
    
    def test_validate_name_invalid_chars(self):
        """Тест валидации имени - недопустимые символы"""
        with self.assertRaises(ValidationError):
            validate_name('Иван123', 'Имя')
        with self.assertRaises(ValidationError):
            validate_name('Иван@', 'Имя')
    
    def test_validate_phone_valid(self):
        """Тест валидации телефона - валидные данные"""
        self.assertTrue(validate_phone('+79001234567'))
        self.assertTrue(validate_phone('89001234567'))
        self.assertTrue(validate_phone('8 (900) 123-45-67'))
    
    def test_validate_phone_empty(self):
        """Тест валидации телефона - пустое значение"""
        with self.assertRaises(ValidationError):
            validate_phone('')
    
    def test_validate_phone_short(self):
        """Тест валидации телефона - слишком короткий"""
        with self.assertRaises(ValidationError):
            validate_phone('12345')
    
    def test_validate_email_valid(self):
        """Тест валидации email - валидные данные"""
        self.assertTrue(validate_email('test@mail.ru'))
        self.assertTrue(validate_email('user.name@example.com'))
    
    def test_validate_email_invalid(self):
        """Тест валидации email - невалидные данные"""
        with self.assertRaises(ValidationError):
            validate_email('invalid-email')
        with self.assertRaises(ValidationError):
            validate_email('test@')
    
    def test_validate_email_empty(self):
        """Тест валидации email - пустое значение (допустимо)"""
        self.assertTrue(validate_email(''))
        self.assertTrue(validate_email(None))
    
    def test_validate_gender_valid(self):
        """Тест валидации пола - валидные данные"""
        self.assertTrue(validate_gender('М'))
        self.assertTrue(validate_gender('Ж'))
    
    def test_validate_gender_invalid(self):
        """Тест валидации пола - невалидные данные"""
        with self.assertRaises(ValidationError):
            validate_gender('X')
        with self.assertRaises(ValidationError):
            validate_gender('Male')


class WhiteBoxTestRoomOccupancy(unittest.TestCase):
    """Тесты внутренней логики заселения (белый ящик)"""
    
    def setUp(self):
        """Создание тестовых данных"""
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
        
        from app.models import StudentModel, CommandantModel, BuildingModel, RoomModel
        
        self.student_model = StudentModel()
        self.commandant_model = CommandantModel()
        self.building_model = BuildingModel()
        self.room_model = RoomModel()
        self.checkin_model = CheckinModel()
        
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
    
    def test_get_current_occupancy_empty(self):
        """Тест получения текущей заселенности - пустая комната"""
        occupancy = self.room_model.get_current_occupancy(self.room_id)
        self.assertEqual(occupancy, 0)
    
    def test_get_current_occupancy_one(self):
        """Тест получения текущей заселенности - один студент"""
        self.checkin_model.create(
            self.student_id, self.commandant_id, self.room_id, '2024-01-01'
        )
        occupancy = self.room_model.get_current_occupancy(self.room_id)
        self.assertEqual(occupancy, 1)
    
    def test_get_room_gender_empty(self):
        """Тест получения пола в комнате - пустая комната"""
        gender = self.room_model.get_room_gender(self.room_id)
        self.assertIsNone(gender)
    
    def test_get_room_gender_male(self):
        """Тест получения пола в комнате - мужская комната"""
        self.checkin_model.create(
            self.student_id, self.commandant_id, self.room_id, '2024-01-01'
        )
        gender = self.room_model.get_room_gender(self.room_id)
        self.assertEqual(gender, 'М')
    
    def test_get_room_gender_after_checkout(self):
        """Тест получения пола после выселения"""
        checkin_id = self.checkin_model.create(
            self.student_id, self.commandant_id, self.room_id, '2024-01-01'
        )
        
        from app.models import CheckoutModel
        checkout_model = CheckoutModel()
        checkout_model.create(checkin_id, self.commandant_id, '2024-01-02')
        
        gender = self.room_model.get_room_gender(self.room_id)
        self.assertIsNone(gender)  # Комната пуста после выселения


if __name__ == '__main__':
    unittest.main()

