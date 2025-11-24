"""
Базовый класс для всех моделей
Реализует общую логику CRUD операций
"""
from typing import Optional, List, Tuple, Any
from contextlib import contextmanager
from app.database import Database
from app.utils.logger import setup_logger
from app.utils.exceptions import DatabaseException

logger = setup_logger('base_model')


@contextmanager
def db_connection(db: Database):
    """Контекстный менеджер для работы с БД"""
    conn = None
    try:
        conn = db.get_connection()
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Ошибка работы с БД: {e}")
        raise DatabaseException(f"Ошибка работы с БД: {str(e)}")
    finally:
        if conn:
            conn.close()


class BaseModel:
    """Базовый класс для всех моделей"""
    
    def __init__(self, table_name: str):
        self.db = Database()
        self.table_name = table_name
        self.logger = setup_logger(f'model_{table_name}')
    
    @contextmanager
    def _get_connection(self):
        """Получить соединение с БД через контекстный менеджер"""
        conn = None
        try:
            conn = self.db.get_connection()
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Ошибка работы с БД: {e}")
            raise DatabaseException(f"Ошибка работы с БД: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: Optional[Tuple] = None, fetch_one: bool = False, fetch_all: bool = True) -> Any:
        """Выполнить SQL запрос"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                return cursor.lastrowid
    
    def get_by_id(self, record_id: int) -> Optional[Tuple]:
        """Получить запись по ID"""
        query = f'SELECT * FROM {self.table_name} WHERE id = ?'
        return self.execute_query(query, (record_id,), fetch_one=True, fetch_all=False)
    
    def get_all(self, order_by: Optional[str] = None) -> List[Tuple]:
        """Получить все записи"""
        query = f'SELECT * FROM {self.table_name}'
        if order_by:
            query += f' ORDER BY {order_by}'
        return self.execute_query(query)
    
    def count(self, where_clause: Optional[str] = None, params: Optional[Tuple] = None) -> int:
        """Подсчитать количество записей"""
        query = f'SELECT COUNT(*) FROM {self.table_name}'
        if where_clause:
            query += f' WHERE {where_clause}'
        
        result = self.execute_query(query, params, fetch_one=True, fetch_all=False)
        return result[0] if result else 0
    
    def exists(self, where_clause: str, params: Tuple) -> bool:
        """Проверить существование записи"""
        return self.count(where_clause, params) > 0
    
    def delete_by_id(self, record_id: int) -> bool:
        """Удалить запись по ID"""
        query = f'DELETE FROM {self.table_name} WHERE id = ?'
        try:
            self.execute_query(query, (record_id,), fetch_one=False, fetch_all=False)
            self.logger.info(f"Удалена запись ID: {record_id} из {self.table_name}")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка удаления записи ID {record_id}: {e}")
            raise

