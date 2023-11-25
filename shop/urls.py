from django.contrib import admin
from django.urls import path, include
from api.urls import apiurlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin page endpoints
    path('auth/', include('djoser.urls')),  # Djoser endpoints
    path('auth/', include('djoser.urls.authtoken')),  # Djoser auth endpoints
    path('api/v1/', include(apiurlpatterns))  # API Endpoints
]
