from typing import Optional

from api.paginator import CursorPaginationHandlerMixin, PaginationHandlerMixin
from api.structure import BaseView
from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response


class CollectBaseView(BaseView, PaginationHandlerMixin):
    """
    A base view for listing and paginating a queryset, returning a DRF response.

    This view processes the request to extract pagination settings from query parameters
    using 'FilterSerializer'. It then calls a service method to obtain a queryset, paginates the result,
    and returns the paginated data in a DRF response.

    Class Attributes:
        service (object): The service class containing the list method to fetch the queryset.
        model (Model): The model class to be used by the service method.
        output_serializer_class (Serializer): The serializer class to format the paginated results.
    """

    def get(
        self,
        request: Request,
        queryset: Optional[QuerySet] = None,
        context: Optional[dict] = None,
        service_method: str = "list",
    ) -> Response:
        """
        Handles GET requests to list and paginate a queryset.

        Args:
            request (Request): The DRF request object containing query parameters for pagination.
            queryset (Optional[QuerySet]): The queryset to paginate. If None, fetched using the service method.
            context (Optional[dict]): Additional context for the serializer.
            service_method (str): The name of the service method to call for fetching the queryset. Defaults to "list".

        Returns:
            Response: The paginated data wrapped in a DRF response.
        """

        if queryset is None:
            func = getattr(self.service, service_method)
            queryset = func(model=self.model)

        data = self.paginate(request, queryset, self.output_serializer_class, context)
        return self.custom_response(data)


class CursorCollectBaseView(BaseView, CursorPaginationHandlerMixin):
    """
    A base view for listing and paginating a queryset, returning a DRF response.

    This view processes the request to extract pagination settings from query parameters
    using 'FilterSerializer'. It then calls a service method to obtain a queryset, paginates the result,
    and returns the paginated data in a DRF response.

    Class Attributes:
        service (object): The service class containing the list method to fetch the queryset.
        model (Model): The model class to be used by the service method.
        output_serializer_class (Serializer): The serializer class to format the paginated results.
    """

    def get(
        self,
        request: Request,
        queryset: Optional[QuerySet] = None,
        context: Optional[dict] = None,
        service_method: str = "list",
        order_by: str = 'id',
        desc: bool = True,
    ) -> Response:
        """
        Handles GET requests to list and paginate a queryset.

        Args:
            request (Request): The DRF request object containing query parameters for pagination.
            queryset (Optional[QuerySet]): The queryset to paginate. If None, fetched using the service method.
            context (Optional[dict]): Additional context for the serializer.
            service_method (str): The name of the service method to call for fetching the queryset. Defaults to "list".
            order_by (str): The field to order the queryset by
            desc (bool): Whether to order the queryset in descending order or not

        Returns:
            Response: The paginated data wrapped in a DRF response.
        """

        if queryset is None:
            func = getattr(self.service, service_method)
            queryset = func(model=self.model)

        data = self.paginate(
            request,
            queryset,
            self.output_serializer_class,
            order_by,
            desc,
            context,
        )

        return self.custom_response(data)
