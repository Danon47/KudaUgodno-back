from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from flights.models import Flight
from flights.serializers import FlightSerializer


class FlightCreateAPIView(CreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightListAPIView(ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightRetrieveAPIView(RetrieveAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightUpdateAPIView(UpdateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightDestroyAPIView(DestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

