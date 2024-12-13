from django.urls import path
from .views import *
from hotels.apps import HotelsConfig

app_name = HotelsConfig.name


urlpatterns = [
    # Отели
    path("hotels/", HotelListCreateView.as_view(), name="hotel-list-create"),
    path("hotels/<int:pk>/", HotelDetailView.as_view(), name="hotel-detail"),
    # Номера отеля
    path("hotel-rooms/", HotelRoomListCreateView.as_view(), name="hotel-room-list-create"),
    path("hotel-rooms/<int:pk>/", HotelRoomDetailView.as_view(), name="hotel-room-detail"),
    # Удобства в номерах
    path("amenity-rooms/", AmenityRoomListCreateView.as_view(), name="amenity-room-list-create",),
    path("amenity-rooms/<int:pk>/", AmenityRoomDetailView.as_view(), name="amenity-room-detail",),
    # Удобства в отелях
    path("amenity-hotels/", AmenityHotelListCreateView.as_view(), name="amenity-hotel-list-create",),
    path("amenity-hotels/<int:pk>/", AmenityHotelDetailView.as_view(), name="amenity-hotel-detail",),
    # Категория номера
    path("hotel-rooms-categories/", CategoryHotelRoomListCreateView.as_view(), name="hotel-room-categories-list-create",),
]
