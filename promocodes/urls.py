from django.urls import include, path
from rest_framework.routers import DefaultRouter

from promocodes.views import PromocodesModelViewSet, PromocodesPhotoModelViewSet


router = DefaultRouter()
router.register(r"promocodes", PromocodesModelViewSet, basename="promocodes")
router.register(r"promocodesphoto", PromocodesPhotoModelViewSet, basename="promocodesphoto")

urlpatterns = [
    path("", include(router.urls)),
]
