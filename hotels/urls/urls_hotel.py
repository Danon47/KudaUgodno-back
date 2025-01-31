from django.urls import path
from hotels.views.hotel.views_hotel import HotelViewSet
from hotels.views.hotel.views_hotel_amenity import HotelAmenityCommonViewSet, HotelAmenityInTheRoomViewSet, \
    HotelAmenitySportsAndRecreationViewSet, HotelAmenityForChildrenViewSet
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


    # Добавление и просмотр всех общих удобств в отеле
    path(
        "hotels/amenities_common/",
        HotelAmenityCommonViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
        name="hotels-common-list",
    ),
    # Обновление, дательный просмотр и удаление общих удобств в отеле
    path(
        "hotels/amenities_common/<int:pk>/",
        HotelAmenityCommonViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
        name="hotels-common-detail",
    ),


    # Добавление и просмотр всех удобств в номере отеля
    path(
        "hotels/amenities_in_the_room/",
        HotelAmenityInTheRoomViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
        name="hotels-in-the-room-list",
    ),
    # Обновление, дательный просмотр и удаление удобств в номере в отеля
    path(
        "hotels/amenities_in_the_room/<int:pk>/",
        HotelAmenityInTheRoomViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
        name="hotels-in-the-room-list",
    ),


    # Добавление и просмотр всех удобств спорт и отдых в отеле
    path(
        "hotels/amenities_sports_and_recreation/",
        HotelAmenitySportsAndRecreationViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
        name="hotels-sports-and-recreation-list",
    ),
    # Обновление, дательный просмотр и удаление удобств спорт и отдых в отеле
    path(
        "hotels/amenities_sports_and_recreation/<int:pk>/",
        HotelAmenitySportsAndRecreationViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
        name="hotels-sports-and-recreation-detail",
    ),


    # Добавление и просмотр всех общих удобств в отеле
    path(
        "hotels/amenities_for_children/",
        HotelAmenityForChildrenViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
        name="hotels-for-children-list",
    ),
    # Обновление, дательный просмотр и удаление общих удобств в отеле
    path(
        "hotels/amenities_for_children/<int:pk>/",
        HotelAmenityForChildrenViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
        name="hotels-for-children-detail",
    ),


    # Добавление и просмотр всех фотографий отеля
    path(
        "hotels/<int:hotel_id>/photos/",
        HotelPhotoViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
        name="hotels-common-photos",
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
