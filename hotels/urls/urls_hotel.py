from django.urls import path

from hotels.views.hotel.views_hotel import HotelViewSet
from hotels.views.hotel.views_hotel_photo import HotelPhotoViewSet
from hotels.views.hotel.views_hotel_what_about import HotelWarpUpViewSet


urlpatterns = [
    # Добавление и просмотр всех отелей
    path(
        "hotels/",
        HotelViewSet.as_view({"get": "list", "post": "create"}),
        name="hotels-list",
    ),
    # Обновление, дательный просмотр и удаление отеля
    path(
        "hotels/<int:pk>/",
        HotelViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="hotels-detail",
    ),
    # Добавление и просмотр всех фотографий отеля
    path(
        "hotels/<int:hotel_id>/photos/",
        HotelPhotoViewSet.as_view({"get": "list", "post": "create"}),
        name="hotels-photos-list",
    ),
    # Удаление выбранной фотографии отеля
    path(
        "hotels/<int:hotel_id>/photos/<int:pk>/",
        HotelPhotoViewSet.as_view({"delete": "destroy"}),
        name="hotels-photos-detail",
    ),
    path(
        "hotels/whats_about/",
        HotelWarpUpViewSet.as_view({"get": "list"}),
        name="hotels-whats-about-list",
    ),
]
