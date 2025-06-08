import itertools
import logging
import re
from uuid import uuid4

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.base import ModelBase
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework.request import Request

User = get_user_model()

logger = logging.getLogger(__name__)


def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model
    && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


def get_query(model: ModelBase, **kwargs):
    """
    Return wanted query in selected model
    """
    return model.objects.filter(**kwargs)  # type: ignore


def get_model(module_name: str, model_name: str):
    """
    Return the ClassModel of the given Module-name and Model-name
    """
    return apps.get_model(app_label=module_name, model_name=model_name)


def get_content(model: ModelBase):
    """
    Return object of wanted content in the ContentType model
    """
    return ContentType.objects.get_for_model(model)


def get_requested_route(request: Request) -> str:
    """
    Return requested route
    """
    return request.path


def get_client_ip(request: Request) -> str:
    """
    Return ip of client
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return (
        x_forwarded_for.split(',')[0]
        if x_forwarded_for
        else request.META.get('REMOTE_ADDR')
    )


def dimension_calculator(width, height, max_size=512):
    """
    Calculate new Ratio based on original Ratio
    """
    ratio = min(max_size / width, max_size / height)
    return (int(width * ratio), int(height * ratio))


def get_valid_count(request):
    """
    keep the count in acceptable Min/Max range
    """
    count = request.GET.get("count", settings.DEFAULT_COUNT_VALUE)
    count = min(
        max(int(count), settings.MINIMUM_COUNT_VALUE),
        settings.MAXIMUM_COUNT_VALUE,
    )
    return count


def slug_generator(model, value: str = None, max_length: int = 7) -> str:
    """
    Generate an slug from given title that is not exists in requested model
    """

    slug_len = max_length - 3
    value = value if value else ''
    user_slug = value = re.sub(r'[^\dA-Za-z\-_]', '', value)
    value = str(uuid4())[: min(slug_len, 5)] if not user_slug else user_slug
    slug_candidate = slug_original = slugify(
        value[:slug_len],
        allow_unicode=True,
    )

    for i in itertools.count(1):
        if not model.objects.filter(slug=slug_candidate).exists():
            break

        slug_candidate = f'{slug_original}-{i}'

    return slug_candidate
