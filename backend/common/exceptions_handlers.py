import socket

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import exceptions, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler


class CustomSocketError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = (
        "A network error occurred. Please check your internet connection and try again."
    )
    default_code = "socket_error"


def custom_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, socket.error):
        exc = CustomSocketError()

    response = exception_handler(exc, ctx)

    if response is not None:
        if isinstance(exc, ValidationError) and hasattr(response.data, "items"):
            for field, errors in response.data.items():
                obj = "".join(list(field)).title()
                msg = "".join(list(errors[0]))

                if "does not exist" in msg:
                    response.data = {"detail": f"This {obj} does not exists"}

                elif "Date has wrong format" in msg:
                    response.data = {"detail": f"Invalid time format in {obj}"}

                elif "is required" in msg:
                    response.data = {"detail": f"{obj} is required"}

                elif "no more than" in msg:
                    err = msg.replace("this", f"{obj}")
                    response.data = {"detail": err}

                elif "may not be blank" in msg:
                    err = msg.replace("This field", f"{obj}")
                    response.data = {"detail": err}

                else:
                    response.data = {"detail": f"{msg}"}

                break

    return response
