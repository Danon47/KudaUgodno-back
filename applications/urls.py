from django.urls import path
from rest_framework.routers import DefaultRouter

from applications.apps import ApplicationsConfig
from applications.views import ApplicationViewSet, HotelApplicationViewSet


app_name = ApplicationsConfig.name

router = DefaultRouter()
router.register("", ApplicationViewSet)

urlpatterns = [
    # Добавление и просмотр всех заявок на отель
    path(
        "hotel_applications/",
        HotelApplicationViewSet.as_view({"get": "list", "post": "create"}),
        name="hotel-applications-list",
    ),
    # Обновление, детальный просмотр и удаление заявки на отель
    path(
        "hotel_applications/<int:pk>/",
        HotelApplicationViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="hotel-applications-detail",
    ),
] + router.urls
