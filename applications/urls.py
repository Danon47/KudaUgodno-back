from django.urls import path

from applications.apps import ApplicationsConfig
from applications.views import ApplicationHotelViewSet, ApplicationTourViewSet


app_name = ApplicationsConfig.name

urlpatterns = [
    # Добавление и просмотр всех заявок на тур
    path(
        "tours/",
        ApplicationTourViewSet.as_view({"get": "list", "post": "create"}),
        name="hotel-applications-list",
    ),
    # Обновление, детальный просмотр и удаление заявки на тур
    path(
        "tours/<int:pk>/",
        ApplicationTourViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="hotel-applications-detail",
    ),
    # Добавление и просмотр всех заявок на отель
    path(
        "hotels/",
        ApplicationHotelViewSet.as_view({"get": "list", "post": "create"}),
        name="hotel-applications-list",
    ),
    # Обновление, детальный просмотр и удаление заявки на отель
    path(
        "hotels/<int:pk>/",
        ApplicationHotelViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="hotel-applications-detail",
    ),
]
