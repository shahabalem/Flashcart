import functools
from dataclasses import dataclass

from django.conf import settings
from rest_framework.exceptions import APIException
from rest_framework.request import Request

from .redis_cache import CacheManagement


@dataclass
class RateLimit:
    """
    A class representing rate limiting configuration.

    Attributes:
        rate (int): The maximum number of requests allowed within a given window.
        window (int): The time period (in seconds) during which the rate limit applies.
        freeze (int): The time (in seconds) to expand the window time of user riches to the maximum rate.
        request (Request): The request object associated with the rate limit.
        success_clear (bool): Whether to clear the cache if the operation was successful.
        key_prefix (str): The key prefix to use in the Redis keys naming.
        redis (CacheManagement): The cache management object to use for Redis operations.
    """

    rate: int = 3
    window: int = 60
    freeze: int = 0
    request: Request = None
    server_side: bool = False
    success_clear: bool = False
    key_prefix: str = settings.REDIS_RATELIMIT_CACHE_PREFIX
    redis: CacheManagement = CacheManagement(db=settings.REDIS_CACHE_GENERAL_DB)

    class RateLimitException(APIException):
        def __init__(self, detail=settings.DEFAULT_DETAIL_KEY, status_code=429):
            self.status_code = status_code
            self.detail = detail

    def _get_client_ip(self, request: Request) -> str:
        """
        Return ip of client
        """

        if self.server_side:
            if ip := request.META.get('HTTP_DIR_CLIENTIP'):
                return ip

        if x_forwarded_for := request.META.get('HTTP_X_FORWARDED_FOR'):
            return x_forwarded_for.split(',')[0]

        return request.META.get('REMOTE_ADDR')

    def _get_requested_route(self, request: Request) -> str:
        """
        Return requested route
        """
        return request.path

    def __call__(self, function):
        """
        Main functionality
        """

        @functools.wraps(function)
        def decorated_function(*args, **kwargs):
            request = args[1] if self.request is None else self.request
            ip = self._get_client_ip(request)
            route = self._get_requested_route(request)
            key = f'{self.key_prefix}:{ip}{route}'

            data = self.redis.get_key(key)

            if data and int(data) == self.rate:
                if self.freeze == 0:
                    raise self.RateLimitException(
                        detail='Too many attempts! Please try again latter'
                    )

                self.redis.set_expire(key, self.freeze)
                blocked_in_minute = int(self.freeze / 60)

                blocked_for = (
                    f'{self.freeze} seconds'
                    if self.freeze < 60
                    else f'{blocked_in_minute} minutes'
                )

                raise self.RateLimitException(
                    detail=f'Too many attempts! Please try again in {blocked_for}'
                )

            if not data:
                self.redis.set_key(key, 1, self.window)
            else:
                self.redis.incr_key(key, 1)

            result = function(*args, **kwargs)
            self.redis.remove_key(key) if self.success_clear else None
            return result

        return decorated_function
