from django.urls import path

from flights.apps import FlightsConfig
from flights.views import (
    FlightCreateAPIView,
    FlightRetrieveAPIView,
    FlightDestroyAPIView,
    FlightListAPIView,
    FlightUpdateAPIView,
)

app_name = FlightsConfig.name

urlpatterns = [
    path("create/", FlightCreateAPIView.as_view(), name="flight-create"),
    path("", FlightListAPIView.as_view(), name="flights-list"),
    path("<int:pk>/", FlightRetrieveAPIView.as_view(), name="flight-detail"),
    path("<int:pk>/update/", FlightUpdateAPIView.as_view(), name="flight-update"),
    path("<int:pk>/delete/", FlightDestroyAPIView.as_view(), name="flight-delete"),
]
