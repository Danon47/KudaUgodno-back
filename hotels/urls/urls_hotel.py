from django.urls import path

from hotels.views.hotel.photo.views_hotel_photo import HotelPhotoViewSet
from hotels.views.hotel.type_of_meals.views_type_of_meals import TypeOfMealViewSet
from hotels.views.hotel.views_hotel import HotelFiltersView, HotelSearchView, HotelViewSet
from hotels.views.hotel.what_about.views_hotel_what_about import HotelWarpUpViewSet


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
    # Подборка, что на счёт
    path(
        "hotels/whats_about/",
        HotelWarpUpViewSet.as_view({"get": "list"}),
        name="hotels-whats-about-list",
    ),
    # Добавление и просмотр всех типов питания
    path(
        "hotels/<int:hotel_id>/type_of_meals/",
        TypeOfMealViewSet.as_view({"get": "list", "post": "create"}),
        name="hotels-type-of-meals-list-create",
    ),
    # Удаление выбранного типа питания
    path(
        "hotels/<int:hotel_id>/type_of_meals/<int:pk>/",
        TypeOfMealViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="hotels-type-of-meals-destroy",
    ),
    path(
        "hotels/search/",
        HotelSearchView.as_view({"get": "search"}),
        name="hotels-search",
    ),
    path(
        "hotels/filters/",
        HotelFiltersView.as_view({"get": "filters"}),
        name="tour-filters",
    ),
]
