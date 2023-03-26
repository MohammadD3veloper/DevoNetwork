from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .apis import ChatViewSet

router = DefaultRouter()
router.register('', ChatViewSet, basename="chat")


urlpatterns = [
    path('', include(router.urls))
]
