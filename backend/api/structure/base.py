from api.permissions import AllowAny
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.serializers import SerializerMetaclass
from rest_framework.views import APIView


class BaseView(APIView):
    permission_classes: BasePermission = (AllowAny,)
    lookup_field: str = 'pk'
    serializer_class: SerializerMetaclass
    output_serializer_class: SerializerMetaclass

    def forbidden(self, msg: str = settings.FORBIDDEN_MESSAGE):
        return Response(msg, status.HTTP_403_FORBIDDEN)

    def not_found(self):
        return Response({}, status.HTTP_404_NOT_FOUND)

    def no_content(self):
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def custom_response(self, data: dict, status: int = status.HTTP_200_OK):
        return Response(data, status=status)

    class Validator:
        def service(self):
            assert hasattr(
                self, 'service'
            ), 'Class {view_class} missing "service" attribute'.format(
                view_class=f'{self.__module__}:{self.__name__}'
            )

        def serializer_class(self):
            assert hasattr(
                self, 'serializer_class'
            ), 'Class {view_class} missing "serializer_class" attribute'.format(
                view_class=f'{self.__module__}:{self.__name__}'
            )

        def output_serializer_class(self):
            assert hasattr(
                self, 'output_serializer_class'
            ), 'Class {view_class} missing "output_serializer_class" attribute'.format(
                view_class=f'{self.__module__}:{self.__name__}'
            )

        def model(self):
            assert hasattr(
                self, 'model'
            ), 'Class {view_class} missing "model" attribute'.format(
                view_class=f'{self.__module__}:{self.__name__}'
            )
