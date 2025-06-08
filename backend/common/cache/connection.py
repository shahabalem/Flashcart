import redis
from django.conf import settings


class RedisDBPool:
    """
    redis-py uses a connection pool to manage connections to a Redis server.
    By default, each Redis instance you create will in turn create its own
    connection pool.
    Here we override this behavior and used an existing connection pool by
    passing an already created connection pool instance to the
    connection_pool argument of the Redis class
    """

    def __init__(self, size) -> None:
        self.size = size
        self.connections = [
            redis.Redis(connection_pool=self.pool(num)) for num in range(size)
        ]

    def pool(self, db):
        return redis.ConnectionPool(
            host=settings.REDIS_CACHE_HOST,
            port=settings.REDIS_CACHE_PORT,
            username=settings.REDIS_CACHE_USERNAME,
            password=settings.REDIS_CACHE_PASSWORD,
            db=db,
            decode_responses=True,
            max_connections=1000,
            socket_timeout=60,
        )

    def con_db(self, num):
        if num > self.size:
            raise ValueError(
                'requested database number is bigger than initialized connections'
            )
        return self.connections[num]


redis_connections = RedisDBPool(settings.REDIS_CACHE_DB_COUNT)
