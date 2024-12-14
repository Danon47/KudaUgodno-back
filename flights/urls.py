from django.urls import path

from flights.apps import FlightsConfig
from flights.views import (
    FlightCreateAPIView,
    FlightRetrieveAPIView,
    FlightDestroyAPIView, FlightListAPIView,
)

app_name = FlightsConfig.name

urlpatterns = [
    path("flights/create/", FlightCreateAPIView.as_view(), name="flight-create"),
    path("flights/", FlightListAPIView.as_view(), name="flights-list"),
    path("flights/<int:pk>/", FlightRetrieveAPIView.as_view(), name="flight-detail"),
    path(
        "flights/<int:pk>/update/", FlightRetrieveAPIView.as_view(), name="flight-update"
    ),
    path(
        "flights/<int:pk>/delete/", FlightDestroyAPIView.as_view(), name="flight-delete"
    ),
]
