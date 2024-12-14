from django.urls import path

from flights.apps import FlightsConfig
from flights.views import (
    FlightListCreateView, FlightDetailView,
)

app_name = FlightsConfig.name

urlpatterns = [
    path("", FlightListCreateView.as_view(), name="flight-list-create"),
    path("<int:pk>/", FlightDetailView.as_view(), name="flight-detail"),
]
