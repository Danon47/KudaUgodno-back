from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from all_fixture.pagination import CustomLOPagination
from hotels.models import Hotel
from rooms.models import PriceCalendar
from rooms.serializer_price_calendar import PriceCalendarSerializer


class PriceCalendarViewSet(viewsets.ModelViewSet):
    queryset = PriceCalendar.objects.none()
    serializer_class = PriceCalendarSerializer
    pagination_class = CustomLOPagination

    def get_queryset(self):
        hotel_id = self.kwargs.get("hotel_id")
        return PriceCalendar.objects.filter(hotel_id=hotel_id)

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get("hotel_id")
        hotel = get_object_or_404(Hotel, id=hotel_id)
        serializer.save(hotel=hotel)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["hotel_id"] = self.kwargs.get("hotel_id")
        return context
