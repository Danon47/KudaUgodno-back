from django.urls import path

from hotels.apps import HotelsConfig
from hotels.views import (
    HotelFiltersView,
    HotelPhotoViewSet,
    HotelSearchView,
    HotelsHotView,
    HotelViewSet,
    HotelWarpUpViewSet,
    TypeOfMealViewSet,
)


app_name = HotelsConfig.name


urlpatterns = [
    path(
        "hotels/",
        HotelViewSet.as_view({"get": "list", "post": "create"}),
        name="hotels-list",
    ),
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
    path(
        "hotels/<int:hotel_id>/photos/",
        HotelPhotoViewSet.as_view({"get": "list", "post": "create"}),
        name="hotels-photos-list",
    ),
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
    path(
        "hotels/<int:hotel_id>/type_of_meals/",
        TypeOfMealViewSet.as_view({"get": "list", "post": "create"}),
        name="hotels-type-of-meals-list-create",
    ),
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
        name="hotels-filters",
    ),
    path(
        "hotels/hot/",
        HotelsHotView.as_view({"get": "list"}),
        name="hotels-hot",
    ),
]
