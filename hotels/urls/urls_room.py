from django.urls import path
from hotels.views.room.views_room import RoomViewSet
from hotels.views.room.views_room_photo import RoomPhotoViewSet


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
        name="room-photos",
    ),
    # Удаление фотографий
    path(
        "rooms/<int:room_id>/photos/<int:pk>/",
        RoomPhotoViewSet.as_view({"delete": "destroy"}),
        name="room-photo-detail",
    ),
]
