from django.urls import path
from rest_framework.routers import DefaultRouter

from tours.apps import ToursConfig
from tours.views import (
    TourFiltersView,
    TourHotView,
    TourPopularView,
    ToursAutocompleteHotel,
    ToursAutocompleteRoom,
    ToursAutocompleteTypeOfMeal,
    TourStockViewSet,
    TourViewSet,
)

app_name = ToursConfig.name

router = DefaultRouter()
router.register("tours", TourViewSet, basename="tours")
router.register("stocks", TourStockViewSet, basename="tours_stocks")


urlpatterns = [
    path(
        "tours/filters/",
        TourFiltersView.as_view({"get": "filters"}),
        name="tour-filters",
    ),
    path(
        "tours/hots/",
        TourHotView.as_view({"get": "list"}),
        name="tour-hots",
    ),
    path(
        "tours/populars/",
        TourPopularView.as_view({"get": "list"}),
        name="tour-populars",
    ),
    path(
        "tours/autocomplete/hotels/",
        ToursAutocompleteHotel.as_view(),
        name="tour_autocomplete_hotels",
    ),
    path(
        "tours/autocomplete/rooms/",
        ToursAutocompleteRoom.as_view(),
        name="tour_autocomplete_rooms",
    ),
    path(
        "tours/autocomplete/type-of-meals/",
        ToursAutocompleteTypeOfMeal.as_view(),
        name="tour_autocomplete_type_of_meals",
    ),
] + router.urls
