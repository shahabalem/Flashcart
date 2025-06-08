from api import apis
from django.urls import include, path

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('ping/', apis.ping, name='ping'),
]
