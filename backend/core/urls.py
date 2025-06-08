import contextlib

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("api/v1/", include('api.urls')),
]

urlpatterns += staticfiles_urlpatterns()

if settings.ADMIN_ENABLED:
    urlpatterns += [
        path("nll/", admin.site.urls),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
        path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]

# import debug_toolbar
if settings.ENABLE_DEBUG_TOOLBAR:
    with contextlib.suppress(Exception):
        import debug_toolbar  # noqa

        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
