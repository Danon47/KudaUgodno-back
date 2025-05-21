from django.urls import path
from rest_framework.routers import DefaultRouter

from tours.apps import ToursConfig
from tours.views import TourFiltersView, TourSearchView, TourStockViewSet, TourViewSet


app_name = ToursConfig.name

router = DefaultRouter()
router.register("tours", TourViewSet, basename="tours")
router.register("stocks", TourStockViewSet, basename="tours_stocks")


urlpatterns = [
    path(
        "tours/searches/",
        TourSearchView.as_view({"get": "search"}),
        name="tour-searches",
    ),
    path(
        "tours/filters/",
        TourFiltersView.as_view({"get": "filters"}),
        name="tour-filters",
    ),
] + router.urls
