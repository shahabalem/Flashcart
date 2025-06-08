# load basic configuration (common configuration in all environments)
from core.django.base import env

BACKEND_ENVIRONMENT = env.str("BACKEND_ENVIRONMENT", default="development")


# match BACKEND_ENVIRONMENT:
# load selected environment-settings based on .env file.
# (default=DEVELOPMENT)


if BACKEND_ENVIRONMENT == "production":
    from core.django.production import *  # noqa
else:
    from core.django.development import *  # noqa
