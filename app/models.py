import sqlite3
from app.database import Database
from app.utils.validators import (
    validate_name, validate_phone, validate_email, validate_group_number,
    validate_gender, validate_building_number, validate_address,
    validate_floors_count, validate_room_number, validate_capacity,
    validate_area, ValidationError
)
from app.utils.logger import setup_logger

logger = setup_logger('models')


class StudentModel:
    def __init__(self):
        self.db = Database()
    
    def create(self, surname, name, patronymic, gender, phone, email, group_number):
        # Валидация
        validate_name(surname, "Фамилия")
        validate_name(name, "Имя")
        if patronymic:
            validate_name(patronymic, "Отчество")
        validate_gender(gender)
        validate_phone(phone)
        if email:
            validate_email(email)
        validate_group_number(group_number)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO students (surname, name, patronymic, gender, phone, email, group_number)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (surname.strip(), name.strip(), patronymic.strip() if patronymic else None, 
                  gender, phone.strip(), email.strip() if email else None, group_number.strip()))
            conn.commit()
            student_id = cursor.lastrowid
            logger.info(f"Создан студент ID: {student_id}")
            return student_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Ошибка создания студента: {e}")
            raise
        finally:
            conn.close()
    
    def get_all(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY surname, name')
        students = cursor.fetchall()
        conn.close()
        return students
    
    def get_by_id(self, student_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()
        return student
    
    def update(self, student_id, surname, name, patronymic, gender, phone, email, group_number):
        # Валидация
        validate_name(surname, "Фамилия")
        validate_name(name, "Имя")
        if patronymic:
            validate_name(patronymic, "Отчество")
        validate_gender(gender)
        validate_phone(phone)
        if email:
            validate_email(email)
        validate_group_number(group_number)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE students 
                SET surname=?, name=?, patronymic=?, gender=?, phone=?, email=?, group_number=?
                WHERE id=?
            ''', (surname.strip(), name.strip(), patronymic.strip() if patronymic else None,
                  gender, phone.strip(), email.strip() if email else None, group_number.strip(), student_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def delete(self, student_id):
        # Проверка, проживал ли студент в общежитии
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM checkins WHERE student_id = ?', (student_id,))
        count = cursor.fetchone()[0]
        conn.close()
        
        if count > 0:
            raise ValueError("Нельзя удалить студента, который проживал в общежитии")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def has_checkins(self, student_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM checkins WHERE student_id = ?', (student_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0


class CommandantModel:
    def __init__(self):
        self.db = Database()
    
    def create(self, surname, name, patronymic, phone):
        # Валидация
        validate_name(surname, "Фамилия")
        validate_name(name, "Имя")
        if patronymic:
            validate_name(patronymic, "Отчество")
        validate_phone(phone)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO commandants (surname, name, patronymic, phone)
                VALUES (?, ?, ?, ?)
            ''', (surname.strip(), name.strip(), patronymic.strip() if patronymic else None, phone.strip()))
            conn.commit()
            commandant_id = cursor.lastrowid
            return commandant_id
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_all(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM commandants ORDER BY surname, name')
        commandants = cursor.fetchall()
        conn.close()
        return commandants
    
    def get_by_id(self, commandant_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM commandants WHERE id = ?', (commandant_id,))
        commandant = cursor.fetchone()
        conn.close()
        return commandant
    
    def update(self, commandant_id, surname, name, patronymic, phone):
        # Валидация
        validate_name(surname, "Фамилия")
        validate_name(name, "Имя")
        if patronymic:
            validate_name(patronymic, "Отчество")
        validate_phone(phone)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE commandants 
                SET surname=?, name=?, patronymic=?, phone=?
                WHERE id=?
            ''', (surname.strip(), name.strip(), patronymic.strip() if patronymic else None, 
                  phone.strip(), commandant_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def delete(self, commandant_id):
        # Проверка, участвовал ли комендант в заселении/выселении
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM checkins WHERE commandant_id = ?', (commandant_id,))
        checkins_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM checkouts WHERE commandant_id = ?', (commandant_id,))
        checkouts_count = cursor.fetchone()[0]
        conn.close()
        
        if checkins_count > 0 or checkouts_count > 0:
            raise ValueError("Нельзя удалить коменданта, который участвовал в оформлении заселения или выселения")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM commandants WHERE id = ?', (commandant_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()


class BuildingModel:
    def __init__(self):
        self.db = Database()
    
    def create(self, building_number, address, floors_count):
        # Валидация
        validate_building_number(building_number)
        validate_address(address)
        validate_floors_count(floors_count)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO buildings (building_number, address, floors_count)
                VALUES (?, ?, ?)
            ''', (building_number.strip(), address.strip(), floors_count))
            conn.commit()
            building_id = cursor.lastrowid
            return building_id
        except sqlite3.IntegrityError:
            conn.rollback()
            raise ValueError("Корпус с таким номером уже существует")
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_all(self, address_filter=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        if address_filter:
            cursor.execute('''
                SELECT * FROM buildings 
                WHERE address LIKE ?
                ORDER BY building_number
            ''', (f'%{address_filter}%',))
        else:
            cursor.execute('SELECT * FROM buildings ORDER BY building_number')
        buildings = cursor.fetchall()
        conn.close()
        return buildings
    
    def get_by_id(self, building_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM buildings WHERE id = ?', (building_id,))
        building = cursor.fetchone()
        conn.close()
        return building
    
    def update(self, building_id, building_number, address, floors_count):
        # Валидация
        validate_building_number(building_number)
        validate_address(address)
        validate_floors_count(floors_count)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE buildings 
                SET building_number=?, address=?, floors_count=?
                WHERE id=?
            ''', (building_number.strip(), address.strip(), floors_count, building_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def delete(self, building_id):
        # Проверка, есть ли связанные комнаты
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM rooms WHERE building_id = ?', (building_id,))
        count = cursor.fetchone()[0]
        conn.close()
        
        if count > 0:
            raise ValueError("Нельзя удалить корпус, с которым связаны комнаты")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM buildings WHERE id = ?', (building_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def has_rooms(self, building_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM rooms WHERE building_id = ?', (building_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0


class RoomModel:
    def __init__(self):
        self.db = Database()
    
    def create(self, building_id, floor, room_number, capacity, area=None):
        # Валидация
        validate_room_number(room_number)
        validate_capacity(capacity)
        if area is not None:
            validate_area(area)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO rooms (building_id, floor, room_number, capacity, area)
                VALUES (?, ?, ?, ?, ?)
            ''', (building_id, floor, room_number.strip(), capacity, area))
            conn.commit()
            room_id = cursor.lastrowid
            return room_id
        except sqlite3.IntegrityError:
            conn.rollback()
            raise ValueError("Комната с таким номером уже существует в этом корпусе на этом этаже")
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_all(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, b.building_number, b.address 
            FROM rooms r
            JOIN buildings b ON r.building_id = b.id
            ORDER BY b.building_number, r.floor, r.room_number
        ''')
        rooms = cursor.fetchall()
        conn.close()
        return rooms
    
    def get_by_id(self, room_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, b.building_number, b.address 
            FROM rooms r
            JOIN buildings b ON r.building_id = b.id
            WHERE r.id = ?
        ''', (room_id,))
        room = cursor.fetchone()
        conn.close()
        return room
    
    def update(self, room_id, building_id, floor, room_number, capacity, area=None):
        # Валидация
        validate_room_number(room_number)
        validate_capacity(capacity)
        if area is not None:
            validate_area(area)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE rooms 
                SET building_id=?, floor=?, room_number=?, capacity=?, area=?
                WHERE id=?
            ''', (building_id, floor, room_number.strip(), capacity, area, room_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def delete(self, room_id):
        # Проверка, проживали ли студенты в комнате
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM checkins WHERE room_id = ?', (room_id,))
        count = cursor.fetchone()[0]
        conn.close()
        
        if count > 0:
            raise ValueError("Нельзя удалить комнату, в которой проживали студенты")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM rooms WHERE id = ?', (room_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_current_occupancy(self, room_id):
        """Получить текущее количество заселенных студентов в комнате"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM checkins c
            LEFT JOIN checkouts co ON c.id = co.checkin_id
            WHERE c.room_id = ? AND co.id IS NULL
        ''', (room_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_room_gender(self, room_id):
        """Получить пол студентов в комнате (если все одного пола)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT s.gender FROM checkins c
            JOIN students s ON c.student_id = s.id
            LEFT JOIN checkouts co ON c.id = co.checkin_id
            WHERE c.room_id = ? AND co.id IS NULL
        ''', (room_id,))
        genders = [row[0] for row in cursor.fetchall()]
        conn.close()
        if len(genders) == 1:
            return genders[0]
        elif len(genders) == 0:
            return None
        else:
            return 'MIXED'  # Разные полы (не должно быть, но на всякий случай)


class CheckinModel:
    def __init__(self):
        self.db = Database()
    
    def create(self, student_id, commandant_id, room_id, checkin_date):
        # Проверка вместимости
        room_model = RoomModel()
        occupancy = room_model.get_current_occupancy(room_id)
        room = room_model.get_by_id(room_id)
        if not room:
            raise ValueError("Комната не найдена")
        capacity = room[4]  # capacity находится в индексе 4
        
        if occupancy >= capacity:
            raise ValueError(f"Комната заполнена. Текущее количество: {occupancy}/{capacity}")
        
        # Проверка пола
        student_model = StudentModel()
        student = student_model.get_by_id(student_id)
        if not student:
            raise ValueError("Студент не найден")
        student_gender = student[4]  # gender находится в индексе 4
        
        room_gender = room_model.get_room_gender(room_id)
        if room_gender and room_gender != 'MIXED' and room_gender != student_gender:
            raise ValueError(f"Пол заселяемого студента ({student_gender}) не соответствует полу уже заселенных студентов ({room_gender})")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO checkins (student_id, commandant_id, room_id, checkin_date)
                VALUES (?, ?, ?, ?)
            ''', (student_id, commandant_id, room_id, checkin_date))
            conn.commit()
            checkin_id = cursor.lastrowid
            return checkin_id
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_all(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, 
                   s.surname || ' ' || s.name || ' ' || COALESCE(s.patronymic, '') as student_name,
                   cmd.surname || ' ' || cmd.name || ' ' || COALESCE(cmd.patronymic, '') as commandant_name,
                   r.room_number, r.floor, b.building_number, b.address
            FROM checkins c
            JOIN students s ON c.student_id = s.id
            JOIN commandants cmd ON c.commandant_id = cmd.id
            JOIN rooms r ON c.room_id = r.id
            JOIN buildings b ON r.building_id = b.id
            ORDER BY c.checkin_date DESC
        ''')
        checkins = cursor.fetchall()
        conn.close()
        return checkins
    
    def get_active_checkins(self):
        """Получить активные заселения (без выселения)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, 
                   s.surname || ' ' || s.name || ' ' || COALESCE(s.patronymic, '') as student_name,
                   r.room_number, r.floor, b.building_number, b.address
            FROM checkins c
            JOIN students s ON c.student_id = s.id
            JOIN rooms r ON c.room_id = r.id
            JOIN buildings b ON r.building_id = b.id
            LEFT JOIN checkouts co ON c.id = co.checkin_id
            WHERE co.id IS NULL
            ORDER BY c.checkin_date DESC
        ''')
        checkins = cursor.fetchall()
        conn.close()
        return checkins


class CheckoutModel:
    def __init__(self):
        self.db = Database()
    
    def create(self, checkin_id, commandant_id, checkout_date):
        # Проверка, что заселение существует и еще не выселено
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM checkouts WHERE checkin_id = ?', (checkin_id,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            raise ValueError("Это заселение уже было выселено")
        conn.close()
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO checkouts (checkin_id, commandant_id, checkout_date)
                VALUES (?, ?, ?)
            ''', (checkin_id, commandant_id, checkout_date))
            conn.commit()
            checkout_id = cursor.lastrowid
            return checkout_id
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_all(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT co.*, 
                   s.surname || ' ' || s.name || ' ' || COALESCE(s.patronymic, '') as student_name,
                   cmd.surname || ' ' || cmd.name || ' ' || COALESCE(cmd.patronymic, '') as commandant_name,
                   r.room_number, r.floor, b.building_number, b.address
            FROM checkouts co
            JOIN checkins c ON co.checkin_id = c.id
            JOIN students s ON c.student_id = s.id
            JOIN commandants cmd ON co.commandant_id = cmd.id
            JOIN rooms r ON c.room_id = r.id
            JOIN buildings b ON r.building_id = b.id
            ORDER BY co.checkout_date DESC
        ''')
        checkouts = cursor.fetchall()
        conn.close()
        return checkouts

