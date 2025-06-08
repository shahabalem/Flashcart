from django.conf import settings
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import APIException


class APIValidationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail_key = settings.DEFAULT_DETAIL_KEY
    default_detail = "Validation failed."
    detail = {default_detail_key: default_detail}

    titles = {
        "USERNAME": "Username must only include letters, numbers, and _ characters.",
        "INVALID_CODE": "Invalid code.",
    }

    def __init__(self, key: str | None = None, status_code: int | None = None):
        self.detail = {
            self.default_detail_key: self.titles.get(key, self.default_detail)
        }
        self.status_code = status_code if status_code else self.status_code


class APINotFoundException(APIValidationException):
    status_code = status.HTTP_404_NOT_FOUND

    titles = {
        "COMMENT": "Comment not found.",
        "USER": "User not found.",
        "POST": "Post not found.",
        "OFFER": "This offer is no longer available.",
    }

    def __init__(self, key: str | None = None, status_code: int | None = None):
        super().__init__(key, status_code)


class APIAlreadyExistException(APIValidationException):
    status_code = status.HTTP_409_CONFLICT

    titles = {
        "WALLET": "You have already connected your wallet.",
        "TWITTER": "You have already connected your twitter.",
        "SUBSCRIBER": "You have already subscribed to our newsletter.",
        "EMAIL": "An account with this email address already exists.",
        "USERNAME": "An account with this username already exists.",
        "REPORT": "Any account or post can be reported only once by each user.",
        "EXHIBITION": "An event with this name already exists.",
        "EXHIBITION_RESPONSIBLE": "Each role can be assigned to a person only once. Please assign a different role.",
        "COLLECTION": "You have already a collection with this name.",
        "TOOLS": "You have already selected this tool.",
        "CATEGORY": "You have already selected this category",
        "OFFER": "You have already claimed this offer.",
        "CODE": "You have already claimed this code.",
        "GRID": "This artwork is already on The Grid.",
        "USER_SOCIAL_LIMIT": "Each social media can be added only once.",
        "GIFT": "This gift has already been sent to a user.",
        "OPEN_CALL": "You have already applied for this open call.",
        "FILE": "This file already used.",
        "SLUG": "This slug already used.",
        "IS_COLLECTION": "You have already added this artwork to this collection.",
    }

    def __init__(self, key: str | None = None, status_code: int | None = None):
        super().__init__(key, status_code)


def do_and_catch_unique_constraint_error(
    classes: object, method_name: str, key='DEFINITION', **kwargs
):
    """
    Insert/Update data in database and raise custom exception if
    database raised IntegrityError because of conflict between
    unique=True and duplicated data
    """

    func = getattr(classes, method_name)

    try:
        result = func(**kwargs)
    except IntegrityError:
        raise APIAlreadyExistException(key)
    else:
        return result


def do_and_raise_unique_constraint_error(instance, exception_key: str):
    """
    Save data in the model and raise DRF-Exception if model raised IntegrityError
    """

    try:
        result = instance.save()
    except IntegrityError:
        raise APIAlreadyExistException(exception_key)
    else:
        return result


def raise_if_query_not_exists(model, **kwargs):
    if not model.objects.filter(**kwargs).exists():
        raise APIValidationException(f'This {model.__name__} does not exist')
