from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .apis import AuthenticationViewSet


router = SimpleRouter()
router.register('', AuthenticationViewSet, basename="authentication")


urlpatterns = [
    path('', include(router.urls)),
]
