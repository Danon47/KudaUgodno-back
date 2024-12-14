from django.urls import path
from .views import *
from hotels.apps import HotelsConfig

app_name = HotelsConfig.name


urlpatterns = [
    # Номера отеля
    path("rooms/", RoomListCreateView.as_view(), name="room_list_create"),
    path("rooms/<int:pk>/", RoomDetailView.as_view(), name="room_detail"),
    # Удобства в номерах
    path("rooms/amenities/", AmenityRoomCreateAPIView.as_view(), name="amenity_room_create"),
    # Категория номера
    path("rooms/categories/", CategoryRoomCreateAPIView.as_view(), name="room_categories_create"),
    # Отели
    path("", HotelListCreateView.as_view(), name="hotel_list_create"),
    path("<int:pk>/", HotelDetailView.as_view(), name="hotel_detail"),
    # Удобства в отелях
    path("amenities/", AmenityHotelCreateAPIView.as_view(), name="amenity_hotel_create"),
]
