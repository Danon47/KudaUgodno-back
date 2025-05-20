from django.urls import path

from hotels.apps import HotelsConfig
from hotels.views.room.date.views_room_date import RoomDateViewSet
from hotels.views.room.photo.views_room_photo import RoomPhotoViewSet
from hotels.views.room.views_room import RoomViewSet


app_name = HotelsConfig.name


urlpatterns = [
    # Добавление и просмотр всех номеров
    path(
        "<int:hotel_id>/rooms/",
        RoomViewSet.as_view({"get": "list", "post": "create"}),
        name="rooms-list",
    ),
    # Обновление, детальный просмотр и удаление номера
    path(
        "<int:hotel_id>/rooms/<int:pk>/",
        RoomViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="rooms-detail",
    ),
    # Добавление и просмотр всех фотографий в номер
    path(
        "rooms/<int:room_id>/photos/",
        RoomPhotoViewSet.as_view({"get": "list", "post": "create"}),
        name="rooms-photos-list",
    ),
    # Удаление фотографий
    path(
        "rooms/<int:room_id>/photos/<int:pk>/",
        RoomPhotoViewSet.as_view({"delete": "destroy"}),
        name="rooms-photo-detail",
    ),
    # Добавление и просмотр всех дат для номеров
    path(
        "<int:hotel_id>/rooms/dates/",
        RoomDateViewSet.as_view({"get": "list", "post": "create"}),
        name="rooms-dates-list",
    ),
    # Обновление, детальный просмотр и удаление дат для номеров
    path(
        "<int:hotel_id>/rooms/dates/<int:pk>/",
        RoomDateViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="rooms-dates-detail",
    ),
]
