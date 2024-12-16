from django.urls import path
from .views import *
from hotels.apps import HotelsConfig

app_name = HotelsConfig.name


urlpatterns = [
    # Номера отеля
    path("rooms/", RoomListCreateView.as_view(), name="room_list_create"),
    path("rooms/<int:pk>/", RoomDetailView.as_view(), name="room_detail_update_delete"),
    # Удобства в номерах
    path("rooms/amenities/", RoomAmenityCreateAPIView.as_view(), name="room_amenity_create"),
    # Категория номера
    path("rooms/categories/", RoomCategoryCreateAPIView.as_view(), name="room_categories_create"),
    # Отели
    path("", HotelListCreateView.as_view(), name="hotel_list_create"),
    path("<int:pk>/", HotelDetailView.as_view(), name="hotel_detail_update_delete"),
    # Удобства в отелях
    path("amenities/", HotelAmenityCreateAPIView.as_view(), name="hotel_amenity_create"),
    # Добавление фотографий отеля и номера в отеле
    # path("photos/", PhotoCreateAPIView.as_view(), name="photo_create"),
    # path("rooms/photos/", PhotoCreateAPIView.as_view(), name="photo_create"),

]
