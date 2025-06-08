import json
from typing import Any, Optional

from common.cache.connection import redis_connections
from django.conf import settings
from django.db.models.base import ModelBase


class CacheManagement:
    """ """

    default_ttl = settings.REDIS_CACHE_LONG_TTL

    def __init__(self, *, db: int = 0):
        self.db = redis_connections.con_db(db)

    def pipeline(self):
        return self.db.pipeline()

    def set_expire(self, key: str, ttl: int) -> bool:
        return self.db.expire(key, ttl)

    def is_exists(self, key):
        """
        Check if the key exists in the cache or not
        """
        return bool(self.db.exists(key))

    def set_key(self, key: str, value: Any, ttl: Optional[int] = default_ttl) -> bool:
        """
        Set the key:value data as a string in Redis and provide a custom TTL value
        if one is specified. If no TTL value is provided, set it to 'None'."
        """
        value = json.dumps(value)
        result = self.db.set(key, str(value))
        self.set_expire(key, ttl) if ttl else None  # type: ignore
        return result

    def setnx_key(self, key: str, value: Any, ttl: Optional[int] = default_ttl) -> bool:
        """
        Set the key:value data as a string in Redis and provide a custom TTL value
        if one is specified. If no TTL value is provided, set it to 'None'."
        """
        value = json.dumps(value)
        result = self.db.setnx(key, value)
        self.set_expire(key, ttl) if ttl else None  # type: ignore
        return result

    def get_key(self, key: str) -> bytes | None:
        """
        Return data of a key
        """
        data = self.db.get(key)
        return json.loads(data) if data else {}

    def incr_key(self, key: str, value: int = 1) -> int:
        """
        Increase value of a key by given number
        """
        return self.db.incr(key, value)

    def get_all_keys(self) -> list:
        """
        Return list of all keys that stored in specific database
        """
        return self.db.keys()

    def remove_key(self, key: str | ModelBase) -> int:
        """
        Delete a key from cache (it can be str or django model class)
        """
        key = f'{key.__name__}:all' if isinstance(key, ModelBase) else key
        return self.db.delete(key)

    def remove_pattern_key(self, pattern: str) -> None:
        """
        Delete keys from cache follow with a pattern
        """
        keys = self.db.keys(pattern)

        for key in keys:
            self.db.delete(key)

    def hset(self, hash_name: str, mapping: dict) -> bool:
        """
        Storing data as HashMap structure
        """
        return self.db.hset(hash_name, mapping=mapping)

    def hset_key(
        self, hash_name: str, key: str, value: str, ttl: Optional[int] = None
    ) -> bool:
        """
        Storing a field in HashMap structure
        """
        result = self.db.hset(hash_name, key, value)
        return self.set_expire(hash_name, ttl) if ttl else result  # type: ignore

    def hsetnx_key(
        self, hash_name: str, key: str, value: str, ttl: Optional[int] = None
    ) -> bool:
        """
        Storing a field in HashMap structure if not exists
        """
        result = self.db.hsetnx(hash_name, key, value)
        return self.set_expire(hash_name, ttl) if ttl else result  # type: ignore

    def hget(self, hash_name: str) -> dict[bytes, bytes]:
        """
        Reading data of HashMap structure
        """
        return self.db.hgetall(hash_name)

    def hget_key(self, hash_name: str, key: str) -> bytes | None:
        """
        Reading a field of HashMap structure
        """
        return self.db.hget(hash_name, key)

    def hdel(self, hash_name: str) -> int:
        """
        Delete a HashMap data
        """
        return self.db.delete(hash_name)

    def hdel_key(self, hash_name: str, key: str) -> int:
        """
        Delete a field of HashMap structure
        """
        return self.db.hdel(hash_name, key)

    def hincr_key(self, hash_name: str, key: str, amount: int = 1) -> int:
        """
        Increase value of a key in HashMap structure
        """
        return self.db.hincrby(hash_name, key, amount)

    def flush_db(self) -> bool:
        """
        Delete all data that stored in selected redis db
        """
        return self.db.flushdb()

    def flush_all(self) -> bool:
        """
        Delete all data that stored in entire redis
        """
        return self.db.flushall()
