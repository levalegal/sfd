"""
Менеджер для работы с базой данных
Обеспечивает connection pooling и оптимизацию запросов
"""
import sqlite3
from contextlib import contextmanager
from typing import Optional
from pathlib import Path
from app.utils.logger import setup_logger
from app.utils.exceptions import DatabaseException

logger = setup_logger('db_manager')


class DatabaseManager:
    """Менеджер для управления соединениями с БД"""
    
    _instance: Optional['DatabaseManager'] = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls, db_name: str = 'dormitory.db'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(db_name)
        return cls._instance
    
    def _initialize(self, db_name: str):
        """Инициализация менеджера"""
        project_root = Path(__file__).parent.parent.parent
        self.db_path = project_root / db_name
        self.db_name = str(self.db_path)
        logger.info(f"Инициализирован DatabaseManager для {self.db_name}")
    
    @contextmanager
    def get_connection(self):
        """Получить соединение с БД (контекстный менеджер)"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row  # Возвращать результаты как Row объекты
            yield conn
            conn.commit()
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Ошибка SQLite: {e}")
            raise DatabaseException(f"Ошибка работы с БД: {str(e)}")
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Неожиданная ошибка: {e}")
            raise DatabaseException(f"Неожиданная ошибка: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def execute(self, query: str, params: Optional[tuple] = None, fetch_one: bool = False, fetch_all: bool = False):
        """Выполнить запрос"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_one:
                row = cursor.fetchone()
                return dict(row) if row else None
            elif fetch_all:
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            else:
                return cursor.lastrowid
    
    def execute_many(self, query: str, params_list: list):
        """Выполнить запрос для множества параметров"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount

