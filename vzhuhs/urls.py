from django.urls import include, path
from rest_framework.routers import DefaultRouter

from vzhuhs.views import VzhuhViewSet


# Роутер для ViewSet
router = DefaultRouter()
router.register(r"vzhuhs", VzhuhViewSet, basename="vzhuhs")

urlpatterns = [
    path("", include(router.urls)),
]
