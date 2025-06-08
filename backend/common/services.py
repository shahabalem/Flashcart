from common.utils import get_object
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet


class BaseCRUD:
    """
    Base CRUD functionality for DRY principle
    """

    @staticmethod
    def create(*, model: ModelBase, validated_data: dict) -> models.Model:
        """
        Create new instance
        """
        instance = model(**validated_data)
        instance.save()
        return instance

    @staticmethod
    def read(*, model: ModelBase, filter_kwargs: dict) -> models.Model | None:
        """
        Return detail of requested instance
        """
        return get_object(model, **filter_kwargs)

    @staticmethod
    def list(*, model: ModelBase) -> QuerySet:
        """
        Return list of all instance for requested model
        """
        return model.objects.all()

    @staticmethod
    def update():
        raise NotImplementedError()

    @staticmethod
    def delete(*, model: ModelBase, filter_kwargs: dict = None) -> None:
        """
        Delete requested instance
        """
        model.objects.filter(**filter_kwargs).delete()
        return None
