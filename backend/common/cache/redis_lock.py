from dataclasses import dataclass
from typing import Optional

from common.cache import CacheManagement
from redis import RedisError


@dataclass
class CacheLock:

    redis_con: CacheManagement
    uuid: str
    expire: Optional[int] = 1

    def __post_init__(self):
        self.uuid = f"lock_{self.uuid}"

    def accrue(self) -> bool:
        """
        Try to use given uuid as lock
        """

        try:
            pipe = self.redis_con.pipeline()
            pipe.incr(self.uuid)
            pipe.pexpire(self.uuid, self.expire)
            result = pipe.execute()

            if result[0] > 1:
                return False

        except RedisError:
            return False

        return True

    def release(self) -> True:
        self.redis_con.remove_key(self.uuid)
        return True

    def is_ready(self):
        return not self.redis_con.is_exists(self.uuid)
