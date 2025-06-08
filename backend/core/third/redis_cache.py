from core.django.base import env

# Do not forget to have Redis installed and running in your os before
# starting the project


# Configure Redis as Cash backend
REDIS_CACHE_HOST = env('REDIS_CACHE_HOST', default='redis')
REDIS_CACHE_PORT = env.int('REDIS_CACHE_PORT', default='6379')
REDIS_CACHE_USERNAME = env("REDIS_USERNAME", default=None)
REDIS_CACHE_PASSWORD = env("REDIS_PASSWORD", default=None)

# Redis DB definition
REDIS_CACHE_DB_COUNT = 2
REDIS_CACHE_GENERAL_DB = 0
REDIS_CACHE_DJANGO_DB = 1

# Redis static keys
REDIS_API_CACHE_PREFIX = 'API'
REDIS_RATELIMIT_CACHE_PREFIX = 'RATELIMIT'
REDIS_USER_VIEW_LOCK_PREFIX = 'USER_VIEW'


# Redis Expires Time
REDIS_CACHE_LONG_TTL = 604800  # 1 week


if REDIS_CACHE_USERNAME and REDIS_CACHE_PASSWORD:
    location = f"redis://{REDIS_CACHE_USERNAME}:{REDIS_CACHE_PASSWORD}@{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}/{REDIS_CACHE_DJANGO_DB}"
else:
    location = (
        f"redis://{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}/{REDIS_CACHE_DJANGO_DB}",
    )

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": location,
        "TIMEOUT": 10 * 60,  # default cashing time
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
