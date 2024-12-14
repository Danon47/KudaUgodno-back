from django.urls import path
from .views import *
from hotels.apps import HotelsConfig

app_name = HotelsConfig.name


urlpatterns = [
    # Номера отеля
    path("hotel-rooms/", HotelRoomListCreateView.as_view(), name="hotel-room-list-create"),
    path("hotel-rooms/<int:pk>/", HotelRoomDetailView.as_view(), name="hotel-room-detail"),
    # Удобства в номерах
    path("hotel-rooms/amenities/", AmenityRoomListCreateView.as_view(), name="amenity-room-list-create"),
    # Категория номера
    path("hotel-rooms/categories/", CategoryHotelRoomListCreateView.as_view(),name="hotel-room-categories-list-create"),
    # Отели
    path("", HotelListCreateView.as_view(), name="hotel-list-create"),
    path("<int:pk>/", HotelDetailView.as_view(), name="hotel-detail"),
    # Удобства в отелях
    path("amenities/", AmenityHotelListCreateView.as_view(), name="amenity-hotel-list-create"),
]
