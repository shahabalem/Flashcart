from typing import Optional, TypeVar

from api.structure import BaseView
from django.conf import settings
from django.db import models
from rest_framework.request import Request
from rest_framework.response import Response

ModelInstance = TypeVar("ModelInstance", bound=models.Model)


class EditBaseView(BaseView):
    """
    A base view for editing a model instance.

    This view handles PUT requests to update an instance of a specified model. The request body
    is passed to the specified serializer class for validation. If the data is valid, the service
    method 'edit' is called to update the instance.

    Attributes:
        service (object): The service object containing the edit method to handle the instance update.
        serializer_class (Serializer): The serializer class to validate and serialize the input data.
        output_serializer_class (Serializer): The serializer class to format the response data.
    """

    def put(
        self,
        request: Request,
        instance: ModelInstance,
        context: Optional[dict] = None,
        isolated: bool = False,
        msg: Optional[str] = None,
        service_method: str = "update",
    ) -> Response:
        """
        Handles PUT requests to update a model instance.

        The request data is validated using the serializer class. If valid, the data is passed to the
        specified service method to update the instance. The response contains the serialized data of
        the updated instance.

        Args:
            request (Request): The DRF request object containing the data for the instance update.
            instance (models.Model): The instance to update.
            context (Optional[dict]): Additional context for the serializer. Defaults to None.
            isolated (bool): Whether to use the output-serializer for the response data. Defaults to False.
            msg (Optional[str]): A custom message to send as response. Defaults to None.
            service_method (str): The name of the service method to call for updating the instance. Defaults to "update".

        Returns:
            Response: The updated instance data wrapped in a DRF response.
        """

        if instance is None:
            return self.not_found()

        serializer = self.serializer_class(instance, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        func = getattr(self.service, service_method)
        updated_instance = func(
            instance=instance, validated_data=serializer.validated_data
        )

        if not isolated:
            if not msg:
                return self.custom_response(serializer.data)
            data = {settings.DEFAULT_STATUS_KEY: msg}
            return self.custom_response(data)

        output_serializer = self.output_serializer_class(
            updated_instance, context=context
        )
        return self.custom_response(output_serializer.data)
