"""devo_network URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('devonetwork/SecurePanel/ui/', admin.site.urls),
    path('prometheus/', include('django_prometheus.urls')),
    path('api/schema', include([
        path('', SpectacularAPIView.as_view(), name='schema'),
        path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ])),
    path('api/', include([
        path('auth/', include('devo_network.authentication.urls')),
        path('chat/', include('devo_network.chat.urls'))
    ])),
    path('api/tokens/', include([
        path('obtain/', TokenObtainPairView.as_view(), name="token_obtain"),
        path('refresh/', TokenRefreshView.as_view(), name="refresh"),
    ]))
]
