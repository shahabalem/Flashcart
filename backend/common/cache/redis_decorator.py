import functools
import json
from dataclasses import dataclass
from typing import ClassVar, Optional

from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import SerializerMetaclass

from .redis_cache import CacheManagement


@dataclass
class ApiCache:
    """
    A class to use as decorator for caching API endpoints.
    """

    identifier: Optional[str] = None
    attr_key: Optional[str] = None
    static_key: Optional[str] = ''
    filters: Optional[SerializerMetaclass] = None
    ttl: Optional[int] = None
    allowed_status: int = 200

    _key_prefix: ClassVar[str] = settings.REDIS_API_CACHE_PREFIX
    _redis: CacheManagement = CacheManagement(
        db=settings.REDIS_CACHE_GENERAL_DB,
    )

    def _get_request(self, *args) -> str:
        """
        Return route of called API
        """
        request = args[0] if len(args) == 1 else args[1]

        if not isinstance(request, Request):
            return Response(
                {'error': 'Can not detect the request object'},
                status=500,
            )

        return request

    def _extract_params(self, request) -> str:
        """
        Read input query_params based on defined filters
        """
        if self.filters:
            filters_serializer = self.filters(data=request.query_params)
            filters_serializer.is_valid(raise_exception=True)
            return json.dumps(filters_serializer.validated_data)
        return ''

    def _generate_hash_name(self, request, params, **kwargs) -> str:
        """
        Return hash_name to be use as storing name
        """
        route = request.path
        attr_key = kwargs.get(self.attr_key, '')
        return f'{self._key_prefix}:{self.identifier}:{attr_key}{self.static_key}:{params}:{route}'

    def __call__(self, function):
        """
        Main functionality
        """

        @functools.wraps(function)
        def decorated_function(*args, **kwargs):
            request = self._get_request(*args)
            params = self._extract_params(request)
            hash_name = self._generate_hash_name(request, params, **kwargs)

            # return previous cached data
            if data := self._redis.get_key(hash_name):
                json_data = json.loads(data)

                return Response(
                    json_data,
                    status=self.allowed_status,
                )

            # call the API
            result = function(*args, **kwargs)

            if not isinstance(result, Response):
                return Response(
                    {'error': 'Response is not JSON-serializable'},
                    status=500,
                )

            # prevent null data or unwanted situations caching
            if not result.data or result.status_code != self.allowed_status:
                return result

            # cache the result
            data_json = json.dumps(result.data)
            self._redis.set_key(hash_name, data_json, self.ttl)

            return Response(
                result.data,
                status=self.allowed_status,
            )

        return decorated_function
