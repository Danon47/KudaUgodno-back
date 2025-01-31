from django.urls import path
from hotels.views.hotel.views_hotel import HotelViewSet
from hotels.views.hotel.views_hotel_amenity import HotelAmenityCommonViewSet
from hotels.views.hotel.views_hotel_photo import HotelPhotoViewSet
from hotels.views.hotel.views_hotel_rules import HotelRulesViewSet

urlpatterns = [
    # Добавление и просмотр всех отелей
    path(
        "hotels/",
        HotelViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
        name="hotels-list",
    ),
    # Обновление, дательный просмотр и удаление отеля
    path(
        "hotels/<int:pk>/",
        HotelViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
        name="hotels-detail",
    ),
    # Добавление и просмотр всех удобств в отеле
    path(
        "hotels/amenities",
        HotelAmenityCommonViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
        name="hotels-list",
    ),
    # Обновление, дательный просмотр и удаление удобств в отеле
    path(
        "hotels/amenities/<int:pk>/",
        HotelAmenityCommonViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
        name="hotels-detail",
    ),
    # Добавление и просмотр всех фотографий отеля
    path(
        "hotels/<int:hotel_id>/photos/",
        HotelPhotoViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
        name="hotels-photos",
    ),
    # Удаление выбранной фотографии отеля
    path(
        "hotels/<int:hotel_id>/photos/<int:pk>/",
        HotelPhotoViewSet.as_view(
            {"delete": "destroy"}
        ),
        name="hotels-photo-detail",
    ),
    # Добавление и просмотр всех правил в отеле
    path(
        "hotels/rules/",
        HotelRulesViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
        name="hotels-rules",
    ),
    # Обновление, дательный просмотр и удаление правил в отеле
    path(
        "hotels/rules/<int:pk>/",
        HotelRulesViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
        name="hotels-rules-detail",
    ),
]
