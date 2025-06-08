from math import ceil

from django.conf import settings
from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.request import Request


class PaginationHandlerMixin:
    """
    This mixin handles pagination functionality using 'Offset:Limit' logic for APIView.

    It provides the `paginate` method which can be used to paginate querysets
    based on offset and limit parameters from the request query parameters.
    """

    class PaginateException(APIException):
        def __init__(self, detail=settings.DEFAULT_DETAIL_KEY, status_code=404):
            self.status_code = status_code
            self.detail = detail

    class FilterSerializer(serializers.Serializer):
        per_page = serializers.IntegerField(required=False)
        page = serializers.IntegerField(required=False)

        def validate_page(self, value):
            return max(value, 1)

        def validate_per_page(self, value):
            return min(
                max(value, settings.MINIMUM_COUNT_VALUE), settings.MAXIMUM_COUNT_VALUE
            )

    def calculate(
        self,
        request: Request,
        queryset: QuerySet,
    ):
        paginate_serializer = self.FilterSerializer(data=request.query_params)
        paginate_serializer.is_valid(raise_exception=True)

        page = paginate_serializer.validated_data.get('page', 1)
        per_page = paginate_serializer.validated_data.get(
            'per_page', settings.PAGINATE_PAGE_SIZE
        )

        count = queryset.count()
        pages = ceil(count / per_page)

        return page, per_page, count, pages

    def paginate(
        self,
        request: Request,
        queryset: QuerySet,
        output_serializer_class,
        context: dict,
    ):
        """
        Paginate the given queryset based on offset and limit from the request.

        Args:
            request (Request): The DRF request object containing query parameters.
            queryset (QuerySet): The queryset to paginate.
            output_serializer_class (Serializer): The serializer class for the output data.
            context (dict): Additional context for the serializer.

        Returns:
            dict: A dictionary containing the count, pages, per_page, page, and paginated results.
        """

        page, per_page, count, pages = self.calculate(request, queryset)

        if 0 < pages < page:
            raise self.PaginateException('Invalid page.')

        if pages <= 0:
            results = []
        else:
            offset = (page - 1) * per_page
            limit = offset + per_page
            limited_queryset = queryset[offset:limit]

            results = output_serializer_class(
                limited_queryset, many=True, context=context
            ).data

        return {
            'count': count,
            'pages': pages,
            'per_page': per_page,
            'page': page,
            'results': results,
        }


class CursorPaginationHandlerMixin:
    """
    This mixin handles pagination functionality using 'Cursor:Limit' logic for APIView.

    It provides the `paginate` method which can be used to paginate querysets
    based on cursor and limit parameters from the request query parameters.
    """

    class PaginateException(APIException):
        def __init__(self, detail=settings.DEFAULT_DETAIL_KEY, status_code=404):
            self.status_code = status_code
            self.detail = detail

    class FilterSerializer(serializers.Serializer):
        cursor = serializers.IntegerField(required=False)
        limit = serializers.IntegerField(required=False)

        def validate_cursor(self, cursor):
            return max(cursor, 1)

        def validate_limit(self, value):
            return min(
                max(value, settings.MINIMUM_COUNT_VALUE), settings.MAXIMUM_COUNT_VALUE
            )

    def paginate(
        self,
        request: Request,
        queryset: QuerySet,
        output_serializer_class,
        order_by: str,
        desc: bool,
        context: dict,
    ):
        """
        Paginate the given queryset based on cursor and limit from the request.

        Args:
            request (Request): The DRF request object containing query parameters.
            queryset (QuerySet): The queryset to paginate.
            output_serializer_class (Serializer): The serializer class for the output data.
            order_by (str): The field to order the queryset by.
            desc (bool): Whether to order the queryset in descending order or not.
            context (dict): Additional context for the serializer.

        Returns:
            dict: A dictionary containing the cursor, limit, next, and paginated results.
        """

        paginate_serializer = self.FilterSerializer(data=request.query_params)
        paginate_serializer.is_valid(raise_exception=True)

        cursor = paginate_serializer.validated_data.get('cursor', None)
        limit = paginate_serializer.validated_data.get(
            'limit', settings.PAGINATE_PAGE_SIZE
        )

        if desc:
            order_by = f'-{order_by}'
            queryset = (
                queryset.filter(id__lte=cursor).order_by(order_by)[:limit]
                if cursor
                else queryset.order_by(order_by)[:limit]
            )
        else:
            queryset = (
                queryset.filter(id__gte=cursor).order_by(order_by)[:limit]
                if cursor
                else queryset.order_by(order_by)[:limit]
            )

        results = output_serializer_class(queryset, many=True, context=context).data
        next_cursor = None

        if results and len(results) == limit:
            id = results[len(results) - 1].get('id')
            next_cursor = id - 1 if desc else id + 1
        else:
            next_cursor = None

        return {
            'cursor': cursor,
            'limit': limit,
            'next': next_cursor,
            'results': results,
        }
