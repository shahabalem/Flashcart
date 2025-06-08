from typing import Optional

from api.exceptions import APIValidationException
from api.structure import BaseView
from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response


class CreateBaseView(BaseView):
    """
    A base view for creating a new model instance.

    This view handles POST requests to create a new instance of a model. The request body
    is passed to the specified serializer class for validation. If the data is valid,
    the service method 'create' is called to create the instance.

    Attributes:
        service (object): The service object containing the create method to handle the instance creation.
        model (Model): The model class to be used by the service method.
        serializer_class (Serializer): The serializer class to validate and serialize the input data.
        output_serializer_class (Serializer): The serializer class to format the response data.
    """

    def post(
        self,
        request: Request,
        context: Optional[dict] = None,
        isolated: bool = False,
        msg: Optional[str] = None,
        failure_msg: bool = False,
        service_method: str = "create",
    ) -> Response:
        """
        Handles POST requests to create a new model instance.

        The request data is validated using the serializer class. If valid, the data is passed to the
        specified service method to create the instance. The response contains the serialized data of
        the created instance or a custom message if provided.

        Args:
            request (Request): The DRF request object containing the data for the new instance.
            context (Optional[dict]): Additional context for the serializer. Defaults to None.
            isolated (bool): Whether to use the output-serializer for the response data. Defaults to False.
            msg (Optional[str]): A custom message to return as response. Defaults to None.
            failure_msg (bool): Whether to raise an exception if the creation fails. Defaults to False.
            service_method (str): The name of the service method to call for creating the instance. Defaults to "create".

        Returns:
            Response: The created instance data wrapped in a DRF response.

        Raises:
            APIValidationException: If the creation fails and failure_msg is True.
        """

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        func = getattr(self.service, service_method)
        result = func(model=self.model, validated_data=serializer.validated_data)

        if msg:
            data = {settings.DEFAULT_STATUS_KEY: msg}
        else:
            if isolated:
                data = self.output_serializer_class(result, context=context).data
            else:
                data = {**{'id': result.id}, **serializer.data}

        if failure_msg and not result:
            raise APIValidationException("TRANSACTION")

        return self.custom_response(data, status=status.HTTP_201_CREATED)
