import sqlite3
import os
from pathlib import Path
from app.utils.logger import setup_logger

logger = setup_logger('database')


class Database:
    def __init__(self, db_name='dormitory.db'):
        # Сохраняем БД в корне проекта
        project_root = Path(__file__).parent.parent
        self.db_path = project_root / db_name
        self.db_name = str(self.db_path)
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Таблица студентов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                surname TEXT NOT NULL,
                name TEXT NOT NULL,
                patronymic TEXT,
                gender TEXT NOT NULL CHECK(gender IN ('М', 'Ж')),
                phone TEXT NOT NULL,
                email TEXT,
                group_number TEXT NOT NULL
            )
        ''')
        
        # Таблица комендантов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commandants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                surname TEXT NOT NULL,
                name TEXT NOT NULL,
                patronymic TEXT,
                phone TEXT NOT NULL
            )
        ''')
        
        # Таблица корпусов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS buildings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                building_number TEXT NOT NULL UNIQUE,
                address TEXT NOT NULL,
                floors_count INTEGER NOT NULL CHECK(floors_count > 0)
            )
        ''')
        
        # Таблица комнат
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                building_id INTEGER NOT NULL,
                floor INTEGER NOT NULL CHECK(floor > 0),
                room_number TEXT NOT NULL,
                capacity INTEGER NOT NULL CHECK(capacity > 0),
                area REAL CHECK(area >= 0),
                FOREIGN KEY (building_id) REFERENCES buildings(id) ON DELETE RESTRICT,
                UNIQUE(building_id, floor, room_number)
            )
        ''')
        
        # Таблица заселений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                commandant_id INTEGER NOT NULL,
                room_id INTEGER NOT NULL,
                checkin_date TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE RESTRICT,
                FOREIGN KEY (commandant_id) REFERENCES commandants(id) ON DELETE RESTRICT,
                FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE RESTRICT
            )
        ''')
        
        # Таблица выселений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                checkin_id INTEGER NOT NULL UNIQUE,
                commandant_id INTEGER NOT NULL,
                checkout_date TEXT NOT NULL,
                FOREIGN KEY (checkin_id) REFERENCES checkins(id) ON DELETE RESTRICT,
                FOREIGN KEY (commandant_id) REFERENCES commandants(id) ON DELETE RESTRICT
            )
        ''')
        
        # Создание индексов для оптимизации
        self._create_indexes(conn)
        
        conn.commit()
        conn.close()
        logger.info("База данных инициализирована")
    
    def _create_indexes(self, conn):
        """Создание индексов для оптимизации запросов"""
        cursor = conn.cursor()
        
        # Индексы для студентов
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_surname ON students(surname)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_group ON students(group_number)')
        
        # Индексы для заселений
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_checkins_student ON checkins(student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_checkins_room ON checkins(room_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_checkins_date ON checkins(checkin_date)')
        
        # Индексы для выселений
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_checkouts_checkin ON checkouts(checkin_id)')
        
        # Индексы для комнат
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_rooms_building ON rooms(building_id)')
        
        logger.info("Индексы созданы")

