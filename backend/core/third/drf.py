REST_FRAMEWORK = {
    # Swagger settings
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Authentication settings
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # permissions
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    # Date settings
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S",
    # Pagination settings
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    # Exception settings
    "EXCEPTION_HANDLER": "common.exceptions_handlers.custom_exception_handler",
}
