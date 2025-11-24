"""
Простой кэш для часто используемых данных
"""
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
from app.utils.logger import setup_logger

logger = setup_logger('cache')


class CacheItem:
    """Элемент кэша с временем жизни"""
    
    def __init__(self, value: Any, ttl: int = 300):
        self.value = value
        self.created_at = datetime.now()
        self.ttl = timedelta(seconds=ttl)
    
    def is_expired(self) -> bool:
        """Проверить, истек ли срок действия"""
        return datetime.now() - self.created_at > self.ttl


class SimpleCache:
    """Простой in-memory кэш"""
    
    def __init__(self):
        self._cache: Dict[str, CacheItem] = {}
        self.logger = setup_logger('cache')
    
    def get(self, key: str) -> Optional[Any]:
        """Получить значение из кэша"""
        if key in self._cache:
            item = self._cache[key]
            if not item.is_expired():
                self.logger.debug(f"Cache hit: {key}")
                return item.value
            else:
                # Удалить истекший элемент
                del self._cache[key]
                self.logger.debug(f"Cache expired: {key}")
        
        self.logger.debug(f"Cache miss: {key}")
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300):
        """Установить значение в кэш"""
        self._cache[key] = CacheItem(value, ttl)
        self.logger.debug(f"Cache set: {key}")
    
    def delete(self, key: str):
        """Удалить значение из кэша"""
        if key in self._cache:
            del self._cache[key]
            self.logger.debug(f"Cache deleted: {key}")
    
    def clear(self):
        """Очистить весь кэш"""
        self._cache.clear()
        self.logger.info("Cache cleared")
    
    def cleanup_expired(self):
        """Очистить истекшие элементы"""
        expired_keys = [
            key for key, item in self._cache.items()
            if item.is_expired()
        ]
        for key in expired_keys:
            del self._cache[key]
        
        if expired_keys:
            self.logger.debug(f"Cleaned up {len(expired_keys)} expired cache items")


# Глобальный экземпляр кэша
cache = SimpleCache()

