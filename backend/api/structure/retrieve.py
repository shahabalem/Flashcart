from typing import Any, Optional, TypeVar

from api.structure import BaseView
from django.db import models
from rest_framework.response import Response

ModelInstance = TypeVar("ModelInstance", bound=models.Model)


class RetrieveBaseView(BaseView):
    """
    A base view for retrieving a model instance.

    This view handles GET requests to retrieve an instance of a specified model. If an instance is provided,
    it will be serialized and returned. Otherwise, the instance will be fetched based on the lookup value.

    Attributes:
        service (object): The service object containing the read method to handle the instance retrieval.
        model (Model): The model class to be used by the service method.
        output_serializer_class (Serializer): The serializer class to format the response data.
        lookup_field (str): The field to use for looking up the instance. Defaults to 'pk'.
    """

    def get(
        self,
        lookup_value: Any = None,
        instance: Optional[ModelInstance] = None,
        context: Optional[dict] = None,
        service_method: str = "read",
    ) -> Response:
        """
        Handles GET requests to retrieve a model instance.

        If an instance is provided, it will be serialized and returned. Otherwise, the instance will be
        fetched using the specified service method and the lookup value.

        Args:
            lookup_value (Any): The value to use for looking up the instance.
            instance (Optional[ModelInstance]): The instance to retrieve. Defaults to None.
            context (Optional[dict]): Additional context for the serializer. Defaults to None.
            service_method (str): The name of the service method to call for retrieving the instance. Defaults to "read".

        Returns:
            Response: The retrieved instance data wrapped in a DRF response, or a not found response if the instance does not exist.
        """

        if not instance:
            filter_kwargs = {self.lookup_field: lookup_value}
            func = getattr(self.service, service_method)
            instance = func(model=self.model, filter_kwargs=filter_kwargs)

        if instance is not None:
            serializer = self.output_serializer_class(instance, context=context)
            return self.custom_response(serializer.data)

        return self.not_found()
