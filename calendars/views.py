from rest_framework import viewsets

from all_fixture.pagination import CustomLOPagination
from calendars.models import CalendarDate
from calendars.serializers import CalendarDateSerializer


class PriceCalendarViewSet(viewsets.ModelViewSet):
    queryset = CalendarDate.objects.all()
    serializer_class = CalendarDateSerializer
    pagination_class = CustomLOPagination
