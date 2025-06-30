from django.urls import path
from rest_framework.routers import DefaultRouter

from tours.apps import ToursConfig
from tours.views import (
    HotelAutocomplete,
    RoomAutocomplete,
    TourFiltersView,
    TourHotView,
    TourStockViewSet,
    TourViewSet,
    TypeOfMealAutocomplete,
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
        "tours/hot/",
        TourHotView.as_view({"get": "list"}),
        name="tour-hot",
    ),
    path("hotel-autocomplete/", HotelAutocomplete.as_view(), name="hotel_autocomplete"),
    path("room-autocomplete/", RoomAutocomplete.as_view(), name="room_autocomplete"),
    path("type-of-meal-autocomplete/", TypeOfMealAutocomplete.as_view(), name="type_of_meal_autocomplete"),
] + router.urls
