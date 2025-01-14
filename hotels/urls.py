from django.urls import path

from hotels.apps import HotelsConfig
from hotels.views.views_hotel import (
    HotelListCreateAPIView,
    HotelDetailAPIView,
    HotelAmenityCreateAPIView,
    HotelPhotoCreateAPIView,
)
from hotels.views.views_room import (
    RoomListCreateAPIView,
    RoomDetailAPIView,
    RoomAmenityCreateAPIView,
    RoomPhotoCreateAPIView,
    RoomCategoryCreateAPIView,
)

app_name = HotelsConfig.name


urlpatterns = [
    # Отели
    path("", HotelListCreateAPIView.as_view(), name="hotel-list-create"),
    path("<int:pk>/", HotelDetailAPIView.as_view(), name="hotel-detail-update-delete"),
    # Удобства в отелях
    path("amenities/", HotelAmenityCreateAPIView.as_view(), name="hotel-amenity-create"),
    # Добавление фотографий отеля
    path("photos/", HotelPhotoCreateAPIView.as_view(), name="hotel-photo-create"),
    # Номера отеля
    path("rooms/", RoomListCreateAPIView.as_view(), name="room-list-create"),
    path("rooms/<int:pk>/", RoomDetailAPIView.as_view(), name="room-detail-update-delete"),
    # Удобства в номерах
    path("rooms/amenities/", RoomAmenityCreateAPIView.as_view(), name="room-amenity-create"),
    # Добавление фотографий номера
    path("rooms/photo/", RoomPhotoCreateAPIView.as_view(), name="room-photo-create"),
    # Категория номера
    path("rooms/categories/", RoomCategoryCreateAPIView.as_view(), name="room-categories-create"),
]
